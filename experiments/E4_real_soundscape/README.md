# Eksperimen E4 — Evaluasi Sensitivitas Terhadap Profil Spektral Derau Latar

## 1. Tujuan Ilmiah
Mengukur sensitivitas representasi audio ketika berhadapan dengan perbedaan profil spektral derau latar aditif: **Derau Lingkungan Kampus ITERA (E2)** vs **Derau Biophony Soundscape Alami Hutan Tropis (E4, dari BirdCLEF `train_soundscapes/`)**.

## 2. Metodologi Eksperimen & Batasan Ilmiah Terbuka
* **Protokol Pencampuran Aditif Terkontrol:** Segmen acak 5,0 detik dari berkas soundscape hutan tropis disuntikkan ke 200 kueri bersih pada grid SNR yang persis sama dengan E2: Clean, 20 dB, 10 dB, 0 dB, dan -5 dB (`seed=42`).
* **Batasan Saintifik Terbuka (*Research Limitation*):** Eksperimen ini mengevaluasi sensitivitas terhadap *noise spectral profile shift* secara aditif. Pengujian *in-situ domain shift* sesungguhnya (melibatkan efek jarak propagasi, redaman kanopi, dan reverberasi lingkungan) ditangguhkan sebagai agenda penelitian masa depan karena dataset `data/itera_soundscape_annotations/` saat ini belum memiliki anotasi *ground-truth*. Selain itu, rekaman soundscape hutan secara alami mengandung suara burung liar latar belakang non-target.
* **Status Hipotesis H3:** Dinyatakan secara jujur dan transparan sebagai **Tidak Diuji (Deferred)** karena pengujian H3 secara formal mensyaratkan ketersediaan anotasi soundscape lapangan ITERA.

## 3. Hasil Empiris Komparatif Seluruh Representasi (`paper/tables/e4_domain_shift_table.csv`)

| Representasi | Kondisi | $mAP@10$ (ITERA / E2) | $mAP@10$ (Soundscape / E4) | Selisih ($\Delta mAP$) | Retensi E2 | Retensi E4 | Karakteristik Pergeseran |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **$R_2$ (BirdNET)** | Clean | 0.9126 | 0.9126 | 0.0000 | 100.0% | 100.0% | Baseline Identik |
| | SNR +20 dB | 0.9068 | 0.9188 | +0.0121 | 99.36% | 100.68% | Sangat Stabil |
| | SNR +10 dB | 0.8858 | 0.9026 | +0.0169 | 97.06% | 98.91% | Sangat Stabil |
| | SNR 0 dB | 0.8317 | 0.8299 | -0.0018 | 91.13% | 90.94% | Identik |
| | **SNR -5 dB** | **0.7707** | **0.7606** | **-0.0101** | **84.45%** | **83.34%** | **Invarian Profil Derau ($p = 0.610$)** |
| **$R_1$ (PANNs)** | Clean | 0.4152 | 0.4152 | 0.0000 | 100.0% | 100.0% | Baseline Identik |
| | SNR +20 dB | 0.4533 | 0.3816 | -0.0717 | 109.16% | 91.89% | Sensitif |
| | SNR +10 dB | 0.3700 | 0.2922 | -0.0778 | 89.11% | 70.36% | Sensitif |
| | SNR 0 dB | 0.1290 | 0.1918 | +0.0628 | 31.06% | 46.19% | Disparitas Tinggi |
| | **SNR -5 dB** | **0.0590** | **0.1480** | **+0.0890** | **14.22%** | **35.64%** | **Sangat Sensitif ($p < 0.001$)** |
| **$R_0$ (MFCC)** | Clean | 0.1319 | 0.1319 | 0.0000 | 100.0% | 100.0% | Baseline Identik |
| | SNR -5 dB | 0.0349 | 0.0364 | +0.0016 | 26.42% | 27.62% | Penurunan Serupa |
| **$R_3$ (Random)**| Clean | 0.0190 | 0.0190 | 0.0000 | 100.0% | 100.0% | Kontrol Acak |
| | SNR -5 dB | 0.0165 | 0.0171 | +0.0006 | 86.71% | 90.12% | Peluang Acak |

## 4. Analisis Temuan Saintifik
* **$R_2$ (BirdNET):** Pada kondisi derau ekstrem (-5 dB), performa BirdNET terhadap derau soundscape hutan tropis hanya berselisih **-0.0101** dibanding derau kampus ITERA. Uji paired bootstrap menunjukkan selisih ini **tidak signifikan secara statistik ($p = 0.6100$, 95% CI $[-0.0479, +0.0275]$)**. Meskipun demikian, secara epistemologis hal ini tidak membuktikan kesetaraan mutlak (*equivalence*).
* **$R_1$ (PANNs):** Sangat rentan terhadap perbedaan spektrum derau latar. Terdapat kesenjangan signifikan sebesar **+0.0890** ($p < 0.001$, 95% CI $[+0.0572, +0.1210]$), di mana PANNs rontok jauh lebih parah pada derau kampus ITERA (0.0590) dibanding pada derau soundscape hutan (0.1480).

## 5. Artefak Terkait
* Tabel Komparasi: [`paper/tables/e4_domain_shift_table.csv`](../../paper/tables/e4_domain_shift_table.csv)
* Grafik Komparasi: [`paper/figures/e4_noise_profile_sensitivity.png`](../../paper/figures/e4_noise_profile_sensitivity.png)
* Log Mentah Per-Kueri: [`results/raw/E4_R0_raw.csv`](../../results/raw/E4_R0_raw.csv) s/d [`results/raw/E4_R3_raw.csv`](../../results/raw/E4_R3_raw.csv)
* Notebook Demonstrasi: [`notebooks/E4_Real_Soundscape_Domain_Shift.ipynb`](../../notebooks/E4_Real_Soundscape_Domain_Shift.ipynb)

