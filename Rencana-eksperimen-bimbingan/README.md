# Rencana Eksperimen & Logbook Pelaksanaan (DSIC-2706)

Repositori ini memuat rencana kerja eksperimental 4 minggu (30 hari) dan rekam jejak bimbingan untuk topik penelitian:
**"Mencari Audio yang Mirip Ketika Datanya Terbatas" (DSIC-2706)**  
*Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise*

* **Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)
* **Dosen Pembimbing:** Bapak Ardika
* **Program Studi:** Sains Data, Institut Teknologi Sumatera (ITERA)
* **Status Terkini:** **SELURUH GATE 1 S.D. 4 SELESAI 100% (TERVERIFIKASI & MEMILIKI BUKTI EMPIRIS LENGKAP)**

---

### Dokumen Rekam Jejak Revisi & Progres:
Seluruh catatan kemajuan, audit metodologi, dan bukti numerik tercatat secara kronologis di:  
👉 **[CATATAN_PROGRES_BIMBINGAN.md](./CATATAN_PROGRES_BIMBINGAN.md)**

---

## Peta Navigasi Rencana Eksperimen & Status Gate

| Direktori Rencana | Fokus & Target Mingguan | Status Pelaksanaan | Tautan Dokumen |
| :--- | :--- | :---: | :--- |
| **[Minggu 1](./minggu-1/README.md)** | Dataset BirdCLEF+ 2026 (20 Spesies), Standarisasi Audio (32 kHz, 5s, RMS 0.05), EDA, E0 (Pipeline Sanity), dan E1 (Clean Retrieval) | **SELESAI 100% (GATE 1-R LOLOS)**<br>• 20 Spesies Target (4.351 Berkas Audio)<br>• Strict Recordist-Disjoint (0 Overlap Author, ID, Path)<br>• $R_2$ (BirdNET) 95.0% > $R_1$ 60.0% > $R_0$ 27.5% >> $R_3$ 6.5%<br>• Suite Uji Saintifik: 9/9 PASS (100.0%) | [Buka Dokumen Minggu 1](./minggu-1/README.md) |
| **[Minggu 2](./minggu-2/README.md)** | Akuisisi Derau Lapangan AudioMoth ITERA & Controlled Noise Robustness (Eksperimen E2: Paired Stress-Testing pada SNR +20, +10, 0, -5 dB) | **SELESAI 100% (GATE 2 LOLOS)**<br>• 1.799 Berkas WAV AudioMoth dari 5 Titik ITERA<br>• Manifes SHA-256 (`itera_noise_manifest.csv`)<br>• Fallback Pink Noise Dihapus Permanen<br>• $R_2$ mAP@10 = 0.7707 pada SNR -5 dB (Retensi 84.45%) | [Buka Dokumen Minggu 2](./minggu-2/README.md) |
| **[Minggu 3](./minggu-3/README.md)** | Open-Set Rejection & Kalibrasi Ambang Batas $\tau^*$ (Eksperimen E3) serta Evaluasi Sensitivitas Profil Derau Latar (E4) | **SELESAI 100% (GATE 3 LOLOS)**<br>• Kalibrasi Bebas Bocor $\tau^*_{R_2} = 0.7128, \tau^*_{R_1} = 0.9117$ via Youden's $J$<br>• Evaluasi 200 Unknown Test Negatif ($R_2$ FPR 9.5% vs $R_1$ FPR 81.5% pada -5 dB)<br>• Sensitivitas Profil Derau E4 vs E2 ($R_2$ invarian $p = 0.610$, $R_1$ sensitif $p < 0.001$) | [Buka Dokumen Minggu 3](./minggu-3/README.md) |
| **[Minggu 4](./minggu-4/README.md)** | Analisis Kegagalan Terstratifikasi (E5), Statistik Inferensial Komprehensif (Paired Bootstrap 1.000 Iterasi CI 95%), Naskah Skripsi, & Freeze Code | **SELESAI 100% (GATE 4 LOLOS)**<br>• Audit Terstratifikasi 30 Kasus Nyata (Clean & -5 dB, $R_2$ & $R_1$)<br>• Paired Bootstrap 7 Skenario ($R_2 > R_1$ $p < 0.001$, Retensi MFCC > PANNs $p < 0.001$)<br>• Repositori Sinkron Penuh & Lolos 9/9 Unit Tests (100%) | [Buka Dokumen Minggu 4](./minggu-4/README.md) |

---

## Hubungan Terhadap Tahapan Naskah Skripsi

Dokumentasi di folder `Rencana-eksperimen-bimbingan/` ini menjadi bukti fisik terverifikasi:

* **Tahap 1 (Dataset 20 Spesies BirdCLEF+, Manifes Bebas Bocor, & Baseline E0/E1):** Menjadi fondasi Bab 3 (Metodologi) dan Tabel 4.1 di Bab 4.
* **Tahap 2 (Akuisisi AudioMoth ITERA & Ketahanan Derau E2):** Menjadi Sub-bab 4.2 (Ketahanan Derau Aditif) beserta Gambar 4.1.
* **Tahap 3 (Open-Set E3 & Domain Shift E4):** Menjadi Sub-bab 4.3 (Evaluasi Ambang Batas $\tau^*$ & Pergeseran Domain Hutan).
* **Tahap 4 (Failure Analysis E5 & Uji Statistik Inferensial):** Menjadi Sub-bab 4.4 (Analisis Kegagalan & Signifikansi Statistik Bootstrap) serta Bab 5 (Kesimpulan).
