# Panduan Bimbingan: Audit E5, H3 Relatif–Absolut, dan Batas Recall@10

Dicatat 18 Oktober 2026 untuk membantu Fabio menjalankan audit dan menjelaskan hasilnya sendiri.

## 1. Siapa yang mendengarkan?

**Fabio sebagai peneliti utama** mendengarkan dan menulis pengamatan. Pembimbing dapat memeriksa beberapa contoh saat bimbingan. Pendengar kedua boleh membantu bila tersedia, dengan nama serta hasil penilaiannya dicatat; dua pendengar bukan syarat tambahan yang ditetapkan dokumen ini.

Audit E5 adalah pemeriksaan kualitatif kasus kegagalan retrieval: apakah vokalisasi pada potongan eksperimen terdengar, bagaimana latarnya, dan bagaimana kemiripan yang terdengar dengan hasil Top-1. Ini bukan tes kemampuan menebak spesies dari telinga dan bukan eksperimen persepsi buta. Halaman menunjukkan metadata dan label komputasional, sehingga potensi bias interpretasi perlu diingat. Jika tidak yakin, tulis uncertain dan alasannya. Label spesies dari dataset tetap metadata; jangan mengganti ground truth hanya berdasarkan kesan dengar.

Saya sebagai asisten menyiapkan audio, perhitungan, formulir, dan pemeriksaan konsistensi. Catatan yang disebut pendengaran manusia harus berasal dari orang yang benar-benar mendengarkan; software tidak mengisinya dari skor model.

## 2. Cara mendengarkan 120 kasus

Buka [halaman audit lokal](audit-pendengaran-E5/listening-pack-20261016/index.html) dengan Chrome/Edge, melalui klik ganda file index.html di folder TA. Buka file lokalnya; GitHub tidak menyertakan WAV dan tidak menjalankan halaman audit. Klip sudah tersedia di komputer ini.

1. Gunakan headphone/earphone di tempat tenang dan volume nyaman. Pertahankan pengaturan playback yang sama saat membandingkan tiga klip.
2. Isi nama pendengar dan pilih kasus, misalnya E5_001. Selesaikan bertahap, misalnya 10–20 kasus per sesi.
3. Dengarkan **query clean** untuk mengenali pola pada segmen burung yang diuji.
4. Dengarkan **query pada kondisi eksperimen**. Pada kondisi noisy ini adalah segmen yang sama setelah dicampur noise dengan SNR tercatat. Nilai apakah vokalisasinya masih jelas, samar, tertutup, atau tidak pasti.
5. Dengarkan **Top-1**, yaitu rekaman gallery yang ditempatkan model pada peringkat pertama. Perhatikan pola bunyi/ritme dan latarnya; perbedaan individu, panggilan, atau perangkat dapat tetap ada pada spesies yang sama.
6. Isi apakah vokalisasi query/Top-1 terdengar (yes/no/uncertain), pengamatan latar, ketidakpastian, dan interpretasi. Tulis apa yang terdengar dahulu, kemudian bedakan dari label kegagalan komputasional.
7. Klik **Simpan sebagai sudah diulas**, atau **Tandai perlu tindak lanjut** bila segmen/observasi belum dapat dipastikan. Isian yang belum disimpan akan hilang saat berpindah kasus.
8. Klik **Unduh catatan JSON** setelah setiap sesi. Simpan file unduhan bernama berbeda per sesi; browser menyimpan salinan lokal sebagai bantuan, tetapi unduhan adalah arsip yang perlu dijaga.

Jangan menghapus data browser sebelum mengunduh catatan. Untuk melanjutkan, gunakan browser dan lokasi file yang sama. Jika catatan browser tidak muncul lagi, simpan ekspor sebelumnya dan gabungkan lewat peninjauan terpisah; jangan menimpa data terdahulu. CSV asli tidak diubah oleh halaman ini.

Contoh **format pengamatan, bukan hasil audit yang sudah dilakukan**: “Pola vokal pada query [jelas/samar/tidak pasti]. Pada versi noisy, latar terdengar seperti […]. Top-1 terdengar [serupa/berbeda/tidak pasti] pada […]. Dugaan hubungan dengan kesalahan retrieval adalah […], dengan ketidakpastian […].” Jangan menulis “serangga menyebabkan model gagal” hanya karena mendengar bunyi yang menyerupai serangga.

Pada kondisi Clean, query clean dan query eksperimen dapat identik. Beberapa kasus memakai query/kondisi yang sama tetapi representasi/Top-1 berbeda; tetap nilai per case_id. Paket mempunyai 276 klip unik untuk 120 kasus. Seluruh klip lima detik, 32 kHz, dan mengikuti segmen eksperimen; jangan memakai lima detik pertama file mentah sebagai pengganti.

[Petunjuk teknis dan impor JSON ke CSV baru](audit-pendengaran-E5/README.md). Impor software hanya memvalidasi format/provenance, bukan membuktikan pendengaran. Audit penuh belum selesai sampai 120 kasus sungguh diulas dan kasus needs_follow_up ditangani atau keterbatasannya dilaporkan.

## 3. Cara menjelaskan H3 absolut dan relatif

H3 membandingkan **ayunan lintas lokasi pada SNR yang sama**, bukan sekadar penurunan skor dari clean ke noisy. Untuk setiap ulangan, hitung mAP@10 lokasi tertinggi dikurangi terendah, lalu rata-ratakan empat ulangan.

- Ayunan absolut: selisih mAP@10 pada skala aslinya.
- Ayunan relatif: ayunan absolut dibagi baseline clean representasi itu sendiri.

Rumus ringkas: S_abs = rata-rata_ulangan(max_lokasi mAP@10 − min_lokasi mAP@10); S_rel = S_abs / mAP@10_clean. Penyebut clean R1 dan R2 berbeda, sehingga urutan absolut dan relatif dapat berbalik.

**Contoh nyata E4 lima lokasi pada −5 dB:**

| Representasi | Baseline clean | Ayunan absolut | Ayunan relatif terhadap baseline sendiri |
|---|---:|---:|---:|
| R1 / PANNs | 0,176268 | 0,045596 | 0,258674 ≈ 25,87% |
| R2 / BirdNET | 0,636709 | 0,061829 | 0,097108 ≈ 9,71% |

R2 mempunyai ayunan absolut lebih besar, tetapi ayunan relatif lebih kecil karena baseline clean-nya jauh lebih tinggi. Angka relatif di tabel adalah **lebar ayunan retensi**, bukan retensi rata-rata atau besarnya kehilangan dari clean. Ayunan absolut 0,045596 setara 4,5596 poin persentase pada skala mAP 0–100, bukan langsung “turun 4,5596% dari baseline”.

Contoh penjelasan lisan:

> “Pak, ayunan absolut menunjukkan seberapa lebar skor mAP@10 berubah antar lokasi. Ayunan relatif membandingkan lebar itu dengan kemampuan clean masing-masing model. Pada −5 dB, BirdNET berayun 0,0618 dan PANNs 0,0456 secara absolut. Setelah dibagi baseline clean, ayunannya menjadi sekitar 9,71% untuk BirdNET dan 25,87% untuk PANNs. Jadi saya tidak menyimpulkan BirdNET selalu lebih stabil pada semua skala. Saya melaporkan keduanya, berikut CI dan sensitivitas lokasi.”

Rata-rata empat SNR pada lima lokasi: selisih ayunan absolut R1−R2 = 0,011375 dengan CI [−0,003993; 0,022140], sehingga keunggulan rata-rata absolut belum meyakinkan. H3 hasil reformulasi tetap eksploratif. [Tabel penghilangan masing-masing lokasi](../results/reproductions/H3_leave_one_location_out_20261018/README.md) memperluas sensitivitas tanpa memilih lokasi terbaik sesudah melihat hasil. Rata-rata absolut semua skenario memiliki CI yang mencakup nol; hasil relatif rata-rata tidak otomatis berlaku untuk tiap SNR. Penghilangan lokasi bukan pembuktian sebab-akibat.

## 4. Cara menjelaskan batas Recall@10

Relevan berarti hasil gallery berspesies sama dengan query. Recall@10 = jumlah hasil relevan pada 10 peringkat teratas / **seluruh rekaman relevan spesies itu dalam gallery**. Penyebutnya bukan 10, bukan 311 query, dan bukan seluruh 673 gallery.

Karena hanya sepuluh hasil boleh diambil, Recall@10 ≤ min(1, 10/R_q), dengan R_q jumlah rekaman relevan di gallery untuk query tersebut.

| Banyak rekaman spesies yang sama dalam gallery | Relevan yang berhasil ditemukan di Top-10 | Recall@10 maksimum |
|---|---:|---:|
| 15 | 10 | 10/15 = 0,6667 |
| 20 | 10 | 10/20 = 0,5000 |
| 100 | 10 | 10/100 = 0,1000 |

Pada ketiga contoh, sepuluh hasil teratas bisa semuanya benar; Precision@10 = 1. Recall berbeda karena jumlah seluruh rekaman relevan berbeda. Batas ini bukan kesalahan model dan bukan jaminan model sudah mencapai batasnya.

Gallery aktif berisi 673 rekaman; per spesies terdapat 15–100 rekaman relevan. Batas maksimum rata-rata Recall@10 berbobot **311 query** adalah 0,363997. Rata-rata tak berbobot atas 20 spesies adalah 0,406900 dan merupakan agregasi berbeda. Recall@10 R2 E1 aktual 0,233109 dibaca bersama batas tersebut dan metrik primer mAP@10, bukan dipaksa mendekati 1.

Contoh penjelasan lisan:

> “Recall@10 saya membagi temuan relevan dengan semua rekaman spesies yang sama dalam gallery. Kalau suatu spesies punya 100 rekaman, meskipun sepuluh hasil teratas semuanya benar, recall maksimalnya hanya 0,1. Karena itu saya menjelaskan batas k dibagi jumlah relevan. Batas rata-rata berbobot query pada dataset saya sekitar 0,364. Semua representasi memakai gallery yang sama, jadi perbandingan antar model tetap bermakna; batas tersebut membantu membaca skalanya.”

Membagi rata-rata recall dengan rata-rata ceiling tidak sama dengan menghitung rata-rata recall ternormalisasi per query; metrik baru itu tidak ditambahkan ke hasil resmi. [Naskah teori §2.5/§2.8](../paper/teori_dasar.md) dan [Gambar 8](../paper/figures/revision_20261015/fig08_recall_ceiling_active.png) memuat landasan serta angka sumber.
