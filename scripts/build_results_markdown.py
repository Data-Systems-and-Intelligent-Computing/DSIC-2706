"""Build the current evidence-linked results markdown from validated artifacts."""
from __future__ import annotations

import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "RESULTS_RQ_HYPOTHESES_2026-10-12.md"
E0 = ROOT / "results/reproductions/E0_20261011_202557"
EDA = ROOT / "results/reproductions/EDA_20261011_202714"
E2 = ROOT / "results/reproductions/E2_controlled_20261012T021600_897497Z"
E3 = ROOT / "results/reproductions/E3_open_set_20261012T022548_802536Z"
E4 = ROOT / "results/reproductions/E4_5sites_20261011T213404_350219Z"
E5 = ROOT / "results/reproductions/E5_diagnostics_20261012T091512_868500Z"
STAT = ROOT / "results/reproductions/STATISTICS_RQ_MATRIX_20261012T092924_809804Z"
H3 = sorted((ROOT / "results" / "reproductions").glob("H3_habitat_profile_stability_*"))[-1]


def table(frame: pd.DataFrame, columns: list[str] | None = None, digits: int = 4) -> str:
    if columns is not None:
        frame = frame[columns]
    frame = frame.copy()
    for col in frame.columns:
        if pd.api.types.is_float_dtype(frame[col]):
            frame[col] = frame[col].map(lambda value: "" if pd.isna(value) else f"{value:.{digits}f}")
    values = frame.fillna("").astype(str)
    header = "| " + " | ".join(values.columns) + " |"
    divider = "| " + " | ".join("---" for _ in values.columns) + " |"
    body = "\n".join("| " + " | ".join(row) + " |" for row in values.itertuples(index=False, name=None))
    return "\n".join([header, divider, body])


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> None:
    e0_summary = pd.read_csv(E0 / "tables/summary.csv")
    eda_meta = json.loads((EDA / "metadata.json").read_text(encoding="utf-8"))
    e2 = pd.read_csv(E2 / "tables/e2_snr_robustness.csv")
    e2 = e2.assign(condition=pd.Categorical(e2.condition, ["Clean", "SNR_20dB", "SNR_10dB", "SNR_0dB", "SNR_-5dB"], ordered=True)).sort_values(["representation", "condition"])
    threshold = pd.read_csv(E3 / "tables/frozen_thresholds.csv")
    transfer = pd.read_csv(E3 / "tables/threshold_transfer.csv")
    transfer = transfer[transfer.condition.isin(["Clean", "SNR_-5dB"])].sort_values(["representation", "snr_db"], ascending=[True, False])
    e4 = pd.read_csv(STAT / "tables/e4_habitat_descriptive.csv").pivot(index="representation", columns="habitat", values="map10").reset_index()
    e5_summary = pd.read_csv(E5 / "tables/failure_mode_summary.csv")
    e5_rollup = e5_summary.groupby(["source_experiment", "representation", "failure_mode"], as_index=False).n_queries.sum()
    matrix = pd.read_csv(ROOT / "results/tables/27_rq_hypothesis_matrix_current.csv")
    bootstrap = pd.read_csv(STAT / "tables/paired_bootstrap_results.csv")
    h3 = pd.read_csv(H3 / "tables/h3_stability_summary.csv")
    h3_primary = h3.loc[h3.analysis_scope.eq("mean_over_4_SNR_levels")].copy()
    h3_row = h3_primary.iloc[0]
    h3_mask = matrix["item"].eq("H3")
    if h3_mask.sum() == 1:
        matrix.loc[h3_mask, "experiment"] = "E4 raw + H3 analysis"
        matrix.loc[h3_mask, "metric"] = "mAP@10 relative-retention swing across five habitat profiles"
        matrix.loc[h3_mask, "artifact"] = "24_h3_habitat_profile_stability.csv; 26_h3_bootstrap_distribution.csv"
        matrix.loc[h3_mask, "result"] = (f"R1 swing {h3_row['R1_generic_mean_swing']:.6f}; R2 swing {h3_row['R2_bioacoustic_mean_swing']:.6f}; "
                                         f"Δ={h3_row['R1_minus_R2_effect']:.6f}; CI 95% [{h3_row['ci95_low']:.6f}, {h3_row['ci95_high']:.6f}].")
        matrix.loc[h3_mask, "conclusion"] = "Supported for retention stability"
        matrix.loc[h3_mask, "limitation"] = "Exploratory analysis; the high/low-frequency mechanism and in-situ bird soundscapes were not tested."
    provenance = pd.read_csv(STAT / "tables/experiment_provenance_status.csv")
    e1_rows = []
    for rep, name in [("R0", "E1_R0_20261011_175321"), ("R1", "E1_R1_cache_20261012T021032_566409Z"), ("R2", "E1_R2_cache_20261012T021034_128124Z"), ("R3", "E1_R3_cache_20261012T021035_119528Z")]:
        row = json.loads((ROOT / "results" / "reproductions" / name / "metadata.json").read_text(encoding="utf-8"))["summary"].copy()
        row["representation"] = rep
        e1_rows.append(row)
    e1_summary = pd.DataFrame(e1_rows).sort_values("representation")

    e2_table = e2.pivot(index="representation", columns="condition", values="mAP@10").reset_index()
    e2_recall = e2.pivot(index="representation", columns="condition", values="Recall@10").reset_index()
    e0_clean = e0_summary.set_index("metric").value.to_dict()
    text = f'''# Hasil Terverifikasi E0–E5, RQ, dan Hipotesis

Dokumen ini adalah ringkasan hasil dari artefak eksperimen aktif yang tervalidasi di repository lokal. Seluruh nilai di bawah berasal dari data asli pada `data/`, bukan data sintetis. Run lama yang terdampak imputasi XC42472 berada di arsip dan tidak dipakai sebagai bukti.

## Dataset dan status provenance

Partisi aktif terdiri dari 673 Gallery, 311 Query bersih, dan 232 Calibration. E3 memakai 233 unknown calibration serta 310 unknown test. Tabel status berikut merujuk artefak konkret dan tidak mengubahnya.

{table(provenance, ["experiment", "status", "artifact", "limitation"])}

## E0 — audit preprocessing

E0 adalah audit 100 rekaman aktif yang dipilih deterministik. E0 bukan retrieval dan bukan R0.

{table(e0_summary, ["metric", "value"])}

Temuan: seluruh 100 audio yang diperiksa menghasilkan 160.000 sampel terhingga setelah preprocessing pada 32 kHz dan durasi 5 detik. Ada 6 ketidakcocokan ekstensi/container dalam sampel, tetapi tidak ada kegagalan decoder. Lihat `{rel(E0 / 'tables/per_recording.csv')}` untuk semua baris audit.

## EDA — kondisi data fisik

Inventaris EDA mencatat {eda_meta['physical_audio_count']} audio fisik, {eda_meta['manifest_target_count']} target aktif, {eda_meta['manifest_noise_count']} audio noise ITERA, dan {eda_meta['manifest_open_set_rows']} item unknown/open-set. Tidak ada error decode soundfile; terdapat {eda_meta['extension_container_mismatches']} ketidakcocokan ekstensi/container dan {eda_meta['unreferenced_physical_audio']} audio fisik belum dirujuk oleh manifes yang diaudit. Ini adalah temuan audit, bukan alasan otomatis untuk menghapus file.

Notebook EDA membangun ulang distribusi spesies, durasi, sampling rate, lokasi noise, waveform, dan mel-spektrogram langsung dari audio fisik.

## E1 — clean retrieval

R0 adalah **baseline MFCC**, bukan preprocessing. Preprocessing menyiapkan audio; R0 mengubah audio siap tersebut menjadi vektor MFCC untuk retrieval.

{table(e1_summary, ['representation','mean_top1','MRR','mAP@10','Recall@10','Precision@10'])}

R2 mempunyai performa bersih tertinggi. R1–R3 dimaterialisasi dari cache clean yang divalidasi dengan hash manifes, urutan ID, dimensi, nilai hingga, dan versi kontrol R3; artefaknya tidak diklaim sebagai run historis.

## E2 — penurunan terkontrol oleh noise ITERA

E2 menggunakan pencampuran noise lapangan ITERA fisik pada SNR +20, +10, 0, dan −5 dB. Terdapat 20 raw CSV, masing-masing berisi 311 query yang sejajar dengan manifes dan menyimpan audit noise/seed/SNR aktual.

### mAP@10

{table(e2_table, digits=6)}

### Recall@10

{table(e2_recall, digits=6)}

Pada −5 dB, retensi mAP@10 adalah R0 33,45%, R1 48,96%, R2 75,88%, dan R3 100%. Retensi R3 tidak diinterpretasikan sebagai ketahanan audio karena R3 merupakan kontrol ID-deterministik.

## E3 — threshold open-set yang dibekukan

Threshold ditentukan hanya dari calibration bersih melalui ROC Youden J, lalu dibekukan sebelum evaluasi query dan unknown test.

{table(threshold, ['representation','frozen_tau','calibration_auroc','calibration_youden_j','calibration_precision','calibration_recall','calibration_fpr'], digits=6)}

### Perubahan titik operasi: Clean ke −5 dB

{table(transfer, ['representation','condition','Recall_at_tau','False_Positive_Rate','AUROC','AUPRC'], digits=6)}

Untuk R0–R2, recall known-set di threshold beku turun pada −5 dB. False-positive rate unknown justru turun pada kondisi ini; H4 didukung melalui penurunan recall, bukan lonjakan false accept.

## E4 — sensitivitas profil noise lintas habitat

E4 tervalidasi sebagai 320 snapshot kondisi additive mixture. E4 memakai rekaman noise asli dari lima habitat/lokasi ITERA yang dicampur ke query focal; E4 **bukan** rekaman burung yang dibuat langsung dalam real soundscape.

### mAP@10 pada −5 dB menurut habitat/lokasi

{table(e4, digits=6)}

E4 raw menyimpan `top1_match` dan `max_score`. Ia tidak menyimpan identitas Top-1, skor kelas benar, skor pesaing, margin kelas, atau fitur akustik dari audio noisy.

### H3 — stabilitas retensi lintas profil lokasi

H3 membandingkan ayunan retensi `mAP@10` lintas lima lokasi (`maksimum − minimum`), dirata-ratakan atas empat segmen noise per lokasi. Analisis hanya membaca raw E4 dan memakai paired bootstrap 10.000 kali pada 311 query yang sama.

{table(h3_primary, ['R1_generic_mean_swing','R2_bioacoustic_mean_swing','R1_minus_R2_effect','ci95_low','ci95_high','supports_H3_at_alpha_0_05'], digits=6)}

H3 didukung karena CI 95% selisih ayunan R1−R2 seluruhnya positif. Detail: `{rel(H3)}` dan `results/tables/24_h3_habitat_profile_stability.csv`.

Uji H3 ditambahkan setelah E4 selesai dan bersifat eksploratif. Hubungan sebab akibat antara distorsi frekuensi tinggi/rendah dan hasil retrieval belum diuji secara langsung.

## E5 — taksonomi kegagalan retrieval

E5 memakai threshold E3 yang beku. E2 menyediakan semua field ranking dan direkonstruksi secara deterministik untuk centroid, bandwidth, dan RMS. Pada E4, field yang tidak pernah tersedia tetap ditandai tidak tersedia dan tidak direka ulang.

{table(e5_rollup, ['source_experiment','representation','failure_mode','n_queries'])}

E5 menyediakan 120 contoh kegagalan E2 yang dipilih secara terstratifikasi dengan seed tetap, grafik moda kegagalan, margin terhadap threshold, dan fitur spektral. Artefak lengkap: `{rel(E5)}`.

## Jawaban RQ dan hipotesis

Dokumen otoritatif repository adalah `docs/research/rq.md` dan `docs/research/hypotheses.md`. H3 menguji stabilitas retensi lintas profil noise lokasi melalui E4; Sub-RQ4 tetap dijawab oleh E5. E4 tidak dipakai untuk klaim performa focal recording yang direkam langsung dalam real soundscape ITERA.

{table(matrix, ['item','experiment','metric','result','conclusion','limitation'])}

## Statistik inferensial

Seluruh perbandingan memakai paired bootstrap 10.000 iterasi, seed 20261012, dengan unit resampling query berpasangan. Nilai `p_value_bootstrap` adalah estimasi empiris dari bootstrap sesuai arah hipotesis yang tercatat di kolom `alternative`.

{table(bootstrap, ['test_id','n_paired','effect_mean_difference','retention_a','retention_b','ci_95_low','ci_95_high','p_value_bootstrap','statistical_result'], digits=6)}

## Kesimpulan yang aman saat ini

- R2/BirdNET memberi retrieval terbaik pada E1 dan seluruh level SNR E2 yang diuji.
- H1, H2, H3, H4, dan H5 didukung dalam desain additive ITERA-noise yang divalidasi.
- H3 didukung: R2/BirdNET mempunyai ayunan retensi lintas lima profil noise yang lebih sempit daripada R1/PANNs; Sub-RQ4 dijawab oleh E5.
- Kesimpulan E4 terbatas pada perbedaan profil noise lapangan yang dicampur secara aditif. Ia tidak membuktikan efek jarak, propagasi, absorpsi, atau reverberasi.

## Artefak utama

- E2: `{rel(E2)}`
- E3: `{rel(E3)}`
- E4 valid, audit pendamping, dan H3 read-only: `{rel(E4)}`, `results/reproductions/E4_audit_20261012T021801_989259Z`, serta `{rel(H3)}`
- E5: `{rel(E5)}`
- Matriks/provenance/statistik: `{rel(STAT)}`
'''
    OUT.write_text(text, encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
