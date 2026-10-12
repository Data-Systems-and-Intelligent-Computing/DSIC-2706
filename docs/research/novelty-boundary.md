# Batasan Kebaruan dan Kontribusi — DSIC-2706

## Kontribusi ilmiah utama

1. **Paired robustness protocol**  
   Query yang sama diuji pada Clean, +20, +10, 0, dan −5 dB sehingga perubahan per-query mencerminkan efek pencampuran noise, bukan variasi rekaman.
2. **Controlled field-noise stress testing**  
   Noise berasal dari rekaman lapangan nyata AudioMoth ITERA dan dicampur secara terukur; tidak menggunakan pink noise sintetis sebagai bukti utama.
3. **Komparasi representasi lintas arsitektur**  
   MFCC, PANNs CNN14, BirdNET, dan kontrol ID-deterministik dibandingkan dengan cosine similarity dan metrik retrieval yang sama.
4. **Frozen open-set threshold**  
   Threshold τ* dikalibrasi pada subset terpisah lalu dibekukan sebelum test.
5. **Sensitivitas profil noise lokasi**  
   E4 membandingkan dampak profil noise dari lima lokasi ITERA pada protokol additive mixture yang sama.
6. **Taksonomi kegagalan yang dapat ditelusuri**  
   E5 memisahkan false rejection, confusion, dan collapse dengan batas field-data yang eksplisit.

## Yang bukan kontribusi atau klaim penelitian

- Validasi retrieval pada rekaman burung target yang dibuat langsung dalam real soundscape ITERA.
- Klaim *domain shift* akibat propagasi jarak, absorpsi, reverberasi, atau perangkat perekam di lapangan.
- Permintaan anotasi spesies target pada bank noise ITERA; set tersebut bebas spesies target dan tidak dipakai sebagai korpus focal-bird.
- Pelatihan model dari nol, fine-tuning penuh, classifier tertutup baru, inventarisasi biodiversitas ITERA, atau aplikasi produksi.
