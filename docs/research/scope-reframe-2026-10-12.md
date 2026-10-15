# Amendemen Scope E4, H3, dan H4

Amendemen awal **12 Oktober 2026**; koreksi pelaporan **15 Oktober 2026**.

## Desain E4 yang dipertahankan

E4 sudah mencakup kelima lokasi: Kebun Raya, Embung F, Gedung F, Masjid At-Tanwir, dan sekitar GKU 1. Untuk setiap representasi terdapat 311 query × 5 lokasi × 4 SNR × 4 ulangan = **24.880 evaluasi noisy**; empat representasi menghasilkan **99.520 baris evaluasi noisy**, di luar baseline clean. Ini bukan 99.520 query independen. Ada 320 snapshot kondisi untuk empat representasi.

E2 dan E4 sama-sama mencampur focal recording Xeno-Canto dengan noise lapangan secara aditif. E2 memakai satu segmen deterministik per query dari pool noise, sedangkan E4 mengondisikan lokasi dan mengulang pemilihan segmen empat kali. Satu lokasi tidak menjawab perbandingan lima profil pada Sub-RQ 3. **E4 tidak dijalankan ulang pada revisi ini.**

E4 tidak menguji vokalisasi target yang direkam langsung di soundscape ITERA. Selisih E4−E2 tidak mengisolasi efek propagasi, jarak, absorpsi, atau reverberasi. Label noise/lokasi juga tidak membuktikan setiap file bebas vokalisasi burung; verifikasi independen per file masih merupakan batasan audit.

## Pelaporan H3 setelah pemeriksaan sensitivitas

Pada lima lokasi, rata-rata ayunan retensi R1 = 0,240111 dan R2 = 0,048607; Δ = 0,191504, CI 95% [0,152203; 0,241969]. Namun rata-rata ayunan **absolut** R1 = 0,042324 dan R2 = 0,030949; Δ = 0,011375, CI [−0,003993; 0,022140], belum membedakan keduanya secara meyakinkan.

Tanpa Kebun Raya, selisih ayunan retensi rata-rata turun menjadi 0,069097, CI [0,048683; 0,121152]. Pada −5 dB, ayunan relatif R1 = 0,065937 dan R2 = 0,083724; Δ = −0,017787, CI [−0,041711; 0,050057]. Pada lima lokasi di −5 dB, ayunan absolut R2 (0,061829) lebih besar daripada R1 (0,045596). Karena itu kalimat umum “R2 berayun lebih sempit di semua SNR” tidak digunakan tanpa menyebut metrik dan subset lokasi.

Kesimpulan H3: **bukti eksploratif bergantung pada normalisasi, SNR, dan komposisi lokasi**, bukan keunggulan stabilitas R2 yang berlaku umum. Dugaan peran serangga atau profil frekuensi tetap dugaan; fitur spektral segmen noise belum diuji sebagai mekanisme kausal.

Analisis memakai [CSV mentah E4](../../results/reproductions/E4_5sites_20261011T213404_350219Z/raw/) dan disimpan terpisah di [H3_sensitivity_20261015](../../results/reproductions/H3_sensitivity_20261015/). Analisis 12 Oktober tetap disimpan sebagai riwayat. Definisi ayunan dan bootstrap tercantum dalam [hipotesis](hypotheses.md).

## Pelaporan H4

Threshold tetap berasal dari calibration-clean dan tidak dikalibrasi ulang. Known acceptance recall R2 turun dari 0,604502 ke 0,254019 pada −5 dB, sementara false-accept rate turun dari 0,222581 ke 0,129032. Recall di sini berarti penerimaan query known, bukan ketepatan spesies hasil Top-1. Hasil itu konsisten dengan klausul penurunan recall pada H4 asli, tetapi tidak dengan dugaan lonjakan false accept. Reformulasi interpretasinya tetap diberi label eksploratif.

## Riwayat rumusan dan status eksploratif

Rumusan asli berikut sudah tercatat pada **6 September 2026**, commit **25ebb72**, dan masih ada pada parent commit konsolidasi **7817355**:

- **H3 asli — Real Domain Shift Gap:** “Kinerja retrieval pada *real soundscape* ITERA turun lebih tajam daripada kondisi *controlled mixture* pada level SNR sebanding karena pergeseran domain tidak hanya berupa derau aditif, melainkan mencakup propagasi jarak, absorpsi udara, dan *reverberation*.”
- **H4 asli — Threshold Transfer Instability:** “Ambang batas kemiripan (τ) yang optimal pada kondisi bersih (*calibration-clean*) mengalami pergeseran titik operasi (*operating point drift*) saat derau lingkungan bertambah, memicu anjloknya *recall* atau lonjakan *false accept rate*.”

**12 Oktober 2026:** commit **7817355** merekam perubahan H3 menjadi stabilitas retensi profil noise lokasi dan H4 menjadi perubahan titik operasi ambang beku. Perubahan rumusan dicatat setelah artefak hasil E4/E3 tersedia, sehingga **H3 hasil reformulasi dan interpretasi H4 hasil reformulasi bersifat eksploratif**, bukan hipotesis baru yang dibekukan sebelum hasil dilihat. Klausul penurunan recall sudah ada pada H4 asli; perluasan bahasa menjadi “perubahan perilaku” tidak boleh digunakan untuk menyembunyikan bahwa false-accept rate tidak meningkat.

**15 Oktober 2026:** pelaporan H3 diperluas dengan ayunan mAP@10 absolut dan analisis sensitivitas tanpa Kebun Raya atas CSV yang sama. Tidak ada penghapusan lokasi dari E4, perubahan threshold, atau pengulangan eksperimen. H3 asli tentang real-soundscape tetap **belum diuji**. Tidak ada bukti uji langsung untuk mekanisme distorsi frekuensi, biofoni serangga, atau kompresi skor sebagai penyebab.
