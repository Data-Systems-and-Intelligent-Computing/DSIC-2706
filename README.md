# DSIC-2706 — Robust Bioacoustic Similarity Retrieval under Noise and Domain Shift

Repositori penelitian untuk topik **DSIC-2706: Mencari Audio yang Mirip Ketika Datanya Terbatas**.

Fokus penelitian ini bukan membuat classifier spesies baru, melainkan menguji **ketahanan representasi audio untuk similarity retrieval** ketika query mengalami derau lingkungan dan pergeseran domain dari *focal recording* ke *real soundscape*.

Judul kerja artikel yang direkomendasikan:

> **Noise and Domain-Shift Robustness of Audio Representations for Cross-Domain Bioacoustic Retrieval: From Xeno-Canto to Environmental Soundscapes**

**Peneliti:** Fabio Banyu Cyto (NIM: 123450104)  
**Kelompok Riset:** DSIC Research Group — Program Studi Sains Data, Institut Teknologi Sumatera  


---

## Status Progres Penelitian (Terverifikasi)

- [x] **Target Taxon Freeze:** 16 spesies burung representatif Sumatera dibekukan (`configs/datasets.yaml`).
- [x] **Data Integrity Audit:** 416 berkas audio burung + 77 berkas non-burung terverifikasi (0 berkas korup, $\ge 15$ klip/spesies).
- [x] **Leakage-Free Partition:** **Strict Global Recordist-Disjoint Cut** ($\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset$, 42 perekam Gallery vs 29 perekam Query Clean, **0 overlap**).
- [x] **Unit Testing:** 9/9 unit testing lolos 100% (`python run_tests.py`), mencakup integritas hash manifes dan dimensi embedding model deep learning asli.
- [x] **Comparative Benchmark:** $R_0$ (MFCC), $R_1$ (PANNs CNN14 asli 2048-d), $R_2$ (BirdNET V2.4 asli 1024-d), dan $R_3$ (Random Control) melintasi Clean, 20 dB, 10 dB, 0 dB, dan -5 dB tereksekusi penuh.
- [x] **Open-Set Threshold Transfer:** Ambang batas $\tau^*$ terkalibrasi empiris via Youden's $J$ ROC dan dibekukan dengan injeksi derau pada unknown audio ($\Delta\text{FPR} \neq 0$).
- [x] **Reproducibility & Visualisasi:** Deterministik tervalidasi hingga 6 digit desimal, visualisasi dengan 95% Bootstrap CI, dan interaktif notebook resmi di `notebooks/01_evaluasi_benchmark_dan_visualisasi.ipynb`.

---

## 1. Pertanyaan Penelitian

### RQ Utama
**Representasi audio mana yang mempertahankan kualitas similarity retrieval paling baik ketika query bioakustik mengalami peningkatan derau lingkungan dan pergeseran domain dari focal recording ke soundscape?**

### Sub-RQ
1. Seberapa besar penurunan `mAP@k` dan `Recall@k` untuk setiap representasi pada beberapa tingkat SNR yang dibentuk menggunakan background noise ITERA?
2. Apakah threshold kemiripan yang dikalibrasi pada data terpisah tetap mampu menolak *unknown species* dan *background noise* ketika tingkat noise dan domain perekaman berubah?
3. Apakah *bioacoustic-specific embedding* memiliki *robustness retention* yang lebih baik daripada *generic pretrained audio embedding* dan MFCC pada kondisi noise yang sama?
4. Sebagai analisis sekunder, candidate match spesies apa yang muncul pada subset soundscape ITERA yang telah diverifikasi manual?

---

## 2. Hipotesis

- **H1 — Robustness retention:** deep pretrained representation mempertahankan proporsi `mAP@k` yang lebih besar daripada MFCC ketika SNR diturunkan.
- **H2 — Domain-specific advantage:** bioacoustic embedding mengalami penurunan retrieval yang lebih kecil daripada generic audio embedding pada query burung dengan environmental noise.
- **H3 — Domain shift:** kinerja pada real soundscape turun lebih besar daripada controlled mixture pada SNR sebanding karena domain shift tidak hanya berupa additive noise.
- **H4 — Threshold transfer:** threshold yang baik pada calibration-clean tidak selalu stabil ketika kondisi noise berubah.
- **H5 — Positive control:** clean retrieval harus mengungguli random ranking. Jika tidak, pipeline harus diaudit sebelum hasil diinterpretasikan.

---

## 3. Batas Kontribusi

### Kontribusi Ilmiah Utama:
- Evaluasi *paired robustness* pada query yang sama;
- Controlled environmental-noise stress test menggunakan background ITERA;
- Perbandingan hand-crafted, generic pretrained, dan bioacoustic pretrained representation;
- Kurva degradasi retrieval terhadap SNR;
- Pengujian transfer threshold pada open-set condition;
- Validasi eksternal pada real ITERA soundscape.

### Yang BUKAN Kontribusi Utama:
- Membuat model BirdNET/PANNs baru dari nol;
- Fine-tuning banyak model;
- Classifier fauna tertutup baru;
- Occupancy modelling / abundance estimation;
- Inventarisasi biodiversitas kampus secara lengkap;
- Dashboard atau aplikasi produksi.

---

## 4. Representasi yang Dibandingkan

| Kode | Representasi | Dimensi | Peran |
|---|---|:---:|---|
| **R0** | MFCC (20 koefisien) + mean/std pooling | 40-dim | Baseline klasik katalog |
| **R1** | Generic pretrained audio embedding (PANNs CNN14 AudioSet) | 2048-dim | Deep embedding generik |
| **R2** | Bioacoustic pretrained embedding (BirdNET V2.4 Backbone) | 1024-dim | Domain-specific representation |
| **R3** | Random ranking control | 40-dim | Negative control |

Semua representasi utama menggunakan **cosine similarity** agar perbandingan tidak tercampur oleh metrik retrieval yang berbeda.

---

## 5. Ringkasan Hasil Benchmark Komparatif (Terkini)

### A. Kualitas Retrieval (mAP@10) vs Tingkat Derau Lingkungan
| Kondisi Derau (SNR) | $R_0$: MFCC Baseline | $R_1$: Generic Audio (PANNs) | $R_2$: Bioacoustic Pretrained (BirdNET) | $R_3$: Random Control |
| :--- | :---: | :---: | :---: | :---: |
| **Clean** | 0.1029 | 0.2069 | **0.5876** | 0.0209 |
| **SNR 20 dB** | 0.0770 | 0.1890 | **0.5736** | 0.0194 |
| **SNR 10 dB** | 0.0549 | 0.1602 | **0.5561** | 0.0295 |
| **SNR 0 dB** | 0.0409 | 0.0756 | **0.5091** | 0.0236 |
| **SNR -5 dB** | 0.0282 | 0.0438 | **0.4710** | 0.0203 |

### B. Retensi Kualitas Relatif (% terhadap Kondisi Clean)
| Kondisi Derau (SNR) | $R_0$: MFCC Baseline | $R_1$: Generic Audio (PANNs) | $R_2$: Bioacoustic Pretrained (BirdNET) |
| :--- | :---: | :---: | :---: |
| **Clean** | 100.0% | 100.0% | **100.0%** |
| **SNR 20 dB** | 74.8% | 91.4% | **97.6%** |
| **SNR 10 dB** | 53.4% | 77.4% | **94.6%** |
| **SNR 0 dB** | 39.8% | 36.5% | **86.6%** |
| **SNR -5 dB** | 27.4% | 21.2% | **80.1%** |

---

## 6. Struktur Repositori

```text
dsic-2706-bioacoustic-retrieval/
├── README.md
├── .gitignore
├── .env.example
├── pyproject.toml
├── requirements.txt
├── Makefile
├── run_tests.py
│
├── configs/
│   ├── audio.yaml
│   ├── datasets.yaml
│   ├── representations.yaml
│   ├── experiments.yaml
│   └── thresholds.yaml
│
├── docs/
│   ├── research/
│   │   ├── research-charter.md
│   │   ├── rq.md
│   │   ├── hypotheses.md
│   │   ├── novelty-boundary.md
│   │   ├── scope-freeze.md
│   │   └── decision-log.md
│   └── protocols/
│       ├── xeno-canto-selection.md
│       ├── itera-recording.md
│       ├── annotation.md
│       └── open-set.md
│
├── data/
│   ├── README.md
│   ├── manifests/
│   │   ├── target_birds_manifest.csv
│   │   ├── dataset_split.csv
│   │   └── unknown_open_set_manifest.csv
│   ├── xeno_canto/                     (diabaikan oleh git)
│   ├── unknown_open_set/               (diabaikan oleh git)
│   ├── itera_noise/                    (diabaikan oleh git)
│   └── itera_soundscape_annotations/
│
├── src/
│   ├── dsic2706/
│   │   ├── data/
│   │   ├── audio/
│   │   ├── features/
│   │   ├── retrieval/
│   │   ├── open_set/
│   │   ├── evaluation/
│   │   ├── analysis/
│   │   └── utils/
│   └── (backward-compatible scripts)
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── reproducibility/
│
├── experiments/
│   ├── E0_pipeline_sanity/
│   ├── E1_clean_retrieval/
│   ├── E2_noise_robustness/
│   ├── E3_open_set_threshold/
│   ├── E4_real_soundscape/
│   ├── E5_failure_analysis/
│   └── E6_external_validation/
│
├── results/
│   ├── raw/                           (20 file log mentah peringkat per-kueri)
│   ├── processed/                     (snr_robustness, threshold_transfer, failure_analysis)
│   ├── tables/                        (tabel sinkronisasi naskah)
│   └── figures/                       (grafik publikasi 300 DPI dengan 95% CI)
│
├── notebooks/
│   ├── 01_evaluasi_benchmark_dan_visualisasi.ipynb   <- [NOTEBOOK RESMI EVALUASI & AUDIT]
│   └── exploratory/
├── paper/
│   ├── manuscript.md
│   ├── figures/
│   ├── tables/
│   └── bibliography/
└── artifacts/
    └── reproducibility/
```

---

## 7. Quick Start & Eksekusi

```bash
# 1. Instal dependensi resmi
pip install -r requirements.txt

# 2. Menjalankan seluruh pengujian saintifik (9/9 Uji Lolos)
python run_tests.py

# 3. Menjalankan benchmark komparatif empiris (E1, E2, E3, E5)
python src/run_benchmark.py

# 4. Membuka notebook visualisasi interaktif di VS Code / Jupyter
# Buka file: notebooks/01_evaluasi_benchmark_dan_visualisasi.ipynb lalu klik "Run All"

# 5. Menghasilkan ulang figur grafik publikasi (resolusi 300 DPI + 95% Bootstrap CI)
python scripts/make_figures.py
```
