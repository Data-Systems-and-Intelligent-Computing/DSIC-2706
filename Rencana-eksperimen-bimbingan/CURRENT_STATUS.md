# Status Saat Ini untuk Bimbingan

**Tanggal:** 12 Oktober 2026  
**Status teknis:** E0, EDA, E1, E2, E3, E4, E5, dan analisis H3 memiliki artefak lokal.  
**Status ilmiah:** H1, H2, H4, H5 didukung oleh uji yang ada. H3 menunjukkan stabilitas retensi R2 yang lebih tinggi daripada R1 dalam campuran noise ITERA; uji H3 ditambahkan setelah E4 selesai dan diperlakukan sebagai analisis eksploratif.

## Angka untuk bimbingan

- Dataset aktif: 673 Gallery, 311 Query, 232 Calibration. E3 memakai 233 unknown calibration dan 310 unknown test.
- E1 clean `mAP@10`: R0 0,0694; R1 0,1763; R2 0,6367; R3 0,0211.
- E2 pada −5 dB: retensi `mAP@10` R0 33,45%; R1 48,96%; R2 75,88%.
- E3 threshold beku R2: τ* = 0,702785; recall known-set turun dari 0,6045 (Clean) menjadi 0,2540 (−5 dB).
- E4/H3: ayunan retensi lintas lima lokasi, dirata-ratakan pada empat SNR, R1 = 0,240111 dan R2 = 0,048607; selisih = 0,191504, CI 95% [0,152203; 0,241969].

## Buka bukti berikut saat bimbingan

- [Ringkasan hasil RQ/H1–H5](../docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md)
- [Matriks RQ/H terkini](../results/tables/27_rq_hypothesis_matrix_current.csv)
- [Tabel H3 per SNR](../results/tables/24_h3_habitat_profile_stability.csv) dan [grafik H3](../results/figures/15_h3_habitat_retention_stability.png)
- [Registri eksperimen E0–E5](../experiments/experiment_registry.csv)
- [Indeks dan checksum 41 bahan laporan](../results/report_materials_manifest.json)

## Batas kesimpulan

H3 mengukur ayunan retensi akibat pencampuran noise dari lima lokasi ITERA. Analisis ini belum menguji apakah perubahan frekuensi tinggi/rendah menyebabkan selisih tersebut, dan tidak menguji rekaman burung yang dibuat langsung di ITERA. Bank noise ITERA bebas spesies target, sehingga anotasi spesies target tidak diperlukan untuk E2/E4. Beberapa status di [matriks statistik historis](../results/tables/23_statistics_rq_hypothesis_matrix.csv) memakai rumusan RQ/H3 lama; gunakan matriks terkini di atas.
