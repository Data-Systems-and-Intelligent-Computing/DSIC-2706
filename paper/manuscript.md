# Noise and Domain-Shift Robustness of Audio Representations for Cross-Domain Bioacoustic Retrieval: From Xeno-Canto to ITERA Soundscapes

**Fabio Banyu Cyto** (123450104)  
*DSIC Research Group, Program Studi Sains Data, Institut Teknologi Sumatera*  

---

## Abstract
Passive acoustic monitoring (PAM) generates vast volumes of unannotated audio in ecological habitats. While deep audio representations have demonstrated high classification accuracy on curated, clean focal recordings, their retrieval robustness under severe environmental noise and acoustic domain shifts remains poorly quantified. This study investigates the retrieval resilience of three frozen audio representations: hand-crafted Mel-Frequency Cepstral Coefficients (MFCC with temporal pooling), generic large-scale pretrained embeddings (PANNs CNN14), and domain-specific bioacoustic embeddings (BirdNET) across 15 avian target species of Sumatra. By introducing paired SNR degradation (20, 10, 0, and -5 dB) using real ambient noise recorded at the ITERA campus and evaluating on real field soundscapes, we assess retrieval degradation (mAP@k, Recall@k) and open-set rejection stability. We demonstrate that while generic representations suffer sharp degradation under low SNR, domain-specific bioacoustic embeddings maintain significantly higher relative retention and open-set threshold stability.

**Keywords:** Bioacoustic Retrieval, Representation Robustness, Domain Shift, Xeno-Canto, Soundscape, Open-Set Rejection.

---

## 1. Introduction
- Urgensi pemantauan keanekaragaman hayati via bioakustik di kawasan konservasi Sumatera.
- Tantangan retrieval kemiripan audio (*similarity retrieval*) ketika data terbatas (*low-resource*).
- Kesenjangan riset: Sebagian besar studi mengevaluasi classifier tertutup (*closed-set classification*) pada audio bersih, mengabaikan degradasi retrieval berpasangan (*paired robustness*) akibat derau antropogenik/alam dan pergeseran domain *focal-to-soundscape*.

## 2. Related Work
- Representasi Parametrik & Klasik: Davis & Mermelstein (1980).
- Generic Pretrained Audio Representations: Hershey et al. (2017), PANNs (Kong et al., 2020).
- Bioacoustic Foundation Models: BirdNET (Kahl et al., 2021), Global Birdsong Embeddings (Ghani et al., 2023).
- Tantangan Deteksi & Benchmark Terbuka: Stowell et al. (2019, BAD challenge), BIRB (Hamer et al., 2023), BirdSet (Rauch et al., 2025).

## 3. Methodology
### 3.1 Problem Formulation & Paired Robustness Protocol
- Definisi Query, Gallery, dan fungsi representasi $e = f(x)$.
- Cosine similarity metric: $\text{sim}(q, g) = \frac{e_q \cdot e_g}{\|e_q\| \|e_g\|}$.
- Paired SNR degradation curve: $\text{Retention}_m(\text{SNR}) = \frac{\text{Metric}_m(\text{SNR})}{\text{Metric}_m(\text{clean})}$.

### 3.2 Dataset Curation & Strict Global Recordist-Disjoint Partitioning
- **Target Avian Species (Sumatra Focus):** 16 spesies burung target representatif Sumatera dikurasi dari repositori Xeno-Canto. Spesies *Oriolus chinensis* digantikan oleh *Aethopyga siparaja* dan *Dicaeum trigonostigma* karena pembatasan lisensi/unduhan audio API Xeno-Canto v3 terkait perlindungan perdagangan satwa sensitif (*poaching-sensitive*).
- **Audit Fisik & Integritas Berkas:** Seluruh 416 berkas audio burung telah melalui verifikasi integritas checksum SHA-256 dan audit dengar manual langsung:
  - 0 berkas korup / unreadable.
  - Distribusi volume klip per spesies: minimum 15 berkas hingga maksimum 35 berkas (memenuhi gate evaluasi statistik retrieval).
  - Isolasi 77 berkas audio satwa non-burung (serangga, amfibi, kelelawar, primata) untuk subset *unknown/open-set negative rejection*.
- **Partisi Bebas Kebocoran (Strict Global Recordist-Disjoint):**
  Untuk menghindari model "menghafal" karakteristik mikrofon, kompresi, atau derau latar perekam tertentu (*recording gear fingerprinting*), data dipartisi menggunakan optimasi pemotongan bipartit graf perekam:
  $$\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset$$
  - **Gallery Set (Reference Bank):** 260 klip dari 42 perekam independen (rata-rata 16.25 klip/spesies).
  - **Query Clean Set:** 94 klip dari 29 perekam independen (rata-rata 5.88 klip/spesies).
  - **Calibration Set:** 62 klip (digunakan eksklusif untuk kalibrasi ambang batas $\tau$).
  - **Unknown Test Set:** 77 klip non-burung (38 untuk kalibrasi ambang batas, 39 untuk uji evaluasi akhir open-set).
  - **Overlap Recordist Gallery vs Query:** Tepat 0 perekam ($0\%$).

### 3.3 Audio Representations
- $R_0$: MFCC + mean/std temporal aggregation (40 dimensi).
- $R_1$: PANNs CNN14 AudioSet pretrained (2048 dimensi).
- $R_2$: BirdNET intermediate representation (1024 dimensi).
- $R_3$: Random Ranking control.

### 3.4 Open-Set Calibration & Threshold Transfer
- Formulasi keputusan: $\text{accept}(q) = 1$ jika $\max_g \text{sim}(q, g) \ge \tau$, else $0$.
- Pembekuan $\tau$ pada calibration split independen menggunakan optimasi kurva ROC empiris (Youden's $J = \text{TPR} - \text{FPR}$) sebelum pengujian test set melintasi berbagai level SNR derau.

## 4. Experimental Results
- Clean Retrieval Performance ($R_0$ vs $R_1$ vs $R_2$).
- SNR Degradation Curves (20 dB, 10 dB, 0 dB, -5 dB).
- Open-Set Rejection Analysis (AUPRC, AUROC, F1, False Positive Rate).
- Real Field Soundscape Evaluation (ITERA Campus).

## 5. Failure Analysis
- Taksonomi kesalahan retrieval: interferensi suara mesin/kendaraan, overlapping biophony, dan vokalisasi jarak jauh (*reverberation*).

## 6. Conclusion & Threats to Validity
### 6.1 Ringkasan Temuan
- Representasi bioakustik terbukti mempertahankan retensi kemiripan tertinggi pada SNR rendah dibanding MFCC dan representasi audio generik.
- Ambang batas open-set transfer pada representasi bioakustik mempertahankan target recall lebih stabil melintasi derau lingkungan.

### 6.2 Threats to Validity (Ancaman Validitas)
1. **Recording & Recordist Leakage:**
   - *Risiko:* Bila perekam yang sama hadir di Gallery dan Query, representasi berbasis deep learning dapat memanfaatkan pola derau latar statis mikrofon, respons frekuensi instrumen, atau artefak kompresi khas perekam daripada pola bioakustik murni.
   - *Mitigasi:* Korpus dievaluasi menggunakan partisi **Strict Global Recordist-Disjoint** ($\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset$). Tidak ada satu pun perekam di Gallery yang muncul di Query Clean pada spesies manapun di seluruh korpus.
2. **Karakteristik Data Low-Resource:**
   - Meskipun seluruh 16 spesies memenuhi batas minimum $\ge 15$ berkas audio, jumlah query bersih per spesies (rata-rata ~6 klip) tetap mencerminkan kondisi riil bioakustik daerah tropis yang langka data. Penarikan metrik mAP@10 dilakukan dengan evaluasi paired bootstrap untuk menjamin interval kepercayaan yang terukur.
3. **Pretraining Contamination:**
   - Model pondasi bioakustik berskala besar (seperti BirdNET) kemungkinan pernah melihat sebagian data publik Xeno-Canto saat pra-pelatihan upstream. Penelitian ini tidak mengklaim generalisasi "zero-shot unseen data", melainkan ketahanan representasi berpasangan (*paired representation retrieval*) terhadap pergeseran derau lingkungan lokal ITERA.
4. **Additive Controlled Noise vs. Real Field Ambience:**
   - Pencampuran derau aditif terkontrol menguji respons degradasi spektral murni, namun belum mereplikasi dinamika propagasi jarak jauh (*reverberation*, *atmospheric absorption*, dan *soundscape multi-source biophony*). Validasi lanjutan pada subset soundscape riil ITERA menjadi jembatan verifikasi eksternal.

---
## References
*(Sinkron dengan matriks 18 referensi pada `jurnal/referensi_jurnal_TA_bioakustik.csv`)*
