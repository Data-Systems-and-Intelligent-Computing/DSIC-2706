
import hashlib
import json
import re
from pathlib import Path


REQUIRED_ASSETS = {
    "dataset_manifest",
    "noise_manifest",
    "R0_cache", "R1_cache", "R2_cache", "R3_cache",
    "R0_metadata", "R1_metadata", "R2_metadata", "R3_metadata",
    "R1_checkpoint", "R2_checkpoint",
    "preprocess_code", "mix_noise_code",
    "embeddings_code", "retrieve_code",
    "noise_identity_code", "query_identity_code",
    "run_identity_code", "e4_script",
}

REQUIRED_DESIGN = {
    "representations",
    "locations",
    "noise_categories",
    "snr_db",
    "repeat_ids",
    "category_seed",
    "noise_seed_rule",
    "n_gallery",
    "n_queries",
    "r3_seed",
}


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1048576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint_json(value):
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_run_identity(
    project_root,
    noise_fingerprint,
    query_fingerprint,
    assets,
    design,
):
    root = Path(project_root).resolve()

    for name, value in {
        "noise": noise_fingerprint,
        "query": query_fingerprint,
    }.items():
        if not isinstance(value, str) or not re.fullmatch(
            r"[0-9a-f]{64}", value
        ):
            raise ValueError(
                f"Fingerprint {name} bukan SHA256 valid."
            )

    if set(assets) != REQUIRED_ASSETS:
        raise ValueError(
            "Daftar aset berbeda. "
            f"Kurang={sorted(REQUIRED_ASSETS - set(assets))}, "
            f"Ekstra={sorted(set(assets) - REQUIRED_ASSETS)}"
        )

    if set(design) != REQUIRED_DESIGN:
        raise ValueError(
            "Konfigurasi desain tidak lengkap atau berlebih. "
            f"Kurang={sorted(REQUIRED_DESIGN - set(design))}, "
            f"Ekstra={sorted(set(design) - REQUIRED_DESIGN)}"
        )

    if design["representations"] != ["R0", "R1", "R2", "R3"]:
        raise ValueError("Daftar representasi berubah.")

    if design["repeat_ids"] != [0, 1, 2, 3]:
        raise ValueError("Harus ada empat pengulangan.")

    if design["n_gallery"] != 673 or design["n_queries"] != 311:
        raise ValueError("Ukuran dataset berubah.")

    asset_hashes = {}

    for name, location in sorted(assets.items()):
        path = Path(location)

        if not path.is_absolute():
            path = root / path

        path = path.resolve()

        try:
            relative = path.relative_to(root).as_posix()
        except ValueError as exc:
            raise ValueError(
                f"Aset di luar proyek: {name}"
            ) from exc

        if not path.is_file():
            raise FileNotFoundError(path)

        asset_hashes[name] = {
            "path": relative,
            "sha256": sha256_file(path),
        }

    identity = {
        "schema": "E4_run_identity_v1",
        "noise_fingerprint": noise_fingerprint,
        "query_fingerprint": query_fingerprint,
        "assets": asset_hashes,
        "design": design,
    }

    return identity, fingerprint_json(identity)
