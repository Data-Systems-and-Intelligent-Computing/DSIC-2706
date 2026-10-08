# Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise

**Fabio Banyu Cyto** (123450104)  
*DSIC Research Group, Program Studi Sains Data, Institut Teknologi Sumatera*  

**Status Naskah:** Naskah Lengkap Final (Gate 1-R s.d. Gate 4 Tuntas 100%). Seluruh eksperimen E1 hingga E5 telah selesai dieksekusi pada korpus resmi BirdCLEF+ 2026 (20 Spesies Neotropis) dan bank derau fisik AudioMoth ITERA (1.799 berkas WAV).

---

## Abstract
Passive acoustic monitoring generates large volumes of unannotated audio, but the robustness of frozen audio representations for similarity retrieval under environmental noise and domain shift is still poorly quantified. This study evaluates four frozen representations on a **BirdCLEF+ 2026** gallery of 20 avian taxa (4,351 clips): hand-crafted MFCC (40-d), generic PANNs CNN14 (2048-d), bioacoustic BirdNET V2.4 (1024-d), and a random-vector control (40-d). All embeddings are $\ell_2$-normalised and ranked by cosine similarity under a **strict global recordist-disjoint** split (gallery 3,653 / query 200 / calibration 498; zero author, recording-id, and filepath overlap). 

Under clean queries (**E1**), BirdNET achieves Top-1 accuracy **95.0%**, mAP@10 **0.9126**, and MRR **0.9658**, substantially outperforming PANNs (60.0%, 0.4152) and MFCC (27.5%, 0.1319). When stressed with paired real tropical noise recorded via AudioMoth at ITERA (**E2**, SNR grid +20 dB to -5 dB), BirdNET exhibits exceptional resilience, retaining **84.45%** of its clean performance at severe -5 dB SNR (mAP@10 = 0.7707), whereas PANNs collapses to 35.65% (mAP@10 = 0.1480). Open-set calibration (**E3**) confirms that a frozen threshold $\tau^* = 0.50$ stably rejects environmental noise and non-target taxa across degraded conditions. Stress-testing under real tropical forest soundscapes (**E4**) reveals a minimal domain shift gap ($\Delta mAP@10 = -0.0101$ at -5 dB). Failure analysis (**E5**) indicates that 66.7% of errors stem from physical low-SNR masking. Finally, 1,000-iteration paired bootstrap resampling proves that BirdNET's superiority over generic audio is statistically significant ($p = 0.0000 < 0.05$, 95% CI $[+0.4285, +0.5621]$).

**Keywords:** Bioacoustic Retrieval, Representation Robustness, Domain Shift, BirdCLEF+ 2026, AudioMoth, Open-Set Rejection, BirdNET, Bootstrap Resampling.

---

## 1. Introduction & Research Questions (RQ)
Pemantauan akustik pasif (*passive acoustic monitoring* / PAM) menghasilkan volume audio yang sangat besar namun minim anotasi. Sebagian besar penelitian machine learning berfokus pada klasifikasi tertutup (*closed-set classification*), yang mengasumsikan seluruh rekaman berasal dari kelas latih yang diketahui. Penelitian ini membedah paradigma temu kembali kemiripan (*similarity retrieval*) berbasis representasi audio beku (*frozen representations*) dengan 5 Pertanyaan Penelitian Utama (*Research Questions* / RQ):

* **RQ1 (Baseline Retrieval Performance):** Sejauh mana representasi audio beku ($R_0$ MFCC, $R_1$ PANNs, $R_2$ BirdNET) mampu mengenali spesies burung pada kueri bersih tanpa derau (*Clean Baseline*) dalam skema *strict recordist-disjoint*?
* **RQ2 (Noise Robustness & Retention):** Bagaimana dinamika ketahanan performa (*noise retention*) masing-masing representasi ketika kueri yang sama mengalami degradasi derau aditif nyata kampus ITERA pada berbagai tingkatan SNR (+20 dB hingga -5 dB)?
* **RQ3 (Open-Set Threshold Rejection):** Apakah nilai ambang batas kemiripan kosinus ($\tau^*$) yang dikalibrasi pada partisi terpisah mampu secara stabil menolak sinyal asing (*unknown fauna* & derau latar) di bawah degradasi derau ekstrem?
* **RQ4 (Real Soundscape Domain Shift):** Seberapa besar kesenjangan performa (*domain shift gap*) ketika derau aditif terkontrol kampus ITERA digantikan oleh rekaman bentang alam asli hutan tropis (*real soundscape*)?
* **RQ5 (Failure Diagnosis & Statistical Significance):** Apa faktor utama penyebab kegagalan temu kembali pada kueri nyata, dan apakah keunggulan representasi bioakustik atas representasi generik signifikan secara statistik ($p < 0.05$)?

---

## 2. Methodology & Experimental Setup

### 2.1 Formulasi Kemiripan Kosinus & Retensi
Setiap klip audio $x$ dinormalisasi ke sampling rate 32 kHz, dipotong pada jendela energi tertinggi 5.0 detik, dinormalisasi energi RMS 0.05, dan dipetakan ke vektor representasi beku $e = f(x)$ ternormalisasi $\ell_2$ unit ($\|e\|_2 = 1$). Kemiripan kosinus didefinisikan:
$$\mathrm{sim}(q, g) = e_q^\top e_g$$
Retensi berpasangan pada kondisi derau SNR didefinisikan:
$$\mathrm{Retention}_m(\mathrm{SNR}) = \frac{\mathrm{mAP@10}_m(\mathrm{SNR})}{\mathrm{mAP@10}_m(\mathrm{clean})} \times 100\%$$

### 2.2 Korpus Data & Partisi Bebas Bocor (*Zero Leakage*)
Menggunakan 20 taksa burung Neotropis dari BirdCLEF+ 2026 (total 4.351 berkas audio fisik). Partisi data dikunci secara global pada `seed=42`:
* **Gallery:** 3.653 rekaman audio dari 377 perekam (*author*) unik.
* **Query Clean:** 200 rekaman audio dari 68 perekam (*author*) unik (tepat 10 klip per spesies).
* **Calibration:** 498 rekaman audio dari 95 perekam (*author*) unik.
* *Integritas Partisi:* $\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset$ (Tepat 0 author overlap, 0 ID overlap, 0 filepath overlap, diverifikasi oleh `tests/run_all_tests.py`).

### 2.3 Bank Derau Fisik AudioMoth ITERA
Bank derau terdiri atas **1.799 berkas audio WAV fisik** yang direkam di 5 lokasi lingkungan kampus ITERA (Masjid At-Tanwir, Embung E, Kebun Raya, Gedung F, GKU 1). Sesuai mandat DEC-09, seluruh derau sintetis (*pink noise*) telah dihapus. Manifes lengkap dienkripsi dengan checksum SHA-256 pada `data/manifests/itera_noise_manifest.csv`.

---

## 3. Hasil Eksperimen Empiris & Pembahasan (Menjawab RQ1 - RQ5)

### 3.1 Jawaban RQ1: Tolok Ukur Temu Kembali Bersih (Eksperimen E1)
Tercatat pada `paper/tables/clean_retrieval_table.csv`:

| Kode | Arsitektur | Dimensi | Top-1 (%) | mAP@10 | MRR | Precision@10 | Recall@10 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$** | **BirdNET V2.4 Backbone** | 1024-d | **95.0%** | **0.9126** | **0.9658** | **0.9280** | **0.0528** |
| **$R_1$** | **PANNs CNN14** | 2048-d | 60.0% | 0.4152 | 0.7005 | 0.5025 | 0.0291 |
| **$R_0$** | **MFCC Baseline** | 40-d | 27.5% | 0.1319 | 0.4224 | 0.2175 | 0.0123 |
| **$R_3$** | **Random Control** | 40-d | 6.5% | 0.0190 | 0.1779 | 0.0530 | 0.0028 |

*Pembahasan RQ1:* $R_2$ (BirdNET) mendominasi seluruh metrik retrieval dengan Top-1 95.0% dan mAP@10 0.9126. Keberhasilan ini membuktikan efektivitas representasi laten yang dilatih khusus pada domain bioakustik burung dalam memetakan variasi vokal antar-individu tanpa proses *fine-tuning*.

---

### 3.2 Jawaban RQ2: Ketahanan Derau Terkontrol (Eksperimen E2)
Tercatat pada `paper/tables/snr_robustness_table.csv` dan `paper/figures/e2_snr_robustness_curve.png`:

| Representasi | Clean | SNR 20 dB | SNR 10 dB | SNR 0 dB | SNR -5 dB | Retensi Relatif (-5 dB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET)** | **0.9126** | **0.9068** | **0.8858** | **0.8317** | **0.7707** | **84.45%** |
| **$R_1$ (PANNs)** | 0.4152 | 0.3816 | 0.2922 | 0.1918 | 0.1480 | 35.65% |
| **$R_0$ (MFCC)** | 0.1319 | 0.1244 | 0.0765 | 0.0502 | 0.0364 | 27.60% |
| **$R_3$ (Random)** | 0.0190 | 0.0137 | 0.0134 | 0.0160 | 0.0171 | - |

*Pembahasan RQ2:* $R_2$ menunjukkan ketahanan luar biasa dengan retensi **84.45%** pada SNR -5 dB. Sebaliknya, $R_1$ runtuh hingga tersisa 35.65% dan $R_0$ tersisa 27.60%. Hal ini membuktikan bahwa bobot filter konvolusi BirdNET memiliki sensitivitas selektif terhadap kontur harmoni vokal burung, mengabaikan energi derau broadband lingkungan kampus ITERA.

---

### 3.3 Jawaban RQ3: Kalibrasi Ambang Batas Open-Set (Eksperimen E3)
Tercatat pada `paper/tables/threshold_transfer_table.csv`:
* Ambang batas optimal dibekukan pada $\tau^* = \mathbf{0.5000}$ via optimasi Youden's Index ($J = 0.7240$ pada $R_2$) menggunakan 498 klip kalibrasi independen.
* *Pembahasan RQ3:* Kriteria penolakan $\max_{g} \mathrm{sim}(q, g) < \tau^*$ terbukti mempertahankan False Positive Rate terkontrol hingga SNR -5 dB karena representasi BirdNET memproyeksikan suara non-burung (amfibi, serangga, derau mesin) pada ruang laten yang ortogonal terhadap manifold burung target.

---

### 3.4 Jawaban RQ4: Kesenjangan Pergeseran Domain Real Soundscape (Eksperimen E4)
Tercatat pada `paper/tables/e4_domain_shift_table.csv` dan `paper/figures/e4_domain_shift_bar.png`:

| Kondisi SNR | $mAP@10$ (Derau ITERA / E2) | $mAP@10$ (Soundscape Hutan / E4) | Domain Shift Gap ($\Delta mAP$) |
| :--- | :---: | :---: | :---: |
| **Clean** | **0.9126** | **0.9126** | 0.0000 |
| **SNR +20 dB** | 0.9068 | 0.9188 | +0.0120 |
| **SNR +10 dB** | 0.8858 | 0.9026 | +0.0168 |
| **SNR 0 dB** | 0.8317 | 0.8299 | -0.0018 |
| **SNR -5 dB** | **0.7707** | **0.7606** | **-0.0101** |

*Pembahasan RQ4:* Pada kondisi paling buruk (-5 dB), selisih kesenjangan pergeseran domain hanya sebesar **-0.0101** (~1.0%). Hal ini membuktikan sifat *domain-invariance* dari representasi BirdNET: fitur representasi mampu memisahkan kicauan burung baik saat tertutup derau antropogenik kampus ITERA maupun saat tertutup biophony hutan tropis alami.

---

### 3.5 Jawaban RQ5: Diagnosis Kegagalan & Inferensi Statistik (Eksperimen E5)
Tercatat pada `paper/tables/failure_analysis_table.csv` dan `paper/tables/statistical_significance_table.csv`:
1. **Audit Kasus Kegagalan Nyata:**
   * *Low SNR Masking (66.67%):* Derau aditif pada SNR -5 dB menutupi frekuensi vokal burung ($P_{\text{noise}} > P_{\text{signal}}$).
   * *Acoustic Feature Overlap (20.00%):* Kemiripan pola kicauan antar-spesies berkerabat dekat pada kondisi bersih.
   * *Inter-Species Confusion / Short Call (13.33%):* Durasi kicauan terlalu pendek (< 1.0 detik).
2. **Evaluasi Statistik Inferensial (Paired Bootstrap 1.000 Iterasi):**
   * Perbandingan $R_2$ (BirdNET) vs $R_1$ (PANNs):
     * Rata-rata selisih $\Delta mAP@10$: **+0.4974**
     * 95% Confidence Interval: **[+0.4285, +0.5621]**
     * Nilai $p$-value empiris: **0.0000** ($p < 0.05$).
   * *Pembahasan RQ5:* Karena selang kepercayaan tidak memuat angka nol dan $p = 0.0000$, hipotesis nol ($H_0$) ditolak secara tegas. Keunggulan model bioakustik atas model audio generik terbukti signifikan secara statistik mutlak.

---

## 4. Kesimpulan & Rekomendasi
Penelitian ini membuktikan secara empiris dan inferensial bahwa model representasi bioakustik beku (*BirdNET*) memiliki keunggulan mutlak dalam akurasi pencarian kueri bersih (mAP@10 = 0.9126), ketahanan terhadap derau aditif tropis (retensi 84.45% pada -5 dB), kestabilan ambang batas open-set ($\tau^* = 0.50$), serta ketahanan terhadap pergeseran domain bentang alam nyata (gap hanya ~1%). Seluruh data, manifes, kode sumber, dan artefak pengujian telah dibekukan (*code freeze*) pada repositori ini.
