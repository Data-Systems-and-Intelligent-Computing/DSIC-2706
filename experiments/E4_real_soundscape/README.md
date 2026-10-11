# Eksperimen E4 — Evaluasi Sensitivitas Terhadap Profil Spektral Derau Lintas Habitat ITERA

## 1. Tujuan Ilmiah
Mengukur ketahanan dan kepekaan representasi audio ketika berhadapan dengan perbedaan profil spektral derau latar aditif dari 3 habitat lingkungan kampus ITERA yang berbeda secara fisik:
1. **Kebun Raya ITERA** (Vegetasi tropis lebat / didominasi biophony serangga)
2. **Embung F ITERA** (Perairan terbuka / didominasi resonansi air dan angin)
3. **Gedung F ITERA** (Koridor struktural / didominasi derau antropogenik)

## 2. Metodologi Eksperimen & Batasan Ilmiah
* **Protokol Pencampuran Aditif Terkontrol:** Segmen 5,0 detik dari berkas derau fisik AudioMoth ITERA (bebas dari 271 berkas negatif E3) dicampurkan ke 311 kueri bersih avifauna Indonesia pada grid SNR: Clean, +20 dB, +10 dB, 0 dB, dan -5 dB (`seed=5000+i`).
* **Batasan Saintifik Terbuka (*Research Limitation*):** Eksperimen ini mengevaluasi kepekaan terhadap variasi spektral derau latar secara terkontrol (*noise spectral profile sensitivity*). Pergeseran domain in-situ penuh (termasuk jarak mikrofon, redaman vegetasi, dan multi-sumber simultan) ditangguhkan sebagai penelitian lanjutan karena memerlukan set data soundscape lapangan yang teranotasi lengkap.

## 3. Hasil Empiris Komparatif Seluruh Representasi (`paper/tables/e4_domain_shift_table.csv`)

| Representasi | Kondisi | Kebun Raya (mAP@10) | Embung F (mAP@10) | Gedung F (mAP@10) | Karakteristik Pergeseran |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **$R_2$ (BirdNET)** | Clean | 0.6370 | 0.6370 | 0.6370 | Baseline Identik |
| | SNR +20 dB | 0.6431 | 0.6416 | 0.6345 | Sangat Stabil |
| | SNR +10 dB | 0.6119 | 0.6262 | 0.6205 | Sangat Stabil |
| | SNR 0 dB | 0.5197 | 0.5661 | 0.5494 | Penurunan Bertahap |
| | **SNR -5 dB** | **0.4446** | **0.4853** | **0.4667** | **Sensitif Biofoni ($p = 0.0040$, Ayunan 6.39%)** |
| **$R_1$ (PANNs)** | Clean | 0.1771 | 0.1771 | 0.1771 | Baseline Identik |
| | SNR +20 dB | 0.1767 | 0.1854 | 0.1894 | Stabil |
| | SNR +10 dB | 0.1462 | 0.1719 | 0.1908 | Disparitas Muncul |
| | SNR 0 dB | 0.0873 | 0.1159 | 0.1317 | Tertekan |
| | **SNR -5 dB** | **0.0590** | **0.0948** | **0.0979** | **Sangat Sensitif ($p \le 0.001$, Ayunan 21.98%)** |
| **$R_0$ (MFCC)** | Clean | 0.0690 | 0.0690 | 0.0690 | Baseline Identik |
| | SNR -5 dB | 0.0228 | 0.0264 | 0.0189 | Tertekan Rendah |
| **$R_3$ (Random)**| Clean | 0.0231 | 0.0231 | 0.0231 | Baseline Kontrol |
| | SNR -5 dB | 0.0203 | 0.0218 | 0.0184 | Peluang Acak |

## 4. Analisis Temuan Saintifik
* **$R_2$ (BirdNET Backbone):** Biofoni serangga berdaya tinggi (2–6 kHz) di Kebun Raya mendegradasi BirdNET paling signifikan dibandingkan Embung F ($\Delta = +0.0398$, $p = 0.0040$). Meskipun demikian, rentang ayunan retensi BirdNET hanya **6.39%**, membuktikan ketahanan filternya yang terfokus pada kontur harmonik vokal burung dibanding model generik.
* **$R_1$ (PANNs CNN14):** Sangat rentan terhadap perbedaan profil spektral ($p \le 0.001$), dengan rentang ayunan retensi mencapai **21.98%**. Derau vegetasi Kebun Raya (didominasi energi serangga) merontokkan mAP@10 PANNs secara signifikan lebih parah (0.0590) dibandingkan derau koridor Gedung F (0.0979). Disparitas stabilitas ayunan $R_1$ vs $R_2$ terbukti signifikan ($\Delta_{\text{obs}} = 0.1560$, bootstrap $+0.1692$, $p \le 0.001$).
* **$R_0$ (MFCC):** Mengalami penurunan performa drastis di seluruh habitat pada SNR -5 dB (mAP@10 $\le 0.0264$), menegaskan bahwa fitur koefisien cepstral klasik tidak memiliki daya tahan representasional terhadap derau lingkungan tropis.

## 5. Artefak Terkait
* Tabel Komparasi: [`paper/tables/e4_domain_shift_table.csv`](../../paper/tables/e4_domain_shift_table.csv)
* Grafik Komparasi: [`paper/figures/e4_noise_profile_sensitivity.png`](../../paper/figures/e4_noise_profile_sensitivity.png)
* Log Mentah Per-Kueri: [`results/raw/E4_R0_raw.csv`](../../results/raw/E4_R0_raw.csv) s/d [`results/raw/E4_R3_raw.csv`](../../results/raw/E4_R3_raw.csv) (memuat kolom `noise_file`)
* Notebook Demonstrasi: [`notebooks/E4_Real_Soundscape_Domain_Shift.ipynb`](../../notebooks/E4_Real_Soundscape_Domain_Shift.ipynb)
