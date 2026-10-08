# Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise

**Fabio Banyu Cyto** (123450104)  
*DSIC Research Group, Program Studi Sains Data, Institut Teknologi Sumatera*  

**Status naskah (1 Oktober 2026):** rezim aktif adalah BirdCLEF+ 2026 (20 spesies, Gate 1-R). Angka empiris yang dilaporkan di sini hanya **E1 clean retrieval**. Eksperimen E2–E5 dan kurva retensi SNR **belum dijalankan** pada rezim ini; hasil Xeno-Canto 16 spesies Sumatera (mAP@10 $R_2$ = 0.5876, retensi −5 dB = 80.1%) telah diarsipkan dan **tidak** dipakai sebagai klaim aktif.

---

## Abstract
Passive acoustic monitoring generates large volumes of unannotated audio, but the robustness of frozen audio representations for similarity retrieval under environmental noise and domain shift is still poorly quantified. This study compares four frozen representations on a **BirdCLEF+ 2026** gallery of 20 avian taxa (4,351 clips): hand-crafted MFCC (40-d), generic PANNs CNN14 (2048-d), bioacoustic BirdNET V2.4 (1024-d), and a random-vector control (40-d). All embeddings are $\ell_2$-normalised and ranked by cosine similarity under a **strict global recordist-disjoint** split (gallery 3,653 / query 200 / calibration 498; zero author, recording-id, and filepath overlap).

On clean queries (**experiment E1**), BirdNET attains Top-1 accuracy **95.0%**, mAP@10 **0.9126**, and MRR **0.9658**, clearly above PANNs (60.0%, 0.4152, 0.7005), MFCC (27.5%, 0.1319, 0.4224), and random control (6.5%, 0.0190, 0.1779). Subsequent experiments will stress the **same 200 queries** with additive campus noise recorded on AudioMoth at ITERA (SNR grid 20, 10, 0, and −5 dB), then test frozen open-set thresholds and BirdCLEF `train_soundscapes` domain shift. Field noise is collected in **daytime only** (campus access does not permit night recording) using **two hardware trigger methods—frequency and amplitude—**so the mixing pipeline can select pre-tagged streams without extra digital band/level filtering.

**Keywords:** Bioacoustic Retrieval, Representation Robustness, Domain Shift, BirdCLEF+ 2026, AudioMoth, Open-Set Rejection, BirdNET.

---

## 1. Introduction
Pemantauan akustik pasif menghasilkan volume audio yang besar, tetapi sebagian besar evaluasi masih berfokus pada klasifikasi tertutup pada rekaman fokus yang relatif bersih. Pertanyaan penelitian ini berbeda: **representasi audio mana yang mempertahankan kualitas similarity retrieval ketika kueri yang sama diberi derau lingkungan dan kemudian diuji pada pergeseran domain soundscape?**

Kerangka biodiversitas Sumatera pada draf awal **dilepas** setelah audit Gate 1 (DEC-09, 12 September 2026). Korpus eksperimen utama kini adalah **BirdCLEF+ 2026** (`train_audio`, taksa *Aves* koleksi Xeno-Canto). Rekaman AudioMoth kampus ITERA **bukan** validasi kehadiran spesies, melainkan bank derau aditif (E2) dan negatif latar (E3).

## 2. Related Work
- Representasi parametrik: Davis & Mermelstein (1980).
- Embedding audio generik: Hershey et al. (2017); PANNs (Kong et al., 2020).
- Model bioakustik: BirdNET (Kahl et al., 2021); global birdsong embeddings (Ghani et al., 2023).
- Benchmark deteksi terbuka: Stowell et al. (2019); BIRB (Hamer et al., 2023); BirdSet (Rauch et al., 2025); BirdCLEF+.

## 3. Methodology

### 3.1 Problem formulation
Setiap klip $x$ dipetakan ke embedding beku $e = f(x)$ dengan $\|e\|_2 = 1$. Kemiripan kueri $q$ terhadap galeri $g$ adalah cosine:

$$
\mathrm{sim}(q,g) = e_q^\top e_g.
$$

Retensi berpasangan (akan dihitung pada E2) didefinisikan

$$
\mathrm{Retention}_m(\mathrm{SNR}) = \frac{\mathrm{Metric}_m(\mathrm{SNR})}{\mathrm{Metric}_m(\mathrm{clean})}.
$$

### 3.2 Dataset and split (rezim aktif)
Dua puluh spesies dipilih dari 156 kandidat yang memenuhi rating $\ge 3.0$, $\ge 20$ klip, dan $\ge 3$ perekam, dengan ranking $n_{\mathrm{author}}$ tertinggi (DEC-10). Korpus aktif: **4.351** berkas. Prapemrosesan dibekukan: 32 kHz, mono, jendela 5.0 s (160.000 sampel), RMS target 0.05.

Partisi `data/manifests/dataset_split.csv` (`seed=42`):

| Peran | Klip | Perekam unik |
|---|---:|---:|
| Gallery | 3.653 | 377 |
| Query clean | 200 (10 per spesies) | 68 |
| Calibration | 498 | 95 |

Irisan author, recording ID, dan filepath antar peran adalah **nol**, diverifikasi `tests/test_split_leakage.py`.

### 3.3 Representations
| Kode | Representasi | Dimensi | Peran |
|---|---|---:|---|
| $R_0$ | MFCC + mean/std pooling | 40 | baseline klasik |
| $R_1$ | PANNs CNN14 (AudioSet) | 2048 | embedding generik |
| $R_2$ | BirdNET V2.4 backbone (ONNX) | 1024 | embedding bioakustik |
| $R_3$ | vektor acak seragam (`seed=42`) | 40 | kontrol negatif |

Tanpa *fine-tuning*. Checkpoint wajib ada; tidak ada silent fallback (DEC-06 / C-01).

### 3.4 ITERA noise bank (E2/E3) — protokol lapangan
Peran rekaman ITERA dipersempit menjadi (i) derau aditif terkontrol dan (ii) negatif open-set *background-only*, **bukan** inventarisasi fauna kampus.

**Batasan akses (DEC-11).** Perekaman hanya diizinkan pada **siang hari**. Sesi malam tidak dilakukan. Kompensasi desain: keragaman lokasi, gain, dan *trigger method*, bukan keragaman daypart.

**Dua metode perangkat, bukan filter di kode (DEC-12).** Pembimbing mensyaratkan akuisisi **frequency trigger** dan **amplitude trigger** pada AudioMoth agar mixer E2 memilih berkas yang sudah bertanda metode di manifes, tanpa penyaringan digital tambahan (band-pass / *level gate*) di pipeline.

| Metode | Apa yang dilakukan perangkat | Status lapangan (1 Okt 2026) |
|---|---|---|
| Frequency | Merekam ketika energi pada pita/ambang frekuensi terpenuhi (konfigurasi Low / Medium / High Filter, 32 kHz) | **Sudah diambil** di lima lokasi, 18–30 September 2026 |
| Amplitude | Merekam ketika amplitudo/ambang level terpenuhi | **Belum diambil**; wajib sebelum main run E2 |

Lokasi frequency yang sudah tercatat: Masjid At-Tanwir, Embung E, Kebun Raya, Gedung F, dan sekitar GKU 1 (lihat `data/itera_noise/Notulensi Pengambilan Data Uji ITERA.txt`). Parameter sesi: rekam 55 s / jeda 5 s, gain Low–High. Segmen *bird-free* dan checksum belum dibekukan di `itera_noise_manifest.csv`.

Grid SNR kandidat (masih boleh disesuaikan pada pilot, lalu dibekukan): clean, 20 dB, 10 dB, 0 dB, −5 dB.

### 3.5 Open-set and domain shift (direncanakan)
Ambang $\tau$ dipilih **hanya** dari calibration (Youden $J$), lalu dibekukan. E3 menguji transfer $\tau$ pada unknown burung non-target, non-burung, dan latar ITERA. E4 menjalankan pipeline beku pada `train_soundscapes` BirdCLEF tanpa *re-tune* $\tau$.

## 4. Experimental results

### 4.1 E1 — clean retrieval (selesai, 12 September 2026)
Sumber: `results/processed/clean_retrieval_table.csv` dan `execution_note_E1.json` (`GATE1R_E1_CLEAN_RETRIEVAL`).

| Representasi | Top-1 (%) | mAP@10 | MRR | Precision@10 | Recall@10 |
|---|---:|---:|---:|---:|---:|
| $R_2$ BirdNET | **95.0** | **0.9126** | **0.9658** | **0.9280** | **0.0528** |
| $R_1$ PANNs | 60.0 | 0.4152 | 0.7005 | 0.5025 | 0.0291 |
| $R_0$ MFCC | 27.5 | 0.1319 | 0.4224 | 0.2175 | 0.0123 |
| $R_3$ Random | 6.5 | 0.0190 | 0.1779 | 0.0530 | 0.0028 |

Urutan $R_2 \gg R_1 \gg R_0 \gg R_3$ memenuhi kontrol positif: pipeline tidak setara dengan ranking acak.

**Catatan metrik Recall@10.** Galeri memuat ribuan klip relevan per spesies (orde $\sim 10^2$), sementara $k=10$. Plafon kasar Recall@10 $\approx 10/n_{\mathrm{gallery,spesies}}$. Nilai 0.0528 pada $R_2$ dekat plafon itu, **bukan** bukti retrieval lemah. Klaim peringkat mengandalkan Top-1, mAP@10, MRR, dan Precision@10.

### 4.2 E2–E5 — belum dijalankan pada rezim aktif
Kurva degradasi SNR, transfer ambang open-set, domain shift soundscape, dan audit kegagalan **tidak** dilaporkan sebagai hasil. Angka retensi lama (misalnya 80.1% pada −5 dB) berasal dari rezim Xeno-Canto yang diarsipkan di `results/archive/2026-09-07_xenocanto16spesies/` dan tidak boleh dikutip sebagai temuan BirdCLEF.

## 5. Planned failure analysis (E5)
Setelah E2 menghasilkan ranking per kueri, minimal 20 kasus *false accept* / *false reject* akan diaudit secara manual (bukan templat diagnosis). Kategori kerja: masking SNR rendah, tumpang tindih akustik, kebingungan antarspesies, derau antropogenik, dan event pendek.

## 6. Conclusion and threats to validity

### 6.1 What is supported now
Pada kueri bersih BirdCLEF, embedding bioakustik beku $R_2$ unggul atas embedding generik, MFCC, dan kontrol acak. Klaim **ketahanan terhadap derau tropis** menunggu E2 setelah bank amplitude dilengkapi dan manifes derau dibekukan.

### 6.2 Threats to validity
1. **Seleksi spesies:** 20 taksa adalah yang paling sering terekam (*conspicuous*), bukan sampel acak (DEC-10).
2. **Kontaminasi pralatih:** sebagian Xeno-Canto mungkin pernah masuk korpus latih BirdNET; keunggulan E1 pada split author-disjoint tetap informatif, tetapi generalisasi ke taksa baru terbatas.
3. **Daypart:** tidak ada rekaman malam; spektrum nokturnal (misalnya serangga/amfibi malam) tidak terwakili di bank derau.
4. **Trigger frequency vs amplitude:** bank saat ini hanya frequency; E2 belum boleh diklaim mewakili kedua metode sampai amplitude selesai.
5. **Derau aditif vs fisika lapangan:** pencampuran SNR tidak memodelkan reverberasi, jarak, dan panggilan tumpang tindih; itu peran E4.
6. **Kalibrasi open-set:** pada rezim aktif, gallery / query / calibration **tidak** berbagi author (ancaman 19 perekam bersama pada rezim Sumatera lama **tidak** berlaku di sini).

---

## References
Sinkron dengan `paper/bibliography/referensi_jurnal_modern.csv`.
