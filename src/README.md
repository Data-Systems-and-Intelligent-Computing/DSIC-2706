# Source Code

`src/` memuat fungsi pipeline yang dipakai oleh kode eksperimen:

- `preprocess.py`, `mfcc.py`: standardisasi audio dan baseline akustik R0.
- `embeddings.py`: ekstraksi representasi beku R1/R2/R3.
- `retrieve.py`, `evaluate.py`: peringkat similarity dan metrik retrieval.
- `mix_noise.py`: pencampuran derau ITERA terkontrol untuk E2/E4.
- `calibrate_threshold.py`, `e3_alignment.py`: threshold open-set E3.
- `analyze_failures.py`, `bootstrap_inference.py`, `plot_results.py`: E5, statistik, dan visualisasi.

Folder `dsic2706/` dipertahankan untuk kompatibilitas impor lama.
