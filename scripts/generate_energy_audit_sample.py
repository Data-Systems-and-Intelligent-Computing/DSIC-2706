"""
Script: scripts/generate_energy_audit_sample.py
Fungsi: Membangun daftar sampel deterministik 50 klip audio (seed=42)
        dari dataset 1.217 rekaman untuk audit aural fungsi select_highest_energy_window:
        - 40 klip berdurasi panjang (> 60 detik, maks 693 detik)
        - 10 klip berdurasi pendek (< 5 detik)
        Output disimpan di data/manifests/energy_audit_50_sample.csv
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOWNLOAD_MANIFEST = PROJECT_ROOT / "data" / "manifests" / "download_manifest.csv"
OUTPUT_SAMPLE = PROJECT_ROOT / "data" / "manifests" / "energy_audit_50_sample.csv"

def generate_audit_sample():
    df = pd.read_csv(DOWNLOAD_MANIFEST)
    
    long_clips = df[df["duration_sec"] > 60].copy()
    short_clips = df[df["duration_sec"] < 5.0].copy()
    
    # 40 klip panjang dipilih secara deterministik dengan seed 42 (stratifikasi per spesies jika memungkinkan)
    sampled_long = long_clips.sample(n=40, random_state=42).copy()
    sampled_long["audit_category"] = "long_duration (>60s)"
    
    # 10 klip pendek dipilih secara deterministik dengan seed 42
    sampled_short = short_clips.sample(n=10, random_state=42).copy()
    sampled_short["audit_category"] = "short_duration (<5s)"
    
    sample_df = pd.concat([sampled_long, sampled_short], ignore_index=True)
    sample_df["audit_checklist"] = "[ ] Vokalisasi target dominan / bukan derau angin / handling noise"
    
    cols = [
        "recording_id",
        "species_key",
        "scientific_name",
        "author",
        "duration_sec",
        "audit_category",
        "audit_checklist"
    ]
    sample_df = sample_df[cols]
    sample_df.to_csv(OUTPUT_SAMPLE, index=False)
    print(f"[+] Berhasil membuat {len(sample_df)} sampel audit di {OUTPUT_SAMPLE}")
    print(f"    - Klip durasi panjang: {len(sampled_long)} berkas (rentang {sampled_long['duration_sec'].min():.1f}s - {sampled_long['duration_sec'].max():.1f}s)")
    print(f"    - Klip durasi pendek: {len(sampled_short)} berkas (rentang {sampled_short['duration_sec'].min():.1f}s - {sampled_short['duration_sec'].max():.1f}s)")

if __name__ == "__main__":
    generate_audit_sample()
