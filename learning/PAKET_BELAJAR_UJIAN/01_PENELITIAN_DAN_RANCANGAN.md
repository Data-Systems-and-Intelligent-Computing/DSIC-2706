# 1. Cerita penelitian dan rancangan

## Penjelasan satu menit

“Saya meneliti pencarian rekaman suara burung. Kita memasukkan satu contoh suara, lalu komputer mencari rekaman dengan jenis burung yang sama dari koleksi pembanding. Masalahnya, suara di lapangan sering bercampur gangguan. Saya membandingkan MFCC, PANNs, dan BirdNET untuk melihat pencarian mana yang paling bertahan ketika contoh suaranya dicampur derau lingkungan ITERA pada beberapa tingkat kebisingan. Saya juga memeriksa penolakan suara di luar jenis target, pengaruh lima lokasi sumber derau, dan contoh kegagalannya. Model dipakai tanpa dilatih ulang. Hasilnya berlaku untuk pencampuran yang diuji, dan belum membuktikan kinerja pada semua rekaman burung langsung di lapangan.”

## Masalah umum, masalah khusus, dan manfaat

**Masalah umum:** pemantauan keanekaragaman hayati membutuhkan pengamatan berulang. Mengandalkan orang yang selalu hadir di semua lokasi membutuhkan waktu dan keahlian. Burung dapat menjadi salah satu kelompok yang diamati melalui suara, tetapi rekaman saja belum otomatis memberi informasi yang benar.

**Masalah khusus:** pencarian contoh rekaman burung dapat terganggu oleh suara lingkungan. Metode yang baik pada rekaman relatif bersih belum tentu tetap baik ketika kueri bising. Sistem juga perlu menangani suara yang jenisnya tidak ada dalam koleksi target, agar tidak selalu memaksakan kecocokan.

**Manfaat umum:** mendukung pemilihan alat bantu penelusuran rekaman untuk pemantauan lingkungan, pendidikan, pengelolaan koleksi audio, dan pekerjaan peneliti. Manfaat sehari-harinya bersifat tidak langsung: mempermudah pekerjaan manusia yang mempelajari lingkungan dan habitat.

**Manfaat khusus TA:** menyediakan bukti perbandingan cara merangkum audio, data tentang penurunan pencarian akibat derau, batas ambang penolakan, serta contoh kegagalan yang bisa diperiksa. Hasil ini membantu memilih metode dan mengetahui kapan hasilnya perlu diperiksa manusia. TA belum mengukur dampak pada kebijakan konservasi, peningkatan populasi burung, atau penghematan biaya operasional.

## Tujuan dan bentuk hasil akhir

Tujuannya **mengevaluasi ketahanan representasi audio untuk retrieval suara burung terhadap derau**. Representasi adalah cara mengubah suara menjadi angka. Retrieval adalah pencarian rekaman dari koleksi. Ketahanan dinilai melalui perubahan kualitas hasil pencarian.

Hasil akhirnya berupa protokol yang dapat ditelusuri, data dan pembagian yang terdokumentasi, kode ekstraksi dan evaluasi, tabel/gambar perbandingan, analisis kegagalan, serta penjelasan batas kesimpulan. Model yang unggul dapat direkomendasikan **di dalam kondisi uji**, tanpa menganggapnya pasti unggul pada semua tugas audio.

## Rumusan masalah dengan kata “bagaimana”

Berikut bahasa sederhana untuk didiskusikan dengan pembimbing; dokumen RQ resmi tidak diubah oleh paket ini.

**RQ utama:** Bagaimana perbandingan ketahanan MFCC, PANNs, dan BirdNET dalam mencari rekaman burung sejenis ketika suara contoh dicampur derau lingkungan ITERA dengan tingkat kebisingan yang berbeda?

1. **Sub-RQ 1 / E2:** Bagaimana perubahan kualitas pencarian setiap representasi pada SNR +20, +10, 0, dan −5 dB dibandingkan kondisi bersih?
2. **Sub-RQ 2 / E3:** Bagaimana perubahan kemampuan menerima suara target dan menolak suara di luar target ketika ambang dari data kalibrasi bersih digunakan pada suara bising?
3. **Sub-RQ 3 / E4:** Bagaimana perbedaan kualitas dan kestabilan pencarian ketika sumber derau berasal dari lima lokasi ITERA pada SNR terkontrol?
4. **Sub-RQ 4 / E5:** Bagaimana bentuk kegagalan pencarian dan kaitannya dengan margin skor serta ciri akustik yang tersedia?

“Kaitan” pada Sub-RQ 4 berarti pola hubungan yang diamati. Menyimpulkan suatu ciri sebagai penyebab kegagalan memerlukan pengujian tambahan.

## Hipotesis: dugaan yang diperiksa

| Kode | Arti sederhana | Cara membaca statusnya |
|---|---|---|
| H1 | Representasi deep mempertahankan proporsi kualitas lebih baik daripada MFCC saat diberi derau. | Didukung dalam pengujian aktif; lihat hasil retensi E2. |
| H2 | Representasi khusus bioakustik mempertahankan proporsi kualitas lebih baik daripada representasi audio generik. | R2 dibandingkan dengan R1 dalam campuran yang diuji. |
| H3 | Kestabilan lintas sumber derau berbeda antara R1 dan R2. | Rumusan berubah setelah hasil tersedia; analisis eksploratif. Laporkan ayunan absolut dan relatif. |
| H4 | Ambang bersih berubah perilakunya saat diterapkan pada kueri bising. | Pelaporan reformulasi eksploratif. Recall turun; false-accept rate tidak meningkat pada hasil yang dilaporkan. |
| H5 | Representasi audio menghasilkan pencarian bersih lebih baik daripada kontrol acak R3. | Memeriksa apakah hasil membawa informasi audio yang berguna. |

H3 awal membahas perbedaan rekaman burung lapangan alami dengan campuran terkontrol. Hal tersebut **belum diuji**. Riwayat H3/H4 ada dalam `docs/research/hypotheses.md`: rumusan awal 6 September 2026; perubahan tercatat 12 Oktober; perluasan pelaporan H3 pada 15 Oktober. Jangan menyebut rumusan pascahasil sebagai prediksi yang dibekukan sejak awal.

## Data yang benar-benar dipakai

| Bagian | Jumlah | Fungsi |
|---|---:|---|
| Spesies target | 20 | Jenis burung yang mempunyai contoh dalam galeri. |
| Rekaman target Xeno-Canto | 1.216 | Sumber audio burung target. |
| Galeri | 673 | Koleksi pembanding yang dicari. |
| Kueri bersih | 311 | Contoh suara untuk pengujian retrieval. |
| Kalibrasi target | 232 | Memilih ambang, terpisah dari kueri uji. |
| Bank derau AudioMoth ITERA | 1.799 | Sumber fisik gangguan lingkungan. |
| Derau untuk pencampuran | 1.528 | Sumber campuran E2/E4. |
| Derau khusus kontrol unknown | 271 | Dipisahkan dari derau pencampuran. |
| Kontrol burung non-target | 272 | Burung di luar 20 spesies target. |
| Total kontrol unknown | 543 | 272 burung non-target + 271 derau; dibagi 233 kalibrasi dan 310 uji. |

Pembagian target memperhatikan identitas rekaman, jalur berkas, dan perekam. Tujuannya mencegah hasil terlihat bagus karena informasi terlalu mirip bocor antarpembagian. Ini tidak menjamin tidak ada kemiripan ekologis atau tumpang tindih data pralatih model dengan sumber internet.

Lima sumber derau E4: Kebun Raya, Embung F, Gedung F, Masjid At Tanwir, dan sekitar GKU 1. Bank berisi **enam kategori konfigurasi AudioMoth**: Amplitude/Frequency × Low/Medium/High. Enam kategori konfigurasi tidak otomatis berarti enam unit perangkat.

## Variabel penelitian

| Kelompok | Yang dimaksud dalam TA |
|---|---|
| Variabel yang dibandingkan | R0/R1/R2; R3 sebagai kontrol; SNR; lokasi derau pada E4. |
| Hasil yang diukur | mAP@10 utama, Top-1, Recall@10, Precision@10, retensi; metrik penerimaan/penolakan E3; ayunan E4; diagnosis E5. |
| Yang dikendalikan | Galeri, daftar kueri, label relevansi spesies, potongan dan prosedur audio, aturan pencampuran, ambang beku, dan penggunaan model tanpa fine-tuning. |
| Ulangan E4 | Empat ulangan pencampuran untuk setiap kombinasi kueri–lokasi–SNR. |

Kesamaan protokol tidak membuat arsitektur, data pralatih, kapasitas, dan dimensi model menjadi sama. Karena itu selisih hasil tidak membuktikan satu faktor arsitektur sebagai penyebab tunggal.

## E0 sampai E5 untuk apa?

| Eksperimen | Pertanyaan praktis | Hasil yang diperlukan |
|---|---|---|
| E0 | Apakah jalur pemrosesan dapat berjalan pada uji awal terbatas? | Pemeriksaan teknis awal; bukan hasil utama untuk semua data. |
| E1 | Seberapa baik pencarian sebelum gangguan tambahan? | Acuan bersih untuk membandingkan representasi dan menghitung retensi. |
| E2 | Apa yang terjadi ketika kueri diberi gangguan makin kuat? | Hasil pada empat SNR dengan galeri tetap bersih. |
| E3 | Bagaimana sistem menerima target dan menolak unknown dengan ambang yang sudah dipilih? | Ambang kalibrasi, recall penerimaan known, FPR unknown, AUROC, dan F1. |
| E4 | Bagaimana hasil berubah jika sumber derau berasal dari lima lokasi berbeda? | 311 × 5 × 4 × 4 = 24.880 baris per representasi; 99.520 baris untuk empat representasi. Ini baris evaluasi, bukan 99.520 rekaman burung independen. |
| E5 | Ketika gagal, kegagalannya seperti apa? | Diagnosis komputasional dan 120 kasus pilihan untuk pemeriksaan pendengaran. |

E4 sudah selesai dan tidak perlu dijalankan ulang menurut arahan pembimbing. Analisis subset lokasi memakai hasil tersimpan.

## Gap dan kontribusi yang aman dinyatakan

Artikel yang dikaji mencakup klasifikasi burung, embedding, benchmark generalisasi, derau, dan open-set. Jadi jangan mengatakan “penelitian suara burung dengan derau belum pernah ada”. Gap yang dapat dirumuskan adalah **belum terjawabnya perbandingan pada kombinasi protokol spesifik TA**: representasi frozen MFCC/PANNs/BirdNET, retrieval spesies Indonesia dengan galeri tetap, derau fisik ITERA terkontrol, transfer ambang bersih, serta sensitivitas lima sumber lokasi.

Kontribusi Anda adalah **bukti evaluasi dan artefak yang dapat ditelusuri untuk kombinasi tersebut**, termasuk perbandingan absolut–relatif H3 dan diagnosis kegagalan. Ini klaim kontribusi kontekstual/metodologis, dengan batas berdasarkan pustaka yang telah dikaji. Klaim “pertama di dunia” membutuhkan penelusuran literatur yang jauh lebih luas dan tidak didukung oleh paket ini.

## Batas penelitian yang harus disebut

Model tidak dilatih ulang; hanya checkpoint tertentu yang diuji. Burung target berasal dari Xeno-Canto dan campurannya dibuat di komputer. Derau berasal dari ITERA, tetapi kinerja pada burung target yang direkam alami di ITERA belum dibuktikan. Lokasi dan segmen gangguan terbatas. R3 merupakan kontrol berbasis ID. Audit pendengaran manusia 120 kasus harus dibuktikan dengan catatan; status pribadi terbaru perlu dicocokkan dengan ekspor yang sah. Penelitian belum membuktikan penyebab berupa serangga, distorsi frekuensi, atau perubahan ekologis.

Sumber utama: manifes dan dokumen ruang lingkup; tautan lengkap pada [peta sumber](06_PETA_BACAAN_DAN_SUMBER.md).
