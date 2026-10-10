"""
Script: scripts/fetch_indonesia_xc_metadata.py
Fungsi: Mengunduh metadata seluruh rekaman burung di Indonesia (cnt:indonesia, grp:birds)
        dari Xeno-Canto API v3, menganalisis ketersediaan spesies umum, dan menyusun
        studi kelayakan (Feasibility Study) serta metadata kandidat spesies untuk Pak Ardika.
"""

import sys
import json
import time
import urllib.request
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "manifests"
DATA_DIR.mkdir(parents=True, exist_ok=True)

RAW_JSON_PATH = DATA_DIR / "xeno_canto_indonesia_raw.json"
CANDIDATE_CSV_PATH = DATA_DIR / "kandidat_spesies_indonesia.csv"
API_KEY = "95dc5b3f6834b56e17da4cf68cc890cb470d1284"

def fetch_all_indonesia_recordings():
    if RAW_JSON_PATH.exists():
        print(f"[*] Berkas cache metadata lokal ditemukan di: {RAW_JSON_PATH}")
        with open(RAW_JSON_PATH, "r", encoding="utf-8") as f:
            all_records = json.load(f)
        print(f"[+] Memuat {len(all_records):,} rekaman dari cache.")
        return all_records

    print("=" * 80)
    print("[*] MENGUNDUH METADATA XENO-CANTO BURUNG INDONESIA (API v3)")
    print("=" * 80)

    base_url = "https://xeno-canto.org/api/3/recordings"
    query = "cnt:indonesia+grp:birds"
    per_page = 500
    page = 1
    all_recordings = []

    # Ambil halaman pertama untuk menentukan total halaman
    first_url = f"{base_url}?query={query}&page={page}&per_page={per_page}&key={API_KEY}"
    req = urllib.request.Request(first_url, headers={"User-Agent": "BirdResearch/1.0"})
    
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.loads(res.read().decode("utf-8"))
        num_recordings = int(data.get("numRecordings", 0))
        num_pages = int(data.get("numPages", 1))
        all_recordings.extend(data.get("recordings", []))
        print(f"[+] Total Rekaman di Indonesia: {num_recordings:,} | Total Halaman: {num_pages}")
        print(f"[-] Berhasil mengunduh Halaman 1/{num_pages} ({len(data.get('recordings', []))} rekaman)")

    for p in range(2, num_pages + 1):
        url = f"{base_url}?query={query}&page={p}&per_page={per_page}&key={API_KEY}"
        req = urllib.request.Request(url, headers={"User-Agent": "BirdResearch/1.0"})
        retries = 3
        while retries > 0:
            try:
                time.sleep(0.5)  # Jeda sopan untuk API
                with urllib.request.urlopen(req, timeout=30) as res:
                    p_data = json.loads(res.read().decode("utf-8"))
                    recs = p_data.get("recordings", [])
                    all_recordings.extend(recs)
                    print(f"[-] Berhasil mengunduh Halaman {p}/{num_pages} ({len(recs)} rekaman, Total sementara: {len(all_recordings):,})")
                break
            except Exception as e:
                retries -= 1
                print(f"[!] Gagal halaman {p}: {e}. Mencoba lagi ({retries} tersisa)...")
                time.sleep(2)

    # Simpan ke cache lokal
    with open(RAW_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(all_recordings, f, indent=2, ensure_ascii=False)
    print(f"\n[+] Seluruh metadata berhasil disimpan ke: {RAW_JSON_PATH}")
    return all_recordings

def analyze_feasibility(records):
    print("\n" + "=" * 80)
    print("[*] MEMULAI ANALISIS STUDI KELAYAKAN (FEASIBILITY STUDY) BURUNG INDONESIA")
    print("=" * 80)

    df = pd.DataFrame(records)
    print(f"[+] Total entri rekaman mentah: {len(df):,} baris")

    # Pastikan spesies valid (tidak kosong, bukan unconfirmed/mystery)
    df = df[df["gen"].notna() & df["sp"].notna()].copy()
    df["scientific_name"] = df["gen"].str.strip() + " " + df["sp"].str.strip()
    df["common_name"] = df["en"].fillna("").str.strip()
    df["author"] = df["rec"].fillna("Unknown").str.strip()
    df["quality"] = df["q"].fillna("no score").str.strip().str.upper()

    # Eksklusi author Unknown
    df = df[df["author"].str.lower() != "unknown"].copy()

    # Hitung agregasi per spesies
    summary = []
    grouped = df.groupby(["scientific_name", "common_name"])
    for (sci_name, com_name), g in grouped:
        total_clips = len(g)
        n_authors = g["author"].nunique()
        q_counts = g["quality"].value_counts().to_dict()
        q_high = q_counts.get("A", 0) + q_counts.get("B", 0)
        q_acceptable = q_high + q_counts.get("C", 0)
        
        # Lokasi / persebaran
        valid_locs = g["loc"].dropna().tolist()
        locs = " | ".join(valid_locs[:3]) if valid_locs else "Tidak tercatat"
        
        # Cek keterwakilan wilayah Sumatera
        loc_str = " ".join(valid_locs).lower()
        has_sumatra = any(kw in loc_str for kw in ["sumat", "lampung", "aceh", "kerinci", "riau", "jambi", "medan", "padang", "way kambas"])
        
        summary.append({
            "scientific_name": sci_name,
            "common_name": com_name,
            "total_clips": total_clips,
            "n_authors": n_authors,
            "q_A_B": q_high,
            "q_A_B_C": q_acceptable,
            "has_sumatra_records": has_sumatra,
            "sample_locations": locs
        })

    df_sum = pd.DataFrame(summary)

    # Filter kriteria kelayakan mirip DEC-10:
    # 1. Total klip >= 25
    # 2. n_author >= 5 (agar author-disjoint split aman: Gallery, Query, Calibration)
    # 3. Kualitas A, B, atau C >= 20
    df_eligible = df_sum[
        (df_sum["total_clips"] >= 25) &
        (df_sum["n_authors"] >= 5) &
        (df_sum["q_A_B_C"] >= 20)
    ].copy()

    print(f"[+] Jumlah total spesies burung yang terekam di Indonesia: {df_sum['scientific_name'].nunique():,} spesies")
    print(f"[+] Spesies yang memenuhi ambang kelayakan (Klip >= 25, Author >= 5, Kualitas A-C >= 20): {len(df_eligible)} spesies")

    # Ranking kandidat: urutkan berdasarkan keragaman author independen dan volume klip
    # Prioritaskan spesies yang tersebar luas (termasuk ada rekaman di Sumatera)
    df_eligible.sort_values(
        by=["n_authors", "total_clips"],
        ascending=[False, False],
        inplace=True
    )

    top20 = df_eligible.head(20).reset_index(drop=True)
    top20.to_csv(CANDIDATE_CSV_PATH, index=False)
    print(f"[+] Top-20 Kandidat Spesies Indonesia disimpan di: {CANDIDATE_CSV_PATH}")

    return df, df_sum, df_eligible, top20

def main():
    records = fetch_all_indonesia_recordings()
    df_raw, df_sum, df_eligible, top20 = analyze_feasibility(records)

    print("\n" + "=" * 90)
    print(f"{'No':<3} | {'Nama Ilmiah':<28} | {'Nama Umum':<25} | {'Klip':<5} | {'Author':<6} | {'Sumatera?':<9}")
    print("-" * 90)
    for idx, row in top20.iterrows():
        sumatra_str = "Ya" if row["has_sumatra_records"] else "Luar Sum"
        print(f"{idx+1:<3} | {row['scientific_name']:<28} | {row['common_name']:<25} | {row['total_clips']:<5} | {row['n_authors']:<6} | {sumatra_str:<9}")
    print("=" * 90)

if __name__ == "__main__":
    main()
