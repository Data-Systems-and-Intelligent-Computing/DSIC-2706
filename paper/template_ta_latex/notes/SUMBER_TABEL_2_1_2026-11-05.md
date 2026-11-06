# Sumber dan pemeriksaan tabel 2.1 — 5 November 2026

Tabel 2.1 awalnya diisi dengan delapan artikel jurnal yang dipilih setelah pemeriksaan koleksi. Setelah arahan berikutnya, tabel diringkas menjadi lima studi: Ghani (2023), Ghaffari–Devos (2024), Clark (2023), Fairbairn (2025), dan Lostanlen (2019). BIRB tetap menjadi rujukan pada BAB I, tetapi tidak dimasukkan sebagai baris jurnal karena versi yang disimpan berstatus preprint. Daftar delapan sumber yang semula ditelaah memakai Ghani (2023), Ghani (2025), Ghaffari–Devos (2024), Clark (2023), Fairbairn (2025), Kong (2020), Kahl (2021), dan Lostanlen (2019).

PDF sumber dibaca dari `paper/bibliography/`; nomor halaman berikut adalah halaman PDF, bukan selalu nomor halaman artikel.

| Baris | Kunci sitasi | Bukti sumber yang diperiksa | Batas ringkasan |
|---|---|---|---|
| 1 | `ghani2023embeddings` | PDF `Global birdsong embeddings enable superior transfer learning.pdf`, hlm. 1–3: empat kelompok hewan; encoder tetap; klasifikator linear; ROC-AUC dan ketepatan hasil pertama. | Keunggulan representasi khusus burung berlaku pada evaluasi klasifikasi artikel; tidak menjadi hasil pencarian berderau TA. |
| 2 | `ghani2025generalization` | PDF `Ghani_2025_Birdsong_transfer_generalization.pdf`, hlm. 1 dan 6: Xeno-canto, Observation.org, Dawn Chorus; penyesuaian bobot dan distilasi; generalisasi pada rekaman lingkungan. | *Shallow fine-tuning* melampaui distilasi pada evaluasi rekaman lingkungan artikel. TA tidak mengadopsi pelatihan ulang tersebut. |
| 3 | `ghaffari2024frontends` | PDF `Ghaffari_2024_Audio_frontends_bird_recognition.pdf`, hlm. 1, 3–4, dan 8: 10 spesies Eropa Barat, delapan kelas ESC-50, normalisasi/kompresi, dan *noise tolerance*. | Eksperimen artikel berfokus pada pengenalan spesies, berbeda dari pencarian dengan galeri tetap pada TA. |
| 4 | `clark2023soundscape` | PDF `Clark_2023_Soundscape_composition.pdf`, hlm. 1: pengembangan pada 54 spesies, evaluasi 37 spesies, dan hubungan komposisi suara dengan kesalahan. | Hubungan statistik tidak ditulis sebagai bukti sebab-akibat. Angin adalah contoh geofoni, bukan satu-satunya gangguan. |
| 5 | `fairbairn2025birdnet` | PDF `Fairbairn_2025_BirdNET_expert_monitoring.pdf`, hlm. 1–2: satu lokasi Munich, 23 spesies menurut pakar, 24 kombinasi pengaturan, empat agregasi waktu, F1 0,46–0,84. | Angka F1 bergantung pengaturan/agregasi. Ambang kepercayaan klasifikator dibedakan dari ambang kosinus TA. |
| 6 | `kong2020panns` | PDF `PANNs Large-Scale Pretrained Audio Neural Networks for Audio Pattern Recognition.pdf`, hlm. 1–2 dan 6–9: AudioSet 527 kategori; CNN14; tabel IV/VII/XI; mAP 0,431 dan vektor 2.048 dimensi. | Nilai 0,431 milik CNN14 pada pengenalan kategori AudioSet. Tidak tertukar dengan Wavegram-Logmel-CNN, skor pencarian, atau hasil TA. |
| 7 | `kahl2021birdnet` | PDF `BirdNET A deep learning solution for avian diversity monitoring.pdf`, hlm. 1: cakupan 984 spesies, pengujian rekaman satu spesies/lingkungan, dan peran augmentasi. | Artikel 2021 menjadi asal keluarga model; rincian tersebut tidak dianggap identik dengan BirdNET v2.4 yang digunakan TA. |
| 8 | `lostanlen2019robust` | PDF `Lostanlen_2019_Robust_bioacoustic_sensor_networks.pdf`, hlm. 1: rekaman migrasi malam 10 jam dari enam perekam; PCEN dan adaptasi konteks; variasi waktu dan sensor. | Tugas artikel adalah deteksi. Ringkasan mengacu pada pengurangan overfitting temporal/spasial, bukan pembuktian bahwa semua selisih kinerja hilang. |

Semua ringkasan ditulis ulang secara singkat. Metrik klasifikasi, deteksi, dan pencarian tidak dipakai untuk membuat peringkat lintas artikel. Relevansi dan pembeda rancangan TA tersimpan sebagai catatan pada audit ini; tabel memakai kolom hasil sebagaimana contoh pengguna.

## Sitasi dan koleksi

- Ditambahkan satu entri BibTeX untuk Ghani dkk. (2025), DOI `10.1038/s41598-025-00996-2`. Artikel dan PDF-nya sudah ada dalam koleksi; tidak ada unduhan atau perubahan CSV/Excel pada pekerjaan ini.
- `references.bib` kini memuat 18 entri. Sepuluh sumber BAB I tetap; setelah tabel diringkas, total sumber yang digunakan pada BAB I–II menjadi 11.
- Nomor sitasi ditentukan otomatis oleh `unsrt`, mengikuti kemunculan pertama di seluruh naskah. Nomor pada tabel tidak harus berurutan karena sebagian sumber sudah dikutip di BAB I.

## Format dan ruang lingkup

Caption pertama dan caption lanjutan dibuat tebal. Jarak sebelum tabel dan jarak caption ke garis atas masing-masing diatur 6 pt, hanya pada tabel ini. Mengikuti contoh PDF pengguna, enam kolom berisi nomor, judul dan peneliti, tahun, data, metode, serta hasil. Header rata tengah; teks isi tetap rata kiri agar mudah dibaca. Garis horizontal mengikuti pola sebelumnya; tidak ditambahkan garis vertikal atau antarbaris. Ukuran font isi 12 pt dipertahankan. Spasi khusus tabel memakai faktor 1,25 agar baris utuh dapat memanfaatkan ruang halaman; paragraf naskah tetap 1,5. Header diulang bila tabel berlanjut ke halaman berikutnya.

Bagian 2.2 tetap kerangka. Sampul/halaman awal, BAB I, BAB III, serta data dan hasil eksperimen tidak diubah.

## Pemilihan lima studi

Studi Ghani (2023) dipertahankan karena membandingkan representasi pralatih. Ghaffari–Devos, Clark, Fairbairn, dan Lostanlen mencakup derau, kesalahan pengenalan, ambang, dan variasi kondisi sensor. Studi Ghani (2025), Kong (2020), dan Kahl (2021) dikeluarkan dari tabel agar ringkas; artikel dan entri pustakanya tetap disimpan, serta Kong dan Kahl tetap dikutip di BAB I. Penulis dicantumkan maksimal tiga orang, diikuti dkk. jika ada penulis lain.
