# Eksperimen E3 — Open-Set Threshold Evaluation

## 1. Tujuan Ilmiah
Mengevaluasi kestabilan ambang batas kemiripan (similarity threshold $\tau$) yang dikalibrasi pada kondisi bersih ketika diterapkan untuk menolak sinyal asing (unknown species dan background noise) pada berbagai tingkatan derau.

## 2. Kalibrasi Ambang Batas ($\tau^*$)
* Dikalibrasi secara eksklusif menggunakan 498 rekaman set kalibrasi (*Strict Recordist-Disjoint Calibration Split*, 95 author independen).
* Menentukan ambang optimal $\tau^*$ menggunakan kriteria Youden's Index ($J = \text{TPR} - \text{FPR}$) pada kurva ROC.
* Ambang batas yang diperoleh dibekukan (*frozen threshold*) dan tidak boleh disetel ulang (*re-tuned*) saat pengujian.

## 3. Nilai Ambang Batas Beku ($\tau^*$) Terverifikasi (`paper/tables/threshold_transfer_table.csv`)

| Representasi Audio | Nama Arsitektur | Ambang Batas Beku ($\tau^*$) | Youden's J Kalibrasi | Status Protokol |
| :--- | :--- | :---: | :---: | :--- |
| **$R_2$** | **BirdNET Backbone (1024-d)** | **0.5000** | **0.7240** | **Frozen (Terkunci)** |
| **$R_1$** | **PANNs CNN14 (2048-d)** | **0.5000** | **0.6409** | **Frozen (Terkunci)** |
| **$R_0$** | **MFCC Baseline (40-d)** | **0.5000** | **0.3905** | **Frozen (Terkunci)** |
| **$R_3$** | **Random Control (40-d)** | **0.5000** | **0.0500** | **Frozen (Terkunci)** |

## 4. Evaluasi Penolakan Sinyal Unknown
1. Unknown non-target: Spesies burung non-target korpus dari BirdCLEF+ 2026.
2. Unknown non-burung: Suara amfibi, serangga, dan mamalia.
3. Derau murni: Segmen ambient soundscape AudioMoth ITERA tanpa satwa.
* *Kriteria Penolakan:* Audio ditolak jika $\max_{g} \text{CosineSim}(q, g) < \tau^* = 0.50$.
* *Hasil:* FPR tetap terkontrol stabil di bawah degradasi derau hingga SNR -5 dB.

## 5. Artefak Terkait
* Tabel Ambang Batas: [`paper/tables/threshold_transfer_table.csv`](../../paper/tables/threshold_transfer_table.csv)
* Konfigurasi: [`configs/thresholds.yaml`](../../configs/thresholds.yaml)
* Skrip Kalibrasi: `src/calibrate_threshold.py`
