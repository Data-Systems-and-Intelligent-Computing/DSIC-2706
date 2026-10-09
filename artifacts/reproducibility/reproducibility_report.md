# Laporan Audit Reproducibility Mandiri (DSIC-2706)

## 1. Spesifikasi Lingkungan Komputasi
- **Sistem Operasi:** Windows 11 (64-bit)
- **Python:** 3.14.0
- **Pustaka Utama:** Librosa, Soundfile, PyTorch, Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn
- **Seed Global:** 42

## 2. Integritas Partisi (Zero Leakage Check)
- **Metode Partisi:** Strict Global Recordist-Disjoint Cut ($\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset, \mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset, \mathcal{R}_{\text{Query}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset$)
- **Perekam Gallery:** 3.653 rekaman audio dari 377 perekam (*author*) unik
- **Perekam Query Clean:** 200 rekaman audio dari 68 perekam (*author*) unik
- **Perekam Calibration:** 498 rekaman audio dari 95 perekam (*author*) unik
- **Tumpang Tindih Perekam:** Tepat 0 perekam (0%)
- **Tumpang Tindih ID Rekaman:** 0 rekaman (0%)
- **Tumpang Tindih Berkas Path:** 0 berkas (0%)

## 3. Hasil Validasi Benchmark Kanonikal (Gate 1 s.d. Gate 4)
Hasil eksekusi benchmark pada korpus 20 Spesies Target BirdCLEF+ 2026 dan bank derau fisik AudioMoth ITERA:
- **E1 Clean Retrieval:**
  - $R_2$ (BirdNET Backbone): mAP@10 = **0.9126**, Top-1 = **95.0%**, MRR = **0.9658**
  - $R_1$ (PANNs CNN14): mAP@10 = **0.4152**, Top-1 = **60.0%**, MRR = **0.7005**
  - $R_0$ (MFCC Baseline): mAP@10 = **0.1319**, Top-1 = **27.5%**, MRR = **0.4224**
  - $R_3$ (Random Control): mAP@10 = **0.0190**, Top-1 = **6.5%**, MRR = **0.1779**
- **E2 Noise Degradation (Derau Kampus ITERA):**
  - $R_2$ @ SNR -5 dB: mAP@10 = **0.7707** (Retensi 84.45%, 95% CI: [80.6%, 88.3%])
  - $R_1$ @ SNR -5 dB: mAP@10 = **0.0590** (Retensi 14.22%, 95% CI: [10.1%, 18.6%])
  - $R_0$ @ SNR -5 dB: mAP@10 = **0.0349** (Retensi 26.42%, 95% CI: [20.8%, 33.4%])
  - Retensi MFCC $R_0$ melampaui PANNs $R_1$ secara signifikan ($p < 0.001$).
- **E3 Open-Set Frozen Threshold:**
  - $\tau^*_{R_2} = \mathbf{0.7128}$ (BirdNET: Youden $J = 0.4779$, AUROC = 0.8147)
  - $\tau^*_{R_1} = \mathbf{0.9117}$ (PANNs: Youden $J = 0.2791$, AUROC = 0.6741)
  - Evaluasi test set 200 unknown negatif membuktikan pergeseran titik operasi (H4 terdukung): $R_2$ penolakan konservatif (recall turun ke 44.5%, FPR 9.5%), sedangkan $R_1$ inflasi FPR katastropik hingga 81.5%.
- **E4 Sensitivitas Profil Spektral Derau Latar:**
  - $R_2$ @ SNR -5 dB: Soundscape 0.7606 vs ITERA 0.7707 ($\Delta = -0.0101$, $p = 0.6100$, invarian profil derau).
  - $R_1$ @ SNR -5 dB: Soundscape 0.1480 vs ITERA 0.0590 ($\Delta = +0.0890$, $p < 0.001$, sangat sensitif profil derau).
  - Status Hipotesis H3: Tidak Diuji (Deferred karena ketiadaan anotasi lapangan ground-truth ITERA).
- **E5 Failure Analysis Terstratifikasi Lintas Spesies:**
  - 30 kasus nyata terstratifikasi dari 16 taksa burung unik: Top-1 Confusion Above Tau 36.67%, Open-Set False Rejection 36.67%, Total Retrieval Collapse 26.67%.
- **Uji Statistik Inferensial (Bootstrap Resampling 1.000 Iterasi):**
  - Clean Retrieval ($R_2$ vs $R_1$): $\Delta mAP@10 = \mathbf{+0.4981}$, CI 95% **$[+0.4504, +0.5473]$**, **$p < 0.001$**.
  - Retensi SNR -5 dB ($R_0$ vs $R_1$): $\Delta = \mathbf{+0.1223}$, CI 95% **$[+0.0581, +0.1994]$**, **$p < 0.001$**.
  - Sensitivitas Derau E4 vs E2 ($R_2$): $\Delta = \mathbf{-0.0097}$, CI 95% **$[-0.0479, +0.0275]$**, **$p = 0.6100$**.

