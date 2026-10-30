# Configurations

YAML memuat konfigurasi audio, dataset, representasi, eksperimen, dan ambang, tetapi sebagian komentar/nilai merupakan rancangan historis. Untuk menulis metode atau memeriksa hasil aktif, utamakan kode pelaksana, manifes, dan metadata/run identity; jangan menganggap seluruh nilai YAML pasti digunakan oleh run.

`active_runs.json` mengindeks run sumber E0–E5 dan statistik, bukan seluruh perkembangan sesudahnya. Ia belum merangkum analisis penghilangan tiap lokasi 18 Oktober atau audit manusia 30 Oktober. Kesimpulan terbaru mengikuti [matriks revisi 28](../results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv) dan [hasil audit E5](../Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/README.md).

Contoh perbedaan yang perlu diperhatikan: H3 aktif memakai 10.000 bootstrap, bukan komentar 1.000 pada konfigurasi umum; E5 memilih 120 kasus, bukan komentar 30 kasus. Parameter MFCC aktual dijelaskan pada [indeks sumber metode](../paper/persiapan_bab1_3/README.md#5-parameter-utamakan-implementasi-dan-artefak-run). Pembaruan dokumentasi ini tidak mengubah konfigurasi atau threshold.
