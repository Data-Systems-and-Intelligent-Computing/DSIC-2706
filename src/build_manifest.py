
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
"""
Script: src/build_manifest.py
Fungsi: Membangun partisi data bebas kebocoran (leakage-free split) untuk eksperimen retrieval.
Menghasilkan: data/manifests/dataset_split.csv

Kriteria Partisi (Sesuai Bab 11.2 Dokumen Audit):
1. Gallery Set (Reference Bank): Basis data representasi spesies acuan.
2. Query Clean Set: Kumpulan audio penguji pada kondisi bersih (E1).
3. Calibration Set: Kumpulan audio terpisah untuk mengkalibrasi threshold tau (E3).
4. Unknown Negative Set: Rekaman satwa non-burung dari unknown_open_set_manifest.csv.
5. Recordist-disjoint & Recording-disjoint: Tidak ada rekaman dengan ID yang sama
   yang muncul di dua partisi berbeda, dan diutamakan recordist yang berbeda antar Gallery dan Query.
"""

import os
import sys
import random
import pandas as pd

TARGET_MANIFEST = str(PROJECT_ROOT / "data/manifests/target_birds_manifest.csv")
UNKNOWN_MANIFEST = str(PROJECT_ROOT / "data/manifests/unknown_open_set_manifest.csv")
OUTPUT_SPLIT = str(PROJECT_ROOT / "data/manifests/dataset_split.csv")

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


def build_split():
    if not os.path.exists(TARGET_MANIFEST):
        print(f"[-] Target manifest belum siap: {TARGET_MANIFEST}")
        return False

    df_target = pd.read_csv(TARGET_MANIFEST)
    # Filter hanya berkas yang file fisik lokalnya benar-benar ada
    valid_mask = df_target['file_path'].apply(lambda p: os.path.exists(str(p)) and os.path.getsize(str(p)) > 1000 if pd.notna(p) else False)
    df_valid = df_target[valid_mask].copy()

    print(f"[*] Total file audio target valid: {len(df_valid)} dari {df_valid['species_key'].nunique()} spesies.")

    split_rows = []

    # Sesuai Bab 11.2 & 22 Audit: Partisi GLOBAL RECORDIST-DISJOINT
    # Memisahkan himpunan recordist secara global sehingga tidak ada recordist di Gallery
    # yang muncul di Query, sambil memastikan seluruh 16 spesies ada di Gallery dan Query.
    rec_counts = df_valid['recordist'].value_counts().to_dict()
    sp_recs = {sp: set(grp['recordist'].dropna().unique()) for sp, grp in df_valid.groupby('species_key')}
    all_recs = sorted(list(rec_counts.keys()))

    best_cut = None
    best_diff = 999999
    random.seed(RANDOM_SEED)

    for trial in range(10000):
        shuffled = all_recs.copy()
        random.shuffle(shuffled)
        split_pt = len(all_recs) * 3 // 5
        G = set(shuffled[:split_pt])
        Q = set(shuffled[split_pt:])

        if all(len(rset.intersection(G)) > 0 and len(rset.intersection(Q)) > 0 for rset in sp_recs.values()):
            n_g = sum(rec_counts[r] for r in G)
            n_q = sum(rec_counts[r] for r in Q)
            diff = abs(n_g - 260) + abs(n_q - 156)
            if diff < best_diff:
                best_diff = diff
                best_cut = (G, Q)

    if not best_cut:
        raise RuntimeError("Tidak ditemukan partisi global recordist-disjoint yang valid.")

    G_artists, Q_artists = best_cut
    print(f"[*] Partisi Recordist Global Ditemukan: {len(G_artists)} recordists Gallery vs {len(Q_artists)} recordists Query.")
    print(f"[*] Overlap Recordist: {len(G_artists.intersection(Q_artists))} (STRICT DISJOINT)")

    for sp_key, group in df_valid.groupby("species_key"):
        recs = group.to_dict("records")
        
        gallery = [r for r in recs if r.get('recordist') in G_artists]
        q_pool = [r for r in recs if r.get('recordist') in Q_artists]

        # Bagi q_pool menjadi query_clean (~65%) dan calibration (~35%)
        random.shuffle(q_pool)
        n_query = max(2, int(len(q_pool) * 0.65))
        query_clean = q_pool[:n_query]
        calibration = q_pool[n_query:]

        if not calibration and len(query_clean) > 2:
            calibration.append(query_clean.pop())

        for r in gallery:
            r['split_role'] = 'gallery'
            split_rows.append(r)
        for r in query_clean:
            r['split_role'] = 'query_clean'
            split_rows.append(r)
        for r in calibration:
            r['split_role'] = 'calibration'
            split_rows.append(r)


    # Tambahkan unknown open-set
    if os.path.exists(UNKNOWN_MANIFEST):
        df_unk = pd.read_csv(UNKNOWN_MANIFEST)
        unk_mask = df_unk['isolated_file_path'].apply(lambda p: os.path.exists(str(p)) and os.path.getsize(str(p)) > 1000 if pd.notna(p) else False)
        for _, r in df_unk[unk_mask].iterrows():
            split_rows.append({
                "id": r.get("id"),
                "species_key": f"{r.get('genus')}_{r.get('spesies')}",
                "scientific_name": r.get("nama_ilmiah"),
                "common_name": r.get("nama_inggris"),
                "is_endemic_sumatra": False,
                "quality": r.get("kualitas"),
                "recordist": r.get("perekam"),
                "date": "",
                "time": "",
                "country": "Indonesia",
                "locality": r.get("lokasi"),
                "latitude": r.get("latitude"),
                "longitude": r.get("longitude"),
                "elevation": "",
                "length_sec": r.get("durasi"),
                "license": "",
                "url_page": r.get("url_halaman"),
                "url_audio": r.get("url_audio"),
                "file_path": r.get("isolated_file_path"),
                "sha256": "",
                "status": "Unknown_OpenSet",
                "split_role": "unknown_test"
            })

    df_out = pd.DataFrame(split_rows)
    df_out.to_csv(OUTPUT_SPLIT, index=False, encoding="utf-8")

    print("\n" + "=" * 80)
    print("[+] SPLIT DATASET BERHASIL DIBENTUK!")
    print(f"[*] File Tersimpan: {OUTPUT_SPLIT}")
    print(f"[*] Distribusi Peran Split:\n{df_out['split_role'].value_counts()}")
    print("=" * 80)
    return True


if __name__ == "__main__":
    build_split()
