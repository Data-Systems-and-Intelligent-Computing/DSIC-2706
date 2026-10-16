# Pemenuhan Revisi Pembimbing — Pemeriksaan Akhir 16 Oktober 2026

## Status terhadap arahan pembimbing

| Arahan | Hasil pemeriksaan akhir |
|---|---|
| E4 kelima titik; 311 × 5 × 4 × 4; tanpa run ulang | Terpenuhi. Kelima lokasi serta hasil sumber dipertahankan. Tidak ada inferensi E4 baru. |
| Skrip asli dengan SHA-256 sesuai run_identity.json | Terpenuhi. Runner stage7 cocok 30cc0ea990e35eda70a98a6928550cb18df39bb4cd9b95837fafe05512f80c2c. Tiga helper identitas juga diperbaiki penyimpanan byte Git-nya tanpa perubahan algoritma. |
| Cache besar tidak di-commit; cara pembangunan ulang | Terpenuhi. Petunjuk dan builder tersedia; ekstraksi ulang clean R0–R3 sekarang juga sudah berhasil pada venv baru. |
| H3 absolut, relatif, dan tanpa Kebun Raya | Terpenuhi. Analisis tersimpan dan statistik reproduksi sama; narasi aktif tidak menyatakan R2 selalu berayun lebih sempit. |
| Serangga/frekuensi hanya dugaan | Terpenuhi. Tidak ada klaim mekanisme kausal telah diuji. |
| H3/H4 eksploratif; rumusan asli dan tanggal di hypotheses/rq/scope | Terpenuhi. Riwayat 6 September, perubahan 12 Oktober, serta koreksi 15 Oktober dicatat. |
| Teori Dasar milik mahasiswa: 2.8, gap, Gambar 6, gallery, Gambar 8, 3.6 | Terpenuhi sebagai draf naskah untuk pemeriksaan pembimbing. E4 additive mixture, gallery 673, batas Recall@10 aktif, dan enam kategori konfigurasi AudioMoth sesuai bukti. |
| Push poin 1–3 dan kabari pembimbing | Revisi utama sebelumnya sudah dipush. Catatan pemeriksaan akhir disertakan pada commit pembaruan ini; draf chat diperbarui, tanpa mengirim pesan otomatis. |

Pemenuhan perubahan di atas tidak berarti pembimbing sudah menyetujui naskah. Naskah masih perlu dibaca, dipahami, dan dipertanggungjawabkan Fabio.

## Perbaikan tambahan pada pemeriksaan ini

README yang masih menyajikan pohon folder, perintah, angka threshold, desain tiga habitat, serta klaim statistik lama telah diringkas dan diganti protokol aktif. Riwayat tetap tersedia di Git. Decision-log dan scope-freeze menjelaskan mana keputusan historis dan mana kesimpulan terbaru. Nama perekam diperjelas: 111 nilai nama pada split, atau 112 orang setelah nama gabungan dipisah; partisi tidak berubah.

Kegagalan preflight klon mengungkap konversi akhir baris tiga helper E4. Aturan Git sekarang mempertahankan byte historis, dan tes baru memeriksa hash seluruh 10 aset sumber terlacak pada file lokal sekaligus Git HEAD. E4 run identity serta file lokal helper tidak diedit.

## Audit pendengaran E5: persiapan selesai, ulasan manusia belum

- Seluruh 120 kasus dipetakan ke audio yang sesuai eksperimen.
- **276 klip unik** tersedia lokal: query pada kondisi eksperimen, query clean pembanding, dan Top-1.
- Identitas noise, seed, posisi segmen, panjang segmen, gain, dan SNR diperiksa terhadap raw E2.
- WAV float32 mono 32 kHz, lima detik, diverifikasi identik sampel setelah write/read.
- Halaman audit lokal menyediakan navigasi, catatan pendengar, penyimpanan lokal, dan ekspor JSON. Pemeriksaan logika memakai fixture terpisah di memori, bukan ulasan manusia asli; tampilan/pemutaran belum diuji melalui browser otomatis.
- Importer memeriksa sumber/case hash, ID ganda, kolom wajib, timestamp berzona waktu, dan menulis CSV baru. File sumber tidak ditimpa.

**Status formal masih 0/120 ulasan tercatat.** Persiapan teknis sudah dikerjakan sampai klip dapat didengar dan catatan dapat diarsipkan. Pendengaran manusia tidak dapat diselesaikan dengan mengisi nama/tanggal/observasi buatan. [Buka paket dan petunjuk audit](audit-pendengaran-E5/README.md).

## Reproduksi: seluruh tahap yang diizinkan selesai

Klon terpisah dan venv baru menjalankan E0, ekstraksi ulang clean R0–R3, E1, E2, E3, dan E5. Input eksternal adalah 3.289 salinan terverifikasi SHA-256 dari arsip lokal; embedding lama tidak dipakai. E4 tidak diulang. Statistik H3 dari raw E4 dihitung ulang.

**41/41 perbandingan cocok; selisih numerik maksimum aktual 0,0**, termasuk threshold E3. Hasil baru disimpan terpisah. Lingkungan baru berarti venv pada komputer yang sama, bukan OS baru; input tidak diunduh ulang. [Protokol dan bukti reproduksi](../docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md).

Reproduksi penuh yang mencakup inferensi E4 tetap tidak diklaim, karena bertentangan dengan arahan E4 tidak perlu dijalankan ulang. Ketidaklengkapan audit pendengaran juga tidak ditutupi oleh keberhasilan komputasional.

## Validasi dan pekerjaan tersisa

Suite utama **36/36 tes lulus**: 25 sebelumnya, 5 H3, 2 seleksi E5, 3 impor ulasan, 1 provenance Git E4. Output eksperimen lama, threshold operasional, manifes, audio, checkpoint, dan identitas run tetap menjadi sumber yang tidak ditimpa. Hasil reproduksi baru mempunyai provenance sendiri.

Pekerjaan yang masih memerlukan tindakan manusia adalah mendengarkan dan mencatat 120 kasus, serta pemeriksaan/persetujuan pembimbing atas naskah. Pengulangan inferensi E4 bukan pekerjaan yang ditambahkan pada revisi aktif.

[Draf chat pembimbing terkini](DRAF_CHAT_PEMBIMBING_2026-10-16.md).

[Verifikasi akhir](../results/reproductions/RECHECK_FRESH_20261016/final_verification.json) mencatat 19 aset E4, 10 sumber Git, 320 snapshot, 41 bahan laporan asli, 276 klip, dan 41 perbandingan reproduksi. Pemeriksaan ukuran/waktu modifikasi tidak menemukan perubahan pada file di luar cakupan revisi.
