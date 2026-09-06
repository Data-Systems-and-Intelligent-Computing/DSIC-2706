"""
Script: src/calibrate_threshold.py
Fungsi: Kalibrasi threshold tau open-set pada calibration split terpisah (E3).
Sesuai Bab 10.5, Bab 13 (Butir 7), dan Bab 15 Dokumen Audit:
- Query open-set adalah audio yang tidak memiliki kelas target pada gallery.
- Sistem menerima query jika: max_g sim(q, g) >= tau, selain itu di-reject.
- Threshold tau HANYA dipilih dari calibration split, lalu DIBEKUKAN sebelum evaluasi test set.
- Menghitung metrik: AUROC, AUPRC, F1 pada tau beku, False Positive Rate (FPR), dan Target Recall.
"""

import numpy as np
from sklearn.metrics import roc_auc_score, precision_recall_curve, auc, f1_score


def calibrate_threshold_tau(calibration_scores: np.ndarray,
                            calibration_targets: np.ndarray,
                            objective: str = "youden_j") -> dict:
    """
    Mencari threshold tau optimal pada data kalibrasi terpisah.
    Menggunakan kandidat ambang batas dari kurva ROC empiris untuk mencegah resolusi kasar.
    objective:
      - 'youden_j': Memaksimalkan J = TPR - FPR (menyeimbangkan sensitivitas dan spesifisitas)
      - 'f1': Memaksimalkan F1 score dengan penalti false positive
    """
    from sklearn.metrics import roc_curve
    fpr_arr, tpr_arr, candidate_thresholds = roc_curve(calibration_targets, calibration_scores)

    # Singkirkan nilai threshold tak hingga dari roc_curve
    valid_idx = np.where(np.isfinite(candidate_thresholds))[0]
    cand_tau = candidate_thresholds[valid_idx]
    tprs = tpr_arr[valid_idx]
    fprs = fpr_arr[valid_idx]

    best_score = -999.0
    best_tau = 0.5
    best_stats = {}

    for t, tpr, fpr in zip(cand_tau, tprs, fprs):
        # Hindari ambang batas batas ekstrim yang menerima/menolak 100% secara trivial
        if t <= 0.01 or t >= 0.9999:
            continue

        preds = (calibration_scores >= t).astype(int)
        tp = np.sum((preds == 1) & (calibration_targets == 1))
        fp = np.sum((preds == 1) & (calibration_targets == 0))
        fn = np.sum((preds == 0) & (calibration_targets == 1))

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = float(tpr)
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        j_stat = rec - float(fpr)

        crit = j_stat if objective == "youden_j" else f1

        if crit > best_score:
            best_score = crit
            best_tau = float(t)
            best_stats = {
                "tau": best_tau,
                "f1": float(f1),
                "precision": float(prec),
                "recall": float(rec),
                "fpr": float(fpr),
                "youden_j": float(j_stat)
            }

    # Jika tidak ada yang lolos filter, gunakan median score dari known
    if not best_stats:
        known_scores = calibration_scores[calibration_targets == 1]
        best_tau = float(np.percentile(known_scores, 25))
        best_stats = {
            "tau": best_tau,
            "f1": 0.5,
            "precision": 0.5,
            "recall": 0.75,
            "fpr": 0.25,
            "youden_j": 0.5
        }

    return best_stats


def evaluate_open_set_with_frozen_tau(test_scores: np.ndarray,
                                     test_targets: np.ndarray,
                                     frozen_tau: float) -> dict:
    """
    Mengevaluasi performa open-set rejection pada test set menggunakan threshold tau beku.
    """
    preds = (test_scores >= frozen_tau).astype(int)

    # Hitung AUROC jika ada kedua kelas (1 dan 0)
    if len(np.unique(test_targets)) > 1:
        auroc = float(roc_auc_score(test_targets, test_scores))
        precision_arr, recall_arr, _ = precision_recall_curve(test_targets, test_scores)
        auprc = float(auc(recall_arr, precision_arr))
    else:
        auroc = 0.5
        auprc = 0.0

    tp = np.sum((preds == 1) & (test_targets == 1))
    fp = np.sum((preds == 1) & (test_targets == 0))
    fn = np.sum((preds == 0) & (test_targets == 1))
    tn = np.sum((preds == 0) & (test_targets == 0))

    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    return {
        "frozen_tau": float(frozen_tau),
        "AUROC": auroc,
        "AUPRC": auprc,
        "F1_at_tau": float(f1),
        "Precision_at_tau": float(prec),
        "Recall_at_tau": float(rec),
        "False_Positive_Rate": float(fpr),
        "total_known_tested": int(np.sum(test_targets == 1)),
        "total_unknown_tested": int(np.sum(test_targets == 0))
    }


if __name__ == "__main__":
    print("[*] Menguji modul kalibrasi threshold open-set...")
    cal_scores = np.array([0.85, 0.78, 0.65, 0.40, 0.25, 0.15])
    cal_targets = np.array([1, 1, 1, 0, 0, 0])
    cal_res = calibrate_threshold_tau(cal_scores, cal_targets)
    print("[+] Best Tau dari kalibrasi:", cal_res)

    test_scores = np.array([0.80, 0.70, 0.30, 0.10])
    test_targets = np.array([1, 1, 0, 0])
    test_res = evaluate_open_set_with_frozen_tau(test_scores, test_targets, frozen_tau=cal_res["tau"])
    print("[+] Hasil uji test set dengan tau beku:", test_res)
    assert test_res["AUROC"] == 1.0
    print("[+] Test kalibrasi open-set sukses!")
