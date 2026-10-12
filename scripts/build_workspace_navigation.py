"""Create non-destructive navigation indexes for the complete TA workspace."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def csv_count(path: Path) -> int:
    with path.open(encoding='utf-8-sig', newline='') as handle:
        return max(sum(1 for _ in csv.reader(handle)) - 1, 0)


def write(path: Path, content: str) -> None:
    path.write_text(content.strip() + '\n', encoding='utf-8')

# Data is indexed only; no audio, manifests, or caches are modified.
data_rows = [
    ('known_active_split', 'data/manifests/dataset_split.csv', csv_count(ROOT / 'data/manifests/dataset_split.csv'), '673 gallery + 311 query_clean + 232 calibration'),
    ('unknown_open_set', 'data/manifests/unknown_open_set_manifest.csv', csv_count(ROOT / 'data/manifests/unknown_open_set_manifest.csv'), '233 calibration + 310 test negative controls'),
    ('itera_noise', 'data/manifests/itera_noise_manifest.csv', csv_count(ROOT / 'data/manifests/itera_noise_manifest.csv'), 'Physical AudioMoth ITERA recordings'),
    ('indonesia_species_freeze', 'data/manifests/indonesia_species_freeze.csv', csv_count(ROOT / 'data/manifests/indonesia_species_freeze.csv'), 'Frozen target species list'),
]
with (ROOT / 'data/dataset_registry.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.writer(handle)
    writer.writerow(['dataset_role', 'manifest', 'rows', 'note'])
    writer.writerows(data_rows)
write(ROOT / 'data/README.md', '''# Data

Folder ini menyimpan data asli dan manifes aktif. Audio tidak dipindahkan atau diubah oleh indeks ini.

| Peran | Lokasi utama | Jumlah |
|---|---|---:|
| Known-set target | `xeno_canto_indonesia/` dan `manifests/dataset_split.csv` | 1.216 baris split aktif |
| Unknown open-set | `xeno_canto_indonesia_unknowns/` dan `manifests/unknown_open_set_manifest.csv` | 543 kontrol negatif |
| Derau lapangan | `itera_noise/` dan `manifests/itera_noise_manifest.csv` | 1.799 rekaman |

`dataset_registry.csv` memberi indeks ringkas setiap manifes aktif. Inventaris fisik terperinci berada di `results/tables/07_eda_physical_audio_inventory.csv`.
''')

# Checkpoints are catalogued but never changed.
checkpoint_rows = [
    ('PANNs CNN14', 'Cnn14_mAP=0.431.pth', (ROOT / 'checkpoints/Cnn14_mAP=0.431.pth').stat().st_size, 'R1 generic deep audio representation'),
    ('BirdNET V2.4', 'BirdNET_GLOBAL_6K_V2.4_Model_FP32.onnx', (ROOT / 'checkpoints/BirdNET_GLOBAL_6K_V2.4_Model_FP32.onnx').stat().st_size, 'R2 domain-specific bioacoustic representation'),
]
with (ROOT / 'checkpoints/model_registry.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.writer(handle)
    writer.writerow(['model', 'file', 'bytes', 'experiment_role'])
    writer.writerows(checkpoint_rows)
write(ROOT / 'checkpoints/README.md', '''# Checkpoints

Model beku yang dipakai representasi R1 dan R2 dicatat dalam `model_registry.csv`.

Berkas checkpoint tidak diubah atau disalin oleh proses audit, notebook, maupun registri proyek. Cache embedding tervalidasi berada di `results/features/` dan provenance-nya tercatat dalam metadata E1.
''')

active_runs = {
    'schema': 'active_runs_v1',
    'policy': 'Indexes only. Results under results/reproductions are immutable source artifacts.',
    'runs': {
        'E0': 'results/reproductions/E0_20261011_202557',
        'EDA': ['results/reproductions/EDA_20261011_202714', 'results/reproductions/EDA_visuals_20261012T133209_032622Z'],
        'E1': ['results/reproductions/E1_R0_20261011_175321', 'results/reproductions/E1_R1_cache_20261012T021032_566409Z', 'results/reproductions/E1_R2_cache_20261012T021034_128124Z', 'results/reproductions/E1_R3_cache_20261012T021035_119528Z'],
        'E2': 'results/reproductions/E2_controlled_20261012T021600_897497Z',
        'E3': 'results/reproductions/E3_open_set_20261012T022548_802536Z',
        'E4': ['results/reproductions/E4_5sites_20261011T213404_350219Z', 'results/reproductions/H3_habitat_profile_stability_20261012T141344_312163Z'],
        'E5': 'results/reproductions/E5_diagnostics_20261012T091512_868500Z',
        'statistics': 'results/reproductions/STATISTICS_RQ_MATRIX_20261012T092924_809804Z',
    },
}
(ROOT / 'configs/active_runs.json').write_text(json.dumps(active_runs, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
write(ROOT / 'configs/README.md', '''# Configurations

YAML membekukan parameter audio, dataset, representasi, eksperimen, dan ambang.

`active_runs.json` adalah indeks run terkini untuk E0–E5 dan statistik. Ia hanya menunjuk run sumber di `results/reproductions/`; tidak mengubah parameter atau hasil eksperimen.
''')

write(ROOT / 'scripts/README.md', '''# Scripts

Folder ini menyimpan kode sumber runner dan pembangun indeks. Notebook di `notebooks/` memuat kode eksperimen yang sama sebagai code cell agar dapat dipelajari langsung.

Runner aktif yang sudah menghasilkan artefak tervalidasi:

- `run_e0_preprocessing_verification.py`, `run_eda_formal.py`, `run_e1_clean_r0.py`
- `materialize_e1_from_cache.py`, `run_e2_controlled_noise.py`, `run_e3_open_set.py`
- `run_e5_diagnostics.py`, `run_statistics_and_rq_matrix.py`, `run_h3_habitat_profile_stability.py`

`run_e4_five_locations_v10_stage7.py.draft` adalah sumber run E4 historis yang tervalidasi; run E4 tidak dijalankan ulang. Berkas `build_experiment_registry.py` dan `curate_report_materials.py` hanya membuat indeks dan salinan bahan laporan dengan checksum.

Jangan menjalankan runner eksperimen untuk sekadar membuka notebook atau melihat hasil: gunakan artefak di `results/`.
''')

write(ROOT / 'src/README.md', '''# Source Code

`src/` memuat fungsi pipeline yang dipakai oleh kode eksperimen:

- `preprocess.py`, `mfcc.py`: standardisasi audio dan baseline akustik R0.
- `embeddings.py`: ekstraksi representasi beku R1/R2/R3.
- `retrieve.py`, `evaluate.py`: peringkat similarity dan metrik retrieval.
- `mix_noise.py`: pencampuran derau ITERA terkontrol untuk E2/E4.
- `calibrate_threshold.py`, `e3_alignment.py`: threshold open-set E3.
- `analyze_failures.py`, `bootstrap_inference.py`, `plot_results.py`: E5, statistik, dan visualisasi.

Folder `dsic2706/` dipertahankan untuk kompatibilitas impor lama.
''')

write(ROOT / 'tests/README.md', '''# Tests

`run_all_tests.py` dan `run_tests.py` di akar proyek menjalankan pemeriksaan integritas manifes, leakage split, cosine retrieval, mixing SNR, pembekuan threshold, serta reproducibility.

Struktur:

- `unit/`: perilaku fungsi kecil.
- `integration/`: hubungan manifest, retrieval, noise, dan threshold.
- `reproducibility/`: pemeriksaan provenance dan konfigurasi.

Validasi terakhir: 25 pemeriksaan lulus. Test tidak mengunduh data, menghapus data, atau menjalankan ulang E2–E5.
''')

write(ROOT / 'learning/README.md', '''# Learning

Latihan 01–06 adalah jalur belajar bertahap: mengenal file audio, menyamakan bentuk audio, MFCC, retrieval kecil, inspeksi panggilan, dan audit manifes.

Latihan tidak menghasilkan bukti E0–E5 dan tidak mengubah audio. Catatan pembelajaran ada di `CATATAN_BELAJAR.md`; eksperimen resmi dipetakan dari `experiments/` dan divisualkan di `notebooks/`.
''')

write(ROOT / 'notebooks/README.md', '''# Notebooks

Semua notebook ada di `D:\\FILE AND TASK\\TA\\notebooks`. Satu eksperimen memakai satu notebook dan kodenya berada langsung pada code cell, bukan memanggil runner melalui `subprocess`.

| Notebook | Fungsi | Hasil yang dibaca |
|---|---|---|
| `01_Preprocessing.ipynb` | pembelajaran preprocessing | tidak membuat hasil resmi |
| `02_E0_Preprocessing_Audit.ipynb` | E0 | `results/figures/01_e0_audio_properties.png` dan tabel 01–03 |
| `03_EDA_Physical_Audio.ipynb` | EDA, waveform, spektrogram | gambar 02–07 dan tabel 04–09 |
| `04_E1_Clean_Retrieval.ipynb` | E1 R0–R3 | tabel 10 |
| `05_E2_Controlled_Noise.ipynb` | E2 | gambar 08, 14; tabel 11, 18 |
| `06_E3_Open_Set_Threshold.ipynb` | E3 | gambar 09; tabel 12, 13, 19 |
| `07_E4_Habitat_Noise_Sensitivity.ipynb` | E4 dan H3 | gambar 10, 15; tabel 14, 20, 24–26 |
| `08_E5_Failure_Diagnostics.ipynb` | E5 | gambar 11–13; tabel 15–17 |

Notebook E4 hanya menampilkan run tervalidasi dan tidak menjalankan ulang 320 kondisi. Hasil RQ dan H1–H5 ada di `docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md`.
''')

figure_rows = [
    ('E0', '../../results/figures/01_e0_audio_properties.png'), ('EDA', '../../results/figures/02_eda_overview.png'),
    ('E2', '../../results/figures/08_e2_snr_robustness_map10.png'), ('E3', '../../results/figures/09_e3_threshold_transfer_recall.png'),
    ('E4', '../../results/figures/10_e4_noise_profile_sensitivity.png'), ('H3', '../../results/figures/15_h3_habitat_retention_stability.png'), ('E5', '../../results/figures/11_e5_failure_modes_by_representation.png'),
]
table_rows = [(f'{i:02d}', f'../../results/tables/{name}') for i, name in [(10,'10_e1_clean_retrieval_summary.csv'),(11,'11_e2_snr_robustness.csv'),(12,'12_e3_frozen_thresholds.csv'),(14,'14_e4_domain_shift.csv'),(15,'15_e5_failure_mode_summary.csv'),(23,'23_statistics_rq_hypothesis_matrix.csv'),(24,'24_h3_habitat_profile_stability.csv'),(27,'27_rq_hypothesis_matrix_current.csv')]]
with (ROOT / 'paper/figures/report_figure_index.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.writer(handle); writer.writerow(['experiment', 'source_report_figure']); writer.writerows(figure_rows)
with (ROOT / 'paper/tables/report_table_index.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.writer(handle); writer.writerow(['table_number', 'source_report_table']); writer.writerows(table_rows)
write(ROOT / 'paper/README.md', '''# Paper

`manuscript.md` adalah draf naskah. `bibliography/` menyimpan referensi.

`figures/report_figure_index.csv` dan `tables/report_table_index.csv` memilih gambar serta tabel laporan dari `results/` tanpa menggandakan atau mengedit bukti eksperimen. Berkas final untuk naskah hanya disalin ke `paper/figures/` atau `paper/tables/` saat susunan Bab 4 dan Bab 5 disetujui.

Rujukan hasil ilmiah terkini: `docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md`. E4 memiliki batasan inferensi: ia menguji pencampuran derau per habitat, bukan rekaman burung in-situ.
''')

write(ROOT / 'docs/README.md', '''# Dokumentasi Penelitian

Dokumen aktif untuk membaca hasil dan metode:

- `RESULTS_RQ_HYPOTHESES_2026-10-12.md`: hasil E0–E5, statistik, RQ, dan H1–H5.
- `research/`: RQ, hipotesis, ruang lingkup, keputusan, dan batas kebaruan.
- `protocols/`: prosedur recording ITERA, open-set, dan anotasi.
- `audit_manifest_2026-10-12.json`: bukti audit dataset/manifes.

Eksperimen E0–E5 memiliki artefak selesai/terverifikasi. H3 diuji dari raw E4 sebagai stabilitas retensi lintas lima profil noise dan didukung; E4 tetap tidak menguji rekaman burung in-situ.

Peta seluruh folder dan file aktif tersedia di `../PROJECT_STRUCTURE.md`.
''')

write(ROOT / 'Audit Pembaruan/README.md', '''# Audit Pembaruan

Folder ini menyimpan dokumen audit historis dan keputusan revisi. Dokumen tidak diubah agar jejak keputusan tetap utuh.

Status implementasi saat ini diringkas dalam `current_workspace_index.csv`, yang menunjuk audit dataset, run E0–E5 tervalidasi, statistik, dan dokumen hasil terbaru.
''')
with (ROOT / 'Audit Pembaruan/current_workspace_index.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.writer(handle); writer.writerow(['item', 'current_path', 'status']); writer.writerows([
        ('dataset audit', '../docs/audit_manifest_2026-10-12.json', 'verified'),
        ('experiment registry', '../experiments/experiment_registry.csv', 'current'),
        ('report figures', '../results/figures', 'checksum copied'),
        ('report tables', '../results/tables', 'checksum copied'),
        ('RQ and hypotheses', '../docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md', 'current'),
    ])

# CURRENT_STATUS.md contains a reviewed briefing with current figures. Navigation
# generation must not replace it with a short template.

folders = [
    ('.venv', 'Lingkungan Python lokal; tidak diindeks atau diubah.'),
    ('Administrasi', 'Berkas administrasi akademik; ditambah README navigasi.'),
    ('artifacts', 'Registri artefak tervalidasi.'),
    ('Audit Pembaruan', 'Dokumen audit historis dan indeks workspace saat ini.'),
    ('checkpoints', 'Model beku R1/R2 dan katalog model.'),
    ('configs', 'Parameter beku dan indeks active run.'),
    ('data', 'Audio asli, manifes, dan registry data.'),
    ('docs', 'Metode, audit, hasil RQ/H.'),
    ('experiments', 'Registri E0–E5.'),
    ('learning', 'Latihan pembelajaran aman.'),
    ('notebooks', 'Notebook yang dapat dibaca/run per eksperimen.'),
    ('paper', 'Draf artikel serta indeks figure/table terpilih.'),
    ('Rencana-eksperimen-bimbingan', 'Rencana/logbook historis dan status terkini.'),
    ('results', 'Run sumber, gambar, tabel, dan manifest checksum.'),
    ('scripts', 'Runner dan pembangun indeks.'),
    ('src', 'Fungsi pipeline.'),
    ('tests', 'Validasi integritas serta metode.'),
]
with (ROOT / 'PROJECT_STRUCTURE.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.writer(handle); writer.writerow(['folder', 'role']); writer.writerows(folders)
write(ROOT / 'PROJECT_STRUCTURE.md', '''# Peta Folder Aktif

`PROJECT_STRUCTURE.csv` memberi peta singkat seluruh folder utama. Gunakan peta berikut saat menulis laporan atau belajar kode.

| Folder | Fungsi |
|---|---|
| `data/` | Audio asli, manifes, dan registry data. |
| `checkpoints/` | Model beku R1/R2; tidak diubah. |
| `configs/` | Parameter eksperimen dan indeks run aktif. |
| `src/` | Implementasi pipeline. |
| `scripts/` | Runner dan pembangun indeks. |
| `notebooks/` | Satu notebook langsung per tahap/eksperimen. |
| `experiments/` | Registri E0–E5 yang menghubungkan notebook, run, figure, dan table. |
| `results/reproductions/` | Artefak sumber per run yang tidak ditimpa. |
| `results/figures/`, `results/tables/` | Bahan laporan yang mudah dicari, dengan checksum. |
| `artifacts/` | Registry bukti dan provenance. |
| `docs/` | Metode, hasil RQ/H, audit. |
| `paper/` | Draf naskah dan indeks figure/table terpilih. |
| `tests/` | Pengujian integritas dan metode. |
| `learning/` | Latihan pembelajaran yang tidak mengubah hasil resmi. |
| `Audit Pembaruan/`, `Rencana-eksperimen-bimbingan/` | Catatan audit dan logbook historis. |
| `Administrasi/` | Dokumen administrasi akademik. |

Tidak ada data audio, checkpoint, cache, manifest, atau run eksperimen yang dipindahkan atau ditimpa oleh penataan ini.
''')

write(ROOT / 'Administrasi/README.md', '''# Administrasi

Folder ini menyimpan formulir dan dokumen administrasi akademik. Berkas tidak terkait pipeline atau hasil eksperimen; ia dipisahkan dari `docs/`, `paper/`, dan `results/` agar tidak tercampur dengan artefak penelitian.
''')

write(ROOT / 'README.md', '''# DSIC-2706 — Tugas Akhir Bioacoustic Similarity Retrieval

Repositori ini mengevaluasi representasi audio beku untuk retrieval burung Indonesia ketika kueri dicampur derau lapangan ITERA.

Mulai dari [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md). Untuk melihat hasil siap pakai laporan:

- gambar: `results/figures/`
- tabel angka CSV: `results/tables/`
- sumber dan checksum: `results/report_materials_manifest.json`
- jawaban RQ dan H1–H5: `docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md`
- peta E0–E5: `experiments/experiment_registry.csv`
- notebook yang dapat dipelajari: `notebooks/`

Run eksperimen sumber tetap disimpan per direktori di `results/reproductions/`. Penataan folder ini hanya membuat indeks dan salinan bahan laporan dengan checksum; audio, checkpoint, cache, manifest, dan run historis tidak diubah.

Status penelitian: artefak E0–E5 dan statistik tersedia. E4 mengukur pencampuran derau per habitat; ia belum membuktikan performa pada rekaman burung in-situ.
''')
print('Workspace navigation updated.')
