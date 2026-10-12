> **Status historis:** dokumen ini mencatat tahap restart sebelumnya. Scope aktif kini ada di `docs/research/scope-reframe-2026-10-12.md`: E4 adalah additive noise-profile sensitivity, dan H3 telah diuji sebagai stabilitas retensi lintas lima profil noise lokasi.

# Status restart — 11 Oktober 2026

Atas instruksi pengguna, keluaran lama yang terbukti bermasalah dihapus dari working tree. Data audio, manifes, checkpoint, referensi, dan arsip eksperimen BirdCLEF tidak dihapus. Belum ada eksperimen yang dijalankan ulang.

## Bukti dan lingkup penghapusan

Versi sebelum perubahan: `930f6f2ea381221ba29fa09227e86d3d3df1eb33`.

`scripts/recompute_and_sync_all.py` mengisi hasil XC42472 dari rata-rata hasil rekaman lain tanpa mengekstrak representasi audionya. Pemeriksaan CSV membuktikan kecocokan rumus imputasi pada 20 berkas E1/E2, 52 baris E4 dalam empat berkas, dan 20 skor E3 test. Skrip tersebut dinonaktifkan sebelum impor dependensi maupun penulisan berkas; badan kode lama dipertahankan sebagai bukti.

Dihapus sebanyak 45 berkas:

- 20 `results/raw/R{0,1,2,3}_{Clean,SNR_20dB,SNR_10dB,SNR_0dB,SNR_-5dB}_raw.csv`;
- empat `results/raw/E4_R{0,1,2,3}_raw.csv`;
- `results/raw/E3_test_scores_raw.csv`;
- lima tabel, masing-masing di `results/processed/` dan `paper/tables/`: `clean_retrieval_table`, `snr_robustness_table`, `threshold_transfer_table`, `e4_domain_shift_table`, `statistical_significance_table`;
- lima grafik, masing-masing di `results/figures/` dan `paper/figures/`: `clean_retrieval_benchmark`, `relative_retention_curve`, `robustness_curve_map10`, `e3_threshold_transfer_snr`, `e4_noise_profile_sensitivity`.

Daftar path persis, ukuran, SHA-256 sebelum penghapusan, dan alasannya dicatat di `restart_deleted_results_2026-10-11.json`. Catatan tersebut menyimpan metadata, bukan salinan hasil. Riwayat Git tetap tersedia; penghapusan ini belum di-commit atau di-push.

Pada 12 Oktober 2026, pelaporan H3 dalam `src/bootstrap_inference.py` diperbaiki: p-value dan status signifikansi kini memakai keluaran `calc_stats`, dan kesimpulan "H3 Terdukung Parsial" yang ditetapkan tetap dihapus. Tes regresi memeriksa bahwa hasil tidak signifikan tetap dilaporkan tidak signifikan. Ini baru perbaikan pelaporan; penyelarasan ID sebelum bootstrap, definisi uji hipotesis, dan keseluruhan metode statistik belum selesai diaudit. Tabel statistik yang terkait tetap telah ditarik; belum ada bootstrap eksperimen yang dijalankan ulang.

## Keluaran yang masih ada

Keberadaan berkas lama bukan tanda sudah valid. Kalibrasi, analisis kegagalan, cache embedding, hasil per-query terdahulu, laporan, notebook, dan naskah masih perlu diaudit. `results/processed/execution_note_E1.json` menyebut gallery 674/query 310/calibration 233, sedangkan manifes saat ini gallery 673/query 311/calibration 232. Jangan gunakan cache atau hasil lama untuk eksperimen baru sebelum kesesuaian ID, urutan, parameter, serta checksum manifes dibuktikan. Jangan mengganti baris hilang dengan angka perkiraan.

Tes lama yang mewajibkan CSV hasil tersebut akan gagal setelah penarikan; ini bukan izin membuat CSV pengganti. Pisahkan nanti tes kebenaran metode dari pemeriksaan kelengkapan keluaran eksperimen.

## Langkah berikutnya

1. Buat latihan terpisah yang dapat diulang untuk query XC42472 dan kandidat XC120964/XC1003648. Tetapkan pemilihan potongan serta parameter MFCC dan jelaskan setiap tahap bersama pengguna. Skor latihan di percakapan bukan hasil E1 resmi.
2. Audit manifes dan cache, lalu bekukan protokol preprocessing dan metrik sebelum baseline baru.
3. Perbaiki statistik dan pengujian metode. Jalankan eksperimen penuh hanya sesudah protokol serta kode siap dan pengguna mengizinkan.

## Paket pembaruan awal — 12 Oktober 2026

- Latihan 01–05 tersedia di `learning/`, terpisah dari eksperimen resmi. Pengamatan pengguna dan hasil latihan dicatat di `learning/CATATAN_BELAJAR.md`. Pengguna telah menjalankan latihan 05 dengan hasil yang sama seperti uji Codex.
- Pemeriksa `scripts/audit_manifests.py` tersedia dengan Python standar tanpa instalasi paket. Default hanya membaca dan mencetak hasil; tidak menjalankan eksperimen atau menyimpan file. Peluncur pengguna: `learning/06_periksa_manifes.ps1`.
- Cakupan pemeriksa: split/download/noise/unknown aktif, serta log unduhan, indonesia_train dan species_freeze bila tersedia; keberadaan/path, ID, SHA-256, ukuran yang tersedia, author known, spesies unknown, duplikasi fisik dan lintas peran. Seluruh audio pada tiga folder data di-hash, termasuk buffer. Ini belum memvalidasi semantik seluruh CSV, decoding/durasi, sesi lapangan, identitas semua perekam unknown, kebenaran bird-free, atau kontaminasi pretraining.
- `VERIFIED_EXISTING` adalah status unduhan sah selain `SUCCESS`; kategori derau aktual adalah `itera_environmental_noise`. Log unduhan boleh menyimpan riwayat rekaman yang sudah dikeluarkan dari split; perbedaan tersebut dilaporkan sebagai peringatan, bukan otomatis dihapus.
- Sepuluh tes di `tests/test_restart_preflight.py` lolos: audit read-only, perubahan manifes selama audit, berkas hilang/rusak, ID duplikat, author dinormalisasi, audio identik lintas kelompok, duplikat buffer, spesies unknown/path keluar proyek, skema aktual/log historis, dan pelaporan H3. Fingerprint manifes dicatat dan diperiksa lagi di akhir audit agar perubahan selama pemeriksaan tidak lolos tanpa peringatan.
- Ditemukan tambahan XC1073401 pada `download_audit_log.csv` dan `indonesia_train.csv`, yang tidak ada di split/download aktif. Dua file audio XC1073400/XC1073401 masih identik secara fisik; file yang dikeluarkan dari split tidak dihapus. Kedua manifes pendukung belum diubah.
- `results/reproductions/` sudah ada ketika paket ini diperiksa; keluaran tersebut bukan dibuat oleh paket latihan ini dan tidak diubah atau dihapus. Perlu ditinjau tersendiri sebelum digunakan.
- Perubahan paket ini masih lokal, belum di-commit atau di-push. GitHub belum diperbarui.

Audit versi final selesai pada 12 Oktober 2026, status `PASS_WITH_WARNINGS`; laporan lengkap `docs/audit_manifest_2026-10-12.json`. Seluruh 3.396 audio fisik diperiksa SHA-256 (1.217 target, 380 unknown, 1.799 noise). Tidak ditemukan berkas rujukan hilang, mismatch checksum, atau audio identik lintas peran yang diperiksa. Perekam gallery/query/calibration beririsan nol setelah normalisasi nama. Derau E3 yang dicadangkan 271 file, menyisakan 1.528 dari pool untuk pencampuran. Peringatan tetap ada untuk 30 grup folder/tanggal noise calibration/test yang sama, author unknown yang belum diverifikasi, dua manifes pendukung yang masih merujuk XC1073401, dan duplikasi fisik XC1073400/XC1073401. Sebanyak 108 audio unknown buffer tidak dirujuk manifes yang diperiksa. Status ini tidak menyatakan keseluruhan dataset bebas kebocoran.

## E0 dan EDA formal — 12 Oktober 2026

- E0 formal selesai pada 100 rekaman aktif yang dipilih deterministik (seed
  `20261012`) dan disimpan sebagai artefak terpisah di
  `results/reproductions/E0_20261011_202557`. Semua 100 berkas menghasilkan
  audio pra-pemrosesan 5 detik/160.000 sampel yang finite. Probe satu berkas
  menghasilkan dimensi R0/R1/R2/R3 yang benar. Enam dari 100 sampel memakai
  kontainer WAV dengan ekstensi `.mp3`; tidak ada kegagalan `soundfile`.
- EDA formal selesai untuk 3.396 audio fisik di
  `results/reproductions/EDA_20261011_202714`: 1.216 target aktif, 272 unknown
  bird, 271 noise E3 yang dicadangkan, 1.528 noise pool, dan 109 berkas fisik
  tak dirujuk. Tidak ada kegagalan decoding `soundfile`; terdapat 101 mismatch
  ekstensi `.mp3` terhadap kontainer WAV. Ini adalah masalah penamaan/format
  yang harus dicatat pada metode, bukan alasan untuk mengubah audio mentah.
- Tabel/grafik E0–EDA lama dan notebook lama dihapus. Naskah lama yang
  mengklaim hasil final diganti dengan draf protokol tanpa angka hasil. Runner
  tes lama juga diganti; `python run_tests.py` kini menjalankan 25 tes metode
  dan integritas restart yang lulus pada lingkungan lokal.

Perbaikan utama berikutnya: validasi/join hasil berdasarkan query_id sebelum statistik; pastikan preprocessing dan extractor utama sesuai konfigurasi serta checkpoint; uji kebenaran metrik; kemudian jalankan ulang baseline yang protokolnya sudah dibekukan. Pengembangan kode bisa berjalan sambil pengguna belajar, tanpa menunggu pengguna menguasai seluruh teori.

Pada pemeriksaan folder lanjutan, tiga cache bersih R1/R2/R3 yang memakai nama E4 sempat terhapus.
Setelah pengguna meminta cache dipertahankan, cache tersebut dibangun ulang dari audio aktif, manifes
aktif, dan checkpoint lokal pada 12 Oktober 2026. Artefak pemulihan berada di:

- `results/reproductions/E4_clean_cache_R1_20261011T204428_478762Z`;
- `results/reproductions/E4_clean_cache_R2_20261011T204031_982072Z`;
- `results/reproductions/E4_clean_cache_R3_20261011T203439_269234Z`.

Setiap folder menyimpan embedding gallery/query, ID, label, checksum manifest, metadata, dan README.
Salinan kompatibilitas juga tersedia pada `results/features/clean_embeddings_R0.npz` sampai
`clean_embeddings_R3.npz` untuk skrip lama yang masih membacanya. Cache ini **bukan** keluaran E4:
tidak ada pencampuran derau, metrik kondisi derau, statistik, atau kesimpulan E2--E5. E1 yang telah
dijalankan lengkap dan dapat dikutip tetap hanya R0.
