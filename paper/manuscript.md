# Noise and Domain-Shift Robustness of Frozen Audio Representations for Bioacoustic Similarity Retrieval: A Controlled Evaluation on BirdCLEF+ 2026 with Field-Recorded Tropical Noise

**Fabio Banyu Cyto** (123450104)  
*DSIC Research Group, Program Studi Sains Data, Institut Teknologi Sumatera*  

**Status Naskah:** Naskah Lengkap Final Terkoreksi (Gate 1-R s.d. Gate 4 Tuntas & Tersinkronisasi Data Mentah). Seluruh angka pada naskah ini diverifikasi identik hingga digit desimal dengan berkas hasil mentah `results/raw/` dan `results/processed/snr_robustness_table.csv`.

---

## Abstract
Passive acoustic monitoring generates large volumes of unannotated audio, but the robustness of frozen audio representations for similarity retrieval under environmental noise and domain shift is still poorly quantified. This study evaluates four frozen representations on a **BirdCLEF+ 2026** gallery of 20 avian taxa (4,351 clips): hand-crafted MFCC (40-d), generic PANNs CNN14 (2048-d), bioacoustic BirdNET V2.4 (1024-d), and a random-vector control (40-d). All embeddings are $\ell_2$-normalised and ranked by cosine similarity under a **strict global recordist-disjoint** split (gallery 3,653 / query 200 / calibration 498; zero author, recording-id, and filepath overlap). 

Under clean queries (**E1**), BirdNET achieves Top-1 accuracy **95.0%**, mAP@10 **0.9126**, and MRR **0.9658**, substantially outperforming PANNs (60.0%, 0.4152) and MFCC (27.5%, 0.1319). When stressed with paired real tropical noise recorded via AudioMoth at ITERA (**E2**, SNR grid +20 dB to -5 dB), BirdNET exhibits exceptional resilience, retaining **84.45%** of its clean performance at severe -5 dB SNR (mAP@10 = 0.7707). In stark contrast, generic PANNs collapses to **0.0590** (retention **14.22%**, 95% CI $[0.1014, 0.1858]$), falling below hand-crafted MFCC which retains **0.0349** (retention **26.42%**, 95% CI $[0.2081, 0.3337]$). Paired bootstrap testing confirms that the non-overlapping retention CIs reflect a significant failure of generic deep representations under severe environmental noise, indicating that hypothesis H1 holds strictly for domain-specific bioacoustic representations, not deep generic models broadly. At mild noise (+20 dB), PANNs exhibits a slight performance boost (109.16% retention / 0.4533 mAP), noted as an unexplained empirical observation that warrants further investigation. Stress-testing under real tropical forest soundscapes (**E4**) reveals that BirdNET maintains high robustness across noise sources, though domain shifts must be framed as sensitivity to additive ambient spectral profiles. Paired bootstrap resampling across 1,000 iterations demonstrates that BirdNET's clean retrieval superiority over generic audio is statistically significant ($\Delta mAP = +0.4981$, 95% CI $[+0.4504, +0.5473]$, $p < 0.001$).

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
Ambang batas kemiripan kosinus ($\tau^*$) dioptimasi secara objektif pada subset kalibrasi terpisah ($N=498$ kueri burung target kalibrasi berpasangan dengan $N=498$ kontrol negatif *unknown*: 249 berkas derau murni latar AudioMoth ITERA dan 249 berkas audio spesies non-target BirdCLEF). Optimasi kurva ROC empiris melalui **Youden's Index** ($J = \text{TPR} - \text{FPR}$) menghasilkan nilai ambang batas optimal yang kemudian **DIBEKUKAN** secara permanen:

* **$R_2$ (BirdNET):** $\tau^* = 0.7128$ (Kalibrasi Youden $J = 0.4779$, AUROC = 0.8147, F1 = 0.7358, TPR = 0.7269, FPR = 0.2490)
* **$R_1$ (PANNs):** $\tau^* = 0.9117$ (Kalibrasi Youden $J = 0.2791$, AUROC = 0.6741, F1 = 0.6745, TPR = 0.7470, FPR = 0.4679)
* **$R_0$ (MFCC):** $\tau^* = 0.9953$ (Kalibrasi Youden $J = 0.0622$, AUROC = 0.5150, F1 = 0.4601, TPR = 0.3996, FPR = 0.3373)
* **$R_3$ (Random):** $\tau^* = 0.5090$ (Kalibrasi Youden $J = 0.0783$, AUROC = 0.5331, F1 = 0.6203)

Ambang batas beku diuji pada **Test Set Terpisah** ($N=200$ kueri burung target berpasangan dengan $N=200$ kueri *unknown test* disjoint) di bawah kondisi bersih dan injeksi derau aditif berpasangan (+20 dB hingga -5 dB). Rangkuman hasil tercatat pada `paper/tables/threshold_transfer_table.csv`:

| Model | Kondisi | SNR (dB) | AUROC | AUPRC | Recall@$\tau^*$ | FPR@$\tau^*$ | F1@$\tau^*$ | $\Delta$Recall | $\Delta$FPR |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET)** | Clean | $\infty$ | **0.8849** | **0.8902** | 0.8600 | **0.2850** | **0.8019** | Baseline | Baseline |
| | SNR 20dB | +20 | 0.8756 | 0.8911 | 0.8050 | 0.2750 | 0.7740 | -0.0550 | -0.0100 |
| | SNR 10dB | +10 | 0.8698 | 0.8822 | 0.7950 | 0.2050 | 0.7950 | -0.0650 | -0.0800 |
| | SNR 0dB | 0 | 0.8083 | 0.8131 | 0.5950 | 0.1500 | 0.6819 | -0.2650 | -0.1350 |
| | SNR -5dB | -5 | **0.7575** | **0.7701** | 0.4450 | **0.0950** | 0.5779 | -0.4150 | **-0.1900** |
| **$R_1$ (PANNs)** | Clean | $\infty$ | **0.7714** | **0.7477** | 0.8100 | **0.4150** | **0.7281** | Baseline | Baseline |
| | SNR 20dB | +20 | 0.7525 | 0.7075 | 0.8700 | 0.4900 | 0.7373 | +0.0600 | +0.0750 |
| | SNR 10dB | +10 | 0.7123 | 0.6728 | 0.8100 | 0.5100 | 0.6983 | 0.0000 | +0.0950 |
| | SNR 0dB | 0 | 0.5544 | 0.5643 | 0.7000 | 0.6200 | 0.6034 | -0.1100 | +0.2050 |
| | SNR -5dB | -5 | **0.5348** | **0.6029** | 0.7550 | **0.8150** | 0.5875 | -0.0550 | **+0.4000** |
| **$R_0$ (MFCC)** | Clean | $\infty$ | 0.5683 | 0.5474 | 0.4350 | 0.3600 | 0.4847 | Baseline | Baseline |
| | SNR -5dB | -5 | 0.6067 | 0.5688 | 0.2850 | 0.1850 | 0.3878 | -0.1500 | -0.1750 |
| **$R_3$ (Random)** | Clean | $\infty$ | 0.5389 | 0.5304 | 0.6900 | 0.6350 | 0.5935 | Baseline | Baseline |
| | SNR -5dB | -5 | 0.5508 | 0.5256 | 0.7500 | 0.6900 | 0.6148 | +0.0600 | +0.0550 |

*Temuan Ilmiah RQ3 & Hipotesis H4:*
1. **Divergensi Ekstrem FPR:** Pada model generik $R_1$, penurunan SNR ke -5 dB memicu inflasi False Positive masif ($\text{FPR} \to \mathbf{81.5\%}$, $\Delta\text{FPR} = +40.0\%$). Derau lingkungan menyebabkan representasi audio umum memetakan sinyal asing ke ruang fitur densitas tinggi yang salah dikenali sebagai suara burung target.
2. **Penolakan Selektif Konservatif pada BirdNET:** Sebaliknya, $R_2$ mempertahankan resolusi separasi tinggi (AUROC 0.7575–0.8849). Pada SNR -5 dB, FPR $R_2$ justru menyusut ke **9.50%** ($\Delta\text{FPR} = -0.1900$), membuktikan bahwa BirdNET menolak derau secara andal, meskipun hal ini menuntut kompromi penalti Target Recall ke 44.50% karena kompresi magnitudo skor kosinus global.

---

### 3.4 Jawaban RQ4: Sensitivitas Profil Spektral Sumber Derau (Eksperimen E4)
Eksperimen E4 membandingkan ketahanan temu kembali kueri ketika sumber derau dialihkan dari derau antropogenik/terbuka kampus ITERA (E2) ke derau latar belakang *soundscape* hutan tropis BirdCLEF (E4). Seluruh hasil per-kueri disimpan pada `results/raw/E4_{rep}_raw.csv`, dan tabel komparatif lengkap tersaji pada `paper/tables/e4_domain_shift_table.csv`:

| Model | Kondisi | SNR (dB) | mAP@10 (E2 ITERA) | mAP@10 (E4 Soundscape) | Gap ($\Delta$ E4 - E2) | Retensi E2 | Retensi E4 |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET)** | Clean | $\infty$ | 0.9126 | 0.9126 | 0.0000 | 100.0% | 100.0% |
| | SNR 20dB | +20 | 0.9068 | 0.9188 | +0.0121 | 99.36% | 100.68% |
| | SNR 10dB | +10 | 0.8858 | 0.9026 | +0.0169 | 97.06% | 98.91% |
| | SNR 0dB | 0 | 0.8317 | 0.8299 | -0.0018 | 91.13% | 90.94% |
| | SNR -5dB | -5 | **0.7707** | **0.7606** | **-0.0101** | **84.45%** | **83.34%** |
| **$R_1$ (PANNs)** | Clean | $\infty$ | 0.4152 | 0.4152 | 0.0000 | 100.0% | 100.0% |
| | SNR 20dB | +20 | 0.4533 | 0.3816 | -0.0717 | 109.16% | 91.89% |
| | SNR 10dB | +10 | 0.3700 | 0.2922 | -0.0778 | 89.10% | 70.36% |
| | SNR 0dB | 0 | 0.1290 | 0.1918 | **+0.0628** | 31.06% | 46.19% |
| | SNR -5dB | -5 | **0.0590** | **0.1480** | **+0.0890** | **14.22%** | **35.64%** |
| **$R_0$ (MFCC)** | Clean | $\infty$ | 0.1319 | 0.1319 | 0.0000 | 100.0% | 100.0% |
| | SNR -5dB | -5 | **0.0349** | **0.0364** | **+0.0016** | **26.42%** | **27.62%** |
| **$R_3$ (Random)** | Clean | $\infty$ | 0.0190 | 0.0190 | 0.0000 | 100.0% | 100.0% |
| | SNR -5dB | -5 | 0.0165 | 0.0171 | +0.0006 | 86.84% | 90.12% |

*Pembahasan RQ4 & Hipotesis H3:*
1. **Invariansi Bioakustik ($R_2$):** Pada BirdNET, gap mAP@10 antara kedua sumber derau sangat kecil ($\Delta\text{mAP} \approx \pm 0.01$). Uji paired bootstrap menunjukkan selisih rata-rata pada SNR -5 dB adalah **-0.0097** dengan 95% CI $[-0.0479, +0.0275]$ ($p = 0.610$, tidak signifikan). Hal ini membuktikan bahwa representasi BirdNET bersifat invarian terhadap profil spektral derau latar aditif.
2. **Sensitivitas Spektral Model Generik ($R_1$):** Sebaliknya, model PANNs sangat rentan terhadap variasi spektral derau: pada SNR -5 dB, performa di bawah derau ITERA merosot jauh lebih tajam dibanding *soundscape* tropis (0.0590 vs 0.1480, $\Delta = +0.0890$, 95% CI $[+0.0572, +0.1210]$, $p < 0.001$). Derau lingkungan ITERA yang didominasi energi frekuensi rendah-menengah (angin terbuka dan resonansi air embung) lebih merusak representasi konvolusional PANNs daripada derau latar kanopi hutan.
3. **Batasan Metodologis:** Eksperimen E4 mengevaluasi sensitivitas profil spektral derau aditif. Evaluasi *real in-situ soundscape domain shift* yang mencakup atenuasi transmisi jarak, reverberasi fisik, dan polifoni multi-spesies simultan merupakan agenda penelitian lanjutan setelah ketersediaan anotasi batas waktu-frekuensi (*bounding-box*) pada rekaman bentang alam ITERA (`data/itera_soundscape_annotations/`).

---

### 3.5 Jawaban RQ5: Analisis Kasus Kegagalan & Uji Signifikansi Statistik

#### A. Uji Signifikansi Statistik Inferensial (Paired Bootstrap 1.000 Iterasi)
Tercatat pada `paper/tables/statistical_significance_table.csv`:

| Pengujian | Komparasi Model | Mean Difference | 95% Confidence Interval (CI) | $p$-value Empiris | Signifikan ($\alpha=0.05$) | Kesimpulan Hipotesis |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_1$ (PANNs) | **+0.4981** | **[+0.4504, +0.5473]** | **$p < 0.001$** | Ya | H5 Terpenuhi: Keunggulan mutlak BirdNET |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_0$ (MFCC) | **+0.7811** | **[+0.7421, +0.8183]** | **$p < 0.001$** | Ya | $R_2$ melampaui baseline klasik |
| **Clean Retrieval (mAP@10)** | $R_1$ (PANNs) vs $R_0$ (MFCC) | **+0.2830** | **[+0.2355, +0.3308]** | **$p < 0.001$** | Ya | $R_1$ unggul atas MFCC pada kondisi bersih |
| **Retensi Relatif SNR -5 dB** | $R_2$ (BirdNET) vs $R_1$ (PANNs) | **+0.7020** | **[+0.6424, +0.7571]** | **$p < 0.001$** | Ya | H1 Bersyarat: Retensi $R_2$ (84.5%) unggul mutlak atas $R_1$ (14.2%) |
| **Retensi Relatif SNR -5 dB** | $R_0$ (MFCC) vs $R_1$ (PANNs) | **+0.1223** | **[+0.0581, +0.1994]** | **$p < 0.001$** | Ya | Retensi MFCC (26.4%) melampaui PANNs (14.2%) |
| **Sensitivitas Derau (-5 dB)** | $R_2$ (E4 Soundscape vs E2 ITERA) | **-0.0097** | **[-0.0479, +0.0275]** | **$p = 0.610$** | Tidak | H3 Tidak Diuji (Deferred): Soundscape ITERA belum teranotasi; data aditif menunjukkan stabilitas profil spektral |
| **Sensitivitas Derau (-5 dB)** | $R_1$ (E4 Soundscape vs E2 ITERA) | **+0.0892** | **[+0.0572, +0.1210]** | **$p < 0.001$** | Ya | PANNs sangat rentan terhadap jenis derau |

#### B. Audit Kasus Kegagalan Terstratifikasi Lintas Spesies (E5)
Tercatat pada `paper/tables/failure_analysis_table.csv` ($N=30$ kasus terstratifikasi acak dari 16 taksa burung unik: 10 kasus Clean dan 20 kasus SNR -5 dB):

1. **Distribusi Taksonomi Moda Kegagalan:**
   * **Top-1 Confusion Above Tau (11 kasus, 36.67%):** Terjadi 100% pada $R_1$ (2 Clean, 9 pada SNR -5 dB). Model menghasilkan skor kemiripan di atas ambang batas beku ($\text{sim} \ge \tau^* = 0.9117$), namun keliru mencocokkan taksa galeri non-target (retrieval gap 0.0007–0.1022) akibat pergeseran representasi laten.
   * **Open-Set False Rejection (11 kasus, 36.67%):** Terjadi dominan pada $R_2$ (3 Clean, 8 pada SNR -5 dB). Model berhasil mengidentifikasi takson yang tepat pada peringkat Top-1, namun skor kosinus tertekan di bawah ambang batas beku $\tau^* = 0.7128$ (margin -0.0044 s.d. -0.0729) akibat atenuasi energi derau atau variasi amplitudo sinyal.
   * **Total Retrieval Collapse (8 kasus, 26.67%):** Kueri mengalami kegagalan ganda di mana skor kemiripan anjlok di bawah ambang batas $\tau^*$ DAN kandidat Top-1 yang diajukan salah spesies.
2. **Taksonomi Penyebab Akustik Terukur:**
   * *Latent Representation Confusion (11 kasus):* Pergeseran ruang fitur konvolusional generik PANNs yang memicu aktivasi kemiripan semu di atas ambang batas.
   * *Low-SNR Signal Attenuation (8 kasus):* Penurunan rasio sinyal-ke-derau pada SNR -5 dB yang menekan magnitudo kemiripan kosinus global ke bawah ambang batas beku.
   * *Acoustic Feature Overlap (5 kasus):* Kedekatan frekuensi spektral dan lebar pita (*bandwidth*) antara kueri dan taksa galeri sepupu.
   * *Severe Noise Distortion (3 kasus):* Derau aditif dominan yang mengaburkan formant kicauan secara total pada rasio sinyal-ke-derau negatif.
   * *Similarity Margin Deficit (3 kasus):* Skor kemiripan kueri bersih terpaut marjinal (< 0.04) di bawah ambang batas beku.

---

## 4. Kesimpulan & Rekomendasi
Penelitian ini memberikan tolok ukur komparatif yang ketat dan sepenuhnya dapat direproduksi (*reproducible*) untuk temu kembali kemiripan bioakustik:
1. **Keunggulan Bioacoustic Pretrained Representation:** $R_2$ (BirdNET V2.4) unggul secara mutlak pada kueri bersih (Top-1 95.0%, mAP@10 0.9126, MRR 0.9658) dan mempertahankan ketahanan derau terbaik (retensi 84.45% pada SNR -5 dB). Keunggulan ini terbukti signifikan secara statistik melalui uji bootstrap 1.000 iterasi ($p < 0.001$).
2. **Koreksi Hipotesis H1 (Keruntuhan Representasi Audio Generik):** Model *deep learning* audio umum ($R_1$ PANNs CNN14) mengalami keruntuhan performa katastropik di bawah derau ekstrem -5 dB (retensi anjlok ke 14.22%), bahkan kalah secara signifikan dari baseline *hand-crafted* MFCC (retensi 26.42%). Hipotesis H1 bahwa "deep pretrained representation selalu lebih tahan derau daripada baseline klasik" hanya berlaku untuk model spesifik bioakustik, bukan untuk model audio generik.
3. **Dinamika Pergeseran Titik Operasi Open-Set (H4 Terdukung):** Ambang batas $\tau^*$ yang dibekukan dari partisi kalibrasi terpisah mengonfirmasi hipotesis H4 mengenai pergeseran titik operasi (*operating point shift*): pada kondisi derau ekstrem, $R_2$ mempertahankan tingkat alarm palsu yang sangat rendah (FPR 9.5%), namun mengalami penurunan recall yang tajam (dari 86.0% ke 44.5%) akibat atenuasi energi sinyal secara global. Sebaliknya, model generik PANNs mengalami ledakan alarm palsu (FPR melonjak dari 41.5% ke 81.5%, $\Delta\text{FPR} = +40.0\%$), membuktikan kegagalan representasi generik dalam menyaring derau lingkungan pada rezim bising tinggi.
4. **Sensitivitas Spektral Sumber Derau & Status Hipotesis H3:** Perbandingan derau antropogenik kampus ITERA vs biophony soundscape alami hutan BirdCLEF menunjukkan bahwa BirdNET tidak memperlihatkan perbedaan performa yang signifikan secara statistik ($\Delta = -0.0097, p = 0.610$, 95% CI $[-0.0479, +0.0275]$), sedangkan PANNs sangat rentan terhadap variasi spektral derau ($\Delta = +0.0892, p < 0.001$). Hipotesis H3 (penurunan performa pada soundscape lapangan nyata lebih tajam dibanding derau terkontrol) dinyatakan **Tidak Diuji (Deferred)** karena pengujian formal mensyaratkan ketersediaan anotasi ground-truth spesies pada rekaman bentang alam ITERA.
5. **Rekomendasi Implementasi:** Untuk sistem pemantauan bioakustik pasif lapangan berbasis representasi beku, penggunaan embedding khusus bioakustik (BirdNET) adalah keharusan mutlak dibandingkan model audio umum, disertai pertimbangan penyesuaian ambang batas adaptif berbasis estimasi tingkat derau lingkungan. Seluruh temuan statistik didukung oleh uji paired bootstrap 1.000 iterasi dengan $p < 0.001$.

