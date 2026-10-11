# Dokumentasi Metodologi & Riset Tugas Akhir (DSIC-2706)
**Topik:** Mencari Audio yang Mirip Ketika Datanya Terbatas  
**Judul Kerja:** *Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on Indonesian Avifauna with Field-Recorded ITERA Tropical Noise*  
**Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)  
**Dosen Pembimbing:** Bapak Ardika Satria  
**Institusi:** Program Studi Sains Data, Institut Teknologi Sumatera (ITERA)  
**Status Terkini:** Seluruh Eksperimen E0 s.d. E5 Selesai 100% pada Korpus Avifauna Indonesia  

---

## 1. Ringkasan Eksekutif Riset

Penelitian ini mengevaluasi **ketahanan representasi audio beku (*frozen representations*) untuk temu kembali kemiripan (*similarity retrieval*)** ketika kueri bioakustik mengalami penurunan kualitas akibat derau lingkungan tropis nyata:

* **Representasi Audio yang Dibandingkan:**
  * $R_0$: MFCC Baseline (40-dim, *handcrafted acoustic*)
  * $R_1$: PANNs CNN14 (2048-dim, *generic deep audio embedding*)
  * $R_2$: BirdNET V2.4 Backbone (1024-dim, *domain-specific bioacoustic representation*)
  * $R_3$: Random Control (40-dim, *negative control baseline*)
* **Korpus Galeri & Kueri (Avifauna Indonesia):** Menggunakan 20 spesies burung Indonesia umum dan tersebar luas dari Xeno-Canto (total 1.217 berkas audio fisik terverifikasi) dengan pembagian *Strict Global Recordist-Disjoint*:
  * Galeri: 674 rekaman audio (60 perekam unik)
  * Kueri Bersih: 310 rekaman audio (31 perekam unik)
  * Kalibrasi Open-Set: 233 rekaman audio (20 perekam unik)
  * Kontrol Negatif Terbuka: 543 rekaman (272 non-bird / non-target + 271 derau ITERA)
* **Derau Lapangan Fisik AudioMoth:** Menggunakan 1.799 berkas audio WAV fisik dari 5 lokasi kampus ITERA (`data/itera_noise/`), bebas pink noise sintetis. Dipartisi 1.528 berkas untuk mixing (E2/E4) dan 271 berkas untuk kontrol negatif E3.
* **Hasil Tolok Ukur Bersih E1:** $R_2\text{ (BirdNET 81.61\%)} > R_1\text{ (PANNs 37.74\%)} > R_0\text{ (MFCC 18.06\%)} \gg R_3\text{ (Random 6.77\%)}$.
* **Ketahanan Derau Ekstrem E2 (-5 dB):** Retensi relatif $R_2\text{ (78.0\%)} > R_1\text{ (55.5\%)} > R_0\text{ (35.7\%)}$.
* **Integritas Suite Uji:** Seluruh 10 unit test saintifik pada `run_tests.py` lulus 100.0%.

---

## 2. Indeks Dokumen Penelitian di `docs/`

### A. Kebijakan, Ruang Lingkup, & Batasan Ilmiah (`docs/research/`)
1. [`research-charter.md`](./research/research-charter.md) — Piagam penelitian, batasan masalah, dan tujuan utama.
2. [`rq.md`](./research/rq.md) — Rincian Pertanyaan Penelitian (RQ Utama dan Sub-RQ).
3. [`hypotheses.md`](./research/hypotheses.md) — 5 Hipotesis kerja ilmiah ($H_1$ s.d. $H_5$).
4. [`novelty-boundary.md`](./research/novelty-boundary.md) — Batasan kebaruan dan kontribusi ilmiah spesifik.
5. [`scope-freeze.md`](./research/scope-freeze.md) — Pembekuan ruang lingkup korpus Avifauna Indonesia (20 taksa beku, 1.217 klip).
6. [`decision-log.md`](./research/decision-log.md) — Register keputusan formal riset (DEC-01 hingga DEC-13).

### B. Protokol Metodologis & Pengujian (`docs/protocols/`)
1. [`itera-recording.md`](./protocols/itera-recording.md) — Panduan penempatan, konfigurasi, dan kurasi derau AudioMoth ITERA.
2. [`open-set.md`](./protocols/open-set.md) — Prosedur kalibrasi ambang batas $\tau^*$ menggunakan Youden's J.
3. [`annotation.md`](./protocols/annotation.md) — Standar anotasi rekaman dan penolakan derau senyap.

---

## 3. Rekam Jejak Pelaksanaan & Logbook

Seluruh rekam jejak revisi bimbingan, matriks audit, log eksekusi terminal, dan data numerik empiris tercatat lengkap dan transparan pada:  
👉 **[`Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md`](../Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md)**
