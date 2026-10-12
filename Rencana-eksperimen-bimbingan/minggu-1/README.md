# Minggu 1 — Dataset, Preprocessing, EDA, E0, dan E1

**Tujuan:** membangun fondasi data, memastikan preprocessing valid, memahami kondisi audio fisik, lalu mengukur clean retrieval sebelum noise ditambahkan.

## Data dan pembagian aktif

| Komponen | Jumlah | Bukti |
|---|---:|---|
| Gallery | 673 | [dataset_split.csv](../../data/manifests/dataset_split.csv) |
| Query clean | 311 | [dataset_split.csv](../../data/manifests/dataset_split.csv) |
| Calibration | 232 | [dataset_split.csv](../../data/manifests/dataset_split.csv) |
| Target species | 20 | [species freeze](../../data/manifests/indonesia_species_freeze.csv) |
| Audio target terdaftar | 1.216 | [dataset registry](../../data/dataset_registry.csv) |

Split memakai perekam yang dipisahkan secara global. Pemeriksaan leakage dan integritas dilakukan oleh [tests/](../../tests/) dan [run_tests.py](../../run_tests.py).

## Preprocessing

Audio dibaca, menjadi mono 32 kHz, dipilih jendela energi 5 detik, lalu dinormalisasi ke RMS 0,05. Preprocessing adalah tahap persiapan audio; **R0 bukan preprocessing**, melainkan baseline retrieval MFCC yang bekerja setelah preprocessing.

- Notebook belajar: [01_Preprocessing.ipynb](../../notebooks/01_Preprocessing.ipynb)
- Kode pipeline: [src/preprocess.py](../../src/preprocess.py)
- Konfigurasi audio: [configs/audio.yaml](../../configs/audio.yaml)
- Audit E0: [02_E0_Preprocessing_Audit.ipynb](../../notebooks/02_E0_Preprocessing_Audit.ipynb)

### E0 — bukti audit

Audit deterministik 100 rekaman menemukan 20 spesies, durasi asli median 31,8648 detik, 6 mismatch ekstensi/container, 0 error decode, dan 0 kegagalan panjang maupun nilai non-finite setelah preprocessing.

- Run sumber: [E0](../../results/reproductions/E0_20261011_202557/)
- Tabel ringkas: [E0 summary](../../results/tables/01_e0_summary.csv)
- Tabel rekaman audit: [E0 per recording](../../results/tables/03_e0_per_recording.csv)
- Gambar: [E0 audio properties](../../results/figures/01_e0_audio_properties.png)

## EDA fisik

EDA menginventaris 3.396 audio fisik: 1.216 target aktif, 1.799 noise ITERA, dan 543 unknown/open-set. Tidak ditemukan error decode soundfile. Terdapat 101 mismatch ekstensi/container serta 109 audio fisik yang belum dirujuk oleh manifes yang diaudit; keduanya dicatat untuk audit dan bukan alasan menghapus file.

- Notebook: [03_EDA_Physical_Audio.ipynb](../../notebooks/03_EDA_Physical_Audio.ipynb)
- Inventaris lengkap: [EDA physical audio inventory](../../results/tables/07_eda_physical_audio_inventory.csv)
- Waveform/spektrogram contoh: [gambar EDA](../../results/figures/03_eda_bird_waveform_spectrogram_examples.png)
- Distribusi durasi dan sample rate: [gambar EDA](../../results/figures/04_eda_duration_sampling_rate.png)
- Profil noise ITERA: [gambar EDA](../../results/figures/05_eda_itera_noise_spectrogram_profiles.png)

## E1 — clean retrieval

Empat representasi dievaluasi pada 311 query terhadap 673 Gallery: R0 MFCC, R1 PANNs CNN14, R2 BirdNET, dan R3 kontrol ID-deterministik.

| Representasi | Top-1 | mAP@10 | Recall@10 |
|---|---:|---:|---:|
| R0 | 0,1833 | 0,0694 | 0,0363 |
| R1 | 0,3762 | 0,1763 | 0,0842 |
| R2 | 0,8167 | 0,6367 | 0,2331 |
| R3 | 0,0643 | 0,0211 | 0,0141 |

- Notebook: [04_E1_Clean_Retrieval.ipynb](../../notebooks/04_E1_Clean_Retrieval.ipynb)
- Tabel E1: [clean retrieval summary](../../results/tables/10_e1_clean_retrieval_summary.csv)
- Cache R1–R3: [results/features](../../results/features/)
- Run R0: [E1 R0](../../results/reproductions/E1_R0_20261011_175321/)
- Run konsolidasi cache: [E1 R1](../../results/reproductions/E1_R1_cache_20261012T021032_566409Z/), [R2](../../results/reproductions/E1_R2_cache_20261012T021034_128124Z/), [R3](../../results/reproductions/E1_R3_cache_20261012T021035_119528Z/)

**Keputusan Minggu 1:** R2 menjadi representasi dengan retrieval bersih tertinggi. Hasil ini menjadi baseline untuk E2, bukan bukti ketahanan terhadap noise.
