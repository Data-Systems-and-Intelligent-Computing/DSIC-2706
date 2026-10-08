"""
Script: scripts/run_e4_domain_shift.py
Fungsi: Eksekusi Eksperimen E4 — Sensitivitas Profil Spektral Sumber Derau (Noise Spectral Profile Sensitivity).
Sesuai audit saintifik:
1. Membandingkan performa retrieval pada derau lapangan ITERA (E2) vs background soundscape tropis BirdCLEF (E4).
2. Memuat gallery embeddings dari results/features/clean_embeddings_{rep}.npz untuk efisiensi komputasi.
3. Menyimpan hasil evaluasi per-query mentah (raw query metrics) ke results/raw/E4_{rep}_raw.csv untuk memungkinkan bootstrap confidence intervals.
4. Menghasilkan tabel komparatif lengkap E2 vs E4 lintas seluruh representasi (R0, R1, R2, R3).
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import librosa

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocess import preprocess_audio, TARGET_SR, TARGET_SAMPLES
from src.embeddings import AudioRepresentationExtractor
from src.mix_noise import compute_signal_power
from src.retrieve import evaluate_retrieval_corpus

SPLIT_PATH = PROJECT_ROOT / "data/manifests/dataset_split.csv"
SOUNDSCAPE_DIR = PROJECT_ROOT / "data/BirdClef/train_soundscapes"
FEATURES_DIR = PROJECT_ROOT / "results/features"
PROCESSED_DIR = PROJECT_ROOT / "results/processed"
RAW_DIR = PROJECT_ROOT / "results/raw"
TABLES_DIR = PROJECT_ROOT / "paper/tables"

def get_soundscape_noise_segment(samples: int, seed: int = 42) -> np.ndarray:
    """Mengambil segmen acak dari dataset soundscape alam bebas BirdCLEF."""
    rng = np.random.default_rng(seed)
    ogg_files = sorted([f for f in os.listdir(SOUNDSCAPE_DIR) if f.endswith('.ogg')])
    selected = str(SOUNDSCAPE_DIR / ogg_files[rng.integers(0, len(ogg_files))])
    
    try:
        y, _ = librosa.load(selected, sr=TARGET_SR, mono=True)
        if len(y) >= samples:
            start = rng.integers(0, len(y) - samples + 1)
            return y[start:start + samples].astype(np.float32)
        else:
            repeats = int(np.ceil(samples / len(y)))
            y = np.tile(y, repeats)
            return y[:samples].astype(np.float32)
    except Exception as e:
        print(f"[-] Gagal membaca soundscape {selected}: {e}")
        return np.zeros(samples, dtype=np.float32)

def mix_with_soundscape(clean: np.ndarray, snr_db: float, seed: int = 42) -> np.ndarray:
    """Mencampur sinyal dengan derau soundscape pada rasio SNR tertentu secara eksak."""
    noise = get_soundscape_noise_segment(samples=len(clean), seed=seed)
    
    p_signal = compute_signal_power(clean)
    p_noise = compute_signal_power(noise)
    
    if p_signal <= 1e-12 or p_noise <= 1e-12:
        return clean
        
    target_p_noise = p_signal / (10.0 ** (snr_db / 10.0))
    alpha = np.sqrt(target_p_noise / p_noise)
    noisy = clean + alpha * noise
    
    max_amp = np.max(np.abs(noisy))
    if max_amp > 1.0:
        noisy = noisy / max_amp
        
    return noisy.astype(np.float32)

def main():
    print("=" * 80)
    print("[*] MEMULAI EKSEKUSI E4: SENSITIVITAS PROFIL SPEKTRAL DERAU (SOUNDSCAPE VS ITERA)")
    print("=" * 80)

    if not SOUNDSCAPE_DIR.exists():
        raise FileNotFoundError(f"Direktori soundscape tidak ditemukan di {SOUNDSCAPE_DIR}!")

    df_split = pd.read_csv(SPLIT_PATH)
    gallery_df = df_split[df_split['split_role'] == 'gallery'].reset_index(drop=True)
    query_df = df_split[df_split['split_role'] == 'query_clean'].reset_index(drop=True)

    print(f"[*] Total Galeri: {len(gallery_df)}, Total Kueri: {len(query_df)}")

    # Muat audio bersih kueri
    print("[*] Memuat sinyal kueri bersih...")
    query_audios = [preprocess_audio(r['file_path']) for _, r in query_df.iterrows()]
    query_labels = list(query_df['species_key'])
    gallery_labels = list(gallery_df['species_key'])

    snr_list = [20, 10, 0, -5]
    representations = ["R0", "R1", "R2", "R3"]

    e4_summary_rows = []

    # Muat tabel E2 untuk perbandingan side-by-side
    e2_table_path = PROCESSED_DIR / "snr_robustness_table.csv"
    df_e2 = pd.read_csv(e2_table_path)

    for rep in representations:
        print(f"\n" + "-" * 60)
        print(f"[*] MEMPROSES E4 REPRESENTASI [{rep}]")
        print("-" * 60)

        # Muat galeri yang sudah tersimpan
        feat_path = FEATURES_DIR / f"clean_embeddings_{rep}.npz"
        feat_data = np.load(feat_path)
        gallery_embs = feat_data["gal_feats"]
        clean_query_embs = feat_data["qry_feats"]

        extractor = AudioRepresentationExtractor(rep)

        # Baseline Clean
        clean_summary, clean_raw = evaluate_retrieval_corpus(
            clean_query_embs, query_labels, gallery_embs, gallery_labels
        )
        clean_map = clean_summary["mAP@10"]
        print(f"    [Clean] mAP@10: {clean_map:.4f}, Top1: {clean_summary['mean_top1']:.4f}")

        e4_raw_records = []
        for i, q_raw in enumerate(clean_raw):
            row_dict = dict(q_raw)
            row_dict["query_id"] = query_df.iloc[i]["recording_id"]
            row_dict["species_key"] = query_df.iloc[i]["species_key"]
            row_dict["condition"] = "Clean"
            row_dict["snr_db"] = 999
            row_dict["representation"] = rep
            e4_raw_records.append(row_dict)

        # Ambil baseline E2 clean untuk perbandingan
        e2_clean_row = df_e2[(df_e2["representation"] == rep) & (df_e2["condition"] == "Clean")].iloc[0]

        e4_summary_rows.append({
            "representation": rep,
            "condition": "Clean",
            "snr_db": 999,
            "mAP@10_E4_Soundscape": clean_map,
            "Top1_E4": clean_summary["mean_top1"],
            "mAP@10_E2_ITERA": e2_clean_row["mAP@10"],
            "delta_mAP10_E4_minus_E2": clean_map - e2_clean_row["mAP@10"],
            "retention_E4": 1.0,
            "retention_E2": 1.0
        })

        # Evaluasi per level SNR
        for snr in snr_list:
            noisy_embs = []
            for i, y_clean in enumerate(query_audios):
                y_noisy = mix_with_soundscape(y_clean, snr_db=snr, seed=100 + i)
                noisy_embs.append(extractor.extract(y_noisy))
            noisy_embs = np.array(noisy_embs)

            noisy_summary, noisy_raw = evaluate_retrieval_corpus(
                noisy_embs, query_labels, gallery_embs, gallery_labels
            )
            noisy_map = noisy_summary["mAP@10"]
            retention_e4 = noisy_map / max(clean_map, 1e-6)

            # Cari baris E2 yang bersesuaian
            e2_noisy_row = df_e2[(df_e2["representation"] == rep) & (df_e2["condition"] == f"SNR_{snr}dB")].iloc[0]
            delta_map = noisy_map - e2_noisy_row["mAP@10"]

            print(f"    [SNR {snr:3d} dB] E4 Soundscape: {noisy_map:.4f} (Ret: {retention_e4*100:.1f}%) | "
                  f"E2 ITERA: {e2_noisy_row['mAP@10']:.4f} | Gap (E4-E2): {delta_map:+.4f}")

            for i, q_raw in enumerate(noisy_raw):
                row_dict = dict(q_raw)
                row_dict["query_id"] = query_df.iloc[i]["recording_id"]
                row_dict["species_key"] = query_df.iloc[i]["species_key"]
                row_dict["condition"] = f"SNR_{snr}dB"
                row_dict["snr_db"] = snr
                row_dict["representation"] = rep
                e4_raw_records.append(row_dict)

            e4_summary_rows.append({
                "representation": rep,
                "condition": f"SNR_{snr}dB",
                "snr_db": snr,
                "mAP@10_E4_Soundscape": noisy_map,
                "Top1_E4": noisy_summary["mean_top1"],
                "mAP@10_E2_ITERA": e2_noisy_row["mAP@10"],
                "delta_mAP10_E4_minus_E2": delta_map,
                "retention_E4": retention_e4,
                "retention_E2": e2_noisy_row["relative_retention"]
            })

        # Simpan raw query file untuk representasi ini
        df_raw_rep = pd.DataFrame(e4_raw_records)
        raw_out_path = RAW_DIR / f"E4_{rep}_raw.csv"
        df_raw_rep.to_csv(raw_out_path, index=False)
        print(f"    [+] Disimpan raw per-query E4: {raw_out_path}")

    # Simpan tabel ringkasan komparatif E4
    df_e4_summary = pd.DataFrame(e4_summary_rows)
    df_e4_summary.to_csv(PROCESSED_DIR / "e4_domain_shift_table.csv", index=False)
    df_e4_summary.to_csv(TABLES_DIR / "e4_domain_shift_table.csv", index=False)
    print(f"\n[+] Sukses menyimpan tabel komparatif E4: {PROCESSED_DIR / 'e4_domain_shift_table.csv'}")

if __name__ == "__main__":
    main()
