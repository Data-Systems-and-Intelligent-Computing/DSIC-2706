
import hashlib
import json
import re
from pathlib import Path

import pandas as pd


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


def build_noise_identity(habitats, manifest_path, noise_dir, reserved):
    manifest_path = Path(manifest_path).resolve()
    noise_dir = Path(noise_dir).resolve()

    df = pd.read_csv(manifest_path)

    records = {}
    for row in df.itertuples(index=False):
        path = (noise_dir / str(row.filename)).resolve()

        if path in records:
            raise ValueError(f"Duplikat manifest: {path}")

        records[path] = row

    reserved_names = sorted(str(x).lower() for x in reserved)
    reserved_set = set(reserved_names)

    selected = []
    categories = set()

    for habitat, files in habitats.items():
        for candidate in files:
            path = Path(candidate).resolve()

            if path not in records:
                raise ValueError(f"Tidak ada di manifest: {path}")

            if not path.is_file():
                raise FileNotFoundError(path)

            if path.name.lower() in reserved_set:
                raise ValueError(f"Noise E3 masuk E4: {path}")

            row = records[path]

            if str(row.verified_bird_free).strip().lower() not in {
                "true", "1"
            }:
                raise ValueError(f"Tidak verified bird-free: {path}")

            declared = str(row.sha256_checksum).strip().lower()

            if not re.fullmatch(r"[0-9a-f]{64}", declared):
                raise ValueError(f"SHA256 manifest tidak valid: {path}")

            words = path.parent.name.split()

            if "Amplitudo" in words:
                mode = "Amplitudo"
            elif "Frequency" in words:
                mode = "Frequency"
            else:
                raise ValueError(f"Mode tidak diketahui: {path}")

            levels = [
                x for x in ("High", "Medium", "Low")
                if x in words
            ]

            if len(levels) != 1:
                raise ValueError(f"Level tidak jelas: {path}")

            category = f"{mode}-{levels[0]}"
            categories.add((habitat, category))

            stat = path.stat()

            selected.append({
                "habitat": habitat,
                "category": category,
                "path": path.relative_to(noise_dir).as_posix(),
                "declared_sha256": declared,
                "size_bytes": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            })

    if len(habitats) != 5:
        raise ValueError("Jumlah lokasi bukan lima.")

    if len(categories) != 30:
        raise ValueError("Tidak semua kelompok lokasi-kategori tersedia.")

    if len(selected) != 1528:
        raise ValueError(
            f"Jumlah kandidat berubah: {len(selected)}"
        )

    identity = {
        "noise_manifest_sha256": sha256_file(manifest_path),
        "e3_reserved_basenames": reserved_names,
        "ordered_candidates": selected,
    }

    return identity, fingerprint_json(identity)
