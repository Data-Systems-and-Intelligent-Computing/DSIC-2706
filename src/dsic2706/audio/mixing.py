"""
Module: src/dsic2706/audio/mixing.py
Fungsi: Engine pencampuran derau aditif fisik ITERA untuk paket dsic2706.
"""

import os
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa
from .preprocess import normalize_rms, TARGET_SR, TARGET_SAMPLES

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ITERA_NOISE_DIR = PROJECT_ROOT / "data" / "itera_noise"
MANIFEST_PATH = PROJECT_ROOT / "data" / "manifests" / "itera_noise_manifest.csv"
UNKNOWN_MANIFEST_PATH = PROJECT_ROOT / "data" / "manifests" / "unknown_open_set_manifest.csv"

_CACHED_FILES = None


def get_e3_reserved_noise_files() -> set:
    reserved = set()
    if UNKNOWN_MANIFEST_PATH.exists():
        try:
            import pandas as pd
            df_unk = pd.read_csv(UNKNOWN_MANIFEST_PATH)
            noise_rows = df_unk[df_unk["source_category"] == "itera_environmental_noise"]
            for fp in noise_rows["file_path"]:
                rel = Path(str(fp).replace("\\", "/"))
                reserved.add(rel.name.lower())
        except Exception:
            pass
    return reserved


def get_available_noise_files(exclude_e3_unknowns: bool = True):
    global _CACHED_FILES
    if _CACHED_FILES is not None:
        return _CACHED_FILES

    noise_files = []
    if MANIFEST_PATH.exists():
        import pandas as pd
        df = pd.read_csv(MANIFEST_PATH)
        if "verified_bird_free" in df.columns:
            df = df[df["verified_bird_free"] == True]

        missing = []
        for fn in df["filename"]:
            full_p = ITERA_NOISE_DIR / str(fn).replace("\\", "/")
            if full_p.exists():
                noise_files.append(str(full_p))
            else:
                missing.append(str(fn))

        if missing:
            raise FileNotFoundError(
                f"[FATAL] Ketidaksesuaian jumlah berkas derau fisik ITERA! "
                f"Manifes mencatat {len(df)} berkas, namun {len(missing)} berkas hilang di {ITERA_NOISE_DIR}."
            )
    else:
        if ITERA_NOISE_DIR.exists():
            for ext in ["*.WAV", "*.wav", "*.mp3", "*.flac"]:
                noise_files.extend([str(p) for p in ITERA_NOISE_DIR.rglob(ext)])

    if not noise_files:
        raise FileNotFoundError(
            f"[FATAL] Tidak ditemukan berkas audio derau fisik ITERA di {ITERA_NOISE_DIR}! "
            "Fallback pink noise sintetis telah DIHAPUS PERMANEN."
        )

    noise_files = sorted(list(set(noise_files)))

    if exclude_e3_unknowns:
        reserved = get_e3_reserved_noise_files()
        noise_files = [f for f in noise_files if Path(f).name.lower() not in reserved]

    _CACHED_FILES = noise_files
    return _CACHED_FILES


def calculate_rms(y: np.ndarray) -> float:
    return float(np.sqrt(np.mean(y ** 2)))


def load_itera_noise_segment(duration_samples: int = TARGET_SAMPLES, seed: int = 42, return_path: bool = False,
                             exclude_e3_unknowns: bool = True):
    noise_files = get_available_noise_files(exclude_e3_unknowns=exclude_e3_unknowns)
    rng = np.random.default_rng(seed)

    max_attempts = 10
    for attempt in range(max_attempts):
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

            raw_rms = calculate_rms(seg)
            if raw_rms < 1e-4:
                continue

            seg_norm = normalize_rms(seg, target_rms=0.05)
            
            try:
                rel_path = str(Path(n_file).relative_to(ITERA_NOISE_DIR)).replace("\\", "/")
            except ValueError:
                rel_path = Path(n_file).name

            if return_path:
                return seg_norm, rel_path
            return seg_norm
        except Exception as e:
            if attempt == max_attempts - 1:
                raise RuntimeError(f"Gagal memuat derau fisik ITERA {n_file}: {e}")

    raise ValueError(f"[FATAL] Terdeteksi segmen derau senyap (RMS < 1e-4) setelah {max_attempts} percobaan pengambilan!")


def mix_audio_at_snr(signal: np.ndarray, snr_db: float, noise: np.ndarray = None, seed: int = 42,
                     return_noise_path: bool = False, exclude_e3_unknowns: bool = True):
    used_file = None
    if noise is None:
        noise, used_file = load_itera_noise_segment(
            duration_samples=len(signal),
            seed=seed,
            return_path=True,
            exclude_e3_unknowns=exclude_e3_unknowns
        )

    if len(noise) < len(signal):
        repeats = int(np.ceil(len(signal) / len(noise)))
        noise = np.tile(noise, repeats)[:len(signal)]
    elif len(noise) > len(signal):
        noise = noise[:len(signal)]

    rms_signal = calculate_rms(signal)
    rms_noise = calculate_rms(noise)

    # Tambalan reviewer: jika derau senyap, tolak
    if rms_noise < 1e-7:
        raise ValueError(f"[FATAL] Derau fisik terdeteksi senyap (RMS={rms_noise:.2e})!")

    # Tambalan reviewer: jika sinyal bersih senyap, kembalikan sinyal bersih senyap (BUKAN derau)
    if rms_signal < 1e-7:
        if return_noise_path:
            return signal.copy(), used_file
        return signal.copy()

    desired_rms_noise = rms_signal / (10.0 ** (snr_db / 20.0))
    scaled_noise = noise * (desired_rms_noise / rms_noise)

    mixed = signal + scaled_noise
    mixed = np.clip(mixed, -1.0, 1.0)
    res = mixed.astype(np.float32)

    if return_noise_path:
        return res, used_file
    return res
