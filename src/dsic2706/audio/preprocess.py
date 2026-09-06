import os
import yaml
import numpy as np
import librosa

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "configs", "audio.yaml")


def load_audio_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
            return cfg.get("audio", {})
    return {
        "target_sample_rate": 32000,
        "mono": True,
        "duration_sec": 5.0,
        "target_length_samples": 160000,
        "normalization": {"type": "rms", "target_rms": 0.05}
    }


CFG = load_audio_config()
TARGET_SR = CFG.get("target_sample_rate", 32000)
DURATION_SEC = CFG.get("duration_sec", 5.0)
TARGET_SAMPLES = int(TARGET_SR * DURATION_SEC)
TARGET_RMS = CFG.get("normalization", {}).get("target_rms", 0.05)


def select_highest_energy_window(y: np.ndarray, sr: int, window_samples: int) -> np.ndarray:
    if len(y) <= window_samples:
        return y
    hop = window_samples // 4
    num_windows = max(1, (len(y) - window_samples) // hop + 1)
    best_rms = -1.0
    best_start = 0

    for i in range(num_windows):
        start = i * hop
        end = start + window_samples
        seg = y[start:end]
        rms = np.sqrt(np.mean(seg ** 2))
        if rms > best_rms:
            best_rms = rms
            best_start = start

    return y[best_start:best_start + window_samples]


def normalize_rms(y: np.ndarray, target_rms: float = 0.05) -> np.ndarray:
    current_rms = np.sqrt(np.mean(y ** 2))
    if current_rms > 1e-6:
        y = y * (target_rms / current_rms)
    return np.clip(y, -1.0, 1.0)


def preprocess_audio(file_path: str, target_sr: int = TARGET_SR, target_samples: int = TARGET_SAMPLES) -> np.ndarray:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File audio tidak ditemukan: {file_path}")

    y, sr = librosa.load(file_path, sr=target_sr, mono=True)
    y = select_highest_energy_window(y, target_sr, target_samples)

    if len(y) < target_samples:
        pad_width = target_samples - len(y)
        y = np.pad(y, (0, pad_width), mode='constant')

    y = y[:target_samples]
    y = normalize_rms(y, target_rms=TARGET_RMS)
    return y.astype(np.float32)
