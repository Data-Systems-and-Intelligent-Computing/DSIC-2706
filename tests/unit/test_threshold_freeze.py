import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.dsic2706.open_set.calibration import calibrate_threshold_tau, evaluate_open_set_with_frozen_tau


def test_threshold_frozen_evaluation():
    cal_scores = np.array([0.9, 0.85, 0.75, 0.3, 0.2, 0.1])
    cal_targets = np.array([1, 1, 1, 0, 0, 0])
    cal_res = calibrate_threshold_tau(cal_scores, cal_targets)

    frozen_tau = cal_res["tau"]
    assert 0.0 <= frozen_tau <= 1.0

    test_scores = np.array([0.7, 0.65, 0.5, 0.45])
    test_targets = np.array([1, 1, 0, 0])
    eval_res = evaluate_open_set_with_frozen_tau(test_scores, test_targets, frozen_tau=frozen_tau)

    assert eval_res["frozen_tau"] == frozen_tau
