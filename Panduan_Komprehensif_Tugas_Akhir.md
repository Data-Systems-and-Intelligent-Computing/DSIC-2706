# Panduan Komprehensif Tugas Akhir DSIC-2706

Jangan khawatir, sangat wajar merasa kebingungan di tengah eksperimen yang kompleks. Dokumen ini saya susun agar Anda bisa memahami secara utuh dari kacamata "helikopter" (gambaran besar) tentang apa yang sebenarnya sedang Anda teliti, seberapa jauh *progress* Anda, dan apa kebaruan (*novelty*) yang bisa Anda banggakan di depan dosen penguji.

---

## 1. Posisi Anda Saat Ini (*Progress Tracker*)

Tugas Akhir ini pada dasarnya memiliki alur eksperimen yang terbagi menjadi beberapa fase. Berikut adalah status Anda hari ini:

- [x] **Tahap 1: Pengumpulan Data** (AudioMoth ITERA & Spesies BirdCLEF) ➔ **SELESAI**
- [x] **Tahap 2: Registrasi Integritas Data** (Manifes SHA-256 & Metadata) ➔ **SELESAI**
- [x] **Tahap 3 & 4 (Eksperimen E1 & E2):** Evaluasi *Clean* & Pencampuran Derau Terkontrol SNR ➔ **SELESAI HARI INI**
- [x] **Eksperimen E3:** Kalibrasi Ambang Batas (*Open-Set Rejection*) ➔ **SELESAI HARI INI**
- [x] **Eksperimen E5:** *Failure Analysis* (Mendiagnosis mengapa sistem salah) ➔ **SELESAI HARI INI**
- [ ] **Eksperimen E4:** *Domain Shift* (Uji coba pada *soundscape* alam bebas seutuhnya) ➔ **BELUM**
- [ ] **Penulisan Naskah Bab 4 & Bab 5** (Memasukkan grafik dan tabel ke draf skripsi) ➔ **BELUM**

**Kesimpulan Progress:** Secara teknis (kodingan dan komputasi eksperimen utama), Anda sudah **90% selesai**. Yang tersisa hanyalah 1 eksperimen terakhir (E4) dan mulai menulis naskah Bab 4 (Pembahasan) berdasarkan grafik-grafik yang sudah kita *generate*.

---

## 2. Metodologi yang Digunakan

Metodologi yang Anda gunakan dalam skripsi ini disebut **Zero-Shot Audio Retrieval berbasis Frozen Pretrained Representations**. 

Artinya, alih-alih Anda melatih ulang model Kecerdasan Buatan (AI) dari nol (yang butuh superkomputer), Anda mengambil AI canggih yang sudah dilatih oleh ilmuwan dunia (*Pretrained*), "membekukan" otaknya (*Frozen*), lalu menggunakannya untuk mengubah suara burung menjadi vektor angka (Ekstraksi Fitur). 

Vektor burung dari alam liar (*Query*) kemudian dicocokkan dengan vektor burung di basis data (*Gallery*) menggunakan metrik jarak **Cosine Similarity**. Jika skor kemiripannya tinggi, AI akan menebak spesies burung tersebut.

---

## 3. Arsitektur Sistem (Diagram Alir)

Berikut adalah arsitektur sistem tugas akhir Anda (Diagram ini bisa Anda jadikan rujukan untuk menggambar di Bab 3 Metodologi):

```mermaid
flowchart TD
    subgraph Data Input
        Q[Kueri Audio Bersih\nBirdCLEF 5 detik]
        N[Derau Lapangan\nITERA AudioMoth]
    end

    subgraph Tahap Pencampuran (Tahap 4)
        M((Mixer SNR))
        Q --> M
        N --> M
        M -->|Audio Bising\nSNR: 20, 10, 0, -5 dB| Audio[Audio Terdegradasi]
    end

    subgraph Ekstraksi Representasi (Tahap 3)
        Audio --> E_R0[R0: MFCC Baseline]
        Audio --> E_R1[R1: PANNs CNN14]
        Audio --> E_R2[R2: BirdNET]
        Audio --> E_R3[R3: Random Control]
    end

    subgraph Retrieval & Evaluasi (E1, E2, E3)
        E_R2 -->|Vektor Kueri| Cosine[Perhitungan Cosine Similarity]
        Gal[Galeri Suara Spesies\nBirdCLEF] --> Cosine
        
        Cosine --> Rank[Ranking & Evaluasi mAP@10]
        Cosine --> OpenSet{Ambang Batas / Tau\nApakah Spesies Dikenal?}
        OpenSet -->|Skor < Tau| Reject[Tolak / Unknown]
        OpenSet -->|Skor >= Tau| Accept[Terima / Klasifikasi]
    end
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
1. **Pendekatan Degradasi Terkontrol (Paired Noise Degradation):** Anda tidak hanya menguji model, tapi Anda **menyuntikkan derau asli dari kampus ITERA** pada berbagai tingkatan yang dikontrol secara matematis (SNR -5 dB hingga 20 dB). Ini membuktikan batas kritis (*breaking point*) dari AI pengenal suara burung terhadap bising lingkungan tropis.
2. **Evaluasi Zero-Shot Retrieval:** Alih-alih melakukan klasifikasi kaku, Anda menggunakan pendekatan *Retrieval* (sistem pencarian kemiripan). Sistem ini jauh lebih fleksibel karena jika ada burung spesies baru besok, Anda cukup menambahkan suaranya ke Galeri, tanpa perlu men-*training* ulang model AI yang memakan waktu berhari-hari.
3. **Open-Set Rejection (Kalibrasi Tau):** Tugas akhir Anda memiliki kemampuan untuk **Menolak (*Reject*)**. Jika suara yang terekam AudioMoth tidak mirip dengan spesies target mana pun, sistem Anda berani mengatakan *"Ini bukan spesies target (Unknown)"* berkat penghitungan statistik Youden's J, meminimalisir deteksi palsu (*False Positive*).
