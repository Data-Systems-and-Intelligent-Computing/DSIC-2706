# Peta Folder Aktif

`PROJECT_STRUCTURE.csv` memberi peta singkat seluruh folder utama. Gunakan peta berikut saat menulis laporan atau belajar kode.

| Folder | Fungsi |
|---|---|
| `.git/` | Riwayat versi dan konfigurasi internal Git. |
| `.venv/` | Lingkungan Python yang digunakan di PC ini. |
| `data/` | Audio asli, manifes, dan registry data. |
| `checkpoints/` | Model beku R1/R2; tidak diubah. |
| `configs/` | Parameter eksperimen dan indeks run aktif. |
| `src/` | Implementasi pipeline. |
| `scripts/` | Runner dan pembangun indeks. |
| `notebooks/` | Satu notebook langsung per tahap/eksperimen. |
| `experiments/` | Registri E0–E5 yang menghubungkan notebook, run, figure, dan table. |
| `results/` | Hasil pengolahan dan evaluasi eksperimen. Subfolder utamanya dirinci di bawah. |
| `results/reproductions/` | Artefak sumber per run yang tidak ditimpa. |
| `results/figures/`, `results/tables/` | Grafik dan tabel keluaran kode eksperimen. |
| `results/artifacts/` | Registri bukti dan keluaran audit eksperimen. |
| `docs/` | Dokumen metode, catatan keputusan, dan audit historis di `docs/research/audits/`. |
| `paper/` | Naskah dan pustaka. `paper/figures/` menyimpan gambar untuk naskah dan `paper/tables/` untuk tabel naskah. |
| `tests/` | Pengujian integritas dan metode. |
| `learning/` | Latihan, panduan, dan arsip teori di `learning/teori_dasar/`. |
| `Teori Dasar/` | Draf teori dan arsip ilustrasi asli dari pembimbing. |
| `Rencana-eksperimen-bimbingan/` | Catatan pembimbing, logbook, dan audit pendengaran. |
| `Administrasi/` | Dokumen administrasi akademik. |
| `tmp/` | Pratinjau, berkas kerja sementara, dan cache alat. |

## Berkas penulisan

Naskah aktif dibuka melalui [main.tex](paper/template_ta_latex/main.tex). Cadangan lokal Bab I–III sebelum revisi dan pemulihan konflik editor disimpan di `paper/persiapan_bab1_3/cadangan_lokal/`. Jurnal dan metadata pustaka berada di [paper/bibliography](paper/bibliography/README.md).

Setelah pemeriksaan tata letak selesai, hapus gambar pratinjau dan log sekali pakai yang dibuat untuk pemeriksaan tersebut. Pertahankan PDF naskah dan berkas pendukung kompilasi aktif di `paper/template_ta_latex/build/`.
