# Rencana tabel 2.1 dan kecukupan referensi BAB II

Pemeriksaan 3 November 2026. Tabel pada `chapters/bab2.tex` masih **template kosong delapan baris**, sesuai permintaan kerangka saja. Isi perbandingan, angka hasil, dan sitasi tabel belum ditulis. Format garis mengikuti contoh pengguna: garis atas, pemisah header, dan garis bawah; tanpa garis vertikal atau antarbaris. Enam artikel jurnal tambahan telah diperoleh dan diverifikasi sebagaimana [audit pustaka](../../bibliography/PEMERIKSAAN_REFERENSI_2026-11-03.md).

## Jumlah yang disarankan

Untuk cakupan TA ini, delapan studi prioritas cukup sebagai rancangan awal tabel 2.1. Lima studi terdekat menjelaskan retrieval, representasi beku, derau, dan penerimaan; dua artikel menjadi asal model yang digunakan; satu studi memperluas pembahasan ketahanan terhadap latar yang heterogen. Angka delapan adalah pertimbangan relevansi untuk rancangan penulisan ini, bukan ketentuan jumlah minimum dari kampus. Tambahan hingga sekitar sepuluh dapat dipilih jika memberi pembanding yang belum terwakili.

Tidak semua referensi skripsi harus menjadi baris tabel penelitian terdahulu. Buku, artikel metode statistik, dokumentasi versi model, dan rujukan definisi lebih tepat digunakan pada 2.2 serta BAB III sesuai kegunaannya.

## Delapan studi prioritas

| Prioritas | Studi | Alasan dipilih dan batas penggunaannya |
|---|---|---|
| 1 | [Hamer dkk., BIRB, 2023](https://arxiv.org/abs/2312.07439v2) | Acuan tugas retrieval dan generalisasi bioakustik; preprint, bukan artikel jurnal. Metrik/protokolnya tidak disamakan dengan mAP@10 campuran aditif TA. |
| 2 | [Ghani dkk., 2023](https://doi.org/10.1038/s41598-023-49989-z) | Acuan embedding pralatih dan perbandingan representasi khusus burung dengan audio umum; eksperimennya klasifikasi transfer, bukan protokol retrieval bising TA. |
| 3 | [Ghaffari dan Devos, 2024](https://doi.org/10.1016/j.ecoinf.2024.102573) | Pembanding langsung untuk perhatian terhadap frontend dan ketahanan derau; tidak menganggap uji penambahan derau atau beberapa SNR sebagai metode baru TA. |
| 4 | [Clark dkk., 2023](https://doi.org/10.1016/j.ecoinf.2023.102065) | Komposisi soundscape dan kesalahan pengenalan; asosiasi dalam tugas klasifikasi dibedakan dari efek campuran terkontrol serta pola kegagalan retrieval TA. |
| 5 | [Fairbairn dkk., 2025](https://doi.org/10.1371/journal.pone.0330836) | Pengaruh pengaturan/ambang pada evaluasi BirdNET; confidence klasifikator berbeda dari ambang kemiripan kosinus TA. |
| 6 | [Kong dkk., PANNs, 2020](https://doi.org/10.1109/TASLP.2020.3030497) | Asal representasi audio umum yang dipakai; bukan kajian terbaru dan bukan eksperimen MFCC/BirdNET dengan derau ITERA. |
| 7 | [Kahl dkk., BirdNET, 2021](https://doi.org/10.1016/j.ecoinf.2021.101236) | Asal sistem khusus burung; uraian artikel 2021 dibedakan dari rincian checkpoint v2.4 pada TA. |
| 8 | [Lostanlen dkk., 2019](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0214168) | Ketahanan deteksi bioakustik terhadap variasi derau antarwaktu/sensor; berguna untuk membahas latar heterogen, dengan perbedaan tugas deteksi dan retrieval. PDF sudah tersedia lokal, belum masuk sepuluh entri BibTeX BAB I. |

Pada pemeriksaan awal, tujuh dari delapan studi di atas sudah ada pada sepuluh entri BibTeX BAB I. Lostanlen kini juga disiapkan pada BibTeX dari PDF koleksi lama. Stowell (2022), Ningrum dkk. (2026), dan BirdSet (2025) tetap berguna sebagai konteks/tinjauan, contoh Indonesia, serta dataset/benchmark; tidak wajib dipaksakan menjadi tiga baris tambahan pada tabel pembanding utama.

## Bentuk tabel

Kolom: **No. | Peneliti dan tahun | Data penelitian | Metode dan evaluasi | Temuan utama | Relevansi dan pembeda**. Kolom data menyebut dataset dan cakupan data sumber; jenis tugas dijelaskan bersama metode/evaluasi bila diperlukan.

Saat diisi, kolom peneliti memuat sitasi yang terhubung ke `references.bib`. Temuan mencantumkan kondisi dan metrik yang relevan; jika menggunakan angka, asal tabel/halaman perlu ditelusuri. Nilai akurasi klasifikasi, F1 deteksi, ROC AUC, dan mAP tidak digunakan untuk membuat peringkat lintas artikel dengan protokol berbeda. Kolom terakhir menerangkan kaitan spesifik dan pembeda TA, bukan menyatakan setiap artikel memiliki kelemahan atau bahwa belum ada penelitian lain yang pernah menguji derau.

## Apakah sumber kita kurang?

Hasil inventaris saat pemeriksaan:

- `references.bib`: 17 entri, terdiri atas 15 artikel jurnal, 1 prosiding, dan 1 preprint. Sepuluh sumber sudah dikutip pada BAB I; tujuh lainnya disiapkan untuk BAB II dan belum dipaksakan muncul di daftar pustaka tercetak.
- `paper/bibliography/referensi_jurnal_modern.csv`: 34 entri; Excel telah dicocokkan seluruh selnya.
- `paper/bibliography/`: 32 PDF. Dua entri lama belum mempunyai PDF penuh, sebagaimana audit koleksi sebelumnya.

Jadi koleksi tidak hanya sepuluh sumber. Jumlah bahan awal cukup untuk menyusun pembanding 2.1, tetapi cakupan rujukan pada BibTeX belum lengkap untuk seluruh dasar teori 2.2. Penambahan dilakukan untuk mengisi kebutuhan tertentu, bukan mengejar jumlah jurnal.

### Bahan relevan yang sudah tersedia lokal

- **Hassanzad dan Hajian-Tilaki (2024):** ROC dan pemilihan cutoff, termasuk Youden. Konteks aslinya biomarker klinis; dipakai untuk dasar statistik, bukan bukti ketahanan threshold audio.
- **Vaze dkk. (ICLR 2022):** konsep open-set dan pemisahan kinerja kelas dikenal/penolakan; konteks citra dan skor logit tidak disamakan dengan kontrol unknown serta kosinus pada TA.
- **Salamon dkk., Scaper (2017):** sintesis/pencampuran dan pengaturan SNR; TA memakai mixer sendiri, tidak mengklaim menjalankan Scaper.
- **Lostanlen dkk. (2019):** ketahanan terhadap latar heterogen, juga diprioritaskan untuk 2.1.

### Rujukan dasar yang telah ditambahkan untuk penulisan 2.2

1. **MFCC dan pengolahan sinyal:** [Davis dan Mermelstein (1980)](https://doi.org/10.1109/TASSP.1980.1163420), disertai rujukan pengolahan sinyal/audio untuk sampling, STFT, RMS, dan spektrum sesuai pembahasan yang benar-benar ditulis. Artikel MFCC tidak menjadi satu-satunya sumber seluruh teori audio.
2. **Ruang vektor dan evaluasi retrieval:** [Salton dkk. (1975)](https://doi.org/10.1145/361219.361220) dan [Moffat (2022)](https://doi.org/10.1109/ACCESS.2022.3211668) telah diunduh. PDF Moffat adalah naskah penulis arXiv v1, sedangkan publikasi jurnalnya diverifikasi terpisah. Buku Manning dkk. tetap calon pendamping, bukan PDF jurnal yang ditambahkan sekarang. Rumus AP terpotong harus sesuai penyebut implementasi TA.
3. **Bootstrap dan ketidakpastian:** [Efron (1979)](https://doi.org/10.1214/aos/1176344552) sebagai dasar resampling, dengan uraian unit sampling berpasangan yang sesuai analisis penelitian. Konsep bootstrap tidak dengan sendirinya mengesahkan setiap pilihan pengujian/interval dalam kode.
4. **Ciri spektral:** artikel jurnal [Peeters dkk. (2011), The Timbre Toolbox](https://doi.org/10.1121/1.3642604) telah diunduh dari laboratorium penulis sebagai landasan deskriptor audio. Laporan CUIDADO 2004 tidak ditambahkan sebagai artikel jurnal. Definisi akhir dicocokkan dengan implementasi yang dipakai.

Empat kelompok tersebut merupakan prioritas kebutuhan teori, bukan kuota jurnal. Davis, Efron, Peeters, Salton, dan Moffat sudah masuk koleksi dan BibTeX. Artikel jurnal van Merrienboer (2024) juga ditambahkan sebagai pendamping generalisasi bioakustik. Penulisan isi dan pemilihan sitasi tepat per definisi masih dilakukan pada tahap berikutnya; template kosong tidak diisi dengan klaim atau angka sementara.

## Kandidat perluasan kajian yang sudah ditelusuri

[Miron dkk. (2025), What Matters for Bioacoustic Encoding, arXiv:2508.11845v1](https://arxiv.org/html/2508.11845v1), relevan untuk memperbarui pembahasan representasi: bagian 3.3 menggunakan augmentasi derau saat pelatihan, sedangkan 3.4 mengevaluasi retrieval berdasarkan kosinus. Keduanya dibedakan dari pengujian kueri berpasangan dengan derau ITERA pada model beku. Sumber ini kandidat baris tambahan, belum termasuk delapan baris prioritas dan belum ditambahkan ke BibTeX. Status sumber yang ditelaah adalah preprint v1, bukan otomatis jurnal.

[van Merrienboer dkk. (2024), Birds, bats and beyond](https://www.frontiersin.org/journals/bird-science/articles/10.3389/fbirs.2024.1369756/full) telah diunduh dari penerbit dan ditambahkan ke CSV/Excel serta BibTeX. Artikel bertipe Review ini merupakan pendamping evaluasi generalisasi/BIRB; judul, penulis, dan isi berbeda dari preprint Hamer. Keduanya tidak otomatis dihitung sebagai dua pembanding independen untuk memperbesar tabel.
