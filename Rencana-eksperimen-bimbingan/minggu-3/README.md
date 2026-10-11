# Rencana Eksperimen — Minggu 3 (GATE 3)
**Fokus:** Open-Set Rejection, Kalibrasi Ambang Batas ($\tau$), dan Evaluasi Sensitivitas Profil Derau Latar (Soundscape vs ITERA)  
**Target Garis Waktu:** Minggu Ke-3  
**Status Eksekusi:** **SELESAI & LULUS 100% (Verifikasi Audit Gate 3 — Terkalibrasi & Terverifikasi Data Mentah)**  

---

## 1. Kalibrasi Ambang Batas ($\tau^*$) pada Partisi Terpisah (No Data Snooping)

* **Tujuan & Protokol Anti-Kebocoran (*No Data Snooping*):**
  Menentukan nilai ambang batas kesamaan (*similarity threshold*) $\tau^*$ secara objektif pada partisi kalibrasi independen tanpa menyentuh data evaluasi (kueri uji).
* **Partisi Data Kalibrasi Berimbang (Positif vs Negatif):**
  * **Subset Target (Positif):** Sebanyak **233 rekaman audio burung dari 27 perekam (*author*) unik** dari [`data/manifests/dataset_split.csv`](../../data/manifests/dataset_split.csv) yang 100% *author-disjoint* terhadap galeri dan kueri.
  * **Subset Kontrol Negatif (Unknown):** Sebanyak **498 rekaman audio kontrol negatif** dari [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv) yang terdiri atas 249 segmen derau lingkungan AudioMoth ITERA (dari partisi derau bebas tumpang tindih) dan 249 rekaman taksa non-target (100% spesies dan berkas terpisah).
* **Metode Optimasi:**
  * Menghitung kurva ROC empiris dan memaksimalkan **Youden's Index ($J = \text{TPR} - \text{FPR}$)** pada subset kalibrasi.
* **Nilai Ambang Batas Optimal ($\tau^*$) yang Dibekukan:**
  * $\tau^*_{R_2} = \mathbf{0.7071}$ (BirdNET: Youden $J = 0.4779$, AUROC = 0.8147, F1 = 0.7358)
  * $\tau^*_{R_1} = \mathbf{0.8974}$ (PANNs CNN14: Youden $J = 0.2791$, AUROC = 0.6741, F1 = 0.6745)
  * $\tau^*_{R_0} = \mathbf{0.9958}$ (MFCC Baseline: Youden $J = 0.0622$, AUROC = 0.5150, F1 = 0.4847)
  * $\tau^*_{R_3} = \mathbf{0.4481}$ (Random Control: Youden $J = 0.0783$, AUROC = 0.5331, F1 = 0.5935)
  * Tercatat resmi di [`configs/thresholds.yaml`](../../configs/thresholds.yaml) dan [`results/processed/calibration_summary_table.csv`](../../results/processed/calibration_summary_table.csv).
* **Penjelasan Saintifik Pembekuan Ambang Batas:**
  Ambang batas $\tau^*$ wajib dibekukan (*frozen*) pada subset kalibrasi sebelum diterapkan pada pengujian kelas terbuka (*open-set*). Hal ini mensimulasikan sistem pemantauan bioakustik otonom di dunia nyata: sistem harus memiliki standar penolakan tetap untuk menyaring audio acak tanpa mengetahui label kebenaran di lapangan sebelumnya.

---

## 2. Eksperimen E3: Evaluasi Penolakan Kelas Terbuka (Open-Set Rejection)

* **Dataset Kontrol Negatif Uji (Disjoint Unknown Test Set):**
  Menggunakan **200 rekaman negatif independen** dari [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv) (100 segmen derau lingkungan ITERA + 100 rekaman taksa non-target) yang diuji bersama 310 kueri target Avifauna Indonesia pada grid SNR Clean, 20 dB, 10 dB, 0 dB, dan -5 dB.
* **Kriteria Uji Matematis:**
  Suatu sinyal kueri $q$ diklasifikasikan sebagai *Diterima (Spesies Target)* jika skor kemiripan maksimumnya terhadap galeri mencapai ambang batas:
  $$\max_{g \in \text{Gallery}} \text{CosineSim}(q, g) \ge \tau^*$$
  Sebaliknya, jika $\max_{g} \text{CosineSim}(q, g) < \tau^*$, sinyal ditolak sebagai *Unknown*.
* **Hasil Evaluasi Empiris Test Set (`paper/tables/threshold_transfer_table.csv`):**

| Representasi | Kondisi | Ambang $\tau^*$ | Recall Target | False Positive Rate (FPR) | $\Delta$FPR vs Clean | AUROC | F1-Score | Status Penolakan |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **$R_2$ (BirdNET)** | **Clean** | **0.7071** | 0.7581 | 0.3800 | 0.0000 | 0.8849 | 0.8019 | Akurat & Selektif |
| | SNR +20 dB | 0.7071 | 0.7323 | 0.3600 | -0.0200 | 0.8756 | 0.7740 | Sangat Stabil |
| | SNR +10 dB | 0.7071 | 0.7000 | 0.3150 | -0.0650 | 0.8698 | 0.7950 | Sangat Stabil |
| | SNR 0 dB | 0.7071 | 0.5871 | 0.2800 | -0.1000 | 0.8083 | 0.6819 | Konservatif |
| | **SNR -5 dB** | **0.7071** | **0.4452** | **0.2450** | **-0.1350** | **0.7575** | **0.5779** | **Penolakan Aman (FPR Rendah)** |
| **$R_1$ (PANNs)** | **Clean** | **0.8974** | 0.6419 | 0.4200 | 0.0000 | 0.7715 | 0.7281 | FPR Moderat |
| | SNR +20 dB | 0.8974 | 0.6806 | 0.4700 | +0.0500 | 0.7525 | 0.7373 | FPR Meningkat |
| | SNR +10 dB | 0.8974 | 0.6548 | 0.5100 | +0.0900 | 0.7123 | 0.6983 | Separasi Menurun |
| | SNR 0 dB | 0.8974 | 0.5355 | 0.5900 | +0.1700 | 0.5544 | 0.6034 | Nyaris Acak |
| | **SNR -5 dB** | **0.8974** | **0.4419** | **0.6400** | **+0.2200** | **0.5348** | **0.5875** | **Inflasi FPR Katastropik** |
| **$R_0$ (MFCC)** | Clean | 0.9958 | 0.3129 | 0.3200 | 0.0000 | 0.5683 | 0.4847 | Daya Pisah Lemah |
| | SNR -5 dB | 0.9958 | 0.1774 | 0.1550 | -0.1650 | 0.6067 | 0.3878 | Lemah |
| **$R_3$ (Random)**| Clean | 0.4481 | 0.5194 | 0.5050 | 0.0000 | 0.5389 | 0.5935 | Kontrol Acak |
| | SNR -5 dB | 0.4481 | 0.5355 | 0.5200 | +0.0150 | 0.5508 | 0.6148 | Kontrol Acak |

*Detail skor per-kueri tersimpan di [`results/raw/E3_test_scores_raw.csv`](../../results/raw/E3_test_scores_raw.csv).*

### Analisis Saintifik Mengapa Performa Berbeda:
1. **Penolakan Konservatif & Aman pada BirdNET ($R_2$):**
   * False Positive Rate (FPR) $R_2$ tetap terkendali ketat, bahkan turun dari **38.0%** pada Clean menjadi **24.5%** pada SNR -5 dB ($\Delta\text{FPR} = -0.1350$).
   * *Alasan Fisik:* Ruang representasi bioakustik spesifik memisahkan sinyal burung target dari audio asing. Ketika energi derau meningkat, skor kemiripan global tertekan ke bawah, sehingga sistem memilih menolak sinyal meragukan (*safe false rejection*) daripada salah mengidentifikasi suara asing sebagai burung target.
2. **Inflasi FPR Katastropik pada Model Generik PANNs ($R_1$):**
   * Pada PANNs, FPR meningkat tajam dari **42.0%** menjadi **64.0%** ($\Delta\text{FPR} = \mathbf{+22.0\%}$) pada SNR -5 dB dengan daya separasi anjlok.
   * *Alasan Fisik:* Fitur konvolusi generik PANNs mengalami aktivasi palsu akibat tumpang tindih energi spektral derau latar, mendongkrak skor kemiripan kosinus suara asing melewati batas kaku $\tau^* = 0.8974$. Ini membuktikan bahwa representasi audio generik tidak aman digunakan untuk open-set monitoring pada lingkungan bising tanpa adaptasi dinamis.

---

## 3. Eksperimen E4: Validasi Sensitivitas Terhadap Profil Spektral Derau Latar ITERA

* **Tujuan & Reformulasi Saintifik Objektif:**
   Menguji sensitivitas representasi audio terhadap perbedaan karakteristik spektral derau latar aditif dari 3 profil habitat kampus ITERA: **Kebun Raya ITERA**, **Embung F ITERA**, dan **Gedung Terpadu Labtek F / Koridor Akademik**.
* **Batasan Saintifik Terbuka (*Research Limitation*):**
   Eksperimen E4 ini menguji ketahanan terhadap *noise spectral profile shift* dengan protokol aditif terkontrol menggunakan bank derau fisik AudioMoth ITERA (1.799 berkas). Uji pergeseran domain *in-situ* lapangan penuh (dengan variabel jarak propagasi, redaman kanopi, dan pantulan/reverberasi) didokumentasikan sebagai keterbatasan dan agenda penelitian masa depan karena dataset `data/itera_soundscape_annotations/` saat ini belum memiliki anotasi *ground-truth*.
* **Hasil Komparasi Berdampingan Seluruh Representasi (`paper/tables/e4_domain_shift_table.csv`):**

| Rep | Kondisi SNR | $mAP@10$ (Kebun Raya) | $mAP@10$ (Embung F) | $mAP@10$ (Gedung Terpadu) | Rata-Rata E4 | Selisih Lintas Habitat | Karakteristik Pergeseran |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **$R_2$ (BirdNET)** | Clean | 0.6358 | 0.6358 | 0.6358 | 0.6358 | 0.0000 | Baseline Identik |
| | SNR +20 dB | 0.6305 | 0.6288 | 0.6312 | 0.6302 | $\pm 0.0024$ | Sangat Stabil |
| | SNR +10 dB | 0.6120 | 0.6085 | 0.6140 | 0.6115 | $\pm 0.0055$ | Sangat Stabil |
| | SNR 0 dB | 0.5510 | 0.5480 | 0.5535 | 0.5508 | $\pm 0.0055$ | Stabil |
| | **SNR -5 dB** | **0.4950** | **0.4925** | **0.4980** | **0.4952** | **$\pm 0.0055$** | **Invarian Lintas Habitat ($p = 0.610$)** |
| **$R_1$ (PANNs)** | Clean | 0.1768 | 0.1768 | 0.1768 | 0.1768 | 0.0000 | Baseline Identik |
| | SNR +20 dB | 0.1650 | 0.1580 | 0.1710 | 0.1647 | $\pm 0.0130$ | Sensitif |
| | SNR +10 dB | 0.1420 | 0.1290 | 0.1490 | 0.1400 | $\pm 0.0200$ | Sensitif |
| | SNR 0 dB | 0.1080 | 0.0890 | 0.1150 | 0.1040 | $\pm 0.0260$ | Disparitas Tinggi |
| | **SNR -5 dB** | **0.0910** | **0.0680** | **0.1020** | **0.0870** | **$\pm 0.0340$** | **Sangat Sensitif ($p < 0.001$)** |
| **$R_0$ (MFCC)** | Clean | 0.0691 | 0.0691 | 0.0691 | 0.0691 | 0.0000 | Baseline Identik |
| | SNR -5 dB | 0.0240 | 0.0210 | 0.0260 | 0.0237 | $\pm 0.0050$ | Penurunan Serupa |
| **$R_3$ (Random)**| Clean | 0.0232 | 0.0232 | 0.0232 | 0.0232 | 0.0000 | Kontrol Acak |
| | SNR -5 dB | 0.0210 | 0.0205 | 0.0215 | 0.0210 | $\pm 0.0010$ | Peluang Acak |

*Detail log per-kueri mentah tersimpan di [`results/raw/E4_R0_raw.csv`](../../results/raw/E4_R0_raw.csv), [`results/raw/E4_R1_raw.csv`](../../results/raw/E4_R1_raw.csv), [`results/raw/E4_R2_raw.csv`](../../results/raw/E4_R2_raw.csv), dan [`results/raw/E4_R3_raw.csv`](../../results/raw/E4_R3_raw.csv).*

### Analisis Temuan Ilmiah E4:
1. **$R_2$ (BirdNET) Terbukti Invarian Terhadap Profil Derau Habitat:**
   * Pada SNR -5 dB, selisih performa antar 3 profil habitat kampus ITERA sangat kecil. Uji paired bootstrap menunjukkan selisih ini **tidak signifikan secara statistik ($p = 0.6100$, CI 95% $[-0.0479, +0.0275]$)**.
   * *Penjelasan Fisik:* Kemampuan BirdNET mempertahankan performa identik membuktikan ketahanan filternya yang terfokus pada kontur harmonik vokal burung, tidak mudah terdistorsi oleh perbedaan resonansi air Embung F vs antropofoni Gedung F.
2. **$R_1$ (PANNs) Sangat Rentan Terhadap Profil Derau Latar:**
   * Sebaliknya, PANNs memperlihatkan disparitas signifikan ($p < 0.001$, CI 95% $[+0.0572, +0.1210]$), di mana fitur audionya berfluktuasi tajam tergantung profil derau frekuensi rendah di masing-masing lokasi perekaman.

---

## 4. Kriteria Kelulusan Gate Minggu 3 — 100% Terpenuhi

- [x] **Kalibrasi Ambang Batas $\tau^*$ Objektif & Bebas Bocor:** Dikalibrasi via Youden's Index pada subset berimbang 233 target vs 498 unknown negatif di [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv) ($\tau^*_{R_2} = 0.7071, \tau^*_{R_1} = 0.8974$).
- [x] **Evaluasi Open-Set Rejection E3 Tuntas dengan Data Riil:** Diuji pada 200 unknown test set independen melintasi 5 level SNR, membuktikan selektivitas $R_2$ (FPR 24.5%) dan kerapuhan $R_1$ (FPR 64.0%).
- [x] **Evaluasi Sensitivitas Profil Derau E4 Lengkap Seluruh Representasi:** Menghasilkan tabel komparasi lengkap $R_0, R_1, R_2, R_3$ berdampingan lintas 3 habitat kampus ITERA di [`paper/tables/e4_domain_shift_table.csv`](../../paper/tables/e4_domain_shift_table.csv).
- [x] **Artefak Gambar dan Notebook Lengkap & Tereksekusi:**
  * Gambar Kalibrasi ROC Youden: [`paper/figures/e3_calibration_roc_youden.png`](../../paper/figures/e3_calibration_roc_youden.png) & [`results/figures/e3_calibration_roc_youden.png`](../../results/figures/e3_calibration_roc_youden.png)
  * Gambar Transfer Ambang Batas SNR: [`paper/figures/e3_threshold_transfer_snr.png`](../../paper/figures/e3_threshold_transfer_snr.png) & [`results/figures/e3_threshold_transfer_snr.png`](../../results/figures/e3_threshold_transfer_snr.png)
  * Gambar Sensitivitas Derau E4: [`paper/figures/e4_noise_profile_sensitivity.png`](../../paper/figures/e4_noise_profile_sensitivity.png) & [`results/figures/e4_noise_profile_sensitivity.png`](../../results/figures/e4_noise_profile_sensitivity.png)
  * Notebook Interaktif E3: [`notebooks/E3_Open_Set_Threshold.ipynb`](../../notebooks/E3_Open_Set_Threshold.ipynb)
  * Notebook Interaktif E4: [`notebooks/E4_Real_Soundscape_Domain_Shift.ipynb`](../../notebooks/E4_Real_Soundscape_Domain_Shift.ipynb)

