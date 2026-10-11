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
| **1. Open-Set False Rejection** | **33.33%** | **10 kasus** | • $R_2$ Clean (3)<br>• $R_2$ SNR -5 dB (7) | Top-1 kueri benar mencocokkan taksa target, namun skor kemiripan tertekan di bawah $\tau^*$ akibat atenuasi energi derau atau variasi amplitudo sinyal. |
| **2. Top-1 Confusion (Above Tau)** | **30.00%** | **9 kasus** | • $R_1$ Clean (2)<br>• $R_1$ SNR -5 dB (7) | Skor kemiripan melampaui $\tau^*$, namun sistem mencocokkan taksa galeri yang keliru akibat kedekatan manifold laten generik ($R_1$). |
| **3. Total Retrieval Collapse** | **36.67%** | **11 kasus** | • $R_2$ Clean (2)<br>• $R_1$ Clean (3)<br>• $R_2$ SNR -5 dB (3)<br>• $R_1$ SNR -5 dB (3) | Kegagalan ganda di mana skor kemiripan anjlok di bawah ambang batas $\tau^*$ DAN Top-1 memprediksi taksa yang keliru. |

*Tabel lengkap 30 kasus rinci per-kueri tersimpan di [`paper/tables/failure_analysis_table.csv`](../../paper/tables/failure_analysis_table.csv).*

### Analisis Saintifik Mengapa Kegagalan Terjadi:
1. **Dilema Penolakan Kaku pada $R_2$ (BirdNET):**
   * Pada kondisi bising ekstrem (SNR -5 dB), kegagalan $R_2$ didominasi oleh *Open-Set False Rejection* (7 kasus). Model sebenarnya menempatkan rekaman taksa yang benar di peringkat #1, tetapi karena skor kemiripan turun tipis di bawah $\tau^* = 0.7071$, sistem menolaknya sebagai audio asing. Ini membuktikan bahwa pembekuan $\tau^*$ yang rigid mempertahankan keselamatan deteksi (*low false alarms*) dengan konsekuensi penurunan recall.
2. **Kelemahan Arsitektural Representasi Generik Audio ($R_1$):**
   * Pada $R_1$ (PANNs), kegagalan didominasi oleh *Top-1 Confusion Above Tau* (7 kasus pada SNR -5 dB dan 2 kasus pada Clean). Derau aditif menginduksi pergeseran representasi laten (*latent representation confusion*), membuat embedding suara kueri salah menempel ke taksa burung lain dengan skor kemiripan palsu yang tinggi (di atas $\tau^* = 0.8974$).
3. **Artefak & Notebook Demonstrasi:**
   * Notebook interaktif: [`notebooks/E5_Failure_Analysis.ipynb`](../../notebooks/E5_Failure_Analysis.ipynb).
   * Visualisasi audit terstratifikasi: [`paper/figures/e5_failure_analysis.png`](../../paper/figures/e5_failure_analysis.png).

---

## 2. Evaluasi Statistik Inferensial Komprehensif (Paired Bootstrap Resampling CI 95%)

* **Tujuan & Formulasi Uji Hipotesis Lengkap:**
  Membuktikan secara statistik inferensial validitas seluruh hipotesis penelitian ($H_1, H_2, H_3, H_5$) melalui *paired bootstrap resampling* sebanyak **1.000 iterasi acak** berulang pada data mentah per-kueri (`seed=42`).
* **Skrip Inferensial Reproduktif:**
  Dijalankan melalui [`src/bootstrap_inference.py`](../../src/bootstrap_inference.py) dan [`scripts/run_bootstrap.py`](../../scripts/run_bootstrap.py).

### Hasil Empiris Uji Statistik Inferensial (`paper/tables/statistical_significance_table.csv`):

| Skenario Pengujian | Komparasi Model / Kondisi | Rata-Rata Selisih ($\Delta$) | 95% Confidence Interval (CI) | $p$-value Empiris | Status Signifikan ($\alpha = 0.05$) | Kesimpulan Saintifik |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_1$ (PANNs) | **+0.4609** | **[+0.4260, +0.4986]** | **$p \le 0.001$** | **Signifikan** | $R_2$ unggul mutlak atas model generik audio |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_0$ (MFCC) | **+0.5688** | **[+0.5316, +0.6054]** | **$p \le 0.001$** | **Signifikan** | $R_2$ unggul mutlak atas baseline klasik |
| **Clean Retrieval (mAP@10)** | $R_1$ (PANNs) vs $R_0$ (MFCC) | **+0.1079** | **[+0.0854, +0.1314]** | **$p \le 0.001$** | **Signifikan** | $R_1$ unggul atas MFCC pada kondisi bersih |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_3$ (Random) | **+0.6145** | **[+0.5753, +0.6528]** | **$p \le 0.001$** | **Signifikan** | H5 Terpenuhi: $R_2$ unggul mutlak atas kontrol acak |
| **Clean Retrieval (mAP@10)** | $R_1$ (PANNs) vs $R_3$ (Random) | **+0.1536** | **[+0.1286, +0.1796]** | **$p \le 0.001$** | **Signifikan** | H5 Terpenuhi: $R_1$ unggul atas kontrol acak |
| **Clean Retrieval (mAP@10)** | $R_0$ (MFCC) vs $R_3$ (Random) | **+0.0457** | **[+0.0327, +0.0589]** | **$p \le 0.001$** | **Signifikan** | H5 Terpenuhi: $R_0$ unggul atas kontrol acak |
| **Retensi Relatif SNR -5 dB** | $R_2$ (BirdNET) vs $R_1$ (PANNs) | **+0.2244** | **[+0.1182, +0.3217]** | **$p \le 0.001$** | **Signifikan** | H1 Terpenuhi: Retensi $R_2$ (78.0%) unggul atas $R_1$ (55.3%) |
| **Retensi Relatif SNR -5 dB** | $R_1$ (PANNs) vs $R_0$ (MFCC) | **+0.1946** | **[+0.0570, +0.3294]** | **$p = 0.0050$** | **Signifikan** | Retensi $R_1$ (55.3%) unggul atas MFCC (35.9%) |
| **Retensi Relatif SNR -5 dB** | $R_2$ (BirdNET) vs $R_0$ (MFCC) | **+0.4190** | **[+0.3016, +0.5173]** | **$p \le 0.001$** | **Signifikan** | Retensi $R_2$ unggul mutlak atas MFCC baseline |
| **Sensitivitas Habitat E4 (-5 dB)** | $R_2$ (Embung F vs Kebun Raya) | **+0.0398** | **[+0.0142, +0.0677]** | **$p = 0.0040$** | **Signifikan** | Embung F (hidro/angin) lebih ramah bagi BirdNET dibanding biofoni Kebun Raya |
| **Sensitivitas Habitat E4 (-5 dB)** | $R_2$ (Gedung F vs Kebun Raya) | **+0.0214** | **[-0.0021, +0.0442]** | **$p = 0.0880$** | **Tidak Signifikan** | Derau gedung berdampak serupa dengan biofoni |
| **Fluktuasi Rentang Habitat (-5 dB)** | $R_1$ vs $R_2$ (Selisih Ayunan Retensi) | **+0.1692** | **[+0.0795, +0.2646]** | **$p \le 0.001$** | **Signifikan** | H3 Terdukung Parsial: $\Delta_{\text{obs}} = 0.1560$, $R_1$ lebih rentan dibanding $R_2$ |
| **Cluster Bootstrap (per Recordist, K=27)** | $R_2$ vs $R_1$ Retensi (-5 dB) | **+0.2310** | **[+0.1473, +0.3321]** | **$p \le 0.001$** | **Signifikan** | Resampling klaster perekam membuktikan keunggulan $R_2$ bebas bias |
| **Sensitivitas Non-Mike Nelson (N=180)** | $R_2$ vs $R_1$ Retensi (-5 dB) | **+0.2485** | **[+0.1188, +0.3701]** | **$p \le 0.001$** | **Signifikan** | Keunggulan $R_2$ tetap signifikan tanpa perekam dominan (42%) |

### Analisis Temuan Ilmiah Signifikansi Statistik:
1. **Keunggulan Bioakustik Spesifik Terbukti Mutlak ($R_2 > R_1$):**
   * Selisih mAP@10 kondisi bersih sebesar $+0.4609$ memiliki CI 95% $[+0.4260, +0.4986]$ dengan $p \le 0.001$.
2. **Validasi Hipotesis H1 & H2:**
   * Uji retensi ketahanan derau pada SNR -5 dB membuktikan $R_2$ unggul atas $R_1$ ($\Delta = +0.2244$, $p \le 0.001$) dan $R_1$ unggul atas MFCC ($\Delta = +0.1946$, $p = 0.0050$), mengonfirmasi H1 ($R_2 > R_1 > R_0$) dan H2 (kelandaian BirdNET).
3. **Uji Sensitivitas Profil Derau Habitat E4:**
   * Embung F vs Kebun Raya terbukti berbeda secara signifikan ($p = 0.0040$), dengan biofoni serangga Kebun Raya menekan performa BirdNET lebih dalam. Disparitas ayunan retensi lintas habitat membuktikan BirdNET (ayunan 6.39%) jauh lebih stabil dibanding PANNs (ayunan 21.98%, disparitas $\Delta_{\text{obs}} = 0.1560$, bootstrap $+0.1692$, $p \le 0.001$).

---

## 3. Penyiapan Naskah Skripsi, Bahan Sidang, & Pembekuan Repositori

* **Dokumentasi Metodologi & Naskah Lengkap:**
   * Seluruh revisi telah disinkronkan ke dalam naskah utama [`paper/manuscript.md`](../../paper/manuscript.md).
   * Panduan komprehensif Bab 1–5 tersimpan di [`Panduan_Komprehensif_Tugas_Akhir.pdf`](../../Panduan_Komprehensif_Tugas_Akhir.pdf).
* **Inventaris Tabel Publikasi Resmi Bab 4 (`paper/tables/`):**
   1. `clean_retrieval_table.csv` — Tolok ukur dasar E1 (mAP@10, Top-1, MRR).
   2. `snr_robustness_table.csv` — Hasil degradasi E2 lintas grid SNR.
   3. `threshold_transfer_table.csv` — Evaluasi open-set E3 lintas SNR dengan $\tau^*$ beku.
   4. `e4_domain_shift_table.csv` — Evaluasi komparatif E4 sensitivitas habitat kampus ITERA.
   5. `failure_analysis_table.csv` — Audit terstratifikasi 30 kasus kegagalan nyata E5.
   6. `statistical_significance_table.csv` — Uji inferensial bootstrap komprehensif (1.000 iterasi).
* **Inventaris Gambar Publikasi Bab 4 (`paper/figures/`):**
   1. `e2_snr_robustness_curve.png` — Kurva degradasi SNR E2.
   2. `e3_calibration_roc_youden.png` — Kurva kalibrasi ROC dan Youden's Index E3.
   3. `e3_threshold_transfer_snr.png` — Grafik transfer ambang batas E3 lintas SNR.
   4. `e4_noise_profile_sensitivity.png` — Diagram batang sensitivitas profil derau E4.
   5. `e5_failure_analysis.png` — Visualisasi audit kegagalan terstratifikasi E5.
* **Pembekuan Kode (*Code Freeze*) & Reprodusibilitas Penuh:**
   * Seluruh *hash* manifes audio tersinkronisasi di [`artifacts/reproducibility/manifest_sha256.txt`](../../artifacts/reproducibility/manifest_sha256.txt).
   * Seluruh 13 unit test saintifik lolos 100% via `python run_tests.py`.

---

## 4. Kriteria Kelulusan Gate Minggu 4 — 100% Terpenuhi

- [x] **Audit Terstratifikasi Kasus Kegagalan E5 Selesai:** 30 kasus nyata terstratifikasi (Clean & -5 dB) terklasifikasi secara objektif (Open-Set False Rejection 33.3%, Top-1 Confusion Above Tau 30.0%, Total Collapse 36.7%) di [`paper/tables/failure_analysis_table.csv`](../../paper/tables/failure_analysis_table.csv) dan [`notebooks/E5_Failure_Analysis.ipynb`](../../notebooks/E5_Failure_Analysis.ipynb).
- [x] **Uji Statistik Inferensial Komprehensif (1.000 Iterasi) Tuntas:** Seluruh hipotesis diuji dengan Paired Bootstrap, membuktikan $R_2$ unggul ($p \le 0.001$, CI $[+0.4260, +0.4986]$), retensi $R_2$ unggul atas $R_1$ ($p \le 0.001$), retensi $R_1$ unggul atas MFCC ($p = 0.0050$), serta disparitas stabilitas habitat terkonfirmasi ($p \le 0.001$).
- [x] **Seluruh Tabel dan Gambar Publikasi Bab 4 Terintegrasi:** Lengkap di direktori `paper/tables/` dan `paper/figures/`.
- [x] **Naskah Skripsi & Catatan Bimbingan Sinkron:** Seluruh angka di `paper/manuscript.md` dan `Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md` cocok 100% dengan data mentah.
- [x] **Repositori Lolos Uji Integritas 100%:** `python run_tests.py` lolos **13 dari 13 (100%)**.

