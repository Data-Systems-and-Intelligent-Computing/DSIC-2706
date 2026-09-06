# Pembekuan Ruang Lingkup (Scope Freeze) — DSIC-2706

## 1. Taksonomi Target (16 Spesies Burung Sumatera)
Ruang lingkup taksonomi target dibekukan pada 16 spesies burung representatif Sumatera dengan volume data terverifikasi:
1. *Acrocephalus orientalis* (Oriental Reed Warbler)
2. *Aethopyga siparaja* (Crimson Sunbird)
3. *Alcedo atthis* (Common Kingfisher)
4. *Alcedo meninting* (Blue-eared Kingfisher)
5. *Anthracoceros albirostris* (Oriental Pied Hornbill)
6. *Centropus bengalensis* (Lesser Coucal)
7. *Copsychus malabaricus* (White-rumped Shama)
8. *Copsychus saularis* (Oriental Magpie-Robin)
9. *Dicaeum trigonostigma* (Orange-bellied Flowerpecker)
10. *Dicrurus paradiseus* (Greater Racket-tailed Drongo)
11. *Eurystomus orientalis* (Dollarbird)
12. *Halcyon smyrnensis* (White-throated Kingfisher)
13. *Lanius schach* (Long-tailed Shrike)
14. *Orthotomus atrogularis* (Dark-necked Tailorbird)
15. *Orthotomus sutorius* (Common Tailorbird)
16. *Pycnonotus goiavier* (Yellow-vented Bulbul)

## 2. Parameter Pra-pemrosesan Audio
- Sample Rate: **32,000 Hz**
- Kanal: **Mono (1 channel)**
- Durasi Segmen: **5.0 detik (160,000 sampel)**
- Seleksi Jendela: **Energi RMS tertinggi**
- Normalisasi Energi: **RMS target 0.05**

## 3. Level Degradasi SNR
Tingkat degradasi derau dibekukan pada 5 level:
- **Clean** ($\text{SNR} = \infty$)
- **SNR 20 dB** (Derau ringan)
- **SNR 10 dB** (Derau sedang)
- **SNR 0 dB** (Derau berat / sinyal sebanding derau)
- **SNR -5 dB** (Derau ekstrem / derau melebihi sinyal)
