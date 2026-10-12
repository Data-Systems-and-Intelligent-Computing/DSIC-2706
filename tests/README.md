# Tests

`run_all_tests.py` dan `run_tests.py` di akar proyek menjalankan pemeriksaan integritas manifes, leakage split, cosine retrieval, mixing SNR, pembekuan threshold, serta reproducibility.

Struktur:

- `unit/`: perilaku fungsi kecil.
- `integration/`: hubungan manifest, retrieval, noise, dan threshold.
- `reproducibility/`: pemeriksaan provenance dan konfigurasi.

Validasi terakhir: 25 pemeriksaan lulus. Test tidak mengunduh data, menghapus data, atau menjalankan ulang E2–E5.
