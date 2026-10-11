"""
Unit Test: tests/unit/test_raw_split_alignment.py
Deskripsi: Memverifikasi keselarasan 100% antara kueri di berkas mentah results/raw/
           dengan query_clean di dataset_split.csv, serta integritas baris data kalibrasi E3.
"""

import unittest
from pathlib import Path
import pandas as pd
import glob

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RAW_DIR = PROJECT_ROOT / "results/raw"
SPLIT_CSV = PROJECT_ROOT / "data/manifests/dataset_split.csv"
CALIB_CSV = RAW_DIR / "E3_calibration_scores_raw.csv"

class TestRawSplitAlignment(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SPLIT_CSV.exists(), "dataset_split.csv harus ada")
        self.split_df = pd.read_csv(SPLIT_CSV)
        self.query_ids = set(self.split_df[self.split_df["split_role"] == "query_clean"]["recording_id"])
        self.assertEqual(len(self.query_ids), 311, "Harus ada tepat 311 kueri di query_clean")

    def test_retrieval_raw_query_ids_match_split(self):
        """Kueri di 20 berkas retrieval mentah harus identik dengan query_clean di split."""
        retrieval_files = list(RAW_DIR.glob("R*_raw.csv")) + list(RAW_DIR.glob("R*_*_raw.csv"))
        self.assertGreaterEqual(len(retrieval_files), 20, "Harus ada minimal 20 berkas retrieval mentah")
        
        for f in retrieval_files:
            if "E4" in f.name:
                continue
            df = pd.read_csv(f)
            self.assertIn("query_id", df.columns, f"Kolom query_id harus ada di {f.name}")
            raw_ids = set(df["query_id"])
            diff = self.query_ids ^ raw_ids
            self.assertEqual(diff, set(), f"Kueri di {f.name} tidak selaras dengan split: {diff}")
            self.assertEqual(len(df), 311, f"Jumlah baris di {f.name} harus tepat 311")

    def test_e4_habitat_raw_query_ids_match_split(self):
        """Kueri di berkas mentah E4 habitat harus selaras dengan query_clean di split."""
        e4_files = list(RAW_DIR.glob("E4_R*_raw.csv"))
        self.assertEqual(len(e4_files), 4, "Harus ada 4 berkas E4_R*_raw.csv")
        for f in e4_files:
            df = pd.read_csv(f)
            raw_ids = set(df["query_id"])
            diff = self.query_ids ^ raw_ids
            self.assertEqual(diff, set(), f"Kueri di {f.name} tidak selaras dengan split")

    def test_calibration_raw_row_counts(self):
        """Baris kalibrasi E3 harus tepat 465 baris per representasi (232 positif, 233 negatif)."""
        self.assertTrue(CALIB_CSV.exists(), "E3_calibration_scores_raw.csv harus ada")
        df = pd.read_csv(CALIB_CSV)
        
        for rep in ["R0", "R1", "R2", "R3"]:
            sub = df[df["representation"] == rep]
            n_pos = len(sub[sub["ground_truth"] == 1])
            n_neg = len(sub[sub["ground_truth"] == 0])
            self.assertEqual(n_pos, 232, f"Positif kalibrasi {rep} harus tepat 232")
            self.assertEqual(n_neg, 233, f"Negatif kalibrasi {rep} harus tepat 233")
            self.assertEqual(len(sub), 465, f"Total kalibrasi {rep} harus tepat 465")
        
        self.assertEqual(len(df), 465 * 4, "Total baris seluruh representasi harus 1.860")


def test_retrieval_raw_query_ids_match_split():
    case = TestRawSplitAlignment()
    case.setUp()
    case.test_retrieval_raw_query_ids_match_split()


def test_e4_habitat_raw_query_ids_match_split():
    case = TestRawSplitAlignment()
    case.setUp()
    case.test_e4_habitat_raw_query_ids_match_split()


def test_calibration_raw_row_counts():
    case = TestRawSplitAlignment()
    case.setUp()
    case.test_calibration_raw_row_counts()


if __name__ == "__main__":
    unittest.main()
