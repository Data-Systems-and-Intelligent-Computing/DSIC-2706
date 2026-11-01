# Template TA LaTeX sampai Bab III

Kerangka ini mengikuti **urutan halaman dan gaya umum** contoh TA pada [Repository ITERA](https://repo.itera.ac.id/depan/submission/SB2604150015). Teks penelitian, judul, identitas, abstrak, dan isi tiap bab tidak disalin. Format ini merupakan rekonstruksi dari contoh yang terlihat, bukan klaim sebagai template resmi fakultas.

- `main.tex`: ukuran halaman, margin, cover, halaman awal, daftar otomatis, serta makro identitas dan judul kerja.
- `chapters/bab1.tex`: Pendahuluan.
- `chapters/bab2.tex`: Tinjauan Pustaka; topik teori sengaja masih placeholder.
- `chapters/bab3.tex`: Metodologi Penelitian.

**Status lokal 31 Oktober 2026:** `main.tex` memakai XeLaTeX, `fontspec`, Times New Roman, makro identitas, judul kerja penelitian, dan pemanggilan logo jika berkas tersedia. Draf Latar Belakang, lima Rumusan Masalah, lima Tujuan yang berpadanan, dan delapan Batasan Penelitian sudah masuk ke `chapters/bab1.tex`. Tujuan dan batasan mengikuti evaluasi campuran aditif terkontrol dan diagnostik yang telah dilakukan; BAB 2 dan BAB 3 tetap kerangka. Periksa kembali identitas, judul, dan isi draf bersama pembimbing.

Halaman pengesahan dan pernyataan masih menunggu redaksi resmi ITERA. `references.bib` memuat sepuluh sumber yang dikutip pada draf latar belakang. `main.tex` mencetak DAFTAR PUSTAKA dengan gaya numerik `unsrt`: nomor mengikuti urutan kemunculan sitasi pertama, dan sumber yang dikutip ulang tetap memakai nomor yang sama. Bab IV dan seterusnya belum dibuat. Sinkronisasi 1 November 2026 menyertakan sumber LaTeX, logo, catatan belajar, dan recipe editor pada repositori. Direktori `build/` tetap lokal.

Untuk membaca tanpa kompilasi, gunakan [BAB I](BAB_1.pdf) atau [BAB I beserta daftar pustaka](BAB_1_dengan_Daftar_Pustaka.pdf). Kedua ekspor diperiksa sama isi dan tata letaknya dengan halaman terkait pada hasil build lokal saat sinkronisasi. BAB II dan BAB III masih kerangka.

Di Antigravity dengan LaTeX Workshop/MiKTeX, buka `main.tex` sebagai dokumen utama dan jalankan recipe **XeLaTeX + BibTeX + XeLaTeX x2**. Pengaturan lokal disediakan pada folder `paper/.vscode/` dan `template_ta_latex/.vscode/`, sehingga berlaku saat salah satu folder tersebut dibuka sebagai workspace. Penanda root pada `bab1.tex` mengarahkan build ke `main.tex`.

```powershell
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
bibtex build/main
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

Jalankan perintah manual di atas dari folder `paper/template_ta_latex`. Hasil PDF berada di `build/main.pdf`. Untuk menambah sitasi, tambahkan entri pada `references.bib`, lalu panggil `\cite{kunciReferensi}` di naskah; jangan mengetik nomor `[1]` secara manual. Periksa sistematika dan gaya pustaka kampus bersama pembimbing; gaya numerik ini belum diklaim sebagai format resmi fakultas. [Paket bahan BAB 1–3](../persiapan_bab1_3/README.md) menyediakan diagram alir dan indeks gambar/tabel.

## Catatan belajar dan pemeriksaan latar belakang

- [Arti istilah untuk Fabio](notes/ISTILAH_LATAR_BELAKANG_UNTUK_FABIO.md): contoh sederhana, hubungan dengan TA, pembedaan model beku, embedding, retrieval, threshold, dan jenis kesalahan, serta latihan hitungan kosinus dan metrik yang muncul dalam BAB I.
- [Audit klaim 31 Oktober](notes/AUDIT_KLAIM_LATAR_BELAKANG_2026-10-31.md): penelusuran sepuluh paragraf ke literatur/data dan batas interpretasinya.

Isi naskah memakai Times New Roman 12 pt, faktor spasi baris eksplisit `\setstretch{1.5}`, rata kanan–kiri, tanpa inden, dan jarak antarparagraf 6 pt agar lebih sesuai contoh visual pengguna. Pengaturan ini menggantikan `\onehalfspacing` yang secara internal memakai faktor berbeda. Jarak judul BAB/subbab tetap memakai pengaturan rapat, termasuk daftar pustaka; ruang kosong buatan pada kerangka subbab dihapus. Catatan belajar disimpan terpisah dari teks skripsi.
