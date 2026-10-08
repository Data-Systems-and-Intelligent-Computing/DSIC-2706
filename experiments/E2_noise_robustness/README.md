# Eksperimen E2 — Controlled Noise Robustness

## 1. Tujuan Ilmiah
Menguji ketahanan (*robustness*) representasi audio ketika kueri bersih mengalami degradasi derau lingkungan tropis nyata pada berbagai tingkatan SNR (+20 dB, +10 dB, 0 dB, -5 dB).

## 2. Sumber Derau & Penghapusan Derau Sintetis
* Sesuai mandat keputusan audit **DEC-09**, derau sintetis pink noise telah dihapus permanen dari `src/mix_noise.py`.
* Menggunakan **1.799 berkas audio nyata AudioMoth** (`data/itera_noise/`) dari 5 lokasi kampus ITERA (Masjid At-Tanwir, Embung E, Kebun Raya, Gedung F, dan GKU 1).
* Seluruh berkas telah diverifikasi bebas dari suara burung target dan diindeks dengan checksum SHA-256 pada [`data/manifests/itera_noise_manifest.csv`](../../data/manifests/itera_noise_manifest.csv).

## 3. Skema Pengujian Terpasang (*Paired Noise Mixing*)
* 200 kueri bersih yang sama dari E1 dipasangkan secara deterministik (`seed=42`) dengan segmen derau AudioMoth.
* Formula pencampuran berbasis daya sinyal eksak:
  $$x_{\text{noisy}} = x_{\text{clean}} + \alpha \cdot n_{\text{noise}}, \quad \alpha = \sqrt{\frac{P_{\text{signal}}}{P_{\text{noise}} \cdot 10^{\text{SNR}/10}}}$$

## 4. Hasil Empiris E2 (`paper/tables/snr_robustness_table.csv`)

| Representasi | Clean | SNR 20 dB | SNR 10 dB | SNR 0 dB | SNR -5 dB | Retensi (-5 dB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET Backbone)** | **0.9126** | **0.9068** | **0.8858** | **0.8317** | **0.7707** | **84.45%** |
| **$R_1$ (PANNs CNN14)** | 0.4152 | 0.3816 | 0.2922 | 0.1918 | 0.1480 | 35.65% |
| **$R_0$ (MFCC Baseline)** | 0.1319 | 0.1244 | 0.0765 | 0.0502 | 0.0364 | 27.60% |
| **$R_3$ (Random Control)** | 0.0190 | 0.0137 | 0.0134 | 0.0160 | 0.0171 | - |

## 5. Artefak Terkait
* Tabel Data: [`paper/tables/snr_robustness_table.csv`](../../paper/tables/snr_robustness_table.csv)
* Grafik Kurva Degradasi: [`paper/figures/e2_snr_robustness_curve.png`](../../paper/figures/e2_snr_robustness_curve.png)
* Notebook Demonstrasi: [`notebooks/E2_Paired_Noise_Degradation.ipynb`](../../notebooks/E2_Paired_Noise_Degradation.ipynb)
* Log Mentah Per-Kueri: `results/raw/R*_SNR_*_raw.csv`
