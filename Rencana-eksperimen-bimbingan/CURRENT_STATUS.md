# Status Saat Ini untuk Bimbingan

**Tanggal: 15 Oktober 2026.** Revisi pembimbing dilakukan pada pelaporan, provenance kode E4, dan naskah teori. E4 lima lokasi tidak dijalankan ulang.

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
