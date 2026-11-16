# Kumpulan gambar BAB III

Gambar disiapkan untuk ditinjau sebelum dipilih dan dimasukkan ke naskah. Penanda A–F menghubungkan diagram utama dengan diagram lanjutan; penomoran gambar skripsi ditentukan ketika gambar dipilih. PNG untuk peninjauan dan SVG untuk penyuntingan tersedia untuk setiap gambar.

| Berkas | Cakupan |
|---|---|
| `revisi_01_alur_keseluruhan.png` | Alur penelitian dan cabang E1–E5; audit E0 dicantumkan pada prapemrosesan. |
| `revisi_A_pemilihan_dan_pembagian_data.png` | Sumber serta pembagian rekaman target, derau, dan kontrol. |
| `revisi_B_prapemrosesan_audio.png` | Pemilihan durasi, normalisasi RMS, dan batas amplitudo. |
| `revisi_C_empat_representasi.png` | Jalur MFCC, PANNs, BirdNET, dan kontrol acak berbasis identitas. |
| `revisi_D_pengujian_kualitas_dan_lokasi.png` | Acuan E1, pengujian E2/E4, metrik, dan analisis kestabilan. |
| `revisi_E_ambang_dan_diagnostik.png` | Kalibrasi dan penerapan ambang E3 serta hubungan dengan diagnostik E5. |
| `revisi_F_kategori_kegagalan.png` | Pengelompokan hasil Top-1 dan keputusan ambang serta audit pendengaran E5. |
| `04_peta_lokasi_rekaman.png` | Lokasi rekaman dari 20 label spesies yang memiliki metadata koordinat. |

Alur D menjelaskan E1, E2, dan E4; alur E menjelaskan E3 dan hubungannya dengan E5; alur F memperinci E5. Diagram dibuat berdasarkan kode serta hasil yang tersimpan, bukan eksperimen baru. E5 menggunakan ciri akustik yang tersedia dan audit 120 kasus E2 pilihan; ini tidak berarti seluruh data E4 mempunyai ciri akustik atau telah didengarkan. Label operasional *total retrieval collapse* pada E5 berarti Top-1 salah dan skor di bawah ambang, bukan bahwa seluruh hasil salah.

Peta menampilkan lokasi rekaman, bukan seluruh persebaran alami spesies. Dari 1.216 rekaman target, 1.163 memiliki koordinat dan 53 tidak; terdapat 371 pasangan koordinat unik sehingga sejumlah titik bertumpuk. Sebagian metadata berada di luar Indonesia atau dekat perbatasan. Batas peta berasal dari [Natural Earth 1:50m](https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-countries/), sehingga garis pantai, pulau kecil, dan titik pesisir tidak selalu berimpit secara tepat. Koordinat berasal dari `data/manifests/dataset_split.csv` dan tidak diubah.

Jalankan `buat_diagram_rinci.py` untuk membuat ulang diagram revisi dan `buat_gambar.py` untuk membuat ulang peta dari manifes serta `ne_50m_admin_0_countries.geojson`.
