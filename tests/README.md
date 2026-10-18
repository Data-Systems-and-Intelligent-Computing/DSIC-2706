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
