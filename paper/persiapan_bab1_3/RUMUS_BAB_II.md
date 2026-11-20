# Rumus dan gambar acuan BAB II

Bahan kerja untuk susunan BAB II yang direncanakan. Rumus utama mengikuti perhitungan di kode TA. Keterangan sumber dicantumkan untuk membantu memilih sitasi sebelum penulisan.

## 2.2 Sinyal Audio Digital dan Prapemrosesan

**Jumlah sampel dan penggabungan kanal**

$$
N_\mathrm{seg}=f_sT,
\qquad x_{\mathrm{mono}}[n]=\frac{1}{C}\sum_{c=1}^{C}x_c[n].
$$

$f_s$ adalah laju sampel (Hz), $T$ durasi segmen (detik), dan $C$ jumlah kanal. Audio disiapkan pada $f_s=32.000$ Hz dan $T=5$ detik, sehingga satu segmen berisi $160.000$ sampel.

**Pemilihan segmen dan penyesuaian RMS**

$$
\operatorname{RMS}(x)=\sqrt{\frac{1}{N}\sum_{n=0}^{N-1}x[n]^2},
\qquad
i^*=\arg\max_i \operatorname{RMS}(x_i).
$$

$x_i$ adalah kandidat segmen berdurasi lima detik. Pada rekaman yang lebih panjang, kandidat diperiksa dengan langkah 1,25 detik. Rekaman lebih pendek dilengkapi nol di bagian akhir.

$$
x_{\mathrm{prep}}[n]=\operatorname{clip}_{[-1,1]}\!\left(\eta\,x[n]\right),
\qquad
\eta=
\begin{cases}
0{,}05/\operatorname{RMS}(x), & \operatorname{RMS}(x)>10^{-6},\\
1, & \operatorname{RMS}(x)\leq 10^{-6}.
\end{cases}
$$

$\eta$ adalah faktor penyesuaian amplitudo. Pembatasan amplitudo dapat membuat RMS akhir berbeda dari target. [Implementasi prapemrosesan](../../src/preprocess.py)

## 2.3 Representasi Audio Berbasis MFCC

**STFT dan spektrum daya**

$$
X[k,j]=\sum_{n=0}^{L-1}x[n+jH]\,w[n]\,e^{-2\pi\mathrm{i}kn/L},
\qquad P[k,j]=|X[k,j]|^2.
$$

$L$ adalah panjang jendela (sampel), $H$ langkah antarjendela (sampel), $w[n]$ fungsi jendela, $j$ indeks *frame*, dan $k$ indeks frekuensi. Tumpang tindihnya $L-H$. Kode MFCC TA menetapkan $L=1.024$ dan $H=512$ sampel. [Jeon dkk. (2020), Persamaan 1](https://www.mdpi.com/2076-3417/10/20/7208) · [Kode MFCC](../../src/mfcc.py)

**Energi pita mel dan pembentukan MFCC**

Bank filter bawaan *librosa* menempatkan pita berdasarkan skala mel Slaney. Untuk frekuensi $f$ dalam Hz, konversinya adalah [Implementasi skala mel *librosa*](https://librosa.org/doc/0.11.0/_modules/librosa/core/convert.html#hz_to_mel)

$$
\operatorname{mel}(f)=
\begin{cases}
3f/200, & 0\le f<1000,\\
15+\dfrac{27}{\ln(6{,}4)}\ln(f/1000), & f\ge1000.
\end{cases}
$$

$$
E[m,j]=\sum_k W_m[k]\,P[k,j],
\qquad
D[m,j]=10\log_{10}\!\left(\max(E[m,j],\epsilon)\right).
$$

$W_m[k]$ adalah bobot filter segitiga ke-$m$ pada frekuensi $k$, $E[m,j]$ energi pada pita mel, dan $\epsilon$ adalah batas kecil sebelum operasi logaritma. Implementasi menggunakan bank filter bawaan *librosa* dan batas bawah rentang desibel bawaan (80 dB di bawah nilai puncak).

$$
c_d[j]=a_d\sum_{m=0}^{M-1}D[m,j]\,
       \cos\!\left[\frac{\pi d}{M}\left(m+\frac12\right)\right],
\qquad
a_d=
\begin{cases}
1/\sqrt{M}, & d=0,\\
\sqrt{2/M}, & d>0.
\end{cases}
$$

$M$ adalah jumlah pita mel dan $c_d[j]$ koefisien MFCC ke-$d$. Perhitungan memakai DCT tipe II dengan normalisasi ortonormal dan mengambil 20 koefisien. [Peng dkk. (2025), Bagian 4.2.1](https://www.mdpi.com/2076-3417/15/9/4913) · [Dokumentasi MFCC *librosa*](https://librosa.org/doc/main/api/generated/librosa.feature.mfcc.html)

**Ringkasan MFCC per rekaman**

$$
\mu_d=\frac{1}{J}\sum_{j=1}^{J}c_d[j],
\qquad
\sigma_d=\sqrt{\frac{1}{J}\sum_{j=1}^{J}(c_d[j]-\mu_d)^2},
\qquad
\mathbf{v}=[\mu_0,\ldots,\mu_{19},\sigma_0,\ldots,\sigma_{19}].
$$

$J$ adalah jumlah *frame*. Penggabungan rata-rata dan simpangan baku populasi menghasilkan vektor 40 komponen. [Kode MFCC](../../src/mfcc.py)

## 2.4 Representasi Audio Pralatih

**Rata-rata vektor BirdNET antarjendela**

$$
\bar{\mathbf{e}}=\frac{1}{J}\sum_{j=1}^{J}\mathbf{e}_j.
$$

$\mathbf{e}_j$ adalah vektor BirdNET 1.024 komponen pada jendela ke-$j$. BirdNET memakai 48 kHz, jendela tiga detik, dan langkah satu detik. Satu masukan lima detik menghasilkan tiga vektor yang dirata-ratakan sebelum normalisasi. PANNs CNN14 mengembalikan satu vektor 2.048 komponen per klip dari keluaran model. Bobot keduanya tetap saat evaluasi. [Implementasi PANNs dan BirdNET](../../src/embeddings.py)

## 2.5 Ruang Embedding, Normalisasi L2, dan Kemiripan Kosinus

**Normalisasi L2 dan skor kosinus**

$$
\|\mathbf{v}\|_2=\sqrt{\sum_{i=1}^{d}v_i^2},
\qquad
\hat{\mathbf{v}}=\frac{\mathbf{v}}{\|\mathbf{v}\|_2},
\qquad
\operatorname{sim}(\mathbf{q},\mathbf{g})
 =\frac{\mathbf{q}^{\mathsf T}\mathbf{g}}{\|\mathbf{q}\|_2\|\mathbf{g}\|_2}
 =\hat{\mathbf{q}}^{\mathsf T}\hat{\mathbf{g}}.
$$

$d$ adalah dimensi vektor, $\mathbf{q}$ vektor kueri, dan $\mathbf{g}$ vektor galeri dari representasi yang sama. Persamaan berlaku untuk vektor dengan norma bukan nol. Hasil diurutkan dari skor kosinus tertinggi. [Implementasi pencarian](../../src/retrieve.py)

## 2.6 Audio Similarity Retrieval dan Metrik Evaluasi

Misalkan $\mathrm{rel}_{q,i}$ bernilai 1 jika hasil peringkat $i$ memiliki label spesies yang sama dengan kueri $q$, dan 0 jika berbeda. $N_q$ adalah jumlah rekaman relevan bagi kueri dalam seluruh galeri. $\mathcal Q$ adalah himpunan kueri yang dinilai.

**Precision@$k$ dan Recall@$k$**

$$
P@k(q)=\frac{1}{k}\sum_{i=1}^{k}\mathrm{rel}_{q,i},
\qquad
R@k(q)=\frac{1}{N_q}\sum_{i=1}^{k}\mathrm{rel}_{q,i}.
$$

Gunakan $k=10$ untuk hasil utama yang dilaporkan. Kode membatasi $k$ sesuai ukuran galeri bila galeri lebih kecil, dan menetapkan *recall* nol bila $N_q=0$.

**AP@10 dan mAP@10**

$$
AP@10(q)=\frac{\sum_{i=1}^{10}P@i(q)\mathrm{rel}_{q,i}}{\min(N_q,10)},
\qquad
mAP@10=\frac{1}{|\mathcal Q|}\sum_{q\in\mathcal Q}AP@10(q).
$$

AP@10 bernilai nol bila $N_q=0$. mAP@10 adalah metrik utama. Penyebut AP@10 mengikuti definisi operasional TA.

**MRR dan Top-1**

$$
RR(q)=\frac{1}{r_q},
\qquad
MRR=\frac{1}{|\mathcal Q|}\sum_{q\in\mathcal Q}RR(q),
\qquad
\mathrm{Top\mbox{-}1}=\frac{1}{|\mathcal Q|}\sum_{q\in\mathcal Q}\mathrm{rel}_{q,1}.
$$

$r_q$ adalah peringkat hasil relevan pertama pada seluruh daftar. Jika galeri tidak menghasilkan rekaman relevan, kontribusi $RR(q)$ bernilai nol. [Implementasi metrik](../../src/retrieve.py) · [Acuan metrik di BAB II](../template_ta_latex/chapters/bab2.tex)

## 2.7 Ketahanan terhadap Derau

**Daya sinyal dan pencampuran pada SNR terkontrol**

$$
P(x)=\frac{1}{N}\sum_{n=0}^{N-1}x[n]^2,
\qquad
\operatorname{SNR}_{\mathrm{dB}}=10\log_{10}\frac{P(s)}{P(\alpha b)}.
$$

$$
\alpha=\sqrt{\frac{P(s)}{P(b)\,10^{\gamma/10}}},
\qquad
z[n]=s[n]+\alpha b[n].
$$

$s[n]$ adalah rekaman kueri acuan, $b[n]$ segmen derau Itera, $\gamma$ SNR sasaran, dan $z[n]$ campuran awal. Penelitian memakai $\gamma\in\{+20,+10,0,-5\}$ dB. Bila puncak campuran melebihi satu, kode mengalikan seluruh campuran dengan faktor yang sama:

$$
g={1\over\max\{1,\max_n|z[n]|\}},
\qquad x_{\mathrm{uji}}[n]=g\,z[n].
$$

Kedua komponen menerima faktor $g$ yang sama sehingga rasio dayanya tetap. Kueri acuan adalah rekaman tanpa penambahan derau Itera dan dapat mengandung suara latar asal. [Kode pencampuran](../../src/mix_noise.py)

**Perubahan kualitas dan retensi**

$$
\Delta M_\gamma=M_\gamma-M_{\mathrm{acuan}},
\qquad
\rho_\gamma=\frac{M_\gamma}{M_{\mathrm{acuan}}},
\qquad \text{retensi dalam persen}=100\,\rho_\gamma.
$$

$M_\gamma$ adalah mAP@10 kueri dengan derau tambahan pada SNR $\gamma$. $M_{\mathrm{acuan}}$ adalah mAP@10 kueri yang sama tanpa penambahan derau. Retensi dihitung jika $M_{\mathrm{acuan}}>0$. [Kode evaluasi ketahanan](../../scripts/run_e2_controlled_noise.py)

## 2.8 Open-Set Recognition dan Kalibrasi Ambang

**Skor terbaik, keputusan, dan tingkat penerimaan**

$$
s_{\max}(q)=\max_{\mathbf{g}\in\mathcal G}\operatorname{sim}(\mathbf{q},\mathbf{g}),
\qquad
\hat y_\tau(q)=\mathbf{1}[s_{\max}(q)\geq\tau].
$$

$\mathcal G$ adalah galeri. $\hat y_\tau(q)=1$ berarti kueri diterima. Untuk tugas penerimaan, kelas positif adalah kueri target, sedangkan kelas negatif adalah kueri kontrol di luar target. Ketepatan label spesies di peringkat pertama dicatat terpisah.

$$
\operatorname{TPR}(\tau)=\frac{TP}{TP+FN},
\qquad
\operatorname{FPR}(\tau)=\frac{FP}{FP+TN},
\qquad
J(\tau)=\operatorname{TPR}(\tau)-\operatorname{FPR}(\tau).
$$

$TP$ dan $FN$ adalah jumlah kueri target yang diterima dan ditolak. $FP$ dan $TN$ adalah jumlah kueri kontrol yang diterima dan ditolak. Ambang dipilih per representasi dari kandidat ambang kurva ROC pada data kalibrasi:

$$
\tau^*=\arg\max_{\tau\in\mathcal T_{\mathrm{kal}}}J(\tau).
$$

$\mathcal T_{\mathrm{kal}}$ berisi ambang ROC yang berhingga dengan $0{,}01<\tau<0{,}9999$ sesuai kode. $\tau^*$ dipertahankan untuk pengujian. Perubahan penerimaan dihitung sebagai tingkat pada kondisi berderau dikurangi tingkat pada kondisi acuan. [Kode kalibrasi](../../src/calibrate_threshold.py) · [You dkk. (2024), konsep *open-set* audio](https://doi.org/10.1038/s41598-023-50639-7) · [Hassanzad dan Hajian-Tilaki (2024), indeks Youden](https://doi.org/10.1186/s12874-024-02198-2)

**Metrik pendukung pada tabel kalibrasi**

$$
\operatorname{Presisi}(\tau)=\frac{TP}{TP+FP},
\qquad
F_1(\tau)=\frac{2TP}{2TP+FP+FN}.
$$

AUROC adalah luas di bawah kurva TPR terhadap FPR pada berbagai ambang. Ringkasan kalibrasi mencatat AUROC dari skor terbaik tiap kueri dan $F_1$ pada ambang yang dipilih. [Kode ringkasan kalibrasi](../../scripts/run_e3_open_set.py) · [Dokumentasi AUROC](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html)

## 2.9 Profil Derau Lapangan dan Kestabilan Pencarian

**Rentang kinerja antarlokasi**

$$
W_{\mathrm{abs}}(m,\gamma)
 =\frac1B\sum_{r=1}^{B}
   \left(\max_{\ell\in\mathcal L}M_{m,\gamma,r,\ell}
        -\min_{\ell\in\mathcal L}M_{m,\gamma,r,\ell}\right),
\qquad
W_{\mathrm{rel}}(m,\gamma)=\frac{W_{\mathrm{abs}}(m,\gamma)}{M_{m,\mathrm{acuan}}}.
$$

$M_{m,\gamma,r,\ell}$ adalah mAP@10 representasi $m$ pada SNR $\gamma$, ulangan $r$, dan lokasi $\ell$. $\mathcal L$ berisi lokasi yang dibandingkan. $B=4$ adalah jumlah ulangan dan $M_{m,\mathrm{acuan}}$ adalah mAP@10 kondisi acuan. Rentang dihitung per ulangan sebelum dirata-ratakan. [Implementasi analisis kestabilan](../../scripts/run_h3_sensitivity_reanalysis.py)

## 2.10 Kebocoran Data, Ketertelusuran, dan Reproduksibilitas

Bagian ini berisi prosedur. Rekaman target dipisah menurut perekam, SHA-256 diperiksa untuk mendeteksi berkas identik, dan identitas data serta parameter eksperimen dicatat pada manifes dan keluaran run. [Audit manifes](../../scripts/audit_manifests.py) · [Kapoor dan Narayanan (2023)](https://doi.org/10.1016/j.patter.2023.100804)

## 2.11 Landasan Statistik

**Selisih berpasangan dan interval bootstrap**

$$
\delta_q=AP@10_{\mathrm{derau}}(q)-AP@10_{\mathrm{acuan}}(q),
\qquad
\bar\delta=\frac{1}{|\mathcal Q|}\sum_{q\in\mathcal Q}\delta_q.
$$

$\delta_q$ adalah perubahan kualitas untuk kueri yang sama. Untuk interval pada analisis kestabilan antarlokasi, ulangi pengambilan sampel ID kueri dengan pengembalian. Satu set ID ulang dipakai bersama untuk seluruh kondisi dan model yang dibandingkan. Pada setiap ulangan, hitung ulang rentang antarlokasi untuk PANNs dan BirdNET, lalu ambil selisih keduanya:

$$
D^{*(b)}=W^{*(b)}_{\mathrm{PANNs}}-W^{*(b)}_{\mathrm{BirdNET}},
\qquad
IC_{95\%}=[Q_{0{,}025}(D^*),\,Q_{0{,}975}(D^*)].
$$

$Q_p$ adalah kuantil empiris pada proporsi $p$. Analisis kestabilan menggunakan 10.000 pengulangan *bootstrap*. Intervalnya bersifat eksploratif dan bergantung pada lokasi dan segmen derau yang diuji. [Kode bootstrap](../../scripts/run_h3_sensitivity_reanalysis.py) · [Ringkasan run](../../results/reproductions/H3_rerun_20261116T132030_189809Z/README.md)

## Rumus pendukung analisis kegagalan (E5)

Siapkan bagian ini untuk diagnostik. Penjelasan singkat dapat dipakai di BAB II, sementara rincian penerapannya dapat diletakkan di BAB III.

$$
\mathrm{margin}(q)=s_{\max}(q)-\tau^*,
\qquad
C_j=\frac{\sum_k f_k A[k,j]}{\sum_k A[k,j]},
\qquad
B_j=\sqrt{\frac{\sum_k A[k,j](f_k-C_j)^2}{\sum_k A[k,j]}}.
$$

$f_k$ adalah frekuensi (Hz), $A[k,j]$ magnitudo spektrum, $C_j$ *spectral centroid*, dan $B_j$ *spectral bandwidth* pada *frame* $j$. Kedua ciri spektral dirata-ratakan antar-*frame*. Pada run diagnostik baru, deskriptor spektral dihitung untuk klip E2 yang direkonstruksi. [Kode diagnostik](../../scripts/run_e5_diagnostics.py)

## Gambar yang digambar ulang

| Untuk bagian | Berkas | Acuan dan catatan pemakaian |
|---|---|---|
| 2.3 STFT | [Ilustrasi STFT](../figures/bab2/stft_adaptasi_jeon_2020.png) | Diadaptasi dari **Gambar 1** Jeon dkk. (2020). Gelombang, jendela, dan keluaran FFT dihitung ulang dari sinyal sintetis. [Artikel](https://www.mdpi.com/2076-3417/10/20/7208) |
| 2.3 MFCC | [Tahapan ekstraksi MFCC dan FBank](../figures/bab2/ekstraksi_mfcc_fbank_adaptasi_peng_2025.png) | Diadaptasi dari **Gambar 5** Peng dkk. (2025). Pengurangan derau dan *pre-emphasis* pada gambar merupakan bagian dari acuan. Jalur MFCC TA dimulai dari audio yang sudah dipraproses dan melanjutkan ekstraksi tanpa kedua tahap tambahan tersebut. [Artikel](https://www.mdpi.com/2076-3417/15/9/4913) |
| 2.7 SNR | [Gelombang dan spektrogram pada 0 dB dan 35 dB](../figures/bab2/gelombang_spektrogram_snr_adaptasi_chen_2023.png) | Diadaptasi dari **Gambar 5** Chen dkk. (2023). Panel memakai campuran sintetis, dengan SNR didefinisikan per kejadian bunyi dalam ilustrasi. Titik merah menunjukkan daya spektral tertinggi tiap panel. Skala amplitudo panel A dan B berbeda. SNR 35 dB dipakai untuk ilustrasi acuan. [Artikel](https://www.frontiersin.org/journals/remote-sensing/articles/10.3389/frsen.2022.1079223/full) |

[Kode pembuat ketiga gambar](../../results/figures/buat_gambar_bab2.py).

