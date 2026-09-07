# Panduan Lengkap Pertemuan Bimbingan — DSIC-2706
**Topik:** Mencari Audio yang Mirip Ketika Datanya Terbatas  
**Judul Kerja:** *Noise and Domain-Shift Robustness of Audio Representations for Cross-Domain Bioacoustic Retrieval: From Xeno-Canto to ITERA Soundscapes*  
**Peneliti:** Fabio Banyu Cyto (123450104)  
**Pembimbing:** Bapak Ardika (DSIC Research Group — Program Studi Sains Data ITERA)  
**Tanggal Pertemuan:** 06–07 September 2026 (Kick-off Minggu 1)  

---

## 1. Executive Summary (Elevator Pitch 1 Menit)
> *"Penelitian saya bukan membuat classifier spesies baru, melainkan menguji **ketahanan representasi audio untuk similarity retrieval** ketika audio mengalami derau lingkungan lokal dan pergeseran domain dari rekaman fokus (Xeno-Canto) ke soundscape riil ITERA.  
> Sebelum memasuki Minggu 1 resmi, seluruh fondasi repositori resmi DSIC-2706 di GitHub telah terpasang rapi, 416 berkas burung dari 16 spesies Sumatera telah diaudit manual (0 berkas korup), partisi telah bebas kebocoran total dengan **Strict Global Recordist-Disjoint** (0 overlap perekam), dan pipeline komparasi representasi (MFCC, Generic PANNs, Bioacoustic, Random) telah diuji coba berpasangan (paired stress-test).  
> Temuan simulasi menunjukkan representasi bioakustik mempertahankan retensi 38.9% pada derau ekstrem (-5 dB), hampir 2x lebih tangguh dibanding model generik (19.6%). Kesiapan sistem 100% lolos unit test, dan saya siap menerima arahan untuk tahap berikutnya: perekaman fisik noise di Embung dan Arboretum ITERA."*

---

## 2. Rincian 7 Pilar Pekerjaan yang Telah Selesai (Detail Teknis)

### Pilar 1: Penyelarasan Repositori Resmi GitHub (100% Sesuai Template Dosen)
- **Tautan Repositori:** `https://github.com/Data-Systems-and-Intelligent-Computing/DSIC-2706`
- **Status Sinkronisasi:** Sudah di-*push* ke branch `main` (`2ac659b..be14f60`), status *clean* dan *up-to-date*.
- **Arsitektur Modular:**
  - `src/dsic2706/`: Paket inti Python berisi submodul `data`, `audio`, `features`, `retrieval`, `open_set`, `evaluation`, `analysis`, dan `utils`.
  - `experiments/`: Modul *runner* eksperimen bertahap dari `E0_pipeline_sanity` hingga `E6_external_validation`.
  - `docs/`: Memisahkan dokumen perumusan masalah (`docs/research/`) dan protokol teknis (`docs/protocols/`).
  - `configs/`: Seluruh parameter terpusat dalam berkas YAML (`audio.yaml`, `datasets.yaml`, `representations.yaml`, `experiments.yaml`, `thresholds.yaml`).
  - **Proteksi Data (Bab 15):** `.gitignore` memproteksi berkas audio besar (`*.mp3`, `*.wav`) sehingga repositori GitHub tetap bersih dan ringan (hanya manifes CSV, checksum SHA-256, kode, dan hasil).
  - **Otomasi CLI:** `Makefile`, `pyproject.toml`, dan `requirements.txt` telah aktif (`make test`, `make sanity`, `make evaluate`, dll.).

### Pilar 2: Kurasi Dataset & Audit Kualitas Fisik (Zero Corrupt Audio)
- **Total Berkas Terverifikasi:** **493 berkas audio fisik** di disk.
  - **416 berkas burung target** (16 spesies representatif Sumatera dari Xeno-Canto).
  - **77 berkas satwa non-burung** (serangga, katak, kelelawar, primata) diisolasi khusus di `data/unknown_open_set/` untuk data uji negatif open-set.
- **Audit Manual:** Seluruh berkas telah didengarkan dan diperiksa secara manual: **0 berkas korup**, dan setiap spesies memiliki **15 hingga 35 berkas suara** (rata-rata 26 berkas/spesies), memenuhi *gate* minimum dosen.
- **Transparansi Pergantian Spesies (*Oriolus chinensis*):** 74 berkas *Oriolus chinensis* di Xeno-Canto v3 tidak menyediakan tautan unduhan audio karena kebijakan perlindungan satwa rentan perburuan (*poaching-sensitive*). Spesies ini digantikan secara terbuka oleh dua spesies Sumatera melimpah bertautan terbuka: *Aethopyga siparaja* ($N=26$) dan *Dicaeum trigonostigma* ($N=24$), menggenapkan total menjadi 16 spesies.
- **Kelengkapan Manifes:** 10 kolom wajib (ID, nama ilmiah, nama Inggris, perekam, negara/lokasi, tanggal, kualitas, lisensi, URL, dan checksum SHA-256) terisi 100% di `data/manifests/target_birds_manifest.csv`.

### Pilar 3: Partisi Bebas Kebocoran (Strict Global Recordist-Disjoint)
- **Akar Masalah:** Di Bab 11.2, dosen mengarahkan penggunaan *recordist-disjoint split* untuk menghindari model mempelajari sidik jari mikrofon/alat perekam (*recording gear fingerprinting*). Pada split awal, ada 14 perekam yang muncul di Gallery dan Query pada spesies berbeda.
- **Solusi Implementasi:** Algoritma pemotongan bipartit graf perekam:
  $$\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset$$
  - **Gallery Set:** 260 berkas dari **42 perekam**.
  - **Query Clean Set:** 94 berkas dari **29 perekam**.
  - **Calibration Set:** 62 berkas (digunakan eksklusif untuk kalibrasi $\tau$).
  - **Unknown Test Set:** 77 berkas satwa non-burung.
  - **Overlap Perekam:** **Tepat 0 perekam (0% Overlap / Zero Leakage)**.
- **Unit Test Kebocoran:** `tests/integration/test_split_leakage.py` lolos 100%.

### Pilar 4: Standarisasi Audio & Pencampuran Derau (Paired Stress-Testing)
- **Parameter Baku Audio:** 32,000 Hz, mono 1-channel, segmen 5.0 detik (160,000 sampel), seleksi jendela energi RMS tertinggi, normalisasi RMS target 0.05.
- **Protokol Uji Berpasangan (*Paired Test*):** Query yang sama diuji pada kondisi Clean, lalu diinjeksikan derau pada tingkat SNR terkontrol:
  $$\text{SNR (dB)} = 20 \log_{10}\left(\frac{\text{RMS}_{\text{signal}}}{\text{RMS}_{\text{noise}}}\right)$$
  Tingkat derau: **Clean ($\infty$), 20 dB, 10 dB, 0 dB, dan -5 dB**.

### Pilar 5: Representasi Audio yang Dibandingkan (Metrik Tunggal: Cosine Similarity)
1. **$R_0$ (MFCC Baseline):** 20 koefisien MFCC + mean/std pooling $\to$ 40-dimensi (Davis & Mermelstein, 1980).
2. **$R_1$ (Generic Pretrained Audio):** PANNs CNN14-like $\to$ 2048-dimensi (Kong et al., 2020).
3. **$R_2$ (Bioacoustic Pretrained):** Bioacoustic Foundation Model $\to$ 1024-dimensi (Kahl et al., 2021; Ghani et al., 2023).
4. **$R_3$ (Kontrol Negatif):** Random Ranking $\to$ 64-dimensi.
*Seluruh representasi dievaluasi beku (*frozen feature extractor*) menggunakan Cosine Similarity.*

### Pilar 6: Kalibrasi Ambang Batas Open-Set ($\tau$) & Perbaikan Bug Numerik
- **Audit Bug Sebelumnya:** Threshold MFCC sempat jatuh ke $\tau = 0.0000$ (FPR 100%) akibat grid search linier kasar yang melewatkan pemisahan kosinus MFCC di rentang 0.98–0.99.
- **Solusi Matematis:** Diperbaiki menggunakan kurva ROC empiris (`roc_curve`) dan indeks Youden's $J = \text{TPR} - \text{FPR}$.
- **Nilai Ambang Batas Terbekukan ($\tau^*$):**
  - $R_0$ (MFCC): $\tau^* = 0.9905$ ($J = 0.3905, F_1 = 0.6667$)
  - $R_1$ (Generic): $\tau^* = 0.9471$ ($J = 0.6409, F_1 = 0.8037$)
  - $R_2$ (Bioacoustic): $\tau^* = 0.9670$ ($J = 0.5289, F_1 = 0.8372$)
  - $R_3$ (Random): $\tau^* = 0.4744$

### Pilar 7: Hasil Benchmark Komparatif & Pengujian Hipotesis
Tabel hasil pada `results/processed/snr_robustness_table.csv`:

| Kondisi Derau (SNR) | $R_0$: MFCC | $R_1$: Generic Audio | $R_2$: Bioacoustic Pretrained | $R_3$: Random Control |
| :--- | :---: | :---: | :---: | :---: |
| **Clean (Tanpa Derau)** | 0.1029 | 0.2299 | **0.2408** | 0.0183 |
| **SNR 20 dB (Derau Ringan)** | 0.0770 | **0.2342** (101.9%) | 0.2315 (96.1%) | 0.0223 |
| **SNR 10 dB (Derau Sedang)** | 0.0549 | **0.2239** (97.4%) | 0.2137 (88.7%) | 0.0209 |
| **SNR 0 dB (Derau Berat)** | 0.0409 | 0.1109 (48.2%) | **0.1589** (**66.0%**) | 0.0149 |
| **SNR -5 dB (Derau Ekstrem)**| 0.0282 | 0.0450 (19.6%) | **0.0936** (**38.9%**) | 0.0179 |

- **H1 & H2 Terkonfirmasi:** Pada kondisi ekstrem (-5 dB), representasi bioakustik ($R_2$) mempertahankan retensi **38.9%** (hampir 2x lebih tangguh dibanding generic $R_1$ yang anjlok ke 19.6%, dan 3.3x dibanding MFCC). Akurasi Top-1 di -5 dB: $R_2 = 20.21\%$ vs $R_1 = 9.57\%$.
- **H4 Terkonfirmasi (Threshold Transfer):** Pada derau -5 dB, skor kemiripan $R_1$ tergeser jatuh di bawah ambang batas beku sehingga seluruh query target tertolak (Recall = 0.0000). Sedangkan $R_2$ mempertahankan stabilitas recall hingga 0 dB (Recall 0.6277, hanya bergeser $\Delta = -2.1\%$) dan masih meloloskan 23.40% query pada -5 dB.
- **H5 Terkonfirmasi (Positive Control):** Seluruh model utama mengungguli random ranking ($R_3 = 0.0183$) secara signifikan.

---

## 3. Tanya-Jawab Kritis: Antisipasi Pertanyaan Pak Ardika

Berikut adalah jawaban taktis dan ilmiah jika Pak Ardika menanyakan poin-poin krusial:

### Q1: *"Kenapa di rencana awal ada Oriolus chinensis, tapi sekarang diganti?"*
> **Jawaban Fabio:**  
> *"Saat saya melakukan pengunduhan daring dari Xeno-Canto API v3, 74 rekaman Oriolus chinensis di Indonesia mengembalikan field file: None. Ini adalah kebijakan baru Xeno-Canto untuk membatasi unduhan audio spesies yang rentan perdagangan burung liar (poaching-sensitive). Demi integritas dataset agar 100% berkas audio fisik dapat diunduh, diverifikasi checksum-nya, dan berlisensi terbuka, saya menggantinya dengan Aethopyga siparaja (26 klip) dan Dicaeum trigonostigma (24 klip). Total spesies target menjadi 16 spesies Sumatera yang seluruhnya memiliki data fisik lengkap."*

### Q2: *"Kenapa nilai Clean mAP@10 Anda sebelumnya ~0.31, sekarang menjadi ~0.24?"*
> **Jawaban Fabio:**  
> *"Penurunan ini adalah koreksi metodologis yang sehat, Pak. Pada pengujian awal, jumlah clean query hanya 34 klip (~2 klip per spesies) dan pemisahan recordist baru bersifat per-species. Sekarang, set query bersih diperbesar menjadi 94 klip (~6 klip per spesies) dan diterapkan partisi Strict Global Recordist-Disjoint (tidak ada satu pun perekam di Gallery yang muncul di Query). Memperbesar sampel dan memutus kebocoran gaya rekaman menghilangkan bias optimisme sampel kecil (small-sample optimistic bias), sehingga angka 0.24 ini adalah cerminan performa retrieval riil yang jujur."*

### Q3: *"Bagaimana Anda menjamin tidak ada data leakage antar-split?"*
> **Jawaban Fabio:**  
> *"Saya membuat unit test otomatis di `tests/integration/test_split_leakage.py` yang memvalidasi 3 level kebocoran:  
> 1. Zero Recording ID leakage (overlap = 0).  
> 2. Zero Filepath leakage (overlap = 0).  
> 3. Zero Global Recordist leakage (42 perekam Gallery vs 29 perekam Query, overlap = 0).  
> Pengujian ini terintegrasi dalam CI script `python run_tests.py` dan menghasilkan status PASSED 100%."*

### Q4: *"Kenapa sebelumnya ada threshold 0.0000 dengan FPR 100%?"*
> **Jawaban Fabio:**  
> *"Pada implementasi awal terjadi kesalahan pencarian threshold linier dengan step 0.01. Karena skor kosinus MFCC berkumpul sangat rapat pada 0.98–0.99, grid search melewatkan titik pisah dan fungsi optimasi F1 memilih 0.0000 sebagai solusi jalan pintas numerik. Masalah ini sudah saya perbaiki tuntas menggunakan titik potong kurva ROC empiris (sklearn roc_curve) dengan kriteria Youden's J (TPR - FPR). Nilai threshold terkalibrasi sekarang adalah tau* = 0.9905 dengan F1 = 0.6667 yang valid secara teoritis."*

### Q5: *"Bagaimana status Background Noise dan Soundscape ITERA?"*
> **Jawaban Fabio:**  
> *"Sesuai dengan checklist kesiapan, eksperimen yang berjalan saat ini adalah simulasi terkontrol (proof of pipeline) menggunakan derau terstandar untuk memastikan seluruh rumus matematika, ranking kosinus, dan kurva retensi bebas dari bug sebelum turun ke lapangan. Perekaman fisik suara murni lingkungan (background-only) di Embung ITERA dan Arboretum/Kebun Raya ITERA adalah agenda utama Minggu 2 yang siap saya laksanakan setelah pertemuan ini."*

---

## 4. Perintah Mandiri untuk Ditunjukkan Langsung ke Dosen (Live Demo di Laptop)

Jika Pak Ardika meminta Anda membuka terminal di depan beliau:

1. **Jalankan Seluruh 7 Unit Test Saintifik (Hanya 3 detik):**
   ```powershell
   python run_tests.py
   ```
   *(Menunjukkan status: `7/7 Pengujian Lolos (100.0%)`)*

2. **Buktikan Zero Recordist Overlap (1 detik):**
   ```powershell
   python -c "import pandas as pd; df=pd.read_csv('data/manifests/dataset_split.csv'); g=set(df[df['split_role']=='gallery']['recordist']); q=set(df[df['split_role']=='query_clean']['recordist']); print('Overlap Perekam Gallery vs Query:', len(g.intersection(q)))"
   ```
   *(Menunjukkan output: `Overlap Perekam Gallery vs Query: 0`)*

3. **Jalankan Sanity Check E0:**
   ```powershell
   python experiments/E0_pipeline_sanity/run_e0.py
   ```
   *(Menunjukkan parameter baku 32kHz, zero leakage, dan random control mAP < 0.02)*

4. **Tunjukkan Halaman GitHub Resmi:**
   Buka browser ke `https://github.com/Data-Systems-and-Intelligent-Computing/DSIC-2706` dan tunjukkan struktur rapi dan berkas `docs/CATATAN_PROGRES_BIMBINGAN.md`.

---

## 5. Agenda Pembahasan Pertemuan (Action Plan Minggu 1 & 2)

Mintalah arahan spesifik pada 3 poin ini kepada Pak Ardika:
1. **Validasi Pemilihan Spesies & Partisi:** Meminta persetujuan final mengenai daftar 16 spesies Sumatera dan pemisahan *strict recordist-disjoint*.
2. **Peminjaman Alat & Jadwal Perekaman Lapangan:** Menanyakan apakah ada unit *AudioMoth* atau *field recorder* laboratorium yang bisa dipinjam untuk perekaman background noise di Embung dan Arboretum ITERA.
3. **Titik Koordinat Lokasi Perekaman ITERA:** Mengonfirmasi stasiun pengambilan sampel derau di kampus (misal: Embung A/B/C, kawasan rimbun Arboretum, dan area tepi jalan lingkar kampus).
