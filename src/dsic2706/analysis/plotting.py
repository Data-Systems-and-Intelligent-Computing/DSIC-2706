import os
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "results", "processed")
FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "results", "figures")


def generate_all_figures():
    os.makedirs(FIG_DIR, exist_ok=True)
    table_path = os.path.join(RESULTS_DIR, "snr_robustness_table.csv")
    if not os.path.exists(table_path):
        return False

    df_snr = pd.read_csv(table_path)
    condition_order = ["Clean", "SNR_20dB", "SNR_10dB", "SNR_0dB", "SNR_-5dB"]
    snr_x_labels = ["Clean", "20 dB", "10 dB", "0 dB", "-5 dB"]
    x_pos = [0, 1, 2, 3, 4]

    colors = {"R0": "#1f77b4", "R1": "#ff7f0e", "R2": "#2ca02c", "R3": "#d62728"}
    labels = {
        "R0": "R0: MFCC Baseline (40-dim)",
        "R1": "R1: Generic Audio (PANNs-like)",
        "R2": "R2: Bioacoustic Pretrained",
        "R3": "R3: Random Ranking (Control)"
    }

    # 1. Plot mAP@10 vs SNR
    plt.figure(figsize=(9, 5.5), dpi=150)
    for rep in ["R0", "R1", "R2", "R3"]:
        sub = df_snr[df_snr["representation"] == rep].copy()
        sub["sort_key"] = sub["condition"].map(lambda c: condition_order.index(c) if c in condition_order else 99)
        sub = sub.sort_values("sort_key")
        plt.plot(x_pos, sub["mAP@10"], marker='o', linewidth=2.2, markersize=7, color=colors[rep], label=labels[rep])

    plt.xticks(x_pos, snr_x_labels, fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel("Kondisi Derau Lingkungan (SNR)", fontsize=12, fontweight='bold')
    plt.ylabel("mAP@10 (Mean Average Precision)", fontsize=12, fontweight='bold')
    plt.title("Ketahanan Representasi Audio terhadap Peningkatan Derau (DSIC27-06)", fontsize=13, fontweight='bold', pad=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(frameon=True, fontsize=10, loc="upper right")
    plt.tight_layout()
    map_fig_path = os.path.join(FIG_DIR, "robustness_curve_map10.png")
    plt.savefig(map_fig_path)
    plt.close()

    # 2. Plot Relative Retention
    plt.figure(figsize=(9, 5.5), dpi=150)
    for rep in ["R0", "R1", "R2"]:
        sub = df_snr[df_snr["representation"] == rep].copy()
        sub["sort_key"] = sub["condition"].map(lambda c: condition_order.index(c) if c in condition_order else 99)
        sub = sub.sort_values("sort_key")
        plt.plot(x_pos, sub["relative_retention"] * 100, marker='s', linewidth=2.2, markersize=7, color=colors[rep], label=labels[rep])

    plt.xticks(x_pos, snr_x_labels, fontsize=11)
    plt.yticks(fontsize=11)
    plt.xlabel("Kondisi Derau Lingkungan (SNR)", fontsize=12, fontweight='bold')
    plt.ylabel("Retensi Relatif (%) terhadap Kondisi Bersih", fontsize=12, fontweight='bold')
    plt.title("Kurva Retensi Relatif Retrieval terhadap Peningkatan Derau (DSIC27-06)", fontsize=13, fontweight='bold', pad=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(frameon=True, fontsize=10, loc="lower left")
    plt.tight_layout()
    ret_fig_path = os.path.join(FIG_DIR, "relative_retention_curve.png")
    plt.savefig(ret_fig_path)
    plt.close()
    return True
