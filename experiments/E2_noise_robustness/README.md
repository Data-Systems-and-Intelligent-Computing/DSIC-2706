# Eksperimen E2 — Controlled Noise Robustness

## 1. Tujuan Ilmiah
Menguji ketahanan (*robustness*) representasi audio ketika kueri bersih mengalami degradasi derau lingkungan tropis nyata pada berbagai tingkatan SNR (+20 dB, +10 dB, 0 dB, -5 dB).

## 2. Sumber Derau & Penghapusan Derau Sintetis
* Sesuai mandat keputusan audit **DEC-09**, derau sintetis pink noise telah dihapus permanen dari `src/mix_noise.py`.
* Menggunakan **1.799 berkas audio nyata AudioMoth** (`data/itera_noise/`) dari 5 lokasi kampus ITERA (Masjid At-Tanwir, Embung F, Kebun Raya, Gedung F, dan GKU 1).
* Seluruh berkas telah diverifikasi bebas dari 20 spesies burung target dan diindeks dengan checksum SHA-256 pada [`data/manifests/itera_noise_manifest.csv`](../../data/manifests/itera_noise_manifest.csv).

## 3. Skema Pengujian Terpasang (*Paired Noise Mixing*)
* 311 kueri bersih yang sama dari E1 dipasangkan secara deterministik (`seed=42`) dengan segmen derau AudioMoth.
* Formula pencampuran berbasis daya sinyal eksak:
  $$x_{\text{noisy}} = x_{\text{clean}} + \alpha \cdot n_{\text{noise}}, \quad \alpha = \sqrt{\frac{P_{\text{signal}}}{P_{\text{noise}} \cdot 10^{\text{SNR}/10}}}$$

## 4. Hasil Empiris E2 (`paper/tables/snr_robustness_table.csv`)

| Representasi | Clean | SNR 20 dB | SNR 10 dB | SNR 0 dB | SNR -5 dB | Retensi (-5 dB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET Backbone)** | **0.6370** | **0.6420** | **0.6213** | **0.5679** | **0.4968** | **77.99%** (CI: 74.0% – 82.1%) |
| **$R_1$ (PANNs CNN14)** | 0.1771 | 0.1964 | 0.1857 | 0.1326 | **0.0979** | **55.27%** (CI: 46.5% – 64.0%) |
| **$R_0$ (MFCC Baseline)** | 0.0690 | 0.0774 | 0.0643 | 0.0369 | **0.0248** | **35.89%** (CI: 27.5% – 44.0%) |
| **$R_3$ (Random Control)** | 0.0231 | 0.0189 | 0.0241 | 0.0213 | 0.0230 | 99.44% (Tebakan Acak) |

### Catatan Saintifik:
1. **Keunggulan Bioakustik Spesifik ($R_2$):** $R_2$ mempertahankan retensi tertinggi (77.99% / mAP 0.4968), jauh melampaui seluruh baseline.
2. **Validasi Hipotesis H1 ($R_2 > R_1 > R_0$):** Pada kondisi derau ekstrem (SNR -5 dB), retensi $R_2$ unggul mutlak atas $R_1$ ($\Delta = +0.2244$, $p \le 0.001$), dan retensi $R_1$ (55.27%) unggul atas $R_0$ (35.89%, $\Delta = +0.1946$, $p = 0.0050$).
3. **Pengamatan Empiris SNR +20 dB:** Kenaikan performa pada derau ringan (SNR +20 dB) teramati akibat efek penghalusan spektral derau latar berdaya sangat rendah.

## 5. Artefak Terkait
* Tabel Data: [`paper/tables/snr_robustness_table.csv`](../../paper/tables/snr_robustness_table.csv)
* Grafik Kurva Degradasi: [`paper/figures/e2_snr_robustness_curve.png`](../../paper/figures/e2_snr_robustness_curve.png)
* Notebook Demonstrasi: [`notebooks/E2_Paired_Noise_Degradation.ipynb`](../../notebooks/E2_Paired_Noise_Degradation.ipynb)
* Log Mentah Per-Kueri: `results/raw/R*_SNR_*_raw.csv`

