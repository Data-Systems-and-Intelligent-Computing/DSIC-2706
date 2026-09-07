# Rencana Eksperimen — Minggu 1
**Fokus:** Dataset, Manifest, Standarisasi Audio, dan Feasibility Pipeline  
**Target Garis Waktu:** Hari 1 – Hari 7  
**Status Eksekusi:** **SELESAI 100% (GATE MINGGU 1 PASSED)**  

---

## 🎯 Target Rencana & Hasil Eksekusi

### Hari 1–2: Pembekuan Target Burung, Manifes, & Preprocessing
* **Target Pembimbing:**
  * Bekukan target burung dan daftar 10–20 spesies.
  * Bangun manifes Xeno-Canto dan periksa atribusi lisensi (*Creative Commons*).
  * Bekukan preprocessing: sample rate dan segment length.
* **Hasil Eksekusi Riil:**
  * **Spesies Terpilih:** **16 spesies burung** (total 416 file audio) dengan rata-rata 26 rekaman per spesies.
  * **Catatan Transparansi:** Spesies *Oriolus chinensis* digantikan oleh *Aethopyga siparaja* ($N=26$) dan *Dicaeum trigonostigma* ($N=24$) karena Xeno-Canto v3 membatasi unduhan publik demi perlindungan satwa terancam perburuan liar (*poaching-sensitive*).
  * **Parameter Preprocessing Dibekukan:**
    * Sample Rate: **32.000 Hz** (Mono)
    * Durasi Potongan Segmen: **5.0 detik**
    * Transformasi Waktu-Frekuensi: $N_{\text{FFT}} = 1024$, $\text{hop\_length} = 512$
* **Bukti Fisik:**
  * Manifes Dataset: [`data/manifests/target_birds_manifest.csv`](../../data/manifests/target_birds_manifest.csv)
  * Konfigurasi Parameter Audio: [`configs/audio.yaml`](../../configs/audio.yaml)

---

### Hari 3–4: Implementasi Representasi Audio & Similarity Engine
* **Target Pembimbing:**
  * Implementasikan baseline MFCC + Cosine Similarity.
  * Smoke test representasi audio umum (Generic PANNs) dan bioakustik (Bioacoustic Pretrained).
  * Pilih checkpoint representasi berdasarkan stabilitas pipeline.
* **Hasil Eksekusi Riil:**
  * Empat representasi berhasil diimplementasikan secara modular:
    1. $R_0$: **MFCC Baseline** (20 koefisien spektral klasik).
    2. $R_1$: **Generic Audio Embedding** (PANNs CNN14, 2048 dimensi).
    3. $R_2$: **Bioacoustic Pretrained** (khusus sinyal suara satwa).
    4. $R_3$: **Random Embedding** (vektor acak Gaussian sebagai kontrol statistik).
  * Engine pencarian kemiripan berbasis *Cosine Similarity* dan metrik $mAP@10$ selesai dibangun.
* **Bukti Fisik:**
  * Modul MFCC: [`src/dsic2706/features/mfcc.py`](../../src/dsic2706/features/mfcc.py)
  * Modul PANNs Generic: [`src/dsic2706/features/panns.py`](../../src/dsic2706/features/panns.py)
  * Modul Bioacoustic: [`src/dsic2706/features/bioacoustic.py`](../../src/dsic2706/features/bioacoustic.py)
  * Modul Similarity Engine: [`src/dsic2706/retrieval/engine.py`](../../src/dsic2706/retrieval/engine.py)

---

### Hari 5–7: Partisi Data Bebas Kebocoran & Baseline Retrieval
* **Target Pembimbing:**
  * Split gallery / query / calibration / test.
  * Buat baseline perolehan kemiripan kondisi bersih (*clean retrieval*).
  * Siapkan protokol kurasi *background-only* lingkungan ITERA.
* **Hasil Eksekusi Riil:**
  * Partisi data ketat menggunakan metode **Strict Global Recordist-Disjoint**:
    * **Gallery Set:** 260 klip dari **42 perekam unik**.
    * **Query Clean Set:** 94 klip dari **29 perekam unik**.
    * **Calibration Set:** 34 klip.
    * **Irisan Perekam (Overlap):** **Tepat 0 Perekam (Zero Leakage)**.
  * Baseline retrieval pada data bersih berhasil dieksekusi ($mAP@10$ Clean: $R_0 = 0.1029$, $R_1 = 0.2299$, $R_2 = 0.2408$, $R_3 = 0.0183$).
  * Protokol perekaman lapangan ITERA selesai disusun di [`docs/protocols/itera-recording.md`](../../docs/protocols/itera-recording.md).
* **Bukti Fisik:**
  * Manifes Pemisahan Data: [`data/manifests/dataset_split.csv`](../../data/manifests/dataset_split.csv)
  * Tabel Hasil Baseline: [`results/tables/snr_robustness_table.csv`](../../results/tables/snr_robustness_table.csv)

---

## 🛡️ Evaluasi Gate Minggu 1
> **Syarat Lolos:** *Minimal tiga representasi termasuk MFCC berhasil menghasilkan embedding dan retrieval pipeline terbukti bebas leakage.*

* **Status:** **LOLOS 100% (PASSED)**
* **Bukti Verifikasi:**
  Jalankan perintah unit test otomatis berikut:
  ```bash
  python run_tests.py
  ```
  Seluruh 7 unit test lolos tanpa galat, termasuk pengujian irisan data pada [`tests/integration/test_split_leakage.py`](../../tests/integration/test_split_leakage.py) yang memverifikasi bahwa:
  $$\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset$$
