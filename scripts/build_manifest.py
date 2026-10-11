"""
Script: scripts/build_manifest.py
Fungsi: Memvalidasi integritas seluruh manifes dataset yang telah dibekukan.
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = PROJECT_ROOT / "data/manifests"

def validate_manifests():
    print("[*] Memvalidasi Manifes Dataset DSIC-2706...")
    required_manifests = {
        "dataset_split.csv": 4351,
        "species_freeze.csv": 20,
        "species_excluded.csv": 186,
        "itera_noise_manifest.csv": 1799,
        "unknown_open_set_manifest.csv": 698
    }
    
    all_valid = True
    for fname, expected_rows in required_manifests.items():
        p = MANIFEST_DIR / fname
        if not p.exists():
            print(f"[-] GAGAL: {fname} tidak ditemukan!")
            all_valid = False
            continue
        df = pd.read_csv(p)
        if len(df) != expected_rows:
            print(f"[-] GAGAL: {fname} memiliki {len(df)} baris (diharapkan {expected_rows})")
            all_valid = False
        else:
            print(f"[+] LULUS: {fname} ({len(df)} baris)")
            
    if all_valid:
        print("[+] Seluruh manifes dataset terverifikasi valid dan lengkap.")
    else:
        print("[-] Ada kegagalan validasi manifes.")

if __name__ == "__main__":
    validate_manifests()
