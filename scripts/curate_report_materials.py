"""Copy verified experiment outputs into report-friendly result folders.

This makes immutable, checksum-recorded copies. It never edits a reproduction run.
"""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
REPRO = RESULTS / "reproductions"
FIGURES = RESULTS / "figures"
TABLES = RESULTS / "tables"
MANIFEST = RESULTS / "report_materials_manifest.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source(run: str, relative: str) -> Path:
    path = REPRO / run / relative
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def copy_item(entries: list[dict], category: str, target_name: str, run: str, relative: str, purpose: str) -> None:
    original = source(run, relative)
    destination = (FIGURES if category == "figure" else TABLES) / target_name
    original_hash = sha256(original)
    if destination.exists():
        if sha256(destination) != original_hash:
            raise FileExistsError(f"Refusing to replace a different existing file: {destination}")
    else:
        shutil.copy2(original, destination)
    entries.append({
        "category": category,
        "target": destination.relative_to(ROOT).as_posix(),
        "source": original.relative_to(ROOT).as_posix(),
        "sha256": original_hash,
        "bytes": original.stat().st_size,
        "purpose": purpose,
    })


def make_e1_summary(entries: list[dict]) -> None:
    runs = [
        ("R0", "E1_R0_20261011_175321", "direct formal run"),
        ("R1", "E1_R1_cache_20261012T021032_566409Z", "cache materialization; cache provenance verified"),
        ("R2", "E1_R2_cache_20261012T021034_128124Z", "cache materialization; cache provenance verified"),
        ("R3", "E1_R3_cache_20261012T021035_119528Z", "cache materialization; cache provenance verified"),
    ]
    destination = TABLES / "10_e1_clean_retrieval_summary.csv"
    rows = []
    for representation, run, provenance in runs:
        metadata_path = source(run, "metadata.json")
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        summary = metadata["summary"]
        rows.append({
            "representation": representation,
            "run": run,
            "provenance": provenance,
            "num_queries": summary["num_queries"],
            "Top1": summary["mean_top1"],
            "MRR": summary["MRR"],
            "mAP@10": summary["mAP@10"],
            "Recall@10": summary["Recall@10"],
            "Precision@10": summary["Precision@10"],
            "manifest_sha256": metadata["manifest_sha256"],
        })
    fieldnames = list(rows[0])
    text_lines = []
    import io
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    expected = stream.getvalue().encode("utf-8")
    expected_hash = hashlib.sha256(expected).hexdigest()
    if destination.exists():
        if sha256(destination) != expected_hash:
            raise FileExistsError(f"Refusing to replace a different existing file: {destination}")
    else:
        destination.write_bytes(expected)
    entries.append({
        "category": "table",
        "target": destination.relative_to(ROOT).as_posix(),
        "source": "metadata.json from four verified E1 runs",
        "sha256": expected_hash,
        "bytes": len(expected),
        "purpose": "Clean retrieval comparison for R0-R3.",
    })


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    entries: list[dict] = []

    figure_specs = [
        ("01_e0_audio_properties.png", "E0_20261011_202557", "figures/e0_audio_properties.png", "E0 preprocessing audit."),
        ("02_eda_overview.png", "EDA_20261011_202714", "figures/eda_overview.png", "EDA overview."),
        ("03_eda_bird_waveform_spectrogram_examples.png", "EDA_visuals_20261012T133209_032622Z", "figures/eda_bird_waveform_spectrogram_examples.png", "Bird audio waveform and spectrogram examples."),
        ("04_eda_duration_sampling_rate.png", "EDA_visuals_20261012T133209_032622Z", "figures/eda_duration_sampling_rate.png", "Duration and sampling-rate distribution."),
        ("05_eda_itera_noise_spectrogram_profiles.png", "EDA_visuals_20261012T133209_032622Z", "figures/eda_itera_noise_spectrogram_profiles.png", "ITERA noise spectral profiles."),
        ("06_eda_noise_locations.png", "EDA_visuals_20261012T133209_032622Z", "figures/eda_noise_locations.png", "ITERA noise locations."),
        ("07_eda_species_distribution.png", "EDA_visuals_20261012T133209_032622Z", "figures/eda_species_distribution.png", "Target species distribution."),
        ("08_e2_snr_robustness_map10.png", "E2_controlled_20261012T021600_897497Z", "figures/e2_snr_robustness_map10.png", "E2 mAP@10 across SNR conditions."),
        ("09_e3_threshold_transfer_recall.png", "E3_open_set_20261012T022548_802536Z", "figures/e3_threshold_transfer_recall.png", "E3 threshold-transfer recall."),
        ("10_e4_noise_profile_sensitivity.png", "E4_5sites_20261011T213404_350219Z", "figures/e4_noise_profile_sensitivity.png", "E4 habitat noise sensitivity."),
        ("11_e5_failure_modes_by_representation.png", "E5_diagnostics_20261012T091512_868500Z", "figures/failure_modes_by_representation.png", "E5 failure-mode composition."),
        ("12_e5_margin_distribution_by_failure_type.png", "E5_diagnostics_20261012T091512_868500Z", "figures/margin_distribution_by_failure_type.png", "E5 similarity-margin distribution."),
        ("13_e5_spectral_features_by_failure_type.png", "E5_diagnostics_20261012T091512_868500Z", "figures/spectral_features_by_failure_type.png", "E5 spectral diagnostics."),
        ("14_e2_clean_minus5_comparison.png", "STATISTICS_RQ_MATRIX_20261012T092924_809804Z", "figures/e2_clean_minus5_comparison.png", "Clean versus -5 dB comparison."),
    ]
    for target, run, relative, purpose in figure_specs:
        copy_item(entries, "figure", target, run, relative, purpose)

    table_specs = [
        ("01_e0_summary.csv", "E0_20261011_202557", "tables/summary.csv", "E0 preprocessing summary."),
        ("02_e0_representation_probe.csv", "E0_20261011_202557", "tables/representation_probe.csv", "E0 representation probe."),
        ("03_e0_per_recording.csv", "E0_20261011_202557", "tables/per_recording.csv", "E0 sampled recording audit."),
        ("04_eda_summary_by_source.csv", "EDA_20261011_202714", "tables/summary_by_source.csv", "Physical-audio summary by source."),
        ("05_eda_target_species_summary.csv", "EDA_20261011_202714", "tables/target_species_summary.csv", "Target species summary."),
        ("06_eda_noise_location_summary.csv", "EDA_20261011_202714", "tables/noise_location_summary.csv", "Noise location summary."),
        ("07_eda_physical_audio_inventory.csv", "EDA_20261011_202714", "tables/physical_audio_inventory.csv", "Complete physical audio inventory."),
        ("08_eda_visual_summary.csv", "EDA_visuals_20261012T133209_032622Z", "tables/eda_visual_summary.csv", "Summary backing EDA figures."),
        ("09_eda_noise_locations.csv", "EDA_visuals_20261012T133209_032622Z", "tables/noise_locations.csv", "ITERA location labels for visual EDA."),
        ("11_e2_snr_robustness.csv", "E2_controlled_20261012T021600_897497Z", "tables/e2_snr_robustness.csv", "E2 controlled-noise results."),
        ("12_e3_frozen_thresholds.csv", "E3_open_set_20261012T022548_802536Z", "tables/frozen_thresholds.csv", "Thresholds calibrated then frozen."),
        ("13_e3_threshold_transfer.csv", "E3_open_set_20261012T022548_802536Z", "tables/threshold_transfer.csv", "Open-set threshold transfer."),
        ("14_e4_domain_shift.csv", "E4_5sites_20261011T213404_350219Z", "tables/e4_domain_shift_table.csv", "E4 habitat-noise domain shift."),
        ("15_e5_failure_mode_summary.csv", "E5_diagnostics_20261012T091512_868500Z", "tables/failure_mode_summary.csv", "E5 failure-mode summary."),
        ("16_e5_selected_case_manifest.csv", "E5_diagnostics_20261012T091512_868500Z", "tables/selected_case_manifest.csv", "Selected E5 cases for inspection."),
        ("17_e5_unknown_open_set_diagnostics.csv", "E5_diagnostics_20261012T091512_868500Z", "tables/unknown_open_set_diagnostics.csv", "Unknown-set E5 diagnostics."),
        ("18_statistics_e2_retention.csv", "STATISTICS_RQ_MATRIX_20261012T092924_809804Z", "tables/e2_retention_summary.csv", "E2 retention summary."),
        ("19_statistics_e3_threshold_transfer.csv", "STATISTICS_RQ_MATRIX_20261012T092924_809804Z", "tables/e3_threshold_transfer_statistics.csv", "E3 statistical summary."),
        ("20_statistics_e4_habitat.csv", "STATISTICS_RQ_MATRIX_20261012T092924_809804Z", "tables/e4_habitat_descriptive.csv", "E4 descriptive habitat results."),
        ("21_statistics_provenance.csv", "STATISTICS_RQ_MATRIX_20261012T092924_809804Z", "tables/experiment_provenance_status.csv", "Experiment provenance status."),
        ("22_statistics_paired_bootstrap.csv", "STATISTICS_RQ_MATRIX_20261012T092924_809804Z", "tables/paired_bootstrap_results.csv", "Paired bootstrap tests."),
        ("23_statistics_rq_hypothesis_matrix.csv", "STATISTICS_RQ_MATRIX_20261012T092924_809804Z", "tables/rq_hypothesis_matrix.csv", "RQ and hypothesis answer matrix."),
    ]
    for target, run, relative, purpose in table_specs:
        copy_item(entries, "table", target, run, relative, purpose)
    make_e1_summary(entries)

    # H3 is a read-only statistical analysis of validated E4 raw CSV files.
    h3_run = sorted(REPRO.glob("H3_habitat_profile_stability_*"))[-1].name
    h3_specs = [
        ("table", "24_h3_habitat_profile_stability.csv", "tables/h3_stability_summary.csv", "H3 retention-swing summary and paired-bootstrap inference."),
        ("table", "25_h3_retention_by_habitat_repeat.csv", "tables/h3_retention_by_habitat_repeat.csv", "H3 per-location retention values across noise repeats."),
        ("table", "26_h3_bootstrap_distribution.csv", "tables/h3_bootstrap_distribution.csv", "H3 10,000 paired-bootstrap draws."),
        ("figure", "15_h3_habitat_retention_stability.png", "figures/h3_habitat_retention_stability.png", "H3 report figure: retention profiles and stability swings."),
    ]
    for category, target, relative, purpose in h3_specs:
        copy_item(entries, category, target, h3_run, relative, purpose)

    payload = {
        "schema": "report_materials_manifest_v2",
        "purpose": "Checksum-recorded report-friendly copies of verified experiment outputs.",
        "source_policy": "Source runs under results/reproductions are not modified by this process.",
        "h3_note": "H3 report materials were added from read-only statistical analysis of validated E4 raw CSV files.",
        "large_tables_kept_at_source": [
            "results/reproductions/E5_diagnostics_20261012T091512_868500Z/tables/all_query_diagnostics.csv",
            "results/reproductions/E5_diagnostics_20261012T091512_868500Z/tables/failure_cases.csv",
        ],
        "entries": entries,
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    # The manifest is a derived checksum index. Rebuild it deterministically from
    # immutable source runs so a new verified report material is registered safely.
    MANIFEST.write_text(rendered, encoding="utf-8")
    print(f"Report materials ready: {len(entries)} files")
    print(FIGURES)
    print(TABLES)
    print(MANIFEST)


if __name__ == "__main__":
    main()
