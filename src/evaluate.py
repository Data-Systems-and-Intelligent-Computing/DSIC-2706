"""
Script: src/evaluate.py
Fungsi: Pipeline komprehensif evaluasi saintifik DSIC27-06.
Mencakup:
1. E1: Clean Retrieval Performance (mAP@10, Recall@10, Precision@10, Top-1)
2. E2: Paired Noise Degradation (Evaluasi Ketahanan Lintas SNR: 20dB, 10dB, 0dB, -5dB)
3. E3: Open-Set Calibration (tau freeze via Youden's J) & Threshold Transfer Test (C-02 FIX)
4. S-02: Pencatatan pemeringkatan mentah per kueri ke results/raw/ untuk audit kegagalan nyata E5
5. S-01: Metadata eksekusi resmi untuk keterlacakan saintifik
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.preprocess import preprocess_audio, TARGET_SR
from src.embeddings import AudioRepresentationExtractor
from src.mix_noise import mix_audio_at_snr
from src.retrieve import evaluate_retrieval_corpus, compute_query_retrieval
from src.calibrate_threshold import calibrate_threshold_tau, evaluate_open_set_with_frozen_tau

SPLIT_PATH = PROJECT_ROOT / "data/manifests/dataset_split.csv"
RESULTS_DIR = PROJECT_ROOT / "results/processed"
RAW_DIR = PROJECT_ROOT / "results/raw"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)


def save_raw_query_metrics(rep_code: str, condition: str, raw_metrics: list, query_df: pd.DataFrame):
    """Menyimpan hasil pemeringkatan mentah per-kueri ke results/raw/ (S-02)."""
    rows = []
    for i, m in enumerate(raw_metrics):
        row = {
            "query_id": query_df.iloc[i]["id"],
            "species_key": query_df.iloc[i]["species_key"],
            "recordist": query_df.iloc[i]["recordist"],
            "top1_match": m["top1_match"],
            "max_similarity_score": m["max_score"],
            "AP@10": m.get("AP@10", 0.0),
            "Recall@10": m.get("R@10", 0.0),
            "Precision@10": m.get("P@10", 0.0),
        }
        rows.append(row)
    df_raw = pd.DataFrame(rows)
    raw_path = RAW_DIR / f"{rep_code}_{condition}_raw.csv"
    df_raw.to_csv(raw_path, index=False)


def run_experiment_for_representation(rep_code: str = "R0", snr_list: list = [20, 10, 0, -5]) -> dict:
    if not SPLIT_PATH.exists():
        raise FileNotFoundError(f"Split file tidak ditemukan: {SPLIT_PATH}")

    df_split = pd.read_csv(SPLIT_PATH)
    gallery_df = df_split[df_split['split_role'] == 'gallery'].copy()
    query_clean_df = df_split[df_split['split_role'] == 'query_clean'].copy()
    calib_df = df_split[df_split['split_role'] == 'calibration'].copy()
    unknown_df = df_split[df_split['split_role'] == 'unknown_test'].copy()

    print(f"\n======================================================================")
    print(f"[*] MENJALANKAN EVALUASI REPRESENTASI [{rep_code}]")
    print(f"[*] Gallery: {len(gallery_df)}, Query Clean: {len(query_clean_df)}, Calib: {len(calib_df)}, Unknown: {len(unknown_df)}")
    print(f"======================================================================")

    extractor = AudioRepresentationExtractor(rep_code)

    # 1. Ekstraksi Gallery Embeddings
    print("[*] Mengekstrak embeddings untuk Gallery Set...")
    gallery_embs = []
    gallery_labels = []
    for _, r in gallery_df.iterrows():
        y = preprocess_audio(r['file_path'])
        emb = extractor.extract(y)
        gallery_embs.append(emb)
        gallery_labels.append(r['species_key'])
    gallery_embs = np.array(gallery_embs)

    # 2. Ekstraksi Preprocessed Clean Queries
    print("[*] Memuat sinyal audio Clean Query...")
    query_clean_audios = []
    query_labels = []
    for _, r in query_clean_df.iterrows():
        y = preprocess_audio(r['file_path'])
        query_clean_audios.append(y)
        query_labels.append(r['species_key'])

    # 3. E1: Clean Evaluation
    print("[*] Menjalankan E1: Clean Retrieval...")
    query_clean_embs = np.array([extractor.extract(y) for y in query_clean_audios])
    clean_summary, clean_raw = evaluate_retrieval_corpus(
        query_embs=query_clean_embs,
        query_labels=query_labels,
        gallery_embs=gallery_embs,
        gallery_labels=gallery_labels
    )
    clean_map10 = clean_summary["mAP@10"]
    save_raw_query_metrics(rep_code, "Clean", clean_raw, query_clean_df)
    print(f"    [E1 Clean] mAP@10: {clean_map10:.4f}, Recall@10: {clean_summary['Recall@10']:.4f}, Top1: {clean_summary['mean_top1']:.4f}")

    # 4. E2: Controlled Noise Robustness (Paired Test)
    print("\n[*] Menjalankan E2: Paired Noise Degradation...")
    snr_results = []
    
    # Masukkan kondisi clean sebagai baseline awal (SNR = inf)
    snr_results.append({
        "representation": rep_code,
        "condition": "Clean",
        "snr_db": 999,
        "mAP@10": clean_map10,
        "Recall@10": clean_summary["Recall@10"],
        "Precision@10": clean_summary["Precision@10"],
        "Top1_Accuracy": clean_summary["mean_top1"],
        "relative_retention": 1.0,
        "absolute_drop": 0.0
    })

    for snr in snr_list:
        noisy_embs = []
        for i, y_clean in enumerate(query_clean_audios):
            # Campurkan noise dengan seed terikat pada index query untuk reproducibility
            y_noisy = mix_audio_at_snr(y_clean, snr_db=snr, seed=42 + i)
            emb_noisy = extractor.extract(y_noisy)
            noisy_embs.append(emb_noisy)
        noisy_embs = np.array(noisy_embs)

        noisy_summary, noisy_raw = evaluate_retrieval_corpus(
            query_embs=noisy_embs,
            query_labels=query_labels,
            gallery_embs=gallery_embs,
            gallery_labels=gallery_labels
        )
        save_raw_query_metrics(rep_code, f"SNR_{snr}dB", noisy_raw, query_clean_df)

        noisy_map10 = noisy_summary["mAP@10"]
        rel_ret = noisy_map10 / max(clean_map10, 1e-6)
        abs_drop = clean_map10 - noisy_map10

        print(f"    [SNR {snr:3d} dB] mAP@10: {noisy_map10:.4f} (Retention: {rel_ret*100:.1f}%, Drop: {abs_drop:.4f}), Top1: {noisy_summary['mean_top1']:.4f}")

        snr_results.append({
            "representation": rep_code,
            "condition": f"SNR_{snr}dB",
            "snr_db": snr,
            "mAP@10": noisy_map10,
            "Recall@10": noisy_summary["Recall@10"],
            "Precision@10": noisy_summary["Precision@10"],
            "Top1_Accuracy": noisy_summary["mean_top1"],
            "relative_retention": rel_ret,
            "absolute_drop": abs_drop
        })

    # 5. E3: Open-Set Calibration & Threshold Transfer (C-02 FIX)
    print("\n[*] Menjalankan E3: Kalibrasi Threshold Open-Set (Youden J)...")
    calib_scores = []
    calib_targets = []

    for _, r in calib_df.iterrows():
        y = preprocess_audio(r['file_path'])
        emb = extractor.extract(y)
        res = compute_query_retrieval(emb, r['species_key'], gallery_embs, gallery_labels)
        calib_scores.append(res["max_score"])
        calib_targets.append(1)

    # Ambil separuh unknown untuk kalibrasi
    n_unk = len(unknown_df)
    n_calib_unk = min(len(calib_df), n_unk // 2)
    calib_unk_df = unknown_df.iloc[:n_calib_unk]
    test_unk_df = unknown_df.iloc[n_calib_unk:]

    for _, r in calib_unk_df.iterrows():
        y = preprocess_audio(r['file_path'])
        emb = extractor.extract(y)
        res = compute_query_retrieval(emb, "UNKNOWN_NON_BIRD", gallery_embs, gallery_labels)
        calib_scores.append(res["max_score"])
        calib_targets.append(0)

    calib_stats = calibrate_threshold_tau(np.array(calib_scores), np.array(calib_targets), objective="youden_j")
    frozen_tau = calib_stats["tau"]
    print(f"    [Kalibrasi] Frozen Tau: {frozen_tau:.4f} (Calib Youden J: {calib_stats.get('youden_j', 0):.4f}, Calib F1: {calib_stats['f1']:.4f})")

    # Memuat sinyal mentah audio unknown untuk pengujian transfer ambang
    unknown_test_audios = []
    for _, r in test_unk_df.iterrows():
        y = preprocess_audio(r['file_path'])
        unknown_test_audios.append(y)

    # Uji Threshold Transfer (E3): Menguji tau beku pada Clean dan seluruh tingkat SNR
    threshold_transfer_rows = []
    conditions_to_test = [("Clean", query_clean_embs, 999)]
    for snr in snr_list:
        n_embs = []
        for i, y_c in enumerate(query_clean_audios):
            y_n = mix_audio_at_snr(y_c, snr_db=snr, seed=42 + i)
            n_embs.append(extractor.extract(y_n))
        conditions_to_test.append((f"SNR_{snr}dB", np.array(n_embs), snr))

    clean_recall = 0.0
    clean_fpr = 0.0

    print("[*] Menguji Open-Set Threshold Transfer dengan injeksi derau pada Unknown (C-02 Fix)...")
    for idx, (cond_name, q_embs, snr_val) in enumerate(conditions_to_test):
        known_scores = [compute_query_retrieval(e, lbl, gallery_embs, gallery_labels)["max_score"] for e, lbl in zip(q_embs, query_labels)]

        # PERBAIKAN C-02: Ekstraksi audio unknown pada kondisi derau yang sama persis
        if cond_name == "Clean":
            u_embs = [extractor.extract(y_u) for y_u in unknown_test_audios]
        else:
            u_embs = []
            for j, y_u in enumerate(unknown_test_audios):
                y_u_noisy = mix_audio_at_snr(y_u, snr_db=snr_val, seed=1000 + j)
                u_embs.append(extractor.extract(y_u_noisy))

        unknown_scores = [compute_query_retrieval(e, "UNKNOWN", gallery_embs, gallery_labels)["max_score"] for e in u_embs]

        all_test_scores = np.concatenate([known_scores, unknown_scores])
        all_test_targets = np.concatenate([np.ones(len(known_scores)), np.zeros(len(unknown_scores))])

        eval_os = evaluate_open_set_with_frozen_tau(all_test_scores, all_test_targets, frozen_tau=frozen_tau)
        
        if idx == 0:
            clean_recall = eval_os["Recall_at_tau"]
            clean_fpr = eval_os["False_Positive_Rate"]
            delta_rec = 0.0
            delta_fpr = 0.0
        else:
            delta_rec = eval_os["Recall_at_tau"] - clean_recall
            delta_fpr = eval_os["False_Positive_Rate"] - clean_fpr

        eval_os["representation"] = rep_code
        eval_os["condition"] = cond_name
        eval_os["snr_db"] = snr_val
        eval_os["delta_Recall"] = delta_rec
        eval_os["delta_FPR"] = delta_fpr
        eval_os["clean_recall"] = clean_recall
        eval_os["clean_fpr"] = clean_fpr

        print(f"    [{cond_name:8s}] Recall@tau: {eval_os['Recall_at_tau']:.4f} (dRec: {delta_rec:+.4f}), FPR: {eval_os['False_Positive_Rate']:.4f} (dFPR: {delta_fpr:+.4f})")

        threshold_transfer_rows.append(eval_os)

    return {
        "snr_table": pd.DataFrame(snr_results),
        "transfer_table": pd.DataFrame(threshold_transfer_rows),
        "snr_summary": pd.DataFrame(snr_results),
        "threshold_transfer_summary": pd.DataFrame(threshold_transfer_rows),
        "frozen_tau": frozen_tau
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Jalankan evaluasi retrieval DSIC27-06.")
    parser.add_argument("--rep", type=str, default="R0", help="Kode representasi (R0, R1, R2, R3)")
    args = parser.parse_args()

    res = run_experiment_for_representation(args.rep)
    print(f"\n[+] Selesai mengevaluasi {args.rep}!")
