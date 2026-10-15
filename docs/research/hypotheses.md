# Hipotesis Penelitian — DSIC-2706

Revisi pelaporan: **15 Oktober 2026**. Hasil E4 berasal dari 311 query × 5 lokasi × 4 SNR × 4 ulangan, dengan gallery tetap. Penelitian mengevaluasi pencampuran aditif noise lapangan ITERA pada audio burung Xeno-Canto; real-soundscape burung in-situ belum diuji.

- **H1 — Robustness retention:** representasi deep pretrained mempertahankan proporsi mAP@10 relatif lebih besar daripada MFCC ketika SNR menurun.
- **H2 — Domain-specific advantage under additive noise:** embedding bioakustik mengalami penurunan retensi retrieval lebih kecil daripada embedding audio generik pada query burung yang dicampur noise ITERA.
- **H3 hasil reformulasi — Stabilitas lintas profil noise lokasi (eksploratif):** ayunan retensi R2/BirdNET dibandingkan dengan R1/PANNs pada profil noise lokasi ITERA. Pelaporan wajib menyertakan ayunan mAP@10 absolut dan sensitivitas komposisi lokasi; mekanisme frekuensi tidak menjadi kesimpulan.
- **H4 hasil reformulasi — Perubahan titik operasi threshold beku (eksploratif):** perubahan recall penerimaan known-set dan false-accept rate unknown dilaporkan terpisah ketika threshold dari calibration-clean dipindahkan ke query bising. Penurunan recall terlihat; kenaikan false-accept rate tidak terlihat.
- **H5 — Positive control baseline:** clean retrieval R0, R1, dan R2 mengungguli kontrol ID-deterministik R3.

## Operasionalisasi H3

Untuk representasi m, SNR s, ulangan r, dan lokasi l, hitung A(m,s,r,l) = rata-rata AP@10 dari 311 query. C(m) adalah mAP@10 bersih representasi tersebut.

- **Ayunan absolut:** S_abs(m,s) = mean_r[max_l A(m,s,r,l) − min_l A(m,s,r,l)].
- **Ayunan relatif:** S_rel(m,s) = S_abs(m,s) / C(m).
- **Urutan agregasi:** hitung rentang lintas lokasi pada setiap ulangan, baru rata-ratakan empat ulangan. Ini berbeda dari rentang atas profil yang terlebih dahulu dirata-ratakan.
- **Sensitivitas:** seluruh lima lokasi dibandingkan dengan subset tanpa Kebun Raya. E4 asli tetap berisi lima lokasi.
- **Inferensi:** bootstrap 10.000 kali, seed 20261012, memakai indeks query yang sama untuk R1/R2 dan semua kondisi. Penyebut clean dihitung kembali pada setiap resampling. CI persentil bersifat eksploratif, kondisional pada lokasi dan segmen noise yang sudah dipilih, tanpa koreksi keluarga uji baru.

Pada lima lokasi, rata-rata ayunan retensi R1 = 0,240111 dan R2 = 0,048607; Δ = 0,191504, CI 95% [0,152203; 0,241969]. Namun rata-rata ayunan **absolut** R1 = 0,042324 dan R2 = 0,030949; Δ = 0,011375, CI [−0,003993; 0,022140], belum membedakan keduanya secara meyakinkan.

Tanpa Kebun Raya, selisih ayunan retensi rata-rata turun menjadi 0,069097, CI [0,048683; 0,121152]. Pada −5 dB, ayunan relatif R1 = 0,065937 dan R2 = 0,083724; Δ = −0,017787, CI [−0,041711; 0,050057]. Pada lima lokasi di −5 dB, ayunan absolut R2 (0,061829) lebih besar daripada R1 (0,045596). Karena itu kalimat umum “R2 berayun lebih sempit di semua SNR” tidak digunakan tanpa menyebut metrik dan subset lokasi.

Kesimpulan H3: **bukti eksploratif bergantung pada normalisasi, SNR, dan komposisi lokasi**, bukan keunggulan stabilitas R2 yang berlaku umum. Dugaan peran serangga atau profil frekuensi tetap dugaan; fitur spektral segmen noise belum diuji sebagai mekanisme kausal.

Sumber lengkap: [analisis sensitivitas](../../results/reproductions/H3_sensitivity_20261015/tables/h3_swing_summary.csv), [catatan revisi](../REVISION_SUPERVISOR_2026-10-15.md), dan [matriks revisi](../../results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv).

## Riwayat rumusan dan status eksploratif

Rumusan asli berikut sudah tercatat pada **6 September 2026**, commit **25ebb72**, dan masih ada pada parent commit konsolidasi **7817355**:

- **H3 asli — Real Domain Shift Gap:** “Kinerja retrieval pada *real soundscape* ITERA turun lebih tajam daripada kondisi *controlled mixture* pada level SNR sebanding karena pergeseran domain tidak hanya berupa derau aditif, melainkan mencakup propagasi jarak, absorpsi udara, dan *reverberation*.”
- **H4 asli — Threshold Transfer Instability:** “Ambang batas kemiripan (τ) yang optimal pada kondisi bersih (*calibration-clean*) mengalami pergeseran titik operasi (*operating point drift*) saat derau lingkungan bertambah, memicu anjloknya *recall* atau lonjakan *false accept rate*.”

**12 Oktober 2026:** commit **7817355** merekam perubahan H3 menjadi stabilitas retensi profil noise lokasi dan H4 menjadi perubahan titik operasi ambang beku. Perubahan rumusan dicatat setelah artefak hasil E4/E3 tersedia, sehingga **H3 hasil reformulasi dan interpretasi H4 hasil reformulasi bersifat eksploratif**, bukan hipotesis baru yang dibekukan sebelum hasil dilihat. Klausul penurunan recall sudah ada pada H4 asli; perluasan bahasa menjadi “perubahan perilaku” tidak boleh digunakan untuk menyembunyikan bahwa false-accept rate tidak meningkat.

**15 Oktober 2026:** pelaporan H3 diperluas dengan ayunan mAP@10 absolut dan analisis sensitivitas tanpa Kebun Raya atas CSV yang sama. Tidak ada penghapusan lokasi dari E4, perubahan threshold, atau pengulangan eksperimen. H3 asli tentang real-soundscape tetap **belum diuji**. Tidak ada bukti uji langsung untuk mekanisme distorsi frekuensi, biofoni serangga, atau kompresi skor sebagai penyebab.
