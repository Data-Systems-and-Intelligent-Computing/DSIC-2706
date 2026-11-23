# TINJAUAN PUSTAKA

## Penelitian Terdahulu

Penelitian ini membandingkan ketahanan tiga representasi audio terhadap
derau pada pencarian rekaman burung berdasarkan kemiripan suara. Untuk
menempatkan posisi penelitian,
Tabel [1.1](#tab:penelitian-terdahulu){reference-type="ref"
reference="tab:penelitian-terdahulu"} merangkum studi terdahulu yang
berkaitan dengan representasi audio pralatih, pencarian bioakustik, dan
ketahanan terhadap derau.

::: jarakTabelPenelitian
::: {#tab:penelitian-terdahulu}
  **No.**                                                                                                                       **Metode dan evaluasi**                                                            **Temuan utama**                                                                       **Relevansi dan pembeda**
  --------- ------------------------------------------------------ ------------------------------------------------------------ ---------------------------------------------------------------------------------- -------------------------------------------------------------------------------------- -----------------------------------------------------------------------------------------------------------------------------
                                                                                                                                                                                                                                                                                                          
  **No.**                                                                                                                       **Metode dan evaluasi**                                                            **Temuan utama**                                                                       **Relevansi dan pembeda**
            Hamer dkk. (2023) [@hamer2023birb]                     Rekaman Xeno-Canto; benchmark BIRB mencakup banyak spesies   Retrieval bioakustik dengan embedding pralatih; cmAP sebagai metrik                Embedding pralatih mengungguli baseline non-pralatih pada retrieval                    Acuan tugas retrieval bioakustik; TA menggunakan mAP@10 pada kueri berderau, bukan cmAP lintas-dataset
            Ghani dkk. (2023) [@ghani2023embeddings]               Rekaman burung; beberapa dataset transfer                    Perbandingan embedding BirdNET, PANNs, dan lainnya untuk klasifikasi transfer      Embedding khusus burung menghasilkan transfer yang lebih baik daripada audio umum      Dasar pemilihan representasi; TA mengukur kemiripan kosinus pada retrieval, bukan akurasi klasifikasi
            Ghaffari dan Devos (2024) [@ghaffari2024frontends]     Rekaman burung dengan derau alami dan perkotaan              Evaluasi frontend audio terhadap ketahanan klasifikasi; normalisasi dan kompresi   Kompresi dan normalisasi frontend mempertahankan kinerja saat derau ditambahkan        Pembanding ketahanan terhadap derau; TA menguji retrieval dan beberapa tingkat SNR terkontrol, bukan klasifikasi
            Clark dkk. (2023) [@clark2023soundscape]               Rekaman citizen science; soundscape beragam                  Klasifikasi BirdNET pada komposisi soundscape berbeda                              Suara manusia berkaitan dengan *false positive*; derau angin dengan *false negative*   Dasar pengujian profil derau lokasi; TA memakai campuran aditif terkontrol, bukan asosiasi observasional
            Fairbairn dkk. (2025) [@fairbairn2025birdnet]          Rekaman perkotaan Eropa; pemantauan burung                   Evaluasi BirdNET dengan ambang confidence berbeda                                  Pemilihan ambang memengaruhi keseimbangan presisi dan recall deteksi                   Dasar kalibrasi ambang; TA menggunakan ambang kemiripan kosinus, bukan confidence klasifikator
            Kong dkk. (2020) [@kong2020panns]                      AudioSet; audio umum skala besar                             PANNs CNN14 pralatih untuk klasifikasi audio; mAP pada AudioSet                    CNN14 menghasilkan embedding 2.048 dimensi dengan kinerja klasifikasi tinggi           Asal representasi audio umum yang dipakai; TA menggunakan bobot tetap untuk embedding retrieval, bukan klasifikasi
            Kahl dkk. (2021) [@kahl2021birdnet]                    Rekaman burung Xeno-Canto                                    BirdNET untuk identifikasi burung; arsitektur deep learning                        Model pralatih mengidentifikasi ratusan spesies burung                                 Asal representasi khusus burung; TA menggunakan embedding beku v2.4 untuk retrieval
            Allen-Ankins dkk. (2025) [@allenankins2025retrieval]   Rekaman lapangan; audio panjang belum berlabel               BirdNET embedding untuk pencarian kelas baru; jarak Euclidean                      Embedding BirdNET dapat menemukan suara baru dalam rekaman panjang                     Acuan langsung retrieval embedding; TA membandingkan tiga representasi dengan kemiripan kosinus dan menguji ketahanan derau

  : Penelitian Terdahulu yang Relevan
:::
:::

Sebagian besar studi pada
Tabel [1.1](#tab:penelitian-terdahulu){reference-type="ref"
reference="tab:penelitian-terdahulu"} mengevaluasi representasi audio
dalam konteks klasifikasi atau deteksi. Penelitian ini berbeda karena
berfokus pada pencarian rekaman berdasarkan kemiripan kosinus, dengan
pengujian ketahanan yang membandingkan kondisi berderau terhadap acuan
tanpa penambahan derau secara berpasangan untuk kueri yang sama. Selain
itu, penerimaan kueri diuji dengan ambang kemiripan pada kelas terbuka,
dan derau dari lima lokasi dibandingkan pada SNR yang sama.

## Sinyal Audio Digital dan Prapemrosesan

Bagian ini membahas dasar pengolahan sinyal audio digital yang digunakan
untuk menyiapkan rekaman sebelum fitur diekstraksi. Prapemrosesan
mencakup pencuplikan, penyeragaman kanal, pemilihan segmen, dan
normalisasi amplitudo [@lu2025dusafnet].

### Sinyal Audio Digital dan Laju Pencuplikan

Sinyal audio digital diperoleh dengan mencuplik sinyal analog pada
interval waktu tetap. Laju pencuplikan (*sampling rate*) $f_s$
menyatakan jumlah sampel per detik, dinyatakan dalam hertz (Hz).
Interval antarsampling adalah $$\label{eq:interval-sampling}
T_s = \frac{1}{f_s}$$ sehingga rekaman berdurasi $D$ detik menghasilkan
jumlah sampel $$\label{eq:jumlah-sampel}
N = f_s \times D$$

::: keteranganRumus
$T_s$ & interval antarsampel (detik)\
$f_s$ & laju pencuplikan (Hz)\
$D$ & durasi rekaman (detik)\
$N$ & jumlah sampel dalam rekaman
:::

Laju pencuplikan menentukan rentang frekuensi yang dapat
direpresentasikan. Berdasarkan teorema Nyquist, frekuensi tertinggi yang
dapat dicuplik tanpa aliasing adalah $f_s/2$ [@jeon2020stft]. Pada
penelitian ini, rekaman diseragamkan ke laju 32 kHz sehingga frekuensi
hingga 16 kHz dapat direpresentasikan, yang mencakup sebagian besar
rentang frekuensi suara burung.

### Penyeragaman Kanal dan Pemilihan Segmen

Rekaman dari berbagai sumber dapat memiliki jumlah kanal yang berbeda.
Untuk menyeragamkan masukan, rekaman stereo digabungkan menjadi mono
dengan merata-ratakan kedua kanal [@lu2025dusafnet]: $$\label{eq:mono}
x[n] = \frac{x_L[n] + x_R[n]}{2}$$

::: keteranganRumus
$n$ & indeks sampel\
$x_L[n]$ & amplitudo kanal kiri pada sampel ke-$n$\
$x_R[n]$ & amplitudo kanal kanan pada sampel ke-$n$\
$x[n]$ & amplitudo sinyal mono
:::

Dari rekaman yang telah diseragamkan, segmen berdurasi tetap dipilih
untuk memastikan panjang masukan yang sama bagi semua metode. Jika
rekaman lebih panjang dari durasi target, jendela digeser sepanjang
rekaman dan tingkat sinyal pada setiap jendela diukur dengan *root mean
square* (RMS). RMS pada jendela ke-$j$ dengan panjang $M$ sampel
dihitung sebagai $$\label{eq:rms-jendela}
\mathrm{RMS}_j = \sqrt{\frac{1}{M}\sum_{n=0}^{M-1} x_j[n]^2}$$

::: keteranganRumus
$j$ & indeks jendela\
$M$ & jumlah sampel per jendela\
$x_j[n]$ & amplitudo sampel ke-$n$ pada jendela ke-$j$\
$\mathrm{RMS}_j$ & akar rata-rata kuadrat amplitudo jendela
:::

Jendela dengan nilai RMS tertinggi dipilih sebagai segmen
masukan [@lu2025dusafnet]. Pemilihan ini bertujuan mengambil bagian
rekaman dengan tingkat sinyal tertinggi, meskipun segmen terpilih juga
dapat memuat suara latar yang kuat.

### Normalisasi Amplitudo dengan RMS

Setelah segmen dipilih, amplitudo dinormalisasi agar tingkat sinyal
antarrekaman lebih sebanding sebelum fitur dihitung. Normalisasi
menggunakan faktor pengali yang membawa RMS segmen menuju nilai
target [@lu2025dusafnet]: $$\label{eq:normalisasi-rms}
x'[n] = x[n] \times \frac{\mathrm{RMS}_{\mathrm{target}}}{\mathrm{RMS}_{\mathrm{asal}}}$$

::: keteranganRumus
$x[n]$ & amplitudo sebelum penyesuaian RMS\
$x'[n]$ & amplitudo sesudah penyesuaian RMS\
$\mathrm{RMS}_{\mathrm{asal}}$ & RMS segmen sebelum penyesuaian\
$\mathrm{RMS}_{\mathrm{target}}$ & RMS yang dituju, yaitu 0,05
:::

Agar sinyal yang sangat senyap tidak diperkuat secara berlebihan, segmen
dengan RMS di bawah batas tertentu ($10^{-6}$) melewati tahap ini tanpa
penyesuaian. Setelah normalisasi, seluruh nilai sampel dibatasi pada
rentang $[-1, 1]$: $$\label{eq:clipping}
\hat{x}[n] = \max\bigl(-1,\;\min(1,\;x'[n])\bigr)$$

::: keteranganRumus
$\hat{x}[n]$ & amplitudo akhir setelah $x'[n]$ dibatasi pada rentang
$[-1,1]$
:::

Pembatasan ini mencegah luapan nilai, meskipun dapat mengubah RMS akhir
dari target jika puncak sinyal terpotong. Dalam penelitian ini, target
RMS ditetapkan pada 0,05 sebagai setelan pengujian.

## Representasi *Hand-crafted* (STFT, Skala Mel, dan MFCC)

Representasi *hand-crafted* mengolah sinyal audio menjadi vektor fitur
melalui tahap yang dirancang secara eksplisit berdasarkan pengetahuan
domain. Bagian ini membahas STFT sebagai dasar analisis
waktu--frekuensi, skala mel yang meniru persepsi pendengaran, dan MFCC
sebagai ringkasan spektral [@peng2025birdfbank].

### Analisis Waktu--Frekuensi dengan STFT

Suara burung berubah sepanjang waktu, sehingga analisis frekuensi perlu
dilakukan pada jendela pendek. *Short-Time Fourier Transform* (STFT)
membagi sinyal menjadi bingkai pendek yang saling bertumpang tindih,
lalu menerapkan *Discrete Fourier Transform* (DFT) pada setiap
bingkai [@jeon2020stft]: $$\label{eq:stft}
X(m, k) = \sum_{n=0}^{N_{\mathrm{FFT}}-1} x[n + mH]\;w[n]\;e^{-j2\pi kn/N_{\mathrm{FFT}}}$$

::: keteranganRumus
$m$ & indeks bingkai waktu\
$k$ & indeks bin frekuensi\
$n$ & indeks sampel dalam jendela\
$N_{\mathrm{FFT}}$ & panjang FFT (sampel)\
$H$ & pergeseran antarbingkai (sampel)\
$x[n+mH]$ & amplitudo sampel ke-$n$ dalam bingkai ke-$m$\
$w[n]$ & bobot jendela pada sampel ke-$n$\
$j$ & satuan imajiner\
$X(m,k)$ & koefisien kompleks STFT pada bingkai ke-$m$ dan bin ke-$k$
:::

Spektrum daya pada setiap bingkai dihitung dari kuadrat magnitudo
koefisien STFT: $$\label{eq:power-spectrum}
P(m, k) = |X(m, k)|^2$$

::: keteranganRumus
$P(m,k)$ & daya pada bingkai ke-$m$ dan bin ke-$k$\
$|X(m,k)|$ & magnitudo koefisien STFT
:::

Gambar [\[fig:stft\]](#fig:stft){reference-type="ref"
reference="fig:stft"} mengilustrasikan proses penerapan jendela dan DFT
pada bingkai-bingkai sinyal yang bertumpang tindih.

::: gambarPenelitian
![image](bab2/stft_adaptasi_jeon_2020.png){width="0.85\\linewidth"}
:::

### Skala Mel dan Bank Filter

Persepsi manusia terhadap frekuensi tidak linear: perbedaan frekuensi
yang sama terasa lebih besar pada frekuensi rendah daripada tinggi. Bank
filter mel menyusun pita frekuensi menurut skala
perseptual [@peng2025birdfbank]. Untuk membentuk bank filter pada
ekstraksi MFCC, pustaka *librosa* menggunakan pemetaan Slaney
berikut.[^1] $$\label{eq:mel}
m(f) =
\begin{cases}
3f/200, & 0\le f<1000,\\
15 + 27\,\ln(f/1000)/\ln(6{,}4), & f\ge 1000.
\end{cases}$$

::: keteranganRumus
$f$ & frekuensi (Hz)\
$m(f)$ & nilai frekuensi pada skala mel Slaney
:::

Bank filter mel terdiri atas sejumlah filter segitiga yang ditempatkan
secara merata pada skala mel, lalu dipetakan kembali ke frekuensi
linear. Setiap filter mengintegrasikan energi spektrum daya pada rentang
frekuensinya: $$\label{eq:mel-energy}
E_i(m) = \sum_{k} P(m, k)\;H_i(k)$$

::: keteranganRumus
$i$ & indeks filter mel\
$H_i(k)$ & bobot filter ke-$i$ pada bin ke-$k$\
$E_i(m)$ & energi bingkai ke-$m$ pada filter ke-$i$
:::

Energi pita mel kemudian diubah ke skala logaritmik untuk memodelkan
sensitivitas pendengaran yang mendekati skala logaritmik terhadap
intensitas.

### Koefisien MFCC dan Ringkasan Antarbingkai

*Mel-Frequency Cepstral Coefficients* (MFCC) diperoleh dengan menerapkan
*Discrete Cosine Transform* (DCT) pada energi mel
logaritmik [@akinci2026mfcc]: $$\label{eq:dct}
c_i(m) = \sum_{j=1}^{J} \log E_j(m) \cos\!\left[\frac{\pi\,i\,(j - 0{,}5)}{J}\right]$$

::: keteranganRumus
$i$ & indeks koefisien MFCC\
$c_i(m)$ & nilai koefisien ke-$i$ pada bingkai ke-$m$\
$j$ & indeks filter mel\
$J$ & jumlah filter mel\
$E_j(m)$ & energi pada pita mel ke-$j$ untuk bingkai tersebut
:::

Untuk meringkas informasi sepanjang segmen menjadi satu vektor per
rekaman, rata-rata dan simpangan baku setiap koefisien dihitung
antarbingkai: $$\label{eq:mfcc-mean}
\bar{c}_i = \frac{1}{T}\sum_{m=1}^{T} c_i(m)$$ $$\label{eq:mfcc-std}
\sigma_i = \sqrt{\frac{1}{T}\sum_{m=1}^{T} \bigl(c_i(m) - \bar{c}_i\bigr)^2}$$

::: keteranganRumus
$T$ & jumlah bingkai dalam segmen\
$\bar c_i$ & rata-rata koefisien ke-$i$ sepanjang bingkai\
$\sigma_i$ & simpangan baku koefisien ke-$i$ sepanjang bingkai
:::

Dengan 20 koefisien, penggabungan rata-rata dan simpangan baku
menghasilkan vektor 40 dimensi per rekaman.
Gambar [\[fig:mfcc-fbank\]](#fig:mfcc-fbank){reference-type="ref"
reference="fig:mfcc-fbank"} mengilustrasikan alur ekstraksi MFCC dari
sinyal audio hingga koefisien.

::: gambarPenelitian
![image](bab2/ekstraksi_mfcc_fbank_adaptasi_peng_2025.png){width="0.85\\linewidth"}
:::

### Ciri Spektral untuk Diagnosis Kegagalan

Selain MFCC, ciri spektral digunakan untuk menggambarkan karakter
frekuensi rekaman dan mendukung diagnosis kegagalan
pencarian [@ghani2021bagbirds]. *Spectral centroid* menunjukkan pusat
massa frekuensi pada setiap bingkai: $$\label{eq:centroid}
\mathrm{SC}(m) = \frac{\sum_{k} f(k)\,|X(m,k)|}{\sum_{k} |X(m,k)|}$$

*Spectral bandwidth* mengukur lebar sebaran frekuensi di sekitar
*centroid*: $$\label{eq:bandwidth}
\mathrm{SB}(m) = \sqrt{\frac{\sum_{k}\bigl(f(k) - \mathrm{SC}(m)\bigr)^2 |X(m,k)|}{\sum_{k} |X(m,k)|}}$$

::: keteranganRumus
$f(k)$ & frekuensi bin ke-$k$ (Hz)\
$\mathrm{SC}(m)$ & pusat spektrum bingkai ke-$m$, berbobot magnitudo
(Hz)\
$\mathrm{SB}(m)$ & lebar sebaran frekuensi terhadap pusat spektrum (Hz)
:::

Kedua ciri dihitung pada setiap bingkai, lalu dirata-ratakan untuk
setiap kueri. RMS pada
Persamaan ([\[eq:rms-jendela\]](#eq:rms-jendela){reference-type="ref"
reference="eq:rms-jendela"}) juga digunakan sebagai ciri tingkat sinyal.
Ketiga nilai ini digunakan secara deskriptif pada analisis kegagalan,
bukan sebagai fitur pencarian.

## Representasi Audio Pralatih sebagai Pengekstrak Fitur

Model *deep learning* pralatih dapat digunakan sebagai pengekstrak fitur
dengan mempertahankan bobot yang telah dipelajari dari data skala besar.
Pendekatan ini memungkinkan pembentukan *embedding* tanpa melatih ulang
model pada data target. Ghani dkk. menunjukkan bahwa embedding pralatih
dari model khusus burung menghasilkan transfer yang lebih baik daripada
model audio umum pada klasifikasi bioakustik [@ghani2023embeddings].

### PANNs CNN14

PANNs (*Pretrained Audio Neural Networks*) CNN14 adalah model konvolusi
yang dilatih pada AudioSet untuk klasifikasi audio
umum [@kong2020panns]. Arsitektur CNN14 memproses mel-spektrogram
masukan melalui blok konvolusi, lalu meratakan dimensi frekuensi dengan
perataan global. Untuk setiap kanal fitur, nilai maksimum dan rata-rata
sepanjang waktu dijumlahkan: $$\label{eq:panns-pooling}
\mathbf{z} = \mathrm{MaxPool}(\mathbf{F}) + \mathrm{AvgPool}(\mathbf{F})$$

::: keteranganRumus
$\mathbf F$ & fitur per waktu dan kanal setelah perataan pada dimensi
frekuensi\
$\mathbf z$ & jumlah maksimum dan rata-rata temporal, dihitung per kanal
:::

Vektor hasil penjumlahan kemudian diproses melalui lapisan linear dan
aktivasi ReLU untuk membentuk embedding 2.048 dimensi. Dalam penelitian
ini, model digunakan dengan bobot tetap: hanya embedding yang diambil,
tanpa memperbarui parameter.

### BirdNET

BirdNET adalah model *deep learning* yang dilatih khusus pada rekaman
suara burung untuk identifikasi spesies [@kahl2021birdnet]. Model
menerima segmen audio dan memprosesnya dalam jendela 3 detik dengan
pergeseran 1 detik. Setiap jendela menghasilkan satu vektor embedding.
Ketika segmen menghasilkan beberapa jendela, vektor antarjendela
dirata-ratakan [@allenankins2025retrieval]: $$\label{eq:birdnet-avg}
\bar{\mathbf{e}} = \frac{1}{W}\sum_{w=1}^{W}\mathbf{e}_w$$

::: keteranganRumus
$W$ & jumlah jendela dalam segmen\
$w$ & indeks jendela\
$\mathbf e_w$ & vektor BirdNET dari jendela ke-$w$\
$\bar{\mathbf e}$ & vektor rata-rata seluruh jendela sebelum normalisasi
L2
:::

Rata-rata ini menghasilkan satu embedding 1.024 dimensi per rekaman.
Seperti PANNs CNN14, BirdNET digunakan dengan bobot model tetap.
Perbedaannya, BirdNET dilatih pada suara burung sehingga embeddingnya
diharapkan menangkap informasi yang lebih spesifik untuk membedakan
spesies.

## Ruang *Embedding*, Normalisasi L2, dan Kemiripan Kosinus {#sec:kemiripan-kosinus}

Setiap rekaman direpresentasikan sebagai vektor dalam ruang berdimensi
tinggi. Kemiripan antarrekaman kemudian diukur berdasarkan arah vektor
dalam ruang tersebut [@milewski2023cosine].

### Vektor Kueri dan Galeri

Dalam pencarian berdasarkan kemiripan, rekaman yang dicari padanannya
disebut kueri, sedangkan kumpulan rekaman pembanding berlabel disebut
galeri [@allenankins2025retrieval]. Kueri dan galeri diproses oleh
representasi audio yang sama untuk menghasilkan vektor fitur. Vektor
kueri kemudian dibandingkan dengan seluruh vektor galeri menggunakan
ukuran kemiripan, dan rekaman galeri diurutkan berdasarkan skor
kemiripan dari yang tertinggi.

Kontrol acak $R_3$ memberikan acuan kinerja pencarian ketika vektor
dibentuk hanya dari peran dan identitas rekaman dengan nilai awal acak
tetap. Penambahan derau mempertahankan identitas kueri. Karena vektor
kueri dan galeri tetap sama, urutan hasil pencarian kontrol ini juga
tetap pada setiap SNR.

### Normalisasi L2 dan Kemiripan Kosinus

Sebelum kemiripan dihitung, vektor dinormalisasi L2 agar perbandingan
hanya bergantung pada arah, bukan panjang vektor [@musgrave2020metric].
Norma L2 dari vektor $\mathbf{v}$ adalah $$\label{eq:l2-norm}
\|\mathbf{v}\| = \sqrt{\sum_{i=1}^{d} v_i^2}$$ dan vektor satuan
diperoleh dengan membagi setiap komponen oleh normanya:
$$\label{eq:unit-vector}
\hat{\mathbf{v}} = \frac{\mathbf{v}}{\|\mathbf{v}\|}$$

::: keteranganRumus
$d$ & dimensi vektor\
$v_i$ & komponen vektor pada dimensi ke-$i$\
$\|\mathbf v\|$ & panjang vektor\
$\hat{\mathbf v}$ & vektor satuan untuk $\mathbf v\ne\mathbf 0$
:::

Kemiripan kosinus antara vektor kueri $\mathbf{q}$ dan vektor galeri
$\mathbf{g}$ dihitung sebagai perkalian titik vektor satuannya:
$$\label{eq:cosine-sim}
\mathrm{sim}(\mathbf{q}, \mathbf{g}) = \hat{\mathbf{q}} \cdot \hat{\mathbf{g}} = \frac{\sum_{i=1}^{d} q_i\,g_i}{\|\mathbf{q}\|\;\|\mathbf{g}\|}$$

::: keteranganRumus
$\mathbf q$ & vektor kueri\
$\mathbf g$ & vektor rekaman galeri\
$\hat{\mathbf q}$ & vektor kueri setelah normalisasi L2\
$\hat{\mathbf g}$ & vektor galeri setelah normalisasi L2
:::

Nilai kemiripan kosinus berkisar antara $-1$ dan $1$. Nilai mendekati
$1$ menunjukkan arah yang serupa, sedangkan nilai mendekati $0$ atau
negatif menunjukkan vektor yang saling tegak lurus atau berlawanan arah.
Gambar [\[fig:normalisasi-kosinus\]](#fig:normalisasi-kosinus){reference-type="ref"
reference="fig:normalisasi-kosinus"} mengilustrasikan normalisasi L2 dan
kemiripan kosinus antara dua vektor.

::: gambarPenelitian
:::

## Pencarian Berdasarkan Kemiripan dan Metrik Evaluasi

Setelah skor kemiripan dihitung, rekaman galeri diurutkan berdasarkan
skor tertinggi. Kualitas urutan ini dinilai dengan metrik evaluasi
pencarian informasi yang membandingkan hasil teratas dengan label
relevansi [@moffat2022metrics].

### Pemeringkatan dan Relevansi Hasil

Untuk setiap kueri, seluruh rekaman galeri diurutkan berdasarkan skor
kemiripan kosinus dari yang tertinggi. Rekaman galeri dinilai relevan
jika label spesiesnya sama dengan label spesies
kueri [@allenankins2025retrieval]. Dengan definisi ini, relevansi
bersifat biner: relevan atau tidak relevan.

### Precision@10 dan Recall@10

*Precision*\@10 mengukur proporsi hasil relevan dalam sepuluh hasil
teratas [@moffat2022metrics]: $$\label{eq:precision10}
\mathrm{Precision@10} = \frac{\text{jumlah hasil relevan dalam 10 teratas}}{10}$$

*Recall*\@10 mengukur proporsi seluruh hasil relevan di galeri yang
muncul dalam sepuluh hasil teratas: $$\label{eq:recall10}
\mathrm{Recall@10} = \frac{\text{jumlah hasil relevan dalam 10 teratas}}{\text{jumlah seluruh hasil relevan di galeri}}$$

::: keteranganRumus
$\mathrm{Precision@10}$ & bagian dari sepuluh hasil teratas yang
berlabel spesies sama dengan kueri\
$\mathrm{Recall@10}$ & bagian dari seluruh rekaman relevan di galeri
yang ditemukan dalam sepuluh hasil teratas
:::

### AP@10 dan mAP@10

*Average Precision* pada 10 hasil (AP@10) memperhitungkan posisi setiap
hasil relevan, bukan hanya jumlahnya [@moffat2022metrics]:
$$\label{eq:ap10}
\mathrm{AP@10} = \frac{1}{\min(R, 10)}\sum_{k=1}^{10} \mathrm{Precision@}k \times \mathrm{rel}(k)$$

::: keteranganRumus
$R$ & jumlah rekaman relevan di galeri\
$k$ & posisi hasil dalam peringkat\
$\mathrm{Precision@}k$ & proporsi hasil relevan hingga peringkat ke-$k$\
$\mathrm{rel}(k)$ & indikator relevansi pada peringkat ke-$k$ (1 jika
relevan, 0 jika lainnya)
:::

Penyebut $\min(R, 10)$ memastikan bahwa kueri dengan banyak hasil
relevan dan kueri dengan sedikit hasil relevan dinilai pada skala yang
sebanding. mAP@10 adalah rata-rata AP@10 seluruh kueri:
$$\label{eq:map10}
\mathrm{mAP@10} = \frac{1}{Q}\sum_{q=1}^{Q} \mathrm{AP@10}_q$$

::: keteranganRumus
$Q$ & jumlah kueri\
$\mathrm{AP@10}_q$ & nilai AP@10 untuk kueri ke-$q$
:::

### MRR dan Ketepatan Top-1

*Mean Reciprocal Rank* (MRR) mengukur rata-rata kebalikan peringkat
hasil relevan pertama [@moffat2022metrics]: $$\label{eq:rr}
\mathrm{RR}_q = \frac{1}{\mathrm{rank}_q}$$ $$\label{eq:mrr}
\mathrm{MRR} = \frac{1}{Q}\sum_{q=1}^{Q}\mathrm{RR}_q$$

::: keteranganRumus
$\mathrm{rank}_q$ & peringkat hasil relevan pertama untuk kueri ke-$q$\
$\mathrm{RR}_q$ & kebalikan peringkat tersebut\
$Q$ & jumlah kueri yang dirata-ratakan
:::

Ketepatan Top-1 mengukur proporsi kueri yang hasil peringkat pertamanya
relevan: $$\label{eq:top1}
\mathrm{Top\text{-}1} = \frac{1}{Q}\sum_{q=1}^{Q}\mathrm{rel}(1)_q$$

::: keteranganRumus
$\mathrm{rel}(1)_q$ & indikator bahwa rekaman teratas berlabel spesies
sama dengan kueri ke-$q$\
$Q$ & jumlah kueri
:::

Nilai MRR dan Top-1 yang tinggi menunjukkan bahwa hasil teratas
cenderung berasal dari spesies yang sama dengan kueri.

## Ketahanan terhadap Derau dengan SNR Terkontrol dan Desain Berpasangan {#sec:ketahanan-derau}

Rekaman lapangan sering kali memuat suara latar yang ikut terekam
bersama suara burung. Untuk menguji seberapa baik representasi audio
mempertahankan kualitas pencarian di bawah derau, kueri dicampur dengan
derau pada tingkat SNR yang terkontrol [@ghaffari2024frontends].

### Daya Sinyal, SNR, dan Pencampuran Derau

*Signal-to-Noise Ratio* (SNR) menyatakan perbandingan daya sinyal
terhadap daya derau dalam desibel (dB). Daya rata-rata sinyal $x$
sepanjang $N$ sampel dihitung sebagai [@chen2023biotic]:
$$\label{eq:power}
P = \frac{1}{N}\sum_{n=0}^{N-1} x[n]^2$$

SNR dinyatakan sebagai: $$\label{eq:snr}
\mathrm{SNR} = 10\log_{10}\!\left(\frac{P_s}{P_d}\right)\;\text{dB}$$

::: keteranganRumus
$x[n]$ & amplitudo sampel ke-$n$\
$N$ & jumlah sampel dalam segmen\
$P$ & daya rata-rata segmen\
$P_s$ & daya rata-rata kueri\
$P_d$ & daya rata-rata derau
:::

Untuk mencampur derau pada SNR target $\gamma$, amplitudo derau
dikalikan faktor: $$\label{eq:noise-scale}
\alpha = \sqrt{\frac{P_s}{P_d\;10^{\gamma/10}}}$$

Sinyal campuran diperoleh dengan menjumlahkan kueri dan derau yang telah
diskalakan: $$\label{eq:mix}
y[n] = x[n] + \alpha\,d[n]$$

::: keteranganRumus
$\gamma$ & SNR target (dB)\
$\alpha$ & faktor pengali amplitudo derau\
$x[n]$ & sampel kueri sebelum pencampuran\
$d[n]$ & sampel derau sebelum penskalaan\
$y[n]$ & sampel campuran pada indeks yang sama
:::

Gambar [\[fig:snr-contoh\]](#fig:snr-contoh){reference-type="ref"
reference="fig:snr-contoh"} menampilkan contoh gelombang dan spektrogram
pada beberapa tingkat SNR untuk memperlihatkan bagaimana derau mengubah
tampilan sinyal.

::: gambarPenelitian
![image](bab2/gelombang_spektrogram_snr_adaptasi_chen_2023.png){width="0.85\\linewidth"}
:::

### Perbandingan Berpasangan dan Retensi Kinerja

Pengaruh derau diukur dengan membandingkan kinerja pada kondisi berderau
terhadap kondisi acuan (tanpa penambahan derau) untuk kueri yang
sama [@ghaffari2024frontends]. Selisih mAP@10 menunjukkan perubahan pada
skala asli metrik: $$\label{eq:noise-delta}
\Delta\;\mathrm{mAP@10} = \mathrm{mAP@10}_{\mathrm{berderau}} - \mathrm{mAP@10}_{\mathrm{acuan}}$$

Retensi menyatakan proporsi kinerja yang masih bertahan:
$$\label{eq:noise-retention}
\mathrm{Retensi} = \frac{\mathrm{mAP@10}_{\mathrm{berderau}}}{\mathrm{mAP@10}_{\mathrm{acuan}}}$$

::: keteranganRumus
$\Delta\,\mathrm{mAP@10}$ & perubahan dari kondisi acuan ke kondisi
berderau (negatif jika kinerja turun)\
$\mathrm{Retensi}$ & rasio kinerja berderau terhadap kinerja acuan pada
representasi yang sama
:::

Retensi mendekati 1 menunjukkan bahwa penambahan derau tidak banyak
mengubah kualitas pencarian. Perbandingan berpasangan memastikan bahwa
setiap kueri yang sama diuji pada kedua kondisi, sehingga perubahan
kinerja dapat ditelusuri ke pengaruh derau pada kueri tersebut.

## *Open-set Recognition* dan Kalibrasi Ambang

Dalam pencarian berdasarkan kemiripan, pemeringkatan selalu menghasilkan
rekaman teratas meskipun kueri berasal dari spesies di luar galeri.
Untuk menangani situasi ini, ambang kemiripan digunakan sebagai batas
penerimaan [@you2024openset].

### Kueri Target dan Kontrol di Luar Target

Kueri target berasal dari spesies yang terdapat dalam galeri, sedangkan
kontrol di luar target berasal dari spesies yang tidak ada dalam galeri
atau dari suara lingkungan. Skor kemiripan tertinggi dari pencarian
menentukan penerimaan kueri [@you2024openset]: $$\label{eq:acceptance}
\text{keputusan} =
\begin{cases}
\text{diterima}, & \text{jika } s_{\max} \geq \tau \\
\text{ditolak}, & \text{jika } s_{\max} < \tau
\end{cases}$$

::: keteranganRumus
$s_{\max}$ & skor kosinus tertinggi terhadap galeri untuk satu kueri\
$\tau$ & ambang penerimaan pada representasi yang digunakan
:::

Penerimaan berdasarkan ambang berbeda dari kesesuaian spesies pada hasil
pertama. Kueri yang diterima masih dapat memperoleh hasil teratas dari
spesies yang berbeda.

### Kurva ROC dan Indeks Youden {#subsec:indeks-youden}

Pemilihan ambang memerlukan keseimbangan antara menerima kueri target
dan menolak kueri kontrol. Kurva ROC (*Receiver Operating
Characteristic*) menunjukkan hubungan antara *True Positive Rate* (TPR)
dan *False Positive Rate* (FPR) pada berbagai
ambang [@hassanzad2024youden]: $$\label{eq:tpr}
\mathrm{TPR}(\tau) = \frac{\text{jumlah target yang diterima}}{\text{jumlah seluruh target}}$$
$$\label{eq:fpr}
\mathrm{FPR}(\tau) = \frac{\text{jumlah kontrol yang diterima}}{\text{jumlah seluruh kontrol}}$$

::: keteranganRumus
$\mathrm{TPR}(\tau)$ & proporsi seluruh kueri target yang diterima pada
ambang $\tau$\
$\mathrm{FPR}(\tau)$ & proporsi seluruh kueri kontrol yang diterima pada
ambang yang sama
:::

Indeks Youden memilih ambang yang memaksimalkan selisih antara TPR dan
FPR: $$\label{eq:youden-j}
J(\tau) = \mathrm{TPR}(\tau) - \mathrm{FPR}(\tau)$$
$$\label{eq:youden-opt}
\tau^* = \arg\max_\tau\; J(\tau)$$

::: keteranganRumus
$J(\tau)$ & selisih TPR dan FPR pada ambang kandidat $\tau$\
$\tau^*$ & ambang terpilih pada data kalibrasi
:::

Ambang $\tau^*$ memberikan keseimbangan terbaik antara penerimaan target
dan penolakan kontrol berdasarkan data kalibrasi.

### Ukuran Penerimaan Kueri

Kinerja penerimaan dinilai dengan beberapa
ukuran [@hassanzad2024youden]. Presisi penerimaan mengukur proporsi
kueri yang diterima dengan benar: $$\label{eq:acceptance-precision}
\mathrm{Presisi}_{\mathrm{penerimaan}} = \frac{\text{target diterima}}{\text{target diterima + kontrol diterima}}$$

Skor F1 menggabungkan presisi dan recall penerimaan: $$\label{eq:f1}
\mathrm{F1} = 2 \times \frac{\mathrm{Presisi}_{\mathrm{penerimaan}} \times \mathrm{TPR}}{\mathrm{Presisi}_{\mathrm{penerimaan}} + \mathrm{TPR}}$$

::: keteranganRumus
$\mathrm{TPR}$ & recall penerimaan, yaitu proporsi target yang diterima\
$\mathrm{F1}$ & rata-rata harmonik presisi dan recall pada ambang yang
sama
:::

AUROC (*Area Under the ROC Curve*) merangkum kemampuan skor kemiripan
dalam membedakan target dan kontrol pada seluruh ambang. AUPRC (*Area
Under the Precision-Recall Curve*) merangkum hubungan antara presisi dan
*recall* penerimaan saat ambang digeser. Interpretasinya memperhatikan
proporsi kueri target, yang pada data uji penelitian ini berjumlah 311
dari 621 kueri.

### Margin terhadap Ambang pada Diagnosis Kegagalan

Untuk menelusuri seberapa dekat suatu kueri dengan batas penerimaan,
selisih antara skor tertinggi dan ambang digunakan sebagai
margin [@hassanzad2024youden]: $$\label{eq:margin}
\mathrm{margin} = s_{\max} - \tau$$

::: keteranganRumus
$s_{\max}-\tau$ & jarak bertanda antara skor tertinggi kueri dan ambang
penerimaan
:::

Margin positif atau nol menunjukkan bahwa kueri diterima, sedangkan
margin negatif menunjukkan penolakan. Besarnya margin menggambarkan
jarak skor terhadap ambang: margin negatif yang besar menandakan skor
jauh di bawah ambang, sedangkan margin positif yang kecil menandakan
penerimaan yang marginal. Untuk kueri target, tanda margin dibaca
bersama label spesies pada peringkat pertama. Jika labelnya benar,
margin nol atau positif menunjukkan pencarian dan penerimaan yang
berhasil, sedangkan margin negatif menunjukkan penolakan meski hasil
pertama benar. Jika labelnya salah, margin nol atau positif menunjukkan
kekeliruan spesies yang lolos ambang, sedangkan margin negatif
menunjukkan hasil pertama salah dan kueri ditolak. Audit pendengaran
pada kasus terpilih melengkapi pengelompokan ini dengan catatan tentang
keterdengaran suara burung dan suara latar.

## Profil Derau Lapangan dan Kestabilan Pencarian Antarlokasi

Derau dari lokasi yang berbeda memiliki komposisi suara latar yang
berbeda. Perbedaan ini dapat memengaruhi kinerja pencarian meskipun daya
derau yang ditambahkan sama [@clark2023soundscape].

### Profil Derau dari Lokasi Berbeda

Setiap lokasi perekaman memiliki profil derau yang khas. Lokasi
bervegetasi cenderung memuat suara serangga dan angin, sedangkan lokasi
dekat aktivitas manusia memuat suara kendaraan atau
percakapan [@clark2023soundscape]. Profil yang berbeda dapat mengubah
bagian spektrum yang terpengaruh derau, sehingga efeknya terhadap
pencarian tidak selalu sama meskipun daya derau yang ditambahkan setara.

### Rentang Kinerja pada SNR yang Sama

Kestabilan pencarian antarlokasi diukur dari rentang mAP@10 antara
lokasi dengan kinerja tertinggi dan terendah pada SNR yang
sama [@ghaffari2024frontends]. Karena setiap kombinasi lokasi dan SNR
diuji dengan empat ulangan, rentang dirata-ratakan dari empat ulangan
tersebut: $$\label{eq:range-abs}
\overline{\Delta}_{\mathrm{lokasi}} = \frac{1}{4}\sum_{r=1}^{4}\bigl(\mathrm{mAP@10}_{\max,r} - \mathrm{mAP@10}_{\min,r}\bigr)$$

Rentang relatif diperoleh dengan membagi rentang absolut terhadap mAP@10
acuan: $$\label{eq:range-rel}
\mathrm{Rentang\;relatif} = \frac{\overline{\Delta}_{\mathrm{lokasi}}}{\mathrm{mAP@10}_{\mathrm{acuan}}}$$

::: keteranganRumus
$r$ & indeks satu dari empat ulangan pencampuran\
$\max$ & nilai tertinggi antarlokasi pada ulangan dan SNR yang sama\
$\min$ & nilai terendah antarlokasi pada ulangan dan SNR yang sama\
$\overline{\Delta}_{\mathrm{lokasi}}$ & rata-rata rentang absolut dari
keempat ulangan\
$\mathrm{mAP@10}_{\mathrm{acuan}}$ & kinerja bersih representasi yang
menjadi penyebut rentang relatif
:::

Rentang yang lebih kecil menunjukkan bahwa kinerja representasi lebih
seragam pada beberapa sumber derau yang diuji. Rentang juga dihitung
kembali dengan mengeluarkan satu lokasi secara bergantian untuk
memeriksa apakah lokasi tertentu memberikan pengaruh yang tidak
proporsional terhadap hasil perbandingan.

## Kebocoran Data, Ketertelusuran, dan Keterulangan Penelitian

Pembagian data dan dokumentasi eksperimen memengaruhi kepercayaan
terhadap hasil penelitian. Kebocoran data terjadi ketika informasi dari
data uji masuk ke proses yang seharusnya independen, misalnya ketika
rekaman dari perekam yang sama tersebar di kelompok latih dan
uji [@kapoor2023leakage].

### Pemisahan Rekaman Berdasarkan Perekam

Untuk mengurangi pengaruh kesamaan perangkat, cara merekam, atau suara
latar terhadap perbandingan pencarian, seluruh rekaman dari perekam yang
sama ditempatkan dalam satu kelompok [@kapoor2023leakage]. Pemisahan ini
mencegah informasi dari perekam yang sama menguntungkan hasil pencarian
karena ciri rekaman yang serupa. Nama perekam diseragamkan dan diperiksa
antarkelompok sebelum pengujian dilakukan.

### Ketertelusuran Data dan Pengaturan Eksperimen

Keterulangan penelitian memerlukan pencatatan identitas rekaman,
pengaturan eksperimen, dan berkas yang digunakan [@kapoor2023leakage].
Kode katalog digunakan untuk menelusuri rekaman ke sumber aslinya. Nilai
SHA-256 memeriksa apakah berkas masih sama dengan yang digunakan pada
pengujian. Manifes eksperimen mencatat pembagian data, parameter
prapemrosesan, dan konfigurasi pencampuran agar hasilnya dapat diulang
dengan data dan pengaturan yang sama.

## Landasan Statistik

Perbandingan kinerja antarrepresentasi atau antarkondisi memerlukan
penilaian ketidakpastian agar selisih yang diamati dapat dibedakan dari
variasi acak [@rousselet2021bootstrap].

### Selisih Kinerja Berpasangan

Karena kueri yang sama diuji pada beberapa representasi dan kondisi,
selisih kinerja dihitung secara berpasangan [@rousselet2021bootstrap]:
$$\label{eq:paired-diff}
\delta_q = m_{A,q} - m_{B,q}$$

Rata-rata selisih berpasangan menunjukkan arah dan besarnya perbedaan
secara keseluruhan: $$\label{eq:mean-diff}
\bar{\delta} = \frac{1}{Q}\sum_{q=1}^{Q}\delta_q$$

::: keteranganRumus
$m_{A,q}$ & nilai metrik untuk kueri ke-$q$ pada kondisi atau
representasi $A$\
$m_{B,q}$ & nilai metrik untuk kueri yang sama pada kondisi atau
representasi $B$\
$\delta_q$ & selisih nilai metrik untuk kueri ke-$q$\
$\bar\delta$ & rata-rata selisih seluruh $Q$ kueri
:::

### *Bootstrap* Berpasangan dan Interval Kepercayaan

*Bootstrap* berpasangan memperkirakan ketidakpastian suatu statistik
dengan mengambil ulang pasangan pengamatan secara acak dengan
pengembalian. Pada setiap sampel ulang, pasangan tetap utuh dan
statistik yang dibandingkan dihitung kembali. Statistik tersebut dapat
berupa rata-rata selisih, rasio, atau rentang. Batas interval
kepercayaan persentil 95% adalah persentil ke-2,5 dan ke-97,5 dari
distribusi statistik hasil pengambilan ulang [@rousselet2021bootstrap].
Persamaan berikut menunjukkan bentuknya untuk rata-rata selisih.
$$\label{eq:bootstrap}
\bar{\delta}^{*(b)} = \frac{1}{Q}\sum_{q \in S^{(b)}}\delta_q$$

::: keteranganRumus
$b$ & indeks sampel ulang\
$S^{(b)}$ & daftar $Q$ indeks pasangan pengamatan yang ditarik dengan
pengembalian\
$\bar{\delta}^{*(b)}$ & rata-rata selisih pada sampel ulang ke-$b$,
dengan setiap kemunculan pasangan ikut dihitung
:::

[^1]: <https://librosa.org/doc/0.11.0/generated/librosa.mel_frequencies.html>
