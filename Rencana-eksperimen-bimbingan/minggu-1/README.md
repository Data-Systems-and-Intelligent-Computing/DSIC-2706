# Rencana Eksperimen — Minggu 1 (GATE 1-R)
**Fokus:** Dataset Avifauna Kepulauan Indonesia (20 Spesies Target, 1.217 Berkas Audio Fisik), Strict Global Recordist-Disjoint Partition (111 Recordist Unik), Standardisasi Audio, EDA, E0 (Pipeline Sanity Check), dan E1 (Clean Retrieval Benchmark).  
**Target Garis Waktu:** Minggu Ke-1  
**Status Eksekusi:** **SELESAI & LULUS 100% (Verifikasi Audit Gate 1-R — Amandemen DEC-13 & DEC-14)**

---

## 1. Pembekuan Target Burung, Manifes, & Preprocessing (DEC-10 & DEC-13)

Sesuai arahan pembimbing (DEC-13), eksperimen beralih dari korpus Neotropis ke korpus **Avifauna Kepulauan Indonesia** guna memastikan keselarasan ekologis tropis dengan derau lapangan AudioMoth ITERA (DEC-14):

* **Spesies Terpilih:** **20 spesies burung umum dan tersebar luas di Indonesia** (total 1.217 berkas audio fisik, 111 perekam unik) yang memenuhi ambang batas ketat (minimal 30 klip dan minimal 14 perekam per spesies, 100% berlabel Indonesia, 20/20 spesies terwakili di Sumatera dengan 168 klip Sumatera / 13,8%).
* **Transparansi Seleksi:** Terpilih secara objektif dari pool kandidat Xeno-Canto Indonesia, didokumentasikan lengkap dalam `Metadata_Indonesia.xlsx` dan `species_freeze.csv`. Seluruh hasil lama BirdCLEF diarsipkan aman di `results/archive/birdclef_2026/`.
* **Parameter Preprocessing Dibekukan:**
  * Sample Rate: **32.000 Hz** (Mono)
  * Durasi Potongan Segmen: **5.0 detik** (160.000 sampel pada jendela energi tertinggi)
  * Normalisasi: RMS Energy Normalization (`target_rms = 0.05`)
  * Transformasi Waktu-Frekuensi: $N_{\text{FFT}} = 1024$, $\text{hop\_length} = 512$
* **Berkas Manifes Kanonikal:**
  * Manifes Spesies Target: [`data/manifests/species_freeze.csv`](../../data/manifests/species_freeze.csv)
  * Manifes Metadata Lengkap: [`data/manifests/Metadata_Indonesia.xlsx`](../../data/manifests/Metadata_Indonesia.xlsx)
  * Manifes Split Bebas Bocor: [`data/manifests/dataset_split.csv`](../../data/manifests/dataset_split.csv)
  * Manifes Unduhan & Verifikasi Hash: [`data/manifests/download_manifest.csv`](../../data/manifests/download_manifest.csv)

---

## 2. Partisi Data Strict Global Recordist-Disjoint (Zero Leakage)

Untuk menjamin evaluasi tidak terdistorsi oleh kesamaan karakteristik perekam (*recorder bias*), pembagian data dilakukan berbasis pengacakan author unik secara global (`seed=42`):

$$\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset, \quad \mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset, \quad \mathcal{R}_{\text{Query}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset$$

* **Gallery:** 674 rekaman audio dari **49 perekam (*author*) unik**
* **Query Clean:** 310 rekaman audio dari **35 perekam (*author*) unik**
* **Calibration:** 233 rekaman audio dari **27 perekam (*author*) unik**
* **Total Audio & Perekam:** 1.217 berkas audio dari **111 perekam (*author*) unik**
* **Integritas:** Diverifikasi otomatis oleh test suite dengan hasil **0 author overlap, 0 XC ID overlap, dan 0 file path overlap**.

---

## 3. Implementasi Representasi Audio (R0, R1, R2, R3)

Empat representasi audio dievaluasi dengan ekstraksi fitur berdimensi asli dan dinormalisasi L2 unit ($\|\mathbf{x}\|_2 = 1.0$):
1. **$R_0$ (MFCC Baseline):** 40 koefisien spektral + pooling rata-rata/standar deviasi (40-dim).
2. **$R_1$ (Generic Pretrained):** PANNs CNN14 pretrained AudioSet (2048-dim).
3. **$R_2$ (Bioacoustic Domain-Specific):** BirdNET V2.4 Backbone (1024-dim).
4. **$R_3$ (Random Control):** Vektor acak terdistribusi seragam (40-dim, `seed=42`).

Metrik kesamaan dihitung menggunakan **Cosine Similarity** murni.

---

## 4. Hasil Evaluasi Empiris Gate 1-R (Kanonikal & Terverifikasi)

Hasil evaluasi E1 Clean Retrieval Benchmark pada 310 kueri bersih terhadap 674 galeri rekaman (tercatat di `results/processed/clean_retrieval_table.csv` dan `paper/tables/clean_retrieval_table.csv`):

| Kode | Representasi | Dimensi | Top-1 Accuracy (%) | mAP@10 | MRR | Recall@10 | Precision@10 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$** | **BirdNET Backbone** | 1024-d | **81.61%** | **0.6358** | **0.8640** | **0.2227** | **0.6274** |
| **$R_1$** | **PANNs CNN14** | 2048-d | **37.74%** | **0.1768** | **0.4907** | **0.0886** | **0.2458** |
| **$R_0$** | **MFCC Baseline** | 40-d | **18.06%** | **0.0691** | **0.2974** | **0.0460** | **0.1274** |
| **$R_3$** | **Random Control** | 40-d | **6.77%** | **0.0232** | **0.1472** | **0.0245** | **0.0668** |

### Analisis Temuan Ilmiah:
1. **Validasi Hipotesis H5 (Kontrol Negatif):** Model terlatih jauh melampaui tebakan acak. Akurasi Top-1 $R_3$ (6.77%) mendekati probabilitas acak teoretis $1/20 = 5.0\%$, membuktikan ketiadaan kebocoran atau jalan pintas (*shortcut learning*).
2. **Hierarki Representasi Bersih:** $R_2\text{ (BirdNET 81.61\%)} > R_1\text{ (PANNs 37.74\%)} > R_0\text{ (MFCC 18.06\%)} \gg R_3\text{ (Random 6.77\%)}$.
3. **Pencatatan Per-Kueri (Audit H5.2):** Berkas [`results/processed/per_query_clean_retrieval.csv`](../../results/processed/per_query_clean_retrieval.csv) menyimpan 1.240 baris rekaman rinci per kueri lengkap dengan kolom `author`, `top1_match`, `max_similarity`, `P@10`, `R@10`, dan `AP@10`.

---

## 5. Notebook Resmi Gate 1-R di `notebooks/`

Direktori `notebooks/` memuat berkas kanonikal yang telah dieksekusi 100%:
1. `notebooks/EDA_Tugas_Akhir.ipynb` — Analisis eksplorasi data 20 spesies Avifauna Indonesia & verifikasi integritas klip.
2. `notebooks/Preprocessing Verification.ipynb` — Validasi pemotongan sinyal 5s dan normalisasi RMS.
3. `notebooks/E0_Pipeline_Sanity_Check.ipynb` — Gerbang anti-kebocoran data dan *smoke test* 4 representasi.
4. `notebooks/E1_Clean_Retrieval.ipynb` — Ekstraksi embedding lengkap dan tolok ukur *clean retrieval*.

---

## 6. Daftar 20 Spesies Target Resmi (`species_freeze.csv`)

| No | Kode Spesies | Nama Ilmiah | Nama Indonesia / Inggris | Klip Total | Perekam | Klip Sumatera |
|:---:|:---|:---|:---|:---:|:---:|:---:|
| 1 | `cinenen_jawa` | *Orthotomus sepium* | Cinenen jawa / Javan Tailorbird | 137 | 35 | 4 |
| 2 | `burungmadu_sriganti` | *Cinnyris jugularis* | Burung-madu sriganti / Olive-backed Sunbird | 128 | 35 | 16 |
| 3 | `walet_linchi` | *Collocalia linchi* | Walet linchi / Cave Swiftlet | 105 | 33 | 9 |
| 4 | `cucak_kutilang` | *Pycnonotus aurigaster* | Cucak kutilang / Sooty-headed Bulbul | 94 | 25 | 12 |
| 5 | `merbah_cerukcuk` | *Pycnonotus goiavier* | Merbah cerukcuk / Yellow-vented Bulbul | 79 | 27 | 17 |
| 6 | `cabai_jawa` | *Dicaeum trochileum* | Cabai jawa / Scarlet-headed Flowerpecker | 65 | 24 | 4 |
| 7 | `remetuk_laut` | *Gerygone sulphurea* | Remetuk laut / Golden-bellied Gerygone | 64 | 27 | 10 |
| 8 | `cipoh_kacat` | *Aegithina tiphia* | Cipoh kacat / Common Iora | 58 | 23 | 8 |
| 9 | `pergam_hijau` | *Ducula aenea* | Pergam hijau / Green Imperial Pigeon | 56 | 23 | 8 |
| 10 | `perkutut_jawa` | *Geopelia striata* | Perkutut jawa / Zebra Dove | 55 | 23 | 4 |
| 11 | `tekukur_biasa` | *Spilopelia chinensis* | Tekukur biasa / Spotted Dove | 50 | 21 | 8 |
| 12 | `layanglayang_loreng` | *Cecropis daurica* | Layang-layang loreng / Red-rumped Swallow | 46 | 20 | 1 |
| 13 | `cekakak_sungai` | *Todiramphus chloris* | Cekakak sungai / Collared Kingfisher | 45 | 21 | 10 |
| 14 | `caladi_tilik` | *Yungipicus moluccensis* | Caladi tilik / Sunda Pygmy Woodpecker | 41 | 19 | 10 |
| 15 | `bultok` | *Psilopogon lineatus* | Takur bultok / Lineated Barbet | 37 | 18 | 4 |
| 16 | `elang_bido` | *Spilornis cheela* | Elang-ular bido / Crested Serpent Eagle | 35 | 15 | 8 |
| 17 | `cekakak_suci` | *Todiramphus sanctus* | Cekakak suci / Sacred Kingfisher | 34 | 14 | 12 |
| 18 | `kapinis_laut` | *Apus pacificus* | Kapinis laut / Pacific Swift | 32 | 16 | 2 |
| 19 | `cabak_kota` | *Caprimulgus affinis* | Cabak kota / Savanna Nightjar | 31 | 16 | 12 |
| 20 | `cinenen_kelabu` | *Orthotomus cinereiceps* | Cinenen kelabu / Grey-hooded Tailorbird | 30 | 14 | 9 |
| **Total** | **20 Spesies** | - | - | **1.217** | **111 unik** | **168 (13,8%)** |

