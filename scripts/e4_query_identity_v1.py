
import hashlib
import json
from pathlib import Path


def sha256_file(path):
    digest = hashlib.sha256()

    with Path(path).open("rb") as stream:
        for chunk in iter(
            lambda: stream.read(1024 * 1024),
            b""
        ):
            digest.update(chunk)

    return digest.hexdigest()


def build_query_audio_identity(query_df, project_root):
    root = Path(project_root).resolve()

    required = {
        "recording_id",
        "species_key",
        "file_path",
    }

    if not required.issubset(query_df.columns):
        raise ValueError("Kolom Query tidak lengkap.")

    if len(query_df) != 311:
        raise ValueError(
            f"Jumlah Query bukan 311: {len(query_df)}"
        )

    if query_df[list(required)].isna().any().any():
        raise ValueError("Ada nilai Query yang kosong.")

    ids = query_df["recording_id"].astype(str)

    if ids.duplicated().any():
        raise ValueError("Recording ID Query duplikat.")

    records = []

    for i, (_, row) in enumerate(query_df.iterrows()):
        query_id = str(row["recording_id"])
        path = Path(str(row["file_path"]))

        if not path.is_absolute():
            path = root / path

        path = path.resolve()

        if not path.is_file():
            raise FileNotFoundError(
                f"Query {query_id}: {path}"
            )

        try:
            relative_path = path.relative_to(root).as_posix()
        except ValueError as exc:
            raise ValueError(
                f"Audio Query di luar proyek: {path}"
            ) from exc

        records.append({
            "query_index": i,
            "query_id": query_id,
            "species_key": str(row["species_key"]),
            "path": relative_path,
            "size_bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        })

    identity = {
        "schema": "E4_query_audio_identity_v1",
        "ordered_queries": records,
    }

    encoded = json.dumps(
        identity,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    fingerprint = hashlib.sha256(encoded).hexdigest()

    return identity, fingerprint
