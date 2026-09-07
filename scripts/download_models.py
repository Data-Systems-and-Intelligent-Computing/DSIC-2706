"""
Skrip Fase 2.1: Pengunduh Bobot Model Asli (BirdNET & PANNs CNN14)
Topik: DSIC-2706 (Penyelesaian Isu Kritis C-01 - Opsi A)
"""

from pathlib import Path
import sys
import urllib.request
import time

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHECKPOINTS_DIR = PROJECT_ROOT / "checkpoints"
CHECKPOINTS_DIR.mkdir(exist_ok=True)

MODELS = {
    "BirdNET_V2.4_Backbone (R2)": {
        "filename": "BirdNET_GLOBAL_6K_V2.4_Model_FP32.onnx",
        "url": "https://huggingface.co/biodiversica/BirdNET-onnx-backbone/resolve/main/model_backbone.onnx",
        "expected_min_bytes": 15 * 1024 * 1024,  # ~20 MB
    },
    "PANNs_CNN14 (R1)": {
        "filename": "Cnn14_mAP=0.431.pth",
        "url": "https://huggingface.co/thelou1s/panns-inference/resolve/main/Cnn14_mAP%3D0.431.pth",
        "fallback_url": "https://zenodo.org/records/3987831/files/Cnn14_mAP%3D0.431.pth?download=1",
        "expected_min_bytes": 300 * 1024 * 1024,  # ~327 MB
    },
}

def download_with_progress(url, dest_path, desc):
    print(f"\n[*] Mengunduh {desc}...")
    print(f"    URL : {url}")
    print(f"    Dest: {dest_path}")
    
    start_time = time.time()
    
    def reporthook(count, block_size, total_size):
        if total_size > 0:
            percent = int(count * block_size * 100 / total_size)
            downloaded_mb = (count * block_size) / (1024 * 1024)
            total_mb = total_size / (1024 * 1024)
            sys.stdout.write(f"\r    Progres: {percent}% [{downloaded_mb:.1f} MB / {total_mb:.1f} MB]")
            sys.stdout.flush()

    opener = urllib.request.build_opener()
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)")]
    urllib.request.install_opener(opener)
    
    urllib.request.urlretrieve(url, dest_path, reporthook)
    elapsed = time.time() - start_time
    size_mb = dest_path.stat().st_size / (1024 * 1024)
    print(f"\n[+] Selesai! Ukuran: {size_mb:.2f} MB (Waktu: {elapsed:.1f} detik)")

def main():
    print("=" * 70)
    print("=== [FASE 2.1] PENGUNDUHAN BOBOT MODEL PRETRAINED NYATA (C-01) ===")
    print("=" * 70)
    
    for name, info in MODELS.items():
        dest = CHECKPOINTS_DIR / info["filename"]
        if dest.exists() and dest.stat().st_size >= info["expected_min_bytes"]:
            size_mb = dest.stat().st_size / (1024 * 1024)
            print(f"\n[SUDAH TERSEDIA] {name}")
            print(f"    Berkas : {dest.name} ({size_mb:.2f} MB)")
            continue
            
        try:
            download_with_progress(info["url"], dest, name)
        except Exception as e:
            print(f"\n[!] Gagal mengunduh dari URL utama: {e}")
            if "fallback_url" in info:
                print("[*] Mencoba URL cadangan...")
                try:
                    download_with_progress(info["fallback_url"], dest, name)
                except Exception as e2:
                    print(f"[ERROR] Gagal dari URL cadangan: {e2}")
                    sys.exit(1)
            else:
                sys.exit(1)

    print("\n" + "=" * 70)
    print("[SUKSES] Seluruh bobot model pretrained resmi telah siap di folder checkpoints/!")
    print("=" * 70)

if __name__ == "__main__":
    main()
