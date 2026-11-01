# 5. Latihan mandiri dan kunci

Kerjakan dahulu di kertas. Semua data pada soal adalah **contoh latihan**, kecuali soal yang secara jelas menyebut hasil TA. Tuliskan rumus, masukkan angka, hitung, lalu jelaskan arti hasil dalam satu kalimat. Jawaban angka tanpa arti belum cukup untuk ujian.

## Soal

1. **Cosine.** q=`[3;4]`, g=`[4;3]`. Hitung norm masing-masing dan cosine. Apakah skor itu probabilitas spesies benar?
2. **Daya dan RMS.** Sampel sinyal `[0,1;−0,1;0,1;−0,1]`. Hitung daya dan RMS.
3. **SNR.** Daya target 0,09, daya derau sebelum skala 0,01. Hitung alpha agar SNR +10 dB. Berapa daya derau sesudah skala?
4. **Makna SNR.** Pada −5 dB, mana yang lebih besar: daya target atau daya derau? Berapa rasionya? Apakah 0 dB berarti tidak ada suara?
5. **AP, Precision, Recall.** Ada 25 rekaman galeri relevan. Dari sepuluh hasil pertama, yang relevan hanya peringkat 2, 5, dan 10. Hitung Top-1 match, RR, P@10, R@10, dan AP@10 menurut kode TA.
6. **mAP.** Tiga kueri mempunyai AP@10 sebesar 0,20; 0,40; 0,90. Hitung mAP. Apakah itu sama dengan menghitung proporsi spesies yang ditemukan?
7. **Batas Recall.** Satu kueri memiliki 40 rekaman galeri relevan dan semuanya memungkinkan dicari. Berapa batas Recall@10? Jika ketiga kueri memiliki R masing-masing 20, 40, dan 100, berapa rata-rata batasnya bila bobot kueri sama?
8. **Retensi.** Hasil bersih 0,50 dan hasil bising 0,35. Hitung retensi, penurunan absolut, dan penurunan relatif.
9. **Open-set.** TP=18, FN=6, FP=4, TN=12. Hitung recall penerimaan, FPR, precision penerimaan, F1, dan Youden J.
10. **Pemilihan ambang.** Skor known `[0,9;0,8;0,7;0,4]` dan unknown `[0,6;0,5;0,3;0,1]`. Mengapa tau 0,7 lebih baik daripada 0,4 menurut Youden J? Data mana yang boleh dipakai untuk memilihnya?
11. **H3 relatif dan absolut.** Representasi A mempunyai acuan bersih 0,80 dan ayunan absolut 0,08; B mempunyai acuan 0,20 dan ayunan 0,03. Hitung ayunan relatif dan jelaskan mana yang lebih stabil menurut masing-masing ukuran.
12. **CI hasil TA.** Selisih ayunan absolut H3 rata-rata mempunyai CI `[−0,003993;0,022140]`. Dapatkah Anda menyebut perbedaan absolut sudah meyakinkan atau kedua metode terbukti sama?
13. **Margin dan kategori E5.** tau=0,70. Kasus a: skor 0,68 dan Top-1 benar. Kasus b: skor 0,75 dan Top-1 salah. Kasus c: skor 0,65 dan Top-1 salah. Hitung margin dan kategori masing-masing. Apakah c berarti semua sepuluh hasil salah?
14. **Centroid.** Frekuensi `[1000;2000;3000]` Hz dan magnitudo `[1;1;2]`. Hitung centroid. Apakah centroid dapat langsung memastikan ada serangga?
15. **Ukuran E4 hasil TA.** Hitung baris per representasi dan seluruh empat representasi dari 311 kueri, lima lokasi, empat SNR, dan empat ulangan. Apakah semua baris itu sampel burung independen?
16. **Pooling R2.** Berapa jendela tiga detik dengan langkah satu detik yang terbentuk dari klip tepat lima detik? Sebut rentang waktunya.
17. **Bedakan metrik.** Mengapa Top-1, Recall@10, dan recall penerimaan open-set bisa menghasilkan angka yang jauh berbeda pada kueri yang sama?
18. **Pertanggungjawaban.** Sebutkan satu klaim yang sudah didukung TA, satu yang belum diuji, dan satu pekerjaan yang memerlukan bukti manusia.

## Kunci dan cara menjelaskan

**1.** Norm q=g=`akar(25)=5`. Dot product `3×4+4×3=24`. Cosine=24/25=**0,96**. Ini skor kesamaan arah vektor, bukan probabilitas spesies benar.

**2.** Kuadrat semua sampel 0,01. Daya=0,01 dan RMS=`akar(0,01)=0,1`.

**3.** alpha=`akar(0,09/(0,01×10))=akar(0,9)=0,948683`. Daya derau hasil skala=`alpha²×0,01=0,009`. Cek `10 log10(0,09/0,009)=10 dB`.

**4.** Target/derau=`10^(−5/10)=0,316228`. Daya derau/target=**3,162278**. Pada 0 dB, daya target sama dengan derau; keduanya tidak harus nol.

**5.** Top-1=0. RR=1/2=0,5. P@10=3/10=0,3. R@10=3/25=0,12. AP@10=`(1/2+2/5+3/10)/10=(0,5+0,4+0,3)/10=0,12`. Pembagi AP ialah min(25,10)=10, sedangkan pembagi recall 25. Hasil keduanya sama di contoh ini karena kebetulan angka, bukan karena rumusnya sama.

**6.** mAP=`(0,20+0,40+0,90)/3=0,50`. Itu rata-rata kualitas ranking per kueri menurut AP, bukan persentase spesies yang ditemukan.

**7.** R=40 → batas 10/40=**0,25**. Tiga kueri: `(10/20+10/40+10/100)/3=(0,5+0,25+0,1)/3=0,283333`. Jangan membagi 30 dengan total R=160 jika yang diminta rata-rata recall per kueri; cara itu menghasilkan agregasi lain.

**8.** Retensi=0,35/0,50=**0,70=70%**. Penurunan absolut=0,15 satuan mAP. Penurunan relatif=(0,50−0,35)/0,50=**30%**. Sebut penyebutnya saat menjawab.

**9.** Recall=18/24=**0,75**; FPR=4/16=**0,25**; precision=18/22=**0,818182**; F1=36/(36+4+6)=**0,782609**; J=0,75−0,25=**0,50**.

**10.** Pada 0,7: TPR=3/4, FPR=0, J=0,75. Pada 0,4: TPR=4/4, FPR=2/4, J=0,50. Memilih ambang memakai kalibrasi terpisah; kueri uji dipakai setelah ambang dibekukan.

**11.** Relatif A=0,08/0,80=0,10; B=0,03/0,20=0,15. Absolut B lebih kecil; relatif A lebih kecil. Selalu sebut ukuran yang dipakai. Kesimpulan itu hanya mengenai ayunan contoh, bukan bukti statistik populasi.

**12.** CI melintasi nol sehingga arah selisih absolut belum terpisah jelas dengan prosedur tersebut. Itu juga belum membuktikan kesamaan. Kesetaraan memerlukan definisi batas kesetaraan dan analisis yang sesuai.

**13.** a: margin −0,02 → open-set false rejection. b: +0,05 → Top-1 confusion above threshold. c: −0,05 → label operasional total retrieval collapse. Kategori c memakai kondisi hasil pertama dan ambang; jangan menyimpulkan seluruh Top-10 salah tanpa memeriksanya.

**14.** Centroid=`(1000×1+2000×1+3000×2)/4=9000/4=2250 Hz`. Ini ringkasan spektral; identitas sumber atau hubungan sebab tidak dapat dipastikan dari satu angka ini.

**15.** `311×5×4×4=24.880` per representasi; `24.880×4=99.520` seluruhnya. Banyak baris berbagi rekaman sumber yang sama. Karena itu bukan 99.520 rekaman burung independen.

**16.** Tiga jendela: **0–3, 1–4, 2–5 detik**. Vektornya dirata-ratakan oleh adapter R2.

**17.** Top-1: benar/salah pada hasil pertama. Recall@10: berapa bagian seluruh galeri relevan yang tertampung dalam sepuluh hasil. Recall penerimaan: berapa kueri known yang skornya melampaui ambang, tanpa mensyaratkan label teratas benar dalam metrik E3 ini.

**18.** Contoh: didukung—R2 tertinggi pada retrieval E2 yang diuji. Belum diuji—keunggulan pada semua rekaman burung alami ITERA atau sebab biofoni serangga. Memerlukan bukti manusia—audit pendengaran E5 berupa pendengar, tanggal, dan observasi yang benar-benar dilakukan.

## Penilaian diri

Beri tanda **paham**, **masih perlu contoh**, atau **belum paham** untuk setiap soal. Ini penilaian belajar pribadi, bukan skor kelulusan kampus. Sebelum bimbingan, usahakan soal 1–13 serta 15 dan 17 dapat dijawab sambil menjelaskan penyebutnya. Pada pertanyaan yang belum dikuasai, lebih baik mengatakan batas pemahaman lalu membuka sumber daripada mengarang alasan.
