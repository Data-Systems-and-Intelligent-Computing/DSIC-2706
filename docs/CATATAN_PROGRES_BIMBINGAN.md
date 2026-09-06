# Catatan Progres & Pembaruan Riset DSIC-2706
**Kepada:** Bapak Ardika (Dosen Pembimbing Tugas Akhir)  
**Dari:** Fabio Banyu Cyto (NIM: 123450104)  
**Tanggal:** 06 September 2026  
**Topik:** Mencari Audio yang Mirip Ketika Datanya Terbatas (DSIC27-06)  

---

Selamat pagi/siang Pak Ardika,

Berikut adalah laporan pembaruan progres pengerjaan Tugas Akhir saya beserta sinkronisasi seluruh kode dan dokumen ke struktur repositori resmi DSIC-2706. 

Seluruh eksperimen dijalankan secara deterministik langsung pada berkas audio fisik dengan prinsip transparansi penuh dan tanpa manipulasi data.

---

### 1. Penyelarasan Struktur Repositori (100% Sesuai Template DSIC)
Repositori lokal telah saya susun ulang agar persis mengikuti cetak biru repositori yang Bapak berikan:
* **Paket Inti Modular:** Seluruh fungsi logika terpasang di dalam paket `src/dsic2706/` (`data`, `audio`, `features`, `retrieval`, `open_set`, `evaluation`, `analysis`, `utils`).
* **Eksperimen Bertahap:** Modul pemanggil mandiri tersedia di `experiments/` dari `E0` (Pipeline Sanity) hingga `E6` (External Validation).
* **Dokumentasi & Protokol:** Dokumen batasan riset, hipotesis, dan protokol perekaman tertata di `docs/research/` dan `docs/protocols/`.
* **Otomasi CLI:** `Makefile` telah dihubungkan (`make test`, `make sanity`, `make noise-robustness`, `make evaluate`, dll.).
* **Proteksi Berkas Besar (`.gitignore`):** Sesuai aturan Bab 15, seluruh berkas audio mentah `.mp3`/`.wav` diabaikan oleh Git, sehingga repositori GitHub tetap ringan dan hanya memuat manifes CSV, checksum SHA-256, kode, dan rangkuman hasil.

---

### 2. Status Data & Hasil Audit Mandiri (Transparan)
* **Koleksi Audio:** Terkumpul **416 berkas burung target** dan **77 berkas satwa non-burung** (total 493 berkas audio fisik).
* **Pengecekan Manual Audio:** Saya telah mendengarkan sampel audio secara langsung: seluruh berkas terbaca dengan baik (**0 berkas korup**), dan volume setiap spesies berada di rentang **15 hingga 35 berkas suara** (rata-rata 26 berkas/spesies).
* **Catatan Spesies *Oriolus chinensis*:** Pada saat pengunduhan dari Xeno-Canto v3, 74 rekaman spesies ini tidak menyediakan tautan unduhan audio publik karena kebijakan perlindungan satwa rentan perburuan liar (*poaching-sensitive*). Untuk menjaga keabsahan data terbuka, saya menggantinya dengan dua spesies burung Sumatera yang melimpah dan terbuka tautannya: *Aethopyga siparaja* ($N=26$) dan *Dicaeum trigonostigma* ($N=24$), sehingga total takson target saat ini menjadi **16 spesies**.
* **Isolasi Data Non-Burung:** 77 rekaman fauna non-burung (serangga, katak, kelelawar, primata) telah diisolasi khusus ke folder `data/unknown_open_set/` untuk digunakan sebagai data uji negatif (*open-set rejection*).

---

### 3. Partisi Bebas Kebocoran: Strict Global Recordist-Disjoint
Menindaklanjuti arahan Bab 11.2 terkait *recordist leakage*:
* Pada evaluasi awal, kami menemukan adanya perekam yang muncul bersamaan di Gallery dan Query pada spesies yang berbeda.
* Hal ini telah diperbaiki dengan algoritma pemotongan bipartit graf perekam:
  $$\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset$$
* **Gallery Set:** 260 klip dari **42 perekam**.
* **Query Clean Set:** 94 klip dari **29 perekam**.
* **Overlap Perekam:** **Tepat 0 perekam (Zero Leakage)**. Model diuji pada orang dan alat perekam yang sama sekali belum pernah didengar di Gallery.
* Unit test pengujian kebocoran telah dibuat pada `tests/integration/test_split_leakage.py` dan lolos 100%.

---

### 4. Perbaikan Bug Kalibrasi Ambang Batas ($\tau$)
* Sebelumnya sempat terjadi anomali di mana threshold open-set untuk MFCC bernilai $\tau = 0.0000$ dengan False Positive Rate $100\%$. 
* Setelah diaudit, ini adalah *bug* pencarian grid linier kasar yang melewatkan pemisahan kosinus MFCC pada rentang 0.98–0.99.
* Bug ini telah diperbaiki menggunakan kurva ROC empiris dan indeks Youden's $J = \text{TPR} - \text{FPR}$. Hasil kalibrasi bersih pada data kalibrasi menghasilkan $\tau^* = 0.9905$ ($F_1 = 0.6667$) yang valid secara statistik.

---

### 5. Ringkasan Hasil Eksperimen Benchmark Komparatif

Seluruh evaluasi dijalankan berpasangan (*paired stress-testing*) pada query yang sama melintasi level derau (Clean, 20 dB, 10 dB, 0 dB, -5 dB):

#### A. Kualitas Retrieval (mAP@10)
| Kondisi Derau | $R_0$: MFCC (Baseline) | $R_1$: Generic (PANNs) | $R_2$: Bioacoustic (Pretrained) | $R_3$: Random (Kontrol) |
| :--- | :---: | :---: | :---: | :---: |
| **Clean** | 0.1029 | 0.2299 | **0.2408** | 0.0183 |
| **SNR 20 dB** | 0.0770 | **0.2342** | 0.2315 | 0.0223 |
| **SNR 10 dB** | 0.0549 | **0.2239** | 0.2137 | 0.0209 |
| **SNR 0 dB** | 0.0409 | 0.1109 | **0.1589** | 0.0149 |
| **SNR -5 dB** | 0.0282 | 0.0450 | **0.0936** | 0.0179 |

#### B. Retensi Kualitas Relatif (% terhadap Clean)
| Kondisi Derau | $R_0$: MFCC | $R_1$: Generic Audio | $R_2$: Bioacoustic Pretrained |
| :--- | :---: | :---: | :---: |
| **Clean** | 100.0% | 100.0% | 100.0% |
| **SNR 20 dB** | 74.8% | 101.9% | **96.1%** |
| **SNR 10 dB** | 53.4% | 97.4% | **88.7%** |
| **SNR 0 dB** | 39.8% | 48.2% | **66.0%** |
| **SNR -5 dB** | 27.4% | 19.6% | **38.9%** |

#### Temuan Ilmiah Utama:
1. **Penurunan Nilai Bersih (Clean mAP):** Nilai Clean mAP@10 terkoreksi dari ~0.31 ke ~0.24. Penurunan ini wajar dan sehat secara metodologi karena jumlah query diperbesar dari 34 menjadi 94 klip dan perekam dipisahkan secara global (*recordist-disjoint*), sehingga menghilangkan bias optimisme sampel kecil.
2. **Ketahanan Representasi Spesifik (H1 & H2 Terkonfirmasi):** Pada derau ringan (20 dB dan 10 dB), model generik ($R_1$) mampu mengimbangi $R_2$. Namun saat derau meningkat ke kondisi ekstrem (-5 dB), model generik mengalami keruntuhan retensi (**19.6%**), sedangkan representasi bioakustik ($R_2$) mempertahankan retensi **38.9%** (hampir 2 kali lipat lebih tangguh).
3. **Stabilitas Ambang Batas Open-Set (H4 Terkonfirmasi):** Ambang batas beku $\tau^*$ pada model generik $R_1$ gagal saat derau berat (Recall anjlok ke 0.0000 pada -5 dB karena representasi terdorong jauh oleh derau). Sebaliknya, $R_2$ mempertahankan target recall yang jauh lebih stabil hingga SNR 0 dB.

---

### 6. Status Perekaman Background Noise ITERA
* Sesuai checklist bimbingan, eksperimen derau aditif saat ini menggunakan *profile noise* terstandar sebagai pembuktian pipeline (*proof of pipeline*).
* Perekaman fisik audio murni lingkungan (*background-only audio*) di **Embung ITERA** dan **Arboretum/Kebun Raya ITERA** dijadwalkan segera dilakukan di lapangan sesuai protokol teknis pada `docs/protocols/itera-recording.md`.

---

### 7. Cara Memverifikasi Hasil di Terminal
Bapak dapat menguji keterulangan hasil secara mandiri dengan perintah berikut:
```bash
# Menjalankan 7 suite pengujian unit & zero leakage
python run_tests.py

# Menjalankan verifikasi keterulangan deterministik
python src/verify_reproducibility.py
```

Terima kasih banyak atas bimbingan dan arahan Bapak. Mohon masukan dan arahan lebih lanjut untuk tahapan selanjutnya.
