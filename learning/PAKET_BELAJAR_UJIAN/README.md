# Mulai belajar penelitian Anda dari sini

Disiapkan untuk Fabio, **27 Oktober 2026**. Bahasa dalam paket ini dibuat untuk belajar dan latihan menjawab. Rumusan sederhana adalah usulan bahasa penjelasan; persetujuan rumusan resmi tetap melalui pembimbing. Angka hasil mengacu pada artefak aktif lokal, bukan hasil eksperimen baru.

**Untuk dibaca atau dicetak sekaligus:** [PDF gabungan enam bacaan](output/pdf/PANDUAN_BELAJAR_DAN_HITUNGAN_TA.pdf).

## Urutan membaca

| Urutan | Berkas | Setelah membaca, Anda seharusnya bisa… |
|---|---|---|
| 1 | [Cerita penelitian dan rancangan](01_PENELITIAN_DAN_RANCANGAN.md) | Menceritakan masalah, manfaat, gap, kontribusi, data, variabel, serta E0–E5. |
| 2 | [Teori dengan bahasa sederhana](02_TEORI_DAN_ALUR_METODE.md) | Menjelaskan embedding, MFCC, model, SNR, spektrum, dan alur pencarian. |
| 3 | [Hitungan langkah demi langkah](03_PERHITUNGAN_LANGKAH_DEMI_LANGKAH.md) | Menghitung cosine, SNR, AP/mAP, Recall, threshold, dan ayunan H3. |
| 4 | [Hasil dan latihan jawaban lisan](04_HASIL_DAN_JAWABAN_UJIAN.md) | Menyebut hasil beserta batas kesimpulannya. |
| 5 | [Latihan mandiri dan kunci](05_LATIHAN_DAN_KUNCI.md) | Mengerjakan perhitungan tanpa melihat contoh terlebih dahulu. |
| 6 | [Peta bacaan jurnal dan bukti](06_PETA_BACAAN_DAN_SUMBER.md) | Memilih jurnal yang perlu dibaca dan menemukan sumber setiap angka penting. |

Sediakan sekitar 45–60 menit per sesi. Baca satu berkas, tutup, lalu jelaskan kembali dengan suara sendiri selama 2–3 menit. Waktu belajar ini saran, bukan syarat penelitian. Jika satu rumus belum dipahami, ulangi contohnya dengan kalkulator sebelum lanjut.

**Target minimum sebelum bimbingan:** bisa menjelaskan penelitian dalam satu menit; membedakan retrieval dan klasifikasi; menyebut asal data; menjelaskan E0–E5; menghitung AP@10, Recall@10 dan retensi; menjelaskan H3 relatif vs absolut; menyebut keterbatasan dan status audit E5 dengan jujur.

## Apa yang sudah diperiksa untuk paket ini?

- Jumlah data dihitung ulang dari manifes: 673 galeri + 311 kueri + 232 kalibrasi = 1.216 rekaman target; 20 spesies.
- Batas Recall@10 dihitung ulang dari jumlah galeri relevan setiap kueri: **0,363997**, dengan bobot 311 kueri.
- Contoh retrieval diperiksa menggunakan fungsi aktual `src/retrieve.py`: P@10 = 0,30; R@10 = 0,15; AP@10 = 0,241667.
- Rumus threshold dibandingkan dengan kode aktual; contoh kecil memiliki τ = 0,70 dan Youden J = 0,75.
- Angka E1–E3 dan H3 disalin dari tabel aktif yang ditautkan pada bacaan keenam. Tidak ada inferensi audio atau pengulangan E4 dalam penyusunan paket.

Paket ini melengkapi [panduan bahasa sehari-hari yang sudah ada](../PANDUAN_PENELITIAN_BAHASA_SEHARI_HARI.md). Catatan belajar tidak menggantikan naskah, tabel mentah, atau pengesahan dosen.

## Berkas yang perlu dibawa saat bimbingan

1. Ringkasan hasil pada berkas 04.
2. Contoh hitungan AP@10, batas Recall@10, dan H3 pada berkas 03.
3. Daftar pertanyaan yang Anda belum kuasai dari berkas 05.
4. [Status hasil audit pendengaran 30 Oktober](../../Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md): catatan tersedia untuk 120/120 kasus oleh satu pendengar. `CURRENT_STATUS.md` 18 Oktober tetap riwayat dan masih menyebut status audit lama; gunakan laporan hasil saat membahas progres terbaru.

**Jangan menghafal angka tanpa memahami penyebutnya.** Contohnya, 81,67% Top-1, 0,6367 mAP@10, 23,31% Recall@10, dan 60,45% recall penerimaan open-set mengukur hal yang berbeda.
