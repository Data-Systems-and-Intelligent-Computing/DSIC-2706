
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
from src.analyze_failures import extract_real_failures_from_raw

REPRESENTATIONS = ["R0", "R1", "R2", "R3"]
RESULTS_DIR = PROJECT_ROOT / "results/processed"
PAPER_TABLES_DIR = PROJECT_ROOT / "paper/tables"
FIGURES_DIR = PROJECT_ROOT / "results/figures"
PAPER_FIG_DIR = PROJECT_ROOT / "paper/figures"

for d in [RESULTS_DIR, PAPER_TABLES_DIR, FIGURES_DIR, PAPER_FIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

all_snr_rows = []
all_openset_rows = []

print("=" * 80)
print("[*] MEMULAI BENCHMARK KOMPARATIF DSIC27-06 LENGKAP (INDONESIAN BIODIVERSITY)")
print(f"[*] Representasi Diuji: {REPRESENTATIONS}")
print("=" * 80)

for rep in REPRESENTATIONS:
    res = run_experiment_for_representation(rep_code=rep, snr_list=[20, 10, 0, -5])
    df_snr = res["snr_summary"]
    all_snr_rows.append(df_snr)

    df_tt = res["threshold_transfer_summary"]
    all_openset_rows.append(df_tt)

# Gabungkan dan simpan tabel SNR (E2)
final_snr_df = pd.concat(all_snr_rows, ignore_index=True)
snr_table_path = RESULTS_DIR / "snr_robustness_table.csv"
final_snr_df.to_csv(snr_table_path, index=False, encoding="utf-8")
final_snr_df.to_csv(PAPER_TABLES_DIR / "snr_robustness_table.csv", index=False, encoding="utf-8")

# Susun dan simpan tabel E1 (Clean Retrieval Table)
clean_sub = final_snr_df[final_snr_df["condition"] == "Clean"].copy()
arch_map = {
    "R2": ("BirdNET V2.4 Backbone", "1024-d"),
    "R1": ("PANNs CNN14", "2048-d"),
    "R0": ("MFCC Baseline", "40-d"),
    "R3": ("Random Control", "40-d")
}
clean_rows = []
for rep in ["R2", "R1", "R0", "R3"]:
    r_match = clean_sub[clean_sub["representation"] == rep]
    if len(r_match) > 0:
        row = r_match.iloc[0]
        arch, dim = arch_map.get(rep, ("Unknown", "-"))
        clean_rows.append({
            "Kode": rep,
            "Arsitektur": arch,
            "Dimensi": dim,
            "Top-1 (%)": f"{row['Top1_Accuracy']*100:.1f}%",
            "mAP@10": round(row["mAP@10"], 4),
            "MRR": round(row.get("MRR", 0.0), 4),
            "Precision@10": round(row["Precision@10"], 4),
            "Recall@10": round(row["Recall@10"], 4)
        })
df_clean_table = pd.DataFrame(clean_rows)
clean_table_path = RESULTS_DIR / "clean_retrieval_table.csv"
df_clean_table.to_csv(clean_table_path, index=False, encoding="utf-8")
df_clean_table.to_csv(PAPER_TABLES_DIR / "clean_retrieval_table.csv", index=False, encoding="utf-8")

# Gabungkan dan simpan tabel E3 (Threshold Transfer Table)
final_os_df = pd.concat(all_openset_rows, ignore_index=True)
os_table_path = RESULTS_DIR / "threshold_transfer_table.csv"
final_os_df.to_csv(os_table_path, index=False, encoding="utf-8")
final_os_df.to_csv(PAPER_TABLES_DIR / "threshold_transfer_table.csv", index=False, encoding="utf-8")

# Jalankan audit failure analysis (E5)
try:
    extract_real_failures_from_raw()
except Exception as e:
    print(f"[-] Catatan failure extraction: {e}")

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
