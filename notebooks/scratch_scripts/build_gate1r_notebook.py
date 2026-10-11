import json
from pathlib import Path

nb_path = Path(r"D:\FILE AND TASK\TA\notebooks\Gate1R_BirdCLEF_E1_Pipeline.ipynb")

cells = []

def add_md(content):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in content.strip().split("\n")]
    })

def add_code(content):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in content.strip().split("\n")]
    })

# Title
add_md("""# GATE 1-R: Pipeline Sanity Check, Geospatial Map, & E1 Clean Retrieval (BirdCLEF+ 2026)
**Topik Penelitian:** DSIC27-06 — Mencari Audio yang Mirip Ketika Datanya Terbatas  
**Dataset:** BirdCLEF+ 2026 (20 Spesies Target Burung Neotropis Pantanal)  
**Tujuan Notebook:**
1. Verifikasi Pembekuan 20 Spesies Burung Target (Aturan H2 Audit).
2. Pembuatan Figure Peta Sebaran Geografis Rekaman (MAP Geospatial).
3. Pembagian Split *Strict Author-Disjoint* dan Uji Gerbang Bebas Kebocoran (*Zero Leakage Assertion*).
4. Smoke Test Ekstraksi Representasi ($R_0, R_1, R_2, R_3$).
5. Eksekusi Benchmark E1 *Clean Retrieval* (Cosine Similarity, mAP@10, MRR, Recall@10, Precision@10).""")

# Cell 1: Setup
add_code("""# Cell 1: Inisialisasi Environment dan Pustaka
import os
import sys
import json
import urllib.request
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
from sklearn.metrics.pairwise import cosine_similarity

# Tentukan Root Path Repositori
NOTEBOOK_DIR = Path(os.getcwd())
REPO_ROOT = NOTEBOOK_DIR.parent if NOTEBOOK_DIR.name == 'notebooks' else NOTEBOOK_DIR
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.preprocess import preprocess_audio, TARGET_SR
from src.embeddings import AudioRepresentationExtractor

# Direktori Data & Output
DATA_DIR = REPO_ROOT / "data" / "BirdClef"
MANIFEST_DIR = REPO_ROOT / "data" / "manifests"
RESULTS_PROC_DIR = REPO_ROOT / "results" / "processed"
RESULTS_FIG_DIR = REPO_ROOT / "results" / "figures"
PAPER_FIG_DIR = REPO_ROOT / "paper" / "figures"

for d in [MANIFEST_DIR, RESULTS_PROC_DIR, RESULTS_FIG_DIR, PAPER_FIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)

print(f"[+] Environment siap! Root Repositori: {REPO_ROOT}")""")

# Section 1
add_md("""---
## Bagian 1: Verifikasi 20 Spesies Target BirdCLEF+ 2026 (Aturan Audit H2)
Memastikan berkas `species_freeze.csv` telah memuat 20 taksa burung target terpilih dengan diversitas author tinggi.""")

add_code("""# Cell 2: Memuat Spesies Target Terbekukan
FREEZE_CSV = MANIFEST_DIR / "species_freeze.csv"
if not FREEZE_CSV.exists():
    raise FileNotFoundError("Berkas species_freeze.csv belum ada. Pastikan skrip select_birdclef_species.py telah dijalankan.")

df_freeze = pd.read_csv(FREEZE_CSV)
print(f"[+] Berhasil memuat {len(df_freeze)} spesies target:")
display(df_freeze[["species_key", "scientific_name", "common_name", "n_klip", "n_author", "rating_median"]])""")

# Section 2
add_md("""---
## Bagian 2: Pembuatan Figure Peta Sebaran Geografis (MAP)
Memetakan sebaran koordinat latitude dan longitude dari rekaman fokal 20 spesies target di benua Amerika Selatan, serta menyoroti area penempatan sensor *soundscape* di Pantanal, Brasil.""")

add_code("""# Cell 3: Visualisasi Peta Spasial Geografis (2-Panel Publication Figure)
TRAIN_CSV = DATA_DIR / "train.csv"
GEOJSON_FILE = MANIFEST_DIR / "south_america.geojson"

df_train = pd.read_csv(TRAIN_CSV)
target_keys = set(df_freeze["species_key"])
df_target = df_train[df_train["primary_label"].isin(target_keys)].dropna(subset=["latitude", "longitude"]).copy()

# Unduh / Muat GeoJSON Poligon Batas Negara Amerika Selatan
if not GEOJSON_FILE.exists():
    print("[*] Mengunduh GeoJSON batas negara Amerika Selatan...")
    url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        world_geo = json.loads(resp.read().decode())
    sa_names = {"Brazil", "Argentina", "Bolivia", "Colombia", "Peru", "Venezuela", "Chile", "Paraguay", "Ecuador", "Guyana", "Uruguay", "Suriname", "French Guiana"}
    sa_features = [f for f in world_geo["features"] if f["properties"]["name"] in sa_names]
    geo_data = {"type": "FeatureCollection", "features": sa_features}
    with open(GEOJSON_FILE, "w", encoding="utf-8") as f:
        json.dump(geo_data, f)
else:
    with open(GEOJSON_FILE, "r", encoding="utf-8") as f:
        geo_data = json.load(f)

def draw_polygons(ax, data, facecolor="#f8f9fa", edgecolor="#adb5bd", lw=0.7):
    for feat in data["features"]:
        geom = feat["geometry"]
        coords = geom["coordinates"]
        if geom["type"] == "Polygon":
            for poly in coords:
                ax.add_patch(Polygon(poly, facecolor=facecolor, edgecolor=edgecolor, linewidth=lw, zorder=1))
        elif geom["type"] == "MultiPolygon":
            for mp in coords:
                for poly in mp:
                    ax.add_patch(Polygon(poly, facecolor=facecolor, edgecolor=edgecolor, linewidth=lw, zorder=1))

# Koordinat Bounding Box Pantanal (-21.6 s/d -16.5 Lat, -57.6 s/d -55.9 Lon)
p_lat_min, p_lat_max = -21.6, -16.5
p_lon_min, p_lon_max = -57.6, -55.9

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8.5), dpi=300)

# Panel 1: Makro (Amerika Selatan)
draw_polygons(ax1, geo_data, facecolor="#f8f9fa", edgecolor="#adb5bd", lw=0.7)
ax1.scatter(df_target["longitude"], df_target["latitude"], c="#1f77b4", alpha=0.35, s=12, edgecolors="none", zorder=2, label=f"Rekaman Fokal 20 Spesies (n={len(df_target):,})")
rect_macro = Rectangle((p_lon_min, p_lat_min), p_lon_max - p_lon_min, p_lat_max - p_lat_min, linewidth=2.0, edgecolor="#d62728", facecolor="#d62728", alpha=0.35, zorder=3, label="Wilayah Pantanal (Soundscape)")
ax1.add_patch(rect_macro)
ax1.set_xlim(-90, -32)
ax1.set_ylim(-58, 15)
ax1.set_xlabel("Longitude (deg)", fontweight="bold")
ax1.set_ylabel("Latitude (deg)", fontweight="bold")
ax1.set_title("(a) Sebaran Geografis Rekaman Fokal 20 Spesies Target", fontweight="bold")
ax1.legend(loc="lower left", framealpha=0.9, fontsize=9)
ax1.grid(True, linestyle="--", alpha=0.35)

# Panel 2: Mikro (Pantanal Focus)
draw_polygons(ax2, geo_data, facecolor="#e9ecef", edgecolor="#6c757d", lw=1.2)
df_pantanal = df_target[(df_target["longitude"] >= -65.0) & (df_target["longitude"] <= -50.0) & (df_target["latitude"] >= -25.0) & (df_target["latitude"] <= -12.0)]
ax2.scatter(df_pantanal["longitude"], df_pantanal["latitude"], c="#2ca02c", alpha=0.55, s=28, edgecolors="black", linewidth=0.3, zorder=2, label=f"Rekaman Fokal Lokal Pantanal (n={len(df_pantanal):,})")
rect_micro = Rectangle((p_lon_min, p_lat_min), p_lon_max - p_lon_min, p_lat_max - p_lat_min, linewidth=2.2, edgecolor="#d62728", facecolor="#ff7f0e", alpha=0.4, zorder=3, label="Area Penempatan Sensor BirdCLEF\\n(Lat: -21.6 s/d -16.5 | Lon: -57.6 s/d -55.9)")
ax2.add_patch(rect_micro)
ax2.set_xlim(-65, -50)
ax2.set_ylim(-25, -12)
ax2.set_xlabel("Longitude (deg)", fontweight="bold")
ax2.set_ylabel("Latitude (deg)", fontweight="bold")
ax2.set_title("(b) Detail Wilayah Penempatan Perekam Soundscape Pantanal", fontweight="bold")
ax2.legend(loc="lower right", framealpha=0.9, fontsize=9)
ax2.grid(True, linestyle="--", alpha=0.35)

plt.suptitle("Peta Sebaran Spasial Data Bioakustik BirdCLEF+ 2026\\nRekaman Fokal (Xeno-Canto) vs Penempatan Soundscape (Pantanal, Brasil)", fontsize=13, fontweight="bold", y=0.98)
plt.tight_layout()

map_out1 = RESULTS_FIG_DIR / "birdclef_geospatial_distribution_map.png"
map_out2 = PAPER_FIG_DIR / "birdclef_geospatial_distribution_map.png"
plt.savefig(map_out1, bbox_inches="tight", dpi=300)
plt.savefig(map_out2, bbox_inches="tight", dpi=300)
plt.show()
print(f"[+] Peta berhasil disimpan ke:\\n    - {map_out1}\\n    - {map_out2}")""")

# Section 3
add_md("""---
## Bagian 3: Pembagian Split Dataset *Strict Author-Disjoint* (Aturan Audit H3)
Menjamin tidak ada satupun author atau perekam yang muncul bersamaan di galeri, kueri bersih, maupun kalibrasi ($R_{gallery} \\cap R_{query} = \\emptyset$).""")

add_code("""# Cell 4: Pembuatan Split Author-Disjoint Terstratifikasi
df_clean = df_train[df_train["author"].str.strip().str.lower() != "unknown"].copy()
df_target = df_clean[df_clean["primary_label"].isin(target_keys) & (df_clean["collection"] == "XC") & (df_clean["rating"] >= 3.0)].copy()

# Alokasi author unik secara global dengan seed tetap (seed=42)
all_unique_authors = df_target["author"].unique()
np.random.seed(42)
shuffled_authors = np.random.permutation(all_unique_authors)

n_total_auth = len(shuffled_authors)
n_gal_auth = int(0.60 * n_total_auth)
n_qry_auth = int(0.25 * n_total_auth)

gal_authors = set(shuffled_authors[:n_gal_auth])
qry_authors = set(shuffled_authors[n_gal_auth:n_gal_auth + n_qry_auth])
cal_authors = set(shuffled_authors[n_gal_auth + n_qry_auth:])

split_records = []
for _, row in df_target.iterrows():
    auth = row["author"]
    if auth in gal_authors:
        role = "gallery"
    elif auth in qry_authors:
        role = "query_clean"
    elif auth in cal_authors:
        role = "calibration"
    else:
        continue
    
    split_records.append({
        "recording_id": Path(row["filename"]).stem,
        "species_key": row["primary_label"],
        "scientific_name": row["scientific_name"],
        "common_name": row["common_name"],
        "author": row["author"],
        "rating": row["rating"],
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "file_path": f"data/BirdClef/train_audio/{row['filename']}",
        "split_role": role
    })

df_split = pd.DataFrame(split_records)

# Ambil tepat 10 kueri bersih per spesies dengan rating tertinggi dari subset query_clean (Total = 200 kueri)
queries_selected = []
for sp in df_freeze["species_key"]:
    sp_qry = df_split[(df_split["species_key"] == sp) & (df_split["split_role"] == "query_clean")]
    sp_qry_top = sp_qry.sort_values(by="rating", ascending=False).head(10)
    queries_selected.append(sp_qry_top)

df_clean_queries = pd.concat(queries_selected).reset_index(drop=True)
df_gallery = df_split[df_split["split_role"] == "gallery"].reset_index(drop=True)
df_calibration = df_split[df_split["split_role"] == "calibration"].reset_index(drop=True)

df_final_split = pd.concat([df_gallery, df_clean_queries, df_calibration]).reset_index(drop=True)

SPLIT_CSV = MANIFEST_DIR / "dataset_split.csv"
df_final_split.to_csv(SPLIT_CSV, index=False)
print(f"[+] Dataset Split berhasil disimpan di: {SPLIT_CSV}")
print(df_final_split["split_role"].value_counts())""")

# Section 4: Assertion
add_md("""---
## Bagian 4: Uji Gerbang Anti-Kebocoran Mutlak (*Assertion Test*)
Pemeriksaan ini melempar `AssertionError` jika ada irisan author, recording ID, atau file path.""")

add_code("""# Cell 5: Uji Kebocoran Author, Recording ID, dan File Path
d_test = pd.read_csv(SPLIT_CSV)

gal_auth = set(d_test[d_test.split_role == "gallery"]["author"])
qry_auth = set(d_test[d_test.split_role == "query_clean"]["author"])
cal_auth = set(d_test[d_test.split_role == "calibration"]["author"])

# 1. Author Disjoint Assertion
assert not (gal_auth & qry_auth), f"[FATAL] Kebocoran Author gallery vs query: {gal_auth & qry_auth}"
assert not (gal_auth & cal_auth), f"[FATAL] Kebocoran Author gallery vs calibration: {gal_auth & cal_auth}"
assert not (qry_auth & cal_auth), f"[FATAL] Kebocoran Author query vs calibration: {qry_auth & cal_auth}"

# 2. Recording ID Disjoint Assertion
gal_id = set(d_test[d_test.split_role == "gallery"]["recording_id"])
qry_id = set(d_test[d_test.split_role == "query_clean"]["recording_id"])
cal_id = set(d_test[d_test.split_role == "calibration"]["recording_id"])
assert not (gal_id & qry_id), "[FATAL] Kebocoran Recording ID gallery vs query!"
assert not (gal_id & cal_id), "[FATAL] Kebocoran Recording ID gallery vs calibration!"

# 3. File Path Disjoint Assertion
gal_p = set(d_test[d_test.split_role == "gallery"]["file_path"])
qry_p = set(d_test[d_test.split_role == "query_clean"]["file_path"])
assert not (gal_p & qry_p), "[FATAL] Kebocoran File Path gallery vs query!"

print("[PASS] 100% LOLOS AUDIT KEBOCORAN:")
print(f"  - Author Gallery   : {len(gal_auth)} author unik")
print(f"  - Author Query     : {len(qry_auth)} author unik")
print(f"  - Author Calib     : {len(cal_auth)} author unik")
print(f"  - Overlap Author   : 0 author")
print(f"  - Overlap ID & Path: 0 rekaman")""")

# Section 5: Smoke Test
add_md("""---
## Bagian 5: Prapemrosesan Audio & Smoke Test Ekstraksi Fitur ($R_0, R_1, R_2, R_3$)
Menguji pembacaan audio OGG dan memverifikasi dimensi fitur:
- $R_0$: Handcrafted MFCC (40 dimensi)
- $R_1$: Generic Audio PANNs CNN14 (2048 dimensi)
- $R_2$: Bioacoustic BirdNET ONNX (1024 dimensi)
- $R_3$: Random Gaussian Control (40 dimensi)""")

add_code("""# Cell 6: Smoke Test Ekstraksi Fitur pada 1 Sampel Audio BirdCLEF
sample_row = df_final_split.iloc[0]
sample_audio_path = REPO_ROOT / sample_row["file_path"]

print(f"[*] Menguji sampel audio: {sample_audio_path.name}")
y_proc = preprocess_audio(str(sample_audio_path))
print(f"[+] Audio pra-pemrosesan: bentuk {y_proc.shape} | Laju sampel: {TARGET_SR} Hz | RMS: {np.sqrt(np.mean(y_proc**2)):.4f}")

for rep in ["R0", "R1", "R2", "R3"]:
    extractor = AudioRepresentationExtractor(rep)
    feat = extractor.extract(y_proc)
    print(f"[PASS] {rep} -> Dimensi Vektor: {feat.shape} | L2-Norm: {np.linalg.norm(feat):.4f}")""")

# Section 6: E1 Clean Retrieval
add_md("""---
## Bagian 6: Eksekusi Benchmark E1 Clean Retrieval
Mengekstrak embedding untuk seluruh galeri dan 200 kueri bersih, lalu menghitung Cosine Similarity untuk menghasilkan perankingan.""")

add_code("""# Cell 7: Ekstraksi Fitur Galeri & Kueri Bersih
df_gal = df_final_split[df_final_split["split_role"] == "gallery"].reset_index(drop=True)
df_qry = df_final_split[df_final_split["split_role"] == "query_clean"].reset_index(drop=True)

print(f"[*] Total Galeri: {len(df_gal)} rekaman | Total Kueri Bersih: {len(df_qry)} rekaman (10 kueri/spesies)")

# Fungsi helper prapemrosesan batch
def load_and_preprocess_list(file_paths):
    audio_signals = []
    for fp in file_paths:
        full_p = REPO_ROOT / fp
        y = preprocess_audio(str(full_p))
        audio_signals.append(y)
    return audio_signals

print("[*] Melakukan prapemrosesan audio kueri...")
qry_signals = load_and_preprocess_list(df_qry["file_path"])

print("[*] Melakukan prapemrosesan audio galeri...")
gal_signals = load_and_preprocess_list(df_gal["file_path"])
print("[+] Seluruh audio galeri dan kueri berhasil diproses!")""")

# Section 7: Retrieval Evaluation
add_md("""---
## Bagian 7: Evaluasi Metrik Retrieval ($mAP@10$, $\\text{Recall}@k$, $\\text{Precision}@k$, $\\text{MRR}$)
Menghitung matriks kemiripan kosinus untuk $R_0, R_1, R_2, R_3$ dan menyimpan tabel agregat serta tabel rinci per-kueri.""")

add_code("""# Cell 8: Menghitung Metrik Retrieval untuk R0, R1, R2, R3
representations = ["R0", "R1", "R2", "R3"]
rep_names = {
    "R0": "R0: MFCC Baseline (40-d)",
    "R1": "R1: PANNs CNN14 (2048-d)",
    "R2": "R2: BirdNET Backbone (1024-d)",
    "R3": "R3: Random Control (40-d)"
}

summary_results = []
per_query_results = []

gal_species = df_gal["species_key"].values
gal_authors = df_gal["author"].values

for rep in representations:
    print(f"[*] Mengekstrak fitur untuk representasi {rep}...")
    extractor = AudioRepresentationExtractor(rep)
    
    # Ekstraksi representasi
    gal_feats = np.array([extractor.extract(y) for y in gal_signals])
    qry_feats = np.array([extractor.extract(y) for y in qry_signals])
    
    # Matriks Kesamaan Kosinus (n_qry x n_gal)
    sim_matrix = cosine_similarity(qry_feats, gal_feats)
    
    top1_correct = 0
    aps_at_10 = []
    reciprocal_ranks = []
    recalls_at_10 = []
    precisions_at_10 = []
    
    for i, q_row in df_qry.iterrows():
        target_sp = q_row["species_key"]
        sim_scores = sim_matrix[i]
        
        # Urutkan peringkat dari skor terbesar ke terkecil
        ranked_indices = np.argsort(sim_scores)[::-1]
        ranked_sp = gal_species[ranked_indices]
        
        is_match = (ranked_sp == target_sp)
        total_relevant = np.sum(is_match)
        
        # Top-1 match
        if is_match[0]:
            top1_correct += 1
            
        # MRR (Mean Reciprocal Rank)
        first_match_idx = np.where(is_match)[0]
        rr = 1.0 / (first_match_idx[0] + 1) if len(first_match_idx) > 0 else 0.0
        reciprocal_ranks.append(rr)
        
        # Precision@10 & Recall@10
        top10_matches = is_match[:10]
        n_rel_in_10 = np.sum(top10_matches)
        prec_10 = n_rel_in_10 / 10.0
        rec_10 = n_rel_in_10 / max(1, total_relevant)
        precisions_at_10.append(prec_10)
        recalls_at_10.append(rec_10)
        
        # Average Precision @ 10 (AP@10)
        hits = 0
        prec_sum = 0.0
        for k in range(10):
            if is_match[k]:
                hits += 1
                prec_sum += hits / (k + 1)
        ap10 = prec_sum / min(10, max(1, total_relevant))
        aps_at_10.append(ap10)
        
        per_query_results.append({
            "query_id": q_row["recording_id"],
            "species_key": target_sp,
            "author": q_row["author"],
            "top1_match": ranked_sp[0],
            "max_similarity": float(sim_scores[ranked_indices[0]]),
            "total_relevant_in_gallery": int(total_relevant),
            "reciprocal_rank": float(rr),
            "P@10": float(prec_10),
            "R@10": float(rec_10),
            "AP@10": float(ap10),
            "representation": rep
        })
        
    summary_results.append({
        "representation": rep,
        "name": rep_names[rep],
        "Top1_Accuracy": (top1_correct / len(df_qry)) * 100.0,
        "mAP@10": float(np.mean(aps_at_10)),
        "MRR": float(np.mean(reciprocal_ranks)),
        "Recall@10": float(np.mean(recalls_at_10)),
        "Precision@10": float(np.mean(precisions_at_10))
    })

df_summary = pd.DataFrame(summary_results)
df_per_query = pd.DataFrame(per_query_results)

# Simpan Tabel Kanonik Sesuai Audit
df_summary.to_csv(RESULTS_PROC_DIR / "clean_retrieval_table.csv", index=False)
df_per_query.to_csv(RESULTS_PROC_DIR / "per_query_clean_retrieval.csv", index=False)

print("\n" + "="*80)
print("HASIL EVALUASI E1 CLEAN RETRIEVAL (BIRDCLEF+ 2026 - 20 SPESIES):")
print("="*80)
display(df_summary)""")

# Section 8: Visualizations
add_md("""---
## Bagian 8: Visualisasi Grafik Publikasi Benchmark E1 Clean Retrieval
Membuat grafik batang tolok ukur mAP@10, Top-1 Accuracy, dan MRR lintas representasi.""")

add_code("""# Cell 9: Visualisasi Hasil Benchmark E1
fig, axes = plt.subplots(1, 3, figsize=(16, 5), dpi=300)

metrics = [("Top1_Accuracy", "Top-1 Accuracy (%)", axes[0]), 
           ("mAP@10", "Mean Average Precision (mAP@10)", axes[1]), 
           ("MRR", "Mean Reciprocal Rank (MRR)", axes[2])]

colors = ["#7f7f7f", "#ff7f0e", "#1f77b4", "#d62728"]

for col, title, ax in metrics:
    bars = ax.bar(df_summary["representation"], df_summary[col], color=colors, edgecolor="black", alpha=0.85)
    ax.set_title(title, fontweight="bold", fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.4, axis="y")
    for bar in bars:
        height = bar.get_height()
        fmt = f"{height:.1f}%" if "%" in title else f"{height:.4f}"
        ax.annotate(fmt, xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")

plt.suptitle("Tolok Ukur E1 Clean Retrieval Lintas Representasi Audio (BirdCLEF+ 2026)", fontsize=13, fontweight="bold", y=1.02)
plt.tight_layout()

e1_fig = RESULTS_FIG_DIR / "clean_retrieval_benchmark.png"
plt.savefig(e1_fig, bbox_inches="tight", dpi=300)
plt.savefig(PAPER_FIG_DIR / "clean_retrieval_benchmark.png", bbox_inches="tight", dpi=300)
plt.show()
print(f"[+] Gambar benchmark disimpan ke: {e1_fig}")""")

nb_content = {
    "cells": cells,
    "metadata": {
        "language_info": {
            "name": "python",
            "version": "3.14.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

nb_path.write_text(json.dumps(nb_content, indent=2), encoding="utf-8")
print(f"Notebook created at: {nb_path}")
