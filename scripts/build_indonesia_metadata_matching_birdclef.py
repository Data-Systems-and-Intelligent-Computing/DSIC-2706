"""
Script: scripts/build_indonesia_metadata_matching_birdclef.py
Fungsi: Membangun metadata 20 kandidat spesies burung Indonesia dengan struktur kolom
        yang 100% persis menyesuaikan format BirdCLEF:
        1. data/manifests/Metadata_Indonesia.xlsx (Menyesuaikan Metadata_BirdCLEF.xlsx)
        2. data/manifests/indonesia_train.csv (Menyesuaikan train.csv)
        3. data/manifests/indonesia_species_freeze.csv (Menyesuaikan species_freeze.csv)
        4. data/manifests/kandidat_ranking_lengkap_indonesia.csv (Seluruh 220 spesies teranking)
"""

import json
from pathlib import Path
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MANIFESTS_DIR = PROJECT_ROOT / "data" / "manifests"
RAW_JSON = MANIFESTS_DIR / "xeno_canto_indonesia_raw.json"

OUTPUT_EXCEL = MANIFESTS_DIR / "Metadata_Indonesia.xlsx"
OUTPUT_TRAIN_CSV = MANIFESTS_DIR / "indonesia_train.csv"
OUTPUT_FREEZE_CSV = MANIFESTS_DIR / "indonesia_species_freeze.csv"
OUTPUT_RANKING_CSV = MANIFESTS_DIR / "kandidat_ranking_lengkap_indonesia.csv"

# Definisi 20 Spesies Target: Semua Non-Endemik, Tersebar Luas, dan Hadir di Sumatera
SPECIES_CONFIG = [
    {"key": "pygcup1", "sci": "Pnoepyga pusilla", "local": "Berencet kerdil", "en": "Pygmy Cupwing"},
    {"key": "moutai1", "sci": "Phyllergates cucullatus", "local": "Cinenen gunung", "en": "Mountain Tailorbird"},
    {"key": "olbsun1", "sci": "Cinnyris jugularis", "local": "Burung-madu sriganti", "en": "Olive-backed Sunbird"},
    {"key": "rubcuc1", "sci": "Cacomantis sepulcralis", "local": "Wiwik uncuing", "en": "Rusty-breasted Cuckoo"},
    {"key": "hacdro1", "sci": "Dicrurus hottentottus", "local": "Srigunting gagak", "en": "Hair-crested Drongo"},
    {"key": "horbab1", "sci": "Malacocincla sepiaria", "local": "Pelanduk semak", "en": "Horsfield's Babbler"},
    {"key": "lessho1", "sci": "Brachypteryx leucophris", "local": "Cingcoang cokelat", "en": "Lesser Shortwing"},
    {"key": "hoopit1", "sci": "Pitta sordida", "local": "Paok hijau", "en": "Hooded Pitta"},
    {"key": "crseag1", "sci": "Spilornis cheela", "local": "Elang bido", "en": "Crested Serpent Eagle"},
    {"key": "latnig1", "sci": "Caprimulgus macrurus", "local": "Cabak maling", "en": "Large-tailed Nightjar"},
    {"key": "subwar1", "sci": "Horornis vulcanius", "local": "Cerik gunung", "en": "Sunda Bush Warbler"},
    {"key": "sohbul1", "sci": "Pycnonotus aurigaster", "local": "Cucak kutilang", "en": "Sooty-headed Bulbul"},
    {"key": "gpipig1", "sci": "Ducula aenea", "local": "Pergam hijau", "en": "Green Imperial Pigeon"},
    {"key": "suncuc1", "sci": "Cuculus lepidus", "local": "Kangkok melayu", "en": "Sunda Cuckoo"},
    {"key": "whbsho1", "sci": "Brachypteryx montana", "local": "Cingcoang alis-putih", "en": "White-browed Shortwing"},
    {"key": "comior1", "sci": "Aegithina tiphia", "local": "Cipoh kacat", "en": "Common Iora"},
    {"key": "ghcfly1", "sci": "Culicicapa ceylonensis", "local": "Sikatan kepala-abu", "en": "Grey-headed Canary-flycatcher"},
    {"key": "colkin1", "sci": "Todiramphus chloris", "local": "Cekakak suci", "en": "Collared Kingfisher"},
    {"key": "savnig1", "sci": "Caprimulgus affinis", "local": "Cabak kota", "en": "Savanna Nightjar"},
    {"key": "ashtai1", "sci": "Orthotomus ruficeps", "local": "Cinenen kelabu", "en": "Ashy Tailorbird"}
]

Q_TO_RATING = {"A": 5.0, "B": 4.0, "C": 3.0, "D": 2.0, "E": 1.0, "NO SCORE": 3.0}

def main():
    print("[*] Memuat data Xeno-Canto Indonesia mentah...")
    with open(RAW_JSON, "r", encoding="utf-8") as f:
        records = json.load(f)

    df_raw = pd.DataFrame(records)
    df_raw = df_raw[df_raw["gen"].notna() & df_raw["sp"].notna()].copy()
    df_raw["scientific_name"] = df_raw["gen"].str.strip() + " " + df_raw["sp"].str.strip()
    # Normalisasi author (title-case) untuk mencegah kebocoran perekam ganda
    df_raw["author"] = df_raw["rec"].fillna("Unknown").str.strip().str.title()
    df_raw = df_raw[df_raw["author"].str.lower() != "unknown"].copy()

    # Ekspor seluruh peringkat kandidat (220 spesies) untuk transparansi seleksi
    sumatra_kw = ['sumat', 'lampung', 'aceh', 'kerinci', 'riau', 'jambi', 'medan', 'padang', 'way kambas', 'bengkulu']
    df_raw['in_sumatra'] = df_raw['loc'].fillna('').str.lower().apply(lambda s: any(k in s for k in sumatra_kw))
    
    all_sp = df_raw[~df_raw["scientific_name"].str.lower().str.contains("mystery")].groupby(["scientific_name", "en"]).agg(
        total_klip=("id", "count"),
        author_unik=("author", "nunique"),
        klip_sumatera=("in_sumatra", "sum"),
        rating_A=("q", lambda q: (q.str.upper()=="A").sum()),
        rating_B=("q", lambda q: (q.str.upper()=="B").sum()),
        rating_C=("q", lambda q: (q.str.upper()=="C").sum()),
    ).reset_index()
    all_sp["rating_AB_pct"] = ((all_sp["rating_A"] + all_sp["rating_B"]) / all_sp["total_klip"] * 100).round(1)
    all_sp = all_sp[(all_sp["total_klip"] >= 20) & (all_sp["author_unik"] >= 5)].sort_values(
        by=["author_unik", "total_klip"], ascending=[False, False]
    ).reset_index(drop=True)
    all_sp.index += 1
    all_sp.to_csv(OUTPUT_RANKING_CSV, index_label="ranking")
    print(f"[+] Daftar seluruh 220 kandidat teranking disimpan ke: {OUTPUT_RANKING_CSV}")

    sci_to_cfg = {c["sci"]: c for c in SPECIES_CONFIG}
    target_scis = set(sci_to_cfg.keys())

    df_target = df_raw[df_raw["scientific_name"].isin(target_scis)].copy()
    print(f"[+] Total rekaman 20 spesies target: {len(df_target):,} klip")

    # -------------------------------------------------------------
    # 1. Format: species_freeze.csv (Menyesuaikan BirdCLEF freeze)
    # -------------------------------------------------------------
    freeze_rows = []
    excel_all_rows = []
    train_rows = []

    for cfg in SPECIES_CONFIG:
        sp_sci = cfg["sci"]
        sp_key = cfg["key"]
        sp_local = cfg["local"]
        sp_en = cfg["en"]

        g = df_target[df_target["scientific_name"] == sp_sci]
        n_klip = len(g)
        n_author = g["author"].nunique()
        ratings = [Q_TO_RATING.get(str(q).strip().upper(), 3.0) for q in g["q"]]
        med_rating = float(pd.Series(ratings).median())

        freeze_rows.append({
            "species_key": sp_key,
            "scientific_name": sp_sci,
            "common_name": sp_en,
            "n_klip": n_klip,
            "n_author": n_author,
            "rating_median": med_rating
        })

        for _, r in g.iterrows():
            rec_id = str(r.get("id", "")).strip()
            xc_id = f"XC{rec_id}"
            fname = f"{xc_id}.mp3"
            lat = float(r["lat"]) if pd.notna(r.get("lat")) and r.get("lat") != "" else None
            lon = float(r["lon"]) if pd.notna(r.get("lon")) and r.get("lon") != "" else None
            q_code = str(r.get("q", "no score")).strip().upper()
            rating_num = Q_TO_RATING.get(q_code, 3.0)
            smp_rate = int(r["smp"]) if pd.notna(r.get("smp")) and str(r.get("smp")).isdigit() else 44100
            sound_type = str(r.get("type", "call")).strip() or "call"
            rec_date = str(r.get("date", "")).strip()
            author_name = str(r.get("author", "Unknown")).strip()
            lic_url = str(r.get("lic", "https://creativecommons.org/licenses/by-nc-sa/4.0/")).strip()
            loc_name = str(r.get("loc", "Indonesia")).strip()
            xc_url = f"https://xeno-canto.org/{rec_id}"

            # Format 1: Menyesuaikan Metadata_BirdCLEF.xlsx persis
            excel_all_rows.append({
                "Spesies": sp_sci,
                "Sub-folder": "kandidat_indonesia",
                "Nama File": fname,
                "XC ID": xc_id,
                "Link XenoCanto": xc_url,
                "Latitude": lat if lat is not None else "-",
                "Longitude": lon if lon is not None else "-",
                "Lokasi": loc_name,
                "Negara": "Indonesia",
                "Sampling Rate (Hz)": smp_rate,
                "Kualitas (A-E)": q_code if q_code in ["A", "B", "C", "D", "E"] else "C",
                "Tipe Suara": sound_type,
                "Tanggal Rekaman": rec_date,
                "Rekorder": author_name,
                "Lisensi": lic_url,
                "_Species_Key": sp_key,
                "_Common_Name": sp_en
            })

            # Format 2: Menyesuaikan train.csv persis
            also_list = r.get("also", [])
            also_str = str(also_list) if isinstance(also_list, list) else "[]"
            type_str = f"['{sound_type}']"

            train_rows.append({
                "primary_label": sp_key,
                "secondary_labels": also_str,
                "type": type_str,
                "latitude": lat,
                "longitude": lon,
                "scientific_name": sp_sci,
                "common_name": sp_en,
                "class_name": "Aves",
                "inat_taxon_id": None,
                "author": author_name,
                "license": lic_url,
                "rating": rating_num,
                "url": xc_url,
                "filename": f"{sp_key}/{fname}",
                "collection": "XC"
            })

    # Simpan indonesia_species_freeze.csv
    df_freeze = pd.DataFrame(freeze_rows)
    df_freeze.to_csv(OUTPUT_FREEZE_CSV, index=False)
    print(f"[+] indonesia_species_freeze.csv berhasil dibuat di: {OUTPUT_FREEZE_CSV}")

    # Simpan indonesia_train.csv
    df_train = pd.DataFrame(train_rows)
    df_train.to_csv(OUTPUT_TRAIN_CSV, index=False)
    print(f"[+] indonesia_train.csv berhasil dibuat di: {OUTPUT_TRAIN_CSV}")

    # -------------------------------------------------------------
    # 2. Format: Metadata_Indonesia.xlsx (Sama persis Metadata_BirdCLEF.xlsx)
    # -------------------------------------------------------------
    wb = openpyxl.Workbook()

    COLUMNS = [
        "Spesies", "Sub-folder", "Nama File", "XC ID", "Link XenoCanto",
        "Latitude", "Longitude", "Lokasi", "Negara", "Sampling Rate (Hz)",
        "Kualitas (A-E)", "Tipe Suara", "Tanggal Rekaman", "Rekorder", "Lisensi"
    ]
    COL_WIDTHS = [24, 18, 16, 12, 32, 12, 12, 35, 12, 18, 14, 20, 16, 24, 38]

    thin = Side(border_style="thin", color="D9D9D9")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    def style_header(cell, color_hex="1F4E79"):
        cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=color_hex)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    def style_cell(cell, is_even, is_numeric=False):
        bg = "F2F2F2" if is_even else "FFFFFF"
        cell.font = Font(name="Calibri", size=10)
        cell.fill = PatternFill("solid", fgColor=bg)
        cell.alignment = Alignment(horizontal="right" if is_numeric else "left", vertical="center")
        cell.border = border

    # --- Sheet 1: SEMUA DATA ---
    ws_all = wb.active
    ws_all.title = "SEMUA DATA"
    ws_all.freeze_panes = "A2"
    ws_all.row_dimensions[1].height = 28

    for ci, (col, width) in enumerate(zip(COLUMNS, COL_WIDTHS), 1):
        cell = ws_all.cell(row=1, column=ci, value=col)
        style_header(cell, "1F4E79")
        ws_all.column_dimensions[get_column_letter(ci)].width = width

    for ri, row in enumerate(excel_all_rows, 2):
        even = (ri % 2 == 0)
        for ci, col in enumerate(COLUMNS, 1):
            val = row.get(col, "")
            is_num = col in ["Latitude", "Longitude", "Sampling Rate (Hz)"]
            c = ws_all.cell(row=ri, column=ci, value=val)
            style_cell(c, even, is_numeric=is_num)
            if col in ["Link XenoCanto", "Lisensi"] and isinstance(val, str) and val.startswith("http"):
                c.hyperlink = val
                c.font = Font(name="Calibri", size=10, color="0563C1", underline="single")
        ws_all.row_dimensions[ri].height = 20

    # --- Sheet 2: RINGKASAN SPESIES ---
    ws_sum = wb.create_sheet(title="RINGKASAN", index=1)
    ws_sum.freeze_panes = "A2"
    ws_sum.row_dimensions[1].height = 28

    sum_headers = [
        "No", "Spesies (Nama Ilmiah)", "Nama Indonesia", "Nama Inggris", "Kode eBird",
        "Total Rekaman", "Perekam Unik", "Median Rating", "Dominan Kualitas (A-B %)"
    ]
    sum_widths = [6, 28, 24, 28, 14, 16, 16, 16, 24]

    for ci, (col, width) in enumerate(zip(sum_headers, sum_widths), 1):
        c = ws_sum.cell(row=1, column=ci, value=col)
        style_header(c, "1F4E79")
        ws_sum.column_dimensions[get_column_letter(ci)].width = width

    for si, cfg in enumerate(SPECIES_CONFIG, 1):
        sp_sci = cfg["sci"]
        sp_rows = [r for r in excel_all_rows if r["Spesies"] == sp_sci]
        n_tot = len(sp_rows)
        n_rec = len(set(r["Rekorder"] for r in sp_rows))
        n_ab = sum(1 for r in sp_rows if r["Kualitas (A-E)"] in ["A", "B"])
        pct_ab = f"{round(n_ab / n_tot * 100, 1)}%" if n_tot > 0 else "0%"
        med_r = df_freeze[df_freeze["scientific_name"] == sp_sci]["rating_median"].iloc[0]

        vals = [si, sp_sci, cfg["local"], cfg["en"], cfg["key"], n_tot, n_rec, med_r, pct_ab]
        even = (si % 2 == 0)
        for ci, val in enumerate(vals, 1):
            c = ws_sum.cell(row=si+1, column=ci, value=val)
            style_cell(c, even, is_numeric=(ci in [1, 6, 7, 8]))
        ws_sum.row_dimensions[si+1].height = 20

    wb.save(OUTPUT_EXCEL)
    print(f"[+] Metadata_Indonesia.xlsx berhasil disimpan di: {OUTPUT_EXCEL}")

if __name__ == "__main__":
    main()
