# Notebooks

Semua notebook ada di `D:\FILE AND TASK\TA\notebooks`. Satu eksperimen memakai satu notebook dan kodenya berada langsung pada code cell, bukan memanggil runner melalui `subprocess`.

| Notebook | Fungsi | Hasil yang dibaca |
|---|---|---|
| `01_Preprocessing.ipynb` | pembelajaran preprocessing | tidak membuat hasil resmi |
| `02_E0_Preprocessing_Audit.ipynb` | E0 | `results/figures/01_e0_audio_properties.png` dan tabel 01–03 |
| `03_EDA_Physical_Audio.ipynb` | EDA, waveform, spektrogram | gambar 02–07 dan tabel 04–09 |
| `04_E1_Clean_Retrieval.ipynb` | E1 R0–R3 | tabel 10 |
| `05_E2_Controlled_Noise.ipynb` | E2 | gambar 08, 14; tabel 11, 18 |
| `06_E3_Open_Set_Threshold.ipynb` | E3 | gambar 09; tabel 12, 13, 19 |
| `07_E4_Habitat_Noise_Sensitivity.ipynb` | E4 dan H3 | gambar 10, 15; tabel 14, 20, 24–26 |
| `08_E5_Failure_Diagnostics.ipynb` | E5 | gambar 11–13; tabel 15–17 |

Notebook E4 hanya menampilkan run tervalidasi dan tidak menjalankan ulang 320 kondisi. Hasil RQ dan H1–H5 ada di `docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md`.

Untuk kesimpulan gunakan [matriks revisi 28](../results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv), [sensitivitas H3 15 Oktober](../results/reproductions/H3_sensitivity_20261015/README.md), dan [penghilangan tiap lokasi 18 Oktober](../results/reproductions/H3_leave_one_location_out_20261018/README.md). Grafik/tabel H3 12 Oktober tetap historis; hasil reformulasi H3/H4 bersifat eksploratif.

[Catatan audit pendengaran E5 30 Oktober](../Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md) tersedia untuk 120/120 kasus pilihan oleh Fabio. Audit ini terpisah dari notebook diagnostik; lembar kosong persiapan tidak menunjukkan status ulasan terbaru. Tidak ada eksekusi ulang notebook atau eksperimen dalam pembaruan README ini.
