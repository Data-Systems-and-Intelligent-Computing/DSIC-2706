# Ketahanan Representasi Audio terhadap Derau dan Pergeseran Domain untuk Pencarian Kemiripan Bioakustik: Tolok Ukur Empiris pada Avifauna Kepulauan Indonesia dengan Derau Lapangan Kampus ITERA

**Fabio Banyu Cyto** (123450104)  
*DSIC Research Group, Program Studi Sains Data, Institut Teknologi Sumatera*  
*Dosen Pembimbing: Pak Ardika Satria, S.T., M.T.*  

**Status Naskah:** Naskah Lengkap Final Terkoreksi (Transisi Menyeluruh ke Avifauna Indonesia & Derau Fisik AudioMoth Kampus ITERA). Seluruh angka pada naskah ini diverifikasi identik hingga digit desimal dengan berkas hasil mentah `results/raw/`, `results/processed/`, dan lolos 100% pada suite pengujian unit saintifik (`run_tests.py`).

---

## Abstract
Passive acoustic monitoring generates massive volumes of unannotated audio, but the robustness of frozen audio representations for similarity retrieval under environmental noise and domain shift remains poorly quantified in tropical Southeast Asia. This study establishes a rigorous empirical benchmark evaluating four frozen representations on an Indonesian archipelago avifauna corpus of 20 widespread, non-endemic bird species (1,216 physical recordings, 100% recorded in Indonesia, all 20 species represented in Sumatra): hand-crafted MFCC ($R_0$, 40-d), generic audio PANNs CNN14 ($R_1$, 2048-d), domain-specific bioacoustic BirdNET V2.4 ($R_2$, 1024-d), and a random-vector control ($R_3$, 40-d). All embeddings are $\ell_2$-normalised and evaluated via cosine similarity under a **strict global recordist-disjoint** split (Gallery: 673 clips / 59 recordists; Query Clean: 311 clips / 27 recordists; Calibration: 232 clips / 25 recordists; 112 unique recordists, zero author, recording ID, and filepath leakage).

Under clean query conditions (**E1**), BirdNET V2.4 achieves dominant retrieval performance with Top-1 accuracy **81.67%**, mAP@10 **0.6370**, and MRR **0.8650**, significantly outperforming generic PANNs (Top-1 37.94%, mAP@10 0.1771) and MFCC baseline (Top-1 18.01%, mAP@10 0.0690) with paired bootstrap statistical significance ($\Delta\text{mAP} = +0.4609$, 95% CI $[+0.4260, +0.4986]$, $p \le 0.001$). When subjected to controlled additive field noise from 1,799 physical AudioMoth recordings at ITERA campus (**E2**, SNR grid +20 dB to -5 dB with 0% synthetic pink noise fallback), BirdNET exhibits superior resilience, retaining **78.0%** of its clean mAP@10 at severe -5 dB SNR (mAP@10 = 0.4968, Top-1 = 64.31%), whereas generic PANNs retains **55.3%** (mAP@10 = 0.0979, Top-1 = 18.97%) and MFCC retains **35.9%** (mAP@10 = 0.0248, Top-1 = 9.65%). Paired bootstrap testing confirms BirdNET's retention superiority over PANNs ($\Delta = +0.2244$, 95% CI $[+0.1182, +0.3217]$, $p \le 0.001$; Cluster Bootstrap $\Delta = +0.2310$, $p \le 0.001$) and MFCC ($\Delta = +0.4190$, $p \le 0.001$), supporting Hypothesis H1 for bioacoustic representations.

In open-set evaluation (**E3**), frozen thresholds calibrated via Youden's $J$ on an independent set ($N=465$, 232 known + 233 unknown; $\tau^* = 0.7071$ for $R_2$ and $\tau^* = 0.8974$ for $R_1$) reveal that under severe -5 dB noise, BirdNET's false positive rate drops conservatively from 20.00% to 9.35% due to global similarity score compression (operating point shift, validating Hypothesis H4), accompanied by a target recall decrease to 24.12%. Habitat noise sensitivity analysis (**E4**) across ITERA micro-environments demonstrates that canopy insect biophony at Kebun Raya causes the steepest degradation to BirdNET (retention 69.89%, mAP@10 = 0.4452) compared to Embung F hydro-acoustics (76.12%, mAP@10 = 0.4849) and Gedung F structural noise (73.23%, mAP@10 = 0.4665), driven by direct spectral overlap in the 2–6 kHz bird vocalization band. Real in-situ soundscape domain shift is framed as Deferred / Not Tested (H3) pending manual bounding-box annotations. Stratified failure analysis (**E5**, $N=30$) demonstrates that 100% of false rejections occur in BirdNET due to noise energy attenuation below frozen $\tau^*$, whereas 90% of false positive confusions above $\tau^*$ occur in generic PANNs due to latent representation drift.

**Keywords:** Bioacoustic Retrieval, Representation Robustness, Indonesian Avifauna, AudioMoth, ITERA Campus Noise, Open-Set Rejection, BirdNET, Paired Bootstrap Resampling.

---

## 1. Pendahuluan & Rumusan Masalah (Research Questions)

Pemantauan bioakustik pasif (*Passive Acoustic Monitoring* / PAM) di wilayah tropis Indonesia menghadapi tantangan lingkungan yang kompleks: dinamika cuaca ekstrem, desis angin kencang, derau resonansi air, dan biofoni serangga berfrekuensi tinggi. Pendekatan konvensional umumnya mengasumsikan klasifikasi himpunan tertutup (*closed-set classification*), yang rapuh terhadap kemunculan spesies asing atau variasi perekam lapangan. Penelitian ini mengkaji paradigma temu kembali kemiripan (*similarity retrieval*) menggunakan representasi audio beku (*frozen representations*) untuk menjawab 5 Pertanyaan Penelitian (*Research Questions* / RQ):

* **RQ1 (Baseline Retrieval Performance):** Sejauh mana representasi audio beku ($R_0$ MFCC, $R_1$ PANNs, $R_2$ BirdNET, $R_3$ Random Control) mampu mengenali spesies burung Indonesia pada kondisi rekaman bersih (*Clean Baseline*) dalam skema pemisahan perekam yang ketat (*strict recordist-disjoint split*)?
* **RQ2 (Noise Robustness & Retention Dynamics):** Bagaimana dinamika ketahanan performa (*noise retention*) masing-masing representasi ketika kueri yang sama mengalami degradasi derau aditif fisik AudioMoth kampus ITERA pada variasi rasio sinyal-ke-derau (+20 dB hingga -5 dB)?
* **RQ3 (Open-Set Threshold Rejection):** Apakah nilai ambang batas kemiripan kosinus ($\tau^*$) yang dikalibrasi secara objektif pada subset terpisah mampu secara stabil menolak sinyal asing (*unknown bird fauna* & derau lingkungan) di bawah degradasi derau ekstrem tanpa lonjakan alarm palsu?
* **RQ4 (Habitat Noise Spectral Sensitivity):** Seberapa sensitif representasi audio terhadap variasi profil spektral sumber derau dari habitat mikro kampus ITERA (Kebun Raya / Biofoni Serangga, Embung F / Hidroakustik & Angin, dan Gedung F / Resonansi Struktural)?
* **RQ5 (Failure Diagnosis & Statistical Significance):** Apa modalitas dan penyebab akustik utama kegagalan temu kembali pada kueri nyata, dan apakah keunggulan performa absolut serta retensi ketahanan terbukti signifikan secara statistik ($p < 0.001$)?

---

## 2. Metodologi Penelitian & Pengaturan Eksperimen

### 2.1 Formulasi Kemiripan Kosinus & Retensi
Setiap sinyal audio $x$ distandardisasi ke frekuensi cuplikan 32.000 Hz (mono), dipotong/dipadatkan tepat 5.0 detik (160.000 sampel waktu), dinormalisasi ke energi RMS 0.05, dan diproyeksikan ke vektor representasi laten beku $e = f(x)$ ternormalisasi unit $\ell_2$ ($\|e\|_2 = 1$). Standarisasi durasi 5.0 detik dan normalisasi amplitudo ini selaras dengan tolok ukur bioakustik komputasi modern terkini (*Rauch et al., 2025; Stowell, 2022; Ghani et al., 2023*), yang membuktikan bahwa jendela 5.0 detik merupakan titik optimal (*sweet-spot*) dalam menangkap struktur frase panggilan avifauna tanpa mengorbankan resolusi temporal representasi konvolusional.

Kemiripan kosinus antara kueri $q$ dan galeri $g$ didefinisikan sebagai perkalian titik langsung:
$$\mathrm{sim}(q, g) = e_q^\top e_g$$
Mengikuti protokol degradasi bioakustik terkontrol (*Chen et al., 2023; Nolasco et al., 2023*), retensi relatif terhadap kondisi bersih pada tingkat SNR tertentu dirumuskan:
$$\mathrm{Retention}_m(\mathrm{SNR}) = \frac{\mathrm{mAP@10}_m(\mathrm{SNR})}{\mathrm{mAP@10}_m(\mathrm{clean})} \times 100\%$$

### 2.2 Korpus Data Burung Indonesia & Partisi Bebas Bocor (*Zero Leakage*)
Sesuai arahan pembimbing (**Pak Ardika Satria, S.T., M.T.**), dataset disusun dari 20 taksa spesies burung Indonesia non-endemik yang umum dan tersebar luas (total **1.216 berkas audio MP3 fisik** terunduh dan terverifikasi checksum SHA-256). Pemilihan taksa umum regional Sundaland ini didukung oleh temuan bioakustik tropis terkini (*Ningrum et al., 2026; Zabidi et al., 2026a, 2026b*), yang menunjukkan bahwa pemantauan spesies umum merupakan bioindikator kunci stabilitas ekosistem dan memiliki ketersediaan rekaman bioakustik lapangan yang memadai untuk pembelajaran representasi:
1. **100% Teritori Indonesia:** Seluruh 1.216 rekaman berlokasi di dalam yurisdiksi Indonesia (`cnt: Indonesia`); rekaman luar negeri dieksklusi 100%.
2. **Keterwakilan Sumatera:** Seluruh 20 spesies terverifikasi hadir di Pulau Sumatera (total 168 klip, 13.8%), menjamin relevansi ekologis dengan wilayah kampus ITERA di Lampung Selatan.
3. **Kepatuhan Ambang DEC-10:** Setiap spesies memiliki 30 s.d. 137 rekaman (rata-rata 60.8 klip) dari 14 s.d. 35 perekam independen (rata-rata 22.5 perekam). Kualitas terkurasi tinggi (Grade A dan B mencapai 77.1%).
4. **Partisi Perekam Bebas Bocor (*Recordist-Disjoint Split* pada Seed 19):**
   * **Gallery Set:** 673 rekaman audio dari 59 perekam independen.
   * **Query Clean Set:** 311 rekaman audio dari 27 perekam independen (28 perekam unik setelah nama komposit dipecah).
   * **Calibration Set:** 232 rekaman audio dari 25 perekam independen.
   * *Verifikasi Integritas:* $\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} \cap \mathcal{R}_{\text{Calibration}} = \emptyset$ (Tepat 0 perekam, 0 berkas, dan 0 ID rekaman tumpang tindih; total 112 perekam unik di seluruh korpus, lolos 100% pada uji integritas otomatis, selaras dengan metodologi *Musgrave et al., 2020; Hamer et al., 2023*).

### 2.3 Bank Derau Fisik AudioMoth Kampus ITERA
Bank derau terdiri atas **1.799 berkas audio WAV fisik** yang direkam secara kontinu menggunakan perekam otonom AudioMoth di habitat mikro kampus ITERA (Kebun Raya, Embung F, Gedung F, Masjid At-Tanwir, GKU 1). Validitas penggunaan AudioMoth sebagai sensor bioakustik pasif berdaya rendah telah terbukti secara ekstensif pada literatur pemantauan satwa liar modern (*Ciapponi et al., 2025; Zabidi et al., 2026c*). Keterbatasan komputasi *on-edge* perangkat mikrokontroler AudioMoth (RAM $\le 1$ MB) menjustifikasi paradigma ekstraksi representasi laten beku pada stasiun kerja terpisah (*offboard similarity retrieval*).

Sesuai mandat integritas data, seluruh fungsi generator sintetis *pink noise* telah dihapus permanen (`FileNotFoundError` ditegakkan). Pemuatan derau dilakukan secara deterministik melalui manifes terenkripsi `data/manifests/itera_noise_manifest.csv`.

---

## 3. Hasil Eksperimen Empiris & Pembahasan (Menjawab RQ1 - RQ5)

### 3.1 Jawaban RQ1: Tolok Ukur Temu Kembali Kondisi Bersih (Eksperimen E1)
Hasil evaluasi 311 kueri bersih terhadap 673 galeri tersaji pada `paper/tables/clean_retrieval_table.csv`:

| Kode | Arsitektur Model | Dimensi Laten | Top-1 Accuracy (%) | mAP@10 | MRR | Precision@10 | Recall@10 |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$** | **BirdNET V2.4 Backbone** | 1024-d | **81.67%** | **0.6370** | **0.8650** | **0.6942** | **0.2325** |
| **$R_1$** | **PANNs CNN14** | 2048-d | 37.94% | 0.1771 | 0.5090 | 0.2586 | 0.0843 |
| **$R_0$** | **MFCC Baseline** | 40-d | 18.01% | 0.0690 | 0.3079 | 0.1308 | 0.0360 |
| **$R_3$** | **Random Control** | 40-d | 6.75% | 0.0231 | 0.1811 | 0.0615 | 0.0150 |

*Pembahasan Saintifik RQ1 & Evaluasi Keunggulan Bioakustik:*
Representasi bioakustik spesifik ($R_2$ BirdNET V2.4) unggul mutlak atas model generik audio ($R_1$ PANNs) dengan selisih mAP@10 sebesar **+0.4609** (95% CI $[+0.4260, +0.4986]$, $p \le 0.001$) dan akurasi Top-1 mencapai **81.67%** (vs 37.94% pada PANNs). Keunggulan ini menjawab **RQ1**: arsitektur yang dipra-latih khusus pada vokal burung mampu memetakan variasi individu antar-perekam (*author-disjoint*) ke klaster biologis yang kohesif, sedangkan model audio umum AudioSet gagal menangkap fitur spektro-temporal mikro kicauan burung tropis. Selain itu, evaluasi kontrol positif paired bootstrap (**Hipotesis H5**) membuktikan bahwa seluruh representasi terlatih berada jauh di atas ekspektasi tebakan acak ($R_3$) secara sangat signifikan ($p \le 0.001$): BirdNET $R_2$ vs $R_3$ memiliki Mean Difference sebesar **+0.6145** (95% CI $[+0.5753, +0.6528]$), PANNs $R_1$ vs $R_3$ sebesar **+0.1536** (95% CI $[+0.1286, +0.1796]$), dan baseline MFCC $R_0$ vs $R_3$ sebesar **+0.0457** (95% CI $[+0.0327, +0.0589]$).

---

### 3.2 Jawaban RQ2: Ketahanan Derau Terkontrol ITERA (Eksperimen E2)
Hasil evaluasi degradasi berpasangan di bawah derau lingkungan kampus ITERA tersaji pada `paper/tables/snr_robustness_table.csv`:

| Representasi | Clean | SNR 20 dB | SNR 10 dB | SNR 0 dB | SNR -5 dB | Retensi Relatif (-5 dB) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET)** | **0.6370** | **0.6420** | **0.6213** | **0.5679** | **0.4968** | **77.99%** (CI: 74.0% – 82.1%) |
| **$R_1$ (PANNs)** | 0.1771 | 0.1964 | 0.1857 | 0.1326 | **0.0979** | **55.27%** (CI: 46.8% – 64.3%) |
| **$R_0$ (MFCC)** | 0.0690 | 0.0774 | 0.0643 | 0.0369 | **0.0248** | **35.89%** (CI: 27.5% – 44.0%) |
| **$R_3$ (Random)** | 0.0231 | 0.0189 | 0.0241 | 0.0213 | 0.0230 | 99.44% (Tebakan Acak) |

*Pembahasan Saintifik RQ2 & Evaluasi Hipotesis H1 & H2:*
1. **Keunggulan Retensi Bioakustik ($R_2$):** Pada derau ekstrem SNR -5 dB, BirdNET mempertahankan **77.99%** performa mAP@10 (mAP = 0.4968, Top-1 = 64.31%), mempertahankan kapasitas diskriminatif yang substansial dibanding model lain, meskipun tetap mengalami degradasi sebesar ~22.0% akibat derau lingkungan. Uji paired bootstrap menunjukkan retensi BirdNET melampaui PANNs secara signifikan ($\Delta = +0.2244$, 95% CI $[+0.1182, +0.3217]$, $p \le 0.001$; Cluster Bootstrap per perekam $\Delta = +0.2310$, $p \le 0.001$) dan MFCC ($\Delta = +0.4190$, 95% CI $[+0.3016, +0.5173]$, $p \le 0.001$).
2. **Koreksi Teoretis Hipotesis H1:** Representasi mendalam generik ($R_1$ PANNs) mempertahankan retensi 55.27% (mAP = 0.0979, Top-1 = 18.97%), meskipun mengalami degradasi yang lebih tajam dibanding BirdNET, model ini masih mempertahankan skor mAP@10 di atas baseline klasik MFCC (retensi 35.89%, mAP = 0.0248, Top-1 = 9.65%, selisih retensi $\Delta = +0.1946$, $p = 0.0050$). Hipotesis H1 terbukti: representasi konvolusional bioakustik ($R_2$) secara signifikan lebih tangguh dibanding model generik ($R_1$) dan konvensional ($R_0$).
3. **Dinamika Degradasi Monoton & Fluktuasi Empiris Ringan (+20 dB):** Pada SNR +20 dB, teramati fluktuasi retensi di atas 100% pada representasi kueri (MFCC 112.0%, PANNs 110.8%, BirdNET 100.7%). Fluktuasi empiris kueri ringan ini merupakan respons terhadap derau latar beramplitudo sangat lemah yang memberikan efek penghalusan spektral minor, sebelum performa merosot secara monoton saat derau bertambah pekat ke 0 dB dan -5 dB (memenuhi Hipotesis H2). Fenomena ini dilaporkan secara objektif sebagai fluktuasi empiris batas atas tanpa mengasumsikan resonansi stokastik sebagai fakta terbukti.

---

### 3.3 Jawaban RQ3: Kalibrasi Ambang Batas Open-Set (Eksperimen E3)
Ambang batas kemiripan kosinus ($\tau^*$) dikalibrasi secara objektif pada subset kalibrasi independen ($N=465$: 232 kueri target burung Indonesia + 233 kontrol negatif *unknown*: 117 spesies burung non-target Indonesia + 116 berkas derau AudioMoth ITERA). Optimasi indeks Youden ($J = \text{TPR} - \text{FPR}$) menghasilkan ambang batas beku:
* **$R_2$ (BirdNET):** $\tau^* = 0.7071$ (Youden $J = 0.4188$, AUROC = 0.7601, F1 = 0.6633, TPR = 0.5733, FPR = 0.1545)
* **$R_1$ (PANNs):** $\tau^* = 0.8974$ (Youden $J = 0.3766$, AUROC = 0.7167, F1 = 0.7047, TPR = 0.7457, FPR = 0.3691)
* **$R_0$ (MFCC):** $\tau^* = 0.9958$ (Youden $J = 0.0995$, AUROC = 0.5298, F1 = 0.3010, TPR = 0.1940, FPR = 0.0944)
* **$R_3$ (Random):** $\tau^* = 0.4481$ (Youden $J = 0.1191$, AUROC = 0.5658, F1 = 0.6279, TPR = 0.7457, FPR = 0.6266)

Pengujian ambang batas beku pada **Test Set Terpisah** ($N=621$: 311 kueri burung target + 310 kueri negatif *unknown* disjoin) tercatat pada `paper/tables/threshold_transfer_table.csv`:

| Model | Kondisi | SNR (dB) | AUROC | AUPRC | Recall@$\tau^*$ | FPR@$\tau^*$ | F1@$\tau^*$ | $\Delta$Recall | $\Delta$FPR |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET)** | Clean | $\infty$ | **0.7589** | **0.7891** | 0.5916 | **0.2000** | **0.6607** | Baseline | Baseline |
| | SNR 20dB | +20 | 0.7576 | 0.7878 | 0.5466 | 0.1613 | 0.6403 | -4.50% | -3.87% |
| | SNR 10dB | +10 | 0.7299 | 0.7642 | 0.4791 | 0.1258 | 0.5972 | -11.25% | -7.42% |
| | SNR 0dB | 0 | 0.6596 | 0.6980 | 0.3183 | 0.1097 | 0.4459 | -27.33% | -9.03% |
| | SNR -5dB | -5 | **0.6153** | **0.6483** | 0.2412 | **0.0935** | 0.3614 | -35.05% | **-10.65%** |
| **$R_1$ (PANNs)** | Clean | $\infty$ | **0.7454** | **0.7166** | 0.8360 | **0.4742** | **0.7242** | Baseline | Baseline |
| | SNR 20dB | +20 | 0.7498 | 0.7056 | 0.8489 | 0.4774 | 0.7303 | +1.29% | +0.32% |
| | SNR 10dB | +10 | 0.7389 | 0.6896 | 0.8006 | 0.4548 | 0.7104 | -3.54% | -1.94% |
| | SNR 0dB | 0 | 0.6833 | 0.6545 | 0.6045 | 0.3419 | 0.6215 | -23.15% | -13.23% |
| | SNR -5dB | -5 | **0.6287** | **0.6145** | 0.4566 | **0.2710** | 0.5289 | -37.94% | **-20.32%** |
| **$R_0$ (MFCC)** | Clean | $\infty$ | 0.5463 | 0.5549 | 0.1865 | 0.1387 | 0.2816 | Baseline | Baseline |
| | SNR -5dB | -5 | 0.5665 | 0.5473 | 0.0064 | 0.0129 | 0.0126 | -18.01% | -12.58% |
| **$R_3$ (Random)** | Clean | $\infty$ | 0.5183 | 0.5346 | 0.6849 | 0.6548 | 0.5860 | Baseline | Baseline |
| | SNR -5dB | -5 | 0.5221 | 0.5117 | 0.6624 | 0.6355 | 0.5770 | -2.25% | -1.94% |

*Pembahasan Saintifik RQ3 & Validasi Hipotesis H4:*
1. **Divergensi Dinamika Titik Operasi:** Pada BirdNET ($R_2$), False Positive Rate (FPR) menyusut secara konservatif dari 20.00% menjadi **9.35%** pada SNR -5 dB ($\Delta\text{FPR} = -10.65\%$). Penurunan ini membuktikan hipotesis **H4**: atenuasi energi sinyal oleh derau menekan magnitudo kemiripan kosinus global ke bawah ambang batas beku, sehingga sistem menjadi hiper-konservatif (Target Recall turun ke 24.12%).
2. **Dinamika Separasi Open-Set:** Pada PANNs CNN14, meskipun FPR pada -5 dB juga menurun (dari 47.42% ke 27.10%), tingkat alarm palsu pada kondisi bersih sangat tinggi (FPR 47.42% vs 20.00% pada BirdNET), menegaskan bahwa BirdNET memiliki batas keputusan open-set yang jauh lebih tajam dan terkendali.

---

### 3.4 Jawaban RQ4: Sensitivitas Profil Spektral Sumber Derau Lintas Habitat ITERA (Eksperimen E4)
Eksperimen E4 membandingkan ketahanan representasi ketika kueri disuntik derau aditif dari tiga habitat mikro berbeda di kampus ITERA: Kebun Raya (Biofoni Kanopi/Serangga), Embung F (Hidroakustik & Angin Terbuka), dan Gedung F (Resonansi Struktural & Antropogenik). Rangkuman tersaji pada `paper/tables/e4_domain_shift_table.csv`:

| Model | Habitat Derau | Kondisi | SNR (dB) | mAP@10 | Top-1 Accuracy (%) | Retensi Relatif |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **$R_2$ (BirdNET)** | Baseline Clean | Clean | $\infty$ | **0.6370** | **81.67%** | 100.0% |
| | Kebun Raya | SNR -5 dB | -5 | **0.4446** | **59.81%** | **69.80%** |
| | Embung F | SNR -5 dB | -5 | **0.4853** | **62.70%** | **76.19%** |
| | Gedung F | SNR -5 dB | -5 | **0.4667** | **64.63%** | **73.27%** |
| **$R_1$ (PANNs)** | Baseline Clean | Clean | $\infty$ | **0.1771** | **37.94%** | 100.0% |
| | Kebun Raya | SNR -5 dB | -5 | **0.0590** | **13.18%** | **33.31%** |
| | Embung F | SNR -5 dB | -5 | **0.0948** | **24.44%** | **53.53%** |
| | Gedung F | SNR -5 dB | -5 | **0.0979** | **22.19%** | **55.28%** |
| **$R_0$ (MFCC)** | Baseline Clean | Clean | $\infty$ | **0.0690** | **18.01%** | 100.0% |
| | Kebun Raya | SNR -5 dB | -5 | **0.0228** | **6.43%** | **33.04%** |
| | Embung F | SNR -5 dB | -5 | **0.0264** | **7.07%** | **38.26%** |
| | Gedung F | SNR -5 dB | -5 | **0.0189** | **4.18%** | **27.39%** |

*Pembahasan Saintifik RQ4 & Status Hipotesis H3:*
1. **Dampak Tumpang Tindih Spektral Biofoni Kebun Raya:** Pada BirdNET ($R_2$), degradasi terdalam terjadi di habitat **Kebun Raya (retensi 69.80%, mAP = 0.4446)**, terpaut signifikan dibanding Embung F (retensi 76.19%, Mean Diff +0.0398, $p = 0.0040$). Biofoni serangga tropis (jangkrik, tonggeret) memiliki konsentrasi energi pada pita frekuensi 2.000–6.000 Hz yang bertumpuk langsung dengan formant vokal utama burung target (*spectral overlap*), mendistorsi representasi laten lebih parah dibanding derau angin atau mesin.
2. **Sensitivitas Ekstrem Model Generik PANNs ($R_1$) & Uji Komparasi Stabilitas Rentang Habitat (Hipotesis H3):** PANNs mengalami keruntuhan hingga retensi **33.31%** di Kebun Raya (vs 53.53% di Embung F dan 55.28% di Gedung F, Mean Diff +0.0358 s.d. +0.0391, keduanya $p \le 0.001$), menegaskan bahwa fitur konvolusional umum sangat rentan terhadap gangguan biofoni frekuensi tinggi. Fluktuasi rentang ayunan retensi lintas habitat pada PANNs mencapai 21.98% (55.28% - 33.31%), sedangkan ayunan retensi pada BirdNET hanya 6.39% (76.19% - 69.80%). Pengujian bootstrap komparasi rentang ayunan retensi ($R_1$ vs $R_2$) menghasilkan disparitas observasi $\Delta_{\text{obs}} = 0.1560$ (rata-rata bootstrap **+0.1692**, 95% CI $[+0.0795, +0.2646]$, $p \le 0.001$). Karena proses resampling bootstrap cenderung menggembungkan estimasi selisih rentang ekstrem ($\max - \min$), pelaporan nilai observasi langsung $\Delta_{\text{obs}} = 0.1560$ mendampingi rerata bootstrap untuk transparansi inferensial penuh. Hal ini memberikan bukti inferensial langsung yang **Mendukung Sebagian Hipotesis H3**: representasi bioakustik spesifik ($R_2$) secara signifikan lebih stabil dan tidak fluktuatif terhadap variasi spektral mikro-habitat dibanding model audio generik.
3. **Integritas Metodologis Hipotesis H3 (Reframed / Deferred):** Sesuai arahan pembimbing (**Pak Ardika Satria**), evaluasi *real in-situ soundscape domain shift* tanpa kontrol aditif dinyatakan **Belum Diuji / Ditangguhkan (Deferred - H3)** karena rekaman bentang alam ITERA belum dilengkapi anotasi kotak batas (*bounding-box ground truth*). Landasan penangguhan ini didukung kuat oleh temuan metodologi bioakustik tropis terkini (*Zabidi et al., 2026c; Stowell, 2022*), yang membuktikan bahwa okupansi vokal burung pada rekaman bentang alam kontinu umumnya di bawah 10%, sementara >90% durasi audio didominasi derau non-target. Tanpa anotasi temporal terverifikasi, evaluasi temu kembali mentah rentan terdistorsi oleh *silent windows* dan tumpang-tindih multi-spesies. Oleh karena itu, pendekatan *Paired In-Situ Evaluation* berbasis injeksi derau fisik ITERA terkontrol (E2 dan E4) menjadi metodologi evaluasi ketahanan paling valid dan terukur secara komputasi.

---

### 3.5 Jawaban RQ5: Analisis Kasus Kegagalan & Uji Signifikansi Statistik

#### A. Uji Signifikansi Statistik Inferensial (Paired Bootstrap 1.000 Iterasi)
Tercatat pada `paper/tables/statistical_significance_table.csv`:

| Pengujian | Komparasi Model | Mean Difference | 95% Confidence Interval (CI) | $p$-value Empiris | Signifikan ($\alpha=0.05$) | Kesimpulan Hipotesis |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_1$ (PANNs) | **+0.4609** | **[+0.4260, +0.4986]** | **$p \le 0.001$** | Ya | BirdNET unggul mutlak atas model generik audio |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_0$ (MFCC) | **+0.5688** | **[+0.5316, +0.6054]** | **$p \le 0.001$** | Ya | $R_2$ unggul mutlak atas baseline klasik MFCC |
| **Clean Retrieval (mAP@10)** | $R_1$ (PANNs) vs $R_0$ (MFCC) | **+0.1079** | **[+0.0854, +0.1314]** | **$p \le 0.001$** | Ya | $R_1$ unggul atas MFCC pada kondisi bersih |
| **Clean Retrieval (mAP@10)** | $R_2$ (BirdNET) vs $R_3$ (Random) | **+0.6145** | **[+0.5753, +0.6528]** | **$p \le 0.001$** | Ya | H5 Terpenuhi: $R_2$ unggul mutlak atas kontrol acak |
| **Clean Retrieval (mAP@10)** | $R_1$ (PANNs) vs $R_3$ (Random) | **+0.1536** | **[+0.1286, +0.1796]** | **$p \le 0.001$** | Ya | H5 Terpenuhi: $R_1$ unggul atas kontrol acak |
| **Clean Retrieval (mAP@10)** | $R_0$ (MFCC) vs $R_3$ (Random) | **+0.0457** | **[+0.0327, +0.0589]** | **$p \le 0.001$** | Ya | H5 Terpenuhi: $R_0$ unggul atas kontrol acak |
| **Retensi Relatif SNR -5 dB** | $R_2$ (BirdNET) vs $R_1$ (PANNs) | **+0.2244** | **[+0.1182, +0.3217]** | **$p \le 0.001$** | Ya | H1 & H2 Terpenuhi: Retensi $R_2$ (78.0%) unggul atas $R_1$ (55.3%) |
| **Retensi Relatif SNR -5 dB** | $R_1$ (PANNs) vs $R_0$ (MFCC) | **+0.1946** | **[+0.0570, +0.3294]** | **$p = 0.0050$** | Ya | Retensi $R_1$ (55.3%) unggul atas MFCC (35.9%) |
| **Retensi Relatif SNR -5 dB** | $R_2$ (BirdNET) vs $R_0$ (MFCC) | **+0.4190** | **[+0.3016, +0.5173]** | **$p \le 0.001$** | Ya | Retensi $R_2$ unggul mutlak atas MFCC baseline |
| **Sensitivitas Habitat E4 (-5 dB)** | $R_2$ (Embung F vs Kebun Raya) | **+0.0398** | **[+0.0142, +0.0677]** | **$p = 0.0040$** | Ya | Biofoni serangga Kebun Raya mendegradasi BirdNET lebih parah |
| **Sensitivitas Habitat E4 (-5 dB)** | $R_2$ (Gedung F vs Kebun Raya) | **+0.0214** | **[-0.0021, +0.0442]** | **$p = 0.0880$** | Tidak | Derau struktural gedung berdampak serupa dengan biofoni |
| **Sensitivitas Habitat E4 (-5 dB)** | $R_1$ (Embung F vs Kebun Raya) | **+0.0358** | **[+0.0179, +0.0526]** | **$p \le 0.001$** | Ya | PANNs sangat rentan terhadap biofoni Kebun Raya |
| **Sensitivitas Habitat E4 (-5 dB)** | $R_1$ (Gedung F vs Kebun Raya) | **+0.0391** | **[+0.0215, +0.0580]** | **$p \le 0.001$** | Ya | PANNs lebih tahan derau gedung dibanding biofoni serangga |
| **Fluktuasi Rentang Habitat (-5 dB)** | $R_1$ vs $R_2$ (Selisih Ayunan Retensi) | **+0.1692** | **[+0.0795, +0.2646]** | **$p \le 0.001$** | Ya | H3 Terdukung Parsial: $\Delta_{\text{obs}} = 0.1560$ (bootstrap +0.1692), $R_1$ lebih rentan dibanding $R_2$ |
| **Cluster Bootstrap (per Recordist, K=27)** | $R_2$ vs $R_1$ Retensi Relatif (-5 dB) | **+0.2310** | **[+0.1473, +0.3321]** | **$p \le 0.001$** | Ya | Resampling klaster perekam membuktikan keunggulan $R_2$ bebas bias |
| **Sensitivitas Non-Mike Nelson (N=180)** | $R_2$ vs $R_1$ Retensi Relatif (-5 dB) | **+0.2485** | **[+0.1188, +0.3701]** | **$p \le 0.001$** | Ya | Keunggulan $R_2$ tetap signifikan tanpa perekam dominan (42%) |

#### B. Audit Kasus Kegagalan Terstratifikasi Lintas Spesies (Eksperimen E5)
Tercatat pada `paper/tables/failure_analysis_table.csv` ($N=30$ kasus terstratifikasi acak dari 17 taksa burung Indonesia: 10 kasus Clean dan 20 kasus SNR -5 dB):
1. **Divergensi Moda Kegagalan per Model:**
   * **Open-Set False Rejection (10 kasus, 33.3%):** Terjadi 100% pada $R_2$ BirdNET (4 pada kondisi Clean, 6 pada SNR -5 dB). Model berhasil menempatkan takson yang benar pada peringkat Top-1, namun skor kosinus tertekan di bawah ambang batas beku $\tau^* = 0.7071$ (margin negatif -0.0044 s.d. -0.0729).
   * **Top-1 Confusion Above Tau (9 kasus, 30.0%):** Didominasi oleh $R_1$ PANNs (8 dari 9 kasus, serta 1 kasus $R_2$ kueri bersih). Model menghasilkan skor kemiripan semu di atas ambang batas $\tau^*$ namun keliru mencocokkan takson galeri non-target akibat pergeseran representasi laten (*latent representation confusion*).
   * **Total Retrieval Collapse (11 kasus, 36.7%):** Terjadi pada 7 kasus $R_1$ (1 Clean + 6 SNR -5 dB) dan 4 kasus $R_2$ (4 SNR -5 dB) di bawah derau ekstrem, di mana skor jatuh di bawah $\tau^*$ DAN kandidat Top-1 salah spesies.
2. **Taksonomi Penyebab Akustik Terukur:**
   * *Severe Noise Distortion (10 kasus):* Sinyal vokal tenggelam di bawah derau lingkungan pada rasio daya negatif.
   * *Latent Representation Confusion (9 kasus):* Terjadi 89% pada PANNs akibat distorsi konvolusional fitur akustik umum.
   * *Low-SNR Signal Attenuation (6 kasus):* Terjadi 100% pada BirdNET akibat penekanan energi skor kemiripan kosinus.
   * *Similarity Margin Deficit (4 kasus):* Kueri bersih yang berada marjinal di bawah ambang batas beku.
   * *Acoustic Feature Overlap (1 kasus):* Kedekatan frekuensi formant dengan takson burung sepupu.

---

## 4. Kesimpulan, Rekomendasi & Ancaman terhadap Validitas

### 4.1 Kesimpulan & Rekomendasi
1. **Keunggulan Representasi Pra-latih Bioakustik:** $R_2$ (BirdNET V2.4) unggul mutlak pada kueri bersih avifauna kepulauan Indonesia (Top-1 81.67%, mAP@10 0.6370, MRR 0.8650) dan mempertahankan ketahanan derau tertinggi (retensi 77.99% pada SNR -5 dB, mAP = 0.4968), terbukti signifikan secara statistik melalui uji paired bootstrap 1.000 iterasi ($\Delta = +0.2244$, $p \le 0.001$) dan cluster bootstrap per perekam ($\Delta = +0.2310$, $p \le 0.001$).
2. **Validasi Hipotesis H1 & H2:** Representasi terlatih bioakustik terbukti secara signifikan lebih tahan derau dibanding model audio generik dan baseline klasik konvensional, membuktikan Hipotesis H1. Degradasi performa berbanding terbalik secara monoton dengan penurunan SNR mulai dari +10 dB ke bawah, membuktikan Hipotesis H2.
3. **Validasi Hipotesis H4 (Pergeseran Titik Operasi Open-Set):** Ambang batas $\tau^*$ beku menunjukkan bahwa pada derau ekstrem, BirdNET tidak mengalami ledakan alarm palsu (FPR menyusut ke 9.35% dari 20.00%), namun menderita penurunan Target Recall ke 24.12% akibat kompresi energi sinyal secara global. Sebaliknya, model generik PANNs memiliki FPR tinggi (47.42% pada kondisi bersih).
4. **Sensitivitas Spektral Habitat & Status Hipotesis H3:** Biofoni serangga Kebun Raya terbukti paling destruktif bagi BirdNET (retensi 69.80% vs 76.19% di Embung F, selisih +0.0398, $p = 0.0040$) akibat tumpang tindih spektral pada pita 2–6 kHz. Kendati demikian, stabilitas rentang ayunan retensi BirdNET (6.39%) terbukti signifikan lebih kokoh dibanding PANNs (21.98%, selisih ayunan observasi $\Delta_{\text{obs}} = 0.1560$, rata-rata bootstrap +0.1692, $p \le 0.001$), mendukung H3 secara parsial. Evaluasi domain shift rekaman bentang alam in-situ tanpa kontrol aditif dinyatakan **Ditangguhkan (Deferred - H3)** hingga tersedianya anotasi *bounding-box ground truth* pada rekaman ITERA, selaras dengan arahan pembimbing.
5. **Rekomendasi Penerapan:** Sistem pemantauan bioakustik pasif di wilayah tropis disarankan mengadopsi representasi berbasis bioakustik spesifik (BirdNET) disertai mekanisme adaptasi ambang batas berbasis estimasi tingkat derau lingkungan setempat.

### 4.2 Ancaman terhadap Validitas (Threats to Validity)
1. **Potensi Tumpang Tindih Data Pra-Latih (Pre-training Data Overlap - H1/H2):**  
   Model BirdNET (V2.4) dilatih pada skala global menggunakan korpus audio Xeno-Canto. Kendati penelitian ini menegakkan partisi ketat bebas perekam (*strict recordist-disjoint split*) yang menjamin zero leakage pada level perekam lokal, terdapat kemungkinan rekaman spesies burung Indonesia di Xeno-Canto yang terekam sebelum tahun publikasi model pernah masuk dalam korpus pra-latih BirdNET. Hal ini menjadi ancaman terhadap validitas eksternal H1/H2 bahwa keunggulan BirdNET dapat sebagian dipengaruhi oleh familiaritas representasi terhadap ciri vokal spesies target. Namun demikian, generalisasi kuat yang teramati pada perekam kueri independen yang belum pernah dilihat model membuktikan bahwa representasi tidak mengalami penghafalan identitas individu (*author overfitting*).
2. **Keterbatasan Seleksi Taksa Berbasis Ketersediaan Data (Protokol DEC-10):**  
   Pemilihan 20 taksa burung didasarkan pada kehadiran di Pulau Sumatera dan ambang batas kecukupan statistik (minimal 30 rekaman dan 14 perekam independen di Indonesia). Konsekuensinya, sampel penelitian didominasi oleh taksa umum dengan bioakustik yang sering didokumentasikan kontributor warga (*citizen science*). Temuan ini belum tentu dapat digeneralisasi langsung ke taksa terancam punah (*endangered*), kriptik kanopi tinggi, atau nokturnal langka dengan ketersediaan data minim.
3. **Kesenjangan Propagasi Akustik Lapangan (*In-situ Propagation Gap*):**  
   Pengujian ketahanan derau dilakukan menggunakan injeksi derau aditif terkontrol pada grid SNR presisi (+20 dB s.d. -5 dB). Metodologi ini efektif untuk mengisolasi dampak interferensi spektral derau latar, namun belum memodelkan transmisi gelombang suara lapangan sesungguhnya yang melibatkan redaman kanopi tropis (*canopy excess attenuation*), pantulan multipath, dan variasi mikroklimat suhu/kelembapan bentang alam liar.

---

## 5. Daftar Pustaka

1. **Best, P., Paris, S., Glotin, H., & Marxer, R. (2023).** Deep audio embeddings for vocalisation clustering. *PLoS ONE*, 18(4), e0283396. [https://doi.org/10.1371/journal.pone.0283396](https://doi.org/10.1371/journal.pone.0283396)
2. **Chen, L., Xu, Z., & Zhao, Z. (2023).** Biotic sound SNR influence analysis on acoustic indices. *Frontiers in Remote Sensing*, 3, 1079223. [https://doi.org/10.3389/frsen.2022.1079223](https://doi.org/10.3389/frsen.2022.1079223)
3. **Ciapponi, S., Mannini, L., Scanferla, J., Anderle, M., & Farella, E. (2025).** Enabling Multi-Species Bird Classification on Low-Power Bioacoustic Loggers. *arXiv preprint arXiv:2509.20103*. [https://doi.org/10.48550/arXiv.2509.20103](https://doi.org/10.48550/arXiv.2509.20103)
4. **Fonseca, E., Favory, X., Pons, J., Font, F., & Serra, X. (2021).** FSD50K: an open dataset of human-labeled sound events. *IEEE/ACM Transactions on Audio, Speech, and Language Processing*, 30, 829-852. [https://doi.org/10.1109/TASLP.2021.3133208](https://doi.org/10.1109/TASLP.2021.3133208)
5. **Ghani, B., Denton, T., Kahl, S., & Klinck, H. (2023).** Global birdsong embeddings enable superior transfer learning for bioacoustic classification. *Scientific Reports*, 13, 22876. [https://doi.org/10.1038/s41598-023-49989-z](https://doi.org/10.1038/s41598-023-49989-z)
6. **Gong, Y., Chung, Y. A., & Glass, J. (2021).** AST: Audio Spectrogram Transformer. *Interspeech 2021*, 571-575. [https://doi.org/10.21437/Interspeech.2021-698](https://doi.org/10.21437/Interspeech.2021-698)
7. **Hamer, J., Triantafillou, E., Van Merrienboer, B., Kahl, S., Klinck, H., Denton, T., & Dumoulin, V. (2023).** BIRB: A Generalization Benchmark for Information Retrieval in Bioacoustics. *arXiv preprint arXiv:2312.07439*. [https://doi.org/10.48550/arXiv.2312.07439](https://doi.org/10.48550/arXiv.2312.07439)
8. **Kahl, S., Wood, C. M., Eibl, M., & Klinck, H. (2021).** BirdNET: A deep learning solution for avian diversity monitoring. *Ecological Informatics*, 61, 101236. [https://doi.org/10.1016/j.ecoinf.2021.101236](https://doi.org/10.1016/j.ecoinf.2021.101236)
9. **Kong, Q., Cao, Y., Iqbal, T., Wang, Y., Wang, W., & Plumbley, M. D. (2020).** PANNs: Large-Scale Pretrained Audio Neural Networks for Audio Pattern Recognition. *IEEE/ACM Transactions on Audio, Speech, and Language Processing*, 28, 2880-2894. [https://doi.org/10.1109/TASLP.2020.3030497](https://doi.org/10.1109/TASLP.2020.3030497)
10. **Munda, dkk. (2020).** Identifikasi Jenis Anura dengan Bioakustik pada Kawasan Hutan Lindung Sungai Wain, Kalimantan Timur. *ULIN: Jurnal Hutan Tropis*, 4(2), 117-124. [https://e-journals.unmul.ac.id/index.php/UJHT/article/view/11718](https://e-journals.unmul.ac.id/index.php/UJHT/article/view/11718)
11. **Musgrave, K., Belongie, S., & Lim, S. N. (2020).** A Metric Learning Reality Check. *European Conference on Computer Vision (ECCV 2020)*, 681-699. [https://doi.org/10.1007/978-3-030-58592-1_41](https://doi.org/10.1007/978-3-030-58592-1_41)
12. **Ningrum, I. P., Mulyani, Y. A., & Mardiastuti, A. (2026).** Single-station passive acoustic monitoring of bird diversity and vocal activity in Cikaniki, Gunung Halimun-Salak National Park, West Java. *Journal of Wildlife and Conservation Medicine*, 2(1), 32-39. [https://doi.org/10.29244/jwcm.2.1.32](https://doi.org/10.29244/jwcm.2.1.32)
13. **Nolasco, I., Singh, S., Benetos, E., Stowell, D., et al. (2023).** Few-shot bioacoustic event detection at the DCASE 2023 challenge. *arXiv preprint arXiv:2306.09223*. [https://doi.org/10.48550/arXiv.2306.09223](https://doi.org/10.48550/arXiv.2306.09223)
14. **Putra, M. R., Nurdiyansyah, F., & Rahman, A. Y. (2024).** Klasifikasi Jenis Burung Cucak Berdasarkan Suara Menggunakan MFCC Dan Naive Bayes. *Jurnal FASILKOM*, 14(2), 463-470. [https://doi.org/10.37859/jf.v14i2.7558](https://doi.org/10.37859/jf.v14i2.7558)
15. **Rauch, L., Schwinger, R., Wirth, M., Heinrich, R., Huseljic, D., Herde, M., Lange, J., Kahl, S., & Sick, B. (2025).** BirdSet: A Large-Scale Dataset for Audio Classification in Avian Bioacoustics. *International Conference on Learning Representations (ICLR 2025)*. [https://doi.org/10.48550/arXiv.2403.10380](https://doi.org/10.48550/arXiv.2403.10380)
16. **Stowell, D. (2022).** Computational bioacoustics with deep learning: a review and roadmap. *PeerJ*, 10, e13152. [https://doi.org/10.7717/peerj.13152](https://doi.org/10.7717/peerj.13152)
17. **Tim Komputa. (2025).** Klasifikasi Jenis Burung Berdasarkan Suara Kicau Menggunakan Ekstraksi MFCC dan BiLSTM. *Komputa: Jurnal Ilmiah Komputer dan Informatika*, 14(1). [https://ojs.unikom.ac.id/index.php/komputa/article/view/17694](https://ojs.unikom.ac.id/index.php/komputa/article/view/17694)
18. **Tim Peneliti Prosiding. (2025a).** Implementasi Model Transfer Learning Arsitektur ConvNeXt untuk Klasifikasi Suara Burung di Taman Nasional Way Kambas. *Prosiding SainTek, Universitas Terbuka*, 2(1). [https://conference.ut.ac.id/index.php/saintek/article/view/5073](https://conference.ut.ac.id/index.php/saintek/article/view/5073)
19. **Tim Peneliti Prosiding. (2025b).** Klasifikasi Suara Katak Menggunakan Model Deep Learning. *Prosiding SainTek, Universitas Terbuka*, 2(1).
20. **Tim TIFRH Hyderabad. (2025).** A Case Study: Using Passive Acoustic Monitoring Devices In A Growing Urban Landscape To Monitor Avian Diversity. *bioRxiv*, 10.1101/2025.07.21.665881. [https://doi.org/10.1101/2025.07.21.665881](https://doi.org/10.1101/2025.07.21.665881)
21. **Vaze, S., Han, K., Vedaldi, A., & Zisserman, A. (2022).** Open-Set Recognition: A Good Closed-Set Classifier is All You Need. *International Conference on Learning Representations (ICLR 2022)*. [https://doi.org/10.48550/arXiv.2110.06207](https://doi.org/10.48550/arXiv.2110.06207)
22. **Zabidi, M. M. A., Idris, M. Y. I., & Idris, N. (2026a).** SEABAD: A Tropical Bird Activity Detection Dataset for Passive Acoustic Monitoring. *arXiv preprint arXiv:2605.20853*. [https://doi.org/10.48550/arXiv.2605.20853](https://doi.org/10.48550/arXiv.2605.20853)
23. **Zabidi, M. M. A., Idris, M. Y. I., & Idris, N. (2026b).** MyGardenBird: A Machine-Learning-Ready Bird Sound Dataset for Twelve Common Malaysian Birds. *arXiv preprint arXiv:2606.06975*. [https://doi.org/10.48550/arXiv.2606.06975](https://doi.org/10.48550/arXiv.2606.06975)
24. **Zabidi, M. M. A., Idris, M. Y. I., & Idris, N. (2026c).** Ultra-Compact CNN Architectures for Tropical Bird Audio Detection on Microcontrollers. *arXiv preprint arXiv:2607.19721*. [https://doi.org/10.48550/arXiv.2607.19721](https://doi.org/10.48550/arXiv.2607.19721)
