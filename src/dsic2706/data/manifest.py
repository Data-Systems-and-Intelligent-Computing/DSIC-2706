import os
import random
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "data", "manifests")
TARGET_MANIFEST = os.path.join(DATA_DIR, "target_birds_manifest.csv")
UNKNOWN_MANIFEST = os.path.join(DATA_DIR, "unknown_open_set_manifest.csv")
OUTPUT_SPLIT = os.path.join(DATA_DIR, "dataset_split.csv")


def build_strict_recordist_split(random_seed: int = 42) -> bool:
    if not os.path.exists(TARGET_MANIFEST):
        return False

    df_target = pd.read_csv(TARGET_MANIFEST)
    valid_mask = df_target['file_path'].apply(lambda p: os.path.exists(str(p)) and os.path.getsize(str(p)) > 1000 if pd.notna(p) else False)
    df_valid = df_target[valid_mask].copy()

    rec_counts = df_valid['recordist'].value_counts().to_dict()
    sp_recs = {sp: set(grp['recordist'].dropna().unique()) for sp, grp in df_valid.groupby('species_key')}
    all_recs = sorted(list(rec_counts.keys()))

    best_cut = None
    best_diff = 999999
    random.seed(random_seed)

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
        raise RuntimeError("Gagal menemukan cut recordist-disjoint.")

    G_artists, Q_artists = best_cut
    split_rows = []

    for sp_key, group in df_valid.groupby("species_key"):
        recs = group.to_dict("records")
        gallery = [r for r in recs if r.get('recordist') in G_artists]
        q_pool = [r for r in recs if r.get('recordist') in Q_artists]

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
    return True
