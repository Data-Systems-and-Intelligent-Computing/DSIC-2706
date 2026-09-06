# Batasan Kebaruan & Kontribusi (Novelty Boundary) — DSIC-2706

## Kontribusi Ilmiah Utama
1. **Paired Robustness Protocol:**
   Evaluasi ketahanan terhadap derau dilakukan berpasangan (*paired stress-testing*) pada query yang sama persis melintasi tingkat SNR (Clean, 20 dB, 10 dB, 0 dB, -5 dB), memastikan perbedaan skor murni mencerminkan ketahanan representasi, bukan variasi rekaman.
2. **Controlled Noise Stress-Testing:**
   Penggunaan bank derau lingkungan riil dari lanskap kampus ITERA (Embung, Arboretum, Area Terbuka).
3. **Komparasi Representasi Lintas Arsitektur:**
   Perbandingan langsung representasi parametrik klasik (MFCC), representasi audio generik (PANNs CNN14), representasi bioakustik terspesialisasi, dan kontrol negatif acak (Random Ranking) menggunakan metrik kemiripan tunggal yang adil (*cosine similarity*).
4. **Analisis Transfer Ambang Batas Open-Set:**
   Pengujian kestabilan operating point ambang batas $\tau$ terbekukan (*frozen threshold transfer*) di bawah pengaruh derau lingkungan.
5. **Jembatan Validasi Eksternal:**
   Membandingkan degradasi derau sintetis terkontrol terhadap pergeseran domain *real field soundscapes*.

---

## Yang BUKAN Kontribusi Utama (Non-Goals)
- Melatih atau membuat arsitektur model bioakustik pondasi baru dari nol (*training from scratch*).
- Fine-tuning ekstensif pada seluruh lapisan model deep learning.
- Membangun classifier spesies fauna tertutup baru (*closed-set multi-class classifier*).
- Pemodelan okupansi (*occupancy modelling*) atau estimasi kelimpahan populasi satwa (*abundance estimation*).
- Inventarisasi biodiversitas menyeluruh untuk kampus ITERA atau Sumatera.
- Pengembangan aplikasi mobile atau dashboard pemantauan produksi.
