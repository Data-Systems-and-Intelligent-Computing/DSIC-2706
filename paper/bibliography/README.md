# Referensi penelitian DSIC-2706

Diperiksa dan diperbarui pada **26 Oktober 2026**. Ruang lingkup pembaruan hanya folder pustaka ini. Kode eksperimen, audio, hasil E0-E5, dan naskah penelitian tidak diubah oleh pembaruan pustaka.

**Pemeriksaan lanjutan 27 Oktober 2026:** [status koreksi dan pencarian alternatif dua PDF](PEMERIKSAAN_REFERENSI_2026-10-27.md). Jumlah tetap 28 entri dan 26 PDF; tersedia pula [paket belajar teori dan perhitungan](../../learning/PAKET_BELAJAR_UJIAN/README.md).

## Daftar aktif

- [Tabel Excel](referensi_jurnal_modern.xlsx) dan [tabel CSV](referensi_jurnal_modern.csv) memuat **28 referensi** dengan isi yang sama.
- **21 referensi terbit pada 2022-2026**, diprioritaskan untuk penelitian terdahulu. Ini mencakup jurnal, prosiding, dan preprint; jenis publikasinya ditandai terpisah.
- **7 referensi lebih lama** dipertahankan sebagai landasan asal model, metode, atau konteks evaluasi. Jangan menyebutnya sebagai kajian terbaru.
- **26 PDF berbeda** tersedia dan dicocokkan dengan entri tabel. Dua entri belum memiliki PDF: Putra dkk. (2024) dan Fluss dkk. (2005).
- Kolom `No` mempertahankan ID lama; nomor yang terputus menandai referensi yang dikeluarkan. Artikel tambahan memakai ID 33 dan 34.
- Kolom baru mencatat jenis publikasi, peran, prioritas tahun, nama PDF, status PDF, sumber verifikasi, dan catatan versi/batas pemeriksaan.

Keberadaan artikel, relevansi, status penelaahan ilmiah, dan mutu metode merupakan hal yang berbeda. Pemeriksaan ini tidak menetapkan peringkat SINTA/Scopus atau mengesahkan seluruh klaim setiap artikel. Tidak ada artikel atau PDF yang dibuat sebagai pengganti sumber ilmiah asli.

## PDF yang diperbaiki

1. **Stowell:** berkas yang sebelumnya berisi artikel matematika diganti naskah asli *Computational bioacoustics with deep learning: a review and roadmap* dari [arXiv](https://arxiv.org/abs/2112.06725). PDF lokal merupakan versi naskah penulis Desember 2021. Artikel jurnalnya terbit di PeerJ pada 2022 dan identitasnya diverifikasi melalui [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8944344/). Perbedaan versi ini dicatat, tidak disamarkan sebagai PDF versi penerbit.
2. **Moummad dkk.:** berkas yang sebelumnya berisi artikel DCASE 2022 diganti [naskah arXiv v8](https://arxiv.org/abs/2409.08589v8) *Domain-Invariant Representation Learning of Bird Sounds*. Versi pertama 2024; PDF yang disimpan Januari 2026. Publikasi ICASSP 2026 dikonfirmasi pada [repositori penulis](https://github.com/ilyassmoummad/ProtoCLR).
3. **Putra dkk.:** PDF yang salah ternyata identik dengan artikel MFCC-BiLSTM. Salinan yang salah dihapus; artikel MFCC-BiLSTM yang benar tetap ada. Artikel MFCC-Naive Bayes tetap dicatat karena identitasnya sah dan relevan, tetapi PDF aslinya belum berhasil diunduh dari situs penerbit.

## PDF tambahan

- **Clark dkk. (2023)**, *The effect of soundscape composition on bird vocalization classification in a citizen science biodiversity monitoring project*. DOI [10.1016/j.ecoinf.2023.102065](https://doi.org/10.1016/j.ecoinf.2023.102065). PDF versi terbit diperoleh dari situs lembaga mitra Pepperwood.
- **Hassanzad dan Hajian-Tilaki (2024)**, *Methods of determining optimal cut-point of diagnostic biomarkers with application of clinical data in ROC analysis: an update review*. DOI [10.1186/s12874-024-02198-2](https://doi.org/10.1186/s12874-024-02198-2). Jurnal terbuka ini menjadi pendamping terbaru untuk dasar ROC/Youden; bukan bukti bahwa threshold audio bersih stabil pada derau.
- **Ghaffari dan Devos (2024)**, *On the role of audio frontends in bird species recognition*. DOI [10.1016/j.ecoinf.2024.102573](https://doi.org/10.1016/j.ecoinf.2024.102573). PDF versi terbit diperoleh dari repositori Ghent University. Penelitian ini membahas frontend audio dan ketahanan derau; berbeda dari perbandingan frozen retrieval TA.

## Artikel sah yang PDF-nya belum diperoleh

| ID | Artikel | Status dan akses resmi |
|---|---|---|
| 7 | Putra, Nurdiyansyah, Rahman (2024), MFCC dan Naive Bayes | Halaman dan abstrak penerbit terverifikasi. Unduhan dari komputer ini gagal tersambung. [Halaman penerbit](https://ejurnal.umri.ac.id/index.php/JIK/article/view/7558), [tautan PDF asli](https://ejurnal.umri.ac.id/index.php/JIK/article/download/7558/3071/24869). |
| 32 | Fluss, Faraggi, Reiser (2005), Estimation of the Youden Index and its Associated Cutoff Point | Identitas dan abstrak terverifikasi di [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1002/bimj.200410135). PDF penuh belum diperoleh; jangan mengutip detail yang belum dibaca. Ulasan terbuka 2024 tersedia sebagai ID 33. |

Ketiadaan PDF lokal tidak berarti artikelnya palsu. Jika sumber memerlukan akses institusi, gunakan akses perpustakaan atau salinan legal penulis. Jangan menyimpan halaman HTML atau ringkasan buatan dengan ekstensi PDF.

## Referensi yang dikeluarkan

PDF dan baris tabel berikut dihapus dari daftar aktif karena tidak mendukung ruang lingkup sekarang. Ini keputusan relevansi, bukan tuduhan bahwa publikasinya palsu.

| ID lama | Judul | Alasan |
|---|---|---|
| 4 | Klasifikasi Suara Katak Menggunakan Model Deep Learning | Objek katak dan klasifikasi DenseNet tidak mendukung variabel atau metode aktif TA. |
| 13 | FSD50K an open dataset of human-labeled sound events | FSD50K tidak digunakan dalam TA dan bukan data pralatih PANNs yang dipakai (AudioSet). |
| 14 | AST Audio Spectrogram Transformer | AST tidak diimplementasikan atau dibandingkan dalam eksperimen TA. |
| 17 | Identifikasi Jenis Anura dengan Bioakustik | Inventarisasi Anura tidak mendukung pertanyaan retrieval burung atau eksperimen aktif. |
| 24 | Enabling Multi-Species Bird Classification on Low-Power Bioacoustic Loggers | Optimasi energi dan deployment WrenNet pada mikrokontroler berada di luar pengujian TA. |
| 25 | Ultra-Compact CNN Architectures for Tropical Bird Audio Detection on Microcontrollers | DrongoNet menguji detektor pada mikrokontroler; TA tidak mengevaluasi perangkat atau efisiensi energi. |

## Koreksi ringkasan

- Nama penulis pengganti seperti "Tim" diperbaiki pada referensi aktif.
- ConvNeXt Way Kambas tidak lagi disebut memiliki arsitektur/lokasi sama dengan TA.
- Ringkasan BirdNET 2021 memakai spesifikasi dan hasil versi artikel 2021; tidak dicampur dengan checkpoint v2.4 TA.
- PANNs CNN14 dibedakan dari Wavegram-Logmel-CNN, dan AudioSet dibedakan dari FSD50K.
- Best dkk. diperbaiki menjadi PLOS ONE 18(7); metode autoencoder dan clustering tidak lagi disebut eksperimen pembanding langsung MFCC/PANNs/BirdNET.
- DCASE 2023 diperbaiki daftar penulis, tugas deteksi kejadian, dan hasil F-score-nya; tidak disebut protokol retrieval E1-E3 yang sama.
- Cikaniki tidak lagi dijadikan bukti bahwa potongan lima detik optimal atau mencakup mayoritas frase semua burung Indonesia.
- MyGardenBird memakai data dan hasil baseline yang dilaporkan; klaim degradasi derau tanpa hasil uji yang ditelusuri dihapus.
- SEABAD dibatasi pada deteksi aktivitas burung; tidak dipakai untuk mengesahkan seluruh protokol TA.
- A Metric Learning Reality Check dibatasi pada evaluasi citra dan prinsip perbandingan yang adil; tidak disebut pengganti teori metrik retrieval.
- Istilah gap lama dan klaim "memvalidasi paired in-situ" dibuang dari tabel aktif. Campuran terkontrol tidak membuktikan kinerja burung target yang direkam langsung di lapangan.
- Angka akurasi klasifikasi, F-score deteksi, cROC-AUC, dan mAP retrieval tidak diperlakukan sebagai metrik yang saling setara.

## Pemeriksaan berkas

CSV dan Excel dibandingkan seluruh sel datanya setelah ekspor. Semua PDF aktif dapat dibaca dan tidak ada hash PDF ganda. PDF lama yang tetap relevan dipastikan tidak berubah. `extracted_texts_all.txt` dibangun ulang dari PDF aktif agar tidak lagi memuat artikel salah atau artikel yang dikeluarkan. Berkas `*.inspect.ndjson` lama bukan daftar referensi aktif.

Hash SHA-256 PDF yang ditambahkan atau diganti:

| Berkas | SHA-256 |
|---|---|
| Domain-Invariant Representation Learning of Bird Sounds.pdf | `11e5525f633fc38ed0ae768177be22122ad8cf5c06f043e2bd80fa598ff0e99a` |
| Computational bioacoustics with deep learning a review and roadmap.pdf | `cba16a470f92947efe33a875e7db73e7d6239a7f35685bdda8497cf61d167635` |
| Clark_2023_Soundscape_composition.pdf | `11af4b319747d5facdd5ef8486b9ec87742d738e872c661f156f336bb113f91f` |
| Hassanzad_2024_ROC_Youden_cutpoint_review.pdf | `aaac4082aa6fd6929d50ed49dc5f22236892a47a6eef9a1332171a3c2e083d31` |
| Ghaffari_2024_Audio_frontends_bird_recognition.pdf | `6a8f57bed2f93d3c71eef54f9586085d8ba3e26c5639983f4a8d11ff81187e08` |
