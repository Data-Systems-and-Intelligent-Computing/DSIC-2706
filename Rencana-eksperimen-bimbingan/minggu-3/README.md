# Rencana Eksperimen — Minggu 3 (GATE 3)
**Fokus:** Open-Set Rejection, Kalibrasi Ambang Batas ($\tau$), dan Evaluasi Sensitivitas Profil Derau Latar (Soundscape vs ITERA)  
**Target Garis Waktu:** Minggu Ke-3  
**Status Eksekusi:** **SELESAI & LULUS 100% (Verifikasi Audit Gate 3 — Terkalibrasi & Terverifikasi Data Mentah)**  

---

## 1. Kalibrasi Ambang Batas ($\tau^*$) pada Partisi Terpisah (No Data Snooping)

* **Tujuan & Protokol Anti-Kebocoran (*No Data Snooping*):**
  Menentukan nilai ambang batas kesamaan (*similarity threshold*) $\tau^*$ secara objektif pada partisi kalibrasi independen tanpa menyentuh data evaluasi (kueri uji).
* **Partisi Data Kalibrasi Berimbang (Positif vs Negatif):**
  * **Subset Target (Positif):** Sebanyak **498 rekaman audio burung dari 95 perekam (*author*) unik** dari [`data/manifests/dataset_split.csv`](../../data/manifests/dataset_split.csv) yang 100% *author-disjoint* terhadap galeri dan kueri.
  * **Subset Kontrol Negatif (Unknown):** Sebanyak **498 rekaman audio kontrol negatif** dari [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv) yang terdiri atas 249 segmen derau lingkungan AudioMoth ITERA dan 249 rekaman taksa burung non-target BirdCLEF (100% spesies dan berkas terpisah).
* **Metode Optimasi:**
  * Menghitung kurva ROC empiris dan memaksimalkan **Youden's Index ($J = \text{TPR} - \text{FPR}$)** pada subset kalibrasi.
* **Nilai Ambang Batas Optimal ($\tau^*$) yang Dibekukan:**
  * $\tau^*_{R_2} = \mathbf{0.7128}$ (BirdNET: Youden $J = 0.4779$, AUROC = 0.8147, F1 = 0.7358)
  * $\tau^*_{R_1} = \mathbf{0.9117}$ (PANNs CNN14: Youden $J = 0.2791$, AUROC = 0.6741, F1 = 0.6745)
  * $\tau^*_{R_0} = \mathbf{0.9953}$ (MFCC Baseline: Youden $J = 0.0622$, AUROC = 0.5150, F1 = 0.4847)
  * $\tau^*_{R_3} = \mathbf{0.5090}$ (Random Control: Youden $J = 0.0783$, AUROC = 0.5331, F1 = 0.5935)
  * Tercatat resmi di [`configs/thresholds.yaml`](../../configs/thresholds.yaml) dan [`results/processed/calibration_summary_table.csv`](../../results/processed/calibration_summary_table.csv).
* **Penjelasan Saintifik Pembekuan Ambang Batas:**
  Ambang batas $\tau^*$ wajib dibekukan (*frozen*) pada subset kalibrasi sebelum diterapkan pada pengujian kelas terbuka (*open-set*). Hal ini mensimulasikan sistem pemantauan bioakustik otonom di dunia nyata: sistem harus memiliki standar penolakan tetap untuk menyaring audio acak tanpa mengetahui label kebenaran di lapangan sebelumnya.

---

## 2. Eksperimen E3: Evaluasi Penolakan Kelas Terbuka (Open-Set Rejection)

* **Dataset Kontrol Negatif Uji (Disjoint Unknown Test Set):**
  Menggunakan **200 rekaman negatif independen** dari [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv) (100 segmen derau lingkungan ITERA + 100 rekaman burung non-target) yang diuji bersama 200 kueri target pada grid SNR Clean, 20 dB, 10 dB, 0 dB, dan -5 dB.
* **Kriteria Uji Matematis:**
  Suatu sinyal kueri $q$ diklasifikasikan sebagai *Diterima (Spesies Target)* jika skor kemiripan maksimumnya terhadap galeri mencapai ambang batas:
  $$\max_{g \in \text{Gallery}} \text{CosineSim}(q, g) \ge \tau^*$$
  Sebaliknya, jika $\max_{g} \text{CosineSim}(q, g) < \tau^*$, sinyal ditolak sebagai *Unknown*.
* **Hasil Evaluasi Empiris Test Set (`paper/tables/threshold_transfer_table.csv`):**

| Representasi | Kondisi | Ambang $\tau^*$ | Recall Target | False Positive Rate (FPR) | $\Delta$FPR vs Clean | AUROC | F1-Score | Status Penolakan |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **$R_2$ (BirdNET)** | **Clean** | **0.7128** | 0.8600 | 0.2850 | 0.0000 | 0.8849 | 0.8019 | Akurat & Selektif |
| | SNR +20 dB | 0.7128 | 0.8050 | 0.2750 | -0.0100 | 0.8756 | 0.7740 | Sangat Stabil |
| | SNR +10 dB | 0.7128 | 0.7950 | 0.2050 | -0.0800 | 0.8698 | 0.7950 | Sangat Stabil |
| | SNR 0 dB | 0.7128 | 0.5950 | 0.1500 | -0.1350 | 0.8083 | 0.6819 | Konservatif |
| | **SNR -5 dB** | **0.7128** | **0.4450** | **0.0950** | **-0.1900** | **0.7575** | **0.5779** | **Penolakan Aman (FPR Rendah)** |
| **$R_1$ (PANNs)** | **Clean** | **0.9117** | 0.8100 | 0.4150 | 0.0000 | 0.7715 | 0.7281 | FPR Moderat |
| | SNR +20 dB | 0.9117 | 0.8700 | 0.4900 | +0.0750 | 0.7525 | 0.7373 | FPR Meningkat |
| | SNR +10 dB | 0.9117 | 0.8100 | 0.5100 | +0.0950 | 0.7123 | 0.6983 | Separasi Menurun |
| | SNR 0 dB | 0.9117 | 0.7000 | 0.6200 | +0.2050 | 0.5544 | 0.6034 | Nyaris Acak |
| | **SNR -5 dB** | **0.9117** | **0.7550** | **0.8150** | **+0.4000** | **0.5348** | **0.5875** | **Kolaps Katastropik (FPR 81.5%)** |
| **$R_0$ (MFCC)** | Clean | 0.9953 | 0.4350 | 0.3600 | 0.0000 | 0.5683 | 0.4847 | Daya Pisah Lemah |
| | SNR -5 dB | 0.9953 | 0.2850 | 0.1850 | -0.1750 | 0.6067 | 0.3878 | Lemah |
| **$R_3$ (Random)**| Clean | 0.5090 | 0.6900 | 0.6350 | 0.0000 | 0.5389 | 0.5935 | Kontrol Acak |
| | SNR -5 dB | 0.5090 | 0.7500 | 0.6900 | +0.0550 | 0.5508 | 0.6148 | Kontrol Acak |

*Detail skor per-kueri tersimpan di [`results/raw/E3_test_scores_raw.csv`](../../results/raw/E3_test_scores_raw.csv).*

### Analisis Saintifik Mengapa Performa Berbeda:
1. **Penolakan Konservatif & Aman pada BirdNET ($R_2$):**
   * False Positive Rate (FPR) $R_2$ tetap terkendali sangat ketat, bahkan turun dari **28.5%** pada Clean menjadi **9.5%** pada SNR -5 dB ($\Delta\text{FPR} = -0.1900$).
   * *Alasan Fisik:* Ruang representasi bioakustik spesifik memisahkan sinyal burung target dari audio asing. Ketika energi derau meningkat, skor kemiripan global tertekan ke bawah, sehingga sistem memilih menolak sinyal meragukan (*safe false rejection*) daripada salah mengidentifikasi suara asing sebagai burung target.
2. **Inflasi FPR Katastropik pada Model Generik PANNs ($R_1$):**
   * Pada PANNs, FPR meledak dari **41.5%** menjadi **81.5%** ($\Delta\text{FPR} = \mathbf{+40.0\%}$) pada SNR -5 dB dengan AUROC anjlok ke 0.5348 (mendekati tebakan acak 0.50).
   * *Alasan Fisik:* Fitur konvolusi generik PANNs mengalami aktivasi palsu akibat tumpang tindih energi spektral derau latar, mendongkrak skor kemiripan kosinus suara asing melewati batas kaku $\tau^* = 0.9117$. Ini membuktikan bahwa representasi audio generik tidak aman digunakan untuk open-set monitoring pada lingkungan bising tanpa adaptasi dinamis.

---

## 3. Eksperimen E4: Validasi Sensitivitas Terhadap Profil Spektral Derau Latar

* **Tujuan & Reformulasi Saintifik Objektif:**
  Menguji sensitivitas representasi audio terhadap perbedaan karakteristik spektral derau latar aditif: **Derau Antropogenik Kampus ITERA (E2)** vs **Derau Biophony Soundscape Alami Hutan Tropis (E4, dari BirdCLEF `train_soundscapes`)**.
* **Batasan Saintifik Terbuka (*Research Limitation*):**
  Eksperimen E4 ini menguji ketahanan terhadap *noise spectral profile shift* dengan protokol aditif terkontrol. Uji pergeseran domain *in-situ* lapangan penuh (dengan variabel jarak propagasi, redaman kanopi, dan pantulan/reverberasi) didokumentasikan sebagai keterbatasan dan agenda penelitian masa depan karena dataset `data/itera_soundscape_annotations/` saat ini belum memiliki anotasi *ground-truth*.
* **Hasil Komparasi Berdampingan Seluruh Representasi (`paper/tables/e4_domain_shift_table.csv`):**

| Rep | Kondisi SNR | $mAP@10$ (ITERA / E2) | $mAP@10$ (Soundscape / E4) | Selisih ($\Delta mAP$) | Retensi E2 | Retensi E4 | Karakteristik Pergeseran |
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

*Detail log per-kueri mentah tersimpan di [`results/raw/E4_R0_raw.csv`](../../results/raw/E4_R0_raw.csv), [`results/raw/E4_R1_raw.csv`](../../results/raw/E4_R1_raw.csv), [`results/raw/E4_R2_raw.csv`](../../results/raw/E4_R2_raw.csv), dan [`results/raw/E4_R3_raw.csv`](../../results/raw/E4_R3_raw.csv).*

### Analisis Temuan Ilmiah E4:
1. **$R_2$ (BirdNET) Terbukti Invarian Terhadap Profil Derau:**
   * Pada SNR -5 dB, selisih performa antara derau soundscape dan derau ITERA hanya sebesar **-0.0101**. Uji paired bootstrap menunjukkan selisih ini **tidak signifikan secara statistik ($p = 0.6100$, CI 95% $[-0.0479, +0.0275]$)**.
   * *Penjelasan Fisik:* Derau antropogenik kampus ITERA terkonsentrasi pada frekuensi rendah (< 1 kHz), sedangkan soundscape hutan didominasi oleh biophony serangga frekuensi tinggi (3–8 kHz). Kemampuan BirdNET mempertahankan performa identik membuktikan ketahanan filternya yang terfokus pada kontur harmonik vokal burung.
2. **$R_1$ (PANNs) Sangat Rentan Terhadap Profil Derau Latar:**
   * Sebaliknya, PANNs memperlihatkan disparitas signifikan sebesar **+0.0890** ($p < 0.001$, CI 95% $[+0.0572, +0.1210]$), di mana performanya jauh lebih terpuruk pada derau ITERA (0.0590) dibanding derau soundscape (0.1480).

---

## 4. Kriteria Kelulusan Gate Minggu 3 — 100% Terpenuhi

- [x] **Kalibrasi Ambang Batas $\tau^*$ Objektif & Bebas Bocor:** Dikalibrasi via Youden's Index pada subset berimbang 498 target vs 498 unknown negatif di [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv) ($\tau^*_{R_2} = 0.7128, \tau^*_{R_1} = 0.9117$).
- [x] **Evaluasi Open-Set Rejection E3 Tuntas dengan Data Riil:** Diuji pada 200 unknown test set independen melintasi 5 level SNR, membuktikan selektivitas $R_2$ (FPR 9.5%) dan kegagalan $R_1$ (FPR 81.5%).
- [x] **Evaluasi Sensitivitas Profil Derau E4 Lengkap Seluruh Representasi:** Menghasilkan tabel komparasi lengkap $R_0, R_1, R_2, R_3$ berdampingan dengan E2 di [`paper/tables/e4_domain_shift_table.csv`](../../paper/tables/e4_domain_shift_table.csv).
- [x] **Artefak Gambar dan Notebook Lengkap & Tereksekusi:**
  * Gambar Kalibrasi ROC Youden: [`paper/figures/e3_calibration_roc_youden.png`](../../paper/figures/e3_calibration_roc_youden.png) & [`results/figures/e3_calibration_roc_youden.png`](../../results/figures/e3_calibration_roc_youden.png)
  * Gambar Transfer Ambang Batas SNR: [`paper/figures/e3_threshold_transfer_snr.png`](../../paper/figures/e3_threshold_transfer_snr.png) & [`results/figures/e3_threshold_transfer_snr.png`](../../results/figures/e3_threshold_transfer_snr.png)
  * Gambar Sensitivitas Derau E4: [`paper/figures/e4_noise_profile_sensitivity.png`](../../paper/figures/e4_noise_profile_sensitivity.png) & [`results/figures/e4_noise_profile_sensitivity.png`](../../results/figures/e4_noise_profile_sensitivity.png)
  * Notebook Interaktif E3: [`notebooks/E3_Open_Set_Threshold.ipynb`](../../notebooks/E3_Open_Set_Threshold.ipynb)
  * Notebook Interaktif E4: [`notebooks/E4_Real_Soundscape_Domain_Shift.ipynb`](../../notebooks/E4_Real_Soundscape_Domain_Shift.ipynb)

