"""
E3: Open-Set Calibration & Threshold Transfer
- Kalibrasi tau pada data kalibrasi terpisah menggunakan Youden's J ROC.
- Pembekuan tau dan transfer evaluasi melintasi Clean, 20 dB, 10 dB, 0 dB, -5 dB.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.run_benchmark import run_experiment_for_representation


def run_e3_open_set():
    print("=" * 70)
    print("[*] MENJALANKAN EXPERIMENT E3: OPEN-SET THRESHOLD TRANSFER")
    print("=" * 70)

    import pandas as pd
    all_tt = []
    for rep in ["R0", "R1", "R2", "R3"]:
        res = run_experiment_for_representation(rep, snr_list=[20, 10, 0, -5])
        all_tt.append(res["threshold_transfer_summary"])

    df_tt = pd.concat(all_tt, ignore_index=True)
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "results", "processed")
    os.makedirs(out_dir, exist_ok=True)
    df_tt.to_csv(os.path.join(out_dir, "threshold_transfer_table.csv"), index=False)

    print("=" * 70)
    print("[+] E3 Selesai! Hasil tersimpan di threshold_transfer_table.csv")
    print("=" * 70)


if __name__ == "__main__":
    run_e3_open_set()
