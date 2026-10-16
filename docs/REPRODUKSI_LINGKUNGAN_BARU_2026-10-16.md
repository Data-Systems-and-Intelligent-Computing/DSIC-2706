# Reproduksi pada Lingkungan Python Baru — 16 Oktober 2026

## Hasil yang sudah dibuktikan

Klon Git terpisah menggunakan commit **3ffce587e85b4c692d42ada1964a4d65ac4a25d5**, setelah perbaikan penyimpanan byte modul identitas E4. Venv baru memakai Python 3.12.14, tanpa system-site-packages. Dependensi dipasang kembali melalui requirements.txt; cache unduhan installer boleh dipakai, sedangkan embedding/cache eksperimen lama tidak disalin.

Sebanyak **3.289 input unik** dipulihkan dari arsip lokal dan diverifikasi SHA-256 sebelum/sesudah penyalinan: 1.216 target, 1.799 noise, 272 unknown burung non-target, dan dua checkpoint. Sebanyak 271 unknown noise sudah termasuk bank noise, sehingga tidak dihitung dua kali. File class_labels_indices.csv PANNs tetap merupakan input eksternal pada profil pengguna; path dan hash-nya tercatat dalam bukti.

| Tahap | Hasil |
|---|---|
| E0 | Audit 100 rekaman dan probe R0–R3 selesai |
| Ekstraksi ulang clean | Gallery/query R0–R3 dibangun dari audio/ID; empat embedding numerik identik dengan cache sumber |
| E1 | Ranking dan metrik empat representasi dihitung dari embedding baru |
| E2 | Seluruh 20 kondisi termasuk clean, masing-masing 311 query, dijalankan ulang |
| E3 | Kalibrasi serta transfer test dijalankan ulang; threshold dan seluruh kolom yang dibandingkan sama |
| E5 | Diagnostik komputasional dijalankan ulang; pilihan/nilai 120 kasus sama, kolom kelompok tetap ada |
| E4 | Audio/model inference tidak diulang sesuai arahan pembimbing; sumber beku dipertahankan |
| H3 | Statistik dari raw E4 tersimpan dihitung ulang; ringkasan identik |

**41/41 perbandingan cocok**, meliputi embedding, E0, E1, 20 raw E2, empat tabel/raw E3, lima tabel E5, dan H3. Toleransi pemeriksaan rtol/atol = 1e-6; selisih numerik maksimum aktual **0,0**. Perbandingan E5 memakai kolom historis yang sama; tiga kolom kelompok tambahan pada ekspor baru tidak dihapus untuk memaksakan identitas schema.

Ini pengujian pada **venv baru di komputer yang sama**, dengan audio/checkpoint dari arsip lokal terverifikasi. Ini bukan instalasi sistem operasi baru atau pengunduhan audio ulang. Tidak ada klaim seluruh inferensi E0–E5 telah diulang karena E4 sengaja dikecualikan. Audit pendengaran manusia adalah pekerjaan lain dan tidak dipenuhi oleh reproduksi komputasional.

[Bukti terstruktur](../results/reproductions/RECHECK_FRESH_20261016/comparison_report.json), [progres tiap tahap](../results/reproductions/RECHECK_FRESH_20261016/pipeline_progress.json), [lingkungan](../results/reproductions/RECHECK_FRESH_20261016/environment.json), dan [versi paket aktual](../results/reproductions/RECHECK_FRESH_20261016/requirements-resolved.txt).

## Kekurangan provenance yang ditemukan dan diperbaiki

Pada percobaan awal, checkout mengubah akhir baris tiga helper identitas E4 menjadi LF, sehingga hash tidak cocok dengan run_identity.json walaupun algoritmanya sama. Perbaikan khusus pada .gitattributes dan penyimpanan ulang blob Git mempertahankan byte CRLF asli untuk e4_noise_identity_v1.py, e4_query_identity_v1.py, dan e4_run_identity_v2.py. File lokal dan algoritma tidak diedit; run_identity.json tidak diubah. Setelah perbaikan, seluruh 10 aset sumber terlacak cocok baik pada file lokal maupun byte Git.

Pemulihan input percobaan awal juga melewatkan lima target berstatus VERIFIED_EXISTING. Kelimanya dilengkapi dari arsip dengan hash asli; manifes tidak diubah. Skrip pemulihan yang disertakan mengikuti seluruh path split aktif, sehingga tidak mengandalkan status SUCCESS saja.

## Protokol pengulangan

Kerjakan pada klon terpisah, bukan folder penelitian aktif. Pilih direktori dan nama output baru. Jangan mengubah threshold konfigurasi atau checksum run historis.

1. Klon repository pada direktori baru dan buat venv baru. Pasang dependensi menggunakan requirements.txt; versi aktual pengujian tersedia pada requirements-resolved.txt di bukti.
2. Sediakan arsip audio/checkpoint yang cocok checksum serta file label PANNs. Dari klon, jalankan skrip pemulihan berikut:

```powershell
.\.venv\Scripts\python.exe -B scripts/restore_reproduction_inputs.py --source-root 'PATH_ARSIP_INPUT' --report results/reproductions/RESTORED_INPUTS_BARU.json
```

Skrip menyalin hanya input yang dirujuk manifes, memverifikasi sumber dan salinan, menolak penggantian file berbeda, dan tidak menyalin embedding. --verify-only memeriksa salinan yang sudah tersedia tanpa membuat salinan baru. Gunakan nama laporan baru.

3. Jalankan E0 dan bangun embedding clean pada direktori baru:

```powershell
.\.venv\Scripts\python.exe -B scripts/run_e0_preprocessing_verification.py
.\.venv\Scripts\python.exe -B scripts/rebuild_e4_clean_caches.py --output-dir results/reproductions/FRESH_CLEAN_BARU
```

4. Untuk E1–E3, runner membaca empat cache dari results/features/. Pada klon yang belum memiliki NPZ, salin empat clean_embeddings_R*.npz yang baru dibuat ke lokasi tersebut. Jangan menyalin cache historis. Bila lokasi tujuan sudah berisi cache, gunakan klon baru atau tinjau provenance lebih dahulu; jangan menimpanya otomatis.
5. Jalankan materialize_e1_from_cache.py untuk R0, R1, R2, R3. Langkah ini menghitung retrieval dari cache yang **baru diekstrak** pada langkah 3.
6. Jalankan run_e2_controlled_noise.py. Catat direktori E2 baru, lalu berikan path itu ke run_e3_open_set.py --e2-run. Berikan E2 baru dan E3 baru ke run_e5_diagnostics.py --e2 ... --e3 ... --e4 results/reproductions/E4_5sites_20261011T213404_350219Z.
7. Hitung ulang H3 dengan run_h3_sensitivity_reanalysis.py ke direktori baru, lalu jalankan python -B run_tests.py. E4 historis tidak dieksekusi.
8. Bandingkan ID/order, field audit noise, ranking/metrik, threshold, dan seleksi E5 dengan sumber. Catat perbedaan yang muncul; kesamaan arsip NPZ secara byte tidak diwajibkan ketika embedding dan provenance baru dicatat terpisah.

Skrip pembanding yang benar-benar dipakai pada pengujian ini diarsipkan di [compare_fresh.py](../results/reproductions/RECHECK_FRESH_20261016/compare_fresh.py). Path komputer pada arsip itu merupakan catatan eksekusi; sesuaikan hanya dalam salinan pengujian bila menjalankan di komputer lain.

## Lokasi hasil baru

Keluaran baru disalin ke results/reproductions/RECHECK_FRESH_20261016/local-output/. Folder ini sengaja tidak dilacak Git; hasil sumber tetap pada direktori historisnya. [Daftar salinan](../results/reproductions/RECHECK_FRESH_20261016/archived_local_outputs.json) menghubungkan tahap dan output lokal. Bukti ringkas, hash, versi paket, dan laporan perbandingan dilacak Git.
