# Eksperimen E5 — Failure Analysis

## 1. Tujuan Ilmiah
Mengaudit dan mendiagnosis secara sistematis kasus-kasus di mana sistem retrieval mengalami kegagalan penemuan ($Top\text{-}1\text{ match} = 0$ atau $\max_g \text{Sim} < \tau^*$) dari hasil evaluasi kueri nyata pada kondisi batas Clean dan SNR -5 dB.

## 2. Metodologi Audit Terstratifikasi Lintas Spesies
* Mengambil sampel acak terstratifikasi sebanyak **30 kasus kegagalan nyata** lintas 16 taksa burung berbeda menggunakan [`src/analyze_failures.py`](../../src/analyze_failures.py):
  * **Kondisi Clean (10 kasus):** 5 spesies unik $R_2$ (BirdNET) + 5 spesies unik $R_1$ (PANNs).
  * **Kondisi SNR -5 dB (20 kasus):** 10 spesies unik $R_2$ (BirdNET) + 10 spesies unik $R_1$ (PANNs).
* Mengukur parameter fisik akustik terukur: frekuensi pusat spektral (*spectral centroid*), lebar pita (*bandwidth*), selisih skor terhadap ambang batas (*margin to tau*), dan selisih kemiripan terhadap taksa target (*retrieval gap*).

## 3. Hasil Distribusi Taksonomi Kegagalan (`paper/tables/failure_analysis_table.csv`)

| Kategori Taksonomi Kegagalan | Proporsi (%) | Jumlah Kasus | Sebaran Model & Kondisi | Karakteristik Bioakustik Utama |
| :--- | :---: | :---: | :--- | :--- |
| **1. Top-1 Confusion (Above Tau)** | **36.67%** | **11 kasus** | • $R_1$ Clean (2)<br>• $R_1$ SNR -5 dB (9) | Skor kemiripan melampaui $\tau^*$, namun sistem mencocokkan taksa galeri yang keliru akibat kedekatan manifold laten generik ($R_1$). |
| **2. Open-Set False Rejection** | **36.67%** | **11 kasus** | • $R_2$ Clean (3)<br>• $R_2$ SNR -5 dB (8) | Top-1 kueri benar mencocokkan taksa target, namun skor kemiripan tertekan sedikit di bawah $\tau^*$ akibat atenuasi energi derau atau variasi vokal. |
| **3. Total Retrieval Collapse** | **26.67%** | **8 kasus** | • $R_2$ Clean (2)<br>• $R_1$ Clean (3)<br>• $R_2$ SNR -5 dB (2)<br>• $R_1$ SNR -5 dB (1) | Kegagalan ganda di mana skor kemiripan anjlok di bawah ambang batas $\tau^*$ DAN Top-1 memprediksi taksa yang keliru. |

## 4. Evaluasi Statistik Inferensial (Paired Bootstrap 1.000 Iterasi)
* Paired Bootstrap Resampling 1.000 iterasi pada 200 kueri evaluasi (`seed=42`) via [`src/bootstrap_inference.py`](../../src/bootstrap_inference.py):
  * **$R_2$ vs $R_1$ (Clean mAP@10):** Rata-rata $\Delta = \mathbf{+0.4981}$, CI 95% **$[+0.4504, +0.5473]$**, **$p < 0.001$** (Signifikan).
  * **Retensi SNR -5 dB ($R_0$ vs $R_1$):** Rata-rata $\Delta = \mathbf{+0.1223}$, CI 95% **$[+0.0581, +0.1994]$**, **$p < 0.001$** (Retensi MFCC mengungguli PANNs secara signifikan).
  * **Sensitivitas Derau E4 vs E2 ($R_2$):** Rata-rata $\Delta = \mathbf{-0.0097}$, CI 95% **$[-0.0479, +0.0275]$**, **$p = 0.6100$** (Invarian profil derau).

## 5. Artefak Terkait
* Tabel Kasus: [`paper/tables/failure_analysis_table.csv`](../../paper/tables/failure_analysis_table.csv)
* Tabel Statistik: [`paper/tables/statistical_significance_table.csv`](../../paper/tables/statistical_significance_table.csv)
* Gambar Visualisasi: [`paper/figures/e5_failure_analysis.png`](../../paper/figures/e5_failure_analysis.png)
* Notebook Demonstrasi: [`notebooks/E5_Failure_Analysis.ipynb`](../../notebooks/E5_Failure_Analysis.ipynb)
* Skrip Eksekutor: [`src/analyze_failures.py`](../../src/analyze_failures.py)

