# Rencana Eksperimen & Logbook Pelaksanaan (DSIC-2706)

Repositori ini memuat rencana kerja eksperimental 4 minggu (30 hari) untuk topik penelitian:
**"Mencari Audio yang Mirip Ketika Datanya Terbatas" (DSIC-2706)**
*Noise and Domain-Shift Robustness of Audio Representations for Cross-Domain Bioacoustic Retrieval: From Xeno-Canto to ITERA Soundscapes*

* **Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)
* **Dosen Pembimbing:** Bapak Ardika
* **Program Studi:** Sains Data, Institut Teknologi Sumatera (ITERA)

---

## 🗺️ Peta Navigasi Rencana Eksperimen

| Direktori Rencana | Fokus & Target Mingguan | Status Gate | Tautan Dokumen |
| :--- | :--- | :---: | :--- |
| **[Minggu 1](./minggu-1/README.md)** | Dataset, Manifest, Standarisasi Audio, & Feasibility Pipeline | **LOLOS (PASSED 100%)** | [Buka Rencana Minggu 1](./minggu-1/README.md) |
| **[Minggu 2](./minggu-2/README.md)** | Controlled Noise Robustness (Paired SNR Stress-Testing) | **LOLOS (PASSED 100%)** | [Buka Rencana Minggu 2](./minggu-2/README.md) |
| **[Minggu 3](./minggu-3/README.md)** | Open-Set Rejection, Kalibrasi $\tau^*$, & Validasi Soundscape Lapangan | **60% SELESAI (On Going)** | [Buka Rencana Minggu 3](./minggu-3/README.md) |
| **[Minggu 4](./minggu-4/README.md)** | Statistik Inferensial (Bootstrap CI), Artikel Ilmiah, & Freeze Code | **DRAF SIAP (Dijadwalkan)** | [Buka Rencana Minggu 4](./minggu-4/README.md) |

---

## 📑 Hubungan Terhadap Logbook Pertemuan Bimbingan

Struktur dokumentasi di folder `Rencana-eksperimen/` ini dirancang untuk menjadi bukti fisik pendukung pada **Logbook 14 Pertemuan** dan **Checklist Artefak Minimum Tugas Akhir**:

* **P1 (Penetapan Topik & RQ):** [docs/research/research_boundaries.md](../docs/research/research_boundaries.md)
* **P2 (Dataset, Pembanding, & Ukuran Keberhasilan):** [Rencana-eksperimen/minggu-1/README.md](./minggu-1/README.md)
* **P3 (Rencana Eksperimen & Protokol Pengukuran):** [Rencana-eksperimen/minggu-2/README.md](./minggu-2/README.md) dan [docs/protocols/itera-recording.md](../docs/protocols/itera-recording.md)
* **P4 (Hasil Pembanding Pertama):** [Rencana-eksperimen/minggu-2/README.md](./minggu-2/README.md#hasil-benchmark-komparatif)
* **P5 (Kesiapan Data & Pipeline Bebas Leakage):** [tests/integration/test_split_leakage.py](../tests/integration/test_split_leakage.py)
* **P6 (Eksperimen Utama & Open-Set Calibration):** [Rencana-eksperimen/minggu-3/README.md](./minggu-3/README.md)
* **P7 (Eksperimen Domain Shift Real Soundscape ITERA):** [docs/protocols/itera-recording.md](../docs/protocols/itera-recording.md)
