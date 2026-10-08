import pandas as pd

df = pd.read_csv(r"D:\FILE AND TASK\TA\data\manifests\dataset_split.csv")

gal = df[df["split_role"] == "gallery"]
qry = df[df["split_role"] == "query_clean"]
cal = df[df["split_role"] == "calibration"]

print("=" * 60)
print("AUDIT KELENGKAPAN & KEBOCORAN DATA: dataset_split.csv")
print("=" * 60)
print(f"Total baris      : {len(df):,} baris")
print(f"Gallery          : {len(gal):,} klip ({gal['author'].nunique()} author unik)")
print(f"Query Clean      : {len(qry):,} klip ({qry['author'].nunique()} author unik)")
print(f"Calibration      : {len(cal):,} klip ({cal['author'].nunique()} author unik)")

print("\n1. IRISAN ID REKAMAN (recording_id):")
id_g_q = len(set(gal["recording_id"]) & set(qry["recording_id"]))
id_g_c = len(set(gal["recording_id"]) & set(cal["recording_id"]))
id_q_c = len(set(qry["recording_id"]) & set(cal["recording_id"]))
print(f"  - Gallery vs Query       : {id_g_q} (Harus 0)")
print(f"  - Gallery vs Calibration : {id_g_c} (Harus 0)")
print(f"  - Query vs Calibration   : {id_q_c} (Harus 0)")

print("\n2. IRISAN BERKAS FISIK (file_path):")
p_g_q = len(set(gal["file_path"]) & set(qry["file_path"]))
p_g_c = len(set(gal["file_path"]) & set(cal["file_path"]))
p_q_c = len(set(qry["file_path"]) & set(cal["file_path"]))
print(f"  - Gallery vs Query       : {p_g_q} (Harus 0)")
print(f"  - Gallery vs Calibration : {p_g_c} (Harus 0)")
print(f"  - Query vs Calibration   : {p_q_c} (Harus 0)")

print("\n3. IRISAN PEREKAM (author / recordist):")
gal_authors = set(gal["author"].dropna().unique())
qry_authors = set(qry["author"].dropna().unique())
cal_authors = set(cal["author"].dropna().unique())

a_g_q = len(gal_authors & qry_authors)
a_g_c = len(gal_authors & cal_authors)
a_q_c = len(qry_authors & cal_authors)
print(f"  - Gallery vs Query       : {a_g_q} (Harus 0)")
print(f"  - Gallery vs Calibration : {a_g_c} (Harus 0)")
print(f"  - Query vs Calibration   : {a_q_c} (Harus 0)")

total_unique_authors = df["author"].nunique()
sum_authors = len(gal_authors) + len(qry_authors) + len(cal_authors)
is_disjoint = (total_unique_authors == sum_authors) and (a_g_q == 0) and (a_g_c == 0) and (a_q_c == 0)

print("\n" + "=" * 60)
print(f"Total Author Unik Global         : {total_unique_authors}")
print(f"Penjumlahan Author Ketiga Subset : {sum_authors}")
print(f"STATUS RESMI BEBAS KEBOCORAN     : {'100% BEBAS BOCOR (TERATASI PENUH)' if is_disjoint else 'ADA KEBOCORAN'}")
print("=" * 60)
