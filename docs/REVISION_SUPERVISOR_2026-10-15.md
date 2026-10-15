# Revisi Pembimbing TA — 15 Oktober 2026

Revisi ini menindaklanjuti empat kelompok arahan pembimbing: sumber kode E4, analisis H3, transparansi perubahan H3/H4, serta penyesuaian Teori Dasar. **E4 tidak dijalankan ulang.** Seluruh perhitungan tambahan H3 membaca CSV yang sudah tersimpan.

## 1. Cakupan pembacaan dan perlindungan berkas

Sebelum revisi, inventaris mencatat 4.673 berkas di luar .git, .venv, dan __pycache__. Pemeriksaan membaca 1.105 berkas teks, kode, JSON, notebook, dan CSV; 53 PDF diekstrak mencakup 640 halaman, bersama empat DOCX dan 14 XLSX. Dua DOC lama diperiksa melalui string teks yang tersedia dan pasangan PDF jika ada. Ekstraksi teks bukan pemeriksaan visual seluruh halaman atau pembuktian validitas setiap isi pustaka.

Audio, checkpoint, arsip ZIP, dan cache biner diperiksa melalui inventaris serta provenance yang relevan. Tidak ada klaim mendengarkan seluruh audio. Draf Teori Dasar dan Gambar 6/8 lama dibaca sebagai rujukan, bukan ditimpa. Hasil ekstraksi dan backup kerja disimpan di direktori sementara di luar TA.

Status lokal awal memiliki tiga penghapusan yang sudah ada: Form Permohonan TA Fakultas Sains.docx, Panduan_Komprehensif_Tugas_Akhir.md, dan Panduan_Komprehensif_Tugas_Akhir.pdf pada root. Penghapusan tersebut tidak dilakukan oleh revisi ini dan tidak dimasukkan ke commit. Folder Teori Dasar serta draf runner lain yang semula belum dilacak juga tidak dimasukkan secara massal.

## 2. Runner yang benar-benar menghasilkan E4

Berkas produsen adalah [scripts/run_e4_five_locations_v10_stage7.py.draft](../scripts/run_e4_five_locations_v10_stage7.py.draft). Hash byte lokal cocok dengan e4_script pada [run_identity.json](../results/reproductions/E4_5sites_20261011T213404_350219Z/run_identity.json):

```text
30cc0ea990e35eda70a98a6928550cb18df39bb4cd9b95837fafe05512f80c2c
```

Runner disertakan dengan nama dan isi asli. Komentar pembukanya masih menyebut tiga habitat karena berasal dari versi sebelumnya, tetapi dictionary lokasi, loop, dan identitas run memuat **lima lokasi**. Komentar itu sengaja tidak diedit agar hash produsen tetap sama. Runner lama run_e4_domain_shift.py dipertahankan, tetapi tidak diposisikan sebagai penghasil run lima lokasi.

Aturan spesifik ditambahkan pada .gitattributes untuk menjaga byte runner ini serta tabel ceiling baru yang checksum-nya dicatat pada metadata gambar saat staging/checkout Git. Tidak ada normalisasi ulang massal terhadap repositori.

Desain E4 adalah 311 query × 5 lokasi × 4 SNR × 4 ulangan = 24.880 evaluasi noisy **per representasi**. Untuk R0–R3 totalnya 99.520 baris noisy, di luar 1.244 baris baseline clean yang tersebar di empat raw CSV. Ada 320 snapshot kondisi. Banyaknya baris evaluasi tidak berarti banyaknya query independen.

## 3. H3 melaporkan kedua skala ayunan

Analisis baru: [run_h3_sensitivity_reanalysis.py](../scripts/run_h3_sensitivity_reanalysis.py). Keluaran: [H3_sensitivity_20261015](../results/reproductions/H3_sensitivity_20261015/).

### Alur perhitungan

1. Baca raw E4 untuk R1 dan R2; urutkan berdasarkan query_id dan pastikan 311 ID sama pada clean maupun seluruh kombinasi SNR, ulangan, dan lokasi.
2. Bentuk array AP@10 dengan dimensi representasi × SNR × ulangan × lokasi × query.
3. Hitung mAP@10 masing-masing kondisi sebagai rata-rata AP@10 atas query.
4. Pada setiap ulangan, hitung maksimum minus minimum mAP@10 lintas lokasi; baru rata-ratakan empat ulangan. Ini adalah **ayunan absolut**.
5. Bagi ayunan absolut dengan mAP@10 clean representasi yang sama untuk mendapatkan **ayunan retensi relatif**. Ini adalah rasio atas mean, bukan mean dari rasio AP setiap query.
6. Ulangi langkah 3–5 pada subset tanpa Kebun Raya; lokasi tersebut tetap ada pada E4 asli.
7. Lakukan bootstrap query berpasangan 10.000 kali, seed 20261012. Indeks query identik dipakai untuk semua representasi dan kondisi. Baseline clean ikut dihitung ulang pada setiap resampling.
8. Hitung CI persentil 95% selisih ayunan R1−R2. Nilai positif berarti ayunan R2 lebih sempit; negatif berarti ayunan R1 lebih sempit. CI yang mencakup nol tidak memberi perbedaan yang meyakinkan dalam analisis ini.
9. Cocokkan lagi SHA-256 raw sumber sebelum dan sesudah analisis. Simpan hasil ke direktori baru dan tolak penimpaan direktori yang sudah ada.

Script tidak mengimpor mixer audio atau extractor model. Tidak ada inferensi, perubahan threshold, atau penulisan ke direktori E4 sumber.

### Ringkasan rata-rata empat SNR

| Subset | Skala | Ayunan R1 | Ayunan R2 | Selisih R1−R2 | CI 95% |
|---|---|---:|---:|---:|---|
| Lima lokasi | Absolut | 0,042324 | 0,030949 | 0,011375 | [−0,003993; 0,022140] |
| Lima lokasi | Relatif | 0,240111 | 0,048607 | 0,191504 | [0,152203; 0,241969] |
| Tanpa Kebun Raya | Absolut | 0,019567 | 0,026686 | −0,007119 | [−0,018009; 0,003056] |
| Tanpa Kebun Raya | Relatif | 0,111009 | 0,041912 | 0,069097 | [0,048683; 0,121152] |

Baseline clean R1 sekitar 0,176268 dan R2 sekitar 0,636709. Baseline R2 yang lebih besar membuat ayunan absolut yang sama menjadi ayunan relatif lebih kecil. Oleh karena itu retensi saja tidak cukup untuk menyatakan stabilitas representasi.

### Point estimate per SNR

| SNR | Subset | Absolut R1 | Absolut R2 | Relatif R1 | Relatif R2 |
|---|---|---:|---:|---:|---:|
| +20 | Lima lokasi | 0,019748 | 0,009452 | 0,112037 | 0,014845 |
| +10 | Lima lokasi | 0,052781 | 0,014625 | 0,299436 | 0,022970 |
| 0 | Lima lokasi | 0,051170 | 0,037888 | 0,290298 | 0,059506 |
| −5 | Lima lokasi | 0,045596 | 0,061829 | 0,258674 | 0,097108 |
| +20 | Tanpa Kebun Raya | 0,017878 | 0,007912 | 0,101423 | 0,012426 |
| +10 | Tanpa Kebun Raya | 0,034225 | 0,013938 | 0,194165 | 0,021891 |
| 0 | Tanpa Kebun Raya | 0,014544 | 0,031586 | 0,082512 | 0,049608 |
| −5 | Tanpa Kebun Raya | 0,011623 | 0,053308 | 0,065937 | 0,083724 |

CI untuk seluruh baris tersedia pada [tabel sensitivitas](../results/reproductions/H3_sensitivity_20261015/tables/h3_swing_summary.csv).

### Perubahan interpretasi

Pada lima lokasi, ayunan relatif R2 memang lebih sempit dalam hasil tersimpan. Namun ayunan absolut R2 lebih besar pada −5 dB. Setelah Kebun Raya dikeluarkan, selisih rata-rata ayunan relatif turun sekitar **63,9%**; pada −5 dB point estimate berbalik dan CI selisih relatif [−0,041711; 0,050057] mencakup nol.

Hasil mendukung peran kuat komposisi lokasi dalam ukuran stabilitas, tetapi tidak menunjukkan bahwa hampir seluruh selisih rata-rata hilang: masih ada selisih rata-rata relatif positif 0,069097. Penurunan 63,9% adalah perbandingan deskriptif, bukan dekomposisi kontribusi kausal lokasi. Pada skala absolut, CI selisih rata-rata mencakup nol baik dengan maupun tanpa Kebun Raya.

Kesimpulan diperbaiki menjadi **bergantung pada metrik, SNR, dan subset lokasi**. Klaim umum “R2 berayun lebih sempit di semua SNR” tidak digunakan tanpa batasan tersebut. Dugaan serangga dan distorsi frekuensi tidak ditulis sebagai penyebab yang sudah terbukti. Analisis spektral segmen noise baru tidak dilakukan dalam revisi ini.

CI bersifat eksploratif, belum dikoreksi sebagai keluarga uji konfirmatori baru, dan kondisional pada lokasi serta segmen noise tetap. Bootstrap query tidak mengukur ketidakpastian pada lokasi atau sesi lapangan baru.

## 4. Riwayat H3 dan H4 setelah hasil

[Hypotheses](research/hypotheses.md), [RQ](research/rq.md), dan [scope-reframe](research/scope-reframe-2026-10-12.md) sekarang mencatat:

- **6 September 2026, 25ebb72:** rumusan asli H3 tentang gap real-soundscape dan H4 tentang penurunan recall atau lonjakan false accept.
- **12 Oktober 2026, 7817355:** H3 menjadi stabilitas retensi profil lokasi dan H4 menjadi perubahan perilaku titik operasi, setelah hasil E4/E3 tersedia.
- **15 Oktober 2026:** tambahan ayunan absolut dan sensitivitas tanpa Kebun Raya, tanpa run E4 ulang.

H3 asli belum diuji oleh additive mixture. Reformulasi H3 dan interpretasi H4 diberi label eksploratif. Klausul penurunan recall memang sudah ada pada H4 asli, sehingga perubahan bahasa tidak dipakai untuk menghapus riwayat itu.

Data E3 dan threshold tetap sama: recall penerimaan known R2 turun 0,604502 → 0,254019; false-accept rate turun 0,222581 → 0,129032. Tidak ada lonjakan false accept yang dinyatakan terbukti. Recall penerimaan known dibedakan dari ketepatan identitas spesies.

Matriks baru [tabel 28](../results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv) menjadi rujukan revisi. Tabel 23/27, statistik lama, serta analisis H3 tanggal 12 Oktober tidak ditimpa. Pembuat matriks diperbarui agar menghasilkan tabel baru dan menolak penimpaan.

## 5. Teori Dasar ditulis pada naskah sendiri

Naskah [paper/teori_dasar.md](../paper/teori_dasar.md) dan [manuscript.md](../paper/manuscript.md) menindaklanjuti draf pembimbing:

- **Bagian 2.8:** membedakan generalisasi focal-to-soundscape dalam literatur dengan desain additive noise lima lokasi pada E4 aktif.
- **Formula gap E4−E2:** tidak lagi digunakan untuk mengisolasi penurunan akibat propagasi, jarak, absorpsi, atau reverberasi. Kedua eksperimen sama-sama additive mixture; formula diganti dengan ayunan absolut dan relatif yang benar-benar dihitung.
- **Gambar 6:** diagram baru memperlihatkan E2 pool noise dan E4 lima lokasi dengan empat ulangan.
- **Jumlah gallery:** 673 rekaman aktif, bukan 3.653 dari rezim lama.
- **Gambar 8 dan recall ceiling:** gallery relevan per spesies 15–100; batas Recall@10 per spesies 0,1000–0,6667. Batas rata-rata 311 query adalah **0,363997**, berbeda dari rata-rata tak berbobot 20 spesies sebesar 0,406900.
- **Bagian 3.6:** enam kategori akuisisi, yaitu Amplitude/Frequency × Low/Medium/High. Enam kategori tidak disamakan dengan enam perangkat fisik. E4 memasangkan kategori per query; pengaruh gain dan trigger belum diisolasi sebagai efek kausal.
- Parameter implementasi mengikuti kode: MFCC 20 koefisien mean/std = 40 dimensi; R3 merupakan kontrol Gaussian berdasarkan ID, bukan kontrol yang merespons noise.

Dua gambar baru, tabel ceiling per spesies, dan metadata provenance berada di [paper/figures/revision_20261015](../paper/figures/revision_20261015/). [Builder gambar](../scripts/build_theory_revision_figures.py) dapat dijalankan dengan direktori keluaran baru. Gambar/draf dosen pada folder Teori Dasar tidak diubah atau dihapus.

## 6. Cache dan cara reproduksinya

README memuat prasyarat serta perintah [rebuild_e4_clean_caches.py](../scripts/rebuild_e4_clean_caches.py). Builder hanya membangun embedding **clean** R0–R3 ke direktori baru. Mode --check-only membaca checksum sumber dan keberadaan audio tanpa menulis cache. Cache, audio, dan checkpoint tetap tidak di-commit.

Builder tidak menjanjikan bahwa arsip baru pasti identik byte dengan cache historis. Metadata mencatat hash baru dan kecocokannya dengan hash lama. Runner stage7 memiliki path dan checksum input historis yang dibekukan; cache baru tidak boleh dipaksakan menjadi input historis dengan mengedit run_identity.json. Rekonstruksi penuh belum dijalankan pada revisi ini karena cache dan hasil E4 sudah tersedia; yang diperiksa adalah prasyarat sumbernya.

## 7. Verifikasi

- Lima tes metode H3 lulus: perbedaan ayunan absolut/relatif, urutan range sebelum mean ulangan, pasangan query bootstrap, penolakan data tidak lengkap, dan penolakan penimpaan output.
- Pemeriksaan sumber pembangun cache lulus, tanpa membangun cache atau mengulang E4.
- Gambar 6, Gambar 8, dan plot sensitivitas baru diperiksa secara visual.
- Hash raw E4 sebelum/sesudah analisis cocok; metadata menyimpan checksum sumber dan keluaran.
- Suite integritas yang sudah ada: **25/25 tes lulus**; suite metode H3 baru: **5/5 tes lulus**.
- Perbandingan inventaris sebelum/sesudah tidak menemukan penghapusan baru atau perubahan ukuran/mtime berkas awal di luar daftar revisi. Seluruh hash berkas teks yang tidak direvisi tetap cocok, termasuk CSV sumber E4 dan bahan laporan lama.

## 8. Temuan di luar revisi yang dipertahankan

Pembacaan pustaka menemukan beberapa nama PDF yang tidak cocok dengan isinya: berkas berjudul Computational bioacoustics with deep learning a review and roadmap berisi artikel matematika RACG; berkas Domain-Invariant Representation Learning of Bird Sounds berisi laporan DCASE 2022; dan berkas MFCC Dan Naive Bayes berisi artikel MFCC/BiLSTM yang sama dengan berkas lain. Tidak ada penghapusan, penggantian, atau perubahan terhadap berkas pustaka tersebut. Naskah baru tidak memakai ketiganya sebagai bukti.

Catatan logbook mingguan, dokumen administrasi, arsip BirdCLEF, dan panduan lama dipertahankan. Untuk status revisi terbaru gunakan CURRENT_STATUS dan dokumen ini; isi historis tidak dianggap sebagai pelaporan baru.

## 9. Catatan untuk bimbingan

Poin 1–3 siap diperiksa melalui runner E4 beserta hash, hasil sensitivitas H3, dan riwayat H3/H4 pada tiga dokumen riset. Penulisan teori dilakukan pada naskah sendiri. Tidak ada pesan yang dikirim otomatis kepada pembimbing; tautan commit dan catatan ini dapat disampaikan oleh Fabio setelah push berhasil.
