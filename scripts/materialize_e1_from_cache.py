"""Materialize auditable E1 artifacts from verified clean embedding caches.

This script never re-extracts audio embeddings.  It verifies the active split
against each cache, derives retrieval ranks and per-query metrics from the
cached vectors, and writes a new timestamped E1 artifact.  It is intended for
R1--R3 caches already used by the verified E4 run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.embeddings import R3_CONTROL_VERSION
from src.retrieve import compute_query_retrieval, evaluate_retrieval_corpus

MANIFEST = ROOT / "data" / "manifests" / "dataset_split.csv"
OUTPUT_ROOT = ROOT / "results" / "reproductions"
CACHE_DIR = ROOT / "results" / "features"
DIMENSIONS = {"R0": 40, "R1": 2048, "R2": 1024, "R3": 40}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_sha() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_and_validate_cache(rep: str, gallery: pd.DataFrame, queries: pd.DataFrame) -> tuple[Path, dict[str, np.ndarray]]:
    cache_path = CACHE_DIR / f"clean_embeddings_{rep}.npz"
    if not cache_path.exists():
        raise FileNotFoundError(f"Cache clean tidak ditemukan: {cache_path}")
    with np.load(cache_path) as raw:
        required = {"gal_feats", "qry_feats", "gal_ids", "qry_ids", "manifest_sha256"}
        missing = sorted(required - set(raw.files))
        if missing:
            raise ValueError(f"Cache {rep} tidak memiliki kolom wajib: {missing}")
        cache = {key: raw[key].copy() for key in raw.files}

    expected_manifest = sha256_file(MANIFEST)
    if str(cache["manifest_sha256"].item()) != expected_manifest:
        raise ValueError(f"Checksum manifest cache {rep} tidak cocok dengan manifest aktif.")
    if cache["gal_feats"].shape != (len(gallery), DIMENSIONS[rep]):
        raise ValueError(f"Bentuk gallery cache {rep} tidak cocok: {cache['gal_feats'].shape}")
    if cache["qry_feats"].shape != (len(queries), DIMENSIONS[rep]):
        raise ValueError(f"Bentuk query cache {rep} tidak cocok: {cache['qry_feats'].shape}")
    if not np.array_equal(cache["gal_ids"].astype(str), gallery["recording_id"].astype(str).to_numpy()):
        raise ValueError(f"Urutan gallery cache {rep} tidak cocok dengan manifest aktif.")
    if not np.array_equal(cache["qry_ids"].astype(str), queries["recording_id"].astype(str).to_numpy()):
        raise ValueError(f"Urutan query cache {rep} tidak cocok dengan manifest aktif.")
    if not np.isfinite(cache["gal_feats"]).all() or not np.isfinite(cache["qry_feats"]).all():
        raise ValueError(f"Cache {rep} mengandung embedding non-finite.")
    if rep == "R3":
        if "r3_control_version" not in cache or str(cache["r3_control_version"].item()) != R3_CONTROL_VERSION:
            raise ValueError("Versi kontrol R3 pada cache tidak cocok.")
    return cache_path, cache


def build_per_query(rep: str, gallery: pd.DataFrame, queries: pd.DataFrame, cache: dict[str, np.ndarray]) -> tuple[pd.DataFrame, dict]:
    gallery_vectors = cache["gal_feats"]
    query_vectors = cache["qry_feats"]
    gallery_labels = gallery["species_key"].astype(str).tolist()
    summary, metrics = evaluate_retrieval_corpus(
        query_vectors, queries["species_key"].astype(str).tolist(), gallery_vectors, gallery_labels
    )
    norm_gallery = gallery_vectors / np.maximum(np.linalg.norm(gallery_vectors, axis=1, keepdims=True), 1e-8)
    rows: list[dict] = []
    for index, (_, query) in enumerate(queries.iterrows()):
        vector = query_vectors[index]
        scores = norm_gallery @ (vector / max(float(np.linalg.norm(vector)), 1e-8))
        ranking = np.argsort(-scores, kind="stable")
        target = str(query["species_key"])
        target_mask = gallery["species_key"].astype(str).to_numpy() == target
        other_mask = ~target_mask
        top_index = int(ranking[0])
        true_max = float(np.max(scores[target_mask]))
        best_other = float(np.max(scores[other_mask]))
        row = {
            "query_id": str(query["recording_id"]),
            "species_key": target,
            "author": str(query["author"]),
            "representation": rep,
            "top1_recording_id": str(gallery.iloc[top_index]["recording_id"]),
            "top1_species_key": str(gallery.iloc[top_index]["species_key"]),
            "top1_similarity": float(scores[top_index]),
            "true_class_max_similarity": true_max,
            "best_other_similarity": best_other,
            "true_vs_other_margin": true_max - best_other,
        }
        row.update(metrics[index])
        rows.append(row)
    return pd.DataFrame(rows), {key: float(value) for key, value in summary.items()}


def materialize(rep: str) -> Path:
    manifest = pd.read_csv(MANIFEST, dtype={"recording_id": str})
    gallery = manifest.loc[manifest["split_role"].eq("gallery")].reset_index(drop=True)
    queries = manifest.loc[manifest["split_role"].eq("query_clean")].reset_index(drop=True)
    if len(gallery) != 673 or len(queries) != 311:
        raise ValueError(f"Split aktif tidak sesuai: gallery={len(gallery)}, query={len(queries)}")
    cache_path, cache = load_and_validate_cache(rep, gallery, queries)
    per_query, summary = build_per_query(rep, gallery, queries, cache)

    timestamp = datetime.now(timezone.utc)
    output = OUTPUT_ROOT / f"E1_{rep}_cache_{timestamp.strftime('%Y%m%dT%H%M%S_%fZ')}"
    tables = output / "tables"
    features = output / "features"
    output.mkdir(parents=True, exist_ok=False)
    tables.mkdir()
    features.mkdir()
    per_query.to_csv(tables / "per_query.csv", index=False)
    reference = {
        "source_cache_path": str(cache_path.relative_to(ROOT)).replace("\\", "/"),
        "source_cache_sha256": sha256_file(cache_path),
        "source_cache_manifest_sha256": str(cache["manifest_sha256"].item()),
        "embedding_dimension": DIMENSIONS[rep],
        "gallery_count": int(len(gallery)),
        "query_count": int(len(queries)),
    }
    (features / "cache_reference.json").write_text(json.dumps(reference, indent=2) + "\n", encoding="utf-8")
    metadata = {
        "artifact_schema": "e1_clean_cache_materialization_v1",
        "status": "complete",
        "experiment": "E1 Clean Retrieval",
        "representation": rep,
        "timestamp_utc": timestamp.isoformat(),
        "git_sha": git_sha(),
        "manifest_sha256": sha256_file(MANIFEST),
        "retrieval_code_sha256": sha256_file(ROOT / "src" / "retrieve.py"),
        "cache_provenance": reference,
        "summary": summary,
    }
    if rep == "R3":
        metadata["r3_control_version"] = R3_CONTROL_VERSION
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (output / "README.md").write_text(
        f"# E1 clean retrieval {rep}\n\n"
        "Artefak ini dihitung ulang dari cache embedding bersih yang diverifikasi; "
        "audio dan embedding tidak diekstrak ulang. `tables/per_query.csv` berisi "
        "peringkat, prediksi Top-1, serta metrik retrieval tiap query.\n",
        encoding="utf-8",
    )
    print(f"Artifact: {output}")
    print(json.dumps(summary, sort_keys=True))
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Materialize E1 artifact from a verified clean cache.")
    parser.add_argument("representation", choices=sorted(DIMENSIONS))
    arguments = parser.parse_args()
    materialize(arguments.representation)
