# Panduan Komprehensif Tugas Akhir DSIC-2706

Jangan khawatir, sangat wajar merasa kebingungan di tengah eksperimen yang kompleks. Dokumen ini saya susun agar Anda bisa memahami secara utuh dari kacamata "helikopter" (gambaran besar) tentang apa yang sebenarnya sedang Anda teliti, seberapa jauh *progress* Anda, dan apa kebaruan (*novelty*) yang bisa Anda banggakan di depan dosen penguji.

---

## 1. Posisi Anda Saat Ini (*Progress Tracker*)

Tugas Akhir ini pada dasarnya memiliki alur eksperimen yang terbagi menjadi beberapa fase. Berikut adalah status Anda saat ini:

- [x] **Tahap 1: Pengumpulan Data** (AudioMoth ITERA & Spesies BirdCLEF+ 2026) ➔ **SELESAI**
- [x] **Tahap 2: Registrasi Integritas Data** (Manifes SHA-256 & Metadata Bebas Bocor) ➔ **SELESAI**
- [x] **Tahap 3 & 4 (Eksperimen E1 & E2):** Evaluasi *Clean* & Pencampuran Derau Terkontrol SNR ➔ **SELESAI**
- [x] **Eksperimen E3:** Kalibrasi Ambang Batas (*Open-Set Rejection* $\tau^* = 0.50$) ➔ **SELESAI**
- [x] **Eksperimen E4:** *Real Soundscape Domain Shift* (Uji coba pada *soundscape* alam bebas tropis) ➔ **SELESAI**
- [x] **Eksperimen E5:** *Failure Analysis* (Mendiagnosis 30 kasus kegagalan nyata) ➔ **SELESAI**
- [x] **Evaluasi Statistik Inferensial:** Paired Bootstrap Resampling 1.000 iterasi ($p = 0.0000 < 0.05$) ➔ **SELESAI**
- [ ] **Penulisan Naskah Bab 4 & Bab 5** (Memasukkan grafik dan tabel siap pakai ke draf skripsi Word) ➔ **SIAP DIMULAI**

**Kesimpulan Progress:** Secara teknis (kodingan, komputasi seluruh model AI E0 s.d. E5, pengujian statistik inferensial, pembuatan tabel dan grafik publikasi), Anda sudah **100% SELESAI**. Semua bahan empiris sudah tersedia lengkap di folder `paper/tables/` dan `paper/figures/`.

---

## 2. Metodologi yang Digunakan

Metodologi yang Anda gunakan dalam skripsi ini disebut **Zero-Shot Audio Retrieval berbasis Frozen Pretrained Representations**. 

Artinya, alih-alih Anda melatih ulang model Kecerdasan Buatan (AI) dari nol (yang butuh superkomputer), Anda mengambil AI canggih yang sudah dilatih oleh ilmuwan dunia (*Pretrained*), "membekukan" otaknya (*Frozen*), lalu menggunakannya untuk mengubah suara burung menjadi vektor angka (Ekstraksi Fitur). 

Vektor burung dari alam liar (*Query*) kemudian dicocokkan dengan vektor burung di basis data (*Gallery*) menggunakan metrik jarak **Cosine Similarity**. Jika skor kemiripannya tinggi, AI akan menebak spesies burung tersebut.

---

## 3. Arsitektur Sistem (Diagram Alir)

Berikut adalah arsitektur sistem tugas akhir Anda (Diagram ini bisa Anda jadikan rujukan untuk menggambar di Bab 3 Metodologi):

```text
+-----------------------+     +------------------------+
|  Kueri Audio Bersih   |     | Derau Fisik AudioMoth  |
|  BirdCLEF (5 detik)   |     | Lingkungan Kampus ITERA|
+-----------+-----------+     +-----------+------------+
            |                             |
            +------------+   +------------+
                         |   |
                         v   v
                [ Mixer Daya SNR ]
             (Clean, 20, 10, 0, -5 dB)
                         |
                         v
             [ Audio Terdegradasi ]
                         |
       +-----------------+-----------------+
       |                 |                 |
       v                 v                 v
[ R0: MFCC 40-d ] [ R1: PANNs 2048-d ] [ R2: BirdNET 1024-d ]
       |                 |                 |
       +-----------------+-----------------+
                         |
                         v
             [ Cosine Similarity Match ] <--- [ Galeri Suara Spesies ]
                         |
          +--------------+--------------+
          |                             |
          v                             v
[ Ranking Top-k & mAP@10 ]    [ Ambang Batas tau* = 0.50 ]
                              /                        \
                    Skor >= 0.50                      Skor < 0.50
                         |                                 |
                         v                                 v
                 [ Diterima / Match ]              [ Ditolak / Unknown ]
```

---

## 4. Referensi Jurnal Utama (Landasan Teori)

Metodologi dan arsitektur yang Anda pakai sangat ilmiah dan didasarkan pada jurnal-jurnal Q1 bertaraf internasional. Anda Wajib memasukkan ini di Daftar Pustaka:

1. **Untuk Model R2 (BirdNET):**
   > Kahl, S., Wood, C. M., Eibl, M., & Klinck, H. (2021). *"BirdNET: A deep learning solution for avian diversity monitoring."* Ecological Informatics, 61, 101236.
2. **Untuk Model R1 (PANNs CNN14):**
   > Kong, Q., Cao, Y., Iqbal, T., Wang, Y., Wang, W., & Plumbley, M. D. (2020). *"PANNs: Large-scale pretrained audio neural networks for audio pattern recognition."* IEEE/ACM Transactions on Audio, Speech, and Language Processing, 28, 2880-2894.
3. **Untuk Model R0 (MFCC):**
   > Davis, S., & Mermelstein, P. (1980). *"Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences."* IEEE transactions on acoustics, speech, and signal processing.
4. **Untuk Metodologi Open-Set (Thresholding via Youden's J):**
   > Scheirer, W. J., de Rezende Rocha, A., Sapkota, A., & Boult, T. E. (2012). *"Toward open set recognition."* IEEE transactions on pattern analysis and machine intelligence.

---

## 5. Kebaruan & Gap Penelitian (The *Novelty*)

Jika dosen penguji bertanya: *"Apa bedanya skripsi kamu dengan penelitian klasifikasi suara burung yang sudah ada?"*, inilah senjata utama Anda:

### Gap Penelitian (Masalah Saat Ini)
Penelitian bioakustik konvensional biasanya melatih model *Machine Learning* (seperti CNN/ResNet) menggunakan dataset yang sangat bersih. **Namun, ketika model tersebut dibawa ke alam liar (seperti di kampus ITERA), model tersebut gagal total.** Mengapa? Karena di lapangan ada suara angin, hujan lebat, motor, dan serangga (Distorsi Domain Akustik). Selain itu, model konvensional akan "memaksa" menebak spesies burung meskipun yang terekam sebenarnya hanya suara klakson motor (*Closed-set assumption*).

### Kebaruan Skripsi Anda (Novelty)
1. **Pendekatan Degradasi Terkontrol (Paired Noise Degradation - E2):** Anda menyuntikkan derau asli dari kampus ITERA pada berbagai tingkatan yang dikontrol secara matematis (SNR -5 dB hingga +20 dB). Ini membuktikan batas kritis (*breaking point*) AI pengenal suara burung terhadap bising lingkungan tropis.
2. **Evaluasi Zero-Shot Retrieval:** Alih-alih melakukan klasifikasi kaku, Anda menggunakan pendekatan *Retrieval* (sistem pencarian kemiripan). Sistem ini fleksibel: jika ada burung baru, cukup tambahkan suaranya ke Galeri tanpa perlu melatih ulang model AI.
3. **Open-Set Rejection (Kalibrasi $\tau^*$ - E3):** Sistem memiliki kemampuan menolak (*reject*) sinyal non-burung menggunakan ambang batas beku $\tau^* = 0.50$ via Youden's J, meminimalisir deteksi palsu (*False Positive*).
4. **Uji Validitas Domain Shift Hutan Tropis (E4):** Menguji model pada ribuan *soundscape* bentang alam asli BirdCLEF dan membuktikan secara empiris bahwa BirdNET bersifat *domain-invariant* dengan kesenjangan performa sangat minim ($\Delta mAP@10 = -0.0101$).
5. **Uji Signifikansi Inferensial (Bootstrap Resampling):** Keunggulan model bioakustik BirdNET atas model generik dibuktikan secara inferensial melalui 1.000 iterasi bootstrap ($p = 0.0000 < 0.05$).
