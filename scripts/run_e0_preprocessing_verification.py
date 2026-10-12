"""Run the formal E0 preprocessing audit without writing to the paper.

E0 is a deterministic 100-recording audit of the active Indonesia split. It
is not a retrieval experiment. Every output is self-contained beneath
``results/reproductions/E0_<UTC timestamp>``.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / "results" / ".mplconfig"))
os.environ["MPLBACKEND"] = "Agg"

import librosa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import soundfile as sf

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.embeddings import AudioRepresentationExtractor
from src.preprocess import DURATION_SEC, TARGET_RMS, TARGET_SAMPLES, TARGET_SR, compute_rms, preprocess_audio

MANIFEST_PATH = PROJECT_ROOT / "data" / "manifests" / "dataset_split.csv"
OUTPUT_ROOT = PROJECT_ROOT / "results" / "reproductions"
SAMPLE_SEED = 20261012
SAMPLE_SIZE = 100


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_sha() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def select_window_start(resampled_mono: np.ndarray) -> int:
    """Return the exact start index used by the current preprocessing algorithm."""
    if len(resampled_mono) <= TARGET_SAMPLES:
        return 0
    hop = TARGET_SAMPLES // 4
    count = max(1, (len(resampled_mono) - TARGET_SAMPLES) // hop + 1)
    rms_values = [compute_rms(resampled_mono[i * hop : i * hop + TARGET_SAMPLES]) for i in range(count)]
    return int(np.argmax(rms_values) * hop)


def deterministic_sample(manifest: pd.DataFrame) -> pd.DataFrame:
    if len(manifest) < SAMPLE_SIZE:
        raise ValueError(f"Active manifest has only {len(manifest)} rows; E0 needs {SAMPLE_SIZE}.")
    pieces: list[pd.DataFrame] = []
    remaining = SAMPLE_SIZE
    roles = [(role, group.reset_index(drop=True)) for role, group in manifest.groupby("split_role", sort=True)]
    for index, (_, group) in enumerate(roles):
        take = round(SAMPLE_SIZE * len(group) / len(manifest)) if index < len(roles) - 1 else remaining
        take = min(take, len(group))
        remaining -= take
        pieces.append(group.sample(n=take, random_state=SAMPLE_SEED + index))
    sample = pd.concat(pieces, ignore_index=True)
    if len(sample) != SAMPLE_SIZE:
        raise AssertionError(f"Internal E0 sampling error: {len(sample)} rows selected.")
    return sample.sort_values(["split_role", "recording_id"]).reset_index(drop=True)


def inspect_recording(row: pd.Series) -> dict[str, object]:
    path = PROJECT_ROOT / str(row["file_path"])
    try:
        info = sf.info(path)
        container, subtype = info.format, info.subtype
        sr_native, channels, duration_native = int(info.samplerate), int(info.channels), float(info.duration)
        soundfile_error = ""
    except RuntimeError as error:
        container, subtype, sr_native, channels, duration_native, soundfile_error = "UNREADABLE_BY_SOUNDFILE", "", np.nan, np.nan, np.nan, str(error)
    decoded, _ = librosa.load(path, sr=TARGET_SR, mono=True)
    start_sample = select_window_start(decoded)
    processed = preprocess_audio(str(path))
    expected_container = path.suffix.removeprefix(".").upper()
    mismatch = bool(container not in {expected_container, "MPEG" if expected_container == "MP3" else expected_container})
    return {
        "recording_id": row["recording_id"], "species_key": row["species_key"], "split_role": row["split_role"],
        "file_path": row["file_path"], "extension": path.suffix.lower(), "container": container, "subtype": subtype,
        "extension_container_mismatch": mismatch, "soundfile_error": soundfile_error,
        "native_sample_rate_hz": sr_native, "native_channels": channels, "native_duration_seconds": duration_native,
        "decoded_sample_rate_hz": TARGET_SR, "decoded_samples_before_window": int(len(decoded)),
        "selected_window_start_sample": start_sample, "selected_window_start_seconds": start_sample / TARGET_SR,
        "selected_window_duration_seconds": DURATION_SEC, "processed_samples": int(len(processed)),
        "processed_sample_rate_hz": TARGET_SR, "processed_rms": compute_rms(processed),
        "processed_peak": float(np.max(np.abs(processed))), "preprocess_length_ok": bool(len(processed) == TARGET_SAMPLES),
        "preprocess_finite_ok": bool(np.isfinite(processed).all()),
    }


def make_plots(audit: pd.DataFrame, figures_dir: Path) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 8))
    audit["native_duration_seconds"].dropna().plot.hist(bins=24, ax=axes[0, 0], color="#356f9b")
    axes[0, 0].set(title="Native duration", xlabel="seconds")
    audit["native_sample_rate_hz"].dropna().value_counts().sort_index().plot.bar(ax=axes[0, 1], color="#5a9d6f")
    axes[0, 1].set(title="Native sampling rate", xlabel="Hz")
    audit["selected_window_start_seconds"].plot.hist(bins=24, ax=axes[1, 0], color="#a36c3e")
    axes[1, 0].set(title="Selected 5-second window start", xlabel="seconds")
    audit["container"].value_counts().plot.bar(ax=axes[1, 1], color="#86589c")
    axes[1, 1].set(title="Decoded container", xlabel="container")
    fig.suptitle("E0 formal preprocessing audit (100 deterministic active-split recordings)")
    fig.tight_layout()
    fig.savefig(figures_dir / "e0_audio_properties.png", dpi=180)
    plt.close(fig)


def main() -> Path:
    manifest = pd.read_csv(MANIFEST_PATH)
    sample = deterministic_sample(manifest)
    now = datetime.now(timezone.utc)
    output_dir = OUTPUT_ROOT / f"E0_{now.strftime('%Y%m%d_%H%M%S')}"
    output_dir.mkdir(parents=True, exist_ok=False)
    tables_dir = output_dir / "tables"
    figures_dir = output_dir / "figures"
    tables_dir.mkdir()
    figures_dir.mkdir()
    print(f"E0 formal: auditing {len(sample)} active recordings; output: {output_dir}")
    records = []
    for position, (_, row) in enumerate(sample.iterrows(), start=1):
        records.append(inspect_recording(row))
        if position % 10 == 0 or position == len(sample):
            print(f"E0 audio audit: {position}/{len(sample)}", flush=True)
    audit = pd.DataFrame(records)
    audit.to_csv(tables_dir / "per_recording.csv", index=False)
    probe_row = sample.iloc[0]
    probe_audio = preprocess_audio(str(PROJECT_ROOT / probe_row["file_path"]))
    probes = []
    for code, dimension in (("R0", 40), ("R1", 2048), ("R2", 1024), ("R3", 40)):
        embedding = AudioRepresentationExtractor(code).extract(probe_audio, item_id=f"e0_probe:{probe_row['recording_id']}")
        probes.append({"representation": code, "expected_dimension": dimension, "actual_dimension": int(embedding.size), "finite": bool(np.isfinite(embedding).all()), "l2_norm": float(np.linalg.norm(embedding))})
    pd.DataFrame(probes).to_csv(tables_dir / "representation_probe.csv", index=False)
    summary = pd.DataFrame([
        {"metric": "audit_rows", "value": len(audit)}, {"metric": "unique_species", "value": int(audit["species_key"].nunique())},
        {"metric": "native_duration_min_seconds", "value": float(audit["native_duration_seconds"].min())},
        {"metric": "native_duration_median_seconds", "value": float(audit["native_duration_seconds"].median())},
        {"metric": "native_duration_max_seconds", "value": float(audit["native_duration_seconds"].max())},
        {"metric": "extension_container_mismatches", "value": int(audit["extension_container_mismatch"].sum())},
        {"metric": "soundfile_decode_errors", "value": int(audit["soundfile_error"].ne("").sum())},
        {"metric": "preprocess_length_failures", "value": int((~audit["preprocess_length_ok"]).sum())},
        {"metric": "preprocess_nonfinite_failures", "value": int((~audit["preprocess_finite_ok"]).sum())},
        {"metric": "target_rms", "value": TARGET_RMS},
    ])
    summary.to_csv(tables_dir / "summary.csv", index=False)
    make_plots(audit, figures_dir)
    metadata = {
        "artifact_schema": "e0_preprocessing_audit_v1", "status": "complete", "timestamp_utc": now.isoformat(),
        "git_sha": git_sha(), "manifest_sha256": sha256_file(MANIFEST_PATH),
        "preprocess_code_sha256": sha256_file(PROJECT_ROOT / "src" / "preprocess.py"),
        "sample_seed": SAMPLE_SEED, "sample_size": SAMPLE_SIZE,
        "sample_roles": {str(k): int(v) for k, v in sample["split_role"].value_counts().sort_index().items()},
        "protocol": {"target_sample_rate_hz": TARGET_SR, "target_samples": TARGET_SAMPLES, "selected_window_seconds": DURATION_SEC, "target_rms": TARGET_RMS},
        "representation_probe_recording_id": str(probe_row["recording_id"]),
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (output_dir / "README.md").write_text(
        "# E0 — Audit pra-pemrosesan\n\n"
        "- `tables/summary.csv`: ringkasan audit.\n"
        "- `tables/per_recording.csv`: detail 100 rekaman.\n"
        "- `tables/representation_probe.csv`: cek R0–R3.\n"
        "- `figures/e0_audio_properties.png`: gambar audit.\n",
        encoding="utf-8",
    )
    print(f"E0 complete: {output_dir}")
    return output_dir


if __name__ == "__main__":
    main()
