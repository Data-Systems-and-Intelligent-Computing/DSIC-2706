# Rencana Eksperimen dan Logbook Bimbingan — DSIC-2706

**Judul kerja:** *Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval under Controlled ITERA Field-Noise Mixtures in Indonesian Avifauna*  
**Pembaruan dokumentasi:** 30 Oktober 2026

**Korpus aktif:** 20 spesies avifauna Indonesia, 1.216 rekaman target, 1.799 rekaman derau ITERA.

Folder ini adalah peta pelaksanaan empat minggu. Semua angka dan tautan di bawah merujuk artefak lokal yang benar-benar ada. Hasil lama yang terkait imputasi `XC42472` tidak dipakai sebagai bukti penelitian.

## Cara membaca bukti penelitian

1. Buka [hasil audit E5 30 Oktober](audit-pendengaran-E5/hasil-20261030/README.md) untuk catatan terbaru 120/120 kasus. [Catatan Progres Bimbingan](CATATAN_PROGRES_BIMBINGAN.md) menjadi kronologi; status 0/120 pada entri lamanya sudah kedaluwarsa.
2. Buka README Minggu 1 sampai Minggu 4 sesuai tahap yang ingin dipelajari.
3. Buka [registri eksperimen](../experiments/experiment_registry.csv) untuk menghubungkan eksperimen, notebook, run, gambar, dan tabel.
4. Buka [matriks RQ/H revisi](../results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv) untuk kesimpulan terkini; dokumen hasil 12 Oktober tetap menjadi arsip.

## Status empat minggu

| Minggu | Tahap | Status bukti | Titik masuk utama |
|---|---|---|---|
| 1 | Dataset, preprocessing, EDA, E0, E1 | Tervalidasi | [Minggu 1](minggu-1/README.md) |
| 2 | Noise ITERA dan E2 | Selesai | [Minggu 2](minggu-2/README.md) |
| 3 | E3 threshold dan E4 habitat mixture | Selesai dengan batasan E4 | [Minggu 3](minggu-3/README.md) |
| 4 | E5, bootstrap, matriks RQ/H | Reproduksi yang diizinkan dan catatan audit manusia 120/120 tersedia; finalisasi naskah/persetujuan tetap terbuka | [Minggu 4](minggu-4/README.md) |

## Arah folder yang digunakan

| Kebutuhan | Lokasi |
|---|---|
| Data audio dan manifes | [data/](../data/) dan [data/manifests/](../data/manifests/) |
| Notebook langsung per tahap | [notebooks/](../notebooks/) |
| Kode pipeline | [src/](../src/) |
| Runner dan pembangun indeks | [scripts/](../scripts/) |
| Konfigurasi beku | [configs/](../configs/) |
| Run sumber tidak ditimpa | [results/reproductions/](../results/reproductions/) |
| Gambar laporan | [results/figures/](../results/figures/) |
| Tabel laporan | [results/tables/](../results/tables/) |
| Uji integritas | [tests/](../tests/) dan [run_tests.py](../run_tests.py) |

## Catatan batasan yang harus dipertahankan

E4 menggunakan pencampuran aditif dengan noise asli lima lokasi ITERA. H3 hasil reformulasi bersifat eksploratif; ayunan absolut, relatif, serta sensitivitas tanpa Kebun Raya menunjukkan kesimpulan bergantung metrik dan subset. Hasilnya tidak diklaim sebagai evaluasi burung yang direkam in-situ.

**Acuan status 30 Oktober:** E0–E5 mempunyai artefak, H1/H2/H5 didukung, H3/H4 reformulasi eksploratif, dan H3 asli real-soundscape belum diuji. Reproduksi terpisah menghasilkan [41/41 pembandingan cocok](../docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md), tanpa inferensi E4 ulang. Audit satu pendengar mencakup 120 kasus pilihan; tidak mengestimasi frekuensi kegagalan seluruh populasi. Bahan cukup untuk mulai menulis dalam scope aktif; judul/RQ final, sistematika, sitasi, dan naskah tetap perlu pembimbing.

[CURRENT_STATUS.md](CURRENT_STATUS.md) bertanggal 18 Oktober masih mencatat 0/120 audit. Baca sebagai ringkasan historis dan gunakan laporan 30 Oktober untuk status audit terkini. [Paket BAB 1–3](../paper/persiapan_bab1_3/README.md) menyediakan diagram alir dan indeks gambar/tabel; template bab masih kerangka.

## Persiapan bimbingan dan audit E5

[Siapa yang mendengarkan, langkah audit, dan penjelasan lisan H3/Recall@10](PANDUAN_AUDIT_E5_DAN_PENJELASAN_LISAN.md) tetap menjadi petunjuk metode. Untuk hasil yang dapat dibagikan gunakan [laporan audit 30 Oktober](audit-pendengaran-E5/hasil-20261030/README.md) beserta matriks revisi; laporan PEMENUHAN_REVISI yang dihapus tidak digunakan.
