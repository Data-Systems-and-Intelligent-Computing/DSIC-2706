"""Run E1 clean retrieval for R0 only and write a self-contained artifact.

This command deliberately does not call the combined legacy evaluator, which
also starts E2 and E3.  It reads the active manifest and physical audio, then
writes one new timestamped artifact under ``results/reproductions``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import librosa
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.embeddings import AudioRepresentationExtractor
from src.preprocess import preprocess_audio
from src.retrieve import evaluate_retrieval_corpus

MANIFEST_PATH = PROJECT_ROOT / "data" / "manifests" / "dataset_split.csv"
OUTPUT_ROOT = PROJECT_ROOT / "results" / "reproductions"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def git_sha() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=PROJECT_ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def extract_rows(extractor: AudioRepresentationExtractor, rows: pd.DataFrame, namespace: str) -> np.ndarray:
    embeddings: list[np.ndarray] = []
    total = len(rows)
    for position, (_, row) in enumerate(rows.iterrows(), start=1):
        audio = preprocess_audio(str(row["file_path"]))
        embedding = extractor.extract(audio, item_id=f"{namespace}:{row['recording_id']}")
        if embedding.shape != (40,) or not np.isfinite(embedding).all():
            raise ValueError(f"R0 embedding invalid for {row['recording_id']}: shape={embedding.shape}")
        embeddings.append(embedding.astype(np.float32, copy=False))
        if position % 25 == 0 or position == total:
            print(f"R0 {namespace}: {position}/{total}", flush=True)
    return np.stack(embeddings, axis=0)


def run(dry_run: bool = False) -> Path | None:
    manifest = pd.read_csv(MANIFEST_PATH)
    gallery = manifest.loc[manifest["split_role"].eq("gallery")].reset_index(drop=True)
    queries = manifest.loc[manifest["split_role"].eq("query_clean")].reset_index(drop=True)
    if len(gallery) != 673 or len(queries) != 311:
        raise ValueError(f"Active split mismatch: gallery={len(gallery)}, query_clean={len(queries)}")
    if gallery["recording_id"].duplicated().any() or queries["recording_id"].duplicated().any():
        raise ValueError("Duplicate recording_id found in active E1 split.")

    print(f"E1 R0 clean: gallery={len(gallery)}, query_clean={len(queries)}")
    if dry_run:
        return None

    extractor = AudioRepresentationExtractor("R0")
    gallery_embeddings = extract_rows(extractor, gallery, "gallery")
    query_embeddings = extract_rows(extractor, queries, "query_clean")

    summary, query_metrics = evaluate_retrieval_corpus(
        query_embs=query_embeddings,
        query_labels=queries["species_key"].tolist(),
        gallery_embs=gallery_embeddings,
        gallery_labels=gallery["species_key"].tolist(),
        k_values=[1, 5, 10],
    )
    per_query = pd.DataFrame(query_metrics)
    per_query.insert(0, "representation", "R0")
    per_query.insert(0, "author", queries["author"].astype(str))
    per_query.insert(0, "species_key", queries["species_key"].astype(str))
    per_query.insert(0, "query_id", queries["recording_id"].astype(str))

    now = datetime.now(timezone.utc)
    output_dir = OUTPUT_ROOT / f"E1_R0_{now.strftime('%Y%m%d_%H%M%S')}"
    output_dir.mkdir(parents=True, exist_ok=False)
    tables_dir = output_dir / "tables"
    features_dir = output_dir / "features"
    tables_dir.mkdir()
    features_dir.mkdir()
    np.savez_compressed(
        features_dir / "embeddings.npz",
        gallery_embeddings=gallery_embeddings,
        query_embeddings=query_embeddings,
        gallery_ids=gallery["recording_id"].astype(str).to_numpy(dtype=str),
        query_ids=queries["recording_id"].astype(str).to_numpy(dtype=str),
    )
    per_query.to_csv(tables_dir / "per_query.csv", index=False)
    metadata = {
        "artifact_schema": "e1_clean_r0_v2",
        "status": "complete",
        "representation": "R0",
        "experiment": "E1 Clean Retrieval only",
        "timestamp_utc": now.isoformat(),
        "git_sha": git_sha(),
        "manifest_sha256": sha256_file(MANIFEST_PATH),
        "preprocess_code_sha256": sha256_file(PROJECT_ROOT / "src" / "preprocess.py"),
        "mfcc_code_sha256": sha256_file(PROJECT_ROOT / "src" / "mfcc.py"),
        "retrieval_code_sha256": sha256_file(PROJECT_ROOT / "src" / "retrieve.py"),
        "python_version": sys.version.split()[0],
        "numpy_version": np.__version__,
        "librosa_version": librosa.__version__,
        "gallery_count": int(len(gallery)),
        "query_count": int(len(queries)),
        "summary": {key: float(value) for key, value in summary.items()},
    }
    (output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (output_dir / "README.md").write_text(
        "# E1 — Clean retrieval R0\n\n"
        "- `tables/per_query.csv`: metrik tiap kueri.\n"
        "- `features/embeddings.npz`: embedding gallery dan query.\n"
        "- `metadata.json`: konfigurasi dan ringkasan metrik.\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, sort_keys=True))
    print(f"Artifact: {output_dir}")
    return output_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run E1 clean R0 only.")
    parser.add_argument("--dry-run", action="store_true", help="Check manifest counts without reading audio or writing output.")
    arguments = parser.parse_args()
    run(dry_run=arguments.dry_run)
