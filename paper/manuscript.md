# Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval under Controlled ITERA Field-Noise Mixtures in Indonesian Avifauna

**Draf metode dan struktur hasil — angka final dirujuk dari artefak tervalidasi**

Penelitian ini mengevaluasi representasi audio beku untuk *similarity retrieval* avifauna Indonesia ketika query focal recording Xeno-Canto dicampur secara terkontrol dengan noise lapangan AudioMoth ITERA. Desain ini adalah *controlled additive field-noise mixture*, bukan evaluasi burung yang direkam langsung di *real soundscape* ITERA.

## Pertanyaan penelitian aktif

1. Representasi mana yang mempertahankan retrieval terbaik ketika SNR query menurun?
2. Apakah threshold kemiripan yang dikalibrasi terpisah dan dibekukan memiliki perilaku penerimaan/penolakan yang terukur pada target dan unknown bising?
3. Apakah representasi bioakustik memiliki retensi retrieval yang lebih stabil lintas profil noise lima lokasi ITERA dibanding representasi audio umum?
4. Faktor margin dan spektral apa yang berkaitan dengan false rejection, top-1 confusion, dan total collapse?

## Eksperimen dan sumber hasil

- **E0:** audit format dan pra-pemrosesan — `results/reproductions/E0_20261011_202557/`.
- **EDA:** distribusi data fisik, waveform, dan spektrogram — `notebooks/03_EDA_Physical_Audio.ipynb`.
- **E1:** clean retrieval R0–R3 — `results/tables/10_e1_clean_retrieval_summary.csv`.
- **E2:** controlled noise — `results/tables/11_e2_snr_robustness.csv`.
- **E3:** frozen open-set threshold — `results/tables/12_e3_frozen_thresholds.csv`.
- **E4/H3:** sensitivitas dan stabilitas profil noise lokasi — `results/tables/14_e4_domain_shift.csv`, `results/tables/24_h3_habitat_profile_stability.csv`, dan `results/figures/15_h3_habitat_retention_stability.png`.
- **E5:** diagnostik kegagalan — `results/tables/15_e5_failure_mode_summary.csv`.

## Hasil H3 untuk Bab 4

R1/PANNs memiliki ayunan retensi rata-rata 0.240, sedangkan R2/BirdNET 0.049; perbedaannya 0.192, CI 95% [0.152, 0.242] melalui paired bootstrap 10.000 kali. H3 didukung: BirdNET lebih stabil lintas lima profil noise lokasi pada empat SNR yang diuji.

Uji stabilitas H3 ditambahkan setelah run E4 selesai dan dilaporkan sebagai analisis eksploratif. Penjelasan khusus tentang distorsi frekuensi tinggi/rendah memerlukan analisis spektral per segmen noise yang belum dilakukan.

## Batasan scope

H3 menguji stabilitas terhadap profil noise lokasi dalam *additive mixture*. Bank ITERA bebas spesies target dan digunakan sebagai noise; penelitian ini tidak meminta atau membutuhkan anotasi spesies target dari bank tersebut. Kesimpulan tidak mencakup jarak burung-mikrofon, propagasi, reverberasi, atau performa focal recording yang direkam langsung dalam soundscape ITERA.

Narasi hasil dan status hipotesis yang terkendali tersedia di `docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md` dan `docs/research/scope-reframe-2026-10-12.md`.
