# Bukti Reproduksi Terisolasi 16 Oktober 2026

Pipeline E0, ekstraksi clean R0–R3, E1, E2, E3, E5, dan statistik H3 selesai pada klon terpisah/venv baru. E4 tidak dijalankan ulang sesuai arahan pembimbing.

- [41 perbandingan dan checksum input](comparison_report.json): seluruhnya cocok; selisih numerik maksimum 0,0.
- [Catatan setiap tahap](pipeline_progress.json).
- [Lingkungan baru](environment.json) dan [versi dependensi aktual](requirements-resolved.txt).
- [Skrip pembanding saat pengujian](compare_fresh.py).
- [Indeks salinan output lokal](archived_local_outputs.json). Folder local-output/ tidak di-commit.
- [Protokol pengulangan dan batas klaim](../../../docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md).

Input audio/checkpoint dipulihkan dari arsip lokal terverifikasi, bukan diunduh ulang. Tidak ada embedding lama yang disalin. Hasil baru tidak menggantikan identitas atau hasil beku penelitian. Audit pendengaran manusia tidak dibuat oleh pipeline ini.

[Verifikasi akhir](final_verification.json) dan [skrip verifikasinya](verify_final.py) mencatat preservasi hasil sumber serta hash seluruh paket. Suite terbaru 36/36 lulus pada venv proyek dan venv baru; suite saat pipeline berjalan pada commit dasar berisi 32 tes.
