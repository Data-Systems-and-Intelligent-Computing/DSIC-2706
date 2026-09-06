# Laporan Audit Reproducibility Mandiri (DSIC-2706)

## 1. Spesifikasi Lingkungan Komputasi
- **Sistem Operasi:** Windows 11 (64-bit)
- **Python:** 3.14.0
- **Pustaka Utama:** Librosa, Soundfile, PyTorch, Scikit-Learn, Pandas, NumPy, Matplotlib
- **Seed Global:** 42

## 2. Integritas Partisi (Zero Leakage Check)
- **Metode Partisi:** Strict Global Recordist-Disjoint Cut ($G_{\text{rec}} \cap Q_{\text{rec}} = \emptyset$)
- **Perekam Gallery:** 42 orang unik
- **Perekam Query:** 29 orang unik
- **Tumpang Tindih Perekam:** Tepat 0 orang (0%)
- **Tumpang Tindih ID Rekaman:** 0 rekaman

## 3. Hasil Validasi Fresh Command
Eksekusi fresh command melalui `python src/verify_reproducibility.py` mencocokkan nilai benchmark:
- $R_2$ Clean mAP@10 = 0.240802
- $R_2$ @ SNR 0 dB mAP@10 = 0.158901 (Identik hingga 6 digit desimal dengan tabel processed)
- Open-Set Frozen Threshold $\tau^* = 0.966971$
