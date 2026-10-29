# Sumber E4 dan reproduksi cache

E4 sudah selesai untuk **311 query × 5 lokasi × 4 SNR × 4 ulangan per representasi**: 24.880 evaluasi noisy per representasi, atau 99.520 untuk R0–R3. Jumlah tersebut adalah baris evaluasi, bukan query independen; checkout yang diperiksa berisi 320 snapshot kondisi dan delapan arsip NPZ lokal. Cache besar tidak perlu di-commit.

Runner yang benar-benar menghasilkan run aktif adalah [run_e4_five_locations_v10_stage7.py.draft](../../scripts/run_e4_five_locations_v10_stage7.py.draft), bukan runner lama tiga habitat. SHA-256 yang tercatat dalam [run_identity.json](../../results/reproductions/E4_5sites_20261011T213404_350219Z/run_identity.json):

```text
30cc0ea990e35eda70a98a6928550cb18df39bb4cd9b95837fafe05512f80c2c
```

Berkas produsen dipertahankan byte-for-byte, termasuk nama dan komentar pembuka lama yang masih menyebut tiga habitat. Desain aktual di dalam kode dan run identity memuat lima lokasi. Atribut Git khusus mencegah konversi akhir baris mengubah hash berkas ini.

Untuk membangun ulang **cache embedding clean saja** pada checkout terpisah yang memiliki audio asli dan checkpoint yang sesuai:

```bash
# Pemeriksaan hash sumber dan keberadaan audio; belum menulis cache.
python scripts/rebuild_e4_clean_caches.py --output-dir results/reproductions/E4_clean_cache_rebuild_local --check-only

# Opsional: ekstraksi ulang clean R0–R3 ke direktori baru.
python scripts/rebuild_e4_clean_caches.py --output-dir results/reproductions/E4_clean_cache_rebuild_local
```

Siapkan lingkungan sesuai requirements.txt, seluruh audio dalam manifes aktif, dan checkpoint lokal. R1 juga memerlukan class_labels_indices.csv pada direktori panns_data pengguna; extractor menolak mengunduhnya diam-diam. Builder memeriksa sumber terhadap identitas E4, menolak direktori keluaran yang sudah ada, serta menyimpan ID, label, hash manifes/checkpoint dan metadata cache baru. Ia tidak mencampur noise, menjalankan E4, menimpa cache lama, atau mengubah run_identity.json. Pemeriksaan --check-only memvalidasi sumber dan path audio; kesiapan dependensi/inferensi penuh diperiksa pada proses ekstraksi. Pada 16 Oktober, ekstraksi clean R0–R3 sudah berhasil pada venv baru dan menghasilkan embedding numerik identik dengan sumber.

Cache hasil rekonstruksi adalah provenance baru. Metadata membandingkan hash arsip baru dengan hash cache historis; kesamaan embedding tidak otomatis menjamin kesamaan byte arsip, versi runtime, atau hasil GPU. Runner historis stage7 memakai path dan checksum input yang dibekukan. Untuk resume run historis, pulihkan input historis yang persis cocok dari arsip, bukan mengganti hash identitas dengan hash cache baru. Kebutuhan reproduksi penelitian di kemudian hari dipisahkan dari revisi ini: **E4 tidak dijalankan ulang**.

Arsip NPZ/NPY, audio, checkpoint, dan cache sudah diabaikan oleh .gitignore. Hasil CSV dan metadata yang telah dilacak tetap dipertahankan. Analisis sensitivitas H3 hanya membutuhkan CSV E4 tersimpan:

```bash
# Gunakan nama baru setiap kali; keluaran yang sudah ada ditolak.
python scripts/run_h3_sensitivity_reanalysis.py --output-dir results/reproductions/H3_sensitivity_reproduction
```

[Kembali ke README utama](../../README.md).
