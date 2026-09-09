# DSIC-2706 — Robust Bioacoustic Similarity Retrieval under Noise and Domain Shift

Repositori penelitian untuk topik **DSIC-2706: Mencari Audio yang Mirip Ketika Datanya Terbatas**.

Fokus penelitian ini bukan membuat classifier spesies baru, melainkan menguji **ketahanan representasi audio untuk similarity retrieval** ketika query mengalami derau lingkungan dan pergeseran domain dari *focal recording* ke *real soundscape*.

Judul kerja artikel yang direkomendasikan:

> **Noise and Domain-Shift Robustness of Audio Representations for Cross-Domain Bioacoustic Retrieval: From Xeno-Canto to ITERA Soundscapes**

## 1. Pertanyaan penelitian

### RQ utama

**Representasi audio mana yang mempertahankan kualitas similarity retrieval paling baik ketika query bioakustik mengalami peningkatan derau lingkungan dan pergeseran domain dari focal recording ke soundscape?**

### Sub-RQ

1. Seberapa besar penurunan `mAP@k` dan `Recall@k` untuk setiap representasi pada beberapa tingkat SNR yang dibentuk menggunakan background noise ITERA?
2. Apakah threshold kemiripan yang dikalibrasi pada data terpisah tetap mampu menolak *unknown species* dan *background noise* ketika tingkat noise dan domain perekaman berubah?
3. Apakah *bioacoustic-specific embedding* memiliki *robustness retention* yang lebih baik daripada *generic pretrained audio embedding* dan MFCC pada kondisi noise yang sama?
4. Sebagai analisis sekunder, candidate match spesies apa yang muncul pada subset soundscape ITERA yang telah diverifikasi manual?

## 2. Hipotesis

- **H1 — Robustness retention:** deep pretrained representation mempertahankan proporsi `mAP@k` yang lebih besar daripada MFCC ketika SNR diturunkan.
- **H2 — Domain-specific advantage:** bioacoustic embedding mengalami penurunan retrieval yang lebih kecil daripada generic audio embedding pada query burung dengan environmental noise.
- **H3 — Domain shift:** kinerja pada real soundscape turun lebih besar daripada controlled mixture pada SNR sebanding karena domain shift tidak hanya berupa additive noise.
- **H4 — Threshold transfer:** threshold yang baik pada calibration-clean tidak selalu stabil ketika kondisi noise berubah.
- **H5 — Positive control:** clean retrieval harus mengungguli random ranking. Jika tidak, pipeline harus diaudit sebelum hasil diinterpretasikan.

Semua hipotesis boleh ditolak. Hasil nol tetap merupakan hasil penelitian apabila eksperimen, kontrol, dan confidence interval valid.

## 3. Batas kontribusi

Kontribusi ilmiah utama:

- evaluasi *paired robustness* pada query yang sama;
- controlled environmental-noise stress test menggunakan background ITERA;
- perbandingan hand-crafted, generic pretrained, dan bioacoustic pretrained representation;
- kurva degradasi retrieval terhadap SNR;
- pengujian transfer threshold pada open-set condition;
- validasi eksternal pada real ITERA soundscape.

Yang **bukan** kontribusi utama:

- membuat model BirdNET/PANNs baru;
- fine-tuning banyak model;
- classifier fauna baru;
- occupancy modelling;
- abundance estimation;
- inventarisasi biodiversitas kampus secara lengkap;
- dashboard atau aplikasi produksi.

## 4. Representasi yang dibandingkan

| Kode | Representasi | Peran |
|---|---|---|
| R0 | MFCC + mean/std pooling | Baseline katalog |
| R1 | Generic pretrained audio embedding, misalnya PANNs | Deep embedding generik |
| R2 | Satu bioacoustic pretrained embedding yang stabil | Domain-specific representation |
| R3 | Random ranking | Negative control |

Semua representasi utama menggunakan **cosine similarity** agar perbandingan tidak tercampur oleh metric retrieval yang berbeda.

Main experiment memakai **frozen representations**. Fine-tuning hanya boleh dilakukan setelah eksperimen utama selesai.

## 5. Dataset dan perannya

### Xeno-Canto

Digunakan sebagai *reference bank/gallery* dan clean query.

Target awal yang realistis:

- 10–20 spesies burung;
- minimum jumlah rekaman per spesies ditentukan sebelum pengambilan final;
- gallery dan query dipisahkan berdasarkan `recording_id`;
- bila data mencukupi, gunakan `recordist-disjoint split` sebagai robustness check.

Metadata minimum:

- recording ID;
- scientific name;
- common name;
- recordist;
- locality/country;
- tanggal;
- quality;
- license;
- URL;
- checksum.

### Background noise ITERA

Background-only audio dari beberapa kondisi, misalnya:

- Embung ITERA;
- Arboretum/Kebun Raya;
- area terbuka/antropogenik.

Noise bank digunakan untuk membuat controlled mixture pada beberapa SNR.

### Real ITERA soundscape

Digunakan sebagai external domain validation. Untuk evaluasi kuantitatif, hanya gunakan subset yang dianotasi atau diverifikasi manual.

### External public validation

BirdCLEF/BirdSet atau ESC-50 bersifat **opsional** dan hanya dikerjakan setelah main experiment selesai.

## 6. Split penelitian

Pisahkan set berikut secara eksplisit:

```text
Xeno-Canto
├── gallery
├── clean-query
├── threshold-calibration
└── retrieval/open-set-test

ITERA
├── background-noise-bank
├── threshold-calibration-background
└── annotated-real-soundscape-test
```

Aturan penting:

- tidak boleh ada recording yang sama di gallery dan query;
- calibration set tidak boleh dipakai sebagai final test;
- threshold tidak boleh diubah setelah test result dilihat;
- real ITERA soundscape tidak dipakai untuk melatih atau memilih representation utama.

## 7. Controlled noise experiment

Setiap clean query dibuat menjadi beberapa versi menggunakan noise ITERA yang sama dan seed yang dibekukan.

Rancangan awal:

```text
clean
20 dB
10 dB
0 dB
-5 dB
```

Level final boleh disesuaikan saat pilot untuk menghindari seluruh model mengalami ceiling/floor effect. Setelah pilot, level SNR dibekukan.

Untuk setiap representasi:

```text
query audio
   ↓
representation extraction
   ↓
embedding
   ↓
cosine similarity terhadap gallery
   ↓
ranking
   ↓
mAP@k / Recall@k / Precision@k
```

## 8. Open-set experiment

Query open-set meliputi:

- unknown bird species yang tidak ada dalam gallery target;
- background-only ITERA;
- non-bird environmental events bila tersedia.

Sistem menerima match bila:

```text
max_similarity(query, gallery) >= threshold
```

Threshold dipilih hanya dari calibration split dan kemudian **dibekukan**.

## 9. Metrik evaluasi

### Retrieval primer

- `mAP@k`
- `Recall@1`
- `Recall@5`
- `Recall@10`
- `Precision@k`

### Robustness

- raw `mAP@k` per SNR;
- absolute performance drop;
- relative robustness retention;
- kurva `metric vs SNR`.

### Open-set

- AUPRC;
- AUROC;
- F1 pada threshold calibration;
- false-positive / false-accept rate;
- recall/TPR pada operating point.

### Sekunder

- median rank / MRR bila berguna;
- embedding dimension;
- inference time;
- UMAP/t-SNE hanya untuk visualisasi, bukan success criterion.

## 10. Rencana eksperimen

### E0 — Pipeline sanity

- bekukan sample rate, segment duration, channel rule, normalization;
- jalankan MFCC, generic embedding, dan bioacoustic embedding pada subset kecil;
- pastikan random ranking lebih buruk dari representation nyata;
- audit split leakage.

### E1 — Clean retrieval

- gallery tetap;
- clean query terpisah;
- hitung retrieval metrics;
- simpan ranking per query, bukan hanya aggregate score.

### E2 — Controlled noise robustness

- gunakan query yang sama dari E1;
- campur background ITERA pada beberapa SNR;
- hitung kurva degradasi untuk seluruh representation.

### E3 — Open-set threshold

- buat calibration known/unknown;
- pilih threshold hanya dari calibration;
- bekukan threshold;
- evaluasi threshold pada clean dan noisy test.

### E4 — Real soundscape domain shift

- jalankan frozen pipeline pada annotated ITERA subset;
- jangan re-tune threshold menggunakan label test ITERA;
- ukur gap controlled-noise vs real soundscape.

### E5 — Failure analysis

Audit minimal 20 kasus:

- overlapping calls;
- low SNR;
- anthropogenic noise;
- similar vocalizations;
- long-distance/reverberation;
- short event;
- background signature;
- false accept unknown species.

### E6 — External public validation

Opsional untuk artikel setelah E0–E5 selesai.

## 11. Struktur repository

```text
dsic-2706-bioacoustic-retrieval/
├── README.md
├── .gitignore
├── .env.example
├── pyproject.toml
├── requirements.txt
├── Makefile
│
├── configs/
│   ├── audio.yaml
│   ├── datasets.yaml
│   ├── representations.yaml
│   ├── experiments.yaml
│   └── thresholds.yaml
│
├── docs/
│   ├── research/
│   │   ├── research-charter.md
│   │   ├── rq.md
│   │   ├── hypotheses.md
│   │   ├── novelty-boundary.md
│   │   ├── scope-freeze.md
│   │   └── decision-log.md
│   └── protocols/
│       ├── xeno-canto-selection.md
│       ├── itera-recording.md
│       ├── annotation.md
│       └── open-set.md
│
├── data/
│   ├── README.md
│   ├── manifests/
│   ├── xeno_canto/
│   ├── itera_noise/
│   └── itera_soundscape_annotations/
│
├── src/
│   └── dsic2706/
│       ├── data/
│       ├── audio/
│       ├── features/
│       ├── retrieval/
│       ├── open_set/
│       ├── evaluation/
│       ├── analysis/
│       └── utils/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── reproducibility/
│
├── experiments/
│   ├── E0_pipeline_sanity/
│   ├── E1_clean_retrieval/
│   ├── E2_noise_robustness/
│   ├── E3_open_set_threshold/
│   ├── E4_real_soundscape/
│   ├── E5_failure_analysis/
│   └── E6_external_validation/
│
├── results/
│   ├── raw/
│   ├── processed/
│   ├── tables/
│   ├── figures/
│   └── failure_cases/
│
├── scripts/
├── notebooks/
│   └── exploratory/
├── paper/
│   ├── manuscript.md
│   ├── figures/
│   ├── tables/
│   └── bibliography/
└── artifacts/
    └── reproducibility/
```

## 12. Tools

Minimum stack:

- Python 3.11/3.12;
- librosa;
- soundfile;
- scipy;
- NumPy;
- pandas;
- scikit-learn;
- PyTorch/TensorFlow sesuai pretrained checkpoint;
- matplotlib;
- FAISS opsional;
- UMAP opsional;
- Git.

Untuk audio lapangan:

- AudioMoth / field recorder bila tersedia;
- WAV lebih disarankan;
- konfigurasi recorder, lokasi, daypart, dan timestamp dicatat.

## 13. Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Salin konfigurasi:

```bash
cp .env.example .env
```

Validasi repository:

```bash
make test
```

Pipeline awal:

```bash
make manifest
make sanity
make clean-retrieval
```

Eksperimen utama:

```bash
make noise-robustness
make open-set
make soundscape
make evaluate
make figures
```

Perintah pada Makefile adalah skeleton dan harus dihubungkan ke implementasi final.

## 14. Aturan reproducibility

Setiap run minimal menyimpan:

```text
run_id
representation
checkpoint/version
query_id
gallery_manifest_version
noise_id
SNR
random_seed
threshold_version
ranking
metrics
runtime
```

Setiap klaim artikel harus dapat ditelusuri:

```text
RQ
 ↓
experiment
 ↓
raw result
 ↓
processed result
 ↓
table / figure
 ↓
claim
```

## 15. Data dan Git

Jangan commit file WAV besar ke repository.

Yang boleh di-version-control:

- manifest;
- metadata;
- checksum;
- annotation;
- configuration;
- code;
- result summary.

Yang tidak di-commit:

- raw audio besar;
- pretrained weights besar;
- temporary embedding cache;
- generated experiment artifacts besar.

## 16. Rencana satu bulan

### Minggu 1

- target species freeze;
- manifest Xeno-Canto;
- recording/preprocessing protocol;
- MFCC + dua embedding smoke test;
- clean retrieval baseline.

### Minggu 2

- ITERA noise bank;
- SNR mixer;
- E1/E2 main run;
- robustness curves.

### Minggu 3

- unknown/background set;
- threshold calibration;
- open-set test;
- annotated ITERA soundscape subset;
- failure audit.

### Minggu 4

- paired bootstrap CI;
- final tables/figures;
- domain-shift analysis;
- manuscript draft;
- fresh reproducibility run.

Untuk skripsi empat bulan, bulan berikutnya dapat digunakan untuk memperbesar data, menambah seed/recordist-disjoint checks, external validation, dan pematangan artikel tanpa mengubah RQ utama.

## 17. Definition of Done

Penelitian utama dianggap selesai bila:

- [ ] target taxon dan species list dibekukan;
- [ ] split bebas duplicate leakage;
- [ ] MFCC baseline selesai;
- [ ] generic pretrained representation selesai;
- [ ] satu bioacoustic representation selesai;
- [ ] clean retrieval selesai;
- [ ] minimal tiga noisy conditions selesai;
- [ ] `mAP@k` dan `Recall@k` dihitung;
- [ ] threshold berasal hanya dari calibration;
- [ ] open-set metrics tersedia;
- [ ] real soundscape external check selesai;
- [ ] minimal 20 failure cases diaudit;
- [ ] confidence interval tersedia;
- [ ] data manifest, seed, config, dan version model terdokumentasi;
- [ ] satu tabel dan satu figure dapat direproduksi dari fresh run;
- [ ] tidak ada klaim kehadiran spesies tanpa verifikasi manual.

## 18. Publication boundary

Paper utama menjawab **robustness of representation for retrieval**.

Luaran aplikasi seperti candidate biodiversity observations di ITERA hanya merupakan secondary output. Jangan mengubah paper menjadi ecological inventory study tanpa RQ, sampling design, dan ground truth ekologis yang baru.

## Catatan Pembimbing

Alur besarnya kira-kira seperti ini:

```text
Xeno-Canto
   ↓
pilih 10–20 spesies burung
   ↓
bersihkan + segmentasi audio
   ↓
pisahkan
Gallery | Query | Calibration | Test
   ↓
ekstrak representasi
MFCC | Generic Embedding | Bioacoustic Embedding
   ↓
Cosine Similarity
   ↓
Ranking audio paling mirip
   ↓
Clean retrieval
   ↓
tambahkan noise ITERA pada query yang SAMA
   ↓
20 dB → 10 dB → 0 dB → -5 dB
   ↓
ukur penurunan retrieval
   ↓
open-set threshold
   ↓
uji pada real soundscape ITERA
```

Secara eksperimen bisa seperti berikut.

1. **Mulai dari membuat “bank referensi” burung, bukan langsung merekam ITERA.** Mahasiswa memilih sekitar 10–20 spesies target terlebih dahulu. Audio referensinya dikumpulkan dari Xeno-Canto, kemudian dibuat manifest yang menyimpan spesies, recording ID, recordist, lokasi, lisensi, dan attribution. Audio kemudian distandardisasi: sample rate, durasi potongan, mono/stereo, dan normalisasi harus sama. Xeno-Canto kemudian dipisah menjadi **gallery** dan **query**; rekaman yang sama tidak boleh bocor ke kedua sisi. Pada minggu pertama audit juga mensyaratkan manifest, preprocessing, split, dan clean baseline sudah selesai. 

   Misalnya ada suara burung A. Beberapa rekamannya masuk ke gallery sebagai “koleksi yang dicari”, sedangkan rekaman burung A yang berbeda menjadi query. Jadi sistem diberi satu query dan ditanya: **dari seluruh gallery, audio mana yang paling mirip?**

2. **Setiap audio diubah menjadi tiga bentuk representasi.** Representasi pertama adalah baseline klasik **MFCC**. Representasi kedua adalah *generic pretrained audio embedding*, misalnya PANNs. Representasi ketiga adalah satu model yang memang lebih khusus bioakustik. Semua dipakai sebagai **feature extractor**, bukan dilatih ulang pada test data. Kemudian ketiganya menggunakan similarity metric yang sama, yaitu cosine similarity. Ini penting supaya yang dibandingkan benar-benar kualitas representasinya, bukan karena satu metode memakai retrieval algorithm yang berbeda. Baseline dan kontrol di audit adalah MFCC + cosine, random ranking, generic deep embedding + cosine, dan bioacoustic embedding + cosine. 

   Jadi untuk satu audio:

```text
audio.wav
   ├── MFCC                 → vector A
   ├── PANNs embedding      → vector B
   └── bioacoustic embedding → vector C
```

Lalu untuk masing-masing ruang vektor dilakukan:

```text
cosine(query, gallery_1)
cosine(query, gallery_2)
...
cosine(query, gallery_n)
```

Hasilnya diurutkan dari similarity tertinggi sampai terendah.

3. **Eksperimen pertama justru dilakukan dalam kondisi bersih.** Ini E1. Gallery tidak berubah dan query bersih benar-benar berbeda dari gallery. Lalu dihitung mAP@k, Recall@1, Recall@5, Recall@10, dan Precision@k.  Tujuannya bukan mencari novelty dahulu, tetapi memastikan pipeline masuk akal. Kalau random ranking ternyata sama bagusnya dengan embedding, berarti ada masalah pada label, split, atau implementasi similarity.

   Misalnya query “spesies A”. Jika lima hasil teratas adalah:

```text
1. A
2. A
3. B
4. A
5. C
```

dari sini kita bisa menghitung Precision@5, Recall@5, AP, dan seterusnya.

4. **Baru di sini eksperimen utama DSIC27-06 dimulai: query yang sama diberi noise ITERA.** Mahasiswa merekam **background-only** di ITERA—misalnya area Embung, Arboretum/Kebun Raya, dan area yang lebih antropogenik. Noise tersebut tidak boleh mengandung vocalization target yang kuat. Lalu clean query dari tahap sebelumnya dicampur dengan noise yang sama secara terkontrol. Audit menggunakan kondisi clean, 20 dB, 10 dB, 0 dB, dan -5 dB sebagai rancangan awal. 

   Jadi query Q yang sama menjadi:

```text
Q_clean
Q_20dB
Q_10dB
Q_0dB
Q_-5dB
```

Lalu kelima versi itu masuk ke **MFCC, generic embedding, dan bioacoustic embedding yang sama**.

Inilah yang membuat eksperimennya kuat. Kita tidak membandingkan audio berbeda pada tiap kondisi. Kita membandingkan **paired query**:

```text
burung yang sama
rekaman yang sama
gallery yang sama
hanya noise level yang berubah
```

Dari situ akan terbentuk kurva seperti:

```text
mAP@k
  |
  |\
  | \      Bioacoustic embedding
  |  \
  |   \    Generic embedding
  |    \
  |     \  MFCC
  +---------------- SNR
   clean 20 10 0 -5
```

Pertanyaan ilmiahnya menjadi sangat jelas: **siapa yang turun paling lambat?**

5. **Setelah retrieval robustness, baru lakukan open-set experiment.** Soundscape nyata tidak selalu berisi salah satu spesies yang ada di gallery. Karena itu kita butuh kemampuan sistem untuk berkata **“tidak ada kecocokan yang cukup meyakinkan.”** Dibuat calibration set yang berisi known dan unknown. Dari calibration set itu dipilih threshold similarity \(\tau\). Setelah \(\tau\) ditetapkan, nilainya **dibekukan** dan tidak boleh disetel lagi menggunakan test set. Audit secara eksplisit meminta pemisahan calibration known/unknown dan test known/unknown, lalu mengukur F1, AUROC, AUPRC, FPR/FAR, dan recall setelah threshold dibekukan. 

   Logikanya sederhana:

```text
max_similarity >= τ  → accept candidate species
max_similarity <  τ  → reject / unknown
```

Yang menarik secara penelitian bukan hanya mencari \(\tau\) terbaik. Yang kita uji adalah:

**threshold yang dipilih saat calibration itu masih bekerja tidak ketika noise bertambah?**

Misalnya \(\tau=0.72\) bagus pada clean audio, tetapi ketika 0 dB hampir semua unknown ikut diterima. Itu adalah hasil ilmiah yang penting.

6. **Terakhir barulah masuk real soundscape ITERA.** Ini berbeda dengan eksperimen noise sintetis. Pada controlled mixing, kita tahu persis ground truth-nya karena vocalization berasal dari query Xeno-Canto yang diketahui. Pada real soundscape, masalahnya jauh lebih sulit: jarak mikrofon berubah, reverberasi, suara kendaraan, overlap beberapa burung, arah sumber, respons mikrofon, dan lain-lain terjadi bersamaan. Karena itu audit memisahkan **controlled noise** dan **real domain shift**. Frozen pipeline dijalankan pada subset soundscape ITERA yang sudah dianotasi, dan threshold tidak boleh di-*retune* menggunakan label test ITERA. 

   Jadi hasil akhir yang menarik bukan:

   > “BirdNET menemukan 25 spesies di ITERA.”

   tetapi:

   > “Representasi bioakustik mempertahankan retrieval lebih baik sampai SNR tertentu, tetapi terjadi gap sebesar X ketika berpindah dari controlled noise ke real ITERA soundscape.”

   Itu jauh lebih kuat sebagai penelitian.

7. **Sesudah itu dilakukan failure analysis.** Kita ambil false positive dan false negative paling menarik, lalu diperiksa penyebabnya: suara tumpang tindih, noise antropogenik, SNR rendah, dua spesies dengan vocalization mirip, jarak jauh/reverberasi, event terlalu pendek, atau background signature. Audit meminta minimal failure cases yang dibahas, bukan hanya satu tabel metrik. 

Untuk tools-nya sebenarnya tidak berat. **Python** menjadi pusat pipeline. `librosa`, `soundfile`, `scipy`, dan bila perlu `ffmpeg` dipakai untuk audio preprocessing dan mixing. Untuk deep embedding digunakan **PyTorch atau TensorFlow** sesuai checkpoint, dengan PANNs sebagai generic representation dan satu implementasi bioacoustic embedding. Similarity retrieval cukup dengan **NumPy/scikit-learn**; FAISS baru diperlukan kalau gallery sudah besar. Statistik memakai `pandas`, `NumPy`, `scipy`, dan bila perlu `statsmodels` atau bootstrap sendiri. Visualisasi cukup `matplotlib`; UMAP hanya pendukung. Untuk reproducibility digunakan Git, YAML config, seed, manifest, checksums, dan lock file. Rekaman ITERA dapat memakai field recorder atau **AudioMoth bila tersedia**, dengan konfigurasi perekam dicatat. 

Jadi **tidak perlu Spark, Hadoop, training GPU besar, database kompleks, atau membuat aplikasi mobile** untuk menjawab RQ ini. GPU akan membantu mempercepat ekstraksi pretrained embedding, tetapi setelah embedding tersimpan, cosine retrieval-nya ringan.

Yang paling penting: penelitian ini bukan pertanyaan **“model mana paling akurat?”**, tetapi pertanyaan **“ketika lingkungan makin buruk, representation mana yang kehilangan kemampuan similarity retrieval paling lambat, dan apakah keputusan accept/reject-nya tetap stabil ketika pindah ke kondisi lapangan nyata?”** begitulah inti eksperimennya.
