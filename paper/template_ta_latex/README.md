# Template TA LaTeX sampai Bab III

**Status 7 November 2026:** BAB I telah ditulis; BAB II memuat penelitian terdahulu dan teori hingga 2.13; BAB III berisi kerangka, termasuk bagian diagram alir, tanpa uraian metodologi. Daftar pustaka dibuat dari sumber yang dikutip. Judul dan naskah masih untuk pembahasan bersama pembimbing. Lihat [draf PDF gabungan](Draf_Skripsi.pdf); PDF ini adalah salinan hasil kompilasi, sedangkan `build/` tetap lokal.

Dokumen ini memakai satu `main.tex` yang memanggil halaman awal dan berkas setiap bab. Gaya draf A4 mengikuti contoh TA Sains Data pada [Repository ITERA](https://repo.itera.ac.id/depan/submission/SB2604150015). Struktur halaman pengesahan dan pernyataan dilengkapi dengan adaptasi [contoh LaTeX ITERA versi 2026.1](https://github.com/rdhnk/Latex-TA-IF-ITERA/tree/v2026.1). Sumber dan batas penyesuaiannya dicatat pada [catatan halaman awal](notes/FORMAT_HALAMAN_AWAL_ITERA_2026-11-04.md); adaptasi ini belum diklaim sebagai template resmi Fakultas Sains.

- `main.tex`: dokumen utama, ukuran halaman, margin, pemanggilan halaman awal/bab, serta daftar otomatis.
- `identitas.tex`: judul Indonesia dan Inggris, identitas mahasiswa, serta kolom isian dosen dan tanggal.
- `halaman_awal/`: sampul, halaman judul, pengesahan, orisinalitas, persetujuan publikasi, abstrak/abstract, motto, persembahan, dan kata pengantar.
- `chapters/bab1.tex`: Pendahuluan.
- `chapters/bab2.tex`: Tinjauan Pustaka; tabel 2.1 memuat lima studi dan teori ditulis hingga 2.13.
- `chapters/bab3.tex`: kerangka Metodologi Penelitian dengan bagian data, diagram alir, tahapan, dan jadwal; uraian belum ditulis.

**Status lokal 4 November 2026:** dokumen memakai XeLaTeX, `fontspec`, dan Times New Roman. BAB I memuat Latar Belakang, lima Rumusan Masalah, lima Tujuan yang berpadanan, dan delapan Batasan Penelitian, dengan istilah pencarian rekaman yang telah dirapikan. Tujuan dan batasan mengikuti evaluasi campuran aditif terkontrol dan diagnostik yang telah dilakukan. BAB II bagian 2.1 berisi tabel lima jurnal dan bagian 2.2 masih kerangka. Atas instruksi pengguna, kerangka BAB III dirinci menjadi tiga subbab utama dan 12 sub-subbab tanpa uraian; isinya dilanjutkan setelah instruksi berikutnya.

Halaman pengesahan dan pernyataan kini berisi template dengan kolom isian. Identitas dosen, tanggal, tanda tangan, dan foto masih berupa isian. Sesuai arahan terbaru, abstrak/abstract, motto, persembahan, dan kata pengantar hanya memuat judul halaman; isinya ditunda. Pembaruan 5 November mengisi tabel 2.1 dan menambahkan entri Ghani (2025) yang artikelnya sudah ada pada koleksi. `references.bib` kini memuat 18 entri; 11 sumber dikutip pada BAB I–II. `main.tex` mencetak DAFTAR PUSTAKA dengan gaya numerik `unsrt`: nomor mengikuti urutan kemunculan sitasi pertama, dan sumber yang dikutip ulang tetap memakai nomor yang sama. Entri yang belum dikutip tidak dipaksakan muncul pada daftar pustaka tercetak. Bab IV dan seterusnya belum dibuat. Direktori `build/` tetap lokal.

Untuk membaca, gunakan [draf PDF gabungan](Draf_Skripsi.pdf), yang memuat halaman awal, BAB I–II, kerangka BAB III, dan daftar pustaka. PDF BAB I yang sudah ada dipertahankan sebagai ekspor terdahulu dan tidak menjadi keluaran utama lagi.

Di Antigravity dengan LaTeX Workshop/MiKTeX, buka `main.tex` sebagai dokumen utama dan jalankan recipe **XeLaTeX + BibTeX + XeLaTeX x2**. Pengaturan lokal disediakan pada folder `paper/.vscode/` dan `template_ta_latex/.vscode/`, sehingga berlaku saat salah satu folder tersebut dibuka sebagai workspace. Penanda root pada `bab1.tex` mengarahkan build ke `main.tex`.

```powershell
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
bibtex build/main
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

Jalankan perintah manual di atas dari folder `paper/template_ta_latex`. Hasil PDF berada di `build/main.pdf`. Untuk menambah sitasi, tambahkan entri pada `references.bib`, lalu panggil `\cite{kunciReferensi}` di naskah; jangan mengetik nomor `[1]` secara manual. Periksa sistematika dan gaya pustaka kampus bersama pembimbing; gaya numerik ini belum diklaim sebagai format resmi fakultas. [Paket bahan BAB 1–3](../persiapan_bab1_3/README.md) menyediakan diagram alir dan indeks gambar/tabel.

## Catatan belajar dan pemeriksaan latar belakang

- [Rencana referensi BAB II](notes/RENCANA_REFERENSI_BAB2_2026-11-03.md): delapan studi prioritas untuk tabel 2.1, peran koleksi lokal, dan rujukan dasar teori. Catatan tersebut merupakan rencana sebelum tabel diisi; versi aktif mengikuti contoh PDF yang diberikan pengguna. [Enam artikel jurnal tambahan](../bibliography/PEMERIKSAAN_REFERENSI_2026-11-03.md) telah diperiksa dan dimasukkan ke koleksi serta CSV/Excel.
- [Sumber tabel 2.1, 5 November](notes/SUMBER_TABEL_2_1_2026-11-05.md): pemilihan akhir lima artikel jurnal, halaman bukti tiap ringkasan, batas perbandingan, dan pengaturan tabel. Catatan ini menggantikan status tabel kosong pada rencana 3 November.
- [Revisi pembimbing kedua 2 November](notes/REVISI_PB2_DAN_KONTRIBUSI_2026-11-02.md): manfaat pemantauan biodiversitas diperjelas, transisi satwa–burung dirapikan, dan pengulangan fokus/rancangan dikurangi. Catatan memetakan alasan dalam latar belakang ke lima Rumusan Masalah serta perbandingan kontribusi dengan literatur. Rumusan Masalah, Tujuan, Batasan Penelitian, dan format dipertahankan.
- [Pemeriksaan persebaran 3 November](notes/PERSEBARAN_20_LABEL_BURUNG_2026-11-03.md): persebaran target, cakupan nama lama, dan hasil verifikasi lokasi yang ditautkan ke bukti sumber. Revisi BAB I memperjelas alasan ITERA sebagai sumber derau lapangan lokal untuk pengujian terkontrol. Bagian 1.4 menegaskan cakupan 20 label spesies yang terdapat di Indonesia dan membatasi kesimpulan pada korpus serta profil derau yang diuji. Persebaran spesies dibedakan dari negara asal rekaman; catatan kaki lokasi telah dihapus atas permintaan pengguna.
- [Arti istilah untuk Fabio](notes/ISTILAH_LATAR_BELAKANG_UNTUK_FABIO.md): contoh sederhana, hubungan dengan TA, pembedaan model beku, embedding, retrieval, threshold, dan jenis kesalahan, serta latihan hitungan kosinus dan metrik yang muncul dalam BAB I.
- Revisi bahasa 4 November: BAB I memakai “pencarian rekaman” sebagai pengganti “temu kembali”, dengan penjelasan singkat istilah teknis dan penyeragaman penulisan bahasa asing. Susunan dan makna paragraf serta poin penelitian dipertahankan. Ringkasan padanan istilah ditambahkan pada catatan belajar di atas; pengerjaan isi BAB II–III menunggu instruksi pengguna.
- [Audit klaim 31 Oktober](notes/AUDIT_KLAIM_LATAR_BELAKANG_2026-10-31.md): penelusuran sepuluh paragraf ke literatur/data dan batas interpretasinya.

Isi naskah memakai Times New Roman 12 pt, faktor spasi baris eksplisit `\setstretch{1.5}`, rata kanan–kiri, tanpa inden, dan jarak antarparagraf 6 pt agar lebih sesuai contoh visual pengguna. Pengaturan ini menggantikan `\onehalfspacing` yang secara internal memakai faktor berbeda. Jarak judul BAB/subbab tetap memakai pengaturan rapat, termasuk daftar pustaka; ruang kosong buatan pada kerangka subbab dihapus. Catatan belajar disimpan terpisah dari teks skripsi.
