# Pembekuan Ruang Lingkup (Scope Freeze) — DSIC-2706

Dokumen ini mencatat batasan ruang lingkup taksonomi, pra-pemrosesan, dan parameter pengujian untuk Tugas Akhir DSIC-2706.

---

## 1. Taksonomi Target (16 Spesies Burung Sumatera)

### Amandemen Resmi Bertanggal (Versi 2.0 — 7 September 2026)
Berdasarkan ketersediaan data rekaman kualitas tinggi (Grade A/B) pada repositori Xeno-Canto dan penguatan relevansi ekologis bioakustik Pulau Sumatera, ruang lingkup taksonomi target secara resmi diformalkan pada **16 spesies burung aktual** (mencakup 5 spesies endemik Sumatera dan burung hutan pegunungan) dengan total **416 rekaman audio**:

| No | Spesies Kunci | Nama Ilmiah | Nama Umum (Inggris) | Status Endemik | Jumlah Klip |
| :-: | :--- | :--- | :--- | :-: | :-: |
| 1 | `Aethopyga_siparaja` | *Aethopyga siparaja* | Crimson Sunbird | Bukan | 26 |
| 2 | `Batrachostomus_cornutus` | *Batrachostomus cornutus* | Sunda Frogmouth | Bukan | 16 |
| 3 | `Brachypteryx_montana` | *Brachypteryx montana* | White-browed Shortwing | Bukan | 35 |
| 4 | `Carpococcyx_viridis` | *Carpococcyx viridis* | Sumatran Ground Cuckoo | **Endemik** | 20 |
| 5 | `Dicaeum_trigonostigma` | *Dicaeum trigonostigma* | Orange-bellied Flowerpecker | Bukan | 24 |
| 6 | `Dicrurus_hottentottus` | *Dicrurus hottentottus* | Hair-crested Drongo | Bukan | 35 |
| 7 | `Gypsophila_rufipectus` | *Gypsophila rufipectus* | Rusty-breasted Wren-Babbler | **Endemik** | 31 |
| 8 | `Halcyon_smyrnensis` | *Halcyon smyrnensis* | White-throated Kingfisher | Bukan | 20 |
| 9 | `Horornis_vulcanius` | *Horornis vulcanius* | Sunda Bush Warbler | Bukan | 35 |
| 10 | `Malacopteron_affine` | *Malacopteron affine* | Sooty-capped Babbler | Bukan | 18 |
| 11 | `Myophonus_melanurus` | *Myophonus melanurus* | Shiny Whistling Thrush | **Endemik** | 15 |
| 12 | `Napothera_albostriata` | *Napothera albostriata* | Sumatran Wren-Babbler | **Endemik** | 20 |
| 13 | `Orthotomus_ruficeps` | *Orthotomus ruficeps* | Ashy Tailorbird | Bukan | 30 |
| 14 | `Pnoepyga_pusilla` | *Pnoepyga pusilla* | Pygmy Cupwing | Bukan | 37 |
| 15 | `Polyplectron_chalcurum` | *Polyplectron chalcurum* | Bronze-tailed Peacock-Pheasant | **Endemik** | 19 |
| 16 | `Spilornis_cheela` | *Spilornis cheela* | Crested Serpent Eagle | Bukan | 35 |
| **Total** | **16 Spesies** | | | **5 Endemik** | **416 Klip** |

*Catatan Distribusi Klip:* Minimum 15 klip per spesies (*Myophonus melanurus*), maksimum 37 klip (*Pnoepyga pusilla*), dengan rata-rata 26 klip per spesies.

#### Alasan & Justifikasi Akademis Penggantian Spesies dari Versi Awal:
1. **Peningkatan Nilai Konservasi & Kebaruan Ilmiah:** Daftar baru mencakup 5 spesies burung endemik Sumatera yang berstatus terancam punah/langka (seperti Tokhtor Sumatera *Carpococcyx viridis* dan Kuwau-kerdil *Polyplectron chalcurum*), menggantikan spesies kosmopolitan umum dari draf awal.
2. **Kesesuaian Lisensi & Kualitas Audio:** Seluruh 416 rekaman terverifikasi memiliki lisensi terbuka Creative Commons (BY-NC-SA / BY-NC-ND) dan kualitas Grade A/B pada Xeno-Canto.
3. **Pencegahan Kebocoran Data (Recordist Disjoint):** Setiap spesies terpilih memiliki jumlah perekam independen yang memadai ($\ge 2$ perekam) sehingga pemisahan *Gallery* dan *Query* dapat dilakukan tanpa adanya tumpang tindih perekam (*Zero Recordist Overlap*).

---

### Catatan Historis Ruang Lingkup Awal (Versi 1.0 — Draf Awal)
*Daftar draf awal sebelum kurasi lapangan komprehensif:*  
*Acrocephalus orientalis, Aethopyga siparaja, Alcedo atthis, Alcedo meninting, Anthracoceros albirostris, Centropus bengalensis, Copsychus malabaricus, Copsychus saularis, Dicaeum trigonostigma, Dicrurus paradiseus, Eurystomus orientalis, Halcyon smyrnensis, Lanius schach, Orthotomus atrogularis, Orthotomus sutorius, Pycnonotus goiavier.*  
*(Sebanyak 13 spesies di atas telah digantikan secara resmi oleh daftar pada Versi 2.0 di atas).*

---

## 2. Parameter Pra-pemrosesan Audio (Tetap Dibekukan)
- Laju Sampel (*Sample Rate*): **32,000 Hz** (diresample otomatis ke 48,000 Hz khusus saat inferensi BirdNET)
- Kanal: **Mono (1 channel)**
- Durasi Segmen: **5.0 detik (160,000 sampel)**
- Seleksi Jendela: **Energi RMS tertinggi (Top-energy window)**
- Normalisasi Energi: **RMS target 0.05**

---

## 3. Tingkat Degradasi Derau (Tetap Dibekukan)
Tingkat degradasi derau aditif dibekukan pada 5 level:
1. **Clean** ($\text{SNR} = \infty$)
2. **SNR 20 dB** (Derau ringan)
3. **SNR 10 dB** (Derau sedang)
4. **SNR 0 dB** (Derau berat / sinyal sebanding derau)
5. **SNR -5 dB** (Derau ekstrem / derau melebihi sinyal)
