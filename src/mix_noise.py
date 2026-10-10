"""
Script: src/mix_noise.py
Fungsi: Engine pencampuran derau aditif fisik ITERA (Controlled Additive Noise Mixing).
Menerapkan formula SNR eksak:
    x_noisy = x_clean + alpha * n_noise
    alpha = sqrt( P_signal / (P_noise * 10^(SNR_dB / 10)) )

ATURAN KETAT INTEGRITAS DATA:
- 100% menggunakan rekaman fisik AudioMoth kampus ITERA (data/itera_noise/).
- SINTESIS PINK NOISE DIHAPUS PERMANEN (Zero Synthetic Fallback).
- Jika berkas derau fisik tidak ditemukan, WAJIB melempar FileNotFoundError.
- Setiap operasi pencampuran dapat mengembalikan metadata berkas derau fisik yang dipakai.
"""

from pathlib import Path
import os
import sys
import numpy as np
import pandas as pd
import soundfile as sf
import librosa

PROJECT_ROOT = Path(__file__).resolve().parent.parent

try:
    from src.preprocess import TARGET_SR, TARGET_SAMPLES, TARGET_RMS, normalize_rms
except ImportError:
    from preprocess import TARGET_SR, TARGET_SAMPLES, TARGET_RMS, normalize_rms

NOISE_DIR = PROJECT_ROOT / "data" / "itera_noise"
MANIFEST_PATH = PROJECT_ROOT / "data" / "manifests" / "itera_noise_manifest.csv"

_CACHED_NOISE_FILES = None


def get_available_itera_noise_files():
    """
    Mengambil daftar berkas derau fisik AudioMoth ITERA secara rekursif
    dari itera_noise_manifest.csv atau langsung dari struktur folder fisik.
    MELEMPAR FileNotFoundError jika tidak ditemukan (TIDAK ADA FALLBACK PINK NOISE).
    """
    global _CACHED_NOISE_FILES
    if _CACHED_NOISE_FILES is not None:
        return _CACHED_NOISE_FILES

    noise_files = []

    # 1. Coba baca dari itera_noise_manifest.csv
    if MANIFEST_PATH.exists():
        try:
            df = pd.read_csv(MANIFEST_PATH)
            if "verified_bird_free" in df.columns:
                df = df[df["verified_bird_free"] == True]
            for fn in df["filename"]:
                # Sesuaikan pemisah path Windows/Linux
                rel_path = Path(str(fn).replace("\\", "/"))
                full_path = NOISE_DIR / rel_path
                if full_path.exists():
                    noise_files.append(str(full_path))
        except Exception as e:
            print(f"[!] Peringatan membaca manifes derau: {e}")

    # 2. Jika manifes belum dibaca / berkas kosong, telusuri folder fisik secara rekursif
    if not noise_files and NOISE_DIR.exists():
        for ext in ["*.WAV", "*.wav", "*.mp3", "*.flac"]:
            noise_files.extend([str(p) for p in NOISE_DIR.rglob(ext)])

    if not noise_files:
        raise FileNotFoundError(
            f"[FATAL] Tidak ditemukan berkas audio derau fisik ITERA di {NOISE_DIR}!\n"
            "Sesuai mandat integritas data, fallback sintetis (pink noise) telah DIHAPUS PERMANEN."
        )

    _CACHED_NOISE_FILES = sorted(list(set(noise_files)))
    return _CACHED_NOISE_FILES


def compute_signal_power(x: np.ndarray) -> float:
    """Menghitung daya rata-rata sinyal (Mean Squared Power)."""
    return float(np.mean(x ** 2))


def get_noise_segment(samples: int = TARGET_SAMPLES, seed: int = 42, return_path: bool = False):
    """
    Mengambil segmen derau 5.0 detik nyata dari bank rekaman AudioMoth ITERA.
    """
    noise_files = get_available_itera_noise_files()
    rng = np.random.default_rng(seed)
    selected_file = rng.choice(noise_files)

    try:
        y_noise, _ = librosa.load(selected_file, sr=TARGET_SR, mono=True)
        if len(y_noise) >= samples:
            start = rng.integers(0, len(y_noise) - samples + 1)
            seg = y_noise[start:start + samples].astype(np.float32)
        else:
            repeats = int(np.ceil(samples / len(y_noise)))
            y_noise = np.tile(y_noise, repeats)
            seg = y_noise[:samples].astype(np.float32)

        seg_norm = normalize_rms(seg, target_rms=TARGET_RMS)
        if return_path:
            return seg_norm, selected_file
        return seg_norm

    except Exception as e:
        raise RuntimeError(f"Gagal memproses berkas derau fisik ITERA {selected_file}: {e}")


def mix_audio_at_snr(clean_signal: np.ndarray, snr_db: float, seed: int = 42, return_noise_info: bool = False):
    """
    Mencampur sinyal bersih dengan derau fisik ITERA pada tingkat SNR (dB) eksak.
    """
    noise, noise_path = get_noise_segment(samples=len(clean_signal), seed=seed, return_path=True)

    p_signal = compute_signal_power(clean_signal)
    p_noise = compute_signal_power(noise)

    if p_signal <= 1e-12:
        if return_noise_info:
            return clean_signal, noise_path
        return clean_signal
    if p_noise <= 1e-12:
        if return_noise_info:
            return clean_signal, noise_path
        return clean_signal

    # Hitung faktor scaling alpha
    target_p_noise = p_signal / (10.0 ** (snr_db / 10.0))
    alpha = np.sqrt(target_p_noise / p_noise)

    # Campurkan
    noisy = clean_signal + alpha * noise

    # Jaga agar tidak clipping
    max_amp = np.max(np.abs(noisy))
    if max_amp > 1.0:
        noisy = noisy / max_amp

    result = noisy.astype(np.float32)
    if return_noise_info:
        return result, noise_path
    return result


if __name__ == "__main__":
    print("[*] Menguji engine pencampuran derau fisik ITERA murni...")
    files = get_available_itera_noise_files()
    print(f"[+] Terdeteksi {len(files):,} berkas derau fisik AudioMoth ITERA.")
    
    clean = np.sin(2 * np.pi * 440 * np.linspace(0, 5, 160000)).astype(np.float32)
    for snr in [20, 10, 0, -5]:
        mixed, n_file = mix_audio_at_snr(clean, snr, seed=123, return_noise_info=True)
        fname = Path(n_file).name
        loc = Path(n_file).parent.parent.name
        print(f"Target SNR: {snr:3d} dB  ==> Berkas Derau: {loc}/{fname}")
    print("[+] Integritas derau fisik ITERA 100% lolos!")
