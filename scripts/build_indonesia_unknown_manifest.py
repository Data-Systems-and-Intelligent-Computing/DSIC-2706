"""
Script: scripts/build_indonesia_unknown_manifest.py
Fungsi: Membangun dataset kontrol negatif Open-Set (Unknown Calibration & Unknown Test)
        khusus biodiversitas Indonesia & derau lingkungan ITERA.
        Rasio 1:1 sempurna terhadap kueri positif:
        - Unknown Calibration: 233 klip (117 burung non-target Indonesia + 116 derau ITERA)
        - Unknown Test: 310 klip (155 burung non-target Indonesia + 155 derau ITERA)
        - Taksa burung non-target antara Calibration dan Test DIJAMIN DISJOINT.
        - Berkas derau ITERA antara Calibration dan Test DIJAMIN DISJOINT.
"""

import os
import sys
import json
import time
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request
import pandas as pd
import numpy as np
import librosa

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = PROJECT_ROOT / "data" / "manifests"
UNK_AUDIO_DIR = PROJECT_ROOT / "data" / "xeno_canto_indonesia_unknowns"
UNK_AUDIO_DIR.mkdir(parents=True, exist_ok=True)

TARGET_FREEZE_CSV = MANIFEST_DIR / "species_freeze.csv"
CANDIDATES_CSV = MANIFEST_DIR / "kandidat_ranking_lengkap_indonesia.csv"
RAW_JSON = MANIFEST_DIR / "xeno_canto_indonesia_raw.json"
ITERA_NOISE_CSV = MANIFEST_DIR / "itera_noise_manifest.csv"
OUTPUT_MANIFEST_CSV = MANIFEST_DIR / "unknown_open_set_manifest.csv"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DSIC-2706-Research/1.0"


def compute_sha256(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def download_and_verify_mp3(url: str, out_file: Path) -> bool:
    if out_file.exists() and out_file.stat().st_size > 1024:
        try:
            y, sr = librosa.load(str(out_file), sr=32000, mono=True, duration=5.0)
            if len(y) > 0:
                return True
        except Exception:
            pass

    out_file.parent.mkdir(parents=True, exist_ok=True)
    retries = 3
    while retries > 0:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=20) as resp:
                if resp.status == 200:
                    data = resp.read()
                    if len(data) < 1000:
                        raise ValueError("File too small")
                    with open(out_file, "wb") as f:
                        f.write(data)
                    y, sr = librosa.load(str(out_file), sr=32000, mono=True, duration=5.0)
                    if len(y) > 0:
                        return True
        except Exception:
            retries -= 1
            if retries == 0:
                if out_file.exists():
                    out_file.unlink(missing_ok=True)
                return False
            time.sleep(1.0)
    return False


def main():
    print("=" * 80)
    print("[*] MEMBANGUN UNKNOWN OPEN-SET MANIFEST (BIODIVERSITAS INDONESIA + DERAU ITERA)")
    print("=" * 80)

    # 1. Target species
    target_df = pd.read_csv(TARGET_FREEZE_CSV)
    target_keys = set(target_df["species_key"])
    target_scis = set(target_df["scientific_name"].str.strip().str.lower())

    # 2. Raw XC records
    print("[*] Memuat xeno_canto_indonesia_raw.json...")
    with open(RAW_JSON, "r", encoding="utf-8") as f:
        raw_records = json.load(f)

    # 3. Filter raw records untuk burung non-target dengan rating valid
    print("[*] Mengelompokkan rekaman non-target...")
    species_to_records = {}
    for r in raw_records:
        sci = f"{r.get('gen', '')} {r.get('sp', '')}".strip().lower()
        if not sci or sci in target_scis:
            continue
        q = r.get("q", "")
        # Filter rating A, B, C (setara >= 3.0)
        if q not in ["A", "B", "C"]:
            continue
        if sci not in species_to_records:
            species_to_records[sci] = []
        species_to_records[sci].append(r)

    # Urutkan spesies berdasarkan ketersediaan rekaman
    available_species = sorted(
        [s for s, recs in species_to_records.items() if len(recs) >= 4],
        key=lambda s: len(species_to_records[s]),
        reverse=True
    )
    print(f"[*] Ditemukan {len(available_species)} taksa non-target dengan >= 4 rekaman.")

    # Alokasi taksa disjoint:
    # 45 taksa pertama untuk Calibration (target: 117 klip)
    # 60 taksa berikutnya untuk Test (target: 155 klip)
    calib_taxa = available_species[:45]
    test_taxa = available_species[45:105]

    print(f"[*] Alokasi Taksa: {len(calib_taxa)} untuk Kalibrasi, {len(test_taxa)} untuk Pengujian (Disjoint: {len(set(calib_taxa) & set(test_taxa)) == 0})")

    # Kumpulkan kandidat klip dengan buffer
    calib_bird_candidates = []
    for sp in calib_taxa:
        for r in species_to_records[sp][:4]:
            calib_bird_candidates.append(r)

    test_bird_candidates = []
    for sp in test_taxa:
        for r in species_to_records[sp][:4]:
            test_bird_candidates.append(r)

    print(f"[*] Terkumpul buffer: {len(calib_bird_candidates)} kandidat kalibrasi, {len(test_bird_candidates)} kandidat test.")

    # 4. Unduh klip burung non-target
    all_bird_tasks = []
    for r in calib_bird_candidates:
        rec_id = r["id"]
        sp_folder = f"{r.get('gen', '')}_{r.get('sp', '')}".lower().replace(" ", "_")
        out_p = UNK_AUDIO_DIR / sp_folder / f"XC{rec_id}.mp3"
        url = f"https://xeno-canto.org/{rec_id}/download"
        all_bird_tasks.append((url, out_p, r, "unknown_calibration"))

    for r in test_bird_candidates:
        rec_id = r["id"]
        sp_folder = f"{r.get('gen', '')}_{r.get('sp', '')}".lower().replace(" ", "_")
        out_p = UNK_AUDIO_DIR / sp_folder / f"XC{rec_id}.mp3"
        url = f"https://xeno-canto.org/{rec_id}/download"
        all_bird_tasks.append((url, out_p, r, "unknown_test"))

    print(f"[*] Mengunduh {len(all_bird_tasks)} berkas audio non-target via ThreadPoolExecutor...")
    downloaded_birds = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_map = {executor.submit(download_and_verify_mp3, t[0], t[1]): t for t in all_bird_tasks}
        for fut in as_completed(future_map):
            t = future_map[fut]
            success = fut.result()
            if success:
                downloaded_birds.append({
                    "task": t,
                    "file_path": str(t[1].relative_to(PROJECT_ROOT)).replace("\\", "/"),
                    "sha256": compute_sha256(t[1]),
                    "label": f"{t[2].get('gen', '')} {t[2].get('sp', '')}",
                    "split_role": t[3]
                })
            else:
                print(f"[-] Gagal mengunduh: {t[0]}")

    print(f"[+] Berhasil mengunduh & memverifikasi {len(downloaded_birds)} berkas audio burung non-target.")

    calib_birds = [b for b in downloaded_birds if b["split_role"] == "unknown_calibration"][:117]
    test_birds = [b for b in downloaded_birds if b["split_role"] == "unknown_test"][:155]
    print(f"[*] Final Burung Non-target: {len(calib_birds)} Kalibrasi, {len(test_birds)} Test.")

    # 5. Pilih Derau ITERA (116 Kalibrasi + 155 Test)
    itera_df = pd.read_csv(ITERA_NOISE_CSV)
    itera_shuffled = itera_df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    
    calib_noise_df = itera_shuffled.iloc[:116]
    test_noise_df = itera_shuffled.iloc[116:116 + 155]
    print(f"[*] Final Derau ITERA: {len(calib_noise_df)} Kalibrasi, {len(test_noise_df)} Test (Disjoint: True).")

    # 6. Bangun baris manifes
    manifest_rows = []

    # Calibration birds (117)
    for idx, b in enumerate(calib_birds):
        manifest_rows.append({
            "unknown_id": f"UNK_CALIB_BIRD_{idx+1:03d}",
            "split_role": "unknown_calibration",
            "source_category": "non_target_species",
            "source_label": b["label"],
            "file_path": b["file_path"],
            "sha256": b["sha256"]
        })

    # Calibration noise (116)
    for idx, r in calib_noise_df.reset_index(drop=True).iterrows():
        rel_p = f"data/itera_noise/{r['filename']}".replace("\\", "/")
        abs_p = PROJECT_ROOT / rel_p
        loc = r["filename"].split("\\")[0]
        manifest_rows.append({
            "unknown_id": f"UNK_CALIB_NOISE_{idx+1:03d}",
            "split_role": "unknown_calibration",
            "source_category": "itera_environmental_noise",
            "source_label": loc,
            "file_path": rel_p,
            "sha256": compute_sha256(abs_p)
        })

    # Test birds (155)
    for idx, b in enumerate(test_birds):
        manifest_rows.append({
            "unknown_id": f"UNK_TEST_BIRD_{idx+1:03d}",
            "split_role": "unknown_test",
            "source_category": "non_target_species",
            "source_label": b["label"],
            "file_path": b["file_path"],
            "sha256": b["sha256"]
        })

    # Test noise (155)
    for idx, r in test_noise_df.reset_index(drop=True).iterrows():
        rel_p = f"data/itera_noise/{r['filename']}".replace("\\", "/")
        abs_p = PROJECT_ROOT / rel_p
        loc = r["filename"].split("\\")[0]
        manifest_rows.append({
            "unknown_id": f"UNK_TEST_NOISE_{idx+1:03d}",
            "split_role": "unknown_test",
            "source_category": "itera_environmental_noise",
            "source_label": loc,
            "file_path": rel_p,
            "sha256": compute_sha256(abs_p)
        })

    out_df = pd.DataFrame(manifest_rows)
    out_df.to_csv(OUTPUT_MANIFEST_CSV, index=False)

    print("\n" + "=" * 80)
    print(f"[+] SUKSES MENYUSUN {OUTPUT_MANIFEST_CSV}")
    print(f"[*] Total Entri Manifes : {len(out_df)}")
    print(out_df["split_role"].value_counts().to_string())
    print("-" * 40)
    print(out_df.groupby(["split_role", "source_category"]).size().to_string())
    print("=" * 80)


if __name__ == "__main__":
    main()
