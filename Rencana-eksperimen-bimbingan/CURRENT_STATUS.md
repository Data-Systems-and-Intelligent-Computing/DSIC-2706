# Status Saat Ini untuk Bimbingan

**Tanggal: 18 Oktober 2026.** Revisi pembimbing dilakukan pada pelaporan, provenance kode E4, dan naskah teori. E4 lima lokasi tidak dijalankan ulang.

- Desain E4 tetap 311 query × 5 lokasi × 4 SNR × 4 ulangan per representasi.
- Runner E4 asli disertakan byte-for-byte; SHA-256: 30cc0ea990e35eda70a98a6928550cb18df39bb4cd9b95837fafe05512f80c2c.
- H3 dilaporkan dengan ayunan absolut dan relatif, serta sensitivitas tanpa Kebun Raya. Tidak digunakan kesimpulan keunggulan stabilitas R2 yang berlaku umum.
- H3/H4 hasil reformulasi diberi label eksploratif pada hypotheses.md, rq.md, dan scope-reframe; rumusan asli 6 September dan perubahan 12/15 Oktober dicatat.
- Naskah teori sendiri serta Gambar 6/8 baru tersedia di paper/. Draf dosen tetap menjadi rujukan.

## Angka utama H3

Rata-rata ayunan absolut lima lokasi: R1 = 0,042324, R2 = 0,030949, Δ = 0,011375; CI [−0,003993; 0,022140]. Selisih rata-rata ayunan relatif lima lokasi adalah 0,191504, lalu turun menjadi 0,069097 tanpa Kebun Raya.

Pada −5 dB tanpa Kebun Raya, ayunan relatif R1 = 0,065937 dan R2 = 0,083724; CI selisih [−0,041711; 0,050057]. Keunggulan relatif R2 tidak meyakinkan pada kondisi tersebut. Mekanisme serangga/frekuensi masih dugaan.

## Bukti untuk diperiksa

- [Catatan perubahan rinci](../docs/REVISION_SUPERVISOR_2026-10-15.md).
- [Tabel sensitivitas dan CI](../results/reproductions/H3_sensitivity_20261015/tables/h3_swing_summary.csv).
- [Matriks RQ/H revisi](../results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv).
- [Naskah Teori Dasar](../paper/teori_dasar.md).
- [Riwayat hipotesis](../docs/research/hypotheses.md).

## Batasan yang tetap berlaku

Analisis membaca raw E4 tersimpan, tanpa pengubahan threshold atau data. Lima profil noise bukan rekaman burung target in-situ. Bootstrap memegang lokasi serta segmen noise tetap. Cache baru hanya dapat dibangun pada direktori baru dengan provenance tersendiri; README menjelaskan prasyarat dan perbedaannya dari input historis.

## Pemeriksaan akhir dan Gate 4

- **Reproduksi yang diizinkan selesai:** klon terpisah, venv baru, 3.289 input salinan terverifikasi, tanpa embedding lama; E0, ekstraksi clean R0–R3, E1, E2, E3, E5, serta statistik H3 selesai. **41/41 perbandingan cocok**, selisih numerik maksimum 0,0.
- **Hasil terbaru 18 Oktober: 41 lulus, 0 dilewati, 0 gagal, 0 error dari 41 tes** pada workspace ini. Hasil 36 tes pada lingkungan lama/baru adalah pemeriksaan 16 Oktober. Tes Git memeriksa seluruh 10 aset sumber E4 terlacak. Byte tiga helper kini cocok dengan hash historis setelah checkout.
- **Audit manusia belum selesai:** 120 kasus sudah memiliki 276 klip terverifikasi, halaman pemutar/catatan, dan importer CSV baru. Masih 0/120 ulasan formal tercatat.
- **Inferensi E4 tidak diulang** sesuai pembimbing. Ini batas reproduksi, bukan kekurangan pelaksanaan E4 aktif. Naskah masih draf untuk pemeriksaan pembimbing.

[Catatan progres](CATATAN_PROGRES_BIMBINGAN.md), [protokol reproduksi](../docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md), dan [paket audit pendengaran](audit-pendengaran-E5/README.md).

## Tindak lanjut umpan balik pembimbing 1 — dicatat 18 Oktober

Menurut umpan balik yang disampaikan Fabio, poin 1–3 telah diperiksa pembimbing dan secara substansi terpenuhi. Tautan laporan pengganti yang masih tersedia adalah [Catatan Progres Bimbingan](CATATAN_PROGRES_BIMBINGAN.md). Runner tiga lokasi ditandai tidak digunakan; pelaporan tes memisahkan lulus dan skipped. [Sensitivitas H3 penghilangan tiap lokasi](../results/reproductions/H3_leave_one_location_out_20261018/README.md) tersedia tanpa run E4 baru.

Pekerjaan utama tetap audit manusia 120 kasus. [Panduan siapa/cara mendengar dan latihan penjelasan lisan](PANDUAN_AUDIT_E5_DAN_PENJELASAN_LISAN.md) menjelaskan langkah yang dilakukan Fabio, H3 absolut/relatif, dan batas Recall@10. Tidak ada observasi manusia yang diisi otomatis.
