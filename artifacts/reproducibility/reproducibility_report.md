# Laporan Audit Reproducibility Mandiri (DSIC-2706)

## 1. Spesifikasi Lingkungan Komputasi
- **Sistem Operasi:** Windows 11 (64-bit)
- **Python:** 3.14.0
- **Pustaka Utama:** Librosa, Soundfile, PyTorch, Scikit-Learn, Pandas, NumPy, Matplotlib, Seaborn
- **Seed Global:** 42

## 2. Integritas Partisi (Zero Leakage Check)
- **Metode Partisi:** Strict Global Recordist-Disjoint Cut ($\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset, \mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset, \mathcal{R}_{\text{Query}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset$)
- **Perekam Gallery:** 673 rekaman audio dari 59 perekam (*author*) unik
- **Perekam Query Clean:** 311 rekaman audio dari 27 perekam (*author*) unik (28 setelah nama komposit dipecah)
- **Perekam Calibration:** 232 rekaman audio dari 25 perekam (*author*) unik
- **Total Audio & Perekam:** 1.216 berkas audio dari 112 perekam (*author*) unik
- **Tumpang Tindih Perekam:** Tepat 0 perekam (0%)
- **Tumpang Tindih ID Rekaman:** 0 rekaman (0%)
- **Tumpang Tindih Berkas Path:** 0 berkas (0%)

## 3. Hasil Validasi Benchmark Kanonikal (Gate 1 s.d. Gate 4)
Hasil eksekusi benchmark pada korpus 20 Spesies Target Avifauna Indonesia (1.216 berkas audio fisik) dan bank derau fisik AudioMoth ITERA (1.799 berkas audio fisik):
- **E1 Clean Retrieval:**
  - $R_2$ (BirdNET Backbone): mAP@10 = **0.6370**, Top-1 = **81.67%**, MRR = **0.8650**, Precision@10 = **0.6942**, Recall@10 = **0.2325**
  - $R_1$ (PANNs CNN14): mAP@10 = **0.1771**, Top-1 = **37.94%**, MRR = **0.5090**, Precision@10 = **0.2586**, Recall@10 = **0.0843**
  - $R_0$ (MFCC Baseline): mAP@10 = **0.0690**, Top-1 = **18.01%**, MRR = **0.3079**, Precision@10 = **0.1308**, Recall@10 = **0.0360**
  - $R_3$ (Random Control): mAP@10 = **0.0231**, Top-1 = **6.75%**, MRR = **0.1811**, Precision@10 = **0.0615**, Recall@10 = **0.0150**
- **E2 Noise Degradation (Derau Kampus ITERA):**
  - $R_2$ @ SNR -5 dB: mAP@10 = **0.4968** (Retensi 77.99%, Top-1 = 64.31%)
  - $R_1$ @ SNR -5 dB: mAP@10 = **0.0979** (Retensi 55.27%, Top-1 = 18.97%)
  - $R_0$ @ SNR -5 dB: mAP@10 = **0.0248** (Retensi 35.89%, Top-1 = 9.65%)
  - $R_3$ @ SNR -5 dB: mAP@10 = **0.0230** (Retensi 99.44%, Tebakan Acak)
- **E3 Open-Set Frozen Threshold:**
  - $\tau^*_{R_2} = \mathbf{0.7071}$ (BirdNET: Youden $J = 0.4188$, TPR = 0.5733, FPR = 0.1545, AUROC = 0.7601, F1 = 0.6633)
  - $\tau^*_{R_1} = \mathbf{0.8974}$ (PANNs: Youden $J = 0.3766$, TPR = 0.7457, FPR = 0.3691, AUROC = 0.7167, F1 = 0.7047)
  - $\tau^*_{R_0} = \mathbf{0.9958}$ (MFCC Baseline: Youden $J = 0.0995$, TPR = 0.1940, FPR = 0.0944, AUROC = 0.5298, F1 = 0.3010)
  - $\tau^*_{R_3} = \mathbf{0.4481}$ (Random Control: Youden $J = 0.1191$, TPR = 0.7457, FPR = 0.6266, AUROC = 0.5658, F1 = 0.6279)
  - Evaluasi test set (311 kueri target + 310 unknown negatif) membuktikan pergeseran titik operasi (H4 terdukung): $R_2$ mempertahankan pergeseran konservatif (Clean AUROC 0.7589, Recall 59.16%, FPR 20.00%; pada SNR -5 dB AUROC 0.6153, Recall 24.12%, FPR 9.35%), sedangkan $R_1$ memiliki FPR tinggi (Clean FPR 47.42%; SNR -5 dB FPR 27.10%).
- **E4 Sensitivitas Profil Spektral Derau Latar (3 Profil Habitat ITERA):**
  - $R_2$ @ SNR -5 dB: Kebun Raya 0.4452 (retensi 69.89%), Embung F 0.4849 (retensi 76.12%), Gedung F 0.4665 (retensi 73.23%). Selisih Kebun Raya vs Embung F: Mean Diff +0.0398 ($p = 0.0040$, biofoni serangga paling merusak).
  - $R_1$ @ SNR -5 dB: Kebun Raya 0.0592 (retensi 33.43%), Embung F 0.0950 (retensi 53.64%), Gedung F 0.0983 (retensi 55.51%). Ayunan retensi PANNs secara signifikan lebih rentan dibanding BirdNET (selisih ayunan observasi $\Delta = 0.1560$, rata-rata bootstrap $+0.1692$, $p \le 0.001$).
  - Status Hipotesis H3: Sebagian terdukung (rentang stabilitas BirdNET lebih kokoh dibanding PANNs; domain shift rekaman in-situ liar tanpa kontrol aditif ditangguhkan).
- **E5 Failure Analysis Terstratifikasi Lintas Spesies:**
  - Audit kasus nyata terstratifikasi ($N=30$ kasus lintas 17 taksa burung Indonesia): Open-Set False Rejection 10 kasus (33.33%), Top-1 Confusion Above Tau 9 kasus (30.00%), Total Retrieval Collapse 11 kasus (36.67%).
- **Uji Statistik Inferensial (Bootstrap Resampling 1.000 Iterasi):**
  - Clean Retrieval: $R_2$ vs $R_1$ ($p \le 0.001$), $R_2$ vs $R_0$ ($p \le 0.001$), $R_1$ vs $R_0$ ($p \le 0.001$).
  - Kontrol Acak H5: $R_2$ vs $R_3$ ($p \le 0.001$), $R_1$ vs $R_3$ ($p \le 0.001$), $R_0$ vs $R_3$ ($p \le 0.001$).
  - Retensi SNR -5 dB: $R_2$ vs $R_1$ ($p \le 0.001$), $R_1$ vs $R_0$ ($p = 0.0050$), $R_2$ vs $R_0$ ($p \le 0.001$).
  - Cluster Bootstrap per Rekorder ($K=27$): $R_2$ vs $R_1$ ($p \le 0.001$).
  - Komparasi Rentang Ayunan Habitat H3: $R_1$ vs $R_2$ ($\Delta_{\text{obs}} = 0.1560$, $p \le 0.001$).
- **Unit Testing Suite:** Seluruh unit test lolos 100.0%.
- **Status Audit Mandiri:** Seluruh 13 pengujian otomatis lolos tanpa catatan kegagalan (`13 passed`).

## 4. Audit Fisik Dataset & Algoritma Pra-Pemrosesan (Verifikasi Audio Fisik)
- **Verifikasi Kuantitatif Jendela Energi Tertinggi (`select_highest_energy_window`):**
  - Dilakukan pengujian acak deterministik (seed 42) pada 50 klip audio fisik (40 klip berdurasi >60s dan 10 klip <5s) menggunakan skrip `scripts/audit_energy_window_acoustics.py`.
  - Hasil audit membuktikan akurasi penangkapan vokalisasi burung aktif mencapai 90.0% secara ketat spektral (centroid 4.382,5 Hz, bio-ratio 83.0%), dan mencapai 96.0% saat memperhitungkan bioakustik vokalisasi nada rendah alami spesies *Ducula aenea* (560–610 Hz).
  - Algoritma sliding window (hop 1.25s) secara konsisten mengabaikan jeda hening dan mengisolasi puncak panggilan aktif dengan penguatan energi RMS rata-rata **1.64×** (hingga 3.07×), tanpa terpengaruh oleh handling noise atau derau angin.
- **Rekonsiliasi Berkas Unknown (380 audio di disk vs 272 audio pada manifes):**
  - Sebanyak 380 berkas audio di `data/xeno_canto_indonesia_unknowns` (105 taksa) merupakan kandidat buffer pool hasil unduhan API Xeno-Canto.
  - Skrip `scripts/build_indonesia_unknown_manifest.py` secara ketat memilih 272 klip (117 untuk kalibrasi dan 155 untuk pengujian) guna menjaga rasio kueri positif berbanding unknown kontrol negatif tepat 1:1. Seluruh 272 berkas ada pada disk dengan SHA-256 100% cocok. Selisih 108 berkas adalah klip buffer cadangan yang sengaja tidak dimasukkan ke dalam partisi final untuk mempertahankan kuota 1:1.
