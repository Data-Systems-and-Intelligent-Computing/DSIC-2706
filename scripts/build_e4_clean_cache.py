import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ["MPLBACKEND"] = "Agg"
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / "results" / ".mplconfig"))

from src.preprocess import preprocess_audio
from src.embeddings import AudioRepresentationExtractor, R3_CONTROL_VERSION
from src.retrieve import evaluate_retrieval_corpus

MANIFEST = ROOT / "data/manifests/dataset_split.csv"
COMPATIBILITY_CACHE_DIR = ROOT / "results" / "features"

CHECKPOINTS = {
    "R1": ROOT / "checkpoints/Cnn14_mAP=0.431.pth",
    "R2": ROOT / "checkpoints/BirdNET_GLOBAL_6K_V2.4_Model_FP32.onnx",
    # R3 is a deterministic control; it has no model checkpoint.
    "R3": None,
}

DIMENSIONS = {"R1": 2048, "R2": 1024, "R3": 40}


def sha256_file(path):
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_split(extractor, rows, namespace, dimension):
    vectors = []

    for i, row in rows.iterrows():
        path = Path(row["file_path"])
        if not path.is_absolute():
            path = ROOT / path

        y = preprocess_audio(str(path))
        emb = extractor.extract(
            y,
            item_id=f"{namespace}:{row['recording_id']}"
        )

        if emb.shape != (dimension,):
            raise ValueError(
                f"Dimensi salah: {row['recording_id']}"
            )

        if not np.isfinite(emb).all():
            raise ValueError(
                f"Embedding non-finite: {row['recording_id']}"
            )

        if not np.isclose(np.linalg.norm(emb), 1.0, atol=1e-5):
            raise ValueError(
                f"L2 norm tidak valid: {row['recording_id']}"
            )

        vectors.append(emb)

        if (i + 1) % 100 == 0 or i + 1 == len(rows):
            print(
                f"[{namespace}] {i + 1}/{len(rows)}",
                flush=True
            )

    return np.stack(vectors).astype(np.float32)


def main(rep):
    print(f"=== MEMBANGUN CACHE CLEAN {rep} ===", flush=True)

    manifest_hash = sha256_file(MANIFEST)
    checkpoint_path = CHECKPOINTS[rep]
    checkpoint_hash = (
        sha256_file(checkpoint_path)
        if checkpoint_path is not None
        else None
    )

    df = pd.read_csv(
        MANIFEST,
        dtype={"recording_id": str}
    )

    gallery = df[df["split_role"] == "gallery"].reset_index(drop=True)
    query = df[df["split_role"] == "query_clean"].reset_index(drop=True)

    if len(gallery) != 673 or len(query) != 311:
        raise ValueError("Jumlah Gallery/Query berubah.")

    if (
        not gallery["recording_id"].is_unique
        or not query["recording_id"].is_unique
    ):
        raise ValueError("Ditemukan recording_id duplikat.")

    print("Memuat model...", flush=True)
    extractor = AudioRepresentationExtractor(rep)

    print("Mengekstrak Gallery...", flush=True)
    gal_feats = extract_split(
        extractor, gallery, "gallery", DIMENSIONS[rep]
    )

    print("Mengekstrak Query...", flush=True)
    qry_feats = extract_split(
        extractor, query, "query_clean", DIMENSIONS[rep]
    )

    if sha256_file(MANIFEST) != manifest_hash:
        raise ValueError("Manifest berubah selama ekstraksi.")

    summary, _ = evaluate_retrieval_corpus(
        qry_feats,
        query["species_key"].tolist(),
        gal_feats,
        gallery["species_key"].tolist(),
    )

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S_%fZ"
    )
    out_dir = (
        ROOT / "results/reproductions"
        / f"E4_clean_cache_{rep}_{timestamp}"
    )
    out_dir.mkdir(parents=True, exist_ok=False)

    cache_payload = {
        "gal_feats": gal_feats,
        "qry_feats": qry_feats,
        "gal_ids": np.asarray(gallery["recording_id"], dtype=str),
        "qry_ids": np.asarray(query["recording_id"], dtype=str),
        "gal_labels": np.asarray(gallery["species_key"], dtype=str),
        "qry_labels": np.asarray(query["species_key"], dtype=str),
        "representation": np.array(rep),
        "manifest_sha256": np.array(manifest_hash),
    }
    if checkpoint_hash is not None:
        cache_payload["checkpoint_sha256"] = np.array(checkpoint_hash)
    if rep == "R3":
        cache_payload["r3_control_version"] = np.array(R3_CONTROL_VERSION)

    artifact_cache = out_dir / f"clean_embeddings_{rep}.npz"
    np.savez_compressed(artifact_cache, **cache_payload)

    # The legacy E4 runner still reads this compatibility location.  Keep the
    # canonical, timestamped copy above as the auditable cache and create the
    # compatibility file only after it has been written successfully.
    COMPATIBILITY_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    compatibility_cache = COMPATIBILITY_CACHE_DIR / f"clean_embeddings_{rep}.npz"
    temporary_cache = compatibility_cache.with_suffix(".tmp.npz")
    np.savez_compressed(temporary_cache, **cache_payload)
    temporary_cache.replace(compatibility_cache)

    metadata = {
        "representation": rep,
        "manifest_sha256": manifest_hash,
        "checkpoint_sha256": checkpoint_hash,
        "gallery_count": len(gallery),
        "query_count": len(query),
        "clean_map10": float(summary["mAP@10"]),
        "clean_top1": float(summary["mean_top1"]),
        "purpose": "Clean cache only, no E2/E3/E4 inference",
    }
    if rep == "R3":
        metadata["r3_control_version"] = R3_CONTROL_VERSION

    (out_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8"
    )
    (out_dir / "README.md").write_text(
        "# Cache embedding bersih\\n\\n"
        "Artefak ini hanya menyimpan embedding gallery dan query bersih dari "
        "manifes aktif. Artefak ini bukan hasil E4 dan tidak memuat pencampuran "
        "derau, metrik kondisi derau, atau kesimpulan penelitian.\\n",
        encoding="utf-8",
    )

    print("\n=== HASIL CACHE CLEAN ===")
    print("Folder:", out_dir)
    print("Cache kompatibilitas:", compatibility_cache)
    print("Gallery:", gal_feats.shape)
    print("Query:", qry_feats.shape)
    print(f"mAP@10: {summary['mAP@10']:.8f}")
    print(f"Top1: {summary['mean_top1']:.8f}")
    print("STATUS: BERHASIL", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("representation", choices=["R1", "R2", "R3"])
    args = parser.parse_args()
    main(args.representation)
