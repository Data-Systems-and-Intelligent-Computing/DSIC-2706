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
   Bagaimana `mAP@10`, Top-1, dan retensi retrieval berubah ketika query yang sama dicampur secara aditif dengan profil noise asli dari lima lokasi ITERA pada SNR yang sama; dan apakah representasi bioakustik mempertahankan ayunan retensi lintas lokasi yang lebih sempit daripada representasi audio umum?
4. **Sub-RQ 4 — Diagnostik kegagalan retrieval (E5)**  
   Moda kegagalan apa—*open-set false rejection*, *top-1 confusion above threshold*, atau *total retrieval collapse*—yang muncul pada kondisi clean dan bising; serta bagaimana hubungan margin threshold dan fitur spektral dengan moda tersebut?

## Di luar cakupan RQ aktif

Perbandingan antara focal recording dan rekaman burung yang dibuat langsung dalam *real soundscape* ITERA tidak diuji. Bank ITERA berisi noise bebas spesies target, sehingga tidak diperlukan anotasi spesies target untuk E2 atau E4. Studi real-soundscape membutuhkan korpus terpisah berisi vokalisasi spesies target yang direkam in-situ dan berada di luar scope penelitian ini.
