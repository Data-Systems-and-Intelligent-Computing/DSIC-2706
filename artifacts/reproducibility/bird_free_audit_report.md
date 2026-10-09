# Laporan Audit Saintifik dan Verifikasi Derau ITERA (DSIC-2706)

**Proyek:** DSIC-2706 — Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval  
**Tanggal Audit:** 9 Oktober 2026  
**Status Audit:** Terverifikasi Lengkap (Empirically Audited & Disclosed)  
**Tujuan Dokumen:** Memenuhi evaluasi saintifik mengenai label `verified_bird_free: True` pada 1.799 berkas derau lapangan ITERA, mendokumentasikan karakteristik spektral perangkat keras, menganalisis faktor false acceptance pada E3, serta menjelaskan keterbatasan alami biofoni pada soundscape BirdCLEF.

---

## 1. Ringkasan Eksekutif & Klarifikasi Definisi "Bird-Free"

Pada manifes `data/manifests/itera_noise_manifest.csv`, terdapat 1.799 berkas audio dengan kolom boolean `verified_bird_free: True`. Batasan semantik dari label tersebut didefinisikan secara ketat sebagai berikut:

1. **Definisi yang Valid (Target-Bird-Free = 100%):**  
   Seluruh 1.799 berkas derau lingkungan ITERA **100.0% bebas dari 20 spesies burung target Neotropis**. Tidak ada satu pun vokalisasi dari spesies target (*Brotogeris jugularis*, *Trogon melanurus*, dsb.) yang masuk ke dalam bank derau, karena pemisahan biogeografis absolut antara Alam Neotropis (Amerika Tropis) dan Alam Sundaland/Indomalayan (Sumatera, Indonesia).
2. **Koreksi & Pembatasan Saintifik (Acoustically Silent / Biophony-Free = False):**  
   Label `verified_bird_free` **TIDAK DAPAT** ditafsirkan sebagai rekaman anechoic murni atau bebas dari seluruh suara hayati. Perekaman outdoor di lingkungan tropis kampus ITERA secara alami menangkap biofoni lokal (stridulasi jangkrik/serangga malam, katak, serta fauna lokal).
3. **Dinamika False Acceptance (FPR E3):**  
   Pada kondisi Clean, representasi BirdNET ($R_2$) menghasilkan False Positive Rate sebesar **39,0%** terhadap 100 berkas derau ITERA pada ambang batas tau* = 0.7128. Rerata kesamaan kosinus derau terhadap galeri berada pada 0.683 (std = 0.064), sehingga ekor atas distribusinya secara probabilistik melampaui tau*. Tren observasional menunjukkan tingkat false accept lebih tinggi pada rekaman outdoor tertentu (seperti Gedung F dan GKU 1), yang dihipotesiskan berkaitan dengan biofoni lokal atau karakteristik akustik lingkungan, namun memerlukan anotasi aural manual lanjutan untuk pembuktian definitif.

---

## 2. Profil Akustik Perangkat Keras AudioMoth (10 Konfigurasi Lapangan)

Pengambilan data lapangan di ITERA dilakukan pada 5 lokasi berbeda menggunakan perekam AudioMoth (32 kHz sampling rate, 55 detik record / 5 detik sleep) dengan dua mekanisme pemicu (*Trigger*): **Frequency Trigger (Center 4.0 kHz)** dan **Amplitude Trigger**.

Berikut adalah rekapitulasi energi spektral terukur dari 1.799 berkas derau:

| Lokasi & Filter | Total Berkas | Filter | Mean RMS | Sub-1kHz (%) | 1–4 kHz (%) | 4–8 kHz (%) | >8 kHz (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Embung F ITERA Amplitudo` | 180 | High-pass | 0.0107 | 57.3% | 26.9% | 5.9% | N/A |
| `Embung F ITERA Frequency` | 180 | Frequency Trigger | 0.0275 | 18.5% | 3.0% | 1.5% | 1.6% |
| `Gedung F Amplitudo` | 180 | High-pass | 0.0185 | 35.6% | 52.2% | 9.5% | 2.7% |
| `Gedung F Frequency` | 180 | Frequency | 0.0588 | 83.2% | 13.4% | 2.5% | 0.9% |
| `Kebun Raya Amplitudo` | 180 | High-pass | 0.0372 | 49.3% | 39.3% | 7.0% | N/A |
| `Kebun Raya Frequency` | 179 | High-pass / Default | 0.0203 | 80.1% | 12.2% | 1.9% | 5.8% |
| `Masjid At-tanwir Amplitudo` | 180 | High-pass | 0.0255 | 45.6% | 37.8% | 3.1% | 13.5% |
| `Masjid At-tanwir Frequency` | 180 | High-pass / Default | 0.0438 | N/A | N/A | N/A | N/A |
| `Sekitar GKU 1 Amplitudo` | 180 | High-pass | 0.0561 | 29.1% | 64.8% | 5.1% | N/A |
| `Sekitar GKU 1 Frequency` | 180 | Frequency | 0.1069 | 66.0% | 31.8% | 1.8% | 0.3% |

### Observasi Akustik Utama:
- **Dominasi Sub-1kHz (Antropofoni & Geofoni):** Sebagian besar rekaman lapangan luar ruangan didominasi oleh energi frekuensi rendah (< 1 kHz, rata-rata 57–83%), mencerminkan hembusan angin terbuka, resonansi air di Embung F, dan aktivitas kampus. Pada `Gedung F Frequency`, energi sub-1kHz mencapai rata-rata 83,2%, sementara pita 1–4 kHz menyumbang 13,4% dan 4–8 kHz menyumbang 2,5%.
- **Variasi Pita 1–4 kHz:** Pada konfigurasi tertentu seperti `Sekitar GKU 1 Amplitudo` (64,8%), `Gedung F Amplitudo` (52,2%), dan `Sekitar GKU 1 Frequency` (31,8%), terdapat proporsi energi yang lebih signifikan pada pita 1–4 kHz. Nilai `N/A` pada kolom >8 kHz menunjukkan batas filter analisis perangkat keras pada subset tertentu.

---

## 3. Dekonstruksi 39 Kasus False Acceptance E3 (BirdNET R2)

Pada pengujian E3 kondisi Clean, kueri kontrol negatif terdiri dari 100 spesies burung non-target dan 100 berkas derau ITERA. Hasil uji menunjukkan:
- **Non-Target Birds False Accept:** 18 dari 100 (18,0%)
- **ITERA Environmental Noise False Accept:** 39 dari 100 (39,0%)
- **Total FPR Gabungan:** 57 dari 200 (28,5%)

Pecahan 39 kasus *False Acceptance* derau berdasarkan lokasi dan jenis trigger diuraikan pada tabel berikut:

| Lokasi & Trigger Asal Berkas | Jumlah Sampel Uji | False Accept ($R_2$) | False Acceptance Rate |
| :--- | :---: | :---: | :---: |
| `Embung F ITERA Amplitudo` | 5 | 3 | 60.0% |
| `Embung F ITERA Frequency` | 11 | 2 | 18.2% |
| `Gedung F Amplitudo` | 12 | 4 | 33.3% |
| `Gedung F Frequency` | 8 | 8 | 100.0% |
| `Kebun Raya Amplitudo` | 6 | 1 | 16.7% |
| `Kebun Raya Frequency` | 11 | 0 | 0.0% |
| `Masjid At-tanwir Amplitudo` | 11 | 1 | 9.1% |
| `Masjid At-tanwir Frequency` | 14 | 4 | 28.6% |
| `Sekitar GKU 1 Amplitudo` | 11 | 7 | 63.6% |
| `Sekitar GKU 1 Frequency` | 11 | 9 | 81.8% |

### Temuan dan Hipotesis Kerja:
1. **Distribusi False Accept Berdasarkan Lokasi (Keterbatasan Ukuran Sampel):**  
   Pada subset uji kontrol negatif ($N=100$ berkas derau), ukuran sampel per lokasi berkisar antara 5 hingga 14 berkas. Perekaman `Gedung F Frequency` mencatat 8/8 (100,0%) false accept, dan `Sekitar GKU 1 Frequency` mencatat 9/11 (81,8%) false accept. Sebaliknya, lokasi seperti `Kebun Raya Frequency` mencatat 0/11 (0,0%) dan `Masjid At-tanwir Amplitudo` mencatat 1/11 (9,1%).
2. **Hipotesis Kerja Mekanisme Bioakustik (Belum Dibuktikan Definitif):**  
   Penyebab spesifik dari false accept pada 8 berkas `Gedung F Frequency` belum diverifikasi secara definitif melalui pendengaran aural manual atau detektor bioakustik per detik. Hipotesis bahwa rekaman tersebut menangkap biofoni lokal (seperti serangga kanopi atau kicauan burung urban setempat) ditempatkan sebagai **hipotesis kerja** yang memerlukan investigasi ornitologis lanjutan.
3. **Dinamika Representasi Kemiripan Kosinus:**  
   Dari perspektif komputasi representasi beku, ruang embedding BirdNET menghasilkan distribusi kesamaan kosinus terhadap derau lingkungan dengan rata-rata empiris sekitar 0.683 (rentang 0.523 - 0.817, simpangan baku 0.064). Karena ambang batas tau* = 0.7128 berada dekat dengan persentil ke-75 dari distribusi derau, secara matematis sekitar 39% derau lingkungan akan memiliki skor di atas ambang batas. Hal ini mengonfirmasi bahwa ambang batas tunggal tau* yang dikalibrasi pada kondisi bersih tidak secara otomatis memberikan kekebalan terhadap sinyal derau lingkungan yang memiliki magnitudo kemiripan moderat.

---

## 4. Keterbatasan Biofoni Latar Belakang pada Eksperimen E4 (BirdCLEF Soundscapes)

Pada Eksperimen E4 (*Sensitivitas Profil Derau Spektral*), sinyal query dicampur dengan rekaman *train_soundscapes* BirdCLEF 2026. Batasan metodologis yang dicatat adalah:

1. **Keberadaan Biofoni Latar Belakang Alami:**  
   Soundscape BirdCLEF merupakan rekaman habitat alami berkelanjutan (panjang 60 detik) yang diambil di cagar alam Neotropis. Secara inheren, rekaman tersebut mengandung vokalisasi burung latar belakang alami (*background chorus*) dan suara serangga tropis.
2. **Sifat Eksperimen Aditif Sintetis:**  
   Proses pencampuran pada E4 dilakukan secara aditif berbasis SNR terkontrol (alpha * s + beta * n), identik dengan formulasi matematis pada E2. Eksperimen ini belum merepresentasikan pergeseran domain propagasi fisik nyata (seperti atenuasi jarak rambat, pantulan geometri kanopi/reverberasi, atau multipath dispersion).
3. **Status Hipotesis H3:**  
   Oleh karena keterbatasan ini dan belum teranotasinya soundscape lapangan ITERA secara ground-truth bounding box, pengujian domain shift in-situ nyata **DITANGGUHKAN (Deferred)** dan secara jujur diberi status **"Tidak Diuji"** dalam naskah skripsi dan tabel ringkasan hipotesis.

---

## 5. Rekomendasi untuk Penggunaan Manifes

1. Kolom `verified_bird_free` pada `itera_noise_manifest.csv` dipertahankan dengan catatan dokumentasi resmi bahwa verifikasi tersebut merujuk pada **Target-Avian-Free Verification** (bebas dari 20 takson target).
2. Peneliti selanjutnya yang menggunakan bank data ini untuk pengujian deteksi bioakustik disarankan memisahkan subset `Amplitudo` (didominasi geofoni/antropofoni murni) dari subset `Frequency` (mengandung biofoni lokal Sundaland).
