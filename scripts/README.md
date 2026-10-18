# Scripts

Folder ini menyimpan kode sumber runner dan pembangun indeks. Notebook di `notebooks/` memuat kode eksperimen yang sama sebagai code cell agar dapat dipelajari langsung.

Runner aktif yang sudah menghasilkan artefak tervalidasi:

- `run_e0_preprocessing_verification.py`, `run_eda_formal.py`, `run_e1_clean_r0.py`
- `materialize_e1_from_cache.py`, `run_e2_controlled_noise.py`, `run_e3_open_set.py`
- `run_e5_diagnostics.py`, `run_statistics_and_rq_matrix.py`
- `run_h3_sensitivity_reanalysis.py`: analisis H3 aktif, meliputi ayunan absolut/relatif dan tanpa Kebun Raya. Runner H3 12 Oktober tetap arsip metode sebelumnya.
- `prepare_e5_listening_review.py`: lembar audit kosong dengan pemulihan metadata kasus secara persis.
- `build_e5_listening_pack.py`: klip E5 terverifikasi dan halaman audit lokal; tidak menciptakan pengamatan manusia.

`run_e4_five_locations_v10_stage7.py.draft` adalah sumber run E4 historis yang tervalidasi; run E4 tidak dijalankan ulang. Berkas `build_experiment_registry.py` dan `curate_report_materials.py` hanya membuat indeks dan salinan bahan laporan dengan checksum.

Jangan menjalankan runner eksperimen untuk sekadar membuka notebook atau melihat hasil: gunakan artefak di `results/`.

Skrip pendukung penyelesaian 16 Oktober:

- import_e5_human_review.py memvalidasi JSON catatan pendengar dan menulis CSV baru, tanpa menimpa sumber.
- restore_reproduction_inputs.py memulihkan hanya input eksternal yang cocok SHA-256 pada klon terpisah, termasuk target VERIFIED_EXISTING, tanpa menyalin embedding lama.
- [Protokol reproduksi lingkungan baru](../docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md).

## Status E4 dan pembaruan 18 Oktober 2026

**run_e4_domain_shift.py TIDAK DIGUNAKAN**. Ini arsip runner tiga lokasi; eksekusi langsung dihentikan sebelum impor audio atau pembuatan output. Produsen run E4 lima lokasi yang sah adalah run_e4_five_locations_v10_stage7.py.draft, dipertahankan dengan hash historis; E4 tidak dijalankan ulang.

run_h3_leave_one_location_out.py menambah tabel sensitivitas dengan menghilangkan masing-masing dari lima lokasi secara bergantian, memakai raw AP@10 tersimpan, tanpa pencampuran audio/inferensi. [Hasil 60 baris dan metadata](../results/reproductions/H3_leave_one_location_out_20261018/README.md).
