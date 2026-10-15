"""Run E5 diagnostic failure taxonomy from validated E2/E3/E4 artifacts."""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

os.environ["MPLBACKEND"] = "Agg"
import librosa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.mix_noise import mix_audio_at_snr
from src.preprocess import preprocess_audio, TARGET_SR

MANIFEST = ROOT / "data/manifests/dataset_split.csv"
REPS = ("R0", "R1", "R2", "R3")


def atomic_json(path: Path, value: object) -> None:
    temp = path.with_name(path.name + ".tmp")
    if path.exists() or temp.exists(): raise FileExistsError(path)
    with temp.open("xb") as f:
        f.write((json.dumps(value, indent=2, allow_nan=False) + "\n").encode()); f.flush(); os.fsync(f.fileno())
    temp.replace(path)


def mode(top1: pd.Series, score: pd.Series, tau: pd.Series) -> pd.Series:
    return np.select(
        [top1.eq(1) & score.ge(tau), top1.eq(1) & score.lt(tau), top1.eq(0) & score.ge(tau)],
        ["Accepted correct", "Open-set false rejection", "Top-1 confusion above threshold"],
        default="Total retrieval collapse",
    )


def select_failure_cases(failures: pd.DataFrame) -> pd.DataFrame:
    """Sample existing E2 failure rows without dropping group-label columns.

    Explicit group iteration preserves representation/condition/failure_mode
    across pandas versions and keeps the historical within-group sampling seed.
    """
    subset = failures.loc[failures.source_experiment.eq("E2")]
    if subset.empty:
        return subset.copy()
    groups = subset.groupby(["representation", "condition", "failure_mode"], sort=True)
    return pd.concat(
        [group.sample(n=min(2, len(group)), random_state=20261012) for _, group in groups],
        ignore_index=True,
    )


def acoustics(y: np.ndarray) -> dict[str, float]:
    return {"spectral_centroid_hz": float(np.mean(librosa.feature.spectral_centroid(y=y, sr=TARGET_SR))),
            "spectral_bandwidth_hz": float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=TARGET_SR))),
            "mean_rms": float(np.mean(librosa.feature.rms(y=y)))}


def e2_features(e2: Path, queries: pd.DataFrame) -> pd.DataFrame:
    """Reconstruct physical E2 mixtures once per query/condition and verify audit identity."""
    reference = pd.read_csv(e2 / "raw" / "R0_Clean.csv", low_memory=False)
    rows = []
    for condition in ["Clean", "SNR_20dB", "SNR_10dB", "SNR_0dB", "SNR_-5dB"]:
        source = reference if condition == "Clean" else pd.read_csv(e2 / "raw" / f"R0_{condition}.csv", low_memory=False)
        for i, (_, item) in enumerate(source.iterrows()):
            if str(item.query_id) != str(queries.iloc[i].recording_id):
                raise ValueError(f"E2 query ordering differs from active manifest at row {i}: {item.query_id}")
            clean = preprocess_audio(str(queries.iloc[i].file_path))
            if condition == "Clean":
                y = clean
            else:
                y, audit = mix_audio_at_snr(clean, float(item.snr_db), seed=int(item.noise_seed), return_audit_info=True)
                if audit["noise_file"] != item.noise_file or not np.isclose(audit["snr_db_achieved"], item.snr_db_achieved, atol=1e-6):
                    raise ValueError(f"E2 mixture audit mismatch: {item.query_id} {condition}")
            row = {"query_id": str(item.query_id), "condition": condition, "acoustic_status": "reconstructed_verified"}
            row.update(acoustics(y)); rows.append(row)
        print(f"E5 acoustic {condition}: {len(source)}/{len(source)}", flush=True)
    return pd.DataFrame(rows)


def main(e2: Path, e3: Path, e4: Path) -> Path:
    e2, e3, e4 = e2.resolve(), e3.resolve(), e4.resolve()
    if json.loads((e2 / "metadata.json").read_text()).get("status") != "complete": raise ValueError("E2 incomplete")
    if json.loads((e3 / "metadata.json").read_text()).get("status") != "complete": raise ValueError("E3 incomplete")
    thresholds = pd.read_csv(e3 / "tables" / "frozen_thresholds.csv")[["representation", "frozen_tau"]]
    queries = pd.read_csv(MANIFEST).query("split_role == 'query_clean'").reset_index(drop=True)
    output = ROOT / "results" / "reproductions" / f"E5_diagnostics_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')}"
    (output / "tables").mkdir(parents=True); (output / "figures").mkdir()

    feature_table = e2_features(e2, queries)
    e2_frames = []
    for rep in REPS:
        for name in ["Clean", "SNR_20dB", "SNR_10dB", "SNR_0dB", "SNR_-5dB"]:
            f = pd.read_csv(e2 / "raw" / f"{rep}_{name}.csv", low_memory=False)
            f["source_experiment"] = "E2"; e2_frames.append(f)
    known_e2 = pd.concat(e2_frames, ignore_index=True).merge(thresholds, on="representation", validate="many_to_one")
    known_e2["failure_mode"] = mode(known_e2.top1_match, known_e2.max_score, known_e2.frozen_tau)
    known_e2 = known_e2.merge(feature_table, on=["query_id", "condition"], validate="many_to_one")
    known_e2["threshold_margin"] = known_e2["max_score"] - known_e2["frozen_tau"]
    known_e2["top1_identity_status"] = "available"

    e4_frames = []
    for rep in REPS:
        f = pd.read_csv(e4 / "raw" / f"E4_{rep}_raw.csv", low_memory=False)
        f["source_experiment"] = "E4"; e4_frames.append(f)
    known_e4 = pd.concat(e4_frames, ignore_index=True).merge(thresholds, on="representation", validate="many_to_one")
    known_e4["failure_mode"] = mode(known_e4.top1_match, known_e4.max_score, known_e4.frozen_tau)
    known_e4["threshold_margin"] = known_e4["max_score"] - known_e4["frozen_tau"]
    for col in ["top1_recording_id", "top1_species_key", "true_class_max_similarity", "best_other_similarity", "true_vs_other_margin", "spectral_centroid_hz", "spectral_bandwidth_hz", "mean_rms"]: known_e4[col] = np.nan
    known_e4["acoustic_status"] = "not_reconstructed_e4_source_lacks_ranking_and_noisy_audio"
    known_e4["top1_identity_status"] = "not_available_in_e4_raw"
    for col in known_e2.columns:
        if col not in known_e4: known_e4[col] = np.nan
    known = pd.concat([known_e2, known_e4[known_e2.columns]], ignore_index=True)
    failures = known[known.failure_mode.ne("Accepted correct")].copy()
    summary = known.groupby(["source_experiment", "representation", "condition", "failure_mode"], dropna=False).size().reset_index(name="n_queries")

    unknown = pd.read_csv(e3 / "raw" / "test_scores.csv")
    unknown = unknown[unknown.target_type.eq("unknown_control")].copy()
    unknown["open_set_outcome"] = np.where(unknown.predicted_accept.eq(1), "False accept", "Correct reject")
    selected = select_failure_cases(failures)

    known.to_csv(output / "tables" / "all_query_diagnostics.csv", index=False)
    failures.to_csv(output / "tables" / "failure_cases.csv", index=False)
    summary.to_csv(output / "tables" / "failure_mode_summary.csv", index=False)
    selected.to_csv(output / "tables" / "selected_case_manifest.csv", index=False)
    unknown.to_csv(output / "tables" / "unknown_open_set_diagnostics.csv", index=False)
    plt.figure(figsize=(10,5)); pivot=summary.groupby(["representation","failure_mode"]).n_queries.sum().unstack(fill_value=0); pivot.plot(kind="bar", stacked=True, ax=plt.gca()); plt.tight_layout(); plt.savefig(output / "figures" / "failure_modes_by_representation.png", dpi=180); plt.close()
    plt.figure(figsize=(9,5)); known_e2.boxplot(column="threshold_margin", by="failure_mode", rot=25); plt.suptitle(""); plt.title("Score margin above/below frozen threshold"); plt.tight_layout(); plt.savefig(output / "figures" / "margin_distribution_by_failure_type.png", dpi=180); plt.close()
    plt.figure(figsize=(9,5)); known_e2.boxplot(column="spectral_centroid_hz", by="failure_mode", rot=25); plt.tight_layout(); plt.savefig(output / "figures" / "spectral_features_by_failure_type.png", dpi=180); plt.close()
    report={"status":"PASS_WITH_E4_FIELD_LIMITATION","e2_known_rows":int(len(known_e2)),"e4_known_rows":int(len(known_e4)),"unknown_rows":int(len(unknown)),"selected_cases":int(len(selected)),"e4_limitation":"Top-1 identity, class margins, and acoustic features are unavailable in E4 raw and not inferred."}
    atomic_json(output / "validation_report.json", report)
    atomic_json(output / "metadata.json", {"status":"complete","artifact_schema":"e5_diagnostics_v1","created_utc":datetime.now(timezone.utc).isoformat(),"e2":str(e2.relative_to(ROOT)),"e3":str(e3.relative_to(ROOT)),"e4":str(e4.relative_to(ROOT)),"threshold_source":"E3 frozen_thresholds.csv","e4_diagnostic_limitation":report["e4_limitation"]})
    (output / "README.md").write_text("# E5 diagnostic analysis\n\nE2 mixtures are reconstructed and verified before acoustic features are measured. E4 failure modes use verified `top1_match` and `max_score`; missing ranking fields remain unavailable.\n",encoding="utf-8")
    print(output)
    return output

if __name__ == "__main__":
    p=argparse.ArgumentParser(); p.add_argument("--e2",type=Path,required=True); p.add_argument("--e3",type=Path,required=True); p.add_argument("--e4",type=Path,required=True); a=p.parse_args(); main(a.e2,a.e3,a.e4)
