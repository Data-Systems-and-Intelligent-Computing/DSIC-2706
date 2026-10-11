# Eksperimen E1 — Clean Retrieval Benchmark

## 1. Tujuan Ilmiah
Membangun tolok ukur dasar (*clean baseline*) kemampuan perolehan kemiripan (*similarity retrieval*) dari representasi audio terstandardisasi pada kondisi ideal (rekaman bersih bebas derau tambahan) lintas 20 spesies burung target korpus Avifauna Indonesia (Xeno-Canto).

## 2. Konfigurasi Eksperimen
* **Data Uji:** 310 kueri bersih dari 31 perekam independen.
* **Data Referensi (Gallery):** 674 rekaman galeri dari 60 perekam independen.
* **Representasi:**
  * $R_0$: MFCC Baseline (40-dim)
  * $R_1$: PANNs CNN14 (2048-dim)
  * $R_2$: BirdNET Backbone V2.4 (1024-dim)
  * $R_3$: Random Control (40-dim)
* **Metrik Kesamaan:** Cosine Similarity ($310 \times 674$ pairwise similarity matrix).

## 3. Eksekusi & Hasil Kanonikal
* **Notebook:** [`notebooks/E1_Clean_Retrieval.ipynb`](../../notebooks/E1_Clean_Retrieval.ipynb)
* **Tabel Hasil Resmi (`results/processed/clean_retrieval_table.csv`):**

| Representasi | Top-1 Accuracy (%) | mAP@10 | MRR | Precision@10 | Recall@10 |
|---|:---:|:---:|:---:|:---:|:---:|
| **$R_2$: BirdNET Backbone (1024-d)** | **81.61%** | **0.6358** | **0.8646** | **0.6932** | **0.2311** |
| **$R_1$: PANNs CNN14 (2048-d)** | **37.74%** | **0.1768** | **0.5079** | **0.2584** | **0.0839** |
| **$R_0$: MFCC Baseline (40-d)** | **18.06%** | **0.0691** | **0.3081** | **0.1310** | **0.0360** |
| **$R_3$: Random Control (40-d)** | **6.77%** | **0.0232** | **0.1815** | **0.0616** | **0.0150** |

* **Log Mentah:** Tersimpan di `results/raw/R{0,1,2,3}_Clean_raw.csv` lengkap dengan kolom pelacakan asal usul `noise_file = "None (Clean)"`.
* **Visualisasi:** Tersimpan di [`results/figures/clean_retrieval_benchmark.png`](../../results/figures/clean_retrieval_benchmark.png) dan [`paper/figures/clean_retrieval_benchmark.png`](../../paper/figures/clean_retrieval_benchmark.png).

## 4. Status Kelulusan
**LULUS 100%**.
