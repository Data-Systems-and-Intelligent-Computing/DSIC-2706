# Artifacts

Folder ini menyimpan **registri artefak**, bukan duplikasi audio, cache, atau hasil mentah.

- `validated_artifact_registry.csv` mengindeks run tervalidasi, gambar laporan, tabel laporan, dan dokumen hasil.
- `reproducibility/manifest_sha256.txt` mencatat hash manifes aktif.
- Artefak eksperimen asal tetap aman di `results/reproductions/`.
- Salinan gambar dan tabel yang dipakai untuk laporan ada di `results/figures/` dan `results/tables/`; checksum sumbernya tercatat dalam `results/report_materials_manifest.json`.

Indeks dan manifest bahan laporan tersebut merekam paket pada waktu pembuatannya, bukan seluruh penambahan terbaru. Gunakan [matriks revisi 28](../results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv), [bukti reproduksi 16 Oktober](../results/reproductions/RECHECK_FRESH_20261016/README.md), dan [hasil audit manusia 30 Oktober](../Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md) untuk perkembangan sesudahnya. Catatan audit tersedia 120/120 kasus pilihan oleh satu pendengar; inferensi E4 tidak diulang.
