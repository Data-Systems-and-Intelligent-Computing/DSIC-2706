# 2. Teori dengan bahasa sederhana

## Kamus yang perlu benar-benar dipahami

| Istilah | Penjelasan sederhana |
|---|---|
| Bioakustik | Kajian suara makhluk hidup. |
| Avifauna | Kelompok burung di suatu wilayah. |
| Waveform | Angka amplitudo suara yang berubah terhadap waktu. |
| Amplitudo | Besar nilai sinyal pada satu saat. Bukan frekuensi. |
| Frekuensi / Hz | Banyaknya getaran per detik; berkaitan dengan tinggi-rendah nada. |
| Sample rate | Banyaknya sampel digital per detik; 32 kHz berarti 32.000 sampel/detik. |
| Spektrum | Gambaran komponen frekuensi pada suatu bagian suara. |
| Spektrogram | Gambaran perubahan energi/magnitudo frekuensi dari waktu ke waktu. |
| Frame / jendela | Potongan pendek audio yang dianalisis bertahap. |
| Fitur | Ciri suara yang dinyatakan dengan angka. |
| Representasi / embedding | Vektor angka yang merangkum ciri suara agar dapat dibandingkan. |
| Dimensi | Banyaknya angka di dalam satu vektor. Bukan jumlah spesies. |
| Pretrained | Model sudah dilatih sebelumnya menggunakan data lain. |
| Frozen | Bobot model tidak diperbarui pada penelitian ini. Keluarannya tetap bergantung pada suara masukan. |
| Checkpoint | Berkas berisi keadaan/bobot model yang digunakan. |
| Fine-tuning | Melatih ulang sebagian/seluruh bobot memakai data baru; tidak dilakukan di TA ini. |
| Pooling | Merangkum beberapa nilai/frame, misalnya dengan rata-rata. |
| Kueri / query | Suara contoh yang ingin dicarikan pasangan rekaman sejenis. |
| Galeri / gallery | Koleksi rekaman pembanding. |
| Retrieval | Mengurutkan rekaman galeri berdasarkan kemiripan terhadap kueri. |
| Relevan | Dalam TA: spesies galeri sama dengan spesies kueri. |
| Ground truth | Label acuan yang dipakai untuk memeriksa hasil. |
| Cosine similarity | Skor kesamaan arah dua vektor. |
| SNR | Perbandingan daya sinyal target dan daya derau; dinyatakan dalam dB. |
| Noise / derau | Gangguan relatif terhadap target tugas. Suara serangga juga dapat menjadi derau untuk pencarian burung. |
| Threshold / ambang / τ | Batas skor untuk menerima atau menolak kueri. |
| Known / target | Jenis yang masuk dalam koleksi spesies target. |
| Unknown / non-target | Suara yang tidak mempunyai kelas target di galeri, termasuk kontrol derau murni. |
| Open-set | Pengujian yang mengizinkan masukan dari luar kelas target. |
| Domain shift | Perubahan kondisi/distribusi antara sumber data atau kondisi uji. TA menguji satu bentuk perubahan melalui derau aditif. |
| Bootstrap | Mengambil ulang sampel dengan pengembalian untuk menilai variasi estimasi. |
| CI 95% | Interval ketidakpastian dari prosedur statistik tertentu; bukan jaminan 95% untuk tiap prediksi. |
| Leakage / kebocoran | Informasi dari bagian evaluasi ikut masuk ke pemilihan/pembentukan sistem sehingga hasil terlalu optimistis. |

## Bagaimana suara berubah menjadi hasil pencarian?

**Audio → persiapan klip → campuran derau bila diperlukan → representasi → cosine terhadap galeri → urutan hasil → pengukuran.** Untuk E3, skor terbesar juga dibandingkan dengan ambang.

1. Audio target disiapkan sebagai mono dengan laju dasar 32 kHz dan panjang lima detik. Jika panjang, kode memilih jendela energi terbesar pada langkah yang ditentukan; jika pendek, ditambah nol. Energi terbesar adalah aturan teknis, bukan bukti pasti bahwa hanya suara burung target yang terpilih.
2. RMS dinormalisasi menuju 0,05. Implementasi praproses juga dapat membatasi amplitudo pada −1 sampai +1. Jadi jangan menyatakan semua pemrosesan bebas potensi perubahan bentuk sinyal.
3. Kueri E2/E4 dicampur segmen derau sesuai daya untuk mencapai SNR tertentu. Galeri tetap menjadi acuan bersih.
4. Masing-masing metode membuat vektor. Vektor kueri dibandingkan dengan semua vektor galeri **dalam representasi yang sama**. Vektor R1 tidak langsung dikosinuskan dengan R2 karena dimensi dan ruangnya berbeda.
5. Skor diurutkan dari besar ke kecil. Label spesies dipakai setelah itu untuk mengukur hasil, bukan diberikan kepada pencari untuk membocorkan jawabannya.

## Mengapa memakai R0, R1, R2, dan R3?

| Kode | Cara kerjanya dalam TA | Alasan pembanding |
|---|---|---|
| R0 | 20 koefisien MFCC per frame; rata-rata dan simpangan baku masing-masing digabung menjadi 40 angka. | Acuan fitur akustik klasik yang tidak membutuhkan bobot deep learning. |
| R1 | PANNs CNN14 pretrained AudioSet; embedding 2.048 angka. | Mewakili model yang belajar dari berbagai suara umum. |
| R2 | BirdNET v2.4 backbone ONNX; embedding 1.024 angka. | Mewakili model yang dilatih untuk domain suara burung. |
| R3 | Vektor acak 40 angka yang ditentukan secara stabil dari ID rekaman dan seed. | Kontrol untuk memeriksa hasil tanpa informasi waveform. |

Ada **tiga representasi audio dan satu kontrol**. R0 bukan jaringan saraf. R3 bukan model yang mendengarkan audio. Pemilihan ini membandingkan kategori pendekatan; belum mencakup semua model yang mungkin tersedia.

Dimensi lebih banyak tidak otomatis lebih baik. R2 berdimensi lebih kecil daripada R1 tetapi lebih baik pada hasil utama TA. Hasil itu juga tidak membuktikan bahwa mengurangi dimensi menyebabkan kenaikan performa.

## Apa sebenarnya MFCC?

Bayangkan Anda ingin merangkum bentuk umum susunan frekuensi suara, tanpa menyimpan seluruh waveform. MFCC melakukan rangkaian: potongan pendek suara → analisis frekuensi → bank filter skala Mel → log energi → transformasi kosinus → sejumlah koefisien.

Skala Mel mendekatkan pengelompokan frekuensi pada sifat persepsi pendengaran; bukan salinan sempurna telinga manusia. Koefisien MFCC bukan daftar langsung frekuensi nada. Pada TA, `n_fft=1024`, langkah antarfame `hop_length=512`, dan `n_mfcc=20`. Pada 32 kHz, 1.024 sampel ≈ 32 ms; langkah 512 sampel ≈ 16 ms. Selanjutnya mean dan std membuat vektor tetap 40 dimensi, berapa pun jumlah frame.

Rata-rata merangkum kecenderungan koefisien; simpangan baku merangkum variasinya. Pooling ini menghilangkan sebagian rincian urutan waktu. TA tidak memakai Naive Bayes atau BiLSTM sebagai R0, meskipun artikel pendukung MFCC memakai model tersebut.

## Penyesuaian BirdNET yang harus diketahui

Klip umum TA lima detik pada 32 kHz. Adapter R2 mengubahnya ke 48 kHz, lalu menggunakan jendela tiga detik dengan langkah satu detik. Untuk klip tepat lima detik, jendelanya 0–3, 1–4, dan 2–5 detik. Embedding ketiganya dirata-ratakan dan dinormalisasi L2.

Jadi “semua klip lima detik” tidak berarti semua model memiliki jendela internal yang sama. BirdNET yang diuji adalah checkpoint v2.4; spesifikasi artikel BirdNET 2021 tidak boleh dianggap persis sama dengan checkpoint ini.

## Mengapa SNR +20, +10, 0, dan −5 dB?

Keempat nilai memberikan kondisi dari target jauh lebih kuat daripada gangguan sampai gangguan lebih kuat daripada target. Ini grid uji yang dipilih; bukan hukum bahwa suara lapangan hanya memiliki empat kondisi tersebut atau bahwa rentang itu paling optimal.

| SNR | Daya target : daya derau | Cara mengucapkan |
|---|---:|---|
| +20 dB | 100 : 1 | Target jauh lebih kuat dalam ukuran daya. |
| +10 dB | 10 : 1 | Target masih lebih kuat. |
| 0 dB | 1 : 1 | Daya keduanya sama. |
| −5 dB | 0,316 : 1 | Daya derau sekitar 3,162 kali daya target. |

SNR ditulis **+20 dB**, bukan “20 SNR”. SNR 0 dB tidak berarti audio senyap. −5 dB tidak berarti amplitudo negatif. Skala logaritmik membandingkan rasio, bukan mengurangkan volume dengan angka 5.

Normalisasi RMS mengatur skala, tetapi target yang disebut “bersih” masih merupakan rekaman sumber dan dapat membawa latar aslinya. SNR yang dihitung dalam campuran adalah rasio daya komponen audio target dan komponen derau tambahan; bukan pengukuran terpisah suara burung murni terhadap semua latar asli.

## Spectral centroid, bandwidth, RMS, dan margin

**Spectral centroid** adalah rata-rata frekuensi berbobot magnitudo spektrum. Bayangkan titik keseimbangan sebaran magnitudo frekuensi. Nilai tinggi berarti bobot spektral cenderung lebih tinggi; itu tidak otomatis berarti suara serangga atau bahwa burung gagal dikenali.

**Spectral bandwidth** merangkum seberapa lebar sebaran frekuensi di sekitar centroid. Dalam contoh dasar dan parameter default p=2, bentuknya seperti simpangan baku berbobot frekuensi. Kode E5 menghitung ciri per frame dengan librosa lalu mengambil rata-ratanya.

**RMS** merangkum besar sinyal dari akar rata-rata kuadrat amplitudo. **Threshold margin = skor kemiripan maksimum − τ**. Nilai positif berarti lolos ambang, tetapi belum tentu spesies teratas benar.

Ciri spektral E5 pada campuran menggambarkan keseluruhan campuran. Menghubungkannya secara khusus dengan serangga atau mekanisme kerusakan model membutuhkan pemeriksaan tambahan terhadap segmen derau dan rancangan pengujian yang sesuai.

## Apa beda klasifikasi, retrieval, dan penolakan?

Klasifikasi memilih label. Retrieval menghasilkan urutan rekaman; label bisa dibaca dari rekaman yang ditemukan. Penolakan open-set menambahkan keputusan menerima atau menolak berdasarkan skor. Keputusan “diterima” tidak otomatis berarti label teratas benar. Itulah sebabnya kualitas ranking dan perilaku ambang harus dilaporkan terpisah.

## Teori mana yang perlu diprioritaskan?

Kuasai dahulu sinyal digital, daya/RMS/SNR, spektrum, representasi, cosine, AP/mAP/Recall, dan threshold. Setelah itu pelajari fungsi umum CNN dan perbedaan data pralatih PANNs–BirdNET. Terakhir pelajari bootstrap, analisis sensitivitas lokasi, serta generalisasi. Anda perlu memahami apa yang dioperasikan kode; tidak harus menurunkan seluruh teori arsitektur dari nol untuk menjelaskan eksperimen ini.

Sumber implementasi: `src/preprocess.py`, `src/mix_noise.py`, `src/mfcc.py`, `src/embeddings.py`, `src/retrieve.py`, `src/calibrate_threshold.py`, dan `scripts/run_e5_diagnostics.py`. Peta bacaan ada pada berkas 06.
