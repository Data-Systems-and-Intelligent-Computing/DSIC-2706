# Rencana Eksperimen — Minggu 1 (GATE 1)
**Fokus:** Dataset 14 Spesies Sumatera, Manifest, Standarisasi Audio, EDA, E0 (Pipeline Sanity), dan E1 (Clean Retrieval).  
**Target Garis Waktu:** Minggu Ke-1  
**Status Eksekusi:** **Aktif & Terstruktur**

---

## 🎯 Target Rencana & Hasil Eksekusi

### 1. Pembekuan Target Burung, Manifes, & Preprocessing
* **Spesies Terpilih:** **14 spesies burung Sumatera** (total 162 file audio MP3) dengan rata-rata 11–28 rekaman per spesies.
* **Koreksi Data:** Seluruh data luar negeri (seperti Malaysia) serta folder non-Sumatera telah dihapus. Folder `Lophura_inornata/D` telah diverifikasi.
* **Parameter Preprocessing Dibekukan:**
  * Sample Rate: **32.000 Hz** (Mono)
  * Durasi Potongan Segmen: **5.0 detik**
  * Normalisasi: RMS Energy Normalization (`target_rms = 0.05`)
  * Transformasi Waktu-Frekuensi: $N_{\text{FFT}} = 1024$, $\text{hop\_length} = 512$
* **Bukti Berkas Repository:**
  * Manifes Utama: [`data/manifests/target_birds_manifest.csv`](../../data/manifests/target_birds_manifest.csv)
  * Manifes Split: [`data/manifests/dataset_split.csv`](../../data/manifests/dataset_split.csv)
  * Konfigurasi Parameter Audio: [`configs/audio.yaml`](../../configs/audio.yaml)
  * Konfigurasi Dataset: [`configs/datasets.yaml`](../../configs/datasets.yaml)

---

### 2. Implementasi Representasi Audio & Similarity Engine (E0 & E1)
* **Empat representasi audio:**
  1. $R_0$: **MFCC Baseline** (20 koefisien spektral + mean/std pooling = 40-dim).
  2. $R_1$: **Generic Audio Embedding** (PANNs CNN14, 2048-dim).
  3. $R_2$: **Bioacoustic Pretrained** (BirdNET V2.4 Backbone, 1024-dim).
  4. $R_3$: **Random Embedding** (Negative control).
* **Engine Pencarian Kemiripan:** Cosine Similarity dengan evaluasi metrik $mAP@k$, $Recall@k$, $Precision@k$, $MRR$.

---

### 3. Hasil Eksekusi Empiris Gate 1 (Resmi & Tervalidasi di Colab)

#### A. Verifikasi Prapemrosesan Audio (150 Berkas: 136 Gallery + 14 Query)
* Laju Sampel: Dari 22.050–48.000 Hz diseragamkan ke **32.000 Hz** (Konstan).
* Durasi Rekaman: Dari 2.5–188.3 detik (rerata 40.1 detik) dipotong pada jendela RMS tertinggi menjadi **5.0 detik** (160.000 sampel).
* Energi RMS: Dinormalisasi dari 0.0024–0.2796 menjadi tepat **0.0500 (+- 0.0004)**.
* Puncak Amplitudo: Dibatasi aman dari 0.0377–1.2652 menjadi **0.1682–1.0000** (bebas kliping).
* Berkas Hasil: [`results/processed/preprocessing_verification_table.csv`](../../results/processed/preprocessing_verification_table.csv) dan [`results/figures/preprocessing_before_after_comparison.png`](../../results/figures/preprocessing_before_after_comparison.png).

#### B. Hasil Evaluasi E1 Clean Retrieval (Seluruh 14 Spesies Sumatera)
| Kode | Nama Representasi | Dimensi | Top-1 Accuracy | mAP@10 | MRR | Recall@10 | Precision@10 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$** | **BirdNET Backbone** | 1024 | **78.57%** | **0.5439** | **0.8004** | **0.5402** | **0.4643** |
| **$R_1$** | **PANNs CNN14** | 2048 | **57.14%** | **0.2510** | **0.6641** | **0.3374** | **0.2929** |
| **$R_0$** | **MFCC Baseline** | 40 | **28.57%** | **0.1447** | **0.4060** | **0.2136** | **0.2071** |
| **$R_3$** | **Random Control** | 40 | **7.14%** | **0.0177** | **0.1912** | **0.0292** | **0.0357** |

* Status Gate 1: **SELESAI (LOLOS / VALID)**.
* Berkas Notebook: [`notebooks/E1_Clean_Retrieval.ipynb`](../../notebooks/E1_Clean_Retrieval.ipynb).

---

## 📊 Daftar 14 Spesies Target (Aktual Sumatera)

1. `Apalharpactes mackloti` (Sumatran Trogon) - 10 file
2. `Batrachostomus_poliolophus` (Sumatran Frogmouth) - 7 file
3. `Caprimulgus_pulchellus` (Salvadori's Nightjar) - 13 file
4. `Carpococcyx_viridis` (Sumatran Ground Cuckoo) - 21 file
5. `Erythropitta_venusta` (Graceful Pitta) - 6 file
6. `Gypsophila_rufipectus` (Rusty-breasted Wren-Babbler) - 28 file
7. `Hydrornis_schneideri` (Schneider's Pitta) - 6 file
8. `Ixos_sumatranus` (Sumatran Bulbul) - 3 file
9. `Lophura_inornata` (Salvadori's Pheasant) - 2 file
10. `Myophonus_melanurus` (Shiny Whistling Thrush) - 15 file
11. `Napothera_albostriata` (Sumatran Wren-Babbler) - 19 file
12. `Pellorneum_buettikoferi` (Sumatran Babbler) - 9 file
13. `Picus_dedemi` (Sumatran Woodpecker) - 4 file
14. `Polyplectron_chalcurum` (Bronze-tailed Peacock-Pheasant) - 19 file
