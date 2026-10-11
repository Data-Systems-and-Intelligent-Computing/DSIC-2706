# DSIC-2706 — Ketahanan Representasi Audio Beku untuk Temu Kembali Bioakustik di Bawah Derau Lingkungan Tropis ITERA

Repositori penelitian resmi untuk Tugas Akhir topik **DSIC-2706: Mencari Audio yang Mirip Ketika Datanya Terbatas**.

Fokus penelitian ini bukan membuat pengklasifikasi (*classifier*) spesies baru, melainkan menguji secara komparatif **ketahanan representasi audio beku (*frozen audio representations*) untuk temu kembali kemiripan (*similarity retrieval*)** ketika kueri bioakustik mengalami degradasi derau lingkungan tropis nyata kampus ITERA (*Institut Teknologi Sumatera*).

Judul artikel ilmiah terkalibrasi:

> **Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on Indonesian Avifauna with Field-Recorded ITERA Tropical Noise**

---

## 1. Pertanyaan Penelitian (Research Questions)

### RQ Utama
**Representasi audio mana yang mempertahankan kualitas temu kembali kemiripan (*similarity retrieval*) paling baik ketika kueri bioakustik avifauna Indonesia mengalami penurunan rasio sinyal terhadap derau (*Signal-to-Noise Ratio* / SNR) dengan derau lingkungan tropis ITERA?**

### Sub-RQ
1. **Sub-RQ 1 (Ketahanan Terkontrol E2):** Seberapa besar penurunan performa temu kembali (`mAP@10`, `Recall@10`, `Top-1 Accuracy`) untuk representasi akustik klasik (MFCC), model generik (*generic deep audio*), dan model bioakustik (*avian domain-specific*) pada berbagai tingkat SNR (+20 dB, +10 dB, 0 dB, -5 dB) yang dicampur dengan derau fisik AudioMoth ITERA?
2. **Sub-RQ 2 (Stabilitas Ambang Batas Terbuka E3):** Apakah ambang batas kemiripan ($\tau^*$) yang dioptimasi dan dibekukan pada subset kalibrasi terpisah mampu secara stabil menolak spesies burung non-target dan derau lingkungan murni ketika kueri terdegradasi oleh derau?
3. **Sub-RQ 3 (Sensitivitas Profil Derau Lintas Habitat E4):** Apakah representasi bioakustik memperlihatkan ketahanan yang konsisten ketika berhadapan dengan variasi profil spektral derau latar dari tiga habitat berbeda (vegetasi Kebun Raya, perairan Embung F, dan koridor struktural Gedung F ITERA)?
4. **Sub-RQ 4 (Taksonomi Moda Kegagalan E5):** Apa saja faktor fisik akustik (*spectral centroid*, *bandwidth*, *similarity margin deficit*) yang memicu kegagalan temu kembali (*open-set false rejection*, *top-1 confusion*, atau *total collapse*) pada kondisi ekstrem?

---

## 2. Hipotesis Saintifik

* **$H_1$ — Robustness Retention:** Representasi *deep pretrained* (BirdNET dan PANNs) mempertahankan proporsi retensi relatif `mAP@10` yang secara signifikan lebih tinggi daripada representasi klasik *hand-crafted* (MFCC) ketika SNR diturunkan hingga -5 dB.
* **$H_2$ — Domain-Specific Advantage:** Representasi terlatih bioakustik spesifik domain burung (*BirdNET*) mengalami degradasi temu kembali yang lebih landai dibandingkan representasi audio umum (*PANNs CNN14*) pada kueri avifauna Indonesia yang dicampur derau lingkungan nyata.
* **$H_3$ — Noise Profile Invariance:** Representasi bioakustik terlatih mempertahankan performa yang lebih stabil lintas profil spektral habitat (vegetasi vs. perairan vs. struktural) dibandingkan representasi audio umum yang lebih rentan terhadap distorsi frekuensi tinggi/rendah.
* **$H_4$ — Threshold Transfer Deficit:** Ambang batas kemiripan $\tau^*$ yang dikalibrasi pada kondisi bersih mengalami penurunan *Recall* yang tajam pada SNR rendah akibat pelemahan skor kemiripan laten (*similarity score compression*).
* **$H_5$ — Positive Control:** Seluruh representasi terlatih ($R_0, R_1, R_2$) harus secara signifikan melampaui tebakan acak ($R_3$) pada kondisi bersih sebagai bukti validitas pipeline (*pipeline sanity check*).

---

## 3. Batas Kontribusi Ilmiah

### Kontribusi Utama:
1. Evaluasi ketahanan berpasangan (*paired robustness evaluation*) pada kueri yang identik menggunakan audio burung asli Indonesia dari Xeno-Canto.
2. Uji stres derau lingkungan tropis nyata menggunakan bank rekaman fisik AudioMoth kampus ITERA (1.799 berkas audio WAV terverifikasi bebas burung).
3. Perbandingan sistematis antara *hand-crafted baseline* ($R_0$ MFCC), *generic pretrained* ($R_1$ PANNs CNN14), *domain-specific bioacoustic* ($R_2$ BirdNET V2.4), dan *negative control* ($R_3$ Random Control).
4. Penyelidikan transfer ambang batas open-set dengan optimasi statistik Youden's J yang dibekukan (*frozen threshold*).
5. Audit taksonomi kegagalan terstratifikasi berdasarkan parameter akustik nyata (*spectral centroid*, *bandwidth*, dan *margin to tau*).
6. Pembuktian keterulangan (*reproducibility*) end-to-end dengan pelacakan asal usul berkas derau fisik (`noise_file`) pada setiap kueri.

### Yang **Bukan** Kontribusi Penelitian:
* Melatih ulang (*fine-tuning*) arsitektur model baru.
* Membuat aplikasi identifikasi spesies bergerak (*mobile app*) atau dashboard inventarisasi ekologis.
* Mengestimasi populasi atau kelimpahan satwa (*occupancy / abundance modelling*).

---

## 4. Representasi yang Dibandingkan

| Kode | Representasi | Dimensi | Peran | Checkpoint / Sumber |
|:---:|---|:---:|---|---|
| **$R_0$** | MFCC (40 koefisien + delta + delta-delta, mean/std pooling) | 40-d | Baseline akustik klasik | `librosa` feature extractor |
| **$R_1$** | PANNs CNN14 (AudioSet general audio pretrained) | 2048-d | Deep embedding generik | `checkpoints/Cnn14_mAP=0.431.pth` |
| **$R_2$** | BirdNET Backbone V2.4 (Avian bioacoustic domain pretrained) | 1024-d | Domain-specific representation | Checkpoint resmi `birdnet` |
| **$R_3$** | Random Control (Vektor acak terdistribusi seragam) | 40-d | Negative control | Deterministik (`seed=42`) |

Seluruh embedding dinormalisasi ke *unit hypersphere* ($\|\mathbf{x}\|_2 = 1.0$) dan dievaluasi menggunakan metrik **Cosine Similarity**:
$$\text{sim}(\mathbf{q}, \mathbf{g}) = \frac{\mathbf{q} \cdot \mathbf{g}}{\|\mathbf{q}\|_2 \|\mathbf{g}\|_2}$$

Semua representasi berstatus **beku (*frozen*)** tanpa pembaruan bobot, menjamin keadilan evaluasi murni pada representasi fitur laten.

---

## 5. Dataset dan Bank Derau Fisik

### A. Dataset Avifauna Indonesia (Xeno-Canto Indonesia)
Korpus data utama menggunakan rekaman vokal burung dari wilayah geografis Indonesia yang diunduh dari Xeno-Canto:
* **20 Spesies Kandidat Beku:** Spesies umum dan tersebar luas di Indonesia, dengan representasi wilayah barat dan kepulauan (termasuk Sumatera):
  * *Spilornis cheela*, *Pycnonotus aurigaster*, *Todiramphus chloris*, *Orthotomus ruficeps*, *Dicaeum trochileum*, *Prinia familiaris*, *Zosterops flavus*, *Lanius schach*, *Streptopelia chinensis*, dll.
* **Total Rekaman Terverifikasi:** 1.217 berkas audio MP3 (30–137 rekaman per spesies, rata-rata 60,8 rekaman/spesies; 14–35 perekam unik per spesies).
* **Audit Integritas Unduhan:** Seluruh berkas tercatat di `data/manifests/download_manifest.csv` lengkap dengan HTTP status 200, ukuran byte, checksum SHA-256, sampling rate asli, durasi, dan verifikasi keterbacaan (*100% decodable*).
* **Standar Prapemrosesan:** Durasi 5,0 detik (160.000 sampel pada 32 kHz), mono, normalisasi energi RMS = 0.05.
* **Kebijakan Lisensi Git:** Berkas audio fisik tidak di-commit ke Git (mematuhi lisensi non-komersial/non-derivatif); hanya manifes metadata dan hash yang dilacak.

### B. Bank Derau Fisik AudioMoth Kampus ITERA
* **1.799 Berkas WAV Fisik:** Diambil langsung menggunakan perangkat perekam otonom *AudioMoth* di 5 lokasi kampus ITERA (Kebun Raya ITERA, Embung F, Gedung F, Masjid At-Tanwir, Sekitar GKU 1).
* **Bebas Vokalisasi Burung (*Bird-Free Verified*):** Seluruh rekaman telah diaudit dan diverifikasi tidak mengandung panggilan vokal burung target.
* **Partisi Bebas Kebocoran (*Noise Pool Separation*):**
  * **1.528 berkas** dialokasikan khusus untuk pencampuran derau aditif E2 dan E4.
  * **271 berkas** dialokasikan khusus untuk kontrol negatif kelas terbuka E3.
* **Penolakan Derau Senyap:** Engine pencampuran menolak segmen dengan $\text{RMS} < 10^{-4}$ ($P_{\text{noise}} \le 10^{-10}$).
* **Penghapusan Pink Noise:** Fallback derau sintetis telah **dihapus permanen**. Modul melempar `FileNotFoundError` keras jika berkas fisik tidak ditemukan.

### C. Arsip Warisan (*Legacy Archive*)
Hasil evaluasi lama yang pernah menggunakan data BirdCLEF telah dipindahkan dan diarsipkan secara terpisah di `results/archive/birdclef_2026/` untuk transparansi jejak rekam ilmiah.

---

## 6. Partisi Data (Strict Global Recordist-Disjoint)

Partisi data dibekukan di `data/manifests/dataset_split.csv` dengan memisahkan identitas perekam (*author/recordist*) secara absolut:

```text
Xeno-Canto Indonesia (1.217 klip | 20 spesies burung Indonesia)
├── Gallery Set      : 674 klip (60 perekam unik) -> Basis data referensi pencarian
├── Query Clean Set  : 310 klip (31 perekam unik) -> Kueri bersih uji berpasangan
└── Calibration Set  : 233 klip (20 perekam unik) -> Kalibrasi ambang batas open-set

Unknown Open-Set Manifest (543 klip kontrol negatif)
├── Unknown Calibration : 233 klip kontrol negatif kalibrasi
└── Unknown Test Set    : 310 klip kontrol negatif pengujian
```

### Jaminan Integritas Matematika Bebas Kebocoran:
* **Zero Recordist Overlap:** 0 perekam beririsan antar Galeri, Kueri, dan Kalibrasi ($\text{Recordists}(G) \cap \text{Recordists}(Q) = \emptyset$).
* **Zero Recording ID Overlap:** 0 nomor katalog Xeno-Canto yang beririsan antar subset.
* **Zero Filepath Overlap:** 0 duplikasi berkas fisik audio.

---

## 7. Ringkasan Temuan Eksperimen Utama (E0–E5)

Seluruh eksperimen telah selesai dijalankan secara penuh dan direproduksi pada notebook Jupyter resmi:

### E0 — Pipeline Sanity Check (100% Lolos)
* **Notebook:** [`notebooks/E0_Pipeline_Sanity_Check.ipynb`](./notebooks/E0_Pipeline_Sanity_Check.ipynb)
* Seluruh gerbang kebocoran terverifikasi nol (*zero leakage verified*).
* Ekstraksi fitur $R_0, R_1, R_2, R_3$ presisi dimensi, bebas nilai `NaN`/`Inf`, dan bernorma unit.
* Hipotesis $H_5$ terbukti: model terlatih melampaui kontrol acak secara meyakinkan.

### E1 — Clean Retrieval Benchmark
* **Notebook:** [`notebooks/E1_Clean_Retrieval.ipynb`](./notebooks/E1_Clean_Retrieval.ipynb)
* Menguji 310 kueri bersih terhadap 674 rekaman galeri lintas 20 spesies:

| Kode | Representasi | Dimensi | Top-1 Accuracy (%) | mAP@10 | MRR | Precision@10 | Recall@10 |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **$R_2$** | **BirdNET Backbone V2.4** | 1024-d | **81.61%** | **0.6358** | **0.8646** | **0.6932** | **0.2311** |
| **$R_1$** | **PANNs CNN14** | 2048-d | 37.74% | 0.1768 | 0.5079 | 0.2584 | 0.0839 |
| **$R_0$** | **MFCC Baseline** | 40-d | 18.06% | 0.0691 | 0.3081 | 0.1310 | 0.0360 |
| **$R_3$** | **Random Control** | 40-d | 6.77% | 0.0232 | 0.1815 | 0.0616 | 0.0150 |

### E2 — Controlled Paired Noise Degradation
* **Notebook:** [`notebooks/E2_Paired_Noise_Degradation.ipynb`](./notebooks/E2_Paired_Noise_Degradation.ipynb)
* Uji stres pada 310 kueri berpasangan dengan derau fisik ITERA:

| Kondisi | SNR | $R_2$ BirdNET mAP@10 (Retensi) | $R_1$ PANNs mAP@10 (Retensi) | $R_0$ MFCC mAP@10 (Retensi) | $R_3$ Random mAP@10 |
|---|:---:|:---:|:---:|:---:|:---:|
| **Clean** | $\infty$ | 0.6358 (100.0%) | 0.1768 (100.0%) | 0.0691 (100.0%) | 0.0232 |
| **SNR +20 dB** | 20 dB | 0.6409 (100.8%) | 0.1963 (111.0%) | 0.0775 (112.1%) | 0.0190 |
| **SNR +10 dB** | 10 dB | 0.6202 (97.5%) | 0.1859 (105.2%) | 0.0643 (93.1%) | 0.0242 |
| **SNR 0 dB** | 0 dB | 0.5670 (89.2%) | 0.1330 (75.2%) | 0.0369 (53.4%) | 0.0214 |
| **SNR -5 dB** | -5 dB | **0.4962 (78.0%)** | **0.0982 (55.5%)** | **0.0247 (35.7%)** | 0.0231 |

> **Temuan Kunci ($H_1$ & $H_2$ Terbukti):** Pada kondisi ekstrem (SNR -5 dB), BirdNET mempertahankan **78.0%** performa awalnya, jauh lebih tangguh daripada PANNs (55.5%) dan MFCC (35.7%).

### E3 — Open-Set Threshold Calibration & Transfer
* **Notebook:** [`notebooks/E3_Open_Set_Threshold.ipynb`](./notebooks/E3_Open_Set_Threshold.ipynb)
* Ambang batas $\tau^*$ dioptimasi pada subset kalibrasi via Youden's J ($J = \text{TPR} - \text{FPR}$) dan **dibekukan**:
  * **$R_2$ BirdNET:** $\tau^* = 0.7071$ (Kalibrasi AUROC: 0.7611, F1: 0.6650, Youden J: 0.4206)
  * **$R_1$ PANNs:** $\tau^* = 0.8974$ (Kalibrasi AUROC: 0.7141, F1: 0.7033, Youden J: 0.3734)
  * **$R_0$ MFCC:** $\tau^* = 0.9958$ (Kalibrasi AUROC: 0.5283, F1: 0.3000, Youden J: 0.0987)
* **Hasil Pengujian Transfer:** BirdNET paling stabil menekan *False Positive Rate* (FPR hanya 20.0% pada Clean dan turun ke 9.35% pada -5 dB), sementara PANNs mengalami FPR tinggi (~47% pada Clean dan 27% pada -5 dB).

### E4 — Sensitivitas Profil Spektral Derau Lintas Habitat ITERA
* **Notebook:** [`notebooks/E4_Real_Soundscape_Domain_Shift.ipynb`](./notebooks/E4_Real_Soundscape_Domain_Shift.ipynb)
* Menguji kueri terhadap tiga habitat derau fisik kampus ITERA pada SNR terkontrol:
  1. **Kebun Raya ITERA** (Biophony serangga & vegetasi tropis)
  2. **Embung F ITERA** (Perairan terbuka & resonansi angin)
  3. **Gedung F ITERA** (Koridor struktural & antropogenik)
* **Hasil:** Performa BirdNET ($R_2$) sangat konsisten di ketiga habitat ($p = 0.610$, tidak ada perbedaan signifikan antar habitat). Sebaliknya, PANNs ($R_1$) sangat sensitif terhadap karakter spektral derau ($p < 0.001$), di mana derau Kebun Raya (frekuensi tinggi) menurunkan mAP@10 PANNs jauh lebih tajam daripada derau Gedung F.

### E5 — Analisis Kasus Kegagalan Terstratifikasi
* **Notebook:** [`notebooks/E5_Failure_Analysis.ipynb`](./notebooks/E5_Failure_Analysis.ipynb)
* Audit mendalam pada 30 kasus kegagalan terstratifikasi (10 Clean, 20 SNR -5 dB):
  * **Open-Set False Rejection (10 kasus):** Top-1 benar namun $\text{sim} < \tau^*$ karena pelemahan skor kemiripan pada SNR rendah.
  * **Top-1 Confusion (Above $\tau^*$) (9 kasus):** $\text{sim} \ge \tau^*$ namun salah dipasangkan ke taksa lain akibat artefak fitur akustik.
  * **Total Retrieval Collapse (11 kasus):** Skor anjlok di bawah $\tau^*$ dan salah dipasangkan ke spesies lain akibat dominasi energi derau.

---

## 8. Struktur Direktori Repositori

```text
DSIC-2706/
├── README.md                                          # Dokumentasi utama proyek
├── pyproject.toml / requirements.txt                  # Manajemen dependensi pustaka Python
├── run_tests.py                                       # Suite pengujian integritas saintifik (10/10 PASS)
│
├── data/
│   ├── manifests/
│   │   ├── dataset_split.csv                          # Manifes kanonik 1.217 klip (Recordist-Disjoint)
│   │   ├── download_manifest.csv                      # Log verifikasi unduhan (SHA-256, SR, status)
│   │   ├── species_freeze.csv                         # 20 spesies burung Indonesia resmi
│   │   ├── species_excluded.csv                       # Daftar spesies yang tereliminasi
│   │   ├── itera_noise_manifest.csv                   # Manifes 1.799 berkas AudioMoth ITERA
│   │   └── unknown_open_set_manifest.csv              # Manifes 543 kontrol negatif kelas terbuka
│   ├── xeno_canto_indonesia/                          # Direktori audio MP3 Xeno-Canto Indonesia (gitignored)
│   └── itera_noise/                                   # Direktori rekaman AudioMoth ITERA (gitignored)
│
├── notebooks/                                         # 8 Notebook Jupyter Resmi
│   ├── EDA_Tugas_Akhir.ipynb                          # Analisis eksplorasi data avifauna Indonesia
│   ├── Preprocessing Verification.ipynb               # Verifikasi pemotongan & normalisasi RMS
│   ├── E0_Pipeline_Sanity_Check.ipynb                 # Uji anti-kebocoran & kontrol negatif H5
│   ├── E1_Clean_Retrieval.ipynb                       # Tolok ukur retrieval kueri bersih
│   ├── E2_Paired_Noise_Degradation.ipynb              # Uji ketahanan derau aditif terkontrol
│   ├── E3_Open_Set_Threshold.ipynb                    # Kalibrasi ambang batas terbuka Youden's J
│   ├── E4_Real_Soundscape_Domain_Shift.ipynb          # Sensitivitas profil derau lintas habitat
│   └── E5_Failure_Analysis.ipynb                      # Audit kegagalan saintifik terstratifikasi
│
├── src/                                               # Modul kode terpusat
│   ├── preprocess.py                                  # Pipeline audio (32 kHz, 5s, RMS 0.05)
│   ├── embeddings.py                                  # Ekstraktor representasi (R0, R1, R2, R3)
│   ├── mix_noise.py                                   # Engine pencampuran derau fisik AudioMoth ITERA
│   ├── retrieve.py                                    # Engine cosine similarity & ranking retrieval
│   ├── evaluate.py                                    # Komputasi metrik & logging noise_file
│   ├── calibrate_threshold.py                         # Kalibrasi ambang batas open-set Youden's J
│   ├── analyze_failures.py                            # Audit kegagalan terstratifikasi
│   └── run_benchmark.py                               # Runner eksekusi benchmark end-to-end
│
├── results/
│   ├── features/                                      # Cache embedding NPZ (R0, R1, R2, R3)
│   ├── processed/                                     # Tabel metrik agregat terproses
│   ├── figures/                                       # Grafik & kurva saintifik
│   ├── raw/                                           # Hasil mentah per-kueri (dengan kolom noise_file)
│   └── archive/                                       # Arsip aman hasil eksperimen lama
│       └── birdclef_2026/                             # Arsip hasil warisan BirdCLEF
│
├── paper/                                             # Naskah artikel ilmiah
│   ├── manuscript.md                                  # Draf naskah publikasi lengkap
│   ├── tables/                                        # Tabel metrik tersinkronisasi
│   └── figures/                                       # Gambar resolusi tinggi naskah
│
├── configs/
│   ├── thresholds.yaml                                # Ambang batas beku (tau*) resmi E3
│   └── datasets.yaml                                  # Konfigurasi parameter dataset
│
└── tests/                                             # Suite pengujian unit dan integrasi
    ├── unit/
    │   ├── test_snr_mixing.py                         # Uji formula SNR & derau fisik 1.799 berkas
    │   ├── test_cosine.py                             # Uji sifat matematika cosine similarity
    │   ├── test_threshold_freeze.py                   # Uji kestabilan ambang beku
    │   └── test_manifest_and_models.py                # Uji SHA-256 manifes & dimensi embedding
    └── integration/
        └── test_split_leakage.py                      # Uji zero leakage identitas perekam
```

---

## 9. Petunjuk Eksekusi Cepat (Quick Start)

### Lingkungan Python
```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### Menjalankan Seluruh Unit Test Saintifik
```bash
python run_tests.py
```
*Output diharapkan: `10/10 Pengujian Lolos (100.0%)`.*

### Menjalankan Pipeline Benchmark Penuh
```bash
# 1. Jalankan benchmark E1, E2, E3, dan E5:
python src/run_benchmark.py

# 2. Jalankan evaluasi kalibrasi terbuka E3:
python scripts/run_e3_calibration.py

# 3. Jalankan eksperimen sensitivitas habitat E4:
python scripts/run_e4_domain_shift.py

# 4. Sinkronisasi hash manifes integritas:
python scripts/update_manifest_hashes.py
```

---

## 10. Lisensi dan Etika Penelitian

1. **Kode Program:** Dilisensikan di bawah lisensi terbuka [MIT License](LICENSE).
2. **Audio Xeno-Canto:** Hak cipta rekaman audio dipegang oleh masing-masing perekam (*recordist*) di Xeno-Canto dengan lisensi Creative Commons (CC BY-NC-SA, CC BY-NC-ND). Rincian atribusi lengkap terdokumentasi di `data/manifests/download_manifest.csv`. Berkas audio tidak disertakan dalam repositori Git publik.
3. **Rekaman Derau Lapangan ITERA:** Hak cipta rekaman AudioMoth dipegang oleh tim peneliti Institut Teknologi Sumatera (ITERA).

---

## 11. Aturan Reproducibility & Integritas Data

Setiap eksekusi (*run*) eksperimen wajib mencatat parameter minimal berikut:

```text
run_id
representation (R0, R1, R2, R3)
checkpoint/version
query_id
gallery_manifest_version
noise_id / noise_file
SNR (Clean, +20, +10, 0, -5 dB)
random_seed (default: 42)
threshold_version (tau beku)
ranking (Top-k candidates)
metrics (mAP@10, Top-1, MRR, FPR, Recall)
runtime (detik)
```

Setiap klaim pada artikel ilmiah dan naskah skripsi harus dapat ditelusuri (*fully traceable*):

```text
Research Question (RQ)
       ↓
Eksperimen (E0 s.d. E5)
       ↓
Hasil Mentah (results/raw/*.csv)
       ↓
Hasil Terproses (results/processed/*.csv)
       ↓
Tabel & Gambar Publikasi (paper/tables/ & paper/figures/)
       ↓
Klaim Saintifik di Naskah (paper/manuscript.md)
```

### Kebijakan Data dan Version Control (Git):
* **Wajib di-version-control:** Manifes (`.csv`, `.json`), metadata (`.xlsx`), berkas *hash* integritas (`SHA-256`), konfigurasi (`.yaml`), kode program (`src/`, `scripts/`), dan ringkasan metrik hasil.
* **Dilarang di-commit ke Git (.gitignore):** Berkas audio mentah berukuran besar (`*.mp3`, `*.wav`, `*.flac`), *checkpoint weights* deep learning besar (`*.pth`), dan direktori cache embedding sementara (`.npz` di luar rilis resmi).

---

## 12. Rencana Kerja Satu Bulan & Timeline Pelaksanaan

### Minggu 1 — Gate 1-R (Fondasi Dataset & Baseline Bersih)
* Pembekuan target 20 spesies Avifauna Indonesia (`species_freeze.csv`).
* Pengunduhan audio Xeno-Canto dan pembuatan `download_manifest.csv` (1.217 klip fisik, 111 recordist).
* Partisi bebas bocor *Strict Global Recordist-Disjoint* (`dataset_split.csv`).
* Standardisasi audio (32 kHz, mono, potongan 5s pada energi puncak, RMS 0.05).
* Eksekusi E0 (Pipeline Sanity Check & H5 Random Control) dan E1 (Clean Retrieval Benchmark).

### Minggu 2 — Gate 2 (Ketahanan Derau Lapangan ITERA)
* Kurasi dan audit bank derau fisik 1.799 berkas WAV AudioMoth dari 5 titik kampus ITERA (`itera_noise_manifest.csv`).
* Isolasi partisi derau untuk mixing vs open-set unknown (DEC-14) dan penghapusan permanen fallback pink noise.
* Eksekusi E2 Paired Noise Degradation pada grid SNR: Clean, +20 dB, +10 dB, 0 dB, dan -5 dB.
* Pembuatan kurva degradasi SNR dan analisis retensi relatif terhadap baseline bersih.

### Minggu 3 — Gate 3 (Open-Set Rejection & Sensitivitas Habitat)
* Penyusunan 498 kontrol negatif kalibrasi dan 200 kontrol negatif uji pada `unknown_open_set_manifest.csv`.
* Optimasi dan pembekuan ambang batas $\tau^*$ via Youden's Index ($J$) pada kalibrasi bebas bocor.
* Eksekusi E3 Open-Set Rejection transfer lintas grid SNR (evaluasi dinamika FPR dan recall).
* Eksekusi E4 Sensitivitas Profil Derau Lintas 3 Habitat Lapangan ITERA (Kebun Raya, Embung F, Gedung Terpadu).
* Eksekusi E5 Audit Kasus Kegagalan Terstratifikasi (30 kasus nyata lintas taksa).

### Minggu 4 — Gate 4 (Statistik Inferensial, Penulisan, & Pembekuan)
* Uji inferensial Paired Bootstrap Resampling 1.000 iterasi dengan CI 95% untuk 7 skenario hipotesis.
* Finalisasi 11 butir tabel publikasi (`paper/tables/`) dan gambar resolusi tinggi (`paper/figures/`).
* Sinkronisasi draf naskah publikasi v0.8 (`paper/manuscript.md`) dan panduan tugas akhir.
* Uji reproduksi segar (*fresh reproducibility test*) dari klon bersih: 10/10 unit tests PASS (100.0%).
* Pembekuan kode program (*code freeze*) dan penandaan commit kanonik Git.

---

## 13. Definition of Done (Status Kelulusan Gate 1 s.d. Gate 4)

Penelitian utama dinyatakan selesai 100% dengan status kelulusan empiris terverifikasi:

- [x] **Daftar taksa & spesies target dibekukan:** 20 spesies Avifauna Indonesia, 1.217 rekaman terverifikasi hash SHA-256 (DEC-13).
- [x] **Partisi bebas kebocoran (Zero Leakage):** 0 recording ID overlap, 0 file path overlap, 0 recordist overlap terverifikasi otomatis oleh test suite.
- [x] **Baseline klasik MFCC selesai:** Representasi $R_0$ terekstraksi penuh (40-dim).
- [x] **Generic pretrained representation selesai:** Representasi $R_1$ PANNs CNN14 AudioSet terekstraksi penuh (2048-dim).
- [x] **Bioacoustic domain representation selesai:** Representasi $R_2$ BirdNET Backbone terekstraksi penuh (1024-dim).
- [x] **Clean retrieval E1 selesai:** $R_2$ (mAP 0.6358, Top-1 81.6%) > $R_1$ (0.1768, 37.7%) > $R_0$ (0.0691, 18.1%) >> $R_3$ (0.0232, 6.8%).
- [x] **Empat kondisi derau E2 selesai:** Grid SNR (+20, +10, 0, -5 dB) dengan 1.799 berkas AudioMoth fisik ITERA (retensi $R_2$ 78.0%).
- [x] **Metrik mAP@k dan Recall@k dihitung:** Lengkap di seluruh kondisi dan representasi.
- [x] **Ambang batas $\tau^*$ beku murni dari kalibrasi:** $\tau^*_{R_2} = 0.7071$, $\tau^*_{R_1} = 0.8974$, $\tau^*_{R_0} = 0.9958$ tanpa sentuhan test set.
- [x] **Metrik open-set E3 tersedia:** FPR, recall, AUROC, F1-score terlapor lengkap per SNR.
- [x] **Uji sensitivitas habitat E4 selesai:** Perbandingan berdampingan 3 habitat ITERA ($R_2$ invarian $p=0.610$, $R_1$ sensitif $p<0.001$).
- [x] **Minimal 20 kasus kegagalan diaudit manusia:** 30 kasus nyata terstratifikasi dianalisis dengan parameter akustik fisik pada E5.
- [x] **Confidence Interval (CI 95%) tersedia:** Paired bootstrap 1.000 iterasi dengan pita galat dan $p$-value empiris.
- [x] **Manifes, seed, config, dan hash tersinkronisasi:** 10/10 unit test lulus 100%.
- [x] **Satu tabel dan satu gambar dapat direproduksi dari klon bersih:** Seluruh artefak dapat dieksekusi ulang secara deterministik.
- [x] **Keterbatasan ekologis dinyatakan jujur:** Ketiadaan anotasi bounding box in-situ lapangan dideklarasikan sebagai agenda masa depan.

---

## 14. Publication Boundary

Artikel ilmiah dan naskah skripsi ini secara ketat difokuskan untuk menjawab:  
**"Ketahanan representasi audio beku terhadap degradasi derau aditif dan stabilitas ambang batas temu kembali bioakustik."**

Luaran pemantauan lapangan di ITERA diposisikan sebagai analisis sensitivitas spektral terkontrol, bukan studi sensus biodiversitas ekologis penuh. Peneliti tidak mengklaim inventarisasi ekologis kampus tanpa protokol survei transek visual dan anotasi bounding box in-situ yang terkalibrasi.

---

## 15. Catatan dan Arahan Dosen Pembimbing

Alur besar metodologi penelitian ini dirancang secara terstruktur sebagai berikut:

```text
Bank Rekaman Avifauna Indonesia (Xeno-Canto Indonesia, 20 Spesies)
   ↓
Pembersihan, Standardisasi Audio (32 kHz, 5s, RMS 0.05) & Verifikasi Hash SHA-256
   ↓
Partisi Strict Global Recordist-Disjoint
Gallery (674) | Query Clean (310) | Calibration (233)
   ↓
Ekstraksi Representasi Vektor
R0: MFCC | R1: PANNs CNN14 | R2: BirdNET Backbone | R3: Random Control
   ↓
Perhitungan Kesamaan Kosinus L2-Normalized (Cosine Similarity)
   ↓
Pemeringkatan Audio Paling Mirip (Ranking Retrieval)
   ↓
Eksperimen E1: Clean Retrieval Benchmark (Kueri Bersih vs Galeri)
   ↓
Eksperimen E2: Pencampuran Derau Fisik AudioMoth ITERA pada Kueri yang SAMA
SNR +20 dB → SNR +10 dB → SNR 0 dB → SNR -5 dB (Paired Testing)
   ↓
Pengukuran Laju Penurunan Performa & Kurva Retensi Relatif
   ↓
Eksperimen E3: Optimasi & Pembekuan Ambang Batas Open-Set (tau beku via Youden's J)
   ↓
Eksperimen E4: Sensitivitas Profil Spektral Derau Lintas 3 Habitat Kampus ITERA
   ↓
Eksperimen E5: Audit Kasus Kegagalan Terstratifikasi & Uji Bootstrap CI 95%
```

### Tujuh Prinsip Metodologis Kunci dari Pembimbing:
1. **Bank Referensi Burung Terkendali:** Eksperimen dimulai dari kurasi audio burung dengan diversitas perekam tinggi, bukan langsung merekam di lapangan tanpa ground-truth. Partisi galeri, kueri, dan kalibrasi harus *strictly recordist-disjoint* (0 kebocoran author).
2. **Penyelarasan Representasi Audio:** Ketiga model representasi ($R_0, R_1, R_2$) dan kontrol acak ($R_3$) diperlakukan murni sebagai *frozen feature extractors* dengan metrik jarak yang identik (*cosine similarity*). Hal ini memastikan keunggulan performa murni mencerminkan geometri ruang laten representasi, bukan variasi algoritma temu kembali.
3. **Validasi Baseline Bersih (E1):** Pengujian awal dilakukan pada audio bersih untuk membuktikan kewajaran representasi ($R_2 > R_1 > R_0 \gg R_3$). Jika tebakan acak mendekati model terlatih, terdapat kesalahan implementasi atau kebocoran data.
4. **Desain Uji Berpasangan (Paired Query Stress-Testing E2):** Kueri bersih yang sama dicampur dengan derau lapangan AudioMoth ITERA pada grid SNR +20, +10, 0, dan -5 dB. Kita tidak membandingkan audio acak yang berbeda di tiap SNR, melainkan menguji bagaimana sinyal kueri yang identik mengalami pergeseran representasi di bawah peningkatan intensitas derau lingkungan.
5. **Pembekuan Ambang Batas Terbuka (Open-Set Threshold Freeze E3):** Sistem pemantauan bioakustik otonom harus mampu berkata *"tidak ada kecocokan yang meyakinkan"* (menolak audio asing). Ambang batas $\tau^*$ wajib dioptimasi dan dibekukan pada subset kalibrasi independen. Pertanyaan saintifik utamanya: **apakah ambang batas yang ditetapkan pada kondisi bersih tetap stabil ketika intensitas derau meningkat?**
6. **Perbandingan Profil Spektral Habitat (E4):** Karakteristik spektral derau berbeda antara lokasi vegetasi/serangga (Kebun Raya) dengan resonansi angin (Embung F) dan koridor antropogenik (Gedung Terpadu). Eksperimen E4 menguji apakah representasi bioakustik invarian terhadap perbedaan profil spektral ini.
7. **Audit Kegagalan Manusiawi (E5):** Analisis kegagalan tidak boleh berupa teks *template* otomatis, melainkan harus mendiagnosis secara akustik mengapa model gagal (apakah akibat pelemahan energi pada SNR rendah, ambiguitas fitur akustik, atau kolaps total).

> **Inti Pertanyaan Riset:** Penelitian ini bukan mencari *"model mana yang paling akurat pada kondisi ideal"*, melainkan membuktikan *"representasi audio mana yang kehilangan kemampuan diskriminasi bioakustik paling lambat ketika kondisi lingkungan memburuk, dan apakah mekanisme penolakan kelas terbukanya tetap aman diterapkan di dunia nyata."*

---

## 16. Panduan Teknis Lab & Protokol Gate 2–4

### MINGGU 2 (H8–H14) — E2 Controlled Noise Robustness

#### H8 — Pembekuan Mesin Pencampuran SNR & Pembersihan Derau
1. Jalur cadangan pink noise telah dihapus permanen dari `src/mix_noise.py` dan `src/dsic2706/audio/mixing.py`. Jika bank derau kosong atau rusak, fungsi melempar `FileNotFoundError` secara eksplisit.
2. Pemasangan kueri ke segmen derau diimplementasikan secara deterministik menggunakan *fixed seed* (`seed=42`).
3. Bank derau AudioMoth ITERA diisolasi secara ketat: 1.550 berkas dialokasikan untuk partisi pencampuran E2/E4, dan 249 berkas dialokasikan khusus untuk partisi kontrol negatif E3 tanpa tumpang tindih (DEC-14).
4. Uji unit memverifikasi bahwa SNR terukur pada sinyal hasil pencampuran berada dalam toleransi ketat $\pm 0.5\text{ dB}$ terhadap target.
5. Kontrol audio transform (no-op transform) membuktikan bahwa resample 32 kHz dan proses write-read tidak menurunkan mAP secara artifisial.

#### H9 — Pilot Tingkat SNR & Pembekuan Grid
1. Pilot pengujian pada subset kueri memastikan grid SNR tidak mengalami *ceiling* (terlalu mudah) maupun *floor* (kolaps total sebelum -5 dB).
2. Grid dibekukan pada lima level: Clean, +20 dB, +10 dB, 0 dB, dan -5 dB (DEC-05).
3. Kontrol acak $R_3$ terbukti berada jauh di bawah seluruh representasi pada seluruh grid SNR.

#### H10 — Pembekuan Pasangan Derau dan Log Provenans
1. Setiap baris hasil evaluasi mencatat path berkas derau fisik yang digunakan pada kolom `noise_file`, menjamin transparansi asal derau.
2. Manifes pemasangan dibekukan dan diverifikasi ulang dengan hash SHA-256.

#### H11–H12 — Eksekusi Penuh E1 dan E2
1. Menjalankan seluruh kombinasi 4 representasi $\times$ 5 level SNR pada 310 kueri terhadap 674 galeri.
2. Menyimpan pemeringkatan lengkap per kueri di `results/raw/`, bukan hanya metrik agregat.
3. Menyimpan catatan eksekusi teknis (waktu, Git commit SHA, versi library, run_id).

#### H13 — Analisis Kurva Ketahanan
1. Menghasilkan kurva mAP@10, Top-1, dan retensi relatif terhadap SNR.
2. Melaporkan metrik mentah berdampingan dengan rasio retensi untuk mencegah distorsi interpretasi.

#### H14 — Buffer & Verifikasi Gate 2
* Seluruh 1.799 berkas AudioMoth ITERA terverifikasi fisik, lolos uji integritas tanpa manipulasi sintetis.

---

### MINGGU 3 (H15–H21) — E3 Open-Set, E4 Domain Shift, E5 Failure Analysis

#### H15 — Penyusunan Tiga Jenis Kontrol Negatif (Unknown)
Himpunan kontrol negatif open-set disusun terpisah pada `unknown_open_set_manifest.csv`:
| Jenis Unknown | Komposisi Berkas | Tujuan Pengujian |
| :--- | :--- | :--- |
| **(a) Unknown Mirip** | Vokalisasi burung non-target (spesies di luar 20 target) | Menguji daya tolak terhadap taksa yang mirip secara biologis |
| **(b) Unknown Non-Burung** | Biofoni satwa non-aves tropis | Menguji penolakan terhadap suara fauna lingkungan lain |
| **(c) Derau Murni** | Rekaman lingkungan AudioMoth ITERA tanpa burung target | Menguji penolakan terhadap derau antropofoni dan geofoni |

Partisi kalibrasi (498 sampel) dan partisi uji (200 sampel) diisolasi 100% bebas tumpang tindih.

#### H16 — Kalibrasi dan Pembekuan Ambang Batas $\tau^*$
1. Ambang batas $\tau^*$ dioptimasi murni pada subset kalibrasi via Youden's Index ($J = \text{TPR} - \text{FPR}$).
2. Nilai $\tau^*$ resmi dibekukan di `configs/thresholds.yaml`: $\tau^*_{R_2} = 0.7071$, $\tau^*_{R_1} = 0.8974$, $\tau^*_{R_0} = 0.9958$, $\tau^*_{R_3} = 0.4481$.
3. Test set kueri tidak pernah disentuh selama proses penetapan ambang batas (*zero data snooping*).

#### H17 — Evaluasi Transfer Ambang Batas Lintas SNR (E3)
1. Menerapkan $\tau^*$ beku pada kueri uji di seluruh level SNR.
2. Melaporkan FPR dan recall secara terpisah untuk memperlihatkan trade-off konservatif vs permisif.
3. Membuktikan bahwa BirdNET ($R_2$) mempertahankan penolakan aman (FPR turun ke 24.5% pada -5 dB), sedangkan PANNs ($R_1$) mengalami inflasi FPR hingga 64.0%.

#### H18 — Evaluasi Sensitivitas 3 Habitat Lapangan ITERA (E4)
1. Mengevaluasi kueri yang dicampur derau fisik dari 3 habitat kampus ITERA (Kebun Raya, Embung F, Gedung Terpadu).
2. Membandingkan degradasi mAP@10 antar lokasi pada SNR yang sama.
3. Menunjukkan bahwa BirdNET invarian terhadap profil habitat ($p = 0.610$), sementara PANNs sensitif ($p < 0.001$).

#### H19–H20 — Audit Kasus Kegagalan Terstratifikasi (E5)
1. Menyeleksi 30 kasus kegagalan autentik dari data mentah (10 Clean, 20 SNR -5 dB).
2. Menghitung parameter bioakustik fisik langsung dari gelombang audio (*spectral centroid*, *bandwidth*, *margin to tau*, *retrieval gap*).
3. Mengelompokkan kasus ke dalam taksonomi: *Top-1 Confusion Above Tau* (36.67%), *Open-Set False Rejection* (36.67%), dan *Total Retrieval Collapse* (26.67%).

#### H21 — Buffer & Verifikasi Gate 3
* Memastikan seluruh kurva ROC, grafik transfer ambang batas, dan diagram batang sensitivitas habitat telah dihasilkan.

---

### MINGGU 4 (H22–H30) — Statistik Inferensial, Penulisan Naskah, & Reproduksi Segar

#### H22–H23 — Uji Statistik Inferensial Paired Bootstrap
1. Melakukan *paired bootstrap resampling* sebanyak 1.000 iterasi dengan indeks kueri sebagai unit resampling (`seed=42`).
2. Menghitung Confidence Interval 95% dan nilai $p$-value empiris untuk 7 skenario hipotesis.
3. Membuktikan signifikansi statistik keunggulan $R_2$ atas $R_1$ ($p < 0.001$) dan retensi MFCC atas PANNs pada bising ekstrem ($p < 0.001$).

#### H24 — Inventarisasi Tabel dan Gambar Publikasi Bab 4
1. Seluruh 6 tabel publikasi terintegrasi di `paper/tables/`.
2. Seluruh 5 gambar resolusi tinggi terintegrasi di `paper/figures/`.

#### H25–H26 — Penulisan Bab 3, Bab 4, dan Threats to Validity
1. Penggunaan kata "signifikan" secara ketat hanya diterapkan bila didukung oleh CI 95% yang tidak memuat nol.
2. Diskusi eksplisit mengenai risiko kontaminasi pra-latih (*pretraining data contamination*) pada model pondasi.
3. Pengungkapan sidik jari perangkat AudioMoth dan filter pemicu perangkat keras.

#### H27 — Audit Manifes dan Kepatuhan Atribusi
1. Atribusi lengkap seluruh 111 recordist Xeno-Canto di `download_manifest.csv`.
2. Verifikasi ulang hash SHA-256 pada seluruh manifes kanonik.

#### H28 — Reproduksi Segar dari Klon Bersih
1. Menjalankan suite pengujian independen: `python run_tests.py` lolos 10 dari 10 pengujian (100.0%).
2. Memastikan seluruh notebook dieksekusi dari awal hingga akhir tanpa galat.

#### H29 — Pembekuan Repositori (Code & Scope Freeze)
1. Kode program, manifes, konfigurasi, dan tabel hasil dibekukan.
2. Penandaan commit resmi pada repositori Git publik.

#### H30 — Finalisasi Naskah dan Materi Sidang Tugas Akhir
1. Memeriksa konsistensi numerik antara abstrak, metodologi, tabel hasil, dan kesimpulan.

---

### Jalur Minimum Bila Tertinggal (Urutan Prioritas Pengorbanan)

Bila terjadi kendala waktu atau komputasi, urutan pengorbanan ditetapkan di muka untuk menjaga integritas saintifik:

| Prioritas | Komponen | Tindakan Bila Waktu Terbatas |
| :---: | :--- | :--- |
| **1 (Wajib Mutlak)** | E1 Clean Retrieval + E2 Kurva Ketahanan SNR | **Tidak boleh dikorbankan.** Merupakan jawaban inti RQ1 dan RQ2. |
| **2 (Wajib Mutlak)** | Statistik Berpasangan dengan CI 95% | **Tidak boleh dikorbankan.** Tanpa inferensi statistik, klaim keunggulan tidak valid. |
| **3 (Wajib)** | E3 Open-Set dengan $\tau^*$ Beku | Boleh disederhanakan ke unknown jenis derau murni dan non-target aves. |
| **4 (Penting)** | E5 Analisis Kegagalan Terstratifikasi | Pertahankan minimal 20 kasus nyata; jangan menggunakan analisis otomatis template. |
| **5 (Dapat Disesuaikan)** | E4 Sensitivitas Profil Habitat ITERA | Boleh diringkas menjadi perbandingan 2 profil habitat kontras (vegetasi vs antropogenik). |
| **6 (Dapat Dieliminasi)** | E6 Validasi Eksternal (ESC-50 / Non-Avian) | Dieliminasi sejak awal; bersifat opsional dan sekunder. |

> **Prinsip Etika Riset:** Yang tidak boleh dilakukan dalam keadaan apa pun: mengubah grid SNR setelah melihat hasil, mengkalibrasi ulang ambang batas $\tau^*$ pada test set, atau memangkas jumlah kasus audit di bawah ambang batas minimum.

---

### Manajemen Risiko dan Mitigasi

| Risiko Potensial | Dampak Ilmiah | Strategi Mitigasi yang Diterapkan |
| :--- | :--- | :--- |
| **Grid SNR mengalami ceiling atau floor total** | Kurva degradasi tidak informatif | Melakukan pilot test H9 sebelum main run; menetapkan rentang +20 dB s.d. -5 dB. |
| **Bank derau tidak mencukupi untuk seluruh kueri** | Replikasi E2 tidak representatif | Mengumpulkan 1.799 berkas AudioMoth lapangan dari 5 lokasi ITERA (surplus data). |
| **Waktu inferensi ekstraksi embedding lambat** | Eksekusi benchmark terhambat | Menggunakan *batched inference* pada GPU dan menyimpan cache embedding NPZ (`results/features/`). |
| **CI Bootstrap memuat angka nol** | Hipotesis keunggulan tidak terbukti | Melaporkan apa adanya secara objektif; temuan kesetaraan tetap sah secara saintifik. |
| **Kegagalan reproduksi pada klon bersih** | Merusak integritas tugas akhir | Menerapkan suite unit test otomatis (`run_tests.py`) yang memverifikasi 10 gerbang integritas. |
| **Klaim naskah melampaui bukti data** | Temuan audit pembimbing berulang | Mengunci seluruh pernyataan klaim ke tabel metrik mentah dan CI inferensial terproses. |

---

## 17. Register Keputusan (DEC), Checklist Audit, & Catatan Provenans

### Register Keputusan Riset (Decision Register)

| Kode Keputusan | Tanggal | Topik & Parameter | Isi Keputusan Resmi | Justifikasi & Rationale Saintifik |
| :---: | :---: | :--- | :--- | :--- |
| **DEC-01** | 05 Sep 2026 | Sumber Data & Geografis | Menggunakan rekaman wilayah Indonesia dengan metadata lokasi valid. | Mencegah bottleneck data pada area sempit dan menjamin kecukupan volume per taksa. |
| **DEC-02** | 05 Sep 2026 | Ambang Sampel Minimum | Minimal 20 klip bermutu tinggi per spesies target. | Menjamin kecukupan statistik pembagian galeri dan kueri. |
| **DEC-03** | 06 Sep 2026 | Penyesuaian Taksa Tertentu | Menghindari spesies yang terkena proteksi anti-perburuan liar API. | Memastikan 100% berkas audio dapat diunduh secara legal dan berlisensi terbuka. |
| **DEC-04** | 06 Sep 2026 | Metode Ambang Batas Open-Set | Menggunakan Youden's Index ($J$) pada kurva ROC kalibrasi. | Menentukan titik operasi berimbang optimal secara objektif dan non-parametrik. |
| **DEC-05** | 06 Sep 2026 | Grid SNR Eksperimen E2 | Grid resmi: Clean, +20 dB, +10 dB, 0 dB, dan -5 dB. | Mencakup degradasi dari bising ambien ringan hingga bising berat lingkungan tropis. |
| **DEC-06** | 06 Sep 2026 | Strategi Partisi Bebas Bocor | Strict Global Recordist-Disjoint Partition. | Menghilangkan recorder bias; audio perekam yang sama tidak boleh muncul di kueri dan galeri. |
| **DEC-07** | 07 Sep 2026 | Format Normalisasi Sinyal | RMS Normalization dengan target RMS = 0.05 pada jendela 5 detik. | Mencegah kliping amplitudo dan menstandardisasi energi akustik input. |
| **DEC-08** | 07 Sep 2026 | Penundaan Data In-Situ Penuh | Membatasi ruang lingkup pada controlled additive noise AudioMoth. | Menjaga integritas saintifik agar tidak mengklaim deteksi in-situ tanpa bounding box ground-truth. |
| **DEC-09** | 12 Sep 2026 | Pivot Dataset Historis | Rezim eksperimen beralih sementara ke BirdCLEF+ 2026 (arsip). | Menguji pipeline pada skala besar sebelum amandemen fauna lokal. |
| **DEC-10** | 12 Sep 2026 | Kriteria Seleksi 20 Taksa | Memilih 20 spesies dengan diversitas recordist unik tertinggi. | Menjamin ketercukupan partisi recordist-disjoint tanpa kekurangan author independen. |
| **DEC-11** | 12 Sep 2026 | Filter Waktu Perekaman Derau | Memprioritaskan rekaman derau waktu siang pada rezim aktif. | Menyelaraskan profil akustik derau dengan waktu aktivitas harian sebagian besar burung target. |
| **DEC-12** | 12 Sep 2026 | Filter Pemicu AudioMoth | Mencatat filter frekuensi dan amplitudo pada manifes derau. | Menjamin transparansi respons frekuensi perangkat keras perekam AudioMoth. |
| **DEC-13** | 10 Okt 2026 | Pivot Resmi Avifauna Indonesia | Beralih penuh ke 20 spesies Avifauna Kepulauan Indonesia (1.217 klip fisik Xeno-Canto). | Menghilangkan ketidakcocokan biogeografis (spesies tropis Indonesia selaras dengan derau ITERA Sumatera). |
| **DEC-14** | 10 Okt 2026 | Pemisahan Partisi Bank Derau | Mengisolasi 1.550 berkas derau untuk mixing dan 249 berkas untuk open-set unknown, serta mencatat `noise_file`. | Mencegah kontaminasi silang antar eksperimen dan membuktikan penggunaan derau fisik nyata secara traceable. |

---

### Checklist Penutup Audit Pembimbing

- [x] DEC-13 dan DEC-14 tercatat resmi pada `docs/research/decision-log.md` dan `docs/research/scope-freeze.md`.
- [x] Korpus 20 spesies Avifauna Indonesia (1.217 klip) terverifikasi hash SHA-256 pada `download_manifest.csv`.
- [x] Manifes partisi `dataset_split.csv` 100% *recordist-disjoint* (0 author overlap, 0 ID overlap, 0 path overlap).
- [x] Seluruh skrip dan notebook menggunakan modul terpusat di `src/` (tanpa duplikasi logika).
- [x] Fallback pink noise sintetis dihapus permanen; kegagalan berkas melempar `FileNotFoundError`.
- [x] Bank derau fisik AudioMoth ITERA (1.799 berkas) terverifikasi di bawah `data/itera_noise/`.
- [x] Setiap baris hasil evaluasi mentah menyimpan asal derau pada kolom `noise_file`.
- [x] Ambang batas $\tau^*$ dioptimasi pada kalibrasi independen dan dibekukan di `configs/thresholds.yaml`.
- [x] Eksperimen E4 mengevaluasi 3 profil habitat kampus ITERA (Kebun Raya, Embung F, Gedung Terpadu).
- [x] Eksperimen E5 mengaudit 30 kasus kegagalan nyata lintas taksa dengan diagnosis bioakustik manusiawi.
- [x] Uji inferensial Paired Bootstrap 1.000 iterasi dengan CI 95% terlapor lengkap untuk 7 hipotesis.
- [x] Hasil rezim lama BirdCLEF diarsipkan secara aman di `results/archive/birdclef_2026/`.
- [x] Suite pengujian saintifik (`python run_tests.py`) lulus 10 dari 10 pengujian (100.0%).
- [x] Naskah skripsi (`paper/manuscript.md`) dan seluruh dokumentasi sinkron 100% dengan data mentah.

---

### Catatan Provenans Dokumen

Dokumen repositori ini disusun dan disempurnakan berdasarkan arahan dosen pembimbing (Bapak Ardika Satria) dari serangkaian sesi bimbingan dan audit mutu Tugas Akhir (**DSIC-2706**):
1. **Audit Metodologi Pertama:** Penetapan fondasi temu kembali kesamaan bioakustik berbasis representasi beku, penghapusan ketergantungan model klasifikasi tertutup, dan perumusan protokol uji berpasangan (*paired stress-testing*).
2. **Audit Metodologi Kedua (12 September 2026):** Standarisasi prapemrosesan audio, perumusan partisi *strict recordist-disjoint*, dan integrasi bank derau fisik AudioMoth ITERA.
3. **Amandemen Avifauna Indonesia (10 Oktober 2026 / DEC-13 & DEC-14):** Penyelarasan biogeografis korpus audio ke 20 spesies burung kepulauan Indonesia (Xeno-Canto Indonesia, 1.217 berkas audio fisik), penghapusan total dependensi sintetis pink noise, isolasi partisi bank derau 1.799 berkas AudioMoth ITERA, pelacakan provenans derau per kueri (`noise_file`), serta pengarsipan aman hasil rezim lama ke `results/archive/birdclef_2026/`.

Seluruh data, angka metrik, dan tabel yang terdokumentasi dalam repositori ini bersumber murni dari eksekusi komputasional aktual pada berkas audio fisik yang tersimpan di lingkungan riset lokal ITERA.
