# Status Saat Ini untuk Bimbingan

**Tanggal: 16 Oktober 2026.** Revisi pembimbing dilakukan pada pelaporan, provenance kode E4, dan naskah teori. E4 lima lokasi tidak dijalankan ulang.

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

## Pemeriksaan lanjutan dan Gate 4

Suite utama lulus **32/32 tes** (25 sebelumnya + 5 H3 + 2 regresi E5). Sebanyak 19 aset identitas E4, 320 snapshot, dan 41 bahan laporan lama tetap cocok checksum. Reproduksi statistik H3 pada klon bersih menghasilkan CSV identik, tetapi memakai runtime proyek yang sudah tersedia.

**Gate 4 belum tuntas:** audit pendengaran formal 120 kasus E5 dan reproduksi penuh E0–E5 pada lingkungan baru masih terbuka. Lembar audit masih 0/120 ulasan tercatat. Kekurangan kolom kelompok pada ekspor E5 diperbaiki untuk eksekusi berikutnya; pilihan/nilai 120 kasus historis tetap sama dan sumber hasil tidak ditimpa.

- [Laporan pemeriksaan ulang dan alasan pekerjaan terbuka](PEMERIKSAAN_ULANG_GATE_2026-10-15.md).
- [Petunjuk audit pendengaran E5](audit-pendengaran-E5/README.md).
- [Draf chat pembimbing](DRAF_CHAT_PEMBIMBING_2026-10-15.md).
