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

def main():
    print("=" * 70)
    print("=== MENJALANKAN SUITE UJI INTEGRITAS SAINTIFIK (DSIC-2706) ===")
    print("=" * 70)
    
    tests = [
        ("Zero ID Leakage (Gallery vs Query vs Calibration)", test_zero_leakage_between_gallery_and_query),
        ("Zero Filepath Leakage Across All Splits", test_zero_filepath_leakage),
        ("Strict Global Recordist-Disjoint (0 Author Overlap)", test_zero_recordist_leakage_global),
        ("Cosine Similarity Math Properties (Range & Symmetry)", test_cosine_similarity_properties),
        ("SNR Mixing Math Precision (Energy Scaling)", test_snr_mixing_accuracy),
        ("Deterministic Mixing Reproducibility (Fixed Seed)", test_snr_mixing_reproducibility),
        ("Frozen Threshold tau Invariance", test_threshold_frozen_evaluation),
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
