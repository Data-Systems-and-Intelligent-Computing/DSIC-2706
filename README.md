# DSIC-2706 — Ketahanan Representasi Audio Beku untuk Temu Kembali Bioakustik di Bawah Derau Lingkungan Tropis ITERA

> **Bahan penulisan — 1 November 2026:** [draf BAB I LaTeX dan PDF](paper/template_ta_latex/README.md), [pustaka yang diperiksa](paper/bibliography/README.md), [paket belajar](learning/PAKET_BELAJAR_UJIAN/README.md), serta [catatan istilah dan contoh hitungan kosinus](paper/template_ta_latex/notes/ISTILAH_LATAR_BELAKANG_UNTUK_FABIO.md) disertakan dalam sinkronisasi repositori. BAB II–III masih kerangka. [Bahan teori lama](Teori%20Dasar/README.md) diberi penanda historis; rincian pembersihan dan cakupan sinkronisasi ada di [catatan 1 November](docs/WORKSPACE_SYNC_2026-11-01.md).

> **Revisi pembimbing 15 Oktober 2026:** E4 lima lokasi tetap digunakan tanpa run ulang. [Hasil sensitivitas H3](results/reproductions/H3_sensitivity_20261015/tables/h3_swing_summary.csv) melaporkan ayunan absolut dan relatif serta subset tanpa Kebun Raya; kesimpulan bergantung pada metrik dan lokasi. H3/H4 hasil reformulasi ditandai eksploratif, dengan [rumusan asli dan tanggal perubahan](docs/research/hypotheses.md). Gunakan [catatan revisi lengkap](docs/REVISION_SUPERVISOR_2026-10-15.md), [matriks RQ/H revisi](results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv), dan [naskah teori](paper/teori_dasar.md). Bahan laporan 12 Oktober beserta checksum tetap dipertahankan sebagai riwayat.
>
> **Status aktif — 30 Oktober 2026:** hasil komputasional E0–E5 dan reproduksi dalam scope revisi tersedia; [catatan audit pendengaran E5](Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md) mencakup **120/120 kasus pilihan oleh satu pendengar**. Bukti cukup untuk mulai menyusun skripsi dalam lingkup campuran aditif terkontrol; persetujuan pembimbing dan kelengkapan naskah tetap terpisah. Gunakan §13 dan laporan audit tersebut. [CURRENT_STATUS.md](Rencana-eksperimen-bimbingan/CURRENT_STATUS.md) bertanggal 18 Oktober masih memuat status audit 0/120 yang sudah kedaluwarsa.

Repositori penelitian resmi untuk Tugas Akhir topik **DSIC-2706: Mencari Audio yang Mirip Ketika Datanya Terbatas**.

Fokus penelitian ini bukan membuat pengklasifikasi (*classifier*) spesies baru, melainkan menguji secara komparatif **ketahanan representasi audio beku (*frozen audio representations*) untuk temu kembali kemiripan (*similarity retrieval*)** ketika kueri bioakustik mengalami degradasi derau lingkungan tropis nyata kampus ITERA (*Institut Teknologi Sumatera*).

Judul kerja yang dipersempit, mengikuti [RQ aktif](docs/research/rq.md); redaksi final mengikuti persetujuan pembimbing:

> **Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval under Controlled ITERA Field-Noise Mixtures in Indonesian Avifauna**

---

## 1. Pertanyaan Penelitian (Research Questions)

### RQ Utama
**Representasi audio mana yang mempertahankan kualitas similarity retrieval paling baik ketika query bioakustik avifauna Indonesia didegradasi secara terkontrol oleh rekaman noise lapangan ITERA pada beberapa tingkat SNR?**

### Sub-RQ
1. **Sub-RQ 1 — Controlled noise degradation (E2):** Seberapa besar perubahan `mAP@10`, `Recall@10`, `Precision@10`, MRR, dan Top-1 untuk R0–R3 pada Clean, +20, +10, 0, dan −5 dB ketika query dicampur noise ITERA fisik?
2. **Sub-RQ 2 — Frozen open-set threshold (E3):** Apakah threshold kemiripan τ* yang dioptimalkan pada subset kalibrasi terpisah dan kemudian dibekukan mempertahankan perilaku penerimaan/penolakan yang terukur untuk target known-set dan kontrol unknown pada query bising?
3. **Sub-RQ 3 — Sensitivitas dan stabilitas profil noise lapangan (E4/H3):** Bagaimana `mAP@10`, Top-1, dan retensi retrieval berubah ketika query yang sama dicampur secara aditif dengan profil noise asli dari lima lokasi ITERA pada SNR yang sama; dan bagaimana perbandingan ayunan mAP@10 absolut serta retensi relatif representasi bioakustik dan audio umum berubah ketika Kebun Raya dikeluarkan sebagai analisis sensitivitas?
4. **Sub-RQ 4 — Diagnostik kegagalan retrieval (E5):** Moda kegagalan apa—*open-set false rejection*, *top-1 confusion above threshold*, atau *total retrieval collapse*—yang muncul pada kondisi clean dan bising; serta bagaimana hubungan margin threshold dan fitur spektral dengan moda tersebut?

Rumusan di atas menyelaraskan README dengan `docs/research/rq.md`, bukan menetapkan RQ baru. Riwayat perubahan setelah hasil pada 12/15 Oktober dan status eksploratif H3/H4 tetap berlaku. H3 asli tentang real-soundscape burung in-situ belum diuji.

---

## 2. Hipotesis Saintifik

* **$H_1$ — Robustness Retention:** Representasi *deep pretrained* (BirdNET dan PANNs) mempertahankan proporsi retensi relatif `mAP@10` yang secara signifikan lebih tinggi daripada representasi klasik *hand-crafted* (MFCC) ketika SNR diturunkan hingga -5 dB.
* **$H_2$ — Domain-Specific Advantage:** Representasi terlatih bioakustik spesifik domain burung (*BirdNET*) mengalami degradasi temu kembali yang lebih landai dibandingkan representasi audio umum (*PANNs CNN14*) pada kueri avifauna Indonesia yang dicampur derau lingkungan nyata.
* **$H_3$ — Stabilitas profil lokasi (reformulasi eksploratif):** bandingkan ayunan mAP@10 absolut dan retensi relatif R1/R2 pada lima lokasi serta sensitivitas tanpa Kebun Raya. Bukti tidak mendukung keunggulan stabilitas R2 yang berlaku umum.
* **$H_4$ — Perubahan titik operasi (reformulasi eksploratif):** recall penerimaan known-set turun pada threshold clean yang beku; false-accept rate tidak meningkat. Rumusan asli dan perubahan 12 Oktober dicatat di hypotheses.md.
* **$H_5$ — Positive Control:** Representasi audio $R_0$ (MFCC), $R_1$, dan $R_2$ mengungguli kontrol ID-deterministik $R_3$ pada kondisi bersih sebagai pemeriksaan baseline. MFCC bukan model yang dilatih.

---

## 3. Batas Kontribusi Ilmiah

### Kontribusi Utama:
1. Evaluasi ketahanan berpasangan (*paired robustness evaluation*) pada kueri yang identik menggunakan audio burung asli Indonesia dari Xeno-Canto.
2. Uji stres derau lingkungan tropis nyata menggunakan bank 1.799 rekaman fisik AudioMoth kampus ITERA; status bebas suara burung untuk setiap berkas belum dibuktikan secara independen.
3. Perbandingan sistematis antara *hand-crafted baseline* ($R_0$ MFCC), *generic pretrained* ($R_1$ PANNs CNN14), *domain-specific bioacoustic* ($R_2$ BirdNET V2.4), dan *negative control* ($R_3$ Random Control).
4. Penyelidikan transfer ambang batas open-set dengan optimasi statistik Youden's J yang dibekukan (*frozen threshold*).
5. Audit taksonomi kegagalan terstratifikasi berdasarkan parameter akustik nyata (*spectral centroid*, *bandwidth*, dan *margin to tau*).
6. Pelacakan asal berkas derau fisik (`noise_file`) dan [reproduksi terpisah](docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md): E0, ekstraksi clean R0–R3, E1–E3, E5, serta statistik H3 menghasilkan 41/41 pembandingan cocok pada venv baru di komputer yang sama. Inferensi E4 tidak diulang; input berasal dari arsip lokal terverifikasi.

### Yang **Bukan** Kontribusi Penelitian:
* Melatih ulang (*fine-tuning*) arsitektur model baru.
* Membuat aplikasi identifikasi spesies bergerak (*mobile app*) atau dashboard inventarisasi ekologis.
* Mengestimasi populasi atau kelimpahan satwa (*occupancy / abundance modelling*).

---

## 4. Representasi yang Dibandingkan

| Kode | Representasi | Dimensi | Peran | Checkpoint / Sumber |
|:---:|---|:---:|---|---|
| **$R_0$** | MFCC (20 koefisien, mean/std temporal pooling) | 40-d | Baseline akustik klasik | `librosa` feature extractor |
| **$R_1$** | PANNs CNN14 (AudioSet general audio pretrained) | 2048-d | Deep embedding generik | `checkpoints/Cnn14_mAP=0.431.pth` |
| **$R_2$** | BirdNET Backbone V2.4 (Avian bioacoustic domain pretrained) | 1024-d | Domain-specific representation | `checkpoints/BirdNET_GLOBAL_6K_V2.4_Model_FP32.onnx` |
| **$R_3$** | Kontrol acak Gaussian berdasarkan ID, dinormalisasi L2 | 40-d | Kontrol pembanding berbasis ID, bukan waveform | Seed dasar 42 dan hash ID/versi kontrol |

Seluruh embedding dinormalisasi ke *unit hypersphere* ($\|\mathbf{x}\|_2 = 1.0$) dan dievaluasi menggunakan metrik **Cosine Similarity**:
$$\text{sim}(\mathbf{q}, \mathbf{g}) = \frac{\mathbf{q} \cdot \mathbf{g}}{\|\mathbf{q}\|_2 \|\mathbf{g}\|_2}$$

R1/R2 digunakan **beku (*frozen*)** tanpa pembaruan bobot. R0 menghitung MFCC, sedangkan R3 membentuk vektor dari ID. Perbandingan memakai query dan gallery yang sama; kondisi ini tidak menghilangkan potensi overlap data pralatih atau perbedaan asal pelatihan model.

---

## 5. Dataset dan Bank Derau Fisik

### A. Dataset Avifauna Indonesia (Xeno-Canto Indonesia)
Korpus data utama menggunakan rekaman vokal burung dari wilayah geografis Indonesia yang diunduh dari Xeno-Canto:
* **20 Spesies Target Beku (`data/manifests/indonesia_species_freeze.csv`):** Spesies umum dan tersebar luas di Indonesia, dengan representasi Pulau Sumatera dan wilayah Sundaland:
  * *Pnoepyga pusilla* (`pygcup1`, Berencet kerdil, 105 klip), *Cacomantis sepulcralis* (`rubcuc1`, Wiwik uncuing, 85 klip), *Malacocincla sepiaria* (`horbab1`, Pelanduk semak, 68 klip), *Phyllergates cucullatus* (`moutai1`, Cinenen gunung, 137 klip), *Brachypteryx leucophris* (`lessho1`, Cingcoang cokelat, 66 klip), *Caprimulgus macrurus* (`latnig1`, Cabak maling, 47 klip), *Pycnonotus aurigaster* (`sohbul1`, Cucak kutilang, 44 klip), *Cinnyris jugularis* (`olbsun1`, Burung-madu sriganti, 123 klip), *Pitta sordida* (`hoopit1`, Paok hijau, 62 klip), *Cuculus lepidus* (`suncuc1`, Kangkok sunda, 42 klip), *Caprimulgus affinis* (`savnig1`, Cabak kota, 31 klip), *Dicrurus hottentottus* (`hacdro1`, Srigunting rambut, 91 klip), *Horornis vulcanius* (`subwar1`, Kerakbasi sunda, 48 klip), *Ducula aenea* (`gpipig1`, Pergam hijau, 45 klip), *Brachypteryx montana* (`whbsho1`, Cingcoang alis-putih, 40 klip), *Culicicapa ceylonensis* (`ghcfly1`, Sikatan kepala-kelabu, 38 klip), *Aegithina tiphia* (`comior1`, Cipoh kacat, 39 klip), *Spilornis cheela* (`crseag1`, Elang-ular bido, 35 klip), *Orthotomus ruficeps* (`ashtai1`, Cinenen kelabu, 30 klip), *Todiramphus chloris* (`colkin1`, Cekakak sungai, 40 klip).
* **Total Rekaman Terverifikasi:** 1.216 berkas audio MP3 (30–137 rekaman per spesies, rata-rata 60,8 rekaman/spesies; 14–35 perekam unik per spesies, 111 nilai nama perekam unik pada manifes split aktif; 112 nama orang setelah pemisahan nama gabungan dengan &).
* **Audit Integritas Unduhan:** Seluruh berkas tercatat di `data/manifests/download_manifest.csv` lengkap dengan HTTP status 200, ukuran byte, checksum SHA-256, sampling rate asli, durasi, dan verifikasi keterbacaan (*100% decodable*).
* **Standar Prapemrosesan:** Durasi 5,0 detik (160.000 sampel pada 32 kHz), mono, normalisasi energi RMS = 0.05.
* **Kebijakan Lisensi Git:** Berkas audio fisik tidak di-commit ke Git (mematuhi lisensi non-komersial/non-derivatif); hanya manifes metadata dan hash yang dilacak.

### B. Bank Derau Fisik AudioMoth Kampus ITERA
* **1.799 Berkas WAV Fisik:** Diambil langsung menggunakan perangkat perekam otonom *AudioMoth* di 5 lokasi kampus ITERA (Kebun Raya ITERA, Embung F, Gedung F, Masjid At-Tanwir, Sekitar GKU 1).
* **Status vokalisasi burung:** Bank ini dipakai sebagai noise lingkungan; bukti audit independen yang menyatakan setiap berkas bebas vokalisasi target belum tersedia.
* **Pemisahan berkas pool noise (*Noise Pool Separation*):**
  * **1.528 berkas** dialokasikan khusus untuk pencampuran derau aditif E2 dan E4.
  * **271 berkas** dialokasikan khusus untuk kontrol negatif kelas terbuka E3.
* **Penolakan Derau Senyap:** Engine pencampuran menolak segmen dengan $\text{RMS} < 10^{-4}$ ($P_{\text{noise}} \le 10^{-10}$).
* **Penghapusan Pink Noise:** Fallback derau sintetis telah **dihapus permanen**. Modul melempar `FileNotFoundError` keras jika berkas fisik tidak ditemukan.

### C. Arsip Warisan (*Legacy Archive*)
Hasil evaluasi lama yang pernah menggunakan data BirdCLEF telah dipindahkan dan diarsipkan secara terpisah di `results/archive/birdclef_2026/` untuk transparansi jejak rekam ilmiah.

---

## 6. Partisi Data (Strict Global Recordist-Disjoint)

Partisi data dibekukan di `data/manifests/dataset_split.csv` dengan memisahkan identitas perekam (*author/recordist*) secara absolut:

```text
Xeno-Canto Indonesia (1.216 klip | 20 spesies burung Indonesia | 111 nama perekam unik)
├── Gallery Set      : 673 klip (59 perekam unik) -> Basis data referensi pencarian
├── Query Clean Set  : 311 klip (27 nilai nama; 28 orang setelah nama gabungan dipisah) -> Kueri bersih uji berpasangan
└── Calibration Set  : 232 klip (25 perekam unik) -> Kalibrasi ambang batas open-set

Unknown Open-Set Manifest (543 klip kontrol negatif)
├── Unknown Calibration : 233 klip kontrol negatif kalibrasi (117 burung non-target + 116 derau ITERA)
└── Unknown Test Set    : 310 klip kontrol negatif pengujian (155 burung non-target + 155 derau ITERA)
```

### Pemeriksaan pemisahan internal target:
* **Zero Recordist Overlap:** 0 perekam beririsan antar Galeri, Kueri, dan Kalibrasi ($\text{Recordists}(G) \cap \text{Recordists}(Q) = \emptyset$).
* **Zero Recording ID Overlap:** 0 nomor katalog Xeno-Canto yang beririsan antar subset.
* **Zero Filepath Overlap:** 0 path beririsan antar Gallery, Query, dan Calibration; audit checksum tidak menemukan audio identik lintas peran yang diperiksa.

Pemisahan berkas tidak membuktikan independensi seluruh sesi/perekam unknown atau bebas overlap data pralatih. Audit masih mencatat 30 grup folder/tanggal noise yang sama pada unknown calibration/test dan metadata author unknown yang belum diverifikasi; lihat [crosscheck data](docs/CROSSCHECK_2026-10-12.md).

---

## 7. Ringkasan Temuan Eksperimen Utama (E0–E5)

Artefak aktif E0–E5 tersedia. Notebook terkini terdapat di [`notebooks/`](notebooks/); status validasi dan batas klaim setiap run dijelaskan pada [hasil RQ/hipotesis](docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md). Angka historis pada rencana mingguan di bagian berikut tidak menggantikan tabel hasil aktif.

### E0 — Audit Prapemrosesan
* **Notebook:** [`notebooks/02_E0_Preprocessing_Audit.ipynb`](notebooks/02_E0_Preprocessing_Audit.ipynb)
* Audit formal mencakup 100 rekaman dan memeriksa properti audio, dekode, serta panjang potongan setelah prapemrosesan. E0 bukan eksperimen retrieval atau representasi $R_0$.
* Hasilnya tersimpan pada [`results/tables/01_e0_summary.csv`](results/tables/01_e0_summary.csv); H5 dinilai dari perbandingan E1, bukan dari E0 saja.

### E1 — Clean Retrieval Benchmark
* **Notebook:** [`notebooks/04_E1_Clean_Retrieval.ipynb`](notebooks/04_E1_Clean_Retrieval.ipynb)
* Menguji 311 kueri bersih terhadap 673 rekaman galeri lintas 20 spesies:

| Kode | Representasi | Dimensi | Top-1 Accuracy (%) | mAP@10 | MRR | Precision@10 | Recall@10 |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **$R_2$** | **BirdNET Backbone V2.4** | 1024-d | **81.67%** | **0.6367** | **0.8652** | **0.6939** | **0.2331** |
| **$R_1$** | **PANNs CNN14** | 2048-d | 37.62% | 0.1763 | 0.5070 | 0.2585 | 0.0842 |
| **$R_0$** | **MFCC Baseline** | 40-d | 18.33% | 0.0694 | 0.3109 | 0.1312 | 0.0363 |
| **$R_3$** | **Random Control** | 40-d | 6.43% | 0.0211 | 0.1639 | 0.0569 | 0.0141 |

E1 R0 memiliki run tersendiri; E1 R1–R3 dikonsolidasikan dari cache clean tervalidasi dan tidak diklaim sebagai run historis yang sebelumnya sudah ada.

### E2 — Controlled Paired Noise Degradation
* **Notebook:** [`notebooks/05_E2_Controlled_Noise.ipynb`](notebooks/05_E2_Controlled_Noise.ipynb)
* Uji stres pada 311 kueri berpasangan dengan derau fisik ITERA:

| Kondisi | SNR | $R_2$ BirdNET mAP@10 (Retensi) | $R_1$ PANNs mAP@10 (Retensi) | $R_0$ MFCC mAP@10 (Retensi) | $R_3$ Random mAP@10 |
|---|:---:|:---:|:---:|:---:|:---:|
| **Clean** | $\infty$ | 0.6367 (100.0%) | 0.1763 (100.0%) | 0.0694 (100.0%) | 0.0211 |
| **SNR +20 dB** | 20 dB | 0.6378 (100.2%) | 0.1849 (104.9%) | 0.0770 (110.9%) | 0.0211 |
| **SNR +10 dB** | 10 dB | 0.6213 (97.6%) | 0.1721 (97.7%) | 0.0604 (87.1%) | 0.0211 |
| **SNR 0 dB** | 0 dB | 0.5549 (87.1%) | 0.1188 (67.4%) | 0.0323 (46.6%) | 0.0211 |
| **SNR -5 dB** | -5 dB | **0.4832 (75.9%)** | **0.0863 (49.0%)** | **0.0232 (33.4%)** | 0.0211 |

> **Temuan E2:** Pada SNR -5 dB, retensi mAP@10 BirdNET adalah **75,9%**, PANNs **49,0%**, dan MFCC **33,4%**. Hasil uji statistik dan batas klaim H1/H2 dijelaskan di [dokumen hasil](docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md).

### E3 — Open-Set Threshold Calibration & Transfer
* **Notebook:** [`notebooks/06_E3_Open_Set_Threshold.ipynb`](notebooks/06_E3_Open_Set_Threshold.ipynb)
* Ambang batas $\tau^*$ dioptimasi pada subset kalibrasi ($N=465$, 232 target + 233 unknown) via Youden's J ($J = \text{TPR} - \text{FPR}$) dan **dibekukan**:
  * **$R_2$ BirdNET:** $\tau^* = 0.7028$ (AUROC kalibrasi 0.7600; Youden J 0.4188).
  * **$R_1$ PANNs:** $\tau^* = 0.8974$ (AUROC kalibrasi 0.7098; Youden J 0.3723).
  * **$R_0$ MFCC:** $\tau^* = 0.9958$ (AUROC kalibrasi 0.5332; Youden J 0.0995).
  * **$R_3$ Random Control:** $\tau^* = 0.4888$ (AUROC kalibrasi 0.5452; Youden J 0.0874).
* **Hasil Pengujian Transfer:** Lihat [tabel transfer ambang batas beku](results/tables/13_e3_threshold_transfer.csv); ambang tidak disetel ulang berdasarkan kondisi uji.

### E4 — Sensitivitas Profil Noise Lima Lokasi ITERA

- Lima lokasi: Kebun Raya, Embung F, Gedung F, Masjid At-Tanwir, sekitar GKU 1.
- Desain: 311 query × 5 lokasi × 4 SNR × 4 ulangan per representasi; E4 tidak diulang.
- Tersedia 320 snapshot kondisi dan 99.520 baris evaluasi noisy untuk R0–R3, di luar baseline clean. Ini evaluasi berulang atas 311 query, bukan 99.520 query independen.
- Uji sensitivitas 15 Oktober melengkapi ayunan retensi dengan ayunan absolut. Pada −5 dB, ayunan absolut R1 = 0,045596 dan R2 = 0,061829. Tanpa Kebun Raya, ayunan relatif R1 = 0,065937 dan R2 = 0,083724; CI selisih mencakup nol.
- [Notebook E4](notebooks/07_E4_Habitat_Noise_Sensitivity.ipynb), [hasil sensitivitas lengkap](results/reproductions/H3_sensitivity_20261015/), dan [penjelasan revisi](docs/REVISION_SUPERVISOR_2026-10-15.md).
- Peran biofoni serangga atau distorsi frekuensi adalah dugaan; mekanisme itu belum diuji terhadap fitur segmen noise.

### E5 — Analisis Kasus Kegagalan Terstratifikasi
* **Notebook:** [`notebooks/08_E5_Failure_Diagnostics.ipynb`](notebooks/08_E5_Failure_Diagnostics.ipynb)
* Diagnostik memakai data E2/E3 dan raw E4 yang tersedia; [ringkasan moda kegagalan](results/tables/15_e5_failure_mode_summary.csv) serta [120 kasus pilihan](results/tables/16_e5_selected_case_manifest.csv) tersimpan terpisah. Identitas Top-1 atau margin yang tidak tersedia pada E4 ditandai sebagai tidak tersedia, bukan ditebak.
* **Audit pendengaran 30 Oktober:** [120/120 kasus mempunyai catatan Fabio](Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md), dengan satu koreksi E5_105 yang dikonfirmasi. Query dinyatakan terdengar pada 116 kasus; Top-1 pada 109 kasus. Sampel mencakup 80 query unik dan 117 pasangan query–kondisi; hitungan deskriptif satu pendengar ini tidak mengestimasi tingkat kegagalan populasi atau mengesahkan identitas spesies secara independen.

---

## 8. Struktur Direktori Repositori

[Peta proyek aktif](PROJECT_STRUCTURE.md) memuat daftar file dan fungsi setiap folder. Titik masuk utama:

| Kebutuhan | Lokasi |
|---|---|
| Notebook E0–E5 dan cara membaca hasil | [notebooks/README.md](notebooks/README.md) |
| Runner eksperimen dan analisis | [scripts/README.md](scripts/README.md) |
| Manifes target, unknown, dan noise | [data/manifests/](data/manifests/) |
| Hasil sumber yang dibekukan | [results/reproductions/](results/reproductions/) |
| Naskah teori dan manuskrip | [paper/teori_dasar.md](paper/teori_dasar.md), [paper/manuscript.md](paper/manuscript.md) |
| Progres dan status bimbingan | [Indeks bimbingan terbaru](Rencana-eksperimen-bimbingan/README.md); CURRENT_STATUS 18 Oktober masih memuat status audit lama |
| Audit pendengaran E5 | [Petunjuk audit](Rencana-eksperimen-bimbingan/audit-pendengaran-E5/README.md) |
| Bahan BAB 1–3, diagram alir, dan indeks gambar/tabel | [Paket persiapan penulisan](paper/persiapan_bab1_3/README.md) |

---

## 9. Petunjuk Eksekusi Cepat (Quick Start)

Siapkan Python dan input eksternal yang sesuai manifes/checksum. Audio, checkpoint, dan embedding tidak ikut dalam klon Git.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -B run_tests.py
```

Pemeriksaan 18 Oktober 2026: total 41 tes, **41 lulus, 0 dilewati, 0 gagal, 0 error**. Tes yang kehilangan input/dependensi kini dilaporkan sebagai skipped, bukan lulus. Ini pemeriksaan integritas/metode, bukan pengganti pengujian ulang pipeline dari audio.

Pemeriksaan audit 30 Oktober mencatat **7 tes importer/finalizer lulus**, bukan eksekusi ulang seluruh suite. Bukti tes dan 41 pembandingan reproduksi merupakan hitungan yang berbeda; pembaruan README ini tidak menjalankan tes atau eksperimen lagi.

Untuk meninjau hasil, buka notebook dan artefak tersimpan. Untuk mengulang statistik H3 saja:

```powershell
.\.venv\Scripts\python.exe -B scripts/run_h3_sensitivity_reanalysis.py --output-dir results/reproductions/H3_reproduction_new
```

Gunakan direktori keluaran baru. E4 historis tidak dijalankan ulang pada revisi pembimbing ini. Instruksi cache clean dan identitas sumber tersedia pada [panduan teknis E4](docs/protocols/e4-cache-reproduction.md).

---

## 10. Lisensi dan Etika Penelitian

1. **Kode Program:** Dilisensikan di bawah lisensi terbuka [MIT License](LICENSE).
2. **Audio Xeno-Canto:** Hak cipta rekaman audio dipegang oleh masing-masing perekam (*recordist*) di Xeno-Canto dengan lisensi Creative Commons (CC BY-NC-SA, CC BY-NC-ND). Rincian atribusi lengkap terdokumentasi di `data/manifests/download_manifest.csv`. Berkas audio tidak disertakan dalam repositori Git publik.
3. **Rekaman Derau Lapangan ITERA:** Hak cipta rekaman AudioMoth dipegang oleh tim peneliti Institut Teknologi Sumatera (ITERA).

---

## 11. Aturan Reproducibility & Integritas Data

Setiap eksekusi (*run*) eksperimen wajib mencatat parameter minimal berikut:

```text
run_id
representation (R0, R1, R2, R3)
checkpoint/version
query_id
gallery_manifest_version
noise_id / noise_file
SNR (Clean, +20, +10, 0, -5 dB)
random_seed (default: 42)
threshold_version (tau beku)
ranking (Top-k candidates)
metrics (mAP@10, Top-1, MRR, FPR, Recall)
runtime (detik)
```

Setiap klaim pada artikel ilmiah dan naskah skripsi harus dapat ditelusuri (*fully traceable*):

```text
Research Question (RQ)
       ↓
Eksperimen (E0 s.d. E5)
       ↓
Hasil Mentah (results/reproductions/<run>/raw/ atau tables/per_query.csv)
       ↓
Hasil Terproses (results/reproductions/<run>/tables/)
       ↓
Tabel & Gambar Laporan (results/tables/ & results/figures/; indeks di paper/)
       ↓
Klaim Saintifik di Naskah (paper/manuscript.md)
```

### Kebijakan Data dan Version Control (Git):
* **Wajib di-version-control:** Manifes (`.csv`, `.json`), metadata (`.xlsx`), berkas *hash* integritas (`SHA-256`), konfigurasi (`.yaml`), kode program (`src/`, `scripts/`), dan ringkasan metrik hasil.
* **Dilarang di-commit ke Git (.gitignore):** Berkas audio mentah berukuran besar (`*.mp3`, `*.wav`, `*.flac`), *checkpoint weights* deep learning besar (`*.pth`), dan direktori cache embedding sementara (`.npz` di luar rilis resmi).

---

## 12. Rencana Kerja Satu Bulan & Timeline Pelaksanaan

| Tahap | Protokol aktif | Status |
|---|---|---|
| Minggu 1 / Gate 1 | Korpus 20 spesies; split internal target 673/311/232; preprocessing; E0; clean retrieval E1 R0–R3 | Keluaran komputasional tersedia |
| Minggu 2 / Gate 2 | E2 pada clean, +20, +10, 0, −5 dB; pairing noise deterministik | Keluaran komputasional tersedia |
| Minggu 3 / Gate 3 | E3 calibration-clean dan threshold beku; E4 lima lokasi × empat SNR × empat ulangan | Keluaran tersedia; inferensi sesuai scope controlled mixture |
| Minggu 4 / Gate 4 | Bootstrap query berpasangan; audit manusia E5; reproduksi; finalisasi naskah | Statistik, reproduksi yang diizinkan, dan catatan audit 120/120 tersedia; finalisasi naskah/persetujuan masih terbuka |

Analisis H3 dan sensitivitas memakai 10.000 bootstrap, seed 20261012. Catatan manusia 120 kasus E5 tersedia pada laporan 30 Oktober, terpisah dari hasil otomatis dan lembar kosong persiapan. Rumusan H3/H4 setelah hasil ditandai eksploratif.

---

## 13. Definition of Done (Status Kelulusan Gate 1 s.d. Gate 4)

**Status dokumentasi: 30 Oktober 2026.** Reproduksi E0/E1/E2/E3/E5 pada venv baru serta statistik H3 selesai dalam scope revisi; inferensi E4 tidak diulang. [Catatan audit manusia 120/120](Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md) tersedia. Bukti cukup untuk mulai menulis, tetapi Gate 4 tidak otomatis disahkan: naskah dan keputusan akhir pembimbing tetap perlu diselesaikan. Entri lama pada [catatan bimbingan](Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md) dibaca sesuai tanggalnya.

- [x] **Daftar taksa & spesies target dibekukan:** 20 spesies avifauna Indonesia, 1.216 rekaman pada manifes aktif beserta catatan SHA-256 dan audit sebelumnya (DEC-13).
- [x] **Pemisahan internal target terverifikasi:** 0 recording ID, file path, dan nama perekam beririsan antar Gallery, Query, dan Calibration. Ini tidak membuktikan independensi sesi/perekam unknown atau bebas overlap data pralatih.
- [x] **Baseline klasik MFCC selesai:** cache R0 Gallery 673 × 40 dan Query 311 × 40 terverifikasi.
- [x] **Generic pretrained representation selesai:** cache R1/PANNs Gallery 673 × 2.048 dan Query 311 × 2.048 terverifikasi.
- [x] **Bioacoustic domain representation selesai:** cache R2/BirdNET Gallery 673 × 1.024 dan Query 311 × 1.024 terverifikasi.
- [x] **Clean retrieval E1 selesai:** R2 (mAP@10 0,6367; Top-1 81,67%) > R1 (0,1763; 37,62%) > R0 (0,0694; 18,33%) > R3 (0,0211; 6,43%).
- [x] **Empat kondisi derau E2 selesai:** +20, +10, 0, −5 dB dengan noise fisik ITERA; retensi R2 pada −5 dB 75,88%.
- [x] **Cakupan metrik retrieval diperiksa:** AP@k/Recall@k untuk k = 1, 5, 10 tersedia pada 20 CSV E2 dan empat CSV raw E4; metrik primer tetap mAP@10.
- [x] **Threshold beku dari calibration-clean tersedia:** τ*(R2) = 0,702785; τ*(R1) = 0,897416; τ*(R0) = 0,995752; τ*(R3) = 0,488838. Threshold tidak diubah pada revisi.
- [x] **Metrik open-set E3 tersedia:** FPR, recall penerimaan known, AUROC, AUPRC, dan F1-score per SNR. Recall penerimaan tidak disamakan dengan ketepatan spesies Top-1.
- [x] **E4 lima lokasi dan sensitivitas H3 selesai:** 311 query × 5 lokasi × 4 SNR × 4 ulangan per representasi; ayunan absolut/relatif dan subset tanpa Kebun Raya dilaporkan. Kesimpulan H3/H4 hasil reformulasi bersifat eksploratif dan dibatasi oleh metrik serta subset.
- [x] **Kasus E5 komputasional disiapkan:** 120 baris pilihan tersedia; lembar audit terpisah memulihkan representasi, kondisi, dan moda kegagalan melalui pencocokan persis dengan diagnostik lengkap. Sumber E5 tidak ditimpa.
- [x] **Catatan audit pendengaran tersedia untuk 120/120 kasus pilihan E5:** Fabio mengisi pengamatan pada 25–30 Oktober; ekspor berstatus reviewed seluruhnya, dengan satu koreksi E5_105 terkonfirmasi. Lembar awal tetap kosong sebagai sumber persiapan. Satu pendengar, sampel kegagalan terpilih, dan ambiguitas catatan tetap menjadi batas interpretasi; lihat [hasil audit](Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md).
- [x] **CI 95% tersedia dengan batas inferensi:** H3/sensitivitas memakai 10.000 bootstrap query berpasangan; CI eksploratif kondisional pada lokasi dan segmen noise tetap. Tidak ada klaim mekanisme spektral sudah terbukti.
- [x] **Suite integritas/metode terpadu lulus:** total 41 tes: **41 lulus, 0 dilewati, 0 gagal, 0 error** melalui run_tests.py pada 18 Oktober 2026. Empat dimensi representasi diuji terpisah; SkipTest dan ringkasan hasil tidak menghitung tes dilewati sebagai lulus.
- [x] **Reproduksi pada lingkungan baru dalam scope revisi:** klon terpisah, venv baru, pemulihan 3.289 input terverifikasi, tanpa embedding lama; E0, ekstraksi clean R0–R3, E1, E2, E3, E5, serta statistik H3 selesai. Seluruh 41 perbandingan cocok, selisih numerik maksimum 0,0. [Bukti dan protokol](docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md).
- **Batas reproduksi, di luar pekerjaan revisi aktif:** run ulang seluruh E0–E5 termasuk inferensi E4 tidak dilakukan, sesuai arahan pembimbing. Ini bukan syarat baru sebelum menulis dan bukan klaim reproduksi penuh. Input eksternal dipulihkan dari arsip lokal, bukan diunduh ulang.
- [ ] **Finalisasi naskah dan persetujuan pembimbing:** judul/RQ final, framing eksploratif H3/H4, sistematika, sitasi, serta isi BAB 1–5 belum dinyatakan selesai. [Bahan BAB 1–3](paper/persiapan_bab1_3/README.md) tersedia; template bab masih kerangka.
- [x] **Batas ekologis dinyatakan sesuai scope:** E2/E4 menguji additive mixture, bukan vokalisasi target in-situ. Pengumpulan/anotasi korpus burung in-situ bukan prasyarat revisi E4 aktif dan tetap di luar scope.

**Verifikasi tambahan:** 19 aset identitas E4 dan 320 snapshot kondisi cocok checksum; 41 bahan laporan lama tetap cocok. CSV hasil H3 dari klon bersih identik byte dengan hasil revisi. Klon H3-only pada pemeriksaan sebelumnya tidak membawa audio/cache; klon reproduksi baru dimulai tanpa embedding, lalu menerima salinan audio/checkpoint terverifikasi dan membangun embedding baru. Tiga helper identitas E4 kini juga dipertahankan byte-for-byte oleh Git.

---

## 14. Publication Boundary

Artikel ilmiah dan naskah skripsi ini secara ketat difokuskan untuk menjawab:  
**"Ketahanan representasi audio beku terhadap degradasi derau aditif dan stabilitas ambang batas temu kembali bioakustik."**

Rekaman ITERA dipakai sebagai sumber noise untuk pencampuran aditif terkontrol. E4 menguji sensitivitas profil noise lima lokasi, bukan inventarisasi biodiversitas atau rekaman vokalisasi target in-situ. Korpus target in-situ dan anotasinya merupakan penelitian terpisah, bukan pekerjaan wajib untuk menuntaskan E4 aktif.

### Ancaman terhadap Validitas (Threats to Validity):
1. **Potensi Kebocoran Pra-latih (Pretraining Data Overlap - H1/H2):**  
   Model BirdNET dipra-latih pada korpus global masif yang sebagian besar bersumber dari repositori publik Xeno-Canto dan Macaulay Library. Meskipun partisi internal evaluasi kami menerapkan *strict author-disjoint* mutlak antara galeri, kueri, dan kalibrasi, terdapat kemungkinan rekaman vokal dari 20 spesies Indonesia ini pernah terpapar pada fase pra-latih BirdNET. Hal ini dapat memberikan keunggulan representasi induktif terhadap fitur kicauan burung target dibanding model audio umum (PANNs) yang dilatih pada AudioSet.
2. **Keterwakilan Spesies Terpilih (Selection Bias - DEC-10):**  
   Taksa target dibatasi pada 20 spesies umum dan tersebar luas dengan ketersediaan rekaman memadai ($\ge 30$ klip, $\ge 14$ perekam). Spesies langka, pemalu (*cryptic*), atau bernada rendah ekstrem belum tercakup dalam benchmark ini.
3. **Pencampuran Aditif vs Propagasi Lapangan (In-situ Soundscape Gap - H3):**  
   Pengujian E2 dan E4 menggunakan derau aditif terkontrol. Dinamika propagasi bentang alam riil (atenuasi jarak, penyerapan kelembapan udara kanopi tropis, dan difraksi multipath) belum diuji; ini adalah H3 asli yang berbeda dari reformulasi eksploratif tentang profil noise lokasi.

---

## 15. Catatan dan Arahan Dosen Pembimbing

Alur aktif penelitian:

```text
Audio target Indonesia + manifes/hash
  → preprocessing: mono 32 kHz, jendela energi 5 detik, RMS 0,05
  → Gallery 673 | Query 311 | Calibration 232 (perekam target terpisah)
  → representasi beku R0/MFCC, R1/PANNs, R2/BirdNET, R3/kontrol ID
  → cosine retrieval pada gallery yang sama
  → E1 clean
  → E2 query berpasangan pada +20, +10, 0, −5 dB
  → E3 calibration-clean → threshold beku → transfer ke test
  → E4 lima lokasi ITERA × empat SNR × empat ulangan
  → E5 diagnostik kegagalan + audit pendengaran manusia
  → bootstrap berpasangan, pelaporan hasil dan batas inferensi
```

Tautan aktif untuk dibagikan: [indeks bimbingan](Rencana-eksperimen-bimbingan/README.md) dan [hasil audit E5 30 Oktober](Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md). [Catatan Progres Bimbingan](Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md) tetap menjadi kronologi; status 0/120 pada entri lama sudah digantikan laporan audit. Empat dokumen yang sebelumnya dihapus tidak dipulihkan.

Arahan revisi pembimbing yang berlaku:

1. E4 menggunakan kelima lokasi. Tidak ada pengulangan E4 untuk revisi ini.
2. Skrip produsen asli dipertahankan dengan SHA-256 yang sama; cache besar tidak di-commit.
3. H3 melaporkan ayunan mAP@10 absolut, retensi relatif, serta sensitivitas tanpa Kebun Raya. Kesimpulan tidak digeneralisasi ke seluruh SNR/metrik/subset.
4. Biofoni serangga dan distorsi frekuensi tetap dugaan sampai diuji terhadap fitur berkas noise. Perbedaan lokasi tidak membuktikan penyebab ekologis.
5. H3/H4 hasil reformulasi diberi label eksploratif; rumusan asli dan tanggal perubahan dicatat.
6. Teori Dasar ditulis pada naskah sendiri: Bagian 2.8, gap E4−E2, Gambar 6/8, gallery 673, dan enam konfigurasi AudioMoth pada Bagian 3.6 telah disesuaikan.
7. Poin 1–3 sudah dipush untuk pemeriksaan ulang pembimbing. Persetujuan pembimbing dan finalisasi naskah tidak diasumsikan dari kelulusan tes.

---

## 16. Panduan Teknis Lab & Protokol Gate 2–4

### Gate 2 — E2 controlled-noise robustness

- Pakai query yang sama, gallery tetap, dan noise fisik dari pool mixing yang terpisah dari noise unknown E3.
- Grid tetap clean, +20, +10, 0, −5 dB. Simpan path/seed/posisi segmen, SNR aktual, dan metrik per query.
- Laporkan skor absolut bersama retensi. Retensi R3 bukan ukuran ketahanan akustik karena kontrol tidak membaca waveform.

### Gate 3 — E3 dan sensitivitas E4

- Calibration: 232 known + 233 unknown. Test: 311 known + 310 unknown. Unknown aktif terdiri atas burung non-target dan noise ITERA sesuai manifes.
- Threshold hasil E3: R0 0,995752; R1 0,897416; R2 0,702785; R3 0,488838. Revisi pelaporan tidak mengubah threshold operasional.
- Recall penerimaan known berbeda dari akurasi spesies. Pada R2, recall clean 0,604502 turun ke 0,254019 pada −5 dB, dan FPR turun dari 0,222581 ke 0,129032.
- E4: Kebun Raya, Embung F, Gedung F, Masjid At-Tanwir, Sekitar GKU 1. Kelima lokasi dipertahankan; penghilangan setiap lokasi secara bergantian hanya analisis sensitivitas, dengan [tabel lengkap](results/reproductions/H3_leave_one_location_out_20261018/README.md).
- Ayunan dihitung per ulangan kemudian dirata-ratakan. Pada −5 dB, ayunan absolut R1 0,045596 dan R2 0,061829. Klaim R2 selalu lebih sempit tidak digunakan.

### Gate 4 — audit, inferensi, reproduksi, dan penulisan

- Catatan audit 120 kasus E5 sudah tersedia beserta identitas pendengar, tanggal, observasi, ketidakpastian, dan jejak koreksi. Untuk audit tambahan gunakan segmen yang sama dengan eksperimen serta simpan keluaran baru; catatan manusia tidak diisi otomatis dari skor model.
- Bootstrap H3 memakai 10.000 iterasi, seed 20261012, unit query, dan pairing lintas representasi/lokasi/SNR/ulangan. Hasil reformulasi eksploratif dan kondisional pada lokasi/segmen tetap.
- Reproduksi harus membedakan tes integritas, analisis ulang CSV, dan ekstraksi/evaluasi ulang dari audio pada lingkungan baru. Bukti parsial tidak dicatat sebagai reproduksi penuh.
- Naskah dan gambar mengikuti hasil aktif. Periksa konsistensi abstrak, metode, hasil, kesimpulan, dan batas generalisasi sebelum meminta persetujuan pembimbing.

---

## 17. Register Keputusan (DEC), Checklist Audit, & Catatan Provenans

Register keputusan kanonik tersedia pada [decision-log.md](docs/research/decision-log.md). DEC-13 mencatat pivot korpus Indonesia, DEC-14 pemisahan bank noise, dan DEC-16 koreksi pelaporan pembimbing. DEC-15 merupakan keputusan historis sebelum perluasan analisis H3; kesimpulan aktif mengikuti DEC-16 serta [riwayat hipotesis](docs/research/hypotheses.md).

Checklist aktif berada pada §13. Bukti historis dirinci pada [catatan bimbingan](Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md); status audit terbaru mengikuti [laporan 30 Oktober](Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md). Rencana kerja dan lembar pending lama tidak menggantikan hasil tersebut.

Arahan dosen merupakan bahan penyusunan dan pemeriksaan penelitian. Draf rujukan dosen tidak diperlakukan sebagai hasil eksperimen mahasiswa. Run sumber, manifes, konfigurasi beku, dan checksum tetap menjadi rujukan utama untuk angka hasil.

[Petunjuk audit pendengaran dan bahan penjelasan lisan H3/Recall@10](Rencana-eksperimen-bimbingan/PANDUAN_AUDIT_E5_DAN_PENJELASAN_LISAN.md).
