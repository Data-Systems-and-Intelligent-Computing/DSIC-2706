# Experiments

Folder ini adalah **registri eksperimen aktif**, bukan tempat menyimpan salinan hasil mentah.

- Setiap folder `E0_...` sampai `E5_...` memuat `experiment_registry.json`: status, notebook, kode asal, run tervalidasi, serta gambar dan tabel laporan terkait.
- `experiment_registry.csv` memberi ringkasan satu baris per eksperimen.
- Kode yang dapat dipelajari berada di `notebooks/`; run asal yang tidak diubah berada di `results/reproductions/`; gambar dan tabel yang siap dipakai laporan berada di `results/figures/` dan `results/tables/`.

Struktur ini membuat folder `experiments/` berfungsi sebagai pintu masuk dan peta provenance tanpa mengubah hasil eksperimen yang telah tervalidasi.

Untuk menghubungkan registri dengan naskah, E0 memeriksa audio dan E1 menetapkan kondisi acuan. E2 menjawab perubahan kualitas dan retensi, E3 menguji penerimaan kueri, E4 membandingkan derau lima lokasi, dan E5 memeriksa pola kegagalan. [Metode Bab III](../paper/template_ta_latex/chapters/bab3.tex) dan [log keputusan](../docs/research/decision-log.md) menjelaskan dasar perbandingan.
