
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
"""
Script: src/isolate_unknown_open_set.py
Fungsi: Memisahkan rekaman satwa non-burung (Grasshoppers, Frogs, Land Mammals, Bats)
ke dalam folder khusus 'data/unknown_open_set/' agar tidak tercampur dengan target gallery burung.
Data ini difungsikan khusus sebagai negative test queries pada evaluasi Open-Set Rejection (E3).
"""

import os
import shutil
import pandas as pd

SRC_CATALOG = str(PROJECT_ROOT / "Dataset/Bioakustik_Sumatera/katalog_metadata_bioakustik.csv")
DEST_DIR = str(PROJECT_ROOT / "data/unknown_open_set")
DEST_CATALOG = str(PROJECT_ROOT / "data/manifests/unknown_open_set_manifest.csv")

os.makedirs(DEST_DIR, exist_ok=True)
os.makedirs(str(PROJECT_ROOT / "data/manifests"), exist_ok=True)

if not os.path.exists(SRC_CATALOG):
    print(f"[-] Katalog sumber tidak ditemukan: {SRC_CATALOG}")
    exit(1)

df = pd.read_csv(SRC_CATALOG)
non_birds = df[df['taksonomi'] != 'Birds'].copy()

print(f"[*] Ditemukan {len(non_birds)} entri satwa non-burung di katalog.")
print(non_birds['taksonomi'].value_counts())

transferred = 0
updated_records = []

for idx, row in non_birds.iterrows():
    local_path = str(row.get('file_path_lokal', ''))
    rec_id = str(row.get('id', ''))
    tax = str(row.get('taksonomi', 'Unknown'))
    species = str(row.get('spesies', 'sp'))
    genus = str(row.get('genus', 'gen'))

    tax_dest_dir = os.path.join(DEST_DIR, tax)
    os.makedirs(tax_dest_dir, exist_ok=True)

    dest_filename = f"UNKNOWN_XC{rec_id}_{genus}_{species}.mp3"
    dest_path = os.path.join(tax_dest_dir, dest_filename)

    file_exists = False
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        file_exists = True
        transferred += 1
    elif os.path.exists(local_path) and os.path.getsize(local_path) > 1000:
        try:
            shutil.copy2(local_path, dest_path)
            file_exists = True
            transferred += 1
        except Exception as err:
            print(f"      [-] Warning copy {local_path} -> {dest_path}: {err}", flush=True)

    row_dict = row.to_dict()
    row_dict['isolated_file_path'] = dest_path if file_exists else ""
    row_dict['role'] = "open_set_unknown_query"
    updated_records.append(row_dict)

# Simpan manifest khusus unknown
df_unknown = pd.DataFrame(updated_records)
df_unknown.to_csv(DEST_CATALOG, index=False, encoding="utf-8")

print(f"[+] Berhasil memisahkan {transferred} file audio satwa non-burung ke: {DEST_DIR}")
print(f"[+] Manifest unknown tersimpan di: {DEST_CATALOG}")
