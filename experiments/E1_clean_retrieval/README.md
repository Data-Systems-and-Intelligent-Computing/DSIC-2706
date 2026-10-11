# Eksperimen E1 — Clean Retrieval Benchmark

## 1. Tujuan Ilmiah
Membangun tolok ukur dasar (*clean baseline*) kemampuan perolehan kemiripan (*similarity retrieval*) dari representasi audio terstandardisasi pada kondisi ideal (rekaman bersih bebas derau tambahan) lintas 20 spesies burung target korpus Avifauna Indonesia (Xeno-Canto).

## 2. Konfigurasi Eksperimen
* **Data Uji:** 311 kueri bersih dari 27 perekam independen (28 split composite).
* **Data Referensi (Gallery):** 673 rekaman galeri dari 59 perekam independen.
* **Representasi:**
  * $R_0$: MFCC Baseline (40-dim)
  * $R_1$: PANNs CNN14 (2048-dim)
  * $R_2$: BirdNET Backbone V2.4 (1024-dim)
  * $R_3$: Random Control (40-dim)
* **Metrik Kesamaan:** Cosine Similarity ($311 \times 673$ pairwise similarity matrix).

## 3. Eksekusi & Hasil Kanonikal
* **Notebook:** [`notebooks/E1_Clean_Retrieval.ipynb`](../../notebooks/E1_Clean_Retrieval.ipynb)
* **Tabel Hasil Resmi (`results/processed/clean_retrieval_table.csv`):**

| Representasi | Top-1 Accuracy (%) | mAP@10 | MRR | Precision@10 | Recall@10 |
|---|:---:|:---:|:---:|:---:|:---:|
| **$R_2$: BirdNET Backbone (1024-d)** | **81.67%** | **0.6370** | **0.8650** | **0.6942** | **0.2325** |
| **$R_1$: PANNs CNN14 (2048-d)** | **37.94%** | **0.1771** | **0.5090** | **0.2586** | **0.0843** |
| **$R_0$: MFCC Baseline (40-d)** | **18.01%** | **0.0690** | **0.3079** | **0.1308** | **0.0360** |
| **$R_3$: Random Control (40-d)** | **6.75%** | **0.0231** | **0.1811** | **0.0615** | **0.0150** |

* **Log Mentah:** Tersimpan di `results/raw/R{0,1,2,3}_Clean_raw.csv` lengkap dengan kolom pelacakan asal usul `noise_file = "None (Clean)"`.
* **Visualisasi:** Tersimpan di [`results/figures/clean_retrieval_benchmark.png`](../../results/figures/clean_retrieval_benchmark.png) dan [`paper/figures/clean_retrieval_benchmark.png`](../../paper/figures/clean_retrieval_benchmark.png).

## 4. Status Kelulusan
**LULUS 100%**.
