# Sinkronisasi folder TA — 1 November 2026

Sinkronisasi dilakukan atas permintaan Fabio untuk mengunggah perubahan yang berkaitan dengan TA ke `Data-Systems-and-Intelligent-Computing/DSIC-2706` dan membersihkan berkas yang tidak berkaitan. Tidak ada eksperimen dijalankan ulang.

## Bahan yang disertakan

- Draf BAB I LaTeX: Latar Belakang, lima Rumusan Masalah, lima Tujuan, dan delapan Batasan Penelitian; BAB II dan BAB III tetap kerangka.
- BibTeX, logo, recipe XeLaTeX/BibTeX, catatan istilah, audit klaim, dan dua PDF ekspor BAB I. Isi dan tata letak ekspor cocok dengan halaman terkait pada build lokal 23 halaman saat pemeriksaan.
- Pembaruan pustaka 26–27 Oktober: katalog CSV/Excel, PDF yang dikoreksi/ditambahkan, hasil ekstraksi teks, dan catatan pemeriksaan. Penghapusan tujuh PDF yang sudah tercatat pada working tree mengikuti alasan di `paper/bibliography/README.md`; penghapusan tersebut bukan pembersihan baru oleh sinkronisasi ini.
- Enam bacaan paket belajar beserta PDF gabungan.
- Bahan `Teori Dasar/` beserta ilustrasi dan penanda historis. Panduan komprehensif berpindah dari root ke folder ini; PDF panduan cocok byte dengan versi Git sebelumnya.
- Draf pengembangan E4 yang sebelumnya belum terlacak, dengan status historis dan byte asli dipertahankan. Produsen E4 aktif tetap `run_e4_five_locations_v10_stage7.py.draft`.
- Penghapusan formulir DOCX root yang sudah ada sebelum sinkronisasi; dokumen administrasi TA yang masih tersedia di `Administrasi/` dipertahankan lokal.

## Pembersihan baru

| Target | Jumlah berkas | Alasan |
|---|---:|---|
| `outputs/wwc-29okt/` | 7 | Berkas jadwal wawancara, panitia, dan peserta yang tidak berkaitan dengan penelitian TA. |
| `Teori Dasar/__MACOSX/` | 9 | Metadata ekstraksi macOS; bukan gambar atau bahan teori. |
| `paper/bibliography/referensi_jurnal_modern.xlsx.inspect.ndjson` | 1 | Hasil inspeksi spreadsheet sementara; katalog aktif tetap CSV/Excel. |

Target absolut dipastikan berada di dalam folder TA sebelum penghapusan. Aturan Git ditambah agar metadata macOS dan inspeksi sementara tidak ikut terlacak kembali.

## Bahan yang tetap lokal

Audio, checkpoint, lingkungan Python, cache, direktori build/temporer, dokumen administrasi akademik, dan arsip audit lokal tetap dipertahankan sesuai `.gitignore`. Data mentah, manifes, hasil run, dan skrip produsen E4 historis tidak diubah oleh sinkronisasi.

## Pemeriksaan

Pemeriksaan akhir mencakup kelengkapan bahan, jalur tautan pada dokumen yang diperbarui, sitasi LaTeX/BibTeX, kecocokan dua ekspor PDF, sumber pustaka, serta cakupan staged Git. Hasil pemeriksaan dan identitas commit dapat ditelusuri dari commit sinkronisasi ini; ini bukan pengulangan seluruh pengujian pipeline.

- Katalog CSV dan Excel identik pada seluruh sel: 28 referensi; 26 PDF lokal dapat dibaca.
- Sepuluh kunci sitasi BAB I tersedia di BibTeX dan urutannya cocok dengan daftar pustaka build terakhir.
- Dua ekspor BAB I cocok isi dan tata letaknya dengan build terakhir; PDF dan sumber bab yang sudah benar tidak ditulis ulang dalam sinkronisasi ini.
- Tautan lokal pada sepuluh dokumen navigasi/catatan diperiksa. Ada satu masalah lama: tautan `LICENSE` pada README root belum memiliki berkas tujuan. Kebijakan lisensi tidak diubah atau dibuat ulang dalam pekerjaan sinkronisasi ini.
- Pemeriksaan jalur perubahan memastikan berkas terlacak pada data, hasil, konfigurasi, kode aktif, notebook, registri eksperimen, dan artefak penelitian tetap sama. Pemeriksaan ukuran berkas baru serta pola kredensial juga dilakukan sebelum staging.
