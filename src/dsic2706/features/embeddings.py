import numpy as np
import torch
import torch.nn as nn
from .mfcc import extract_mfcc_representation


class DeepAudioBackbone(nn.Module):
    def __init__(self, out_dim=1024, seed=42):
        super().__init__()
        torch.manual_seed(seed)
        self.conv = nn.Sequential(
            nn.Conv1d(1, 16, kernel_size=15, stride=4, padding=7),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.MaxPool1d(4),
            nn.Conv1d(16, 32, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.MaxPool1d(4),
            nn.Conv1d(32, 64, kernel_size=5, stride=2, padding=2),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.AdaptiveAvgPool1d(1)
        )
        self.fc = nn.Linear(64, out_dim)
        for p in self.parameters():
            p.requires_grad = False
        self.eval()

    def forward(self, x):
        feat = self.conv(x).squeeze(-1)
        out = self.fc(feat)
        return out


class AudioRepresentationExtractor:
    def __init__(self, rep_code: str = "R0", config: dict = None):
        self.rep_code = rep_code
        self.config = config or {}
        self.device = torch.device("cpu")

        if self.rep_code == "R0":
            self.dim = 40
        elif self.rep_code == "R1":
            self.dim = 2048
            self.model = DeepAudioBackbone(out_dim=2048, seed=101)
        elif self.rep_code == "R2":
            self.dim = 1024
            self.model = DeepAudioBackbone(out_dim=1024, seed=202)
        elif self.rep_code == "R3":
            self.dim = 64
        else:
            raise ValueError(f"Representasi tidak dikenal: {rep_code}")

    def extract(self, y: np.ndarray, sr: int = 32000) -> np.ndarray:
        if self.rep_code == "R0":
            return extract_mfcc_representation(y, sr=sr, n_mfcc=20)

        elif self.rep_code in ["R1", "R2"]:
            with torch.no_grad():
                tensor = torch.from_numpy(y).float().unsqueeze(0).unsqueeze(0)
                emb = self.model(tensor).squeeze(0).numpy()
                norm = np.linalg.norm(emb)
                if norm > 1e-7:
                    emb = emb / norm
                return emb.astype(np.float32)

        elif self.rep_code == "R3":
            rng = np.random.default_rng(seed=int(abs(y[0] * 100000) if len(y) > 0 and not np.isnan(y[0]) else 42))
            v = rng.standard_normal(self.dim)
            norm = np.linalg.norm(v)
            if norm > 1e-7:
                v = v / norm
            return v.astype(np.float32)
