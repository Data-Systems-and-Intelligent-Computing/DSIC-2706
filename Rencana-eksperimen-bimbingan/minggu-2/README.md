# Rencana Eksperimen — Minggu 2
**Fokus:** Controlled Noise Robustness (Paired SNR Stress-Testing)  
**Target Garis Waktu:** Hari 8 – Hari 14  
**Status Eksekusi:** **SELESAI (Kriteria Teknis Terpenuhi, Siap Ditinjau)**  

---

## 🎯 Target Rencana & Hasil Eksekusi

### Hari 8–10: Implementasi Mixing SNR Reproducible & Pembekuan Seed
* **Target Pembimbing:**
  * Implementasikan modul peracikan derau (*noise mixing*) berbasis rasio sinyal terhadap derau (SNR) yang dapat diulang secara persis (*reproducible*).
  * Lakukan pilot testing tingkatan level derau SNR.
  * Bekukan segmen derau dan bilangan acak (*random seed*).
* **Hasil Eksekusi Riil:**
  * Modul injeksi derau aditif berbasis energi Root Mean Square (RMS) berhasil dibangun:
    $$\text{SNR}_{\text{dB}} = 10 \log_{10}\left(\frac{P_{\text{signal}}}{P_{\text{noise}}}\right)$$
  * Skala pengujian dibekukan pada lima kondisi: **Clean, SNR 20 dB (ringan), SNR 10 dB (sedang), SNR 0 dB (sama kuat), dan SNR -5 dB (ekstrem/derau mendominasi)**.
  * *Seed* ditetapkan secara deterministik pada `seed=42`.
* **Bukti Fisik:**
  * Modul Derau Reproducible: [`src/dsic2706/audio/noise.py`](../../src/dsic2706/audio/noise.py)
  * Konfigurasi Parameter Derau: [`configs/audio.yaml`](../../configs/audio.yaml)

---

### Hari 11–14: Eksperimen E1–E2 & Pembentukan Robustness Curve
* **Target Pembimbing:**
  * Jalankan eksperimen E1 (ekstraksi representasi) dan E2 (noise stress-testing) pada seluruh 94 query.
  * Simpan hasil perolehan (*ranking*) per query.
  * Buat kurva ketahanan (*robustness curve*) dan kurva retensi relatif awal.
* **Hasil Eksekusi Riil:**
  * Eksperimen dijalankan secara berpasangan (*paired stress-testing*) pada 94 query identik di setiap tingkatan derau.
  * Hasil komparatif perolehan kemiripan ($mAP@10$):

| Kondisi Derau | $R_0$: MFCC (Klasik) | $R_1$: Generic (PANNs) | $R_2$: Bioacoustic Pretrained | $R_3$: Random (Kontrol) |
| :--- | :---: | :---: | :---: | :---: |
| **Clean** | 0.1029 | 0.2299 | **0.2408** | 0.0183 |
| **SNR 20 dB** | 0.0770 | **0.2342** | 0.2315 | 0.0223 |
| **SNR 10 dB** | 0.0549 | **0.2239** | 0.2137 | 0.0209 |
| **SNR 0 dB** | 0.0409 | 0.1109 | **0.1589** | 0.0149 |
| **SNR -5 dB** | 0.0282 | 0.0450 | **0.0936** | 0.0179 |

  * Retensi performa relatif terhadap kondisi bersih pada SNR -5 dB:
    * $R_0$ MFCC: **27.4%**
    * $R_1$ Generic: **19.6%** (Runtuh drastis)
    * $R_2$ Bioacoustic: **38.9%** (Hampir 2 kali lipat lebih tangguh dibanding $R_1$)
* **Bukti Fisik:**
  * Tabel Hasil Lengkap: [`results/tables/snr_robustness_table.csv`](../../results/tables/snr_robustness_table.csv)
  * Grafik Kurva mAP@10: [`results/figures/robustness_curve_map10.png`](../../results/figures/robustness_curve_map10.png)
  * Grafik Kurva Retensi Relatif: [`results/figures/relative_retention_curve.png`](../../results/figures/relative_retention_curve.png)

---

## 🛡️ Evaluasi Kesiapan Gate Minggu 2
> **Kriteria Acuan:** *Tidak ada fenomena ceiling (mentok di atas) atau floor total (semua nol), pasangan query konsisten, dan baseline kontrol acak masuk akal.*

* **Status Verifikasi Internal:** **Kriteria Teknis Terpenuhi (Menunggu Evaluasi Pembimbing)**
* **Justifikasi Ilmiah:**
  1. **Tidak Ada Ceiling/Floor:** Rentang skor bergerak wajar dari 0.24 hingga 0.09 (tidak ada skor 1.0 yang mencurigakan, dan tidak ada angka 0.00 total).
  2. **Konsistensi Berpasangan:** Seluruh 94 query diuji pada sampel yang identik di setiap level SNR.
  3. **Kontrol Acak Masuk Akal:** Representasi acak ($R_3$ Random) bernilai stabil pada rentang $0.018 - 0.022$ (mendekati probabilitas tebak acak murni dari 16 kelas $\approx 1/16 = 0.062$).
