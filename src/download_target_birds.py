
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
"""
Script: src/download_target_birds.py
Fungsi: Mengumpulkan dan mengunduh rekaman 15 spesies burung target Sumatera dari Xeno-Canto.
Sesuai arahan Audit Bab 11.2:
- Tidak mensyaratkan rekaman harus tepat di dalam batas taman nasional.
- Mengambil seluruh rekaman spesies target di wilayah Indonesia/Sumatera dengan lokasi terverifikasi.
- Mencatat metadata lengkap: recording ID, spesies, perekam, tanggal, lokasi, lisensi, dan checksum SHA-256.
- Memanfaatkan file yang sudah ada sebelumnya di Dataset/Bioakustik_Sumatera/ untuk efisiensi.
"""

import os
import sys
import time
import hashlib
import shutil
import requests
import pandas as pd

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

API_ENDPOINT = "https://xeno-canto.org/api/3/recordings"
API_KEY = "95dc5b3f6834b56e17da4cf68cc890cb470d1284"
HEADERS = {
    "User-Agent": "BioacousticResearchITERA/1.0 (Academic Research; dsic.itera.ac.id)"
}

TARGET_DIR = str(PROJECT_ROOT / "data/xeno_canto")
MANIFEST_PATH = str(PROJECT_ROOT / "data/manifests/target_birds_manifest.csv")
EXISTING_DIR = str(PROJECT_ROOT / "Dataset/Bioakustik_Sumatera")

# 15 Spesies Burung Target Sumatera Terpilih (100% rekaman terbuka dan terverifikasi di Indonesia)
FROZEN_TARGET_SPECIES = [
    ("Carpococcyx", "viridis", "Sumatran Ground Cuckoo", True),
    ("Gypsophila", "rufipectus", "Rusty-breasted Wren-Babbler", True),
    ("Napothera", "albostriata", "Sumatran Wren-Babbler", True),
    ("Myophonus", "melanurus", "Shiny Whistling Thrush", True),
    ("Polyplectron", "chalcurum", "Bronze-tailed Peacock-Pheasant", True),
    ("Halcyon", "smyrnensis", "White-throated Kingfisher", False),
    ("Orthotomus", "ruficeps", "Ashy Tailorbird", False),
    ("Spilornis", "cheela", "Crested Serpent Eagle", False),
    ("Dicrurus", "hottentottus", "Hair-crested Drongo", False),
    ("Pnoepyga", "pusilla", "Pygmy Cupwing", False),
    ("Brachypteryx", "montana", "White-browed Shortwing", False),
    ("Horornis", "vulcanius", "Sunda Bush Warbler", False),
    ("Batrachostomus", "cornutus", "Sunda Frogmouth", False),
    ("Malacopteron", "affine", "Sooty-capped Babbler", False),
    ("Aethopyga", "siparaja", "Crimson Sunbird", False),
    ("Dicaeum", "trigonostigma", "Orange-bellied Flowerpecker", False)
]


def compute_sha256(file_path: str) -> str:
    """Menghitung SHA-256 hash dari berkas audio untuk menjamin integritas."""
    hasher = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return ""


def find_existing_file(rec_id: str, species_name: str) -> str:
    """Mencari apakah berkas audio sudah pernah diunduh sebelumnya."""
    target_name = f"XC{rec_id}_{species_name}.mp3"
    for root, dirs, files in os.walk(EXISTING_DIR):
        if target_name in files:
            candidate = os.path.join(root, target_name)
            if os.path.getsize(candidate) > 1000:
                return candidate
    return ""


def fetch_species_recordings(genus: str, species: str) -> list:
    """Mengambil seluruh metadata rekaman untuk spesies dari Xeno-Canto di Indonesia."""
    query = f"gen:{genus} sp:{species} cnt:indonesia"
    all_recs = []
    page = 1
    while True:
        params = {"query": query, "key": API_KEY, "page": page, "per_page": 500}
        try:
            r = requests.get(API_ENDPOINT, params=params, headers=HEADERS, timeout=30)
            if r.status_code != 200:
                print(f"      [Warning] HTTP {r.status_code} on page {page}", flush=True)
                break
            data = r.json()
            recs = data.get("recordings", [])
            all_recs.extend(recs)
            num_pages = int(data.get("numPages", 1))
            if page >= num_pages or not recs:
                break
            page += 1
            time.sleep(0.2)
        except Exception as e:
            print(f"      [Error] {e}", flush=True)
            break
    return all_recs


def main():
    os.makedirs(TARGET_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(MANIFEST_PATH), exist_ok=True)

    print("=" * 85, flush=True)
    print("[*] AKUISISI DATASET 15 SPESIES BURUNG TARGET SUMATERA (XENO-CANTO)", flush=True)
    print(f"[*] Target Folder  : {os.path.abspath(TARGET_DIR)}", flush=True)
    print(f"[*] Manifest Output: {os.path.abspath(MANIFEST_PATH)}", flush=True)
    print("=" * 85, flush=True)

    manifest_records = []
    total_audio_ready = 0

    for genus, sp, common, is_endemic in FROZEN_TARGET_SPECIES:
        species_key = f"{genus}_{sp}"
        species_dir = os.path.join(TARGET_DIR, species_key)
        os.makedirs(species_dir, exist_ok=True)

        print(f"\n>>> Mengumpulkan: {genus} {sp} ({common}) {'[ENDEMIK SUMATERA]' if is_endemic else ''}", flush=True)
        recs = fetch_species_recordings(genus, sp)
        print(f"    Ditemukan {len(recs)} rekaman potensial di Indonesia.", flush=True)

        # Urutkan berdasarkan kualitas rekaman (A, B, C terlebih dahulu)
        quality_rank = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "no score": 5}
        recs.sort(key=lambda x: quality_rank.get(str(x.get("q", "")).upper(), 6))

        sp_downloaded = 0
        for rec in recs:
            rec_id = str(rec.get("id", ""))
            if not rec_id:
                continue

            dest_filename = f"XC{rec_id}_{species_key}.mp3"
            dest_path = os.path.join(species_dir, dest_filename)
            download_url = rec.get("file", "")
            quality = str(rec.get("q", "")).upper()
            recordist = rec.get("rec", "")
            rec_date = rec.get("date", "")
            rec_time = rec.get("time", "")
            country = rec.get("cnt", "Indonesia")
            locality = rec.get("loc", "")
            lat = rec.get("lat", "")
            lon = rec.get("lon", "")
            elevation = rec.get("elevation", "")
            length_s = rec.get("length", "")
            license_url = rec.get("lic", "")
            web_url = rec.get("url", f"https://xeno-canto.org/{rec_id}")

            # Cek ketersediaan file lokal
            file_ready = False
            status = "Pending"

            if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
                file_ready = True
                status = "Ready_Existing"
            else:
                existing_local = find_existing_file(rec_id, species_key)
                if existing_local and os.path.exists(existing_local):
                    try:
                        shutil.copy2(existing_local, dest_path)
                        file_ready = True
                        status = "Reused_Local"
                    except Exception:
                        pass

            # Jika belum ada lokal dan ada URL unduh, unduh audio (target kuota hingga 35 rekaman per spesies)
            if not file_ready and download_url and sp_downloaded < 35:
                try:
                    resp = requests.get(download_url, headers=HEADERS, timeout=40)
                    if resp.status_code == 200:
                        with open(dest_path, "wb") as f:
                            f.write(resp.content)
                        file_ready = True
                        status = "Downloaded_Fresh"
                        print(f"      [+] Terunduh XC{rec_id} (Q:{quality}, {length_s}s)", flush=True)
                        time.sleep(0.3)
                    else:
                        status = f"HTTP_{resp.status_code}"
                except Exception as e:
                    status = f"Error_{type(e).__name__}"

            sha256_hash = compute_sha256(dest_path) if file_ready else ""
            if file_ready:
                sp_downloaded += 1
                total_audio_ready += 1

            manifest_records.append({
                "id": rec_id,
                "species_key": species_key,
                "scientific_name": f"{genus} {sp}",
                "common_name": common,
                "is_endemic_sumatra": is_endemic,
                "quality": quality,
                "recordist": recordist,
                "date": rec_date,
                "time": rec_time,
                "country": country,
                "locality": locality,
                "latitude": lat,
                "longitude": lon,
                "elevation": elevation,
                "length_sec": length_s,
                "license": license_url,
                "url_page": web_url,
                "url_audio": download_url,
                "file_path": dest_path if file_ready else "",
                "sha256": sha256_hash,
                "status": status
            })

    # Simpan manifest ke CSV
    df_manifest = pd.DataFrame(manifest_records)
    df_manifest.to_csv(MANIFEST_PATH, index=False, encoding="utf-8")

    print("\n" + "=" * 85, flush=True)
    print("[+] SELESAI MENGUMPULKAN DATASET BURUNG TARGET SUMATERA!", flush=True)
    print(f"[*] Total Rekaman Terkatalog : {len(df_manifest)} entri", flush=True)
    print(f"[*] Total File Audio Siap    : {total_audio_ready} berkas", flush=True)
    print(f"[*] Manifest Tersimpan       : {MANIFEST_PATH}", flush=True)
    print("=" * 85, flush=True)


if __name__ == "__main__":
    main()
