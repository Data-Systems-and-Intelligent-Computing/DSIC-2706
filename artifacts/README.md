# Artifacts

Folder ini menyimpan **registri artefak**, bukan duplikasi audio, cache, atau hasil mentah.

- `validated_artifact_registry.csv` mengindeks run tervalidasi, gambar laporan, tabel laporan, dan dokumen hasil.
- `reproducibility/manifest_sha256.txt` mencatat hash manifes aktif.
- Artefak eksperimen asal tetap aman di `results/reproductions/`.
- Salinan gambar dan tabel yang dipakai untuk laporan ada di `results/figures/` dan `results/tables/`; checksum sumbernya tercatat dalam `results/report_materials_manifest.json`.
