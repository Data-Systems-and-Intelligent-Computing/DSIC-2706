# Eksperimen E5 — Failure Analysis

## 1. Tujuan Ilmiah
Mengaudit dan mendiagnosis secara sistematis kasus-kasus di mana sistem retrieval mengalami kegagalan penemuan ($Top\text{-}1\text{ match} = 0$) dari hasil evaluasi kueri nyata pada kondisi batas SNR -5 dB dan Clean.

## 2. Metodologi Audit
* Mengekstraksi 30 kasus kueri gagal nyata menggunakan [`src/analyze_failures.py`](../../src/analyze_failures.py).
* Menghubungkan setiap kueri gagal dengan metadata rekaman asli di `data/manifests/dataset_split.csv`.
* Mengklasifikasikan kegagalan ke dalam kategori akustik diagnostik independen.

## 3. Hasil Distribusi Kasus Kegagalan (`paper/tables/failure_analysis_table.csv`)

| Kategori Diagnosis Kegagalan | Proporsi (%) | Jumlah Kasus | Karakteristik Akustik Utama |
| :--- | :---: | :---: | :--- |
| **1. Low SNR Masking** | **66.67%** | 20 kasus | Terjadi pada SNR -5 dB dan 0 dB saat energi derau aditif menutupi struktur formulan vokal burung. |
| **2. Acoustic Feature Overlap** | **20.00%** | 6 kasus | Terjadi pada kondisi Clean saat vokal burung target memiliki keserupaan akustik tinggi dengan spesies sepupu pada galeri. |
| **3. Inter-Species Confusion / Short Call** | **13.33%** | 4 kasus | Durasi kicauan sangat singkat (< 1.0 detik) dalam jendela 5,0 detik sehingga energi vokal kalah dominan dibanding latar. |

## 4. Evaluasi Statistik Inferensial (Bootstrap Resampling)
* 1.000 iterasi Paired Bootstrap Resampling antara $R_2$ (BirdNET) vs $R_1$ (PANNs CNN14):
  * Rata-rata $\Delta mAP@10$: **+0.4974**
  * 95% Confidence Interval: **[+0.4285, +0.5621]**
  * Nilai Empiris $p$-value: **0.0000** ($p < 0.05$, Signifikan Mutlak).

## 5. Artefak Terkait
* Tabel Kasus: [`paper/tables/failure_analysis_table.csv`](../../paper/tables/failure_analysis_table.csv)
* Tabel Statistik: [`paper/tables/statistical_significance_table.csv`](../../paper/tables/statistical_significance_table.csv)
* Notebook Demonstrasi: [`notebooks/E5_Failure_Analysis.ipynb`](../../notebooks/E5_Failure_Analysis.ipynb)
* Skrip Diagnostik: [`src/analyze_failures.py`](../../src/analyze_failures.py)
