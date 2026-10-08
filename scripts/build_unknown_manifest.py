"""
Script: scripts/build_unknown_manifest.py
Fungsi: Membangun manifes dataset kontrol negatif (Unknown Open-Set) untuk Eksperimen E3.
Sesuai audit saintifik:
- Calibration Unknown (y=0): 498 klip (249 derau ITERA + 249 spesies non-target BirdCLEF).
  Rasio 1:1 dengan data kalibrasi positif (498 klip).
- Test Unknown (y=0): 200 klip (100 derau ITERA + 100 spesies non-target BirdCLEF).
  Rasio 1:1 dengan query clean (200 klip).
- Spesies non-target pada unknown_test DISJOINT dengan unknown_calibration.
- Berkas derau ITERA pada unknown_test DISJOINT dengan unknown_calibration.
- Seluruh berkas dihitung checksum SHA-256 untuk keterulangan (reproducibility).
"""

import os
import sys
import hashlib
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = PROJECT_ROOT / "data/manifests"
OUTPUT_PATH = MANIFEST_DIR / "unknown_open_set_manifest.csv"

def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("[*] Membangun Unknown Open-Set Manifest untuk E3...")
    np.random.seed(42)

    # 1. Muat target species agar tidak bocor ke unknown
    target_df = pd.read_csv(MANIFEST_DIR / "species_freeze.csv")
    target_species = set(target_df["species_key"])
    print(f"[*] Terdata {len(target_species)} target species.")

    # 2. Muat BirdCLEF train metadata
    train_meta_path = PROJECT_ROOT / "data/BirdClef/train.csv"
    train_df = pd.read_csv(train_meta_path)
    non_target_df = train_df[~train_df["primary_label"].isin(target_species)].copy()
    
    # Filter hanya berkas yang benar-benar ada di disk
    audio_base = PROJECT_ROOT / "data/BirdClef/train_audio"
    valid_non_targets = []
    for _, r in non_target_df.iterrows():
        fpath = audio_base / r["filename"]
        if fpath.exists():
            valid_non_targets.append({
                "species": r["primary_label"],
                "filename": r["filename"],
                "author": r.get("author", "unknown"),
                "abs_path": fpath,
                "rel_path": f"data/BirdClef/train_audio/{r['filename']}"
            })
    valid_non_target_df = pd.DataFrame(valid_non_targets)
    print(f"[*] Ditemukan {len(valid_non_target_df)} rekaman audio non-target valid di disk.")

    unique_non_target_species = sorted(valid_non_target_df["species"].unique())
    print(f"[*] Jumlah takson non-target unik: {len(unique_non_target_species)}")

    # Bagi spesies non-target: 100 takson untuk kalibrasi, sisanya untuk test (disjoint species)
    rng = np.random.default_rng(42)
    shuffled_species = list(unique_non_target_species)
    rng.shuffle(shuffled_species)

    calib_species = set(shuffled_species[:100])
    test_species = set(shuffled_species[100:])

    pool_calib_birds = valid_non_target_df[valid_non_target_df["species"].isin(calib_species)].sample(n=249, random_state=42)
    pool_test_birds = valid_non_target_df[valid_non_target_df["species"].isin(test_species)].sample(n=100, random_state=42)

    # 3. Muat ITERA noise
    itera_noise_meta = pd.read_csv(MANIFEST_DIR / "itera_noise_manifest.csv")
    itera_base = PROJECT_ROOT / "data/itera_noise"
    valid_itera = []
    for _, r in itera_noise_meta.iterrows():
        p = itera_base / r["filename"]
        if p.exists():
            valid_itera.append({
                "filename": r["filename"],
                "abs_path": p,
                "rel_path": f"data/itera_noise/{r['filename']}".replace("\\", "/")
            })
    valid_itera_df = pd.DataFrame(valid_itera)
    print(f"[*] Ditemukan {len(valid_itera_df)} rekaman derau ITERA valid di disk.")

    shuffled_itera = valid_itera_df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    pool_calib_noise = shuffled_itera.iloc[:249]
    pool_test_noise = shuffled_itera.iloc[249:349]

    # 4. Susun entri manifes
    manifest_rows = []

    # Calibration Unknown: 249 birds + 249 noise = 498
    for idx, r in pool_calib_birds.reset_index(drop=True).iterrows():
        fpath = r["abs_path"]
        manifest_rows.append({
            "unknown_id": f"UNK_CALIB_BIRD_{idx+1:03d}",
            "split_role": "unknown_calibration",
            "source_category": "non_target_species",
            "source_label": r["species"],
            "file_path": r["rel_path"],
            "sha256": compute_sha256(fpath)
        })

    for idx, r in pool_calib_noise.reset_index(drop=True).iterrows():
        fpath = r["abs_path"]
        loc = r["filename"].split("\\")[0]
        manifest_rows.append({
            "unknown_id": f"UNK_CALIB_NOISE_{idx+1:03d}",
            "split_role": "unknown_calibration",
            "source_category": "itera_environmental_noise",
            "source_label": loc,
            "file_path": r["rel_path"],
            "sha256": compute_sha256(fpath)
        })

    # Test Unknown: 100 birds + 100 noise = 200
    for idx, r in pool_test_birds.reset_index(drop=True).iterrows():
        fpath = r["abs_path"]
        manifest_rows.append({
            "unknown_id": f"UNK_TEST_BIRD_{idx+1:03d}",
            "split_role": "unknown_test",
            "source_category": "non_target_species",
            "source_label": r["species"],
            "file_path": r["rel_path"],
            "sha256": compute_sha256(fpath)
        })

    for idx, r in pool_test_noise.reset_index(drop=True).iterrows():
        fpath = r["abs_path"]
        loc = r["filename"].split("\\")[0]
        manifest_rows.append({
            "unknown_id": f"UNK_TEST_NOISE_{idx+1:03d}",
            "split_role": "unknown_test",
            "source_category": "itera_environmental_noise",
            "source_label": loc,
            "file_path": r["rel_path"],
            "sha256": compute_sha256(fpath)
        })

    df_manifest = pd.DataFrame(manifest_rows)
    df_manifest.to_csv(OUTPUT_PATH, index=False)
    print(f"\n[+] Sukses membuat unknown manifest: {OUTPUT_PATH}")
    print(f"[+] Total entri: {len(df_manifest)}")
    print(df_manifest["split_role"].value_counts())
    print(df_manifest["source_category"].value_counts())

if __name__ == "__main__":
    main()
