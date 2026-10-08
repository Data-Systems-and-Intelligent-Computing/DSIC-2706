"""
Script: scripts/run_e3_calibration.py
Fungsi: Eksekusi Eksperimen E3 — Kalibrasi Ambang Batas Open-Set (tau*) & Pengujian Transfer Lintas SNR.
Sesuai audit saintifik:
1. Subset Kalibrasi Terpisah:
   - Positif (Known Bird): 498 klip dari dataset_split.csv (split_role: calibration).
   - Negatif (Unknown Non-Bird & Non-Target): 498 klip dari unknown_open_set_manifest.csv (split_role: unknown_calibration).
   - Ambang tau* dioptimasi dengan kurva ROC empiris & Youden's J = TPR - FPR.
   - tau* DIBEKUKAN (FROZEN) sebelum evaluasi test set.
2. Subset Pengujian (Test Set):
   - Positif (Known Bird Query): 200 klip dari dataset_split.csv (split_role: query_clean).
   - Negatif (Unknown Test): 200 klip dari unknown_open_set_manifest.csv (split_role: unknown_test).
   - Diuji pada kondisi Clean dan 4 tingkat derau aditif (SNR 20 dB, 10 dB, 0 dB, -5 dB) secara berpasangan.
   - Menghitung AUROC, AUPRC, F1@tau*, Precision@tau*, Recall@tau*, False Positive Rate (FPR), Delta Recall, dan Delta FPR.
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc, roc_curve

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocess import preprocess_audio, TARGET_SR, TARGET_SAMPLES
from src.embeddings import AudioRepresentationExtractor
from src.mix_noise import mix_audio_at_snr
from src.calibrate_threshold import calibrate_threshold_tau, evaluate_open_set_with_frozen_tau

SPLIT_PATH = PROJECT_ROOT / "data/manifests/dataset_split.csv"
UNK_PATH = PROJECT_ROOT / "data/manifests/unknown_open_set_manifest.csv"
FEATURES_DIR = PROJECT_ROOT / "results/features"
PROCESSED_DIR = PROJECT_ROOT / "results/processed"
RAW_DIR = PROJECT_ROOT / "results/raw"
TABLES_DIR = PROJECT_ROOT / "paper/tables"

def compute_max_similarities(query_embs: np.ndarray, gallery_embs: np.ndarray) -> np.ndarray:
    """Menghitung skor cosine similarity maksimum terhadap seluruh klip dalam gallery."""
    # L2-normalize queries
    q_norms = np.linalg.norm(query_embs, axis=1, keepdims=True)
    q_norms[q_norms < 1e-8] = 1e-8
    q_normed = query_embs / q_norms

    # L2-normalize gallery
    g_norms = np.linalg.norm(gallery_embs, axis=1, keepdims=True)
    g_norms[g_norms < 1e-8] = 1e-8
    g_normed = gallery_embs / g_norms

    # Matrix multiplication: (N_query, N_gallery)
    sim_matrix = np.dot(q_normed, g_normed.T)
    max_sims = np.max(sim_matrix, axis=1)
    return max_sims

def main():
    print("=" * 80)
    print("[*] MEMULAI REKONSTRUKSI EKSPERIMEN E3: OPEN-SET CALIBRATION & TRANSFER")
    print("=" * 80)

    df_split = pd.read_csv(SPLIT_PATH)
    df_unk = pd.read_csv(UNK_PATH)

    calib_pos_df = df_split[df_split["split_role"] == "calibration"].copy().reset_index(drop=True)
    query_pos_df = df_split[df_split["split_role"] == "query_clean"].copy().reset_index(drop=True)
    calib_neg_df = df_unk[df_unk["split_role"] == "unknown_calibration"].copy().reset_index(drop=True)
    test_neg_df = df_unk[df_unk["split_role"] == "unknown_test"].copy().reset_index(drop=True)

    print(f"[*] Calibration Positives: {len(calib_pos_df)}, Negatives: {len(calib_neg_df)}")
    print(f"[*] Test Positives:        {len(query_pos_df)}, Negatives: {len(test_neg_df)}")

    # Muat audio mentah
    print("\n[*] Memuat dan mem-preprocess audio kalibrasi & unknown...")
    calib_pos_audios = [preprocess_audio(r["file_path"]) for _, r in calib_pos_df.iterrows()]
    calib_neg_audios = [preprocess_audio(r["file_path"]) for _, r in calib_neg_df.iterrows()]
    test_neg_audios = [preprocess_audio(r["file_path"]) for _, r in test_neg_df.iterrows()]
    query_pos_audios = [preprocess_audio(r["file_path"]) for _, r in query_pos_df.iterrows()]

    snr_list = [20, 10, 0, -5]
    representations = ["R0", "R1", "R2", "R3"]

    results_table_rows = []
    calibration_summary_rows = []
    all_raw_e3_scores = []

    for rep in representations:
        print(f"\n" + "-" * 60)
        print(f"[*] MEMPROSES REPRESENTASI [{rep}]")
        print("-" * 60)

        # 1. Muat gallery embeddings yang sudah tersimpan
        feat_path = FEATURES_DIR / f"clean_embeddings_{rep}.npz"
        feat_data = np.load(feat_path)
        gallery_embs = feat_data["gal_feats"]
        print(f"[*] Gallery embeddings {rep} dimuat: {gallery_embs.shape}")

        extractor = AudioRepresentationExtractor(rep)

        # 2. Ekstrak Calibration Embeddings
        print(f"[*] Mengekstrak embedding kalibrasi ({rep})...")
        calib_pos_embs = np.array([extractor.extract(y) for y in calib_pos_audios])
        calib_neg_embs = np.array([extractor.extract(y) for y in calib_neg_audios])

        calib_pos_scores = compute_max_similarities(calib_pos_embs, gallery_embs)
        calib_neg_scores = compute_max_similarities(calib_neg_embs, gallery_embs)

        calib_scores = np.concatenate([calib_pos_scores, calib_neg_scores])
        calib_targets = np.concatenate([np.ones(len(calib_pos_scores)), np.zeros(len(calib_neg_scores))])

        # 3. Optimasi Youden's J pada data kalibrasi
        calib_res = calibrate_threshold_tau(calib_scores, calib_targets, objective="youden_j")
        frozen_tau = float(calib_res["tau"])
        calib_auroc = float(roc_auc_score(calib_targets, calib_scores))

        print(f"    [Kalibrasi Selesai]")
        print(f"    -> Frozen Tau*       : {frozen_tau:.4f}")
        print(f"    -> Calibration Youden J: {calib_res['youden_j']:.4f}")
        print(f"    -> Calibration AUROC : {calib_auroc:.4f}")
        print(f"    -> Calibration F1    : {calib_res['f1']:.4f}")
        print(f"    -> Calibration TPR   : {calib_res['recall']:.4f}")
        print(f"    -> Calibration FPR   : {calib_res['fpr']:.4f}")

        calibration_summary_rows.append({
            "representation": rep,
            "frozen_tau": frozen_tau,
            "calib_youden_j": calib_res["youden_j"],
            "calib_auroc": calib_auroc,
            "calib_f1": calib_res["f1"],
            "calib_recall": calib_res["recall"],
            "calib_fpr": calib_res["fpr"],
            "n_calib_known": len(calib_pos_scores),
            "n_calib_unknown": len(calib_neg_scores)
        })

        # 4. Evaluasi Test Set Lintas Tingkat Derau (Clean s/d -5 dB)
        print(f"\n[*] Mengevaluasi Open-Set Rejection pada Test Set dengan Frozen Tau* = {frozen_tau:.4f}...")
        
        # Positif queries test:
        # Clean
        pos_clean_embs = feat_data["qry_feats"]
        pos_clean_scores = compute_max_similarities(pos_clean_embs, gallery_embs)

        # Unknown test clean
        neg_clean_embs = np.array([extractor.extract(y) for y in test_neg_audios])
        neg_clean_scores = compute_max_similarities(neg_clean_embs, gallery_embs)

        # Uji kondisi Clean
        test_scores_clean = np.concatenate([pos_clean_scores, neg_clean_scores])
        test_targets_clean = np.concatenate([np.ones(len(pos_clean_scores)), np.zeros(len(neg_clean_scores))])
        clean_eval = evaluate_open_set_with_frozen_tau(test_scores_clean, test_targets_clean, frozen_tau=frozen_tau)
        clean_eval["representation"] = rep
        clean_eval["condition"] = "Clean"
        clean_eval["snr_db"] = 999
        clean_eval["delta_Recall"] = 0.0
        clean_eval["delta_FPR"] = 0.0
        clean_eval["clean_recall"] = clean_eval["Recall_at_tau"]
        clean_eval["clean_fpr"] = clean_eval["False_Positive_Rate"]
        results_table_rows.append(clean_eval)

        # Simpan raw skor clean
        for i, sc in enumerate(pos_clean_scores):
            all_raw_e3_scores.append({
                "representation": rep, "condition": "Clean", "snr_db": 999,
                "query_id": query_pos_df.iloc[i]["recording_id"],
                "target_type": "known_bird", "similarity_score": sc,
                "frozen_tau": frozen_tau, "predicted_accept": int(sc >= frozen_tau), "ground_truth": 1
            })
        for i, sc in enumerate(neg_clean_scores):
            all_raw_e3_scores.append({
                "representation": rep, "condition": "Clean", "snr_db": 999,
                "query_id": test_neg_df.iloc[i]["unknown_id"],
                "target_type": "unknown_control", "similarity_score": sc,
                "frozen_tau": frozen_tau, "predicted_accept": int(sc >= frozen_tau), "ground_truth": 0
            })

        print(f"    [Test Clean] AUROC: {clean_eval['AUROC']:.4f}, AUPRC: {clean_eval['AUPRC']:.4f}, "
              f"Recall: {clean_eval['Recall_at_tau']:.4f}, FPR: {clean_eval['False_Positive_Rate']:.4f}, F1: {clean_eval['F1_at_tau']:.4f}")

        clean_rec = clean_eval["Recall_at_tau"]
        clean_fpr_val = clean_eval["False_Positive_Rate"]

        # Evaluasi per level SNR
        for snr in snr_list:
            # Baca skor known query dari results/raw/{rep}_SNR_{snr}dB_raw.csv untuk paired consistency
            raw_pos_csv = RAW_DIR / f"{rep}_SNR_{snr}dB_raw.csv"
            raw_pos_df = pd.read_csv(raw_pos_csv)
            pos_noisy_scores = raw_pos_df["max_similarity_score"].values

            # Inject noise pada unknown test queries dengan seed berpasangan
            neg_noisy_embs = []
            for j, y_neg in enumerate(test_neg_audios):
                y_neg_noisy = mix_audio_at_snr(y_neg, snr_db=snr, seed=1000 + j)
                neg_noisy_embs.append(extractor.extract(y_neg_noisy))
            neg_noisy_embs = np.array(neg_noisy_embs)
            neg_noisy_scores = compute_max_similarities(neg_noisy_embs, gallery_embs)

            test_scores_noisy = np.concatenate([pos_noisy_scores, neg_noisy_scores])
            test_targets_noisy = np.concatenate([np.ones(len(pos_noisy_scores)), np.zeros(len(neg_noisy_scores))])

            noisy_eval = evaluate_open_set_with_frozen_tau(test_scores_noisy, test_targets_noisy, frozen_tau=frozen_tau)
            delta_rec = noisy_eval["Recall_at_tau"] - clean_rec
            delta_fpr = noisy_eval["False_Positive_Rate"] - clean_fpr_val

            noisy_eval["representation"] = rep
            noisy_eval["condition"] = f"SNR_{snr}dB"
            noisy_eval["snr_db"] = snr
            noisy_eval["delta_Recall"] = delta_rec
            noisy_eval["delta_FPR"] = delta_fpr
            noisy_eval["clean_recall"] = clean_rec
            noisy_eval["clean_fpr"] = clean_fpr_val
            results_table_rows.append(noisy_eval)

            # Simpan raw skor noisy
            for i, sc in enumerate(pos_noisy_scores):
                all_raw_e3_scores.append({
                    "representation": rep, "condition": f"SNR_{snr}dB", "snr_db": snr,
                    "query_id": query_pos_df.iloc[i]["recording_id"],
                    "target_type": "known_bird", "similarity_score": sc,
                    "frozen_tau": frozen_tau, "predicted_accept": int(sc >= frozen_tau), "ground_truth": 1
                })
            for i, sc in enumerate(neg_noisy_scores):
                all_raw_e3_scores.append({
                    "representation": rep, "condition": f"SNR_{snr}dB", "snr_db": snr,
                    "query_id": test_neg_df.iloc[i]["unknown_id"],
                    "target_type": "unknown_control", "similarity_score": sc,
                    "frozen_tau": frozen_tau, "predicted_accept": int(sc >= frozen_tau), "ground_truth": 0
                })

            print(f"    [SNR {snr:3d} dB] AUROC: {noisy_eval['AUROC']:.4f}, AUPRC: {noisy_eval['AUPRC']:.4f}, "
                  f"Recall: {noisy_eval['Recall_at_tau']:.4f} (dRec: {delta_rec:+.4f}), FPR: {noisy_eval['False_Positive_Rate']:.4f} (dFPR: {delta_fpr:+.4f})")

    # 5. Simpan Hasil
    df_results = pd.DataFrame(results_table_rows)
    df_results_out = PROCESSED_DIR / "threshold_transfer_table.csv"
    df_results.to_csv(df_results_out, index=False)
    df_results.to_csv(TABLES_DIR / "threshold_transfer_table.csv", index=False)
    print(f"\n[+] Sukses menyimpan tabel E3: {df_results_out}")

    df_raw_scores = pd.DataFrame(all_raw_e3_scores)
    df_raw_scores.to_csv(RAW_DIR / "E3_test_scores_raw.csv", index=False)
    print(f"[+] Sukses menyimpan raw query scores E3: {RAW_DIR / 'E3_test_scores_raw.csv'}")

    df_calib_summary = pd.DataFrame(calibration_summary_rows)
    df_calib_summary.to_csv(PROCESSED_DIR / "calibration_summary_table.csv", index=False)
    print(f"[+] Sukses menyimpan ringkasan kalibrasi: {PROCESSED_DIR / 'calibration_summary_table.csv'}")

    # 6. Perbarui configs/thresholds.yaml dengan nilai beku asli
    update_thresholds_yaml(df_calib_summary)

def update_thresholds_yaml(calib_df: pd.DataFrame):
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
        "  calibration_positives_count: 498",
        "  calibration_unknowns_count: 498",
        "  dataset_source: \"data/manifests/dataset_split.csv & data/manifests/unknown_open_set_manifest.csv\"",
        "  frozen: true",
        "",
        "thresholds:"
    ]

    for _, r in calib_df.iterrows():
        rep = r["representation"]
        tau = float(r["frozen_tau"])
        j_val = float(r["calib_youden_j"])
        yaml_lines.extend([
            f"  {rep}:",
            f"    name: \"{names.get(rep, rep)}\"",
            f"    tau: {tau:.4f}",
            f"    calibration_youden_j: {j_val:.4f}",
            f"    calibration_auroc: {float(r['calib_auroc']):.4f}",
            f"    calibration_f1: {float(r['calib_f1']):.4f}",
            f"    status: \"frozen\"",
            ""
        ])

    with open(yaml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(yaml_lines))
    print(f"[+] Berhasil menyinkronkan nilai tau* beku ke {yaml_path}")

if __name__ == "__main__":
    main()
