import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.dsic2706.features.mfcc import cosine_similarity
from src.dsic2706.retrieval.engine import compute_query_retrieval


def test_cosine_similarity_properties():
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([1.0, 0.0, 0.0])
    v3 = np.array([0.0, 1.0, 0.0])
    v4 = np.array([-1.0, 0.0, 0.0])

    assert abs(cosine_similarity(v1, v2) - 1.0) < 1e-6
    assert abs(cosine_similarity(v1, v3) - 0.0) < 1e-6
    assert abs(cosine_similarity(v1, v4) - (-1.0)) < 1e-6


def test_retrieval_ranking_logic():
    q = np.array([1.0, 0.0])
    gallery = np.array([
        [0.0, 1.0],
        [1.0, 0.0],
        [0.7, 0.7]
    ])
    labels = ["sp_B", "sp_A", "sp_A"]

    res = compute_query_retrieval(q, "sp_A", gallery, labels, k_values=[1, 2, 3])
    assert res["top1_match"] == 1
    assert res["P@1"] == 1.0
    assert res["AP@1"] == 1.0
