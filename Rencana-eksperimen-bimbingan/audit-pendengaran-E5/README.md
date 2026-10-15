# Petunjuk Audit Pendengaran E5

Lembar E5_AUDIT_PENDENGARAN.csv berisi 120 kasus dari artefak E5 yang sudah ada. Saat disiapkan, semua berstatus pending dan kolom pengamatan manusia kosong. Label spesies merupakan metadata dataset, bukan hasil identifikasi baru oleh pendengar.

Kolom representasi, kondisi, dan moda kegagalan komputasional dipulihkan dari diagnostik lengkap dengan pencocokan persis terhadap seluruh kolom sumber kasus pilihan. Metadata mencatat hash sumber serta output. Berkas sumber E5 tidak diubah.

## Audio yang perlu diperiksa

Untuk query clean dan audio Top-1, gunakan hasil preprocessing resmi: mono 32 kHz, jendela lima detik berenergi tertinggi dengan hop 1,25 detik, padding bila pendek, dan normalisasi RMS sesuai kode. Jangan menggantinya dengan lima detik pertama file asli.

Untuk query noisy E2, rekonstruksi campuran sesuai kondisi, noise_seed, noise_file, noise_start_sample, dan SNR pada kasus. Sebelum dipakai mendengar, identitas noise/segmen serta SNR harus cocok dengan audit sumber. Menyiapkan klip dengar E2 tidak memerlukan menjalankan E4 atau mengekstraksi embedding model.

File path pada lembar menunjuk audio asli; lembar ini belum menyediakan klip terproses. Review atas audio asli yang tidak sesuai segmen belum memenuhi audit kasus eksperimen.

## Cara mengisi

1. Catat nama pendengar dan tanggal pada reviewer serta reviewed_at.
2. Dengarkan query pada kondisi yang tercatat dan hasil Top-1; gunakan versi clean query sebagai pembanding bila diperlukan.
3. Isi query_vocalisation_audible dan top1_vocalisation_audible dengan yes, no, atau uncertain.
4. Catat latar yang terdengar pada background_observation. Gunakan “terdengar seperti …” jika sumber belum pasti; jangan mengubah dugaan menjadi identitas sumber atau jarak terukur.
5. Isi uncertainty_notes dan auditory_interpretation. Kemiripan menurut pendengaran tidak membuktikan mekanisme spektral atau mengubah label ground truth secara otomatis.
6. Ubah review_status menjadi reviewed hanya setelah pemeriksaan dilakukan. Gunakan needs_follow_up jika audio/segmen tidak bisa dipastikan. Baris pending tidak dihitung selesai.

Dua kasus dengan query/kondisi sama tetap dapat mempunyai Top-1 atau representasi berbeda. Catat penilaian per case_id. Jika koreksi label dataset diduga diperlukan, laporkan melalui catatan terpisah; jangan mengubah manifes atau hasil eksperimen secara langsung.

## Kriteria selesai

Seluruh 120 baris mempunyai reviewer, reviewed_at, observasi query/Top-1, dan interpretasi yang dapat ditelusuri ke segmen yang benar; seluruh masalah needs_follow_up ditangani atau dilaporkan sebagai keterbatasan. Audit ini tidak boleh diisi otomatis dari skor model.

Builder prepare_e5_listening_review.py hanya menyiapkan lembar kosong dan menolak direktori yang sudah ada. Setelah pengisian dimulai, jangan menjalankannya untuk menimpa catatan pendengar.
