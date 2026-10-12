"""Create a formal, manifest-led EDA inventory without touching the manuscript.

The prior EDA notebook contained output from a former dataset/regime. This
script supersedes it and writes an inspectable physical-audio inventory and
plots to one timestamped reproduction directory.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / "results" / ".mplconfig"))
os.environ["MPLBACKEND"] = "Agg"

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import soundfile as sf

MANIFEST_DIR = PROJECT_ROOT / "data" / "manifests"
OUTPUT_ROOT = PROJECT_ROOT / "results" / "reproductions"
AUDIO_SUFFIXES = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_sha() -> str | None:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def normal_path(value: str) -> str:
    return Path(value).as_posix().lower()


def physical_inventory() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    split = pd.read_csv(MANIFEST_DIR / "dataset_split.csv")
    unknown = pd.read_csv(MANIFEST_DIR / "unknown_open_set_manifest.csv")
    noise = pd.read_csv(MANIFEST_DIR / "itera_noise_manifest.csv")
    references: dict[str, dict[str, object]] = {}
    for _, row in noise.iterrows():
        parts = Path(str(row.filename)).parts
        references[normal_path(str(Path("data/itera_noise") / row.filename))] = {
            "source": "noise", "role": "verified_bird_free" if bool(row.verified_bird_free) else "mixing_pool",
            "species_key": "", "noise_location": parts[0] if len(parts) > 1 else "unclassified",
        }
    for _, row in split.iterrows():
        references[normal_path(row.file_path)] = {"source": "target", "role": row.split_role, "species_key": row.species_key, "noise_location": ""}
    for _, row in unknown.iterrows():
        category = str(row.source_category)
        references[normal_path(row.file_path)] = {
            "source": "noise_e3_reserved" if category == "itera_environmental_noise" else "unknown_bird",
            "role": row.split_role, "species_key": row.source_label,
            "noise_location": Path(str(row.file_path)).parts[2] if category == "itera_environmental_noise" and len(Path(str(row.file_path)).parts) > 3 else "",
        }

    roots = ("data/xeno_canto_indonesia", "data/xeno_canto_indonesia_unknowns", "data/itera_noise")
    audio_files = [p for root in roots for p in (PROJECT_ROOT / root).rglob("*") if p.is_file() and p.suffix.lower() in AUDIO_SUFFIXES]
    records: list[dict[str, object]] = []
    for number, path in enumerate(sorted(audio_files), start=1):
        relative = path.relative_to(PROJECT_ROOT).as_posix()
        reference = references.get(normal_path(relative), {"source": "unreferenced", "role": "", "species_key": "", "noise_location": ""})
        try:
            info = sf.info(path)
            values = {"container": info.format, "subtype": info.subtype, "sample_rate_hz": int(info.samplerate), "channels": int(info.channels), "duration_seconds": float(info.duration), "decode_error": ""}
        except RuntimeError as error:
            values = {"container": "UNREADABLE_BY_SOUNDFILE", "subtype": "", "sample_rate_hz": np.nan, "channels": np.nan, "duration_seconds": np.nan, "decode_error": str(error)}
        expected = path.suffix.removeprefix(".").upper()
        mismatch = values["container"] not in {expected, "MPEG" if expected == "MP3" else expected}
        records.append({"file_path": relative, "extension": path.suffix.lower(), "extension_container_mismatch": mismatch, **reference, **values})
        if number % 250 == 0 or number == len(audio_files):
            print(f"EDA physical audio: {number}/{len(audio_files)}", flush=True)
    return pd.DataFrame(records), split, unknown, noise


def make_plots(inventory: pd.DataFrame, split: pd.DataFrame, figures_dir: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 9))
    split.groupby("species_key").size().sort_values().plot.barh(ax=axes[0, 0], color="#356f9b")
    axes[0, 0].set(title="Active target recordings by species", xlabel="recordings")
    inventory.groupby("source")["duration_seconds"].median().sort_values().plot.bar(ax=axes[0, 1], color="#5a9d6f")
    axes[0, 1].set(title="Median duration by source", ylabel="seconds")
    inventory["sample_rate_hz"].dropna().astype(int).value_counts().sort_index().plot.bar(ax=axes[1, 0], color="#a36c3e")
    axes[1, 0].set(title="Physical sample-rate distribution", xlabel="Hz")
    noise = inventory.loc[inventory["source"].eq("noise")]
    noise["noise_location"].replace("", "unclassified").value_counts().head(12).plot.bar(ax=axes[1, 1], color="#86589c")
    axes[1, 1].set(title="ITERA noise recordings by folder/location", xlabel="location")
    fig.suptitle("Formal EDA: active Indonesian target, unknown buffer, and ITERA noise")
    fig.tight_layout()
    fig.savefig(figures_dir / "eda_overview.png", dpi=180)
    plt.close(fig)


def main() -> Path:
    now = datetime.now(timezone.utc)
    output_dir = OUTPUT_ROOT / f"EDA_{now.strftime('%Y%m%d_%H%M%S')}"
    output_dir.mkdir(parents=True, exist_ok=False)
    tables_dir = output_dir / "tables"
    figures_dir = output_dir / "figures"
    tables_dir.mkdir()
    figures_dir.mkdir()
    inventory, split, unknown, noise = physical_inventory()
    inventory.to_csv(tables_dir / "physical_audio_inventory.csv", index=False)
    grouped = inventory.groupby(["source", "role"], dropna=False).size().rename("count").reset_index()
    durations = inventory.groupby("source")["duration_seconds"].agg(["min", "median", "max"]).reset_index()
    grouped.merge(durations, on="source", how="left").to_csv(tables_dir / "summary_by_source.csv", index=False)
    species = split.groupby(["species_key", "scientific_name", "common_name"], dropna=False).agg(recordings=("recording_id", "count"), recordists=("author", "nunique"), median_rating=("rating", "median")).reset_index().sort_values("species_key")
    species.to_csv(tables_dir / "target_species_summary.csv", index=False)
    inventory.loc[inventory.source.eq("noise")].groupby("noise_location").size().rename("recordings").reset_index().sort_values("recordings", ascending=False).to_csv(tables_dir / "noise_location_summary.csv", index=False)
    make_plots(inventory, split, figures_dir)
    metadata = {
        "artifact_schema": "eda_physical_inventory_v1", "status": "complete", "timestamp_utc": now.isoformat(), "git_sha": git_sha(),
        "manifest_sha256": {name: sha256_file(MANIFEST_DIR / name) for name in ("dataset_split.csv", "unknown_open_set_manifest.csv", "itera_noise_manifest.csv")},
        "physical_audio_count": int(len(inventory)), "manifest_target_count": int(len(split)),
        "manifest_open_set_rows": int(len(unknown)),
        "manifest_unknown_bird_rows": int((unknown.source_category == "non_target_species").sum()),
        "manifest_e3_reserved_noise_rows": int((unknown.source_category == "itera_environmental_noise").sum()),
        "manifest_noise_count": int(len(noise)),
        "soundfile_decode_errors": int(inventory.decode_error.ne("").sum()), "extension_container_mismatches": int(inventory.extension_container_mismatch.sum()), "unreferenced_physical_audio": int(inventory.source.eq("unreferenced").sum()),
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (output_dir / "README.md").write_text(
        "# EDA — Inventaris audio fisik\n\n"
        "- `tables/physical_audio_inventory.csv`: detail setiap audio.\n"
        "- `tables/summary_by_source.csv`: ringkasan sumber.\n"
        "- `tables/target_species_summary.csv`: ringkasan spesies.\n"
        "- `tables/noise_location_summary.csv`: lokasi noise.\n"
        "- `figures/eda_overview.png`: gambar EDA.\n",
        encoding="utf-8",
    )
    print(f"EDA complete: {output_dir}")
    return output_dir


if __name__ == "__main__":
    main()
