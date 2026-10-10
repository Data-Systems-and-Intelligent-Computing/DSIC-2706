# Arsip Hasil Eksperimen Regime BirdCLEF+ 2026 (Neotropis)

Direktori ini menyimpan seluruh artefak hasil eksperimen, tabel metrik mentah (*raw*), tabel olahan (*processed*), visualisasi (*figures*), dan manifes partisi dari **Regime BirdCLEF+ 2026** (20 spesies burung Neotropis Amerika Selatan, 4.351 audio klip).

## Rationale Pengarsipan
Sesuai arahan pembimbing (Pak Ardika Satria) per 10 Oktober 2026:
1. Domain spesies digeser dari burung Neotropis ke burung daratan tropis Indonesia (Kepulauan Sunda/Indonesia) untuk menyelaraskan habitat dengan bank derau fisik AudioMoth ITERA (Sumatera).
2. Seluruh hasil eksperimen lama disimpan secara permanen di arsip ini untuk keperluan audit dan transparansi ilmiah.
3. Eksperimen aktif utama repositori beralih ke 20 spesies burung umum Indonesia yang diunduh dari Xeno-Canto.

## Isi Arsip
- `processed/`: Tabel evaluasi benchmark E1 s.d. E5 (mAP@10, Top-1, kalibrasi threshold Youden's J, uji retensi).
- `raw/`: Skor metrik per-query mentah untuk R0 (MFCC), R1 (PANNs), R2 (BirdNET), R3 (Random).
- `figures/`: Grafik visualisasi benchmark retrieval dan pergeseran domain.
- `manifests/`: Manifes partisi `dataset_split.csv` (3.653 galeri, 200 kueri, 498 kalibrasi), `species_freeze.csv`, dan `Metadata_BirdCLEF.xlsx`.
