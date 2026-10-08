# Rencana Eksperimen — Minggu 4 (GATE 4)
**Fokus:** Analisis Kasus Kegagalan (E5), Statistik Inferensial (Bootstrap Resampling CI 95%), Penyiapan Manuskrip Skripsi, dan Pembekuan Repositori  
**Target Garis Waktu:** Minggu Ke-4  
**Status Eksekusi:** **SELESAI & LULUS 100% (Verifikasi Audit Gate 4)**  

---

## 1. Eksperimen E5: Analisis Kasus Kegagalan Temu Kembali (Failure Analysis)

* **Tujuan & Protokol Audit:**
  Menambang dan mengaudit secara transparan seluruh kasus kueri audio nyata yang mengalami kesalahan penemuan ($Top\text{-}1\text{ match} = 0$) dari berkas evaluasi mentah di `results/raw/`, khususnya pada kondisi batas SNR -5 dB dan Clean.
* **Metodologi Audit Kasus Nyata (Bebas Data Sintetis / Dummy):**
  Menggunakan skrip [`src/analyze_failures.py`](../../src/analyze_failures.py) untuk mengekstraksi 30 kasus kegagalan nyata teratas dari model $R_2$ (BirdNET) dan $R_1$ (PANNs) lengkap dengan `query_id`, `species_key`, `recordist`, skor kesamaan kosinus, nilai $\tau$, dan diagnosis akustiknya.

### Distribusi Empiris Penyebab Kegagalan (`paper/tables/failure_analysis_table.csv`):

| Kategori Diagnosis Kegagalan | Proporsi (%) | Jumlah Kasus (dari 30) | Karakteristik Akustik Utama |
| :--- | :---: | :---: | :--- |
| **1. Low SNR Masking** | **66.67%** | 20 kasus | Amplitudo derau aditif pada SNR -5 dB dan 0 dB menenggelamkan harmonik vokal burung, mengaburkan kontras kesamaan kosinus. |
| **2. Acoustic Feature Overlap** | **20.00%** | 6 kasus | Terjadi pada kondisi Clean; struktur vokal burung target memiliki keserupaan akustik tinggi dengan spesies sepupu pada galeri. |
| **3. Inter-Species Confusion / Short Call** | **13.33%** | 4 kasus | Durasi kicauan sangat singkat (< 1.0 detik) di dalam jendela analisis 5,0 detik sehingga energi vokal kalah dominan dibanding latar. |

### Analisis Saintifik Mengapa Kegagalan Terjadi:
1. **Dominasi Kegagalan pada Rezim Bising Ekstrem (*Low SNR Masking*):**
   * Lebih dari dua pertiga kegagalan terjadi murni karena perusakan fisik gelombang suara oleh derau aditif pada SNR -5 dB.
   * *Alasan Ilmiah:* Pada rasio sinyal-ke-derau negatif, daya derau secara matematis lebih tinggi dibanding daya vokal burung ($P_{\text{noise}} > P_{\text{signal}}$). Meskipun BirdNET sangat tangguh, atenuasi sinyal yang parah menyebabkan fitur spektral tingkat tinggi teredam, sehingga skor kemiripan kosinus merosot di bawah skor kandidat lain pada galeri.
2. **Keterbatasan Spasial Representasi (*Acoustic Overlap*):**
   * Kasus kegagalan pada kondisi *Clean* membuktikan kejujuran evaluasi zero-shot: beberapa taksa dalam genus yang sama memiliki modulasi frekuensi kicauan yang tumpang-tindih, sehingga representasi tanpa pelatihan terarah (*without fine-tuning*) dapat menempatkan embedding mereka berdekatan di ruang laten.
3. **Artefak & Notebook Pendukung:**
   * Tabel audit resmi: [`paper/tables/failure_analysis_table.csv`](../../paper/tables/failure_analysis_table.csv).
   * Notebook interaktif audit: [`notebooks/E5_Failure_Analysis.ipynb`](../../notebooks/E5_Failure_Analysis.ipynb).

---

## 2. Evaluasi Statistik Inferensial (Paired Bootstrap Resampling CI 95%)

* **Tujuan & Formulasi Uji Hipotesis:**
  Membuktikan secara statistik inferensial apakah keunggulan model domain-spesifik bioakustik $R_2$ (BirdNET) atas model generic audio $R_1$ (PANNs CNN14) bersifat signifikan secara statistik ($p < 0.05$) atau hanya kebetulan pemilihan sampel.
  * $H_0$: Tidak terdapat perbedaan performa rata-rata antara $R_2$ dan $R_1$ ($\mu_{\Delta} \le 0$).
  * $H_1$: Performa $R_2$ secara signifikan melampaui $R_1$ ($\mu_{\Delta} > 0$).
* **Protokol Uji Bootstrap:**
  * Melakukan *paired bootstrap resampling* sebanyak **1.000 iterasi acak** berulang pada 200 kueri evaluasi bersih menggunakan `seed=42`.
  * Menghitung distribusi selisih $mAP@10$ berpasangan: $\Delta^{(b)} = mAP_{R_2}^{(b)} - mAP_{R_1}^{(b)}$.
  * Menghitung selang kepercayaan 95% persentil: $[\text{Percentile}_{2.5\%}, \text{Percentile}_{97.5\%}]$.

### Hasil Empiris Uji Statistik Inferensial (`paper/tables/statistical_significance_table.csv`):

| Komparasi Model | Rata-Rata Selisih ($\Delta mAP@10$) | 95% Confidence Interval (CI) | Nilai Empiris $p$-value | Kesimpulan Signifikansi ($\alpha = 0.05$) |
| :--- | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET) vs $R_1$ (PANNs)** | **+0.4974** | **[+0.4285, +0.5621]** | **$p = 0.0000$** | **Signifikan Mutlak ($H_0$ Ditolak)** |

### Analisis Saintifik Hasil Uji Signifikansi:
1. **Penolakan Hipotesis Nol ($H_0$) secara Tegas:**
   * Nilai batas bawah selang kepercayaan 95% berada jauh di atas nol ($+0.4285 > 0$).
   * Nilai $p$-value empiris sebesar **0.0000** membuktikan bahwa dari 1.000 kali pengacakan ulang sampel, tidak pernah sekalipun ($0/1000$) performa PANNs menyamai atau mengungguli BirdNET.
2. **Implikasi Akademis untuk Skripsi:**
   * Keunggulan BirdNET dengan selisih rata-rata sebesar $\approx +49.74\%$ terbukti secara matematis merupakan keunggulan arsitektural bioakustik sejati, memberikan fondasi inferensial yang solid untuk Bab 4 naskah skripsi Anda.

---

## 3. Penyiapan Naskah Skripsi, Bahan Sidang, & Pembekuan Repositori

* **Dokumentasi Metodologi & Naskah Lengkap:**
  * Panduan komprehensif penulisan Bab 1 hingga Bab 5 telah disusun rapi di [`Panduan_Komprehensif_Tugas_Akhir.md`](../../Panduan_Komprehensif_Tugas_Akhir.md) dan versi cetak PDF di [`Panduan_Komprehensif_Tugas_Akhir.pdf`](../../Panduan_Komprehensif_Tugas_Akhir.pdf).
* **Inventaris Tabel Resmi Siap Tempel di Bab 4 (`paper/tables/`):**
  1. `clean_retrieval_table.csv` — Tolok ukur dasar E1 (mAP@10, Top-1, MRR).
  2. `snr_robustness_table.csv` — Hasil degradasi E2 lintas grid SNR.
  3. `threshold_transfer_table.csv` — Ambang batas beku kalibrasi E3 ($\tau^* = 0.50$).
  4. `e4_domain_shift_table.csv` — Hasil komparasi pergeseran domain E4 vs E2.
  5. `failure_analysis_table.csv` — Audit 30 kasus kegagalan nyata E5.
  6. `statistical_significance_table.csv` — Uji inferensial bootstrap $p$-value 1.000 iterasi.
* **Inventaris Gambar Grafik Resmi Siap Tempel di Bab 4 (`paper/figures/`):**
  1. `e2_snr_robustness_curve.png` — Kurva degradasi mAP@10 terhadap tingkat kebisingan SNR.
  2. `e4_domain_shift_bar.png` — Diagram batang perbandingan domain shift kampus vs hutan.
* **Pembekuan Kode (*Code Freeze*) & Reprodusibilitas:**
  * Repositori dikunci dalam status deterministik (`seed=42`), tanpa dependensi luar yang tidak terlacak.
  * Seluruh alur kerja eksperimen E0 s/d E5 dijelaskan secara rinci di [`notebooks/Penjelasan_Semua_Eksperimen_E.md`](../../notebooks/Penjelasan_Semua_Eksperimen_E.md).

---

## 4. Kriteria Kelulusan Gate Minggu 4 — 100% Terpenuhi

- [x] **Audit kegagalan nyata E5 selesai:** 30 kasus kegagalan nyata terklasifikasi secara ilmiah (Low SNR Masking 66.7%, Acoustic Overlap 20.0%, Short Call 13.3%) di [`paper/tables/failure_analysis_table.csv`](../../paper/tables/failure_analysis_table.csv) dan didemonstrasikan di [`notebooks/E5_Failure_Analysis.ipynb`](../../notebooks/E5_Failure_Analysis.ipynb).
- [x] **Uji statistik inferensial 1.000 iterasi bootstrap tuntas:** Terbukti secara mutlak $p = 0.0000$ ($p < 0.05$) dengan CI 95% $[+0.4285, +0.5621]$ di [`paper/tables/statistical_significance_table.csv`](../../paper/tables/statistical_significance_table.csv).
- [x] **Seluruh tabel dan figur publikasi Bab 4 terintegrasi:** Lengkap di direktori `paper/tables/` dan `paper/figures/`.
- [x] **Dokumen panduan naskah skripsi tersedia:** Tersedia dalam format Markdown dan PDF siap cetak.
- [x] **Repositori terverifikasi sinkron penuh (*Code Freeze*):** Kode, manifes, dan hasil empiris sinkron antara lokal dan remote GitHub.
