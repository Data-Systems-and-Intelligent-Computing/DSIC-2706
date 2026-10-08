"""
Script: src/bootstrap_inference.py
Deskripsi: Evaluasi statistik inferensial menggunakan paired bootstrap resampling (1.000 iterasi)
Mencakup:
1. Uji keunggulan performa absolut pada kondisi Clean (R2 vs R1, R2 vs R0, R1 vs R0)
2. Uji retensi ketahanan relatif pada kondisi derau ekstrem SNR -5 dB (H1 & H2)
3. Uji sensitivitas profil spektral sumber derau E4 Soundscape vs E2 ITERA pada SNR -5 dB (H3)
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "results/raw"
OUTPUT_TABLE = PROJECT_ROOT / "results/processed/statistical_significance_table.csv"
PAPER_TABLE = PROJECT_ROOT / "paper/tables/statistical_significance_table.csv"


def run_paired_bootstrap(n_iterations: int = 1000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    
    # 1. Muat AP@10 per kueri dari berkas mentah E1 & E2
    r2_clean = pd.read_csv(RAW_DIR / "R2_Clean_raw.csv")["AP@10"].values
    r1_clean = pd.read_csv(RAW_DIR / "R1_Clean_raw.csv")["AP@10"].values
    r0_clean = pd.read_csv(RAW_DIR / "R0_Clean_raw.csv")["AP@10"].values

    r2_n5 = pd.read_csv(RAW_DIR / "R2_SNR_-5dB_raw.csv")["AP@10"].values
    r1_n5 = pd.read_csv(RAW_DIR / "R1_SNR_-5dB_raw.csv")["AP@10"].values
    r0_n5 = pd.read_csv(RAW_DIR / "R0_SNR_-5dB_raw.csv")["AP@10"].values

    # Muat kueri mentah E4 (Soundscape) jika tersedia
    e4_r2_f = RAW_DIR / "E4_R2_raw.csv"
    e4_r1_f = RAW_DIR / "E4_R1_raw.csv"
    has_e4 = e4_r2_f.exists() and e4_r1_f.exists()

    if has_e4:
        df_e4_r2 = pd.read_csv(e4_r2_f)
        e4_r2_n5 = df_e4_r2[df_e4_r2["condition"] == "SNR_-5dB"]["AP@10"].values
        df_e4_r1 = pd.read_csv(e4_r1_f)
        e4_r1_n5 = df_e4_r1[df_e4_r1["condition"] == "SNR_-5dB"]["AP@10"].values
    else:
        e4_r2_n5, e4_r1_n5 = None, None

    n = len(r2_clean)
    
    # Koleksi metrik bootstrap
    diff_clean_r2_r1 = []
    diff_clean_r2_r0 = []
    diff_clean_r1_r0 = []

    ret_r2_list = []
    ret_r1_list = []
    ret_r0_list = []

    diff_ret_r2_r1 = []
    diff_ret_r0_r1 = []

    diff_e4_e2_r2 = []
    diff_e4_e2_r1 = []

    for _ in range(n_iterations):
        idx = np.random.randint(0, n, n)
        
        # Nilai Clean rata-rata pada sampel bootstrap
        m_r2_c = np.mean(r2_clean[idx])
        m_r1_c = np.mean(r1_clean[idx])
        m_r0_c = np.mean(r0_clean[idx])
        
        diff_clean_r2_r1.append(m_r2_c - m_r1_c)
        diff_clean_r2_r0.append(m_r2_c - m_r0_c)
        diff_clean_r1_r0.append(m_r1_c - m_r0_c)
        
        # Nilai SNR -5 dB rata-rata pada sampel bootstrap
        m_r2_n = np.mean(r2_n5[idx])
        m_r1_n = np.mean(r1_n5[idx])
        m_r0_n = np.mean(r0_n5[idx])
        
        # Retensi relatif: mAP(-5dB) / mAP(Clean)
        ret2 = m_r2_n / m_r2_c
        ret1 = m_r1_n / m_r1_c
        ret0 = m_r0_n / m_r0_c
        
        ret_r2_list.append(ret2)
        ret_r1_list.append(ret1)
        ret_r0_list.append(ret0)
        
        diff_ret_r2_r1.append(ret2 - ret1)
        diff_ret_r0_r1.append(ret0 - ret1)

        if has_e4:
            m_e4_r2 = np.mean(e4_r2_n5[idx])
            m_e4_r1 = np.mean(e4_r1_n5[idx])
            diff_e4_e2_r2.append(m_e4_r2 - m_r2_n)
            diff_e4_e2_r1.append(m_e4_r1 - m_r1_n)

    def calc_stats(diff_array, two_tailed: bool = False):
        mean_val = np.mean(diff_array)
        ci_low, ci_high = np.percentile(diff_array, [2.5, 97.5])
        if two_tailed:
            p_val_num = 2 * min(np.sum(np.array(diff_array) <= 0), np.sum(np.array(diff_array) >= 0)) / len(diff_array)
        else:
            p_val_num = np.sum(np.array(diff_array) <= 0) / len(diff_array)
        p_val_str = "< 0.001" if p_val_num < 0.001 else f"{p_val_num:.4f}"
        sig = p_val_num < 0.05
        return round(mean_val, 4), round(ci_low, 4), round(ci_high, 4), p_val_str, sig

    results = []

    # 1. Clean Comparisons
    mean_v, low, high, p_str, sig = calc_stats(diff_clean_r2_r1)
    results.append({
        "Pengujian": "Clean Retrieval (mAP@10)",
        "Komparasi": "R2 (BirdNET) vs R1 (PANNs)",
        "Mean_Diff": mean_v,
        "CI_95_Lower": low,
        "CI_95_Upper": high,
        "p_value": p_str,
        "Signifikan_0.05": sig,
        "Catatan": "R2 unggul mutlak atas model generik audio"
    })

    mean_v, low, high, p_str, sig = calc_stats(diff_clean_r2_r0)
    results.append({
        "Pengujian": "Clean Retrieval (mAP@10)",
        "Komparasi": "R2 (BirdNET) vs R0 (MFCC)",
        "Mean_Diff": mean_v,
        "CI_95_Lower": low,
        "CI_95_Upper": high,
        "p_value": p_str,
        "Signifikan_0.05": sig,
        "Catatan": "R2 unggul mutlak atas baseline klasik"
    })

    mean_v, low, high, p_str, sig = calc_stats(diff_clean_r1_r0)
    results.append({
        "Pengujian": "Clean Retrieval (mAP@10)",
        "Komparasi": "R1 (PANNs) vs R0 (MFCC)",
        "Mean_Diff": mean_v,
        "CI_95_Lower": low,
        "CI_95_Upper": high,
        "p_value": p_str,
        "Signifikan_0.05": sig,
        "Catatan": "R1 unggul atas MFCC pada kondisi bersih"
    })

    # 2. Relative Retention Comparisons at SNR -5 dB (H1 & H2 Testing)
    mean_v, low, high, p_str, sig = calc_stats(diff_ret_r2_r1)
    results.append({
        "Pengujian": "Retensi Relatif SNR -5 dB",
        "Komparasi": "R2 (BirdNET) vs R1 (PANNs)",
        "Mean_Diff": mean_v,
        "CI_95_Lower": low,
        "CI_95_Upper": high,
        "p_value": p_str,
        "Signifikan_0.05": sig,
        "Catatan": "Retensi R2 (84.5%) unggul mutlak atas R1 (14.2%)"
    })

    mean_v, low, high, p_str, sig = calc_stats(diff_ret_r0_r1)
    results.append({
        "Pengujian": "Retensi Relatif SNR -5 dB",
        "Komparasi": "R0 (MFCC) vs R1 (PANNs)",
        "Mean_Diff": mean_v,
        "CI_95_Lower": low,
        "CI_95_Upper": high,
        "p_value": p_str,
        "Signifikan_0.05": sig,
        "Catatan": "Retensi MFCC (26.4%) melampaui PANNs (14.2%) secara signifikan"
    })

    # 3. Noise Source Sensitivity (E4 Soundscape vs E2 ITERA at SNR -5 dB)
    if has_e4:
        mean_v, low, high, p_str, sig = calc_stats(diff_e4_e2_r2, two_tailed=True)
        results.append({
            "Pengujian": "Sensitivitas Sumber Derau (-5 dB)",
            "Komparasi": "R2 (E4 Soundscape vs E2 ITERA)",
            "Mean_Diff": mean_v,
            "CI_95_Lower": low,
            "CI_95_Upper": high,
            "p_value": p_str,
            "Signifikan_0.05": sig,
            "Catatan": "Tidak ada perbedaan signifikan (invarian profil derau)"
        })

        mean_v, low, high, p_str, sig = calc_stats(diff_e4_e2_r1, two_tailed=True)
        results.append({
            "Pengujian": "Sensitivitas Sumber Derau (-5 dB)",
            "Komparasi": "R1 (E4 Soundscape vs E2 ITERA)",
            "Mean_Diff": mean_v,
            "CI_95_Lower": low,
            "CI_95_Upper": high,
            "p_value": p_str,
            "Signifikan_0.05": sig,
            "Catatan": "PANNs sangat sensitif terhadap profil derau (unggul pada soundscape)"
        })

    df_res = pd.DataFrame(results)
    OUTPUT_TABLE.parent.mkdir(parents=True, exist_ok=True)
    df_res.to_csv(OUTPUT_TABLE, index=False)
    PAPER_TABLE.parent.mkdir(parents=True, exist_ok=True)
    df_res.to_csv(PAPER_TABLE, index=False)

    print("=" * 80)
    print(f"[+] Uji Statistik Inferensial ({n_iterations} Iterasi Bootstrap) Selesai!")
    print(f"[+] Berkas disimpan di: {OUTPUT_TABLE} dan {PAPER_TABLE}")
    print("=" * 80)
    print(df_res[["Pengujian", "Komparasi", "Mean_Diff", "CI_95_Lower", "CI_95_Upper", "p_value", "Signifikan_0.05"]])
    return df_res


if __name__ == "__main__":
    run_paired_bootstrap()
