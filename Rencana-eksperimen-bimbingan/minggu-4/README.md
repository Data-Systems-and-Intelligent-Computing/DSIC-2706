# Minggu 4 — E5, Statistik, dan Pemetaan RQ/Hipotesis

**Tujuan:** mengklasifikasikan bentuk kegagalan retrieval secara transparan, menjalankan statistik berpasangan, lalu membatasi kesimpulan pada bukti yang tersedia.

## E5 — failure diagnostics

E5 memakai threshold beku dari E3. Untuk E2, ranking dapat direkonstruksi secara deterministik sehingga centroid, bandwidth, RMS, skor, dan margin dapat dihitung. Untuk E4, identitas Top-1, skor kelas benar, skor pesaing, margin kelas, dan fitur noisy yang memang tidak tersedia tetap ditandai sebagai tidak tersedia; nilainya tidak direka.

Empat kategori yang digunakan:

1. **Accepted correct:** Top-1 benar dan skor memenuhi τ*.
2. **Open-set false rejection:** Top-1 benar tetapi skor di bawah τ*.
3. **Top-1 confusion above threshold:** skor memenuhi τ* tetapi spesies Top-1 salah.
4. **Total retrieval collapse:** Top-1 salah dan skor di bawah τ*.

- Notebook: [08_E5_Failure_Diagnostics.ipynb](../../notebooks/08_E5_Failure_Diagnostics.ipynb)
- Kode: [run_e5_diagnostics.py](../../scripts/run_e5_diagnostics.py) dan [analyze_failures.py](../../src/analyze_failures.py)
- Run sumber: [E5 diagnostics](../../results/reproductions/E5_diagnostics_20261012T091512_868500Z/)
- Ringkasan: [E5 failure mode summary](../../results/tables/15_e5_failure_mode_summary.csv)
- Kasus terpilih: [E5 selected case manifest](../../results/tables/16_e5_selected_case_manifest.csv)
- Figure 1: [failure modes](../../results/figures/11_e5_failure_modes_by_representation.png)
- Figure 2: [margin distribution](../../results/figures/12_e5_margin_distribution_by_failure_type.png)
- Figure 3: [spectral features](../../results/figures/13_e5_spectral_features_by_failure_type.png)

**Status 30 Oktober: catatan audit manusia tersedia untuk 120/120 kasus pilihan.** CSV historis kehilangan kolom representasi, kondisi, dan moda kegagalan pada ekspor. [Lembar persiapan terpisah](../audit-pendengaran-E5/E5_AUDIT_PENDENGARAN.csv) memulihkan kolom melalui pencocokan persis ke diagnostik lengkap; lembar kosong dan hasil komputasional lama tetap utuh. Hasil manusia berada pada [CSV terisi](../audit-pendengaran-E5/E5_HASIL_ULASAN_2026-10-30.csv) dan [laporan 30 Oktober](../audit-pendengaran-E5/hasil-20261030/README.md), termasuk jejak satu koreksi E5_105 yang dikonfirmasi Fabio.

Fabio adalah satu-satunya pendengar. Dari 120 kasus, query dinyatakan terdengar pada 116 dan Top-1 pada 109; terdapat 80 query unik dan 117 pasangan query–kondisi. Sampel dipilih menurut kegagalan dan tidak dipakai mengestimasi tingkat kegagalan populasi atau kesepakatan antarpendengar. Label collapse berarti Top-1 salah dan skor di bawah ambang, bukan bukti sepuluh hasil semuanya salah.

## Statistik berpasangan

Bootstrap berpasangan menggunakan 10.000 iterasi, seed 20261012, dan unit resampling query. Uji yang tersedia mencakup H1–H5; H3 dihitung dari raw E4 sebagai perbandingan ayunan absolut/relatif lintas lokasi, termasuk sensitivitas tanpa Kebun Raya.

- Kode: [bootstrap_inference.py](../../src/bootstrap_inference.py)
- Run sumber: [statistics matrix](../../results/reproductions/STATISTICS_RQ_MATRIX_20261012T092924_809804Z/)
- Semua hasil bootstrap: [paired bootstrap](../../results/tables/22_statistics_paired_bootstrap.csv)
- Ringkasan retensi: [E2 retention](../../results/tables/18_statistics_e2_retention.csv)
- Matriks terkini: [RQ/H revisi](../../results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv)
- [Sensitivitas H3](../../results/reproductions/H3_sensitivity_20261015/tables/h3_swing_summary.csv); tabel 23 tetap menjadi riwayat.

| Hipotesis | Kesimpulan saat ini |
|---|---|
| H1 | Didukung: retensi R1 dan R2 pada −5 dB lebih tinggi dari R0. |
| H2 | Didukung: retensi R2 − R1 = 0,269212; CI 95% [0,160783, 0,364992]; p = 0,000100. |
| H3 | Eksploratif; kesimpulan bergantung skala dan subset. CI selisih rata-rata ayunan absolut lima lokasi mencakup nol; H3 asli real-soundscape belum diuji. |
| H4 | Reformulasi eksploratif; recall penerimaan known turun untuk R0–R2 pada −5 dB. FPR tidak meningkat. |
| H5 | Didukung: R0, R1, dan R2 mengungguli kontrol R3 pada clean AP@10. |

**Reproduksi 16 Oktober:** E0, ekstraksi clean R0–R3, E1, E2, E3, E5, serta statistik H3 selesai pada klon/venv baru di komputer yang sama; 41/41 pembandingan cocok, selisih numerik maksimum 0,0. Input berasal dari arsip lokal terverifikasi; inferensi E4 tidak diulang. [Laporan reproduksi](../../docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md).

**Riwayat tes:** 36/36 pada pemeriksaan 16 Oktober; 41 lulus, 0 dilewati/gagal/error pada 18 Oktober. Verifikasi audit 30 Oktober mencatat tujuh tes importer/finalizer lulus, bukan pengulangan seluruh suite. Pembaruan dokumentasi ini tidak menjalankan tes/eksperimen lagi. [Bukti audit terbaru](../audit-pendengaran-E5/hasil-20261030/verifikasi_akhir.json).

## Arah penulisan laporan

Gunakan matriks revisi dan [pemeriksaan ulang](../CATATAN_PROGRES_BIMBINGAN.md) sebagai sumber narasi terkini; hasil 12 Oktober tetap menjadi riwayat. Ambil gambar dari [results/figures](../../results/figures/) dan angka dari [results/tables](../../results/tables/). `paper/` masih draf; jangan memindahkan hasil lama ke naskah sebelum struktur Bab 4/Bab 5 diputuskan.

Untuk status audit gunakan laporan 30 Oktober; angka 0/120 pada catatan bimbingan/CURRENT_STATUS lama sudah kedaluwarsa. [Paket BAB 1–3](../../paper/persiapan_bab1_3/README.md) menyediakan diagram alir dan indeks bahan. Bukti penelitian cukup untuk mulai menulis dalam scope controlled additive mixtures; finalisasi judul/RQ, framing H3/H4, sistematika, sitasi, dan persetujuan pembimbing tetap perlu diselesaikan.
