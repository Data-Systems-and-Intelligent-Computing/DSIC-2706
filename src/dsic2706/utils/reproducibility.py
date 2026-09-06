import hashlib
import random
import os
import numpy as np
import torch


def get_file_sha256(filepath: str) -> str:
    """Menghitung SHA-256 hash dari sebuah berkas di disk."""
    if not os.path.exists(filepath):
        return ""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def set_global_seeds(seed: int = 42):
    """Membekukan seed acak pada seluruh pustaka komputasi."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
