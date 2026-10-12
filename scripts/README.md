# Scripts

Folder ini menyimpan kode sumber runner dan pembangun indeks. Notebook di `notebooks/` memuat kode eksperimen yang sama sebagai code cell agar dapat dipelajari langsung.

Runner aktif yang sudah menghasilkan artefak tervalidasi:

- `run_e0_preprocessing_verification.py`, `run_eda_formal.py`, `run_e1_clean_r0.py`
- `materialize_e1_from_cache.py`, `run_e2_controlled_noise.py`, `run_e3_open_set.py`
- `run_e5_diagnostics.py`, `run_statistics_and_rq_matrix.py`, `run_h3_habitat_profile_stability.py`

`run_e4_five_locations_v10_stage7.py.draft` adalah sumber run E4 historis yang tervalidasi; run E4 tidak dijalankan ulang. Berkas `build_experiment_registry.py` dan `curate_report_materials.py` hanya membuat indeks dan salinan bahan laporan dengan checksum.

Jangan menjalankan runner eksperimen untuk sekadar membuka notebook atau melihat hasil: gunakan artefak di `results/`.
