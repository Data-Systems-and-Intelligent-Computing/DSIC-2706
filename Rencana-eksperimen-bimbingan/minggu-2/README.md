# Minggu 2 — Derau ITERA dan E2 Controlled Noise

**Tujuan:** mengukur penurunan retrieval saat query yang sama dicampur dengan rekaman noise lapangan ITERA pada SNR yang terkontrol.

## Bank noise lapangan

Bank noise berisi 1.799 rekaman AudioMoth ITERA dari lima lokasi: Embung F, Gedung F, Kebun Raya, Masjid At-Tanwir, dan Sekitar GKU 1. Noise ini adalah rekaman fisik, bukan pink noise sintetis.

- Lokasi dan metadata: [itera_noise_manifest.csv](../../data/manifests/itera_noise_manifest.csv)
- Folder audio: [data/itera_noise](../../data/itera_noise/)
- Distribusi lokasi: [EDA noise locations](../../results/figures/06_eda_noise_locations.png)
- Spektrogram profil noise: [EDA noise profiles](../../results/figures/05_eda_itera_noise_spectrogram_profiles.png)
- Kode mixing: [src/mix_noise.py](../../src/mix_noise.py)
- Konfigurasi E2: [configs/experiments.yaml](../../configs/experiments.yaml)

## Desain E2

Setiap 311 query clean dipasangkan secara deterministik dengan noise ITERA pada Clean, +20, +10, 0, dan −5 dB. Gallery tetap sama. Metrik yang dicatat adalah Top-1, MRR, mAP@10, Recall@10, dan Precision@10. Dua puluh raw CSV menyimpan hasil per-query untuk empat representasi dan lima kondisi.

- Notebook: [05_E2_Controlled_Noise.ipynb](../../notebooks/05_E2_Controlled_Noise.ipynb)
- Kode sumber: [run_e2_controlled_noise.py](../../scripts/run_e2_controlled_noise.py)
- Run sumber: [E2 controlled](../../results/reproductions/E2_controlled_20261012T021600_897497Z/)
- Tabel agregat: [E2 SNR robustness](../../results/tables/11_e2_snr_robustness.csv)
- Gambar mAP@10: [E2 robustness curve](../../results/figures/08_e2_snr_robustness_map10.png)

## Hasil pada −5 dB

| Representasi | mAP@10 Clean | mAP@10 −5 dB | Retensi |
|---|---:|---:|---:|
| R0 | 0,0694 | 0,0232 | 33,45% |
| R1 | 0,1763 | 0,0863 | 48,96% |
| R2 | 0,6367 | 0,4832 | 75,88% |
| R3 | 0,0211 | 0,0211 | 100,00%* |

\*R3 adalah kontrol ID-deterministik; retensinya tidak diartikan sebagai ketahanan audio.

## Interpretasi dan lanjut

R2 mempunyai mAP@10 tertinggi pada semua SNR yang diuji dan retensi −5 dB paling tinggi di antara representasi audio. Bukti statistik untuk H1 dan H2 tersedia di [paired bootstrap](../../results/tables/22_statistics_paired_bootstrap.csv). Minggu berikutnya memakai data E2 untuk memeriksa threshold terbuka E3 dan variasi profil noise E4.
