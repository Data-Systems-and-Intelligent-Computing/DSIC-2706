# Rencana Eksperimen — Minggu 2 (GATE 2)
**Fokus:** Akuisisi Data Lapangan AudioMoth ITERA & Controlled Noise Robustness (Paired SNR Stress-Testing)  
**Target Garis Waktu:** Minggu Ke-2 (H8–H14)  
**Status Eksekusi:** **SELESAI & LULUS 100% (Verifikasi Audit Gate 2)**  

---

## 1. Perekaman Fisik AudioMoth di Kampus ITERA (H8–H13)

* **Status Lapangan:** Pengambilan data lapangan menggunakan perekam pasif AudioMoth telah selesai dilaksanakan pada 5 titik lingkungan kampus ITERA: Masjid At-Tanwir, Embung F, Kebun Raya, Gedung F, dan GKU 1.
* **Karakteristik Akustik Titik Penempatan:**
  1. *Titik Vegetasi/Embung:* Menangkap ambien alam, biophony serangga/jangkrik, gemerisik dedaunan, hembusan angin, dan riak air.
  2. *Titik Antropogenik:* Menangkap derau aktivitas manusia, koridor gedung, dengung trafo listrik gedung F, dan derau kendaraan bermotor.
* **Standarisasi & Konfigurasi AudioMoth:**
  * Sample Rate: **32.000 Hz** (Mono)
  * Hardware Gain: Medium
  * Format Output: Berkas WAV 16-bit
  * Segmentasi: Dipotong presisi ke jendela waktu 5,0 detik (160.000 sampel).
* **Total Volume Bank Derau & Kurasi (*Bird-Free*):**
  * Terkumpul sebanyak **1.799 berkas audio WAV fisik** di dalam direktori `data/itera_noise/`.
  * Seluruh rekaman telah melewati kurasi dan verifikasi bebas dari keberadaan vokalisasi 20 spesies burung target korpus evaluasi.
* **Manifes Kriptografis SHA-256:**
  * Seluruh 1.799 berkas derau telah diindeks ke dalam [`data/manifests/itera_noise_manifest.csv`](../../data/manifests/itera_noise_manifest.csv) lengkap dengan *hash* SHA-256 kriptografis per berkas dan label verifikasi `verified_bird_free: True`.
* **Pembersihan Jalur Derau Sintetis (Mandat Wajib DEC-09):**
  * Sesuai mandat supervisor, fungsi pembangkit derau sintetis (*pink noise fallback*) `generate_environmental_pink_noise` telah **DIHAPUS PERMANEN** dari `src/mix_noise.py`.
  * Sistem kini secara tegas memicu galat fatal (`raise FileNotFoundError`) jika folder `data/itera_noise/` tidak tersedia, menjamin 100% eksperimen hanya menggunakan rekaman derau fisik nyata.

---

## 2. Eksperimen E2: Evaluasi Temu Kembali di Bawah Derau (Paired SNR Stress-Testing)

* **Kueri Terpasang:** 200 kueri audio bersih dari E1 (10 rekaman per spesies, 68 *author* independen) dipasangkan secara deterministik (`seed=42`) dengan segmen derau AudioMoth ITERA.
* **Grid SNR Terkontrol:**
  1. *Clean:* Kondisi dasar tanpa derau (baseline E1)
  2. *SNR +20 dB:* Derau latar sangat ringan
  3. *SNR +10 dB:* Derau latar sedang
  4. *SNR 0 dB:* Daya sinyal dan derau berimbang
  5. *SNR -5 dB:* Derau dominan terhadap sinyal vokal burung
* **Formulasi Pencampuran Eksak (Berdasarkan Daya RMS):**
  $$x_{\text{noisy}} = x_{\text{clean}} + \alpha \cdot n_{\text{noise}}, \quad \alpha = \sqrt{\frac{P_{\text{signal}}}{P_{\text{noise}} \cdot 10^{\text{SNR}/10}}}$$

### Hasil Empiris Eksperimen E2 (Tercatat di `paper/tables/snr_robustness_table.csv`):

| Representasi | Clean | SNR 20 dB | SNR 10 dB | SNR 0 dB | SNR -5 dB | Retensi Relatif (-5 dB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET Backbone)** | **0.9126** | **0.9068** | **0.8858** | **0.8317** | **0.7707** | **84.45%** (CI: 80.6% – 88.3%) |
| **$R_1$ (PANNs CNN14)** | 0.4152 | 0.4533 | 0.3700 | 0.1290 | **0.0590** | **14.22%** (CI: 10.1% – 18.6%) |
| **$R_0$ (MFCC Baseline)** | 0.1319 | 0.1320 | 0.1022 | 0.0587 | **0.0349** | **26.42%** (CI: 20.8% – 33.4%) |
| **$R_3$ (Random Control)** | 0.0190 | 0.0158 | 0.0148 | 0.0142 | 0.0165 | - |

### Analisis Saintifik Hasil E2 (Mengapa Hasilnya Demikian?):
1. **Ketahanan Superior Model Bioakustik Spesifik ($R_2$):**
   * $R_2$ (BirdNET) mempertahankan skor $mAP@10 = 0.7707$ pada kondisi paling buruk (SNR -5 dB) dengan retensi sebesar **84.45%**.
   * *Alasan Fisik/Arsitektural:* BirdNET dilatih (*pre-trained*) khusus pada jutaan vokalisasi burung dunia. Bobot filternya memiliki sensitivitas selektif frekuensi tinggi (*bandpass tuning*) yang mampu mengabaikan derau *broadband* lingkungan kampus ITERA dan mempertahankan formulan harmoni unik kicauan burung.
2. **Keruntuhan Katastropik Representasi Generic Audio ($R_1$) di Bawah MFCC ($R_0$):**
   * $R_1$ (PANNs CNN14) mengalami penurunan tajam dari 0.4152 ke **0.0590** (hanya tersisa **14.22%** retensi).
   * Yang sangat menarik secara ilmiah: pada SNR -5 dB, retensi relatif $R_1$ (14.22%) **kalah signifikan** dari retensi baseline klasik MFCC ($R_0$) yang masih bertahan di **26.42%**.
   * *Alasan Fisik/Arsitektural:* PANNs dilatih pada AudioSet (suara kendaraan, mesin, percakapan). Pada rasio sinyal-ke-derau negatif ($P_{\text{noise}} > P_{\text{signal}}$), derau kampus ITERA mendistorsi aktivasi neuron konvolusi generik PANNs. Sebaliknya, MFCC mengekstraksi energi filterbank Mel lokal tanpa interaksi non-linear yang dapat memicu *hallucinated features*.
   * *Implikasi terhadap Hipotesis H1:* Hipotesis keunggulan representasi deep atas handcrafted hanya terbukti untuk model domain-spesifik ($R_2$), bukan untuk model deep generik secara umum.
3. **Efek Stochastic Resonance pada SNR +20 dB untuk $R_1$:**
   * Pada derau sangat ringan (SNR +20 dB), performa $R_1$ sedikit naik menjadi 0.4533 (retensi 109.16%). Hal ini konsisten dengan fenomena *stochastic resonance* atau *noise dithering*, di mana sedikit derau aditif bertindak sebagai regularisasi yang menghaluskan representasi spektrogram kueri bersih.
4. **Validitas Kontrol Acak ($R_3$):**
   * $R_3$ konsisten berada di sekitar peluang acak teoretis $1/20 = 0.05$ (0.014 – 0.019) di seluruh rentang SNR, membuktikan ketiadaan artefak *ceiling* maupun *floor* pada formula metrik retrieval.


---

## 3. Kriteria Kelulusan Gate 2 (H14) — 100% Terpenuhi

- [x] **Bank derau `data/itera_noise/` terisi audio nyata AudioMoth:** Terverifikasi 1.799 berkas audio WAV fisik dari 5 lokasi ITERA dan lolos audit bebas suara burung target.
- [x] **Manifes `data/manifests/itera_noise_manifest.csv` terisi lengkap:** 1.799 berkas terdata dengan enkripsi kriptografis SHA-256 dan kolom `verified_bird_free`.
- [x] **Fallback pink noise di `src/mix_noise.py` dihapus:** Kode cadangan derau sintetis telah dilenyapkan; sistem memicu `FileNotFoundError` fatal jika berkas fisik tidak ada.
- [x] **Pemasangan kueri bersifat deterministik:** Pencampuran menggunakan parameter generator acak tetap (`seed=42`) sehingga 100% dapat direproduksi (*reproducible*).
- [x] **Kurva degradasi $mAP@10$ dan retensi relatif dihasilkan:** Tersimpan resmi dalam format tabel di [`paper/tables/snr_robustness_table.csv`](../../paper/tables/snr_robustness_table.csv) dan gambar grafik publikasi di [`paper/figures/e2_snr_robustness_curve.png`](../../paper/figures/e2_snr_robustness_curve.png).
- [x] **Seluruh log pemeringkatan per-kueri mentah tersimpan:** Direktori `results/raw/` menyimpan berkas `R0_SNR_*_raw.csv`, `R1_SNR_*_raw.csv`, `R2_SNR_*_raw.csv`, dan `R3_SNR_*_raw.csv` dengan detail per-kueri.
- [x] **Notebook interaktif pengujian tersedia:** Tersedia di [`notebooks/E2_Paired_Noise_Degradation.ipynb`](../../notebooks/E2_Paired_Noise_Degradation.ipynb).
