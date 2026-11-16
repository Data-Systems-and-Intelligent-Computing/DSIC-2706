# Peta Folder Aktif

`PROJECT_STRUCTURE.csv` memberi peta singkat seluruh folder utama. Gunakan peta berikut saat menulis laporan atau belajar kode.

| Folder | Fungsi |
|---|---|
| `data/` | Audio asli, manifes, dan registry data. |
| `checkpoints/` | Model beku R1/R2; tidak diubah. |
| `configs/` | Parameter eksperimen dan indeks run aktif. |
| `src/` | Implementasi pipeline. |
| `scripts/` | Runner dan pembangun indeks. |
| `notebooks/` | Satu notebook langsung per tahap/eksperimen. |
| `experiments/` | Registri E0–E5 yang menghubungkan notebook, run, figure, dan table. |
| `results/reproductions/` | Artefak sumber per run yang tidak ditimpa. |
| `results/figures/`, `results/tables/` | Grafik dan tabel keluaran kode eksperimen. |
| `results/artifacts/` | Registri bukti dan keluaran audit eksperimen. |
| `docs/` | Dokumen metode, catatan keputusan, dan audit historis di `docs/research/audits/`. |
| `paper/` | Naskah dan pustaka. `paper/figures/` menyimpan gambar untuk naskah dan `paper/tables/` untuk tabel naskah. |
| `tests/` | Pengujian integritas dan metode. |
| `learning/` | Latihan, panduan, dan arsip teori di `learning/teori_dasar/`. |
| `Rencana-eksperimen-bimbingan/` | Catatan pembimbing, logbook, dan audit pendengaran. |
| `Administrasi/` | Dokumen administrasi akademik. |
| `tmp/` | Pratinjau, berkas kerja sementara, dan cache alat. |
