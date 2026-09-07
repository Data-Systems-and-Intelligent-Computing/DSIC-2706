
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
"""
Script: src/run_benchmark.py
Fungsi: Menjalankan benchmark paired retrieval lengkap untuk R0 (MFCC), R1 (Generic), R2 (Bioacoustic), dan R3 (Random Control).
Menyimpan hasil ke results/processed/ dan results/figures/.
"""

import os
import sys
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.evaluate import run_experiment_for_representation
from src.analyze_failures import audit_failure_cases

REPRESENTATIONS = ["R0", "R1", "R2", "R3"]
RESULTS_DIR = str(PROJECT_ROOT / "results/processed")
os.makedirs(RESULTS_DIR, exist_ok=True)

all_snr_rows = []
all_openset_rows = []

print("=" * 80)
print("[*] MEMULAI BENCHMARK KOMPARATIF DSIC27-06 LENGKAP")
print(f"[*] Representasi Diuji: {REPRESENTATIONS}")
print("=" * 80)

for rep in REPRESENTATIONS:
    res = run_experiment_for_representation(rep_code=rep, snr_list=[20, 10, 0, -5])
    df_snr = res["snr_summary"]
    all_snr_rows.append(df_snr)

    df_tt = res["threshold_transfer_summary"]
    all_openset_rows.append(df_tt)

# Gabungkan dan simpan tabel
final_snr_df = pd.concat(all_snr_rows, ignore_index=True)
snr_table_path = os.path.join(RESULTS_DIR, "snr_robustness_table.csv")
final_snr_df.to_csv(snr_table_path, index=False, encoding="utf-8")

final_os_df = pd.concat(all_openset_rows, ignore_index=True)
os_table_path = os.path.join(RESULTS_DIR, "threshold_transfer_table.csv")
final_os_df.to_csv(os_table_path, index=False, encoding="utf-8")

# Jalankan audit failure analysis
audit_failure_cases([])

print("\n" + "=" * 80)
print("[+] SELURUH EKSPERIMEN SELESAI!")
print(f"[*] Tabel Ketahanan SNR     : {snr_table_path}")
print(f"[*] Tabel Evaluasi Open-Set : {os_table_path}")
print("=" * 80)

# Tampilkan ringkasan
print("\n--- RINGKASAN RETRIEVAL mAP@10 TERHADAP TINGKAT DERAU ---")
pivot = final_snr_df.pivot(index="condition", columns="representation", values="mAP@10")
print(pivot.to_string())

print("\n--- RINGKASAN RELATIVE RETENTION TERHADAP DERAU ---")
pivot_ret = final_snr_df.pivot(index="condition", columns="representation", values="relative_retention")
print((pivot_ret * 100).round(1).to_string())

print("\n--- RINGKASAN OPEN-SET REJECTION (FROZEN TAU) ---")
print(final_os_df[["representation", "frozen_tau", "AUROC", "AUPRC", "F1_at_tau", "False_Positive_Rate"]].to_string(index=False))
