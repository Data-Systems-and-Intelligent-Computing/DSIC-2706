# Panduan Singkat Seluruh Kode Eksperimen (E0 - E5)
Dokumen ini merangkum fungsi, parameter, pustaka (library), dan hasil dari seluruh tahap eksperimen (E0 hingga E5) di dalam repositori skripsi Anda.

## 1. E0: Pipeline Sanity (Integritas Prapemrosesan)
- **Fungsi:** Memastikan kodingan memuat audio dengan format seragam (Target *Sampling Rate* 32.000 Hz) dan memotong durasi audio secara presisi ke jendela 5 detik (*chunking*). Ini juga memverifikasi bahwa tabel *Gallery* (Referensi) dan *Query* (Uji) tidak tumpang tindih dari perekam (*author*) yang sama.
- **Library:** `librosa`, `soundfile`, `pandas`, `numpy`.
- **Parameter Utama:** `TARGET_SR = 32000`, `TARGET_DUR = 5.0`.
- **Output:** Memori sistem yang tersanitasi (terfilter) untuk diproses ke E1.

## 2. E1: Clean Retrieval (Pengujian Akurasi Dasar)
- **Fungsi:** Menguji kecerdasan murni dari Model Representasi (R0-MFCC, R1-CNN14, R2-BirdNET, R3-Random) dalam mengenali 20 burung target pada rekaman **bersih** (tanpa derau). Ini adalah *baseline*.
- **Library:** `torch` (PyTorch untuk memuat model CNN14 & BirdNET), `sklearn.metrics.pairwise.cosine_similarity` (untuk menghitung kemiripan vektor).
- **Parameter Utama:** Model pembekuan (*Frozen weights*), fungsi *Cosine Distance*.
- **Output:** Nilai acuan mAP@10 tertinggi sebelum audio dirusak.

## 3. E2: Paired Noise Degradation (Uji Ketahanan Derau)
- **Fungsi:** Mencampur audio burung yang bersih (Query) dengan derau lingkungan dari rekaman AudioMoth kampus ITERA (Embung/Gedung F). Pencampuran dilakukan secara bertahap pada *Signal-to-Noise Ratio* (SNR) eksak. Semakin minus SNR-nya, semakin besar volume bisingnya.
- **Library:** `numpy` (untuk perhitungan akar persamaan daya sinyal audio / RMS).
- **Parameter Utama:** `snr_db = [20, 10, 0, -5]`. Nilai SNR -5 dB adalah ujian paling mematikan. `seed = 42` (agar derau yang dicampur selalu sama jika kode diulang).
- **Output:** `snr_robustness_table.csv` yang menunjukkan seberapa parah nilai mAP@10 anjlok dibandingkan E1.

## 4. E3: Open-Set Calibration (Sistem Penolakan Suara Asing)
- **Fungsi:** Mencari ambang batas presisi (skor kalibrasi $\tau$) menggunakan Statistik *Youden's J*. Tujuannya agar sistem AI berani "Menolak" (Reject) jika mendengarkan rekaman yang ternyata adalah suara macan atau katak, bukannya malah menebak salah satu dari 20 burung.
- **Library:** `sklearn.metrics.roc_curve`, `pandas`.
- **Parameter Utama:** `Objective = Youden_J`. Memisahkan distribusi skor burung vs distribusi skor non-burung (*Unknown*).
- **Output:** Nilai `Frozen Tau` ($\tau$) untuk tiap model, serta tabel `threshold_transfer_table.csv`.

## 5. E4: Noise Profile Sensitivity (Sensitivitas Profil Spektral Derau Lintas Habitat)
- **Fungsi:** Menguji kepekaan representasi audio terhadap perbedaan spektral derau latar nyata dari 3 profil habitat kampus ITERA (Kebun Raya / biophony serangga, Embung F / resonansi air dan angin, Gedung F / koridor antropogenik-struktural). Menguji apakah representasi tetap stabil atau mengalami distorsi ketika karakter spektral derau berubah pada SNR yang setara.
- **Library:** `librosa`, `numpy`, `pandas`, `matplotlib`.
- **Output:** `e4_domain_shift_table.csv` dan visualisasi grafik `e4_noise_profile_sensitivity.png`.

## 6. E5: Failure Analysis (Analisis Kegagalan Nyata)
- **Fungsi:** Mengambil catatan tebakan AI yang SALAH MENEBAK (Top-1 match = 0) dari *log raw* CSV. Melakukan analisis diagnostik mengapa sistem gagal, misalnya apakah karena tertutup suara derau -5dB (*Low SNR Masking*) atau karena kicauannya mirip dengan spesies sepupu (*Inter-species Confusion*).
- **Library:** `pandas`, `pathlib`.
- **Output:** `failure_analysis_table.csv`. Berisi 30 daftar file audio yang gagal ditebak oleh mesin berserta alasan saintifik kegagalannya. Tabel ini sangat penting untuk dikupas mendalam di sub-bab terakhir Pembahasan Skripsi.
