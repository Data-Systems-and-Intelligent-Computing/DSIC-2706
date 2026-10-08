from pathlib import Path

BASE = Path("D:/FILE AND TASK/TA")

# 1. Rencana-eksperimen-bimbingan/minggu-1/README.md
m1_content = """# Rencana Eksperimen — Minggu 1 (GATE 1-R)
**Fokus:** Dataset BirdCLEF+ 2026 (20 Spesies Target), Strict Global Recordist-Disjoint Partition, Standardisasi Audio, EDA, E0 (Pipeline Sanity Check), dan E1 (Clean Retrieval Benchmark).  
**Target Garis Waktu:** Minggu Ke-1  
**Status Eksekusi:** **SELESAI & LULUS 100% (Verifikasi Audit Gate 1-R — 12 September 2026)**

---

## 1. Pembekuan Target Burung, Manifes, & Preprocessing (DEC-09 & DEC-10)

Sesuai arahan Audit Keputusan Kedua tanggal 12 September 2026, eksperimen beralih dari korpus awal 14 spesies manual ke korpus **BirdCLEF+ 2026** guna menjamin daya statistik ($n=200$ kueri bersih) dan independensi rekaman:

* **Spesies Terpilih:** **20 spesies burung Neotropis** (total 4.351 berkas audio fisik) yang lolos seleksi objektif §11.3 (koleksi Xeno-Canto, Aves, rating $\\ge 3.0$, klip $\\ge 20$, author $\\ge 3$). Dari pool 156 kandidat yang lolos ambang, 20 spesies dipilih berdasarkan diversitas perekam tertinggi ($n_{\\text{author}} \\ge 105$).
* **Transparansi Eksklusi:** 136 spesies kandidat tersisih murni karena kuota 20 taksa, dan 50 spesies tersisih karena kriteria substantif (§11.3), seluruhnya tercatat di `species_excluded.csv`.
* **Parameter Preprocessing Dibekukan:**
  * Sample Rate: **32.000 Hz** (Mono)
  * Durasi Potongan Segmen: **5.0 detik** (160.000 sampel pada jendela energi tertinggi)
  * Normalisasi: RMS Energy Normalization (`target_rms = 0.05`)
  * Transformasi Waktu-Frekuensi: $N_{\\text{FFT}} = 1024$, $\\text{hop\\_length} = 512$
* **Berkas Manifes Kanonikal:**
  * Manifes Spesies Target: [`data/manifests/species_freeze.csv`](../../data/manifests/species_freeze.csv)
  * Manifes Spesies Tereksklusi: [`data/manifests/species_excluded.csv`](../../data/manifests/species_excluded.csv)
  * Manifes Split Bebas Bocor: [`data/manifests/dataset_split.csv`](../../data/manifests/dataset_split.csv)
  * Manifes Inventaris BirdCLEF: [`data/manifests/birdclef_inventory.json`](../../data/manifests/birdclef_inventory.json)

---

## 2. Partisi Data Strict Global Recordist-Disjoint (Zero Leakage)

Untuk menjamin evaluasi tidak terdistorsi oleh kesamaan karakteristik perekam (*recorder bias*), pembagian data dilakukan berbasis pengacakan author unik secara global (`seed=42`):

$$\\mathcal{R}_{\\text{Gallery}} \\cap \\mathcal{R}_{\\text{Query}} = \\emptyset, \\quad \\mathcal{R}_{\\text{Gallery}} \\cap \\mathcal{R}_{\\text{Calibration}} = \\emptyset, \\quad \\mathcal{R}_{\\text{Query}} \\cap \\mathcal{R}_{\\text{Calibration}} = \\emptyset$$

* **Gallery:** 3.653 rekaman audio dari **377 perekam (*author*) unik**
* **Query Clean:** 200 rekaman audio bersih dari **68 perekam (*author*) unik** (tepat 10 klip per spesies)
* **Calibration:** 498 rekaman audio dari **95 perekam (*author*) unik**
* **Integritas:** Diverifikasi otomatis oleh `tests/test_split_leakage.py` dan `tests/integration/test_split_leakage.py` dengan hasil **0 author overlap, 0 recording ID overlap, dan 0 file path overlap**.

---

## 3. Implementasi Representasi Audio (R0, R1, R2, R3)

Empat representasi audio dievaluasi dengan ekstraksi fitur berdimensi asli dan dinormalisasi L2 unit ($\\|\\mathbf{x}\\|_2 = 1.0$):
1. **$R_0$ (MFCC Baseline):** 40 koefisien spektral + pooling rata-rata/standar deviasi (40-dim).
2. **$R_1$ (Generic Pretrained):** PANNs CNN14 pretrained AudioSet (2048-dim).
3. **$R_2$ (Bioacoustic Domain-Specific):** BirdNET V2.4 Backbone (1024-dim).
4. **$R_3$ (Random Control):** Vektor acak terdistribusi seragam (40-dim, `seed=42`).

Metrik kesamaan dihitung menggunakan **Cosine Similarity** murni.

---

## 4. Hasil Evaluasi Empiris Gate 1-R (Kanonikal & Terverifikasi)

Hasil evaluasi E1 Clean Retrieval Benchmark pada 200 kueri bersih terhadap 3.653 galeri rekaman (tercatat di `results/processed/clean_retrieval_table.csv` dan `paper/tables/clean_retrieval_table.csv`):

| Kode | Representasi | Dimensi | Top-1 Accuracy (%) | mAP@10 | MRR | Recall@10 | Precision@10 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$** | **BirdNET Backbone** | 1024-d | **95.0%** | **0.9126** | **0.9658** | **0.0528** | **0.9280** |
| **$R_1$** | **PANNs CNN14** | 2048-d | **60.0%** | **0.4152** | **0.7005** | **0.0291** | **0.5025** |
| **$R_0$** | **MFCC Baseline** | 40-d | **27.5%** | **0.1319** | **0.4224** | **0.0123** | **0.2175** |
| **$R_3$** | **Random Control** | 40-d | **6.5%** | **0.0190** | **0.1779** | **0.0028** | **0.0530** |

### Analisis Temuan Ilmiah:
1. **Validasi Hipotesis H5 (Kontrol Negatif):** Model terlatih jauh melampaui tebakan acak. Akurasi Top-1 $R_3$ (6.5%) mendekati probabilitas acak teoretis $1/20 = 5.0\\%$, membuktikan ketiadaan kebocoran atau jalan pintas (*shortcut learning*).
2. **Hierarki Representasi Bersih:** $R_2\\text{ (BirdNET 95.0\\%)} > R_1\\text{ (PANNs 60.0\\%)} > R_0\\text{ (MFCC 27.5\\%)} \\gg R_3\\text{ (Random 6.5\\%)}$.
3. **Pencatatan Per-Kueri (Audit H5.2):** Berkas [`results/processed/per_query_clean_retrieval.csv`](../../results/processed/per_query_clean_retrieval.csv) menyimpan 800 baris rekaman rinci per kueri lengkap dengan kolom `author`, `top1_match`, `max_similarity`, `P@10`, `R@10`, dan `AP@10`.

---

## 5. Notebook Resmi Gate 1-R di `notebooks/`

Direktori `notebooks/` saat ini hanya memuat 4 berkas kanonikal:
1. `notebooks/EDA_Tugas_Akhir.ipynb` — Analisis eksplorasi data & verifikasi kriteria seleksi §11.3.
2. `notebooks/Preprocessing Verification.ipynb` — Validasi pemotongan sinyal 5s dan normalisasi RMS.
3. `notebooks/E0_Pipeline_Sanity_Check.ipynb` — Gerbang anti-kebocoran data dan *smoke test* 4 representasi.
4. `notebooks/E1_Clean_Retrieval.ipynb` — Ekstraksi embedding lengkap dan tolok ukur *clean retrieval*.

*Catatan Pengarsipan:* Seluruh berkas notebook dan tabel eksperimen 14 spesies Sumatra lama telah diarsipkan secara aman di `results/archive/2026-09-07_xenocanto16spesies/`.

---

## 6. Daftar 20 Spesies Target Resmi (`species_freeze.csv`)

| No | Kode Spesies | Nama Ilmiah | Nama Umum | Jumlah Klip | Jumlah Author Unik |
|:---:|:---|:---|:---|:---:|:---:|
| 1 | `coffal1` | *Micrastur semitorquatus* | Collared Forest-Falcon | 253 | 129 |
| 2 | `sobtyr1` | *Camptostoma obsoletum* | Southern Beardless Tyrannulet | 331 | 126 |
| 3 | `greant1` | *Taraba major* | Great Antshrike | 337 | 124 |
| 4 | `squcuc1` | *Piaya cayana* | Common Squirrel-Cuckoo | 332 | 123 |
| 5 | `roahaw` | *Rupornis magnirostris* | Roadside Hawk | 243 | 122 |
| 6 | `trsowl` | *Megascops choliba* | Tropical Screech Owl | 234 | 122 |
| 7 | `banana` | *Coereba flaveola* | Bananaquit | 301 | 121 |
| 8 | `baffal1` | *Micrastur ruficollis* | Barred Forest-Falcon | 273 | 121 |
| 9 | `soulap1` | *Vanellus chilensis* | Southern Lapwing | 243 | 120 |
| 10 | `strcuc1` | *Tapera naevia* | Striped Cuckoo | 250 | 117 |
| 11 | `pabspi1` | *Synallaxis albescens* | Pale-breasted Spinetail | 214 | 117 |
| 12 | `yeofly1` | *Tolmomyias sulphurescens* | Yellow-olive Flatbill | 393 | 115 |
| 13 | `gycwor1` | *Aramides cajaneus* | Grey-cowled Wood Rail | 219 | 115 |
| 14 | `compau` | *Nyctidromus albicollis* | Pauraque | 206 | 115 |
| 15 | `barant1` | *Thamnophilus doliatus* | Barred Antshrike | 294 | 114 |
| 16 | `pirfly1` | *Legatus leucophaius* | Piratic Flycatcher | 288 | 114 |
| 17 | `linwoo1` | *Dryocopus lineatus* | Lineated Woodpecker | 254 | 113 |
| 18 | `whtdov` | *Leptotila verreauxi* | White-tipped Dove | 269 | 111 |
| 19 | `bobfly1` | *Megarynchus pitangua* | Boat-billed Flycatcher | 272 | 107 |
| 20 | `trokin` | *Tyrannus melancholicus* | Tropical Kingbird | 220 | 105 |
"""

(BASE / "Rencana-eksperimen-bimbingan/minggu-1/README.md").write_text(m1_content, encoding="utf-8")
print("[+] Updated: Rencana-eksperimen-bimbingan/minggu-1/README.md")

# 2. Rencana-eksperimen-bimbingan/minggu-2/README.md
m2_content = """# Rencana Eksperimen — Minggu 2 (GATE 2)
**Fokus:** Akuisisi Data Lapangan AudioMoth ITERA & Controlled Noise Robustness (Paired SNR Stress-Testing)  
**Target Garis Waktu:** Minggu Ke-2 (H8–H14)  
**Status Eksekusi:** **TERJADWAL / BELUM DILAKUKAN (Menunggu Perekaman Fisik Lapangan AudioMoth)**  

---

## 1. Perekaman Fisik AudioMoth di Kampus ITERA (H8–H13)
* **Status Lapangan:** **Belum Dilakukan**. Unit AudioMoth dijadwalkan dipasang di kampus ITERA pada Minggu 2.
* **Titik Penempatan:**
  1. *Titik Vegetasi/Embung:* Ambien alam, biophony serangga/jangkrik, gemerisik dedaunan, dan angin.
  2. *Titik Antropogenik:* Dekat koridor gedung/jalan kampus untuk menangkap derau aktivitas manusia dan kendaraan.
* **Konfigurasi AudioMoth:** Sample rate 32.000 Hz, gain medium, interval perekaman kontinu/berkala. Salinan berkas `CONFIG.TXT` wajib disimpan di repositori.
* **Kurasi Segmen Derau Murni (H13):** Memotong segmen 5,0 detik yang dipastikan **bebas dari suara burung target korpus** dan menyimpannya di `data/itera_noise/`.
* **Pembersihan Jalur Derau Sintetis:** Sesuai mandat DEC-09, derau sintetis (*pink noise*) ditinggalkan seutuhnya. Fungsi cadangan pada `src/mix_noise.py` akan diubah menjadi galat fatal (`raise FileNotFoundError`) saat data AudioMoth dimasukkan.

---

## 2. Eksperimen E2: Evaluasi Temu Kembali di Bawah Derau (H11–H13)
* **Kueri Terpasang:** 200 kueri bersih dari E1 dicampur dengan segmen derau AudioMoth yang sama menggunakan seed tetap (`seed=42`).
* **Grid SNR Terkontrol:**
  1. *Clean:* Kondisi dasar tanpa derau (baseline E1)
  2. *SNR +20 dB:* Derau latar sangat ringan
  3. *SNR +10 dB:* Derau latar sedang
  4. *SNR 0 dB:* Daya sinyal dan derau berimbang
  5. *SNR -5 dB:* Derau dominan terhadap sinyal vokal
* **Formulasi Pencampuran Eksak:**
  $$x_{\\text{noisy}} = x_{\\text{clean}} + \\alpha \\cdot n_{\\text{noise}}, \\quad \\alpha = \\sqrt{\\frac{P_{\\text{signal}}}{P_{\\text{noise}} \\cdot 10^{\\text{SNR}/10}}}$$
* **Model yang Dievaluasi:**
  * $R_0$: MFCC Baseline (40-dim)
  * $R_1$: PANNs CNN14 Generic Audio (2048-dim)
  * $R_2$: BirdNET Backbone Bioacoustic (1024-dim)
  * $R_3$: Random Control (40-dim)

---

## 3. Kriteria Kelulusan Gate 2 (H14)
- [ ] Bank derau `data/itera_noise/` terisi audio rekaman nyata AudioMoth dan lolos verifikasi ketiadaan burung target.
- [ ] Manifes `data/manifests/itera_noise_manifest.csv` terisi lengkap dan di-checksum SHA-256.
- [ ] Fallback pink noise di `src/mix_noise.py` dihapus.
- [ ] Pemasangan kueri ke segmen derau bersifat deterministik.
- [ ] Kurva degradasi $mAP@10$ dan retensi relatif terhadap SNR dihasilkan tanpa artefak *ceiling*/*floor*.
- [ ] Seluruh log pemeringkatan per-kueri mentah tersimpan secara terstruktur di `results/raw/`.
"""

(BASE / "Rencana-eksperimen-bimbingan/minggu-2/README.md").write_text(m2_content, encoding="utf-8")
print("[+] Updated: Rencana-eksperimen-bimbingan/minggu-2/README.md")

# 3. docs/README.md
docs_content = """# Dokumentasi Metodologi & Riset Tugas Akhir (DSIC-2706)
**Topik:** Mencari Audio yang Mirip Ketika Datanya Terbatas  
**Judul Kerja:** *Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise*  
**Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)  
**Dosen Pembimbing:** Bapak Ardika  
**Institusi:** Program Studi Sains Data, Institut Teknologi Sumatera (ITERA)  
**Status Terkini:** Revisi Audit Gate 1-R Selesai 100% (12 September 2026)  

---

## 1. Ringkasan Eksekutif Riset

Penelitian ini mengevaluasi **ketahanan representasi audio beku (*frozen representations*) untuk temu kembali kemiripan (*similarity retrieval*)** ketika kueri bioakustik mengalami penurunan kualitas akibat derau lingkungan tropis dan pergeseran domain:

* **Representasi Audio yang Dibandingkan:**
  * $R_0$: MFCC Baseline (40-dim, *handcrafted acoustic*)
  * $R_1$: PANNs CNN14 (2048-dim, *generic deep audio embedding*)
  * $R_2$: BirdNET V2.4 Backbone (1024-dim, *domain-specific bioacoustic representation*)
  * $R_3$: Random Control (40-dim, *negative control baseline*)
* **Korpus Galeri & Kueri (DEC-09 / Gate 1-R):** Menggunakan subset terkurasi **BirdCLEF+ 2026** lintas 20 spesies burung Neotropis (total 4.351 berkas audio fisik) dengan pembagian *Strict Global Recordist-Disjoint*:
  * Galeri: 3.653 rekaman audio (377 perekam unik)
  * Kueri Bersih: 200 rekaman audio (68 perekam unik, 10 klip/spesies)
  * Kalibrasi Open-Set: 498 rekaman audio (95 perekam unik)
* **Derau Lapangan Terkontrol:** Menggunakan rekaman langsung perangkat **AudioMoth** dari kampus ITERA (`data/itera_noise/`), derau sintetis pink noise ditinggalkan sepenuhnya. *(Catatan: Perekaman fisik AudioMoth dijadwalkan pada Minggu 2 / H8–H14).*
* **Hasil Tolok Ukur Bersih E1:** $R_2\\text{ (BirdNET 95.0\\%)} > R_1\\text{ (PANNs 60.0\\%)} > R_0\\text{ (MFCC 27.5\\%)} \\gg R_3\\text{ (Random 6.5\\%)}$.
* **Integritas Suite Uji:** Seluruh 9 unit test saintifik pada `run_tests.py` lulus 100.0%.

---

## 2. Indeks Dokumen Penelitian di `docs/`

### A. Kebijakan, Ruang Lingkup, & Batasan Ilmiah (`docs/research/`)
1. [`research-charter.md`](./research/research-charter.md) — Piagam penelitian, batasan masalah, dan tujuan utama.
2. [`rq.md`](./research/rq.md) — Rincian Pertanyaan Penelitian (RQ Utama dan Sub-RQ).
3. [`hypotheses.md`](./research/hypotheses.md) — 5 Hipotesis kerja ilmiah ($H_1$ s.d. $H_5$).
4. [`novelty-boundary.md`](./research/novelty-boundary.md) — Batasan kebaruan dan kontribusi ilmiah spesifik.
5. [`scope-freeze.md`](./research/scope-freeze.md) — Pembekuan ruang lingkup korpus Versi 3.0 (BirdCLEF+ 2026, 20 taksa beku).
6. [`decision-log.md`](./research/decision-log.md) — Register keputusan formal riset (DEC-01 hingga DEC-10).

### B. Protokol Metodologis & Pengujian (`docs/protocols/`)
1. [`itera-recording.md`](./protocols/itera-recording.md) — Panduan penempatan, konfigurasi, dan kurasi derau AudioMoth ITERA.
2. [`open-set.md`](./protocols/open-set.md) — Prosedur kalibrasi ambang batas $\\tau^*$ menggunakan Youden's J pada target FAR 5% dan 10%.
3. [`birdclef-license.md`](./protocols/birdclef-license.md) — Klausul kepatuhan lisensi kompetisi BirdCLEF untuk penggunaan akademik dan skripsi.
4. [`annotation.md`](./protocols/annotation.md) — Standar anotasi rekaman bentang suara (*soundscapes*).
5. [`xeno-canto-selection.md`](./protocols/xeno-canto-selection.md) — Kriteria awal penyaringan rekaman audio.

---

## 3. Rekam Jejak Pelaksanaan & Logbook

Seluruh rekam jejak revisi bimbingan, matriks audit, log eksekusi terminal, dan data numerik empiris tercatat lengkap dan transparan pada:  
👉 **[`Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md`](../Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md)**
"""

(BASE / "docs/README.md").write_text(docs_content, encoding="utf-8")
print("[+] Updated: docs/README.md")

# 4. experiments/E0_pipeline_sanity/README.md
e0_content = """# Eksperimen E0 — Pipeline Sanity Check

## 1. Tujuan Ilmiah
Memvalidasi keutuhan jalur pipa komputasi (*pipeline sanity*), memverifikasi ketiadaan kebocoran data (*split leakage*), memastikan stabilitas dimensi fitur serta normalisasi representasi audio (R0, R1, R2, R3), dan menguji hipotesis kontrol negatif H5 sebelum eksperimen skala penuh dijalankan.

## 2. Masukan & Parameter
* **Manifes Data:** `data/manifests/dataset_split.csv` (4.351 baris: 3.653 galeri, 200 kueri bersih, 498 kalibrasi).
* **Standar Audio:** Laju sampel 32.000 Hz, jendela 5.0 detik (160.000 sampel), mono, normalisasi RMS = 0.05.
* **Audio Smoke Test:** Berkas nyata `XC1053050.ogg`.

## 3. Eksekusi Kanonikal
* **Notebook:** [`notebooks/E0_Pipeline_Sanity_Check.ipynb`](../../notebooks/E0_Pipeline_Sanity_Check.ipynb)
* **Gerbang Asersi Anti-Bocor:**
  * 0 author overlap antara galeri, kueri bersih, dan kalibrasi (100% *Strict Global Recordist-Disjoint*).
  * 0 recording ID overlap dan 0 file path overlap.
  * Uji kebocoran melempar `AssertionError` jika ada irisan data sekecil apa pun.
* **Smoke Test Dimensi:** R0=(40,), R1=(2048,), R2=(1024,), R3=(40,), seluruhnya bernorma $L_2 = 1.0$ dan bebas NaN/Inf.
* **Verifikasi Kontrol Negatif H5 (Subset 20 Kueri vs 100 Galeri):**
  * $R_2$ (BirdNET): 85.0%
  * $R_1$ (PANNs): 40.0%
  * $R_0$ (MFCC): 5.0%
  * $R_3$ (Random Control): 10.0%

## 4. Status Kelulusan
**LULUS 100% (Gate 1-R)**. Seluruh kriteria dipenuhi tanpa peringatan galat.
"""

(BASE / "experiments/E0_pipeline_sanity/README.md").write_text(e0_content, encoding="utf-8")
print("[+] Updated: experiments/E0_pipeline_sanity/README.md")

# 5. experiments/E1_clean_retrieval/README.md
e1_content = """# Eksperimen E1 — Clean Retrieval Benchmark

## 1. Tujuan Ilmiah
Membangun tolok ukur dasar (*clean baseline*) kemampuan perolehan kemiripan (*similarity retrieval*) dari representasi audio terstandardisasi pada kondisi ideal (rekaman bersih bebas derau tambahan) lintas 20 spesies burung target korpus BirdCLEF+ 2026.

## 2. Konfigurasi Eksperimen
* **Data Uji:** 200 kueri bersih (tepat 10 kueri per spesies dari 68 perekam independen).
* **Data Referensi (Gallery):** 3.653 rekaman galeri dari 377 perekam independen.
* **Representasi:**
  * $R_0$: MFCC Baseline (40-dim)
  * $R_1$: PANNs CNN14 (2048-dim)
  * $R_2$: BirdNET Backbone (1024-dim)
  * $R_3$: Random Control (40-dim)
* **Metrik Kesamaan:** Cosine Similarity ($200 \\times 3.653$ pairwise similarity matrix).

## 3. Eksekusi & Hasil Kanonikal
* **Notebook:** [`notebooks/E1_Clean_Retrieval.ipynb`](../../notebooks/E1_Clean_Retrieval.ipynb)
* **Tabel Hasil Resmi (`results/processed/clean_retrieval_table.csv`):**

| Representasi | Top-1 Accuracy (%) | mAP@10 | MRR | Precision@10 | Recall@10 |
|---|:---:|:---:|:---:|:---:|:---:|
| **$R_2$: BirdNET Backbone (1024-d)** | **95.0%** | **0.9126** | **0.9658** | **0.9280** | **0.0528** |
| **$R_1$: PANNs CNN14 (2048-d)** | **60.0%** | **0.4152** | **0.7005** | **0.5025** | **0.0291** |
| **$R_0$: MFCC Baseline (40-d)** | **27.5%** | **0.1319** | **0.4224** | **0.2175** | **0.0123** |
| **$R_3$: Random Control (40-d)** | **6.5%** | **0.0190** | **0.1779** | **0.0530** | **0.0028** |

* **Log Granular (Audit H5.2):** Tersimpan di [`results/processed/per_query_clean_retrieval.csv`](../../results/processed/per_query_clean_retrieval.csv) (800 baris memuat kolom `author`, `top1_match`, `max_similarity`, `P@10`, `R@10`, `AP@10`).
* **Visualisasi:** Tersimpan di [`results/figures/clean_retrieval_benchmark.png`](../../results/figures/clean_retrieval_benchmark.png).

## 4. Status Kelulusan
**LULUS 100% (Gate 1-R)**.
"""

(BASE / "experiments/E1_clean_retrieval/README.md").write_text(e1_content, encoding="utf-8")
print("[+] Updated: experiments/E1_clean_retrieval/README.md")

# 6. experiments/E2_noise_robustness/README.md
e2_content = """# Eksperimen E2 — Controlled Noise Robustness

## 1. Tujuan Ilmiah
Menguji ketahanan (*robustness*) representasi audio ketika kueri bersih mengalami degradasi derau lingkungan tropis nyata pada berbagai tingkatan SNR (+20 dB, +10 dB, 0 dB, -5 dB).

## 2. Sumber Derau & Penghapusan Derau Sintetis
* Sesuai keputusan audit **DEC-09**, derau sintetis pink noise ditinggalkan seutuhnya.
* Menggunakan rekaman suara lingkungan murni (*ambient soundscape*) dari kampus ITERA yang direkam menggunakan perangkat **AudioMoth** (`data/itera_noise/`).
* *Catatan Lapangan:* Perekaman fisik AudioMoth di kampus ITERA dijadwalkan pada Minggu 2 (H8–H14).

## 3. Skema Pengujian Terpasang (*Paired Noise Mixing*)
* 200 kueri bersih yang sama dari E1 dipasangkan secara deterministik (`seed=42`) dengan segmen derau AudioMoth.
* Formula pencampuran berbasis daya sinyal eksak:
  $$x_{\\text{noisy}} = x_{\\text{clean}} + \\alpha \\cdot n_{\\text{noise}}, \\quad \\alpha = \\sqrt{\\frac{P_{\\text{signal}}}{P_{\\text{noise}} \\cdot 10^{\\text{SNR}/10}}}$$

## 4. Status Pelaksanaan
**TERJADWAL / BELUM DILAKUKAN** (Tahap Minggu 2 / H8–H14).
"""

(BASE / "experiments/E2_noise_robustness/README.md").write_text(e2_content, encoding="utf-8")
print("[+] Updated: experiments/E2_noise_robustness/README.md")
