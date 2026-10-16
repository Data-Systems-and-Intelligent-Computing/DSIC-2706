# Pemeriksaan Ulang Revisi Pembimbing dan Gate 1–4

> Catatan tahap sebelumnya. Status lanjutan dan bukti reproduksi baru tersedia pada [pemeriksaan akhir 16 Oktober](PEMENUHAN_REVISI_2026-10-16.md); gunakan [draf chat terbaru](DRAF_CHAT_PEMBIMBING_2026-10-16.md).

**Pemeriksaan: 15–16 Oktober 2026.** Basis pemeriksaan adalah commit revisi utama **8bf54415859f3473105c68c369832c2f66522fd8**, yang sudah dipush ke GitHub. Pemeriksaan lanjutan ini menyelaraskan dokumentasi, memeriksa ulang artefak, dan menyiapkan audit manusia. E4 tidak dijalankan ulang dan hasil sumber tidak ditimpa.

## 1. Status setiap arahan pembimbing

| Arahan | Status setelah pemeriksaan ulang | Bukti |
|---|---|---|
| Gunakan kelima lokasi E4, tanpa run ulang | Selesai sesuai arahan | Identitas run memuat 311 query × 5 lokasi × 4 SNR × 4 ulangan; 320 snapshot kondisi cocok checksum |
| Commit skrip penghasil E4 dengan SHA-256 asli | Selesai pada commit 8bf5441 | [Runner asli](../scripts/run_e4_five_locations_v10_stage7.py.draft); hash 30cc0ea990e35eda70a98a6928550cb18df39bb4cd9b95837fafe05512f80c2c cocok identitas run dan klon |
| Cache tidak di-commit; dokumentasikan rekonstruksi | Selesai untuk kode dan petunjuk; ekstraksi penuh belum diuji | [README](../README.md) dan [builder cache clean](../scripts/rebuild_e4_clean_caches.py). Mode check-only telah lulus pada workspace berisi input asli |
| H3 melaporkan ayunan absolut, relatif, dan tanpa Kebun Raya | Selesai | [20 baris ringkasan H3](../results/reproductions/H3_sensitivity_20261015/tables/h3_swing_summary.csv), termasuk CI berpasangan |
| Hindari klaim R2 selalu lebih sempit; mekanisme serangga/frekuensi sebagai dugaan | Selesai; narasi yang tertinggal diselaraskan pada pemeriksaan ini | README §13, catatan bimbingan, log Minggu 3/4, naskah, dan matriks revisi |
| H3/H4 eksploratif; simpan rumusan asli dan tanggal perubahan | Selesai | [Hypotheses](../docs/research/hypotheses.md), [RQ](../docs/research/rq.md), dan [scope-reframe](../docs/research/scope-reframe-2026-10-12.md) mencatat 6 September, 12 Oktober, dan 15 Oktober |
| Teori Dasar ditulis pada naskah sendiri; koreksi 2.8, gap, gambar, gallery, 3.6 | Selesai sebagai draf naskah | [Teori Dasar Fabio](../paper/teori_dasar.md) dan [dua gambar baru](../paper/figures/revision_20261015/). Draf dosen tetap utuh |
| Poin 1–3 dipush agar dapat diperiksa pembimbing | Sudah dipush pada 8bf5441 | [Commit revisi utama](https://github.com/Data-Systems-and-Intelligent-Computing/DSIC-2706/commit/8bf54415859f3473105c68c369832c2f66522fd8). Draf chat tersedia terpisah; tidak dikirim otomatis |

Angka 99.520 pada desain ini adalah baris evaluasi noisy empat representasi, bukan 99.520 query independen. Tidak ada audio, checkpoint, atau cache NPZ/NPY yang dilacak Git.

## 2. Kekurangan yang ditemukan pada pemeriksaan ulang

Checklist README §13 sebelumnya masih memakai ringkasan retensi H3 saja. Catatan Progres Bimbingan dan beberapa ringkasan Minggu 3/4 juga masih memakai kesimpulan lama “H1–H5 didukung” atau H3 didukung tanpa pembatasan skala/subset. Bagian-bagian tersebut kini diselaraskan dengan sensitivitas 15 Oktober; hasil statistik historis tetap dipertahankan.

Klaim reproduksi end-to-end dan bank noise “bird-free verified” pada ringkasan README juga dipersempit sesuai bukti. Rencana historis tetap ditandai sebagai riwayat, bukan bukti kelulusan Gate aktif.

Istilah “Zero Leakage” pada checklist diperjelas menjadi pemisahan internal target antara Gallery, Query, dan Calibration. Nol overlap pada tiga partisi ini tidak membuktikan independensi sesi/perekam unknown, dan tidak menghapus kemungkinan overlap data pralatih.

Angka 25 tes masih benar untuk suite lama, tetapi lima tes H3 sebelumnya perlu dijalankan terpisah. Kelima tes H3 dan dua tes regresi E5 kini dimasukkan ke entry point utama; satu perintah python run_tests.py menjalankan **32/32 tes**, dan semuanya lulus pada pemeriksaan akhir 16 Oktober.

Kalimat tentang bounding box/in-situ dan “Deferred H3” pada checklist/batas publikasi diperjelas. E4 aktif adalah additive noise lima lokasi. Pengumpulan serta anotasi korpus burung in-situ bukan pekerjaan wajib untuk menuntaskan revisi tersebut.

Ditemukan pula bahwa CSV 120 kasus E5 tidak memuat kolom representation, condition, dan failure_mode, sementara ketiganya ada pada diagnostik lengkap. Kode seleksi historis memakai groupby/apply; pada lingkungan pandas yang tercatat, kolom pengelompokan tidak hadir pada ekspor kasus terpilih. Sumber E5 tidak diubah. Lembar audit baru memulihkan ketiganya dengan syarat **setiap baris pilihan memiliki tepat satu pasangan yang cocok pada semua kolom aslinya** di diagnostik E2 lengkap. Seluruh 120 baris berhasil dicocokkan; tidak ada label yang ditebak.

Untuk mencegah kehilangan kolom pada ekspor berikutnya, fungsi select_failure_cases pada scripts/run_e5_diagnostics.py kini mengiterasi kelompok secara eksplisit, mempertahankan seluruh kolom, kuota dua kasus per kelompok, serta seed 20261012. Dua tes regresi membuktikan kolom kelompok tetap ada dan pilihan/nilai 120 kasus historis tidak berubah. Perbaikan kode ini tidak menjalankan E5 ulang atau mengganti CSV sumber.

## 3. Status Gate dan pekerjaan yang masih terbuka

| Gate | Status | Penjelasan |
|---|---|---|
| Gate 1: data, preprocessing, representasi, E1 | Keluaran komputasional tersedia dan pemeriksaan internal lulus | Manifes 673 Gallery, 311 Query, 232 Calibration; dimensi cache R0–R3 dan pemisahan ID/path/perekam diperiksa |
| Gate 2: E2 | Selesai dalam scope controlled mixture | 20 CSV, masing-masing 311 query, tersedia untuk R0–R3 × lima kondisi termasuk clean |
| Gate 3: E3/E4 | Selesai dalam scope aktif, dengan batas inferensi | E4 tetap lima lokasi; H3/H4 reformulasi eksploratif, bukan validasi in-situ |
| Gate 4: audit kualitatif, reproduksi penuh, finalisasi penulisan | **Belum tuntas** | Audit manusia 120 kasus dan reproduksi penuh dari lingkungan baru masih terbuka; naskah masih draf untuk pemeriksaan pembimbing |

Checklist lengkap yang diperbarui ada pada [README §13](../README.md#13-definition-of-done-status-kelulusan-gate-1-sd-gate-4).

### Audit pendengaran E5

**Mengapa belum selesai:** diagnosis komputasional, label metadata, dan tersedianya 120 kasus tidak sama dengan bukti pendengaran manusia. Belum ada lembar formal yang mendokumentasikan pendengar, waktu, observasi, dan ketidakpastian untuk seluruh kasus. Catatan latihan pada learning/ tidak otomatis memenuhi audit E5 karena protokol segmen/fiturnya berbeda.

**Bisa dikerjakan:** ya, bertahap oleh Fabio atau penelaah yang ditunjuk, misalnya 10–20 kasus per sesi. [Lembar audit](audit-pendengaran-E5/E5_AUDIT_PENDENGARAN.csv) dan [petunjuk](audit-pendengaran-E5/README.md) sudah disiapkan. Saat pembuatan lembar, 120/120 baris berstatus pending dan seluruh kolom pengamatan manusia kosong. Ini bukan klaim bahwa belum pernah ada orang mendengar file-file tersebut; ini status bukti formal audit yang tersedia.

Terdapat 80 query unik dan 117 pasangan query–kondisi di antara 120 kasus. Kasus yang memakai audio query sama tetap dapat memiliki hasil retrieval berbeda dan memerlukan penilaian per kasus. Audio yang didengar harus mengikuti jendela berenergi dan campuran E2 yang digunakan eksperimen; mendengarkan lima detik pertama file asli saja tidak cukup. Klip dengar terproses belum dibuat dalam pemeriksaan ini.

### Reproduksi penuh dari klon bersih

**Mengapa belum selesai:** klon Git memang tidak membawa audio, checkpoint, atau cache. Reproduksi penuh perlu menyiapkan input eksternal yang cocok checksum, lingkungan baru, membangun embedding, menjalankan tahapan eksperimen, dan membandingkan keluaran. Pemeriksaan checksum atau tes unit pada workspace lama tidak membuktikan semua tahapan itu.

**Bisa dikerjakan:** secara teknis bisa melalui protokol reproduksi terpisah dengan input serta lingkungan tercatat. Namun pemeriksaan ini tetap mematuhi arahan bahwa E4 tidak dijalankan ulang; reproduksi penuh E0–E5 tidak dicentang selesai. Pengujian ulang statistik dari hasil tersimpan sudah dilakukan sebagai bukti parsial yang dijelaskan berikut.

### Pekerjaan yang tidak menjadi syarat revisi aktif

Pengumpulan korpus burung target in-situ serta anotasinya adalah perluasan penelitian. Analisis fitur spektral noise diperlukan bila ingin menguji dugaan hubungan spektral; karena mekanisme tersebut tidak diklaim terbukti, analisis itu tidak harus dilakukan untuk menyelesaikan arahan “tulis sebagai dugaan”. Analisis hubungan spektral pun tidak otomatis membuktikan sebab-akibat.

## 4. Reproduksi parsial yang sudah berhasil

Klon bersih dibuat melalui transport Git lokal dengan --no-local --depth 1, sehingga hanya isi commit 8bf5441 yang ikut, bukan perubahan working tree, audio, atau cache lokal. Commit itu sebelumnya sudah dicocokkan dengan origin/main. Ini bukan unduhan baru dari GitHub dan bukan penyiapan lingkungan dari nol.

Analisis H3 dijalankan dari kode dan CSV pada klon tersebut, memakai Python/venv proyek yang sudah tersedia. Klon tidak memiliki audio, checkpoint, NPZ, atau NPY. Tidak ada pencampuran audio atau inferensi model.

Hasilnya:

- Seluruh **20 baris statistik H3 sama**, selisih numerik maksimum 0,0.
- CSV ringkasan hasil klon **identik byte** dengan artefak sensitivitas 15 Oktober.
- Lima tes metode H3 pada klon lulus.
- Bukti ini mencakup reproduksi statistik H3 dari CSV tersimpan, bukan reproduksi penuh E0–E5 atau lingkungan perangkat lunak baru.

Peringatan pandas tentang tipe kolom campuran muncul pada kolom audit yang tidak dipakai menghitung AP@10; proses selesai dan kesamaan keluaran diverifikasi. Tidak ada perubahan pada script H3 atau sumber E4 untuk menghilangkan peringatan tersebut.

## 5. Bukti pemeriksaan artefak

[Catatan verifikasi terstruktur](BUKTI_PEMERIKSAAN_ULANG_2026-10-15.json) merekam hasil:

- **19/19 aset** yang dirujuk identitas E4 cocok SHA-256.
- **320/320 snapshot kondisi** cocok checksum dan mencatat 311 query.
- Cache clean memiliki ukuran Gallery/Query sesuai R0 40-d, R1 2.048-d, R2 1.024-d, dan R3 40-d.
- AP@k dan Recall@k untuk k = 1, 5, 10 tersedia pada 20 CSV E2 dan empat raw E4; setiap raw E4 berisi 25.191 baris termasuk baseline clean.
- Semua pasangan partisi internal target memiliki nol irisan ID, path, dan nama perekam sesuai manifes.
- **41/41 bahan laporan lama** tetap cocok checksum, begitu pula output revisi yang dirujuk metadata.
- Lembar audit E5 cocok dengan sumber dan belum memuat jawaban manusia.
- Suite utama **32/32 tes lulus**; lima tes H3 pada klon bersih juga lulus.

## 6. Urutan tindak lanjut

1. Sampaikan revisi utama dan catatan pemeriksaan ulang ini kepada pembimbing untuk pengecekan poin 1–3.
2. Lakukan audit pendengaran E5 dengan segmen yang sesuai eksperimen dan simpan observasi per kasus.
3. Susun protokol reproduksi penuh secara terpisah bila diperlukan; jangan menganggap bukti parsial H3 sebagai kelulusan end-to-end.
4. Lanjutkan pengembangan Bab 4/Bab 5 dari hasil serta batas inferensi yang sudah dikalibrasi. Draf teori bukan naskah akhir yang sudah disetujui pembimbing.

[Draf chat kepada pembimbing](DRAF_CHAT_PEMBIMBING_2026-10-15.md) disiapkan untuk disalin oleh Fabio; tidak ada pesan yang dikirim otomatis.
