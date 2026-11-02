# Pemeriksaan penambahan referensi — 3 November 2026

Enam artikel terbitan jurnal ditambahkan untuk menutup kebutuhan dasar teori BAB II. Identitas setiap artikel dibandingkan dengan metadata DOI/Crossref dan isi PDF, bukan hanya nama berkas. Seluruh PDF dapat dibuka, mempunyai teks yang dapat diperiksa, dan mempunyai hash berbeda dari 26 PDF lama. Salinan PDF tidak dibuat ulang atau diganti dengan ringkasan.

| ID | Artikel | Sumber PDF dan versi | Penggunaan yang sesuai |
|---|---|---|---|
| 35 | Davis dan Mermelstein (1980), *Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences*, DOI [10.1109/TASSP.1980.1163420](https://doi.org/10.1109/TASSP.1980.1163420) | Salinan artikel terbit, 10 halaman, dari [University of Illinois](https://courses.physics.illinois.edu/ece417/fa2017/davis80.pdf). | Dasar representasi mel-frequency cepstrum/MFCC; konteks ucapan tidak dianggap bukti kinerja audio burung. |
| 36 | Efron (1979), *Bootstrap Methods: Another Look at the Jackknife*, DOI [10.1214/aos/1176344552](https://doi.org/10.1214/aos/1176344552) | Salinan artikel terbit dari [University of Helsinki](https://blogs.helsinki.fi/bk-club/files/2012/05/Efron_Bootstrap_AS1979.pdf), 27 halaman PDF termasuk sampul JSTOR; isi jurnal halaman 1-26. | Dasar bootstrap/resampling, dengan unit sampling berpasangan tetap mengikuti rancangan TA. |
| 37 | Peeters dkk. (2011), *The Timbre Toolbox: Extracting audio descriptors from musical signals*, DOI [10.1121/1.3642604](https://doi.org/10.1121/1.3642604) | Salinan artikel terbit JASA, 15 halaman, dari [laboratorium penulis McGill](https://www.mcgill.ca/mpcl/files/mpcl/peeters_2011_jasa.pdf). | Definisi deskriptor temporal/spektral, termasuk centroid dan spread; bukan pembuktian sebab kegagalan retrieval. |
| 38 | Salton, Wong, dan Yang (1975), *A vector space model for automatic indexing*, DOI [10.1145/361219.361220](https://doi.org/10.1145/361219.361220) | Salinan artikel terbit Communications of the ACM, 8 halaman, dari [bahan kuliah Openlib](https://openlib.org/home/krichel/courses/lis618/readings/salton75.pdf). | Landasan representasi dan perbandingan vektor untuk retrieval. Pembobotan istilah teks tidak disamakan dengan embedding audio. |
| 39 | Moffat (2022), *Batch Evaluation Metrics in Information Retrieval: Measures, Scales, and Meaning*, DOI jurnal [10.1109/ACCESS.2022.3211668](https://doi.org/10.1109/ACCESS.2022.3211668) | [Naskah penulis arXiv:2207.03103v1](https://arxiv.org/pdf/2207.03103v1), 7 Juli 2022, 30 halaman. **Bukan PDF versi penerbit.** Publikasi jurnal IEEE Access 10:105564-105577 diverifikasi melalui DOI/Crossref. | Makna dan interpretasi metrik ranking, termasuk AP dan reciprocal rank; rumus AP@k TA tetap dicocokkan dengan kode. |
| 40 | van Merrienboer dkk. (2024), *Birds, bats and beyond: evaluating generalization in bioacoustics models*, DOI [10.3389/fbirs.2024.1369756](https://doi.org/10.3389/fbirs.2024.1369756) | [PDF penerbit Frontiers](https://www.frontiersin.org/journals/bird-science/articles/10.3389/fbirs.2024.1369756/pdf), 16 halaman, tipe Review. | Pendamping jurnal untuk evaluasi dan generalisasi bioakustik. Tidak dihitung sebagai pembanding empiris independen yang identik dengan preprint BIRB 2023. |

Metadata DOI lengkap diambil melalui layanan Crossref. Untuk ID 36 dan 37 permintaan awal sempat gagal, kemudian permintaan ulang berhasil; tidak ada metadata yang diganti dengan judul atau DOI buatan. Endpoint penerbit yang mengembalikan HTML atau galat tidak disimpan sebagai PDF. Identitas naskah Moffat memerlukan normalisasi ligatur PDF pada nama penulis; pemeriksaan tidak mengubah PDF aslinya.

## Dampak pada berkas referensi

- CSV dan Excel bertambah dari 28 menjadi **34 entri**; 28 baris lama dibandingkan dan tetap sama.
- Koleksi bertambah dari 26 menjadi **32 PDF unik**; kedua entri lama tanpa PDF tetap ditandai sesuai statusnya.
- Jumlah sumber 2022-2026 menjadi **23**, sedangkan **11** sumber lebih lama dipertahankan sebagai landasan.
- Indeks `extracted_texts_all.txt` diperbarui menjadi 32 PDF: hasil ekstraksi 26 sumber lama dipertahankan, lalu teks enam PDF baru ditambahkan.
- BibTeX berisi **17 entri**: sepuluh sumber yang telah dikutip BAB I, enam tambahan di atas, dan Lostanlen (2019) dari koleksi lama untuk rencana 2.1. Tabel 2.1 masih kosong dan tidak diberi sitasi yang mengesankan isinya sudah ditelaah/ditulis.
- Sumber unduhan, versi, jumlah halaman dan SHA-256 terdapat pada [audit JSON](VERIFIKASI_TAMBAHAN_2026-11-03.json).

Penambahan pustaka tidak mengubah audio, manifes, parameter, kode eksperimen, atau hasil E0-E5. Sumber lama tidak disebut sebagai penelitian terbaru. Ketersediaan file dan kecocokan identitas tidak berarti seluruh klaim metodologis setiap artikel telah diaudit secara independen.
