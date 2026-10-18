# Catatan Progres Bimbingan — DSIC-2706

**Judul kerja:** *Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval under Controlled ITERA Field-Noise Mixtures in Indonesian Avifauna*  
**Pembaruan terakhir:** 18 Oktober 2026 — tindak lanjut pembimbing dan panduan audit

**Tujuan dokumen:** catatan pelaksanaan yang dapat dicek langsung oleh mahasiswa dan pembimbing melalui file lokal.

## 1. Cara memeriksa bukti

| Apa yang ingin diperiksa | File atau folder langsung |
|---|---|
| Status E0–E5 | [experiments/experiment_registry.csv](../experiments/experiment_registry.csv) |
| Jawaban RQ dan H1–H5 terkini | [Matriks revisi](../results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv) dan [catatan revisi](../docs/REVISION_SUPERVISOR_2026-10-15.md) |
| Angka CSV yang siap dipakai laporan | [results/tables/](../results/tables/) |
| Gambar kurva/spektrogram | [results/figures/](../results/figures/) |
| Artefak sumber per run | [results/reproductions/](../results/reproductions/) |
| Notebook yang dapat dibaca dan dijalankan per eksperimen | [notebooks/](../notebooks/) |
| Kode pipeline | [src/](../src/) |
| Konfigurasi | [configs/](../configs/) |
| Data dan manifes | [data/](../data/) |
| Uji integritas | [run_tests.py](../run_tests.py) dan [tests/](../tests/) |

Sebanyak 41 bahan laporan 12 Oktober tercatat pada [report_materials_manifest.json](../results/report_materials_manifest.json); artefak revisi dan tabel 28 mempunyai metadata provenance tersendiri. Run di `results/reproductions/` tidak ditimpa oleh penataan dokumentasi ini.

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

Pada −5 dB, recall known-set di τ* turun untuk R0–R2. Untuk R2, nilai turun dari 0,604502 pada Clean menjadi 0,254019 pada −5 dB. FPR unknown turun dalam hasil ini. Penurunan recall konsisten dengan salah satu klausul H4 asli; interpretasi hasil reformulasi setelah hasil tersedia diberi label eksploratif.

**Bukti langsung:** [notebook E3](../notebooks/06_E3_Open_Set_Threshold.ipynb), [kode E3](../scripts/run_e3_open_set.py), [tabel threshold](../results/tables/12_e3_frozen_thresholds.csv), [tabel transfer](../results/tables/13_e3_threshold_transfer.csv), [kurva E3](../results/figures/09_e3_threshold_transfer_recall.png), dan [raw E3](../results/reproductions/E3_open_set_20261012T022548_802536Z/raw/).

## 6. E4 — sensitivitas profil noise lokasi

E4 membandingkan lima lokasi noise ITERA pada kondisi additive mixture. Pada −5 dB, R2 memiliki mAP@10 antara 0,444612 dan 0,503990 menurut lokasi; R1 antara 0,048673 dan 0,090600.

**Bukti langsung:** [notebook E4](../notebooks/07_E4_Habitat_Noise_Sensitivity.ipynb), [tabel E4](../results/tables/14_e4_domain_shift.csv), [gambar E4](../results/figures/10_e4_noise_profile_sensitivity.png), [run E4](../results/reproductions/E4_5sites_20261011T213404_350219Z/), dan [audit E4](../results/reproductions/E4_audit_20261012T021801_989259Z/).

**Framing aktif:** E4 menguji sensitivitas profil noise lima lokasi melalui additive mixture. Revisi H3 mempertahankan ayunan retensi, tetapi menambahkan ayunan absolut serta sensitivitas tanpa Kebun Raya. Rata-rata ayunan absolut lima lokasi R1 = 0,042324 dan R2 = 0,030949; CI selisih [−0,003993; 0,022140]. Tanpa Kebun Raya pada −5 dB, ayunan relatif R1 = 0,065937 dan R2 = 0,083724; CI [−0,041711; 0,050057]. Kesimpulan bergantung pada metrik, SNR, dan subset.

Uji H3 ditambahkan setelah E4 selesai, sehingga status signifikansinya bersifat eksploratif. Klaim mekanisme distorsi frekuensi tinggi/rendah belum diuji langsung terhadap fitur spektral noise per segmen.

## 7. E5 dan statistik

E5 mengelompokkan accepted correct, open-set false rejection, top-1 confusion above threshold, dan total retrieval collapse. Untuk E2, fitur spektral dan margin tersedia melalui rekonstruksi deterministik. Untuk E4, field yang tidak tersedia ditandai unavailable tanpa diisi.

**Bukti langsung:** [notebook E5](../notebooks/08_E5_Failure_Diagnostics.ipynb), [tabel failure mode](../results/tables/15_e5_failure_mode_summary.csv), [kasus terpilih](../results/tables/16_e5_selected_case_manifest.csv), [gambar modus](../results/figures/11_e5_failure_modes_by_representation.png), [gambar margin](../results/figures/12_e5_margin_distribution_by_failure_type.png), [gambar spektral](../results/figures/13_e5_spectral_features_by_failure_type.png).

Bootstrap berpasangan memakai 10.000 iterasi dan seed 20261012. H1, H2, dan H5 memiliki dukungan pada uji tersimpan. H3/H4 hasil reformulasi adalah eksploratif. H3 asli real-soundscape belum diuji; keunggulan stabilitas R2 tidak berlaku umum lintas ukuran dan subset.

**Bukti langsung:** [paired bootstrap](../results/tables/22_statistics_paired_bootstrap.csv), [matriks RQ/H revisi](../results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv), [run statistik](../results/reproductions/STATISTICS_RQ_MATRIX_20261012T092924_809804Z/).

## 8. Status jawaban pertanyaan penelitian

| Item | Status | Batasan |
|---|---|---|
| RQ utama | Terjawab dalam controlled additive ITERA-noise mixture: R2 tertinggi pada E2 dan E4 | Bukan klaim real-soundscape burung in-situ |
| Sub-RQ1 | Terjawab oleh E2: perubahan retrieval lintas SNR | Satu pairing noise deterministik per query/SNR |
| Sub-RQ2 | Terjawab oleh E3: frozen threshold pada target dan unknown | Unknown bukan korpus focal-bird field soundscape |
| Sub-RQ3 | Terjawab oleh E4 sebagai sensitivitas profil noise lima lokasi | Tidak mencakup real-soundscape bird recording |
| Sub-RQ4 | Terjawab oleh E5 sebagai diagnostik kegagalan | Bergantung pada field yang tersedia dalam raw experiment |
| H3 | Eksploratif; bergantung metrik dan subset lokasi | Rata-rata ayunan absolut: CI mencakup nol; H3 asli real-soundscape belum diuji |
| H1 | Didukung | R3 dikecualikan sebagai kontrol ID |
| H2 | Didukung | Tidak membuktikan sebab arsitektur model |
| H4 | Interpretasi reformulasi eksploratif; recall penerimaan turun | FPR tidak meningkat; threshold tidak diubah |
| H5 | Didukung | R3 bukan representasi audio |

## 9. Pemeriksaan suite saat ini

`run_tests.py` kini menjalankan 36 pemeriksaan integritas/metode (25 sebelumnya + 5 H3 + 2 seleksi E5 + 3 impor ulasan + 1 provenance Git E4) dan seluruhnya lulus pada pemeriksaan ulang 16 Oktober. Pemeriksaan ini tidak menghapus audio, cache, checkpoint, manifes, atau run eksperimen.

## 10. Progres pemeriksaan awal — 15–16 Oktober 2026 (dilanjutkan §11)

Revisi utama telah dipush pada commit [8bf5441](https://github.com/Data-Systems-and-Intelligent-Computing/DSIC-2706/commit/8bf54415859f3473105c68c369832c2f66522fd8): runner E4 asli cocok SHA-256, H3 dilengkapi ayunan absolut dan tanpa Kebun Raya, riwayat eksploratif H3/H4 dicatat, serta naskah teori dan Gambar 6/8 dikoreksi. E4 tetap lima lokasi dan tidak dijalankan ulang.

Pemeriksaan lanjutan menemukan ringkasan lama pada checklist/logbook dan kehilangan tiga kolom kelompok pada ekspor kasus E5. Narasi kini diselaraskan. Seleksi E5 diperbaiki untuk ekspor berikutnya dengan dua tes regresi; pilihan serta nilai 120 kasus historis tetap sama. Sumber hasil E5 tidak ditimpa.

Bukti tambahan: 19 aset identitas E4, 320 snapshot kondisi, dan 41 bahan laporan lama cocok checksum. Analisis H3 dari klon bersih menghasilkan 20 baris identik byte, tanpa audio/cache dalam klon; ini reproduksi statistik parsial dengan runtime yang sudah tersedia.

**Gate 4 belum tuntas.** Audit pendengaran formal masih 0/120 ulasan tercatat. Reproduksi penuh E0–E5 di lingkungan baru belum dibuktikan; arahan tidak mengulang E4 tetap berlaku. Naskah teori tersedia sebagai draf untuk pemeriksaan pembimbing, bukan persetujuan final. Kedua pekerjaan terbuka dapat dikerjakan melalui audit manusia dan protokol reproduksi tersendiri.

- [Rincian revisi pembimbing](../docs/REVISION_SUPERVISOR_2026-10-15.md).
- [Bukti pemeriksaan terstruktur](BUKTI_PEMERIKSAAN_ULANG_2026-10-15.json).
- [Lembar dan petunjuk audit pendengaran E5](audit-pendengaran-E5/README.md).

## 11. Pemeriksaan akhir dan penyelesaian yang dapat diotomasi — 16 Oktober 2026

README dan petunjuk aktif yang masih memuat desain tiga habitat, angka threshold lama, atau klaim reproduksi usang diganti dengan protokol aktif. Perubahan ini merapikan tulisan, tanpa menghapus sumber penelitian yang masih dipakai.

Pengujian lingkungan baru mengungkap perubahan akhir baris pada tiga helper identitas E4 saat checkout. .gitattributes dan penyimpanan blob Git diperbaiki agar hash byte cocok dengan run identity; algoritma serta file lokal sumber tetap sama. Tes baru menguji seluruh 10 aset sumber terlacak pada file lokal dan Git HEAD.

**Reproduksi E0, ekstraksi ulang clean R0–R3, E1, E2, E3, E5, dan statistik H3 sudah selesai pada klon terpisah/venv baru.** Seluruh 3.289 input salinan cocok SHA-256; tidak ada embedding lama yang dipakai. Seluruh 41 perbandingan cocok dan selisih numerik maksimum 0,0. Suite terbaru lulus 36/36 tes pada lingkungan lama dan venv baru.

E4 audio/model inference tetap tidak diulang sesuai arahan pembimbing. Hasil baru disimpan terpisah pada results/reproductions/RECHECK_FRESH_20261016; keluaran besar lokal tidak di-commit. Ini belum diklaim reproduksi seluruh E0–E5 termasuk inferensi E4 atau lingkungan OS baru.

**Persiapan audit pendengaran tuntas:** 120 kasus dipetakan ke 276 klip unik dengan identitas noise, segmen, SNR, dan sampel WAV terverifikasi. Halaman lokal menyediakan pemutar dan pencatatan; importer mengekspor ke CSV baru setelah validasi provenance. **Ulasan manusia masih 0/120 tercatat** dan harus diisi sesudah pendengaran yang benar-benar dilakukan.

- [Rincian revisi pembimbing](../docs/REVISION_SUPERVISOR_2026-10-15.md).
- [Protokol dan bukti lingkungan baru](../docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md).
- [Paket audit pendengaran](audit-pendengaran-E5/README.md).

## 12. Tindak lanjut pembimbing 1 — dicatat 18 Oktober 2026

Fabio menyampaikan umpan balik bahwa poin 1–3 secara substansi telah terpenuhi: hash E4 cocok, angka H3 sesuai hitungan ulang, dan Teori Dasar benar. Ini catatan umpan balik pembimbing, bukan klaim seluruh Gate 4 sudah selesai.

- **Tautan laporan pengganti:** dokumen Catatan Progres Bimbingan ini tetap tersedia di GitHub. Empat laporan/draf chat yang diminta dihapus tidak dipulihkan. Tautan yang sudah dikirim ke pembimbing perlu diganti dengan URL dokumen ini.
- **Runner tidak digunakan:** run_e4_domain_shift.py diberi label arsip tiga lokasi dan eksekusi langsung dihentikan sebelum impor/pembuatan output. Runner stage7 serta hash identitas aktif tidak berubah.
- **Tes:** total 41, lulus 41, dilewati 0, gagal 0, error 0 pada workspace ini. Missing input/model sekarang menjadi SkipTest, dan alasan skip dicetak. Penambahan lima hitungan berasal dari pemisahan empat dimensi model dan dua regresi pelaporan. [Ringkasan terstruktur](../artifacts/reproducibility/test_summary_2026-10-18.json). Hasil 36 tes pada 16 Oktober tetap riwayat, bukan pengganti hasil saat ini.
- **Opsional H3 selesai:** lima lokasi dihilangkan satu per satu, dengan baseline lima lokasi, dua metrik, empat SNR serta rata-rata SNR. Total 60 baris; 10.000 bootstrap query berpasangan, seed sama. Dua skenario historis direproduksi dalam toleransi 1e-12. [Tabel dan metadata](../results/reproductions/H3_leave_one_location_out_20261018/README.md). Semua CI selisih rata-rata absolut mencakup nol; hasil relatif rata-rata tetap bergantung skala dan tidak boleh digeneralisasi ke tiap SNR. Penghilangan lokasi tidak menguji sebab-akibat.
- **Audit manusia:** paket 120 kasus tetap siap, tetapi observasi harus ditulis oleh Fabio/pendengar yang benar-benar mendengarkan. Tidak ada kasus yang otomatis ditandai reviewed. [Panduan praktis dan latihan penjelasan lisan](PANDUAN_AUDIT_E5_DAN_PENJELASAN_LISAN.md).
