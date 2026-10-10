"""
Script: scripts/build_indonesia_dataset_split.py
Fungsi: Membangun partisi resmi Strict Author-Disjoint Split untuk dataset 20 spesies
        burung Indonesia (1.217 audio fisik terverifikasi), membekukan manifes
        dataset_split.csv, species_freeze.csv, species_excluded.csv, dan memverifikasi
        zero leakage.
"""

from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_DIR = PROJECT_ROOT / "data" / "manifests"

AUDIT_LOG_CSV = MANIFEST_DIR / "download_audit_log.csv"
TRAIN_CSV = MANIFEST_DIR / "indonesia_train.csv"
RANKING_CSV = MANIFEST_DIR / "kandidat_ranking_lengkap_indonesia.csv"

OUT_SPLIT_CSV = MANIFEST_DIR / "dataset_split.csv"
OUT_FREEZE_CSV = MANIFEST_DIR / "species_freeze.csv"
OUT_EXCLUDED_CSV = MANIFEST_DIR / "species_excluded.csv"


def build_split():
    print("=" * 80)
    print("[*] MEMBANGUN PARTISI RESMI STRICT AUTHOR-DISJOINT SPLIT (BURUNG INDONESIA)")
    print("=" * 80)

    audit_df = pd.read_csv(AUDIT_LOG_CSV)
    train_df = pd.read_csv(TRAIN_CSV)
    train_df["recording_id"] = train_df["filename"].apply(lambda x: Path(x).stem)

    merged = pd.merge(train_df, audit_df[["recording_id", "sha256", "duration_sec", "bytes", "is_decodable"]], on="recording_id")
    print(f"[+] Total audio terverifikasi fisik: {len(merged):,} klip")

    authors = sorted(merged["author"].unique())
    author2idx = {a: i for i, a in enumerate(authors)}
    species = sorted(merged["primary_label"].unique())
    sp2idx = {s: i for i, s in enumerate(species)}

    arr_author = np.array([author2idx[a] for a in merged["author"]], dtype=np.int32)
    arr_sp = np.array([sp2idx[s] for s in merged["primary_label"]], dtype=np.int32)
    N_authors = len(authors)
    N_sp = len(species)
    N_clips = len(merged)

    # Seed 19 terbukti menghasilkan partisi seimbang: 60 Galeri, 26 Kueri, 25 Kalibrasi
    rng = np.random.default_rng(19)
    perm = rng.permutation(N_authors)

    gal_auth_set = set([authors[i] for i in perm[:60]])
    qry_auth_set = set([authors[i] for i in perm[60:86]])
    cal_auth_set = set([authors[i] for i in perm[86:]])

    def assign_role(auth):
        if auth in gal_auth_set:
            return "gallery"
        elif auth in qry_auth_set:
            return "query_clean"
        elif auth in cal_auth_set:
            return "calibration"
        else:
            raise ValueError(f"Author {auth} tidak terpetakan!")

    merged["split_role"] = merged["author"].apply(assign_role)

    # Susun kolom resmi dataset_split.csv persis schema baku
    split_df = pd.DataFrame({
        "recording_id": merged["recording_id"],
        "species_key": merged["primary_label"],
        "scientific_name": merged["scientific_name"],
        "common_name": merged["common_name"],
        "author": merged["author"],
        "rating": merged["rating"],
        "latitude": merged["latitude"],
        "longitude": merged["longitude"],
        "file_path": merged["primary_label"].apply(lambda sp: f"data/xeno_canto_indonesia/{sp}") + "/" + merged["recording_id"] + ".mp3",
        "split_role": merged["split_role"]
    })

    split_df.sort_values(by=["split_role", "species_key", "recording_id"], inplace=True)
    split_df.to_csv(OUT_SPLIT_CSV, index=False)
    print(f"[+] Manifes resmi dataset_split.csv berhasil disimpan di: {OUT_SPLIT_CSV}")

    # Cetak ringkasan per role
    role_summary = split_df["split_role"].value_counts()
    print("\n[+] Rincian Alokasi Partisi:")
    for role, count in role_summary.items():
        n_auth = split_df[split_df["split_role"] == role]["author"].nunique()
        print(f"  - {role:<12}: {count:4d} klip ({count/N_clips*100:.1f}%) | {n_auth:2d} perekam independen")

    # Cetak minimal per spesies
    sp_summary = split_df.groupby(["species_key", "split_role"]).size().unstack(fill_value=0)
    print("\n[+] Matriks Alokasi per Spesies:")
    print(sp_summary.to_string())

    # -------------------------------------------------------------
    # 2. Bekukan species_freeze.csv
    # -------------------------------------------------------------
    freeze_df = merged.groupby(["primary_label", "scientific_name", "common_name"]).agg(
        n_klip=("recording_id", "count"),
        n_author=("author", "nunique"),
        rating_median=("rating", "median")
    ).reset_index()
    freeze_df.rename(columns={"primary_label": "species_key"}, inplace=True)
    freeze_df.sort_values(by=["n_author", "n_klip"], ascending=[False, False], inplace=True)
    freeze_df.to_csv(OUT_FREEZE_CSV, index=False)
    print(f"\n[+] Manifes resmi species_freeze.csv berhasil disimpan di: {OUT_FREEZE_CSV}")

    # -------------------------------------------------------------
    # 3. Bekukan species_excluded.csv dari 200 kandidat lainnya
    # -------------------------------------------------------------
    if RANKING_CSV.exists():
        rank_df = pd.read_csv(RANKING_CSV)
        target_scis = set(freeze_df["scientific_name"])
        excluded_df = rank_df[~rank_df["scientific_name"].isin(target_scis)].copy()
        excluded_df["alasan_eksklusi"] = "Di luar kuota Top 20 taksa terpilih (DEC-10 ranking)"
        excluded_df.rename(columns={
            "scientific_name": "scientific_name",
            "en": "common_name",
            "total_klip": "n_klip",
            "author_unik": "n_author",
            "rating_AB_pct": "rating_AB_persen"
        }, inplace=True)
        cols_exc = ["ranking", "scientific_name", "common_name", "n_klip", "n_author", "alasan_eksklusi"]
        excluded_df[cols_exc].to_csv(OUT_EXCLUDED_CSV, index=False)
        print(f"[+] Manifes species_excluded.csv (200 spesies) berhasil disimpan di: {OUT_EXCLUDED_CSV}")

    # -------------------------------------------------------------
    # 4. Validasi Zero Leakage Formal
    # -------------------------------------------------------------
    print("\n[*] Menjalankan verifikasi zero leakage:")
    gal_ids = set(split_df[split_df["split_role"] == "gallery"]["recording_id"])
    qry_ids = set(split_df[split_df["split_role"] == "query_clean"]["recording_id"])
    cal_ids = set(split_df[split_df["split_role"] == "calibration"]["recording_id"])

    assert len(gal_ids.intersection(qry_ids)) == 0, "BOCOR ID: Galeri vs Kueri"
    assert len(gal_ids.intersection(cal_ids)) == 0, "BOCOR ID: Galeri vs Kalibrasi"
    assert len(qry_ids.intersection(cal_ids)) == 0, "BOCOR ID: Kueri vs Kalibrasi"
    print("  [PASS] Zero Recording ID Overlap (0 kebocoran ID)")

    gal_authors = set(split_df[split_df["split_role"] == "gallery"]["author"])
    qry_authors = set(split_df[split_df["split_role"] == "query_clean"]["author"])
    cal_authors = set(split_df[split_df["split_role"] == "calibration"]["author"])

    assert len(gal_authors.intersection(qry_authors)) == 0, "BOCOR AUTHOR: Galeri vs Kueri"
    assert len(gal_authors.intersection(cal_authors)) == 0, "BOCOR AUTHOR: Galeri vs Kalibrasi"
    assert len(qry_authors.intersection(cal_authors)) == 0, "BOCOR AUTHOR: Kueri vs Kalibrasi"
    print("  [PASS] Strict Global Recordist-Disjoint (0 kebocoran author)")

    print("\n[+] SELURUH VERIFIKASI DATASET SELESAI & SUKSES 100%!")


if __name__ == "__main__":
    build_split()
