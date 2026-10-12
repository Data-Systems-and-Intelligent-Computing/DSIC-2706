"""Read-only provenance and completeness audit for a completed E4 run.

The source E4 directory is never modified.  The audit result is written to a
separate timestamped directory under ``results/reproductions``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RUN_DEFAULT = ROOT / "results" / "reproductions" / "E4_5sites_20261011T213404_350219Z"
BACKUP_DEFAULT = Path(r"C:\Users\Fabio\Documents\TA_E4_Backups\E4_5sites_20261011T213404_350219Z.zip")
REPRESENTATIONS = ("R0", "R1", "R2", "R3")
EXPECTED_QUERIES = 311
EXPECTED_CONDITIONS_PER_REP = 80
EXPECTED_RAW_ROWS_PER_REP = 25_191


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_fingerprint(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def audit(run: Path, backup: Path | None) -> Path:
    run = run.resolve()
    identity_path = run / "run_identity.json"
    if not identity_path.is_file():
        raise FileNotFoundError(identity_path)
    envelope = json.loads(identity_path.read_text(encoding="utf-8"))
    identity = envelope.get("identity")
    if not isinstance(identity, dict) or envelope.get("sha256") != json_fingerprint(identity):
        raise ValueError("E4 run identity checksum is invalid.")

    asset_results = []
    for name, detail in identity["assets"].items():
        asset = ROOT / detail["path"]
        actual = sha256_file(asset) if asset.is_file() else None
        asset_results.append({
            "asset": name, "path": detail["path"], "expected_sha256": detail["sha256"],
            "actual_sha256": actual, "status": "PASS" if actual == detail["sha256"] else "FAIL",
        })

    condition_rows = []
    aggregate_rows = []
    for rep in REPRESENTATIONS:
        paths = sorted((run / "raw" / f"E4_{rep}_conditions").glob("repeat_*/*.csv"))
        if len(paths) != EXPECTED_CONDITIONS_PER_REP:
            raise ValueError(f"{rep} has {len(paths)} condition files, expected {EXPECTED_CONDITIONS_PER_REP}.")
        for path in paths:
            frame = pd.read_csv(path, low_memory=False)
            required = {"query_id", "species_key", "max_score", "top1_match", "snr_db", "snr_db_achieved"}
            missing = sorted(required.difference(frame.columns))
            if len(frame) != EXPECTED_QUERIES or missing:
                raise ValueError(f"Invalid E4 condition {path}: rows={len(frame)}, missing={missing}")
            if frame["query_id"].duplicated().any() or not np.isfinite(frame["max_score"].to_numpy(dtype=float)).all():
                raise ValueError(f"Invalid query IDs or scores in {path}")
            if not np.isfinite(frame.loc[frame["condition"].ne("Clean"), "snr_db_achieved"].to_numpy(dtype=float)).all():
                raise ValueError(f"Invalid achieved SNR in {path}")
            condition_rows.append({"representation": rep, "path": str(path.relative_to(run)).replace("\\", "/"), "rows": len(frame), "status": "PASS"})
        aggregate = pd.read_csv(run / "raw" / f"E4_{rep}_raw.csv", low_memory=False)
        aggregate_rows.append({
            "representation": rep, "rows": len(aggregate),
            "unique_keys": int(not aggregate.duplicated(["query_id", "habitat", "snr_db", "repeat_id"]).any()),
            "finite_max_score": int(np.isfinite(aggregate["max_score"].to_numpy(dtype=float)).all()),
            "has_top1_identity": int({"top1_species_key", "top1_recording_id"}.issubset(aggregate.columns)),
            "status": "PASS" if len(aggregate) == EXPECTED_RAW_ROWS_PER_REP else "FAIL",
        })

    table = pd.read_csv(run / "tables" / "e4_domain_shift_table.csv")
    if len(table) != 324 or table.duplicated(["representation", "repeat_id", "habitat", "condition", "snr_db"]).any():
        raise ValueError("E4 aggregate table is incomplete or has duplicate condition keys.")
    backup_report: dict[str, object] = {"path": None, "status": "NOT_CHECKED"}
    if backup is not None and backup.is_file():
        with zipfile.ZipFile(backup) as archive:
            corrupt = archive.testzip()
            backup_report = {"path": str(backup), "entries": len(archive.infolist()), "status": "PASS" if corrupt is None else "FAIL", "first_corrupt_entry": corrupt}

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    output = ROOT / "results" / "reproductions" / f"E4_audit_{timestamp}"
    output.mkdir(parents=True, exist_ok=False)
    (output / "tables").mkdir()
    pd.DataFrame(asset_results).to_csv(output / "tables" / "asset_provenance.csv", index=False)
    pd.DataFrame(condition_rows).to_csv(output / "tables" / "condition_inventory.csv", index=False)
    pd.DataFrame(aggregate_rows).to_csv(output / "tables" / "raw_inventory.csv", index=False)
    report = {
        "schema": "e4_read_only_audit_v1", "status": "PASS_WITH_E5_FIELD_LIMITATION",
        "source_run": str(run.relative_to(ROOT)).replace("\\", "/"),
        "source_run_identity_sha256": envelope["sha256"],
        "asset_provenance_pass": all(row["status"] == "PASS" for row in asset_results),
        "condition_files": len(condition_rows), "aggregate_table_rows": int(len(table)),
        "backup": backup_report,
        "e5_limitation": "Raw E4 stores max_score and top1_match, but not Top-1 species/recording nor true-class and best-other scores. These values must remain unavailable unless reconstructed deterministically from valid source embeddings and exact mixing provenance.",
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    (output / "validation_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    (output / "README.md").write_text(
        "# E4 read-only audit\n\n"
        "This companion artifact validates provenance and completeness of the referenced E4 run. "
        "It does not alter E4 source files and does not rerun E4.\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit an E4 run without modifying it.")
    parser.add_argument("--run", type=Path, default=RUN_DEFAULT)
    parser.add_argument("--backup", type=Path, default=BACKUP_DEFAULT)
    arguments = parser.parse_args()
    audit(arguments.run, arguments.backup)
