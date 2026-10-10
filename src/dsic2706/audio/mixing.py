import os
import glob
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa
from .preprocess import normalize_rms, TARGET_SR, TARGET_SAMPLES

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ITERA_NOISE_DIR = PROJECT_ROOT / "data" / "itera_noise"
MANIFEST_PATH = PROJECT_ROOT / "data" / "manifests" / "itera_noise_manifest.csv"

_CACHED_FILES = None


def get_available_noise_files():
    global _CACHED_FILES
    if _CACHED_FILES is not None:
        return _CACHED_FILES

    noise_files = []
    if MANIFEST_PATH.exists():
        try:
            import pandas as pd
            df = pd.read_csv(MANIFEST_PATH)
            if "verified_bird_free" in df.columns:
                df = df[df["verified_bird_free"] == True]
            for fn in df["filename"]:
                full_p = ITERA_NOISE_DIR / str(fn).replace("\\", "/")
                if full_p.exists():
                    noise_files.append(str(full_p))
        except Exception:
            pass

    if not noise_files and ITERA_NOISE_DIR.exists():
        for ext in ["*.WAV", "*.wav", "*.mp3", "*.flac"]:
            noise_files.extend([str(p) for p in ITERA_NOISE_DIR.rglob(ext)])

    if not noise_files:
        raise FileNotFoundError(
            f"[FATAL] Tidak ditemukan berkas audio derau fisik ITERA di {ITERA_NOISE_DIR}! "
            "Fallback pink noise sintetis telah DIHAPUS PERMANEN."
        )

    _CACHED_FILES = sorted(list(set(noise_files)))
    return _CACHED_FILES


def calculate_rms(y: np.ndarray) -> float:
    return float(np.sqrt(np.mean(y ** 2)))


def load_itera_noise_segment(duration_samples: int = TARGET_SAMPLES, seed: int = 42, return_path: bool = False):
    noise_files = get_available_noise_files()
    rng = np.random.default_rng(seed)
    n_file = rng.choice(noise_files)

    try:
        y_noise, _ = librosa.load(n_file, sr=TARGET_SR, mono=True)
        if len(y_noise) >= duration_samples:
            max_start = len(y_noise) - duration_samples
            start = rng.integers(0, max_start + 1)
            seg = y_noise[start:start + duration_samples]
        else:
            repeats = int(np.ceil(duration_samples / len(y_noise)))
            seg = np.tile(y_noise, repeats)[:duration_samples]

        seg_norm = normalize_rms(seg, target_rms=0.05)
        if return_path:
            return seg_norm, n_file
        return seg_norm
    except Exception as e:
        raise RuntimeError(f"Gagal memuat derau fisik ITERA {n_file}: {e}")


def mix_audio_at_snr(signal: np.ndarray, snr_db: float, noise: np.ndarray = None, seed: int = 42, return_noise_path: bool = False):
    used_file = None
    if noise is None:
        noise, used_file = load_itera_noise_segment(len(signal), seed=seed, return_path=True)

    if len(noise) < len(signal):
        repeats = int(np.ceil(len(signal) / len(noise)))
        noise = np.tile(noise, repeats)[:len(signal)]
    elif len(noise) > len(signal):
        noise = noise[:len(signal)]

    rms_signal = calculate_rms(signal)
    rms_noise = calculate_rms(noise)

    if rms_noise < 1e-7:
        if return_noise_path:
            return signal.copy(), used_file
        return signal.copy()
    if rms_signal < 1e-7:
        if return_noise_path:
            return noise.copy(), used_file
        return noise.copy()

    desired_rms_noise = rms_signal / (10.0 ** (snr_db / 20.0))
    scaled_noise = noise * (desired_rms_noise / rms_noise)

    mixed = signal + scaled_noise
    mixed = np.clip(mixed, -1.0, 1.0)
    res = mixed.astype(np.float32)

    if return_noise_path:
        return res, used_file
    return res
