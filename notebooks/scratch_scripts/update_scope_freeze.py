import pandas as pd
from pathlib import Path

freeze_path = Path(r"D:\FILE AND TASK\TA\data\manifests\species_freeze.csv")
split_path = Path(r"D:\FILE AND TASK\TA\data\manifests\dataset_split.csv")
scope_path = Path(r"D:\FILE AND TASK\TA\docs\research\scope-freeze.md")

freeze = pd.read_csv(freeze_path)
split = pd.read_csv(split_path)

table_rows = []
for idx, row in freeze.iterrows():
    sp_k = row['species_key']
    sci_n = row['scientific_name']
    com_n = row['common_name']
    n_k = row['n_klip']
    n_a = row['n_author']
    r_m = row['rating_median']
    table_rows.append(f"| {idx+1} | `{sp_k}` | *{sci_n}* | {com_n} | {n_k} | {n_a} | {r_m:.1f} |")

table_str = "\n".join(table_rows)

content = f"""# Pembekuan Ruang Lingkup (Scope Freeze) — DSIC-2706

Dokumen ini mencatat batasan ruang lingkup taksonomi, pra-pemrosesan, dan parameter pengujian untuk Tugas Akhir DSIC-2706.

---

## 1. Taksonomi Target (20 Spesies Burung Neotropis Pantanal)

### Amandemen Resmi Bertanggal (Versi 3.0 — 12 September 2026 / Keputusan Kedua)
Berdasarkan audit Gate 1 tanggal 12 September 2026 dan keputusan pembimbing (DEC-09), ruang lingkup dataset utama dialihkan ke **BirdCLEF+ 2026 (`train_audio`)** dengan memfilter taksa burung (*Aves*) koleksi Xeno-Canto berkategori rating >= 3.0 serta memiliki diversitas perekam tinggi ($N_{{\\text{{author}}}} \\ge 3$ dan $N_{{\\text{{klip}}}} \\ge 20$).

Daftar resmi **20 spesies burung target** dengan total **4.351 rekaman audio** terkelola:

| No | Spesies Kunci | Nama Ilmiah | Nama Umum (Inggris) | Jumlah Klip | Jumlah Author | Median Rating |
| :-: | :--- | :--- | :--- | :-: | :-: | :-: |
{table_str}
| **Total** | **20 Spesies** | | | **5.426 Klip Kandidat** | **629 Author Global** | **4.0** |

#### Distribusi Partisi Dataset Split (`data/manifests/dataset_split.csv`):
- **Galeri (*Gallery Bank*):** 3.653 rekaman (377 author independen).
- **Kueri Bersih (*Query Clean*):** Tepat 200 rekaman (20 spesies x 10 kueri per spesies; 68 author independen).
- **Subset Kalibrasi (*Calibration*):** 498 rekaman (95 author independen).
- **Status Kebocoran Perekam:** **Strict Global Author-Disjoint** (0 author tumpang tindih antara Galeri, Kueri, maupun Kalibrasi).

---

### Catatan Historis Ruang Lingkup Sebelumnya
- **Versi 2.0 (07 September 2026):** 16 taksa burung Sumatera (416 rekaman, kurasi manual Xeno-Canto). Dibatalkan oleh audit Gate 1 (12 September 2026) karena kelangkaan data kueri independen ($n=14$), kebocoran perekam (C-04), dan ketergantungan derau sintetis (M-05).
- **Versi 1.0 (Draf Awal):** 16 spesies kosmopolitan umum (digantikan oleh Versi 2.0).

---

## 2. Parameter Pra-pemrosesan Audio (Tetap Dibekukan)
- Laju Sampel (*Sample Rate*): **32.000 Hz** (mono).
- Durasi Segmen: **5.0 detik** (160.000 sampel).
- Seleksi Jendela: **Energi RMS tertinggi (*Top-energy sliding window*)**.
- Normalisasi Energi: **RMS target 0.05** dengan pembatasan puncak kliping <= 1.0.

---

## 3. Tingkat Degradasi Derau Terkontrol (Tetap Dibekukan)
Tingkat degradasi derau aditif dibekukan pada 5 level:
1. **Clean** (SNR = inf)
2. **SNR 20 dB** (Derau ringan)
3. **SNR 10 dB** (Derau sedang)
4. **SNR 0 dB** (Derau berat / sinyal sebanding derau)
5. **SNR -5 dB** (Derau ekstrem / derau melebihi sinyal)

---

## 4. Peran Baru Rekaman AudioMoth Kampus ITERA
Sesuai audit keputusan kedua, rekaman AudioMoth ITERA **tidak lagi menjadi validasi retrieval spesies**, melainkan murni dipersempit menjadi:
1. **Bank derau lingkungan nyata (E2):** Segmen *background-only* bebas vokalisasi burung dari 3 tipe lokasi (Embung, Arboretum, Antropogenik) pada 2 waktu (*daypart*).
2. **Sampel negatif open-set (E3):** Sebagai data uji negatif jenis *pure background*.
"""

scope_path.write_text(content.strip(), encoding="utf-8")
print("Updated scope-freeze.md to Version 3.0 successfully.")
