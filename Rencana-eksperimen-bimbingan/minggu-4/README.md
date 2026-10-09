# Rencana Eksperimen — Minggu 4 (GATE 4)
**Fokus:** Analisis Kasus Kegagalan Terstratifikasi (E5), Statistik Inferensial Komprehensif (Paired Bootstrap 1.000 Iterasi CI 95%), Penyiapan Manuskrip, dan Pembekuan Repositori  
**Target Garis Waktu:** Minggu Ke-4  
**Status Eksekusi:** **SELESAI & LULUS 100% (Verifikasi Audit Gate 4 — Terverifikasi Data Mentah & Uji Bootstrap Lengkap)**  

---

## 1. Eksperimen E5: Analisis Kasus Kegagalan Temu Kembali (Stratified Failure Analysis)

* **Tujuan & Protokol Audit Terstratifikasi:**
  Menambang dan mengaudit secara transparan kasus kueri audio nyata yang mengalami kegagalan penemuan dari berkas evaluasi mentah di `results/raw/`. Sampel diambil secara terstratifikasi sebanyak **30 kasus autentik** yang mencakup:
  * **Kondisi Clean:** 10 kasus (5 kasus $R_2$ + 5 kasus $R_1$)
  * **Kondisi SNR -5 dB (Bising Ekstrem):** 20 kasus (10 kasus $R_2$ + 10 kasus $R_1$)
* **Metodologi Analisis Akustik Bebas Template:**
  Menggunakan [`src/analyze_failures.py`](../../src/analyze_failures.py) untuk menghitung parameter bioakustik fisik langsung dari gelombang audio: frekuensi pusat (*spectral centroid*), lebar pita (*bandwidth*), selisih skor terhadap ambang batas (*margin to tau*), dan selisih kemiripan terhadap taksa target (*retrieval gap*).

#### Distribusi Empiris Taksonomi Kegagalan (`paper/tables/failure_analysis_table.csv`):

| Kategori Taksonomi Kegagalan | Proporsi (%) | Jumlah Kasus | Sebaran Model & Kondisi | Karakteristik Bioakustik Utama |
| :--- | :---: | :---: | :--- | :--- |
| **1. Top-1 Confusion (Above Tau)** | **36.67%** | **11 kasus** | • $R_1$ Clean (2)<br>• $R_1$ SNR -5 dB (9) | Skor kemiripan melampaui $\tau^*$, namun sistem mencocokkan taksa galeri yang keliru akibat kedekatan manifold laten generik ($R_1$). |
| **2. Open-Set False Rejection** | **36.67%** | **11 kasus** | • $R_2$ Clean (3)<br>• $R_2$ SNR -5 dB (8) | Top-1 kueri benar mencocokkan taksa target, namun skor kemiripan tertekan di bawah $\tau^*$ akibat atenuasi energi derau atau variasi amplitudo sinyal. |
| **3. Total Retrieval Collapse** | **26.67%** | **8 kasus** | • $R_2$ Clean (2)<br>• $R_1$ Clean (3)<br>• $R_2$ SNR -5 dB (2)<br>• $R_1$ SNR -5 dB (1) | Kegagalan ganda di mana skor kemiripan anjlok di bawah ambang batas $\tau^*$ DAN Top-1 memprediksi taksa yang keliru. |

*Tabel lengkap 30 kasus rinci per-kueri tersimpan di [`paper/tables/failure_analysis_table.csv`](../../paper/tables/failure_analysis_table.csv).*

### Analisis Saintifik Mengapa Kegagalan Terjadi:
1. **Dilema Penolakan Kaku pada $R_2$ (BirdNET):**
   * Pada kondisi bising ekstrem (SNR -5 dB), sebagian besar kegagalan $R_2$ tergolong *Open-Set False Rejection*. Model sebenarnya menempatkan rekaman taksa yang benar di peringkat #1, tetapi karena skor kemiripan turun tipis di bawah $\tau^* = 0.7128$ (margin -0.0044 s.d. -0.0729), sistem menolaknya sebagai audio asing. Ini membuktikan bahwa pembekuan $\tau^*$ yang rigid mempertahankan keselamatan deteksi (*low false alarms*) dengan konsekuensi penurunan recall.
2. **Kelemahan Arsitektural Representasi Generik Audio ($R_1$):**
   * Pada $R_1$ (PANNs), kegagalan didominasi oleh *Top-1 Confusion Above Tau* (9 kasus pada SNR -5 dB dan 2 kasus pada Clean). Derau aditif menginduksi pergeseran representasi laten (*latent representation confusion*), membuat embedding suara kueri salah menempel ke taksa burung lain dengan skor kemiripan palsu yang tinggi (di atas $\tau^* = 0.9117$).
3. **Artefak & Notebook Demonstrasi:**
   * Notebook interaktif: [`notebooks/E5_Failure_Analysis.ipynb`](../../notebooks/E5_Failure_Analysis.ipynb).
   * Visualisasi audit terstratifikasi: [`paper/figures/e5_failure_analysis.png`](../../paper/figures/e5_failure_analysis.png).

---

## 2. Evaluasi Statistik Inferensial Komprehensif (Paired Bootstrap Resampling CI 95%)

* **Tujuan & Formulasi Uji Hipotesis Lengkap:**
  Membuktikan secara statistik inferensial validitas seluruh hipotesis penelitian ($H_1, H_2, H_3, H_5$) melalui *paired bootstrap resampling* sebanyak **1.000 iterasi acak** berulang pada data mentah per-kueri (`seed=42`).
* **Skrip Inferensial Reproduktif:**
  Dijalankan melalui [`src/bootstrap_inference.py`](../../src/bootstrap_inference.py) dan [`scripts/run_bootstrap.py`](../../scripts/run_bootstrap.py).

### Hasil Empiris Uji Statistik Inferensial 7 Hipotesis (`paper/tables/statistical_significance_table.csv`):

| Skenario Pengujian | Komparasi Model / Kondisi | Rata-Rata Selisih ($\Delta$) | 95% Confidence Interval (CI) | $p$-value Empiris | Status Signifikan ($\alpha = 0.05$) | Kesimpulan Saintifik |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_1$ (PANNs) | **+0.4981** | **[+0.4504, +0.5473]** | **$p < 0.001$** | **Signifikan** | $R_2$ unggul mutlak atas model generik audio |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_0$ (MFCC) | **+0.7811** | **[+0.7421, +0.8183]** | **$p < 0.001$** | **Signifikan** | $R_2$ unggul mutlak atas baseline klasik |
| **Clean Retrieval (mAP@10)** | $R_1$ (PANNs) vs $R_0$ (MFCC) | **+0.2830** | **[+0.2355, +0.3308]** | **$p < 0.001$** | **Signifikan** | $R_1$ unggul atas MFCC pada kondisi bersih |
| **Retensi Relatif SNR -5 dB** | $R_2$ (BirdNET) vs $R_1$ (PANNs) | **+0.7020** | **[+0.6424, +0.7571]** | **$p < 0.001$** | **Signifikan** | Retensi $R_2$ (84.5%) unggul mutlak atas $R_1$ (14.2%) |
| **Retensi Relatif SNR -5 dB** | $R_0$ (MFCC) vs $R_1$ (PANNs) | **+0.1223** | **[+0.0581, +0.1994]** | **$p < 0.001$** | **Signifikan** | Retensi MFCC (26.4%) melampaui PANNs (14.2%) secara signifikan |
| **Sensitivitas Derau (-5 dB)** | $R_2$ (E4 Soundscape vs E2 ITERA) | **-0.0097** | **[-0.0479, +0.0275]** | **$p = 0.6100$** | **Tidak Signifikan** | H3 Tidak Diuji (Deferred): Soundscape ITERA belum teranotasi; data aditif menunjukkan stabilitas profil spektral |
| **Sensitivitas Derau (-5 dB)** | $R_1$ (E4 Soundscape vs E2 ITERA) | **+0.0892** | **[+0.0572, +0.1210]** | **$p < 0.001$** | **Signifikan** | PANNs sangat sensitif terhadap profil spektral derau |

### Analisis Temuan Ilmiah Signifikansi Statistik:
1. **Keunggulan Bioakustik Spesifik Terbukti Mutlak ($R_2 > R_1$):**
   * Selisih mAP@10 kondisi bersih sebesar $+0.4981$ memiliki CI 95% $[+0.4504, +0.5473]$ dengan $p < 0.001$. Tidak ada satu pun dari 1.000 iterasi di mana PANNs menyamai BirdNET.
2. **Koreksi Hipotesis H1 & Retensi SNR -5 dB ($R_0$ vs $R_1$):**
   * Uji retensi ketahanan derau pada SNR -5 dB membuktikan bahwa baseline klasik MFCC ($R_0$, retensi 26.4%) justru **mengungguli PANNs ($R_1$, retensi 14.2%) secara signifikan** dengan $\Delta = +0.1223$, CI 95% $[+0.0581, +0.1994]$, dan $p < 0.001$.
   * *Temuan Saintifik:* Hipotesis keunggulan *deep pretrained representations* atas *handcrafted features* di bawah derau lingkungan hanya terbukti untuk model domain-spesifik bioakustik ($R_2$), bukan untuk representasi deep generic audio secara umum.
3. **Uji Sensitivitas Profil Derau E4 vs E2:**
   * Untuk $R_2$, nilai $p = 0.6100$ dan CI 95% yang mencakup 0 ($[-0.0479, +0.0275]$) mengindikasikan tidak terdeteksi perbedaan performa yang signifikan secara statistik antara derau kampus ITERA dan soundscape BirdCLEF. Ketiadaan perbedaan signifikan ini menunjukkan stabilitas retensi terhadap variasi spektral derau aditif, bukan bukti ekuivalensi absolut.
   * Sebaliknya, untuk $R_1$, nilai $p < 0.001$ membuktikan bahwa model generic audio mengalami sensitivitas signifikan terhadap perbedaan profil spektral derau.

---

## 3. Penyiapan Naskah Skripsi, Bahan Sidang, & Pembekuan Repositori

* **Dokumentasi Metodologi & Naskah Lengkap:**
  * Seluruh revisi telah disinkronkan ke dalam naskah utama [`paper/manuscript.md`](../../paper/manuscript.md).
  * Panduan komprehensif Bab 1–5 tersimpan di [`Panduan_Komprehensif_Tugas_Akhir.md`](../../Panduan_Komprehensif_Tugas_Akhir.md).
* **Inventaris Tabel Publikasi Resmi Bab 4 (`paper/tables/`):**
  1. `clean_retrieval_table.csv` — Tolok ukur dasar E1 (mAP@10, Top-1, MRR).
  2. `snr_robustness_table.csv` — Hasil degradasi E2 lintas grid SNR.
  3. `threshold_transfer_table.csv` — Evaluasi open-set E3 lintas SNR dengan $\tau^*$ beku.
  4. `e4_domain_shift_table.csv` — Evaluasi komparatif E4 soundscape vs E2 derau ITERA.
  5. `failure_analysis_table.csv` — Audit terstratifikasi 30 kasus kegagalan nyata E5.
  6. `statistical_significance_table.csv` — Uji inferensial bootstrap 7 skenario (1.000 iterasi).
* **Inventaris Gambar Publikasi Bab 4 (`paper/figures/`):**
  1. `e2_snr_robustness_curve.png` — Kurva degradasi SNR E2.
  2. `e3_calibration_roc_youden.png` — Kurva kalibrasi ROC dan Youden's Index E3.
  3. `e3_threshold_transfer_snr.png` — Grafik transfer ambang batas E3 lintas SNR.
  4. `e4_noise_profile_sensitivity.png` — Diagram batang sensitivitas profil derau E4 vs E2.
  5. `e5_failure_analysis.png` — Visualisasi audit kegagalan terstratifikasi E5.
* **Pembekuan Kode (*Code Freeze*) & Reprodusibilitas Penuh:**
  * Seluruh *hash* manifes audio tersinkronisasi di [`artifacts/reproducibility/manifest_sha256.txt`](../../artifacts/reproducibility/manifest_sha256.txt).
  * Seluruh 9 unit test saintifik lolos 100% via `python run_tests.py`.

---

## 4. Kriteria Kelulusan Gate Minggu 4 — 100% Terpenuhi

- [x] **Audit Terstratifikasi Kasus Kegagalan E5 Selesai:** 30 kasus nyata terstratifikasi lintas 16 takson (Clean & -5 dB) terklasifikasi secara objektif (Top-1 Confusion Above Tau 36.67%, Open-Set False Rejection 36.67%, Total Collapse 26.67%) di [`paper/tables/failure_analysis_table.csv`](../../paper/tables/failure_analysis_table.csv) dan [`notebooks/E5_Failure_Analysis.ipynb`](../../notebooks/E5_Failure_Analysis.ipynb).
- [x] **Uji Statistik Inferensial Komprehensif (1.000 Iterasi) Tuntas:** 7 skenario hipotesis diuji dengan Paired Bootstrap, membuktikan $R_2$ unggul ($p < 0.001$, CI $[+0.4504, +0.5473]$), retensi MFCC unggul atas PANNs ($p < 0.001$), serta tidak terdeteksi perbedaan signifikan profil derau pada $R_2$ ($p = 0.6100$).
- [x] **Seluruh Tabel dan Gambar Publikasi Bab 4 Terintegrasi:** Lengkap di direktori `paper/tables/` dan `paper/figures/`.
- [x] **Naskah Skripsi & Catatan Bimbingan Sinkron:** Seluruh angka di `paper/manuscript.md` dan `Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md` cocok 100% dengan data mentah.
- [x] **Repositori Lolos Uji Integritas 100%:** `python run_tests.py` lolos **9 dari 9 (100%)**.

