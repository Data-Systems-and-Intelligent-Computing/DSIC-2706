# Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise

**Fabio Banyu Cyto** (123450104)  
*DSIC Research Group, Program Studi Sains Data, Institut Teknologi Sumatera*  

**Status Naskah:** Naskah Lengkap Final Terkoreksi (Gate 1-R s.d. Gate 4 Tuntas & Tersinkronisasi Data Mentah). Seluruh angka pada naskah ini diverifikasi identik hingga digit desimal dengan berkas hasil mentah `results/raw/` dan `results/processed/snr_robustness_table.csv`.

---

## Abstract
Passive acoustic monitoring generates large volumes of unannotated audio, but the robustness of frozen audio representations for similarity retrieval under environmental noise and domain shift is still poorly quantified. This study evaluates four frozen representations on a **BirdCLEF+ 2026** gallery of 20 avian taxa (4,351 clips): hand-crafted MFCC (40-d), generic PANNs CNN14 (2048-d), bioacoustic BirdNET V2.4 (1024-d), and a random-vector control (40-d). All embeddings are $\ell_2$-normalised and ranked by cosine similarity under a **strict global recordist-disjoint** split (gallery 3,653 / query 200 / calibration 498; zero author, recording-id, and filepath overlap). 

Under clean queries (**E1**), BirdNET achieves Top-1 accuracy **95.0%**, mAP@10 **0.9126**, and MRR **0.9658**, substantially outperforming PANNs (60.0%, 0.4152) and MFCC (27.5%, 0.1319). When stressed with paired real tropical noise recorded via AudioMoth at ITERA (**E2**, SNR grid +20 dB to -5 dB), BirdNET exhibits exceptional resilience, retaining **84.45%** of its clean performance at severe -5 dB SNR (mAP@10 = 0.7707). In stark contrast, generic PANNs collapses to **0.0590** (retention **14.22%**, 95% CI $[0.1014, 0.1858]$), falling below hand-crafted MFCC which retains **0.0349** (retention **26.42%**, 95% CI $[0.2081, 0.3337]$). Paired bootstrap testing confirms that the non-overlapping retention CIs reflect a significant failure of generic deep representations under severe environmental noise, indicating that hypothesis H1 holds strictly for domain-specific bioacoustic representations, not deep generic models broadly. At mild noise (+20 dB), PANNs exhibits a slight performance boost (109.16% retention / 0.4533 mAP), consistent with stochastic resonance regularizing generic convolutional feature maps. Stress-testing under real tropical forest soundscapes (**E4**) reveals that BirdNET maintains high robustness across noise sources, though domain shifts must be framed as sensitivity to additive ambient spectral profiles. Paired bootstrap resampling across 1,000 iterations demonstrates that BirdNET's clean retrieval superiority over generic audio is statistically significant ($\Delta mAP = +0.4974$, 95% CI $[+0.4504, +0.5473]$, $p < 0.001$).

**Keywords:** Bioacoustic Retrieval, Representation Robustness, Domain Shift, BirdCLEF+ 2026, AudioMoth, Open-Set Rejection, BirdNET, Bootstrap Resampling.

---

## 1. Introduction & Research Questions (RQ)
Pemantauan akustik pasif (*passive acoustic monitoring* / PAM) menghasilkan volume audio yang sangat besar namun minim anotasi. Sebagian besar penelitian machine learning berfokus pada klasifikasi tertutup (*closed-set classification*), yang mengasumsikan seluruh rekaman berasal dari kelas latih yang diketahui. Penelitian ini membedah paradigma temu kembali kemiripan (*similarity retrieval*) berbasis representasi audio beku (*frozen representations*) dengan 5 Pertanyaan Penelitian Utama (*Research Questions* / RQ):

* **RQ1 (Baseline Retrieval Performance):** Sejauh mana representasi audio beku ($R_0$ MFCC, $R_1$ PANNs, $R_2$ BirdNET) mampu mengenali spesies burung pada kueri bersih tanpa derau (*Clean Baseline*) dalam skema *strict recordist-disjoint*?
* **RQ2 (Noise Robustness & Differential Retention):** Bagaimana dinamika ketahanan performa (*noise retention*) masing-masing representasi ketika kueri yang sama mengalami degradasi derau aditif nyata kampus ITERA pada berbagai tingkatan SNR (+20 dB hingga -5 dB)?
* **RQ3 (Open-Set Threshold Rejection):** Apakah nilai ambang batas kemiripan kosinus ($\tau^*$) yang dikalibrasi pada partisi terpisah mampu secara stabil menolak sinyal asing (*unknown fauna* & derau latar) di bawah degradasi derau ekstrem?
* **RQ4 (Sensitivity to Noise Source / Soundscape):** Seberapa besar kesenjangan performa (*performance gap*) ketika derau aditif kampus ITERA digantikan oleh derau aditif bentang alam asli hutan tropis (*real soundscape*)?
* **RQ5 (Failure Diagnosis & Statistical Significance):** Apa faktor utama penyebab kegagalan temu kembali pada kueri nyata, dan apakah keunggulan performa absolut serta retensi ketahanan signifikan secara statistik ($p < 0.001$)?

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
* *Integritas Partisi:* $\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset$ (Tepat 0 author overlap, 0 ID overlap, 0 filepath overlap, diverifikasi oleh `tests/run_all_tests.py` dan `run_tests.py`).

### 2.3 Bank Derau Fisik AudioMoth ITERA
Bank derau terdiri atas **1.799 berkas audio WAV fisik** yang direkam di 5 lokasi lingkungan kampus ITERA (Masjid At-Tanwir, Embung F, Kebun Raya, Gedung F, GKU 1) mencakup frequency dan amplitude trigger (memenuhi DEC-12). Sesuai mandat DEC-09, seluruh derau sintetis (*pink noise*) telah dihapus. Manifes lengkap dienkripsi dengan checksum SHA-256 pada `data/manifests/itera_noise_manifest.csv`.

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

### 3.2 Jawaban RQ2: Ketahanan Derau Terkontrol (Eksperimen E2 - Data Otentik Mentah)
Tercatat pada `paper/tables/snr_robustness_table.csv` dan `paper/figures/e2_snr_robustness_curve.png`:

| Representasi | Clean | SNR 20 dB | SNR 10 dB | SNR 0 dB | SNR -5 dB | Retensi Relatif (-5 dB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET)** | **0.9126** | **0.9068** | **0.8858** | **0.8317** | **0.7707** | **84.45%** (CI: 80.6% – 88.3%) |
| **$R_1$ (PANNs)** | 0.4152 | 0.4533 | 0.3700 | 0.1290 | **0.0590** | **14.22%** (CI: 10.1% – 18.6%) |
| **$R_0$ (MFCC)** | 0.1319 | 0.1320 | 0.1022 | 0.0587 | **0.0349** | **26.42%** (CI: 20.8% – 33.4%) |
| **$R_3$ (Random)** | 0.0190 | 0.0158 | 0.0148 | 0.0142 | 0.0165 | - |

*Pembahasan Saintifik Kritis RQ2 & Evaluasi Hipotesis H1:*
1. **Keunggulan Eksklusif Representasi Bioakustik ($R_2$):** BirdNET membuktikan ketahanan luar biasa dengan retensi **84.45%** pada SNR -5 dB (mAP@10 = 0.7707).
2. **Keruntuhan Representasi Audio Generik ($R_1$) di Bawah MFCC ($R_0$):** Pada SNR -5 dB, performa PANNs ($R_1$) runtuh ke **0.0590** dengan retensi hanya **14.22%**, secara statistik lebih rendah dibandingkan retensi MFCC ($R_0$) yang mencapai **26.42%**. Selang kepercayaan bootstrap retensi keduanya tidak saling tumpang tindih ($R_1$ $[0.101, 0.186]$ vs $R_0$ $[0.208, 0.334]$, $\Delta = +0.1223$, $p < 0.001$).
3. **Koreksi Teoretis Hipotesis H1:** Hipotesis bahwa representasi *deep neural network* secara inheren lebih tahan derau dibandingkan fitur konvensional *hanya terbukti untuk model domain-spesifik bioakustik*, bukan untuk model deep generic audio. Fitur generic AudioSet sangat rentan terhadap pengaburan sinyal oleh derau lingkungan tropis pada rasio daya negatif.
4. **Fenomena SNR +20 dB pada PANNs:** Peningkatan performa $R_1$ pada SNR +20 dB (retensi 109.16% / mAP 0.4533 vs Clean 0.4152) merefleksikan fenomena *stochastic resonance* atau *noise dithering*, di mana sedikit derau latar bertindak sebagai regularisasi yang menutupi fluktuasi halus pada spektrogram sinyal bersih.

---

### 3.3 Jawaban RQ3: Kalibrasi Ambang Batas Open-Set (Eksperimen E3)
* *Status Metodologis:* Kalibrasi ambang batas open-set pada partisi kalibrasi mandiri (498 klip). Uji transfer ambang batas $\tau$ memerlukan pembedaan tegas antara sinyal target dan koleksi unknown sejati (derau murni latar ITERA dan audio non-burung) agar penghitungan Youden's Index $J = \text{TPR} - \text{FPR}$ memiliki landasan biner yang sah.

---

### 3.4 Jawaban RQ4: Kesenjangan Sumber Derau Soundscape (Eksperimen E4)
Tercatat pada `paper/tables/e4_domain_shift_table.csv`:
* Pengujian E4 mencampurkan potongan acak dari 10.658 rekaman soundscape hutan tropis BirdCLEF sebagai derau aditif untuk mengukur sensitivitas terhadap karakteristik spektral sumber derau yang berbeda (derau antropogenik kampus ITERA vs biophony serangga hutan tropis).
* *Hasil:* Pada $R_2$, mAP@10 pada SNR -5 dB adalah 0.7606 (dibandingkan 0.7707 pada derau ITERA, selisih -0.0101). Namun pada $R_1$ pada SNR 0 dB, terdapat kesenjangan yang lebih lebar (E4 = 0.19 vs E2 = 0.13), menunjukkan bahwa model generik sangat sensitif terhadap profil spektral sumber derau.
* *Batasan Riset:* E4 merupakan pengujian derau aditif terkontrol, bukan deteksi bentang alam kontinu di lapangan yang memodelkan jarak fisik dan atenuasi akustik 3D.

---

### 3.5 Jawaban RQ5: Analisis Kasus Kegagalan & Uji Signifikansi Statistik
Tercatat pada `paper/tables/statistical_significance_table.csv` (dihasilkan oleh `src/bootstrap_inference.py`):

| Komparasi Model | Domain Uji | Rata-Rata Selisih | 95% Confidence Interval (CI) | $p$-value Empiris | Kesimpulan Hipotesis |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET) vs $R_1$ (PANNs)** | Clean mAP@10 | **+0.4974** | **[+0.4504, +0.5473]** | **$p < 0.001$** | $H_0$ Ditolak (Signifikan) |
| **$R_2$ (BirdNET) vs $R_0$ (MFCC)** | Clean mAP@10 | **+0.7807** | **[+0.7423, +0.8183]** | **$p < 0.001$** | $H_0$ Ditolak (Signifikan) |
| **$R_1$ (PANNs) vs $R_0$ (MFCC)** | Clean mAP@10 | **+0.2833** | **[+0.2351, +0.3308]** | **$p < 0.001$** | $H_0$ Ditolak (Signifikan) |
| **$R_2$ vs $R_1$** | Retensi SNR -5 dB | **+0.7020** | **[+0.6402, +0.7571]** | **$p < 0.001$** | $H_0$ Ditolak (Signifikan) |
| **$R_0$ vs $R_1$** | Retensi SNR -5 dB | **+0.1223** | **[+0.0581, +0.1994]** | **$p < 0.001$** | $H_0$ Ditolak (Signifikan) |

*Pembahasan RQ5:* Uji paired bootstrap resampling 1.000 iterasi membuktikan secara meyakinkan bahwa keunggulan absolut BirdNET pada kueri bersih serta keunggulan retensinya pada derau ekstrem adalah nyata secara statistik ($p < 0.001$). Terlebih lagi, terbukti secara inferensial bahwa MFCC mempertahankan retensi relatif lebih tinggi daripada PANNs pada SNR -5 dB.

---

## 4. Kesimpulan & Rekomendasi
Penelitian ini membuktikan bahwa:
1. Representasi spesifik domain bioakustik ($R_2$ BirdNET) memberikan performa retrieval terbaik pada kueri bersih (Top-1 95.0%, mAP 0.9126) dan ketahanan derau superior (retensi 84.45% pada -5 dB).
2. Representasi deep learning audio umum ($R_1$ PANNs) mengalami keruntuhan katastropik pada SNR -5 dB (retensi hanya 14.22%), bahkan kalah dalam retensi relatif dibandingkan MFCC (26.42%).
3. Seluruh temuan statistik didukung oleh uji paired bootstrap 1.000 iterasi dengan $p < 0.001$.
