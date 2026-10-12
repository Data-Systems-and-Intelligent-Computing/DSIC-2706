"""Materialize the current RQ/H matrix without altering the historical statistics run."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL = ROOT / "results/tables/23_statistics_rq_hypothesis_matrix.csv"
H3 = ROOT / "results/tables/24_h3_habitat_profile_stability.csv"
OUTPUT = ROOT / "results/tables/27_rq_hypothesis_matrix_current.csv"

matrix = pd.read_csv(HISTORICAL)
summary = pd.read_csv(H3)
row = summary.loc[summary.analysis_scope.eq("mean_over_4_SNR_levels")].iloc[0]
mask = matrix["item"].eq("H3")
if mask.sum() != 1:
    raise RuntimeError("Expected exactly one H3 row in the historical matrix")
matrix.loc[mask, "experiment"] = "E4 raw + H3 analysis"
matrix.loc[mask, "metric"] = "mAP@10 relative-retention swing across five habitat profiles"
matrix.loc[mask, "artifact"] = "24_h3_habitat_profile_stability.csv; 26_h3_bootstrap_distribution.csv"
matrix.loc[mask, "result"] = (
    f"R1 swing {row['R1_generic_mean_swing']:.6f}; R2 swing {row['R2_bioacoustic_mean_swing']:.6f}; "
    f"Δ={row['R1_minus_R2_effect']:.6f}; CI 95% [{row['ci95_low']:.6f}, {row['ci95_high']:.6f}]."
)
matrix.loc[mask, "conclusion"] = "Supported for retention stability"
matrix.loc[mask, "limitation"] = "Exploratory analysis added after E4; high/low-frequency distortion mechanism and in-situ bird soundscapes were not tested."
subrq3 = matrix["item"].eq("Sub-RQ 3")
subrq4 = matrix["item"].eq("Sub-RQ 4")
if subrq3.sum() != 1 or subrq4.sum() != 1:
    raise RuntimeError("Expected exactly one row for each active Sub-RQ 3 and 4")
matrix.loc[subrq3, ["experiment", "metric", "artifact", "result", "conclusion", "limitation"]] = [
    "E4/H3",
    "habitat-conditioned mAP@10 and relative-retention swing",
    "14_e4_domain_shift.csv; 24_h3_habitat_profile_stability.csv",
    "Five ITERA noise-location profiles compared at matched SNR; R2 has a narrower retention swing than R1.",
    "Answered within additive field-noise mixtures",
    "Spectral frequency mechanism and in-situ bird recordings are not directly tested.",
]
matrix.loc[subrq4, ["experiment", "metric", "artifact", "result", "conclusion", "limitation"]] = [
    "E5",
    "failure mode, threshold margin, and available acoustic diagnostics",
    "15_e5_failure_mode_summary.csv; 16_e5_selected_case_manifest.csv",
    "E5 reports false rejection, confusion, collapse, and available spectral diagnostics.",
    "Answered as controlled diagnostics",
    "Fields absent from E4 raw outputs remain unavailable.",
]
matrix.to_csv(OUTPUT, index=False)
sha256 = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
metadata = {
    "artifact": OUTPUT.relative_to(ROOT).as_posix(),
    "kind": "current RQ/H matrix derived from historical statistics plus H3 analysis",
    "sources": {
        HISTORICAL.relative_to(ROOT).as_posix(): sha256(HISTORICAL),
        H3.relative_to(ROOT).as_posix(): sha256(H3),
    },
    "sha256": sha256(OUTPUT),
    "historical_matrix_policy": "Original statistics run and table 23 are preserved unchanged.",
}
OUTPUT.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
print(OUTPUT)
