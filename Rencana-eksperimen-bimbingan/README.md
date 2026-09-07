# Rencana Eksperimen & Logbook Pelaksanaan (DSIC-2706)

Repositori ini memuat rencana kerja eksperimental 4 minggu (30 hari) dan rekam jejak tindak lanjut revisi bimbingan untuk topik penelitian:
**"Mencari Audio yang Mirip Ketika Datanya Terbatas" (DSIC-2706)**  
*Noise and Domain-Shift Robustness of Audio Representations for Cross-Domain Bioacoustic Retrieval: From Xeno-Canto to Environmental Soundscapes*

* **Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)
* **Dosen Pembimbing:** Bapak Ardika
* **Program Studi:** Sains Data, Institut Teknologi Sumatera (ITERA)
* **Terakhir Diperbarui:** 07 September 2026 (Audit Revisi Supervisi Komprehensif)

---

> [!TIP]
> ### 📖 Dokumen Rekam Jejak Revisi Terbaru:
> Seluruh matriks penyelesaian audit pembimbing per 7 September 2026 (C-01, C-02, C-03, M-01 s/d M-07) lengkap dengan **tautan berkas, baris kode, gambar kurva 95% CI, dan tabel data empiris** tercatat secara konsisten di:  
> 👉 **[CATATAN_PROGRES_BIMBINGAN.md](./CATATAN_PROGRES_BIMBINGAN.md)**

---

## 🗺️ Peta Navigasi Rencana Eksperimen & Status Gate

| Direktori Rencana | Fokus & Target Mingguan | Kesiapan Kriteria Gate | Tautan Dokumen |
| :--- | :--- | :---: | :--- |
| **[Minggu 1](./minggu-1/README.md)** | Dataset, Manifest, Standarisasi Audio, & Feasibility Pipeline | **Kriteria Teknis Terpenuhi (16 Spesies Sumatera, 416 Audio, 0 Leakage)** | [Buka Rencana Minggu 1](./minggu-1/README.md) |
| **[Minggu 2](./minggu-2/README.md)** | Controlled Noise Robustness (Paired SNR Stress-Testing) | **Kriteria Teknis Terpenuhi (Model BirdNET Asli 1024-d, Retensi 80.1%)** | [Buka Rencana Minggu 2](./minggu-2/README.md) |
| **[Minggu 3](./minggu-3/README.md)** | Open-Set Rejection, Kalibrasi $\tau^*$, & Validasi Soundscape | **Open-Set Dinamis Terpenuhi (C-02 Fix) — Validasi Lapangan ITERA Ditunda (D-03)** | [Buka Rencana Minggu 3](./minggu-3/README.md) |
| **[Minggu 4](./minggu-4/README.md)** | Statistik Inferensial (Bootstrap CI 95%), Naskah, & Freeze Code | **Selesai (Grafik 300 DPI Pita Galat & Notebook Resmi Siap)** | [Buka Rencana Minggu 4](./minggu-4/README.md) |

---

## 📑 Hubungan Terhadap Logbook Pertemuan Bimbingan

Struktur dokumentasi di folder `Rencana-eksperimen-bimbingan/` ini dirancang untuk menjadi bukti fisik pendukung pada **Logbook 14 Pertemuan** dan **Checklist Artefak Minimum Tugas Akhir**:

* **P1 (Penetapan Topik & RQ):** [docs/research/research-charter.md](../docs/research/research-charter.md)
* **P2 (Dataset, Pembanding, & Ukuran Keberhasilan):** [docs/research/scope-freeze.md](../docs/research/scope-freeze.md) (16 Spesies Aktual)
* **P3 (Rencana Eksperimen & Protokol Pengukuran):** [Rencana Minggu 2](./minggu-2/README.md) dan [docs/protocols/itera-recording.md](../docs/protocols/itera-recording.md)
* **P4 (Hasil Pembanding Pertama):** [CATATAN_PROGRES_BIMBINGAN.md](./CATATAN_PROGRES_BIMBINGAN.md) (Bagian Hasil Eksperimen Nyata)
* **P5 (Kesiapan Data & Pipeline Bebas Leakage):** [run_tests.py](../run_tests.py) (**9/9 Test Lolos 100%**)
* **P6 (Eksperimen Utama & Open-Set Calibration):** [results/processed/threshold_transfer_table.csv](../results/processed/threshold_transfer_table.csv)
* **P7 (Rencana Pengujian Lapangan ITERA):** [docs/protocols/itera-recording.md](../docs/protocols/itera-recording.md) *(Akan dilaksanakan pasca-bimbingan)*
