"""Validasi dan penyelarasan skor known-query untuk evaluasi E3.

E3 menerima hasil E2 yang telah dihitung sebelumnya.  Penyelarasan wajib
berdasarkan ``query_id`` agar perubahan urutan baris CSV tidak dapat
memasangkan skor satu rekaman dengan identitas rekaman lain.
"""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


REQUIRED_COLUMNS = ("query_id", "max_similarity_score")


def align_known_noisy_scores(raw_scores: pd.DataFrame, expected_query_ids: Sequence[str]) -> pd.DataFrame:
    """Return raw E2 scores in the manifest's query order, with strict checks.

    Raises:
        ValueError: when required columns, duplicate IDs, missing IDs, or extra
            IDs would make a paired E3 comparison invalid.
    """
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in raw_scores.columns]
    if missing_columns:
        raise ValueError(
            "Raw E2 tidak dapat dipakai untuk E3 karena kolom wajib tidak ada: "
            + ", ".join(missing_columns)
        )

    expected = [str(query_id) for query_id in expected_query_ids]
    if len(expected) != len(set(expected)):
        raise ValueError("Manifes query E3 memiliki query_id ganda; penyelarasan dihentikan.")

    scores = raw_scores.copy()
    scores["query_id"] = scores["query_id"].astype(str)
    duplicate_ids = sorted(scores.loc[scores["query_id"].duplicated(), "query_id"].unique())
    if duplicate_ids:
        raise ValueError(f"Raw E2 memiliki query_id ganda: {duplicate_ids[:5]}")

    actual = set(scores["query_id"])
    expected_set = set(expected)
    missing_ids = sorted(expected_set - actual)
    extra_ids = sorted(actual - expected_set)
    if missing_ids or extra_ids:
        details = []
        if missing_ids:
            details.append(f"hilang={missing_ids[:5]}")
        if extra_ids:
            details.append(f"tambahan={extra_ids[:5]}")
        raise ValueError("Raw E2 dan query E3 tidak identik: " + "; ".join(details))

    ordered = scores.set_index("query_id", drop=False).loc[expected].reset_index(drop=True)
    numeric_scores = pd.to_numeric(ordered["max_similarity_score"], errors="coerce")
    if numeric_scores.isna().any():
        invalid_ids = ordered.loc[numeric_scores.isna(), "query_id"].tolist()
        raise ValueError(f"Raw E2 memiliki max_similarity_score non-numerik: {invalid_ids[:5]}")
    ordered["max_similarity_score"] = numeric_scores.astype(float)
    return ordered
