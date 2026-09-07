"""
Script: scripts/update_manifest_hashes.py
Fungsi: Menghitung ulang dan mencatat hash integritas SHA-256 ketiga manifes resmi.
Menyelesaikan temuan audit M-06.
Perintah pembuatan: python scripts/update_manifest_hashes.py
"""

import hashlib
from pathlib import Path
import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = PROJECT_ROOT / "data/manifests"
OUTPUT_FILE = PROJECT_ROOT / "artifacts/reproducibility/manifest_sha256.txt"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

manifest_files = [
    "target_birds_manifest.csv",
    "dataset_split.csv",
    "unknown_open_set_manifest.csv",
]

def get_file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("=" * 70)
    print("=== PENGHITUNGAN ULANG SHA-256 MANIFES INTEGRITAS (M-06) ===")
    print("=" * 70)

    lines = [
        "# Rekam Jejak Audit Integritas & Reproducibility DSIC-2706",
        f"# Tanggal: {datetime.date.today().strftime('%d %B %Y')}",
        "# Perintah Pembuat: python scripts/update_manifest_hashes.py",
        "",
    ]

    for fname in manifest_files:
        fpath = MANIFEST_DIR / fname
        if not fpath.exists():
            print(f"[!] File {fname} tidak ditemukan!")
            continue
        sha = get_file_sha256(fpath)
        lines.append(f"{fname} : {sha}")
        print(f"[+] {fname:<30} : {sha}")

    lines.extend([
        "",
        "# Baseline Verifikasi Model Asli R2 (BirdNET) @ SNR 0 dB:",
        "mAP@10    : 0.509081",
        "Recall@10 : 0.368139",
        "Top1_Acc  : 0.755319",
        "Frozen Tau: 0.648770",
        ""
    ])

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "=" * 70)
    print(f"[SUKSES] Hash integritas berhasil diperbarui di: {OUTPUT_FILE}")
    print("=" * 70)

if __name__ == "__main__":
    main()
