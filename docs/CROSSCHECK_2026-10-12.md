# Crosscheck Pembaruan TA — 12 Oktober 2026

Pemeriksaan ini membaca sumber data dan artefak aktif di `D:\FILE AND TASK\TA`. Run audio E0–E5 tidak dijalankan ulang. Hasil di bawah adalah status bukti yang berhasil diperiksa, bukan pernyataan bahwa semua ancaman validitas penelitian telah hilang.

## Hasil yang cocok

| Area | Pemeriksaan | Hasil |
|---|---|---|
| Dataset | `scripts/audit_manifests.py` menghitung ulang SHA-256 seluruh 3.396 audio fisik dan membandingkan manifes | `PASS_WITH_WARNINGS`; partisi aktif 673 Gallery, 311 Query, 232 Calibration; 1.217 audio target fisik, 380 unknown fisik, 1.799 noise ITERA |
| XC42472 | File, ukuran, SHA-256, dan peran split dicocokkan dengan manifes | Ada: `data/xeno_canto_indonesia/savnig1/XC42472.mp3`, 689.576 byte, SHA-256 `b9c874aeb40d4d5f9092a21105627f7702206e34d99d8b5f39f50380e900a20c`, peran `query_clean` |
| E0/EDA | Metadata dan tabel aktif ada | E0 mengaudit 100 audio; EDA menginventaris 3.396 audio, 0 error decode, 101 ketidakcocokan ekstensi/container |
| E1 | Metadata R0–R3 ada; nilai Clean R1/R2 di raw E4 dicocokkan lagi dengan E1 | R1 `mAP@10=0,17626780`; R2 `mAP@10=0,63670852`, cocok persis |
| E2 | Berkas raw dan jumlah baris dihitung | 20 CSV untuk R0–R3 × lima kondisi; setiap CSV 311 query |
| E3 | Berkas raw dan jumlah baris dihitung | 1.860 baris calibration (4 representasi × 465) dan 12.420 baris test (4 × 5 kondisi × 621) |
| E4 | Identitas aset dan audit pendamping diverifikasi ulang | Semua SHA-256 aset sumber cocok; audit E4 menyatakan 320 snapshot kondisi, 324 baris agregat, dan backup ZIP valid |
| H3 | Ayunan retensi dihitung ulang secara independen dengan `groupby` dari raw E4 | R1 0,240111; R2 0,048607; selisih 0,191504, CI bootstrap 95% [0,152203; 0,241969]. Angka per SNR cocok dengan tabel H3 |
| E5 | Metadata dan tabel aktif ada | Ringkasan mode kegagalan 159 baris; manifest kasus pilihan 120 baris |
| Bahan laporan | Semua file dalam `results/report_materials_manifest.json` dicocokkan dengan SHA-256 | 41/41 cocok; 15 gambar dan 27 tabel ada di folder laporan. Matriks nomor 27 adalah turunan baru yang punya metadata provenance sendiri |
| Notebook | Delapan `.ipynb` dibaca sebagai JSON dan semua code cell diperiksa sintaksnya | JSON/sintaks valid. Sel runner adalah kode langsung di notebook; entry point eksperimen tidak dipanggil otomatis |
| Dokumentasi | Tautan relatif aktif diperiksa | Tidak ditemukan tautan putus dalam dokumen hasil, riset, bimbingan, notebook, dan naskah yang diperiksa |
| Tes kode | `run_tests.py` | 25 tes lulus |

## Koreksi selama crosscheck

1. [Matriks RQ/H terkini](../results/tables/27_rq_hypothesis_matrix_current.csv) sekarang menempatkan Sub-RQ3 pada E4/H3 dan Sub-RQ4 pada E5. [Matriks nomor 23](../results/tables/23_statistics_rq_hypothesis_matrix.csv) dipertahankan sebagai keluaran historis; jangan memakainya sebagai status RQ terbaru.
2. H3 dilaporkan sebagai dukungan untuk **kestabilan retensi lintas lokasi noise**. Uji inferensial ini ditambahkan setelah E4 selesai, sehingga interpretasinya eksploratif. Klaim mekanisme distorsi frekuensi tinggi/rendah belum diuji dengan fitur spektral noise per segmen. Penjelasan ini ditambahkan ke [hipotesis](research/hypotheses.md), [hasil lengkap](RESULTS_RQ_HYPOTHESES_2026-10-12.md), [naskah](../paper/manuscript.md), dan [status bimbingan](../Rencana-eksperimen-bimbingan/CURRENT_STATUS.md).
3. Angka 109 audio tidak dirujuk pada EDA dan 108 pada audit manifes berbeda karena EDA hanya memakai tiga manifes aktif, sedangkan audit juga membaca `indonesia_train.csv` historis. Berkas pembeda adalah `data/xeno_canto_indonesia/latnig1/XC1073401.mp3`.
4. Pembuat peta folder tidak lagi menimpa status bimbingan yang telah ditinjau. Kode analisis H3 juga menolak penimpaan bahan laporan yang berbeda bila dijalankan lagi.

## Temuan yang perlu ditangani sebelum GitHub diperbarui

**Prioritas tinggi — perubahan Git belum ditinjau seluruhnya.** Cabang lokal masih `main` pada commit `930f6f2ea381221ba29fa09227e86d3d3df1eb33`; pembaruan ini belum di-commit atau di-push. `git status` menunjukkan 163 berkas terlacak berstatus terhapus. Sebanyak 45 tercatat dalam [log penghapusan hasil lama yang terimputasi](restart_deleted_results_2026-10-11.json), sedangkan 118 lainnya meliputi notebook/scratch, skrip, hasil, artefak, serta berkas `paper/`. Status penghapusan itu harus ditinjau satu per satu sebelum commit/push. Crosscheck ini tidak menghapus atau memulihkan berkas-berkas tersebut.

**Prioritas metode — cakupan kesimpulan.** H3 menguji perbedaan ayunan retensi, bukan penyebab frekuensi tinggi/rendah. Lima profil lokasi bukan uji burung target yang direkam langsung di ITERA. Bootstrap H3 memasangkan query dan memakai segmen noise E4 yang tetap; ia tidak mengukur ketidakpastian terhadap lokasi baru atau sesi lapangan baru.

**Prioritas data — peringatan audit yang masih ada.** Terdapat satu pasangan audio fisik identik `XC1073400`/`XC1073401`, satu ID tambahan di log unduhan dan `indonesia_train.csv`, 30 grup folder/tanggal noise yang beririsan antara unknown calibration/test, serta author unknown yang tidak tersedia di manifes. Tidak ditemukan audio identik lintas peran pada audit ini, tetapi independensi sesi/perekam unknown dan status bird-free setiap audio belum dibuktikan. Jangan menghapus buffer/audio berdasarkan peringatan ini saja.

**Prioritas notebook — verifikasi eksekusi.** Code cell valid secara sintaks dan tidak memanggil runner eksperimen eksternal sebagai langkah utama. Notebook E4 menampilkan hasil E4/H3 yang tersimpan; ia tidak mengeksekusi ulang E4. Seluruh notebook belum dieksekusi ulang dari awal pada kernel baru dalam crosscheck ini, jadi status "dapat dijalankan end-to-end" belum dibuktikan oleh pemeriksaan sintaks.

## Rujukan aktif

- [Registri eksperimen](../experiments/experiment_registry.csv)
- [Hasil RQ dan hipotesis](RESULTS_RQ_HYPOTHESES_2026-10-12.md)
- [Matriks RQ/H terkini](../results/tables/27_rq_hypothesis_matrix_current.csv)
- [Tabel H3](../results/tables/24_h3_habitat_profile_stability.csv)
- [Grafik H3](../results/figures/15_h3_habitat_retention_stability.png)
- [Manifest bahan laporan](../results/report_materials_manifest.json)
