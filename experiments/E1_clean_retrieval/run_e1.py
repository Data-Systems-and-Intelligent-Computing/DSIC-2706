"""
E1: Clean Retrieval Experiment
- Menguji seluruh representasi (R0, R1, R2, R3) pada kondisi tanpa derau (Clean).
- Menghitung mAP@10, Recall@k, Precision@k, dan Top-1 Accuracy.
"""

import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.dsic2706.evaluation.evaluator import run_experiment_for_representation


def run_e1_clean():
    print("=" * 70)
    print("[*] MENJALANKAN EXPERIMENT E1: CLEAN RETRIEVAL")
    print("=" * 70)

    rows = []
    for rep in ["R0", "R1", "R2", "R3"]:
        res = run_experiment_for_representation(rep, snr_list=[])
        df_clean = res["snr_summary"]
        clean_row = df_clean[df_clean["condition"] == "Clean"].iloc[0].to_dict()
        rows.append(clean_row)
        print(f"  [{rep}] mAP@10: {clean_row['mAP@10']:.4f}, Top-1 Acc: {clean_row['Top1_Accuracy']:.4f}")

    df_res = pd.DataFrame(rows)
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "results", "tables")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "e1_clean_retrieval_table.csv")
    df_res.to_csv(out_path, index=False)

    print("=" * 70)
    print(f"[+] E1 Selesai! Hasil tersimpan di: {out_path}")
    print("=" * 70)
    return df_res


if __name__ == "__main__":
    run_e1_clean()
