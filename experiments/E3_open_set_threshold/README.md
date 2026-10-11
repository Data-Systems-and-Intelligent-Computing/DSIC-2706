# Eksperimen E3 — Open-Set Threshold Evaluation

## 1. Tujuan Ilmiah
Mengevaluasi kestabilan ambang batas kemiripan (similarity threshold $\tau$) yang dikalibrasi pada partisi kalibrasi independen ketika diterapkan untuk menolak sinyal asing (*unknown species* dan derau lingkungan) pada berbagai tingkatan derau.

## 2. Kalibrasi Ambang Batas ($\tau^*$) pada Partisi Terpisah
* Dikalibrasi menggunakan subset berimbang pada [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv):
  * **232 audio burung target** (*calibration split*, 25 author independen dari `dataset_split.csv`).
  * **233 audio kontrol negatif** (kontrol satwa non-burung / non-target dan rekaman derau AudioMoth ITERA). Total $N=465$.
* Ambang optimal $\tau^*$ ditentukan dengan memaksimalkan **Youden's Index ($J = \text{TPR} - \text{FPR}$)** pada kurva ROC empiris, lalu dibekukan (*frozen*).

## 3. Nilai Ambang Batas Beku ($\tau^*$) Terverifikasi (`paper/tables/threshold_transfer_table.csv`)

| Representasi Audio | Nama Arsitektur | Ambang Batas Beku ($\tau^*$) | Youden's J Kalibrasi | AUROC Kalibrasi | Status Protokol |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **$R_2$** | **BirdNET Backbone (1024-d)** | **0.7071** | **0.4188** | **0.7601** | **Frozen (Terkunci)** |
| **$R_1$** | **PANNs CNN14 (2048-d)** | **0.8974** | **0.3766** | **0.7167** | **Frozen (Terkunci)** |
| **$R_0$** | **MFCC Baseline (40-d)** | **0.9958** | **0.0995** | **0.5298** | **Frozen (Terkunci)** |
| **$R_3$** | **Random Control (40-d)** | **0.4481** | **0.1191** | **0.5658** | **Frozen (Terkunci)** |

## 4. Evaluasi Penolakan Test Set (311 Target vs 310 Unknown, Total $N=621$)
* **Dataset Uji Negatif:** 310 kontrol negatif independen (taksa non-burung / burung non-target dan segmen derau AudioMoth ITERA).
* **Hasil Empiris Lintas Kondisi Derau:**
  * **$R_2$ (BirdNET):** Pada kondisi Clean, FPR adalah 20.00% dan Recall adalah 59.16% (AUROC 0.7589). Pada SNR -5 dB, FPR turun ke 9.35% sementara Recall tertekan ke 24.12% ($\Delta\text{Recall} = -35.05\%$, AUROC 0.6153). Penurunan ini membuktikan kompresi skor laten pada derau tinggi.
  * **$R_1$ (PANNs):** Pada kondisi Clean, FPR adalah 47.42% dan Recall 83.60% (AUROC 0.7454). Pada SNR -5 dB, FPR turun ke 27.10% sementara Recall anjlok ke 45.66% (AUROC 0.6287).
  * **Validasi Hipotesis H4:** Terbukti terjadi pergeseran titik operasi (*operating point shift*): penambahan derau aditif merusak efektivitas ambang batas beku yang dikalibrasi pada data bersih, menuntut kalibrasi adaptif pada aplikasi pemantauan otonom.

## 5. Artefak Terkait
* Tabel Ambang Batas: [`paper/tables/threshold_transfer_table.csv`](../../paper/tables/threshold_transfer_table.csv)
* Ringkasan Kalibrasi: [`paper/tables/calibration_summary_table.csv`](../../paper/tables/calibration_summary_table.csv)
* Konfigurasi Resmi: [`configs/thresholds.yaml`](../../configs/thresholds.yaml)
* Log Mentah Skor: [`results/raw/E3_test_scores_raw.csv`](../../results/raw/E3_test_scores_raw.csv) (dengan kolom `noise_file`)
* Notebook Demonstrasi: [`notebooks/E3_Open_Set_Threshold.ipynb`](../../notebooks/E3_Open_Set_Threshold.ipynb)
* Gambar Kurva ROC: [`paper/figures/e3_calibration_roc_youden.png`](../../paper/figures/e3_calibration_roc_youden.png)
* Gambar Transfer Ambang: [`paper/figures/e3_threshold_transfer_snr.png`](../../paper/figures/e3_threshold_transfer_snr.png)
