"""
E2: Paired Controlled Noise Robustness
- Menguji degradasi berpasangan (paired stress-test) pada SNR 20, 10, 0, -5 dB.
- Menghasilkan snr_robustness_table.csv dan kurva retensi relatif.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.run_benchmark import run_experiment_for_representation
from src.dsic2706.analysis.plotting import generate_all_figures


def run_e2_robustness():
    print("=" * 70)
    print("[*] MENJALANKAN EXPERIMENT E2: NOISE ROBUSTNESS")
    print("=" * 70)

    # Menggunakan runner utama yang menyimpan ke results/processed/snr_robustness_table.csv
    import pandas as pd
    all_rows = []
    for rep in ["R0", "R1", "R2", "R3"]:
        res = run_experiment_for_representation(rep, snr_list=[20, 10, 0, -5])
        all_rows.append(res["snr_summary"])

    df_snr = pd.concat(all_rows, ignore_index=True)
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "results", "processed")
    os.makedirs(out_dir, exist_ok=True)
    df_snr.to_csv(os.path.join(out_dir, "snr_robustness_table.csv"), index=False)

    generate_all_figures()
    print("=" * 70)
    print("[+] E2 Selesai! Tabel dan figur telah dimutakhirkan.")
    print("=" * 70)


if __name__ == "__main__":
    run_e2_robustness()
