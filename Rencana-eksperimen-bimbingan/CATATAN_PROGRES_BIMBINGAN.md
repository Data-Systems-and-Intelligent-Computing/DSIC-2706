# Catatan Progres Bimbingan — DSIC-2706

**Judul kerja:** *Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval under Controlled ITERA Field-Noise Mixtures in Indonesian Avifauna*  
**Pembaruan terakhir:** 12 Oktober 2026  
**Tujuan dokumen:** catatan pelaksanaan yang dapat dicek langsung oleh mahasiswa dan pembimbing melalui file lokal.

## 1. Cara memeriksa bukti

| Apa yang ingin diperiksa | File atau folder langsung |
|---|---|
| Status E0–E5 | [experiments/experiment_registry.csv](../experiments/experiment_registry.csv) |
| Jawaban RQ dan H1–H5 | [docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md](../docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md) |
| Angka CSV yang siap dipakai laporan | [results/tables/](../results/tables/) |
| Gambar kurva/spektrogram | [results/figures/](../results/figures/) |
| Artefak sumber per run | [results/reproductions/](../results/reproductions/) |
| Notebook yang dapat dibaca dan dijalankan per eksperimen | [notebooks/](../notebooks/) |
| Kode pipeline | [src/](../src/) |
| Konfigurasi | [configs/](../configs/) |
| Data dan manifes | [data/](../data/) |
| Uji integritas | [run_tests.py](../run_tests.py) dan [tests/](../tests/) |

Setiap bahan laporan di `results/figures/` dan `results/tables/` memiliki sumber serta checksum pada [report_materials_manifest.json](../results/report_materials_manifest.json). Run di `results/reproductions/` tidak ditimpa oleh penataan dokumentasi ini.

## 2. Fondasi data dan audit

### Data aktif

- 20 spesies target Indonesia.
- 673 Gallery, 311 Query bersih, dan 232 Calibration dari [dataset_split.csv](../data/manifests/dataset_split.csv).
- 233 unknown calibration dan 310 unknown test dari [unknown_open_set_manifest.csv](../data/manifests/unknown_open_set_manifest.csv).
- 1.799 rekaman noise AudioMoth ITERA dari [itera_noise_manifest.csv](../data/manifests/itera_noise_manifest.csv).

### E0 dan EDA

E0 mengaudit 100 rekaman deterministik. Semua menghasilkan 160.000 sampel terhingga sesudah mono 32 kHz, jendela 5 detik, dan RMS 0,05. Ada 6 mismatch ekstensi/container, tanpa error decoder.

EDA menginventaris 3.396 audio fisik: 1.216 target aktif, 1.799 noise ITERA, dan 543 unknown. Temuan penting ialah 101 mismatch ekstensi/container serta 109 audio fisik yang belum dirujuk manifest audit. Temuan tersebut dicatat, tidak digunakan untuk menghapus data.

**Bukti langsung:** [notebook preprocessing](../notebooks/01_Preprocessing.ipynb), [notebook E0](../notebooks/02_E0_Preprocessing_Audit.ipynb), [notebook EDA](../notebooks/03_EDA_Physical_Audio.ipynb), [tabel E0](../results/tables/01_e0_summary.csv), [inventaris EDA](../results/tables/07_eda_physical_audio_inventory.csv), dan [spektrogram EDA](../results/figures/03_eda_bird_waveform_spectrogram_examples.png).

## 3. E1 — clean retrieval

Empat representasi dibandingkan pada query clean yang sama: R0 MFCC, R1 PANNs CNN14, R2 BirdNET, dan R3 kontrol ID-deterministik.

| Representasi | Top-1 | MRR | mAP@10 | Recall@10 |
|---|---:|---:|---:|---:|
| R0 | 0,1833 | 0,3109 | 0,0694 | 0,0363 |
| R1 | 0,3762 | 0,5070 | 0,1763 | 0,0842 |
| R2 | 0,8167 | 0,8652 | 0,6367 | 0,2331 |
| R3 | 0,0643 | 0,1639 | 0,0211 | 0,0141 |

R2 memberikan retrieval clean tertinggi. R1–R3 dibuat sebagai konsolidasi dari cache bersih yang lolos pemeriksaan hash manifes, urutan Gallery/Query, dimensi embedding, dan identitas kontrol R3; konsolidasi tidak diklaim sebagai run historis.

**Bukti langsung:** [notebook E1](../notebooks/04_E1_Clean_Retrieval.ipynb), [tabel E1](../results/tables/10_e1_clean_retrieval_summary.csv), [run R0](../results/reproductions/E1_R0_20261011_175321/), [run R1](../results/reproductions/E1_R1_cache_20261012T021032_566409Z/), [run R2](../results/reproductions/E1_R2_cache_20261012T021034_128124Z/), [run R3](../results/reproductions/E1_R3_cache_20261012T021035_119528Z/).

## 4. E2 — controlled ITERA noise

E2 mencampur query dengan noise fisik ITERA pada Clean, +20, +10, 0, dan −5 dB. Gallery dan identitas query tetap sama, sehingga perbandingan per-query bersifat berpasangan.

| Representasi | mAP@10 Clean | mAP@10 −5 dB | Retensi −5 dB |
|---|---:|---:|---:|
| R0 | 0,069393 | 0,023210 | 33,45% |
| R1 | 0,176268 | 0,086306 | 48,96% |
| R2 | 0,636709 | 0,483160 | 75,88% |
| R3 | 0,021141 | 0,021141 | 100,00%* |

\*Kontrol R3 tidak dipakai sebagai bukti ketahanan terhadap noise.

**Bukti langsung:** [notebook E2](../notebooks/05_E2_Controlled_Noise.ipynb), [kode E2](../scripts/run_e2_controlled_noise.py), [tabel E2](../results/tables/11_e2_snr_robustness.csv), [kurva E2](../results/figures/08_e2_snr_robustness_map10.png), dan [raw E2](../results/reproductions/E2_controlled_20261012T021600_897497Z/raw/).

## 5. E3 — open-set threshold

E3 menentukan τ* pada calibration terpisah menggunakan Youden J, lalu membekukannya sebelum pengujian target dan unknown test.

| Representasi | τ* | AUROC kalibrasi | Recall kalibrasi | FPR kalibrasi |
|---|---:|---:|---:|---:|
| R0 | 0,995752 | 0,533225 | 0,193966 | 0,094421 |
| R1 | 0,897416 | 0,709801 | 0,745690 | 0,373391 |
| R2 | 0,702785 | 0,759953 | 0,590517 | 0,171674 |
| R3 | 0,488838 | 0,545194 | 0,366379 | 0,278970 |

Pada −5 dB, recall known-set di τ* turun untuk R0–R2. Untuk R2, nilai turun dari 0,604502 pada Clean menjadi 0,254019 pada −5 dB. FPR unknown turun dalam hasil ini; klaim H4 didasarkan pada degradasi recall known-set.

**Bukti langsung:** [notebook E3](../notebooks/06_E3_Open_Set_Threshold.ipynb), [kode E3](../scripts/run_e3_open_set.py), [tabel threshold](../results/tables/12_e3_frozen_thresholds.csv), [tabel transfer](../results/tables/13_e3_threshold_transfer.csv), [kurva E3](../results/figures/09_e3_threshold_transfer_recall.png), dan [raw E3](../results/reproductions/E3_open_set_20261012T022548_802536Z/raw/).

## 6. E4 — sensitivitas profil noise lokasi

E4 membandingkan lima lokasi noise ITERA pada kondisi additive mixture. Pada −5 dB, R2 memiliki mAP@10 antara 0,444612 dan 0,503990 menurut lokasi; R1 antara 0,048673 dan 0,090600.

**Bukti langsung:** [notebook E4](../notebooks/07_E4_Habitat_Noise_Sensitivity.ipynb), [tabel E4](../results/tables/14_e4_domain_shift.csv), [gambar E4](../results/figures/10_e4_noise_profile_sensitivity.png), [run E4](../results/reproductions/E4_5sites_20261011T213404_350219Z/), dan [audit E4](../results/reproductions/E4_audit_20261012T021801_989259Z/).

**Framing aktif:** E4 adalah uji sensitivitas terhadap profil noise lokasi nyata ITERA dalam additive mixture. H3 diuji sebagai stabilitas retensi lintas lima profil: ayunan R1 = 0.240111, R2 = 0.048607, Δ = 0.191504, CI 95% [0.152203, 0.241969]. Karena bank ITERA bebas spesies target, anotasi target-species tidak diperlukan.

Uji H3 ditambahkan setelah E4 selesai, sehingga status signifikansinya bersifat eksploratif. Klaim mekanisme distorsi frekuensi tinggi/rendah belum diuji langsung terhadap fitur spektral noise per segmen.

## 7. E5 dan statistik

E5 mengelompokkan accepted correct, open-set false rejection, top-1 confusion above threshold, dan total retrieval collapse. Untuk E2, fitur spektral dan margin tersedia melalui rekonstruksi deterministik. Untuk E4, field yang tidak tersedia ditandai unavailable tanpa diisi.

**Bukti langsung:** [notebook E5](../notebooks/08_E5_Failure_Diagnostics.ipynb), [tabel failure mode](../results/tables/15_e5_failure_mode_summary.csv), [kasus terpilih](../results/tables/16_e5_selected_case_manifest.csv), [gambar modus](../results/figures/11_e5_failure_modes_by_representation.png), [gambar margin](../results/figures/12_e5_margin_distribution_by_failure_type.png), [gambar spektral](../results/figures/13_e5_spectral_features_by_failure_type.png).

Bootstrap berpasangan memakai 10.000 iterasi dan seed 20261012. H1–H5 didukung di bawah desain additive-noise yang tervalidasi. H3 dihitung read-only dari raw E4 dan menunjukkan ayunan retensi R2 lebih sempit daripada R1.

**Bukti langsung:** [paired bootstrap](../results/tables/22_statistics_paired_bootstrap.csv), [matriks RQ/H](../results/tables/27_rq_hypothesis_matrix_current.csv), [run statistik](../results/reproductions/STATISTICS_RQ_MATRIX_20261012T092924_809804Z/).

## 8. Status jawaban pertanyaan penelitian

| Item | Status | Batasan |
|---|---|---|
| RQ utama | Terjawab dalam controlled additive ITERA-noise mixture: R2 tertinggi pada E2 dan E4 | Bukan klaim real-soundscape burung in-situ |
| Sub-RQ1 | Terjawab oleh E2: perubahan retrieval lintas SNR | Satu pairing noise deterministik per query/SNR |
| Sub-RQ2 | Terjawab oleh E3: frozen threshold pada target dan unknown | Unknown bukan korpus focal-bird field soundscape |
| Sub-RQ3 | Terjawab oleh E4 sebagai sensitivitas profil noise lima lokasi | Tidak mencakup real-soundscape bird recording |
| Sub-RQ4 | Terjawab oleh E5 sebagai diagnostik kegagalan | Bergantung pada field yang tersedia dalam raw experiment |
| H3 | Didukung: R2 memiliki ayunan retensi lintas lokasi lebih sempit daripada R1 | Additive mixture, bukan bird recording in-situ |
| H1 | Didukung | R3 dikecualikan sebagai kontrol ID |
| H2 | Didukung | Tidak membuktikan sebab arsitektur model |
| H4 | Didukung melalui recall degradation | FPR tidak meningkat pada data ini |
| H5 | Didukung | R3 bukan representasi audio |

## 9. Pemeriksaan terakhir

`run_tests.py` menjalankan 25 pemeriksaan integritas/metode dan lulus pada pembaruan ini. Pemeriksaan ini tidak menghapus audio, cache, checkpoint, manifes, atau run eksperimen.
