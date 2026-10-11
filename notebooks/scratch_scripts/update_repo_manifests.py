import os
import re
import hashlib
import time
import requests
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import yaml
import mutagen
from mutagen.mp3 import MP3

ROOT_DIR = r"D:\FILE AND TASK\TA"
XC_DIR = os.path.join(ROOT_DIR, "data", "xeno_canto")
MANIFEST_DIR = os.path.join(ROOT_DIR, "data", "manifests")
CONFIGS_DIR = os.path.join(ROOT_DIR, "configs")
EXCEL_PATH = os.path.join(XC_DIR, "Metadata_XenoCanto.xlsx")

API_KEY = "95dc5b3f6834b56e17da4cf68cc890cb470d1284"
HEADERS_HTTP = {
    "X-API-Key": API_KEY,
    "User-Agent": "BirdSoundResearch/1.0",
    "Accept": "application/json",
}

SPECIES_ENDEMIC_MAP = {
    "Apalharpactes_mackloti": True,
    "Apalharpactes mackloti": True,
    "Batrachostomus_poliolophus": True,
    "Caprimulgus_pulchellus": True,
    "Carpococcyx_viridis": True,
    "Erythropitta_venusta": True,
    "Gypsophila_rufipectus": True,
    "Hydrornis_schneideri": True,
    "Ixos_sumatranus": True,
    "Lophura_inornata": True,
    "Myophonus_melanurus": True,
    "Napothera_albostriata": True,
    "Pellorneum_buettikoferi": True,
    "Picus_dedemi": True,
    "Polyplectron_chalcurum": True,
}

def extract_xc_id(filename):
    match = re.search(r'XC(\d+)', filename, re.IGNORECASE)
    return match.group(1) if match else None

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def get_audio_info(filepath):
    try:
        audio = MP3(filepath)
        sr = int(audio.info.sample_rate)
        length_sec = round(audio.info.length, 2)
        mins = int(length_sec // 60)
        secs = int(length_sec % 60)
        length_str = f"{mins}:{secs:02d}"
        return sr, length_sec, length_str
    except Exception as e:
        print(f"Error reading MP3 {filepath}: {e}")
        return 44100, 0.0, "0:00"

def fetch_api_metadata(xc_id):
    urls = [
        f"https://xeno-canto.org/api/3/recordings?query=nr:{xc_id}&key={API_KEY}",
        f"https://xeno-canto.org/api/3/recordings/{xc_id}?key={API_KEY}",
    ]
    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS_HTTP, timeout=12)
            if resp.status_code == 200:
                data = resp.json()
                recs = data.get("recordings", [])
                if not recs and "id" in data:
                    recs = [data]
                if recs:
                    r = recs[0]
                    return {
                        "scientific_name": f"{r.get('gen', '')} {r.get('sp', '')}".strip(),
                        "common_name": r.get("en", ""),
                        "recordist": r.get("rec", "Unknown"),
                        "date": r.get("date", ""),
                        "time": r.get("time", ""),
                        "country": r.get("cnt", "Indonesia"),
                        "locality": r.get("loc", ""),
                        "latitude": r.get("lat", ""),
                        "longitude": r.get("lng", ""),
                        "elevation": r.get("ele", ""),
                        "license": r.get("lic", ""),
                        "quality": r.get("q", ""),
                        "type": r.get("type", ""),
                    }
        except Exception as e:
            pass
    return None

def main():
    species_folders = sorted([d for d in os.listdir(XC_DIR) if os.path.isdir(os.path.join(XC_DIR, d))])
    print(f"Ditemukan {len(species_folders)} folder spesies di {XC_DIR}")

    records = []
    api_cache = {}

    for s_folder in species_folders:
        s_path = os.path.join(XC_DIR, s_folder)
        subfolders = sorted([sub for sub in os.listdir(s_path) if os.path.isdir(os.path.join(s_path, sub))])
        
        for sub in subfolders:
            sub_path = os.path.join(s_path, sub)
            quality_from_folder = sub.upper()  # A, B, C, D, E
            
            for fname in sorted(os.listdir(sub_path)):
                if not fname.lower().endswith(".mp3"):
                    continue
                
                fp = os.path.join(sub_path, fname)
                xc_id = extract_xc_id(fname)
                if not xc_id:
                    print(f"Skipping non-XC file: {fname}")
                    continue
                
                print(f"Processing [{s_folder}/{sub}] XC{xc_id}...", flush=True)
                sr, length_sec, length_str = get_audio_info(fp)
                sha256 = compute_sha256(fp)
                
                if xc_id not in api_cache:
                    meta = fetch_api_metadata(xc_id)
                    api_cache[xc_id] = meta
                    time.sleep(0.3)
                else:
                    meta = api_cache[xc_id]
                
                if meta is None:
                    meta = {}
                
                sci_name = meta.get("scientific_name") or s_folder.replace("_", " ")
                com_name = meta.get("common_name") or s_folder.replace("_", " ")
                recordist = meta.get("recordist") or "Unknown"
                date_val = meta.get("date") or ""
                time_val = meta.get("time") or ""
                country = meta.get("country") or "Indonesia"
                locality = meta.get("locality") or ""
                lat = meta.get("latitude") or ""
                lng = meta.get("longitude") or ""
                ele = meta.get("elevation") or ""
                license_val = meta.get("license") or "https://creativecommons.org/licenses/by-nc-sa/4.0/"
                quality = quality_from_folder if quality_from_folder in ['A','B','C','D','E'] else (meta.get("quality") or "A")
                type_val = meta.get("type") or "song"
                
                # Rel path POSIX
                rel_path = f"data/xeno_canto/{s_folder}/{sub}/{fname}"
                
                rec = {
                    "id": xc_id,
                    "species_key": s_folder,
                    "scientific_name": sci_name,
                    "common_name": com_name,
                    "is_endemic_sumatra": SPECIES_ENDEMIC_MAP.get(s_folder, True),
                    "quality": quality,
                    "recordist": recordist,
                    "date": date_val,
                    "time": time_val,
                    "country": country,
                    "locality": locality,
                    "latitude": lat,
                    "longitude": lng,
                    "elevation": ele,
                    "length_sec_num": length_sec,
                    "length_sec": length_str,
                    "sampling_rate_hz": sr,
                    "license": license_val,
                    "url_page": f"https://xeno-canto.org/{xc_id}",
                    "url_audio": f"https://xeno-canto.org/{xc_id}/download",
                    "file_path": rel_path,
                    "sha256": sha256,
                    "status": "Ready_Existing",
                    "type": type_val,
                    "subfolder": sub,
                    "filename": fname
                }
                records.append(rec)

    print(f"\nTotal rekaman diproses: {len(records)}")

    # 1. Update datasets.yaml
    species_list_yaml = []
    unique_species = sorted(list(set(r["species_key"] for r in records)))
    for skey in unique_species:
        s_recs = [r for r in records if r["species_key"] == skey]
        sci = s_recs[0]["scientific_name"]
        com = s_recs[0]["common_name"]
        species_list_yaml.append({
            "species_key": skey,
            "scientific_name": sci,
            "common_name": com
        })
        
    ds_yaml = {
        "datasets": {
            "target_birds": {
                "source": "Xeno-Canto",
                "geographic_focus": "Sumatra & Indonesia Verified",
                "num_species": len(unique_species),
                "manifest_path": "data/manifests/target_birds_manifest.csv",
                "split_manifest_path": "data/manifests/dataset_split.csv",
                "audio_directory": "data/xeno_canto/",
                "species_list": species_list_yaml
            },
            "unknown_open_set": {
                "source": "Sumatran Non-Bird Fauna",
                "manifest_path": "data/manifests/unknown_open_set_manifest.csv",
                "audio_directory": "data/unknown_open_set/",
                "taxa_included": [
                    "Insects (Cicadas/Orthoptera)",
                    "Amphibians (Frogs/Toads)",
                    "Mammals (Primates/Bats)"
                ]
            },
            "itera_noise": {
                "directory": "data/itera_noise/",
                "sampling_rate": 32000,
                "sub_locations": [
                    "Embung ITERA (Aquatic / Amphibian ambient)",
                    "Arboretum / Kebun Raya ITERA (Forest canopy biophony)",
                    "Area Terbuka / Gedung Kuliah (Anthropogenic traffic/construction)"
                ]
            },
            "itera_soundscape": {
                "annotations_directory": "data/itera_soundscape_annotations/",
                "validation_subset_minutes": 30
            }
        }
    }
    
    with open(os.path.join(CONFIGS_DIR, "datasets.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(ds_yaml, f, sort_keys=False, default_flow_style=False)
    print("Updated configs/datasets.yaml")

    # 2. Write target_birds_manifest.csv
    headers = [
        "id", "species_key", "scientific_name", "common_name", "is_endemic_sumatra",
        "quality", "recordist", "date", "time", "country", "locality", "latitude",
        "longitude", "elevation", "length_sec", "license", "url_page", "url_audio",
        "file_path", "sha256", "status"
    ]
    
    manifest_csv_path = os.path.join(MANIFEST_DIR, "target_birds_manifest.csv")
    import csv
    with open(manifest_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for r in records:
            writer.writerow(r)
    print("Updated data/manifests/target_birds_manifest.csv")

    # 3. Create dataset_split.csv (Recordist-disjoint split)
    # Split rule per species:
    # Query: quality A/B prefered, disjoint recordists from gallery
    # Calibration: remaining or allocated per species
    # Gallery: the main reference set
    split_records = []
    
    for skey in unique_species:
        s_recs = [r for r in records if r["species_key"] == skey]
        recordists = sorted(list(set(r["recordist"] for r in s_recs)))
        
        # Sort recs by quality (A, B, C, D, E)
        q_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
        s_recs_sorted = sorted(s_recs, key=lambda x: q_map.get(x['quality'], 9))
        
        if len(s_recs) == 1:
            s_recs[0]['split_role'] = 'gallery'
            split_records.append(s_recs[0])
        elif len(s_recs) == 2:
            s_recs_sorted[0]['split_role'] = 'gallery'
            s_recs_sorted[1]['split_role'] = 'clean_query'
            split_records.extend(s_recs_sorted)
        else:
            # Multi-recordist split
            # Select 1 query recordist if possible, else 1 query file
            query_rec = s_recs_sorted[0]
            query_recordist = query_rec['recordist']
            
            query_rec['split_role'] = 'clean_query'
            
            # Calibration file
            calib_candidate = [r for r in s_recs_sorted[1:] if r['recordist'] != query_recordist]
            if calib_candidate and len(s_recs) >= 4:
                calib_rec = calib_candidate[0]
                calib_rec['split_role'] = 'calibration'
            elif len(s_recs_sorted) > 1:
                calib_rec = s_recs_sorted[1]
                calib_rec['split_role'] = 'gallery'
            
            for r in s_recs_sorted:
                if 'split_role' not in r:
                    r['split_role'] = 'gallery'
                split_records.append(r)
                
    split_headers = headers + ["split_role"]
    split_csv_path = os.path.join(MANIFEST_DIR, "dataset_split.csv")
    with open(split_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=split_headers, extrasaction="ignore")
        writer.writeheader()
        for r in split_records:
            writer.writerow(r)
    print("Updated data/manifests/dataset_split.csv")

    # 4. Rebuild Metadata_XenoCanto.xlsx
    wb = openpyxl.Workbook()
    ws_all = wb.active
    ws_all.title = "SEMUA DATA"
    ws_all.freeze_panes = "A2"
    
    excel_cols = [
        "Spesies", "Sub-folder", "Nama File", "XC ID", "Link XenoCanto",
        "Latitude", "Longitude", "Lokasi", "Negara",
        "Sampling Rate (Hz)", "Kualitas (A-E)", "Tipe Suara",
        "Tanggal Rekaman", "Rekorder", "Lisensi"
    ]
    excel_widths = [28, 12, 52, 12, 38, 12, 12, 35, 14, 18, 14, 18, 16, 25, 45]
    
    thin = Side(style="thin", color="CCCCCC")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    
    def style_header(cell, color="1F4E79"):
        cell.font = Font(bold=True, color="FFFFFF", size=11)
        cell.fill = PatternFill("solid", fgColor=color)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = border

    def style_cell(cell, even=True):
        cell.fill = PatternFill("solid", fgColor="F2F2F2" if even else "FFFFFF")
        cell.alignment = Alignment(vertical="center")
        cell.border = border

    for ci, (col, w) in enumerate(zip(excel_cols, excel_widths), 1):
        c = ws_all.cell(row=1, column=ci, value=col)
        style_header(c, "1F4E79")
        ws_all.column_dimensions[get_column_letter(ci)].width = w

    for ri, r in enumerate(records, 2):
        even = (ri % 2 == 0)
        row_vals = [
            r["species_key"], r["subfolder"], r["filename"], f"XC{r['id']}",
            r["url_page"], r["latitude"], r["longitude"], r["locality"],
            r["country"], r["sampling_rate_hz"], r["quality"], r["type"],
            r["date"], r["recordist"], r["license"]
        ]
        for ci, val in enumerate(row_vals, 1):
            c = ws_all.cell(row=ri, column=ci, value=val)
            style_cell(c, even)
            if ci == 5:
                c.hyperlink = val
                c.font = Font(color="0563C1", underline="single")

    # Sheet per spesies
    HEADER_COLORS = [
        "1F4E79","2E75B6","1C6B2B","375623","833C0B",
        "7B3F00","4A235A","154360","0E4D2E","5D2E0C",
        "1B2631","4A4A00","4A0000","00394A"
    ]
    for si, skey in enumerate(unique_species):
        s_recs = [r for r in records if r["species_key"] == skey]
        sheet_name = skey.replace("_", " ")[:31]
        ws = wb.create_sheet(title=sheet_name)
        ws.freeze_panes = "A2"
        hc = HEADER_COLORS[si % len(HEADER_COLORS)]
        
        for ci, (col, w) in enumerate(zip(excel_cols, excel_widths), 1):
            c = ws.cell(row=1, column=ci, value=col)
            style_header(c, hc)
            ws.column_dimensions[get_column_letter(ci)].width = w
            
        for ri, r in enumerate(s_recs, 2):
            even = (ri % 2 == 0)
            row_vals = [
                r["species_key"], r["subfolder"], r["filename"], f"XC{r['id']}",
                r["url_page"], r["latitude"], r["longitude"], r["locality"],
                r["country"], r["sampling_rate_hz"], r["quality"], r["type"],
                r["date"], r["recordist"], r["license"]
            ]
            for ci, val in enumerate(row_vals, 1):
                c = ws.cell(row=ri, column=ci, value=val)
                style_cell(c, even)
                if ci == 5:
                    c.hyperlink = val
                    c.font = Font(color="0563C1", underline="single")

    # Sheet Ringkasan
    ws_sum = wb.create_sheet(title="RINGKASAN", index=1)
    ws_sum.freeze_panes = "A2"
    sum_headers = ["No", "Spesies", "Jumlah Rekaman", "Sub-folder (Kualitas)", "Sampling Rate Unik (Hz)"]
    sum_widths = [5, 32, 16, 25, 30]
    for ci, (col, w) in enumerate(zip(sum_headers, sum_widths), 1):
        c = ws_sum.cell(row=1, column=ci, value=col)
        style_header(c, "1F4E79")
        ws_sum.column_dimensions[get_column_letter(ci)].width = w

    for si, skey in enumerate(unique_species, 1):
        s_recs = [r for r in records if r["species_key"] == skey]
        subfolders = sorted(set(r["subfolder"] for r in s_recs))
        srates = sorted(set(str(r["sampling_rate_hz"]) for r in s_recs))
        even = (si % 2 == 0)
        row_vals = [
            si, skey.replace("_", " "), len(s_recs),
            ", ".join(subfolders), ", ".join(srates)
        ]
        for ci, val in enumerate(row_vals, 1):
            c = ws_sum.cell(row=si+1, column=ci, value=val)
            style_cell(c, even)

    wb.save(EXCEL_PATH)
    print(f"Updated {EXCEL_PATH}")

if __name__ == "__main__":
    main()
