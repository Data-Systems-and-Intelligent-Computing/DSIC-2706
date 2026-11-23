# Source Code

`src/` memuat fungsi pipeline yang dipakai oleh kode eksperimen:

- `preprocess.py`, `mfcc.py`: standardisasi audio dan baseline akustik R0.
- `embeddings.py`: ekstraksi fitur PANNs CNN14 (R1) dan BirdNET (R2) dengan bobot tetap, serta pembentukan vektor kontrol acak berbasis identitas rekaman (R3).
- `retrieve.py`, `evaluate.py`: peringkat similarity dan metrik retrieval.
- `mix_noise.py`: pencampuran derau ITERA terkontrol untuk E2/E4.
- `calibrate_threshold.py`, `e3_alignment.py`: pemilihan satu ambang per representasi dari data kalibrasi dan penyelarasan skor dengan kueri uji E3.
- `analyze_failures.py`, `bootstrap_inference.py`, `plot_results.py`: E5, statistik, dan visualisasi.

Folder `dsic2706/` dipertahankan untuk kompatibilitas impor lama.
