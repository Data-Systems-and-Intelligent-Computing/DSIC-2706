"""
Script: src/embeddings.py
Fungsi: Antarmuka terpadu ekstraksi representasi audio (R0, R1, R2, R3).
Sesuai Dokumen Audit (Penyelesaian C-01 Opsi A):
- R0: Baseline MFCC + temporal mean/std pooling (40 dimensi).
- R1: Generic Pretrained Audio Embedding (PANNs CNN14 AudioSet, 2048 dimensi).
- R2: Bioacoustic Pretrained Embedding (BirdNET V2.4 Backbone ONNX, 1024 dimensi).
- R3: Random Control Embedding (40 dimensi).
- Seluruh representasi bersifat FROZEN (tanpa fine-tuning).
- TANPA peralihan diam-diam (silent fallback). Jika bobot tidak ada atau dimensi salah, wajib raise Exception.
"""

import os
import sys
import hashlib
from pathlib import Path
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHECKPOINTS_DIR = PROJECT_ROOT / "checkpoints"
R3_CONTROL_VERSION = "stable_id_v1"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.preprocess import TARGET_SR
    from src.mfcc import extract_mfcc_representation
except ImportError:
    from preprocess import TARGET_SR
    from mfcc import extract_mfcc_representation


class AudioRepresentationExtractor:
    def __init__(self, rep_code: str = "R0", random_seed: int = 42):
        self.rep_code = rep_code.upper()
        self.random_seed = int(random_seed)
        self._model = None
        self._init_model()

    def _init_model(self):
        if self.rep_code == "R0":
            # Baseline MFCC tidak memerlukan pemuatan bobot deep learning
            pass

        elif self.rep_code == "R1":
            # Generic Pretrained PANNs CNN14 (2048 dimensi)
            ckpt_path = CHECKPOINTS_DIR / "Cnn14_mAP=0.431.pth"
            if not ckpt_path.exists():
                raise FileNotFoundError(
                    f"[C-01 ERROR] Checkpoint PANNs CNN14 tidak ditemukan di: {ckpt_path}\n"
                    f"Silakan jalankan: python scripts/download_models.py"
                )

            try:
                import torch
                # Jangan mengunduh diam-diam pada saat eksperimen. Berkas pendukung
                # harus tersedia lokal agar lingkungan dapat direproduksi.
                labels_path = Path.home() / "panns_data" / "class_labels_indices.csv"
                if not labels_path.exists():
                    raise FileNotFoundError(
                        "[R1 ERROR] class_labels_indices.csv PANNs tidak tersedia secara lokal di "
                        f"{labels_path}. Siapkan dependensi model sebelum menjalankan eksperimen; "
                        "pipeline tidak diizinkan mengunduh berkas saat evaluasi."
                    )
                from panns_inference import AudioTagging
            except ImportError as e:
                raise ImportError(
                    f"[C-01 ERROR] Pustaka 'panns_inference' belum terpasang!\n"
                    f"Silakan jalankan di terminal: python -m pip install panns_inference\n"
                    f"Rincian error: {e}"
                )

            device = "cuda" if torch.cuda.is_available() else "cpu"
            self._device = device
            # Memuat model PANNs CNN14 dari checkpoint lokal resmi (relative POSIX path)
            try:
                rel_ckpt_path = Path(os.path.relpath(ckpt_path, Path.cwd())).as_posix()
            except Exception:
                rel_ckpt_path = str(ckpt_path)
            self._model = AudioTagging(checkpoint_path=rel_ckpt_path, device=device)

        elif self.rep_code == "R2":
            # Bioacoustic Pretrained Model (BirdNET V2.4 Backbone, 1024 dimensi)
            ckpt_path = CHECKPOINTS_DIR / "BirdNET_GLOBAL_6K_V2.4_Model_FP32.onnx"
            if not ckpt_path.exists():
                raise FileNotFoundError(
                    f"[C-01 ERROR] Checkpoint BirdNET ONNX tidak ditemukan di: {ckpt_path}\n"
                    f"Silakan jalankan: python scripts/download_models.py"
                )

            try:
                import onnxruntime as ort
            except ImportError:
                raise ImportError(
                    "[C-01 ERROR] Pustaka 'onnxruntime' belum terpasang!\n"
                    "Silakan jalankan di terminal: python -m pip install onnxruntime"
                )

            # Prioritaskan CUDA jika tersedia di onnxruntime
            available_providers = ort.get_available_providers()
            providers = ["CUDAExecutionProvider", "CPUExecutionProvider"] if "CUDAExecutionProvider" in available_providers else ["CPUExecutionProvider"]
            try:
                rel_ckpt_onnx = Path(os.path.relpath(ckpt_path, Path.cwd())).as_posix()
            except Exception:
                rel_ckpt_onnx = str(ckpt_path)
            self._model = ort.InferenceSession(rel_ckpt_onnx, providers=providers)

        elif self.rep_code == "R3":
            # Kontrol Acak
            pass

        else:
            raise ValueError(f"Kode representasi tidak dikenal: {self.rep_code}")

    def extract(self, y: np.ndarray, sr: int = TARGET_SR, item_id: str | None = None) -> np.ndarray:
        """
        Mengekstrak vektor embedding ternormalisasi L2 dari sinyal 1D audio y.
        """
        if self.rep_code == "R0":
            emb = extract_mfcc_representation(y, sr=sr)
            if emb.shape != (40,):
                raise ValueError(f"[C-01 ERROR] Dimensi R0 tidak sesuai! Diharapkan (40,), didapat {emb.shape}")
            return emb

        elif self.rep_code == "R1":
            # Ekstraksi intermediate feature vector 2048-dim dari PANNs CNN14
            import torch
            with torch.no_grad():
                audio_tensor = torch.as_tensor(y[None, :]).float().to(self._device)
                # inference menghasilkan (clipwise_output, embedding)
                _, emb_out = self._model.inference(audio_tensor)
                if hasattr(emb_out, "cpu"):
                    emb = emb_out.cpu().numpy().squeeze()
                else:
                    emb = np.array(emb_out).squeeze()
                
            if emb.shape != (2048,):
                raise ValueError(f"[C-01 ERROR] Dimensi R1 tidak sesuai! Diharapkan (2048,), didapat {emb.shape}")
            
            norm = np.linalg.norm(emb)
            return (emb / max(norm, 1e-8)).astype(np.float32)

        elif self.rep_code == "R2":
            # Ekstraksi representasi bioakustik BirdNET V2.4 (1024-dimensi)
            # BirdNET beroperasi pada laju sampel 48 kHz dan jendela 3 detik (144.000 sampel)
            if sr != 48000:
                try:
                    import librosa
                except ImportError as error:
                    raise ImportError("[R2 ERROR] Pustaka 'librosa' diperlukan untuk resampling ke 48 kHz.") from error
                y_48k = librosa.resample(y, orig_sr=sr, target_sr=48000)
            else:
                y_48k = y

            window_size = 144000  # 3 detik pada 48 kHz
            total_samples = len(y_48k)

            if total_samples < window_size:
                # Padding jika audio kurang dari 3 detik
                pad_width = window_size - total_samples
                y_48k = np.pad(y_48k, (0, pad_width), mode="constant")
                total_samples = len(y_48k)

            # Buat sliding windows (langkah 1 detik / 48.000 sampel) untuk temporal pooling
            hop_size = 48000
            windows = []
            for start in range(0, total_samples - window_size + 1, hop_size):
                windows.append(y_48k[start : start + window_size])

            if not windows:
                windows.append(y_48k[:window_size])

            batch = np.stack(windows, axis=0).astype(np.float32)
            # Jalankan inferensi ONNX
            out = self._model.run(["embedding"], {"INPUT": batch})[0]  # shape (num_windows, 1024)
            # Temporal mean pooling melintasi seluruh jendela klip
            emb = np.mean(out, axis=0)

            if emb.shape != (1024,):
                raise ValueError(f"[C-01 ERROR] Dimensi R2 tidak sesuai! Diharapkan (1024,), didapat {emb.shape}")

            norm = np.linalg.norm(emb)
            return (emb / max(norm, 1e-8)).astype(np.float32)

        elif self.rep_code == "R3":
            # Kontrol acak harus independen dari waveform. ID yang stabil membuat
            # hasil dapat direproduksi dan tetap sama untuk versi clean/noisy dari
            # rekaman yang sama.
            if item_id is None or not str(item_id).strip():
                raise ValueError("R3 membutuhkan item_id stabil; kontrol acak tidak boleh memakai waveform sebagai seed.")
            seed_material = f"{R3_CONTROL_VERSION}:{self.random_seed}:{item_id}".encode("utf-8")
            seed = int.from_bytes(hashlib.sha256(seed_material).digest()[:8], byteorder="big", signed=False)
            rng = np.random.default_rng(seed)
            rnd = rng.standard_normal(40).astype(np.float32)
            return (rnd / max(np.linalg.norm(rnd), 1e-8)).astype(np.float32)

        else:
            raise ValueError(f"Representasi tidak dikenal: {self.rep_code}")


if __name__ == "__main__":
    print("=" * 60)
    print("[*] Menguji AudioRepresentationExtractor R0, R1, R2, R3...")
    print("=" * 60)
    test_sig = np.random.randn(160000).astype(np.float32)  # 5 detik @ 32 kHz
    for code in ["R0", "R1", "R2", "R3"]:
        try:
            ext = AudioRepresentationExtractor(code)
            feat = ext.extract(test_sig, item_id="smoke-test")
            print(f"[PASS] {code} -> Dimensi Vektor: {feat.shape} | L2-Norm: {np.linalg.norm(feat):.4f}")
        except Exception as e:
            print(f"[FAIL] {code} -> Error: {e}")
    print("=" * 60)
