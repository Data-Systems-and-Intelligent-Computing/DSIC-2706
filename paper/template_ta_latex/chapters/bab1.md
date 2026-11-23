# PENDAHULUAN

## Latar Belakang

Burung merupakan salah satu bagian dari keanekaragaman hayati yang
berperan menjaga regenerasi hutan. Peran ini terlihat pada burung
pemakan buah yang menyebarkan biji jauh dari pohon induknya sehingga
biji dapat berkecambah di tempat lain. Dalam studi di Bolivia, 47,1%
dari 22.997 biji yang dianalisis berasal dari tumbuhan yang bijinya
biasa disebarkan oleh burung [@mayta2024seedrain]. Meski demikian,
pembukaan hutan untuk pertanian dapat mengurangi tempat mencari pakan
dan berkembang biak bagi sebagian spesies burung dan satwa
lainnya [@hatfield2024seeddispersal]. Oleh karena itu, perubahan
keberadaan spesies perlu dipantau agar upaya perlindungan dapat
disesuaikan dengan kondisi di lapangan. Salah satu caranya adalah
merekam suara burung, karena kicauan dan panggilan dapat membantu
mengenali spesies yang sulit diamati secara
langsung [@lewis2021vocalizations; @stowell2022bioacoustics].

Penelitian Bennovry dkk. di Taman Nasional Way Kambas menggunakan
ConvNeXt untuk mengidentifikasi spesies burung dari rekaman suara. Model
yang dilatih dengan augmentasi data mencapai akurasi klasifikasi
71% [@bennovry2025waykambas]. Prediksi tersebut memberikan dugaan awal
tentang identitas burung, yang dapat diperiksa lebih lanjut dengan
membandingkan rekaman yang sedang diidentifikasi dengan contoh suara
dari spesies yang diprediksi.

Untuk memperoleh rekaman pembanding, pencarian dapat dilakukan
berdasarkan kemiripan ciri suara. Allen-Ankins dkk. menggunakan BirdNET
untuk mengekstraksi fitur dari sebuah contoh suara dan potongan audio
dari rekaman panjang yang belum berlabel. Kemiripan dinilai dengan
menghitung jarak Euclidean antara fitur contoh suara dan fitur setiap
potongan. Potongan dengan jarak paling kecil kemudian dapat didengarkan
kembali untuk memeriksa kecocokannya [@allenankins2025retrieval].

Namun, kemiripan antarrekaman dapat dipengaruhi oleh suara latar yang
ikut terekam bersama suara burung. Pada pengenalan suara burung, Clark
dkk. mendapati bahwa bunyi aktivitas manusia berkaitan dengan deteksi
spesies yang keliru (*false positive*), sedangkan derau angin berkaitan
dengan suara burung yang terlewat (*false
negative*) [@clark2023soundscape]. Ghaffari dan Devos juga menguji
rekaman yang diberi derau alami dan perkotaan serta menunjukkan bahwa
kompresi dan normalisasi pada tahap pengolahan awal audio (*frontend*)
membantu mempertahankan kinerja klasifikasi [@ghaffari2024frontends].
Temuan tersebut mendasari pengujian apakah rekaman dari spesies yang
sama masih muncul di urutan atas hasil pencarian ketika rekaman yang
menjadi masukan mengandung derau. Studi tentang pencarian rekaman serupa
dan pengenalan suara berderau masih menyisakan pertanyaan tentang
kemampuan berbagai representasi audio dalam mempertahankan kualitas
pencarian ketika tingkat dan sumber derau
berubah [@allenankins2025retrieval; @clark2023soundscape; @ghaffari2024frontends].

Besarnya pengaruh derau terhadap urutan hasil pencarian dapat berbeda
menurut representasi audio yang digunakan. Hal ini menimbulkan
pertanyaan utama penelitian, yaitu representasi audio mana yang paling
mampu mempertahankan kualitas pencarian rekaman burung Indonesia
berdasarkan kemiripan suara ketika derau ditambahkan. Untuk menjawabnya,
penelitian ini menggunakan rekaman Xeno-Canto dari 20 spesies burung di
Indonesia [@xenocantoArchive]. Rekaman yang dicari padanannya disebut
kueri, sedangkan galeri adalah kumpulan rekaman pembanding berlabel
spesies yang diurutkan berdasarkan kemiripannya dengan kueri sehingga
hasil terdekat dapat diperiksa lebih dahulu. Kemiripan dihitung
menggunakan ciri audio dari MFCC [@peng2025birdfbank], PANNs
CNN14 [@kong2020panns], dan BirdNET [@kahl2021birdnet]. Kueri dicampur
secara terkontrol dengan derau lapangan dari lima lokasi di Institut
Teknologi Sumatera (Itera) pada beberapa tingkat *signal-to-noise ratio*
(SNR), yaitu rasio daya kueri terhadap daya derau tambahan.

Kualitas pencarian pada kondisi berderau dibandingkan dengan kondisi
tanpa penambahan derau untuk memperoleh retensi, yaitu proporsi kinerja
yang masih bertahan. Karena hasil teratas tetap muncul untuk suara di
luar cakupan galeri, penerimaan kueri juga diuji dengan ambang
kemiripan, yaitu skor minimum hasil teratas agar kueri diterima. Ambang
ditentukan melalui kalibrasi pada rekaman target (spesies dalam galeri)
dan kontrol (burung non-target dan derau lingkungan) yang terpisah dari
data uji. Kebaruan penelitian ini terletak pada perbandingan ketahanan
tiga representasi terhadap perubahan tingkat derau, dengan kueri yang
sama diuji pada kondisi acuan dan kondisi berderau terhadap galeri yang
tetap. Selain itu, derau dari kelima lokasi dibandingkan pada SNR yang
sama untuk melihat perbedaan kinerja menurut sumbernya.

## Rumusan Masalah

Berdasarkan latar belakang tersebut, rumusan masalah dalam penelitian
ini adalah sebagai berikut:

::: daftarBernomor
Bagaimana perubahan kualitas pencarian rekaman dan retensi ketiga
representasi audio pada SNR $+20$, $+10$, $0$, dan $-5$ dB dibandingkan
dengan kondisi tanpa penambahan derau?

Bagaimana perubahan penerimaan kueri target dan penerimaan keliru
kontrol di luar target ketika ambang kemiripan hasil kalibrasi tanpa
penambahan derau dipertahankan dan diterapkan pada kondisi bising?

Bagaimana perbedaan kualitas dan kestabilan pencarian rekaman ketika
kueri dicampur dengan derau dari lima lokasi Itera pada SNR yang sama?

Bagaimana pola kegagalan pencarian rekaman ditinjau dari margin terhadap
ambang, ciri spektral yang tersedia, dan catatan audit pendengaran pada
kasus pilihan?
:::

## Tujuan

Berdasarkan rumusan masalah tersebut, tujuan penelitian ini adalah
sebagai berikut:

::: daftarBernomor
Mengukur perubahan kualitas pencarian rekaman dan retensi ketiga
representasi pada SNR $+20$, $+10$, $0$, dan $-5$ dB terhadap kondisi
tanpa penambahan derau, dengan mAP@10 sebagai metrik utama dan metrik
pencarian rekaman lainnya sebagai pendukung.

Menganalisis perubahan penerimaan kueri target dan penerimaan keliru
kontrol di luar target pada kondisi bising menggunakan ambang kemiripan
yang ditentukan dari data kalibrasi terpisah tanpa penambahan derau dan
kemudian dipertahankan.

Membandingkan kualitas dan kestabilan pencarian rekaman pada campuran
derau dari lima lokasi Itera pada SNR yang sama, berdasarkan kualitas
absolut dan retensi relatif serta analisis sensitivitas terhadap
komposisi lokasi.

Mengidentifikasi pola kegagalan pencarian rekaman berdasarkan margin
terhadap ambang dan ciri spektral yang tersedia, serta melengkapinya
dengan catatan audit pendengaran pada kasus pilihan.
:::

## Batasan Penelitian

Agar pembahasan terarah dan sesuai dengan tujuan penelitian, batasan
penelitian ini ditetapkan sebagai berikut:

::: daftarBernomor
Data penelitian dibatasi pada potongan audio lima detik dari Xeno-Canto
dengan 20 label spesies burung yang terdapat di Indonesia, sesuai
metadata dan daftar rekaman eksperimen yang telah ditetapkan. Cakupan
label mengikuti metadata arsip, sehingga tidak selalu sama dengan
taksonomi terbaru.

Representasi yang dibandingkan adalah MFCC, PANNs CNN14, dan BirdNET.
Model pralatih digunakan tanpa pembaruan bobot, sedangkan vektor acak
berbasis identitas rekaman digunakan sebagai kontrol pembanding.

Penelitian berfokus pada pencarian rekaman menggunakan kemiripan
kosinus, yaitu ukuran kemiripan arah dua vektor fitur. Relevansi hasil
ditentukan berdasarkan kesamaan label spesies pada metadata, dengan
koleksi referensi yang dipertahankan selama pengujian.

Derau bersumber dari lima lokasi Itera, yaitu Kebun Raya, Embung F,
Gedung F, Masjid At-Tanwir, dan sekitar GKU 1. Derau dicampurkan secara
aditif pada kueri dengan SNR $+20$, $+10$, $0$, dan $-5$ dB, serta
dibandingkan dengan kondisi tanpa penambahan derau.

Pengujian dibatasi pada campuran aditif terkontrol dan belum mencakup
suara burung target yang direkam langsung di lingkungan Itera. Pengaruh
jarak, perambatan, dan pantulan suara tidak diuji secara terpisah.
Kesimpulan penelitian dibatasi pada kumpulan rekaman target dan profil
derau Itera yang digunakan.

Ambang kemiripan ditentukan menggunakan data kalibrasi terpisah tanpa
penambahan derau dan dipertahankan selama pengujian. Evaluasi penerimaan
dan penolakan dibatasi pada data target serta kontrol di luar target
yang digunakan dalam penelitian.

Evaluasi kualitas pencarian rekaman menggunakan mAP@10 sebagai metrik
utama, didukung *precision*\@10, *recall*\@10, MRR, dan ketepatan hasil
pertama. Analisis ketahanan dan kestabilan mempertimbangkan perubahan
kualitas absolut serta retensi relatif terhadap kondisi tanpa penambahan
derau.

Analisis kegagalan menggunakan margin terhadap ambang dan ciri spektral
yang tersedia, dilengkapi audit pendengaran terhadap 120 kasus pilihan
oleh satu pendengar. Hasil audit bersifat deskriptif dan tidak digunakan
untuk membuktikan penyebab kegagalan maupun menggeneralisasi frekuensi
kegagalan pada seluruh data.
:::
