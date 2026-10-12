"""Consolidate one direct-code Jupyter notebook per E1--E5 experiment."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / "notebooks"
SCRIPTS = ROOT / "scripts"


def cell(source: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source}


def write(name: str, cells: list[str]) -> None:
    data = {"nbformat": 4, "nbformat_minor": 5,
            "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}},
            "cells": [cell(value) for value in cells]}
    (NOTEBOOKS / name).write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def inline_script(filename: str) -> str:
    """Embed the current runner source but suppress its CLI entry point."""
    source = (SCRIPTS / filename).read_text(encoding="utf-8-sig")
    source = source.replace("from __future__ import annotations\n", "")
    source = re.split(r"\nif __name__ == [\"']__main__[\"']:\s*", source, maxsplit=1)[0].rstrip()
    return f'''# Kode eksperimen berasal dari scripts/{filename} dan ditempatkan langsung di notebook ini.
# Tidak ada pemanggilan subprocess atau eksekusi file runner eksternal.
# Entry point CLI sengaja tidak dipanggil otomatis agar artefak valid tidak tertimpa.
__file__ = str(ROOT / "scripts" / "{filename}")

{source}

print("Kode {filename} telah dimuat di notebook. Jalankan fungsi eksperimen hanya jika memang ingin membuat run baru.")
'''


SETUP = r'''from pathlib import Path
import os
import sys
import json
import csv

ROOT = Path.cwd()
if not (ROOT / "data" / "manifests").exists():
    ROOT = Path(r"D:\\FILE AND TASK\\TA")
assert (ROOT / "data" / "manifests").exists(), ROOT
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.environ["MPLBACKEND"] = "Agg"

try:
    from IPython.display import display, Image
except ImportError:
    def display(item): print(item)
    class Image:
        def __init__(self, filename): self.filename = filename

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print("Project:", ROOT)
print("Kernel:", sys.executable)


def show_json(path):
    print(path)
    print(json.dumps(json.loads(path.read_text(encoding="utf-8")), ensure_ascii=False, indent=2))


def show_csv(path, rows=30):
    frame = pd.read_csv(path, low_memory=False)
    print(path, "|", len(frame), "baris")
    display(frame if len(frame) <= rows else pd.concat([frame.head(rows // 2), frame.tail(rows // 2)]))
    if len(frame) > rows:
        print("Tampilan adalah sampel; CSV lengkap tetap berada di path di atas.")
    return frame
'''


def main() -> None:
    e1_results = r'''runs = {
    "R0": ROOT / "results/reproductions/E1_R0_20261011_175321",
    "R1": ROOT / "results/reproductions/E1_R1_cache_20261012T021032_566409Z",
    "R2": ROOT / "results/reproductions/E1_R2_cache_20261012T021034_128124Z",
    "R3": ROOT / "results/reproductions/E1_R3_cache_20261012T021035_119528Z",
}
summary_rows = []
for representation, path in runs.items():
    metadata = json.loads((path / "metadata.json").read_text(encoding="utf-8"))
    summary_rows.append({"representation": representation, **metadata["summary"]})
summary = pd.DataFrame(summary_rows).sort_values("representation")
display(summary)
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
summary.plot.bar(x="representation", y="mAP@10", ax=axes[0], legend=False, color="#356f9b", title="E1 Clean mAP@10")
summary.plot.bar(x="representation", y="mean_top1", ax=axes[1], legend=False, color="#5a9d6f", title="E1 Clean Top-1 accuracy")
for axis in axes: axis.set_ylim(0, 1)
fig.tight_layout(); display(fig); plt.close(fig)
for representation, path in runs.items():
    show_csv(path / "tables" / "per_query.csv", rows=20)
print("R0 adalah MFCC baseline. Preprocessing adalah tahap terpisah pada notebook 01.")
'''
    e2_results = r'''run = ROOT / "results/reproductions/E2_controlled_20261012T021600_897497Z"
show_json(run / "validation_report.json")
show_json(run / "metadata.json")
show_csv(run / "tables/e2_snr_robustness.csv")
display(Image(filename=str(run / "figures/e2_snr_robustness_map10.png")))
for name in ("R0_Clean.csv", "R1_SNR_-5dB.csv", "R2_SNR_-5dB.csv", "R3_SNR_-5dB.csv"):
    show_csv(run / "raw" / name, rows=12)
print("Semua 20 raw CSV per kondisi berada di:", run / "raw")
'''
    e3_results = r'''run = ROOT / "results/reproductions/E3_open_set_20261012T022548_802536Z"
show_json(run / "validation_report.json")
show_json(run / "metadata.json")
show_csv(run / "tables/frozen_thresholds.csv")
show_csv(run / "tables/threshold_transfer.csv")
display(Image(filename=str(run / "figures/e3_threshold_transfer_recall.png")))
show_csv(run / "raw/calibration_scores.csv", rows=20)
show_csv(run / "raw/test_scores.csv", rows=20)
'''
    e4_results = r'''run = ROOT / "results/reproductions/E4_5sites_20261011T213404_350219Z"
audit = ROOT / "results/reproductions/E4_audit_20261012T021801_989259Z"
show_json(run / "run_identity.json")
show_json(audit / "validation_report.json")
show_csv(run / "processed/e4_domain_shift_table.csv", rows=80)
for figure in sorted((run / "figures").glob("*.png")):
    print(figure.name)
    display(Image(filename=str(figure)))
show_csv(run / "raw/E4_R2_raw.csv", rows=12)
print("E4 raw menyediakan top1_match dan max_score, tetapi identitas Top-1, margin kelas, dan fitur noisy tidak tersedia.")
'''
    e5_results = r'''run = ROOT / "results/reproductions/E5_diagnostics_20261012T091512_868500Z"
show_json(run / "validation_report.json")
show_json(run / "metadata.json")
show_csv(run / "tables/failure_mode_summary.csv", rows=200)
show_csv(run / "tables/selected_case_manifest.csv", rows=120)
show_csv(run / "tables/unknown_open_set_diagnostics.csv", rows=30)
for name in ("failure_modes_by_representation.png", "margin_distribution_by_failure_type.png", "spectral_features_by_failure_type.png"):
    display(Image(filename=str(run / "figures" / name)))
print("Seluruh diagnostik per-query:", run / "tables/all_query_diagnostics.csv")
print("Seluruh kasus kegagalan:", run / "tables/failure_cases.csv")
'''

    write("04_E1_Clean_Retrieval.ipynb", [SETUP, inline_script("run_e1_clean_r0.py"), inline_script("materialize_e1_from_cache.py"), e1_results])
    write("05_E2_Controlled_Noise.ipynb", [SETUP, inline_script("run_e2_controlled_noise.py"), e2_results])
    write("06_E3_Open_Set_Threshold.ipynb", [SETUP, inline_script("run_e3_open_set.py"), e3_results])
    write("07_E4_Habitat_Noise_Sensitivity.ipynb", [SETUP, inline_script("run_e4_five_locations_v10_stage7.py.draft"), e4_results])
    write("08_E5_Failure_Diagnostics.ipynb", [SETUP, inline_script("run_e5_diagnostics.py"), e5_results])
    print("Consolidated direct-code notebooks E1--E5.")


if __name__ == "__main__":
    main()
