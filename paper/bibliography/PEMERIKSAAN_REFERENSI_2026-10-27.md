# Pemeriksaan lanjutan referensi - 27 Oktober 2026

## Jawaban atas status koreksi

**Koreksi yang teridentifikasi pada pemeriksaan sebelumnya sudah ditangani dalam tabel referensi aktif dan indeks teks PDF.** Sebagiannya diperbaiki, sementara enam referensi di luar ruang lingkup dikeluarkan sesuai permintaan. Itu tidak berarti semua versi naskah, slide, atau catatan lama di seluruh folder sudah diselaraskan. Dua entri belum mempunyai PDF penuh, sehingga rincian yang memerlukan full-text tetap belum dapat disahkan.

Pemeriksaan ulang 27 Oktober membaca kembali CSV, Excel, dan seluruh PDF aktif. Hasilnya: **28 entri; 21 terbit 2022–2026; 26 PDF dapat dibaca dengan hash berbeda; dua entri tanpa PDF (ID 7 dan 32)**. Seluruh sel data CSV dan Excel cocok setelah baris format kosong diabaikan. Tidak ada referensi atau PDF penelitian baru yang dibuat untuk menutupi akses yang gagal.

## Daftar koreksi yang ditangani

| Topik | Penanganan pada daftar aktif |
|---|---|
| Stowell: PDF sebelumnya salah isi | Diganti naskah penulis yang sesuai; versi naskah 2021 dibedakan dari jurnal 2022. |
| Domain-invariant: PDF sebelumnya artikel lain | Diganti arXiv v8 Januari 2026; ICASSP 2026 dan riwayat versi dicatat. |
| Putra MFCC–Naive Bayes | Salinan salah yang ternyata identik dengan BiLSTM dihapus; artikel asli tetap tercatat tanpa PDF lokal. |
| Nama penulis generik/pengganti | Identitas penulis referensi aktif diperbaiki. |
| ConvNeXt Way Kambas | Tidak disebut metode atau lokasi yang sama dengan TA. |
| MFCC–BiLSTM | Data, segmentasi, fitur, dan akurasi dibatasi pada protokol artikel klasifikasi. |
| BirdSet, BIRB, Ghani | Tugas, data, jenis publikasi, dan perbedaan metrik/konteks dibedakan dari TA. |
| Open-set | Prinsip penolakan dibedakan dari bukti langsung untuk threshold cosine TA. |
| BirdNET 2021 | Spesifikasi artikel 2021 tidak dicampur dengan checkpoint v2.4 TA. |
| PANNs | CNN14 dibedakan dari Wavegram-Logmel-CNN; AudioSet tidak disebut FSD50K. |
| Metric Learning Reality Check | Konteks citra dan prinsip evaluasi dibedakan dari definisi metrik audio retrieval. |
| DCASE 2023 | Penulis, tugas deteksi kejadian, dan F-score dikoreksi; tidak disamakan dengan retrieval TA. |
| Best dkk. | PLOS ONE 18(7), autoencoder/clustering, dan batas hasil dibetulkan. |
| Cikaniki | Klaim lima detik optimal atau mencakup mayoritas frase semua burung Indonesia dihapus. |
| SEABAD dan MyGardenBird | Tugas/dataset serta hasil yang didukung dibatasi; klaim uji derau yang tidak ditelusuri dihapus. |
| Angka lintas tugas | Akurasi, F-score, cROC-AUC, dan mAP tidak diperlakukan setara. |
| Gap dan kinerja lapangan | Klaim bahwa campuran membuktikan paired in-situ/seluruh lapangan dihapus. |
| Referensi tidak relevan | ID lama 4, 13, 14, 17, 24, 25 dikeluarkan; alasan tercatat di README. |
| Indeks teks | Dibangun ulang dari PDF aktif; bukan lagi indeks artikel salah/dikeluarkan. |

Catatan: pemeriksaan ini menilai identitas sumber dan kesesuaian ringkasan yang telah diidentifikasi. Ini bukan penetapan status indeks jurnal atau validasi independen seluruh eksperimen setiap artikel.

## Pencarian alternatif dua PDF

| Artikel asli | Jalur yang diperiksa | Hasil | Pendamping yang tersedia |
|---|---|---|---|
| Putra dkk. (2024), MFCC–Naive Bayes | [Halaman penerbit](https://ejurnal.umri.ac.id/index.php/JIK/article/view/7558), [PDF penerbit](https://ejurnal.umri.ac.id/index.php/JIK/article/download/7558/3071/24869); percobaan HTTP serta penelusuran indeks | Artikel terindeks dan identitasnya dapat ditelusuri; unduhan komputer ini gagal tersambung. PDF lokal tetap belum tersedia. | ID 3, MFCC–BiLSTM (2025), PDF tersedia. Berguna untuk konsep MFCC lokal; algoritme dan hasilnya berbeda. |
| Fluss, Faraggi, Reiser (2005), Youden | [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1002/bimj.200410135), [CiteSeerX](https://citeseerx.ist.psu.edu/document?doi=4f25f7cd8f8cc84a1e15c486c036d88bed6ec250&repid=rep1&type=pdf), tautan unggahan penulis ResearchGate yang terindeks | Wiley/unggahan penulis tidak memberikan unduhan yang dapat disimpan; CiteSeerX gagal diakses melalui jalur yang diperiksa. Status tetap belum diperoleh. | ID 33, Hassanzad–Hajian-Tilaki (2024), ulasan ROC/Youden, PDF terbuka tersedia. Konteks klinisnya bukan hasil audio TA. |

Dua artikel pendamping di atas sudah ada dalam tabel dan folder; tidak ditambahkan lagi sebagai duplikat. Jangan mengganti judul atau nama berkas pendamping agar seolah-olah merupakan PDF artikel asli. Jika kemudian PDF asli diperoleh dari perpustakaan atau salinan legal penulis, cocokkan judul/penulis/DOI sebelum memperbarui status.

## Apa yang masih perlu diperhatikan sebelum masuk skripsi?

1. Baca artikel yang benar-benar akan dikutip. Keberadaan PDF dan ringkasan bukan pengganti membaca bagian yang dijadikan dasar klaim.
2. Pertahankan label versi: Stowell naskah 2021 untuk artikel 2022, Moummad arXiv v8 2026, dan preprint lain sebagaimana tabel.
3. Jangan mengutip detail full-text Putra atau Fluss yang belum tersedia. Gunakan pendamping yang sudah dibaca untuk penjelasan konsep sesuai batasnya.
4. Cocokkan sitasi akhir pada naskah dengan sumber primer dan daftar pustaka yang benar. Tabel aktif memuat jurnal, prosiding, dan preprint, bukan seluruhnya jurnal.
5. Konfirmasikan fokus kebaruan sebagai evaluasi spesifik protokol TA. Penelusuran ini belum membenarkan klaim “belum pernah ada di dunia”.

Paket belajar berada di [learning/PAKET_BELAJAR_UJIAN](../../learning/PAKET_BELAJAR_UJIAN/README.md). Pembaruan lanjutan ini menambah catatan pemeriksaan serta bahan belajar; tidak mengubah kode atau hasil eksperimen.
