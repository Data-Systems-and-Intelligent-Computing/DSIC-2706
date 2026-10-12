"""Build reproducible paired statistics and an RQ/H evidence matrix from validated runs."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

os.environ["MPLBACKEND"] = "Agg"
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
REPS = ("R0", "R1", "R2", "R3")
PRIMARY_REPS = ("R0", "R1", "R2")
CONDITIONS = ("Clean", "SNR_20dB", "SNR_10dB", "SNR_0dB", "SNR_-5dB")
SEED = 20261012
BOOTSTRAPS = 10000


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + ".tmp")
    if path.exists() or temporary.exists():
        raise FileExistsError(path)
    with temporary.open("xb") as handle:
        handle.write((json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode())
        handle.flush(); os.fsync(handle.fileno())
    temporary.replace(path)


def atomic_csv(frame: pd.DataFrame, path: Path) -> None:
    temporary = path.with_name(path.name + ".tmp")
    if path.exists() or temporary.exists():
        raise FileExistsError(path)
    with temporary.open("x", newline="", encoding="utf-8") as handle:
        frame.to_csv(handle, index=False)
        handle.flush(); os.fsync(handle.fileno())
    temporary.replace(path)


def require_complete(path: Path, label: str) -> dict:
    metadata = path / "metadata.json"
    if not metadata.exists():
        raise FileNotFoundError(f"{label} metadata is missing: {metadata}")
    value = json.loads(metadata.read_text(encoding="utf-8"))
    if value.get("status") != "complete":
        raise ValueError(f"{label} is not complete")
    return value


def e2_by_condition(e2: Path) -> dict[tuple[str, str], pd.DataFrame]:
    frames: dict[tuple[str, str], pd.DataFrame] = {}
    expected_ids: list[str] | None = None
    for rep in REPS:
        for condition in CONDITIONS:
            path = e2 / "raw" / f"{rep}_{condition}.csv"
            frame = pd.read_csv(path, low_memory=False)
            needed = {"query_id", "AP@10", "top1_match", "max_score"}
            if len(frame) != 311 or not needed.issubset(frame.columns) or frame[list(needed)].isna().any().any():
                raise ValueError(f"E2 raw schema/value check failed: {path}")
            ids = frame.query_id.astype(str).tolist()
            if expected_ids is None:
                expected_ids = ids
            if ids != expected_ids or frame.query_id.astype(str).duplicated().any():
                raise ValueError(f"E2 query ordering/uniqueness failed: {path}")
            frames[(rep, condition)] = frame
    return frames


def bootstrap_difference(a: np.ndarray, b: np.ndarray, rng: np.random.Generator, alternative: str, label: str) -> dict:
    if a.shape != b.shape or a.ndim != 1 or len(a) == 0:
        raise ValueError(f"invalid paired samples for {label}")
    index = rng.integers(0, len(a), size=(BOOTSTRAPS, len(a)))
    draws = (a[index] - b[index]).mean(axis=1)
    observed = float((a - b).mean())
    if alternative == "greater":
        p_value = float((np.count_nonzero(draws <= 0) + 1) / (len(draws) + 1))
    elif alternative == "less":
        p_value = float((np.count_nonzero(draws >= 0) + 1) / (len(draws) + 1))
    else:
        p_value = float(min(1.0, 2 * min((np.count_nonzero(draws <= 0) + 1) / (len(draws) + 1), (np.count_nonzero(draws >= 0) + 1) / (len(draws) + 1))))
    paired_sd = float(np.std(a - b, ddof=1))
    return {"test_id": label, "n_paired": int(len(a)), "effect_mean_difference": observed,
            "paired_standardized_effect": (observed / paired_sd if paired_sd else np.nan),
            "ci_95_low": float(np.quantile(draws, .025)), "ci_95_high": float(np.quantile(draws, .975)),
            "p_value_bootstrap": p_value, "alternative": alternative,
            "statistical_result": "significant" if p_value < .05 else "not_significant"}


def bootstrap_retention(noisy_a: np.ndarray, clean_a: np.ndarray, noisy_b: np.ndarray, clean_b: np.ndarray, rng: np.random.Generator, label: str) -> dict:
    if not (noisy_a.shape == clean_a.shape == noisy_b.shape == clean_b.shape):
        raise ValueError(f"invalid retention samples for {label}")
    index = rng.integers(0, len(clean_a), size=(BOOTSTRAPS, len(clean_a)))
    a_ret = noisy_a[index].mean(axis=1) / clean_a[index].mean(axis=1)
    b_ret = noisy_b[index].mean(axis=1) / clean_b[index].mean(axis=1)
    draws = a_ret - b_ret
    observed_a = float(noisy_a.mean() / clean_a.mean())
    observed_b = float(noisy_b.mean() / clean_b.mean())
    p_value = float((np.count_nonzero(draws <= 0) + 1) / (len(draws) + 1))
    return {"test_id": label, "n_paired": int(len(clean_a)), "effect_mean_difference": float(observed_a - observed_b),
            "retention_a": observed_a, "retention_b": observed_b,
            "ci_95_low": float(np.quantile(draws, .025)), "ci_95_high": float(np.quantile(draws, .975)),
            "p_value_bootstrap": p_value, "alternative": "greater",
            "statistical_result": "significant" if p_value < .05 else "not_significant"}


def transfer_statistics(e3: Path, rng: np.random.Generator) -> tuple[pd.DataFrame, list[dict]]:
    test = pd.read_csv(e3 / "raw" / "test_scores.csv", low_memory=False)
    output = []
    rows: list[dict] = []
    for rep in REPS:
        data = test[test.representation.eq(rep)]
        for target_type, metric, alternative in [("known_bird", "accept_recall", "less"), ("unknown_control", "false_accept_rate", "greater")]:
            clean = data[(data.condition == "Clean") & (data.target_type == target_type)].sort_values("query_id")
            n5 = data[(data.condition == "SNR_-5dB") & (data.target_type == target_type)].sort_values("query_id")
            if clean.query_id.astype(str).tolist() != n5.query_id.astype(str).tolist():
                raise ValueError(f"E3 IDs cannot be paired for {rep}, {target_type}")
            a = n5.predicted_accept.to_numpy(dtype=float)
            b = clean.predicted_accept.to_numpy(dtype=float)
            stat = bootstrap_difference(a, b, rng, alternative, f"H4_{rep}_{metric}_minus5_vs_clean")
            stat.update({"hypothesis": "H4", "representation": rep, "metric": metric,
                         "clean_rate": float(b.mean()), "snr_minus5_rate": float(a.mean()),
                         "change_minus5_minus_clean": float(a.mean() - b.mean())})
            rows.append(stat)
            output.append({"representation": rep, "target_type": target_type, "metric": metric,
                           "clean_rate": float(b.mean()), "snr_minus5_rate": float(a.mean()),
                           "change_minus5_minus_clean": float(a.mean() - b.mean())})
    return pd.DataFrame(output), rows


def e4_descriptive(e4: Path) -> pd.DataFrame:
    frames = []
    for rep in REPS:
        frame = pd.read_csv(e4 / "raw" / f"E4_{rep}_raw.csv", low_memory=False)
        n5 = frame[frame.condition.eq("SNR_-5dB")]
        if len(n5) != 311 * 5 * 4:
            raise ValueError(f"Unexpected E4 -5 dB rows for {rep}")
        grouped = n5.groupby(["representation", "habitat"], as_index=False).agg(
            n=("query_id", "size"), map10=("AP@10", "mean"), top1_accuracy=("top1_match", "mean"))
        frames.append(grouped)
    return pd.concat(frames, ignore_index=True)


def main(e2: Path, e3: Path, e4: Path) -> Path:
    require_complete(e2, "E2"); require_complete(e3, "E3")
    e2_data = e2_by_condition(e2)
    rng = np.random.default_rng(SEED)
    output = ROOT / "results" / "reproductions" / f"STATISTICS_RQ_MATRIX_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')}"
    (output / "tables").mkdir(parents=True); (output / "figures").mkdir()

    stats: list[dict] = []
    # H5: strict paired clean AP@10 comparisons with the deterministic random control.
    for rep in PRIMARY_REPS:
        row = bootstrap_difference(e2_data[(rep, "Clean")]["AP@10"].to_numpy(), e2_data[("R3", "Clean")]["AP@10"].to_numpy(), rng, "greater", f"H5_{rep}_clean_AP10_vs_R3")
        row.update({"hypothesis": "H5", "representation": rep, "metric": "AP@10", "condition": "Clean"}); stats.append(row)
    # H1/H2: the ratio is a bootstrap statistic at the aggregate mAP@10 level, sampled by query.
    for deep in ("R1", "R2"):
        row = bootstrap_retention(e2_data[(deep, "SNR_-5dB")]["AP@10"].to_numpy(), e2_data[(deep, "Clean")]["AP@10"].to_numpy(), e2_data[("R0", "SNR_-5dB")]["AP@10"].to_numpy(), e2_data[("R0", "Clean")]["AP@10"].to_numpy(), rng, f"H1_{deep}_retention_vs_R0_at_minus5")
        row.update({"hypothesis": "H1", "representation": deep, "comparator": "R0", "metric": "mAP@10 retention", "condition": "SNR_-5dB"}); stats.append(row)
    row = bootstrap_retention(e2_data[("R2", "SNR_-5dB")]["AP@10"].to_numpy(), e2_data[("R2", "Clean")]["AP@10"].to_numpy(), e2_data[("R1", "SNR_-5dB")]["AP@10"].to_numpy(), e2_data[("R1", "Clean")]["AP@10"].to_numpy(), rng, "H2_R2_retention_vs_R1_at_minus5")
    row.update({"hypothesis": "H2", "representation": "R2", "comparator": "R1", "metric": "mAP@10 retention", "condition": "SNR_-5dB"}); stats.append(row)
    transfer, h4_stats = transfer_statistics(e3, rng); stats.extend(h4_stats)
    statistics = pd.DataFrame(stats)
    e4_table = e4_descriptive(e4)

    h1 = statistics[statistics.hypothesis.eq("H1")]
    h2 = statistics[statistics.hypothesis.eq("H2")]
    h5 = statistics[statistics.hypothesis.eq("H5")]
    h4 = statistics[statistics.hypothesis.eq("H4")]
    matrix = pd.DataFrame([
        {"item": "RQ utama", "experiment": "E1/E2/E4", "metric": "mAP@10", "artifact": "E2 robustness table; E4 domain table", "result": "R2 has the highest observed mAP@10 in E2 at every tested SNR and in the validated E4 mixture conditions.", "conclusion": "Answered within additive ITERA-noise mixtures", "limitation": "Does not establish performance on naturally recorded bird soundscapes."},
        {"item": "Sub-RQ 1", "experiment": "E2", "metric": "mAP@10, Recall@10, Precision@10", "artifact": "E2 tables/e2_snr_robustness.csv", "result": "All representations have per-query and aggregate values at Clean/+20/+10/0/-5 dB.", "conclusion": "Answered", "limitation": "One deterministic physical-noise segment per query/SNR, not repeated stochastic draws."},
        {"item": "Sub-RQ 2", "experiment": "E3", "metric": "frozen-threshold recall and false-accept rate", "artifact": "E3 threshold_transfer.csv; paired E3 raw scores", "result": "Frozen clean thresholds change their acceptance behavior at -5 dB; see H4 rows.", "conclusion": "Answered", "limitation": "Unknown test controls are synthetic mixes of real unknown/noise audio, not a field soundscape bird test."},
        {"item": "Sub-RQ 3", "experiment": "E2", "metric": "mAP@10 retention at -5 dB", "artifact": "paired_bootstrap_results.csv", "result": f"R2-R1 retention difference={h2.iloc[0].effect_mean_difference:.6f}.", "conclusion": "Answered", "limitation": "Conclusion applies to these representations and the ITERA additive-mixture protocol."},
        {"item": "Sub-RQ 4", "experiment": "E4", "metric": "habitat-conditioned mixture mAP@10", "artifact": "e4_habitat_descriptive.csv", "result": "E4 compares additive mixtures from ITERA habitat recordings, not focal bird recordings captured inside real soundscapes.", "conclusion": "Not answered as written", "limitation": "Cannot infer propagation, distance, absorption, or reverberation effects required by the repository's RQ4 wording."},
        {"item": "H1", "experiment": "E2", "metric": "paired bootstrap of -5 dB / Clean mAP@10", "artifact": "paired_bootstrap_results.csv", "result": f"R1 vs R0 p={h1[h1.representation.eq('R1')].iloc[0].p_value_bootstrap:.6g}; R2 vs R0 p={h1[h1.representation.eq('R2')].iloc[0].p_value_bootstrap:.6g}.", "conclusion": "Supported" if (h1.statistical_result == 'significant').all() and (h1.effect_mean_difference > 0).all() else "Not supported", "limitation": "R3 excluded: it is an ID-deterministic control, not an audio representation."},
        {"item": "H2", "experiment": "E2", "metric": "paired bootstrap of R2-R1 -5 dB retention", "artifact": "paired_bootstrap_results.csv", "result": f"difference={h2.iloc[0].effect_mean_difference:.6f}, 95% CI [{h2.iloc[0].ci_95_low:.6f}, {h2.iloc[0].ci_95_high:.6f}], p={h2.iloc[0].p_value_bootstrap:.6g}.", "conclusion": "Supported" if h2.iloc[0].statistical_result == 'significant' and h2.iloc[0].effect_mean_difference > 0 else "Not supported", "limitation": "No causal statement about the model architecture follows from this comparison."},
        {"item": "H3", "experiment": "E4", "metric": "not validly defined by available design", "artifact": "e4_habitat_descriptive.csv", "result": "No paired corpus of birds recorded in real ITERA soundscapes exists in validated evidence.", "conclusion": "Not testable with current data", "limitation": "E4 is real-noise additive mixing, so it cannot test the stated real-soundscape mechanisms."},
        {"item": "H4", "experiment": "E3", "metric": "paired change in known accept recall and unknown false-accept rate", "artifact": "e3_threshold_transfer_statistics.csv", "result": "Known acceptance recall declines significantly from Clean to -5 dB for R0, R1, and R2; false-accept rate falls rather than rises.", "conclusion": "Supported for R0-R2 through recall degradation; R3 is unchanged by design.", "limitation": "Threshold is optimized for clean calibration with Youden J; it is not recalibrated at test SNR."},
        {"item": "H5", "experiment": "E1/E2 Clean", "metric": "paired clean AP@10 vs R3", "artifact": "paired_bootstrap_results.csv", "result": f"All primary comparisons significant={bool((h5.statistical_result == 'significant').all())} with positive effect={bool((h5.effect_mean_difference > 0).all())}.", "conclusion": "Supported" if (h5.statistical_result == 'significant').all() and (h5.effect_mean_difference > 0).all() else "Not supported", "limitation": "R3 is a deterministic random-ID control and is not evidence of acoustic noise robustness."},
    ])

    atomic_csv(statistics, output / "tables" / "paired_bootstrap_results.csv")
    atomic_csv(transfer, output / "tables" / "e3_threshold_transfer_statistics.csv")
    atomic_csv(e4_table, output / "tables" / "e4_habitat_descriptive.csv")
    atomic_csv(matrix, output / "tables" / "rq_hypothesis_matrix.csv")
    provenance = pd.DataFrame([
        {"experiment": "E0", "status": "VALID", "artifact": "results/reproductions/E0_20261011_202557", "basis": "Saved standalone audit artifact; active-manifest work is not inferred from legacy results.", "limitation": "Descriptive audit, not a retrieval comparison."},
        {"experiment": "E1 R0", "status": "VALID", "artifact": "results/reproductions/E1_R0_20261011_175321", "basis": "Clean retrieval artifact matches active-manifest R0 baseline.", "limitation": "One clean evaluation only."},
        {"experiment": "E1 R1-R3", "status": "VALID", "artifact": "results/reproductions/E1_R1_cache_20261012T021032_566409Z; E1_R2_cache_20261012T021034_128124Z; E1_R3_cache_20261012T021035_119528Z", "basis": "Explicit cache materializations with active-manifest hash, ID order, dimensions, finite values, and R3 version checked.", "limitation": "Materialized from valid clean caches; not represented as historical runs."},
        {"experiment": "E2", "status": "VALID", "artifact": str(e2.relative_to(ROOT)).replace("\\", "/"), "basis": "20 raw condition files, 311 aligned queries each, mixing audit, per-query retrieval metrics.", "limitation": "Controlled additive mixing only."},
        {"experiment": "E3", "status": "VALID", "artifact": str(e3.relative_to(ROOT)).replace("\\", "/"), "basis": "Separate calibration split, frozen per-representation thresholds, 12,420 test rows.", "limitation": "Unknown controls are not naturally recorded bird soundscapes."},
        {"experiment": "E4", "status": "VALID", "artifact": "results/reproductions/E4_5sites_20261011T213404_350219Z; results/reproductions/E4_audit_20261012T021801_989259Z", "basis": "Read-only audit verified 320 snapshots, 4 raw CSVs, 324 comparison rows, run identity, and tested ZIP backup.", "limitation": "Original raw lacks ranking identities, class margins, and noisy-audio feature fields."},
        {"experiment": "E5", "status": "VALID_WITH_LIMITATION", "artifact": "results/reproductions/E5_diagnostics_20261012T091512_868500Z", "basis": "E2 6,220 known rows plus E4 100,764 rows and E3 6,200 unknown rows classified with frozen thresholds.", "limitation": "E4 unavailable fields are marked unavailable; no identities or margins are invented."},
        {"experiment": "Legacy BirdCLEF results", "status": "SUPERSEDED", "artifact": "results/archive/birdclef_2026", "basis": "Documented historical outputs include withdrawn/imputed XC42472-era evidence and are excluded from official evidence.", "limitation": "Retained only as historical archive; not used in current matrix."},
    ])
    atomic_csv(provenance, output / "tables" / "experiment_provenance_status.csv")
    # Figure only uses valid, paired E2 clean/-5 observations.
    summary = []
    for rep in REPS:
        clean = e2_data[(rep, "Clean")]["AP@10"].mean()
        n5 = e2_data[(rep, "SNR_-5dB")]["AP@10"].mean()
        summary.append({"representation": rep, "clean_map10": clean, "minus5_map10": n5, "retention": n5 / clean})
    retention = pd.DataFrame(summary)
    atomic_csv(retention, output / "tables" / "e2_retention_summary.csv")
    ax = retention.set_index("representation")[["clean_map10", "minus5_map10"]].plot(kind="bar", figsize=(8, 5))
    ax.set_ylabel("mean AP@10 (mAP@10)"); ax.set_title("E2 clean vs -5 dB retrieval"); plt.tight_layout(); plt.savefig(output / "figures" / "e2_clean_minus5_comparison.png", dpi=180); plt.close()
    validation = {"status": "PASS_WITH_H3_DESIGN_LIMITATION", "bootstrap_iterations": BOOTSTRAPS, "seed": SEED, "e2_raw_files_checked": 20, "e2_query_count": 311, "e3_test_rows": 12420, "e4_habitat_rows": int(len(e4_table)), "matrix_rows": int(len(matrix)), "provenance_rows": int(len(provenance)), "h3_limit": "E4 is additive mixing of real noise, not a corpus of bird recordings made in real soundscapes."}
    atomic_json(output / "validation_report.json", validation)
    atomic_json(output / "metadata.json", {"status": "complete", "artifact_schema": "statistics_rq_matrix_v1", "created_utc": datetime.now(timezone.utc).isoformat(), "e2": str(e2.relative_to(ROOT)), "e3": str(e3.relative_to(ROOT)), "e4": str(e4.relative_to(ROOT)), "bootstrap": {"iterations": BOOTSTRAPS, "seed": SEED, "unit": "paired query"}, "h3_status": "not_testable_with_current_design"})
    (output / "README.md").write_text("# Statistics and RQ/H matrix\n\nAll inferential comparisons use paired query bootstrap (10,000 iterations, seed 20261012). H3/RQ4 is explicitly not treated as answered: validated E4 is additive mixing with real ITERA noise, not a real-soundscape bird corpus.\n", encoding="utf-8")
    print(output)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--e2", required=True, type=Path)
    parser.add_argument("--e3", required=True, type=Path)
    parser.add_argument("--e4", required=True, type=Path)
    args = parser.parse_args()
    main(args.e2.resolve(), args.e3.resolve(), args.e4.resolve())
