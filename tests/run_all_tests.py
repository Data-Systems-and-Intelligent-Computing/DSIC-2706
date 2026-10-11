"""
Master Test Runner: tests/run_all_tests.py
Menjalankan seluruh unit test dan asersi saintifik DSIC-2706
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.test_split_leakage import (
    test_zero_leakage_between_gallery_and_query,
    test_zero_filepath_leakage,
    test_zero_recordist_leakage_global
)
from tests.test_cosine import test_cosine_similarity_properties
from tests.test_snr_mixing import (
    test_snr_mixing_accuracy,
    test_snr_mixing_reproducibility
)
from tests.test_threshold_freeze import test_threshold_frozen_evaluation
from tests.unit.test_manuscript_table_consistency import (
    test_clean_retrieval_consistency,
    test_snr_robustness_consistency,
    test_threshold_transfer_e3_consistency,
    test_e4_habitat_sensitivity_consistency,
    test_bootstrap_significance_consistency,
    test_text_claims_integrity,
)
from tests.unit.test_manifest_and_models import test_model_embedding_dimensions
from tests.unit.test_raw_split_alignment import (
    test_retrieval_raw_query_ids_match_split,
    test_calibration_raw_row_counts,
)

def main():
    print("=" * 70)
    print("=== MENJALANKAN SUITE UJI INTEGRITAS SAINTIFIK (DSIC-2706) ===")
    print("=" * 70)
    
    tests = [
        ("Zero ID Leakage (Gallery vs Query vs Calibration)", test_zero_leakage_between_gallery_and_query),
        ("Zero Filepath Leakage Across All Splits", test_zero_filepath_leakage),
        ("Strict Global Recordist-Disjoint (0 Author Overlap)", test_zero_recordist_leakage_global),
        ("Raw Query IDs Match dataset_split.csv Exactly (311 queries)", test_retrieval_raw_query_ids_match_split),
        ("Calibration Raw Rows Integrity (465 rows per model)", test_calibration_raw_row_counts),
        ("Cosine Similarity Math Properties (Range & Symmetry)", test_cosine_similarity_properties),
        ("SNR Mixing Math Precision (Energy Scaling)", test_snr_mixing_accuracy),
        ("Deterministic Mixing Reproducibility (Fixed Seed)", test_snr_mixing_reproducibility),
        ("Frozen Threshold tau Invariance", test_threshold_frozen_evaluation),
        ("Model Latent Embedding Dimensions (C-01)", test_model_embedding_dimensions),
        ("Manuscript Table Consistency: Clean E1", test_clean_retrieval_consistency),
        ("Manuscript Table Consistency: SNR Robustness E2", test_snr_robustness_consistency),
        ("Manuscript Table Consistency: Threshold Transfer E3", test_threshold_transfer_e3_consistency),
        ("Manuscript Table Consistency: Habitat Sensitivity E4", test_e4_habitat_sensitivity_consistency),
        ("Manuscript Table Consistency: Bootstrap Significance", test_bootstrap_significance_consistency),
        ("Manuscript Text Claims & Hypothesis Integrity", test_text_claims_integrity),
    ]

    passed = 0
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  [PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")

    print("=" * 70)
    print(f"[+] HASIL: {passed}/{len(tests)} Pengujian Lolos ({passed/len(tests)*100:.1f}%)")
    print("=" * 70)

    if passed != len(tests):
        sys.exit(1)

if __name__ == "__main__":
    main()
