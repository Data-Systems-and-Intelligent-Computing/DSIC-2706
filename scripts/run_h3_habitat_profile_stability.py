"""H3 habitat-profile stability analysis from immutable E4 raw files.

This is a post-hoc statistical analysis of the validated E4 run.  It never
mixes audio or writes into the original E4 directory.
"""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
E4 = ROOT / "results" / "reproductions" / "E4_5sites_20261011T213404_350219Z"
RAW = E4 / "raw"
OUT_ROOT = ROOT / "results" / "reproductions"
TABLES = ROOT / "results" / "tables"
FIGURES = ROOT / "results" / "figures"
SEED = 20261012
BOOTSTRAPS = 10_000
PRIMARY_REPS = ("R1", "R2")  # PANN generic audio vs BirdNET bioacoustic
HABITATS = ("Embung_F", "Gedung_F", "Kebun_Raya", "Masjid_At_Tanwir", "Sekitar_GKU_1")
SNRS = (20, 10, 0, -5)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def percentile_ci(values: np.ndarray) -> tuple[float, float]:
    return tuple(float(x) for x in np.quantile(values, [0.025, 0.975]))


def p_from_bootstrap(values: np.ndarray) -> float:
    # Conservative two-sided tail estimate. CI is the primary inference.
    lower = (np.count_nonzero(values <= 0) + 1) / (len(values) + 1)
    upper = (np.count_nonzero(values >= 0) + 1) / (len(values) + 1)
    return float(min(1.0, 2 * min(lower, upper)))


def read_representation(rep: str) -> tuple[np.ndarray, np.ndarray, list[str]]:
    path = RAW / f"E4_{rep}_raw.csv"
    frame = pd.read_csv(path, low_memory=False)
    clean = frame.loc[frame["condition"].eq("Clean"), ["query_id", "AP@10"]].copy()
    clean = clean.sort_values("query_id").reset_index(drop=True)
    ids = clean["query_id"].tolist()
    if len(ids) != 311 or len(set(ids)) != len(ids):
        raise RuntimeError(f"{rep}: clean query IDs are not 311 unique values")
    clean_values = clean["AP@10"].to_numpy(float)
    noisy = np.empty((len(SNRS), 4, len(HABITATS), len(ids)), dtype=float)
    for s_idx, snr in enumerate(SNRS):
        for repeat in range(4):
            for h_idx, habitat in enumerate(HABITATS):
                subset = frame.loc[
                    frame["snr_db"].eq(snr)
                    & frame["repeat_id"].eq(repeat)
                    & frame["habitat"].eq(habitat),
                    ["query_id", "AP@10"],
                ].sort_values("query_id")
                if subset["query_id"].tolist() != ids:
                    raise RuntimeError(f"{rep}/{snr}/{repeat}/{habitat}: query order mismatch")
                if len(subset) != len(ids):
                    raise RuntimeError(f"{rep}/{snr}/{repeat}/{habitat}: expected {len(ids)} rows")
                noisy[s_idx, repeat, h_idx] = subset["AP@10"].to_numpy(float)
    return clean_values, noisy, ids


def bootstrap_stability(clean: np.ndarray, noisy: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return bootstrap and observed habitat swing, indexed [snr, representation]."""
    # clean: [representation, query]; noisy: [representation, snr, repeat, habitat, query]
    reps, n_snr, n_repeat, n_habitat, n_query = noisy.shape
    observed_retention = noisy.mean(axis=-1) / clean.mean(axis=-1)[:, None, None, None]
    observed_swing = observed_retention.max(axis=-1) - observed_retention.min(axis=-1)  # rep,snr,repeat
    observed = observed_swing.mean(axis=-1).transpose(1, 0)  # snr,rep

    rng = np.random.default_rng(SEED)
    out = np.empty((BOOTSTRAPS, n_snr, reps), dtype=float)
    flat_noisy = noisy.reshape(reps * n_snr * n_repeat * n_habitat, n_query)
    for start in range(0, BOOTSTRAPS, 100):
        stop = min(start + 100, BOOTSTRAPS)
        indexes = rng.integers(0, n_query, size=(stop - start, n_query))
        # mean bootstrap values: [batch, flat condition] and [batch, representation]
        n_means = flat_noisy[:, indexes].mean(axis=-1).transpose(1, 0)
        n_means = n_means.reshape(stop - start, reps, n_snr, n_repeat, n_habitat)
        c_means = clean[:, indexes].mean(axis=-1).transpose(1, 0)
        retention = n_means / c_means[:, :, None, None, None]
        swing = retention.max(axis=-1) - retention.min(axis=-1)
        out[start:stop] = swing.mean(axis=-1).transpose(0, 2, 1)
    return observed, out


def main() -> None:
    inputs = {p.name: sha256(p) for p in sorted(RAW.glob("E4_R*_raw.csv"))}
    if set(inputs) != {f"E4_{r}_raw.csv" for r in ("R0", "R1", "R2", "R3")}:
        raise RuntimeError("The four expected E4 raw CSV files are required")

    loaded = {rep: read_representation(rep) for rep in PRIMARY_REPS}
    ids = loaded["R1"][2]
    if ids != loaded["R2"][2]:
        raise RuntimeError("R1 and R2 do not have identical query IDs")
    clean = np.stack([loaded[rep][0] for rep in PRIMARY_REPS])
    noisy = np.stack([loaded[rep][1] for rep in PRIMARY_REPS])
    observed, boot = bootstrap_stability(clean, noisy)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    run = OUT_ROOT / f"H3_habitat_profile_stability_{timestamp}"
    run_tables = run / "tables"
    run_figures = run / "figures"
    run_tables.mkdir(parents=True)
    run_figures.mkdir(parents=True)
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    summary_rows = []
    boot_rows = []
    for s_idx, snr in enumerate(SNRS):
        diff = boot[:, s_idx, 0] - boot[:, s_idx, 1]
        low, high = percentile_ci(diff)
        summary_rows.append({
            "analysis_scope": "per_snr",
            "snr_db": snr,
            "metric": "mAP@10 relative-retention swing across 5 ITERA habitat profiles",
            "R1_generic_mean_swing": observed[s_idx, 0],
            "R2_bioacoustic_mean_swing": observed[s_idx, 1],
            "R1_minus_R2_effect": observed[s_idx, 0] - observed[s_idx, 1],
            "ci95_low": low,
            "ci95_high": high,
            "bootstrap_two_sided_p": p_from_bootstrap(diff),
            "bootstrap_iterations": BOOTSTRAPS,
            "queries": len(ids),
            "noise_repeats_per_habitat": 4,
            "habitats": len(HABITATS),
            "supports_H3_at_alpha_0_05": bool(low > 0),
        })
        boot_rows.extend({"snr_db": snr, "iteration": i, "R1_swing": boot[i, s_idx, 0], "R2_swing": boot[i, s_idx, 1], "R1_minus_R2": diff[i]} for i in range(BOOTSTRAPS))

    diff_all = boot[:, :, 0].mean(axis=1) - boot[:, :, 1].mean(axis=1)
    low, high = percentile_ci(diff_all)
    summary_rows.append({
        "analysis_scope": "mean_over_4_SNR_levels",
        "snr_db": "20,10,0,-5",
        "metric": "mean mAP@10 relative-retention swing across 5 ITERA habitat profiles",
        "R1_generic_mean_swing": float(observed[:, 0].mean()),
        "R2_bioacoustic_mean_swing": float(observed[:, 1].mean()),
        "R1_minus_R2_effect": float(observed[:, 0].mean() - observed[:, 1].mean()),
        "ci95_low": low,
        "ci95_high": high,
        "bootstrap_two_sided_p": p_from_bootstrap(diff_all),
        "bootstrap_iterations": BOOTSTRAPS,
        "queries": len(ids),
        "noise_repeats_per_habitat": 4,
        "habitats": len(HABITATS),
        "supports_H3_at_alpha_0_05": bool(low > 0),
    })
    summary = pd.DataFrame(summary_rows)
    bootstrap = pd.DataFrame(boot_rows)

    retention_rows = []
    for r_idx, rep in enumerate(PRIMARY_REPS):
        for s_idx, snr in enumerate(SNRS):
            clean_mean = clean[r_idx].mean()
            for repeat in range(4):
                for h_idx, habitat in enumerate(HABITATS):
                    noisy_mean = noisy[r_idx, s_idx, repeat, h_idx].mean()
                    retention_rows.append({
                        "representation": rep,
                        "representation_class": "generic_audio" if rep == "R1" else "bioacoustic",
                        "snr_db": snr,
                        "repeat_id": repeat,
                        "habitat": habitat,
                        "clean_mean_AP10": clean_mean,
                        "noisy_mean_AP10": noisy_mean,
                        "relative_retention": noisy_mean / clean_mean,
                    })
    retention = pd.DataFrame(retention_rows)

    summary_path = run_tables / "h3_stability_summary.csv"
    boot_path = run_tables / "h3_bootstrap_distribution.csv"
    retention_path = run_tables / "h3_retention_by_habitat_repeat.csv"
    summary.to_csv(summary_path, index=False)
    bootstrap.to_csv(boot_path, index=False)
    retention.to_csv(retention_path, index=False)

    # Single report-ready figure: profile means and range per SNR.
    fig, axes = plt.subplots(2, 2, figsize=(13, 8), sharey=False)
    colors = {"R1": "#d95f02", "R2": "#1b9e77"}
    for ax, (s_idx, snr) in zip(axes.flat, enumerate(SNRS)):
        means = retention.loc[retention["snr_db"].eq(snr)].groupby(["representation", "habitat"], sort=False)["relative_retention"].mean().reset_index()
        for rep in PRIMARY_REPS:
            series = means.loc[means["representation"].eq(rep)].set_index("habitat").reindex(HABITATS)["relative_retention"]
            ax.plot(range(len(HABITATS)), series.values, marker="o", linewidth=2, label=rep, color=colors[rep])
            ax.fill_between(range(len(HABITATS)), series.min(), series.max(), color=colors[rep], alpha=.08)
        effect = summary.loc[summary["analysis_scope"].eq("per_snr") & summary["snr_db"].eq(snr)].iloc[0]
        ax.set_title(f"SNR {snr} dB | swing R1={effect['R1_generic_mean_swing']:.3f}, R2={effect['R2_bioacoustic_mean_swing']:.3f}")
        ax.set_xticks(range(len(HABITATS)), [x.replace("_", " ") for x in HABITATS], rotation=25, ha="right")
        ax.set_ylabel("mAP@10 relative retention")
        ax.grid(axis="y", alpha=.25)
    axes[0, 0].legend(title="Representation")
    fig.suptitle("H3 — Stability of mAP@10 retention across ITERA habitat noise profiles\n(mean over four independently sampled noise segments)", fontsize=13)
    fig.tight_layout()
    fig_path = run_figures / "h3_habitat_retention_stability.png"
    fig.savefig(fig_path, dpi=220, bbox_inches="tight")
    plt.close(fig)

    # Report copies are new named files, never replacements of older results.
    report_summary = TABLES / "24_h3_habitat_profile_stability.csv"
    report_retention = TABLES / "25_h3_retention_by_habitat_repeat.csv"
    report_boot = TABLES / "26_h3_bootstrap_distribution.csv"
    report_figure = FIGURES / "15_h3_habitat_retention_stability.png"
    for source, target in ((summary_path, report_summary), (retention_path, report_retention), (boot_path, report_boot), (fig_path, report_figure)):
        if target.exists():
            if sha256(source) != sha256(target):
                raise FileExistsError(f"Refusing to replace a different report artifact: {target}")
        else:
            target.write_bytes(source.read_bytes())

    metadata = {
        "analysis": "H3 habitat-profile stability",
        "source_experiment": str(E4.relative_to(ROOT)).replace("\\", "/"),
        "source_raw_sha256": inputs,
        "immutable_source_note": "Original E4 files were read only; no E4 run file was modified.",
        "comparison": "R1 generic pretrained audio (PANN) versus R2 bioacoustic pretrained embedding (BirdNET V2.4)",
        "outcome_metric": "mAP@10 relative-retention swing = max habitat retention - min habitat retention, averaged over four noise repeats",
        "inference": f"paired query bootstrap percentile CI, {BOOTSTRAPS} resamples, seed {SEED}; H3 supported when R1-R2 swing CI lower bound > 0",
        "unit": "311 shared query recordings; 5 habitats; 4 noise-segment repeats per habitat and SNR",
        "outputs": {"summary": str(summary_path.relative_to(ROOT)).replace("\\", "/"), "retention": str(retention_path.relative_to(ROOT)).replace("\\", "/"), "bootstrap": str(boot_path.relative_to(ROOT)).replace("\\", "/"), "figure": str(fig_path.relative_to(ROOT)).replace("\\", "/")},
    }
    (run / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps({"run": str(run.relative_to(ROOT)), "summary": summary.to_dict(orient="records")}, indent=2))

if __name__ == "__main__":
    main()
