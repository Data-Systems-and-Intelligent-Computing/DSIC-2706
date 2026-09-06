import os
import glob
import numpy as np
import soundfile as sf
import librosa
from .preprocess import normalize_rms, TARGET_SR, TARGET_SAMPLES

ITERA_NOISE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "itera_noise")


def calculate_rms(y: np.ndarray) -> float:
    return float(np.sqrt(np.mean(y ** 2)))


def load_itera_noise_segment(duration_samples: int = TARGET_SAMPLES, seed: int = 42) -> np.ndarray:
    noise_files = glob.glob(os.path.join(ITERA_NOISE_DIR, "*.wav")) + glob.glob(os.path.join(ITERA_NOISE_DIR, "*.mp3"))
    if noise_files:
        rng = np.random.default_rng(seed)
        n_file = rng.choice(noise_files)
        y_noise, _ = librosa.load(n_file, sr=TARGET_SR, mono=True)
        if len(y_noise) >= duration_samples:
            max_start = len(y_noise) - duration_samples
            start = rng.integers(0, max_start + 1)
            seg = y_noise[start:start + duration_samples]
        else:
            repeats = int(np.ceil(duration_samples / len(y_noise)))
            seg = np.tile(y_noise, repeats)[:duration_samples]
        return normalize_rms(seg, target_rms=0.05)

    # Ambient pink noise fallback
    rng = np.random.default_rng(seed)
    white = rng.normal(0, 0.05, duration_samples)
    b = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
    a = [1, -2.494956002, 2.017265875, -0.522189400]
    try:
        from scipy.signal import lfilter
        pink = lfilter(b, a, white)
    except Exception:
        pink = white
    return normalize_rms(pink, target_rms=0.05)


def mix_audio_at_snr(signal: np.ndarray, snr_db: float, noise: np.ndarray = None, seed: int = 42) -> np.ndarray:
    if noise is None:
        noise = load_itera_noise_segment(len(signal), seed=seed)

    if len(noise) < len(signal):
        repeats = int(np.ceil(len(signal) / len(noise)))
        noise = np.tile(noise, repeats)[:len(signal)]
    elif len(noise) > len(signal):
        noise = noise[:len(signal)]

    rms_signal = calculate_rms(signal)
    rms_noise = calculate_rms(noise)

    if rms_noise < 1e-7:
        return signal.copy()
    if rms_signal < 1e-7:
        return noise.copy()

    desired_rms_noise = rms_signal / (10.0 ** (snr_db / 20.0))
    scaled_noise = noise * (desired_rms_noise / rms_noise)

    mixed = signal + scaled_noise
    mixed = np.clip(mixed, -1.0, 1.0)
    return mixed.astype(np.float32)
