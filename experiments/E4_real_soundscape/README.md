# Eksperimen E4 — Real Soundscape Domain Shift

## 1. Tujuan Ilmiah
Mengukur kesenjangan performa (*domain shift gap*) antara pengujian derau terkontrol (additive noise AudioMoth ITERA pada E2) dengan rekaman bentang alam asli hutan tropis (*real soundscape* dari `data/BirdClef/train_soundscapes/`).

## 2. Metodologi Eksperimen
* Mengambil segmen acak 5,0 detik dari 10.658 rekaman soundscape `.ogg` hutan tropis.
* Menyuntikkan derau soundscape tersebut ke 200 kueri bersih pada grid SNR yang persis sama dengan E2: Clean, 20 dB, 10 dB, 0 dB, dan -5 dB (`seed=42`).
* Mengevaluasi perolehan kesamaan kosinus terhadap galeri 3.653 rekaman.
* Membekukan ambang batas $\tau^* = 0.50$ tanpa kalibrasi ulang (*frozen protocol*).

## 3. Hasil Empiris & Komparasi Domain Shift (Model $R_2$ BirdNET)

| Kondisi Pengujian | $mAP@10$ (Derau Kampus ITERA / E2) | $mAP@10$ (Real Soundscape Hutan / E4) | Selisih (*Domain Shift Gap*) | Kesimpulan |
| :--- | :---: | :---: | :---: | :--- |
| **Clean** | **0.9126** | **0.9126** | 0.0000 | Baseline Identik |
| **SNR +20 dB** | 0.9068 | 0.9188 | +0.0120 | Sangat Stabil |
| **SNR +10 dB** | 0.8858 | 0.9026 | +0.0168 | Sangat Stabil |
| **SNR 0 dB** | 0.8317 | 0.8299 | -0.0018 | Penurunan Minimal |
| **SNR -5 dB** | **0.7707** | **0.7606** | **-0.0101** | **Tangguh (Robust)** |

## 4. Analisis Temuan Saintifik
* **Domain-Invariance:** Pada kondisi bising ekstrem (-5 dB), pergeseran domain dari derau kampus ke soundscape hutan tropis hanya menimbulkan penurunan performa sebesar **0.0101** (~1.0%).
* Hal ini membuktikan bahwa representasi beku BirdNET mengekstraksi struktur vokal yang invarian terhadap variasi lingkungan fisik (suara mesin kendaraan kampus vs suara serangga/hujan hutan tropis).

## 5. Artefak Terkait
* Tabel Data: [`paper/tables/e4_domain_shift_table.csv`](../../paper/tables/e4_domain_shift_table.csv)
* Diagram Batang: [`paper/figures/e4_domain_shift_bar.png`](../../paper/figures/e4_domain_shift_bar.png)
* Notebook Demonstrasi: [`notebooks/E4_Real_Soundscape_Domain_Shift.ipynb`](../../notebooks/E4_Real_Soundscape_Domain_Shift.ipynb)
* Skrip Eksekutor: [`notebooks/scratch_scripts/run_e4_domain_shift.py`](../../notebooks/scratch_scripts/run_e4_domain_shift.py)
* Notepad Penjelasan: [`notebooks/Penjelasan_Kode_E4.txt`](../../notebooks/Penjelasan_Kode_E4.txt)
