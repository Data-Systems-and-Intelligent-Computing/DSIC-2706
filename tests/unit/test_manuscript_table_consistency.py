"""
Unit Test: tests/unit/test_manuscript_table_consistency.py
Memverifikasi sinkronisasi 100% antara angka-angka yang dikutip dalam naskah publikasi (paper/manuscript.md)
dengan tabel-tabel hasil mentah dan olahan resmi di paper/tables/*.csv.
"""

import re
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MANUSCRIPT_PATH = PROJECT_ROOT / "paper/manuscript.md"
TABLES_DIR = PROJECT_ROOT / "paper/tables"


def test_manuscript_exists():
    assert MANUSCRIPT_PATH.exists(), f"File naskah {MANUSCRIPT_PATH} tidak ditemukan!"


def test_clean_retrieval_consistency():
    """Memverifikasi konsistensi metrik kondisi bersih E1 (Clean Retrieval)."""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    df_clean = pd.read_csv(TABLES_DIR / "clean_retrieval_table.csv")
    
    # R2 (BirdNET)
    r2_row = df_clean[df_clean["Kode"] == "R2"].iloc[0]
    r2_map = f"{r2_row['mAP@10']:.4f}"
    r2_mrr = f"{r2_row['MRR']:.4f}"
    assert r2_map in text, f"mAP@10 R2 ({r2_map}) tidak ditemukan dalam naskah!"
    assert r2_mrr in text, f"MRR R2 ({r2_mrr}) tidak ditemukan dalam naskah!"

    # R1 (PANNs)
    r1_row = df_clean[df_clean["Kode"] == "R1"].iloc[0]
    r1_map = f"{r1_row['mAP@10']:.4f}"
    assert r1_map in text, f"mAP@10 R1 ({r1_map}) tidak ditemukan dalam naskah!"

    # R0 (MFCC)
    r0_row = df_clean[df_clean["Kode"] == "R0"].iloc[0]
    r0_map = f"{r0_row['mAP@10']:.4f}"
    assert r0_map in text, f"mAP@10 R0 ({r0_map}) tidak ditemukan dalam naskah!"


def test_snr_robustness_consistency():
    """Memverifikasi konsistensi metrik ketahanan derau E2 pada SNR -5 dB."""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    df_snr = pd.read_csv(TABLES_DIR / "snr_robustness_table.csv")

    # Nilai mAP@10 pada SNR -5 dB
    r2_n5 = df_snr[(df_snr["representation"] == "R2") & (df_snr["condition"] == "SNR_-5dB")].iloc[0]
    r1_n5 = df_snr[(df_snr["representation"] == "R1") & (df_snr["condition"] == "SNR_-5dB")].iloc[0]
    r0_n5 = df_snr[(df_snr["representation"] == "R0") & (df_snr["condition"] == "SNR_-5dB")].iloc[0]

    assert f"{r2_n5['mAP@10']:.4f}" in text, f"mAP R2 -5dB ({r2_n5['mAP@10']:.4f}) tidak cocok dengan naskah!"
    assert f"{r1_n5['mAP@10']:.4f}" in text, f"mAP R1 -5dB ({r1_n5['mAP@10']:.4f}) tidak cocok dengan naskah!"
    assert f"{r0_n5['mAP@10']:.4f}" in text, f"mAP R0 -5dB ({r0_n5['mAP@10']:.4f}) tidak cocok dengan naskah!"

    # Retensi relatif R2 pada -5 dB: 78.04% atau 78.0%
    assert "78.0" in text, "Retensi relatif R2 (78.0%) tidak ditemukan dalam naskah!"
    assert "55.5" in text, "Retensi relatif R1 (55.5%) tidak ditemukan dalam naskah!"
    assert "35.7" in text, "Retensi relatif R0 (35.7%) tidak ditemukan dalam naskah!"


def test_threshold_transfer_e3_consistency():
    """Memverifikasi konsistensi metrik open-set E3 (tau beku dan test set transfer)."""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    df_e3 = pd.read_csv(TABLES_DIR / "threshold_transfer_table.csv")
    df_cal = pd.read_csv(TABLES_DIR / "calibration_summary_table.csv")

    # Frozen Tau
    r2_tau = f"{df_cal[df_cal['representation'] == 'R2'].iloc[0]['frozen_tau']:.4f}"
    r1_tau = f"{df_cal[df_cal['representation'] == 'R1'].iloc[0]['frozen_tau']:.4f}"
    assert r2_tau in text, f"Frozen tau R2 ({r2_tau}) tidak ditemukan dalam naskah!"
    assert r1_tau in text, f"Frozen tau R1 ({r1_tau}) tidak ditemukan dalam naskah!"

    # AUROC kondisi Clean Test Set (bukan kalibrasi!)
    r2_clean_test = df_e3[(df_e3["representation"] == "R2") & (df_e3["condition"] == "Clean")].iloc[0]
    assert f"{r2_clean_test['AUROC']:.4f}" in text, f"AUROC test clean R2 ({r2_clean_test['AUROC']:.4f}) tidak ditemukan!"


def test_e4_habitat_sensitivity_consistency():
    """Memverifikasi konsistensi hasil habitat sensitivity E4 pada SNR -5 dB."""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    df_e4 = pd.read_csv(TABLES_DIR / "e4_domain_shift_table.csv")

    r2_kebun = df_e4[(df_e4["representation"] == "R2") & (df_e4["habitat"] == "Kebun_Raya") & (df_e4["condition"] == "SNR_-5dB")].iloc[0]
    r2_embung = df_e4[(df_e4["representation"] == "R2") & (df_e4["habitat"] == "Embung_F") & (df_e4["condition"] == "SNR_-5dB")].iloc[0]

    assert f"{r2_kebun['mAP@10']:.4f}" in text, f"mAP Kebun Raya R2 ({r2_kebun['mAP@10']:.4f}) tidak ditemukan!"
    assert f"{r2_embung['mAP@10']:.4f}" in text, f"mAP Embung F R2 ({r2_embung['mAP@10']:.4f}) tidak ditemukan!"


def test_bootstrap_significance_consistency():
    """Memverifikasi konsistensi hasil uji statistik paired bootstrap."""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    df_boot = pd.read_csv(TABLES_DIR / "statistical_significance_table.csv")

    clean_r2_r1 = df_boot[(df_boot["Pengujian"].str.contains("Clean")) & (df_boot["Komparasi"].str.contains("R2.*R1"))].iloc[0]
    ret_r2_r1 = df_boot[(df_boot["Pengujian"].str.contains("Retensi")) & (df_boot["Komparasi"].str.contains("R2.*R1"))].iloc[0]

    assert f"{clean_r2_r1['Mean_Diff']:.4f}" in text, f"Mean Diff Clean R2-R1 ({clean_r2_r1['Mean_Diff']:.4f}) tidak ditemukan!"
    assert f"{ret_r2_r1['Mean_Diff']:.4f}" in text, f"Mean Diff Retensi R2-R1 ({ret_r2_r1['Mean_Diff']:.4f}) tidak ditemukan!"

    # H5 Kontrol Acak (R2, R1, R0 vs R3)
    r2_r3 = df_boot[df_boot["Komparasi"].str.contains("R2.*R3")].iloc[0]
    r1_r3 = df_boot[df_boot["Komparasi"].str.contains("R1.*R3")].iloc[0]
    r0_r3 = df_boot[df_boot["Komparasi"].str.contains("R0.*R3")].iloc[0]
    assert f"{r2_r3['Mean_Diff']:.4f}" in text, f"Mean Diff R2-R3 ({r2_r3['Mean_Diff']:.4f}) tidak ditemukan!"
    assert f"{r1_r3['Mean_Diff']:.4f}" in text, f"Mean Diff R1-R3 ({r1_r3['Mean_Diff']:.4f}) tidak ditemukan!"
    assert f"{r0_r3['Mean_Diff']:.4f}" in text, f"Mean Diff R0-R3 ({r0_r3['Mean_Diff']:.4f}) tidak ditemukan!"

    # H3 Komparasi Selisih Ayunan Rentang Habitat (R1 vs R2)
    h3_swing = df_boot[df_boot["Pengujian"].str.contains("Rentang Habitat")].iloc[0]
    assert f"{h3_swing['Mean_Diff']:.4f}" in text, f"Mean Diff Ayunan Habitat ({h3_swing['Mean_Diff']:.4f}) tidak ditemukan!"

    # Cluster Bootstrap & Mike Nelson Sensitivity
    cluster_row = df_boot[df_boot["Pengujian"].str.contains("Cluster Bootstrap")].iloc[0]
    assert f"{cluster_row['Mean_Diff']:.4f}" in text, f"Cluster Bootstrap ({cluster_row['Mean_Diff']:.4f}) tidak ditemukan!"

    nelson_row = df_boot[df_boot["Pengujian"].str.contains("Mike Nelson")].iloc[0]
    assert f"{nelson_row['Mean_Diff']:.4f}" in text, f"Non-Mike Nelson ({nelson_row['Mean_Diff']:.4f}) tidak ditemukan!"


if __name__ == "__main__":
    print("[*] Menjalankan test_manuscript_table_consistency...")
    test_manuscript_exists()
    test_clean_retrieval_consistency()
    test_snr_robustness_consistency()
    test_threshold_transfer_e3_consistency()
    test_e4_habitat_sensitivity_consistency()
    test_bootstrap_significance_consistency()
    print("[+] SEMUA UJI KONSISTENSI NASKAH VS TABEL CSV LOLOS 100%!")
