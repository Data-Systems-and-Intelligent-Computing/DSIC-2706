# Rencana Eksperimen — Minggu 1 (GATE 1-R)
**Fokus:** Dataset Avifauna Kepulauan Indonesia (20 Spesies Target, 1.216 Berkas Audio Fisik), Strict Global Recordist-Disjoint Partition (112 Recordist Unik), Standardisasi Audio, EDA, E0 (Pipeline Sanity Check), dan E1 (Clean Retrieval Benchmark).  
**Target Garis Waktu:** Minggu Ke-1  
**Status Eksekusi:** **SELESAI & LULUS 100% (Verifikasi Audit Gate 1-R — Amandemen DEC-13 & DEC-14)**

---

## 1. Pembekuan Target Burung, Manifes, & Preprocessing (DEC-10 & DEC-13)

Sesuai arahan pembimbing (DEC-13), eksperimen beralih dari korpus Neotropis ke korpus **Avifauna Kepulauan Indonesia** guna memastikan keselarasan ekologis tropis dengan derau lapangan AudioMoth ITERA (DEC-14):

* **Spesies Terpilih:** **20 spesies burung umum dan tersebar luas di Indonesia** (total 1.216 berkas audio fisik, 112 perekam unik) yang memenuhi ambang batas ketat (minimal 30 klip dan minimal 14 perekam per spesies, 100% berlabel Indonesia, 20/20 spesies terwakili di Sumatera dengan 168 klip Sumatera / 13,8%).
* **Transparansi Seleksi:** Terpilih secara objektif dari pool kandidat Xeno-Canto Indonesia, didokumentasikan lengkap dalam `species_freeze.csv`. Seluruh hasil lama BirdCLEF diarsipkan aman di `results/archive/birdclef_2026/`.
* **Parameter Preprocessing Dibekukan:**
  * Sample Rate: **32.000 Hz** (Mono)
  * Durasi Potongan Segmen: **5.0 detik** (160.000 sampel pada jendela energi tertinggi)
  * Normalisasi: RMS Energy Normalization (`target_rms = 0.05`)
  * Transformasi Waktu-Frekuensi: $N_{\text{FFT}} = 1024$, $\text{hop\_length} = 512$
* **Berkas Manifes Kanonikal:**
  * Manifes Spesies Target: [`data/manifests/species_freeze.csv`](../../data/manifests/species_freeze.csv)
  * Manifes Split Bebas Bocor: [`data/manifests/dataset_split.csv`](../../data/manifests/dataset_split.csv)
  * Manifes Unduhan & Verifikasi Hash: [`data/manifests/download_manifest.csv`](../../data/manifests/download_manifest.csv)

---

## 2. Partisi Data Strict Global Recordist-Disjoint (Zero Leakage)

Untuk menjamin evaluasi tidak terdistorsi oleh kesamaan karakteristik perekam (*recorder bias*), pembagian data dilakukan berbasis pengacakan author unik secara global (`seed=42`):

$$\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset, \quad \mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset, \quad \mathcal{R}_{\text{Query}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset$$

* **Gallery:** 673 rekaman audio dari **59 perekam (*author*) unik**
* **Query Clean:** 311 rekaman audio dari **27 perekam (*author*) unik** (28 split composite)
* **Calibration:** 232 rekaman audio dari **25 perekam (*author*) unik**
* **Total Audio & Perekam:** 1.216 berkas audio dari **112 perekam (*author*) unik**
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

Hasil evaluasi E1 Clean Retrieval Benchmark pada 311 kueri bersih terhadap 673 galeri rekaman (tercatat di `results/processed/clean_retrieval_table.csv` dan `paper/tables/clean_retrieval_table.csv`):

| Kode | Representasi | Dimensi | Top-1 Accuracy (%) | mAP@10 | MRR | Recall@10 | Precision@10 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$** | **BirdNET Backbone** | 1024-d | **81.67%** | **0.6370** | **0.8650** | **0.2325** | **0.6942** |
| **$R_1$** | **PANNs CNN14** | 2048-d | **37.94%** | **0.1771** | **0.5090** | **0.0843** | **0.2586** |
| **$R_0$** | **MFCC Baseline** | 40-d | **18.01%** | **0.0690** | **0.3079** | **0.0360** | **0.1308** |
| **$R_3$** | **Random Control** | 40-d | **6.75%** | **0.0231** | **0.1811** | **0.0150** | **0.0615** |

### Analisis Temuan Ilmiah:
1. **Validasi Hipotesis H5 (Kontrol Negatif):** Model terlatih jauh melampaui tebakan acak. Akurasi Top-1 $R_3$ (6.75%) mendekati probabilitas acak teoretis $1/20 = 5.0\%$, membuktikan ketiadaan kebocoran atau jalan pintas (*shortcut learning*).
2. **Hierarki Representasi Bersih:** $R_2\text{ (BirdNET 81.67\%)} > R_1\text{ (PANNs 37.94\%)} > R_0\text{ (MFCC 18.01\%)} \gg R_3\text{ (Random 6.75\%)}$.
3. **Pencatatan Per-Kueri (Audit H5.2):** Berkas [`results/processed/per_query_clean_retrieval.csv`](../../results/processed/per_query_clean_retrieval.csv) menyimpan rekaman rinci per kueri lengkap dengan kolom `query_id`, `author`, `top1_match`, `max_similarity`, `P@10`, `R@10`, dan `AP@10`.

---

## 5. Notebook Resmi Gate 1-R di `notebooks/`

Direktori `notebooks/` memuat berkas kanonikal yang telah dieksekusi 100%:
1. `notebooks/EDA_Tugas_Akhir.ipynb` — Analisis eksplorasi data 20 spesies Avifauna Indonesia & verifikasi integritas klip.
2. `notebooks/Preprocessing Verification.ipynb` — Validasi pemotongan sinyal 5s dan normalisasi RMS.
3. `notebooks/E0_Pipeline_Sanity_Check.ipynb` — Gerbang anti-kebocoran data dan *smoke test* 4 representasi.
4. `notebooks/E1_Clean_Retrieval.ipynb` — Ekstraksi embedding lengkap dan tolok ukur *clean retrieval*.

---

## 6. Daftar 20 Spesies Target Resmi (`species_freeze.csv`)

| No | Spesies Kunci | Nama Ilmiah | Nama Indonesia / Inggris | Klip Terverifikasi | Perekam Unik |
| :-: | :--- | :--- | :--- | :-: | :-: |
| 1 | `pygcup1` | *Pnoepyga pusilla* | Berencet kerdil / Pygmy Cupwing | 105 | 35 |
| 2 | `rubcuc1` | *Cacomantis sepulcralis* | Wiwik uncuing / Rusty-breasted Cuckoo | 85 | 32 |
| 3 | `horbab1` | *Malacocincla sepiaria* | Pelanduk semak / Horsfield's Babbler | 68 | 32 |
| 4 | `moutai1` | *Phyllergates cucullatus* | Cinenen gunung / Mountain Tailorbird | 137 | 29 |
| 5 | `lessho1` | *Brachypteryx leucophris* | Cingcoang cokelat / Lesser Shortwing | 66 | 26 |
| 6 | `latnig1` | *Caprimulgus macrurus* | Cabak maling / Large-tailed Nightjar | 47 | 26 |
| 7 | `sohbul1` | *Pycnonotus aurigaster* | Cucak kutilang / Sooty-headed Bulbul | 44 | 26 |
| 8 | `olbsun1` | *Cinnyris jugularis* | Burung-madu sriganti / Olive-backed Sunbird | 123 | 23 |
| 9 | `hoopit1` | *Pitta sordida* | Paok hijau / Hooded Pitta | 62 | 22 |
| 10 | `suncuc1` | *Cuculus lepidus* | Kangkok sunda / Sunda Cuckoo | 42 | 22 |
| 11 | `savnig1` | *Caprimulgus affinis* | Cabak kota / Savanna Nightjar | 31 | 20 |
| 12 | `hacdro1` | *Dicrurus hottentottus* | Srigunting rambut / Hair-crested Drongo | 91 | 19 |
| 13 | `subwar1` | *Horornis vulcanius* | Kerakbasi sunda / Sunda Bush Warbler | 48 | 19 |
| 14 | `gpipig1` | *Ducula aenea* | Pergam hijau / Green Imperial Pigeon | 45 | 19 |
| 15 | `whbsho1` | *Brachypteryx montana* | Cingcoang alis-putih / White-browed Shortwing | 40 | 19 |
| 16 | `ghcfly1` | *Culicicapa ceylonensis* | Sikatan kepala-kelabu / Grey-headed Canary-flycatcher | 38 | 19 |
| 17 | `comior1` | *Aegithina tiphia* | Cipoh kacat / Common Iora | 39 | 18 |
| 18 | `crseag1` | *Spilornis cheela* | Elang-ular bido / Crested Serpent Eagle | 35 | 15 |
| 19 | `ashtai1` | *Orthotomus ruficeps* | Cinenen kelabu / Ashy Tailorbird | 30 | 15 |
| 20 | `colkin1` | *Todiramphus chloris* | Cekakak sungai / Collared Kingfisher | 40 | 14 |
| **Total** | **20 Spesies** | | | **1.216 Klip** | **112 Author Unik** |

