"""Build direct, code-cell-only notebooks for preprocessing, E0, EDA, and E1."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / "notebooks"


def make_cell(source: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source}


def write(name: str, cells: list[str]) -> None:
    payload = {"nbformat": 4, "nbformat_minor": 5,
               "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}},
               "cells": [make_cell(source) for source in cells]}
    (NOTEBOOKS / name).write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


SETUP = r'''from pathlib import Path
import os
import sys

ROOT = Path.cwd()
if not (ROOT / "data" / "manifests").exists():
    ROOT = Path(r"D:\\FILE AND TASK\\TA")
assert (ROOT / "data" / "manifests").exists(), ROOT
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.environ["MPLBACKEND"] = "Agg"

try:
    from IPython.display import display
except ImportError:
    def display(item):
        print(item)

import json
import numpy as np
import pandas as pd
import librosa
import matplotlib.pyplot as plt

print("Project:", ROOT)
print("Python:", sys.executable)
print("NumPy:", np.__version__)
print("Pandas:", pd.__version__)
print("Librosa:", librosa.__version__)
'''


def main() -> None:
    write("01_Preprocessing.ipynb", [SETUP, r'''from src.preprocess import TARGET_SR, TARGET_SAMPLES, DURATION_SEC, compute_rms, preprocess_audio

files = [
    ROOT / "data/xeno_canto_indonesia/savnig1/XC42472.mp3",
    ROOT / "data/xeno_canto_indonesia/savnig1/XC120964.mp3",
    ROOT / "data/xeno_canto_indonesia/ashtai1/XC1003648.mp3",
]
records = []
for path in files:
    audio = preprocess_audio(str(path))
    records.append({"file": path.name, "samples": len(audio), "sampling_rate_hz": TARGET_SR, "duration_seconds": len(audio) / TARGET_SR, "rms": compute_rms(audio), "finite": bool(np.isfinite(audio).all())})
result = pd.DataFrame(records)
display(result)
assert (result.samples == TARGET_SAMPLES).all()
print("Preprocessing: decode -> mono -> 32 kHz -> selected 5 seconds -> RMS normalization.")
print("Ini tahap persiapan audio. R0 berbeda: R0 adalah representasi MFCC yang memakai audio hasil preprocessing.")
'''])
    write("02_E0_Preprocessing_Audit.ipynb", [SETUP, r'''run = ROOT / "results/reproductions/E0_20261011_202557"
assert run.is_dir(), run
metadata = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
print(json.dumps(metadata, ensure_ascii=False, indent=2))
summary = pd.read_csv(run / "tables/summary.csv")
probe = pd.read_csv(run / "tables/representation_probe.csv")
per_recording = pd.read_csv(run / "tables/per_recording.csv")
display(summary)
display(probe)
print("E0 memeriksa 100 rekaman aktif secara deterministik. E0 adalah audit preprocessing dan bukan evaluasi retrieval.")
''', r'''fig = plt.imread(run / "figures/e0_audio_properties.png")
plt.figure(figsize=(13, 8))
plt.imshow(fig)
plt.axis("off")
plt.show()
display(per_recording.head(20))
print("Seluruh 100 baris audit tersedia di:", run / "tables/per_recording.csv")
'''])
    write("03_EDA_Physical_Audio.ipynb", [SETUP, r'''run = ROOT / "results/reproductions/EDA_20261011_202714"
assert run.is_dir(), run
inventory = pd.read_csv(run / "tables/physical_audio_inventory.csv")
split = pd.read_csv(ROOT / "data/manifests/dataset_split.csv")
unknown = pd.read_csv(ROOT / "data/manifests/unknown_open_set_manifest.csv")
noise_manifest = pd.read_csv(ROOT / "data/manifests/itera_noise_manifest.csv")
print(json.dumps(json.loads((run / "metadata.json").read_text(encoding="utf-8")), ensure_ascii=False, indent=2))
display(pd.read_csv(run / "tables/summary_by_source.csv"))
display(pd.read_csv(run / "tables/target_species_summary.csv"))
display(pd.read_csv(run / "tables/noise_location_summary.csv"))
''', r'''fig, axes = plt.subplots(2, 2, figsize=(15, 10))
split.groupby("species_key").size().sort_values().plot.barh(ax=axes[0, 0], color="#356f9b")
axes[0, 0].set_title("Jumlah rekaman target per spesies")
axes[0, 0].set_xlabel("rekaman")
inventory.groupby("source")["duration_seconds"].median().sort_values().plot.bar(ax=axes[0, 1], color="#5a9d6f")
axes[0, 1].set_title("Median durasi menurut sumber")
axes[0, 1].set_ylabel("detik")
inventory["sample_rate_hz"].dropna().astype(int).value_counts().sort_index().plot.bar(ax=axes[1, 0], color="#a36c3e")
axes[1, 0].set_title("Distribusi sampling rate fisik")
axes[1, 0].set_xlabel("Hz")
noise_locations = inventory.loc[inventory.source.eq("noise"), "noise_location"].replace("", "unclassified").value_counts().head(12)
noise_locations.plot.bar(ax=axes[1, 1], color="#86589c")
axes[1, 1].set_title("Rekaman noise ITERA menurut lokasi/folder")
axes[1, 1].tick_params(axis="x", rotation=35)
fig.suptitle("EDA fisik: target Indonesia, unknown buffer, dan noise ITERA")
fig.tight_layout()
display(fig)
plt.close(fig)
''', r'''examples = [
    ("Query XC42472", ROOT / "data/xeno_canto_indonesia/savnig1/XC42472.mp3"),
    ("Gallery relevan XC120964", ROOT / "data/xeno_canto_indonesia/savnig1/XC120964.mp3"),
    ("Noise ITERA", ROOT / "data/itera_noise" / str(noise_manifest.iloc[0]["filename"])),
]
fig, axes = plt.subplots(len(examples), 2, figsize=(15, 10))
for row, (label, path) in enumerate(examples):
    audio, sr = librosa.load(str(path), sr=32000, mono=True, duration=5.0)
    time = np.arange(len(audio)) / sr
    axes[row, 0].plot(time, audio, linewidth=0.45, color="#356f9b")
    axes[row, 0].set(title=f"Waveform — {label}", xlabel="detik", ylabel="amplitudo")
    mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=1024, hop_length=320, n_mels=80, fmax=16000)
    image = axes[row, 1].imshow(librosa.power_to_db(mel, ref=np.max), origin="lower", aspect="auto", cmap="magma", extent=[0, len(audio) / sr, 0, 16000])
    axes[row, 1].set(title=f"Mel-spectrogram — {label}", xlabel="detik", ylabel="Hz")
    fig.colorbar(image, ax=axes[row, 1], label="dB")
fig.tight_layout()
display(fig)
plt.close(fig)
print("Figur dibuat langsung oleh cell ini dari audio fisik dan tidak disimpan/ditimpa ke results.")
''', r'''format_issues = inventory.loc[inventory.extension_container_mismatch, ["file_path", "extension", "container", "sample_rate_hz", "duration_seconds"]]
display(format_issues.head(50))
print("Jumlah mismatch ekstensi/container:", len(format_issues))
print("Inventaris lengkap:", run / "tables/physical_audio_inventory.csv")
'''])
    write("04_E1_Clean_R0.ipynb", [SETUP, r'''runs = {
    "R0": ROOT / "results/reproductions/E1_R0_20261011_175321",
    "R1": ROOT / "results/reproductions/E1_R1_cache_20261012T021032_566409Z",
    "R2": ROOT / "results/reproductions/E1_R2_cache_20261012T021034_128124Z",
    "R3": ROOT / "results/reproductions/E1_R3_cache_20261012T021035_119528Z",
}
summary_rows = []
for representation, run in runs.items():
    assert run.is_dir(), run
    metadata = json.loads((run / "metadata.json").read_text(encoding="utf-8"))
    summary_rows.append({"representation": representation, **metadata["summary"]})
summary = pd.DataFrame(summary_rows).sort_values("representation")
display(summary)
print("E1 adalah retrieval bersih. R0 adalah MFCC, yaitu representasi baseline setelah preprocessing; bukan preprocessing itu sendiri.")
''', r'''fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
summary.plot.bar(x="representation", y="mAP@10", ax=axes[0], legend=False, color="#356f9b", title="E1 Clean mAP@10")
summary.plot.bar(x="representation", y="mean_top1", ax=axes[1], legend=False, color="#5a9d6f", title="E1 Clean Top-1 accuracy")
for axis in axes:
    axis.set_ylim(0, 1)
    axis.set_xlabel("representasi")
fig.tight_layout()
display(fig)
plt.close(fig)
''', r'''r0_per_query = pd.read_csv(runs["R0"] / "tables/per_query.csv")
display(r0_per_query.head(30))
print("R0 per-query lengkap:", runs["R0"] / "tables/per_query.csv")
print("R1--R3 per-query lengkap tersedia pada notebook 05_E1_Clean_R0_R3.ipynb.")
'''])
    print("Updated direct notebooks 01--04.")


if __name__ == "__main__":
    main()
