# 6. Peta bacaan jurnal dan sumber hasil

## Jangan mulai dengan membaca semua PDF sekaligus

Mulai dari berkas 01–03 paket ini. Lalu buka artikel sesuai konsep yang belum jelas. Untuk setiap artikel, catat lima hal: masalahnya, data/tugasnya, metodenya, hasil yang benar-benar diukur, dan batas kaitannya dengan TA. Mengetahui judul saja belum cukup untuk menjadikannya dasar klaim.

Nomor ID berikut mengikuti [tabel pustaka aktif](../../paper/bibliography/referensi_jurnal_modern.csv). Tahun 2022–2026 diprioritaskan untuk penelitian terdahulu; artikel lebih lama dipakai sebagai sumber asal model/metode. Prosiding dan preprint diberi jenisnya pada tabel, sehingga jangan menyebut seluruh 28 entri sebagai “28 jurnal”.

## Urutan bacaan inti

| Urutan | Bacaan lokal | Fokus ketika membaca | Yang perlu Anda bisa jelaskan |
|---|---|---|---|
| 1 | ID 26, Stowell, review bioakustik; jurnal 2022, PDF naskah penulis 2021 | Abstrak, pengantar, representasi/model, evaluasi dan tantangan. | Mengapa audio berguna, mengapa model/data/evaluasi punya batas. |
| 2 | ID 3, MFCC–BiLSTM, 2025 | Alur ekstraksi fitur dan pemisahan tugas klasifikasi. | Apa itu MFCC; apa bedanya dengan R0 TA. |
| 3 | ID 15, PANNs, 2020 | Data AudioSet, CNN14, keluaran embedding, transfer learning. | Mengapa R1 disebut audio generik dan dari mana fitur berasal. |
| 4 | ID 11, BirdNET, 2021; lanjut ID 9, Ghani dkk., 2023 | Tugas/model artikel BirdNET; penggunaan embedding untuk transfer. | Apa arti model khusus burung; mengapa checkpoint v2.4 TA tidak disamakan dengan artikel 2021. |
| 5 | ID 8, BIRB, 2024 | Rumusan retrieval, query–reference, rancangan evaluasi generalisasi dan metrik. | Mengapa retrieval perlu dievaluasi menurut ranking, serta mengapa metriknya tidak otomatis sama dengan TA. |
| 6 | ID 34, Ghaffari–Devos, 2024; ID 31, Clark dkk., 2023 | Frontend, derau, komposisi soundscape, batas eksperimen. | Mengapa perubahan kondisi suara dapat mengubah hasil tanpa mengklaim mekanisme TA sudah terbukti. |
| 7 | ID 33, Hassanzad–Hajian-Tilaki, 2024 | ROC, sensitivity/specificity, metode cut-point dan Youden. | Bagaimana ambang dipilih dan apa trade-off menerima–menolak. |
| 8 | ID 6, Moummad dkk., ICASSP 2026; PDF arXiv v8 Jan 2026 | Domain-invariant representation dan rancangan pengujiannya. | Apa yang dimaksud generalisasi lintas kondisi dan apa bedanya dari E4 TA. |

Untuk bacaan lokal tentang konteks Indonesia, lanjutkan ID 21 Cikaniki dan ID 2 Way Kambas. Untuk konteks aktivitas burung tropis baca ID 22 SEABAD. Ketiganya mendukung konteks tertentu; tidak otomatis membuktikan durasi lima detik optimal, retensi TA, atau kemampuan lapangan sistem TA.

## Tautan PDF inti

- [Review Stowell](../../paper/bibliography/Computational%20bioacoustics%20with%20deep%20learning%20a%20review%20and%20roadmap.pdf)
- [MFCC–BiLSTM 2025](../../paper/bibliography/Klasifikasi%20Jenis%20Burung%20Berdasarkan%20Suara%20Kicau%20Menggunakan%20Ekstraksi%20MFCC%20dan%20BiLSTM.pdf)
- [PANNs](../../paper/bibliography/PANNs%20Large-Scale%20Pretrained%20Audio%20Neural%20Networks%20for%20Audio%20Pattern%20Recognition.pdf)
- [BirdNET 2021](../../paper/bibliography/BirdNET%20A%20deep%20learning%20solution%20for%20avian%20diversity%20monitoring.pdf)
- [Ghani dkk. 2023](../../paper/bibliography/Global%20birdsong%20embeddings%20enable%20superior%20transfer%20learning.pdf)
- [BIRB](../../paper/bibliography/BIRB%20A%20Generalization%20Benchmark%20for%20Information%20Retrieval.pdf)
- [Frontend audio 2024](../../paper/bibliography/Ghaffari_2024_Audio_frontends_bird_recognition.pdf)
- [Komposisi soundscape 2023](../../paper/bibliography/Clark_2023_Soundscape_composition.pdf)
- [ROC dan Youden 2024](../../paper/bibliography/Hassanzad_2024_ROC_Youden_cutpoint_review.pdf)
- [Domain-invariant representation](../../paper/bibliography/Domain-Invariant%20Representation%20Learning%20of%20Bird%20Sounds.pdf)

## Dua PDF yang belum diperoleh: alternatif untuk belajar

**Putra dkk. 2024, MFCC–Naive Bayes:** [penerbit](https://ejurnal.umri.ac.id/index.php/JIK/article/view/7558) dan [PDF asli](https://ejurnal.umri.ac.id/index.php/JIK/article/download/7558/3071/24869). Upaya akses ulang melalui tautan asli dan alternatif protokol belum berhasil dari komputer ini. Sebagai bacaan pendamping MFCC lokal, gunakan **ID 3 MFCC–BiLSTM 2025** yang PDF-nya sudah tersedia. Penulis, data, dan algoritmenya berbeda; jangan memakai hasil BiLSTM sebagai hasil Naive Bayes.

**Fluss dkk. 2005, Youden:** [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1002/bimj.200410135). Jalur CiteSeerX yang terindeks dan tautan unggahan penulis ResearchGate juga belum menghasilkan unduhan yang dapat disimpan. Sebagai pendamping yang lebih baru dan terbuka, gunakan **ID 33 ulasan ROC/Youden 2024**, DOI [10.1186/s12874-024-02198-2](https://doi.org/10.1186/s12874-024-02198-2). Ulasan ini membahas metode cut-point pada konteks biomarker; dasar statistiknya dapat dipelajari, tetapi hasil klinisnya bukan bukti performa audio TA.

Alternatif tersebut adalah **artikel pendamping yang sudah tersedia**, bukan salinan dua artikel yang belum diperoleh. Status dua entri asli tetap jujur “PDF belum diperoleh”. Ketiadaan PDF tidak berarti artikelnya palsu. Jangan menyusun uraian detail full-text yang belum Anda baca.

## Dari mana teori dan angka TA bisa diperiksa?

| Yang ingin dicek | Sumber aktif |
|---|---|
| 20 spesies, 1.216 target, 673/311/232 | [dataset_split.csv](../../data/manifests/dataset_split.csv) dan [scope-freeze](../../docs/research/scope-freeze.md) |
| Identitas sumber derau dan konfigurasi | [itera_noise_manifest.csv](../../data/manifests/itera_noise_manifest.csv) dan scope-freeze |
| Pembagian unknown | [unknown_open_set_manifest.csv](../../data/manifests/unknown_open_set_manifest.csv) |
| Pemotongan, 32 kHz, RMS | [preprocess.py](../../src/preprocess.py) |
| Daya, alpha, SNR dan audit campuran | [mix_noise.py](../../src/mix_noise.py) |
| MFCC 20 mean + 20 std | [mfcc.py](../../src/mfcc.py) |
| R1/R2/R3, dimensi, jendela internal R2 | [embeddings.py](../../src/embeddings.py) |
| Cosine, AP/mAP, Recall, RR | [retrieve.py](../../src/retrieve.py) |
| Kandidat ROC, Youden, tau, AUROC dan AUPRC | [calibrate_threshold.py](../../src/calibrate_threshold.py) |
| Hasil E1 | [10_e1_clean_retrieval_summary.csv](../../results/tables/10_e1_clean_retrieval_summary.csv) |
| Hasil E2 dan retensi | [11_e2_snr_robustness.csv](../../results/tables/11_e2_snr_robustness.csv) |
| Ambang E3 | [12_e3_frozen_thresholds.csv](../../results/tables/12_e3_frozen_thresholds.csv) |
| Recall penerimaan, FPR, AUROC E3 | [13_e3_threshold_transfer.csv](../../results/tables/13_e3_threshold_transfer.csv) |
| H3 absolut/relatif dan CI | [h3_swing_summary.csv](../../results/reproductions/H3_sensitivity_20261015/tables/h3_swing_summary.csv) |
| H3 buang satu lokasi bergantian | [README leave-one-location-out](../../results/reproductions/H3_leave_one_location_out_20261018/README.md) |
| Hipotesis asli dan tanggal perubahan | [hypotheses.md](../../docs/research/hypotheses.md) |
| Kategori E5 yang digunakan | [run_e5_diagnostics.py](../../scripts/run_e5_diagnostics.py) |
| Panduan mendengar E5 | [panduan audit dan penjelasan lisan](../../Rencana-eksperimen-bimbingan/PANDUAN_AUDIT_E5_DAN_PENJELASAN_LISAN.md) |
| Riwayat reproduksi yang sudah dilakukan | [laporan reproduksi](../../docs/REPRODUKSI_LINGKUNGAN_BARU_2026-10-16.md) |

Berkas lama atau modul yang hanya berisi kerangka tidak otomatis menjadi sumber definisi aktif. Untuk rumus retrieval gunakan `src/retrieve.py`; untuk kategori 120 kasus gunakan skrip E5 di atas. Jangan menyimpulkan metode dari nama file saja.

## Sebelum mulai menulis BAB 1–3

1. Kuasai cerita penelitian dan perhitungan pokok dari paket ini; tandai bagian yang masih membingungkan.
2. Konfirmasikan judul, RQ, hipotesis/label eksploratif, ruang lingkup campuran, dan persetujuan mulai menulis kepada pembimbing sesuai alur bimbingan Anda.
3. Pilih klaim BAB 1 yang ditopang sumber nyata, mulai dari masalah umum lalu masalah khusus TA. Hindari klaim prioritas “pertama” tanpa penelusuran memadai.
4. Untuk BAB 2, pisahkan teori, penelitian terdahulu, dan hasil eksperimen sendiri. Tandai versi PDF serta status preprint/prosiding/jurnal dengan benar.
5. Untuk BAB 3, pastikan alur tertulis sesuai kode aktif: pemisahan data, lima detik, adaptasi R2, pencampuran SNR, rumus AP, kalibrasi, E4 lima lokasi, serta batas E5.
6. Selesaikan atau laporkan secara terbuka sisa audit pendengaran dengan bukti manusia. Anda dapat menyiapkan draf teori sambil audit berjalan; jangan menyatakan audit selesai sebelum buktinya ada.

Paket ini tidak menuliskan ulang BAB 1–3 atau mengubah dokumen penelitian resmi. Pemeriksaan pustaka lanjutan dicatat pada [hasil cek referensi](../../paper/bibliography/PEMERIKSAAN_REFERENSI_2026-10-27.md).
