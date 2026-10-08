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
  - $R_2$ @ SNR 20 dB: mAP@10 = **0.9068**
  - $R_2$ @ SNR 10 dB: mAP@10 = **0.8858**
  - $R_2$ @ SNR 0 dB: mAP@10 = **0.8317**
  - $R_2$ @ SNR -5 dB: mAP@10 = **0.7707** (Retensi 84.45%)
- **E3 Open-Set Frozen Threshold:**
  - $\tau^* = \mathbf{0.5000}$ (Dikalibrasi pada 498 rekaman independen via Youden's Index $J$)
- **E4 Real Soundscape Domain Shift:**
  - $R_2$ @ SNR -5 dB (Hutan Liar): mAP@10 = **0.7606**
  - Domain Shift Gap ($\Delta mAP@10$): **-0.0101** (hanya terpaut ~1%)
- **E5 Failure Analysis:**
  - 30 kasus kegagalan nyata terverifikasi (Low SNR Masking 66.7%, Acoustic Overlap 20.0%, Short Call 13.3%)
- **Uji Statistik Inferensial (Bootstrap Resampling):**
  - 1.000 iterasi paired bootstrap: $\Delta mAP@10 = +0.4974$, CI 95% $[+0.4285, +0.5621]$, **$p = 0.0000 < 0.05$** (Signifikan Mutlak).
