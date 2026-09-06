"""
Unit Test: tests/test_threshold_freeze.py
Memvalidasi bahwa threshold tau dibekukan dari set kalibrasi dan tidak dihitung ulang pada test set.
"""

import sys
import numpy as np

sys.path.insert(0, "d:/FILE AND TASK/TA")
from src.calibrate_threshold import calibrate_threshold_tau, evaluate_open_set_with_frozen_tau


def test_threshold_frozen_evaluation():
    # 1. Kalibrasi pada set A
    cal_scores = np.array([0.9, 0.85, 0.75, 0.3, 0.2, 0.1])
    cal_targets = np.array([1, 1, 1, 0, 0, 0])
    cal_res = calibrate_threshold_tau(cal_scores, cal_targets)

    frozen_tau = cal_res["tau"]
    assert 0.0 <= frozen_tau <= 1.0

    # 2. Uji pada test set B dengan skor yang bergeser
    test_scores = np.array([0.7, 0.65, 0.5, 0.45])
    test_targets = np.array([1, 1, 0, 0])

    eval_res = evaluate_open_set_with_frozen_tau(test_scores, test_targets, frozen_tau=frozen_tau)

    # Pastikan hasil uji mencatat tau yang sama persis
    assert eval_res["frozen_tau"] == frozen_tau
