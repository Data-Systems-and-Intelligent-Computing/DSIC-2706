# Eksperimen E3 — Open-Set Threshold Evaluation

## 1. Tujuan Ilmiah
Mengevaluasi kestabilan ambang batas kemiripan (similarity threshold $\tau$) yang dikalibrasi pada partisi kalibrasi independen ketika diterapkan untuk menolak sinyal asing (*unknown species* dan derau lingkungan) pada berbagai tingkatan derau.

## 2. Kalibrasi Ambang Batas ($\tau^*$) pada Partisi Terpisah
* Dikalibrasi menggunakan subset berimbang pada [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv):
  * **498 audio burung target** (*calibration split*, 95 author independen dari `dataset_split.csv`).
  * **498 audio kontrol negatif** (249 derau lingkungan AudioMoth ITERA + 249 burung non-target BirdCLEF).
* Ambang optimal $\tau^*$ ditentukan dengan memaksimalkan **Youden's Index ($J = \text{TPR} - \text{FPR}$)** pada kurva ROC empiris, lalu dibekukan (*frozen*).

## 3. Nilai Ambang Batas Beku ($\tau^*$) Terverifikasi (`paper/tables/threshold_transfer_table.csv`)

| Representasi Audio | Nama Arsitektur | Ambang Batas Beku ($\tau^*$) | Youden's J Kalibrasi | AUROC Kalibrasi | Status Protokol |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **$R_2$** | **BirdNET Backbone (1024-d)** | **0.7128** | **0.4779** | **0.8147** | **Frozen (Terkunci)** |
| **$R_1$** | **PANNs CNN14 (2048-d)** | **0.9117** | **0.2791** | **0.6741** | **Frozen (Terkunci)** |
| **$R_0$** | **MFCC Baseline (40-d)** | **0.9953** | **0.0622** | **0.5150** | **Frozen (Terkunci)** |
| **$R_3$** | **Random Control (40-d)** | **0.5090** | **0.0783** | **0.5331** | **Frozen (Terkunci)** |

## 4. Evaluasi Penolakan Test Set (200 Target vs 200 Unknown)
* **Dataset Uji Negatif:** 100 segmen derau AudioMoth ITERA + 100 rekaman taksa non-target BirdCLEF.
* **Hasil Empiris Lintas Kondisi Derau:**
  * **$R_2$ (BirdNET):** Pada kondisi Clean, FPR rata-rata adalah 28.5% (ITERA derau 39.0%, burung non-target 18.0%). Pada SNR -5 dB, FPR turun ke 9.5% sementara Recall jatuh dari 86.0% ke 44.5%. Penurunan FPR ini bukan akibat penolakan selektif adaptif, melainkan karena atenuasi energi sinyal yang menekan seluruh skor kemiripan ke bawah ambang beku $\tau^* = 0.7128$.
  * **$R_1$ (PANNs):** Pada kondisi Clean, FPR adalah 41.5%. Pada SNR -5 dB, FPR **meledak hingga 81.5%** ($\Delta\text{FPR} = +40.0\%$), membuktikan representasi generik gagal total menyaring derau lingkungan pada rezim bising tinggi.
  * **Validasi Hipotesis H4 (Terdukung):** Terjadi pergeseran titik operasi (*operating point shift*): penambahan derau aditif merusak keseimbangan sensitivitas/spesifisitas ambang batas beku, di mana $R_2$ bergeser ke arah penolakan konservatif (recall turun drastis) dan $R_1$ bergeser ke arah lonjakan alarm palsu (FPR meledak).

## 5. Artefak Terkait
* Tabel Ambang Batas: [`paper/tables/threshold_transfer_table.csv`](../../paper/tables/threshold_transfer_table.csv)
* Konfigurasi Resmi: [`configs/thresholds.yaml`](../../configs/thresholds.yaml)
* Log Mentah Skor: [`results/raw/E3_test_scores_raw.csv`](../../results/raw/E3_test_scores_raw.csv)
* Notebook Demonstrasi: [`notebooks/E3_Open_Set_Threshold.ipynb`](../../notebooks/E3_Open_Set_Threshold.ipynb)
* Gambar Kurva ROC: [`paper/figures/e3_calibration_roc_youden.png`](../../paper/figures/e3_calibration_roc_youden.png)
* Gambar Transfer Ambang: [`paper/figures/e3_threshold_transfer_snr.png`](../../paper/figures/e3_threshold_transfer_snr.png)

