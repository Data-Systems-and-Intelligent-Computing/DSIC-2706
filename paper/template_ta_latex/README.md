# Template TA LaTeX sampai Bab III

[Bab I](chapters/bab1.tex) memuat pertanyaan utama pada latar belakang dan empat rumusan masalah. [Bab II](chapters/bab2.tex) memuat lima studi di Tabel 2.1 dan landasan teori sampai Subbab 2.11. [Bab III](chapters/bab3.tex) memuat data dan variabel pada 3.1 serta tahapan penelitian sampai evaluasi pada 3.2.9.

Dokumen ini memakai satu `main.tex` yang memanggil halaman awal dan berkas setiap bab. Gaya draf A4 mengikuti contoh TA Sains Data pada [Repository ITERA](https://repo.itera.ac.id/depan/submission/SB2604150015). Struktur halaman pengesahan dan pernyataan dilengkapi dengan adaptasi [contoh LaTeX ITERA versi 2026.1](https://github.com/rdhnk/Latex-TA-IF-ITERA/tree/v2026.1). Sumber dan batas penyesuaiannya dicatat pada [catatan halaman awal](notes/FORMAT_HALAMAN_AWAL_ITERA_2026-11-04.md); adaptasi ini belum diklaim sebagai template resmi Fakultas Sains.

- `main.tex`: dokumen utama, ukuran halaman, margin, pemanggilan halaman awal/bab, serta daftar otomatis.
- `identitas.tex`: judul Indonesia dan Inggris, identitas mahasiswa, serta kolom isian dosen dan tanggal.
- `halaman_awal/`: sampul, halaman judul, pengesahan, orisinalitas, persetujuan publikasi, abstrak/abstract, motto, persembahan, dan kata pengantar.
- `chapters/bab1.tex`: Pendahuluan.
- `chapters/bab2.tex`: Tinjauan Pustaka; tabel 2.1 memuat lima studi dan teori ditulis hingga 2.11.
- `chapters/bab3.tex`: Metodologi Penelitian dengan [diagram alir utama](../figures/bab3/Diagram%20Utama.drawio.png) dan [peta lokasi rekaman](../figures/bab3/peta_rekaman_xenocanto.png).

Tabel 2.1 membahas Hamer, Ghani, Bennovry, Allen-Ankins, serta Ghaffari dan Devos. Untuk memeriksa metode, ikuti empat rumusan masalah dari uji ketahanan pada variasi SNR, penerimaan kueri, kestabilan antarlokasi, hingga diagnosis kegagalan.

Identitas untuk halaman awal diatur di `identitas.tex`. Daftar pustaka mengambil entri yang dikutip dari [references.bib](references.bib) dengan gaya numerik `unsrt`. Nomor mengikuti urutan kemunculan pertama.

[Draf PDF gabungan](Draf_Skripsi.pdf) dan PDF BAB I merupakan ekspor terdahulu. Untuk melihat revisi terbaru, kompilasi `main.tex`.

Di Antigravity dengan LaTeX Workshop/MiKTeX, buka `main.tex` sebagai dokumen utama dan jalankan recipe **XeLaTeX + BibTeX + XeLaTeX x2**. Pengaturan lokal disediakan pada folder `paper/.vscode/` dan `template_ta_latex/.vscode/`, sehingga berlaku saat salah satu folder tersebut dibuka sebagai workspace. Penanda root pada `bab1.tex` mengarahkan build ke `main.tex`.

```powershell
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
bibtex build/main
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build main.tex
```

Jalankan perintah manual di atas dari folder `paper/template_ta_latex`. Hasil PDF berada di `build/main.pdf`. Untuk menambah sitasi, tambahkan entri pada `references.bib`, lalu panggil `\cite{kunciReferensi}` di naskah; jangan mengetik nomor `[1]` secara manual. Periksa sistematika dan gaya pustaka kampus bersama pembimbing; gaya numerik ini belum diklaim sebagai format resmi fakultas. [Paket bahan BAB 1–3](../persiapan_bab1_3/README.md) menyediakan diagram alir dan indeks gambar/tabel.

## Catatan belajar dan pemeriksaan latar belakang

- [Rencana referensi BAB II](notes/RENCANA_REFERENSI_BAB2_2026-11-03.md): delapan studi prioritas untuk tabel 2.1, peran koleksi lokal, dan rujukan dasar teori. Catatan tersebut merupakan rencana sebelum tabel diisi; daftar yang dipakai dapat dibaca di Bab II. [Enam artikel jurnal tambahan](../bibliography/PEMERIKSAAN_REFERENSI_2026-11-03.md) telah diperiksa dan dimasukkan ke koleksi serta CSV/Excel.
- [Sumber tabel 2.1, 5 November](notes/SUMBER_TABEL_2_1_2026-11-05.md): pemilihan artikel pada draf 5 November, halaman bukti tiap ringkasan, batas perbandingan, dan pengaturan tabel. Catatan ini menggantikan status tabel kosong pada rencana 3 November.
- [Revisi pembimbing kedua 2 November](notes/REVISI_PB2_DAN_KONTRIBUSI_2026-11-02.md): manfaat pemantauan biodiversitas diperjelas, transisi satwa–burung dirapikan, dan pengulangan fokus/rancangan dikurangi. Catatan memetakan alasan dalam latar belakang ke lima Rumusan Masalah serta perbandingan kontribusi dengan literatur. Rumusan Masalah, Tujuan, Batasan Penelitian, dan format dipertahankan.
- [Pemeriksaan persebaran 3 November](notes/PERSEBARAN_20_LABEL_BURUNG_2026-11-03.md): persebaran target, cakupan nama lama, dan hasil verifikasi lokasi yang ditautkan ke bukti sumber. Revisi BAB I memperjelas alasan ITERA sebagai sumber derau lapangan lokal untuk pengujian terkontrol. Bagian 1.4 menegaskan cakupan 20 label spesies yang terdapat di Indonesia dan membatasi kesimpulan pada korpus serta profil derau yang diuji. Persebaran spesies dibedakan dari negara asal rekaman; catatan kaki lokasi telah dihapus atas permintaan pengguna.
- [Arti istilah untuk Fabio](notes/ISTILAH_LATAR_BELAKANG_UNTUK_FABIO.md): contoh sederhana, hubungan dengan TA, pembedaan model beku, embedding, retrieval, threshold, dan jenis kesalahan, serta latihan hitungan kosinus dan metrik yang muncul dalam BAB I.
- Revisi bahasa 4 November: BAB I memakai “pencarian rekaman” sebagai pengganti “temu kembali”, dengan penjelasan singkat istilah teknis dan penyeragaman penulisan bahasa asing. Susunan dan makna paragraf serta poin penelitian dipertahankan. Ringkasan padanan istilah ditambahkan pada catatan belajar di atas; pada tanggal tersebut, BAB II–III masih dalam persiapan.
- [Audit klaim 31 Oktober](notes/AUDIT_KLAIM_LATAR_BELAKANG_2026-10-31.md): penelusuran sepuluh paragraf ke literatur/data dan batas interpretasinya.

Isi naskah memakai Times New Roman 12 pt, faktor spasi baris eksplisit `\setstretch{1.5}`, rata kanan–kiri, tanpa inden, dan jarak antarparagraf 6 pt agar lebih sesuai contoh visual pengguna. Pengaturan ini menggantikan `\onehalfspacing` yang secara internal memakai faktor berbeda. Jarak judul BAB/subbab tetap memakai pengaturan rapat, termasuk daftar pustaka; ruang kosong buatan pada kerangka subbab dihapus. Catatan belajar disimpan terpisah dari teks skripsi.
