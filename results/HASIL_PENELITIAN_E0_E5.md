# Hasil penelitian pencarian rekaman suara burung Indonesia

**BirdNET menghasilkan kualitas pencarian tertinggi pada kondisi acuan dan pada seluruh tingkat derau yang diuji.** Pada kondisi terberat (−5 dB), BirdNET mempertahankan 75,88% kinerja acuannya. Namun, dengan ambang penerimaan yang ditetapkan sebelum pengujian, hanya 25,40% kueri target diterima pada kondisi tersebut. Artinya, kemampuan menempatkan spesies yang sesuai di urutan atas dan kemampuan menerima kueri berdasarkan skor perlu dibaca sebagai dua hasil yang berbeda.

Angka utama berasal dari eksperimen Oktober 2026. Pemeriksaan ulang November dijelaskan pada akhir laporan. [Registri eksperimen](../configs/active_runs.json) · [Log keputusan](../docs/research/decision-log.md)

## Data yang masuk ke eksperimen

Sebanyak 1.216 rekaman Xeno-Canto mencakup 20 spesies target dan 111 perekam. Pembagian berdasarkan perekam menghasilkan 673 rekaman galeri sebagai pembanding, 232 rekaman untuk kalibrasi, dan 311 kueri uji. Seluruh kelompok mencakup 20 spesies. Pemeriksaan nama perekam, kode katalog, dan isi berkas tidak menemukan tumpang tindih antarkelompok target.

Satu berkas derau lapangan rusak dikeluarkan. Dari 1.799 berkas derau Itera yang dapat digunakan, 1.528 disediakan untuk dicampur dengan kueri dan 271 disisihkan sebagai kontrol suara lingkungan. Bersama 272 rekaman dari 69 spesies burung non-target, tersedia 543 kontrol. Kalibrasi memakai 117 rekaman burung non-target dan 116 derau lingkungan. Pengujian memakai 155 rekaman dari masing-masing sumber. [Manifes target](../data/manifests/dataset_split.csv) · [Manifes kontrol](../data/manifests/unknown_open_set_manifest.csv)

## E0 · Hasil prapemrosesan dan audit

Seluruh 100 rekaman yang diperiksa (55 galeri, 26 kueri uji, dan 19 kalibrasi) dapat dibaca. Durasi asli berkisar dari 4,48 hingga 199,15 detik dengan median 31,86 detik. Enam berkas memiliki ekstensi yang berbeda dari format isinya, tetapi seluruh keluaran audit tetap mencapai 160.000 sampel bernilai hingga, setara dengan 5 detik pada 32 kHz. Pemeriksaan vektor menghasilkan dimensi 40 untuk MFCC (R0), 2.048 untuk PANNs CNN14 (R1), 1.024 untuk BirdNET (R2), dan 40 untuk kontrol acak berbasis ID (R3). Norma L2 hasil pemeriksaan mendekati satu pada keempatnya.

[e0_summary](tables/01_e0_summary.csv) · [e0_representation_probe](tables/02_e0_representation_probe.csv) · [e0_per_recording](tables/03_e0_per_recording.csv) · [eda_summary_by_source](tables/04_eda_summary_by_source.csv) · [eda_target_species_summary](tables/05_eda_target_species_summary.csv) · [eda_noise_location_summary](tables/06_eda_noise_location_summary.csv) · [eda_physical_audio_inventory](tables/07_eda_physical_audio_inventory.csv)

## E1 · Kualitas pencarian tanpa penambahan derau

Untuk setiap kueri, 673 rekaman galeri diurutkan berdasarkan kemiripan kosinus. Hasil dianggap relevan jika spesiesnya sama dengan kueri. mAP@10 memperhitungkan posisi hasil yang relevan di sepuluh peringkat teratas. Top-1 mengukur ketepatan spesies pada peringkat pertama, sedangkan MRR merangkum posisi kemunculan pertama spesies yang sesuai. Seluruh angka pada tabel berskala 0 sampai 1.

| Representasi | mAP@10 | Top-1 | MRR | Precision@10 | Recall@10 |
| --- | --- | --- | --- | --- | --- |
| R0 | 0,0694 | 0,1833 | 0,3109 | 0,1312 | 0,0363 |
| R1 | 0,1763 | 0,3762 | 0,5070 | 0,2585 | 0,0842 |
| R2 | 0,6367 | 0,8167 | 0,8652 | 0,6939 | 0,2331 |
| R3 | 0,0211 | 0,0643 | 0,1639 | 0,0569 | 0,0141 |

BirdNET menempati urutan pertama pada seluruh metrik. Ketiga representasi audio mengungguli kontrol acak pada AP@10 dalam pembandingan berpasangan atas 311 kueri. [e1_clean_retrieval_summary](tables/10_e1_clean_retrieval_summary.csv) · [statistics_paired_bootstrap](tables/22_statistics_paired_bootstrap.csv)

## E2 · Perubahan kualitas setelah kueri dicampur derau

Setiap sel memuat **mAP@10 / retensi (%)**. Retensi membagi mAP@10 kondisi berderau dengan mAP@10 acuan dari representasi yang sama. Untuk setiap kueri, segmen derau dipertahankan ketika tingkat SNR diubah. Galeri tetap sama.

| Representasi | +20 dB | +10 dB | 0 dB | −5 dB |
| --- | --- | --- | --- | --- |
| R0 | 0,0770 / 110,94 | 0,0604 / 87,06 | 0,0323 / 46,60 | 0,0232 / 33,45 |
| R1 | 0,1849 / 104,90 | 0,1721 / 97,66 | 0,1188 / 67,40 | 0,0863 / 48,96 |
| R2 | 0,6378 / 100,17 | 0,6213 / 97,58 | 0,5549 / 87,15 | 0,4832 / 75,88 |
| R3 | 0,0211 / 100,00 | 0,0211 / 100,00 | 0,0211 / 100,00 | 0,0211 / 100,00 |

Pada −5 dB, selisih retensi BirdNET dan PANNs mencapai 26,92 poin persentase (interval kepercayaan 95% dari 16,08 hingga 36,50 poin). R3 menghasilkan vektor dari ID rekaman sehingga nilainya tetap ketika audio berubah. [e2_snr_robustness](tables/11_e2_snr_robustness.csv) · [statistics_e2_retention](tables/18_statistics_e2_retention.csv) · [statistics_paired_bootstrap](tables/22_statistics_paired_bootstrap.csv)

## E3 · Kalibrasi ambang dan penerimaan kueri

Satu ambang dipilih untuk setiap representasi menggunakan kurva ROC dan indeks Youden pada 232 target dan 233 kontrol kalibrasi. AUROC menggambarkan kemampuan skor membedakan target dan kontrol di berbagai ambang. Indeks Youden pada ambang terpilih adalah tingkat penerimaan target dikurangi tingkat penerimaan kontrol.

| Representasi | Ambang | AUROC kalibrasi | Indeks Youden |
| --- | --- | --- | --- |
| R0 | 0,995752 | 0,5332 | 0,0995 |
| R1 | 0,897416 | 0,7098 | 0,3723 |
| R2 | 0,702785 | 0,7600 | 0,4188 |
| R3 | 0,488838 | 0,5452 | 0,0874 |

Pada pengujian, kueri diterima jika skor kemiripan tertingginya mencapai ambang. Setiap sel menunjukkan **target yang diterima (%) / kontrol yang diterima sebagai target (%)**, masing-masing dari 311 target dan 310 kontrol.

| Representasi | Acuan | +20 dB | +10 dB | 0 dB | −5 dB |
| --- | --- | --- | --- | --- | --- |
| R0 | 18,65 / 13,87 | 24,12 / 13,55 | 23,47 / 14,19 | 4,82 / 3,55 | 0,96 / 1,29 |
| R1 | 83,60 / 47,74 | 83,60 / 47,74 | 77,81 / 41,61 | 60,13 / 31,29 | 44,05 / 25,16 |
| R2 | 60,45 / 22,26 | 55,31 / 17,74 | 49,20 / 14,19 | 32,48 / 14,52 | 25,40 / 12,90 |
| R3 | 36,33 / 27,42 | 36,33 / 27,42 | 36,33 / 27,42 | 36,33 / 27,42 | 36,33 / 27,42 |

Dari acuan ke −5 dB, penerimaan target turun pada ketiga representasi audio. Penerimaan kontrol juga turun. Pada BirdNET, penurunan penerimaan target sebesar 35,05 poin persentase menunjukkan bahwa ambang dari kondisi acuan semakin sulit dicapai pada kueri berderau. [e3_frozen_thresholds](tables/12_e3_frozen_thresholds.csv) · [e3_threshold_transfer](tables/13_e3_threshold_transfer.csv) · [statistics_e3_threshold_transfer](tables/19_statistics_e3_threshold_transfer.csv)

## E4 · Perbedaan kinerja menurut sumber derau

Di setiap lokasi, 311 kueri diuji pada empat SNR dengan empat ulangan. Rancangan ini menghasilkan 80 kombinasi atau 24.880 evaluasi kueri berderau per representasi. Berikut rata-rata mAP@10 BirdNET atas empat ulangan pada setiap kombinasi lokasi dan SNR.

| Lokasi | +20 dB | +10 dB | 0 dB | −5 dB |
| --- | --- | --- | --- | --- |
| Embung F | 0,6366 | 0,6233 | 0,5655 | 0,5040 |
| Gedung F | 0,6371 | 0,6177 | 0,5403 | 0,4541 |
| Kebun Raya | 0,6439 | 0,6185 | 0,5318 | 0,4446 |
| Masjid At Tanwir | 0,6442 | 0,6302 | 0,5643 | 0,5025 |
| Sekitar GKU 1 | 0,6419 | 0,6244 | 0,5391 | 0,4547 |

Untuk membandingkan kestabilan, rentang dihitung dari selisih mAP@10 lokasi tertinggi dan terendah pada SNR dan ulangan yang sama. Rentang relatif membagi selisih itu dengan mAP@10 acuan representasi tersebut. Pada lima lokasi, selisih rentang relatif PANNs dikurangi BirdNET adalah 0,1915 (IK 95% dari 0,1522 hingga 0,2420). Untuk rentang absolut, IK 95% mencakup nol (−0,0040 hingga 0,0221). Ketika Kebun Raya dikeluarkan, selisih rentang relatif pada −5 dB juga memiliki interval yang mencakup nol. Maka, keunggulan BirdNET dalam kualitas pencarian lebih konsisten daripada kesimpulan tentang kestabilannya antarlokasi. Analisis kestabilan ini bersifat eksploratif. [e4_domain_shift](tables/14_e4_domain_shift.csv) · [h3_habitat_profile_stability](tables/24_h3_habitat_profile_stability.csv) · [h3_retention_by_habitat_repeat](tables/25_h3_retention_by_habitat_repeat.csv) · [Analisis sensitivitas lokasi](reproductions/H3_leave_one_location_out_20261018/README.md)

## E5 · Pola kegagalan dan hasil audit pendengaran

Setiap hasil dikelompokkan menurut kecocokan spesies pada peringkat pertama dan apakah skornya mencapai ambang E3. Tabel berikut menjumlahkan hasil per representasi pada 311 kueri target dalam lima kondisi E2 (acuan dan empat SNR). Setiap baris mewakili 1.555 evaluasi atas kueri yang sama.

| Representasi | Cocok, diterima | Cocok, ditolak | Berbeda, diterima | Berbeda, ditolak |
| --- | --- | --- | --- | --- |
| R0 | 63 | 147 | 161 | 1184 |
| R1 | 389 | 120 | 697 | 349 |
| R2 | 626 | 574 | 67 | 288 |
| R3 | 45 | 55 | 520 | 935 |

Untuk BirdNET, tabel berikut merangkum kasus gagal di E2 dengan median. Margin adalah skor tertinggi dikurangi ambang. Sentroid merangkum pusat frekuensi spektrum kueri, sedangkan lebar pita menggambarkan sebarannya. Angka spektral menjelaskan ciri kasus yang diamati dan belum menetapkan penyebab kegagalannya.

| Kasus BirdNET | Margin | Sentroid (Hz) | Lebar pita (Hz) |
| --- | --- | --- | --- |
| Cocok, ditolak | -0,0434 | 4374 | 3832 |
| Berbeda, diterima | 0,0313 | 4182 | 3491 |
| Berbeda, ditolak | -0,0693 | 4541 | 3893 |

[e5_failure_mode_summary](tables/15_e5_failure_mode_summary.csv) · [e5_selected_case_manifest](tables/16_e5_selected_case_manifest.csv) · [e5_unknown_open_set_diagnostics](tables/17_e5_unknown_open_set_diagnostics.csv) · [Hasil diagnosis per kueri](reproductions/E5_diagnostics_20261012T091512_868500Z/tables/all_query_diagnostics.csv)

**Audit pendengaran.** Peneliti mendengarkan 120 kasus yang mencakup 80 kueri unik. Dua kasus dipilih dari setiap kombinasi empat representasi, lima kondisi uji, dan tiga jenis kegagalan. Pada kueri, suara burung terdengar dalam 116 kasus dan tidak terdengar dalam empat kasus. Pada rekaman galeri peringkat pertama, suara burung terdengar dalam 109 kasus, tidak terdengar dalam delapan kasus, dan diragukan dalam tiga kasus. Dalam 106 kasus, suara burung terdengar pada kedua rekaman. Artinya, pencarian dapat gagal meskipun suara burung masih terdengar. Audit oleh satu pendengar ini menggambarkan kasus terpilih. Identitas spesies tetap mengacu pada label rekaman. [Hasil audit dan rincian menurut kondisi](../Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md)

## Pemeriksaan ulang dan kesimpulan

Pengulangan 16 November menghasilkan ringkasan E2 yang konsisten hingga toleransi numerik 10⁻¹². Pada E3, proporsi penerimaan target dan kontrol tetap sama. Pada E4, perbedaan mAP@10 PANNs terbesar antara dua pengujian yang dipadankan sekitar 0,000204. BirdNET memperoleh mAP@10 tertinggi pada seluruh 80 kombinasi lokasi, SNR, dan ulangan dalam pengulangan tersebut. [Hasil E2 November](reproductions/E2_controlled_20261116T132030_189809Z/tables/e2_snr_robustness.csv) · [Hasil E3 November](reproductions/E3_open_set_20261116T134710_006216Z/tables/threshold_transfer.csv) · [Hasil E4 November](reproductions/E4_5sites_20261116T131634_985229Z/tables/e4_domain_shift_table.csv)

Di antara tiga representasi audio yang diuji, **BirdNET merupakan pilihan yang paling didukung hasil untuk mengurutkan rekaman spesies yang sama ketika kueri diberi derau Itera**. Untuk penggunaan yang juga memerlukan keputusan menerima atau menolak kueri, hasil E3 menunjukkan konsekuensi praktis penggunaan ambang tetap pada rekaman berderau. Kesimpulan ini berlaku untuk galeri tetap dan campuran rekaman Xeno-Canto dengan derau lapangan yang diuji. Kinerja pada rekaman burung yang diperoleh langsung di lokasi memerlukan pengujian tersendiri. [Matriks temuan dan batas kesimpulan](tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv)

Pada E0, seluruh nilai ringkasan November sesuai dengan Oktober. Dalam diagnosis E5, hitungan kategori untuk kueri E2 juga sesuai. Perbedaan kecil muncul pada PANNs dalam kondisi E4. Misalnya, pada −5 dB jumlah hasil pertama yang berbeda spesies tetapi diterima berubah dari 2.170 menjadi 2.169, sedangkan jumlah hasil pertama yang berbeda spesies dan ditolak berubah dari 2.858 menjadi 2.859.

## Lampiran · Berkas sumber hasil penelitian

Kolom Oktober berisi hasil utama sesuai registri penelitian. Kolom November menyediakan hasil pengulangan 16 November 2026 untuk diperiksa hingga tingkat kueri atau kondisi uji.

| Tahap | Hasil utama Oktober | Pengulangan November |
|---|---|---|
| E0 | [e0 summary](tables/01_e0_summary.csv) · [e0 representation probe](tables/02_e0_representation_probe.csv) · [e0 per recording](tables/03_e0_per_recording.csv) | [summary](reproductions/E0_20261116_131535/tables/summary.csv) |
| E1 | [e1 clean retrieval summary](tables/10_e1_clean_retrieval_summary.csv) | [R0 per query](reproductions/E1_R0_cache_20261116T133240_739212Z/tables/per_query.csv) · [R1 per query](reproductions/E1_R1_cache_20261116T133242_268036Z/tables/per_query.csv) · [R2 per query](reproductions/E1_R2_cache_20261116T133243_173920Z/tables/per_query.csv) · [R3 per query](reproductions/E1_R3_cache_20261116T133243_681397Z/tables/per_query.csv) |
| E2 | [e2 snr robustness](tables/11_e2_snr_robustness.csv) · [statistics e2 retention](tables/18_statistics_e2_retention.csv) | [e2 snr robustness](reproductions/E2_controlled_20261116T132030_189809Z/tables/e2_snr_robustness.csv) |
| E3 | [e3 frozen thresholds](tables/12_e3_frozen_thresholds.csv) · [e3 threshold transfer](tables/13_e3_threshold_transfer.csv) · [statistics e3 threshold transfer](tables/19_statistics_e3_threshold_transfer.csv) | [frozen thresholds](reproductions/E3_open_set_20261116T134710_006216Z/tables/frozen_thresholds.csv) · [threshold transfer](reproductions/E3_open_set_20261116T134710_006216Z/tables/threshold_transfer.csv) |
| E4 | [e4 domain shift](tables/14_e4_domain_shift.csv) · [h3 habitat profile stability](tables/24_h3_habitat_profile_stability.csv) · [h3 retention by habitat repeat](tables/25_h3_retention_by_habitat_repeat.csv) | [e4 domain shift table](reproductions/E4_5sites_20261116T131634_985229Z/tables/e4_domain_shift_table.csv) |
| E5 | [e5 failure mode summary](tables/15_e5_failure_mode_summary.csv) · [e5 selected case manifest](tables/16_e5_selected_case_manifest.csv) · [e5 unknown open set diagnostics](tables/17_e5_unknown_open_set_diagnostics.csv) | [failure mode summary](reproductions/E5_diagnostics_20261116T163735_918996Z/tables/failure_mode_summary.csv) · [selected case manifest](reproductions/E5_diagnostics_20261116T163735_918996Z/tables/selected_case_manifest.csv) |

[Manifes target](../data/manifests/dataset_split.csv) · [Inventaris derau](../data/manifests/itera_noise_manifest.csv) · [Statistik berpasangan](tables/22_statistics_paired_bootstrap.csv) · [Lembar hasil audit pendengaran](../Rencana-eksperimen-bimbingan/audit-pendengaran-E5/E5_HASIL_ULASAN_2026-10-30.csv)
