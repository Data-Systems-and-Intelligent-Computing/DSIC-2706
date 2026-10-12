"""Build a non-destructive experiment/artifact registry for navigation."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / 'experiments'
ARTIFACTS = ROOT / 'artifacts'

items = [
    {
        'id': 'E0', 'directory': 'E0_preprocessing_audit', 'title': 'Preprocessing Audit', 'status': 'verified',
        'notebook': 'notebooks/02_E0_Preprocessing_Audit.ipynb',
        'source_code': 'scripts/run_e0_preprocessing_verification.py',
        'runs': ['results/reproductions/E0_20261011_202557'],
        'figures': ['results/figures/01_e0_audio_properties.png'],
        'tables': ['results/tables/01_e0_summary.csv', 'results/tables/02_e0_representation_probe.csv', 'results/tables/03_e0_per_recording.csv'],
    },
    {
        'id': 'EDA', 'directory': 'EDA_physical_audio', 'title': 'Physical Audio Exploratory Data Analysis', 'status': 'verified',
        'notebook': 'notebooks/03_EDA_Physical_Audio.ipynb',
        'source_code': 'scripts/run_eda_formal.py',
        'runs': ['results/reproductions/EDA_20261011_202714', 'results/reproductions/EDA_visuals_20261012T133209_032622Z'],
        'figures': [f'results/figures/{n}' for n in ['02_eda_overview.png','03_eda_bird_waveform_spectrogram_examples.png','04_eda_duration_sampling_rate.png','05_eda_itera_noise_spectrogram_profiles.png','06_eda_noise_locations.png','07_eda_species_distribution.png']],
        'tables': [f'results/tables/{n}' for n in ['04_eda_summary_by_source.csv','05_eda_target_species_summary.csv','06_eda_noise_location_summary.csv','07_eda_physical_audio_inventory.csv','08_eda_visual_summary.csv','09_eda_noise_locations.csv']],
    },
    {
        'id': 'E1', 'directory': 'E1_clean_retrieval', 'title': 'Clean Similarity Retrieval', 'status': 'verified_and_consolidated',
        'notebook': 'notebooks/04_E1_Clean_Retrieval.ipynb',
        'source_code': 'scripts/run_e1_clean_r0.py; scripts/materialize_e1_from_cache.py',
        'runs': ['results/reproductions/E1_R0_20261011_175321','results/reproductions/E1_R1_cache_20261012T021032_566409Z','results/reproductions/E1_R2_cache_20261012T021034_128124Z','results/reproductions/E1_R3_cache_20261012T021035_119528Z'],
        'figures': [],
        'tables': ['results/tables/10_e1_clean_retrieval_summary.csv'],
    },
    {
        'id': 'E2', 'directory': 'E2_controlled_noise', 'title': 'Controlled ITERA Noise Robustness', 'status': 'complete',
        'notebook': 'notebooks/05_E2_Controlled_Noise.ipynb',
        'source_code': 'scripts/run_e2_controlled_noise.py',
        'runs': ['results/reproductions/E2_controlled_20261012T021600_897497Z'],
        'figures': ['results/figures/08_e2_snr_robustness_map10.png','results/figures/14_e2_clean_minus5_comparison.png'],
        'tables': ['results/tables/11_e2_snr_robustness.csv','results/tables/18_statistics_e2_retention.csv'],
    },
    {
        'id': 'E3', 'directory': 'E3_open_set_threshold', 'title': 'Open-Set Frozen Threshold', 'status': 'complete',
        'notebook': 'notebooks/06_E3_Open_Set_Threshold.ipynb',
        'source_code': 'scripts/run_e3_open_set.py',
        'runs': ['results/reproductions/E3_open_set_20261012T022548_802536Z'],
        'figures': ['results/figures/09_e3_threshold_transfer_recall.png'],
        'tables': ['results/tables/12_e3_frozen_thresholds.csv','results/tables/13_e3_threshold_transfer.csv','results/tables/19_statistics_e3_threshold_transfer.csv'],
    },
    {
        'id': 'E4', 'directory': 'E4_habitat_noise_sensitivity', 'title': 'Habitat Noise Profile Sensitivity', 'status': 'verified_existing_run',
        'notebook': 'notebooks/07_E4_Habitat_Noise_Sensitivity.ipynb',
        'source_code': 'scripts/run_e4_five_locations_v10_stage7.py.draft; scripts/run_h3_habitat_profile_stability.py',
        'runs': ['results/reproductions/E4_5sites_20261011T213404_350219Z','results/reproductions/E4_audit_20261012T021801_989259Z','results/reproductions/H3_habitat_profile_stability_20261012T141344_312163Z'],
        'figures': ['results/figures/10_e4_noise_profile_sensitivity.png','results/figures/15_h3_habitat_retention_stability.png'],
        'tables': ['results/tables/14_e4_domain_shift.csv','results/tables/20_statistics_e4_habitat.csv','results/tables/24_h3_habitat_profile_stability.csv','results/tables/25_h3_retention_by_habitat_repeat.csv','results/tables/26_h3_bootstrap_distribution.csv','results/tables/27_rq_hypothesis_matrix_current.csv'],
    },
    {
        'id': 'E5', 'directory': 'E5_failure_diagnostics', 'title': 'Failure-Mode Diagnostics', 'status': 'complete',
        'notebook': 'notebooks/08_E5_Failure_Diagnostics.ipynb',
        'source_code': 'scripts/run_e5_diagnostics.py',
        'runs': ['results/reproductions/E5_diagnostics_20261012T091512_868500Z'],
        'figures': ['results/figures/11_e5_failure_modes_by_representation.png','results/figures/12_e5_margin_distribution_by_failure_type.png','results/figures/13_e5_spectral_features_by_failure_type.png'],
        'tables': ['results/tables/15_e5_failure_mode_summary.csv','results/tables/16_e5_selected_case_manifest.csv','results/tables/17_e5_unknown_open_set_diagnostics.csv'],
    },
]

for item in items:
    folder = EXPERIMENTS / item['directory']
    folder.mkdir(parents=True, exist_ok=True)
    payload = {key: value for key, value in item.items() if key != 'directory'}
    payload['role'] = 'Navigation and provenance index. Source results remain immutable under results/reproductions.'
    for key in ['notebook']:
        assert (ROOT / payload[key]).is_file(), payload[key]
    for key in ['runs', 'figures', 'tables']:
        for relative in payload[key]:
            assert (ROOT / relative).exists(), relative
    (folder / 'experiment_registry.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

registry_csv = EXPERIMENTS / 'experiment_registry.csv'
fieldnames = ['experiment', 'title', 'status', 'notebook', 'source_code', 'validated_runs', 'report_figures', 'report_tables']
rows = [{
    'experiment': x['id'], 'title': x['title'], 'status': x['status'], 'notebook': x['notebook'],
    'source_code': x['source_code'], 'validated_runs': '; '.join(x['runs']),
    'report_figures': '; '.join(x['figures']) or '(none)', 'report_tables': '; '.join(x['tables']),
} for x in items]
with registry_csv.open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

(EXPERIMENTS / 'README.md').write_text('''# Experiments\n\nFolder ini adalah **registri eksperimen aktif**, bukan tempat menyimpan salinan hasil mentah.\n\n- Setiap folder `E0_...` sampai `E5_...` memuat `experiment_registry.json`: status, notebook, kode asal, run tervalidasi, serta gambar dan tabel laporan terkait.\n- `experiment_registry.csv` memberi ringkasan satu baris per eksperimen.\n- Kode yang dapat dipelajari berada di `notebooks/`; run asal yang tidak diubah berada di `results/reproductions/`; gambar dan tabel yang siap dipakai laporan berada di `results/figures/` dan `results/tables/`.\n\nStruktur ini membuat folder `experiments/` berfungsi sebagai pintu masuk dan peta provenance tanpa mengubah hasil eksperimen yang telah tervalidasi.\n''', encoding='utf-8')

artifact_rows = []
for item in items:
    for run in item['runs']:
        artifact_rows.append({'experiment': item['id'], 'artifact_type': 'validated_run', 'path': run, 'status': item['status']})
    for path in item['figures']:
        artifact_rows.append({'experiment': item['id'], 'artifact_type': 'report_figure', 'path': path, 'status': 'copied_with_checksum'})
    for path in item['tables']:
        artifact_rows.append({'experiment': item['id'], 'artifact_type': 'report_table', 'path': path, 'status': 'copied_with_checksum'})
artifact_rows.extend([
    {'experiment': 'Statistics', 'artifact_type': 'validated_run', 'path': 'results/reproductions/STATISTICS_RQ_MATRIX_20261012T092924_809804Z', 'status': 'complete'},
    {'experiment': 'Statistics', 'artifact_type': 'report_manifest', 'path': 'results/report_materials_manifest.json', 'status': 'checksum_verified'},
    {'experiment': 'Results', 'artifact_type': 'narrative_results', 'path': 'docs/RESULTS_RQ_HYPOTHESES_2026-10-12.md', 'status': 'current'},
])
with (ARTIFACTS / 'validated_artifact_registry.csv').open('w', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=['experiment', 'artifact_type', 'path', 'status'])
    writer.writeheader()
    writer.writerows(artifact_rows)

(ARTIFACTS / 'README.md').write_text('''# Artifacts\n\nFolder ini menyimpan **registri artefak**, bukan duplikasi audio, cache, atau hasil mentah.\n\n- `validated_artifact_registry.csv` mengindeks run tervalidasi, gambar laporan, tabel laporan, dan dokumen hasil.\n- `reproducibility/manifest_sha256.txt` mencatat hash manifes aktif.\n- Artefak eksperimen asal tetap aman di `results/reproductions/`.\n- Salinan gambar dan tabel yang dipakai untuk laporan ada di `results/figures/` dan `results/tables/`; checksum sumbernya tercatat dalam `results/report_materials_manifest.json`.\n''', encoding='utf-8')
print(f'Created/updated experiment registry: {len(items)} experiments')
print(f'Created artifact registry: {len(artifact_rows)} entries')
