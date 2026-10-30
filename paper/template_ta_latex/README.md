# Template TA LaTeX sampai Bab III

Kerangka ini mengikuti **urutan halaman dan gaya umum** contoh TA pada [Repository ITERA](https://repo.itera.ac.id/depan/submission/SB2604150015). Teks penelitian, judul, identitas, abstrak, dan isi tiap bab tidak disalin. Format ini merupakan rekonstruksi dari contoh yang terlihat, bukan klaim sebagai template resmi fakultas.

- `main.tex`: ukuran halaman, margin, cover, halaman awal, daftar otomatis, serta makro identitas dan judul kerja.
- `chapters/bab1.tex`: Pendahuluan.
- `chapters/bab2.tex`: Tinjauan Pustaka; topik teori sengaja masih placeholder.
- `chapters/bab3.tex`: Metodologi Penelitian.

**Status lokal 30 Oktober 2026:** `main.tex` sudah memakai XeLaTeX, `fontspec`, Times New Roman, makro identitas, judul kerja penelitian, dan pemanggilan logo jika berkas tersedia. Periksa kembali nilai identitas/judul sebelum digunakan. Berkas `chapters/bab1.tex` sampai `bab3.tex` masih kerangka berkomentar; pembaruan README tidak mengisi atau mengubah bab tersebut.

Halaman pengesahan dan pernyataan masih menunggu redaksi resmi ITERA. Daftar pustaka serta Bab IV dan seterusnya belum dibuat sesuai permintaan. Sumber LaTeX dan aset template masih lokal pada pemeriksaan ini; publikasi README tidak berarti seluruh proyek LaTeX telah tersedia di GitHub.

Di Antigravity dengan LaTeX Workshop/MiKTeX, buka `main.tex` sebagai dokumen utama dan gunakan XeLaTeX. Pembaruan dokumentasi ini tidak menjalankan kompilasi. Periksa aturan fakultas, sistematika, sitasi, dan persetujuan pembimbing sebelum memakai format sebagai naskah final. [Paket bahan BAB 1–3](../persiapan_bab1_3/README.md) menyediakan diagram alir dan indeks gambar/tabel.
