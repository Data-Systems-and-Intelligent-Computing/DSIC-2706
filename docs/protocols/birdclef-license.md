# Protokol Kepatuhan Lisensi Kompetisi BirdCLEF+ 2026 (D-07)

**Topik Riset:** DSIC27-06 — Mencari Audio yang Mirip Ketika Datanya Terbatas  
**Nama Kompetisi:** BirdCLEF+ 2026 — Acoustic Species Identification in the Pantanal, South America  
**Penyelenggara:** LifeCLEF 2026 / Google Research & Cornell Lab of Ornithology, dihosting di Kaggle  
**URL Halaman Kompetisi:** <https://www.kaggle.com/competitions/birdclef-2026>  
**URL Aturan Kompetisi:** <https://www.kaggle.com/competitions/birdclef-2026/rules>  
**Tanggal Akses & Persetujuan:** 12 September 2026  
**Status Keputusan Pembimbing:** D-07 (Disetujui untuk Skripsi & Artikel Ilmiah)

---

## 1. Lisensi Data Kompetisi

Data kompetisi BirdCLEF+ 2026 dirilis di bawah lisensi:

> **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**

Teks ringkas lisensi (Legal Code: <https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode>):

### Anda diizinkan untuk:

- **Berbagi** — menyalin dan menyebarluaskan materi ini dalam bentuk atau format apa pun.
- **Adaptasi** — menggubah, mengubah, dan membuat turunan dari materi ini.

Pemberi lisensi tidak dapat mencabut kebebasan di atas selama Anda mematuhi ketentuan lisensi.

### Dengan ketentuan berikut:

- **Atribusi (BY)** — Anda harus mencantumkan kredit yang sesuai, memberikan tautan ke lisensi, dan menunjukkan perubahan yang dilakukan. Anda dapat melakukannya dengan cara yang wajar, tetapi tidak dengan cara apa pun yang menyarankan pemberi lisensi mendukung Anda atau penggunaan Anda.
- **NonKomersial (NC)** — Anda tidak boleh menggunakan materi ini untuk tujuan komersial.
- **BerbagiSerupa (SA)** — Apabila Anda menggubah, mengubah, atau membuat turunan dari materi ini, Anda harus mendistribusikan kontribusi Anda di bawah lisensi yang sama dengan aslinya.

### Tidak ada pembatasan tambahan:

- Anda tidak boleh menggunakan persyaratan hukum atau sarana teknologi yang secara hukum membatasi orang lain untuk melakukan hal-hal yang diizinkan oleh lisensi.

---

## 2. Klausul Penggunaan Data Kompetisi Kaggle (Competition Rules)

Berikut adalah teks verbatim dari bagian **Data Access and Use** pada aturan kompetisi BirdCLEF+ 2026:

> **DATA ACCESS AND USE:**
>
> "Unless otherwise specified in the Competition Specific Terms above, you may access and use the Competition Data for non-commercial purposes only. You may access and use the Competition Data specifically including:
>
> (a) participating in the Competition;
> (b) participating in Kaggle.com forums; and
> (c) academic research and education.
>
> You agree to use reasonable and suitable measures to prevent persons who have not agreed to these Rules from gaining access to the Competition Data. You agree not to transmit, duplicate, publish, redistribute, or otherwise provide the Competition Data to any party not participating in the Competition.
>
> You agree to notify Kaggle immediately upon learning of any potential, suspected, or actual unauthorized access, transmission, or copying of the Competition Data and will cooperate with Kaggle and the Competition Sponsor in mitigating any resulting harm.
>
> The Competition Sponsor may disqualify you if you use the Competition Data in a manner not permitted by the Competition Website, these Rules, or the terms of the Creative Commons license. If these Rules conflict with such license terms, these Rules will govern."

### 2.1 Ringkasan Klausul Utama

| # | Aspek | Ketentuan |
|---|---|---|
| a | **Penggunaan yang Diizinkan** | Non-komersial saja, termasuk partisipasi kompetisi, forum Kaggle, riset akademik, dan pendidikan |
| b | **Larangan Redistribusi** | Dilarang mentransmisikan, menduplikasi, mempublikasikan, meredistribusikan, atau menyebarkan data kepada pihak yang belum menyetujui aturan |
| c | **Keamanan Data** | Peserta wajib mengambil langkah wajar untuk mencegah akses oleh pihak yang belum menyetujui aturan |
| d | **Kewajiban Pemberitahuan** | Wajib memberitahu Kaggle segera jika terjadi akses/transmisi/penyalinan tidak sah |
| e | **Klausul Preseden** | Jika aturan kompetisi bertentangan dengan ketentuan lisensi CC, aturan kompetisi yang berlaku |

### 2.2 Lisensi Solusi Pemenang

Pemenang hadiah (total prize pool \$50,000) diwajibkan melisensikan solusi kemenangan mereka di bawah lisensi *open-source* yang disetujui OSI (misal Apache 2.0 atau MIT) dan menyediakan kode reproduksi lengkap.

### 2.3 Data Eksternal

Data eksternal diizinkan **hanya jika tersedia secara publik dan dapat diakses secara setara oleh semua peserta tanpa biaya**, serta diumumkan di forum kompetisi.

---

## 3. Atribusi Sumber Data (Kewajiban Hak Cipta)

### 3.1 Xeno-Canto Foundation

Dataset `train_audio` BirdCLEF+ 2026 bersumber utama dari repositori bioakustik terbuka **Xeno-Canto** (<https://xeno-canto.org/>). Setiap rekaman pada Xeno-Canto dilisensikan secara individual oleh perekam aslinya di bawah salah satu lisensi Creative Commons berikut:

| Lisensi | Kode SPDX | Penggunaan Komersial | Karya Turunan |
|---|---|---|---|
| CC BY 4.0 | `CC-BY-4.0` | ✅ Ya | ✅ Ya |
| CC BY-SA 4.0 | `CC-BY-SA-4.0` | ✅ Ya | ✅ Ya (ShareAlike) |
| CC BY-NC 4.0 | `CC-BY-NC-4.0` | ❌ Tidak | ✅ Ya |
| CC BY-NC-SA 4.0 | `CC-BY-NC-SA-4.0` | ❌ Tidak | ✅ Ya (ShareAlike) |
| CC BY-NC-ND 4.0 | `CC-BY-NC-ND-4.0` | ❌ Tidak | ❌ Tidak |

**Kewajiban atribusi per rekaman:**
- Nama perekam (*recordist/author*)
- ID rekaman unik Xeno-Canto (misal: `XC1053050`)
- Jenis lisensi CC yang berlaku
- Tautan ke halaman rekaman asli di Xeno-Canto

Seluruh informasi ini dicatat pada manifes data `data/manifests/dataset_split.csv`.

### 3.2 iNaturalist

Sebagian data juga dapat bersumber dari **iNaturalist** (<https://www.inaturalist.org/>) dengan lisensi Creative Commons atau Public Domain (CC0).

### 3.3 Kewajiban Sitasi Akademik

Untuk penggunaan dalam publikasi ilmiah, wajib menyitasi:

1. **Kompetisi BirdCLEF+ 2026:**
   ```
   Stefan Kahl, Holger Klinck, Connor Wood, Tom Denton et al.
   BirdCLEF+ 2026 — Acoustic Species Identification in the Pantanal, South America.
   Kaggle Competition, 2026.
   https://www.kaggle.com/competitions/birdclef-2026
   ```

2. **Xeno-Canto:**
   ```
   Xeno-Canto Foundation and Naturalis Biodiversity Center.
   xeno-canto — Sharing bird sounds from around the world.
   https://xeno-canto.org/
   ```

---

## 4. Penerapan pada Penelitian DSIC-2706

### 4.1 Kepatuhan Lisensi CC BY-NC-SA 4.0

| Aspek | Status | Keterangan |
|---|---|---|
| Non-Komersial | ✅ Patuh | Penelitian untuk Tugas Akhir/Skripsi dan artikel ilmiah peer-reviewed |
| Atribusi | ✅ Patuh | Nama perekam, ID rekaman, dan lisensi dicatat di manifes |
| BerbagiSerupa | ✅ Patuh | Kode penelitian dirilis di bawah lisensi MIT; data turunan tidak didistribusikan |
| Larangan Redistribusi Audio | ✅ Patuh | Audio mentah masuk `.gitignore`; tidak dipublikasikan ulang |
| Persetujuan Pembimbing | ✅ Disetujui | Keputusan D-07, disetujui Dosen Pembimbing I |

### 4.2 Batasan Penggunaan

- Penelitian DSIC-2706 **bukan bertujuan mengejar peringkat di leaderboard Kaggle**, melainkan studi ketahanan representasi audio (*audio representation robustness study*) pada kondisi derau dan pergeseran domain.
- Seluruh penggunaan data dibekukan secara deterministik melalui aturan kode pada Gate 1-R.
- Audio mentah berukuran besar **tidak** disertakan dalam repositori Git (ditegakkan melalui `.gitignore` pada folder `data/BirdClef/`).

---

## 5. Riwayat Dokumen

| Versi | Tanggal | Perubahan |
|---|---|---|
| 1.0 | 12 Sep 2026 | Versi awal — klausul penggunaan, atribusi sumber, batasan eksperimen |
| 2.0 | 03 Okt 2026 | Pembaruan lengkap — menambahkan teks lisensi CC BY-NC-SA 4.0 penuh, klausul Kaggle Competition Rules, tabel lisensi per rekaman Xeno-Canto, kewajiban sitasi akademik, dan tabel kepatuhan |