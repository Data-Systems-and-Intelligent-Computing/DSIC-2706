# Catatan Keputusan Riset (Decision Log) — DSIC-2706

| Tanggal | ID Keputusan | Topik / Isu | Keputusan yang Diambil | Rationale & Dampak |
| :---: | :---: | :--- | :--- | :--- |
| **05 Sep 2026** | **DEC-01** | Sumber Data & Geografis | Tidak mensyaratkan rekaman harus tepat di dalam 4 Taman Nasional. Menggunakan rekaman Xeno-Canto di wilayah Sumatera / Indonesia dengan metadata lokasi valid. | Mencegah *extreme low-resource sample bottleneck* dan memastikan kecukupan volume audio per spesies. |
| **05 Sep 2026** | **DEC-02** | Takson Non-Burung | Mengisolasi 77 berkas audio fauna non-burung (serangga, katak, kelelawar, primata) ke dalam `data/unknown_open_set/`. | Menghindari polusi kelas pada target retrieval burung, sekaligus menyediakan dataset negatif realistis untuk evaluasi open-set rejection. |
| **06 Sep 2026** | **DEC-03** | Spesies *Oriolus chinensis* | Mengganti *Oriolus chinensis* (akses audio terbatas via API Xeno-Canto v3 karena kebijakan anti-perburuan liar) dengan *Aethopyga siparaja* dan *Dicaeum trigonostigma*. | Memastikan 100% berkas audio fisik dapat diunduh secara legal dan berlisensi terbuka tanpa tautan terputus. |
| **06 Sep 2026** | **DEC-04** | Kalibrasi Threshold $\tau$ | Mengganti grid search linier kasar dengan ambang batas kurva ROC empiris dan indeks Youden's $J = \text{TPR} - \text{FPR}$. | Mengatasi bug degenerasi numerik $\tau = 0.0000$ (FPR 100%) pada skor kosinus MFCC, menghasilkan $\tau^* = 0.9905$ yang valid secara teoritis. |
| **06 Sep 2026** | **DEC-05** | Partisi Data | Menerapkan partisi **Strict Global Recordist-Disjoint** ($\mathcal{R}_{\text{Gallery}} \cap \mathcal{R}_{\text{Query}} = \emptyset$). | Mencegah kebocoran mikrofon dan alat perekam (*recording gear fingerprinting*), diuji dengan unit testing formal. |
