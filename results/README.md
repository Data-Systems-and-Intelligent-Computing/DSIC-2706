# Results

`reproductions/` menyimpan run sumber, konsolidasi cache, audit pendamping, dan analisis statistik. Ikuti [registri eksperimen](../experiments/experiment_registry.csv) untuk memilih run aktif. Bentuk metadata berbeda menurut tahap: E4 historis memakai `run_identity.json`, sementara run lain dapat memakai `metadata.json`. Keberadaan folder saja tidak menjadikan semua keluaran historis sebagai acuan terkini.

`figures/` dan `tables/` berisi bahan laporan yang mudah dicari. [Manifest bahan laporan 12 Oktober](report_materials_manifest.json) mencatat checksum paket saat itu, bukan seluruh penambahan sesudahnya. Analisis H3 revisi dan matriks 28 mempunyai provenance tersendiri; salinan laporan tidak menggantikan artefak asal.

Tabel E5 yang sangat besar tetap berada di sumbernya agar hasil per-query tidak diduplikasi tanpa kebutuhan laporan:

- `reproductions/E5_diagnostics_20261012T091512_868500Z/tables/all_query_diagnostics.csv`
- `reproductions/E5_diagnostics_20261012T091512_868500Z/tables/failure_cases.csv`

Untuk hasil RQ dan H1–H5, baca [ringkasan hasil](../docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md) dan [matriks revisi 28](tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv). Matriks 23/27 adalah riwayat; H3/H4 reformulasi eksploratif, dan H3 asli real-soundscape belum diuji.

- [Sensitivitas H3 15 Oktober](reproductions/H3_sensitivity_20261015/README.md) dan [penghilangan tiap lokasi 18 Oktober](reproductions/H3_leave_one_location_out_20261018/README.md) membaca raw E4 tersimpan. E4 berisi 320 snapshot dan 99.520 evaluasi noisy atas 311 query, bukan query independen sebanyak itu.
- [Reproduksi 16 Oktober](reproductions/RECHECK_FRESH_20261016/README.md): 41/41 pembandingan cocok pada venv baru di komputer yang sama; inferensi E4 dikecualikan.
- [Audit manusia 30 Oktober](../Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md): 120/120 catatan kasus pilihan oleh satu pendengar, terpisah dari E5 komputasional. Ini tidak mengestimasi frekuensi kegagalan seluruh populasi.
