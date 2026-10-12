"""Read-only preflight: physical files, manifest identity, SHA-256 and leakage.

Standard library only. Does not import experiment runners or write any file.
This validates the active split/download/noise/unknown manifests and selected
supporting manifests, not the scientific correctness of every project CSV.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
from pathlib import Path, PureWindowsPath
import sys
import unicodedata

AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".opus", ".m4a", ".aac", ".wma"}
FOLDERS = ("xeno_canto_indonesia", "xeno_canto_indonesia_unknowns", "itera_noise")


def normalize_label(value):
    return " ".join(unicodedata.normalize("NFC", value or "").casefold().split())


def safe_path(root, value):
    value = (value or "").replace("\\", "/")
    if not value or Path(value).is_absolute() or PureWindowsPath(value).drive:
        raise ValueError("Path harus relatif terhadap proyek: " + value)
    result = (root / value).resolve()
    if not result.is_relative_to(root):
        raise ValueError("Path keluar dari proyek: " + value)
    if not result.is_relative_to(root / "data"):
        raise ValueError("Path audio di luar data/: " + value)
    return result


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_project(root, progress=None):
    root = Path(root).resolve()
    issues = []
    references = []
    manifest_counts = {}
    manifest_fingerprints = {}

    def issue(level, code, message):
        issues.append({"level": level, "code": code, "message": message})

    def table(name, required, optional=False):
        path = root / "data/manifests" / name
        if optional and not path.exists():
            return []
        try:
            contents = path.read_bytes()
            manifest_fingerprints[name] = hashlib.sha256(contents).hexdigest()
            with io.StringIO(contents.decode("utf-8-sig"), newline="") as stream:
                reader = csv.DictReader(stream)
                if not set(required).issubset(reader.fieldnames or []):
                    raise ValueError("Kolom wajib: " + ", ".join(required))
                rows = list(reader)
            manifest_counts[name] = len(rows)
            if not rows:
                issue("ERROR", "empty_manifest", str(path))
            return rows
        except (OSError, UnicodeError, csv.Error, ValueError) as error:
            issue("ERROR", "manifest_unreadable", f"{path}: {error}")
            return []

    def unique_ids(rows, column, source):
        counts = Counter(row.get(column, "") for row in rows)
        for key, count in counts.items():
            if not key or count > 1:
                issue("ERROR", "duplicate_or_empty_id", f"{source}: {column}={key!r}, n={count}")

    def reference(row, source, role="", category="", expected="", size=""):
        try:
            path = safe_path(root, row.get("file_path", ""))
        except (OSError, ValueError) as error:
            issue("ERROR", "unsafe_path", f"{source}: {error}")
            return
        references.append({"path": path, "source": source, "role": role,
                           "category": category, "expected": expected.strip().lower(), "size": size})

    split = table("dataset_split.csv", ("recording_id", "species_key", "scientific_name", "author", "file_path", "split_role"))
    download = table("download_manifest.csv", ("recording_id", "file_path", "sha256", "bytes", "status"))
    noise = table("itera_noise_manifest.csv", ("filename", "sha256_checksum"))
    unknown = table("unknown_open_set_manifest.csv", ("unknown_id", "split_role", "source_category", "source_label", "file_path", "sha256"))
    unique_ids(split, "recording_id", "dataset_split.csv")
    unique_ids(download, "recording_id", "download_manifest.csv")
    unique_ids(unknown, "unknown_id", "unknown_open_set_manifest.csv")
    unique_ids(noise, "filename", "itera_noise_manifest.csv")
    split_by_id = {row["recording_id"]: row for row in split}
    download_by_id = {row["recording_id"]: row for row in download}
    if set(split_by_id) != set(download_by_id):
        issue("ERROR", "download_split_ids", "ID split/download berbeda: " +
              repr(sorted(set(split_by_id) ^ set(download_by_id))))
    authors = defaultdict(set)
    known_species = set()
    for row in split:
        role = row["split_role"]
        if role not in {"gallery", "query_clean", "calibration"}:
            issue("ERROR", "unknown_split_role", f"{row['recording_id']}: {role}")
        author = normalize_label(row["author"])
        if not author or author in {"unknown", "anonymous", "none", "nan"}:
            issue("ERROR", "missing_author", row["recording_id"])
        else:
            authors[role].add(author)
        known_species.add(normalize_label(row["scientific_name"]))
        reference(row, "dataset_split.csv", role, "target")
        other = download_by_id.get(row["recording_id"])
        if other and row["file_path"].replace("\\", "/") != other["file_path"].replace("\\", "/"):
            issue("ERROR", "download_split_path", row["recording_id"])
    for row in download:
        if row["status"] not in {"SUCCESS", "VERIFIED_EXISTING"}:
            issue("ERROR", "download_status", f"{row['recording_id']}: {row['status']}")
        reference(row, "download_manifest.csv", expected=row["sha256"], size=row["bytes"])
    roles = sorted(authors)
    if set(roles) != {"gallery", "query_clean", "calibration"}:
        issue("ERROR", "missing_split_role", "Gallery/query/calibration harus semuanya tersedia.")
    author_overlap = {}
    for i, a in enumerate(roles):
        for b in roles[i + 1:]:
            overlap = sorted(authors[a] & authors[b])
            author_overlap[a + " / " + b] = overlap
            if overlap:
                issue("ERROR", "author_overlap", f"{a}/{b}: {overlap}")

    noise_paths = set()
    for row in noise:
        mapped = {"file_path": "data/itera_noise/" + row["filename"]}
        reference(mapped, "itera_noise_manifest.csv", expected=row["sha256_checksum"])
        try:
            noise_paths.add(safe_path(root, mapped["file_path"]))
        except ValueError:
            pass
    unknown_species = defaultdict(set)
    reserved_noise = set()
    noise_sessions = defaultdict(set)
    for row in unknown:
        role, category = row["split_role"], row["source_category"]
        if category == "itera_environmental_noise":
            category = "environmental_noise"
        if role not in {"unknown_calibration", "unknown_test"}:
            issue("ERROR", "unknown_open_role", f"{row['unknown_id']}: {role}")
        if category not in {"non_target_species", "environmental_noise"}:
            issue("ERROR", "unknown_category", f"{row['unknown_id']}: {category}")
        reference(row, "unknown_open_set_manifest.csv", role, category, row["sha256"])
        if category == "non_target_species":
            species = normalize_label(row["source_label"])
            if not species:
                issue("ERROR", "empty_unknown_species", row["unknown_id"])
            unknown_species[role].add(species)
            if species in known_species:
                issue("ERROR", "known_species_in_unknown", row["unknown_id"] + ": " + species)
        elif category == "environmental_noise":
            try:
                physical = safe_path(root, row["file_path"])
                reserved_noise.add(physical)
                if physical not in noise_paths:
                    issue("ERROR", "noise_reserve_not_in_pool", row["file_path"])
                noise_sessions[role].add((str(physical.parent), physical.name[:8]))
            except ValueError:
                pass
    species_overlap = sorted(unknown_species["unknown_calibration"] & unknown_species["unknown_test"])
    if species_overlap:
        issue("ERROR", "unknown_species_overlap", repr(species_overlap))
    shared_sessions = noise_sessions["unknown_calibration"] & noise_sessions["unknown_test"]
    if shared_sessions:
        issue("WARN", "noise_session_overlap", f"{len(shared_sessions)} grup folder/tanggal beririsan antara unknown calibration/test; bukan bukti audio identik.")
    if any(row["source_category"] == "non_target_species" for row in unknown):
        issue("WARN", "unknown_authors_not_checked", "Manifes unknown tidak memiliki author; pemisahan perekam known/unknown dan antar unknown belum dibuktikan pemeriksa ini.")

    # Supporting manifests with physical paths; no experiment outputs are read.
    audit_log = table("download_audit_log.csv", ("recording_id", "file_path", "sha256", "bytes"), optional=True)
    if audit_log:
        unique_ids(audit_log, "recording_id", "download_audit_log.csv")
        if {row["recording_id"] for row in audit_log} != set(download_by_id):
            log_ids = {row["recording_id"] for row in audit_log}
            issue("WARN", "audit_download_ids", "Log unduhan tidak identik dengan manifes aktif; tambahan=" +
                  repr(sorted(log_ids - set(download_by_id))) + "; tidak tercatat=" +
                  repr(sorted(set(download_by_id) - log_ids)) + ". Log dapat berisi riwayat; jangan dihapus otomatis.")
        for row in audit_log:
            reference(row, "download_audit_log.csv", expected=row["sha256"], size=row["bytes"])
    train = table("indonesia_train.csv", ("filename", "primary_label"), optional=True)
    if train:
        train_paths = {row["filename"].replace("\\", "/") for row in train}
        split_paths = {row["file_path"].replace("\\", "/").removeprefix("data/xeno_canto_indonesia/") for row in split}
        if train_paths != split_paths:
            issue("WARN", "train_split_paths", "indonesia_train berbeda dari split aktif; tambahan=" +
                  repr(sorted(train_paths - split_paths)) + "; tidak tercatat=" + repr(sorted(split_paths - train_paths)))
    for row in train:
        reference({"file_path": "data/xeno_canto_indonesia/" + row["filename"]}, "indonesia_train.csv")
    freeze = table("species_freeze.csv", ("species_key", "n_klip"), optional=True)
    counts = Counter(row["species_key"] for row in split)
    unique_ids(freeze, "species_key", "species_freeze.csv")
    for row in freeze:
        try:
            if int(row["n_klip"]) != counts[row["species_key"]]:
                issue("ERROR", "species_count", f"{row['species_key']}: freeze={row['n_klip']}, split={counts[row['species_key']]}")
        except ValueError:
            issue("ERROR", "invalid_species_count", repr(row))

    physical = set()
    folder_counts = {}
    for folder in FOLDERS:
        directory = root / "data" / folder
        if not directory.is_dir():
            issue("ERROR", "missing_audio_folder", str(directory))
        files = set()
        for p in directory.rglob("*"):
            if p.is_file() and p.suffix.lower() in AUDIO_EXTENSIONS:
                resolved = p.resolve()
                if not resolved.is_relative_to(root):
                    issue("ERROR", "physical_path_outside_project", str(p))
                else:
                    files.add(resolved)
        folder_counts[folder] = len(files)
        physical.update(files)
    referenced = {ref["path"] for ref in references}
    by_hash = defaultdict(list)
    checksums = {}
    for index, path in enumerate(sorted(physical | referenced), 1):
        if not path.is_file():
            issue("ERROR", "missing_audio", str(path))
            continue
        try:
            before = path.stat()
            checksums[path] = sha256(path)
            after = path.stat()
            if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                issue("ERROR", "audio_changed_during_hash", str(path))
            by_hash[checksums[path]].append(path)
        except OSError as error:
            issue("ERROR", "audio_unreadable", f"{path}: {error}")
        if progress and index % 250 == 0:
            progress(index, len(physical | referenced))
    roles_by_path = defaultdict(set)
    for ref in references:
        path, expected = ref["path"], ref["expected"]
        if path not in checksums:
            continue
        if expected and (len(expected) != 64 or expected != checksums[path]):
            issue("ERROR", "checksum_mismatch", f"{ref['source']}: {path}")
        if not expected and ref["source"] in {"download_manifest.csv", "download_audit_log.csv", "unknown_open_set_manifest.csv", "itera_noise_manifest.csv"}:
            issue("ERROR", "missing_checksum", f"{ref['source']}: {path}")
        if ref["size"]:
            try:
                if float(ref["size"]) != path.stat().st_size:
                    issue("ERROR", "byte_size_mismatch", f"{ref['source']}: {path}")
            except (OSError, ValueError):
                issue("ERROR", "invalid_byte_size", f"{ref['source']}: {path}")
        if ref["role"]:
            roles_by_path[path].add(ref["category"] + ":" + ref["role"])
    duplicates = []
    for digest, paths in by_hash.items():
        roles_for_hash = set().union(*(roles_by_path[path] for path in paths))
        if len(roles_for_hash) > 1:
            issue("ERROR", "cross_role_identical_audio", f"{sorted(roles_for_hash)}: {[str(p.relative_to(root)) for p in paths]}")
        if len(paths) > 1:
            relative_paths = [str(p.relative_to(root)) for p in paths]
            duplicates.append({"sha256": digest, "paths": relative_paths, "roles": sorted(roles_for_hash)})
            issue("WARN", "physical_duplicate", repr(relative_paths))
    unreferenced = sorted(str(path.relative_to(root)) for path in physical - referenced)
    if unreferenced:
        issue("INFO", "unreferenced_audio", f"{len(unreferenced)} audio fisik tidak dirujuk manifes yang diperiksa; dapat berupa buffer, bukan otomatis berkas salah.")
    for name, digest in manifest_fingerprints.items():
        try:
            if sha256(root / "data/manifests" / name) != digest:
                issue("ERROR", "manifest_changed_during_audit", name)
        except OSError as error:
            issue("ERROR", "manifest_changed_during_audit", f"{name}: {error}")
    errors = sum(item["level"] == "ERROR" for item in issues)
    return {
        "status": "FAIL" if errors else "PASS_WITH_WARNINGS" if any(i["level"] == "WARN" for i in issues) else "PASS",
        "root": str(root), "manifest_counts": manifest_counts,
        "manifest_sha256": manifest_fingerprints,
        "split_counts": dict(Counter(row["split_role"] for row in split)),
        "author_counts": {key: len(value) for key, value in authors.items()},
        "author_overlap": author_overlap, "physical_audio_counts": folder_counts,
        "hashed_physical_files": len(checksums), "duplicate_groups": duplicates,
        "unreferenced_audio": unreferenced,
        "unknown_species_overlap": species_overlap,
        "reserved_noise": len(reserved_noise), "noise_available_for_mixing": len(noise_paths - reserved_noise),
        "issues": issues,
        "limitations": ["Checksum sama membuktikan file identik; checksum berbeda tidak menyingkirkan rekaman ulang/hasil transkode/potongan sesi sama.", "Pemisahan sesi/perekam unknown dan kontaminasi pretraining belum dibuktikan.", "Label bird-free tidak diverifikasi dari isi audio.", "Tidak mendekode audio, mengukur durasi, atau menilai hasil eksperimen; semua berkas hanya dibaca."],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--json", action="store_true", help="Cetak JSON ke terminal; tidak menyimpan file.")
    args = parser.parse_args()
    report = audit_project(args.root, lambda done, total: print(f"Checksum: {done}/{total}", file=sys.stderr, flush=True))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("PEMERIKSAAN MANIFES - READ ONLY")
        print("Status:", report["status"])
        print("Pembagian rekaman:", report["split_counts"])
        print("Perekam per kelompok:", report["author_counts"])
        print("Audio fisik:", report["physical_audio_counts"])
        print("File diperiksa SHA-256:", report["hashed_physical_files"])
        print("Derau dicadangkan:", report["reserved_noise"])
        print("Derau tersisa untuk pencampuran:", report["noise_available_for_mixing"])
        for item in report["issues"]:
            print(f"[{item['level']}] {item['code']}: {item['message']}")
        print("\nPASS hanya untuk pemeriksaan yang tercakup, bukan jaminan bebas kebocoran.")
        print("Tidak ada file yang diubah atau eksperimen yang dijalankan.")
    return int(report["status"] == "FAIL")


if __name__ == "__main__":
    raise SystemExit(main())
