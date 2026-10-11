# Eksperimen E4 — Evaluasi Sensitivitas Terhadap Profil Spektral Derau Lintas Habitat ITERA

## 1. Tujuan Ilmiah
Mengukur ketahanan dan kepekaan representasi audio ketika berhadapan dengan perbedaan profil spektral derau latar aditif dari 3 habitat lingkungan kampus ITERA yang berbeda secara fisik:
1. **Kebun Raya ITERA** (Vegetasi tropis lebat / didominasi biophony serangga)
2. **Embung F ITERA** (Perairan terbuka / didominasi resonansi air dan angin)
3. **Gedung F ITERA** (Koridor struktural / didominasi derau antropogenik)

## 2. Metodologi Eksperimen & Batasan Ilmiah
* **Protokol Pencampuran Aditif Terkontrol:** Segmen 5,0 detik dari berkas derau fisik AudioMoth ITERA (bebas dari 271 berkas negatif E3) dicampurkan ke 310 kueri bersih avifauna Indonesia pada grid SNR: Clean, +20 dB, +10 dB, 0 dB, dan -5 dB (`seed=5000+i`).
* **Batasan Saintifik Terbuka (*Research Limitation*):** Eksperimen ini mengevaluasi kepekaan terhadap variasi spektral derau latar secara terkontrol (*noise spectral profile sensitivity*). Pergeseran domain in-situ penuh (termasuk jarak mikrofon, redaman vegetasi, dan multi-sumber simultan) ditangguhkan sebagai penelitian lanjutan karena memerlukan set data soundscape lapangan yang teranotasi lengkap.

## 3. Hasil Empiris Komparatif Seluruh Representasi (`paper/tables/e4_domain_shift_table.csv`)

| Representasi | Kondisi | Kebun Raya (mAP@10) | Embung F (mAP@10) | Gedung F (mAP@10) | Karakteristik Pergeseran |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **$R_2$ (BirdNET)** | Clean | 0.6358 | 0.6358 | 0.6358 | Baseline Identik |
| | SNR +20 dB | 0.6420 | 0.6405 | 0.6334 | Sangat Stabil |
| | SNR +10 dB | 0.6108 | 0.6250 | 0.6194 | Sangat Stabil |
| | SNR 0 dB | 0.5186 | 0.5651 | 0.5486 | Konsisten |
| | **SNR -5 dB** | **0.4434** | **0.4842** | **0.4661** | **Invarian Lintas Habitat ($p = 0.610$)** |
| **$R_1$ (PANNs)** | Clean | 0.1768 | 0.1768 | 0.1768 | Baseline Identik |
| | SNR +20 dB | 0.1765 | 0.1852 | 0.1894 | Stabil |
| | SNR +10 dB | 0.1460 | 0.1718 | 0.1909 | Disparitas Muncul |
| | SNR 0 dB | 0.0873 | 0.1158 | 0.1321 | Tertekan |
| | **SNR -5 dB** | **0.0590** | **0.0949** | **0.0982** | **Sangat Sensitif ($p < 0.001$)** |
| **$R_0$ (MFCC)** | Clean | 0.0691 | 0.0691 | 0.0691 | Baseline Identik |
| | SNR -5 dB | 0.0228 | 0.0263 | 0.0188 | Tertekan Rendah |
| **$R_3$ (Random)**| Clean | 0.0232 | 0.0232 | 0.0232 | Baseline Kontrol |
| | SNR -5 dB | 0.0203 | 0.0218 | 0.0184 | Peluang Acak |

## 4. Analisis Temuan Saintifik
* **$R_2$ (BirdNET Backbone):** Membuktikan stabilitas tinggi di ketiga habitat derau ITERA. Penurunan performa pada SNR -5 dB tidak berbeda secara signifikan antar ketiga habitat ($p = 0.610$). Fitur bioakustik laten BirdNET terlatih mengenali sinyal burung tanpa terdistorsi oleh perbedaan warna derau latar (biophony vs resonansi angin vs antropogenik).
* **$R_1$ (PANNs CNN14):** Sangat rentan terhadap perbedaan profil spektral ($p < 0.001$). Derau vegetasi Kebun Raya (didominasi energi frekuensi tinggi serangga) merontokkan mAP@10 PANNs secara signifikan lebih parah (0.0590) dibandingkan derau koridor Gedung F (0.0982).
* **$R_0$ (MFCC):** Mengalami penurunan performa drastis di seluruh habitat pada SNR -5 dB (mAP@10 $\le 0.026$), menegaskan bahwa fitur koefisien cepstral klasik tidak memiliki daya tahan representasional terhadap derau lingkungan tropis.

## 5. Artefak Terkait
* Tabel Komparasi: [`paper/tables/e4_domain_shift_table.csv`](../../paper/tables/e4_domain_shift_table.csv)
* Grafik Komparasi: [`paper/figures/e4_noise_profile_sensitivity.png`](../../paper/figures/e4_noise_profile_sensitivity.png)
* Log Mentah Per-Kueri: [`results/raw/E4_R0_raw.csv`](../../results/raw/E4_R0_raw.csv) s/d [`results/raw/E4_R3_raw.csv`](../../results/raw/E4_R3_raw.csv) (memuat kolom `noise_file`)
* Notebook Demonstrasi: [`notebooks/E4_Real_Soundscape_Domain_Shift.ipynb`](../../notebooks/E4_Real_Soundscape_Domain_Shift.ipynb)
