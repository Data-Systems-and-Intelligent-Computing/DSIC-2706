import numpy as np
from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, auc


def calibrate_threshold_tau(calibration_scores: np.ndarray, calibration_targets: np.ndarray, objective: str = "youden_j") -> dict:
    fpr_arr, tpr_arr, thresholds = roc_curve(calibration_targets, calibration_scores)
    best_tau = float(thresholds[len(thresholds) // 2])
    best_j = -1.0
    best_f1 = 0.0

    for fpr, tpr, tau in zip(fpr_arr, tpr_arr, thresholds):
        if np.isinf(tau) or tau > 1.0:
            continue
        j_val = tpr - fpr
        preds = (calibration_scores >= tau).astype(int)
        tp = np.sum((preds == 1) & (calibration_targets == 1))
        fp = np.sum((preds == 1) & (calibration_targets == 0))
        fn = np.sum((preds == 0) & (calibration_targets == 1))
        f1 = (2 * tp / (2 * tp + fp + fn)) if (2 * tp + fp + fn) > 0 else 0.0

        if j_val > best_j:
            best_j = j_val
            best_tau = float(tau)
            best_f1 = float(f1)

    return {
        "tau": best_tau,
        "youden_j": float(best_j),
        "f1": float(best_f1),
        "objective": objective
    }


def evaluate_open_set_with_frozen_tau(test_scores: np.ndarray, test_targets: np.ndarray, frozen_tau: float) -> dict:
    try:
        auroc = float(roc_auc_score(test_targets, test_scores))
    except Exception:
        auroc = 0.5

    try:
        precision_curve, recall_curve, _ = precision_recall_curve(test_targets, test_scores)
        auprc = float(auc(recall_curve, precision_curve))
    except Exception:
        auprc = 0.0

    preds = (test_scores >= frozen_tau).astype(int)
    tp = int(np.sum((preds == 1) & (test_targets == 1)))
    fp = int(np.sum((preds == 1) & (test_targets == 0)))
    tn = int(np.sum((preds == 0) & (test_targets == 0)))
    fn = int(np.sum((preds == 0) & (test_targets == 1)))

    prec = float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0
    rec = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
    f1 = float(2 * prec * rec / (prec + rec)) if (prec + rec) > 0 else 0.0
    fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0

    return {
        "frozen_tau": float(frozen_tau),
        "AUROC": auroc,
        "AUPRC": auprc,
        "F1_at_tau": f1,
        "Precision_at_tau": prec,
        "Recall_at_tau": rec,
        "False_Positive_Rate": fpr,
        "total_known_tested": int(np.sum(test_targets == 1)),
        "total_unknown_tested": int(np.sum(test_targets == 0))
    }
