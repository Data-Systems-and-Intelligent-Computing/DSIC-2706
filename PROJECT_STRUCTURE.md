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
| `results/figures/`, `results/tables/` | Bahan laporan yang mudah dicari, dengan checksum. |
| `artifacts/` | Registry bukti dan provenance. |
| `docs/` | Metode, hasil RQ/H, audit. |
| `paper/` | Draf naskah dan indeks figure/table terpilih. |
| `tests/` | Pengujian integritas dan metode. |
| `learning/` | Latihan pembelajaran yang tidak mengubah hasil resmi. |
| `Teori Dasar/` | Draf teori dan panduan historis; periksa penanda status sebelum memakai angka atau klaimnya. |
| `Audit Pembaruan/`, `Rencana-eksperimen-bimbingan/` | Catatan audit dan logbook historis. |
| `Administrasi/` | Dokumen administrasi akademik. |

Tidak ada data audio, checkpoint, cache, manifest, atau run eksperimen yang dipindahkan atau ditimpa oleh penataan ini.
