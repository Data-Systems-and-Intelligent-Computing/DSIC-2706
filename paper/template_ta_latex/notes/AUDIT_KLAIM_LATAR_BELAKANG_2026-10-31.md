# Audit klaim Latar Belakang — 31 Oktober 2026

## Cakupan dan hasil

Pemeriksaan membaca ulang sepuluh paragraf Latar Belakang pada [bab1.tex](../chapters/bab1.tex), entri [references.bib](../references.bib), bagian relevan dari PDF lokal, serta sumber penerbit/repository di bawah. Ini pemeriksaan kesesuaian klaim dengan sumber, bukan tinjauan sistematis seluruh publikasi atau pengesahan independen seluruh metode jurnal.

**Klaim eksternal utama mempunyai sumber yang sesuai.** Perbaikan terutama memperjelas batas interpretasi dan memisahkan hasil jurnal dari pilihan rancangan TA. Sumber yang tersedia cukup untuk klaim yang dipertahankan; tidak perlu menambahkan artikel baru untuk menutupi klaim yang terlalu luas. Jika kelak ditambahkan angka nasional, tren populasi, atau manfaat ekologis terukur, sumber primer untuk angka tersebut harus diperiksa tersendiri.

Nomor [1]–[10] mengikuti urutan pada saat audit. Kunci BibTeX tetap menjadi penghubung bila nomor berubah.

## 1. Penelusuran per paragraf

| Paragraf | Klaim/fungsi | Bukti dan bagian yang diperiksa | Keputusan dan batas |
|---|---|---|---|
| 1 | Suara menyediakan informasi aktivitas satwa; perkembangan perekaman memperbesar kebutuhan analisis dan waktu ahli. | [1] `stowell2022bioacoustics`: abstrak/pendahuluan, PDF lokal hlm. 1. [Versi jurnal](https://pmc.ncbi.nlm.nih.gov/articles/PMC8944344/). | Didukung. Tidak ditambahkan angka penghematan waktu atau manfaat konservasi yang tidak diukur. |
| 2 | Cikaniki: 40 spesies terdeteksi, pemantauan 15 hari, termasuk burung nokturnal. | [2] `ningrum2026cikaniki`: abstrak hlm. 1 dan metode/hasil. [Penerbit](https://journal.ipb.ac.id/jwcm/article/view/72427). | Angka berlaku pada studi tersebut; bukan jumlah individu atau kekayaan spesies seluruh Indonesia. |
| 3 | BirdSet: >6.800 jam pelatihan, >400 jam pada delapan dataset evaluasi, kondisi rekaman beragam. | [3] `rauch2025birdset`: abstrak dan pendahuluan hlm. 1–3. [Prosiding ICLR](https://proceedings.iclr.cc/paper_files/paper/2025/hash/484d254ff80e99d543159440a06db0de-Abstract-Conference.html). | Didukung sebagai skala benchmark, bukan jumlah data TA atau satu lokasi. |
| 4 | Evaluasi 37 spesies; suara manusia berasosiasi dengan false positive, gangguan fisik/geofoni dengan false negative. | [4] `clark2023soundscape`: abstrak hlm. 1, pemilihan spesies hlm. 4/7, analisis komponen suara. [PDF lembaga mitra](https://www.pepperwoodpreserve.org/wp-content/uploads/2024/04/1-s2.0-S1574954123000948-main.pdf). | Didukung sebagai asosiasi pada klasifikasi; tidak membuktikan sebab kausal kegagalan model TA. |
| 5 | BIRB: retrieval nearest-centroid dan generalisasi. Ghani: encoder beku, linear classifier, perbandingan embedding burung/audio umum. | [5] `hamer2023birb`: hlm. 1/5/9; [arXiv v2](https://arxiv.org/abs/2312.07439v2). [6] `ghani2023embeddings`: abstrak hlm. 1, linear probes hlm. 3; [jurnal](https://www.nature.com/articles/s41598-023-49989-z). | Didukung. Kalimat akhir diubah menjadi alasan memilih pembanding dan pengujian TA sendiri. Hasil klasifikasi tidak disebut bukti retrieval berderau. |
| 6 | Ghaffari–Devos: delapan gangguan, normalisasi/kompresi, pengaruh konfigurasi. Fairbairn: 24 kombinasi, empat agregasi, F1 0,46–0,84 dan threshold. | [7] `ghaffari2024frontends`: abstrak hlm. 1, noise dataset hlm. 4, noise tolerance hlm. 8; [repository penulis](https://biblio.ugent.be/publication/01HYG8REQ5B156T9NJ0M9SVM16). [8] `fairbairn2025birdnet`: abstrak hlm. 1, analisis hlm. 5/8; [jurnal](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0330836). | Didukung. Pengaruh threshold dibatasi terhadap F1 dalam analisis Fairbairn. Confidence classifier tidak disamakan dengan cosine TA. |
| 7 | Alasan menetapkan fokus protokol TA. | Sintesis peneliti atas perbedaan tugas/kondisi [5]–[8]; sitasi kini diletakkan langsung pada kalimat penghubung. | Ini penalaran untuk rancangan, bukan temuan suatu jurnal atau klaim riset sejenis belum pernah ada. Rumusan dipersempit. |
| 8 | PANNs dipralatih pada AudioSet; BirdNET mengenali suara burung. Pilihan MFCC/PANNs/BirdNET, R3, encoder beku, dan penilaian spesies adalah rancangan TA. | [9] `kong2020panns`: abstrak hlm. 1; [repository institusi penulis](https://openresearch.surrey.ac.uk/esploro/outputs/journalArticle/PANNs-Large-Scale-Pretrained-Audio-Neural-Networks-for-Audio-Pattern-Recognition/99520023602346). [10] `kahl2021birdnet`: abstrak hlm. 1, DOI 10.1016/j.ecoinf.2021.101236. [Kode representasi](../../../src/embeddings.py), [MFCC](../../../src/mfcc.py), dan [retrieval](../../../src/retrieve.py). | Asal model didukung jurnal; pilihan metode dinyatakan sebagai keputusan penelitian ini. Spesifikasi BirdNET 2021 tidak dianggap identik dengan v2.4. |
| 9 | Data 20 spesies, kueri/galeri tetap, campuran aditif, kalibrasi, lima lokasi, dan pencatatan sumber. | Bukti primer TA: [split](../../../data/manifests/dataset_split.csv), [manifes derau](../../../data/manifests/itera_noise_manifest.csv), [RQ](../../../docs/research/rq.md), [mixer](../../../src/mix_noise.py), [E2](../../../scripts/run_e2_controlled_noise.py), [E3](../../../scripts/run_e3_open_set.py), dan [identitas E4](../../../results/reproductions/E4_5sites_20261011T213404_350219Z/run_identity.json). | Data/rancangan sendiri, bukan angka dari jurnal. Dihitung ulang: 20 species_key dan 1.216 baris target. Sumber dicatat pula sebagai komentar LaTeX; rincian provenance dapat dikembangkan pada BAB 3. |
| 10 | Tujuan evaluasi dan kontribusi yang ditawarkan. | [RQ aktif](../../../docs/research/rq.md) dan [batas kontribusi](../../../docs/research/novelty-boundary.md). | Tujuan penelitian, bukan janji aplikasi berhasil, manfaat konservasi terukur, atau keunggulan model universal. |

## 2. Koreksi isi yang dilakukan

1. Kalimat bahwa hasil terdahulu “belum menentukan” hasil TA diganti menjadi alasan pemilihan pembanding dan pengujian protokol sendiri.
2. Hubungan literatur–fokus penelitian diberi sitasi [5]–[8] dan diperjelas sebagai sintesis/rancangan peneliti.
3. Pengaruh threshold dinyatakan paling kuat **terhadap F1 dalam analisis Fairbairn**, bukan seluruh sistem pengenalan suara.
4. Asal PANNs/BirdNET tetap bersitasi; pilihan pembanding dinyatakan dengan frasa “Penelitian ini menetapkan”.
5. Jumlah spesies dan prosedur TA ditelusuri ke manifes/kode, bukan diberi sitasi jurnal milik peneliti lain. Identitas rekaman serta parameter mixing dinyatakan dicatat agar dapat ditelusuri.

## 3. Batas interpretasi

- F1, akurasi klasifikasi, dan mAP retrieval tidak saling menggantikan.
- Asosiasi noise–kesalahan pada Clark bukan uji penyebab kegagalan TA.
- BIRB meneliti generalisasi focal–passive; E4 TA masih campuran aditif.
- Hasil linear classifier Ghani tidak langsung menjadi hasil retrieval TA.
- Bobot model beku tidak berarti embedding tetap ketika audio berubah.
- R3 berbasis ID dan retensinya bukan ukuran ketahanan akustik.
- Perbedaan lokasi tidak membuktikan mekanisme serangga/frekuensi tertentu.
- Pemisahan internal target tidak membuktikan bebas overlap seluruh data pralatih.

## 4. Status referensi

Sepuluh sumber tetap digunakan; tidak ada referensi atau DOI baru yang diada-adakan. BirdSet adalah **prosiding ICLR 2025**, dan PDF BIRB yang dirujuk adalah **preprint arXiv v2 tahun 2023**. Keduanya tidak dilabeli sebagai jurnal. Stowell dikutip sebagai PeerJ 2022; isi relevan diperiksa pada versi jurnal daring, sementara PDF lokal adalah naskah penulis 2021.

PDF yang diperiksa berada di `paper/bibliography/` sesuai tabel referensi aktif. Kunci yang dipakai naskah ada di `references.bib`. Tidak ada eksperimen/data yang dijalankan ulang atau diubah dalam audit ini; persetujuan naskah tetap melalui pembimbing.

## 5. Perapian tata letak

Teks tetap rata kanan–kiri, tanpa inden, dan Times New Roman 12 pt. Pada perapian awal, antarparagraf dibuat 3 pt dengan `\onehalfspacing`. Setelah pengguna memberikan contoh visual berikutnya, faktor baris diubah menjadi `\setstretch{1.5}` dan antarparagraf menjadi 6 pt agar tampil lebih renggang. Jarak setelah judul BAB tetap 12 pt, juga berlaku pada DAFTAR PUSTAKA. Subbab memakai jarak sebelum 10 pt/sesudah 3 pt; sub-subbab 8 pt/3 pt. Ruang kosong buatan `vspace` pada kerangka BAB 1–3 dihapus, sementara judul/komentar subbab dipertahankan. Format akhir tetap mengikuti keputusan pembimbing/fakultas.
