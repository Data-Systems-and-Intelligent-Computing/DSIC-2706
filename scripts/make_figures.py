"""
Script: scripts/make_figures.py
Fungsi: Menghasilkan gambar publikasi ilmiah resolusi tinggi (300 DPI)
dengan pita selang kepercayaan 95% (95% Bootstrap Confidence Interval).
Menyelesaikan temuan M-03, m-06, dan m-07.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "results/raw"
FIG_DIR = PROJECT_ROOT / "results/figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Bootstrap Confidence Interval 95%
def compute_bootstrap_ci(rep_code, condition, n_boot=1000, ci=0.95):
    f_path = RAW_DIR / f"{rep_code}_{condition}_raw.csv"
    if not f_path.exists():
        return np.nan, np.nan, np.nan
    df_raw = pd.read_csv(f_path)
    scores = df_raw["AP@10"].values
    n = len(scores)

    rng = np.random.RandomState(42)
    boot_means = []
    for _ in range(n_boot):
        sample = rng.choice(scores, size=n, replace=True)
        boot_means.append(np.mean(sample))

    boot_means = np.sort(boot_means)
    alpha = (1 - ci) / 2
    low = boot_means[int(alpha * n_boot)]
    high = boot_means[int((1 - alpha) * n_boot)]
    mean_val = np.mean(scores)
    return mean_val, low, high

def main():
    print("=" * 60)
    print("=== MEMBUAT GAMBAR GRAFIK DENGAN PITA GALAT 95% CI ===")
    print("=" * 60)

    conditions = ["Clean", "SNR_20dB", "SNR_10dB", "SNR_0dB", "SNR_-5dB"]
    snr_x = [30, 20, 10, 0, -5]

    colors = {
        "R0": "#e74c3c", # Merah
        "R1": "#3498db", # Biru
        "R2": "#2ecc71", # Hijau
        "R3": "#95a5a6", # Abu-abu
    }
    labels = {
        "R0": "R0: MFCC Baseline (40-d)",
        "R1": "R1: PANNs CNN14 (2048-d)",
        "R2": "R2: BirdNET V2.4 (1024-d)",
        "R3": "R3: Random Control (40-d)"
    }

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=300)

    # 1. mAP@10 dengan 95% CI Band
    for rep in ["R2", "R1", "R0", "R3"]:
        means, lows, highs = [], [], []
        for cond in conditions:
            m, l, h = compute_bootstrap_ci(rep, cond)
            means.append(m)
            lows.append(l)
            highs.append(h)
        ax1.plot(snr_x, means, 'o-', color=colors[rep], label=labels[rep], linewidth=2.2, markersize=6)
        ax1.fill_between(snr_x, lows, highs, color=colors[rep], alpha=0.18)

    ax1.set_xlabel("Signal-to-Noise Ratio (SNR in dB)")
    ax1.set_ylabel("Mean Average Precision (mAP@10)")
    ax1.set_title("(a) Retrieval Robustness across Noise (95% CI)")
    ax1.set_xticks(snr_x)
    ax1.set_xticklabels(["Clean", "20 dB", "10 dB", "0 dB", "-5 dB"])
    ax1.set_ylim(-0.02, 1.02)
    ax1.legend(loc="upper left", frameon=True)

    # 2. Relative Retention Curve (%)
    for rep in ["R2", "R1", "R0", "R3"]:
        clean_m = compute_bootstrap_ci(rep, "Clean")[0]
        ret_pct = []
        for cond in conditions:
            m = compute_bootstrap_ci(rep, cond)[0]
            ret_pct.append((m / max(clean_m, 1e-6)) * 100)
        ax2.plot(snr_x, ret_pct, 's--', color=colors[rep], label=labels[rep], linewidth=2.0, markersize=6)

    ax2.set_xlabel("Signal-to-Noise Ratio (SNR in dB)")
    ax2.set_ylabel("Relative Retention (%)")
    ax2.set_title("(b) Relative Retention Curve (% of Clean mAP)")
    ax2.set_xticks(snr_x)
    ax2.set_xticklabels(["Clean", "20 dB", "10 dB", "0 dB", "-5 dB"])
    ax2.set_ylim(0, 110)
    ax2.axhline(100, color='gray', linestyle=':', alpha=0.6)
    ax2.legend(loc="lower left", frameon=True)

    plt.tight_layout()
    out_path = FIG_DIR / "robustness_curve_map10.png"
    plt.savefig(out_path, dpi=300)
    print(f"[+] Gambar berhasil disimpan di: {out_path}")

    paper_fig = PROJECT_ROOT / "paper/figures/robustness_curve_map10.png"
    if paper_fig.parent.exists():
        import shutil
        shutil.copy(out_path, paper_fig)
        print(f"[+] Disinkronkan ke: {paper_fig}")

    # Simpan juga relative retention curve secara mandiri
    fig_ret, ax_ret = plt.subplots(figsize=(7, 5), dpi=300)
    for rep in ["R2", "R1", "R0", "R3"]:
        clean_m = compute_bootstrap_ci(rep, "Clean")[0]
        ret_pct = []
        for cond in conditions:
            m = compute_bootstrap_ci(rep, cond)[0]
            ret_pct.append((m / max(clean_m, 1e-6)) * 100)
        ax_ret.plot(snr_x, ret_pct, 's--', color=colors[rep], label=labels[rep], linewidth=2.0, markersize=6)
    ax_ret.set_xlabel("Signal-to-Noise Ratio (SNR in dB)")
    ax_ret.set_ylabel("Relative Retention (%)")
    ax_ret.set_title("Relative Retention Curve (% of Clean mAP)")
    ax_ret.set_xticks(snr_x)
    ax_ret.set_xticklabels(["Clean", "20 dB", "10 dB", "0 dB", "-5 dB"])
    ax_ret.set_ylim(0, 110)
    ax_ret.axhline(100, color='gray', linestyle=':', alpha=0.6)
    ax_ret.legend(loc="lower left", frameon=True)
    plt.tight_layout()
    ret_path = FIG_DIR / "relative_retention_curve.png"
    plt.savefig(ret_path, dpi=300)
    paper_ret = PROJECT_ROOT / "paper/figures/relative_retention_curve.png"
    if paper_ret.parent.exists():
        import shutil
        shutil.copy(ret_path, paper_ret)
    plt.close()

    # Buat Clean Retrieval Benchmark Bar Chart (E1)
    clean_csv = PROJECT_ROOT / "results/processed/clean_retrieval_table.csv"
    if clean_csv.exists():
        df_clean = pd.read_csv(clean_csv)
        fig_clean, ax_c = plt.subplots(figsize=(8, 5), dpi=300)
        x_pos = np.arange(len(df_clean))
        maps = df_clean["mAP@10"].values
        top1s = [float(str(t).replace("%", "")) / 100.0 for t in df_clean["Top-1 (%)"].values]
        
        width = 0.35
        b1 = ax_c.bar(x_pos - width/2, maps, width, label="mAP@10", color="#1b9e77")
        b2 = ax_c.bar(x_pos + width/2, top1s, width, label="Top-1 Accuracy", color="#d95f02")
        
        for b in b1:
            h = b.get_height()
            ax_c.annotate(f"{h:.3f}", (b.get_x() + b.get_width() / 2, h), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=9)
        for b in b2:
            h = b.get_height()
            ax_c.annotate(f"{h*100:.1f}%", (b.get_x() + b.get_width() / 2, h), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=9)
            
        ax_c.set_xticks(x_pos)
        ax_c.set_xticklabels(df_clean["Kode"] + "\n" + df_clean["Arsitektur"].str.split(" ").str[0])
        ax_c.set_ylabel("Nilai Metrik (0 - 1.0)")
        ax_c.set_title("E1: Clean Retrieval Performance Benchmark", fontweight="bold")
        ax_c.set_ylim(0, 1.15)
        ax_c.legend()
        plt.tight_layout()
        c_path = FIG_DIR / "clean_retrieval_benchmark.png"
        plt.savefig(c_path, dpi=300)
        paper_c = PROJECT_ROOT / "paper/figures/clean_retrieval_benchmark.png"
        if paper_c.parent.exists():
            import shutil
            shutil.copy(c_path, paper_c)
        plt.close()
        print(f"[+] Grafik E1 berhasil disimpan di: {c_path}")

if __name__ == "__main__":
    main()
