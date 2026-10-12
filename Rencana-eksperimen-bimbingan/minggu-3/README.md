# Minggu 3 — E3 Open Set dan E4 Sensitivitas Profil Noise

**Tujuan:** membekukan threshold dari calibration terpisah untuk E3, lalu mengukur perbedaan profil noise ITERA lintas lokasi pada E4.

## E3 — threshold open set yang dibekukan

Threshold τ* dioptimalkan hanya pada 232 target calibration dan 233 unknown calibration melalui ROC Youden J. Setelah itu threshold dibekukan dan dipakai pada 311 target test dan 310 unknown test. Hal ini mencegah test-set tuning.

| Representasi | τ* | AUROC calibration | Recall calibration | FPR calibration |
|---|---:|---:|---:|---:|
| R0 | 0,995752 | 0,533225 | 0,193966 | 0,094421 |
| R1 | 0,897416 | 0,709801 | 0,745690 | 0,373391 |
| R2 | 0,702785 | 0,759953 | 0,590517 | 0,171674 |
| R3 | 0,488838 | 0,545194 | 0,366379 | 0,278970 |

- Notebook: [06_E3_Open_Set_Threshold.ipynb](../../notebooks/06_E3_Open_Set_Threshold.ipynb)
- Kode: [run_e3_open_set.py](../../scripts/run_e3_open_set.py), [calibrate_threshold.py](../../src/calibrate_threshold.py)
- Manifes unknown: [unknown_open_set_manifest.csv](../../data/manifests/unknown_open_set_manifest.csv)
- Run sumber: [E3](../../results/reproductions/E3_open_set_20261012T022548_802536Z/)
- Threshold final: [frozen thresholds](../../results/tables/12_e3_frozen_thresholds.csv)
- Transfer test: [threshold transfer](../../results/tables/13_e3_threshold_transfer.csv)
- Gambar: [E3 threshold transfer](../../results/figures/09_e3_threshold_transfer_recall.png)

Pada −5 dB, recall known-set turun untuk R0–R2; misalnya R2 dari 0,6045 menjadi 0,2540. FPR unknown tidak meningkat pada data ini. H4 didukung melalui penurunan recall known-set, bukan klaim kenaikan false accept.

## E4 — profil noise lintas lima lokasi ITERA

E4 memakai noise asli dari Embung F, Gedung F, Kebun Raya, Masjid At-Tanwir, dan Sekitar GKU 1 untuk additive mixture pada query focal. Run tervalidasi menyimpan 320 snapshot kondisi dan 324 baris tabel komparatif.

- Notebook: [07_E4_Habitat_Noise_Sensitivity.ipynb](../../notebooks/07_E4_Habitat_Noise_Sensitivity.ipynb)
- Run sumber: [E4 five sites](../../results/reproductions/E4_5sites_20261011T213404_350219Z/)
- Audit run: [E4 audit](../../results/reproductions/E4_audit_20261012T021801_989259Z/)
- Tabel: [E4 domain shift](../../results/tables/14_e4_domain_shift.csv)
- Gambar: [E4 habitat sensitivity](../../results/figures/10_e4_noise_profile_sensitivity.png)

### mAP@10 pada −5 dB

| Representasi | Embung F | Gedung F | Kebun Raya | Masjid At-Tanwir | Sekitar GKU 1 |
|---|---:|---:|---:|---:|---:|
| R0 | 0,028389 | 0,019348 | 0,022228 | 0,025731 | 0,017891 |
| R1 | 0,087315 | 0,090465 | 0,048673 | 0,090600 | 0,083264 |
| R2 | 0,503990 | 0,454128 | 0,444612 | 0,502504 | 0,454732 |
| R3 | 0,021141 | 0,021141 | 0,021141 | 0,021141 | 0,021141 |

## H3 — stabilitas profil habitat

E4 menguji **sensitivitas terhadap profil noise lokasi dalam additive mixture**. H3 memakai raw E4 untuk membandingkan ayunan retensi: R1/PANNs = 0.240111, R2/BirdNET = 0.048607, selisih = 0.191504, CI 95% [0.152203, 0.241969]. H3 didukung. Bank ITERA bebas spesies target sehingga anotasi target-species tidak diperlukan.

- [Tabel H3](../../results/tables/24_h3_habitat_profile_stability.csv)
- [Grafik H3](../../results/figures/15_h3_habitat_retention_stability.png)
- [Run analisis H3](../../results/reproductions/H3_habitat_profile_stability_20261012T141344_312163Z/)
