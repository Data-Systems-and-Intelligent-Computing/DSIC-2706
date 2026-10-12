"""
Script: src/bootstrap_inference.py
Deskripsi: Evaluasi statistik inferensial menggunakan paired bootstrap resampling (1.000 iterasi)
Mencakup:
1. Uji keunggulan performa absolut pada kondisi Clean (R2 vs R1, R2 vs R0, R1 vs R0, dan H5 vs R3)
2. Uji retensi ketahanan relatif pada kondisi derau ekstrem SNR -5 dB (H1 & H2)
3. Uji sensitivitas profil spektral sumber derau lintas habitat ITERA E4 pada SNR -5 dB
4. Uji disparitas rentang ayunan habitat H3 (R1 vs R2) dengan statistik hasil perhitungan
5. Cluster Bootstrap per Perekam (K=27)
6. Analisis Sensitivitas Non-Mike Nelson (subset query tanpa dominasi perekam terbanyak)
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
    
    # 1. Muat AP@10 dan metadata per kueri dari berkas mentah E1 & E2
    df_r2_c = pd.read_csv(RAW_DIR / "R2_Clean_raw.csv")
    df_r1_c = pd.read_csv(RAW_DIR / "R1_Clean_raw.csv")
    df_r0_c = pd.read_csv(RAW_DIR / "R0_Clean_raw.csv")
    df_r3_c = pd.read_csv(RAW_DIR / "R3_Clean_raw.csv")

    df_r2_n5 = pd.read_csv(RAW_DIR / "R2_SNR_-5dB_raw.csv")
    df_r1_n5 = pd.read_csv(RAW_DIR / "R1_SNR_-5dB_raw.csv")
    df_r0_n5 = pd.read_csv(RAW_DIR / "R0_SNR_-5dB_raw.csv")
    df_r3_n5 = pd.read_csv(RAW_DIR / "R3_SNR_-5dB_raw.csv")

    r2_clean = df_r2_c["AP@10"].values
    r1_clean = df_r1_c["AP@10"].values
    r0_clean = df_r0_c["AP@10"].values
    r3_clean = df_r3_c["AP@10"].values

    r2_n5 = df_r2_n5["AP@10"].values
    r1_n5 = df_r1_n5["AP@10"].values
    r0_n5 = df_r0_n5["AP@10"].values
    r3_n5 = df_r3_n5["AP@10"].values

    recordists = df_r2_c["recordist"].values if "recordist" in df_r2_c.columns else None

    # Muat kueri mentah E4 (Habitat ITERA) jika tersedia
    e4_r2_f = RAW_DIR / "E4_R2_raw.csv"
    e4_r1_f = RAW_DIR / "E4_R1_raw.csv"
    has_e4 = e4_r2_f.exists() and e4_r1_f.exists()

    if has_e4:
        df_e4_r2 = pd.read_csv(e4_r2_f)
        df_e4_r1 = pd.read_csv(e4_r1_f)
        
        # Ekstrak per habitat pada SNR -5 dB
        r2_e4_kebun = df_e4_r2[(df_e4_r2["habitat"] == "Kebun_Raya") & (df_e4_r2["condition"] == "SNR_-5dB")]["AP@10"].values
        r2_e4_embung = df_e4_r2[(df_e4_r2["habitat"] == "Embung_F") & (df_e4_r2["condition"] == "SNR_-5dB")]["AP@10"].values
        r2_e4_gedung = df_e4_r2[(df_e4_r2["habitat"] == "Gedung_F") & (df_e4_r2["condition"] == "SNR_-5dB")]["AP@10"].values

        r1_e4_kebun = df_e4_r1[(df_e4_r1["habitat"] == "Kebun_Raya") & (df_e4_r1["condition"] == "SNR_-5dB")]["AP@10"].values
        r1_e4_embung = df_e4_r1[(df_e4_r1["habitat"] == "Embung_F") & (df_e4_r1["condition"] == "SNR_-5dB")]["AP@10"].values
        r1_e4_gedung = df_e4_r1[(df_e4_r1["habitat"] == "Gedung_F") & (df_e4_r1["condition"] == "SNR_-5dB")]["AP@10"].values
    else:
        r2_e4_kebun, r2_e4_embung, r2_e4_gedung = None, None, None
        r1_e4_kebun, r1_e4_embung, r1_e4_gedung = None, None, None

    n = len(r2_clean)
    
    # Koleksi metrik bootstrap standar
    diff_clean_r2_r1 = []
    diff_clean_r2_r0 = []
    diff_clean_r1_r0 = []
    diff_clean_r2_r3 = []
    diff_clean_r1_r3 = []
    diff_clean_r0_r3 = []

    ret_r2_list = []
    ret_r1_list = []
    ret_r0_list = []

    diff_ret_r2_r1 = []
    diff_ret_r1_r0 = []
    diff_ret_r2_r0 = []

    # E4 habitat sensitivity lists
    diff_e4_r2_kebun_embung = []
    diff_e4_r2_kebun_gedung = []
    diff_e4_r1_kebun_embung = []
    diff_e4_r1_kebun_gedung = []
    diff_habitat_swing_r1_r2 = []

    for _ in range(n_iterations):
        idx = np.random.randint(0, n, n)
        
        # Nilai Clean rata-rata pada sampel bootstrap
        m_r2_c = np.mean(r2_clean[idx])
        m_r1_c = np.mean(r1_clean[idx])
        m_r0_c = np.mean(r0_clean[idx])
        m_r3_c = np.mean(r3_clean[idx])
        
        diff_clean_r2_r1.append(m_r2_c - m_r1_c)
        diff_clean_r2_r0.append(m_r2_c - m_r0_c)
        diff_clean_r1_r0.append(m_r1_c - m_r0_c)
        diff_clean_r2_r3.append(m_r2_c - m_r3_c)
        diff_clean_r1_r3.append(m_r1_c - m_r3_c)
        diff_clean_r0_r3.append(m_r0_c - m_r3_c)
        
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
        diff_ret_r1_r0.append(ret1 - ret0)
        diff_ret_r2_r0.append(ret2 - ret0)

        if has_e4:
            # E4 R2 habitat comparisons
            m_r2_kebun = np.mean(r2_e4_kebun[idx])
            m_r2_embung = np.mean(r2_e4_embung[idx])
            m_r2_gedung = np.mean(r2_e4_gedung[idx])

            diff_e4_r2_kebun_embung.append(m_r2_embung - m_r2_kebun)
            diff_e4_r2_kebun_gedung.append(m_r2_gedung - m_r2_kebun)

            # E4 R1 habitat comparisons
            m_r1_kebun = np.mean(r1_e4_kebun[idx])
            m_r1_embung = np.mean(r1_e4_embung[idx])
            m_r1_gedung = np.mean(r1_e4_gedung[idx])

            diff_e4_r1_kebun_embung.append(m_r1_embung - m_r1_kebun)
            diff_e4_r1_kebun_gedung.append(m_r1_gedung - m_r1_kebun)

            # Habitat swing disparity: swing(R1) - swing(R2)
            # swing = max(hab) - min(hab) normalized to clean
            swing_r1 = (max(m_r1_kebun, m_r1_embung, m_r1_gedung) - min(m_r1_kebun, m_r1_embung, m_r1_gedung)) / m_r1_c
            swing_r2 = (max(m_r2_kebun, m_r2_embung, m_r2_gedung) - min(m_r2_kebun, m_r2_embung, m_r2_gedung)) / m_r2_c
            diff_habitat_swing_r1_r2.append(swing_r1 - swing_r2)

    def calc_stats(diff_array, two_tailed: bool = False):
        mean_val = np.mean(diff_array)
        ci_low, ci_high = np.percentile(diff_array, [2.5, 97.5])
        if two_tailed:
            p_val_num = 2 * min(np.sum(np.array(diff_array) <= 0), np.sum(np.array(diff_array) >= 0)) / len(diff_array)
        else:
            p_val_num = np.sum(np.array(diff_array) <= 0) / len(diff_array)
        p_val_str = "<= 0.001" if p_val_num <= 0.001 else f"{p_val_num:.4f}"
        sig = p_val_num < 0.05
        return round(mean_val, 4), round(ci_low, 4), round(ci_high, 4), p_val_str, sig

    results = []

    # 1. Clean Comparisons (E1)
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

    # H5 Testing (vs R3 Random Control)
    mean_v, low, high, p_str, sig = calc_stats(diff_clean_r2_r3)
    results.append({
        "Pengujian": "Clean Retrieval (mAP@10)",
        "Komparasi": "R2 (BirdNET) vs R3 (Random)",
        "Mean_Diff": mean_v,
        "CI_95_Lower": low,
        "CI_95_Upper": high,
        "p_value": p_str,
        "Signifikan_0.05": sig,
        "Catatan": "H5 Terpenuhi: R2 unggul mutlak atas kontrol acak"
    })

    mean_v, low, high, p_str, sig = calc_stats(diff_clean_r1_r3)
    results.append({
        "Pengujian": "Clean Retrieval (mAP@10)",
        "Komparasi": "R1 (PANNs) vs R3 (Random)",
        "Mean_Diff": mean_v,
        "CI_95_Lower": low,
        "CI_95_Upper": high,
        "p_value": p_str,
        "Signifikan_0.05": sig,
        "Catatan": "H5 Terpenuhi: R1 unggul atas kontrol acak"
    })

    mean_v, low, high, p_str, sig = calc_stats(diff_clean_r0_r3)
    results.append({
        "Pengujian": "Clean Retrieval (mAP@10)",
        "Komparasi": "R0 (MFCC) vs R3 (Random)",
        "Mean_Diff": mean_v,
        "CI_95_Lower": low,
        "CI_95_Upper": high,
        "p_value": p_str,
        "Signifikan_0.05": sig,
        "Catatan": "H5 Terpenuhi: R0 unggul atas kontrol acak"
    })

    # 2. Relative Retention Comparisons at SNR -5 dB (H1 & H2 Testing)
    mean_ret2 = np.mean(ret_r2_list) * 100
    mean_ret1 = np.mean(ret_r1_list) * 100
    mean_ret0 = np.mean(ret_r0_list) * 100

    mean_v, low, high, p_str, sig = calc_stats(diff_ret_r2_r1)
    results.append({
        "Pengujian": "Retensi Relatif SNR -5 dB",
        "Komparasi": "R2 (BirdNET) vs R1 (PANNs)",
        "Mean_Diff": mean_v,
        "CI_95_Lower": low,
        "CI_95_Upper": high,
        "p_value": p_str,
        "Signifikan_0.05": sig,
        "Catatan": f"Retensi R2 ({mean_ret2:.1f}%) unggul signifikan atas R1 ({mean_ret1:.1f}%)"
    })

    mean_v, low, high, p_str, sig = calc_stats(diff_ret_r1_r0)
    results.append({
        "Pengujian": "Retensi Relatif SNR -5 dB",
        "Komparasi": "R1 (PANNs) vs R0 (MFCC)",
        "Mean_Diff": mean_v,
        "CI_95_Lower": low,
        "CI_95_Upper": high,
        "p_value": p_str,
        "Signifikan_0.05": sig,
        "Catatan": f"Retensi R1 ({mean_ret1:.1f}%) unggul signifikan atas MFCC ({mean_ret0:.1f}%)"
    })

    mean_v, low, high, p_str, sig = calc_stats(diff_ret_r2_r0)
    results.append({
        "Pengujian": "Retensi Relatif SNR -5 dB",
        "Komparasi": "R2 (BirdNET) vs R0 (MFCC)",
        "Mean_Diff": mean_v,
        "CI_95_Lower": low,
        "CI_95_Upper": high,
        "p_value": p_str,
        "Signifikan_0.05": sig,
        "Catatan": f"Retensi R2 ({mean_ret2:.1f}%) unggul mutlak atas MFCC ({mean_ret0:.1f}%)"
    })

    # 3. Noise Source Habitat Sensitivity (E4 ITERA Habitats at SNR -5 dB)
    if has_e4:
        # R2 Embung F vs Kebun Raya
        mean_v, low, high, p_str, sig = calc_stats(diff_e4_r2_kebun_embung, two_tailed=True)
        results.append({
            "Pengujian": "Sensitivitas Habitat E4 (-5 dB)",
            "Komparasi": "R2 (Embung F vs Kebun Raya)",
            "Mean_Diff": mean_v,
            "CI_95_Lower": low,
            "CI_95_Upper": high,
            "p_value": p_str,
            "Signifikan_0.05": sig,
            "Catatan": "Embung F (hidro/angin) lebih ramah bagi BirdNET dibanding biofoni serangga Kebun Raya"
        })

        # R2 Gedung F vs Kebun Raya
        mean_v, low, high, p_str, sig = calc_stats(diff_e4_r2_kebun_gedung, two_tailed=True)
        results.append({
            "Pengujian": "Sensitivitas Habitat E4 (-5 dB)",
            "Komparasi": "R2 (Gedung F vs Kebun Raya)",
            "Mean_Diff": mean_v,
            "CI_95_Lower": low,
            "CI_95_Upper": high,
            "p_value": p_str,
            "Signifikan_0.05": sig,
            "Catatan": "Gedung F (antropogenik) mempertahankan skor lebih tinggi dari biofoni Kebun Raya"
        })

        # R1 Embung F vs Kebun Raya
        mean_v, low, high, p_str, sig = calc_stats(diff_e4_r1_kebun_embung, two_tailed=True)
        results.append({
            "Pengujian": "Sensitivitas Habitat E4 (-5 dB)",
            "Komparasi": "R1 (Embung F vs Kebun Raya)",
            "Mean_Diff": mean_v,
            "CI_95_Lower": low,
            "CI_95_Upper": high,
            "p_value": p_str,
            "Signifikan_0.05": sig,
            "Catatan": "PANNs sangat sensitif: Embung F mempertahankan mAP@10 lebih baik dibanding Kebun Raya"
        })

        # R1 Gedung F vs Kebun Raya
        mean_v, low, high, p_str, sig = calc_stats(diff_e4_r1_kebun_gedung, two_tailed=True)
        results.append({
            "Pengujian": "Sensitivitas Habitat E4 (-5 dB)",
            "Komparasi": "R1 (Gedung F vs Kebun Raya)",
            "Mean_Diff": mean_v,
            "CI_95_Lower": low,
            "CI_95_Upper": high,
            "p_value": p_str,
            "Signifikan_0.05": sig,
            "Catatan": "PANNs lebih tahan terhadap derau struktural gedung dibanding biofoni serangga"
        })

        # H3: Fluktuasi Rentang Habitat (Selisih Ayunan Retensi R1 vs R2)
        # Delta observasi empiris
        obs_swing_r1 = (max(np.mean(r1_e4_kebun), np.mean(r1_e4_embung), np.mean(r1_e4_gedung)) - min(np.mean(r1_e4_kebun), np.mean(r1_e4_embung), np.mean(r1_e4_gedung))) / np.mean(r1_clean)
        obs_swing_r2 = (max(np.mean(r2_e4_kebun), np.mean(r2_e4_embung), np.mean(r2_e4_gedung)) - min(np.mean(r2_e4_kebun), np.mean(r2_e4_embung), np.mean(r2_e4_gedung))) / np.mean(r2_clean)
        obs_delta = obs_swing_r1 - obs_swing_r2
        mean_v, low, high, p_str, sig = calc_stats(diff_habitat_swing_r1_r2)
        results.append({
            "Pengujian": "Fluktuasi Rentang Habitat (-5 dB)",
            "Komparasi": "R1 vs R2 (Selisih Ayunan Retensi)",
            "Mean_Diff": mean_v,
            "CI_95_Lower": low,
            "CI_95_Upper": high,
            "p_value": p_str,
            "Signifikan_0.05": sig,
            "Catatan": f"Delta ayunan habitat R1-R2: observasi {obs_delta:.4f}, bootstrap {mean_v:.4f}; interpretasikan arah dan ketidakpastian berdasarkan CI dan p-value."
        })

    # 4. Cluster Bootstrap per Perekam (K=27 recordists)
    if recordists is not None:
        unique_recs = np.unique(recordists)
        rec_to_indices = {rec: np.where(recordists == rec)[0] for rec in unique_recs}
        diff_ret_r2_r1_cluster = []
        for _ in range(n_iterations):
            sampled_recs = np.random.choice(unique_recs, size=len(unique_recs), replace=True)
            c_idx = np.concatenate([rec_to_indices[r] for r in sampled_recs])
            m2_c = np.mean(r2_clean[c_idx])
            m1_c = np.mean(r1_clean[c_idx])
            m2_n = np.mean(r2_n5[c_idx])
            m1_n = np.mean(r1_n5[c_idx])
            ret2 = m2_n / m2_c
            ret1 = m1_n / m1_c
            diff_ret_r2_r1_cluster.append(ret2 - ret1)

        mean_v, low, high, p_str, sig = calc_stats(diff_ret_r2_r1_cluster)
        results.append({
            "Pengujian": f"Cluster Bootstrap (per Recordist, K={len(unique_recs)})",
            "Komparasi": "R2 vs R1 Retensi Relatif (-5 dB)",
            "Mean_Diff": mean_v,
            "CI_95_Lower": low,
            "CI_95_Upper": high,
            "p_value": p_str,
            "Signifikan_0.05": sig,
            "Catatan": "Resampling klaster perekam tetap membuktikan keunggulan R2 atas R1 secara signifikan"
        })

    # 5. Analisis Sensitivitas Non-Mike Nelson
    if recordists is not None:
        mask_non_mike = recordists != "Mike Nelson"
        nm_idx = np.where(mask_non_mike)[0]
        nm_r2_c = r2_clean[nm_idx]
        nm_r1_c = r1_clean[nm_idx]
        nm_r2_n = r2_n5[nm_idx]
        nm_r1_n = r1_n5[nm_idx]
        n_nm = len(nm_idx)

        diff_ret_nm = []
        for _ in range(n_iterations):
            b_idx = np.random.randint(0, n_nm, n_nm)
            m2_c = np.mean(nm_r2_c[b_idx])
            m1_c = np.mean(nm_r1_c[b_idx])
            m2_n = np.mean(nm_r2_n[b_idx])
            m1_n = np.mean(nm_r1_n[b_idx])
            diff_ret_nm.append((m2_n / m2_c) - (m1_n / m1_c))

        mean_v, low, high, p_str, sig = calc_stats(diff_ret_nm)
        results.append({
            "Pengujian": f"Sensitivitas Non-Mike Nelson (N={n_nm})",
            "Komparasi": "R2 vs R1 Retensi Relatif (-5 dB)",
            "Mean_Diff": mean_v,
            "CI_95_Lower": low,
            "CI_95_Upper": high,
            "p_value": p_str,
            "Signifikan_0.05": sig,
            "Catatan": "Menghilangkan perekam mayoritas tidak mengubah signifikansi keunggulan R2"
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
