# Fase A — Perbaikan Pipeline sebelum Reproduksi

Tanggal: 12 Oktober 2026.

Fase ini mengubah kode dan menambahkan tes sintetis saja. Tidak ada audio,
manifes, artefak E1 yang valid, atau eksperimen E2–E5 yang dijalankan.

## Perbaikan yang diterapkan

1. `scripts/run_e3_calibration.py` sekarang menyelaraskan skor E2 dengan
   `query_id` dari manifes. Berkas dengan ID ganda, ID hilang, atau ID tambahan
   dihentikan dengan error yang menjelaskan masalahnya.
2. `src/mix_noise.py` dan `scripts/run_e4_domain_shift.py` dapat menghasilkan
   audit pencampuran per query: file noise, posisi segmen, seed, percobaan,
   gain noise, gain pasca-campur, SNR target, dan SNR aktual. `src/evaluate.py`
   menyimpan informasi itu ke raw E2 baru ketika eksperimen kelak dijalankan.
3. R1 tidak lagi mengunduh label AudioSet ketika evaluasi sedang berjalan.
   Dependensi tersebut harus tersedia lokal terlebih dahulu.
4. R3 sekarang menghasilkan vektor acak dari ID rekaman dan seed eksperimen,
   bukan dari sampel waveform. Versi clean dan noisy dari rekaman yang sama
   sengaja memakai vektor R3 yang sama; R3 mengukur level peluang, bukan
   respons terhadap isi audio.
5. Jalur paket `src/dsic2706/` yang dahulu memiliki jaringan placeholder untuk
   R1/R2 sekarang meneruskan ke extractor dan mixer kanonik di `src/`.

## Konsekuensi untuk hasil lama

Cache atau tabel R3 yang dibuat sebelum catatan ini tidak sebanding dengan R3
yang baru. Jangan gunakan untuk H5, tabel, atau grafik. Hasil E1 R0 yang sudah
diaudit tetap dipertahankan sebagai artefak terpisah; ia tidak memakai R3.

## Validasi yang telah dilakukan

`tests/test_phase_a_integrity.py` memakai data sintetis dan memeriksa:

- penyelarasan E3 menurut ID, bukan urutan CSV;
- penolakan ID ganda atau hilang;
- R3 stabil untuk ID sama dan independen dari waveform;
- audit SNR tetap akurat saat gain pasca-campur diperlukan;
- pemeriksaan manifes restart yang sudah ada.

Tidak ada uji audio/model nyata pada Fase A. Runtime Python yang tersedia di
Codex belum memiliki dependensi proyek seperti `librosa`, `PyYAML`, dan
`scikit-learn`; lingkungan proyek perlu disiapkan secara eksplisit sebelum
smoke test audio pertama.
