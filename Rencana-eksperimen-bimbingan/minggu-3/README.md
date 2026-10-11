# Rencana Eksperimen — Minggu 3 (GATE 3)
**Fokus:** Open-Set Rejection, Kalibrasi Ambang Batas ($\tau$), dan Evaluasi Sensitivitas Profil Derau Latar (Soundscape vs ITERA)  
**Target Garis Waktu:** Minggu Ke-3  
**Status Eksekusi:** **SELESAI & LULUS 100% (Verifikasi Audit Gate 3 — Terkalibrasi & Terverifikasi Data Mentah)**  

---

## 1. Kalibrasi Ambang Batas ($\tau^*$) pada Partisi Terpisah (No Data Snooping)

* **Tujuan & Protokol Anti-Kebocoran (*No Data Snooping*):**
  Menentukan nilai ambang batas kesamaan (*similarity threshold*) $\tau^*$ secara objektif pada partisi kalibrasi independen tanpa menyentuh data evaluasi (kueri uji).
* **Partisi Data Kalibrasi Berimbang (Positif vs Negatif):**
  * **Subset Target (Positif):** Sebanyak **232 rekaman audio burung dari 25 perekam (*author*) unik** dari [`data/manifests/dataset_split.csv`](../../data/manifests/dataset_split.csv) yang 100% *author-disjoint* terhadap galeri dan kueri.
  * **Subset Kontrol Negatif (Unknown):** Sebanyak **233 rekaman audio kontrol negatif** dari [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv) yang terdiri atas 117 segmen derau lingkungan AudioMoth ITERA (dari partisi derau bebas tumpang tindih) dan 116 rekaman taksa non-target (100% spesies dan berkas terpisah). Total subset kalibrasi $N = 465$.
* **Metode Optimasi:**
  * Menghitung kurva ROC empiris dan memaksimalkan **Youden's Index ($J = \text{TPR} - \text{FPR}$)** pada subset kalibrasi.
* **Nilai Ambang Batas Optimal ($\tau^*$) yang Dibekukan:**
  * $\tau^*_{R_2} = \mathbf{0.7071}$ (BirdNET: Youden $J = 0.4188$, AUROC = 0.7601, F1 = 0.6633)
  * $\tau^*_{R_1} = \mathbf{0.8974}$ (PANNs CNN14: Youden $J = 0.3766$, AUROC = 0.7167, F1 = 0.7047)
  * $\tau^*_{R_0} = \mathbf{0.9958}$ (MFCC Baseline: Youden $J = 0.0995$, AUROC = 0.5298, F1 = 0.3010)
  * $\tau^*_{R_3} = \mathbf{0.4481}$ (Random Control: Youden $J = 0.1191$, AUROC = 0.5658, F1 = 0.6279)
  * Tercatat resmi di [`configs/thresholds.yaml`](../../configs/thresholds.yaml) dan [`results/processed/calibration_summary_table.csv`](../../results/processed/calibration_summary_table.csv).
* **Penjelasan Saintifik Pembekuan Ambang Batas:**
  Ambang batas $\tau^*$ wajib dibekukan (*frozen*) pada subset kalibrasi sebelum diterapkan pada pengujian kelas terbuka (*open-set*). Hal ini mensimulasikan sistem pemantauan bioakustik otonom di dunia nyata: sistem harus memiliki standar penolakan tetap untuk menyaring audio acak tanpa mengetahui label kebenaran di lapangan sebelumnya.

---

## 2. Eksperimen E3: Evaluasi Penolakan Kelas Terbuka (Open-Set Rejection)

* **Dataset Kontrol Negatif Uji (Disjoint Unknown Test Set):**
  Menggunakan **310 rekaman negatif independen** dari [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv) (155 segmen derau lingkungan ITERA + 155 rekaman taksa non-target) yang diuji bersama 311 kueri target Avifauna Indonesia (Total $N=621$) pada grid SNR Clean, 20 dB, 10 dB, 0 dB, dan -5 dB.
* **Kriteria Uji Matematis:**
  Suatu sinyal kueri $q$ diklasifikasikan sebagai *Diterima (Spesies Target)* jika skor kemiripan maksimumnya terhadap galeri mencapai ambang batas:
  $$\max_{g \in \text{Gallery}} \text{CosineSim}(q, g) \ge \tau^*$$
  Sebaliknya, jika $\max_{g} \text{CosineSim}(q, g) < \tau^*$, sinyal ditolak sebagai *Unknown*.
* **Hasil Evaluasi Empiris Test Set (`paper/tables/threshold_transfer_table.csv`):**

| Representasi | Kondisi | Ambang $\tau^*$ | Recall Target (TPR) | False Positive Rate (FPR) | $\Delta$FPR vs Clean | AUROC | F1-Score | Status Penolakan |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **$R_2$ (BirdNET)** | **Clean** | **0.7071** | **0.5916** | **0.2000** | 0.0000 | **0.7589** | **0.6607** | Akurat & Selektif |
| | SNR +20 dB | 0.7071 | 0.5466 | 0.1613 | -0.0387 | 0.7576 | 0.6403 | Sangat Stabil |
| | SNR +10 dB | 0.7071 | 0.4791 | 0.1258 | -0.0742 | 0.7299 | 0.5972 | Sangat Stabil |
| | SNR 0 dB | 0.7071 | 0.3183 | 0.1097 | -0.0903 | 0.6596 | 0.4459 | Konservatif |
| | **SNR -5 dB** | **0.7071** | **0.2412** | **0.0935** | **-0.1065** | **0.6153** | **0.3614** | **Penolakan Aman (FPR Rendah)** |
| **$R_1$ (PANNs)** | **Clean** | **0.8974** | **0.8360** | **0.4742** | 0.0000 | **0.7454** | **0.7242** | FPR Moderat |
| | SNR +20 dB | 0.8974 | 0.8489 | 0.4774 | +0.0032 | 0.7498 | 0.7303 | FPR Meningkat |
| | SNR +10 dB | 0.8974 | 0.8006 | 0.4548 | -0.0194 | 0.7389 | 0.7104 | Separasi Menurun |
| | SNR 0 dB | 0.8974 | 0.6045 | 0.3419 | -0.1323 | 0.6833 | 0.6215 | Nyaris Acak |
| | **SNR -5 dB** | **0.8974** | **0.4566** | **0.2710** | **-0.2032** | **0.6287** | **0.5289** | **Penolakan Menurun** |
| **$R_0$ (MFCC)** | Clean | 0.9958 | 0.1865 | 0.1387 | 0.0000 | 0.5463 | 0.2816 | Daya Pisah Lemah |
| | SNR -5 dB | 0.9958 | 0.0064 | 0.0129 | -0.1258 | 0.5665 | 0.0126 | Kolaps |
| **$R_3$ (Random)**| Clean | 0.4481 | 0.6849 | 0.6548 | 0.0000 | 0.5183 | 0.5860 | Kontrol Acak |
| | SNR -5 dB | 0.4481 | 0.6624 | 0.6355 | -0.0194 | 0.5221 | 0.5770 | Kontrol Acak |

*Detail skor per-kueri tersimpan di [`results/raw/E3_test_scores_raw.csv`](../../results/raw/E3_test_scores_raw.csv).*

### Analisis Saintifik Mengapa Performa Berbeda:
1. **Penolakan Konservatif & Aman pada BirdNET ($R_2$):**
   * False Positive Rate (FPR) $R_2$ tetap terkendali ketat, turun dari **20.00%** pada Clean menjadi **9.35%** pada SNR -5 dB ($\Delta\text{FPR} = -0.1065$).
   * *Alasan Fisik:* Ruang representasi bioakustik spesifik memisahkan sinyal burung target dari audio asing. Ketika energi derau meningkat, skor kemiripan global tertekan ke bawah, sehingga sistem memilih menolak sinyal meragukan (*safe false rejection*) daripada salah mengidentifikasi suara asing sebagai burung target.
2. **Karakteristik Model Generik PANNs ($R_1$):**
   * Pada PANNs, FPR awal jauh lebih tinggi (**47.42%**) pada kondisi Clean dan berada di **27.10%** pada SNR -5 dB, menunjukkan ambang $\tau^*$ PANNs kurang selektif dalam menolak derau non-target.

---

## 3. Eksperimen E4: Validasi Sensitivitas Terhadap Profil Spektral Derau Latar ITERA

* **Tujuan & Reformulasi Saintifik Objektif:**
   Menguji sensitivitas representasi audio terhadap perbedaan karakteristik spektral derau latar aditif dari 3 profil habitat kampus ITERA: **Kebun Raya ITERA** (biofoni serangga 2–6 kHz), **Embung F ITERA** (hidrofoni/angin frekuensi rendah), dan **Gedung F / Koridor Akademik** (antropofoni struktural).
* **Batasan Saintifik Terbuka (*Research Limitation*):**
   Eksperimen E4 ini menguji ketahanan terhadap *noise spectral profile shift* dengan protokol aditif terkontrol menggunakan bank derau fisik AudioMoth ITERA (1.799 berkas). Uji pergeseran domain *in-situ* lapangan penuh (dengan variabel jarak propagasi, redaman kanopi, dan pantulan/reverberasi) didokumentasikan sebagai keterbatasan dan agenda penelitian masa depan karena dataset `data/itera_soundscape_annotations/` saat ini belum memiliki anotasi *ground-truth*.
* **Hasil Komparasi Berdampingan Seluruh Representasi (`paper/tables/e4_domain_shift_table.csv`):**

| Rep | Kondisi SNR | $mAP@10$ (Kebun Raya) | $mAP@10$ (Embung F) | $mAP@10$ (Gedung F) | Rata-Rata E4 | Retensi Relatif Range | Karakteristik Pergeseran |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **$R_2$ (BirdNET)** | Clean | 0.6370 | 0.6370 | 0.6370 | 0.6370 | 100.0% | Baseline Identik |
| | SNR +20 dB | 0.6431 | 0.6416 | 0.6345 | 0.6397 | 99.6% – 101.0% | Sangat Stabil |
| | SNR +10 dB | 0.6119 | 0.6262 | 0.6205 | 0.6195 | 96.1% – 98.3% | Sangat Stabil |
| | SNR 0 dB | 0.5197 | 0.5661 | 0.5494 | 0.5451 | 81.6% – 88.9% | Penurunan Bertahap |
| | **SNR -5 dB** | **0.4446** | **0.4853** | **0.4667** | **0.4655** | **69.8% – 76.2%** | **Ayunan 6.39% (Sensitif Biofoni, $p = 0.0040$)** |
| **$R_1$ (PANNs)** | Clean | 0.1771 | 0.1771 | 0.1771 | 0.1771 | 100.0% | Baseline Identik |
| | SNR +20 dB | 0.1767 | 0.1854 | 0.1894 | 0.1838 | 99.8% – 106.9% | Sensitif |
| | SNR +10 dB | 0.1462 | 0.1719 | 0.1908 | 0.1696 | 82.6% – 107.7% | Fluktuatif |
| | SNR 0 dB | 0.0873 | 0.1159 | 0.1317 | 0.1116 | 49.3% – 74.4% | Disparitas Tinggi |
| | **SNR -5 dB** | **0.0590** | **0.0948** | **0.0979** | **0.0839** | **33.3% – 55.3%** | **Ayunan 21.98% (Sangat Sensitif, $p \le 0.001$)** |
| **$R_0$ (MFCC)** | Clean | 0.0690 | 0.0690 | 0.0690 | 0.0690 | 100.0% | Baseline Identik |
| | SNR -5 dB | 0.0228 | 0.0264 | 0.0189 | 0.0227 | 27.4% – 38.3% | Penurunan Parah |
| **$R_3$ (Random)**| Clean | 0.0231 | 0.0231 | 0.0231 | 0.0231 | 100.0% | Kontrol Acak |
| | SNR -5 dB | 0.0203 | 0.0218 | 0.0184 | 0.0202 | - | Peluang Acak |

*Detail log per-kueri mentah tersimpan di [`results/raw/E4_R0_raw.csv`](../../results/raw/E4_R0_raw.csv), [`results/raw/E4_R1_raw.csv`](../../results/raw/E4_R1_raw.csv), [`results/raw/E4_R2_raw.csv`](../../results/raw/E4_R2_raw.csv), dan [`results/raw/E4_R3_raw.csv`](../../results/raw/E4_R3_raw.csv).*

### Analisis Temuan Ilmiah E4:
1. **Sensitivitas Terhadap Biofoni Serangga Kebun Raya:**
   * Pada SNR -5 dB, biofoni serangga berdaya tinggi (2–6 kHz) di Kebun Raya mendegradasi BirdNET paling signifikan dibandingkan Embung F ($\Delta = +0.0398$, $p = 0.0040$). Ini menunjukkan bahwa profil frekuensi serangga menabrak pita komunikasi vokal avifauna.
2. **Stabilitas Relatif BirdNET ($R_2$) atas PANNs ($R_1$):**
   * Meskipun dipengaruhi biofoni, rentang ayunan retensi BirdNET hanya **6.39%** (retensi 69.80% s.d. 76.19%), sedangkan PANNs terhempas dengan rentang ayunan sebesar **21.98%** (retensi 33.31% s.d. 55.28%). Disparitas stabilitas ini terbukti sangat signifikan ($\Delta_{\text{obs}} = 0.1560$, rata-rata bootstrap $+0.1692$ [0.0795; 0.2646], $p \le 0.001$).

---

## 4. Kriteria Kelulusan Gate Minggu 3 — 100% Terpenuhi

- [x] **Kalibrasi Ambang Batas $\tau^*$ Objektif & Bebas Bocor:** Dikalibrasi via Youden's Index pada subset berimbang 232 target vs 233 unknown negatif di [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv) ($\tau^*_{R_2} = 0.7071, \tau^*_{R_1} = 0.8974$).
- [x] **Evaluasi Open-Set Rejection E3 Tuntas dengan Data Riil:** Diuji pada 310 unknown test set independen melintasi 5 level SNR, membuktikan selektivitas $R_2$ (FPR 9.35% pada -5 dB) dan kerapuhan $R_1$ (FPR 27.10% pada -5 dB).
- [x] **Evaluasi Sensitivitas Profil Derau E4 Lengkap Seluruh Representasi:** Menghasilkan tabel komparasi lengkap $R_0, R_1, R_2, R_3$ berdampingan lintas 3 habitat kampus ITERA di [`paper/tables/e4_domain_shift_table.csv`](../../paper/tables/e4_domain_shift_table.csv).
- [x] **Artefak Gambar dan Notebook Lengkap & Tereksekusi:**
  * Gambar Kalibrasi ROC Youden: [`paper/figures/e3_calibration_roc_youden.png`](../../paper/figures/e3_calibration_roc_youden.png) & [`results/figures/e3_calibration_roc_youden.png`](../../results/figures/e3_calibration_roc_youden.png)
  * Gambar Transfer Ambang Batas SNR: [`paper/figures/e3_threshold_transfer_snr.png`](../../paper/figures/e3_threshold_transfer_snr.png) & [`results/figures/e3_threshold_transfer_snr.png`](../../results/figures/e3_threshold_transfer_snr.png)
  * Gambar Sensitivitas Derau E4: [`paper/figures/e4_noise_profile_sensitivity.png`](../../paper/figures/e4_noise_profile_sensitivity.png) & [`results/figures/e4_noise_profile_sensitivity.png`](../../results/figures/e4_noise_profile_sensitivity.png)
  * Notebook Interaktif E3: [`notebooks/E3_Open_Set_Threshold.ipynb`](../../notebooks/E3_Open_Set_Threshold.ipynb)
  * Notebook Interaktif E4: [`notebooks/E4_Real_Soundscape_Domain_Shift.ipynb`](../../notebooks/E4_Real_Soundscape_Domain_Shift.ipynb)

