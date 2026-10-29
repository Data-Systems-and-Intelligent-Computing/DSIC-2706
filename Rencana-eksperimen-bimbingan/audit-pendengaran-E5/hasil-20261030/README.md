# Hasil audit pendengaran E5 dan progres bimbingan

**Tanggal laporan: 30 Oktober 2026.** Pendengar: Fabio Banyu Cyto. Sebanyak **120/120 kasus pilihan mempunyai catatan pendengaran** dan lolos validasi struktur serta identitas sumber. Tidak ada baris pending atau needs_follow_up pada ekspor. Ini bukti pelaksanaan audit oleh satu pendengar berdasarkan catatannya; pemeriksaan perangkat lunak tidak mengesahkan identitas spesies atau pengalaman mendengar secara independen.

## 1. Bukti dan koreksi yang disetujui

- [JSON asli](E5_catatan_pendengaran_asli.json) disimpan identik byte dengan berkas yang dikirim Fabio.
- [JSON hasil satu koreksi](E5_catatan_pendengaran_terkoreksi.json) mengubah hanya E5_105, `query_vocalisation_audible`, dari `uncertain` ke `yes`.
- Fabio mengonfirmasi salah tekan: “itu kepencet yang ragu (aslinya terdengar jelas)”. [Catatan koreksi](koreksi_E5_105.json) menyimpan alasan, otorisasi, dan hash sebelum/sesudah.
- [CSV gabungan 120 kasus](../E5_HASIL_ULASAN_2026-10-30.csv) mempertahankan kolom eksperimen sumber dan seluruh teks pengamatan asli. Tanggal pendengaran tidak diganti dengan waktu pengolahan.
- [Ringkasan hitungan](ringkasan_pendengaran.json), [manifest hash](manifest_artefak.json), dan [log pengerjaan](LOG_AUDIT.md) tersedia untuk pemeriksaan.

Periode waktu catatan, pada UTC+07:00: **2026-10-25T13:15:40.565000+07:00** sampai **2026-10-30T01:12:44.845000+07:00**. File kosong sumber serta metadata persiapan 16 Oktober tetap menjadi riwayat. Status nol ulasan pada dokumen persiapan lama tidak menggambarkan hasil impor 30 Oktober ini.

## 2. Cara analisis dan satuan hitung

Penggabungan memakai `case_id`, hash setiap baris, dan hash lembar sumber melalui importer yang sudah ada. Seluruh label, representasi, kondisi, skor, dan ambang tetap berasal dari E5 terdahulu. Analisis hanya menghitung kategori isian manusia secara deskriptif, lalu mengelompokkannya menurut representasi, kondisi, dan jenis kegagalan komputer.

Terdapat **80 kueri unik** dan **117 pasangan kueri–kondisi unik**. Unit hitung tabel adalah 120 baris kasus pilihan. Sampel dipilih menurut jenis kegagalan: masing-masing 40 false rejection, confusion, dan collapse; masing-masing representasi 30 kasus; masing-masing kondisi 24 kasus. Komposisi pilihan ini tidak mengestimasi frekuensi kegagalan pada seluruh kueri. Tidak dilakukan uji signifikansi yang menganggap 120 kasus independen.

## 3. Hasil keterdengaran

| Audio yang dinilai | Terdengar (yes) | Tidak terdengar (no) | Ragu (uncertain) | Penyebut |
|---|---:|---:|---:|---:|
| Kueri sesuai kondisi | 116 (96.67%) | 4 (3.33%) | 0 | 120 kasus |
| Hasil Top-1 | 109 (90.83%) | 8 (6.67%) | 3 (2.50%) | 120 kasus |

Pada **106 kasus**, kueri dan Top-1 sama-sama dinyatakan terdengar. Pada subset **90 kasus R0/R1/R2**, kueri terdengar pada **87/90 kasus**. R3 dipisahkan karena vektornya bergantung pada ID, bukan waveform; retensi atau dugaan distraksi audio pada R3 tidak boleh ditafsirkan seperti model audio.

### Menurut representasi

| Kelompok | Kasus | Kueri yes / no / ragu | Top-1 yes / no / ragu |
|---|---:|---:|---:|
| R0 | 30 | 29 / 1 / 0 | 26 / 2 / 2 |
| R1 | 30 | 30 / 0 / 0 | 28 / 1 / 1 |
| R2 | 30 | 28 / 2 / 0 | 30 / 0 / 0 |
| R3 | 30 | 29 / 1 / 0 | 25 / 5 / 0 |

### Menurut kondisi

| Kelompok | Kasus | Kueri yes / no / ragu | Top-1 yes / no / ragu |
|---|---:|---:|---:|
| Clean | 24 | 21 / 3 / 0 | 22 / 2 / 0 |
| SNR_-5dB | 24 | 24 / 0 / 0 | 20 / 2 / 2 |
| SNR_0dB | 24 | 23 / 1 / 0 | 22 / 1 / 1 |
| SNR_10dB | 24 | 24 / 0 / 0 | 22 / 2 / 0 |
| SNR_20dB | 24 | 24 / 0 / 0 | 23 / 1 / 0 |

Clean berarti tidak diberi derau tambahan pada eksperimen. Rekaman sumber masih dapat mempunyai latar. Top-1 berasal dari galeri tetap, sehingga kategori Top-1 pada kelompok SNR bukan hasil menyuntikkan SNR tersebut ke audio galeri.

### Menurut jenis kegagalan komputer

| Kelompok | Kasus | Kueri yes / no / ragu | Top-1 yes / no / ragu |
|---|---:|---:|---:|
| Open-set false rejection | 40 | 40 / 0 / 0 | 38 / 1 / 1 |
| Top-1 confusion above threshold | 40 | 37 / 3 / 0 | 33 / 5 / 2 |
| Total retrieval collapse | 40 | 39 / 1 / 0 | 38 / 2 / 0 |

False rejection berarti hasil pertama berspesies sesuai metadata tetapi skornya di bawah ambang. Confusion berarti hasil pertama berbeda spesies dan skornya melewati ambang. Label operasional collapse berarti hasil pertama salah dan skor maksimum di bawah ambang; label itu tidak membuktikan sepuluh hasil semuanya salah.

## 4. Pembahasan yang didukung catatan

Sebagian besar kueri pada kasus kegagalan yang dipilih masih mengandung suara burung yang terdengar menurut Fabio. Ini menunjukkan bahwa kegagalan pada pilihan kasus ini tidak selalu bersamaan dengan hilangnya seluruh suara burung dari pendengaran. Keterdengaran oleh manusia dan keberhasilan ranking/ambang komputer merupakan ukuran yang berbeda. Mendengar suara burung juga belum membuktikan bahwa vokalisasi yang terdengar berasal dari spesies target metadata.

Empat kueri dinyatakan tidak terdengar: E5_018, E5_063, E5_064, E5_093. Top-1 diragukan pada E5_010, E5_015, E5_037. Kasus tersebut memperlihatkan batas penafsiran pendengaran ketika latar atau suara singkat menyulitkan pemeriksaan. Nama sumber latar seperti hujan, angin, air, mesin, atau serangga dalam catatan adalah kesan pendengar jika belum diukur/dikonfirmasi secara terpisah.

Contoh berikut menyalin interpretasi Fabio, termasuk ejaan aslinya:

| Kasus | Representasi / kondisi | Diagnosis komputer | Catatan pendengar (verbatim) |
|---|---|---|---|
| E5_001 | R0 / Clean | Open-set false rejection | Suara kicauan terdengar berbeda antara query (lebih kasar), dengan top 1(lebih halus) |
| E5_005 | R0 / Clean | Total retrieval collapse | Saya tidak bisa membedakan karena suara derau sangat kencang, apakah ini termasuk spesies yang sama |
| E5_018 | R0 / SNR_0dB | Total retrieval collapse | Suara query full derau dan suara top 1 kicauan burung lebih mendominasi |
| E5_037 | R1 / SNR_-5dB | Open-set false rejection | Suara top 1 dipenuhi dengan suara derau, belum bisa dipastikan adanya suara burung karena tertutup |
| E5_063 | R2 / Clean | Top-1 confusion above threshold | Saya mmasih belum bisa menentukan karena suara query tidak ada suara burung, dan kicauan pada top 1 hanya sekali |
| E5_105 | R3 / SNR_0dB | Top-1 confusion above threshold | Mungkin terdistraksi oleh suara derau yang sangat berisik |

Pada E5_001, metadata Top-1 sama spesiesnya dengan kueri walaupun kesan bunyinya berbeda. Perbedaan bunyi tidak otomatis membatalkan label spesies. Pada E5_105, kalimat “Mungkin terdistraksi ...” merupakan dugaan Fabio; karena kasus ini R3, kalimat tersebut tidak dijadikan mekanisme gangguan pada embedding berbasis ID.

## 5. Pemeriksaan konsistensi dan batas interpretasi

Terdapat 0 kelompok kueri–kondisi berulang dengan kategori keterdengaran berbeda, dan 0 kelompok rekaman Top-1 berulang dengan kategori berbeda. Daftar berikut dipertahankan sebagai pemeriksaan transparansi, tanpa mengganti pilihan pendengar:

- Tidak ada perbedaan kategori pada audio berulang yang diperiksa.

Pada E5_018, deskripsi latar menyebut Top-1 “hanya suara angin”, sementara pilihan Top-1 dan interpretasinya menyatakan kicauan terdengar. Kedua teks tetap disimpan sebagai ambiguitas redaksional; tidak ada koreksi tambahan tanpa konfirmasi Fabio. Laporan memakai kategori terstruktur untuk menghitung, bukan menebak pengganti jawaban dari kalimat bebas. Status `reviewed` menyatakan catatan sudah dibuat, bukan semua pengamatan sudah bebas ketidakpastian.

Audit hanya melibatkan satu pendengar dan tidak bersifat penilaian buta; halaman menampilkan identitas/diagnosis kasus. Tidak dihitung kesepakatan antarpendengar. Sampel dipilih dari kegagalan dan tidak memiliki kelompok pembanding sukses yang seimbang. Tidak disimpulkan penyebab kausal derau, jarak, serangga, atau sifat arsitektur. E4 tidak mendapat penambahan ciri akustik atau anotasi melalui audit ini.

## 6. Bahan pembahasan E5 untuk naskah (draf)

Audit pendengaran dilakukan oleh peneliti terhadap 120 kasus E5 yang telah dipilih berdasarkan kelompok representasi, kondisi, dan jenis kegagalan komputasional. Setiap kasus dihubungkan dengan identitas sumber dan pengamatan atas kueri serta hasil Top-1. Setelah satu koreksi isian yang dikonfirmasi peneliti, vokalisasi pada kueri dinyatakan terdengar pada 116 dari 120 kasus dan tidak terdengar pada 4 kasus. Vokalisasi pada Top-1 dinyatakan terdengar pada 109 kasus, tidak terdengar pada 8 kasus, dan diragukan pada 3 kasus. Temuan ini menunjukkan bahwa, dalam kasus kegagalan yang dipilih, keterdengaran vokalisasi oleh peneliti sering tetap ada ketika ranking atau keputusan ambang gagal menurut metadata. Penafsiran dibatasi oleh pemilihan kasus, pengulangan beberapa audio, pendengar tunggal, ketiadaan penilaian buta, dan ketidakpastian identitas sumber suara. Audit tidak digunakan untuk mengubah label acuan atau menyimpulkan penyebab kausal kegagalan.

Paragraf ini merupakan bahan pembahasan yang dapat ditinjau pembimbing. Persetujuan memulai atau mengesahkan bab skripsi tetap mengikuti bimbingan; paket ini tidak menulis ulang bab yang sudah ada.

## 7. Progres yang dapat dilaporkan

| Pekerjaan nomor 1–3 | Hasil 30 Oktober 2026 |
|---|---|
| Arsip dan ekspor audit | JSON asli, JSON terkoreksi, CSV 120 kasus, serta metadata sumber tersedia. |
| Analisis manusia–komputer | Tabel deskriptif menurut representasi, kondisi, dan jenis kegagalan; contoh kasus dan batas analisis tersedia. |
| Pembahasan dan progres | Laporan ini menyediakan pembahasan E5 dan draf paragraf naskah. |
| Integritas | Hanya satu nilai isian manusia berubah atas konfirmasi Fabio; sumber eksperimen tidak ditimpa. Bukti pemeriksaan akhir dicatat pada log dan manifest. |
| Publikasi GitHub | Status commit/push ditambahkan ke log setelah pemeriksaan lingkup perubahan. |

Pelaporan audit manusia dapat diperbarui menjadi **catatan tersedia 120/120, satu pendengar**, dengan batas dan ambiguitas di atas. Ini tidak otomatis mengesahkan seluruh Gate 4 atau seluruh naskah. Inferensi E4 tetap tidak diulang dan hasil reproduksi terdahulu dipertahankan sebagai riwayat.

## 8. Mengulangi pengolahan catatan di direktori baru

Jalankan dari akar proyek, gunakan direktori dan nama CSV yang belum ada:

```powershell
.\.venv\Scripts\python.exe -B scripts/finalize_e5_human_review.py --review-json Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/E5_catatan_pendengaran_asli.json --output-dir Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-ulangan-baru --csv-output Rencana-eksperimen-bimbingan/audit-pendengaran-E5/E5_HASIL_ULASAN_ULANGAN.csv --confirm-e5-105-query-audible
```

Flag konfirmasi hanya digunakan karena Fabio sudah secara eksplisit mengoreksi E5_105 dalam percakapan ini. Skrip tidak mengisi atau menafsirkan pengamatan manusia baru. Pengulangan pengolahan ini tidak melibatkan audio, embedding, atau inferensi E0–E5.
