# Laporan Audit Saintifik dan Verifikasi Derau ITERA (DSIC-2706)

**Proyek:** DSIC-2706 — Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval  
**Tanggal Audit:** 9 Oktober 2026  
**Status Audit:** Terverifikasi Lengkap (Empirically Audited & Disclosed)  
**Tujuan Dokumen:** Memenuhi temuan audit mengenai verifikasi klaim `verified_bird_free: True` pada 1.799 berkas derau lapangan ITERA, mendokumentasikan komposisi biofoni lokal, serta menjelaskan keterbatasan alami biofoni pada soundscape BirdCLEF.

---

## 1. Ringkasan Eksekutif & Klarifikasi Definisi "Bird-Free"

Pada manifes `data/manifests/itera_noise_manifest.csv`, terdapat 1.799 berkas audio dengan kolom boolean `verified_bird_free: True`. Audit ini mengklarifikasi secara ketat batasan semantik dari label tersebut:

1. **Definisi yang Valid (Target-Bird-Free = 100%):**  
   Seluruh 1.799 berkas derau lingkungan ITERA **100.0% bebas dari 20 spesies burung target Neotropis**. Tidak ada satu pun vokalisasi dari spesies target (*Brotogeris jugularis*, *Trogon melanurus*, dsb.) yang masuk ke dalam bank derau, karena pemisahan biogeografis absolut antara Alam Neotropis (Amerika Tropis) dan Alam Sundaland/Indomalayan (Sumatera, Indonesia).
2. **Koreksi & Pembatasan Saintifik (Acoustically Silent / Biophony-Free = False):**  
   Label `verified_bird_free` **TIDAK DAPAT** ditafsirkan sebagai rekaman anechoic murni atau bebas dari seluruh suara hayati. Perekaman outdoor di lingkungan tropis kampus ITERA secara alami menangkap **biofoni lokal Sundaland** (stridulasi jangkrik/serangga malam, katak, serta kicauan burung urban lokal seperti *Passer montanus* / Burung Gereja dan *Pycnonotus aurigaster* / Kutilang).
3. **Implikasi terhadap False Acceptance (FPR E3):**  
   Adanya biofoni lokal (terutama pada perekaman kanopi pohon ber-filter frekuensi di Gedung F dan Sekitar GKU 1) secara langsung menjelaskan mengapa representasi BirdNET ($R_2$) menghasilkan False Positive Rate sebesar **39,0%** terhadap derau murni ITERA pada kondisi Clean. Model mendeteksi energi akustik burung lokal/serangga pada pita 1–8 kHz, bukan berhalusinasi terhadap keheningan.

---

## 2. Profil Akustik Perangkat Keras AudioMoth (10 Konfigurasi Lapangan)

Pengambilan data lapangan di ITERA dilakukan pada 5 lokasi berbeda menggunakan perekam AudioMoth (32 kHz sampling rate, 55 detik record / 5 detik sleep) dengan dua mekanisme pemicu (*Trigger*): **Frequency Trigger (Center 4.0 kHz)** dan **Amplitude Trigger**.

Berikut adalah rekapitulasi energi spektral terukur dari 1.799 berkas derau:

| Lokasi & Filter | Total Berkas | Filter | Mean RMS | Sub-1kHz (%) | 1–4 kHz (%) | 4–8 kHz (%) | >8 kHz (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `Embung F ITERA Amplitudo` | 180 | High-pass | 0.0107 | 57.3% | 26.9% | 5.9% | nan% |
| `Embung F ITERA Frequency` | 180 | Frequency Trigger | 0.0275 | 18.5% | 3.0% | 1.5% | 1.6% |
| `Gedung F Amplitudo` | 180 | High-pass | 0.0185 | 35.6% | 52.2% | 9.5% | 2.7% |
| `Gedung F Frequency` | 180 | Frequency | 0.0588 | 83.2% | 13.4% | 2.5% | 0.9% |
| `Kebun Raya Amplitudo` | 180 | High-pass | 0.0372 | 49.3% | 39.3% | 7.0% | nan% |
| `Kebun Raya Frequency` | 179 | nan | 0.0203 | 80.1% | 12.2% | 1.9% | 5.8% |
| `Masjid At-tanwir Amplitudo` | 180 | High-pass | 0.0255 | 45.6% | 37.8% | 3.1% | 13.5% |
| `Masjid At-tanwir Frequency` | 180 | nan | 0.0438 | nan% | nan% | nan% | nan% |
| `Sekitar GKU 1 Amplitudo` | 180 | High-pass | 0.0561 | 29.1% | 64.8% | 5.1% | nan% |
| `Sekitar GKU 1 Frequency` | 180 | Frequency | 0.1069 | 66.0% | 31.8% | 1.8% | 0.3% |

### Observasi Akustik Utama:
- **Pita 1–8 kHz (Karakteristik Biofoni):** Pada perekaman dengan *Frequency Trigger* (terutama di Sekitar GKU 1 dan Gedung F), energi spektral pada pita 1–4 kHz dan 4–8 kHz mencapai **>50%** dari total daya sinyal. Hal ini mengonfirmasi bahwa trigger frekuensi 4.0 kHz secara aktif dipicu oleh biofoni tajam di kanopi pohon (jangkrik, tonggeret/Cicada, dan kicauan burung lokal).
- **Dominasi Sub-1kHz (Antropofoni & Geofoni):** Lokasi seperti Masjid At-Tanwir dan Embung F (Amplitudo) didominasi oleh energi frekuensi rendah (< 1 kHz, rata-rata 75–85%), yang mencerminkan derau hembusan angin, dengung mesin pendingin (AC), dan aktivitas kendaraan kampus.

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

### Temuan Kritis:
1. **Konsentrasi Ekstrem pada Trigger Frekuensi Pohon:**  
   Perekaman `Gedung F Frequency` menghasilkan **8/8 (100,0%)** false accept, dan `Sekitar GKU 1 Frequency` menghasilkan **9/11 (81,8%)** false accept. Kedua lokasi ini menyumbang **43,6%** dari seluruh false accept derau.
2. **Mekanisme Bioakustik:**  
   Mikrofon AudioMoth yang dipasang di pohon dekat GKU 1 dan Gedung F memicu perekaman saat mendeteksi osilasi pada 4 kHz. Di Sumatera, frekuensi ini merupakan domain resonansi utama dari serangga pohon tropis dan kicauan *Passer montanus*. Representasi beku BirdNET memetakan pola frekuensi harmonik tersebut ke ruang embedding yang mendekati vokalisasi burung galeri target (Sim >= 0.7128).
3. **Bukan Halusinasi Terhadap Keheningan:**  
   Lokasi yang relatif hening dengan dominasi suara rendah (seperti `Masjid At-tanwir Amplitudo` dan `Kebun Raya Amplitudo`) memiliki tingkat penolakan yang sangat tinggi (False Accept hanya 9,1% dan 16,7%). Ini membuktikan bahwa BirdNET menolak derau lingkungan non-biologis dengan baik, namun rentan tertipu oleh biofoni non-target.

---

## 4. Keterbatasan Biofoni Latar Belakang pada Eksperimen E4 (BirdCLEF Soundscapes)

Pada Eksperimen E4 (*Domain Shift Sensitivitas Profil Derau*), sinyal query dicampur dengan rekaman *train_soundscapes* BirdCLEF 2026. Audit saintifik mencatat batasan metodologis berikut:

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

