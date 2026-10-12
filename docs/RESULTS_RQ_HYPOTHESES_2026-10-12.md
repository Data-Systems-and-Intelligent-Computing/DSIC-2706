# Hasil Terverifikasi E0–E5, RQ, dan Hipotesis

Dokumen ini adalah ringkasan hasil dari artefak eksperimen aktif yang tervalidasi di repository lokal. Seluruh nilai di bawah berasal dari data asli pada `data/`, bukan data sintetis. Run lama yang terdampak imputasi XC42472 berada di arsip dan tidak dipakai sebagai bukti.

## Dataset dan status provenance

Partisi aktif terdiri dari 673 Gallery, 311 Query bersih, dan 232 Calibration. E3 memakai 233 unknown calibration serta 310 unknown test. Tabel status berikut merujuk artefak konkret dan tidak mengubahnya.

| experiment | status | artifact | limitation |
| --- | --- | --- | --- |
| E0 | VALID | results/reproductions/E0_20261011_202557 | Descriptive audit, not a retrieval comparison. |
| E1 R0 | VALID | results/reproductions/E1_R0_20261011_175321 | One clean evaluation only. |
| E1 R1-R3 | VALID | results/reproductions/E1_R1_cache_20261012T021032_566409Z; E1_R2_cache_20261012T021034_128124Z; E1_R3_cache_20261012T021035_119528Z | Materialized from valid clean caches; not represented as historical runs. |
| E2 | VALID | results/reproductions/E2_controlled_20261012T021600_897497Z | Controlled additive mixing only. |
| E3 | VALID | results/reproductions/E3_open_set_20261012T022548_802536Z | Unknown controls are not naturally recorded bird soundscapes. |
| E4/H3 | VALID | results/reproductions/E4_5sites_20261011T213404_350219Z; results/reproductions/E4_audit_20261012T021801_989259Z; results/reproductions/H3_habitat_profile_stability_20261012T141344_312163Z | H3 is derived read-only from E4 raw; raw lacks ranking identities, class margins, and noisy-audio feature fields. |
| E5 | VALID_WITH_LIMITATION | results/reproductions/E5_diagnostics_20261012T091512_868500Z | E4 unavailable fields are marked unavailable; no identities or margins are invented. |
| Legacy BirdCLEF results | SUPERSEDED | results/archive/birdclef_2026 | Retained only as historical archive; not used in current matrix. |

## E0 — audit preprocessing

E0 adalah audit 100 rekaman aktif yang dipilih deterministik. E0 bukan retrieval dan bukan R0.

| metric | value |
| --- | --- |
| audit_rows | 100.0000 |
| unique_species | 20.0000 |
| native_duration_min_seconds | 4.4775 |
| native_duration_median_seconds | 31.8648 |
| native_duration_max_seconds | 199.1526 |
| extension_container_mismatches | 6.0000 |
| soundfile_decode_errors | 0.0000 |
| preprocess_length_failures | 0.0000 |
| preprocess_nonfinite_failures | 0.0000 |
| target_rms | 0.0500 |

Temuan: seluruh 100 audio yang diperiksa menghasilkan 160.000 sampel terhingga setelah preprocessing pada 32 kHz dan durasi 5 detik. Ada 6 ketidakcocokan ekstensi/container dalam sampel, tetapi tidak ada kegagalan decoder. Lihat `results/reproductions/E0_20261011_202557/tables/per_recording.csv` untuk semua baris audit.

## EDA — kondisi data fisik

Inventaris EDA mencatat 3396 audio fisik, 1216 target aktif, 1799 audio noise ITERA, dan 543 item unknown/open-set. Tidak ada error decode soundfile; terdapat 101 ketidakcocokan ekstensi/container dan 109 audio fisik belum dirujuk oleh manifes yang diaudit. Ini adalah temuan audit, bukan alasan otomatis untuk menghapus file.

Audit manifes menyebut 108 audio tidak dirujuk karena turut memeriksa `indonesia_train.csv` dan log unduhan historis; EDA menghitung 109 terhadap tiga manifes aktif. Perbedaan satu berkas tersebut berasal dari cakupan rujukan yang berbeda, bukan perubahan jumlah audio fisik.

Notebook EDA membangun ulang distribusi spesies, durasi, sampling rate, lokasi noise, waveform, dan mel-spektrogram langsung dari audio fisik.

## E1 — clean retrieval

R0 adalah **baseline MFCC**, bukan preprocessing. Preprocessing menyiapkan audio; R0 mengubah audio siap tersebut menjadi vektor MFCC untuk retrieval.

| representation | mean_top1 | MRR | mAP@10 | Recall@10 | Precision@10 |
| --- | --- | --- | --- | --- | --- |
| R0 | 0.1833 | 0.3109 | 0.0694 | 0.0363 | 0.1312 |
| R1 | 0.3762 | 0.5070 | 0.1763 | 0.0842 | 0.2585 |
| R2 | 0.8167 | 0.8652 | 0.6367 | 0.2331 | 0.6939 |
| R3 | 0.0643 | 0.1639 | 0.0211 | 0.0141 | 0.0569 |

R2 mempunyai performa bersih tertinggi. R1–R3 dimaterialisasi dari cache clean yang divalidasi dengan hash manifes, urutan ID, dimensi, nilai hingga, dan versi kontrol R3; artefaknya tidak diklaim sebagai run historis.

## E2 — penurunan terkontrol oleh noise ITERA

E2 menggunakan pencampuran noise lapangan ITERA fisik pada SNR +20, +10, 0, dan −5 dB. Terdapat 20 raw CSV, masing-masing berisi 311 query yang sejajar dengan manifes dan menyimpan audit noise/seed/SNR aktual.

### mAP@10

| representation | Clean | SNR_20dB | SNR_10dB | SNR_0dB | SNR_-5dB |
| --- | --- | --- | --- | --- | --- |
| R0 | 0.069393 | 0.076988 | 0.060414 | 0.032334 | 0.023210 |
| R1 | 0.176268 | 0.184900 | 0.172136 | 0.118796 | 0.086306 |
| R2 | 0.636709 | 0.637767 | 0.621312 | 0.554874 | 0.483160 |
| R3 | 0.021141 | 0.021141 | 0.021141 | 0.021141 | 0.021141 |

### Recall@10

| representation | Clean | SNR_20dB | SNR_10dB | SNR_0dB | SNR_-5dB |
| --- | --- | --- | --- | --- | --- |
| R0 | 0.036321 | 0.039478 | 0.032554 | 0.023583 | 0.019337 |
| R1 | 0.084175 | 0.082629 | 0.077801 | 0.053061 | 0.039470 |
| R2 | 0.233109 | 0.230940 | 0.227686 | 0.206628 | 0.182992 |
| R3 | 0.014092 | 0.014092 | 0.014092 | 0.014092 | 0.014092 |

Pada −5 dB, retensi mAP@10 adalah R0 33,45%, R1 48,96%, R2 75,88%, dan R3 100%. Retensi R3 tidak diinterpretasikan sebagai ketahanan audio karena R3 merupakan kontrol ID-deterministik.

## E3 — threshold open-set yang dibekukan

Threshold ditentukan hanya dari calibration bersih melalui ROC Youden J, lalu dibekukan sebelum evaluasi query dan unknown test.

| representation | frozen_tau | calibration_auroc | calibration_youden_j | calibration_precision | calibration_recall | calibration_fpr |
| --- | --- | --- | --- | --- | --- | --- |
| R0 | 0.995752 | 0.533225 | 0.099545 | 0.671642 | 0.193966 | 0.094421 |
| R1 | 0.897416 | 0.709801 | 0.372299 | 0.665385 | 0.745690 | 0.373391 |
| R2 | 0.702785 | 0.759953 | 0.418843 | 0.774011 | 0.590517 | 0.171674 |
| R3 | 0.488838 | 0.545194 | 0.087409 | 0.566667 | 0.366379 | 0.278970 |

### Perubahan titik operasi: Clean ke −5 dB

| representation | condition | Recall_at_tau | False_Positive_Rate | AUROC | AUPRC |
| --- | --- | --- | --- | --- | --- |
| R0 | Clean | 0.186495 | 0.138710 | 0.546380 | 0.555039 |
| R0 | SNR_-5dB | 0.009646 | 0.012903 | 0.498009 | 0.500115 |
| R1 | Clean | 0.836013 | 0.477419 | 0.745877 | 0.717167 |
| R1 | SNR_-5dB | 0.440514 | 0.251613 | 0.649507 | 0.631850 |
| R2 | Clean | 0.604502 | 0.222581 | 0.758936 | 0.790130 |
| R2 | SNR_-5dB | 0.254019 | 0.129032 | 0.599409 | 0.617399 |
| R3 | Clean | 0.363344 | 0.274194 | 0.547163 | 0.561990 |
| R3 | SNR_-5dB | 0.363344 | 0.274194 | 0.547163 | 0.561990 |

Untuk R0–R2, recall known-set di threshold beku turun pada −5 dB. False-positive rate unknown justru turun pada kondisi ini; H4 didukung melalui penurunan recall, bukan lonjakan false accept.

## E4 — sensitivitas profil noise lintas habitat

E4 tervalidasi sebagai 320 snapshot kondisi additive mixture. E4 memakai rekaman noise asli dari lima habitat/lokasi ITERA yang dicampur ke query focal; E4 **bukan** rekaman burung yang dibuat langsung dalam real soundscape.

### mAP@10 pada −5 dB menurut habitat/lokasi

| representation | Embung_F | Gedung_F | Kebun_Raya | Masjid_At_Tanwir | Sekitar_GKU_1 |
| --- | --- | --- | --- | --- | --- |
| R0 | 0.028389 | 0.019348 | 0.022228 | 0.025731 | 0.017891 |
| R1 | 0.087315 | 0.090465 | 0.048673 | 0.090600 | 0.083264 |
| R2 | 0.503990 | 0.454128 | 0.444612 | 0.502504 | 0.454732 |
| R3 | 0.021141 | 0.021141 | 0.021141 | 0.021141 | 0.021141 |

E4 raw menyimpan `top1_match` dan `max_score`. Ia tidak menyimpan identitas Top-1, skor kelas benar, skor pesaing, margin kelas, atau fitur akustik dari audio noisy.

### H3 — stabilitas retensi lintas profil lokasi

H3 membandingkan ayunan retensi `mAP@10` lintas lima lokasi: `maksimum retensi − minimum retensi`, dirata-ratakan atas empat segmen noise acak per lokasi. Hasil statistik berasal dari CSV mentah E4, memakai 311 query yang sama dan bootstrap berpasangan 10.000 kali. Tidak ada audio yang dicampur ulang.

| ringkasan 4 SNR | Ayunan R1/PANNs | Ayunan R2/BirdNET | R1 − R2 | CI 95% | Kesimpulan |
| --- | ---: | ---: | ---: | --- | --- |
| mAP@10 relative retention | 0.240111 | 0.048607 | 0.191504 | [0.152203, 0.241969] | H3 didukung |

Pada −5 dB, ayunan R1 = 0.258674 dan R2 = 0.097108; selisih 0.161566, CI 95% [0.105339, 0.226667]. Detail tersedia pada `results/tables/24_h3_habitat_profile_stability.csv` dan `results/figures/15_h3_habitat_retention_stability.png`.

Uji H3 ini ditambahkan setelah E4 selesai dan bersifat eksploratif. Ia menguji kestabilan retensi menurut lokasi noise. Penjelasan bahwa perbedaan berasal dari distorsi frekuensi tinggi/rendah belum diuji secara langsung terhadap fitur spektral setiap segmen noise.

## E5 — taksonomi kegagalan retrieval

E5 memakai threshold E3 yang beku. E2 menyediakan semua field ranking dan direkonstruksi secara deterministik untuk centroid, bandwidth, dan RMS. Pada E4, field yang tidak pernah tersedia tetap ditandai tidak tersedia dan tidak direka ulang.

| source_experiment | representation | failure_mode | n_queries |
| --- | --- | --- | --- |
| E2 | R0 | Accepted correct | 63 |
| E2 | R0 | Open-set false rejection | 147 |
| E2 | R0 | Top-1 confusion above threshold | 161 |
| E2 | R0 | Total retrieval collapse | 1184 |
| E2 | R1 | Accepted correct | 389 |
| E2 | R1 | Open-set false rejection | 120 |
| E2 | R1 | Top-1 confusion above threshold | 697 |
| E2 | R1 | Total retrieval collapse | 349 |
| E2 | R2 | Accepted correct | 626 |
| E2 | R2 | Open-set false rejection | 574 |
| E2 | R2 | Top-1 confusion above threshold | 67 |
| E2 | R2 | Total retrieval collapse | 288 |
| E2 | R3 | Accepted correct | 45 |
| E2 | R3 | Open-set false rejection | 55 |
| E2 | R3 | Top-1 confusion above threshold | 520 |
| E2 | R3 | Total retrieval collapse | 935 |
| E4 | R0 | Accepted correct | 847 |
| E4 | R0 | Open-set false rejection | 2302 |
| E4 | R0 | Top-1 confusion above threshold | 2365 |
| E4 | R0 | Total retrieval collapse | 19677 |
| E4 | R1 | Accepted correct | 5461 |
| E4 | R1 | Open-set false rejection | 2002 |
| E4 | R1 | Top-1 confusion above threshold | 11203 |
| E4 | R1 | Total retrieval collapse | 6525 |
| E4 | R2 | Accepted correct | 9365 |
| E4 | R2 | Open-set false rejection | 9206 |
| E4 | R2 | Top-1 confusion above threshold | 817 |
| E4 | R2 | Total retrieval collapse | 5803 |
| E4 | R3 | Accepted correct | 729 |
| E4 | R3 | Open-set false rejection | 891 |
| E4 | R3 | Top-1 confusion above threshold | 8424 |
| E4 | R3 | Total retrieval collapse | 15147 |

E5 menyediakan 120 contoh kegagalan E2 yang dipilih secara terstratifikasi dengan seed tetap, grafik moda kegagalan, margin terhadap threshold, dan fitur spektral. Artefak lengkap: `results/reproductions/E5_diagnostics_20261012T091512_868500Z`.

## Jawaban RQ dan hipotesis

Scope aktif merujuk `docs/research/rq.md`, `docs/research/hypotheses.md`, dan `docs/research/scope-reframe-2026-10-12.md`. E4 dibingkai sebagai sensitivitas profil noise lapangan dalam additive mixture, menjawab Sub-RQ3, dan menyediakan data mentah untuk uji H3. E5 menjawab Sub-RQ4 sebagai diagnostik kegagalan.

| item | experiment | metric | result | conclusion | limitation |
| --- | --- | --- | --- | --- | --- |
| RQ utama | E1/E2/E4 | mAP@10 | R2 has the highest observed mAP@10 in E2 at every tested SNR and in the validated E4 mixture conditions. | Answered within additive ITERA-noise mixtures | Does not establish performance on naturally recorded bird soundscapes. |
| Sub-RQ 1 | E2 | mAP@10, Recall@10, Precision@10 | All representations have per-query and aggregate values at Clean/+20/+10/0/-5 dB. | Answered | One deterministic physical-noise segment per query/SNR, not repeated stochastic draws. |
| Sub-RQ 2 | E3 | frozen-threshold recall and false-accept rate | Frozen clean thresholds change their acceptance behavior at -5 dB; see H4 rows. | Answered | Unknown test controls are synthetic mixes of real unknown/noise audio, not a field soundscape bird test. |
| Sub-RQ 3 | E4 | habitat/location-conditioned mixture mAP@10 | E4 compares five verified ITERA noise-location profiles under the same additive-mixture protocol. | Answered within the narrowed scope | Does not measure bird recordings made in real soundscapes. |
| Sub-RQ 4 | E5 | failure mode, margin, and spectral diagnostics | E5 reports false rejection, confusion, collapse, and available acoustic diagnostics. | Answered as controlled diagnostics | E4 fields absent in raw outputs remain unavailable. |
| H1 | E2 | paired bootstrap of -5 dB / Clean mAP@10 | R1 vs R0 p=0.0112989; R2 vs R0 p=9.999e-05. | Supported | R3 excluded: it is an ID-deterministic control, not an audio representation. |
| H2 | E2 | paired bootstrap of R2-R1 -5 dB retention | difference=0.269212, 95% CI [0.160783, 0.364992], p=9.999e-05. | Supported | No causal statement about the model architecture follows from this comparison. |
| H3 | E4 raw + H3 analysis | mAP@10 retention swing across five habitat noise profiles | R1 swing 0.240111; R2 swing 0.048607; Δ=0.191504, CI 95% [0.152203, 0.241969]. | Supported for retention stability | Exploratory analysis; high/low-frequency mechanism and in-situ bird soundscapes were not tested. |
| H4 | E3 | paired change in known accept recall and unknown false-accept rate | Known acceptance recall declines significantly from Clean to -5 dB for R0, R1, and R2; false-accept rate falls rather than rises. | Supported for R0-R2 through recall degradation; R3 is unchanged by design. | Threshold is optimized for clean calibration with Youden J; it is not recalibrated at test SNR. |
| H5 | E1/E2 Clean | paired clean AP@10 vs R3 | All primary comparisons significant=True with positive effect=True. | Supported | R3 is a deterministic random-ID control and is not evidence of acoustic noise robustness. |

## Statistik inferensial

Seluruh perbandingan memakai paired bootstrap 10.000 iterasi, seed 20261012, dengan unit resampling query berpasangan. Nilai `p_value_bootstrap` adalah estimasi empiris dari bootstrap sesuai arah hipotesis yang tercatat di kolom `alternative`.

| test_id | n_paired | effect_mean_difference | retention_a | retention_b | ci_95_low | ci_95_high | p_value_bootstrap | statistical_result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| H5_R0_clean_AP10_vs_R3 | 311 | 0.048252 |  |  | 0.036018 | 0.060567 | 0.000100 | significant |
| H5_R1_clean_AP10_vs_R3 | 311 | 0.155127 |  |  | 0.130114 | 0.181303 | 0.000100 | significant |
| H5_R2_clean_AP10_vs_R3 | 311 | 0.615568 |  |  | 0.577635 | 0.653400 | 0.000100 | significant |
| H1_R1_retention_vs_R0_at_minus5 | 311 | 0.155156 | 0.489628 | 0.334473 | 0.022600 | 0.280543 | 0.011299 | significant |
| H1_R2_retention_vs_R0_at_minus5 | 311 | 0.424368 | 0.758840 | 0.334473 | 0.307567 | 0.517913 | 0.000100 | significant |
| H2_R2_retention_vs_R1_at_minus5 | 311 | 0.269212 | 0.758840 | 0.489628 | 0.160783 | 0.364992 | 0.000100 | significant |
| H4_R0_accept_recall_minus5_vs_clean | 311 | -0.176849 |  |  | -0.221865 | -0.131833 | 0.000100 | significant |
| H4_R0_false_accept_rate_minus5_vs_clean | 310 | -0.125806 |  |  | -0.167742 | -0.087097 | 1.000000 | not_significant |
| H4_R1_accept_recall_minus5_vs_clean | 311 | -0.395498 |  |  | -0.456592 | -0.331190 | 0.000100 | significant |
| H4_R1_false_accept_rate_minus5_vs_clean | 310 | -0.225806 |  |  | -0.287097 | -0.164516 | 1.000000 | not_significant |
| H4_R2_accept_recall_minus5_vs_clean | 311 | -0.350482 |  |  | -0.408360 | -0.292605 | 0.000100 | significant |
| H4_R2_false_accept_rate_minus5_vs_clean | 310 | -0.093548 |  |  | -0.148387 | -0.038710 | 0.999400 | not_significant |
| H4_R3_accept_recall_minus5_vs_clean | 311 | 0.000000 |  |  | 0.000000 | 0.000000 | 1.000000 | not_significant |
| H4_R3_false_accept_rate_minus5_vs_clean | 310 | 0.000000 |  |  | 0.000000 | 0.000000 | 1.000000 | not_significant |

## Kesimpulan yang aman saat ini

- R2/BirdNET memberi retrieval terbaik pada E1 dan seluruh level SNR E2 yang diuji.
- H1, H2, H3, H4, dan H5 didukung dalam desain additive ITERA-noise yang divalidasi.
- H3 didukung sebagai stabilitas retensi lintas profil noise lokasi: R2/BirdNET berayun lebih sempit daripada R1/PANNs pada seluruh SNR yang diuji. Sub-RQ3 dijawab oleh E4 dan Sub-RQ4 oleh diagnostik E5.
- Kesimpulan E4 terbatas pada perbedaan profil noise lapangan yang dicampur secara aditif. Ia tidak membuktikan efek jarak, propagasi, absorpsi, atau reverberasi.

## Artefak utama

- E2: `results/reproductions/E2_controlled_20261012T021600_897497Z`
- E3: `results/reproductions/E3_open_set_20261012T022548_802536Z`
- E4 valid, audit pendamping, dan analisis H3 read-only: `results/reproductions/E4_5sites_20261011T213404_350219Z`, `results/reproductions/E4_audit_20261012T021801_989259Z`, serta `results/reproductions/H3_habitat_profile_stability_20261012T141344_312163Z`
- E5: `results/reproductions/E5_diagnostics_20261012T091512_868500Z`
- Matriks/provenance/statistik: `results/reproductions/STATISTICS_RQ_MATRIX_20261012T092924_809804Z`
