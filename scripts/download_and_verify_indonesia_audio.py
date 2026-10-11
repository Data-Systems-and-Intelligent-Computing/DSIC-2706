"""
Script: scripts/download_and_verify_indonesia_audio.py
Fungsi: Mengunduh 1.217 berkas audio MP3 resmi dari Xeno-Canto untuk 20 kandidat
        spesies burung Indonesia, memverifikasi integritas fisik audio (SHA-256,
        durasi, sampling rate, keterdekodean), dan mencatat log audit lengkap.
"""

import os
import sys
import time
import hashlib
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib.request
import pandas as pd
import numpy as np
import librosa
import soundfile as sf

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = PROJECT_ROOT / "data" / "manifests"
AUDIO_DIR = PROJECT_ROOT / "data" / "xeno_canto_indonesia"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

INPUT_CSV = MANIFEST_DIR / "indonesia_train.csv"
AUDIT_LOG_CSV = MANIFEST_DIR / "download_audit_log.csv"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) DSIC-2706-Research/1.0"


def download_and_verify_single(row):
    """
    Mengunduh satu file MP3 dari Xeno-Canto dan memverifikasi integritas fisiknya.
    """
    rec_id = str(row["url"]).split("/")[-1].strip()
    sp_key = str(row["primary_label"]).strip()
    sci_name = str(row["scientific_name"]).strip()
    author_name = str(row["author"]).strip()
    
    target_sp_dir = AUDIO_DIR / sp_key
    target_sp_dir.mkdir(parents=True, exist_ok=True)
    out_file = target_sp_dir / f"XC{rec_id}.mp3"

    download_url = f"https://xeno-canto.org/{rec_id}/download"
    result = {
        "recording_id": f"XC{rec_id}",
        "species_key": sp_key,
        "scientific_name": sci_name,
        "author": author_name,
        "file_path": str(out_file.relative_to(PROJECT_ROOT)).replace("\\", "/"),
        "status": "FAILED",
        "http_code": None,
        "bytes": 0,
        "sha256": None,
        "duration_sec": 0.0,
        "sr_native": None,
        "is_decodable": False,
        "error_msg": None
    }

    # Jika file sudah ada di disk dan valid, langsung verifikasi lokal
    if out_file.exists() and out_file.stat().st_size > 1024:
        try:
            with open(out_file, "rb") as f:
                data = f.read()
            result["bytes"] = len(data)
            result["sha256"] = hashlib.sha256(data).hexdigest()
            y, sr = librosa.load(str(out_file), sr=None, mono=True)
            result["duration_sec"] = round(len(y) / sr, 2)
            result["sr_native"] = int(sr)
            result["is_decodable"] = True
            result["status"] = "VERIFIED_EXISTING"
            return result
        except Exception:
            pass  # Unduh ulang jika corrupt

    # Lakukan pengunduhan via HTTP
    retries = 3
    while retries > 0:
        try:
            req = urllib.request.Request(download_url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=20) as resp:
                result["http_code"] = resp.status
                if resp.status == 200:
                    data = resp.read()
                    if len(data) < 1000:
                        raise ValueError(f"Ukuran berkas terlalu kecil ({len(data)} bytes, kemungkinan error page)")
                    
                    # Simpan data biner ke disk
                    with open(out_file, "wb") as f:
                        f.write(data)
                    
                    result["bytes"] = len(data)
                    result["sha256"] = hashlib.sha256(data).hexdigest()
                    
                    # Verifikasi keterdekodean audio nyata
                    y, sr = librosa.load(str(out_file), sr=None, mono=True)
                    result["duration_sec"] = round(len(y) / sr, 2)
                    result["sr_native"] = int(sr)
                    result["is_decodable"] = True
                    result["status"] = "SUCCESS"
                    return result
                else:
                    raise urllib.error.HTTPError(download_url, resp.status, "Non-200 status", resp.headers, None)
        except Exception as e:
            retries -= 1
            if retries == 0:
                result["error_msg"] = str(e)
                if out_file.exists():
                    out_file.unlink(missing_ok=True)
                return result
            time.sleep(1.0)

    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Batas unduhan untuk pengujian (misal 5)")
    parser.add_argument("--workers", type=int, default=4, help="Jumlah thread worker paralel (default: 4)")
    args = parser.parse_args()

    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Berkas manifes {INPUT_CSV} tidak ditemukan!")

    df = pd.read_csv(INPUT_CSV)
    if args.limit:
        df = df.head(args.limit)

    total_tasks = len(df)
    print("=" * 80)
    print(f"[*] MEMULAI PENGUNDUHAN & VERIFIKASI AUDIO BURUNG INDONESIA ({total_tasks:,} klip)")
    print(f"[*] Target Direktori: {AUDIO_DIR}")
    print(f"[*] Thread Workers: {args.workers}")
    print("=" * 80)

    results = []
    completed = 0
    success_count = 0

    rows = df.to_dict(orient="records")

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(download_and_verify_single, r): r for r in rows}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            completed += 1
            if res["status"] in ["SUCCESS", "VERIFIED_EXISTING"]:
                success_count += 1
            
            if completed % 25 == 0 or completed == total_tasks:
                print(f"[-] Progres: {completed}/{total_tasks} ({completed/total_tasks*100:.1f}%) | Berhasil: {success_count} | Gagal: {completed - success_count}")

    # Simpan log audit ke CSV
    df_audit = pd.DataFrame(results)
    df_audit.sort_values(by=["species_key", "recording_id"], inplace=True)
    df_audit.to_csv(AUDIT_LOG_CSV, index=False)
    print(f"\n[+] Seluruh log audit unduhan disimpan ke: {AUDIT_LOG_CSV}")

    # Rekapitulasi per spesies
    print("\n" + "=" * 80)
    print("[*] REKAPITULASI HASIL VERIFIKASI PER SPESIES:")
    print("=" * 80)
    summary = df_audit[df_audit["status"].isin(["SUCCESS", "VERIFIED_EXISTING"])].groupby(
        ["species_key", "scientific_name"]
    ).agg(
        klip_berhasil=("recording_id", "count"),
        author_berhasil=("author", "nunique"),
        durasi_median=("duration_sec", "median"),
        min_durasi=("duration_sec", "min"),
        max_durasi=("duration_sec", "max")
    ).reset_index()

    print(summary.to_string(index=False))

    # Cek apakah ada spesies yang jatuh di bawah ambang DEC-10
    dropped = summary[(summary["klip_berhasil"] < 20) | (summary["author_berhasil"] < 5)]
    if len(dropped) > 0:
        print("\n[!] PERINGATAN: Terdapat spesies yang jatuh di bawah ambang batas DEC-10:")
        print(dropped.to_string(index=False))
    else:
        print("\n[+] SELURUH SPESIES MEMENUHI AMBANG DEC-10 DENGAN SEMPURNA!")

if __name__ == "__main__":
    main()
