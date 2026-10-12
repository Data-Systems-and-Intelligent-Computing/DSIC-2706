"""Synchronize H3 documentation with the completed E4 raw-data analysis."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RUN = sorted((ROOT / "results/reproductions").glob("H3_habitat_profile_stability_*"))[-1]
SUMMARY = pd.read_csv(RUN / "tables/h3_stability_summary.csv")
ALL = SUMMARY.loc[SUMMARY.analysis_scope.eq("mean_over_4_SNR_levels")].iloc[0]
MINUS5 = SUMMARY.loc[SUMMARY.analysis_scope.eq("per_snr") & SUMMARY.snr_db.astype(str).eq("-5")].iloc[0]


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if old not in text:
        raise RuntimeError(f"Expected text not found: {path}")
    target.write_text(text.replace(old, new), encoding="utf-8")

h3_statement = """- **H3 — Habitat Profile Stability**  
  Representasi bioakustik terlatih mempertahankan retensi relatif `mAP@10` yang secara signifikan lebih stabil dan tidak fluktuatif lintas profil spektral habitat (ayunan retensi sempit) dibandingkan representasi audio umum yang rentan terhadap distorsi frekuensi tinggi/rendah."""

write("docs/research/hypotheses.md", f"""# Hipotesis Penelitian — DSIC-2706

H1, H2, H4, dan H5 diuji pada protokol *controlled additive field-noise mixture*. H3 juga diuji pada E4, sebagai perbandingan stabilitas retensi lintas **profil noise lapangan** ITERA. E4 tidak diklaim sebagai validasi rekaman burung *in-situ*.

- **H1 — Robustness retention**  
  Representasi *deep pretrained* mempertahankan proporsi `mAP@10` relatif lebih besar daripada MFCC ketika SNR diturunkan secara progresif.
- **H2 — Domain-specific advantage under additive noise**  
  Embedding bioakustik mengalami penurunan retensi retrieval lebih kecil daripada embedding audio generik pada query burung yang dicampur noise ITERA.
{h3_statement}
- **H4 — Frozen-threshold operating-point change**  
  Threshold τ* yang optimal pada calibration-clean berubah perilaku operasionalnya saat query diberi noise; perubahan dapat tampak sebagai penurunan recall known-set atau perubahan false-accept rate.
- **H5 — Positive control baseline**  
  Clean retrieval R0, R1, dan R2 secara signifikan mengungguli kontrol ID-deterministik R3.

## Operasionalisasi H3

- **Pembanding utama:** R1/PANNs (audio umum) versus R2/BirdNET (bioakustik).
- **Sumber:** CSV mentah E4 yang tervalidasi, tanpa menghitung ulang pencampuran audio.
- **Unit:** 311 query yang sama, lima profil lokasi noise ITERA, empat segmen noise acak per lokasi, dan empat SNR.
- **Ukuran stabilitas:** untuk setiap representasi, `swing = max(relative retention antar lokasi) − min(relative retention antar lokasi)`, dirata-ratakan atas empat pengulangan segmen noise.
- **Uji:** paired bootstrap 10.000 resampling query, seed 20261012. H3 didukung apabila CI 95% untuk `swing R1 − swing R2` seluruhnya positif.

Hasil rata-rata empat SNR: ayunan R1 = {ALL['R1_generic_mean_swing']:.6f}; R2 = {ALL['R2_bioacoustic_mean_swing']:.6f}; selisih = {ALL['R1_minus_R2_effect']:.6f}; CI 95% [{ALL['ci95_low']:.6f}, {ALL['ci95_high']:.6f}]. H3 **didukung** dalam desain additive ITERA-noise.

## Aturan interpretasi

E4 membuktikan stabilitas atau sensitivitas terhadap **profil noise lapangan** dari lokasi ITERA setelah pencampuran aditif pada SNR terkendali. E4 tidak mendukung klaim tentang jarak burung-mikrofon, propagasi, absorpsi, reverberasi, atau perilaku burung *in-situ*. Bank ITERA bebas spesies target; karenanya anotasi spesies target tidak diperlukan untuk E2/E4.
""")

write("docs/research/scope-reframe-2026-10-12.md", f"""# Amendemen Scope dan H3 — 12 Oktober 2026

## Batas desain yang tetap berlaku

E2 dan E4 mencampur focal recording Xeno-Canto dengan noise lapangan AudioMoth ITERA secara aditif. Karena itu penelitian tidak mengklaim evaluasi rekaman burung yang dibuat langsung dalam *real soundscape* ITERA, termasuk efek jarak, propagasi, atau perilaku burung *in-situ*.

## H3 yang diuji

H3 bukan klaim *real-soundscape domain shift*. H3 menguji apakah representasi bioakustik mempertahankan **ayunan retensi yang lebih sempit** lintas profil spektral noise dari habitat/lokasi ITERA daripada representasi audio umum. Ini tepat diuji oleh E4 karena semua query, SNR, gallery, dan protokol retrieval dibuat sama; hanya profil noise lokasi yang berubah.

E4 memakai lima lokasi noise ITERA: Kebun Raya, Embung F, Gedung F, Masjid At-Tanwir, dan Sekitar GKU 1. Set ITERA bebas spesies target sehingga anotasi target-species tidak diperlukan.

## Bukti dan keputusan

Analisis statistik H3 memakai 311 query, lima profil lokasi, empat pengulangan segmen noise per lokasi, empat SNR, dan paired bootstrap 10.000 kali. Pada rata-rata empat SNR, ayunan retensi R1/PANNs = {ALL['R1_generic_mean_swing']:.6f} dan R2/BirdNET = {ALL['R2_bioacoustic_mean_swing']:.6f}; selisih R1−R2 = {ALL['R1_minus_R2_effect']:.6f}, CI 95% [{ALL['ci95_low']:.6f}, {ALL['ci95_high']:.6f}]. H3 **didukung**.

Artefak: [`{RUN.relative_to(ROOT).as_posix()}`](../../{RUN.relative_to(ROOT).as_posix()}/), [tabel ringkasan](../../results/tables/24_h3_habitat_profile_stability.csv), dan [grafik](../../results/figures/15_h3_habitat_retention_stability.png).
""")

replace("configs/experiments.yaml", '''    interpretation_scope: "additive field-noise profile sensitivity only"
    real_soundscape_domain_shift_h3: "not_tested_out_of_scope"''', '''    interpretation_scope: "additive field-noise profile sensitivity only; not an in-situ bird soundscape claim"
    h3_habitat_profile_stability: "tested from E4 raw: R1/PANNs vs R2/BirdNET retention swing across five locations"''')
replace("configs/datasets.yaml", '''    interpretation_scope: "additive noise-profile sensitivity only; not real-soundscape domain shift"''', '''    interpretation_scope: "additive noise-profile sensitivity; supports H3 retention-stability comparison, not an in-situ bird soundscape claim"''')

results = ROOT / "docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md"
text = results.read_text(encoding="utf-8")
text = text.replace("| E4 | VALID | results/reproductions/E4_5sites_20261011T213404_350219Z; results/reproductions/E4_audit_20261012T021801_989259Z | Original raw lacks ranking identities, class margins, and noisy-audio feature fields. |", f"| E4/H3 | VALID | results/reproductions/E4_5sites_20261011T213404_350219Z; results/reproductions/E4_audit_20261012T021801_989259Z; {RUN.relative_to(ROOT).as_posix()} | H3 is derived read-only from E4 raw; raw lacks ranking identities, class margins, and noisy-audio feature fields. |")
text = text.replace("E4 raw menyimpan `top1_match` dan `max_score`. Ia tidak menyimpan identitas Top-1, skor kelas benar, skor pesaing, margin kelas, atau fitur akustik dari audio noisy.", f"""E4 raw menyimpan `top1_match` dan `max_score`. Ia tidak menyimpan identitas Top-1, skor kelas benar, skor pesaing, margin kelas, atau fitur akustik dari audio noisy.

### H3 — stabilitas retensi lintas profil lokasi

H3 membandingkan ayunan retensi `mAP@10` lintas lima lokasi: `maksimum retensi − minimum retensi`, dirata-ratakan atas empat segmen noise acak per lokasi. Hasil statistik berasal dari CSV mentah E4, memakai 311 query yang sama dan bootstrap berpasangan 10.000 kali. Tidak ada audio yang dicampur ulang.

| ringkasan 4 SNR | Ayunan R1/PANNs | Ayunan R2/BirdNET | R1 − R2 | CI 95% | Kesimpulan |
| --- | ---: | ---: | ---: | --- | --- |
| mAP@10 relative retention | {ALL['R1_generic_mean_swing']:.6f} | {ALL['R2_bioacoustic_mean_swing']:.6f} | {ALL['R1_minus_R2_effect']:.6f} | [{ALL['ci95_low']:.6f}, {ALL['ci95_high']:.6f}] | H3 didukung |

Pada −5 dB, ayunan R1 = {MINUS5['R1_generic_mean_swing']:.6f} dan R2 = {MINUS5['R2_bioacoustic_mean_swing']:.6f}; selisih {MINUS5['R1_minus_R2_effect']:.6f}, CI 95% [{MINUS5['ci95_low']:.6f}, {MINUS5['ci95_high']:.6f}]. Detail tersedia pada `results/tables/24_h3_habitat_profile_stability.csv` dan `results/figures/15_h3_habitat_retention_stability.png`.""")
text = text.replace("Scope aktif merujuk `docs/research/rq.md`, `docs/research/hypotheses.md`, dan `docs/research/scope-reframe-2026-10-12.md`. E4 dibingkai sebagai sensitivitas profil noise lapangan dalam additive mixture dan menjawab Sub-RQ3 yang dipersempit. H3 tentang real-soundscape domain shift ditulis belum diuji dan berada di luar scope aktif. E5 menjawab Sub-RQ4 sebagai diagnostik kegagalan.", "Scope aktif merujuk `docs/research/rq.md`, `docs/research/hypotheses.md`, dan `docs/research/scope-reframe-2026-10-12.md`. E4 dibingkai sebagai sensitivitas profil noise lapangan dalam additive mixture, menjawab Sub-RQ3, dan menyediakan data mentah untuk uji H3. E5 menjawab Sub-RQ4 sebagai diagnostik kegagalan.")
text = text.replace("| H3 | Not tested | Real-soundscape focal-bird corpus is outside the active design. | Not tested / out of scope | E4 is additive noise-profile sensitivity and is not used to accept or reject H3. |", f"| H3 | E4 raw + H3 analysis | mAP@10 retention swing across five habitat noise profiles | R1 swing {ALL['R1_generic_mean_swing']:.6f}; R2 swing {ALL['R2_bioacoustic_mean_swing']:.6f}; Δ={ALL['R1_minus_R2_effect']:.6f}, CI 95% [{ALL['ci95_low']:.6f}, {ALL['ci95_high']:.6f}]. | Supported | Additive mixture only; it does not assess naturally recorded birds in an ITERA soundscape. |")
text = text.replace("- H1, H2, H4, dan H5 didukung dalam desain additive ITERA-noise yang divalidasi.\n- H3 tentang real-soundscape domain shift **belum diuji dan di luar scope aktif**. Sub-RQ3 dibatasi pada sensitivitas profil noise aditif E4, sedangkan Sub-RQ4 dijawab oleh diagnostik E5.", "- H1, H2, H3, H4, dan H5 didukung dalam desain additive ITERA-noise yang divalidasi.\n- H3 didukung sebagai stabilitas retensi lintas profil noise lokasi: R2/BirdNET berayun lebih sempit daripada R1/PANNs pada seluruh SNR yang diuji. Sub-RQ3 dijawab oleh E4 dan Sub-RQ4 oleh diagnostik E5.")
text = text.replace(f"- E4 valid dan audit pendamping: `results/reproductions/E4_5sites_20261011T213404_350219Z` serta `results/reproductions/E4_audit_20261012T021801_989259Z`", f"- E4 valid, audit pendamping, dan analisis H3 read-only: `results/reproductions/E4_5sites_20261011T213404_350219Z`, `results/reproductions/E4_audit_20261012T021801_989259Z`, serta `{RUN.relative_to(ROOT).as_posix()}`")
results.write_text(text, encoding="utf-8")

write("paper/manuscript.md", f"""# Noise and Spectral Sensitivity of Frozen Audio Representations for Bioacoustic Similarity Retrieval under Controlled ITERA Field-Noise Mixtures in Indonesian Avifauna

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

R1/PANNs memiliki ayunan retensi rata-rata {ALL['R1_generic_mean_swing']:.3f}, sedangkan R2/BirdNET {ALL['R2_bioacoustic_mean_swing']:.3f}; perbedaannya {ALL['R1_minus_R2_effect']:.3f}, CI 95% [{ALL['ci95_low']:.3f}, {ALL['ci95_high']:.3f}] melalui paired bootstrap 10.000 kali. H3 didukung: BirdNET lebih stabil lintas lima profil noise lokasi pada empat SNR yang diuji.

## Batasan scope

H3 menguji stabilitas terhadap profil noise lokasi dalam *additive mixture*. Bank ITERA bebas spesies target dan digunakan sebagai noise; penelitian ini tidak meminta atau membutuhkan anotasi spesies target dari bank tersebut. Kesimpulan tidak mencakup jarak burung-mikrofon, propagasi, reverberasi, atau performa focal recording yang direkam langsung dalam soundscape ITERA.

Narasi hasil dan status hipotesis yang terkendali tersedia di `docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md` dan `docs/research/scope-reframe-2026-10-12.md`.
""")

# Short, direct document updates.
replace("docs/README.md", "Eksperimen E0–E5 memiliki artefak selesai/terverifikasi. E4 dibingkai sebagai sensitivitas profil noise dalam additive mixture; H3 tentang real-soundscape domain shift ditulis belum diuji dan di luar scope aktif. Lihat `research/scope-reframe-2026-10-12.md`.", "Eksperimen E0–E5 memiliki artefak selesai/terverifikasi. H3 diuji dari CSV mentah E4 sebagai stabilitas retensi lintas lima profil noise lokasi dan didukung; E4 tetap bukan uji rekaman burung in-situ. Lihat `research/scope-reframe-2026-10-12.md`.")
replace("paper/README.md", "Rujukan hasil ilmiah terkini: `docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md`. E4 dibingkai sebagai sensitivitas profil noise lokasi dalam additive mixture; H3 real-soundscape domain shift belum diuji.", "Rujukan hasil ilmiah terkini: `docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md`. E4 menguji sensitivitas profil noise lokasi dalam additive mixture; analisis H3 menunjukkan retensi R2 lebih stabil daripada R1 lintas lima lokasi.")
replace("Panduan_Komprehensif_Tugas_Akhir.md", "> **Scope aktif per 12 Oktober 2026:** penelitian menguji *controlled additive field-noise mixtures* dengan noise ITERA. E4 adalah sensitivitas profil noise lima lokasi; H3 mengenai real-soundscape domain shift ditulis **belum diuji**. Bank ITERA bebas spesies target sehingga anotasi spesies target tidak diperlukan.", f"> **Scope aktif per 12 Oktober 2026:** penelitian menguji *controlled additive field-noise mixtures* dengan noise ITERA. E4 menguji sensitivitas lima profil noise lokasi, dan H3 diuji sebagai stabilitas retensi lintas profil tersebut: R2/BirdNET lebih stabil daripada R1/PANNs (Δ ayunan = {ALL['R1_minus_R2_effect']:.3f}; CI 95% [{ALL['ci95_low']:.3f}, {ALL['ci95_high']:.3f}]). Bank ITERA bebas spesies target sehingga anotasi spesies target tidak diperlukan.")
replace("docs/research/scope-freeze.md", "E4 dibatasi sebagai sensitivitas profil noise lokasi ITERA dalam additive mixture. H3 real-soundscape domain shift belum diuji dan berada di luar scope aktif. Bank noise ITERA bebas spesies target; anotasi spesies target tidak diminta untuk E2/E4. Lihat `scope-reframe-2026-10-12.md`.", "E4 dibatasi sebagai sensitivitas profil noise lokasi ITERA dalam additive mixture. H3 diuji sebagai stabilitas retensi lintas lima profil noise lokasi, bukan real-soundscape domain shift. Bank noise ITERA bebas spesies target; anotasi spesies target tidak diminta untuk E2/E4. Lihat `scope-reframe-2026-10-12.md`.")
replace("docs/RESTART_STATUS.md", "> **Status historis sebelum DEC-15:** dokumen ini mencatat tahap restart sebelumnya. Scope aktif kini ada di `docs/research/scope-reframe-2026-10-12.md`: E4 adalah additive noise-profile sensitivity; H3 real-soundscape domain shift belum diuji.", "> **Status historis:** dokumen ini mencatat tahap restart sebelumnya. Scope aktif kini ada di `docs/research/scope-reframe-2026-10-12.md`: E4 adalah additive noise-profile sensitivity, dan H3 telah diuji sebagai stabilitas retensi lintas lima profil noise lokasi.")

# Decision log remains a living decision, so correct DEC-15 rather than append a contradictory record.
replace("docs/research/decision-log.md", "| **12 Okt 2026** | **DEC-15** | **Penyempitan Scope E4/H3** | Atas arahan pembimbing, E4 dibingkai sebagai sensitivitas profil noise lapangan ITERA dalam controlled additive mixture. H3 real-soundscape domain shift dinyatakan belum diuji dan di luar scope aktif; anotasi spesies target pada bank ITERA tidak diminta karena set noise bebas target. | Menyelaraskan judul, RQ, hipotesis, dan klaim dengan data yang tersedia tanpa mengubah artefak E0–E5. |", f"| **12 Okt 2026** | **DEC-15** | **Pembingkaian E4/H3** | E4 dibingkai sebagai sensitivitas profil noise lapangan ITERA dalam controlled additive mixture. H3 didefinisikan sebagai stabilitas ayunan retensi lintas profil tersebut dan diuji dari raw E4; anotasi spesies target pada bank ITERA tidak diminta karena set noise bebas target. | H3 didukung: ayunan R1−R2 = {ALL['R1_minus_R2_effect']:.6f}, CI 95% [{ALL['ci95_low']:.6f}, {ALL['ci95_high']:.6f}]. Klaim real-soundscape bird in-situ tetap di luar scope. |")

# Bimbingan documents
replace("Rencana-eksperimen-bimbingan/CURRENT_STATUS.md", "**Status ilmiah:** H1, H2, H4, dan H5 didukung dalam desain additive ITERA-noise; H3 tentang real-soundscape domain shift belum diuji dan di luar scope aktif.", "**Status ilmiah:** H1, H2, H3, H4, dan H5 didukung dalam desain additive ITERA-noise. H3 menguji stabilitas retensi lintas lima profil noise lokasi, bukan rekaman burung in-situ.")
replace("Rencana-eksperimen-bimbingan/CURRENT_STATUS.md", "H3 belum diuji karena desain aktif tidak membangun korpus focal-bird in-situ. E4 hanya membandingkan profil noise asli yang dicampur secara aditif; anotasi target-species pada bank noise ITERA tidak diperlukan.", f"H3 diuji dari raw E4: ayunan retensi R1 = {ALL['R1_generic_mean_swing']:.3f}, R2 = {ALL['R2_bioacoustic_mean_swing']:.3f}; Δ = {ALL['R1_minus_R2_effect']:.3f}, CI 95% [{ALL['ci95_low']:.3f}, {ALL['ci95_high']:.3f}]. E4 tetap hanya additive mixture; anotasi target-species pada bank noise ITERA tidak diperlukan.")
replace("Rencana-eksperimen-bimbingan/README.md", "E4 menggunakan pencampuran aditif dengan noise asli lima lokasi ITERA. E4 dibingkai sebagai sensitivitas profil noise lapangan; H3 tentang real-soundscape domain shift ditulis belum diuji dan berada di luar scope aktif.", "E4 menggunakan pencampuran aditif dengan noise asli lima lokasi ITERA. H3 diuji sebagai stabilitas ayunan retensi lintas profil noise: R2 lebih stabil daripada R1. Hasilnya tidak diklaim sebagai evaluasi burung yang direkam in-situ.")
replace("Rencana-eksperimen-bimbingan/minggu-3/README.md", "## Batasan yang wajib ditulis\n\nE4 menguji **sensitivitas terhadap profil noise lokasi dalam additive mixture**. Ini adalah scope aktif E4. H3 tentang real-soundscape domain shift ditulis belum diuji dan tidak dinilai dengan E4; bank ITERA bebas spesies target sehingga anotasi target-species tidak diperlukan.", f"## H3 — stabilitas profil habitat\n\nE4 menguji **sensitivitas terhadap profil noise lokasi dalam additive mixture**. H3 memakai raw E4 untuk membandingkan ayunan retensi: R1/PANNs = {ALL['R1_generic_mean_swing']:.6f}, R2/BirdNET = {ALL['R2_bioacoustic_mean_swing']:.6f}, selisih = {ALL['R1_minus_R2_effect']:.6f}, CI 95% [{ALL['ci95_low']:.6f}, {ALL['ci95_high']:.6f}]. H3 didukung. Bank ITERA bebas spesies target sehingga anotasi target-species tidak diperlukan.\n\n- [Tabel H3](../../results/tables/24_h3_habitat_profile_stability.csv)\n- [Grafik H3](../../results/figures/15_h3_habitat_retention_stability.png)\n- [Run analisis H3](../../{RUN.relative_to(ROOT).as_posix()}/)")
replace("Rencana-eksperimen-bimbingan/minggu-4/README.md", "Bootstrap berpasangan menggunakan 10.000 iterasi, seed 20261012, dan unit resampling query. Uji yang tersedia mencakup H1, H2, H4, dan H5.", "Bootstrap berpasangan menggunakan 10.000 iterasi, seed 20261012, dan unit resampling query. Uji yang tersedia mencakup H1–H5; H3 dihitung secara terpisah dari raw E4 sebagai perbandingan ayunan retensi lintas habitat.")
replace("Rencana-eksperimen-bimbingan/minggu-4/README.md", "| H3 | Belum diuji dan di luar scope aktif: E4 adalah additive noise-profile sensitivity, bukan real-soundscape domain-shift validation. |", f"| H3 | Didukung: ayunan retensi R1 = {ALL['R1_generic_mean_swing']:.6f}, R2 = {ALL['R2_bioacoustic_mean_swing']:.6f}; Δ = {ALL['R1_minus_R2_effect']:.6f}, CI 95% [{ALL['ci95_low']:.6f}, {ALL['ci95_high']:.6f}]. |")
replace("Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md", "**Framing aktif:** E4 adalah uji sensitivitas terhadap profil noise lokasi nyata ITERA dalam additive mixture. H3 tentang real-soundscape domain shift belum diuji dan di luar scope aktif. Karena bank ITERA bebas spesies target, anotasi target-species tidak diperlukan.", f"**Framing aktif:** E4 adalah uji sensitivitas terhadap profil noise lokasi nyata ITERA dalam additive mixture. H3 diuji sebagai stabilitas retensi lintas lima profil: ayunan R1 = {ALL['R1_generic_mean_swing']:.6f}, R2 = {ALL['R2_bioacoustic_mean_swing']:.6f}, Δ = {ALL['R1_minus_R2_effect']:.6f}, CI 95% [{ALL['ci95_low']:.6f}, {ALL['ci95_high']:.6f}]. Karena bank ITERA bebas spesies target, anotasi target-species tidak diperlukan.")
replace("Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md", "Bootstrap berpasangan memakai 10.000 iterasi dan seed 20261012. H1, H2, H4, dan H5 didukung di bawah desain additive-noise yang tervalidasi. H3 ditulis belum diuji dan di luar scope aktif; E4 tidak dipakai untuk menerima atau menolak H3.", "Bootstrap berpasangan memakai 10.000 iterasi dan seed 20261012. H1–H5 didukung di bawah desain additive-noise yang tervalidasi. H3 dihitung read-only dari raw E4 dan menunjukkan ayunan retensi R2 lebih sempit daripada R1.")
replace("Rencana-eksperimen-bimbingan/CATATAN_PROGRES_BIMBINGAN.md", "| H3 | Belum diuji / di luar scope aktif | E4 bukan real-soundscape validation |", "| H3 | Didukung: R2 memiliki ayunan retensi lintas lokasi lebih sempit daripada R1 | Additive mixture, bukan bird recording in-situ |")

print(f"Updated H3 documentation from {RUN.relative_to(ROOT)}")
