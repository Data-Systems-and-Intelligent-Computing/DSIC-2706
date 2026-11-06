# Halaman awal dan dokumen utama — 4 November 2026

## Bentuk penyerahan

Dokumen utama adalah `main.tex`, dengan PDF gabungan pada `build/main.pdf`. Sumber setiap bab tetap terpisah pada `chapters/bab1.tex`, `chapters/bab2.tex`, dan `chapters/bab3.tex`; halaman awal pada `halaman_awal/`; semua identitas pada `identitas.tex`. Ekspor PDF BAB I yang sudah ada merupakan ekspor terdahulu, bukan keluaran utama untuk pembaruan selanjutnya.

Judul bahasa Indonesia yang ditambahkan:

**Analisis Ketahanan dan Sensitivitas Spektral Representasi Audio dalam Pencarian Rekaman Suara Burung Indonesia dengan Campuran Derau Lapangan ITERA Terkontrol**

Judul Inggris tetap disimpan pada `identitas.tex` untuk penulisan abstract berikutnya. Sampul dan halaman judul memakai judul Indonesia dengan layout yang sudah disetujui pengguna. “Burung Indonesia” mengikuti cakupan BAB I: label burung yang terdapat di Indonesia; bukan pernyataan bahwa semua rekaman dibuat di Indonesia. Rincian penggunaan model tanpa pembaruan bobot dijelaskan pada BAB I dan tidak dicantumkan lagi dalam judul. MFCC tetap fitur hitungan, sedangkan bobot PANNs CNN14 dan BirdNET tidak diperbarui.

## Sumber yang diperiksa

1. [Laman Tugas Akhir Sains Data ITERA](https://sd.itera.ac.id/akademik/tugas-akhir), yang menautkan konteks pedoman TA 2026. Ringkasan terindeks menyebut penulisan mengikuti pedoman ITERA; dokumen pedoman lengkap dari laman ini belum berhasil diunduh pada pemeriksaan ini.
2. [Contoh TA Sains Data pada Repository ITERA](https://repo.itera.ac.id/depan/submission/SB2604150015), yang sebelumnya menjadi acuan gaya dan urutan halaman draf. Identitas, isi penelitian, dan tanda tangan contoh tidak disalin.
3. [Template LaTeX TA Teknik Informatika ITERA, versi 2026.1](https://github.com/rdhnk/Latex-TA-IF-ITERA/tree/v2026.1), rilis 29 Januari 2026, commit `e2a333eac12f8840f77bfd7508a29cb2f1aa6d59`. Kontributor tercantum pada README repositori. Berkas sumber yang diperiksa adalah `chapters/approval.tex`, `chapters/statement.tex`, `chapters/publication.tex`, `chapters/cover-hard.tex`, `chapters/abstract-id.tex`, serta versi A4 halaman pengesahan. Susunan kolom dan pernyataan diadaptasi untuk Sains Data/Fakultas Sains dengan kode LaTeX lokal.

Template Teknik Informatika dipakai sebagai **contoh ITERA**, bukan dinyatakan sebagai template resmi Sains Data. Halaman pengesahan lokal menyediakan dua pembimbing dan dua penguji sebagai kolom isian; ini bukan penetapan jumlah penguji yang wajib untuk semua tahap TA.

## Penyesuaian yang dilakukan

- Sampul dan halaman judul dalam memakai judul Indonesia dengan posisi elemen yang sama seperti draf sebelumnya. Judul Inggris tersedia pada template *abstract*.
- Lembar pengesahan menyediakan identitas mahasiswa, tanggal kosong, ruang pasfoto 3 × 4 cm, pembimbing, penguji, tanda tangan, serta koordinator program studi. Belum menyatakan tanggal lulus atau memuat pengesahan jadi.
- Halaman orisinalitas dan persetujuan publikasi berisi draf pernyataan dengan ruang tanda tangan dan tanggal. Penyediaan template bukan pelaksanaan persetujuan publikasi.
- Mengikuti arahan terbaru pengguna, abstrak Indonesia dan Inggris hanya memuat judul halaman; isi, metadata abstrak, dan kata kunci ditunda.
- Motto, persembahan, dan kata pengantar hanya memuat judul halaman. Isi pribadi dan ucapan terima kasih ditunda.
- Semua nama/gelar dosen, NIP/NIDN, dan tanggal yang belum tersedia dipusatkan sebagai isian pada `identitas.tex`. Nama dan NIM mahasiswa mengikuti data yang sudah ada pada draf lokal; tetap perlu diperiksa penulis sebelum pengesahan.
- Halaman awal dipisahkan per berkas agar perubahan identitas tidak memerlukan penyuntingan isi tiap bab.
- Isi BAB I, kerangka BAB II–III, daftar pustaka, dan pengaturan isi 12 pt/spasi 1,5/rata kanan–kiri dipertahankan pada pekerjaan ini.

## Ukuran kertas dan batas penyesuaian

Draf bimbingan tetap memakai A4 dengan margin yang sebelumnya disepakati pengguna. README template Teknik Informatika 2026.1 menyebut format UNESCO 155 × 230 mm untuk versi perpustakaan dan menyediakan versi A4 terpisah. Karena dokumen ketentuan lengkap khusus Sains Data/Fakultas Sains belum diperoleh, PDF A4 ini tidak dilabeli sebagai berkas final siap cetak/perpustakaan. Penyesuaian ukuran akhir memerlukan acuan yang berlaku untuk pengumpulan Fabio; tidak dilakukan perubahan ukuran seluruh bab tanpa dasar khusus prodi.

Penulisan isi BAB II dan BAB III tetap menunggu instruksi pengguna.

## Contoh yang ditegaskan pengguna pada akhir revisi

Pengguna meminta mengikuti https://repository.itera.ac.id/depan/submission/SB2604150015 dengan layout yang sudah benar dan menunda kata pengantar, abstrak, serta motto. Halaman lengkap/berkas lampiran pada tautan tersebut belum berhasil diakses: pembacaan web tidak memperoleh halaman, unduhan langsung mengembalikan HTTP 403, dan akses browser dihentikan karena alat tidak dapat memastikan URL browser di Windows. Karena itu, redaksi halaman pengesahan/pernyataan saat ini masih adaptasi contoh LaTeX yang diperiksa di atas, belum dinyatakan sama persis dengan lampiran contoh SB2604150015. Pencocokan persis memerlukan PDF bagian awal contoh tersebut.

Penyesuaian ejaan 4 November, mengikuti klarifikasi pengguna: nama singkat kampus ditulis **Itera** dalam paragraf dan **ITERA** pada judul atau subbab. Judul sampul tetap kapital seluruhnya. Nama berkas, alamat sumber, dan gambar logo tidak diubah.

Revisi judul berikutnya pada 4 November menambahkan kata “Analisis”, menonjolkan ketahanan dan sensitivitas spektral, serta menghapus frasa “tanpa pelatihan ulang” dari judul Indonesia dan padanan *frozen* dari judul Inggris. Penyebutan pendekatan kuantitatif sempat ditambahkan, lalu dihapus dari BAB I mengikuti arahan berikutnya karena belum diperlukan pada latar belakang. Kerangka BAB II–III tidak diubah; rumusan masalah, tujuan, batasan, dan urutan sitasi tetap.

Penyempurnaan berikutnya: kata “untuk” pada judul diganti menjadi “dalam”; padanan judul Inggris mengikuti perubahan tersebut. Penutup latar belakang kembali berfokus pada arah penelitian tanpa menyebut jenis pendekatan.
