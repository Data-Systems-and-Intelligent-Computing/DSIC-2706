# Petunjuk Audit Pendengaran E5

Lembar E5_AUDIT_PENDENGARAN.csv berisi 120 kasus dari artefak E5 yang sudah ada. Saat disiapkan, semua berstatus pending dan kolom pengamatan manusia kosong. Label spesies merupakan metadata dataset, bukan hasil identifikasi baru oleh pendengar.

Kolom representasi, kondisi, dan moda kegagalan komputasional dipulihkan dari diagnostik lengkap dengan pencocokan persis terhadap seluruh kolom sumber kasus pilihan. Metadata mencatat hash sumber serta output. Berkas sumber E5 tidak diubah.

## Siapa yang mendengarkan?

Fabio sebagai peneliti utama mendengarkan dan mencatat pengamatannya sendiri. Pembimbing dapat memeriksa contoh saat bimbingan; pendengar kedua boleh membantu jika tersedia, dengan namanya dicatat. Asisten menyiapkan klip dan memvalidasi data, tetapi tidak mengisi pengamatan atas nama manusia. Tidak perlu menebak spesies jika tidak yakin: gunakan uncertain.

[Langkah praktis dan contoh penjelasan lisan H3/Recall@10](../PANDUAN_AUDIT_E5_DAN_PENJELASAN_LISAN.md).

## Audio yang perlu diperiksa

Untuk query clean dan audio Top-1, gunakan hasil preprocessing resmi: mono 32 kHz, jendela lima detik berenergi tertinggi dengan hop 1,25 detik, padding bila pendek, dan normalisasi RMS sesuai kode. Jangan menggantinya dengan lima detik pertama file asli.

Untuk query noisy E2, rekonstruksi campuran sesuai kondisi, noise_seed, noise_file, noise_start_sample, dan SNR pada kasus. Sebelum dipakai mendengar, identitas noise/segmen serta SNR harus cocok dengan audit sumber. Menyiapkan klip dengar E2 tidak memerlukan menjalankan E4 atau mengekstraksi embedding model.

File path pada lembar menunjuk audio asli. **Klip terproses sudah tersedia** pada [halaman audit lokal](listening-pack-20261016/index.html), dengan [indeks kasus–audio](listening-pack-20261016/case_audio_index.csv) dan [metadata verifikasi](listening-pack-20261016/metadata.json). Terdapat 276 klip unik untuk 120 kasus: query sesuai kondisi, query clean pembanding, serta Top-1. Semua mono 32 kHz, lima detik, WAV float32; penyimpanan audio diverifikasi identik sampel. Identitas segmen noise dan SNR dibandingkan ke raw E2.

Buka index.html dari folder lokal setelah klip dibangun; GitHub tidak membawa WAV dan tidak menjalankan halaman audit ini. Gunakan pemutar browser lokal. Navigasi, penyimpanan, dan ekspor diuji dengan fixture di memori; belum ada validasi tampilan atau pemutaran suara melalui browser otomatis. Review atas audio asli yang tidak sesuai segmen belum memenuhi audit kasus eksperimen.

## Cara mengisi

1. Catat nama pendengar dan tanggal pada reviewer serta reviewed_at.
2. Dengarkan query pada kondisi yang tercatat dan hasil Top-1; gunakan versi clean query sebagai pembanding bila diperlukan.
3. Isi query_vocalisation_audible dan top1_vocalisation_audible dengan yes, no, atau uncertain.
4. Catat latar yang terdengar pada background_observation. Gunakan “terdengar seperti …” jika sumber belum pasti; jangan mengubah dugaan menjadi identitas sumber atau jarak terukur.
5. Isi uncertainty_notes dan auditory_interpretation. Kemiripan menurut pendengaran tidak membuktikan mekanisme spektral atau mengubah label ground truth secara otomatis.
6. Ubah review_status menjadi reviewed hanya setelah pemeriksaan dilakukan. Gunakan needs_follow_up jika audio/segmen tidak bisa dipastikan. Baris pending tidak dihitung selesai.

Dua kasus dengan query/kondisi sama tetap dapat mempunyai Top-1 atau representasi berbeda. Catat penilaian per case_id. Jika koreksi label dataset diduga diperlukan, laporkan melalui catatan terpisah; jangan mengubah manifes atau hasil eksperimen secara langsung.

## Kriteria selesai

Seluruh 120 baris mempunyai reviewer, reviewed_at, observasi query/Top-1, dan interpretasi yang dapat ditelusuri ke segmen yang benar; seluruh masalah needs_follow_up ditangani atau dilaporkan sebagai keterbatasan. Audit ini tidak boleh diisi otomatis dari skor model.

Builder prepare_e5_listening_review.py hanya menyiapkan lembar kosong dan menolak direktori yang sudah ada. Setelah pengisian dimulai, jangan menjalankannya untuk menimpa catatan pendengar.

## Alur halaman audit dan pencatatan hasil

1. Buka halaman lokal, isi nama pendengar, pilih kasus, lalu dengarkan tiga audio pembanding.
2. Isi pengamatan dan ketidakpastian. Penyimpanan ditolak jika kolom wajib belum terisi; penyimpanan dilakukan atas tindakan pendengar. Tidak ada label pengamatan yang diisi dari skor model.
3. Unduh catatan JSON setelah sesi; browser menyimpan catatan lokal sebagai bantuan, bukan satu-satunya arsip. Perpindahan kasus mengabaikan isian yang belum disimpan.
4. Validasi JSON, lalu ekspor ke CSV baru. Script memeriksa sumber/case hash, kolom wajib, timestamp berzona waktu, ID ganda, dan status. Validasi software memeriksa struktur serta provenance, bukan membuktikan pendengaran benar-benar dilakukan.

```powershell
.\.venv\Scripts\python.exe -B scripts/import_e5_human_review.py --review-json PATH_KE/E5_catatan_pendengaran.json --check-only
.\.venv\Scripts\python.exe -B scripts/import_e5_human_review.py --review-json PATH_KE/E5_catatan_pendengaran.json --output Rencana-eksperimen-bimbingan/audit-pendengaran-E5/E5_HASIL_ULASAN_BARU.csv
```

Semua 120 kasus masih pending pada saat paket disiapkan. Tidak ada nama, tanggal pendengaran, atau observasi manusia yang direka. Kriteria audit penuh tetap 120/120 kasus benar-benar diulas.

## Membangun ulang klip pada checkout lain

Siapkan audio dan dependensi sesuai manifes; gunakan direktori baru:

```powershell
.\.venv\Scripts\python.exe -B scripts/build_e5_listening_pack.py --output-dir Rencana-eksperimen-bimbingan/audit-pendengaran-E5/listening-pack-baru
```

Builder tidak mengekstraksi embedding, menjalankan E4, atau menimpa klip/hasil lama. WAV tidak di-commit; metadata dan halaman audit disertakan. Metadata hash mengacu pada lembar kosong sumber; bila lembar itu sudah diubah, builder menolak dan meminta provenance ditinjau, bukan menimpa ulasan.
