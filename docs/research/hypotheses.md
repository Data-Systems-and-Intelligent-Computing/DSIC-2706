# Hipotesis Penelitian — DSIC-2706

Penelitian ini merumuskan lima hipotesis formal:

- **H1 — Robustness Retention:**
  Representasi *deep pretrained* mempertahankan proporsi `mAP@k` relatif yang lebih besar daripada representasi parametrik klasik MFCC ketika SNR diturunkan secara progresif.
- **H2 — Domain-Specific Advantage:**
  *Bioacoustic pretrained embedding* mengalami penurunan retensi retrieval yang lebih kecil daripada *generic pretrained audio embedding* (seperti PANNs) pada query burung dengan derau lingkungan tropis.
- **H3 — Real Domain Shift Gap:**
  Kinerja retrieval pada *real soundscape* ITERA turun lebih tajam daripada kondisi *controlled mixture* pada level SNR sebanding karena pergeseran domain tidak hanya berupa derau aditif, melainkan mencakup propagasi jarak, absorpsi udara, dan *reverberation*.
- **H4 — Threshold Transfer Instability:**
  Ambang batas kemiripan ($\tau$) yang optimal pada kondisi bersih (*calibration-clean*) mengalami pergeseran titik operasi (*operating point drift*) saat derau lingkungan bertambah, memicu anjloknya *recall* atau lonjakan *false accept rate*.
- **H5 — Positive Control Baseline:**
  Retrieval pada kondisi bersih (*clean retrieval*) untuk seluruh representasi utama (R0, R1, R2) harus secara signifikan mengungguli *random ranking* ($R_3$). Jika tidak, pipeline eksperimen wajib diaudit sebelum interpretasi dilakukan.

*Catatan Metodologi: Semua hipotesis diuji secara empiris dengan interval kepercayaan 95%. Hasil penolakan hipotesis tetap merupakan temuan ilmiah yang valid.*
