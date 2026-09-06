"""
Script: src/mfcc.py
Fungsi: Ekstraksi Representasi Baseline R0 (MFCC + Temporal Pooling + Cosine Distance).
Sesuai:
- Katalog DSIC27-06: Baseline wajib MFCC dengan jarak kosinus.
- Davis & Mermelstein (1980): Parametric speech/audio representations.
- Audit Bab 10.1 & 12: Embedding dibentuk dari statistik temporal (mean dan std)
  dari setiap koefisien MFCC agar menghasilkan representasi berdimensi tetap (40-dim).
"""

import os
import sys
import numpy as np
import librosa

try:
    from src.preprocess import preprocess_audio, TARGET_SR
except ImportError:
    from preprocess import preprocess_audio, TARGET_SR


def extract_mfcc_representation(y: np.ndarray, sr: int = TARGET_SR, n_mfcc: int = 20) -> np.ndarray:
    """
    Mengekstrak fitur MFCC (20 koefisien) dan melakukan temporal pooling (mean + std).
    Menghasilkan vektor representasi berdimensi 40.
    """
    # Ekstraksi MFCC
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_fft=1024, hop_length=512)

    # Pooling temporal
    mean = np.mean(mfcc, axis=1)  # shape: (n_mfcc,)
    std = np.std(mfcc, axis=1)    # shape: (n_mfcc,)

    # Penggabungan mean dan std
    emb = np.concatenate([mean, std])  # shape: (40,)

    # L2 Normalization untuk komputasi cosine yang stabil
    norm = np.linalg.norm(emb)
    if norm > 1e-8:
        emb = emb / norm

    return emb.astype(np.float32)


def extract_mfcc_from_file(file_path: str, sr: int = TARGET_SR) -> np.ndarray:
    """Helper untuk memproses berkas audio langsung menjadi vektor MFCC 40-dim."""
    y = preprocess_audio(file_path, target_sr=sr)
    return extract_mfcc_representation(y, sr=sr)


def cosine_similarity(e1: np.ndarray, e2: np.ndarray) -> float:
    """Menghitung cosine similarity antara dua vektor embedding."""
    norm1 = np.linalg.norm(e1)
    norm2 = np.linalg.norm(e2)
    if norm1 < 1e-8 or norm2 < 1e-8:
        return 0.0
    return float(np.dot(e1, e2) / (norm1 * norm2))


def batch_cosine_similarity(query_emb: np.ndarray, gallery_embs: np.ndarray) -> np.ndarray:
    """
    Menghitung kemiripan kosinus antara 1 vektor query (D,) dan matriks gallery (N, D).
    Kembalian berupa array 1D berisi skor kemiripan untuk seluruh item gallery.
    """
    q_norm = np.linalg.norm(query_emb)
    g_norms = np.linalg.norm(gallery_embs, axis=1)
    
    # Hindari pembagian dengan nol
    denom = q_norm * g_norms
    denom[denom < 1e-8] = 1e-8
    
    scores = np.dot(gallery_embs, query_emb) / denom
    return scores


if __name__ == "__main__":
    print("[*] Menguji ekstraksi MFCC baseline...")
    dummy_signal = np.random.randn(160000).astype(np.float32)
    dummy_emb = extract_mfcc_representation(dummy_signal, sr=32000)
    print(f"[+] Dimensi embedding MFCC: {dummy_emb.shape} (Ekspektasi: (40,))")
    print(f"[+] L2 Norm: {np.linalg.norm(dummy_emb):.4f}")
    assert dummy_emb.shape == (40,), "Dimensi embedding MFCC harus 40!"
    print("[+] Test sukses!")
