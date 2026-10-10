"""
Script: scripts/build_indonesia_candidates.py
Fungsi: Memfilter dan menyusun tabel 20 kandidat spesies burung Indonesia
        dengan keragaman author tertinggi dan volume klip melimpah.
"""

import json
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_JSON = PROJECT_ROOT / "data" / "manifests" / "xeno_canto_indonesia_raw.json"
OUTPUT_CSV = PROJECT_ROOT / "data" / "manifests" / "kandidat_spesies_indonesia_metadata.csv"

# Kamus nama lokal bahasa Indonesia untuk burung umum Indonesia
LOCAL_NAMES = {
    "Pnoepyga pusilla": "Berencet kerdil",
    "Phyllergates cucullatus": "Cinenen gunung",
    "Cinnyris jugularis": "Burung-madu sriganti",
    "Cacomantis sepulcralis": "Wiwik uncuing",
    "Dicrurus hottentottus": "Srigunting gagak",
    "Malacocincla sepiaria": "Pelanduk semak",
    "Brachypteryx leucophris": "Cingcoang cokelat",
    "Pitta sordida": "Paok hijau",
    "Psilopogon armillaris": "Takur tohtor",
    "Caprimulgus macrurus": "Cabak maling",
    "Horornis vulcanius": "Cerik gunung",
    "Pycnonotus aurigaster": "Cucak kutilang",
    "Ducula aenea": "Pergam hijau",
    "Cuculus lepidus": "Kangkok melayu",
    "Brachypteryx montana": "Cingcoang alis-putih",
    "Aegithina tiphia": "Cipoh kacat",
    "Culicicapa ceylonensis": "Sikatan kepala-abu",
    "Todiramphus chloris": "Cekakak suci",
    "Caprimulgus affinis": "Cabak kota",
    "Orthotomus ruficeps": "Cinenen kelabu"
}

def main():
    with open(RAW_JSON, "r", encoding="utf-8") as f:
        records = json.load(f)

    df = pd.DataFrame(records)
    df = df[df["gen"].notna() & df["sp"].notna()].copy()
    df["scientific_name"] = df["gen"].str.strip() + " " + df["sp"].str.strip()
    df["common_name"] = df["en"].fillna("").str.strip()
    df["author"] = df["rec"].fillna("Unknown").str.strip()
    df["quality"] = df["q"].fillna("no score").str.strip().str.upper()
    df = df[df["author"].str.lower() != "unknown"].copy()

    sumatra_kw = ['sumat', 'lampung', 'aceh', 'kerinci', 'riau', 'jambi', 'medan', 'padang', 'way kambas', 'bengkulu']
    df['in_sumatra'] = df['loc'].fillna('').str.lower().apply(lambda s: any(k in s for k in sumatra_kw))

    # Ambil hanya spesies yang masuk target daftar 20 burung umum tersebar luas
    selected_species = list(LOCAL_NAMES.keys())

    res = []
    for sp in selected_species:
        g = df[df["scientific_name"] == sp]
        if len(g) == 0:
            continue
        cname = g["common_name"].iloc[0]
        n_clips = len(g)
        n_authors = g["author"].nunique()
        n_sumatra = g["in_sumatra"].sum()
        q_A = (g["quality"] == "A").sum()
        q_B = (g["quality"] == "B").sum()
        q_C = (g["quality"] == "C").sum()
        
        # Contoh lokasi rekaman
        valid_locs = g["loc"].dropna().unique().tolist()
        loc_sample = " ; ".join(valid_locs[:3]) if valid_locs else "Indonesia"
        
        res.append({
            "species_key": sp.lower().replace(" ", "_"),
            "scientific_name": sp,
            "indonesian_name": LOCAL_NAMES[sp],
            "english_name": cname,
            "total_clips_indonesia": n_clips,
            "unique_authors": n_authors,
            "clips_in_sumatra": n_sumatra,
            "rating_A": q_A,
            "rating_B": q_B,
            "rating_C": q_C,
            "rating_AB_pct": round((q_A + q_B) / n_clips * 100, 1),
            "sample_locations": loc_sample
        })

    df_out = pd.DataFrame(res)
    df_out.sort_values(by=["unique_authors", "total_clips_indonesia"], ascending=[False, False], inplace=True)
    df_out.reset_index(drop=True, inplace=True)
    df_out.to_csv(OUTPUT_CSV, index=False)
    print(f"[+] 20 Spesies Kandidat Burung Indonesia berhasil disimpan ke: {OUTPUT_CSV}")
    print(df_out[["scientific_name", "indonesian_name", "total_clips_indonesia", "unique_authors", "clips_in_sumatra", "rating_AB_pct"]].to_string(index=True))

if __name__ == "__main__":
    main()
