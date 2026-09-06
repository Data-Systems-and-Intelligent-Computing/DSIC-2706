import os
import numpy as np
import pandas as pd
from ..audio.preprocess import preprocess_audio
from ..audio.mixing import mix_audio_at_snr
from ..features.embeddings import AudioRepresentationExtractor
from ..retrieval.engine import evaluate_retrieval_corpus, compute_query_retrieval
from ..open_set.calibration import calibrate_threshold_tau, evaluate_open_set_with_frozen_tau

SPLIT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "manifests", "dataset_split.csv")


def run_experiment_for_representation(rep_code: str = "R0", snr_list: list = [20, 10, 0, -5]) -> dict:
    if not os.path.exists(SPLIT_PATH):
        raise FileNotFoundError(f"Split file tidak ditemukan: {SPLIT_PATH}")

    df_split = pd.read_csv(SPLIT_PATH)
    gallery_df = df_split[df_split['split_role'] == 'gallery'].copy()
    query_clean_df = df_split[df_split['split_role'] == 'query_clean'].copy()
    calib_df = df_split[df_split['split_role'] == 'calibration'].copy()
    unknown_df = df_split[df_split['split_role'] == 'unknown_test'].copy()

    extractor = AudioRepresentationExtractor(rep_code)

    # 1. Ekstraksi Gallery
    gallery_embs = []
    gallery_labels = []
    for _, r in gallery_df.iterrows():
        y = preprocess_audio(r['file_path'])
        gallery_embs.append(extractor.extract(y))
        gallery_labels.append(r['species_key'])
    gallery_embs = np.array(gallery_embs)

    # 2. Ekstraksi Clean Query
    query_clean_audios = []
    query_labels = []
    for _, r in query_clean_df.iterrows():
        y = preprocess_audio(r['file_path'])
        query_clean_audios.append(y)
        query_labels.append(r['species_key'])

    # 3. E1: Clean Evaluation
    query_clean_embs = np.array([extractor.extract(y) for y in query_clean_audios])
    clean_summary, _ = evaluate_retrieval_corpus(
        query_embs=query_clean_embs,
        query_labels=query_labels,
        gallery_embs=gallery_embs,
        gallery_labels=gallery_labels
    )
    clean_map10 = clean_summary["mAP@10"]

    snr_results = [{
        "representation": rep_code,
        "condition": "Clean",
        "snr_db": 999,
        "mAP@10": clean_map10,
        "Recall@10": clean_summary["Recall@10"],
        "Precision@10": clean_summary["Precision@10"],
        "Top1_Accuracy": clean_summary["mean_top1"],
        "relative_retention": 1.0,
        "absolute_drop": 0.0
    }]

    # 4. E2: Noise Robustness
    for snr in snr_list:
        noisy_embs = []
        for i, y_clean in enumerate(query_clean_audios):
            y_noisy = mix_audio_at_snr(y_clean, snr_db=snr, seed=42 + i)
            noisy_embs.append(extractor.extract(y_noisy))
        noisy_embs = np.array(noisy_embs)

        noisy_summary, _ = evaluate_retrieval_corpus(
            query_embs=noisy_embs,
            query_labels=query_labels,
            gallery_embs=gallery_embs,
            gallery_labels=gallery_labels
        )
        noisy_map10 = noisy_summary["mAP@10"]
        rel_ret = noisy_map10 / max(clean_map10, 1e-6)
        abs_drop = clean_map10 - noisy_map10

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

    # 5. E3: Open-Set Calibration & Threshold Transfer
    calib_scores = []
    calib_targets = []
    for _, r in calib_df.iterrows():
        y = preprocess_audio(r['file_path'])
        emb = extractor.extract(y)
        res = compute_query_retrieval(emb, r['species_key'], gallery_embs, gallery_labels)
        calib_scores.append(res["max_score"])
        calib_targets.append(1)

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

    unknown_test_embs = np.array([extractor.extract(preprocess_audio(r['file_path'])) for _, r in test_unk_df.iterrows()])
    unknown_scores = [compute_query_retrieval(e, "UNKNOWN", gallery_embs, gallery_labels)["max_score"] for e in unknown_test_embs]

    threshold_transfer_rows = []
    conditions_to_test = [("Clean", query_clean_embs, 999)]
    for snr in snr_list:
        n_embs = [extractor.extract(mix_audio_at_snr(y_c, snr_db=snr, seed=42 + i)) for i, y_c in enumerate(query_clean_audios)]
        conditions_to_test.append((f"SNR_{snr}dB", np.array(n_embs), snr))

    clean_recall = 0.0
    clean_fpr = 0.0
    for idx, (cond_name, q_embs, snr_val) in enumerate(conditions_to_test):
        known_scores = [compute_query_retrieval(e, lbl, gallery_embs, gallery_labels)["max_score"] for e, lbl in zip(q_embs, query_labels)]
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
        threshold_transfer_rows.append(eval_os)

    return {
        "representation": rep_code,
        "clean_summary": clean_summary,
        "snr_summary": pd.DataFrame(snr_results),
        "calibration": calib_stats,
        "threshold_transfer_summary": pd.DataFrame(threshold_transfer_rows)
    }
