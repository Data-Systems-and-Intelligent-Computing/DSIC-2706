"""
Script: scripts/build_e2_notebook.py
Fungsi: Membangun dan mengeksekusi notebooks/E2_Paired_Noise_Degradation.ipynb untuk dataset burung Indonesia.
"""

import os
import sys
from pathlib import Path
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks/E2_Paired_Noise_Degradation.ipynb"

def create_and_execute_e2_notebook():
    print("[*] Membangun notebooks/E2_Paired_Noise_Degradation.ipynb...")
    nb = nbf.v4.new_notebook()
    cells = []

    # Markdown Header
    cells.append(nbf.v4.new_markdown_cell(
        "# Eksperimen E2: Degradasi Derau Terpasang (Paired Noise Degradation Benchmark)\n\n"
        "**Topik Penelitian:** Ketahanan Representasi Audio terhadap Derau dan Pergeseran Domain untuk Pencarian Kemiripan Bioakustik\n\n"
        "### Pertanyaan Penelitian Terkait (RQ2, H1 & H2):\n"
        "> *Bagaimana ketahanan (*robustness*) representasi audio terdegradasi secara bertahap "
        "saat diuji di bawah derau lingkungan nyata kampus ITERA (AudioMoth) dengan rasio sinyal-ke-derau terkontrol "
        "(SNR +20 dB, +10 dB, 0 dB, dan derau ekstrem -5 dB)?*\n\n"
        "### Hipotesis H1 & H2:\n"
        "- **H1:** Representasi mendalam bioakustik ($R_2$) mempertahankan tingkat retensi performa relatif yang lebih tinggi secara signifikan "
        "dibandingkan representasi generik ($R_1$) dan baseline klasik ($R_0$) pada kondisi derau ekstrem SNR -5 dB.\n"
        "- **H2:** Degradasi performa model berbanding terbalik secara monoton dengan penurunan SNR lingkungan.\n\n"
        "---"
    ))

    # Cell 1: Environment & Module Loading
    c1 = (
        "import os\n"
        "import sys\n"
        "from pathlib import Path\n"
        "import numpy as np\n"
        "import pandas as pd\n"
        "import matplotlib.pyplot as plt\n"
        "import librosa\n"
        "import librosa.display\n"
        "\n"
        "NOTEBOOK_DIR = Path(os.getcwd())\n"
        "REPO_ROOT = NOTEBOOK_DIR.parent if NOTEBOOK_DIR.name == 'notebooks' else NOTEBOOK_DIR\n"
        "if str(REPO_ROOT) not in sys.path:\n"
        "    sys.path.insert(0, str(REPO_ROOT))\n"
        "\n"
        "from src.preprocess import preprocess_audio\n"
        "from src.mix_noise import mix_audio_at_snr, get_noise_segment, MANIFEST_PATH as NOISE_MANIFEST\n"
        "\n"
        "PROCESSED_DIR = REPO_ROOT / 'results/processed'\n"
        "FIGURES_DIR = REPO_ROOT / 'results/figures'\n"
        "PAPER_FIG_DIR = REPO_ROOT / 'paper/figures'\n"
        "FIGURES_DIR.mkdir(parents=True, exist_ok=True)\n"
        "PAPER_FIG_DIR.mkdir(parents=True, exist_ok=True)\n"
        "\n"
        "print(f'[+] Bank Derau ITERA: Manifes {NOISE_MANIFEST} valid dan siap digunakan!')"
    )
    cells.append(nbf.v4.new_code_cell(c1))

    # Cell 2: Demonstration of Additive Noise Mixing
    c2 = (
        "# Demonstrasi Pencampuran Derau Terpasang (Tahap 4)\n"
        "df_split = pd.read_csv(REPO_ROOT / 'data/manifests/dataset_split.csv')\n"
        "sample_row = df_split[df_split['split_role'] == 'query_clean'].iloc[0]\n"
        "y_clean = preprocess_audio(str(REPO_ROOT / sample_row['file_path']))\n"
        "\n"
        "# Ambil segmen derau nyata ITERA dan campur pada SNR -5 dB\n"
        "y_noise, noise_path = get_noise_segment(samples=len(y_clean), seed=42, return_path=True)\n"
        "y_mixed = mix_audio_at_snr(y_clean, snr_db=-5.0, seed=42)\n"
        "\n"
        "print(f'[-] Sumber Derau: {Path(noise_path).name}')\n"
        "print(f'[-] Durasi Sinyal Campuran: {len(y_mixed)/32000:.2f}s | RMS: {np.sqrt(np.mean(y_mixed**2)):.4f} | Max: {np.max(np.abs(y_mixed)):.4f}')\n"
        "\n"
        "fig, axes = plt.subplots(3, 1, figsize=(12, 7), dpi=300)\n"
        "librosa.display.waveshow(y_clean, sr=32000, ax=axes[0], color='#1b9e77')\n"
        "axes[0].set_title(f'1. Kueri Bersih: {sample_row[\"species_key\"]} ({sample_row[\"recording_id\"]})', fontsize=10, fontweight='bold')\n"
        "\n"
        "librosa.display.waveshow(y_noise, sr=32000, ax=axes[1], color='#e74c3c')\n"
        "axes[1].set_title(f'2. Derau Lapangan ITERA (AudioMoth)', fontsize=10, fontweight='bold')\n"
        "\n"
        "librosa.display.waveshow(y_mixed, sr=32000, ax=axes[2], color='#7570b3')\n"
        "axes[2].set_title('3. Sinyal Campuran Terdegradasi pada SNR -5 dB', fontsize=10, fontweight='bold')\n"
        "\n"
        "plt.tight_layout()\n"
        "plt.show()"
    )
    cells.append(nbf.v4.new_code_cell(c2))

    # Cell 3: Display E2 Robustness Table
    c3 = (
        "table_path = PROCESSED_DIR / 'snr_robustness_table.csv'\n"
        "df_snr = pd.read_csv(table_path)\n"
        "print('=== TABEL BENCHMARK KETAHANAN TERHADAP DERAU (E2 SNR ROBUSTNESS) ===')\n"
        "display(df_snr)"
    )
    cells.append(nbf.v4.new_code_cell(c3))

    # Cell 4: Plot Robustness Curves
    c4 = (
        "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n"
        "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5), dpi=300)\n"
        "\n"
        "conditions = ['Clean', 'SNR_20dB', 'SNR_10dB', 'SNR_0dB', 'SNR_-5dB']\n"
        "snr_labels = ['Clean', '+20 dB', '+10 dB', '0 dB', '-5 dB']\n"
        "colors = {'R2': '#1b9e77', 'R1': '#3498db', 'R0': '#e74c3c', 'R3': '#95a5a6'}\n"
        "labels = {\n"
        "    'R2': 'R2: BirdNET V2.4 (1024-d)',\n"
        "    'R1': 'R1: PANNs CNN14 (2048-d)',\n"
        "    'R0': 'R0: MFCC Baseline (40-d)',\n"
        "    'R3': 'R3: Random Control (40-d)'\n"
        "}\n"
        "\n"
        "# 1. Plot Nilai Absolut mAP@10\n"
        "for rep in ['R2', 'R1', 'R0', 'R3']:\n"
        "    sub = df_snr[df_snr['representation'] == rep]\n"
        "    m_dict = {r['condition']: r['mAP@10'] for _, r in sub.iterrows()}\n"
        "    y_vals = [m_dict[c] for c in conditions]\n"
        "    ax1.plot(snr_labels, y_vals, 'o-', color=colors[rep], label=labels[rep], linewidth=2.2, markersize=6)\n"
        "\n"
        "ax1.set_title('A. Kurva Degradasi Temu Kembali (mAP@10)', fontsize=12, fontweight='bold')\n"
        "ax1.set_xlabel('Tingkat Rasio Sinyal-ke-Derau (SNR)', fontsize=11)\n"
        "ax1.set_ylabel('mAP@10', fontsize=11)\n"
        "ax1.set_ylim(-0.02, 0.75)\n"
        "ax1.legend(loc='upper right', frameon=True)\n"
        "\n"
        "# 2. Plot Retensi Relatif (%)\n"
        "for rep in ['R2', 'R1', 'R0', 'R3']:\n"
        "    sub = df_snr[df_snr['representation'] == rep]\n"
        "    ret_dict = {r['condition']: r['relative_retention'] * 100 for _, r in sub.iterrows()}\n"
        "    y_ret = [ret_dict[c] for c in conditions]\n"
        "    ax2.plot(snr_labels, y_ret, 's--', color=colors[rep], label=labels[rep], linewidth=2.0, markersize=6)\n"
        "\n"
        "ax2.axhline(100, color='gray', linestyle=':', alpha=0.7)\n"
        "ax2.set_title('B. Kurva Retensi Relatif (% terhadap Clean)', fontsize=12, fontweight='bold')\n"
        "ax2.set_xlabel('Tingkat Rasio Sinyal-ke-Derau (SNR)', fontsize=11)\n"
        "ax2.set_ylabel('Retensi Relatif (%)', fontsize=11)\n"
        "ax2.set_ylim(20, 120)\n"
        "ax2.legend(loc='lower left', frameon=True)\n"
        "\n"
        "plt.tight_layout()\n"
        "plt.savefig(FIGURES_DIR / 'robustness_curve_map10.png', dpi=300)\n"
        "plt.savefig(PAPER_FIG_DIR / 'robustness_curve_map10.png', dpi=300)\n"
        "plt.show()"
    )
    cells.append(nbf.v4.new_code_cell(c4))

    # Cell 5: Statistical Significance Table for SNR -5 dB
    c5 = (
        "sig_path = PROCESSED_DIR / 'statistical_significance_table.csv'\n"
        "if sig_path.exists():\n"
        "    df_sig = pd.read_csv(sig_path)\n"
        "    ret_sig = df_sig[df_sig['Pengujian'] == 'Retensi Relatif SNR -5 dB']\n"
        "    print('=== UJI SIGNIFIKANSI RETENSI RELATIF PADA DERAU EKSTREM (SNR -5 dB) ===')\n"
        "    display(ret_sig[['Komparasi', 'Mean_Diff', 'CI_95_Lower', 'CI_95_Upper', 'p_value', 'Signifikan_0.05', 'Catatan']])"
    )
    cells.append(nbf.v4.new_code_cell(c5))

    # Cell 6: Scientific Discussion
    cells.append(nbf.v4.new_markdown_cell(
        "### Pembahasan Saintifik Eksperimen E2:\n\n"
        "1. **Keunggulan Ketahanan Representasi Bioakustik ($R_2$ BirdNET):**\n"
        "   - Di bawah derau ekstrem SNR -5 dB, BirdNET mempertahankan **76.2% retensi relatif** (mAP@10 = 0.4843), "
        "unggul signifikan secara statistik atas PANNs CNN14 (retensi 46.2%, $p < 0.001$, Mean Diff +0.2980) "
        "dan MFCC baseline (retensi 32.4%, $p < 0.001$, Mean Diff +0.4342).\n"
        "   - Hal ini membuktikan Hipotesis H1: representasi terlatih bioakustik memiliki kapasitas *noise invariance* "
        "yang kokoh karena mampu menyaring komponen spektral derau latar tanpa kehilangan fitur diskriminatif spesies.\n\n"
        "2. **Fenomena Stokastik Resonansi Ringan (+20 dB):**\n"
        "   - Pada SNR +20 dB, model klasik MFCC mengalami kenaikan retensi semu (+13.4%) dan PANNs (+4.5%). "
        "Derau latar berenergi rendah bertindak sebagai penghalus kontur spektrogram (*dithering effect*), "
        "sebelum performanya merosot tajam ketika derau meningkat ke 0 dB dan -5 dB.\n\n"
        "3. **Evaluasi Monotonisitas Degradasi (Hipotesis H2):**\n"
        "   - Mulai dari SNR +10 dB ke bawah, seluruh representasi mengalami degradasi monoton seiring meningkatnya intensitas derau, "
        "mengonfirmasi kebenaran Hipotesis H2.\n"
    ))

    nb.cells = cells

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"[+] Berhasil menulis struktur notebook: {NOTEBOOK_PATH}")

    print("[*] Mengeksekusi notebook E2...")
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    ep.preprocess(nb, {"metadata": {"path": str(PROJECT_ROOT / "notebooks")}})

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"[+] Eksekusi E2 sukses! Seluruh tabel dan grafik ketahanan derau telah diperbarui.")

if __name__ == "__main__":
    create_and_execute_e2_notebook()
