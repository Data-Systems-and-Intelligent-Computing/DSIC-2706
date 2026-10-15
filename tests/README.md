# Tests

`run_all_tests.py` dan `run_tests.py` di akar proyek menjalankan pemeriksaan integritas manifes, leakage split, cosine retrieval, mixing SNR, pembekuan threshold, provenance, lima tes metode H3, dan dua tes regresi seleksi E5.

Struktur:

- `unit/`: perilaku fungsi kecil.
- `integration/`: hubungan manifest, retrieval, noise, dan threshold.
- `reproducibility/`: pemeriksaan provenance dan konfigurasi.

Validasi 16 Oktober 2026: 32 pemeriksaan lulus melalui `python run_tests.py` (25 sebelumnya + 5 H3 + 2 E5). Tes tidak mengunduh data, menghapus data, atau menjalankan ulang E2–E5. Kelulusan ini bukan bukti reproduksi end-to-end E0–E5 pada lingkungan baru. Lima tes H3 juga lulus secara terpisah pada klon bersih yang memakai runtime Python yang sudah tersedia.
