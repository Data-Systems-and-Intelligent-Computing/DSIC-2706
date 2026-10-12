"""Build code-only read-only notebooks for validated E1--E5 and RQ/H evidence."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / "notebooks"


def code(source: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source}


def write(name: str, cells: list[str]) -> None:
    notebook = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}},
        "cells": [code(value) for value in cells],
    }
    (NOTEBOOKS / name).write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


SETUP = r'''from pathlib import Path
import csv
import json
try:
    from IPython.display import Image, display
except ImportError:
    class Image:
        def __init__(self, filename):
            self.filename = filename
    def display(item):
        print("Gambar:", item.filename)

ROOT = Path.cwd()
if not (ROOT / "results" / "reproductions").exists():
    ROOT = Path(r"D:\\FILE AND TASK\\TA")
assert (ROOT / "results" / "reproductions").exists(), ROOT

def run_exact(name):
    path = ROOT / "results" / "reproductions" / name
    assert path.is_dir(), path
    return path

def show_json(path):
    print(path)
    print(json.dumps(json.loads(path.read_text(encoding="utf-8")), ensure_ascii=False, indent=2))

def show_csv(path, limit=200):
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    print(f"{path} | {len(rows)} baris")
    if not rows:
        return
    keys = list(rows[0])
    shown = rows if len(rows) <= limit else rows[:limit // 2] + rows[-limit // 2:]
    widths = {key: min(34, max(len(key), *(len(str(row.get(key, ""))) for row in shown))) for key in keys}
    print(" | ".join(key[:widths[key]].ljust(widths[key]) for key in keys))
    print("-+-".join("-" * widths[key] for key in keys))
    for row in shown:
        print(" | ".join(str(row.get(key, ""))[:widths[key]].ljust(widths[key]) for key in keys))
    if len(rows) > limit:
        print(f"... {len(shown)} dari {len(rows)} baris ditampilkan; CSV lengkap tetap berada di path di atas.")
'''


def main() -> None:
    write("05_E1_Clean_R0_R3.ipynb", [SETUP, r'''runs = {
    "R0": run_exact("E1_R0_20261011_175321"),
    "R1": run_exact("E1_R1_cache_20261012T021032_566409Z"),
    "R2": run_exact("E1_R2_cache_20261012T021034_128124Z"),
    "R3": run_exact("E1_R3_cache_20261012T021035_119528Z"),
}
for rep, path in runs.items():
    print("=" * 80, rep)
    metadata = json.loads((path / "metadata.json").read_text(encoding="utf-8"))
    print(json.dumps({key: metadata.get(key) for key in ("status", "representation", "experiment", "summary", "cache_provenance")}, ensure_ascii=False, indent=2))
''', r'''for rep, path in runs.items():
    print("=" * 80, rep, "per-query retrieval")
    show_csv(path / "tables" / "per_query.csv", limit=20)
'''])
    write("06_E2_Controlled_Noise.ipynb", [SETUP, r'''run = run_exact("E2_controlled_20261012T021600_897497Z")
show_json(run / "validation_report.json")
show_json(run / "metadata.json")
''', r'''show_csv(run / "tables" / "e2_snr_robustness.csv")
display(Image(filename=str(run / "figures" / "e2_snr_robustness_map10.png")))
''', r'''print("Contoh metrik per-query dan audit pencampuran; 20 CSV lengkap:", run / "raw")
for name in ("R0_Clean.csv", "R1_SNR_-5dB.csv", "R2_SNR_-5dB.csv", "R3_SNR_-5dB.csv"):
    show_csv(run / "raw" / name, limit=10)
'''])
    write("07_E3_Open_Set_Threshold.ipynb", [SETUP, r'''run = run_exact("E3_open_set_20261012T022548_802536Z")
show_json(run / "validation_report.json")
show_json(run / "metadata.json")
''', r'''show_csv(run / "tables" / "frozen_thresholds.csv")
show_csv(run / "tables" / "threshold_transfer.csv")
display(Image(filename=str(run / "figures" / "e3_threshold_transfer_recall.png")))
''', r'''show_csv(run / "raw" / "calibration_scores.csv", limit=20)
show_csv(run / "raw" / "test_scores.csv", limit=20)
'''])
    write("08_E4_Habitat_Noise_Sensitivity.ipynb", [SETUP, r'''run = run_exact("E4_5sites_20261011T213404_350219Z")
audit = run_exact("E4_audit_20261012T021801_989259Z")
show_json(run / "run_identity.json")
show_json(audit / "validation_report.json")
''', r'''show_csv(run / "processed" / "e4_domain_shift_table.csv")
for figure in sorted((run / "figures").glob("*.png")):
    print(figure.name)
    display(Image(filename=str(figure)))
''', r'''print("E4 raw menyimpan max_score dan top1_match, tetapi tidak menyimpan identitas Top-1, margin kelas, atau fitur akustik noisy.")
show_csv(run / "raw" / "E4_R2_raw.csv", limit=12)
'''])
    write("09_E5_Failure_Diagnostics.ipynb", [SETUP, r'''run = run_exact("E5_diagnostics_20261012T091512_868500Z")
show_json(run / "validation_report.json")
show_json(run / "metadata.json")
''', r'''for name in ("failure_mode_summary.csv", "selected_case_manifest.csv", "unknown_open_set_diagnostics.csv"):
    show_csv(run / "tables" / name, limit=150)
''', r'''for name in ("failure_modes_by_representation.png", "margin_distribution_by_failure_type.png", "spectral_features_by_failure_type.png"):
    display(Image(filename=str(run / "figures" / name)))
print("Semua per-query:", run / "tables" / "all_query_diagnostics.csv")
print("Semua kegagalan:", run / "tables" / "failure_cases.csv")
'''])
    print("Created E1--E5 result notebooks.")


if __name__ == "__main__":
    main()
