import numpy as np
import librosa


def extract_mfcc_representation(y: np.ndarray, sr: int = 32000, n_mfcc: int = 20) -> np.ndarray:
    """Ekstraksi MFCC dengan temporal pooling (mean + std) -> 40 dimensi."""
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_fft=1024, hop_length=512)
    mfcc_mean = np.mean(mfcc, axis=1)
    mfcc_std = np.std(mfcc, axis=1)
    vector = np.concatenate([mfcc_mean, mfcc_std])
    norm = np.linalg.norm(vector)
    if norm > 1e-7:
        vector = vector / norm
    return vector.astype(np.float32)


def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    dot = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 < 1e-7 or norm2 < 1e-7:
        return 0.0
    return float(np.clip(dot / (norm1 * norm2), -1.0, 1.0))


def batch_cosine_similarity(query_vec: np.ndarray, gallery_matrix: np.ndarray) -> np.ndarray:
    q_norm = np.linalg.norm(query_vec)
    if q_norm < 1e-7:
        return np.zeros(len(gallery_matrix), dtype=np.float32)
    g_norms = np.linalg.norm(gallery_matrix, axis=1)
    g_norms[g_norms < 1e-7] = 1.0
    dots = np.dot(gallery_matrix, query_vec)
    sims = dots / (g_norms * q_norm)
    return np.clip(sims, -1.0, 1.0).astype(np.float32)
