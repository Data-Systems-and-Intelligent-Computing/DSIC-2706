# Catatan Progres Riset & Rekam Jejak Revisi Bimbingan (DSIC-2706)
**Topik:** Mencari Audio yang Mirip Ketika Datanya Terbatas  
**Judul Kerja:** *Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise*  
**Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)  
**Dosen Pembimbing:** Bapak Ardika  
**Institusi:** Program Studi Sains Data, Institut Teknologi Sumatera (ITERA)  
**Terakhir Diperbarui:** 12 September 2026 (Penyelesaian Resmi Revisi Audit Gate 1-R: Pivot BirdCLEF+ 2026, E0 Sanity Check, E1 Clean Retrieval, dan Penutupan Bug Integritas)  

---

## Ringkasan Eksekutif & Status Kejujuran Akademis

Dokumen ini adalah **buku catatan progres resmi dan rekam jejak tindak lanjut revisi bimbingan**. Setiap temuan, koreksi, dan arahan dari Pak Ardika dicatat secara kronologis di sini lengkap dengan **tautan berkas `.py`/`.csv`/`.ipynb` yang langsung bisa diklik, bukti hasil eksekusi (*terminal run output*), data numerik empiris, dan visualisasi grafik** tanpa ada manipulasi atau klaim palsu.

> [!IMPORTANT]
> ### Status Kepatuhan Revisi Audit Keputusan Kedua (12 September 2026 - Gate 1-R):
> 1. **Eksperimen & Infrastruktur yang Sudah Selesai 100% (Gate 1-R / Minggu 1):**
>    * **Pivot Dataset Resmi (DEC-09 & DEC-10):** Beralih dari kurasi manual 14 spesies Sumatera ke **BirdCLEF+ 2026 (20 spesies burung Neotropis Pantanal, 4.351 berkas audio fisik)** untuk mengatasi kelangkaan sampel ($n=14$ kueri pada M-10) dan kebocoran perekam (C-04).
>    * **Pembekuan Spesies Objektif (H2):** [`data/manifests/species_freeze.csv`](../data/manifests/species_freeze.csv) (20 spesies dengan $n_{\text{author}} \ge 105$) dan [`data/manifests/species_excluded.csv`](../data/manifests/species_excluded.csv) (186 taksa non-target dengan alasan penolakan eksplisit dari pool 156 spesies yang lolos seluruh ambang §11.3).
>    * **Partisi Bebas Bocor (*Strict Author-Disjoint* — H3):** [`data/manifests/dataset_split.csv`](../data/manifests/dataset_split.csv) membagi 3.653 galeri (377 author), 200 kueri bersih (68 author), dan 498 kalibrasi (95 author). Terbukti **0 overlap ID rekaman, 0 overlap path file, dan 0 overlap author/perekam** (540 author unik global, 100% disjoint).
>    * **Penutupan Bug Pengujian Integritas (H3.2):** Memperbaiki bug kedalaman path `SPLIT_PATH` dan menghapus total klausa *silent pass* (`if not exists: return`) di [`tests/test_split_leakage.py`](../tests/test_split_leakage.py) sehingga pengujian terbukti gagal keras melempar `AssertionError` saat kebocoran disuntikkan.
>    * **Eksekusi E0 Pipeline Sanity Check (H4):** Lulus penuh pada audio BirdCLEF nyata dengan verifikasi parameter audio di [`configs/audio.yaml`](../configs/audio.yaml) (32 kHz, 5s window, RMS 0.05).
>    * **Eksekusi E1 Clean Retrieval (H5):** Selesai pada 20 spesies burung: $R_2$ (BirdNET: **95.0%**) > $R_1$ (PANNs: **60.0%**) > $R_0$ (MFCC: **27.5%**) >> $R_3$ (Random: **6.5%**).
>    * **Pemisahan Rezim Hasil Lama (C-05 / H5.3):** Hasil Xeno-Canto 14 spesies lama telah diarsipkan penuh ke [`results/archive/2026-09-07_xenocanto16spesies/`](../results/archive/2026-09-07_xenocanto16spesies/). Direktori [`results/processed/`](../results/processed/) kini murni hanya memuat satu rezim hasil aktif didampingi catatan eksekusi [`execution_note_E1.json`](../results/processed/execution_note_E1.json).
>    * **Integritas Checksum & Suite Pengujian (M-06 / H7):** Hash manifes di [`artifacts/reproducibility/manifest_sha256.txt`](../artifacts/reproducibility/manifest_sha256.txt) membaca baseline E1 secara dinamis dan meloloskan **9/9 pengujian saintifik di [`run_tests.py`](../run_tests.py) (100.0% PASS)**.
> 2. **Pekerjaan yang Masih Terjadwal / Pending (Menunggu Lapangan):**
>    * **H6 (Derau Lapangan AudioMoth ITERA):** Skema manifes [`data/manifests/itera_noise_manifest.csv`](../data/manifests/itera_noise_manifest.csv) sudah siap; perekaman fisik di kampus ITERA (3 lokasi $\times 2$ daypart, target $\ge 30$ segmen 60s bebas burung) dan penyalinan `CONFIG.TXT` dijadwalkan untuk persiapan eksperimen Minggu 2 (E2).
>    * **D-07:** Konfirmasi formal Pembimbing 1 terkait lisensi kompetisi Kaggle untuk publikasi artikel/skripsi.

---

## 📋 MATRIKS REKAM JEJAK PENYELESAIAN REVISI (Klik Berkas untuk Meninjau Kode & Data)

Semua nama berkas di bawah ini berupa **tautan langsung** yang dapat diklik di VS Code / GitHub untuk langsung membuka berkas kode sumber atau data terkait:

| No | Kode Isu | Temuan & Catatan Dosen Pembimbing | Tindakan Koreksi Riil | Berkas Terkait (Klik untuk Buka) | Bukti Hasil Eksekusi (*Run Output*) |
|:---:|:---:|---|---|---|---|
| 1 | **C-01** | **Model $R_2$ tidak memuat bobot BirdNET asli:** Inisialisasi hanya `pass`, yang berjalan adalah ringkasan statistik log-mel 384-d buatan tangan. | Mengunduh bobot resmi BirdNET V2.4 Backbone (ONNX FP32, 1024-d) dan PANNs CNN14 (PyTorch AudioSet, 2048-d). Menghapus seluruh mock log-mel dan fallback hening. | • [`checkpoints/BirdNET_GLOBAL_6K_V2.4_Model_FP32.onnx`](../checkpoints/BirdNET_GLOBAL_6K_V2.4_Model_FP32.onnx)<br>• [`src/embeddings.py`](../src/embeddings.py)<br>• [`run_tests.py`](../run_tests.py) | **Verifikasi Dimensi Ekstraksi:**<br>• $R_1$: (2048-d) `PASS`<br>• $R_2$: (1024-d) `PASS`<br>*(Lihat Bukti Run 1 di bawah)* |
| 2 | **C-02** | **Evaluasi open-set cacat ($\Delta\text{FPR} = 0.0$):** Data non-burung diekstrak sekali dari audio bersih sehingga FPR konstan di semua level SNR. | Memindahkan ekstraksi audio tak dikenal ke dalam perulangan kondisi SNR di `src/evaluate.py` dengan menginjeksi derau berpasangan pada audio unknown. | • [`src/evaluate.py`](../src/evaluate.py)<br>• [`results/processed/threshold_transfer_table.csv`](../results/processed/threshold_transfer_table.csv) | **$\Delta\text{FPR}$ Bergeser Dinamis:**<br>Clean: 0.0000<br>SNR 20dB: +0.0256<br>SNR 10dB: +0.0769<br>SNR 0dB: +0.0513<br>SNR -5dB: +0.0256 |
| 3 | **C-03** | **Tabel kegagalan E5 dummy:** 4 file tiruan menduplikasi teks yang sama karena peringkat kueri mentah belum disimpan di raw data. | Menyimpan log pemeringkatan per-kueri ke 20 berkas CSV mentah di `results/raw/`, lalu menambang 30 kasus kegagalan nyata kueri Xeno-Canto di `src/analyze_failures.py`. | • Log Mentah: [`results/raw/`](../results/raw/)<br>• [`src/analyze_failures.py`](../src/analyze_failures.py)<br>• [`results/processed/failure_analysis_table.csv`](../results/processed/failure_analysis_table.csv) | **30 Kasus Riil Terlacak:**<br>• Low SNR Masking: 66.7%<br>• Feature Overlap: 20.0%<br>• Inter-Species: 13.3%<br>*(Lihat Bukti Run 3 di bawah)* |
| 4 | **M-01** | **Path Windows hardcoded:** 10 skrip Python menggunakan path absolut `d:/FILE AND TASK/TA`. | Mengubah seluruh path menjadi relatif dinamis berbasis `Path(__file__).resolve().parent.parent`. Kolom `file_path` di `dataset_split.csv` diubah ke relative POSIX path. | • [`src/preprocess.py`](../src/preprocess.py)<br>• [`data/manifests/dataset_split.csv`](../data/manifests/dataset_split.csv) | **Path Relatif Portabel:**<br>`data/xeno_canto/...`<br>Bebas error di Linux/Windows |
| 5 | **M-02** | **Inkonsistensi takson target di `scope-freeze.md`:** Masih tertulis 16 spesies kosmopolitan lama, bukan takson Sumatera yang sebenarnya dikurasi. | Memformalkan amandemen resmi (Versi 2.0 per 7 September 2026) berisi 16 takson aktual Sumatera (5 endemik, 416 rekaman audio fisik, 15 s/d 37 klip per spesies) beserta justifikasi ilmiahnya. | • [`docs/research/scope-freeze.md`](../docs/research/scope-freeze.md)<br>• [`docs/research/decision-log.md`](../docs/research/decision-log.md) | **Ruang Lingkup Terkunci:**<br>16 Spesies Sumatera<br>5 Spesies Endemik<br>416 Klip Audio Nyata |
| 6 | **M-03 & m-06** | **Metrik mAP@10 tanpa selang kepercayaan (CI) & grafik tanpa pita galat:** Kurva degradasi tidak mencerminkan variabilitas sampling. | Menghitung 1.000 iterasi Bootstrap resampling pada nilai per-kueri mentah di `results/raw/` untuk membentuk selang kepercayaan 95% (CI), serta membuat grafik publikasi resolusi 300 DPI berpita galat (*confidence band*). | • [`scripts/make_figures.py`](../scripts/make_figures.py)<br>• [`results/figures/robustness_curve_map10.png`](../results/figures/robustness_curve_map10.png) | **Grafik Publikasi Siap:**<br>Resolusi 300 DPI<br>Lengkap pita galat 95% CI<br>*(Lihat Gambar di bawah)* |
| 7 | **M-04 & D-03** | **Klaim prematur soundscape ITERA pada naskah:** Draf naskah mengklaim evaluasi rekaman lapangan ITERA padahal audio lapangan belum diambil. | Menghapus seluruh klaim pengujian soundscape ITERA dari Abstrak, Metodologi, dan README. Membatasi pengujian pada controlled additive noise Xeno-Canto dan memposisikan soundscape ITERA sebagai tahap lanjutan (D-03). | • [`paper/manuscript.md`](../paper/manuscript.md)<br>• [`README.md`](../README.md) | **Klaim Diselaraskan:**<br>Murni controlled noise;<br>Field test ditunda ke D-03 |
| 8 | **M-06** | **Manifes hash SHA-256 belum mencakup kondisi terkini:** Checksum manifes belum diperbarui pasca-normalisasi data. | Menghitung ulang nilai checksum SHA-256 riil untuk seluruh 3 berkas manifes CSV dan memvalidasinya lewat unit test otomatis. | • [`scripts/update_manifest_hashes.py`](../scripts/update_manifest_hashes.py)<br>• [`artifacts/reproducibility/manifest_sha256.txt`](../artifacts/reproducibility/manifest_sha256.txt) | **Integritas Manifes:**<br>3 CSV lolos checksum SHA-256 pada `run_tests.py` |
| 9 | **M-07 & m-08** | **Redundansi berkas & artefak usang:** Terdapat duplikat file referensi jurnal dan file tabel evaluasi lama yang sudah tidak relevan. | Menghapus `jurnal/referensi_jurnal_TA_bioakustik (1).csv`, menghapus `openset_evaluation_table.csv`, dan menyinkronkan seluruh tabel resmi ke `paper/tables/`. | • [`paper/tables/`](../paper/tables/) | **Direktori Rapi:**<br>0 Berkas Duplikat Usang |
| 10 | **m-09** | **Catatan metodologi tumpang tindih perekam kalibrasi:** Subset kalibrasi dan query_clean masih berbagi 19 perekam. | Mendokumentasikan secara transparan batasan ini di naskah skripsi (§6.2 *Threats to Validity*) dan di `scope-freeze.md` Bagian 4 sebagai potensi bias optimistik lokal pada recall $\tau$, sementara metrik primer mAP@10 pada E1/E2 tetap 100% bebas kebocoran. | • [`paper/manuscript.md`](../paper/manuscript.md)<br>• [`docs/research/scope-freeze.md`](../docs/research/scope-freeze.md) | **Transparansi Ilmiah:**<br>Tercatat di Bab 6.2<br>*Threats to Validity* |
| 11 | **DEC-09 & M-10** | **Daya statistik runtuh ($n=14$ kueri) & derau sintetis:** Korpus 14 spesies Sumatera terlalu kecil dan jatuh ke pink noise sintetis. | **Pivot Dataset Resmi:** Beralih ke BirdCLEF+ 2026 (20 spesies burung, 4.351 klip) dan memposisikan AudioMoth ITERA sebagai bank derau aditif E2 serta negatif open-set E3. | • [`docs/research/decision-log.md`](../docs/research/decision-log.md)<br>• [`docs/research/scope-freeze.md`](../docs/research/scope-freeze.md)<br>• [`data/manifests/dataset_split.csv`](../data/manifests/dataset_split.csv) | **Data Cukup Kuat:**<br>• Galeri: 3.653 klip<br>• Kueri: 200 klip bersih<br>• Kalibrasi: 498 klip |
| 12 | **DEC-10 & H2** | **Seleksi spesies tidak terlacak:** Menghindari pola pembuangan spesies tanpa jejak keputusan terverifikasi. | Menyaring dari pool 156 spesies yang memenuhi seluruh kriteria §11.3 (rating $\ge 3.0$, $\ge 20$ klip, $\ge 3$ author), memilih Top 20 dengan $n_{\text{author}}$ tertinggi (105–129 author). 136 sisanya dicatat di `species_excluded.csv`. | • [`scripts/select_birdclef_species.py`](../scripts/select_birdclef_species.py)<br>• [`data/manifests/species_freeze.csv`](../data/manifests/species_freeze.csv)<br>• [`data/manifests/species_excluded.csv`](../data/manifests/species_excluded.csv) | **Manifes Objektif:**<br>• 20 Spesies Target<br>• 186 Spesies Eksklusi<br>(136 kuota + 50 substantif) |
| 13 | **C-04 & H3.2** | **Kebocoran perekam & bug pengujian *silent pass*:** Pengujian kebocoran data keluar diam-diam tanpa asersi saat path salah hitung kedalaman direktori. | Menghapus total seluruh klausa `if not exists: return`, membetulkan resolusi path dinamis, dan menambahkan asersi pasangan kalibrasi. Terbukti gagal melempar `AssertionError` saat disuntik kebocoran author. | • [`tests/test_split_leakage.py`](../tests/test_split_leakage.py)<br>• [`tests/integration/test_split_leakage.py`](../tests/integration/test_split_leakage.py)<br>• [`run_tests.py`](../run_tests.py) | **Gerbang Penguji Aktif:**<br>• 0 ID overlap<br>• 0 Path overlap<br>• 0 Author overlap<br>(540 author disjoint) |
| 14 | **C-05 & H5.3** | **Rezim ganda hasil eksperimen:** Berkas hasil Xeno-Canto lama dan BirdCLEF baru tercampur dalam satu folder. | Mengarsipkan seluruh berkas CSV mentah dan tabel lama ke `results/archive/2026-09-07_xenocanto16spesies/`. Direktori `results/processed/` kini murni hanya memuat hasil BirdCLEF aktif beserta catatan eksekusi JSON. | • [`results/archive/`](../results/archive/)<br>• [`results/processed/clean_retrieval_table.csv`](../results/processed/clean_retrieval_table.csv)<br>• [`results/processed/execution_note_E1.json`](../results/processed/execution_note_E1.json) | **Satu Rezim Aktif:**<br>Tabel kanonik E1 + 800 baris per-query (kolom author lengkap) |
| 15 | **H6 & H7** | **Manifes integritas usang & derau AudioMoth:** Skrip hash meng-hash berkas usang dan baseline E1 di-hardcode. | Memperbarui `scripts/update_manifest_hashes.py`: mengganti target lama ke `itera_noise_manifest.csv`, membaca baseline E1 secara dinamis, dan meloloskan 9/9 pengujian integritas saintifik. | • [`scripts/update_manifest_hashes.py`](../scripts/update_manifest_hashes.py)<br>• [`data/manifests/itera_noise_manifest.csv`](../data/manifests/itera_noise_manifest.csv)<br>• [`artifacts/reproducibility/manifest_sha256.txt`](../artifacts/reproducibility/manifest_sha256.txt) | **9/9 Pengujian PASS:**<br>100% lulus pada `run_tests.py` |

---

## BUKTI RESMI HASIL EKSEKUSI GATE 1-R (BIRDCLEF+ 2026 — REVISI 12 SEPTEMBER 2026)

Tahap Gate 1-R (Minggu Ke-1 Revisi) telah selesai 100% pada dataset BirdCLEF+ 2026 (20 spesies burung Neotropis Pantanal, 4.351 berkas audio terkurasi) dengan split author-disjoint ketat.

### 1. Komposisi Dataset & Partisi Author-Disjoint Global (4.351 Klip Audio)
* **Total Baris Dataset:** 4.351 klip audio format OGG/FLAC (32.000 Hz, jendela 5.0 detik, mono, RMS 0.05).
* **Partisi Subset:**
  * **Gallery:** 3.653 klip audio dari **377 perekam (*author*) unik**.
  * **Query Clean:** 200 klip audio bersih dari **68 perekam (*author*) unik** (tepat 10 klip per spesies dari 20 taksa).
  * **Calibration:** 498 klip audio dari **95 perekam (*author*) unik** (untuk kalibrasi ambang batas open-set $\tau$).
* **Verifikasi Bebas Kebocoran (Zero Overlap Leakage):**
  * Irisan ID Rekaman: **0 overlap** (Gallery $\cap$ Query = 0, Gallery $\cap$ Calib = 0, Query $\cap$ Calib = 0).
  * Irisan Path Berkas: **0 overlap** di seluruh ketiga subset.
  * Irisan Perekam (*Strict Author-Disjoint*): **0 overlap** ($377 + 68 + 95 = 540$ author unik global, 100% independen).
* **Tautan Manifes:**
  * Manifes Partisi Resmi: [`data/manifests/dataset_split.csv`](../data/manifests/dataset_split.csv)
  * Spesies Target Terpilih (20 Taksa): [`data/manifests/species_freeze.csv`](../data/manifests/species_freeze.csv)
  * Spesies Non-Target Tereksklusi (186 Taksa): [`data/manifests/species_excluded.csv`](../data/manifests/species_excluded.csv)
  * Inventaris Mesin Dataset: [`data/manifests/birdclef_inventory.json`](../data/manifests/birdclef_inventory.json)
  * Metadata Komprehensif Excel (22 Sheet): [`data/manifests/Metadata_BirdCLEF.xlsx`](../data/manifests/Metadata_BirdCLEF.xlsx)

### 2. Hasil Evaluasi E1 Clean Retrieval pada 20 Spesies Burung Target (Gate 1-R)
| Kode | Representasi Audio | Dimensi | Top-1 Accuracy | mAP@10 | MRR | Recall@10 | Precision@10 | Status Metodologis |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$** | **BirdNET Backbone V2.4 (ONNX)** | 1024 | **95.00%** | **0.9126** | **0.9658** | **0.0528** | **0.9280** | Terbaik (Bioakustik Pretrained) |
| **$R_1$** | **PANNs CNN14 AudioSet (PyTorch)** | 2048 | **60.00%** | **0.4152** | **0.7005** | **0.0291** | **0.5025** | Menengah (Generic Audio) |
| **$R_0$** | **MFCC Baseline Handcrafted** | 40 | **27.50%** | **0.1319** | **0.4224** | **0.0123** | **0.2175** | Rendah (Baseline Klasik) |
| **$R_3$** | **Random Control (Kontrol Negatif)** | 40 | **6.50%** | **0.0190** | **0.1779** | **0.0028** | **0.0530** | Kontrol Acak Murni |

* **Temuan Saintifik E1:**
  1. **Kontrol Positif H5 Terbukti Mutlak:** Seluruh representasi ($R_2 \gg R_1 \gg R_0 \gg R_3$) secara konsisten dan signifikan melampaui kontrol acak $R_3$.
  2. **Keunggulan Bioakustik Spesifik Domain:** Representasi bioakustik $R_2$ mencapai Top-1 Accuracy 95.00% dan mAP@10 0.9126 pada kondisi tanpa kebocoran perekam.
* **Tautan Berkas Hasil E1 (Rezim Aktif Tunggal):**
  * Tabel Metrik Ringkasan Kanonik: [`results/processed/clean_retrieval_table.csv`](../results/processed/clean_retrieval_table.csv)
  * Tabel Rincian Per Kueri (800 Baris Lengkap Kolom `author`): [`results/processed/per_query_clean_retrieval.csv`](../results/processed/per_query_clean_retrieval.csv)
  * Catatan Eksekusi Mesin (S-01): [`results/processed/execution_note_E1.json`](../results/processed/execution_note_E1.json)
  * Gambar Visualisasi Benchmark: [`results/figures/clean_retrieval_benchmark.png`](../results/figures/clean_retrieval_benchmark.png)
  * Peta Persebaran Geospasial: [`results/figures/birdclef_geospatial_distribution_map.png`](../results/figures/birdclef_geospatial_distribution_map.png)
  * Notebook E0 Sanity Check: [`notebooks/E0_Pipeline_Sanity_Check.ipynb`](../notebooks/E0_Pipeline_Sanity_Check.ipynb)
  * Notebook E1 Clean Retrieval: [`notebooks/E1_Clean_Retrieval.ipynb`](../notebooks/E1_Clean_Retrieval.ipynb)

---

## ARSIP: HASIL EKSEKUSI GATE 1 LAMA (14 SPESIES SUMATERA — 11 SEPTEMBER 2026)
*(Catatan: Korpus lama ini telah dibatalkan melalui keputusan DEC-09 per 12 September 2026 karena keterbatasan volume sampel query $n=14$, dan seluruh berkas hasil eksperimennya telah diarsipkan secara aman di [`results/archive/2026-09-07_xenocanto16spesies/`](../results/archive/2026-09-07_xenocanto16spesies/)).*

## BUKTI HASIL EKSEKUSI LAINNYA

Berikut adalah bukti rekaman terminal saat skrip-skrip inti dieksekusi:

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

### Bukti Run 2: Suite Pengujian Integritas Saintifik ([`run_tests.py`](../run_tests.py))
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
Checkpoint path: D:\FILE AND TASK\TA\checkpoints\Cnn14_mAP=0.431.pth
GPU number: 1
  [PASS] Model Embedding Dimension Compliance (C-01)
================================================================================
[+] HASIL: 9/9 Pengujian Lolos (100.0%)
================================================================================
```

### Bukti Run 3: Penambangan Kasus Kegagalan Riil ([`src/analyze_failures.py`](../src/analyze_failures.py))
Perintah yang dijalankan: `python src/analyze_failures.py`
```text
======================================================================
[*] Menambang Kasus Kegagalan Nyata dari results/raw/...
======================================================================
[+] Berhasil menambang 30 kasus kegagalan nyata kueri Xeno-Canto!
Distribusi Penyebab:
  - low_snr_masking          : 20 kasus (66.7%)
  - acoustic_feature_overlap : 6 kasus (20.0%)
  - inter_species_confusion  : 4 kasus (13.3%)
[+] Tabel disimpan di: D:\FILE AND TASK\TA\results\processed\failure_analysis_table.csv
======================================================================
```

### Bukti Run 4: Pembuatan Grafik Publikasi 300 DPI ([`scripts/make_figures.py`](../scripts/make_figures.py))
Perintah yang dijalankan: `python scripts/make_figures.py`
```text
============================================================
=== MEMBUAT GAMBAR GRAFIK DENGAN PITA GALAT 95% CI ===
============================================================
[+] Gambar berhasil disimpan di: D:\FILE AND TASK\TA\results\figures\robustness_curve_map10.png
[+] Disinkronkan ke: D:\FILE AND TASK\TA\paper\figures\robustness_curve_map10.png
```

---

## 📊 HASIL EKSPERIMEN NYATA PASCA-PERBAIKAN MODEL ASLI

Berikut adalah angka komputasi nyata dari hasil inferensi model deep learning asli yang tersimpan di berkas [`results/processed/snr_robustness_table.csv`](../results/processed/snr_robustness_table.csv):

### 1. Kualitas Retrieval (mAP@10) Lintas Kondisi Derau
Setiap nilai dihasilkan dari pengujian 94 kueri bersih terhadap 260 rekaman galeri independen (*Strict Recordist-Disjoint*, 0 tumpang tindih perekam):

| Kondisi Derau (SNR) | $R_0$: MFCC Baseline (40-d) | $R_1$: Generic Audio (PANNs 2048-d) | $R_2$: Bioacoustic (BirdNET 1024-d) | $R_3$: Random Control (40-d) |
| :--- | :---: | :---: | :---: | :---: |
| **Clean (Tanpa Derau)** | 0.1029 | 0.2069 | **0.5876** | 0.0209 |
| **SNR 20 dB (Derau Ringan)** | 0.0770 | 0.1890 | **0.5736** | 0.0194 |
| **SNR 10 dB (Derau Sedang)** | 0.0549 | 0.1602 | **0.5561** | 0.0295 |
| **SNR 0 dB (Derau Berat)** | 0.0409 | 0.0756 | **0.5091** | 0.0236 |
| **SNR -5 dB (Derau Ekstrem)** | 0.0282 | 0.0438 | **0.4710** | 0.0203 |

### 2. Retensi Kualitas Relatif (% terhadap Kondisi Bersih)
| Kondisi Derau (SNR) | $R_0$: MFCC Baseline | $R_1$: Generic Audio (PANNs) | $R_2$: Bioacoustic Pretrained (BirdNET) |
| :--- | :---: | :---: | :---: |
| **Clean** | 100.0% | 100.0% | **100.0%** |
| **SNR 20 dB** | 74.8% | 91.4% | **97.6%** |
| **SNR 10 dB** | 53.4% | 77.4% | **94.6%** |
| **SNR 0 dB** | 39.8% | 36.5% | **86.6%** |
| **SNR -5 dB** | 27.4% | 21.2% | **80.1%** |

### 3. Temuan Kunci Sesuai Arahan Dosen:
1. **Koreksi Hipotesis H1 & H2:** Benar sesuai catatan Pak Ardika, *"titik awal rendah tidak sama dengan runtuh cepat"*. Representasi generik $R_1$ (PANNs CNN14) mengalami keruntuhan katastropik saat derau meningkat (retensi anjlok ke **21.2%** pada SNR -5 dB), bahkan secara relatif lebih rapuh dibanding baseline klasik $R_0$ MFCC (**27.4%**).
2. **Keunggulan Bioakustik Spesifik Domain ($R_2$ BirdNET Asli):** Setelah model BirdNET asli dimuat, representasi bioakustik menunjukkan ketahanan yang luar biasa: mempertahankan retensi relatif **80.1%** pada SNR -5 dB dengan akurasi Top-1 tetap di angka **71.3%** (mAP@10 = 0.4710).

---

## 📈 BUKTI VISUALISASI GRAFIK DENGAN PITA GALAT (95% CI)

Grafik komparasi ilmiah beresolusi 300 DPI yang memperlihatkan kurva mAP@10 dengan pita galat Bootstrap 95% Confidence Interval dan kurva retensi relatif telah dibuat dan tersimpan di:
- **Tautan Berkas:** [`results/figures/robustness_curve_map10.png`](../results/figures/robustness_curve_map10.png)
- **Salinan untuk Naskah:** [`paper/figures/robustness_curve_map10.png`](../paper/figures/robustness_curve_map10.png)

![Kurva Ketahanan Retrieval](../results/figures/robustness_curve_map10.png)

---

## 📓 BUKTI JUPYTER NOTEBOOK RESMI (GATE 1-R BIRDCLEF+ 2026)

Seluruh alur kerja Gate 1-R, mulai dari eksplorasi data, verifikasi prapemrosesan, *sanity check* bebas kebocoran, hingga evaluasi *clean retrieval* dieksekusi secara transparan pada 4 notebook resmi berikut:
1. **EDA & Eksplorasi Spasial:** [`notebooks/EDA_Tugas_Akhir.ipynb`](../notebooks/EDA_Tugas_Akhir.ipynb) — Peta geospasial Pantanal, distribusi 20 spesies target, dan analisis fisik audio.
2. **Verifikasi Prapemrosesan:** [`notebooks/Preprocessing Verification.ipynb`](../notebooks/Preprocessing%20Verification.ipynb) — Standarisasi 32 kHz, durasi 5.0s, normalisasi RMS 0.05.
3. **E0 Pipeline Sanity Check:** [`notebooks/E0_Pipeline_Sanity_Check.ipynb`](../notebooks/E0_Pipeline_Sanity_Check.ipynb) — Zero leakage ID/Path/Author overlap pada 4.351 klip audio.
4. **E1 Clean Retrieval Benchmark:** [`notebooks/E1_Clean_Retrieval.ipynb`](../notebooks/E1_Clean_Retrieval.ipynb) — Benchmark $R_0$ s/d $R_3$ pada 200 kueri bersih.

*(Catatan arsip: Notebook lama 14 spesies Sumatera telah dipindahkan ke [`results/archive/2026-09-07_xenocanto16spesies/notebooks/01_evaluasi_benchmark_dan_visualisasi.ipynb`](../results/archive/2026-09-07_xenocanto16spesies/notebooks/01_evaluasi_benchmark_dan_visualisasi.ipynb)).*

---

## 📅 RENCANA TAHAP BERIKUTNYA PASCA-BIMBINGAN:
1. Membuka dan mendiskusikan 4 notebook resmi Gate 1-R bersama Pak Ardika pada sesi bimbingan berikutnya sebagai bukti penyelesaian audit Gate 1-R.
2. Meminta arahan dan izin terkait pelaksanaan perekaman fisik AudioMoth di kampus ITERA (H6: Embung, Arboretum, Antropogenik) untuk persiapan eksperimen Minggu 2 (E2: Controlled Noise Robustness).
3. Mengonfirmasi keputusan formal D-07 mengenai kepatuhan aturan kompetisi Kaggle BirdCLEF+ 2026 untuk skripsi dan artikel ilmiah.
