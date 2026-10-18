"""
Unit Test: Verifikasi Integritas Manifes (M-06) dan Dimensi Model (C-01)
"""

import hashlib
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def test_manifest_sha256_integrity():
    """Memverifikasi bahwa hash aktual dataset_split.csv cocok dengan rekam jejak audit (M-06)."""
    split_csv = PROJECT_ROOT / "data/manifests/dataset_split.csv"
    manifest_txt = PROJECT_ROOT / "artifacts/reproducibility/manifest_sha256.txt"
    
    assert split_csv.exists(), f"File {split_csv} tidak ditemukan!"
    assert manifest_txt.exists(), f"File {manifest_txt} tidak ditemukan!"
    
    # Hitung hash aktual dengan normalisasi LF lintas platform
    content_bytes = split_csv.read_bytes().replace(b"\r\n", b"\n")
    actual_hash = hashlib.sha256(content_bytes).hexdigest()
    
    # Baca hash tercatat
    content = manifest_txt.read_text(encoding="utf-8")
    assert actual_hash in content, f"Hash aktual dataset_split.csv ({actual_hash}) tidak cocok dengan catatan di {manifest_txt}!"

def check_model_embedding_dimension(code):
    """One representation is one reported test; missing inputs are explicit skips."""
    from unittest import SkipTest
    try:
        from src.embeddings import AudioRepresentationExtractor
        extractor = AudioRepresentationExtractor(code)
        embedding = extractor.extract(np.zeros(160000, dtype=np.float32), item_id="unit-test")
    except (FileNotFoundError, ImportError, ModuleNotFoundError) as error:
        raise SkipTest(f"{code}: checkpoint/dependensi tidak tersedia: {error}") from error
    expected = {"R0": 40, "R1": 2048, "R2": 1024, "R3": 40}
    assert embedding.shape == (expected[code],), f"Dimensi {code} tidak sesuai: {embedding.shape}"
    assert np.isfinite(embedding).all(), f"Embedding {code} tidak finite"


import unittest
class ModelEmbeddingDimensionTests(unittest.TestCase):
    def test_r0_dimension(self):
        check_model_embedding_dimension("R0")
    def test_r1_dimension(self):
        check_model_embedding_dimension("R1")
    def test_r2_dimension(self):
        check_model_embedding_dimension("R2")
    def test_r3_dimension(self):
        check_model_embedding_dimension("R3")
