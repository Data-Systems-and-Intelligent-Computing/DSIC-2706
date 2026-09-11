# Rencana Eksperimen — Minggu 2 (GATE 2)
**Fokus:** Controlled Noise Robustness (Paired SNR Stress-Testing)  
**Target Garis Waktu:** Minggu Ke-2  
**Status Eksekusi:** **BELUM DILAKUKAN (TAHAP MENDATANG / TERJADWAL)**  

---

## Target Rencana Kerja Minggu 2

### 1. Perancangan Modul Mixing Derau Terkendali (Reproducible Noise Mixing)
* **Tujuan:** Menguji ketahanan representasi audio ($R_0, R_1, R_2, R_3$) ketika rekaman audio terdegradasi oleh derau lingkungan.
* **Formulasi Derau Aditif Berbasis RMS:**
  $$\text{SNR}_{\text{dB}} = 10 \log_{10}\left(\frac{P_{\text{signal}}}{P_{\text{noise}}}\right)$$
* **Tingkatan Level Derau yang Direncanakan:**
  1. Clean (Kondisi dasar tanpa derau tambahan, baseline dari Gate 1)
  2. SNR 20 dB (Derau ringan)
  3. SNR 10 dB (Derau sedang)
  4. SNR 0 dB (Sinyal dan derau berkekuatan sama)
  5. SNR -5 dB (Derau berat / ekstrem, mendominasi sinyal burung)
* **Kriteria Pengujian Berpasangan (*Paired Test*):** Seluruh query audio diuji secara deterministik dengan seed acak yang dibekukan (`seed=42`).

---

### 2. Eksperimen E2: Evaluasi Temu Kembali di Bawah Derau
* **Model yang Diuji:**
  * $R_0$: MFCC Handcrafted Baseline (40-dim)
  * $R_1$: PANNs CNN14 Generic Pretrained (2048-dim)
  * $R_2$: BirdNET V2.4 Bioacoustic Backbone (1024-dim)
  * $R_3$: Random Control (40-dim)
* **Metrik yang Akan Diukur:**
  * Degradasi $mAP@10$ dan Top-1 Accuracy pada tiap level SNR.
  * Retensi performa relatif: $\text{Retention} = \frac{mAP@10(\text{SNR})}{mAP@10(\text{Clean})} \times 100\%$.
* **Hipotesis yang Diuji (H2):** Model bioakustik ($R_2$) mampu mempertahankan retensi relatif lebih baik daripada model generik ($R_1$) saat SNR turun hingga -5 dB.

---

## Kriteria Kelulusan Gate Minggu 2
* Penurunan performa terpantau bertahap (tidak ada *floor* mendadak atau *ceiling* buatan).
* Kontrol acak ($R_3$) tetap berada di batas bawah pada seluruh level SNR.
* Berkas hasil pemeringkatan mentah per-kueri tersimpan secara reproduktif.

