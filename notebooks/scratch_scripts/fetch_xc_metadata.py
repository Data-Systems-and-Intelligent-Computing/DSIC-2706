"""
Script: fetch_xc_metadata_v3.py
Tujuan: Ambil metadata (koordinat & Hz) dari Xeno-Canto API v3
        berdasarkan file .mp3 di dataset burung.
API Key: 95dc5b3f6834b56e17da4cf68cc890cb470d1284
CATATAN: Script ini HANYA membaca nama file, tidak mengubah data apapun.
"""

import os
import re
import time
import requests
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT_DIR    = r"D:\FILE AND TASK\TA\data\xeno_canto"
OUTPUT_FILE = r"D:\FILE AND TASK\TA\data\xeno_canto\Metadata_XenoCanto.xlsx"
API_KEY     = "95dc5b3f6834b56e17da4cf68cc890cb470d1284"

SPECIES_LIST = [
    "Apalharpactes mackloti",
    "Batrachostomus_poliolophus",
    "Caprimulgus_pulchellus",
    "Carpococcyx_viridis",
    "Erythropitta_venusta",
    "Gypsophila_rufipectus",
    "Hydrornis_schneideri",
    "Ixos_sumatranus",
    "Lophura_inornata",
    "Myophonus_melanurus",
    "Napothera_albostriata",
    "Niltava sumatrana",
    "Pellorneum_buettikoferi",
    "Picus_dedemi",
    "Polyplectron_chalcurum",
]

HEADERS_HTTP = {
    "X-API-Key"  : API_KEY,
    "User-Agent" : "BirdSoundResearch/1.0",
    "Accept"     : "application/json",
}

def log(msg):
    print(msg, flush=True)

def extract_xc_id(filename):
    match = re.match(r'XC(\d+)', filename, re.IGNORECASE)
    return match.group(1) if match else None

def get_xc_metadata_v3(xc_id, retries=3):
    """
    Xeno-Canto API v3 - coba beberapa endpoint yang umum.
    """
    # Endpoint 1: search by recording ID
    urls_to_try = [
        f"https://xeno-canto.org/api/3/recordings?query=nr:{xc_id}&key={API_KEY}",
        f"https://xeno-canto.org/api/3/recordings/{xc_id}?key={API_KEY}",
        f"https://xeno-canto.org/api/3/recordings?query=id:{xc_id}&key={API_KEY}",
    ]

    for attempt in range(retries):
        for url in urls_to_try:
            try:
                resp = requests.get(url, headers=HEADERS_HTTP, timeout=15)
                if resp.status_code == 200:
                    data = resp.json()
                    # Format list recordings
                    recs = data.get("recordings", [])
                    if not recs and "id" in data:
                        # Format single recording
                        recs = [data]
                    if recs:
                        r = recs[0]
                        return {
                            "lat"      : r.get("lat", ""),
                            "lng"      : r.get("lng", ""),
                            "lokasi"   : r.get("loc", ""),
                            "negara"   : r.get("cnt", ""),
                            "hz_low"   : r.get("hz-low", ""),
                            "hz_high"  : r.get("hz-high", ""),
                            "kualitas" : r.get("q", ""),
                            "tipe"     : r.get("type", ""),
                            "tanggal"  : r.get("date", ""),
                            "rekorder" : r.get("rec", ""),
                            "url_ok"   : url,
                        }
                elif resp.status_code == 401:
                    log(f"  [AUTH ERROR] API Key ditolak untuk XC{xc_id}")
                    log(f"  Response: {resp.text[:200]}")
                    return None
                elif resp.status_code == 404:
                    continue  # coba url berikutnya
                else:
                    log(f"  [HTTP {resp.status_code}] XC{xc_id}: {resp.text[:100]}")
            except Exception as e:
                log(f"  [Percobaan {attempt+1}] Error XC{xc_id}: {e}")
                time.sleep(1)

        if attempt < retries - 1:
            time.sleep(2)

    return None

# ============================================================
log("=" * 60)
log("  Xeno-Canto Metadata Fetcher (API v3)")
log("=" * 60)

# Test koneksi API dulu dengan 1 rekaman
log("\n[TEST] Mencoba koneksi API v3...")
test_urls = [
    f"https://xeno-canto.org/api/3/recordings?query=nr:409514&key={API_KEY}",
    f"https://xeno-canto.org/api/3/recordings?query=nr:39384&key={API_KEY}",
]
api_working = False
working_format = None

for test_url in test_urls:
    try:
        tr = requests.get(test_url, headers=HEADERS_HTTP, timeout=15)
        log(f"  URL: {test_url[:80]}")
        log(f"  Status: {tr.status_code}")
        log(f"  Response preview: {tr.text[:300]}")
        if tr.status_code == 200:
            api_working = True
            working_format = "query_nr"
            break
    except Exception as e:
        log(f"  Error: {e}")
log("")

# ============================================================
all_rows = []
species_files = {}

for species_folder in SPECIES_LIST:
    species_path = os.path.join(ROOT_DIR, species_folder)
    if not os.path.isdir(species_path):
        log(f"[SKIP] Folder tidak ditemukan: {species_folder}")
        continue

    log(f"\n{'-'*55}")
    log(f"[SPESIES] {species_folder}")
    rows_for_species = []

    for subfolder in sorted(os.listdir(species_path)):
        sub_path = os.path.join(species_path, subfolder)
        if not os.path.isdir(sub_path):
            continue

        for fname in sorted(os.listdir(sub_path)):
            if not fname.lower().endswith(".mp3"):
                continue

            xc_id = extract_xc_id(fname)
            if not xc_id:
                log(f"  [WARN] Tidak bisa ekstrak XC ID dari: {fname}")
                continue

            short_name = fname[:50] + "..." if len(fname) > 50 else fname
            log(f"  [{subfolder}] XC{xc_id} -> {short_name}")
            meta = get_xc_metadata_v3(xc_id)

            row = {
                "Spesies"         : species_folder,
                "Sub-folder"      : subfolder,
                "Nama File"       : fname,
                "XC ID"           : f"XC{xc_id}",
                "Link XenoCanto"  : f"https://xeno-canto.org/{xc_id}",
                "Latitude"        : meta["lat"]      if meta else "GAGAL",
                "Longitude"       : meta["lng"]      if meta else "GAGAL",
                "Lokasi"          : meta["lokasi"]   if meta else "GAGAL",
                "Negara"          : meta["negara"]   if meta else "GAGAL",
                "Hz Low"          : meta["hz_low"]   if meta else "GAGAL",
                "Hz High"         : meta["hz_high"]  if meta else "GAGAL",
                "Kualitas (A-E)"  : meta["kualitas"] if meta else "GAGAL",
                "Tipe Suara"      : meta["tipe"]     if meta else "GAGAL",
                "Tanggal Rekaman" : meta["tanggal"]  if meta else "GAGAL",
                "Rekorder"        : meta["rekorder"] if meta else "GAGAL",
            }
            rows_for_species.append(row)
            all_rows.append(row)
            time.sleep(0.5)

    species_files[species_folder] = rows_for_species
    log(f"  => {len(rows_for_species)} rekaman diproses")

# ============================================================
log(f"\n{'='*60}")
log("  Membuat file Excel...")

wb = openpyxl.Workbook()

HEADER_COLORS = [
    "1F4E79", "2E75B6", "1C6B2B", "375623", "833C0B",
    "7B3F00", "4A235A", "154360", "0E4D2E", "5D2E0C",
    "1B2631", "4A4A00", "4A0000", "00394A", "2D0B4A",
]

COLUMNS = [
    "Spesies", "Sub-folder", "Nama File", "XC ID", "Link XenoCanto",
    "Latitude", "Longitude", "Lokasi", "Negara",
    "Hz Low", "Hz High", "Kualitas (A-E)", "Tipe Suara",
    "Tanggal Rekaman", "Rekorder",
]
COL_WIDTHS = [28, 12, 52, 12, 38, 12, 12, 35, 14, 10, 10, 14, 18, 16, 25]

thin   = Side(style="thin", color="CCCCCC")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

def style_header(cell, hex_color):
    cell.font      = Font(bold=True, color="FFFFFF", size=11)
    cell.fill      = PatternFill("solid", fgColor=hex_color)
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border    = border

def style_cell(cell, row_even=True):
    bg = "F2F2F2" if row_even else "FFFFFF"
    cell.fill      = PatternFill("solid", fgColor=bg)
    cell.alignment = Alignment(vertical="center", wrap_text=True)
    cell.border    = border

# -- Sheet SEMUA DATA
ws_all = wb.active
ws_all.title = "SEMUA DATA"
ws_all.freeze_panes = "A2"
ws_all.row_dimensions[1].height = 30

for ci, (col, width) in enumerate(zip(COLUMNS, COL_WIDTHS), 1):
    cell = ws_all.cell(row=1, column=ci, value=col)
    style_header(cell, "1F4E79")
    ws_all.column_dimensions[get_column_letter(ci)].width = width

for ri, row in enumerate(all_rows, 2):
    even = (ri % 2 == 0)
    for ci, col in enumerate(COLUMNS, 1):
        val = row.get(col, "")
        c   = ws_all.cell(row=ri, column=ci, value=val)
        style_cell(c, even)
        if col == "Link XenoCanto" and isinstance(val, str) and val.startswith("http"):
            c.hyperlink = val
            c.font = Font(color="0563C1", underline="single")

# -- Sheet per Spesies
for si, (species, rows) in enumerate(species_files.items()):
    sheet_name = species.replace("_", " ")[:31]
    ws         = wb.create_sheet(title=sheet_name)
    ws.freeze_panes = "A2"
    ws.row_dimensions[1].height = 30
    hex_color  = HEADER_COLORS[si % len(HEADER_COLORS)]

    for ci, (col, width) in enumerate(zip(COLUMNS, COL_WIDTHS), 1):
        cell = ws.cell(row=1, column=ci, value=col)
        style_header(cell, hex_color)
        ws.column_dimensions[get_column_letter(ci)].width = width

    if not rows:
        ws.cell(row=2, column=1, value="Tidak ada data ditemukan")
        continue

    for ri, row in enumerate(rows, 2):
        even = (ri % 2 == 0)
        for ci, col in enumerate(COLUMNS, 1):
            val = row.get(col, "")
            c   = ws.cell(row=ri, column=ci, value=val)
            style_cell(c, even)
            if col == "Link XenoCanto" and isinstance(val, str) and val.startswith("http"):
                c.hyperlink = val
                c.font = Font(color="0563C1", underline="single")

    log(f"  Sheet '{sheet_name}' => {len(rows)} rekaman")

# -- Sheet RINGKASAN
ws_sum = wb.create_sheet(title="RINGKASAN", index=1)
ws_sum.freeze_panes = "A2"

sum_headers = ["No", "Spesies", "Jumlah Rekaman", "Sub-folder", "Negara (unik)"]
sum_widths  = [5, 32, 16, 22, 30]

for ci, (col, width) in enumerate(zip(sum_headers, sum_widths), 1):
    c = ws_sum.cell(row=1, column=ci, value=col)
    style_header(c, "1F4E79")
    ws_sum.column_dimensions[get_column_letter(ci)].width = width
ws_sum.row_dimensions[1].height = 25

for si, (species, rows) in enumerate(species_files.items(), 1):
    subfolders = sorted(set(r["Sub-folder"] for r in rows))
    countries  = sorted(set(r["Negara"]     for r in rows
                            if r["Negara"] not in ("", "GAGAL")))
    even = (si % 2 == 0)
    for ci, val in enumerate([
        si,
        species.replace("_", " "),
        len(rows),
        ", ".join(subfolders),
        ", ".join(countries) if countries else "-",
    ], 1):
        c = ws_sum.cell(row=si + 1, column=ci, value=val)
        style_cell(c, even)

wb.save(OUTPUT_FILE)

log(f"\n{'='*60}")
log(f"  File Excel berhasil disimpan:")
log(f"     {OUTPUT_FILE}")
log(f"  Total rekaman: {len(all_rows)}")
gagal = sum(1 for r in all_rows if r["Latitude"] == "GAGAL")
log(f"  Berhasil: {len(all_rows) - gagal} | Gagal: {gagal}")
log("=" * 60)
