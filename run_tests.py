"""
Script: run_tests.py
Fungsi: Menjalankan seluruh unit test saintifik Tugas Akhir DSIC27-06 tanpa dependensi eksternal.
Mencakup:
1. Zero Data Leakage (ID, Filepath, dan Recordist-Disjoint Global)
2. Akurasi Controlled SNR Noise Mixing (Paired Noise)
3. Sifat Matematika Cosine Similarity & Ranking Logic
4. Pembekuan Threshold Kalibrasi Open-Set (tau freeze)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.integration.test_split_leakage import (
    test_zero_leakage_between_gallery_and_query,
    test_zero_filepath_leakage,
    test_zero_recordist_leakage_global,
)
from tests.unit.test_snr_mixing import test_snr_mixing_accuracy
from tests.unit.test_cosine import (
    test_cosine_similarity_properties,
    test_retrieval_ranking_logic,
)
from tests.unit.test_threshold_freeze import test_threshold_frozen_evaluation


def run_all_tests():
    print("=" * 80)
    print("[*] MENJALANKAN SUITE PENGUJIAN SAINTIFIK DSIC27-06")
    print("=" * 80)

    tests = [
        ("Zero Recording ID Overlap", test_zero_leakage_between_gallery_and_query),
        ("Zero File Path Overlap", test_zero_filepath_leakage),
        ("Strict Global Recordist-Disjoint (Zero Recordist Overlap)", test_zero_recordist_leakage_global),
        ("SNR Controlled Mixing Accuracy", test_snr_mixing_accuracy),
        ("Cosine Similarity Mathematical Bounds", test_cosine_similarity_properties),
        ("Retrieval Ranking & Metric Logic", test_retrieval_ranking_logic),
        ("Open-Set Threshold Freeze Validation", test_threshold_frozen_evaluation),
    ]

    passed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"  [PASS] {name}")
            passed += 1
        except AssertionError as e:
            print(f"  [FAIL] {name} -> {e}")
        except Exception as e:
            print(f"  [ERROR] {name} -> {e}")

    print("=" * 80)
    print(f"[+] HASIL: {passed}/{len(tests)} Pengujian Lolos ({passed/len(tests)*100:.1f}%)")
    print("=" * 80)
    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
