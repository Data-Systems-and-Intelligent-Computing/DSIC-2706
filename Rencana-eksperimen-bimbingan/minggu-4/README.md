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

## Statistik berpasangan

Bootstrap berpasangan menggunakan 10.000 iterasi, seed 20261012, dan unit resampling query. Uji yang tersedia mencakup H1–H5; H3 dihitung secara terpisah dari raw E4 sebagai perbandingan ayunan retensi lintas habitat.

- Kode: [bootstrap_inference.py](../../src/bootstrap_inference.py)
- Run sumber: [statistics matrix](../../results/reproductions/STATISTICS_RQ_MATRIX_20261012T092924_809804Z/)
- Semua hasil bootstrap: [paired bootstrap](../../results/tables/22_statistics_paired_bootstrap.csv)
- Ringkasan retensi: [E2 retention](../../results/tables/18_statistics_e2_retention.csv)
- Matriks akhir: [RQ/H matrix](../../results/tables/23_statistics_rq_hypothesis_matrix.csv)

| Hipotesis | Kesimpulan saat ini |
|---|---|
| H1 | Didukung: retensi R1 dan R2 pada −5 dB lebih tinggi dari R0. |
| H2 | Didukung: retensi R2 − R1 = 0,269212; CI 95% [0,160783, 0,364992]; p = 0,000100. |
| H3 | Didukung: ayunan retensi R1 = 0.240111, R2 = 0.048607; Δ = 0.191504, CI 95% [0.152203, 0.241969]. |
| H4 | Didukung untuk R0–R2 melalui penurunan recall acceptance known-set pada −5 dB. |
| H5 | Didukung: R0, R1, dan R2 mengungguli kontrol R3 pada clean AP@10. |

## Arah penulisan laporan

Gunakan [hasil RQ/H1–H5](../../docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md) sebagai sumber narasi hasil. Ambil gambar dari [results/figures](../../results/figures/) dan angka dari [results/tables](../../results/tables/). `paper/` masih draf; jangan memindahkan hasil lama ke naskah sebelum struktur Bab 4/Bab 5 diputuskan.
