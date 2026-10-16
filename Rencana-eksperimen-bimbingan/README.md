# Rencana Eksperimen dan Logbook Bimbingan — DSIC-2706

**Judul kerja:** *Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval under Controlled ITERA Field-Noise Mixtures in Indonesian Avifauna*  
**Pembaruan terakhir:** 16 Oktober 2026

**Korpus aktif:** 20 spesies avifauna Indonesia, 1.216 rekaman target, 1.799 rekaman derau ITERA.

Folder ini adalah peta pelaksanaan empat minggu. Semua angka dan tautan di bawah merujuk artefak lokal yang benar-benar ada. Hasil lama yang terkait imputasi `XC42472` tidak dipakai sebagai bukti penelitian.

## Cara membaca bukti penelitian

1. Buka [Catatan Progres Bimbingan](CATATAN_PROGRES_BIMBINGAN.md) untuk kronologi, hasil, dan batasan ilmiah.
2. Buka README Minggu 1 sampai Minggu 4 sesuai tahap yang ingin dipelajari.
3. Buka [registri eksperimen](../experiments/experiment_registry.csv) untuk menghubungkan eksperimen, notebook, run, gambar, dan tabel.
4. Buka [matriks RQ/H revisi](../results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv) untuk kesimpulan terkini; dokumen hasil 12 Oktober tetap menjadi arsip.

## Status empat minggu

| Minggu | Tahap | Status bukti | Titik masuk utama |
|---|---|---|---|
| 1 | Dataset, preprocessing, EDA, E0, E1 | Tervalidasi | [Minggu 1](minggu-1/README.md) |
| 2 | Noise ITERA dan E2 | Selesai | [Minggu 2](minggu-2/README.md) |
| 3 | E3 threshold dan E4 habitat mixture | Selesai dengan batasan E4 | [Minggu 3](minggu-3/README.md) |
| 4 | E5, bootstrap, matriks RQ/H | Reproduksi tahap yang diizinkan selesai; audit manusia terbuka | [Minggu 4](minggu-4/README.md) |

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

Gunakan [CURRENT_STATUS.md](CURRENT_STATUS.md) sebagai ringkasan satu halaman saat bimbingan.
