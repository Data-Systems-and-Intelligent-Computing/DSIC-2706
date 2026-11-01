# 3. Perhitungan langkah demi langkah

**Angka pada bagian bertanda CONTOH adalah angka buatan untuk latihan.** Angka bertanda HASIL TA berasal dari tabel penelitian. Desimal memakai koma pada penjelasan; kode dan CSV memakai titik. Kalkulator ilmiah cukup untuk latihan ini.

## A. Rata-rata, daya, RMS, dan simpangan baku

**CONTOH daya/RMS:** sinyal empat sampel `[0,2; −0,2; 0,2; −0,2]`.

1. Kuadratkan: `[0,04; 0,04; 0,04; 0,04]`.
2. Rata-rata kuadrat = `(0,04 + 0,04 + 0,04 + 0,04) / 4 = 0,04`. Inilah daya rata-rata P dalam perhitungan campuran digital.
3. `RMS = akar(P) = akar(0,04) = 0,2`.

**CONTOH pooling MFCC:** satu koefisien pada tiga frame bernilai `[1; 3; 5]`.

1. Mean = `(1+3+5)/3 = 3`.
2. Selisih dari mean = `[-2; 0; 2]`.
3. Kuadrat selisih = `[4; 0; 4]`.
4. Varians untuk pooling kode = `8/3`.
5. Std = `akar(8/3) = 1,632993`.

Di sini pembaginya N, sesuai `numpy.std` default, bukan N−1. Dua puluh koefisien masing-masing memiliki mean dan std: `20+20=40` angka sebelum normalisasi L2.

## B. Normalisasi L2 dan cosine similarity

**CONTOH:** kueri q = `[1; 2]`, galeri g = `[2; 1]`.

1. Dot product: `q·g = 1×2 + 2×1 = 4`.
2. Panjang q: `||q|| = akar(1²+2²) = akar(5)`.
3. Panjang g juga `akar(5)`.
4. `cosine(q,g) = 4 / (akar(5)×akar(5)) = 4/5 = 0,8`.
5. Vektor q yang dinormalisasi: `[1/akar(5); 2/akar(5)] ≈ [0,447214; 0,894427]`.

Jika keduanya sudah memiliki panjang satu, cosine cukup dihitung dengan dot product. Rentang matematis cosine adalah −1 sampai +1 untuk vektor tak nol. Nilai 0,8 bukan peluang 80% bahwa spesiesnya benar. Distribusi skor tiap representasi berbeda sehingga nilai ambang juga berbeda.

## C. SNR dan skala derau

Rumus dasar:

```text
SNR_dB = 10 × log10(P_target / P_derau)
P_target / P_derau = 10^(SNR_dB / 10)
y = x + alpha × n
alpha = akar(P_x / (P_n × 10^(SNR_dB / 10)))
```

x adalah komponen target; n komponen derau sebelum skala alpha; y campurannya. Gunakan daya **komponen**, bukan daya total campuran, untuk mengecek rasio target–derau.

**CONTOH:** `P_x=0,04`, `P_n=0,01`. Nilai daya ini contoh, berbeda dari skala RMS normalisasi standar TA.

| SNR | Langkah alpha | alpha | Daya derau setelah skala |
|---|---|---:|---:|
| +20 | akar(0,04/(0,01×100)) | 0,200000 | 0,000400 |
| +10 | akar(0,04/(0,01×10)) | 0,632456 | 0,004000 |
| 0 | akar(0,04/(0,01×1)) | 2,000000 | 0,040000 |
| −5 | akar(0,04/(0,01×0,316228)) | 3,556559 | 0,126491 |

Cek untuk −5 dB: `10×log10(0,04/0,126491) ≈ −5`. Daya derau sekitar 3,162 kali daya target. Perbandingan RMS-nya sekitar 1,778 kali; rasio daya dan amplitudo tidak sama.

Mengapa rumus daya memakai 10 log, sedangkan perbandingan RMS dapat memakai 20 log? Karena daya sebanding dengan kuadrat RMS: `10 log(a²)=20 log(a)` untuk rasio amplitudo/RMS positif.

Dalam kode TA, derau juga dinormalisasi RMS sebelum alpha dihitung. Jika campuran berisiko melampaui batas amplitudo, kedua komponen dikalikan faktor global yang sama. Rasionya tetap: `(c² P_x)/(c² P_derau)=P_x/P_derau`. Pemeriksaan ini tidak boleh disamakan dengan mengklaim seluruh rantai praproses bebas clipping.

## D. Menghitung metrik satu kueri

Kode menganggap rekaman relevan jika **spesiesnya sama dengan kueri**. Misalkan ada **20 rekaman relevan di seluruh galeri**. Sepuluh hasil teratas memiliki pola berikut.

| Peringkat i | Relevan? rel(i) | Jumlah benar sampai i | Precision sampai i | Sumbangan untuk AP |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 1/1 = 1 | 1 |
| 2 | 0 | 1 | 1/2 | 0 |
| 3 | 1 | 2 | 2/3 | 2/3 |
| 4 | 1 | 3 | 3/4 | 3/4 |
| 5 | 0 | 3 | 3/5 | 0 |
| 6 | 0 | 3 | 3/6 | 0 |
| 7 | 0 | 3 | 3/7 | 0 |
| 8 | 0 | 3 | 3/8 | 0 |
| 9 | 0 | 3 | 3/9 | 0 |
| 10 | 0 | 3 | 3/10 | 0 |

**Top-1 match = 1**, sebab hasil pertama benar. **P@10 = 3/10 = 0,30. Recall@10 = 3/20 = 0,15.**

Rumus AP@k **yang digunakan kode TA**:

```text
AP@k = jumlah_{i=1..k'} [Precision@i × rel(i)] / min(R, k')
k' = min(k, jumlah galeri)
R = seluruh jumlah rekaman relevan di galeri
```

Untuk contoh: `AP@10 = (1 + 2/3 + 3/4)/min(20,10) = 2,416667/10 = 0,241667`.

Mengapa bukan dibagi tiga? Pembaginya menurut implementasi TA adalah jumlah relevan yang mungkin ditampung dalam k hasil, bukan jumlah yang kebetulan ditemukan. Definisi AP terpotong dapat berbeda antarsumber/perangkat; ketika ujian, nyatakan definisi yang dipakai dan rujuk kode.

Jika seluruh galeri hanya mempunyai **tiga** rekaman relevan dengan pola tiga temuan yang sama, AP@10 menjadi `2,416667/3 = 0,805556` dan Recall@10 menjadi `3/3 = 1`. Karena itu jumlah relevan di galeri harus diketahui.

**Reciprocal Rank (RR)** = `1/peringkat temuan relevan pertama`. Pada contoh RR=1. Jika temuan pertama di urutan 4, RR=0,25. Kode TA menghitung RR atas seluruh galeri; jangan menyebutnya otomatis RR@10.

## E. Dari AP menjadi mAP

**CONTOH:** dua kueri memiliki AP@10 sebesar 0,241667 dan 0,500000.

`mAP@10 = (0,241667+0,500000)/2 = 0,370833`.

**HASIL TA:** rata-rata dihitung atas 311 kueri. Kueri berbobot sama; spesies dengan lebih banyak kueri menyumbang lebih banyak pada rata-rata. Ini berbeda dari menghitung rata-rata per spesies dahulu lalu merata-ratakan 20 spesies.

Top-1 Accuracy juga dirata-ratakan atas kueri: bila 254 dari 311 kueri benar pada urutan pertama, `254/311 = 0,816720 = 81,6720%`, sesuai hasil R2 E1. mAP@10 0,636709 tidak berarti 63,67% rekaman atau spesies pasti dikenali; mAP adalah ukuran kualitas ranking.

## F. Mengapa Recall@10 tidak selalu bisa mencapai 100%?

Jika ada R rekaman relevan dalam galeri, sepuluh posisi hanya dapat memuat paling banyak `min(10,R)` rekaman relevan.

```text
Batas Recall@10 per kueri = min(10,R)/R
```

**CONTOH:** R=50 → batasnya 10/50=0,20, walaupun seluruh sepuluh hasil benar. Jika R=20, batasnya 0,50. Ini berbeda dengan Precision@10 yang bisa bernilai 1 ketika semua sepuluh hasil benar.

**HASIL TA:** per spesies terdapat 15–100 rekaman galeri. Setelah batas setiap kueri dirata-ratakan dengan bobot 311 kueri, batas rata-rata Recall@10 = **0,363997**. Recall@10 R2 E1 aktual = **0,233109**. Jangan menilainya seolah-olah batasnya selalu 1. Jangan pula menyebut 0,233109/0,363997 sebagai metrik resmi baru tanpa definisi dan persetujuan pelaporan.

## G. Retensi dan penurunan

```text
Retensi = mAP_bising / mAP_bersih
Penurunan absolut = mAP_bersih − mAP_bising
Penurunan relatif = 1 − retensi
```

**HASIL TA R2, E2 −5 dB:** bersih 0,6367085183; bising 0,4831600572.

1. Retensi = `0,4831600572 / 0,6367085183 = 0,758840 ≈ 75,8840%`.
2. Penurunan absolut = `0,6367085183−0,4831600572 = 0,1535484612` satuan mAP.
3. Penurunan relatif = `1−0,758840 = 0,241160 ≈ 24,1160%` dari acuan bersih.

Jika mAP ditampilkan pada skala 0–100, penurunan absolut itu 15,3548 poin pada skala tersebut. Jangan menukar persen penurunan relatif dengan poin absolut. Retensi dapat melebihi 1 bila hasil bising lebih baik daripada acuan pada kondisi tertentu; ini bukan otomatis kesalahan hitung. R3 beretensi 100% karena vektornya tidak berubah mengikuti audio, sehingga retensinya tidak membuktikan ketahanan pendengaran.

## H. Ambang penerimaan dan confusion matrix open-set

Ambil skor terbesar terhadap galeri: `s_max`. Terima jika `s_max >= tau`; jika lebih kecil, tolak. Tanda sama dengan ikut diterima.

| Acuan sebenarnya | Sistem menerima | Sistem menolak |
|---|---|---|
| Known/target | TP | FN |
| Unknown | FP | TN |

“Positif” di E3 berarti **diterima sebagai known**, bukan “spesies teratas pasti benar”.

**CONTOH:** TP=8, FN=2, FP=3, TN=7.

```text
Recall penerimaan / TPR = TP/(TP+FN) = 8/10 = 0,8
FPR = FP/(FP+TN) = 3/10 = 0,3
Specificity = TN/(TN+FP) = 7/10 = 0,7
Precision penerimaan = TP/(TP+FP) = 8/11 = 0,727273
F1 = 2TP/(2TP+FP+FN) = 16/21 = 0,761905
Youden J = TPR−FPR = 0,8−0,3 = 0,5
```

Precision penerimaan E3 berbeda dari Precision@10. Recall penerimaan E3 berbeda dari Recall@10. Yang satu menghitung keputusan kueri; yang lain menghitung hasil galeri relevan dalam ranking.

## I. Bagaimana memilih tau dari kalibrasi?

**CONTOH kalibrasi:** skor known `[0,9;0,8;0,7;0,4]`, unknown `[0,6;0,5;0,3;0,1]`.

| Kandidat tau | Known diterima /4 | Unknown diterima /4 | J |
|---:|---:|---:|---:|
| 0,9 | 1/4 | 0/4 | 0,25 |
| 0,8 | 2/4 | 0/4 | 0,50 |
| 0,7 | 3/4 | 0/4 | 0,75 |
| 0,6 | 3/4 | 1/4 | 0,50 |
| 0,5 | 3/4 | 2/4 | 0,25 |
| 0,4 | 4/4 | 2/4 | 0,50 |
| 0,3 | 4/4 | 3/4 | 0,25 |
| 0,1 | 4/4 | 4/4 | 0,00 |

Nilai terbaik J=0,75 pada tau=0,7. Sesudah itu tau dibekukan, lalu diuji pada data uji terpisah. Tabel contoh menampilkan semua skor unik agar mudah dihitung; kode utama memakai kandidat ROC empiris, menyaring nilai tak hingga dan kandidat di luar `0,01 < tau < 0,9999`. Ketika J sama, kode mempertahankan kandidat pertama yang mencapai maksimum. Jangan menyebut prosesnya mencari tau terbaik pada data uji.

**HASIL TA R2:** tau sekitar 0,702785, berasal dari 232 known + 233 unknown kalibrasi. Angka 0,7 pada contoh bukan pengganti ambang hasil penelitian.

**AUROC** merangkum pemisahan skor known–unknown pada berbagai ambang. Cara sederhana memahaminya adalah proporsi pasangan known–unknown yang skornya terurut benar, dengan setengah kredit untuk seri. **CONTOH:** known `[0,9;0,4]`, unknown `[0,8;0,3]`; dari empat pasangan ada tiga yang benar, AUROC=3/4=0,75. AUROC tidak bergantung hanya pada satu tau beku. AUPRC E3 dihitung sebagai luas kurva precision–recall; berbeda dari AP@10 retrieval.

## J. H3 absolut dan relatif

Pertama hitung rata-rata AP@10 dari 311 kueri pada setiap kombinasi lokasi–SNR–ulangan. Sebut A. Acuan bersih suatu representasi disebut C.

```text
Ayunan absolut per ulangan = A_lokasi_tertinggi − A_lokasi_terendah
S_abs = rata-rata ayunan itu atas empat ulangan
S_rel = S_abs / C
```

**CONTOH:** metode A mempunyai C=0,60 dan ayunan absolut 0,06 → ayunan relatif 0,10. Metode B mempunyai C=0,20 dan ayunan absolut 0,04 → ayunan relatif 0,20. B lebih kecil secara absolut, tetapi lebih besar terhadap acuan bersihnya. Keduanya menjawab pertanyaan berbeda.

**Urutan agregasi harus benar. CONTOH dua lokasi:** pada ulangan 1 nilainya 0,6 dan 0,4; pada ulangan 2 nilainya 0,4 dan 0,6; pola ini terulang pada ulangan 3–4. Rentang setiap ulangan 0,2 sehingga mean rentang 0,2. Jika lokasi dirata-ratakan dahulu, keduanya menjadi 0,5 dan rentangnya 0. H3 memakai cara pertama.

**HASIL TA, lima lokasi, rata-rata empat SNR:**

| Ukuran | R1 | R2 | R1−R2 |
|---|---:|---:|---:|
| Ayunan absolut | 0,042324 | 0,030949 | 0,011375 |
| Ayunan relatif | 0,240111 | 0,048607 | 0,191504 |

CI selisih absolut `[−0,003993;0,022140]` melintasi nol, sehingga belum membedakan ayunan rata-rata absolut secara meyakinkan. CI selisih relatif `[0,152203;0,241969]` berada di atas nol dalam analisis eksploratif ini.

Pada −5 dB, ayunan absolut lima lokasi R2=0,061829 **lebih besar** daripada R1=0,045596. Tanpa Kebun Raya, selisih rata-rata ayunan relatif turun dari 0,191504 menjadi 0,069097. Jangan menyimpulkan R2 selalu lebih stabil pada semua metrik dan seluruh subset lokasi. Membuang satu lokasi juga mengurangi jumlah lokasi dan dapat memperkecil rentang; itu bukan bukti kausal bahwa lokasi tersebut penyebab tunggal.

## K. Bootstrap dan membaca CI

Pada H3, 311 indeks kueri diambil ulang dengan pengembalian sebanyak 10.000 iterasi. Indeks yang sama dipakai untuk kedua representasi dan seluruh kondisi agar pasangan perbandingannya terjaga. Dalam setiap iterasi, acuan bersih untuk retensi ikut dihitung ulang. Batas persentil 2,5% dan 97,5% membentuk CI yang dilaporkan.

CI menunjukkan ketidakpastian menurut prosedur sampling yang dipakai. Jika CI selisih mencakup nol, jangan mengatakan kesamaan sudah terbukti; buktinya belum memisahkan arah perbedaan dengan jelas. Interval ini kondisional pada lokasi dan segmen gangguan yang tetap, serta eksploratif tanpa penyesuaian semua perbandingan. Interval tersebut tidak menjamin hasil yang sama untuk lokasi baru.

## L. Centroid, bandwidth, dan margin

**CONTOH spektrum satu frame:** frekuensi `[1.000;2.000;3.000]` Hz, magnitudo `[1;2;1]`.

```text
Centroid = (1000×1 + 2000×2 + 3000×1)/(1+2+1) = 2000 Hz
Bandwidth p=2 = akar([1×(1000−2000)^2 + 2×0^2 + 1×(3000−2000)^2]/4)
              = akar(500000) = 707,107 Hz
```

Bobot contoh ini magnitudo, bukan log-dB. Kode E5 menghitung per frame dan merata-ratakannya; hasil contoh satu frame bukan hasil satu berkas TA.

**CONTOH margin:** tau=0,70, skor terbesar=0,68 → margin=−0,02 → ditolak. Jika spesies teratas benar, kasus ini false rejection. Jika spesies teratas salah dan skornya di bawah tau, label operasional kode adalah total retrieval collapse. Label terakhir **tidak membuktikan semua sepuluh hasil salah**.

Semua rumus di sini dihubungkan ke kode dan tabel pada [peta sumber](06_PETA_BACAAN_DAN_SUMBER.md).
