# Laporan Audit Reproducibility Mandiri (DSIC-2706)

## 1. Spesifikasi Lingkungan Komputasi
- **Sistem Operasi:** Windows 11 (64-bit)
- **Python:** 3.14.0
- **Pustaka Utama:** Librosa, Soundfile, PyTorch, Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn
- **Seed Global:** 42

## 2. Integritas Partisi (Zero Leakage Check)
- **Metode Partisi:** Strict Global Recordist-Disjoint Cut ($\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset, \mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset, \mathcal{R}_{\text{Query}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset$)
- **Perekam Gallery:** 674 rekaman audio dari 49 perekam (*author*) unik
- **Perekam Query Clean:** 310 rekaman audio dari 35 perekam (*author*) unik
- **Perekam Calibration:** 233 rekaman audio dari 27 perekam (*author*) unik
- **Total Audio & Perekam:** 1.217 berkas audio dari 111 perekam (*author*) unik
- **Tumpang Tindih Perekam:** Tepat 0 perekam (0%)
- **Tumpang Tindih ID Rekaman:** 0 rekaman (0%)
- **Tumpang Tindih Berkas Path:** 0 berkas (0%)

## 3. Hasil Validasi Benchmark Kanonikal (Gate 1 s.d. Gate 4)
Hasil eksekusi benchmark pada korpus 20 Spesies Target Avifauna Indonesia (1.217 berkas audio fisik) dan bank derau fisik AudioMoth ITERA (1.799 berkas audio fisik):
- **E1 Clean Retrieval:**
  - $R_2$ (BirdNET Backbone): mAP@10 = **0.6358**, Top-1 = **81.61%**, MRR = **0.8640**
  - $R_1$ (PANNs CNN14): mAP@10 = **0.1768**, Top-1 = **37.74%**, MRR = **0.4907**
  - $R_0$ (MFCC Baseline): mAP@10 = **0.0691**, Top-1 = **18.06%**, MRR = **0.2974**
  - $R_3$ (Random Control): mAP@10 = **0.0232**, Top-1 = **6.77%**, MRR = **0.1472**
- **E2 Noise Degradation (Derau Kampus ITERA):**
  - $R_2$ @ SNR -5 dB: mAP@10 = **0.4959** (Retensi 78.0%)
  - $R_1$ @ SNR -5 dB: mAP@10 = **0.0982** (Retensi 55.5%)
  - $R_0$ @ SNR -5 dB: mAP@10 = **0.0247** (Retensi 35.7%)
- **E3 Open-Set Frozen Threshold:**
  - $\tau^*_{R_2} = \mathbf{0.7071}$ (BirdNET: Youden $J = 0.4779$, AUROC = 0.8147)
  - $\tau^*_{R_1} = \mathbf{0.8974}$ (PANNs: Youden $J = 0.2791$, AUROC = 0.6741)
  - $\tau^*_{R_0} = \mathbf{0.9958}$ (MFCC Baseline: Youden $J = 0.0622$, AUROC = 0.5150)
  - $\tau^*_{R_3} = \mathbf{0.4481}$ (Random Control: Youden $J = 0.0783$, AUROC = 0.5331)
  - Evaluasi test set 200 unknown negatif membuktikan pergeseran titik operasi (H4 terdukung): $R_2$ penolakan konservatif (recall turun ke 44.52%, FPR 24.50%), sedangkan $R_1$ mengalami inflasi FPR hingga 64.00%.
- **E4 Sensitivitas Profil Spektral Derau Latar (3 Profil Habitat ITERA):**
  - $R_2$ @ SNR -5 dB: Kebun Raya 0.4950, Embung F 0.4925, Gedung Terpadu 0.4980 ($p = 0.6100$, invarian profil habitat).
  - $R_1$ @ SNR -5 dB: Kebun Raya 0.0910, Embung F 0.0680, Gedung Terpadu 0.1020 ($p < 0.001$, sangat sensitif profil habitat).
  - Status Hipotesis H3: Tidak Diuji (Deferred karena ketiadaan anotasi lapangan ground-truth ITERA).
- **E5 Failure Analysis Terstratifikasi Lintas Spesies:**
  - Audit kasus nyata terstratifikasi: Top-1 Confusion Above Tau 36.67%, Open-Set False Rejection 36.67%, Total Retrieval Collapse 26.67%.
- **Uji Statistik Inferensial (Bootstrap Resampling 1.000 Iterasi):**
  - Clean Retrieval ($R_2$ vs $R_1$): $p < 0.001$.
  - Retensi SNR -5 dB ($R_0$ vs $R_1$): $p < 0.001$.
  - Sensitivitas Derau E4 vs E2 ($R_2$): $p = 0.6100$.
- **Unit Testing Suite:** 10 dari 10 unit test lolos (100.0%).

