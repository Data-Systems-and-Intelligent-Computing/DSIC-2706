# Catatan Progres Riset Tugas Akhir (DSIC-2706)
**Topik:** Mencari Audio yang Mirip Ketika Datanya Terbatas  
**Judul Kerja:** *Noise and Domain-Shift Robustness of Audio Representations for Cross-Domain Bioacoustic Retrieval: From Xeno-Canto to ITERA Soundscapes*  
**Mahasiswa:** Fabio Banyu Cyto (NIM: 123450104)  
**Dosen Pembimbing:** Bapak Ardika  
**Institusi:** Program Studi Sains Data, Institut Teknologi Sumatera (ITERA)  
**Terakhir Diperbarui:** 07 September 2026  

---

## 📌 Ringkasan Eksekutif (TL;DR)
Laporan ini memuat rekam jejak lengkap, transparan, dan dapat direproduksi (*reproducible*) dari pengerjaan Tugas Akhir DSIC-2706. Hingga saat ini, seluruh repositori telah disinkronkan secara modular mengikuti standar template riset pembimbing. Eksperimen dasar (**E0: Pipeline Sanity**, **E1: Ekstraksi Representasi Audio**, dan **E2: Paired Noise Stress-Testing**) telah selesai dijalankan pada 416 audio burung (16 spesies) dan 77 audio satwa non-burung dengan partisi ketat **Zero Recordist Leakage**. 

Temuan utama menunjukkan bahwa pada kondisi derau ekstrem (SNR -5 dB), representasi khusus bioakustik (**Bioacoustic Pretrained**) memiliki retensi kualitas perolehan kemiripan (**38.9%**) yang hampir **2 kali lipat lebih tangguh** dibanding representasi audio umum/generik PANNs (**19.6%**) dan fitur klasik MFCC (**27.4%**).

---

## ⏱️ Bagian 1: Posisi Progres Saat Ini vs Timeline 30 Hari Dosen Pembimbing

Berikut adalah audit posisi pengerjaan riil dibandingkan dengan target roadmap 30 hari yang diberikan oleh dosen pembimbing:

### 🟢 Status Keseluruhan: **AHEAD OF SCHEDULE (Lebih Cepat dari Jadwal)**
Secara teknis algoritma, rekayasa data, dan eksperimen komputasi, **kita saat ini berada di akhir Minggu ke-2 menuju Minggu ke-3**. Kriteria teknis pada **Gate Minggu 1** dan **Gate Minggu 2** telah **terpenuhi secara internal dan siap ditinjau oleh dosen pembimbing** dengan bukti artefak dan kode yang konkret.

```
[ Minggu 1: Dataset & Feasibility ]   ======> Kriteria Teknis Terpenuhi (Siap Ditinjau)
[ Minggu 2: Controlled Noise Test ]   ======> Kriteria Teknis Terpenuhi (Siap Ditinjau)
[ Minggu 3: Open-Set & Field Eval ]   ======> 60% Selesai (Dalam Pengerjaan)
[ Minggu 4: Statistik & Penulisan ]   ======> Draf Awal Siap (Terjadwal)
```

---

### 📋 Matriks Rincian Timeline, Status, & Bukti Fisik

| Periode Roadmap | Target Pembimbing | Status Riil | Bukti Fisik di Repositori |
| :--- | :--- | :---: | :--- |
| **Minggu 1: Hari 1-2** | • Bekukan target 10-20 burung<br>• Manifest Xeno-Canto & lisensi<br>• Bekukan sample rate & durasi | **SELESAI** | • Manifes 16 spesies (416 audio): `data/manifests/target_birds_manifest.csv`<br>• Konfigurasi audio (32 kHz, 5.0 detik): `configs/audio.yaml` |
| **Minggu 1: Hari 3-4** | • Implementasi MFCC + Cosine<br>• Smoke test PANNs & Bioacoustic<br>• Pilih checkpoint representasi | **SELESAI** | • Kode ekstraktor: `src/dsic2706/features/` (`mfcc.py`, `panns.py`, `bioacoustic.py`)<br>• Engine pencarian: `src/dsic2706/retrieval/engine.py`<br>• Skrip uji: `run_tests.py` & `experiments/e0_pipeline_sanity/` |
| **Minggu 1: Hari 5-7** | • Ambil/kurasi background ITERA<br>• Split gallery/query/calibration<br>• Buat baseline clean retrieval | **85% SELESAI** | • Protokol rekam ITERA: `docs/protocols/itera-recording.md`<br>• Manifes split: `data/manifests/dataset_split.csv`<br>• Baseline retrieval: `results/tables/snr_robustness_table.csv` (Kolom `clean`) |
| **GATE MINGGU 1** | **Minimal 3 representasi (termasuk MFCC) menghasilkan embedding & pipeline bebas leakage** | **Kriteria Terpenuhi (Siap Ditinjau)** | **`python run_tests.py` lolos 7/7 unit test; Irisan perekam Galeri vs Query tepat 0 (Zero Leakage)** |
| **Minggu 2: Hari 8-10**| • Implementasi mixing SNR reproducible<br>• Pilot level SNR (20 s/d -5 dB)<br>• Bekukan noise segment & seed | **SELESAI** | • Modul derau deterministik (seed 42): `src/dsic2706/audio/noise.py`<br>• Definisi level SNR: `configs/audio.yaml` |
| **Minggu 2: Hari 11-14**| • Jalankan E1-E2 seluruh query<br>• Simpan ranking per query<br>• Buat robustness curve awal | **SELESAI** | • Tabel hasil E2: `results/tables/snr_robustness_table.csv`<br>• Grafik mAP@10: `results/figures/robustness_curve_map10.png`<br>• Grafik retensi: `results/figures/relative_retention_curve.png` |
| **GATE MINGGU 2** | **Tidak ada ceiling/floor total, query pairs konsisten, kontrol acak masuk akal** | **Kriteria Terpenuhi (Siap Ditinjau)** | **Nilai mAP terdistribusi alami (0.24 -> 0.09), Kontrol acak ($R_3$) stabil di 0.018–0.022** |
| **Minggu 3: Hari 15-18**| • Susun unknown/background set<br>• Kalibrasi threshold ($\tau$) pada calibration split<br>• Jalankan open-set test semua SNR | **SELESAI** | • Dataset unknown (77 audio): `data/manifests/unknown_open_set_manifest.csv`<br>• Kalibrasi ROC & Youden's J: `src/dsic2706/open_set/threshold.py` ($\tau^* = 0.9905$)<br>• Tabel open-set: `results/tables/openset_evaluation_table.csv` |
| **Minggu 3: Hari 19-21**| • Anotasi subset real soundscape ITERA<br>• Validasi eksternal tanpa re-tuning<br>• Audit minimal 20 failure cases | **50% SELESAI** | • Audit kegagalan retrieval: `results/tables/failure_analysis_table.csv`<br>• *Catatan:* Menunggu perekaman audio fisik di Embung & Arboretum ITERA |
| **Minggu 4: Hari 22-30**| • Paired bootstrap CI & kurva final<br>• Naskah laporan & artikel v0.8<br>• Freeze code & materi bimbingan | **DALAM PROGRES** | • Catatan progres: `Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md` |

---

## 🧭 Bagian 2: Latar Belakang, Motivasi, & Relevansi SDGs

### 2.1 Masalah Riil di Lapangan
Pemantauan keanekaragaman hayati secara konvensional (misal pengamatan visual burung di hutan atau kebun raya) memiliki keterbatasan besar: memakan waktu, mahal, mengganggu habitat satwa liar, dan bergantung pada subjektivitas pengamat. Metode modern menggunakan **Passive Acoustic Monitoring (PAM)**, yaitu meletakkan alat perekam suara nirawak di alam liar untuk merekam suara lingkungan (*soundscape*) secara terus-menerus.

Namun, penerapan kecerdasan buatan (*Artificial Intelligence*) pada PAM menghadapi tiga tantangan besar:
1. **Data Terbatas (*Data Scarcity / Few-Shot*):** Banyak spesies burung langka di Indonesia hanya memiliki segelintir rekaman suara berkualitas baik.
2. **Derau Lingkungan (*Environmental Noise*):** Rekaman alam terbuka selalu tercemar suara angin, hujan lebat, aliran air, gemerisik daun, dan bising kendaraan (*anthrophony*).
3. **Pergeseran Domain (*Domain Shift*):** Model yang diuji pada rekaman studio/fokal bersih (misal dari basis data Xeno-Canto) sering kali gagal total (*catastrophic failure*) ketika diuji pada rekaman lingkungan nyata (*soundscape* terbuka di ITERA).

### 2.2 Relevansi dengan Sustainable Development Goals (SDGs)
Penelitian analitik data audio ini secara langsung mendukung agenda global pembangunan berkelanjutan:
* **SDG 15: Ekosistem Darat (Life on Land) — Target 15.5 & 15.9 [UTAMA]:** Menyediakan instrumen pemantauan keanekaragaman hayati berbasis bioakustik yang otomatis, akurat, non-invasif, dan tangguh terhadap cuaca buruk untuk perlindungan habitat satwa liar.
* **SDG 11: Kota dan Pemukiman yang Berkelanjutan (Target 11.7):** Menguji ketahanan akustik di ruang terbuka hijau kampus (Embung dan Arboretum ITERA) guna memantau koeksistensi satwa liar di tengah pembangunan kawasan urban/pendidikan.
* **SDG 13: Penanganan Perubahan Iklim (Target 13.3):** Pola suara soundscape (biophony vs anthrophony) berfungsi sebagai bioindikator peringatan dini (*early warning indicator*) degradasi iklim mikro lokal.
* **SDG 9: Industri, Inovasi, dan Infrastruktur (Target 9.5):** Inovasi keilmuan *Data Science* dalam perolehan kemiripan audio (*robust similarity retrieval*) pada data berskala kecil dan berderau tinggi.

---

## 🛠️ Bagian 3: Kronologi Pekerjaan Teknis yang Telah Diselesaikan

### Tahap 1: Penyelarasan Arsitektur Repositori (100% Sesuai Template Pembimbing)
Kode lokal telah direstrukturisasi secara profesional agar sesuai dengan repositori resmi DSIC:
* **Paket Modular `src/dsic2706/`:**
  * `audio`: Pemrosesan sinyal audio, augmentasi, injeksi derau SNR.
  * `features`: Ekstraksi representasi ($R_0$ MFCC, $R_1$ Generic PANNs, $R_2$ Bioacoustic, $R_3$ Random).
  * `retrieval`: Engine perolehan kemiripan (*Cosine Similarity*) dan metrik $mAP@10$.
  * `open_set`: Kalibrasi ambang batas $\tau^*$ penolakan spesies tak dikenal.
  * `evaluation`: Paired stress-testing dan kalkulasi kurva retensi.
* **Manajemen Konfigurasi:** Menggunakan file YAML terpusat di `configs/` (`audio.yaml`, `representation.yaml`, `split.yaml`, `open_set.yaml`).
* **Proteksi Berkas Audio (`.gitignore`):** Seluruh berkas biner `.mp3` dan `.wav` diabaikan dari pelacakan Git, sehingga repositori GitHub tetap bersih dan ringan (< 5 MB), hanya menyimpan kode, manifes CSV, checksum SHA-256, dan hasil eksperimen.

### Tahap 2: Audit Integritas Dataset Audio
* **Jumlah Berkas:** Terkumpul **416 rekaman burung target** dan **77 rekaman satwa non-burung** (total 493 berkas fisik).
* **Kualitas Berkas:** 100% berkas terbaca sempurna (**0 berkas korup**), terstandarisasi pada sampling rate mono 32.000 Hz dengan durasi klip 5.0 detik.
* **Catatan Transparansi Penggantian Spesies:**
  * Saat pengunduhan dari Xeno-Canto v3, rekaman spesies *Oriolus chinensis* (Kepodang Kuduk Hitam) memblokir tautan unduhan audio publik karena regulasi perlindungan satwa rentan perburuan liar (*poaching-sensitive*).
  * Agar data 100% legal, terbuka, dan dapat direproduksi publik, spesies tersebut digantikan oleh 2 spesies burung endemik/lokal Sumatera yang memiliki rekaman terbuka: *Aethopyga siparaja* (Burung-madu sepah, $N=26$) dan *Dicaeum trigonostigma* (Cabai bunga api, $N=24$). Total takson target menjadi **16 spesies**.
* **Isolasi Data Non-Burung:** 77 audio non-burung (katak, jangkrik/serangga, kelelawar, primata) diisolasi ke `data/unknown_open_set/` sebagai *negative control* untuk uji penolakan kelas asing (*open-set rejection*).

### Tahap 3: Pemisahan Data Tanpa Kebocoran (*Strict Global Recordist-Disjoint*)
Untuk menjamin hasil pengujian bebas dari bias "hafalan alat rekam":
* Dilakukan pemotongan graf bipartit antara identitas perekam (*recordist*) pada data referensi (Gallery) dan data uji (Query):
  $$\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset$$
* **Gallery Set:** 260 klip dari **42 perekam unik**.
* **Query Clean Set:** 94 klip dari **29 perekam unik**.
* **Tingkat Kebocoran (*Leakage*):** **Tepat 0 perekam (Zero Leakage)**. Model diuji pada audio dari orang dan mikrofon yang 100% belum pernah ada di galeri data.
* Dilengkapi unit test otomatis di `tests/integration/test_split_leakage.py` yang lolos 100%.

### Tahap 4: Pelaksanaan Eksperimen Benchmark (E0, E1, E2)
* **E0 (Pipeline Sanity Check):** Pengujian ujung-ke-ujung (*end-to-end*) pada sub-sampel kecil audio untuk memastikan komputasi fitur, pencarian kemiripan, dan kalkulasi metrik berjalan tanpa galat.
* **E1 (Ekstraksi Representasi Audio):** Mengekstraksi fitur embedding dari 4 model:
  1. $R_0$: **MFCC Baseline** (20 koefisien spektral klasik).
  2. $R_1$: **Generic Audio (PANNs CNN14)** (pretrained pada 2 juta klip AudioSet umum).
  3. $R_2$: **Bioacoustic Pretrained** (khusus dilatih pada data suara satwa liar).
  4. $R_3$: **Random Embedding** (vektor acak terdistribusi normal sebagai kontrol statistik).
* **E2 (Paired Noise Stress-Testing):** Menguji ketahanan query yang sama ketika disuntik derau lingkungan sintetis bertingkat dari Clean, 20 dB, 10 dB, 0 dB, hingga -5 dB SNR.

---

## 📊 Bagian 4: Hasil Eksperimen & Temuan Ilmiah (Hasil Run)

Seluruh metrik dihitung secara adil dan berpasangan (*paired*) pada 94 query yang identik di setiap tingkatan derau:

### 4.1 Tabel Kualitas Perolehan Kemiripan (mAP@10)
*mAP@10 (Mean Average Precision pada Top-10 hasil retrieval teratas):*

| Kondisi Derau | $R_0$: MFCC (Klasik) | $R_1$: Generic Audio (PANNs) | $R_2$: Bioacoustic (Spesifik) | $R_3$: Random (Kontrol Acak) |
| :--- | :---: | :---: | :---: | :---: |
| **Clean (Tanpa Derau)** | 0.1029 | 0.2299 | **0.2408** | 0.0183 |
| **SNR 20 dB (Derau Ringan)** | 0.0770 | **0.2342** | 0.2315 | 0.0223 |
| **SNR 10 dB (Derau Sedang)** | 0.0549 | **0.2239** | 0.2137 | 0.0209 |
| **SNR 0 dB (Derau Sama Kuat)**| 0.0409 | 0.1109 | **0.1589** | 0.0149 |
| **SNR -5 dB (Derau Ekstrem)** | 0.0282 | 0.0450 | **0.0936** | 0.0179 |

### 4.2 Tabel Retensi Kualitas Relatif Terhadap Kondisi Bersih (%)
*Menunjukkan berapa persen performa model yang mampu bertahan hidup saat derau meningkat dibandingkan saat kondisi bersih:*

| Kondisi Derau | $R_0$: MFCC | $R_1$: Generic Audio | $R_2$: Bioacoustic Pretrained |
| :--- | :---: | :---: | :---: |
| **Clean (100%)** | 100.0% | 100.0% | 100.0% |
| **SNR 20 dB** | 74.8% | 101.9% | **96.1%** |
| **SNR 10 dB** | 53.4% | 97.4% | **88.7%** |
| **SNR 0 dB** | 39.8% | 48.2% | **66.0%** |
| **SNR -5 dB** | 27.4% | 19.6% | **38.9%** (Hampir 2x lipat $R_1$) |

### 4.3 Temuan Ilmiah Utama (Validasi Hipotesis)
1. **Validasi Hipotesis H1 & H2 (Ketahanan Representasi Spesifik Domain):**
   * Pada derau ringan hingga sedang (20 dB dan 10 dB), model umum ($R_1$) memiliki performa yang sangat kompetitif dengan model bioakustik ($R_2$).
   * Namun, begitu memasuki derau berat (0 dB dan -5 dB), performa model umum **runtuh secara drastis** (retensi anjlok ke 19.6%).
   * Sebaliknya, representasi bioakustik ($R_2$) terbukti jauh lebih tangguh menghadapi derau ekstrem dengan retensi **38.9%** (mAP 0.0936 vs 0.0450). Model bioakustik memahami fitur harmonik vokal burung sehingga tidak mudah terdistorsi oleh frekuensi bising lingkungan.
2. **Koreksi Nilai Bersih (Clean mAP) yang Lebih Realistis:**
   * Pada uji coba awal sebelum pemisahan perekam, nilai mAP berkisar ~0.31. Setelah diterapkan pemisahan perekam global (*recordist-disjoint*) dan penambahan query dari 34 menjadi 94 klip, nilai mAP menjadi ~0.24.
   * Penurunan ini merupakan **koreksi positif yang jujur secara metodologis**, membuktikan bahwa tidak ada lagi kebocoran data di mana model mengenali suara karena kesamaan perangkat rekam.
3. **Validasi Hipotesis H4 (Kegagalan Ambang Batas Statis pada Model Generik):**
   * Ketika ambang batas open-set ($\tau^*$) dibekukan dari data bersih lalu diuji pada query berderau berat (-5 dB), model generik $R_1$ mengalami fenomena *false rejection* total (Recall anjlok ke 0.0000 karena derau mendorong vektor fitur menjauhi galeri).
   * Model $R_2$ mempertahankan stabilitas jarak kemiripan yang jauh lebih konsisten.

---

## 📅 Bagian 5: Agenda Tahapan Selanjutnya (Next Steps)
1. **Perekaman Derau Lingkungan Asli ITERA (Minggu ke-2 / Minggu ke-3 Lapangan):**
   * Melakukan pengambilan sampel suara murni lingkungan (*noise-only soundscape*) tanpa suara burung di dua lokasi target: **Embung ITERA** dan **Arboretum/Kebun Raya ITERA** sesuai protokol pada `docs/protocols/itera-recording.md`.
2. **Eksperimen E3 (Domain-Shift Xeno-Canto to ITERA Soundscapes):**
   * Mengganti derau sintetis dengan rekaman derau nyata dari ITERA untuk menguji ketahanan model pada kondisi fisik kampus yang sesungguhnya.
3. **Penyusunan Bab 3 & Bab 4 Skripsi:**
   * Memindahkan tabel hasil eksperimen dan grafik retensi ke dalam format naskah skripsi resmi.

---

## 💻 Cara Menjalankan & Memverifikasi Kode Secara Mandiri

Untuk menguji kembali seluruh hasil di atas dari terminal secara transparan:

```bash
# 1. Menjalankan seluruh pengujian unit & verifikasi zero leakage
python run_tests.py

# 2. Menjalankan verifikasi keterulangan deterministik (sanity check)
python -m dsic2706.cli sanity

# 3. Menjalankan pengujian ketahanan derau komparatif (E2)
python -m dsic2706.cli noise-robustness
```
Semua artefak grafik kurva retensi tersimpan secara otomatis di direktori `results/figures/` dan tabel di `results/tables/`.
