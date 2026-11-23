# Artifacts

Folder ini menyimpan **registri artefak**, bukan duplikasi audio, cache, atau hasil mentah.

## Berkas acuan BAB 3

| Keperluan | Berkas yang dipakai |
|---|---|
| Pembagian burung target | [dataset_split.csv](../../data/manifests/dataset_split.csv) memuat 673 rekaman galeri, 311 kueri uji, dan 232 rekaman kalibrasi. [download_manifest.csv](../../data/manifests/download_manifest.csv) menyimpan ID sumber, jalur berkas, dan SHA-256 rekaman target. |
| Kumpulan derau dan pembagian kontrol | [itera_noise_manifest.csv](../../data/manifests/itera_noise_manifest.csv) menginventarisasi 1.799 berkas. [unknown_open_set_manifest.csv](../../data/manifests/unknown_open_set_manifest.csv) menetapkan 233 kontrol kalibrasi dan 310 kontrol uji, termasuk 271 berkas derau yang dicadangkan dari bank pencampuran. [Identitas run E2](../reproductions/E2_controlled_20261012T021600_897497Z/run_identity.json) dan [metadata E3](../reproductions/E3_open_set_20261012T022548_802536Z/metadata.json) mencatat manifes dan pengaturan yang dipakai. |
| Kode dan parameter eksperimen | [Registri eksperimen](../../experiments/experiment_registry.csv) menunjuk skrip, notebook, dan run sumber E0–E5. [Indeks run](../../configs/active_runs.json) menunjuk folder yang memuat `metadata.json` atau `run_identity.json` untuk memeriksa parameter yang dipakai. [Identitas run lima lokasi](../reproductions/E4_5sites_20261011T213404_350219Z/run_identity.json) mencatat parameter dan aset E4. |
| Analisis lanjutan dan audit | [Analisis penghilangan tiap lokasi](../reproductions/H3_leave_one_location_out_20261018/README.md) menelusuri hasil E4 yang dianalisis ulang. [Daftar 120 kasus E5](../reproductions/E5_diagnostics_20261012T091512_868500Z/tables/selected_case_manifest.csv) dan [hasil audit pendengaran](../../Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md) menghubungkan kasus terpilih dengan catatan pendengar. |

Manifes, kode, dan metadata run dilacak melalui Git. Audio asli berada di `data/xeno_canto_indonesia/`, `data/xeno_canto_indonesia_unknowns/`, dan `data/itera_noise/`. Kedua bobot model tercantum di [registri model](../../checkpoints/model_registry.csv). Audio, bobot, dan cache fitur disimpan di luar riwayat Git. Untuk memulihkan input ke salinan proyek lain, ikuti [panduan reproduksi](../../docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md) dan [skrip pemulihan yang memeriksa SHA-256](../../scripts/restore_reproduction_inputs.py). Bukti pengujian juga mencatat [versi pustaka](../reproductions/RECHECK_FRESH_20261016/requirements-resolved.txt) dan identitas berkas label PANNs.

<details>
<summary>Draf paragraf untuk naskah</summary>

Untuk menelusuri kembali eksperimen, daftar rekaman yang dipakai sebagai galeri, kueri uji, kalibrasi, dan kontrol disimpan dalam manifes di `data/manifests`. Manifes tersebut juga digunakan untuk menelusuri berkas derau yang tersedia untuk pencampuran. Indeks di `results/artifacts/README.md` merujuk langsung ke manifes, kode pelaksana, serta catatan parameter dan keluaran tiap eksperimen. Berkas audio dan bobot model disimpan secara terpisah dari Git, dengan nilai SHA-256 untuk memeriksa kesesuaiannya dengan berkas yang digunakan.

</details>

## Indeks dan catatan historis

- `validated_artifact_registry.csv` mengindeks run tervalidasi, gambar laporan, tabel laporan, dan dokumen hasil.
- `reproducibility/manifest_sha256.txt` mencatat hash manifes pada audit 11 Oktober. Untuk manifes kontrol yang dipakai dalam pengujian ini, gunakan hash yang tercatat dalam metadata E3.
- Artefak eksperimen asal tetap aman di `results/reproductions/`.
- Salinan gambar dan tabel yang dipakai untuk laporan ada di `results/figures/` dan `results/tables/`; checksum sumbernya tercatat dalam `results/report_materials_manifest.json`.

Indeks dan manifest bahan laporan tersebut merekam paket pada waktu pembuatannya, bukan seluruh penambahan terbaru. Gunakan [matriks revisi 28](../tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv), [bukti reproduksi 16 Oktober](../reproductions/RECHECK_FRESH_20261016/README.md), dan [hasil audit manusia 30 Oktober](../../Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md) untuk perkembangan sesudahnya. Audit satu pendengar mencakup 120 kasus pilihan. Pemeriksaan Oktober dan [pengulangan E4 November](../reproductions/E4_5sites_20261116T131634_985229Z/run_identity.json) memiliki identitas terpisah. [Log keputusan](../../docs/research/decision-log.md) merangkum perbandingan hasilnya.
