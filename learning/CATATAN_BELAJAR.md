# Catatan belajar audio

Dicatat oleh Codex dari percakapan pengguna, 11 Oktober 2026. Pengguna tidak perlu menyalin ulang catatan. Ini anotasi latihan berdasarkan pendengaran pengguna, bukan verifikasi jumlah individu, identitas semua sumber suara, jarak, atau SNR.

## Tiga rekaman latihan

| Rekaman | Peran | Label spesies | Pengamatan umum pengguna |
|---|---|---|---|
| XC42472 | Query | Caprimulgus affinis | Panggilan berulang dan jelas. Latar terdengar seperti angin. Dugaan bahwa sensitivitas mikrofon menjadi penyebab belum dibuktikan. |
| XC120964 | Gallery relevan | Caprimulgus affinis | Terdengar seperti dua burung; panggilannya mirip query dan jelas. Serangga terdengar sepanjang latar, lebih lemah daripada panggilan menurut pendengaran. Dua suara belum memastikan dua individu atau dua spesies. Pemutar menampilkan subspesies propinquus. |
| XC1003648 | Gallery berbeda | Orthotomus ruficeps | Panggilan berbeda dari query dan jelas. Latar terdengar seperti kendaraan (pengguna menduga mobil/kereta dan lainnya), jenis sumber belum dipastikan. |

Rekaman tambahan yang pernah didengarkan: XC360828, berlabel Caprimulgus affinis dan berperan calibration pada manifes yang ditampilkan pengguna. Panggilan terdengar mirip XC42472 dan sangat jelas, dengan derau minim menurut pendengaran. Tidak digunakan dalam perhitungan tiga file ini.

## Pengamatan khusus detik 0–5

Berikut catatan pengguna, dengan waktu sebagai perkiraan pendengaran, bukan anotasi batas panggilan yang sudah diverifikasi:

- XC42472: "2 kicauan dekat (burung 1) detik 1-3, 4-5 1 kicauan burung ke-2".
- XC120964: "5 kicauan, 4 kicauan dekat, 1 kicauan jauh".
- XC1003648: "3 kicauan".

Ketiga potongan berisi suara burung menurut pengguna. Kesan dekat/jauh dan dugaan burung kedua tidak diperlakukan sebagai fakta jarak atau jumlah individu.

## Protokol latihan yang telah dijalankan

- Membaca informasi fisik file: XC42472 34,25 detik, MP3 stereo 44.100 Hz; XC120964 28,55 detik, MP3 stereo 44.100 Hz; XC1003648 35,54 detik, WAV stereo 48.000 Hz meskipun namanya berakhiran .mp3. Durasi MP3 berdasarkan frame, bukan durasi setelah koreksi encoder delay/padding.
- Decode/resample dengan Web Audio pada Edge yang tersedia lokal; mono adalah rata-rata dua kanal. Ambil detik 0–5. Tidak menormalisasi amplitudo per rekaman dan tidak menyaring derau secara terpisah.
- Setiap potongan: mono, 32.000 Hz, 160.000 sampel. Potongan diproses di memori; file asli tidak ditimpa.
- MFCC latihan: Hann 800 sampel (25 ms), hop 320 (10 ms), FFT 1024, 40 filter Mel HTK segitiga tanpa normalisasi luas, rentang 0–16.000 Hz, log natural dengan floor 1e-12, DCT-II ortonormal C1–C19 (tanpa C0), tanpa pre-emphasis. Power spectrum dibagi 1024. Tanpa padding di ujung: 498 bingkai.
- Ringkasan: 19 rata-rata dan 19 simpangan baku populasi, total 38 dimensi. Bandingkan dengan cosine similarity.
- Hasil latihan yang telah dijalankan pengguna: XC42472 vs XC120964 = 0,566662; XC42472 vs XC1003648 = 0,231286. Skor bukan probabilitas spesies. Ini bukan keluaran E1 resmi atau bukti ketahanan derau.

## Pemahaman yang sudah dibahas

- Gallery adalah koleksi yang dicari, query adalah masukan pencarian, calibration digunakan untuk menetapkan ambang.
- Label spesies digunakan untuk menilai relevansi setelah pengurutan, bukan masukan perhitungan skor.
- Top-1 menilai relevansi hasil peringkat pertama. Contoh Recall@10: enam ditemukan dari 15 relevan = 40%; Precision@10: enam relevan dari sepuluh hasil = 60%.
- Stereo berarti dua kanal audio, bukan dua burung. Sampling rate bukan tinggi nada.
- MFCC merangkum campuran panggilan, jeda, dan latar. Lima detik yang sama panjang tidak menjamin jumlah panggilan yang sama.
- Sebutan clean berarti belum ditambahkan derau eksperimen, bukan sepenuhnya bebas suara latar.

## Latihan gallery 30

Perbandingan ketiga pasangan melalui skrip 03 telah dijalankan pengguna. Pasangan XC120964/XC1003648 mendapat skor 0,165812; pasangan spesies sama tetap memiliki skor tertinggi di antara ketiganya.

Skrip 04 disiapkan dan dicoba Codex pada 11 Oktober 2026: satu query XC42472 melawan 30 kandidat. Daftar kandidat dan checksum dibekukan di `gallery_latihan_30.json` sebelum skoring. Kandidat adalah seluruh 15 savnig1 di gallery dan masing-masing tiga rekaman dari lima spesies lain pertama menurut urutan species_key, dengan recording_id diurutkan alfabetis dan durasi fisik >=5 detik. Spesies pembanding: ashtai1, colkin1, comior1, crseag1, ghcfly1.

Manifes dan semua audio diperiksa SHA-256 saat skrip dijalankan. Tidak ada checksum identik di antara 31 file. Tidak ada perekam query di gallery latihan. Rekaman mono maupun stereo didukung, dengan aturan yang sama seperti latihan 02.

Hasil uji Codex (belum merupakan hasil yang dikirim pengguna): XC40064 menjadi peringkat pertama, skor 0,838747, spesies sama. Empat dari sepuluh hasil teratas relevan: Top-1 benar untuk satu query, Precision@10 = 4/10 = 40%, Recall@10 = 4/15 = 26,67%. XC120964 menjadi peringkat kesembilan; skornya tetap 0,566662. Skor sepasang rekaman tetap, tetapi peringkat dapat berubah ketika kandidat ditambah.

Ini subset pilihan untuk belajar, bukan gallery lengkap 673 rekaman atau hasil E1 resmi. Satu query belum mengukur akurasi dataset. Dengan 15 rekaman relevan, Recall@10 maksimum 10/15 = 66,67%, walaupun sepuluh hasil teratas semuanya relevan. Pengamatan jumlah panggilan detik 0–5 baru tersedia untuk tiga file awal, bukan seluruh kandidat baru.

Pembacaan audio dilakukan satu file per giliran dengan konteks decoder yang dipakai ulang. Perhitungan metrik telah diperiksa memakai ranking buatan dengan jawaban diketahui (6/10 precision, 6/15 recall, Top-1 salah) dan kasus ID duplikat/tanpa rekaman relevan. Perubahan decoder juga diperiksa dengan menjalankan ulang latihan 03: skor ketiga pasangan tetap sama.

Pengguna telah menjalankan skrip 04 dan mengirim hasil yang sama dengan uji Codex: Top-1 benar, empat relevan pada peringkat 1/2/6/9, Precision@10 40%, Recall@10 26,67%.

## Pemeriksaan hasil tidak relevan XC166746

Pengguna diminta mendengarkan detik 0–5 dari XC166746, kandidat peringkat ketiga dengan cosine 0,684869. Pengamatan pengguna: hanya satu kicauan, terdengar seperti elang; latar terdengar seperti aliran air. Tangkapan pemutar menampilkan Crested Serpent Eagle (Spilornis cheela bido), perekam Frank Lambert; label spesies pada gallery adalah Spilornis cheela (crseag1), berbeda dari query Caprimulgus affinis. `bido` merupakan nama subspesies yang ditampilkan pemutar.

Suara latar belum diverifikasi sebagai air. Jumlah panggilan adalah anotasi pendengaran awal. Skor tinggi tidak membuktikan suara air menjadi penyebab kesalahan atau panggilan burung serupa. MFCC mean/std merangkum keseluruhan campuran dan tidak menyimpan urutan bingkai secara eksplisit atau menghitung jumlah panggilan. Perlu pemeriksaan visual/akustik dan perbandingan terkontrol untuk menguji penyebab skor tinggi.

Langkah berikutnya adalah membandingkan spektrogram query dengan XC166746 pada detik 0–5, menggunakan skala yang sama. Protokol eksperimen resmi tetap perlu diaudit dan dibekukan tersendiri.

## Pemeriksaan potongan panggilan — 12 Oktober 2026

Spektrogram kedua potongan ditampilkan dengan skala warna bersama. Pada query terlihat dua pola menonjol sekitar 0,5 dan 3 detik, terutama 2–5 kHz; pada XC166746 satu pola menonjol sekitar 1,9–2,3 detik dekat 2 kHz dengan garis di atasnya. Visual tidak memastikan sumber latar atau penyebab skor.

Atas permintaan pengguna, Codex membuat dan mencoba latihan 05. Batas disimpan sebelum skoring di `05_batas_panggilan.json`: query 0,45–1,05 detik dan 2,95–3,55 detik, kandidat 1,8–2,4 detik. Semua potongan 0,6 detik, 19.200 sampel dan 58 bingkai, dengan parameter MFCC yang sama. Dua panggilan query dilaporkan bersama untuk menghindari pemilihan hasil yang paling mendukung dugaan. Batas adalah perkiraan visual, bukan anotasi ahli; latar belum dihilangkan.

Hasil uji Codex: baseline detik 0–5 = 0,684869. Panggilan query pertama vs kandidat = 0,628638 (selisih -0,056231); panggilan kedua vs kandidat = 0,638236 (selisih -0,046632, dihitung sebelum pembulatan). Pengguna telah menjalankan skrip 05 dan mengirim hasil yang sama.

Skor lebih rendah pada kedua potongan pendek, tetapi perubahan durasi, jumlah bingkai, dan komposisi audio juga memengaruhi ringkasan. Ini tidak mengisolasi efek latar dan tidak membuktikan latar air/angin sebagai penyebab kesalahan. Tidak ada potongan audio atau hasil eksperimen resmi yang disimpan/ditimpa.
