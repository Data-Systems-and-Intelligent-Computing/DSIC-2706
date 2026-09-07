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
    
    # Hitung hash aktual
    h = hashlib.sha256()
    with open(split_csv, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    actual_hash = h.hexdigest()
    
    # Baca hash tercatat
    content = manifest_txt.read_text(encoding="utf-8")
    assert actual_hash in content, f"Hash aktual dataset_split.csv ({actual_hash}) tidak cocok dengan catatan di {manifest_txt}!"

def test_model_embedding_dimensions():
    """Memverifikasi dimensi embedding asli R0=40, R1=2048, R2=1024, R3=40 (C-01)."""
    from src.embeddings import AudioRepresentationExtractor
    
    test_signal = np.zeros(160000, dtype=np.float32)
    expected = {"R0": 40, "R1": 2048, "R2": 1024, "R3": 40}
    
    for code, dim in expected.items():
        ext = AudioRepresentationExtractor(code)
        emb = ext.extract(test_signal)
        assert emb.shape == (dim,), f"Model {code} menghasilkan dimensi {emb.shape}, diharapkan ({dim},)!"
