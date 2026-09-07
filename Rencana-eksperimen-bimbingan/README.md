# Rencana Eksperimen & Logbook Pelaksanaan (DSIC-2706)

Repositori ini memuat rencana kerja eksperimental 4 minggu (30 hari) untuk topik penelitian:
**"Mencari Audio yang Mirip Ketika Datanya Terbatas" (DSIC-2706)**
*Noise and Domain-Shift Robustness of Audio Representations for Cross-Domain Bioacoustic Retrieval: From Xeno-Canto to ITERA Soundscapes*

* **Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)
* **Dosen Pembimbing:** Bapak Ardika
* **Program Studi:** Sains Data, Institut Teknologi Sumatera (ITERA)

---

## 🗺️ Peta Navigasi Rencana Eksperimen

| Direktori Rencana | Fokus & Target Mingguan | Kesiapan Kriteria Gate | Tautan Dokumen |
| :--- | :--- | :---: | :--- |
| **[Minggu 1](./minggu-1/README.md)** | Dataset, Manifest, Standarisasi Audio, & Feasibility Pipeline | **Kriteria Teknis Terpenuhi (Siap Ditinjau)** | [Buka Rencana Minggu 1](./minggu-1/README.md) |
| **[Minggu 2](./minggu-2/README.md)** | Controlled Noise Robustness (Paired SNR Stress-Testing) | **Kriteria Teknis Terpenuhi (Siap Ditinjau)** | [Buka Rencana Minggu 2](./minggu-2/README.md) |
| **[Minggu 3](./minggu-3/README.md)** | Open-Set Rejection, Kalibrasi $\tau^*$, & Validasi Soundscape Lapangan | **Dalam Pengerjaan (Sebagian Siap Ditinjau)** | [Buka Rencana Minggu 3](./minggu-3/README.md) |
| **[Minggu 4](./minggu-4/README.md)** | Statistik Inferensial (Bootstrap CI), Artikel Ilmiah, & Freeze Code | **Draf Awal Siap (Terjadwal)** | [Buka Rencana Minggu 4](./minggu-4/README.md) |

---

## 📑 Hubungan Terhadap Logbook Pertemuan Bimbingan

Struktur dokumentasi di folder `Rencana-eksperimen-bimbingan/` ini dirancang untuk menjadi bukti fisik pendukung pada **Logbook 14 Pertemuan** dan **Checklist Artefak Minimum Tugas Akhir**:

* **P1 (Penetapan Topik & RQ):** [docs/research/research_boundaries.md](../docs/research/research_boundaries.md)
* **P2 (Dataset, Pembanding, & Ukuran Keberhasilan):** [Rencana Minggu 1](./minggu-1/README.md)
* **P3 (Rencana Eksperimen & Protokol Pengukuran):** [Rencana Minggu 2](./minggu-2/README.md) dan [docs/protocols/itera-recording.md](../docs/protocols/itera-recording.md)
* **P4 (Hasil Pembanding Pertama):** [Rencana Minggu 2](./minggu-2/README.md#hasil-benchmark-komparatif)
* **P5 (Kesiapan Data & Pipeline Bebas Leakage):** [tests/integration/test_split_leakage.py](../tests/integration/test_split_leakage.py)
* **P6 (Eksperimen Utama & Open-Set Calibration):** [Rencana Minggu 3](./minggu-3/README.md)
* **P7 (Eksperimen Domain Shift Real Soundscape ITERA):** [docs/protocols/itera-recording.md](../docs/protocols/itera-recording.md)

---

## 📚 Dokumen Pegangan & Rekam Jejak Bimbingan
* 📖 **[Catatan Progres Lengkap & FAQ Teknis (CATATAN_PROGRES_BIMBINGAN.md)](./CATATAN_PROGRES_BIMBINGAN.md)**: Rekam jejak seluruh data, parameter audio, tabel hasil benchmark, serta penjelasan konsep teknis.
* 🗣️ **[Panduan Pembicaraan Meeting Bimbingan (PANDUAN_MEETING_PEMBIMBING.md)](./PANDUAN_MEETING_PEMBIMBING.md)**: Panduan ringkas berbicara dan menyampaikan progres di hadapan dosen pembimbing.
