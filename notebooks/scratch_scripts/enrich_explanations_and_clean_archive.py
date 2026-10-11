from pathlib import Path

# --- 1. CATATAN_PROGRES_BIMBINGAN.md ---
c_path = Path("D:/FILE AND TASK/TA/Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md")
content = c_path.read_text(encoding="utf-8")

# Replace manifest bullet points with crisp dense explanations
old_manifest_block = """* **Tautan Manifes:**
  * Manifes Partisi Resmi: [`data/manifests/dataset_split.csv`](../data/manifests/dataset_split.csv)
  * Spesies Target Terpilih (20 Taksa): [`data/manifests/species_freeze.csv`](../data/manifests/species_freeze.csv)
  * Spesies Non-Target Tereksklusi (186 Taksa): [`data/manifests/species_excluded.csv`](../data/manifests/species_excluded.csv)
  * Inventaris Mesin Dataset: [`data/manifests/birdclef_inventory.json`](../data/manifests/birdclef_inventory.json)
  * Metadata Komprehensif Excel (22 Sheet): [`data/manifests/Metadata_BirdCLEF.xlsx`](../data/manifests/Metadata_BirdCLEF.xlsx)"""

new_manifest_block = """* **Tautan & Penjelasan Berkas Manifes Data:**
  * **Manifes Partisi Resmi ([`data/manifests/dataset_split.csv`](../data/manifests/dataset_split.csv)):** Manifes kanonikal seluruh 4.351 berkas audio yang membagi data ke peran Galeri (3.653 klip), Kueri Bersih (200 klip), dan Kalibrasi (498 klip) dengan pemisahan perekam mutlak (*Strict Global Recordist-Disjoint*, 0 kebocoran ID/author/path).
  * **Spesies Target Terpilih / 20 Taksa ([`data/manifests/species_freeze.csv`](../data/manifests/species_freeze.csv)):** Daftar 20 spesies burung Neotropis terpilih dari pool 156 kandidat §11.3 berdasarkan peringkat diversitas perekam tertinggi ($n_{\\text{author}} \\ge 105$) guna menjamin independensi data kueri vs galeri.
  * **Spesies Non-Target Tereksklusi / 186 Taksa ([`data/manifests/species_excluded.csv`](../data/manifests/species_excluded.csv)):** Transparansi eliminasi 186 taksa non-target (136 spesies tersisih murni akibat kuota batas 20 spesies, dan 50 spesies tidak memenuhi ambang kualitas/volume §11.3).
  * **Inventaris Mesin Dataset ([`data/manifests/birdclef_inventory.json`](../data/manifests/birdclef_inventory.json)):** Berkas JSON hasil ekstraksi terotomatisasi dari skrip inventarisasi langsung terhadap berkas audio guna menjamin seluruh angka statistik korpus valid tanpa ada yang diketik tangan.
  * **Metadata Komprehensif Excel / 22 Sheet ([`data/manifests/Metadata_BirdCLEF.xlsx`](../data/manifests/Metadata_BirdCLEF.xlsx)):** Buku kerja metadata 22 lembar kerja yang memetakan profil taksonomi, sebaran koordinat geospasial, durasi audio, dan statistik perekam untuk setiap spesies target."""

assert old_manifest_block in content, "old_manifest_block not found"
content = content.replace(old_manifest_block, new_manifest_block)

# Replace results bullet points with crisp dense explanations
old_results_block = """* **Tautan Berkas Hasil E1 (Rezim Aktif Tunggal):**
  * Tabel Metrik Ringkasan Kanonik: [`results/processed/clean_retrieval_table.csv`](../results/processed/clean_retrieval_table.csv)
  * Tabel Rincian Per Kueri (800 Baris Lengkap Kolom `author`): [`results/processed/per_query_clean_retrieval.csv`](../results/processed/per_query_clean_retrieval.csv)
  * Catatan Eksekusi Mesin (S-01): [`results/processed/execution_note_E1.json`](../results/processed/execution_note_E1.json)
  * Gambar Visualisasi Benchmark: [`results/figures/clean_retrieval_benchmark.png`](../results/figures/clean_retrieval_benchmark.png)
  * Peta Persebaran Geospasial: [`results/figures/birdclef_geospatial_distribution_map.png`](../results/figures/birdclef_geospatial_distribution_map.png)
  * Notebook E0 Sanity Check: [`notebooks/E0_Pipeline_Sanity_Check.ipynb`](../notebooks/E0_Pipeline_Sanity_Check.ipynb)
  * Notebook E1 Clean Retrieval: [`notebooks/E1_Clean_Retrieval.ipynb`](../notebooks/E1_Clean_Retrieval.ipynb)"""

new_results_block = """* **Tautan & Penjelasan Berkas Hasil E1 (Rezim Aktif Tunggal):**
  * **Tabel Metrik Ringkasan Kanonik ([`results/processed/clean_retrieval_table.csv`](../results/processed/clean_retrieval_table.csv)):** Berkas tabel resmi luaran E1 yang memuat metrik agregat makro (Top-1 Accuracy, mAP@10, MRR, Recall@10, Precision@10) lintas 4 representasi audio ($R_0, R_1, R_2, R_3$).
  * **Tabel Rincian Per Kueri ([`results/processed/per_query_clean_retrieval.csv`](../results/processed/per_query_clean_retrieval.csv)):** Log granular 800 baris evaluasi kueri yang mencatat ID kueri, spesies target, author perekam, kecocokan Top-1, skor kemiripan maksimum, dan metrik ranking per kueri sesuai standar audit H5.2.
  * **Catatan Eksekusi Mesin ([`results/processed/execution_note_E1.json`](../results/processed/execution_note_E1.json)):** Rekam jejak audit sistem otomatis yang mencatat stempel waktu eksekusi, versi pustaka, SHA commit git, dan parameter hardware.
  * **Gambar Visualisasi Benchmark ([`results/figures/clean_retrieval_benchmark.png`](../results/figures/clean_retrieval_benchmark.png)):** Grafik visual resolusi tinggi (300 DPI) yang membandingkan performa Top-1, mAP@10, dan MRR keempat representasi audio pada kondisi bersih.
  * **Peta Persebaran Geospasial ([`results/figures/birdclef_geospatial_distribution_map.png`](../results/figures/birdclef_geospatial_distribution_map.png)):** Peta sebaran spasial koordinat lintang/bujur perekaman audio 20 spesies burung target di wilayah Neotropis / Pantanal.
  * **Notebook E0 Pipeline Sanity Check ([`notebooks/E0_Pipeline_Sanity_Check.ipynb`](../notebooks/E0_Pipeline_Sanity_Check.ipynb)):** Notebook verifikasi gerbang anti-kebocoran data dan smoke test fitur sebelum benchmark penuh.
  * **Notebook E1 Clean Retrieval ([`notebooks/E1_Clean_Retrieval.ipynb`](../notebooks/E1_Clean_Retrieval.ipynb)):** Notebook utama inferensi embedding dan tolok ukur perolehan kemiripan bersih."""

assert old_results_block in content, "old_results_block not found"
content = content.replace(old_results_block, new_results_block)

# Now replace the entire legacy archive section from line 99 to line 218 with clean active proof runs
legacy_start = "## ARSIP: HASIL EKSEKUSI GATE 1 LAMA (14 SPESIES SUMATERA — 11 SEPTEMBER 2026)"
legacy_end = "## 📅 RENCANA TAHAP BERIKUTNYA PASCA-BIMBINGAN:"

assert legacy_start in content, "legacy_start not found"
assert legacy_end in content, "legacy_end not found"

idx_start = content.index(legacy_start)
idx_end = content.index(legacy_end)

new_middle_section = """## BUKTI HASIL EKSEKUSI SUITE PENGUJIAN SAINTIFIK & INTEGRITAS

Berikut adalah bukti rekaman eksekusi terkini dari lingkungan aktif yang memvalidasi seluruh pipeline Gate 1-R:

### Bukti Run 1: Verifikasi Dimensi Vektor Model Asli ([`src/embeddings.py`](../src/embeddings.py))
Perintah yang dijalankan: `python src/embeddings.py`
```text
============================================================
[*] Menguji AudioRepresentationExtractor R0, R1, R2, R3...
============================================================
[PASS] R0 -> Dimensi Vektor: (40,)   | L2-Norm: 1.0000  (MFCC Baseline)
[PASS] R1 -> Dimensi Vektor: (2048,) | L2-Norm: 1.0000  (PANNs CNN14 AudioSet PyTorch)
[PASS] R2 -> Dimensi Vektor: (1024,) | L2-Norm: 1.0000  (BirdNET V2.4 Backbone ONNX)
[PASS] R3 -> Dimensi Vektor: (40,)   | L2-Norm: 1.0000  (Random Negative Control)
============================================================
```

### Bukti Run 2: Suite Pengujian Integritas Saintifik Penuh ([`run_tests.py`](../run_tests.py))
Perintah yang dijalankan: `python run_tests.py`
```text
================================================================================
[*] MENJALANKAN SUITE PENGUJIAN SAINTIFIK DSIC27-06
================================================================================
  [PASS] Zero Recording ID Overlap
  [PASS] Zero File Path Overlap
  [PASS] Strict Global Recordist-Disjoint (Zero Recordist Overlap)
  [PASS] SNR Controlled Mixing Accuracy
  [PASS] Cosine Similarity Mathematical Bounds
  [PASS] Retrieval Ranking & Metric Logic
  [PASS] Open-Set Threshold Freeze Validation
  [PASS] Manifest SHA-256 Integrity Verification (M-06)
Checkpoint path: D:\\FILE AND TASK\\TA\\checkpoints\\Cnn14_mAP=0.431.pth
GPU number: 1
  [PASS] Model Embedding Dimension Compliance (C-01)
================================================================================
[+] HASIL: 9/9 Pengujian Lolos (100.0%)
================================================================================
```

### Bukti Run 3: Sinkronisasi Dinamis Checksum SHA-256 Manifes ([`scripts/update_manifest_hashes.py`](../scripts/update_manifest_hashes.py))
Perintah yang dijalankan: `python scripts/update_manifest_hashes.py`
```text
======================================================================
=== PENGHITUNGAN ULANG SHA-256 MANIFES INTEGRITAS (M-06) ===
======================================================================
[+] dataset_split.csv              : 4fb0681aab39415384cf85c2f43b3b83f932ed08a97364d19c50e39fd9b27d3e
[+] species_freeze.csv             : 2267c13535546b02a090ad67ca4eecdf443dc11e348f44b3a3d7fea51bc71f6a
[+] species_excluded.csv           : 36046986f5b16b718c778b3115e773abf949fa5861c7f6ccd9b6765a09289ec7
[+] itera_noise_manifest.csv       : 6f2eea8985be845260836653400d8ccef675c19cf5c628ce98d89fc5fe0de3c7
======================================================================
[SUKSES] Hash integritas berhasil diperbarui di: artifacts/reproducibility/manifest_sha256.txt
======================================================================
```

---

## 📓 BUKTI JUPYTER NOTEBOOK RESMI (GATE 1-R BIRDCLEF+ 2026)

Seluruh alur kerja aktif Gate 1-R dieksekusi secara transparan pada 4 notebook resmi berikut di folder `notebooks/`:
1. **EDA & Eksplorasi Spasial ([`notebooks/EDA_Tugas_Akhir.ipynb`](../notebooks/EDA_Tugas_Akhir.ipynb)):** Pemetaan geospasial sebaran koordinat 20 spesies burung Neotropis di kawasan Pantanal, verifikasi kriteria inklusi §11.3, dan inspeksi integritas format berkas audio fisik.
2. **Verifikasi Prapemrosesan ([`notebooks/Preprocessing Verification.ipynb`](../notebooks/Preprocessing%20Verification.ipynb)):** Standardisasi sinyal audio ke sampling rate 32 kHz, pemotongan segmen 5,0 detik berbasis jendela energi tertinggi, dan verifikasi normalisasi RMS energi ke nilai konstan 0.05.
3. **E0 Pipeline Sanity Check ([`notebooks/E0_Pipeline_Sanity_Check.ipynb`](../notebooks/E0_Pipeline_Sanity_Check.ipynb)):** Gerbang asersi anti-kebocoran data (*zero overlap* ID/author/path pada 4.351 klip) dan pembuktian hipotesis kontrol negatif H5 ($R_2 > R_1 > R_0 \\gg R_3$).
4. **E1 Clean Retrieval Benchmark ([`notebooks/E1_Clean_Retrieval.ipynb`](../notebooks/E1_Clean_Retrieval.ipynb)):** Ekstraksi representasi audio beku lengkap dan perhitungan tolok ukur perolehan kemiripan (*similarity retrieval*) pada 200 kueri bersih terhadap 3.653 rekaman galeri.

---

"""

content = content[:idx_start] + new_middle_section + content[idx_end:]
c_path.write_text(content, encoding="utf-8")
print("[+] CATATAN_PROGRES_BIMBINGAN.md successfully cleaned of legacy archive and enriched with dense explanations!")

# --- 2. README.md cleanup ---
r_path = Path("D:/FILE AND TASK/TA/README.md")
r_content = r_path.read_text(encoding="utf-8")

old_r_arch = "- **Koleksi Awal Xeno-Canto (14 Spesies)**: Korpus awal kurasi manual Xeno-Canto Sumatera telah diarsipkan secara aman di `results/archive/2026-09-07_xenocanto16spesies/` sebagai rekam jejak audit.\n\n"
if old_r_arch in r_content:
    r_content = r_content.replace(old_r_arch, "")
    r_path.write_text(r_content, encoding="utf-8")
    print("[+] Cleaned legacy archive note from README.md")

# --- 3. minggu-1/README.md cleanup ---
m_path = Path("D:/FILE AND TASK/TA/Rencana-eksperimen-bimbingan/minggu-1/README.md")
m_content = m_path.read_text(encoding="utf-8")

old_m_arch = "\n*Catatan Pengarsipan:* Seluruh berkas notebook dan tabel eksperimen 14 spesies Sumatra lama telah diarsipkan secara aman di `results/archive/2026-09-07_xenocanto16spesies/`."
if old_m_arch in m_content:
    m_content = m_content.replace(old_m_arch, "")
    m_path.write_text(m_content, encoding="utf-8")
    print("[+] Cleaned legacy archive note from minggu-1/README.md")
