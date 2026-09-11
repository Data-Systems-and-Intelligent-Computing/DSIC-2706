# Rencana Eksperimen & Logbook Pelaksanaan (DSIC-2706)

Repositori ini memuat rencana kerja eksperimental 4 minggu (30 hari) dan rekam jejak bimbingan untuk topik penelitian:
**"Mencari Audio yang Mirip Ketika Datanya Terbatas" (DSIC-2706)**  
*Noise and Domain-Shift Robustness of Audio Representations for Cross-Domain Bioacoustic Retrieval: From Xeno-Canto to Environmental Soundscapes*

* **Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)
* **Dosen Pembimbing:** Bapak Ardika
* **Program Studi:** Sains Data, Institut Teknologi Sumatera (ITERA)
* **Status Terkini:** Minggu Ke-1 (GATE 1) Selesai 100%. Minggu 2 s.d 4 Belum Dilakukan (Terjadwal).

---

### Dokumen Rekam Jejak Revisi & Progres:
Seluruh catatan kemajuan, audit metodologi, dan bukti numerik tercatat secara kronologis di:  
👉 **[CATATAN_PROGRES_BIMBINGAN.md](./CATATAN_PROGRES_BIMBINGAN.md)**

---

## Peta Navigasi Rencana Eksperimen & Status Gate

| Direktori Rencana | Fokus & Target Mingguan | Status Pelaksanaan | Tautan Dokumen |
| :--- | :--- | :---: | :--- |
| **[Minggu 1](./minggu-1/README.md)** | Dataset 14 Spesies Sumatera, Standarisasi Audio, EDA, E0 (Pipeline Sanity), dan E1 (Clean Retrieval) | **SELESAI 100% (GATE 1 LOLOS)**<br>• 14 Spesies Sumatera (162 Berkas MP3)<br>• Zero Split Leakage (ID & Path Overlap = 0)<br>• $R_2$ (BirdNET) 78.57% > $R_1$ 57.14% > $R_0$ 28.57% >> $R_3$ 7.14% | [Buka Dokumen Minggu 1](./minggu-1/README.md) |
| **[Minggu 2](./minggu-2/README.md)** | Controlled Noise Robustness (Eksperimen E2: Paired Stress-Testing pada SNR Clean, 20dB, 10dB, 0dB, -5dB) | **BELUM DILAKUKAN**<br>*(Terjadwal untuk Minggu Ke-2)* | [Buka Rencana Minggu 2](./minggu-2/README.md) |
| **[Minggu 3](./minggu-3/README.md)** | Open-Set Rejection & Kalibrasi Ambang Batas Tau (Eksperimen E3 & E4) | **BELUM DILAKUKAN**<br>*(Terjadwal untuk Minggu Ke-3)* | [Buka Rencana Minggu 3](./minggu-3/README.md) |
| **[Minggu 4](./minggu-4/README.md)** | Analisis Kasus Kegagalan (E5), Statistik Inferensial (Bootstrap CI 95%), Naskah Skripsi, & Freeze Code | **BELUM DILAKUKAN**<br>*(Terjadwal untuk Minggu Ke-4)* | [Buka Rencana Minggu 4](./minggu-4/README.md) |

---

## Hubungan Terhadap Tahapan Bimbingan

Dokumentasi di folder `Rencana-eksperimen-bimbingan/` ini menjadi bukti fisik terverifikasi:

* **Tahap 1 (Dataset 14 Spesies, Manifes, & Baseline E0/E1):** Telah selesai di [Minggu 1](./minggu-1/README.md).
* **Tahap 2 (Ketahanan Derau Terkendali E2):** Dirancang pada [Minggu 2](./minggu-2/README.md).
* **Tahap 3 (Open-Set & Kalibrasi Tau E3):** Dirancang pada [Minggu 3](./minggu-3/README.md).
* **Tahap 4 (Evaluasi Lengkap & Naskah Akhir):** Dirancang pada [Minggu 4](./minggu-4/README.md).

