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
