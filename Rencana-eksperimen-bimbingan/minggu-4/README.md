# Rencana Eksperimen — Minggu 4
**Fokus:** Analisis Statistik Lanjutan, Penulisan Naskah Skripsi/Artikel, dan Pembekuan Repositori  
**Target Garis Waktu:** Hari 22 – Hari 30  
**Status Eksekusi:** **DIJADWALKAN (DRAF AWAL & TEMPLATE TELAH SIAP)**  

---

## 🎯 Target Rencana & Langkah Kerja

### Hari 22–24: Statistik Inferensial & Kurva Presisi-Recall
* **Target Pembimbing:**
  * Hitung selang kepercayaan berpasangan (*paired bootstrap confidence interval* 95%) untuk membuktikan signifikansi perbedaan performa antar model.
  * Buat plot kurva Precision-Recall (PR) komprehensif.
  * Uji ketahanan perpindahan ambang batas (*threshold transfer stability*).
* **Kesiapan Modul:**
  * Pipeline evaluasi di [`src/dsic2706/evaluation/`](../../src/dsic2706/evaluation/) telah siap untuk pemanggilan bootstrap sampling.

---

### Hari 25–27: Penulisan Naskah Skripsi & Artikel Ilmiah
* **Target Pembimbing:**
  * Menyusun naskah Bab 3 (Metode Penelitian), Bab 4 (Hasil dan Pembahasan), serta sub-bab *Threats to Validity*.
  * Merapikan atribuisi sitasi, sumber dataset Xeno-Canto, dan deklarasi etika penelitian bioakustik.
* **Kesiapan Draf:**
  * Draf laporan dan catatan hasil riset telah terintegrasi di:
    * [`CATATAN_PROGRES_BIMBINGAN.md`](../CATATAN_PROGRES_BIMBINGAN.md)

---

### Hari 28–30: Reproduksi Mandiri, Freeze Code, & Materi Sidang
* **Target Pembimbing:**
  * Lakukan *fresh reproduction* dari awal (*clean environment*) untuk mereproduksi satu tabel utama dan satu grafik utama.
  * Kunci kode, konfigurasi, dan artefak hasil (*code & result freeze*).
  * Selesaikan draf artikel jurnal v0.8 dan slide presentasi sidang/seminar.
* **Prosedur Uji Reproduksibilitas:**
  ```bash
  # Verifikasi keterulangan deterministik
  python -m dsic2706.cli sanity
  ```
