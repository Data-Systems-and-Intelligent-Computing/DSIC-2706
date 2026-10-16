# Pembekuan Ruang Lingkup (Scope Freeze) — DSIC-2706

Dokumen ini mencatat batasan ruang lingkup taksonomi, pra-pemrosesan, dan parameter pengujian untuk Tugas Akhir DSIC-2706.

---

## 1. Taksonomi Target (20 Spesies Avifauna Indonesia)

### Amandemen Resmi Bertanggal (Versi 4.0 — 10 Oktober 2026)
Berdasarkan arahan resmi Dosen Pembimbing (Bapak Ardika Satria) pada 10 Oktober 2026, ruang lingkup dataset dialihkan sepenuhnya ke **Avifauna Kepulauan Indonesia (Xeno-Canto Indonesia)**. Keputusan ini diambil untuk mengeliminasi ketidakcocokan biogeografis (spesies Neotropis vs derau Sumatera) dan memastikan keterikatan ekologis yang valid dengan habitat tropis Indonesia:
1. Spesies target dibatasi pada burung yang **hadir dan tercatat di Indonesia**, dengan seleksi spesies umum dan tersebar luas (*widespread species*, termasuk kehadiran klip dari Sumatera).
2. Rekaman di luar wilayah geografis Indonesia **dieksklusi secara mutlak**.
3. Seluruh berkas audio diunduh langsung dari Xeno-Canto dan diaudit secara ketat: durasi, sampling rate asli, SHA-256, dan keterbacaan (*100% decodable*).
4. Hasil lama berbasis BirdCLEF dipindahkan ke arsip historis (`results/archive/birdclef_2026/`).

Daftar resmi **20 spesies burung target** dengan total **1.216 rekaman audio** terkelola (`data/manifests/species_freeze.csv`):

| No | Spesies Kunci | Nama Ilmiah | Nama Indonesia / Inggris | Klip Terverifikasi | Perekam Unik |
| :-: | :--- | :--- | :--- | :-: | :-: |
| 1 | `pygcup1` | *Pnoepyga pusilla* | Berencet kerdil / Pygmy Cupwing | 105 | 35 |
| 2 | `rubcuc1` | *Cacomantis sepulcralis* | Wiwik uncuing / Rusty-breasted Cuckoo | 85 | 32 |
| 3 | `horbab1` | *Malacocincla sepiaria* | Pelanduk semak / Horsfield's Babbler | 68 | 32 |
| 4 | `moutai1` | *Phyllergates cucullatus* | Cinenen gunung / Mountain Tailorbird | 137 | 29 |
| 5 | `lessho1` | *Brachypteryx leucophris* | Cingcoang cokelat / Lesser Shortwing | 66 | 26 |
| 6 | `latnig1` | *Caprimulgus macrurus* | Cabak maling / Large-tailed Nightjar | 47 | 26 |
| 7 | `sohbul1` | *Pycnonotus aurigaster* | Cucak kutilang / Sooty-headed Bulbul | 44 | 26 |
| 8 | `olbsun1` | *Cinnyris jugularis* | Burung-madu sriganti / Olive-backed Sunbird | 123 | 23 |
| 9 | `hoopit1` | *Pitta sordida* | Paok hijau / Hooded Pitta | 62 | 22 |
| 10 | `suncuc1` | *Cuculus lepidus* | Kangkok sunda / Sunda Cuckoo | 42 | 22 |
| 11 | `savnig1` | *Caprimulgus affinis* | Cabak kota / Savanna Nightjar | 31 | 20 |
| 12 | `hacdro1` | *Dicrurus hottentottus* | Srigunting rambut / Hair-crested Drongo | 91 | 19 |
| 13 | `subwar1` | *Horornis vulcanius* | Kerakbasi sunda / Sunda Bush Warbler | 48 | 19 |
| 14 | `gpipig1` | *Ducula aenea* | Pergam hijau / Green Imperial Pigeon | 45 | 19 |
| 15 | `whbsho1` | *Brachypteryx montana* | Cingcoang alis-putih / White-browed Shortwing | 40 | 19 |
| 16 | `ghcfly1` | *Culicicapa ceylonensis* | Sikatan kepala-kelabu / Grey-headed Canary-flycatcher | 38 | 19 |
| 17 | `comior1` | *Aegithina tiphia* | Cipoh kacat / Common Iora | 39 | 18 |
| 18 | `crseag1` | *Spilornis cheela* | Elang-ular bido / Crested Serpent Eagle | 35 | 15 |
| 19 | `ashtai1` | *Orthotomus ruficeps* | Cinenen kelabu / Ashy Tailorbird | 30 | 15 |
| 20 | `colkin1` | *Todiramphus chloris* | Cekakak sungai / Collared Kingfisher | 40 | 14 |
| **Total** | **20 Spesies** | | | **1.216 Klip** | **111 nilai nama / 112 orang setelah pemisahan nama gabungan** |

#### Distribusi Partisi Dataset Split (`data/manifests/dataset_split.csv`):
* **Galeri (*Gallery Set*):** 673 rekaman (59 perekam independen).
* **Kueri Bersih (*Query Clean*):** 311 rekaman (27 perekam independen / 28 setelah nama gabungan dipecah).
* **Subset Kalibrasi (*Calibration*):** 232 rekaman (25 perekam independen).
* **Integritas Bebas Bocor:** **Strict Global Author-Disjoint** (0 perekam beririsan antar Galeri, Kueri, dan Kalibrasi; 0 tumpang tindih ID rekaman maupun file path).

#### Subset Negatif Open-Set (`data/manifests/unknown_open_set_manifest.csv`):
* Total 543 rekaman kontrol negatif:
  * 272 rekaman kontrol burung non-target (dipilih secara ketat dari 380 kandidat buffer taksa non-target pada 105 spesies Indonesia untuk menjaga rasio kuota 1:1; 108 berkas sisanya adalah buffer cadangan).
  * 271 rekaman derau lingkungan murni AudioMoth ITERA.
* Dipartisi menjadi 233 rekaman untuk `unknown_calibration` dan 310 rekaman untuk `unknown_test`.

---

## 2. Bank Derau Fisik AudioMoth ITERA (1.799 Berkas WAV)
Bank derau lingkungan fisik ITERA berlokasi di `data/itera_noise/` dengan catatan manifes di `data/manifests/itera_noise_manifest.csv`:
* **Total Berkas Fisik:** Tepat 1.799 berkas audio WAV.
* **Partisi Non-Overlap:**
  * **1.528 berkas** untuk pencampuran derau aditif terkontrol (E2 dan E4).
  * **271 berkas** khusus dialokasikan untuk kontrol negatif kelas terbuka E3.
* **Penolakan Derau Senyap:** Penolakan keras segmen $\text{RMS} < 10^{-4}$.
* **Zero Synthetic Noise:** Fallback pink noise dihapus permanen.

---

## 3. Parameter Pra-pemrosesan Audio (Dibekukan)
* Laju Sampel (*Sample Rate*): **32.000 Hz** (mono).
* Durasi Segmen: **5.0 detik** (160.000 sampel).
* Seleksi Jendela: **Energi RMS tertinggi (*Top-energy sliding window*)** dengan hop 1.25s. Ini heuristik pemilihan segmen, bukan anotasi vokalisasi; gangguan non-burung yang keras juga dapat terpilih. Audit teknis tidak disamakan dengan verifikasi pendengaran manusia.
* Normalisasi Energi: **RMS target 0.05** dengan pembatasan puncak kliping $\le 1.0$.

---

## 4. Tingkat Degradasi Derau Terkontrol (Dibekukan)
Tingkat degradasi derau aditif dibekukan pada 5 level:
1. **Clean** (SNR = $\infty$)
2. **SNR +20 dB** (Derau ringan)
3. **SNR +10 dB** (Derau sedang)
4. **SNR 0 dB** (Derau berat)
5. **SNR -5 dB** (Derau ekstrem)

---

## 5. Catatan Historis Ruang Lingkup
* **Versi 4.0 (10 Oktober 2026):** Avifauna Kepulauan Indonesia (20 spesies, 1.216 rekaman terverifikasi dari Xeno-Canto, derau fisik ITERA 1.799 berkas). Hasil lama BirdCLEF diarsipkan di `results/archive/birdclef_2026/`.
* **Versi 3.0 (12 September 2026):** 20 taksa BirdCLEF Neotropis (dibatalkan per arahan pembimbing 10 Oktober 2026).
* **Versi 2.0 (07 September 2026):** 16 taksa burung Sumatera lama (dibatalkan akibat kelangkaan data kueri independen dan kebocoran author).
* **Versi 1.0 (Draf Awal):** 16 spesies kosmopolitan umum.

## Amendemen Scope 12 Oktober 2026 — riwayat sebelum revisi pembimbing

E4 dibatasi sebagai sensitivitas profil noise lokasi ITERA dalam additive mixture. H3 diuji sebagai stabilitas retensi lintas lima profil noise lokasi, bukan real-soundscape domain shift. Bank noise ITERA bebas spesies target; anotasi spesies target tidak diminta untuk E2/E4. Lihat `scope-reframe-2026-10-12.md`.


## Penjelasan aktif 16 Oktober 2026

Scope E4 tetap pencampuran aditif lima lokasi × empat SNR × empat ulangan atas 311 query per representasi. E4 tidak dijalankan ulang. Kesimpulan retensi saja pada catatan 12 Oktober telah diperluas oleh [revisi 15 Oktober](scope-reframe-2026-10-12.md) dengan ayunan absolut dan sensitivitas tanpa Kebun Raya. H3/H4 hasil reformulasi eksploratif; H3 asli mengenai real-soundscape belum diuji.

Bank AudioMoth mencakup enam kategori konfigurasi (Amplitude/Frequency × Low/Medium/High), bukan satu konfigurasi atau enam unit perangkat yang jumlahnya sudah dibuktikan. Label verified_bird_free pada manifes adalah metadata sumber, bukan bukti tersedianya audit pendengaran independen untuk seluruh berkas. Anotasi korpus burung in-situ tetap di luar scope E4 aktif.

Pemeriksaan baru menyiapkan klip E5 dan reproduksi pada lingkungan terisolasi. Semua keluarannya dicatat terpisah dari artefak beku; parameter di atas, audio sumber, serta identitas E4 tidak diubah.
