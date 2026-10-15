# Pertanyaan Penelitian (Research Questions) — DSIC-2706

## Judul kerja yang dipersempit

> **Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval under Controlled ITERA Field-Noise Mixtures in Indonesian Avifauna**

Judul ini membatasi penelitian pada pencampuran aditif terkontrol memakai rekaman noise lapangan ITERA. Penelitian ini tidak mengklaim validasi *domain shift* atau kinerja pada *real soundscape* burung in-situ.

## RQ utama

> **Representasi audio mana yang mempertahankan kualitas similarity retrieval paling baik ketika query bioakustik avifauna Indonesia didegradasi secara terkontrol oleh rekaman noise lapangan ITERA pada beberapa tingkat SNR?**

## Sub-RQ

1. **Sub-RQ 1 — Controlled noise degradation (E2)**  
   Seberapa besar perubahan `mAP@10`, `Recall@10`, `Precision@10`, MRR, dan Top-1 untuk R0–R3 pada Clean, +20, +10, 0, dan −5 dB ketika query dicampur noise ITERA fisik?
2. **Sub-RQ 2 — Frozen open-set threshold (E3)**  
   Apakah threshold kemiripan τ* yang dioptimalkan pada subset kalibrasi terpisah dan kemudian dibekukan mempertahankan perilaku penerimaan/penolakan yang terukur untuk target known-set dan kontrol unknown pada query bising?
3. **Sub-RQ 3 — Sensitivitas dan stabilitas profil noise lapangan (E4/H3)**  
   Bagaimana `mAP@10`, Top-1, dan retensi retrieval berubah ketika query yang sama dicampur secara aditif dengan profil noise asli dari lima lokasi ITERA pada SNR yang sama; dan bagaimana perbandingan ayunan mAP@10 absolut serta retensi relatif representasi bioakustik dan audio umum berubah ketika Kebun Raya dikeluarkan sebagai analisis sensitivitas?
4. **Sub-RQ 4 — Diagnostik kegagalan retrieval (E5)**  
   Moda kegagalan apa—*open-set false rejection*, *top-1 confusion above threshold*, atau *total retrieval collapse*—yang muncul pada kondisi clean dan bising; serta bagaimana hubungan margin threshold dan fitur spektral dengan moda tersebut?

## Di luar cakupan RQ aktif

Perbandingan antara focal recording dan rekaman burung yang dibuat langsung dalam *real soundscape* ITERA tidak diuji. Bank ITERA berisi noise bebas spesies target, sehingga tidak diperlukan anotasi spesies target untuk E2 atau E4. Studi real-soundscape membutuhkan korpus terpisah berisi vokalisasi spesies target yang direkam in-situ dan berada di luar scope penelitian ini.

## Riwayat rumusan dan status eksploratif

Rumusan asli berikut sudah tercatat pada **6 September 2026**, commit **25ebb72**, dan masih ada pada parent commit konsolidasi **7817355**:

- **H3 asli — Real Domain Shift Gap:** “Kinerja retrieval pada *real soundscape* ITERA turun lebih tajam daripada kondisi *controlled mixture* pada level SNR sebanding karena pergeseran domain tidak hanya berupa derau aditif, melainkan mencakup propagasi jarak, absorpsi udara, dan *reverberation*.”
- **H4 asli — Threshold Transfer Instability:** “Ambang batas kemiripan (τ) yang optimal pada kondisi bersih (*calibration-clean*) mengalami pergeseran titik operasi (*operating point drift*) saat derau lingkungan bertambah, memicu anjloknya *recall* atau lonjakan *false accept rate*.”

**12 Oktober 2026:** commit **7817355** merekam perubahan H3 menjadi stabilitas retensi profil noise lokasi dan H4 menjadi perubahan titik operasi ambang beku. Perubahan rumusan dicatat setelah artefak hasil E4/E3 tersedia, sehingga **H3 hasil reformulasi dan interpretasi H4 hasil reformulasi bersifat eksploratif**, bukan hipotesis baru yang dibekukan sebelum hasil dilihat. Klausul penurunan recall sudah ada pada H4 asli; perluasan bahasa menjadi “perubahan perilaku” tidak boleh digunakan untuk menyembunyikan bahwa false-accept rate tidak meningkat.

**15 Oktober 2026:** pelaporan H3 diperluas dengan ayunan mAP@10 absolut dan analisis sensitivitas tanpa Kebun Raya atas CSV yang sama. Tidak ada penghapusan lokasi dari E4, perubahan threshold, atau pengulangan eksperimen. H3 asli tentang real-soundscape tetap **belum diuji**. Tidak ada bukti uji langsung untuk mekanisme distorsi frekuensi, biofoni serangga, atau kompresi skor sebagai penyebab.

## Perubahan pertanyaan penelitian

Rumusan RQ utama pada 6 September 2026 (25ebb72) adalah: “Representasi audio mana yang mempertahankan kualitas similarity retrieval paling baik ketika query bioakustik mengalami peningkatan derau lingkungan dan pergeseran domain dari focal recording ke soundscape?”

Sub-RQ 3 asli menanyakan keunggulan retensi bioakustik dibanding audio generik dan MFCC pada derau setara. Sub-RQ 4 asli adalah: “Sebagai analisis sekunder, seberapa besar kesenjangan retrieval (*retrieval gap*) ketika beralih dari derau aditif terkontrol ke rekaman lapangan nyata (*real ITERA soundscapes*) yang mengalami pergeseran domain akustik multi-sumber?”

Pada 12 Oktober 2026, RQ utama dibatasi ke additive mixture, Sub-RQ 3 dialihkan ke profil lima lokasi E4/H3, dan Sub-RQ 4 ke diagnostik E5. Analisis stabilitas baru tidak menjawab ulang pertanyaan real-soundscape asli. Pada 15 Oktober, Sub-RQ 3 diperjelas agar memuat kedua skala ayunan dan sensitivitas lokasi. Jawaban terkini ada pada [catatan revisi](../REVISION_SUPERVISOR_2026-10-15.md).
