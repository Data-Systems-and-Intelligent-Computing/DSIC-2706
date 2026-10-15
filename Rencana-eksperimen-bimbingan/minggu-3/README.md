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

Pada −5 dB, recall known-set turun untuk R0–R2; misalnya R2 dari 0,6045 menjadi 0,2540. FPR unknown tidak meningkat pada data ini. Penurunan recall sesuai salah satu klausul H4 asli; interpretasi reformulasi setelah hasil tersedia bersifat eksploratif. Recall ini adalah penerimaan known-set, bukan ketepatan spesies Top-1.

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

## H3 — analisis eksploratif sensitivitas profil lokasi

E4 menguji sensitivitas profil noise lokasi dalam additive mixture. Analisis lama memakai ayunan retensi rata-rata lima lokasi: R1 = 0,240111, R2 = 0,048607. Revisi 15 Oktober menambahkan ayunan mAP@10 absolut serta subset tanpa Kebun Raya.

Rata-rata ayunan absolut lima lokasi R1 = 0,042324 dan R2 = 0,030949; CI selisih [−0,003993; 0,022140] mencakup nol. Tanpa Kebun Raya, selisih rata-rata ayunan relatif turun dari 0,191504 menjadi 0,069097. Pada −5 dB tanpa Kebun Raya, ayunan relatif R1 = 0,065937 dan R2 = 0,083724, dengan CI selisih mencakup nol. Karena itu R2 tidak dinyatakan berayun lebih sempit di semua SNR.

H3 hasil reformulasi adalah eksploratif; H3 asli mengenai real-soundscape belum diuji. Biofoni serangga dan distorsi frekuensi masih dugaan. Status bebas vokalisasi target seluruh bank noise belum dibuktikan secara independen.

- [Hasil sensitivitas H3 terkini](../../results/reproductions/H3_sensitivity_20261015/tables/h3_swing_summary.csv)
- [Riwayat rumusan H3/H4](../../docs/research/hypotheses.md)
- [Catatan revisi utama](../../docs/REVISION_SUPERVISOR_2026-10-15.md)
- [Tabel H3 historis 12 Oktober](../../results/tables/24_h3_habitat_profile_stability.csv)
