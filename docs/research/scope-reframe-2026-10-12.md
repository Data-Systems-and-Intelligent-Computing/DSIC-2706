# Amendemen Scope dan H3 — 12 Oktober 2026

## Batas desain yang tetap berlaku

E2 dan E4 mencampur focal recording Xeno-Canto dengan noise lapangan AudioMoth ITERA secara aditif. Karena itu penelitian tidak mengklaim evaluasi rekaman burung yang dibuat langsung dalam *real soundscape* ITERA, termasuk efek jarak, propagasi, atau perilaku burung *in-situ*.

## H3 yang diuji

H3 bukan klaim *real-soundscape domain shift*. H3 menguji apakah representasi bioakustik mempertahankan **ayunan retensi yang lebih sempit** lintas profil spektral noise dari habitat/lokasi ITERA daripada representasi audio umum. Ini tepat diuji oleh E4 karena semua query, SNR, gallery, dan protokol retrieval dibuat sama; hanya profil noise lokasi yang berubah.

E4 memakai lima lokasi noise ITERA: Kebun Raya, Embung F, Gedung F, Masjid At-Tanwir, dan Sekitar GKU 1. Set ITERA bebas spesies target sehingga anotasi target-species tidak diperlukan.

## Bukti dan keputusan

Analisis statistik H3 memakai 311 query, lima profil lokasi, empat pengulangan segmen noise per lokasi, empat SNR, dan paired bootstrap 10.000 kali. Pada rata-rata empat SNR, ayunan retensi R1/PANNs = 0.240111 dan R2/BirdNET = 0.048607; selisih R1−R2 = 0.191504, CI 95% [0.152203, 0.241969]. H3 **didukung**.

Artefak: [`results/reproductions/H3_habitat_profile_stability_20261012T141344_312163Z`](../../results/reproductions/H3_habitat_profile_stability_20261012T141344_312163Z/), [tabel ringkasan](../../results/tables/24_h3_habitat_profile_stability.csv), dan [grafik](../../results/figures/15_h3_habitat_retention_stability.png).
