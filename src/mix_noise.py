"""
Script: src/mix_noise.py
Fungsi: Engine pencampuran derau aditif terkontrol (Controlled Additive Noise Mixing).
Menerapkan formula SNR eksak:
    x_noisy = x_clean + alpha * n_noise
    alpha = sqrt( P_signal / (P_noise * 10^(SNR_dB / 10)) )

Sesuai Bab 11.4 Dokumen Audit:
- SNR Grid: 20 dB, 10 dB, 0 dB, -5 dB
- Seed terkontrol (reproducible)
- Mendukung sumber derau nyata (data/itera_noise/) jika sudah tersedia,
  serta fallback ke profil derau spektral lingkungan (pink/environmental noise)
  sebelum perekaman lapangan selesai.
"""

import os
import sys
import numpy as np
import soundfile as sf
import librosa

try:
    from src.preprocess import TARGET_SR, TARGET_SAMPLES, TARGET_RMS, normalize_rms
except ImportError:
    from preprocess import TARGET_SR, TARGET_SAMPLES, TARGET_RMS, normalize_rms

NOISE_DIR = "d:/FILE AND TASK/TA/data/itera_noise"


def compute_signal_power(x: np.ndarray) -> float:
    """Menghitung daya rata-rata sinyal (Mean Squared Power)."""
    return float(np.mean(x ** 2))


def generate_environmental_pink_noise(samples: int, seed: int = 42) -> np.ndarray:
    """
    Menghasilkan profil derau lingkungan (pink noise 1/f) sebagai baseline fallback
    ketika berkas audio fisik lapangan belum diletakkan di folder.
    """
    rng = np.random.default_rng(seed)
    # Sintesis derau pink via spectral filtering
    white = rng.standard_normal(samples)
    X = np.fft.rfft(white)
    frequencies = np.fft.rfftfreq(samples)
    frequencies[0] = 1.0  # Hindari division by zero pada frekuensi DC
    # Penurunan daya 1/sqrt(f) pada amplitudo (1/f pada daya)
    X_pink = X / np.sqrt(frequencies)
    X_pink[0] = 0.0
    pink = np.fft.irfft(X_pink, n=samples)
    return pink.astype(np.float32)


def get_noise_segment(samples: int = TARGET_SAMPLES, seed: int = 42) -> np.ndarray:
    """
    Mengambil segmen derau latar belakang dari data/itera_noise jika tersedia,
    atau menggunakan derau spektral terstandarisasi jika folder masih kosong.
    """
    if os.path.exists(NOISE_DIR):
        noise_files = [
            os.path.join(NOISE_DIR, f)
            for f in os.listdir(NOISE_DIR)
            if f.lower().endswith(('.wav', '.mp3', '.flac'))
        ]
        if noise_files:
            # Ambil file derau berdasarkan seed
            rng = np.random.default_rng(seed)
            selected_file = rng.choice(noise_files)
            try:
                y_noise, _ = librosa.load(selected_file, sr=TARGET_SR, mono=True)
                if len(y_noise) >= samples:
                    start = rng.integers(0, len(y_noise) - samples + 1)
                    return y_noise[start:start + samples].astype(np.float32)
                else:
                    # Tile jika durasi derau pendek
                    repeats = int(np.ceil(samples / len(y_noise)))
                    y_noise = np.tile(y_noise, repeats)
                    return y_noise[:samples].astype(np.float32)
            except Exception as e:
                print(f"[-] Gagal membaca file derau {selected_file}: {e}")

    # Fallback ke environmental pink noise
    return generate_environmental_pink_noise(samples, seed=seed)


def mix_audio_at_snr(clean_signal: np.ndarray, snr_db: float, seed: int = 42) -> np.ndarray:
    """
    Mencampur sinyal bersih dengan derau pada tingkat SNR (dB) yang ditentukan secara eksak.
    """
    noise = get_noise_segment(samples=len(clean_signal), seed=seed)

    p_signal = compute_signal_power(clean_signal)
    p_noise = compute_signal_power(noise)

    if p_signal <= 1e-12:
        return clean_signal
    if p_noise <= 1e-12:
        return clean_signal

    # Hitung scaling factor alpha
    target_p_noise = p_signal / (10.0 ** (snr_db / 10.0))
    alpha = np.sqrt(target_p_noise / p_noise)

    # Campurkan
    noisy = clean_signal + alpha * noise

    # Jaga agar tidak clipping
    max_amp = np.max(np.abs(noisy))
    if max_amp > 1.0:
        noisy = noisy / max_amp

    return noisy.astype(np.float32)


if __name__ == "__main__":
    print("[*] Menguji formula pencampuran derau...")
    clean = np.sin(2 * np.pi * 440 * np.linspace(0, 5, 160000)).astype(np.float32)
    for snr in [20, 10, 0, -5]:
        mixed = mix_audio_at_snr(clean, snr, seed=123)
        p_c = compute_signal_power(clean)
        # Estimasi komponen derau
        noise_comp = mixed - clean
        p_n = compute_signal_power(noise_comp)
        actual_snr = 10 * np.log10(p_c / p_n) if p_n > 0 else 999
        print(f"Target SNR: {snr:3d} dB  ==>  Approx SNR: {actual_snr:.2f} dB")
    print("[+] Test mixing selesai!")
