# Rencana Eksperimen — Minggu 3
**Fokus:** Open-Set Rejection, Kalibrasi Ambang Batas ($\tau$), dan Validasi Soundscape Lapangan  
**Target Garis Waktu:** Hari 15 – Hari 21  
**Status Eksekusi:** **60% SELESAI (TAHAP KOMPUTASI SELESAI, TAHAP PEREKAMAN FISIK DIJADWALKAN)**  

---

## 🎯 Target Rencana & Hasil Eksekusi

### Hari 15–18: Isolasi Data Asing, Kalibrasi $\tau^*$, & Open-Set Testing
* **Target Pembimbing:**
  * Susun himpunan data tak dikenal (*unknown/background set*) sebagai kontrol negatif.
  * Kalibrasi ambang batas kemiripan ($\tau$) pada split kalibrasi.
  * Bekukan nilai $\tau^*$ dan uji ketahanan penolakan kelas asing pada semua level SNR.
* **Hasil Eksekusi Riil:**
  * **Dataset Unknown Terkumpul:** 77 rekaman fauna non-burung (katak, jangkrik, serangga malam, kelelawar, primata).
  * **Perbaikan Kalibrasi Optimal:**
    * Grid search kasar sebelumnya menghasilkan anomali $\tau = 0.0000$ (FPR 100%).
    * Telah diperbaiki menggunakan analisis **Kurva ROC Empiris** dan optimasi **Youden's Index ($J = \text{TPR} - \text{FPR}$)**.
    * Didapatkan nilai ambang batas optimal yang stabil: $\tau^* = 0.9905$ ($F_1\text{-score} = 0.6667$).
  * **Open-Set Testing:** Evaluasi penolakan audio asing berhasil dijalankan pada berbagai tingkatan derau.
* **Bukti Fisik:**
  * Manifes Data Non-Burung: [`data/manifests/unknown_open_set_manifest.csv`](../../data/manifests/unknown_open_set_manifest.csv)
  * Modul Kalibrasi Threshold: [`src/dsic2706/open_set/threshold.py`](../../src/dsic2706/open_set/threshold.py)
  * Tabel Evaluasi Open-Set: [`results/tables/openset_evaluation_table.csv`](../../results/tables/openset_evaluation_table.csv)
  * Tabel Transfer Ambang Batas: [`results/tables/threshold_transfer_table.csv`](../../results/tables/threshold_transfer_table.csv)

---

### Hari 19–21: Validasi Lapangan Soundscape ITERA & Audit Failure Cases
* **Target Pembimbing:**
  * Anotasi subset kecil rekaman lingkungan nyata (*real soundscape*) dari kampus ITERA.
  * Jalankan validasi eksternal tanpa melatih ulang model (*no re-tuning*).
  * Lakukan audit minimal 20 kasus kegagalan retrieval (*failure cases*).
* **Hasil Eksekusi Riil:**
  * **Audit Kasus Kegagalan:** Selesai dilakukan pada lebih dari 20 kasus retrieval dengan analisis penyebab kesalahan (derau frekuensi rendah menutupi harmonik vokal, durasi panggilan terlalu pendek, dll.).
  * **Status Perekaman Lapangan:** Protokol teknis telah disiapkan secara rinci di [`docs/protocols/itera-recording.md`](../../docs/protocols/itera-recording.md), mencakup dua lokasi utama kampus:
    1. **Embung ITERA** (karakteristik: derau angin terbuka, percikan air, serangga air).
    2. **Arboretum / Kebun Raya ITERA** (karakteristik: derau gesekan dedaunan, gemuruh jalan raya sekitar).
  * *Jadwal:* Pengambilan audio fisik di lapangan direncanakan segera berlangsung sesuai jadwal izin bimbingan.
* **Bukti Fisik:**
  * Tabel Audit Kasus Kegagalan: [`results/tables/failure_analysis_table.csv`](../../results/tables/failure_analysis_table.csv)
  * Protokol Perekaman Lapangan: [`docs/protocols/itera-recording.md`](../../docs/protocols/itera-recording.md)
