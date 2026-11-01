# 4. Hasil dan latihan jawaban ujian

Angka berikut adalah hasil TA aktif. Contoh jawaban boleh disesuaikan dengan cara bicara Anda. Jangan menghafal jawaban yang belum dapat Anda jelaskan dengan contoh sendiri.

## Angka utama yang perlu dikuasai

| Representasi | E1 mAP@10 bersih | E1 Top-1 | E2 mAP@10 −5 dB | Retensi −5 dB |
|---|---:|---:|---:|---:|
| R0 MFCC | 0,069393 | 18,33% | 0,023210 | 33,45% |
| R1 PANNs | 0,176268 | 37,62% | 0,086306 | 48,96% |
| R2 BirdNET | 0,636709 | 81,67% | 0,483160 | 75,88% |
| R3 kontrol ID | 0,021141 | 6,43% | 0,021141 | 100,00% |

R2 memiliki hasil retrieval tertinggi di kondisi E2 yang diuji. Namun retensi R3 100% tidak menunjukkan kontrol itu memahami suara: embedding-nya ditentukan ID dan tidak berubah saat audio diberi derau. Karena itu retensi harus dibaca bersama kualitas absolut dan sifat kontrol.

**E3 R2, tau beku 0,702785:** recall penerimaan known turun dari **60,45% ke 25,40%**; FPR unknown turun dari **22,26% ke 12,90%**, dari kondisi bersih ke −5 dB. AUROC berubah dari 0,758936 menjadi 0,599409. Jadi hasil tidak mendukung cerita bahwa semua jenis kesalahan memburuk dengan cara yang sama. Sistem semakin sering menolak target; penurunan FPR saja belum berarti sistem secara keseluruhan membaik.

**H3:** ayunan relatif rata-rata R2 lebih kecil pada lima sumber lokasi. Perbedaan absolut rata-ratanya belum meyakinkan menurut CI, dan pada −5 dB ayunan absolut R2 justru lebih besar. Tanpa Kebun Raya, selisih relatif rata-rata mengecil. Analisis membuang satu lokasi secara bergantian juga sudah tersedia pada artefak 18 Oktober; E4 tidak dijalankan ulang untuk itu.

**E5:** 120 kasus pilihan telah disiapkan untuk audit; ada 117 pasangan kueri–kondisi unik dan 80 kueri unik dalam metadata paket. Jadi 120 baris tidak sama dengan 120 rekaman sumber independen. Metadata persiapan mencatat nol ulasan manusia saat paket dibuat; angka itu tidak dapat memastikan progres pribadi Anda sekarang. Penyelesaian audit harus dibuktikan dengan catatan ekspor terbaru yang valid.

## Latihan pertanyaan dosen

### 1. Penelitian Anda tentang apa?

“Saya membandingkan ketahanan beberapa cara merangkum suara untuk mencari rekaman burung sejenis ketika contoh suaranya diberi gangguan lingkungan. Saya juga menguji penolakan suara di luar target dan memeriksa contoh kegagalan.”

### 2. Mengapa suara burung perlu diteliti?

“Suara dapat membantu pemantauan burung tanpa pengamat selalu hadir. Tetapi rekaman yang banyak masih perlu ditelusuri dan diperiksa. Penelitian saya membantu mengetahui representasi mana yang cocok dan batasnya ketika rekaman bising.”

### 3. Apa masalah paling spesifik yang Anda jawab?

“Bagaimana kualitas pencarian berubah ketika kueri burung Indonesia dicampur derau fisik ITERA pada SNR tertentu, serta bagaimana ranking dan penolakan unknown bereaksi.”

### 4. Mengapa tidak langsung pakai keluaran label BirdNET?

“Tugas saya retrieval. Saya mengambil embedding untuk membandingkan kueri dengan galeri milik penelitian. Dengan cara ini, MFCC, PANNs, dan BirdNET sama-sama dinilai melalui pencarian berbasis cosine. Saya belum membandingkan secara langsung dengan klasifikasi label bawaan BirdNET.”

### 5. Apa kontribusi baru Anda?

“Kontribusi saya berupa bukti evaluasi dalam protokol spesifik: tiga representasi frozen untuk retrieval 20 spesies Indonesia, campuran derau fisik ITERA, ambang kalibrasi yang dibekukan, sensitivitas lima sumber lokasi, dan diagnosis kegagalan. Kebaruannya ada pada kombinasi evaluasi dan artefaknya; saya tidak mengklaim membuat arsitektur baru atau menjadi yang pertama di dunia.”

### 6. Apa gap dari penelitian sebelumnya?

“Bacaan yang dikaji membahas bagian-bagian seperti klasifikasi burung, embedding, derau, dan generalisasi. Hasilnya belum langsung menjawab perbandingan pada data dan protokol TA saya. Karena itu saya menguji kombinasi tersebut secara terkontrol. Saya tidak mengatakan seluruh topik derau burung belum pernah diteliti.”

### 7. Mengapa memakai tiga representasi tersebut?

“MFCC mewakili fitur klasik, PANNs mewakili pembelajaran audio umum, dan BirdNET mewakili domain burung. R3 menjadi kontrol tanpa informasi audio. Saya ingin mengetahui perbedaan hasil ketiga kategori ini pada kondisi yang sama.”

### 8. Apakah bobot model Anda dilatih lagi?

“Tidak. Model pretrained digunakan frozen. Yang disiapkan adalah klip, embedding, pencarian, pencampuran derau, dan ambang. Kalibrasi ambang mengubah aturan penerimaan, bukan bobot jaringan.”

### 9. Apakah 1.216 rekaman semuanya menjadi data uji?

“Tidak. Ada 673 rekaman galeri, 311 kueri uji, dan 232 kalibrasi target. Kalibrasi dipisahkan agar pemilihan ambang tidak memakai kueri uji.”

### 10. Apakah data burungnya direkam langsung di ITERA?

“Burung target berasal dari Xeno-Canto Indonesia. Derau lingkungan berasal dari rekaman AudioMoth ITERA. Keduanya dicampur di komputer. Saya belum membuktikan performa pada korpus burung target yang direkam alami di ITERA.”

### 11. Mengapa memilih lima detik?

“Lima detik adalah panjang klip operasional agar masukan konsisten dan komputasi dapat ditangani. Saya tidak melakukan pencarian durasi terbaik. BirdNET kemudian memakai jendela internal tiga detik sesuai adapter. Jadi saya tidak mengklaim lima detik optimal bagi semua spesies.”

### 12. Mengapa sampai −5 dB?

“Agar ada kondisi ketika daya derau lebih besar daripada daya target. Pada −5 dB, daya derau sekitar 3,162 kali target. Rentang empat SNR memberi beberapa tingkat gangguan, bukan mewakili semua kondisi lapangan.”

### 13. Mengapa memakai mAP@10 sebagai hasil utama?

“Saya ingin menilai kualitas sepuluh hasil pencarian, termasuk posisi hasil yang benar. Top-1 hanya melihat urutan pertama, sedangkan AP memberi nilai lebih baik ketika hasil relevan muncul lebih awal. mAP merata-ratakan AP seluruh kueri.”

### 14. Mengapa Recall@10 hanya 23,31% padahal Top-1 81,67%?

“Penyebutnya berbeda. Top-1 menghitung berapa kueri yang hasil pertamanya benar. Recall@10 membagi temuan benar di sepuluh hasil dengan semua rekaman relevan di galeri. Jika satu spesies punya 50 contoh galeri, paling banyak sepuluh ditemukan sehingga batas recall-nya 20%. Batas rata-rata berbobot kueri pada galeri TA adalah 36,40%.”

### 15. Bagaimana memilih ambang 0,7028?

“Dari skor kalibrasi R2 untuk known dan unknown, saya memilih kandidat yang memaksimalkan Youden J, yaitu TPR dikurangi FPR. Ambang lalu dibekukan sebelum evaluasi uji. Angka tersebut milik ruang skor R2 dan tidak bisa dianggap cocok untuk semua representasi.”

### 16. Kalau skor melewati ambang, apakah spesies pasti benar?

“Tidak pasti. Ambang memutuskan menerima atau menolak berdasarkan skor terbesar. Hasil teratas tetap bisa salah spesies. Karena itu saya juga mengukur ranking dan membedakan jenis kegagalan pada E5.”

### 17. Bagaimana menjelaskan relatif dan absolut H3 secara lisan?

“Absolut melihat selisih mAP antarlokasi apa adanya. Relatif membagi selisih itu dengan hasil bersih modelnya. Acuan bersih R1 dan R2 berbeda jauh sehingga kesan kestabilannya dapat berubah. Di data saya, keunggulan relatif R2 lebih jelas daripada keunggulan absolut rata-ratanya. Karena itu saya harus melaporkan keduanya.”

### 18. Apakah Kebun Raya menjadi penyebab perbedaan model?

“Analisis tanpa Kebun Raya menunjukkan selisih relatif rata-rata mengecil. Itu berarti kesimpulan sensitif terhadap komposisi lokasi. Ini belum membuktikan sebab biologisnya. Menghapus satu lokasi juga mengurangi jumlah pembanding, dan dugaan serangga atau frekuensi belum diuji sebagai penyebab.”

### 19. Apa maksud H3 dan H4 eksploratif?

“Rumusan/pelaporannya diperbarui setelah hasil tersedia. Analisis itu tetap berguna untuk memahami data, tetapi tidak boleh diceritakan seolah-olah semua dugaan sudah ditetapkan sebelum melihat hasil. Saya menyertakan riwayat rumusan dan tanggalnya.”

### 20. Siapa yang mendengarkan E5 dan bagaimana?

“Saya sebagai peneliti dapat melakukan audit pendengaran, atau orang lain yang benar-benar mendengarkan dan identitas/perannya dicatat. Saya memakai klip yang sesuai segmen dan campuran eksperimen, membandingkan suara bersih, bising, serta hasil galeri yang tersedia, lalu menulis pendengar, tanggal, dan observasi per kasus. Jika ragu tentang spesies, saya tulis ragu dan meminta bantuan ahli. Diagnosis otomatis atau jawaban AI tidak menggantikan catatan pendengaran manusia.”

### 21. Apakah audit 120 kasus membuktikan frekuensi gagal pada populasi?

“Tidak. Kasus dipilih untuk diagnosis menurut kelompok kegagalan. Proporsi di dalam pilihan itu tidak otomatis menjadi proporsi semua kueri atau suara lapangan. Frekuensi keseluruhan harus dihitung dari seluruh keluaran yang sesuai.”

### 22. Apa arti total retrieval collapse di kode?

“Itu label operasional untuk hasil teratas salah dan skor maksimum di bawah ambang. Nama itu tidak otomatis membuktikan sepuluh hasil semuanya salah. Saya harus memeriksa ranking jika ingin membuat klaim tentang sepuluh hasil.”

### 23. Apakah eksperimen sudah dapat direproduksi?

“Ada bukti reproduksi terpisah pada komputer yang sama dengan lingkungan Python baru dan input lokal terverifikasi. Laporan mencatat 41 perbandingan cocok. Ruang lingkupnya tidak mencakup inferensi E4 ulang atau unduh audio ulang, sehingga saya menjelaskan batas reproduksi tersebut.”

### 24. Apa yang masih perlu dilakukan sebelum skripsi final?

“Memastikan audit pendengaran dan bukti ekspornya selesai, mengonfirmasi rumusan/judul serta izin mulai BAB 1–3 kepada pembimbing sesuai alur bimbingan, memastikan seluruh klaim naskah cocok dengan artefak aktif, dan memakai referensi yang sudah dibaca. Dua PDF pustaka belum tersedia penuh dan tidak boleh diberi ringkasan detail yang belum diperiksa.”

## Kalimat yang perlu dihindari

| Terlalu jauh dari bukti | Penjelasan yang lebih tepat |
|---|---|
| “BirdNET pasti terbaik di semua lapangan.” | “R2 terbaik untuk retrieval pada kondisi campuran yang diuji.” |
| “Semua performa selalu turun setiap SNR turun.” | “Ada tren penurunan, tetapi kondisi ringan tertentu dapat melebihi acuan bersih.” |
| “R2 paling stabil di semua kondisi.” | “Kesimpulan stabilitas bergantung pada ukuran, SNR, dan subset lokasi.” |
| “99 ribu data burung baru.” | “99.520 baris evaluasi E4 untuk empat representasi.” |
| “FPR turun, berarti open-set membaik.” | “FPR turun bersama recall penerimaan target; keduanya harus dibaca.” |
| “Semua 120 kasus sudah didengar oleh sistem.” | “Diagnosis otomatis tersedia; audit manusia memerlukan catatan pendengar yang nyata.” |

Sumber angka dan batas pelaporan ada pada [peta sumber](06_PETA_BACAAN_DAN_SUMBER.md).
