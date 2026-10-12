# Hipotesis Penelitian — DSIC-2706

H1, H2, H4, dan H5 diuji pada protokol *controlled additive field-noise mixture*. H3 juga diuji pada E4, sebagai perbandingan stabilitas retensi lintas **profil noise lapangan** ITERA. E4 tidak diklaim sebagai validasi rekaman burung *in-situ*.

- **H1 — Robustness retention**  
  Representasi *deep pretrained* mempertahankan proporsi `mAP@10` relatif lebih besar daripada MFCC ketika SNR diturunkan secara progresif.
- **H2 — Domain-specific advantage under additive noise**  
  Embedding bioakustik mengalami penurunan retensi retrieval lebih kecil daripada embedding audio generik pada query burung yang dicampur noise ITERA.
- **H3 — Habitat Profile Stability**  
  Representasi bioakustik terlatih mempertahankan retensi relatif `mAP@10` yang secara signifikan lebih stabil dan tidak fluktuatif lintas profil spektral habitat (ayunan retensi sempit) dibandingkan representasi audio umum yang rentan terhadap distorsi frekuensi tinggi/rendah.
- **H4 — Frozen-threshold operating-point change**  
  Threshold τ* yang optimal pada calibration-clean berubah perilaku operasionalnya saat query diberi noise; perubahan dapat tampak sebagai penurunan recall known-set atau perubahan false-accept rate.
- **H5 — Positive control baseline**  
  Clean retrieval R0, R1, dan R2 secara signifikan mengungguli kontrol ID-deterministik R3.

## Operasionalisasi H3

- **Pembanding utama:** R1/PANNs (audio umum) versus R2/BirdNET (bioakustik).
- **Sumber:** CSV mentah E4 yang tervalidasi, tanpa menghitung ulang pencampuran audio.
- **Unit:** 311 query yang sama, lima profil lokasi noise ITERA, empat segmen noise acak per lokasi, dan empat SNR.
- **Ukuran stabilitas:** untuk setiap representasi, `swing = max(relative retention antar lokasi) − min(relative retention antar lokasi)`, dirata-ratakan atas empat pengulangan segmen noise.
- **Uji:** paired bootstrap 10.000 resampling query, seed 20261012. H3 didukung apabila CI 95% untuk `swing R1 − swing R2` seluruhnya positif.

Hasil rata-rata empat SNR: ayunan R1 = 0.240111; R2 = 0.048607; selisih = 0.191504; CI 95% [0.152203, 0.241969]. H3 **didukung** dalam desain additive ITERA-noise.

Analisis inferensial H3 ditambahkan setelah E4 selesai, sehingga hasil signifikansi ini diperlakukan sebagai analisis eksploratif. Bagian H3 yang menyebut distorsi frekuensi tinggi/rendah belum diuji sebagai mekanisme penyebab: analisis ini membandingkan label lokasi dan retensi, belum mengaitkan ukuran spektral setiap noise dengan perubahan skor retrieval.

## Aturan interpretasi

E4 membuktikan stabilitas atau sensitivitas terhadap **profil noise lapangan** dari lokasi ITERA setelah pencampuran aditif pada SNR terkendali. E4 tidak mendukung klaim tentang jarak burung-mikrofon, propagasi, absorpsi, reverberasi, atau perilaku burung *in-situ*. Bank ITERA bebas spesies target; karenanya anotasi spesies target tidak diperlukan untuk E2/E4.
