# Catatan istilah BAB I untuk Fabio

Disiapkan 31 Oktober 2026. Catatan ini bahan belajar pribadi, terpisah dari naskah skripsi. Contoh angka pada bagian latihan adalah ilustrasi, bukan hasil eksperimen.

## 1. Pahami satu kalimat penelitian kita dahulu

**Kita menguji cara mengubah suara burung menjadi angka yang paling membantu komputer mencari rekaman sejenis ketika contoh suara ditambahkan gangguan.** Model yang sudah dilatih dipakai dengan bobot tetap. Kita membandingkan hasil pencariannya, bukan melatih model burung baru.

Istilah pada naskah adalah **representasi audio beku untuk temu kembali**. Kata “beku” menjelaskan bobot model yang tidak dilatih ulang. File suara tetap berupa rekaman biasa. Ketika suara ditambah derau, vektor hasil ekstraksinya dapat berubah meskipun bobot model tetap. Ini berlaku pada model audio R1/R2; R3 hanya menggunakan ID.

Contoh cerita: Fabio memiliki satu contoh suara burung dan koleksi rekaman referensi. Komputer mengubah keduanya menjadi vektor, membandingkan kemiripannya, lalu menyusun urutan hasil. Kita memeriksa apakah rekaman berspesies sama muncul di urutan atas dan apakah skor hasil melewati ambang penerimaan. Langkah itu diulangi ketika contoh suara diberi derau pada kondisi terkontrol.

## 2. Istilah tentang data dan pencarian

| Istilah | Arti sederhana | Relevansi untuk TA Fabio |
|---|---|---|
| Bioakustik | Kajian suara makhluk hidup. | Objek kita adalah rekaman suara burung. |
| Biodiversitas / keanekaragaman hayati | Keragaman kehidupan; pada pembahasan ini terutama keragaman jenis burung. | Menjadi konteks manfaat analisis suara; TA tidak menghitung kelimpahan seluruh burung ITERA. |
| Vokalisasi | Suara yang dihasilkan hewan, misalnya kicauan atau panggilan burung. | Suara inilah yang ingin diwakili oleh fitur audio. |
| Pemantauan akustik pasif / PAM | Perekam mengumpulkan suara lingkungan tanpa peneliti harus terus mendengarkan di tempat. | Menjelaskan kebutuhan pengolahan rekaman. Data burung target TA berasal dari Xeno-Canto; ITERA menyediakan rekaman derau untuk campuran. |
| Focal recording | Rekaman yang dibuat dengan perhatian pada satu sumber target, misalnya seekor burung. Latar masih dapat terdengar. | Menjelaskan jenis kueri sumber; “clean” pada eksperimen berarti tidak ditambah derau, bukan pasti tanpa latar. |
| Soundscape | Keseluruhan suasana suara di suatu tempat, termasuk hewan, angin, kendaraan, dan sumber lain. | E4 mencampur kueri dengan derau lokasi; belum menguji vokalisasi target yang direkam langsung di soundscape ITERA. |
| Dataset / korpus | Kumpulan data yang dipakai untuk penelitian. | Korpus target aktif berisi 1.216 rekaman dari 20 spesies. |
| Manifes dan metadata | Manifes adalah daftar rekaman beserta perannya; metadata adalah informasi tentang rekaman, seperti ID, spesies, sumber, dan hash. | Menjadi bukti pembagian data dan asal rekaman. |
| Query / kueri | Contoh suara yang menjadi bahan pencarian. | Ada 311 kueri clean pada partisi aktif. |
| Gallery / galeri | Koleksi rekaman yang dicari oleh sistem. | Ada 673 rekaman galeri; galeri tetap saat kondisi kueri berubah. |
| Calibration / kalibrasi | Data terpisah untuk memilih aturan keputusan sebelum aturan diuji. | Sebanyak 232 target calibration dan 233 unknown calibration digunakan pada E3; ambang lalu dibekukan. |
| Temu kembali / retrieval | Mengambil dan mengurutkan rekaman relevan dari koleksi. Ejaan Inggrisnya **retrieval**, bukan “retribal”. | Ini tugas utama kita. |
| Similarity retrieval | Pencarian berdasarkan skor kemiripan terhadap contoh. | Relevansi hasil TA dinilai dari kesamaan label spesies. Skor mirip tinggi belum selalu berarti spesiesnya sama. |
| Klasifikasi | Memberi label pada masukan, misalnya “burung A”. | Berbeda tugas dari menyusun daftar rekaman galeri. Akurasi klasifikasi jurnal tidak disamakan dengan mAP TA. |
| Top-1 / ranking | Top-1 ialah hasil urutan pertama; ranking ialah keseluruhan urutan hasil. | Top-1 benar berarti spesies hasil pertama sama dengan spesies kueri. |
| Nearest centroid | Membandingkan contoh dengan pusat/rata-rata vektor suatu kelompok. | Ini bagian baseline BIRB. TA kita membandingkan kueri dengan vektor tiap rekaman galeri, jadi istilah ini tidak otomatis menjadi metode TA. |

## 3. Istilah tentang representasi dan model

| Istilah | Arti sederhana | Relevansi untuk TA Fabio |
|---|---|---|
| Representasi / fitur audio | Cara menggambarkan suara sebagai angka agar dapat dihitung komputer. | Suara yang sama diolah melalui R0, R1, dan R2. |
| Vektor / embedding | Deretan angka yang mewakili karakteristik suatu masukan. Bayangkan “ringkasan angka” dari rekaman, bukan salinan bunyinya. | Vektor kueri dibandingkan dengan vektor galeri. Tiap angka embedding tidak harus mempunyai arti fisik yang dapat diberi nama. |
| Dimensi | Banyaknya angka dalam satu vektor. | R0 dan R3 berdimensi 40; R1 2.048; R2 1.024. Dimensi besar tidak otomatis memberi hasil lebih baik. |
| Encoder | Bagian pengolah yang menghasilkan representasi dari audio. | Pada R1/R2, hasilnya berupa embedding. Kepala klasifikasi asli model tidak menjadi aturan pemeringkatan galeri TA. |
| Pralatih / pretrained | Model sudah mempelajari pola dari data sebelum penelitian kita. | Kita memakai bobot PANNs/BirdNET yang tersedia. |
| Bobot dan model beku / frozen | Bobot ialah parameter yang dipelajari model. “Beku” berarti bobot itu tidak diperbarui saat eksperimen kita. | Model tetap dapat menghasilkan embedding berbeda ketika audionya berubah. R0 adalah perhitungan MFCC, bukan model pralatih. |
| Fine-tuning | Melanjutkan pelatihan untuk mengubah bobot model pada data baru. | Tidak dilakukan pada encoder R1/R2 TA ini. |
| MFCC | Ringkasan karakteristik spektral suara. Implementasi TA merangkum 20 koefisien melalui mean dan simpangan baku menjadi 40 angka. | R0, pembanding akustik klasik. |
| PANNs CNN14 | Model audio umum yang dipralatih pada AudioSet. | R1, pembanding dari domain suara umum. |
| BirdNET | Keluarga model pengenalan suara burung. | R2 memakai checkpoint v2.4 untuk menghasilkan representasi. Spesifikasi artikel BirdNET 2021 tidak otomatis sama dengan checkpoint ini. |
| Kontrol acak deterministik / R3 | Vektor acak yang dapat dihasilkan kembali dari ID dan seed yang sama. | Tidak membaca waveform. Skor R3 yang tetap ketika SNR berubah bukan bukti tahan derau. |
| Cosine similarity | Ukuran kemiripan arah dua vektor. | Dibandingkan dalam ruang representasi yang sama: kueri R1 dengan galeri R1, misalnya. Skornya bukan probabilitas spesies benar. |
| Frontend | Bagian awal pengolahan audio menjadi bentuk yang siap dipakai model. | Muncul pada studi Ghaffari–Devos; TA tidak mengimplementasikan semua frontend dalam studi itu. |
| Generalisasi | Kemampuan tetap bekerja ketika data/kondisi uji berbeda dari kondisi yang dipelajari atau diuji sebelumnya. | Hasil pada campuran yang diuji belum membuktikan kemampuan pada semua lokasi atau rekaman lapangan baru. |

## 4. Istilah tentang derau dan keputusan

| Istilah | Arti sederhana | Relevansi untuk TA Fabio |
|---|---|---|
| Derau / noise | Suara yang diperlakukan sebagai gangguan terhadap suara target. | Kita menggunakan rekaman lingkungan ITERA untuk campuran. Identitas sumber latar tidak ditebak sebagai fakta hanya dari nama lokasi. |
| SNR | Perbandingan daya sinyal acuan dengan daya derau. SNR rendah berarti gangguan relatif lebih kuat. | Pada +20 dB, daya acuan 100 kali daya derau; 0 dB berarti setara; pada −5 dB, daya derau sekitar 3,16 kali daya acuan. Acuannya sinyal kueri yang sudah diproses, bukan pemisahan sempurna suara burung murni. |
| Campuran aditif | Menjumlahkan sinyal kueri dengan derau yang telah diatur skalanya. | Sumber audio nyata dicampur secara digital agar tingkat gangguan terkontrol. Ini tidak memodelkan seluruh propagasi/reverberasi lapangan. |
| Profil derau | Karakter gangguan, termasuk persebaran energinya pada frekuensi berbeda. | E4 membandingkan profil dari lima lokasi; perbedaan hasil tidak otomatis membuktikan penyebabnya serangga atau frekuensi tertentu. |
| Ambang / threshold / tau | Batas skor untuk mengambil keputusan. Contoh: hasil dengan skor setidaknya tau diterima. | E3 memilih satu tau untuk setiap representasi dari calibration-clean. |
| Ambang beku | Nilai tau yang sudah dipilih tidak disetel ulang berdasarkan hasil uji bising. | Memungkinkan kita mengamati perubahan penerimaan/penolakan pada aturan yang sama. Berbeda arti dengan bobot model beku. |
| Confidence / skor kepercayaan | Skor keluaran klasifikator yang digunakan untuk keputusan model itu. | Confidence pada jurnal Fairbairn berbeda dari skor cosine TA. Nilai yang sama tidak berarti kedua skor setara. |
| Known / unknown / open-set | Known ialah kelompok spesies target; unknown ialah kontrol di luar target, termasuk derau; open-set mengizinkan sistem menolak masukan. | E3 menguji penerimaan target dan penerimaan keliru unknown secara terpisah. |
| Agregasi waktu | Menggabungkan hasil dari rentang waktu tertentu. | Empat tingkat agregasi pada Fairbairn bukan empat tingkat SNR TA. |
| Normalisasi dan kompresi | Normalisasi mengatur skala; kompresi memperkecil rentang nilai besar–kecil. | Operasinya bergantung metode. RMS pada praproses TA, normalisasi L2 vektor, dan kompresi frontend jurnal adalah operasi berbeda. |

## 5. Jangan tertukar membaca jenis kesalahan dan metrik

| Istilah | Arti sederhana dan batasnya |
|---|---|
| False positive | Secara umum, sistem menyatakan sesuatu ada/positif padahal seharusnya tidak. Pada studi deteksi spesies, contohnya spesies A dinyatakan hadir padahal tidak ada. |
| False negative | Sistem tidak menemukan/menolak sesuatu yang seharusnya positif. Definisi tepat mengikuti tugas dan label yang diuji. |
| False accept / FAR / FPR E3 | Kontrol unknown melewati tau dan diterima sebagai target. Ini tidak sama dengan semua hasil Top-1 yang salah spesies. |
| False rejection E5 | Pada label operasional E5, Top-1 sudah benar spesiesnya tetapi skor di bawah tau. Ini lebih khusus daripada semua known yang ditolak dalam E3. |
| Confusion E5 | Top-1 berbeda spesies dan skor melewati tau. Sistem menerima hasil pertama yang salah. |
| Collapse E5 | Top-1 berbeda spesies dan skor di bawah tau. Nama “collapse” tidak membuktikan sepuluh hasil semuanya salah. |
| Precision | Bagian hasil yang dinyatakan positif/relevan yang ternyata benar. Penyebut bergantung tugas: hasil deteksi atau k hasil retrieval, misalnya. |
| Recall | Bagian item positif/relevan yang berhasil ditemukan. **Recall@10** menghitung rekaman relevan yang ditemukan di 10 hasil atas. **Recall penerimaan E3** menghitung known yang melewati tau; tidak mensyaratkan spesies Top-1 benar. |
| F1 | Ringkasan keseimbangan precision dan recall. F1 = 0,84 tidak otomatis berarti akurasi 84%. |
| AP@10 dan mAP@10 | AP@10 menilai urutan hasil relevan untuk satu kueri; mAP@10 merata-ratakannya pada kueri. Nilai mAP 0,63 tidak dibaca sebagai “63% spesies teridentifikasi”. |
| Retensi | Bagian skor clean yang masih bertahan pada kondisi bising, misalnya mAP bising dibagi mAP clean. |
| Bootstrap / CI | Bootstrap menghitung ulang statistik dari sampel ulang; CI menyatakan rentang ketidakpastian menurut prosedur dan asumsi itu. Pada H3, query diambil ulang secara berpasangan, sementara lokasi/segmen noise tetap. |

### Contoh empat keputusan E5

**Ilustrasi saja:** anggap tau = 0,70. Angka ini tidak menggantikan tau aktual tiap representasi.

| Spesies hasil Top-1 | Skor | Label E5 |
|---|---:|---|
| Sama dengan kueri | 0,80 | Accepted correct: benar dan diterima |
| Sama dengan kueri | 0,60 | False rejection: benar tetapi ditolak |
| Berbeda dari kueri | 0,80 | Confusion: salah tetapi diterima |
| Berbeda dari kueri | 0,60 | Collapse: salah dan ditolak |

Jadi, **“hasil pencariannya benar”** dan **“hasilnya diterima”** menjawab pertanyaan yang berbeda. Inilah alasan E2 dan E3 dilaporkan terpisah.

## 6. Cara menjelaskan penelitian dalam bahasa sendiri

“Saya membandingkan MFCC, PANNs, dan BirdNET untuk mencari rekaman burung yang sejenis dengan contoh suara. Contoh yang sama saya uji pada beberapa tingkat gangguan dari rekaman derau ITERA, dengan koleksi referensi tetap. Saya juga memeriksa apakah aturan penerimaannya berubah perilaku ketika suara bising dan seperti apa kegagalannya. Model pralatih tidak saya latih ulang. Kesimpulan saya terbatas pada campuran yang diuji.”

Sebelum bimbingan, coba jelaskan tiga pasangan ini: **kueri–galeri**, **model beku–ambang beku**, dan **Top-1 benar–hasil diterima**. Jika ketiganya sudah jelas, alur utama TA akan lebih mudah diikuti.

## 7. Sumber untuk memeriksa kembali

Definisi sederhana di atas merujuk konteks naskah dan implementasi, bukan kutipan langsung. Untuk konteks penelitian terdahulu, gunakan kunci sitasi pada [references.bib](../references.bib): Stowell, BIRB, Ghani, Ghaffari–Devos, dan Fairbairn. Nomor sitasi dapat berubah ketika urutan naskah berubah; kunci referensinya tetap.

- [Audit klaim latar belakang](AUDIT_KLAIM_LATAR_BELAKANG_2026-10-31.md) menghubungkan klaim dengan bukti.
- [Pembagian data](../../../data/manifests/dataset_split.csv), [unknown](../../../data/manifests/unknown_open_set_manifest.csv), dan [kode representasi](../../../src/embeddings.py) menjelaskan istilah dalam implementasi aktif.
- [Kode retrieval](../../../src/retrieve.py), [ambang](../../../src/calibrate_threshold.py), dan [diagnostik E5](../../../scripts/run_e5_diagnostics.py) menjadi acuan definisi metrik/label operasional.
- [Paket belajar dan hitungan](../../../learning/PAKET_BELAJAR_UJIAN/README.md) menyediakan latihan lebih lengkap.

## 8. Kemiripan kosinus: bagaimana komputer membandingkan suara kita?

**Kosinus di sini membandingkan arah dua vektor fitur, bukan menghitung kemiripan dari nama spesies atau membandingkan keras suara saja.** Bayangkan tiap vektor sebagai panah yang berawal dari titik nol. Panah yang arahnya makin berdekatan mendapat skor kosinus makin tinggi. Gambar panah dua dimensi hanya alat bantu; vektor penelitian kita berisi puluhan sampai ribuan angka.

Alur dalam TA:

1. Ambil satu potongan suara kueri dan potongan suara pada galeri.
2. Ekstrak keduanya dengan representasi yang sama, misalnya BirdNET untuk kueri dan BirdNET untuk semua rekaman galeri.
3. Samakan panjang matematis vektornya melalui normalisasi L2. Ini berbeda dari menyamakan durasi rekaman.
4. Hitung skor kosinus antara kueri dan setiap rekaman galeri.
5. Urutkan skor dari terbesar ke terkecil. Rekaman dengan skor terbesar menjadi Top-1.
6. Gunakan metadata spesies untuk menilai apakah hasilnya benar. Untuk keputusan penerimaan, bandingkan skor tertinggi dengan ambang.

**Komputer tidak memakai label spesies kueri untuk memilih urutan.** Label itu dipakai saat menilai hasil setelah urutan terbentuk. Dalam TA, kueri PANNs dibandingkan dengan galeri PANNs; kueri BirdNET dengan galeri BirdNET. Koordinat dari model berbeda tidak langsung dicampurkan dalam satu perhitungan kosinus.

### Rumus dengan bahasa sederhana

Untuk vektor bukan nol:

`cosine(q, g) = (q · g) / (panjang(q) × panjang(g))`

- `q` adalah vektor kueri dan `g` adalah vektor satu rekaman galeri.
- `q · g` disebut hasil kali titik atau *dot product*: kalikan angka yang posisinya sama, lalu jumlahkan.
- Panjang L2 vektor `[a, b]` adalah `akar(a² + b²)`.
- Jika kedua vektor sudah dinormalisasi menjadi panjang 1, skor cukup dihitung melalui hasil kali titik.
- Secara matematis, skor berada pada rentang -1 sampai 1: 1 berarti arah sama, 0 berarti tegak lurus, dan -1 berarti berlawanan arah. Skor negatif bukan berarti gelombang suara pasti saling membatalkan.

Skor **0,90 tidak berarti peluang benar 90%**. Skor tinggi juga belum membuktikan spesies sama. Keberhasilan harus diperiksa terhadap metadata acuan.

### Latihan angka: satu kueri dan tiga rekaman galeri

Semua angka berikut **ilustrasi dua dimensi, bukan embedding atau hasil eksperimen asli**. Misalkan `q = [3, 4]`, sehingga panjangnya `akar(9 + 16) = 5`.

| Rekaman galeri | Vektor ilustrasi | Hasil kali titik dengan q | Panjang vektor | Skor kosinus |
|---|---|---:|---:|---:|
| A | `[6, 8]` | `3×6 + 4×8 = 50` | 10 | `50 / (5×10) = 1,00` |
| B | `[4, 3]` | `3×4 + 4×3 = 24` | 5 | `24 / (5×5) = 0,96` |
| C | `[4, -3]` | `3×4 + 4×(-3) = 0` | 5 | `0 / (5×5) = 0,00` |

Urutan hasilnya A, B, lalu C. Vektor A dua kali lebih panjang daripada q, tetapi arahnya sama, sehingga skornya 1. Setelah normalisasi, q dan A sama-sama menjadi `[0,6; 0,8]`. Normalisasi B menghasilkan `[0,8; 0,6]`.

**Batas contoh:** mengalikan vektor dengan bilangan positif tidak mengubah arah. Ini tidak membuktikan bahwa memperkeras audio sebelum masuk model pasti menghasilkan embedding atau skor yang sama; pengolahan audio dan model juga berperan.

### Hubungannya dengan penambahan derau

Misalkan setelah derau ditambahkan, model menghasilkan vektor kueri baru `q_bising = [4, 3]`. Pada ilustrasi ini, skor terhadap A menjadi 0,96 dan terhadap B menjadi 1,00. Urutan teratas berpindah dari A ke B, walaupun vektor galeri tetap.

Jika A sejenis dengan kueri sedangkan B berbeda spesies, perubahan urutan itu menjadi kegagalan pencarian. Namun, derau tidak selalu menurunkan skor atau membalik urutan pada setiap rekaman. Itulah yang harus diukur melalui eksperimen, bukan diasumsikan dari contoh ini. Bobot model yang beku juga tidak membuat embedding kueri selalu tetap ketika suaranya berubah.

### Hubungannya dengan ambang dan margin

**Ilustrasi terpisah:** anggap ambang `tau = 0,97`.

| Skor tertinggi | Margin `skor - tau` | Keputusan |
|---:|---:|---|
| 1,00 | +0,03 | Diterima |
| 0,96 | -0,01 | Ditolak |
| 0,97 | 0,00 | Diterima, karena aturan menggunakan `skor >= tau` |

Margin adalah jarak bertanda dari skor ke batas keputusan, bukan selisih skor peringkat pertama dan kedua. Nilai dekat nol berarti dekat batas penerimaan. **Diterima tidak menjamin spesies Top-1 benar**, dan ditolak tidak selalu berarti Top-1 salah. Tau dipilih terpisah untuk tiap representasi; jangan mengganti tau aktual dengan angka ilustrasi ini.

## 9. Istilah tambahan pada rumusan masalah, tujuan, dan batasan

| Istilah | Penjelasan sederhana | Hubungan dengan TA |
|---|---|---|
| Prapemrosesan | Menyiapkan suara sebelum pengambilan fitur. | Audio diseragamkan ke mono, 32 kHz, dan panjang lima detik; tingkat RMS juga diatur. |
| Mono | Satu saluran audio. | Menyeragamkan masukan dari rekaman yang mungkin memiliki jumlah saluran berbeda. |
| Sample rate / laju pencuplikan | Banyaknya nilai gelombang suara yang disimpan per detik. | 32 kHz berarti 32.000 sampel per detik; lima detik berisi 160.000 sampel. Ini bukan jumlah rekaman atau spesies. |
| Waveform / sinyal audio | Deretan nilai amplitudo suara sepanjang waktu. | Berbeda dari embedding, yang merupakan ringkasan fitur hasil pengolahan. |
| RMS | Akar dari rata-rata kuadrat amplitudo; ukuran tingkat sinyal. | Normalisasi RMS mengatur skala sinyal. Ini bukan pemisahan suara burung dari latarnya. |
| Normalisasi L2 | Membagi semua angka vektor dengan panjang matematisnya sehingga panjangnya menjadi 1, untuk vektor bukan nol. | Memudahkan perhitungan kemiripan kosinus. Berbeda dari normalisasi RMS pada waveform. |
| Relevansi | Kesesuaian hasil dengan kebutuhan pencarian menurut aturan penilaian. | Dalam TA, hasil relevan jika spesies pada metadata sama dengan spesies kueri. Skor kosinus tidak dipakai sebagai label kebenaran. |
| Koleksi referensi tetap | Rekaman dan vektor galeri tidak diubah mengikuti kondisi derau kueri. | Membantu membandingkan pengaruh perubahan kueri pada koleksi yang sama. |
| Desibel / dB | Cara logaritmik menyatakan suatu perbandingan. | SNR -5 dB bukan volume negatif: daya derau lebih besar daripada daya sinyal acuan. |
| Frekuensi / spektrum | Frekuensi menggambarkan banyaknya getaran per detik; spektrum menggambarkan sebaran komponen frekuensi suatu sinyal. | Ciri spektral merangkum karakter frekuensi, tetapi tidak otomatis menyatakan jenis burung atau sumber derau. |
| Spectral centroid | Rata-rata frekuensi yang diberi bobot menurut besar spektrumnya, seperti titik keseimbangan spektrum. | Menjadi petunjuk deskriptif karakter suara. Nilai tinggi tidak membuktikan suara serangga. |
| Spectral bandwidth | Ukuran sebaran frekuensi di sekitar pusat spektrum. | Membantu mendeskripsikan lebar sebaran suara; bukan lebar pita internet. |
| Kualitas absolut | Nilai metrik asli pada suatu kondisi. | Contohnya mAP@10 sebesar 0,40. |
| Retensi relatif | Nilai pada kondisi bising dibagi nilai pembanding tanpa derau tambahan. | Menyatakan bagian kualitas awal yang bertahan, bukan nilai kualitas awal itu sendiri. |
| Ayunan lintas lokasi | Selisih nilai tertinggi dan terendah antarlokasi pada kondisi yang dibandingkan. | Membantu menilai kestabilan; ayunan absolut dan ayunan retensi dapat memberi penilaian berbeda. |
| Analisis sensitivitas | Memeriksa apakah interpretasi berubah ketika pilihan analisis tertentu diubah secara terencana dan dilaporkan. | Hasil lima lokasi dibandingkan dengan analisis tanpa Kebun Raya. Lokasi itu tetap dipertahankan dalam data E4 asli. |
| Diagnostik | Pemeriksaan lebih rinci untuk memahami bentuk kegagalan. | Melihat hasil urutan pertama, skor, margin, dan ciri yang tersedia; bukan otomatis menemukan penyebab. |
| Deskriptif | Menjelaskan apa yang terlihat atau tercatat pada data yang diperiksa. | Audit pendengaran merangkum catatan pada kasus pilihan. |
| Kausal / sebab-akibat | Menyatakan bahwa perubahan satu faktor menyebabkan perubahan hasil. | Hubungan ciri spektral dengan kegagalan belum membuktikan bahwa ciri itu penyebabnya. |
| Generalisasi | Memperluas kesimpulan ke data atau kondisi lain. | Hasil 20 spesies dan campuran yang diuji tidak otomatis berlaku bagi semua burung atau semua lingkungan. |

### Membaca metrik dengan contoh kecil

Semua angka berikut ilustrasi. Misalkan galeri memiliki delapan rekaman yang berspesies sama dengan kueri. Dari sepuluh hasil teratas, hanya peringkat ke-3 dan ke-5 yang relevan.

- **Precision@10 = 2/10 = 0,20:** dua dari sepuluh hasil atas relevan.
- **Recall@10 = 2/8 = 0,25:** dua dari seluruh delapan rekaman relevan ditemukan dalam sepuluh hasil atas.
- **RR = 1/3:** hasil relevan pertama muncul di urutan ketiga. MRR adalah rata-rata RR semua kueri.
- **AP@10**, mengikuti kode TA, menjumlahkan precision pada posisi hasil relevan, lalu membaginya dengan `min(jumlah relevan di galeri, 10)`. Pada contoh ini: `(1/3 + 2/5) / 8 = sekitar 0,0917`. Hasil relevan yang muncul lebih awal membantu menaikkan AP. **mAP@10** adalah rata-rata AP@10 seluruh kueri.
- **Ketepatan Top-1** kueri ini bernilai 0, karena hasil pertama tidak relevan. Ketepatan Top-1 keseluruhan merata-ratakan nilai benar/salah itu pada seluruh kueri.

Angka 10 berarti batas posisi hasil yang diperiksa, bukan sepuluh spesies. Jangan membaca mAP@10 sebesar 0,60 sebagai peluang benar 60% atau enam dari sepuluh spesies teridentifikasi.

### Mengapa kualitas absolut dan retensi perlu dibaca bersama?

Ilustrasi: model A turun dari mAP 0,60 menjadi 0,30, sehingga retensinya 50%. Model B turun dari 0,10 menjadi 0,08, sehingga retensinya 80%. Model B mempertahankan proporsi lebih besar, tetapi model A tetap memiliki kualitas pencarian bising yang lebih tinggi, yaitu 0,30 dibandingkan 0,08. Jadi, retensi tertinggi dan kualitas pencarian tertinggi menjawab pertanyaan berbeda. Retensi juga dapat melebihi 100% jika skor kondisi bising lebih tinggi daripada pembandingnya.

### Mengapa audit 120 kasus tidak mewakili semua kegagalan?

Kasus audit dipilih menurut kelompok representasi, kondisi, dan jenis kegagalan; bukan sampel acak yang proporsinya mewakili seluruh evaluasi. Audit juga memuat audio yang berulang pada beberapa kasus dan dilakukan oleh satu pendengar. Karena itu, misalnya 40 dari 120 kasus berlabel confusion tidak dapat dibaca sebagai tingkat confusion seluruh sistem sebesar 33,3%. Mendengar kicauan belum mengesahkan bahwa sumbernya spesies target pada metadata.

Untuk bimbingan, coba jawab: **“Kosinus memilih hasil berdasarkan apa?”**, **“Apakah skor 0,90 berarti benar 90%?”**, dan **“Apa bedanya hasil benar, hasil diterima, dan suara terdengar?”** Jawaban singkatnya: arah vektor; bukan probabilitas; ketiganya memakai aturan penilaian yang berbeda.
