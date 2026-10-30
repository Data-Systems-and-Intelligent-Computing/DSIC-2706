# Tests

Jalankan python -B run_tests.py dari akar proyek. Pada pemeriksaan 18 Oktober 2026 hasilnya:

| Status | Jumlah |
|---|---:|
| Total tes | 41 |
| Lulus | 41 |
| Dilewati / skipped | 0 |
| Gagal assertion | 0 |
| Error | 0 |

Jumlah sebelumnya 36 berubah karena satu tes dimensi model dipisah menjadi empat tes (R0–R3), serta ditambahkan dua regresi pelaporan. Tes yang kehilangan checkpoint/dependensi/audio mengangkat unittest.SkipTest; tidak lagi mencetak SKIP lalu kembali seolah lulus. Runner menghitung sukses melalui addSuccess, mencetak status secara terpisah, serta mencantumkan nama/alasan setiap skip. Dua regresi memeriksa pemisahan lulus/skip/failure/error dan missing checkpoint menjadi skip.

Isi suite: 28 pemeriksaan integritas/metode dasar termasuk empat dimensi model; lima H3; dua seleksi E5; tiga impor catatan pendengaran; satu provenance Git E4; dua pelaporan runner.

Nol skip di komputer ini berarti input/dependensi pemeriksaan tersedia saat pengujian. Pada checkout tanpa input, jumlah lulus dan skip dapat berbeda dan harus disalin dari hasil aktual. Catatan 16 Oktober tetap menjadi riwayat suite sebelumnya, bukan hasil baru untuk setiap lingkungan.

[Bukti ringkasan terbaru](../artifacts/reproducibility/test_summary_2026-10-18.json). Tes Git membandingkan seluruh 10 aset sumber E4 terlacak dengan SHA-256 beku pada file lokal dan Git HEAD. Fixture pengamatan pendengaran bersifat sintetis di memori dan tidak mengisi audit manusia.

Suite ini tidak menjalankan ulang E2–E5. [Reproduksi eksperimen](../docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md) dicatat terpisah. Inferensi E4 tetap tidak diulang.

## Pemeriksaan audit 30 Oktober 2026

[Verifikasi audit manusia](../Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/verifikasi_akhir.json) mencatat tujuh tes importer/finalizer lulus, nol dilewati/gagal/error, melalui `python -B -m unittest tests.test_e5_human_review_import tests.test_e5_human_review_finalize -v`. Ini pengujian khusus, bukan pengulangan seluruh suite 41 tes. Finalizer belum dimasukkan pada daftar modul `run_tests.py`; jangan menjumlahkan tujuh tes itu dengan 41 karena tes importer beririsan.

Catatan pendengaran Fabio tersedia untuk 120/120 kasus, tetapi lulus tes hanya memvalidasi logika/struktur/provenance, bukan pengalaman mendengar atau identitas spesies secara independen. Pembaruan README ini tidak menjalankan tes atau eksperimen lagi. Angka 41 pembandingan reproduksi juga berbeda dari 41 tes suite historis.
