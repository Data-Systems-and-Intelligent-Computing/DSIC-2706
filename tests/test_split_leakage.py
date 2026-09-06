"""
Unit Test: tests/test_split_leakage.py
Memvalidasi tidak adanya data leakage antar-split:
- Zero recording ID overlap antara Gallery dan Query.
- Zero file path overlap antara Gallery dan Query.
"""

import os
import pandas as pd

SPLIT_PATH = "d:/FILE AND TASK/TA/data/manifests/dataset_split.csv"


def test_zero_leakage_between_gallery_and_query():
    if not os.path.exists(SPLIT_PATH):
        pytest.skip(f"Dataset split belum ada di {SPLIT_PATH}")

    df = pd.read_csv(SPLIT_PATH)
    gallery_ids = set(df[df['split_role'] == 'gallery']['id'].astype(str))
    query_ids = set(df[df['split_role'] == 'query_clean']['id'].astype(str))

    # Recording ID overlap
    overlap = gallery_ids.intersection(query_ids)
    assert len(overlap) == 0, f"Ditemukan kebocoran {len(overlap)} ID rekaman antara Gallery dan Query: {overlap}"


def test_zero_filepath_leakage():
    if not os.path.exists(SPLIT_PATH):
        return

    df = pd.read_csv(SPLIT_PATH)
    gallery_paths = set(df[df['split_role'] == 'gallery']['file_path'].dropna())
    query_paths = set(df[df['split_role'] == 'query_clean']['file_path'].dropna())

    overlap = gallery_paths.intersection(query_paths)
    assert len(overlap) == 0, f"Ditemukan kebocoran path berkas antara Gallery dan Query: {overlap}"


def test_zero_recordist_leakage_global():
    if not os.path.exists(SPLIT_PATH):
        return

    df = pd.read_csv(SPLIT_PATH)
    gallery_recs = set(df[df['split_role'] == 'gallery']['recordist'].dropna().unique())
    query_recs = set(df[df['split_role'] == 'query_clean']['recordist'].dropna().unique())

    overlap = gallery_recs.intersection(query_recs)
    assert len(overlap) == 0, f"Ditemukan kebocoran recordist antara Gallery dan Query: {overlap}"
