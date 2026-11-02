# Revisi latar belakang dan penjelasan kontribusi — 2 November 2026

Catatan pendamping untuk Fabio. Latar belakang pada `chapters/bab1.tex` mempertahankan uraian dan gaya penyampaian sebelumnya, dengan perapian hubungan antarparagraf dan penghapusan pengulangan. Rumusan Masalah, Tujuan, Batasan Penelitian, serta pengaturan format dipertahankan. Perbandingan terperinci di bawah disimpan sebagai bahan penjelasan, bukan bahasan atau subbab baru dalam naskah.

## Alur alasan penelitian

Paragraf pembuka berangkat dari konteks keanekaragaman hayati, kemudian menghubungkannya dengan informasi keberadaan/aktivitas satwa, manfaat pemantauan perubahan komunitas, dan suara sebagai sumber data. Kebutuhan pemantauan diperkenalkan melalui alur tersebut, bukan langsung dinyatakan pada kalimat pertama. Paragraf berikutnya baru mempersempit pembahasan ke burung dan bukti penerapannya di Indonesia. Dukungan umum pemantauan tetap mengikuti Stowell (2022), sedangkan contoh Indonesia mengikuti Ningrum dkk. (2026). Tidak ditambahkan bahasan khusus kelestarian, pertanian, atau pengendalian hama.

Urutan pembahasan berikutnya dipertahankan: skala dan keragaman data → masalah suara latar → retrieval dan representasi → studi ketahanan derau serta ambang. Tiga paragraf yang mengulang fokus/rancangan dirapikan menjadi dua: pilihan representasi (apa yang dibandingkan) dan rancangan evaluasi (bagaimana perbandingan dilakukan). Penutup menghubungkan rangkaian pengujian dengan aspek ketahanan yang dinilai, lalu kontribusi empirisnya terhadap literatur; kalimat “Oleh karena itu” ditempatkan sesudah hubungan tersebut untuk mengantar arah penelitian. Kalimat penghubung umum yang ditunjuk Fabio tetap dihapus. Pustaka tetap sepuluh sumber dalam urutan semula.

Kalimat tentang keterbatasan waktu dan tenaga ahli ditempatkan setelah contoh besarnya koleksi BirdSet, agar pembuka berakhir pada manfaat pemantauan dan disambung contoh penerapan di Indonesia. Paragraf retrieval kemudian menjelaskan kegunaannya menyediakan kandidat untuk diperiksa lebih lanjut serta alasan menguji kualitasnya saat kueri terganggu. Beban analisis manual menjadi konteks kebutuhan pengolahan rekaman; TA tidak mengukur atau mengklaim penghematan waktu maupun pengurangan beban kerja ahli.

## Hubungan latar belakang dengan rumusan masalah

Judul kerja sudah memuat `Controlled ITERA Field-Noise Mixtures in Indonesian Avifauna` dan tetap digunakan pada sampul. Hubungan kedua konteks diperjelas sebelum rincian protokol: rekaman 20 spesies Indonesia dari Xeno-Canto menjadi target pencarian, sementara rekaman lingkungan ITERA menjadi sumber derau yang dicampurkan secara terkontrol. Pemilihan sumber derau lapangan memberi kondisi gangguan dari rekaman nyata yang dapat ditelusuri, dengan tingkat pencampuran yang diatur. Variasi lima lokasi dinilai dalam protokol berikutnya. Ini hubungan eksperimental antara dua sumber data, bukan bukti semua spesies target direkam atau hidup di ITERA. Dasarnya adalah manifes target dan derau penelitian sendiri, bukan hasil suatu jurnal eksternal. Batas pengujian campuran aditif tetap dinyatakan pada naskah.

Fabio menjelaskan bahwa pemilihan awal berfokus pada rekaman 20 spesies dari Sumatera, lalu cakupan lokasi rekaman diperluas ke Indonesia karena keterbatasan jumlah rekaman. Riwayat ini menjadi alasan cakupan kurasi. Pemeriksaan lanjutan pada 3 November disimpan dalam [catatan persebaran 20 label](PERSEBARAN_20_LABEL_BURUNG_2026-11-03.md): keterkaitan dengan Sumatera perlu membedakan daratan/kepulauan, introduksi, dan cakupan taksonomi lama. Sebaran spesies juga berbeda dari lokasi perekaman tiap klip dan keberadaan spesies di kampus ITERA. Hubungan yang benar-benar diuji adalah respons retrieval ketika kueri yang sama mendapat derau ITERA dengan tingkat SNR atau profil lokasi berbeda. Klaim representativitas derau ITERA terhadap seluruh lingkungan Indonesia dan validasi populasi burung di ITERA tetap di luar bukti yang tersedia.

**Alasan yang disetujui Fabio, 3 November 2026:** ITERA dipilih sebagai sumber derau lapangan lokal untuk menguji ketahanan pencarian secara terkontrol. Alasan ini dimasukkan secara singkat pada paragraf rancangan di BAB I, diikuti cara pencampuran dan perbandingan lima profil lokasi yang sudah ada. Ini penjelasan pilihan rancangan penelitian sendiri, bukan klaim hasil jurnal tentang keterwakilan akustik seluruh Indonesia. Pernyataan bahwa semua target hidup di ITERA atau bahwa kesamaan “burung tropis” membuktikan kesesuaian derau tidak ditambahkan. Frasa “Untuk menelaah koleksi besar” juga diganti dengan pengantar pencarian berdasarkan kemiripan suara. Temuan taksonomi dan ketidaksesuaian metadata pada catatan persebaran tetap dicatat sebagai pemeriksaan terpisah; label dan hasil eksperimen tidak diubah melalui revisi redaksi ini.

| Rumusan masalah | Alasan yang dibangun dalam latar belakang |
|---|---|
| 1 — Perbandingan ketahanan representasi | Literatur membedakan representasi umum dan khusus burung; paragraf pilihan representasi menetapkan MFCC/PANNs/BirdNET sebagai pembanding, lalu rancangan memasangkan kondisi uji. |
| 2 — Perubahan kualitas dan retensi menurut SNR | Bukti gangguan pada pengenalan dan studi toleransi derau mendasari perlunya mengukur perubahan mAP@10 serta retensi terhadap pembanding tanpa derau tambahan. |
| 3 — Penerimaan target dan kontrol pada ambang beku | Literatur menunjukkan pengaruh ambang pada keputusan klasifikasi. Rancangan TA memeriksa ambang kemiripan yang dikalibrasi terpisah lalu dibekukan, dengan penerimaan target dan false accept dinilai terpisah. |
| 4 — Kualitas dan kestabilan antarprofil lokasi | Keragaman kondisi rekaman dan hubungan suara latar dengan kesalahan mendasari pembandingan lima profil derau pada SNR setara, sehingga variasi tidak dibaca dari tingkat SNR saja. |
| 5 — Pola kegagalan | Kualitas agregat belum menjelaskan bentuk kegagalan tiap kasus. Margin, ciri spektral yang tersedia, dan audit pendengaran digunakan sebagai penelaahan pelengkap dalam rancangan, dengan batas deskriptifnya. |

## Pemeriksaan keselarasan dan revisi batasan — 3 November 2026

Alasan ITERA sebagai sumber derau lapangan lokal memperjelas pilihan rancangan tanpa mengubah lima pertanyaan dan lima tujuan. Pertanyaan/tujuan 1 membandingkan representasi; 2 menilai perubahan dan retensi menurut SNR; 3 mengevaluasi ambang beku; 4 membandingkan profil lokasi; 5 menelaah kegagalan. Semua aspek tetap dijelaskan pada latar belakang yang telah disetujui Fabio.

Atas persetujuan Fabio, bagian 1.4 diperjelas pada tiga tempat:

- Poin 1 menyebut **20 label spesies burung yang terdapat di Indonesia, sesuai metadata dan manifes yang dibekukan**, karena cakupan label arsip tidak selalu sama dengan taksonomi terbaru. Negara asal rekaman dibedakan dari persebaran spesies. Catatan kaki lokasi yang sempat ditambahkan kemudian dihapus atas permintaan Fabio; hasil verifikasi tetap disimpan dalam [audit lokasi](../../../docs/research/audits/xc_location_20261103/README.md).
- Poin 3 menyatakan relevansi berdasarkan **kesamaan label spesies**, sesuai unit penilaian pada eksperimen yang sudah dijalankan.
- Poin 5 membatasi kesimpulan pada korpus target dan profil derau ITERA yang digunakan. Tidak dibuat klaim keterwakilan nasional, keberadaan semua target di ITERA, atau validasi rekaman burung in-situ.

Revisi ini tidak mengubah latar belakang yang disetujui, Rumusan Masalah, Tujuan, sumber/manifes data, label, maupun hasil eksperimen. Verifikasi lanjutan berhasil mengakses kelima halaman dan API resmi: ketidaksesuaian negara/lokasi juga ada pada sumber, sedangkan koordinat berada di Malaysia menurut geometri batas negara yang diperiksa. Fabio menerima penggunaan rekaman lintas negara untuk spesies yang terdapat di Indonesia, sehingga kelimanya dipertahankan dalam korpus asli. Penegasan cakupan setelah hasil tersedia dicatat pada audit; tidak diklaim sebagai pemeriksaan geografis sebelum eksperimen. Pemetaan ulang taksonomi atau penilaian korpus yang mengecualikan rekaman tersebut belum dilakukan.

## Kontribusi yang ditonjolkan

1. **Bukti ketahanan retrieval dalam pengujian berpasangan.** MFCC, PANNs, dan BirdNET diuji pada 311 kueri dan 673 galeri dengan 20 label spesies sesuai metadata dan manifes yang dibekukan. Kueri yang sama mendapat penambahan derau ITERA pada empat SNR. Kualitas mAP@10 dan retensinya terhadap pembanding tanpa derau tambahan dibaca bersama, sehingga mutu awal tidak tertukar dengan proporsi yang bertahan.
2. **Pemisahan kualitas pencarian dan perilaku ambang beku.** Ambang tiap representasi berasal dari kalibrasi bersih terpisah. Penerimaan target dan penerimaan keliru kontrol di luar target dilaporkan terpisah ketika ambang tersebut dipakai pada kueri bising. Penerimaan target tidak otomatis berarti spesies Top-1 benar.
3. **Evaluasi variasi profil derau lima lokasi.** Pada SNR yang sama, kualitas absolut dan retensi relatif dibandingkan bersama analisis sensitivitas komposisi lokasi. Kesimpulan kestabilan tidak hanya didasarkan pada satu skala metrik. Reformulasi H3 dan interpretasi H4 tetap eksploratif sebagaimana riwayat penelitian.
4. **Penjelasan bentuk kegagalan yang dapat ditelusuri.** Margin, ciri spektral yang tersedia, dan audit pendengaran 120 kasus pilihan melengkapi skor agregat. Audit satu pendengar bersifat deskriptif, tidak mengesahkan spesies secara independen, dan tidak membuktikan penyebab kegagalan.

Identitas rekaman, catatan pencampuran, artefak hasil, dan analisis berpasangan menjadi dukungan keterlacakan. Penggunaan kosinus, model beku, SNR, atau bootstrap secara sendiri-sendiri tidak diklaim sebagai metode baru. Kontribusi TA merupakan bukti empiris dan gabungan rancangan evaluasi pada konteks/protokol tersebut; penelusuran ini bukan tinjauan sistematis yang membuktikan belum ada studi serupa di seluruh dunia.

## Perbandingan dengan penelitian terdahulu

| Penelitian | Hal yang sudah diteliti | Pembeda evaluasi TA |
|---|---|---|
| [Ghaffari dan Devos, 2024](https://doi.org/10.1016/j.ecoinf.2024.102573), Ecological Informatics | Bagian 2.7 menggunakan delapan kelas gangguan ESC-50; bagian 3.3 (*Noise tolerance*) mengevaluasi frontend pengenalan spesies pada beberapa SNR. Kode penulis juga menyediakan `noisy_validate`. | Uji SNR bukan temuan baru TA. TA menilai ranking rekaman dengan representasi yang dibekukan, galeri tetap, mAP@10/retensi, serta keputusan ambang kemiripan. Derau berasal dari bank lapangan ITERA. |
| [Hamer dkk., BIRB, 2023](https://arxiv.org/abs/2312.07439v2), preprint | Bagian 3.2 dan 4 mengevaluasi retrieval/generalization, termasuk focal-to-soundscape, dengan baseline nearest-centroid. | TA mengikuti perubahan kueri yang sama saat derau ditambahkan secara terkontrol terhadap galeri tetap. Ini pertanyaan yang lebih terbatas, bukan evaluasi in-situ yang lebih realistis daripada BIRB. |
| [Ghani dkk., 2023](https://doi.org/10.1038/s41598-023-49989-z), Scientific Reports | Bagian *Linear probes on feature embeddings* membekukan embedding dan melatih satu lapisan klasifikator untuk tugas baru. | TA memakai representasi untuk mengurutkan rekaman galeri serta mengukur respons terhadap gangguan, tanpa melatih klasifikator downstream baru. Pembekuan model sendiri bukan pembeda baru. |
| [Fairbairn dkk., 2025](https://doi.org/10.1371/journal.pone.0330836), PLOS ONE | Metode *Parameter effects* dan *Temporal aggregation* menelaah pengaturan BirdNET, ambang confidence, serta ketepatan daftar spesies dibanding pakar. | TA mengkalibrasi ambang kemiripan pada subset terpisah, membekukannya, lalu memisahkan penerimaan target dan false accept kontrol pada kondisi bising. Skor confidence dan kosinus berbeda. |
| [Clark dkk., 2023](https://doi.org/10.1016/j.ecoinf.2023.102065), Ecological Informatics | Analisis 37 spesies mengaitkan komposisi soundscape dengan kesalahan klasifikasi. | TA menambahkan derau pada kueri acuan secara terkontrol dan mendeskripsikan pola kegagalan retrieval, dengan batas campuran aditif. Analisis TA tidak mengisolasi sebab ekologis atau frekuensi tertentu. |

Sebagai pemeriksaan pembatas klaim, [Miron dkk. (2025), *What Matters for Bioacoustic Encoding*, arXiv:2508.11845v1](https://arxiv.org/html/2508.11845v1), bagian 3.3–3.4, juga sudah menggabungkan pelatihan dengan noise augmentation dan evaluasi retrieval kosinus lintas banyak dataset. Kajian tersebut semakin menegaskan bahwa kosinus, embedding, atau penambahan derau tidak layak diklaim sebagai inovasi tunggal TA. Perbandingan ini tidak dimasukkan sebagai paragraf tambahan pada BAB I agar latar belakang tetap ringkas.

## Bukti internal untuk klaim rancangan

- [Manifes target](../../../data/manifests/dataset_split.csv): 20 label spesies, galeri 673, kueri 311, kalibrasi 232.
- [E2 dan validasinya](../../../results/reproductions/E2_controlled_20261012T021600_897497Z/validation_report.json): identitas kueri berpasangan pada pembanding dan empat SNR, dengan audit SNR serta sumber derau.
- [E3](../../../results/tables/13_e3_threshold_transfer.csv): penerimaan target dan penerimaan keliru kontrol pada ambang beku.
- [Revisi sensitivitas H3](../../../docs/REVISION_SUPERVISOR_2026-10-15.md): ayunan absolut/relatif, komposisi lokasi, dan batas inferensi.
- [Audit pendengaran E5](../../../Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md): 120/120 kasus mempunyai catatan satu pendengar.

Sumber primer ditelaah melalui teks PDF lokal, halaman penerbit, naskah penulis, dan repository kode penulis. Kalimat yang diminta dihapus tidak dipertahankan. Sepuluh kunci sitasi dan urutannya tidak berubah; daftar pustaka dibangun ulang dengan `unsrt`.
