# Catatan Progres Riset & Rekam Jejak Revisi Bimbingan (DSIC-2706)
**Topik:** Mencari Audio yang Mirip Ketika Datanya Terbatas  
**Judul Kerja:** *Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on Indonesian Avifauna with Field-Recorded ITERA Tropical Noise*  
**Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)  
**Dosen Pembimbing:** Bapak Ardika Satria  
**Institusi:** Program Studi Sains Data, Institut Teknologi Sumatera (ITERA)  
**Terakhir Diperbarui:** 10 Oktober 2026 (Penyelesaian Penuh Migrasi Avifauna Indonesia & Gate 1-R s.d. Gate 4: E0 Sanity Check, E1 Clean Benchmark, E2 Noise Degradation, E3 Open-Set Calibration, E4 Habitat Sensitivity, E5 Failure Analysis, dan Uji Statistik Inferensial)  

---

## 📢 LAPORAN PROGRES UTAMA UNTUK DOSEN PEMBIMBING (BAPAK ARDIKA)

> **Yth. Bapak Ardika,**  
> Berikut adalah laporan pertanggungjawaban komprehensif atas penyelesaian seluruh rangkaian eksperimen penelitian Tugas Akhir saya (**DSIC-2706**): *"Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on Indonesian Avifauna with Field-Recorded ITERA Tropical Noise"*. Seluruh tahapan dari **Gate 1-R, Gate 2, Gate 3, hingga Gate 4 telah selesai dieksekusi 100% secara nyata pada dataset Avifauna Indonesia** tanpa manipulasi atau data sintetis. Hasil lama BirdCLEF diarsipkan secara aman di `results/archive/birdclef_2026/`.

### 📌 Ringkasan Capaian yang Telah Dikerjakan & Dihasilkan:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        STATUS RISET MAHASISWA: SELESAI 100%                            │
├──────────────────┬─────────────────────────────────────┬───────────────────────────────┤
│ Komponen Riset   │ Apa yang Telah Dikerjakan Fisik     │ Apa yang Telah Dihasilkan     │
├──────────────────┼─────────────────────────────────────┼───────────────────────────────┤
│ Gate 1-R (E0/E1) │ Standarisasi 1.217 audio Indonesia  │ Tabel E1 Clean Benchmark      │
│                  │ (20 spesies), partisi bebas bocor   │ Top-1: R2 81.61% > R1 37.74%  │
│                  │ 0 author overlap (111 author unik)  │ mAP@10: R2 0.6358 > R1 0.1768 │
├──────────────────┼─────────────────────────────────────┼───────────────────────────────┤
│ Gate 2 (E2)      │ Perekaman 1.799 berkas AudioMoth    │ Tabel E2 & Gambar Kurva SNR   │
│                  │ di 5 titik ITERA, hapus pink noise, │ R2 tahan di -5 dB (retensi    │
│                  │ stress-testing SNR +20 s.d. -5 dB   │ 78.04% / mAP@10 = 0.4962)     │
├──────────────────┼─────────────────────────────────────┼───────────────────────────────┤
│ Gate 3 (E3/E4)   │ Rekonstruksi E3: 233 unknown calib  │ Tabel E3: R2 tau*=0.7071 beku │
│                  │ & 310 unknown test (ITERA + non-tgt)│ (Youden J=0.421, AUROC=0.761) │
│                  │ Uji E4: komparasi 4 representasi    │ Tabel E4: Kebun Raya p=0.0040 │
│                  │ di 3 habitat kampus ITERA           │ R2 ayunan 6.4% vs R1 22.2%    │
├──────────────────┼─────────────────────────────────────┼───────────────────────────────┤
│ Gate 4 (E5/Stat) │ Audit 30 kasus berstrata (Clean     │ Tabel Failure E5 (10 Reject,  │
│                  │ vs -5 dB) lintas taksa burung;      │ 9 Confusion, 11 Collapse)     │
│                  │ Paired Bootstrap 1.000 iterasi      │ Bootstrap 12 uji (p < 0.001)  │
│                  │ estimasi 95% CI performa & retensi  │ 10/10 Unit Test Lulus (100%)  │
└──────────────────┴─────────────────────────────────────┴───────────────────────────────┘
```

### 📂 Inventaris Berkas Resmi Siap Verifikasi:
1. **Tabel Empiris Publikasi Bab 4 (`paper/tables/`):**
   * [`clean_retrieval_table.csv`](../paper/tables/clean_retrieval_table.csv) — Hasil E1 kueri bersih.
   * [`snr_robustness_table.csv`](../paper/tables/snr_robustness_table.csv) — Hasil E2 degradasi derau ITERA (data mentah).
   * [`threshold_transfer_table.csv`](../paper/tables/threshold_transfer_table.csv) — Ambang batas beku kalibrasi $\tau^*$ dan uji transfer open-set dinamis ($N=310$ unknown tested).
   * [`e4_domain_shift_table.csv`](../paper/tables/e4_domain_shift_table.csv) — Hasil komparasi sensitivitas profil spektral 3 habitat kampus ITERA (Kebun Raya, Embung F, Gedung F).
   * [`failure_analysis_table.csv`](../paper/tables/failure_analysis_table.csv) — Audit 30 kasus kegagalan berstrata nyata E5 dengan parameter akustik kuantitatif.
   * [`statistical_significance_table.csv`](../paper/tables/statistical_significance_table.csv) — Uji inferensial bootstrap komparasi model, kontrol acak, dan rentang habitat ($p < 0.001$ s.d. $p = 0.0060$).
2. **Gambar Publikasi Bab 4 (`paper/figures/`):**
   * [`e2_snr_robustness_curve.png`](../paper/figures/e2_snr_robustness_curve.png) — Kurva degradasi akurasi terhadap kebisingan SNR.
   * [`e3_calibration_roc_youden.png`](../paper/figures/e3_calibration_roc_youden.png) — Kurva ROC kalibrasi dan kurva Youden's J E3.
   * [`e3_threshold_transfer_snr.png`](../paper/figures/e3_threshold_transfer_snr.png) — Transfer threshold tau* lintas SNR (AUROC, Recall, FPR).
   * [`e4_noise_profile_sensitivity.png`](../paper/figures/e4_noise_profile_sensitivity.png) — Kurva sensitivitas profil spektral sumber derau E4 vs E2.
   * [`e5_failure_analysis.png`](../paper/figures/e5_failure_analysis.png) — Distribusi moda kegagalan dan parameter akustik E5.
3. **Notebook Interaktif untuk Presentasi Sidang (`notebooks/`):**
   * 8 Notebook kanonikal (`EDA`, `Preprocessing Verification`, `E0`, `E1`, `E2`, `E3`, `E4`, `E5`) yang telah dieksekusi tuntas dengan grafik interaktif.
4. **Naskah & Panduan Skripsi Lengkap:**
   * Draf manuskrip artikel ilmiah: [`paper/manuscript.md`](../paper/manuscript.md) (Menjawab penuh RQ1 s.d. RQ5).
   * Panduan komprehensif naskah Bab 1–5: [`Panduan_Komprehensif_Tugas_Akhir.pdf`](../Panduan_Komprehensif_Tugas_Akhir.pdf).
5. **Suite Uji Saintifik Otomatis (`run_tests.py` & `tests/run_all_tests.py`):**
   * 10/10 unit test saintifik lolos 100% (*Zero Leakage, Filepath Leakage, Author Disjoint, Cosine Properties, SNR Math, Reproducibility, Frozen Tau, Manifest SHA-256, Model Dimensions, Manuscript Consistency*).

---

## Ringkasan Eksekutif & Status Kejujuran Akademis

Dokumen ini adalah **buku catatan progres resmi dan rekam jejak tindak lanjut revisi bimbingan**. Setiap temuan, koreksi, dan arahan dari Pak Ardika dicatat secara kronologis di sini lengkap dengan **tautan berkas `.py`/`.csv`/`.ipynb` yang langsung bisa diklik, bukti hasil eksekusi (*terminal run output*), data numerik empiris, dan visualisasi grafik** tanpa ada manipulasi atau klaim palsu.


> [!IMPORTANT]
> ### Status Kepatuhan & Penyelesaian Menyeluruh (Gate 1-R s.d. Gate 4 — Tuntas 100%):
> 1. **Gate 1-R (Minggu 1) — Tuntas 100%:**
>    * **Pivot Dataset Resmi (DEC-13):** Beralih ke **Avifauna Indonesia (20 spesies burung umum dan tersebar luas di kepulauan Indonesia, 1.217 berkas audio fisik)** untuk menjaga relevansi ekologis dan memenuhi arahan pembimbing.
>    * **Pembekuan Spesies Objektif:** [`data/manifests/species_freeze.csv`](../data/manifests/species_freeze.csv) (20 spesies dengan kriteria DEC-10: hadir di Sumatera, $\ge 30$ klip dan $\ge 14$ perekam di Indonesia) dan [`data/manifests/species_excluded.csv`](../data/manifests/species_excluded.csv) (spesies di luar kuota Top 20).
>    * **Partisi Bebas Bocor (*Strict Author-Disjoint*):** [`data/manifests/dataset_split.csv`](../data/manifests/dataset_split.csv) membagi 674 galeri (60 author), 310 kueri bersih (26 author), dan 233 kalibrasi (25 author). Terbukti **0 overlap ID rekaman, 0 overlap path file, dan 0 overlap author/perekam** (111 author unik global, 100% disjoint).
>    * **Eksekusi E0 & E1:** Lulus penuh pada audio avifauna Indonesia nyata: $R_2$ (BirdNET: **81.61%** / mAP **0.6358**) > $R_1$ (PANNs: **37.74%** / mAP **0.1768**) > $R_0$ (MFCC: **18.06%** / mAP **0.0691**) >> $R_3$ (Random: **6.77%** / mAP **0.0232**).
> 2. **Gate 2 (Minggu 2) — Tuntas 100%:**
>    * **Akuisisi Derau Lapangan AudioMoth ITERA:** Terkumpul **1.799 berkas audio WAV fisik** dari 5 lokasi kampus ITERA (Masjid At-Tanwir, Embung F, Kebun Raya, Gedung F, GKU 1).
>    * **Manifes Kriptografis SHA-256:** [`data/manifests/itera_noise_manifest.csv`](../data/manifests/itera_noise_manifest.csv) memuat 1.799 berkas lengkap dengan checksum SHA-256 dan verifikasi `verified_bird_free: True`.
>    * **Pembersihan Pink Noise & Pemisahan Partisi (DEC-14):** Fungsi fallback derau sintetis dihapus total. Bank derau dipisahkan menjadi 1.528 berkas mixing dan 271 berkas E3 negatives.
>    * **Eksekusi E2 (Paired SNR Stress-Testing):** Pengujian kueri berpasangan pada grid SNR (+20 dB, +10 dB, 0 dB, -5 dB). $R_2$ mempertahankan retensi **78.04%** ($mAP = 0.4962$) pada kondisi ekstrem -5 dB.
> 3. **Gate 3 (Minggu 3) — Tuntas 100%:**
>    * **Kalibrasi Ambang Batas Bebas Bocor ($\tau^*$):** $\tau^*$ dioptimasi via Youden's Index ($J = \text{TPR} - \text{FPR}$) pada subset kalibrasi independen (233 burung target kalibrasi + 233 kontrol negatif unknown: 117 derau ITERA + 116 spesies non-target). Ambang beku: $R_2 = 0.7071$ ($J=0.4206$, AUROC 0.7611), $R_1 = 0.8974$ ($J=0.3734$), $R_0 = 0.9958$, $R_3 = 0.4481$ ([`configs/thresholds.yaml`](../configs/thresholds.yaml)).
>    * **Evaluasi Open-Set E3 Lintas Derau:** Evaluasi pada 310 kueri target berpasangan dengan 310 unknown test disjoint. $R_2$ mempertahankan stabilitas penolakan konservatif dengan FPR menyusut dari 20.00% ke 9.35% ([`notebooks/E3_Open_Set_Threshold.ipynb`](../notebooks/E3_Open_Set_Threshold.ipynb)).
>    * **Evaluasi Sensitivitas Sumber Derau E4:** Pengujian komparatif 4 representasi pada 3 habitat kampus ITERA (Kebun Raya, Embung F, Gedung F). Biofoni serangga Kebun Raya mendegradasi BirdNET ($p=0.0040$), namun rentang ayunan retensi BirdNET (6.42%) jauh lebih stabil dibanding keruntuhan PANNs (22.17%, disparitas ayunan +17.07%, $p=0.0010$) ([`notebooks/E4_Real_Soundscape_Domain_Shift.ipynb`](../notebooks/E4_Real_Soundscape_Domain_Shift.ipynb)).
> 4. **Gate 4 (Minggu 4) — Tuntas 100%:**
>    * **Audit Kasus Kegagalan Berstrata E5:** 30 kasus kegagalan nyata terklasifikasi secara ilmiah di [`paper/tables/failure_analysis_table.csv`](../paper/tables/failure_analysis_table.csv) dan didemonstrasikan di [`notebooks/E5_Failure_Analysis.ipynb`](../notebooks/E5_Failure_Analysis.ipynb). Moda kegagalan terkuantisasi: Open-Set False Rejection (10 kasus, 33.3%), Top-1 Confusion Above Tau (9 kasus, 30.0%), Total Collapse (11 kasus, 36.7%).
>    * **Uji Statistik Inferensial (Bootstrap Resampling):** 1.000 iterasi paired bootstrap resampling membuktikan keunggulan BirdNET atas PANNs signifikan secara statistik ($p < 0.001$).
>    * **Suite Pengujian Saintifik:** 10/10 pengujian lolos 100% pada [`run_tests.py`](../run_tests.py), termasuk verifikasi 1.799 berkas fisik ITERA.

---

## 📋 MATRIKS REKAM JEJAK PENYELESAIAN REVISI & AUDIT

Semua nama berkas di bawah ini berupa **tautan langsung** yang dapat diklik di VS Code / GitHub untuk langsung membuka berkas kode sumber atau data terkait:

| No | Kode Isu | Temuan & Catatan Dosen Pembimbing | Tindakan Koreksi Riil & Eksekusi Lapangan | Berkas Terkait (Klik untuk Buka) | Bukti Hasil Eksekusi (*Run Output*) |
|:---:|:---:|---|---|---|---|
| 1 | **C-01** | **Model $R_2$ tidak memuat bobot BirdNET asli:** Inisialisasi hanya `pass`, yang berjalan adalah ringkasan log-mel 384-d buatan tangan. | Mengunduh bobot resmi BirdNET V2.4 Backbone (ONNX FP32, 1024-d) dan PANNs CNN14 (PyTorch AudioSet, 2048-d). Menghapus seluruh mock log-mel. | • [`checkpoints/BirdNET_GLOBAL_6K_V2.4_Model_FP32.onnx`](../checkpoints/BirdNET_GLOBAL_6K_V2.4_Model_FP32.onnx)<br>• [`src/embeddings.py`](../src/embeddings.py) | **Dimensi Vektor L2-Norm 1.0:**<br>• $R_1$: (2048-d) `PASS`<br>• $R_2$: (1024-d) `PASS` |
| 2 | **C-02** | **Evaluasi open-set cacat ($\Delta\text{FPR} = 0.0$ & $N_{unk}=0$):** Data non-burung tidak ada di split, Youden J tak terhitung karena kalibrasi tanpa kontrol negatif. | Membangun manifes 543 unknown riil (233 kalibrasi + 310 uji) dari derau ITERA & kontrol non-target. Menghitung kurva ROC & Youden J sejati, membekukan $\tau^*$, dan mengevaluasi unknown pada tiap SNR. | • [`data/manifests/unknown_open_set_manifest.csv`](../data/manifests/unknown_open_set_manifest.csv)<br>• [`scripts/run_e3_calibration.py`](../scripts/run_e3_calibration.py)<br>• [`results/processed/threshold_transfer_table.csv`](../results/processed/threshold_transfer_table.csv) | **Metrik Open-Set Riil ($N_{unk}=310$):**<br>• $R_2$: AUROC 0.758 (Clean) $\to$ 0.614 (-5 dB), FPR 20.00% $\to$ 9.35%<br>• $R_1$: FPR 47.42% $\to$ 27.10% |
| 3 | **C-03** | **Tabel kegagalan E5 homogen:** Diagnosis seragam tanpa analisis akustik atau stratifikasi. | Mengimplementasikan sampling berstrata $N=30$ kasus (Clean: 5 $R_2$ + 5 $R_1$; -5 dB: 10 $R_2$ + 10 $R_1$) dengan pengukuran centroid & bandwidth spektral terukur serta margin ke $\tau^*$. | • [`src/analyze_failures.py`](../src/analyze_failures.py)<br>• [`results/processed/failure_analysis_table.csv`](../results/processed/failure_analysis_table.csv)<br>• [`notebooks/E5_Failure_Analysis.ipynb`](../notebooks/E5_Failure_Analysis.ipynb) | **30 Kasus Riil Berstrata:**<br>• Open-Set False Rejection: 10 (33.3%)<br>• Top-1 Confusion > $\tau^*$: 9 (30.0%)<br>• Total Retrieval Collapse: 11 (36.7%) |
| 4 | **M-01** | **Path Windows hardcoded:** Skrip Python memuat path absolut kaku. | Mengubah seluruh path menjadi relatif dinamis berbasis `Path(__file__).resolve().parent.parent` dan POSIX path. | • [`src/preprocess.py`](../src/preprocess.py)<br>• [`src/embeddings.py`](../src/embeddings.py)<br>• [`data/manifests/dataset_split.csv`](../data/manifests/dataset_split.csv) | **Path Portabel Bebas Error** lintas Windows & Linux |
| 5 | **M-02** | **Inkonsistensi takson target:** Masih tertulis data lama. | Memformalkan pembekuan resmi 20 spesies Avifauna Indonesia (Xeno-Canto, 1.217 klip). | • [`docs/research/scope-freeze.md`](../docs/research/scope-freeze.md)<br>• [`data/manifests/species_freeze.csv`](../data/manifests/species_freeze.csv) | **20 Spesies Target Indonesia Terkunci** |
| 6 | **M-03 & m-06** | **Metrik mAP@10 tanpa selang kepercayaan (CI) & grafik tanpa pita galat.** | Menghitung 1.000 iterasi Bootstrap resampling berpasangan pada kueri mentah untuk membentuk CI 95% dan kurva resolusi 300 DPI. | • [`scripts/make_figures.py`](../scripts/make_figures.py)<br>• [`paper/figures/robustness_curve_map10.png`](../paper/figures/robustness_curve_map10.png) | **95% CI Terverifikasi & Grafik Siap Publikasi** |
| 7 | **M-04 & D-03** | **Klaim prematur soundscape ITERA.** | Menyelaraskan peran AudioMoth ITERA murni sebagai bank derau aditif terkontrol (E2) dan negatif latar (E3). E4 diarahkan ke sensitivitas profil spektral lintas 3 habitat kampus ITERA. | • [`paper/manuscript.md`](../paper/manuscript.md)<br>• [`Rencana-eksperimen-bimbingan/minggu-3/README.md`](./minggu-3/README.md) | **Protokol Lapangan Diselaraskan** |
| 8 | **M-06** | **Manifes hash SHA-256 belum mencakup kondisi terkini.** | Menghitung ulang SHA-256 untuk seluruh berkas manifes CSV secara otomatis termasuk download manifest. | • [`scripts/update_manifest_hashes.py`](../scripts/update_manifest_hashes.py)<br>• [`artifacts/reproducibility/manifest_sha256.txt`](../artifacts/reproducibility/manifest_sha256.txt) | **7 Manifes SHA-256 Lolos Validasi Kriptografis** |
| 9 | **DEC-09, DEC-13 & M-10** | **Daya statistik runtuh & derau sintetis.** | **Pivot Resmi:** Beralih ke 20 spesies Avifauna Indonesia (1.217 klip) dan menghapus total derau sintetis pink noise. | • [`docs/research/decision-log.md`](../docs/research/decision-log.md)<br>• [`src/mix_noise.py`](../src/mix_noise.py) | **Galeri: 674, Kueri: 310, Kalibrasi: 233. Pink Noise: Musnah.** |
| 10 | **C-04 & H3.2** | **Kebocoran perekam & penanganan author `Unknown`.** | Menghapus klausa silent-pass, menambahkan asersi pasangan, dan menolak rekaman author Unknown. | • [`tests/test_split_leakage.py`](../tests/test_split_leakage.py)<br>• [`run_tests.py`](../run_tests.py) | **0 ID Overlap, 0 Path Overlap, 0 Author Overlap** |
| 11 | **H6 & Gate 2** | **Akuisisi fisik AudioMoth ITERA.** | **Selesai 100%:** 1.799 berkas WAV fisik terkumpul di `data/itera_noise/` dari 5 titik dan diindeks lengkap dengan checksum SHA-256. | • [`data/itera_noise/`](../data/itera_noise/)<br>• [`data/manifests/itera_noise_manifest.csv`](../data/manifests/itera_noise_manifest.csv) | **1.799 Berkas WAV Terverifikasi Bebas Burung Target** |
| 12 | **Gate 4 Statistik** | **Uji Signifikansi Inferensial (Bootstrap).** | **Selesai 100%:** Paired bootstrap 1.000 iterasi: Clean ($\Delta=+0.4595$, CI $[+0.4246, +0.4940]$, $p < 0.001$), Retensi -5 dB ($\Delta=+0.2214$, CI $[+0.1190, +0.3156]$, $p < 0.001$), Selisih Ayunan Habitat $R_1$ vs $R_2$ ($\Delta=+0.1707$, $p = 0.0010$). | • [`paper/tables/statistical_significance_table.csv`](../paper/tables/statistical_significance_table.csv) | **$p < 0.001$ (Signifikan Mutlak)** |

---

## 🔬 BUKTI HASIL EKSEKUSI EMPIRIS SELURUH GERBANG (GATE 1-R S.D. GATE 4)

---

### 1. BUKTI GATE 1-R: Komposisi Partisi & Hasil E1 Clean Retrieval
* **Komposisi Partisi Data:** 1.217 audio fisik (32.000 Hz, 5.0s, RMS 0.05).
  * Gallery: 674 rekaman (60 author unik)
  * Query Clean: 310 rekaman (26 author unik, 15–16 klip/spesies)
  * Calibration: 233 rekaman (25 author unik)
  * *Leakage:* 0 author overlap, 0 ID overlap, 0 path overlap.
* **Tabel Hasil Empiris E1 Clean Retrieval ([`paper/tables/clean_retrieval_table.csv`](../paper/tables/clean_retrieval_table.csv)):**

| Kode | Representasi Audio | Dimensi | Top-1 Accuracy | mAP@10 | MRR | Precision@10 | Recall@10 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$** | **BirdNET Backbone V2.4** | 1024 | **81.61%** | **0.6358** | **0.8646** | **0.6932** | **0.2311** |
| **$R_1$** | **PANNs CNN14 AudioSet** | 2048 | 37.74% | 0.1768 | 0.5079 | 0.2584 | 0.0839 |
| **$R_0$** | **MFCC Baseline Handcrafted** | 40 | 18.06% | 0.0691 | 0.3081 | 0.1310 | 0.0360 |
| **$R_3$** | **Random Ranking Control** | 40 | 6.77% | 0.0232 | 0.1815 | 0.0603 | 0.0163 |

---

### 2. BUKTI GATE 2: Perekaman Fisik AudioMoth & Hasil E2 Paired Noise Degradation
* **Koleksi Bank Derau:** 1.799 berkas audio WAV AudioMoth dari 5 titik lingkungan kampus ITERA terdaftar di [`data/manifests/itera_noise_manifest.csv`](../data/manifests/itera_noise_manifest.csv) dengan trigger frequency dan amplitude (memenuhi DEC-12).
* **Penghapusan Fallback Sintetis:** `src/mix_noise.py` bebas dari pink noise; memicu `FileNotFoundError` fatal jika data fisik kosong.
* **Tabel Hasil Empiris E2 Degradasi Derau ([`paper/tables/snr_robustness_table.csv`](../paper/tables/snr_robustness_table.csv)):**

| Representasi | Clean | SNR 20 dB | SNR 10 dB | SNR 0 dB | SNR -5 dB | Retensi Relatif (-5 dB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET Backbone)** | **0.6358** | **0.6409** | **0.6202** | **0.5670** | **0.4962** | **78.04%** (CI: 74.0% – 82.1%) |
| **$R_1$ (PANNs CNN14)** | 0.1768 | 0.1963 | 0.1859 | 0.1330 | **0.0982** | **55.53%** (CI: 46.8% – 64.3%) |
| **$R_0$ (MFCC Baseline)** | 0.0691 | 0.0775 | 0.0643 | 0.0369 | **0.0247** | **35.74%** (CI: 27.5% – 44.0%) |
| **$R_3$ (Random Control)** | 0.0232 | 0.0190 | 0.0242 | 0.0214 | 0.0231 | 99.46% (Tebakan Acak) |

*Analisis Kritis:* Pada derau ekstrem SNR -5 dB, BirdNET ($R_2$) mempertahankan retensi 78.04% (mAP = 0.4962), unggul mutlak dibanding PANNs ($R_1$, 55.53%, mAP = 0.0982) dan MFCC ($R_0$, 35.74%, mAP = 0.0247). Paired bootstrap membuktikan keunggulan $R_2$ atas $R_1$ ($\Delta = +0.2214$, $p < 0.001$) dan $R_1$ atas $R_0$ ($\Delta = +0.1987$, $p = 0.0060$). Pada SNR +20 dB, teramati fluktuasi empiris ringan di atas 100% pada semua model akibat efek penghalusan spektral derau latar berdaya sangat rendah.  
*Visualisasi kurva degradasi publikasi: [`paper/figures/e2_snr_robustness_curve.png`](../paper/figures/e2_snr_robustness_curve.png).*

---

### 3. BUKTI GATE 3: Kalibrasi Ambang Batas E3 & Hasil E4 Sensitivitas Sumber Derau
* **Kalibrasi Ambang Batas Bebas Bocor ($\tau^*$):**
  * Dioptimasi secara objektif via kurva ROC empiris & Youden's Index ($J = \text{TPR} - \text{FPR}$) pada subset kalibrasi terpisah ($N=466$: 233 kueri target burung Indonesia + 233 kontrol negatif unknown: 117 derau ITERA + 116 spesies non-target dari [`data/manifests/unknown_open_set_manifest.csv`](../data/manifests/unknown_open_set_manifest.csv)).
  * Nilai ambang batas optimal yang **dibekukan**:
    * $R_2$ (BirdNET): $\tau^* = \mathbf{0.7071}$ (Youden $J = 0.4206$, AUROC = 0.7611, F1 = 0.6650)
    * $R_1$ (PANNs): $\tau^* = \mathbf{0.8974}$ (Youden $J = 0.3734$, AUROC = 0.7141, F1 = 0.7033)
    * $R_0$ (MFCC): $\tau^* = \mathbf{0.9958}$ (Youden $J = 0.0987$, AUROC = 0.5283, F1 = 0.3000)
    * $R_3$ (Random): $\tau^* = \mathbf{0.4481}$ (Youden $J = 0.1202$, AUROC = 0.5662)
* **Tabel Hasil Empiris E3 Evaluasi Open-Set pada Test Set ($N=620$: 310 Kueri Target + 310 Unknown Uji Disjoint — [`paper/tables/threshold_transfer_table.csv`](../paper/tables/threshold_transfer_table.csv)):**

| Model | Kondisi | SNR (dB) | AUROC | AUPRC | Recall@$\tau^*$ | FPR@$\tau^*$ | F1@$\tau^*$ | $\Delta$Recall | $\Delta$FPR |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET)** | Clean | $\infty$ | **0.7582** | **0.7889** | 0.5903 | **0.2000** | **0.6595** | Baseline | Baseline |
| | SNR 20dB | +20 | 0.7569 | 0.7876 | 0.5452 | 0.1613 | 0.6389 | -0.0452 | -0.0387 |
| | SNR 10dB | +10 | 0.7291 | 0.7639 | 0.4774 | 0.1258 | 0.5956 | -0.1129 | -0.0742 |
| | SNR 0dB | 0 | 0.6585 | 0.6977 | 0.3161 | 0.1097 | 0.4434 | -0.2742 | -0.0903 |
| | SNR -5dB | -5 | **0.6141** | **0.6481** | 0.2387 | **0.0935** | 0.3584 | -0.3516 | **-0.1065** |
| **$R_1$ (PANNs)** | Clean | $\infty$ | **0.7459** | **0.7165** | 0.8355 | **0.4742** | **0.7235** | Baseline | Baseline |
| | SNR 20dB | +20 | 0.7500 | 0.7055 | 0.8484 | 0.4774 | 0.7295 | +0.0129 | +0.0032 |
| | SNR 10dB | +10 | 0.7389 | 0.6895 | 0.8000 | 0.4548 | 0.7096 | -0.0355 | -0.0194 |
| | SNR 0dB | 0 | 0.6833 | 0.6544 | 0.6032 | 0.3419 | 0.6202 | -0.2323 | -0.1323 |
| | SNR -5dB | -5 | **0.6286** | **0.6144** | 0.4581 | **0.2710** | 0.5299 | -0.3774 | **-0.2032** |
| **$R_0$ (MFCC)** | Clean | $\infty$ | 0.5467 | 0.5548 | 0.1871 | 0.1387 | 0.2822 | Baseline | Baseline |
| | SNR -5dB | -5 | 0.5669 | 0.5472 | 0.0065 | 0.0129 | 0.0127 | -0.1806 | -0.1258 |
| **$R_3$ (Random)** | Clean | $\infty$ | 0.5181 | 0.5345 | 0.6839 | 0.6548 | 0.5848 | Baseline | Baseline |
| | SNR -5dB | -5 | 0.5218 | 0.5116 | 0.6613 | 0.6355 | 0.5758 | -0.0226 | -0.0194 |

* **Tabel Hasil Empiris E4 Sensitivitas Profil Spektral 3 Habitat Kampus ITERA ([`paper/tables/e4_domain_shift_table.csv`](../paper/tables/e4_domain_shift_table.csv)):**

| Model | Habitat Derau | Kondisi | SNR (dB) | mAP@10 | Top-1 Accuracy (%) | Retensi Relatif |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET)** | Baseline Clean | Clean | $\infty$ | **0.6358** | **81.61%** | 100.0% |
| | Kebun Raya | SNR -5 dB | -5 | **0.4434** | **59.68%** | **69.73%** |
| | Embung F | SNR -5 dB | -5 | **0.4842** | **62.58%** | **76.15%** |
| | Gedung F | SNR -5 dB | -5 | **0.4661** | **64.52%** | **73.30%** |
| **$R_1$ (PANNs)** | Baseline Clean | Clean | $\infty$ | **0.1768** | **37.74%** | 100.0% |
| | Kebun Raya | SNR -5 dB | -5 | **0.0590** | **13.23%** | **33.38%** |
| | Embung F | SNR -5 dB | -5 | **0.0949** | **24.52%** | **53.69%** |
| | Gedung F | SNR -5 dB | -5 | **0.0982** | **22.26%** | **55.55%** |
| **$R_0$ (MFCC)** | Baseline Clean | Clean | $\infty$ | **0.0691** | **18.06%** | 100.0% |
| | Kebun Raya | SNR -5 dB | -5 | **0.0228** | **6.45%** | **33.01%** |
| | Embung F | SNR -5 dB | -5 | **0.0263** | **7.10%** | **38.00%** |
| | Gedung F | SNR -5 dB | -5 | **0.0188** | **4.19%** | **27.24%** |

*Analisis Kritis E4:* Biofoni serangga Kebun Raya (2–6 kHz) mendegradasi BirdNET paling signifikan (retensi 69.73% vs 76.15% di Embung F, $p=0.0040$). Meskipun demikian, rentang ayunan retensi BirdNET lintas ketiga habitat hanya 6.42%, jauh lebih stabil dan kokoh dibandingkan keruntuhan rentang ayunan PANNs sebesar 22.17% (selisih ayunan +17.07%, $p=0.0010$).  
*Demonstrasi interaktif:* [`notebooks/E3_Open_Set_Threshold.ipynb`](../notebooks/E3_Open_Set_Threshold.ipynb) dan [`notebooks/E4_Real_Soundscape_Domain_Shift.ipynb`](../notebooks/E4_Real_Soundscape_Domain_Shift.ipynb).  
*Visualisasi grafik publikasi:* [`paper/figures/e3_threshold_transfer_snr.png`](../paper/figures/e3_threshold_transfer_snr.png) & [`paper/figures/e4_noise_profile_sensitivity.png`](../paper/figures/e4_noise_profile_sensitivity.png).

---

### 4. BUKTI GATE 4: Audit Kegagalan Terstratifikasi Lintas Spesies E5 & Uji Statistik Inferensial Bootstrap
* **Audit Kegagalan Terstratifikasi Lintas Spesies E5 ([`paper/tables/failure_analysis_table.csv`](../paper/tables/failure_analysis_table.csv)):**
  * Membedah 30 kasus kueri gagal nyata terstratifikasi acak dari 17 taksa burung Indonesia: 10 kasus Clean dan 20 kasus SNR -5 dB.
  * Kuantisasi moda kegagalan: **Open-Set False Rejection (10 kasus / 33.33%)**, **Top-1 Confusion Above Tau (9 kasus / 30.00%)**, dan **Total Retrieval Collapse (11 kasus / 36.67%)**.
  * Demonstrasi interaktif: [`notebooks/E5_Failure_Analysis.ipynb`](../notebooks/E5_Failure_Analysis.ipynb) dan grafik [`paper/figures/e5_failure_analysis.png`](../paper/figures/e5_failure_analysis.png).
* **Hasil Uji Statistik Inferensial (Paired Bootstrap 1.000 Iterasi — [`paper/tables/statistical_significance_table.csv`](../paper/tables/statistical_significance_table.csv)):**

| Pengujian | Komparasi Model | Mean Difference | 95% Confidence Interval (CI) | $p$-value Empiris | Signifikan ($\alpha=0.05$) | Kesimpulan Hipotesis |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_1$ (PANNs) | **+0.4595** | **[+0.4246, +0.4940]** | **$p < 0.001$** | Ya | H5 Terpenuhi Mutlak: BirdNET unggul atas PANNs |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_0$ (MFCC) | **+0.5668** | **[+0.5289, +0.6039]** | **$p < 0.001$** | Ya | $R_2$ melampaui baseline klasik MFCC |
| **Clean Retrieval (mAP@10)** | $R_1$ (PANNs) vs $R_0$ (MFCC) | **+0.1074** | **[+0.0834, +0.1304]** | **$p < 0.001$** | Ya | $R_1$ unggul atas MFCC pada kondisi bersih |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_3$ (Random) | **+0.6124** | **[+0.5760, +0.6504]** | **$p < 0.001$** | Ya | H5 Terpenuhi: $R_2$ unggul mutlak atas kontrol acak |
| **Clean Retrieval (mAP@10)** | $R_1$ (PANNs) vs $R_3$ (Random) | **+0.1531** | **[+0.1300, +0.1782]** | **$p < 0.001$** | Ya | H5 Terpenuhi: $R_1$ unggul atas kontrol acak |
| **Clean Retrieval (mAP@10)** | $R_0$ (MFCC) vs $R_3$ (Random) | **+0.0460** | **[+0.0349, +0.0583]** | **$p < 0.001$** | Ya | H5 Terpenuhi: $R_0$ unggul atas kontrol acak |
| **Retensi Relatif SNR -5 dB** | $R_2$ (BirdNET) vs $R_1$ (PANNs) | **+0.2214** | **[+0.1190, +0.3156]** | **$p < 0.001$** | Ya | H1 Terpenuhi: Retensi $R_2$ (78.0%) unggul atas $R_1$ (55.5%) |
| **Retensi Relatif SNR -5 dB** | $R_1$ (PANNs) vs $R_0$ (MFCC) | **+0.1987** | **[+0.0598, +0.3321]** | **$p = 0.0060$** | Ya | Retensi $R_1$ (55.5%) unggul atas MFCC (35.7%) |
| **Retensi Relatif SNR -5 dB** | $R_2$ (BirdNET) vs $R_0$ (MFCC) | **+0.4201** | **[+0.2990, +0.5202]** | **$p < 0.001$** | Ya | Retensi $R_2$ unggul mutlak atas MFCC baseline |
| **Sensitivitas Habitat E4 (-5 dB)** | $R_2$ (Embung F vs Kebun Raya) | **+0.0400** | **[+0.0134, +0.0667]** | **$p = 0.0040$** | Ya | Biofoni serangga Kebun Raya mendegradasi BirdNET lebih parah |
| **Sensitivitas Habitat E4 (-5 dB)** | $R_2$ (Gedung F vs Kebun Raya) | **+0.0220** | **[-0.0029, +0.0456]** | **$p = 0.0700$** | Tidak | Derau struktural gedung berdampak serupa dengan biofoni |
| **Sensitivitas Habitat E4 (-5 dB)** | $R_1$ (Embung F vs Kebun Raya) | **+0.0361** | **[+0.0190, +0.0528]** | **$p < 0.001$** | Ya | PANNs sangat rentan terhadap biofoni Kebun Raya |
| **Sensitivitas Habitat E4 (-5 dB)** | $R_1$ (Gedung F vs Kebun Raya) | **+0.0393** | **[+0.0212, +0.0585]** | **$p < 0.001$** | Ya | PANNs lebih tahan derau gedung dibanding biofoni serangga |
| **Fluktuasi Rentang Habitat (-5 dB)** | $R_1$ vs $R_2$ (Selisih Ayunan Retensi) | **+0.1707** | **[+0.0743, +0.2767]** | **$p = 0.0010$** | Ya | H3 Terdukung Parsial: $R_1$ (ayunan 22.2%) secara signifikan lebih rentan dibanding $R_2$ (ayunan 6.4%) |
| **Cluster Bootstrap (per Recordist, K=26)** | $R_2$ vs $R_1$ Retensi Relatif (-5 dB) | **+0.2273** | **[+0.1445, +0.3306]** | **$p < 0.001$** | Ya | Resampling klaster perekam membuktikan keunggulan $R_2$ bebas bias |
| **Sensitivitas Non-Mike Nelson (N=179)** | $R_2$ vs $R_1$ Retensi Relatif (-5 dB) | **+0.2445** | **[+0.1153, +0.3629]** | **$p < 0.001$** | Ya | Keunggulan $R_2$ tetap signifikan tanpa perekam dominan (42%) |

---

## 🧪 BUKTI EKSEKUSI SUITE PENGUJIAN INTEGRITAS (10/10 PASS 100%)

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
  [PASS] Model Embedding Dimension Compliance (C-01)
  [PASS] Manuscript & Table Numeric Consistency (100% Match)
================================================================================
[+] HASIL: 10/10 Pengujian Lolos (100.0%)
================================================================================
```

---

## 📓 BUKTI JUPYTER NOTEBOOK RESMI KANONIKAL DI `notebooks/`

Seluruh alur kerja eksperimen dapat dijalankan ulang secara interaktif pada 8 notebook resmi berikut:
1. [`notebooks/EDA_Tugas_Akhir.ipynb`](../notebooks/EDA_Tugas_Akhir.ipynb) — Eksplorasi geospasial avifauna Indonesia dan verifikasi kriteria inklusi DEC-10.
2. [`notebooks/Preprocessing Verification.ipynb`](../notebooks/Preprocessing%20Verification.ipynb) — Validasi pemotongan sinyal 5s dan normalisasi RMS 0.05.
3. [`notebooks/E0_Pipeline_Sanity_Check.ipynb`](../notebooks/E0_Pipeline_Sanity_Check.ipynb) — Gerbang anti-kebocoran data dan smoke test representasi.
4. [`notebooks/E1_Clean_Retrieval.ipynb`](../notebooks/E1_Clean_Retrieval.ipynb) — Ekstraksi embedding lengkap dan tolok ukur temu kembali bersih.
5. [`notebooks/E2_Paired_Noise_Degradation.ipynb`](../notebooks/E2_Paired_Noise_Degradation.ipynb) — Demonstrasi pencampuran derau aditif nyata AudioMoth ITERA pada grid SNR.
6. [`notebooks/E3_Open_Set_Threshold.ipynb`](../notebooks/E3_Open_Set_Threshold.ipynb) — Kalibrasi Youden J objektif dan evaluasi transfer ambang batas beku.
7. [`notebooks/E4_Real_Soundscape_Domain_Shift.ipynb`](../notebooks/E4_Real_Soundscape_Domain_Shift.ipynb) — Uji komparasi sensitivitas profil spektral sumber derau lintas 3 habitat kampus ITERA.
8. [`notebooks/E5_Failure_Analysis.ipynb`](../notebooks/E5_Failure_Analysis.ipynb) — Audit dan visualisasi diagnostik 30 kasus kegagalan retrieval berstrata.

---

## 🎯 KESIMPULAN KESIAPAN SIDANG SKRIPSI

1. **Seluruh Eksperimen Teknis Selesai 100%:** E0, E1, E2, E3, E4, E5, dan Uji Statistik Inferensial Bootstrap telah selesai dieksekusi secara nyata tanpa data sintetis.
2. **Kesiapan Naskah Skripsi:** Seluruh 6 tabel resmi telah terisi di `paper/tables/`, seluruh grafik publikasi tersedia di `paper/figures/`, dan draf artikel ilmiah lengkap telah diselaraskan di `paper/manuscript.md` serta `Panduan_Komprehensif_Tugas_Akhir.pdf`.
3. **Status Repositori:** Terkunci penuh (*Code Freeze*), bersih, deterministik (`seed=42`), dan tersinkronisasi 100% antara lokal dan remote GitHub.
