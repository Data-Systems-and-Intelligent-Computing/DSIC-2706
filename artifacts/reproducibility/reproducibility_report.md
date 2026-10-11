# Laporan Audit Reproducibility Mandiri (DSIC-2706)

## 1. Spesifikasi Lingkungan Komputasi
- **Sistem Operasi:** Windows 11 (64-bit)
- **Python:** 3.14.0
- **Pustaka Utama:** Librosa, Soundfile, PyTorch, Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn
- **Seed Global:** 42

## 2. Integritas Partisi (Zero Leakage Check)
- **Metode Partisi:** Strict Global Recordist-Disjoint Cut ($\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset, \mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset, \mathcal{R}_{\text{Query}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset$)
- **Perekam Gallery:** 674 rekaman audio dari 60 perekam (*author*) unik
- **Perekam Query Clean:** 310 rekaman audio dari 26 perekam (*author*) unik
- **Perekam Calibration:** 233 rekaman audio dari 25 perekam (*author*) unik
- **Total Audio & Perekam:** 1.217 berkas audio dari 111 perekam (*author*) unik
- **Tumpang Tindih Perekam:** Tepat 0 perekam (0%)
- **Tumpang Tindih ID Rekaman:** 0 rekaman (0%)
- **Tumpang Tindih Berkas Path:** 0 berkas (0%)

## 3. Hasil Validasi Benchmark Kanonikal (Gate 1 s.d. Gate 4)
Hasil eksekusi benchmark pada korpus 20 Spesies Target Avifauna Indonesia (1.217 berkas audio fisik) dan bank derau fisik AudioMoth ITERA (1.799 berkas audio fisik):
- **E1 Clean Retrieval:**
  - $R_2$ (BirdNET Backbone): mAP@10 = **0.6358**, Top-1 = **81.61%**, MRR = **0.8646**
  - $R_1$ (PANNs CNN14): mAP@10 = **0.1768**, Top-1 = **37.74%**, MRR = **0.5079**
  - $R_0$ (MFCC Baseline): mAP@10 = **0.0691**, Top-1 = **18.06%**, MRR = **0.3081**
  - $R_3$ (Random Control): mAP@10 = **0.0232**, Top-1 = **6.77%**, MRR = **0.1815**
- **E2 Noise Degradation (Derau Kampus ITERA):**
  - $R_2$ @ SNR -5 dB: mAP@10 = **0.4962** (Retensi 78.04%, CI: 74.0% – 82.1%)
  - $R_1$ @ SNR -5 dB: mAP@10 = **0.0982** (Retensi 55.53%, CI: 46.8% – 64.3%)
  - $R_0$ @ SNR -5 dB: mAP@10 = **0.0247** (Retensi 35.74%, CI: 27.5% – 44.0%)
  - $R_3$ @ SNR -5 dB: mAP@10 = **0.0231** (Retensi 99.46%, Tebakan Acak)
- **E3 Open-Set Frozen Threshold:**
  - $\tau^*_{R_2} = \mathbf{0.7071}$ (BirdNET: Youden $J = 0.4206$, AUROC = 0.7611, F1 = 0.6650)
  - $\tau^*_{R_1} = \mathbf{0.8974}$ (PANNs: Youden $J = 0.3734$, AUROC = 0.7141, F1 = 0.7033)
  - $\tau^*_{R_0} = \mathbf{0.9958}$ (MFCC Baseline: Youden $J = 0.0987$, AUROC = 0.5283, F1 = 0.3000)
  - $\tau^*_{R_3} = \mathbf{0.4481}$ (Random Control: Youden $J = 0.1202$, AUROC = 0.5662)
  - Evaluasi test set 310 kueri target + 310 unknown negatif membuktikan pergeseran titik operasi (H4 terdukung): $R_2$ mempertahankan pergeseran konservatif (Clean AUROC 0.7582, Recall 59.03%, FPR 20.00%; pada SNR -5 dB AUROC 0.6141, Recall 23.87%, FPR 9.35%), sedangkan $R_1$ memiliki FPR tinggi (Clean FPR 47.42%; SNR -5 dB FPR 27.10%).
- **E4 Sensitivitas Profil Spektral Derau Latar (3 Profil Habitat ITERA):**
  - $R_2$ @ SNR -5 dB: Kebun Raya 0.4434 (retensi 69.73%), Embung F 0.4842 (retensi 76.15%), Gedung F 0.4661 (retensi 73.30%). Selisih Kebun Raya vs Embung F: Mean Diff +0.0400 ($p = 0.0040$, biofoni serangga paling merusak).
  - $R_1$ @ SNR -5 dB: Kebun Raya 0.0590 (retensi 33.38%), Embung F 0.0949 (retensi 53.69%), Gedung F 0.0982 (retensi 55.55%). Ayunan retensi PANNs (22.17%) secara signifikan lebih rentan dibanding BirdNET (6.42%, selisih ayunan +17.07%, $p = 0.0010$).
  - Status Hipotesis H3: Sebagian terdukung (rentang stabilitas BirdNET lebih kokoh dibanding PANNs; domain shift rekaman in-situ liar tanpa kontrol aditif ditangguhkan).
- **E5 Failure Analysis Terstratifikasi Lintas Spesies:**
  - Audit kasus nyata terstratifikasi ($N=30$ kasus lintas 17 taksa burung Indonesia): Open-Set False Rejection 10 kasus (33.33%), Top-1 Confusion Above Tau 9 kasus (30.00%), Total Retrieval Collapse 11 kasus (36.67%).
- **Uji Statistik Inferensial (Bootstrap Resampling 1.000 Iterasi):**
  - Clean Retrieval: $R_2$ vs $R_1$ ($p < 0.001$), $R_2$ vs $R_0$ ($p < 0.001$), $R_1$ vs $R_0$ ($p < 0.001$).
  - Kontrol Acak H5: $R_2$ vs $R_3$ ($p < 0.001$), $R_1$ vs $R_3$ ($p < 0.001$), $R_0$ vs $R_3$ ($p < 0.001$).
  - Retensi SNR -5 dB: $R_2$ vs $R_1$ ($p < 0.001$), $R_1$ vs $R_0$ ($p = 0.0060$), $R_2$ vs $R_0$ ($p < 0.001$).
  - Cluster Bootstrap per Rekorder ($K=26$): $R_2$ vs $R_1$ ($p < 0.001$).
  - Komparasi Rentang Ayunan Habitat H3: $R_1$ vs $R_2$ ($p = 0.0010$).
- **Unit Testing Suite:** 10 dari 10 unit test lolos (100.0%).
