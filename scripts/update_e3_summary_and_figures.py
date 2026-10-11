"""
Script: scripts/update_e3_summary_and_figures.py
Fungsi: Memperbarui calibration_summary_table.csv, configs/thresholds.yaml,
        serta menghasilkan gambar resolusi tinggi untuk Eksperimen E3:
        1. results/figures/e3_calibration_roc_youden.png
        2. results/figures/e3_threshold_transfer_snr.png
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, roc_auc_score
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocess import preprocess_audio
from src.embeddings import AudioRepresentationExtractor
from src.retrieve import compute_query_retrieval
from src.calibrate_threshold import calibrate_threshold_tau

SPLIT_PATH = PROJECT_ROOT / "data/manifests/dataset_split.csv"
UNK_PATH = PROJECT_ROOT / "data/manifests/unknown_open_set_manifest.csv"
FEATURES_DIR = PROJECT_ROOT / "results/features"
PROCESSED_DIR = PROJECT_ROOT / "results/processed"
PAPER_TABLES_DIR = PROJECT_ROOT / "paper/tables"
FIG_DIR = PROJECT_ROOT / "results/figures"
PAPER_FIG_DIR = PROJECT_ROOT / "paper/figures"

for d in [PROCESSED_DIR, PAPER_TABLES_DIR, FIG_DIR, PAPER_FIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def main():
    print("=" * 80)
    print("[*] MEMPERBARUI HASIL KALIBRASI & GAMBAR E3 (DATASET INDONESIA)")
    print("=" * 80)

    df_split = pd.read_csv(SPLIT_PATH)
    df_unk = pd.read_csv(UNK_PATH)

    calib_pos_df = df_split[df_split["split_role"] == "calibration"].reset_index(drop=True)
    calib_neg_df = df_unk[df_unk["split_role"] == "unknown_calibration"].reset_index(drop=True)

    print(f"[*] Calibration Positives: {len(calib_pos_df)}, Negatives: {len(calib_neg_df)}")

    calib_pos_audios = [preprocess_audio(r["file_path"]) for _, r in calib_pos_df.iterrows()]
    calib_neg_audios = [preprocess_audio(r["file_path"]) for _, r in calib_neg_df.iterrows()]

    representations = ["R0", "R1", "R2", "R3"]
    calib_summary_rows = []
    all_calib_raw = []
    roc_data = {}

    for rep in representations:
        print(f"[*] Menghitung kalibrasi untuk {rep}...")
        feat_path = FEATURES_DIR / f"clean_embeddings_{rep}.npz"
        feat_data = np.load(feat_path)
        gallery_embs = feat_data["gal_feats"]
        gallery_labels = feat_data["gal_labels"]

        extractor = AudioRepresentationExtractor(rep)
        calib_scores = []
        calib_targets = []

        for y, (_, r) in zip(calib_pos_audios, calib_pos_df.iterrows()):
            emb = extractor.extract(y)
            res = compute_query_retrieval(emb, r["species_key"], gallery_embs, gallery_labels)
            calib_scores.append(res["max_score"])
            calib_targets.append(1)

        for y, (_, r) in zip(calib_neg_audios, calib_neg_df.iterrows()):
            emb = extractor.extract(y)
            res = compute_query_retrieval(emb, "UNKNOWN_NON_BIRD", gallery_embs, gallery_labels)
            calib_scores.append(res["max_score"])
            calib_targets.append(0)

        scores = np.array(calib_scores)
        targets = np.array(calib_targets)

        calib_res = calibrate_threshold_tau(scores, targets, objective="youden_j")
        tau_val = float(calib_res["tau"])
        fpr_arr, tpr_arr, _ = roc_curve(targets, scores)
        auroc_val = float(auc(fpr_arr, tpr_arr))

        # Simpan raw calibration scores per kueri
        for i, (_, r) in enumerate(calib_pos_df.iterrows()):
            sc = calib_scores[i]
            all_calib_raw.append({
                "representation": rep,
                "split_role": "calibration",
                "query_id": r["recording_id"],
                "species_key": r["species_key"],
                "target_type": "known_bird",
                "similarity_score": sc,
                "frozen_tau": tau_val,
                "predicted_accept": int(sc >= tau_val),
                "ground_truth": 1
            })
        for j, (_, r) in enumerate(calib_neg_df.iterrows()):
            sc = calib_scores[len(calib_pos_df) + j]
            all_calib_raw.append({
                "representation": rep,
                "split_role": "unknown_calibration",
                "query_id": r["unknown_id"],
                "species_key": "UNKNOWN_CONTROL",
                "target_type": "unknown_control",
                "similarity_score": sc,
                "frozen_tau": tau_val,
                "predicted_accept": int(sc >= tau_val),
                "ground_truth": 0
            })

        roc_data[rep] = {
            "fpr": fpr_arr,
            "tpr": tpr_arr,
            "auroc": auroc_val,
            "tau": tau_val,
            "youden_j": calib_res["youden_j"],
            "recall": calib_res["recall"],
            "fpr_at_tau": calib_res["fpr"]
        }

        calib_summary_rows.append({
            "representation": rep,
            "frozen_tau": tau_val,
            "calib_youden_j": calib_res["youden_j"],
            "calib_auroc": auroc_val,
            "calib_f1": calib_res["f1"],
            "calib_recall": calib_res["recall"],
            "calib_fpr": calib_res["fpr"],
            "n_calib_known": len(calib_pos_audios),
            "n_calib_unknown": len(calib_neg_audios)
        })

    # Simpan raw calibration scores
    df_raw_calib = pd.DataFrame(all_calib_raw)
    raw_calib_out = PROJECT_ROOT / "results/raw/E3_calibration_scores_raw.csv"
    raw_calib_out.parent.mkdir(parents=True, exist_ok=True)
    df_raw_calib.to_csv(raw_calib_out, index=False)
    print(f"[+] Berhasil menyimpan {len(df_raw_calib)} skor kalibrasi mentah ke: {raw_calib_out}")

    # Simpan tabel kalibrasi
    df_calib_summary = pd.DataFrame(calib_summary_rows)
    df_calib_summary.to_csv(PROCESSED_DIR / "calibration_summary_table.csv", index=False)
    df_calib_summary.to_csv(PAPER_TABLES_DIR / "calibration_summary_table.csv", index=False)
    print("\n--- RINGKASAN KALIBRASI AMBANG BATAS BEKU (YOUDEN J) ---")
    print(df_calib_summary.to_string(index=False))

    # Perbarui configs/thresholds.yaml
    yaml_path = PROJECT_ROOT / "configs/thresholds.yaml"
    names = {
        "R0": "MFCC Baseline (40-dim)",
        "R1": "Generic Pretrained Audio (PANNs CNN14, 2048-dim)",
        "R2": "Bioacoustic Pretrained Embedding (BirdNET V2.4, 1024-dim)",
        "R3": "Random Ranking Control (40-dim)"
    }
    yaml_lines = [
        "# Open-Set Decision Thresholds (Frozen from Calibration Split)",
        "# Topic: DSIC27-06 Audio Representation Robustness for Bioacoustic Retrieval",
        "# Method: Empirical ROC Curve Optimization via Youden's J Statistic (TPR - FPR)",
        "",
        "calibration_protocol:",
        "  objective: \"youden_j\"",
        f"  calibration_positives_count: {len(calib_pos_audios)}",
        f"  calibration_unknowns_count: {len(calib_neg_audios)}",
        "  dataset_source: \"data/manifests/dataset_split.csv & data/manifests/unknown_open_set_manifest.csv\"",
        "  frozen: true",
        "",
        "thresholds:"
    ]
    for _, r in df_calib_summary.iterrows():
        rep = r["representation"]
        yaml_lines.extend([
            f"  {rep}:",
            f"    name: \"{names.get(rep, rep)}\"",
            f"    tau: {r['frozen_tau']:.4f}",
            f"    calibration_youden_j: {r['calib_youden_j']:.4f}",
            f"    calibration_auroc: {r['calib_auroc']:.4f}",
            f"    calibration_f1: {r['calib_f1']:.4f}",
            f"    status: \"frozen\"",
            ""
        ])
    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines))
    print(f"[+] Berhasil menyinkronkan {yaml_path}")

    # Plot 1: e3_calibration_roc_youden.png
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    # Subplot A: Kurva ROC Lintas Model
    colors = {"R2": "#1b9e77", "R1": "#d95f02", "R0": "#7570b3", "R3": "#e7298a"}
    for rep in ["R2", "R1", "R0", "R3"]:
        d = roc_data[rep]
        axes[0].plot(d["fpr"], d["tpr"], color=colors[rep], linewidth=2.0,
                     label=f"{rep} (AUROC = {d['auroc']:.3f}, τ* = {d['tau']:.3f})")
    axes[0].plot([0, 1], [0, 1], color="gray", linestyle="--", alpha=0.7)
    axes[0].set_xlabel("False Positive Rate (FPR)")
    axes[0].set_ylabel("True Positive Rate (TPR / Recall)")
    axes[0].set_title("A. Kurva ROC Kalibrasi Open-Set Terpisah", fontweight="bold")
    axes[0].legend(loc="lower right")

    # Subplot B: Youden's J & AUROC Bar Chart
    x = np.arange(len(df_calib_summary))
    w = 0.35
    b1 = axes[1].bar(x - w/2, df_calib_summary["calib_auroc"], w, label="Calibration AUROC", color="#1f77b4", alpha=0.85)
    b2 = axes[1].bar(x + w/2, df_calib_summary["calib_youden_j"], w, label="Youden's J (TPR - FPR)", color="#2ca02c", alpha=0.85)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(df_calib_summary["representation"], fontweight="bold")
    axes[1].set_ylabel("Skor (0 - 1.0)")
    axes[1].set_title("B. Kemampuan Separasi pada Subset Kalibrasi", fontweight="bold")
    axes[1].set_ylim(0, 1.1)
    axes[1].legend()

    for b in b1:
        h = b.get_height()
        axes[1].annotate(f"{h:.3f}", (b.get_x() + b.get_width()/2, h), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=9)
    for b in b2:
        h = b.get_height()
        axes[1].annotate(f"{h:.3f}", (b.get_x() + b.get_width()/2, h), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=9)

    plt.tight_layout()
    p1 = FIG_DIR / "e3_calibration_roc_youden.png"
    plt.savefig(p1, dpi=300)
    plt.savefig(PAPER_FIG_DIR / "e3_calibration_roc_youden.png", dpi=300)
    plt.close()
    print(f"[+] Gambar ROC Kalibrasi disimpan di: {p1}")

    # Plot 2: e3_threshold_transfer_snr.png
    tt_df = pd.read_csv(PROCESSED_DIR / "threshold_transfer_table.csv")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    cond_order = ["Clean", "SNR_20dB", "SNR_10dB", "SNR_0dB", "SNR_-5dB"]
    cond_labels = ["Clean", "+20 dB", "+10 dB", "0 dB", "-5 dB"]

    # Subplot A: Recall@tau* lintas SNR
    for rep in ["R2", "R1", "R0", "R3"]:
        sub = tt_df[tt_df["representation"] == rep].set_index("condition").reindex(cond_order)
        axes[0].plot(cond_labels, sub["Recall_at_tau"], marker="o", color=colors[rep], linewidth=2.0, label=f"{rep}")
    axes[0].set_xlabel("Tingkat Derau (SNR)")
    axes[0].set_ylabel("Recall pada Ambang Beku τ*")
    axes[0].set_title("A. Target Recall@τ* terhadap Derau", fontweight="bold")
    axes[0].set_ylim(0, 1.05)
    axes[0].legend()

    # Subplot B: False Positive Rate lintas SNR
    for rep in ["R2", "R1", "R0", "R3"]:
        sub = tt_df[tt_df["representation"] == rep].set_index("condition").reindex(cond_order)
        axes[1].plot(cond_labels, sub["False_Positive_Rate"], marker="s", color=colors[rep], linewidth=2.0, label=f"{rep}")
    axes[1].set_xlabel("Tingkat Derau (SNR)")
    axes[1].set_ylabel("False Positive Rate (FPR)")
    axes[1].set_title("B. False Positive Rate terhadap Derau", fontweight="bold")
    axes[1].set_ylim(0, 1.05)
    axes[1].legend()

    plt.tight_layout()
    p2 = FIG_DIR / "e3_threshold_transfer_snr.png"
    plt.savefig(p2, dpi=300)
    plt.savefig(PAPER_FIG_DIR / "e3_threshold_transfer_snr.png", dpi=300)
    plt.close()
    print(f"[+] Gambar Threshold Transfer disimpan di: {p2}")
    print("=" * 80)


if __name__ == "__main__":
    main()
