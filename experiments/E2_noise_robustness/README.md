# Eksperimen E2 — Controlled Noise Robustness

## 1. Tujuan Ilmiah
Menguji ketahanan (*robustness*) representasi audio ketika kueri bersih mengalami degradasi derau lingkungan tropis nyata pada berbagai tingkatan SNR (+20 dB, +10 dB, 0 dB, -5 dB).

## 2. Sumber Derau & Penghapusan Derau Sintetis
* Sesuai mandat keputusan audit **DEC-09**, derau sintetis pink noise telah dihapus permanen dari `src/mix_noise.py`.
* Menggunakan **1.799 berkas audio nyata AudioMoth** (`data/itera_noise/`) dari 5 lokasi kampus ITERA (Masjid At-Tanwir, Embung F, Kebun Raya, Gedung F, dan GKU 1).
* Seluruh berkas telah diverifikasi bebas dari 20 spesies burung target dan diindeks dengan checksum SHA-256 pada [`data/manifests/itera_noise_manifest.csv`](../../data/manifests/itera_noise_manifest.csv).

## 3. Skema Pengujian Terpasang (*Paired Noise Mixing*)
* 200 kueri bersih yang sama dari E1 dipasangkan secara deterministik (`seed=42`) dengan segmen derau AudioMoth.
* Formula pencampuran berbasis daya sinyal eksak:
  $$x_{\text{noisy}} = x_{\text{clean}} + \alpha \cdot n_{\text{noise}}, \quad \alpha = \sqrt{\frac{P_{\text{signal}}}{P_{\text{noise}} \cdot 10^{\text{SNR}/10}}}$$

## 4. Hasil Empiris E2 (`paper/tables/snr_robustness_table.csv`)

| Representasi | Clean | SNR 20 dB | SNR 10 dB | SNR 0 dB | SNR -5 dB | Retensi (-5 dB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET Backbone)** | **0.9126** | **0.9068** | **0.8858** | **0.8317** | **0.7707** | **84.45%** (CI: 80.6% – 88.3%) |
| **$R_1$ (PANNs CNN14)** | 0.4152 | 0.4533 | 0.3700 | 0.1290 | **0.0590** | **14.22%** (CI: 10.1% – 18.6%) |
| **$R_0$ (MFCC Baseline)** | 0.1319 | 0.1320 | 0.1022 | 0.0587 | **0.0349** | **26.42%** (CI: 20.8% – 33.4%) |
| **$R_3$ (Random Control)** | 0.0190 | 0.0158 | 0.0148 | 0.0142 | 0.0165 | - |

### Catatan Saintifik:
1. **Keunggulan Bioakustik Spesifik ($R_2$):** $R_2$ mempertahankan retensi tertinggi (84.45%), jauh melampaui seluruh baseline.
2. **Koreksi Hipotesis H1 ($R_1$ vs $R_0$):** Pada kondisi derau ekstrem (SNR -5 dB), retensi relatif PANNs ($R_1$, 14.22%) justru **kalah signifikan** dari baseline klasik MFCC ($R_0$, 26.42%) dengan selisih $+0.1223$ ($p < 0.001$, CI 95% $[+0.0581, +0.1994]$). Ini menunjukkan bahwa fitur konvolusi generic audio rentan terhadap distorsi derau lingkungan pada rasio sinyal-ke-derau negatif.
3. **Pengamatan Empiris SNR +20 dB:** Kenaikan performa $R_1$ pada SNR +20 dB (0.4533 vs 0.4152 Clean) dicatat sebagai pengamatan empiris yang belum terjelaskan secara definitif (*unexplained empirical observation*).

## 5. Artefak Terkait
* Tabel Data: [`paper/tables/snr_robustness_table.csv`](../../paper/tables/snr_robustness_table.csv)
* Grafik Kurva Degradasi: [`paper/figures/e2_snr_robustness_curve.png`](../../paper/figures/e2_snr_robustness_curve.png)
* Notebook Demonstrasi: [`notebooks/E2_Paired_Noise_Degradation.ipynb`](../../notebooks/E2_Paired_Noise_Degradation.ipynb)
* Log Mentah Per-Kueri: `results/raw/R*_SNR_*_raw.csv`

