"""
Script: scripts/build_e3_notebook.py
Fungsi: Membangun dan mengeksekusi Jupyter Notebook notebooks/E3_Open_Set_Threshold.ipynb.
"""

import os
import sys
from pathlib import Path
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks/E3_Open_Set_Threshold.ipynb"

def create_and_execute_notebook():
    print("[*] Membangun notebooks/E3_Open_Set_Threshold.ipynb...")
    nb = nbf.v4.new_notebook()

    cells = []

    # Markdown Header
    cells.append(nbf.v4.new_markdown_cell(
        "# Eksperimen E3: Evaluasi Penolakan Kelas Terbuka (Open-Set Rejection) & Kalibrasi Ambang Batas (τ*)\n\n"
        "**Topik Penelitian:** Ketahanan Representasi Audio terhadap Derau dan Pergeseran Domain untuk Pencarian Kemiripan Bioakustik\n\n"
        "### Pertanyaan Penelitian Terkait (Sub-RQ2):\n"
        "> *Apakah ambang batas kemiripan (similarity threshold τ) yang dikalibrasi secara objektif pada subset terpisah "
        "mampu menolak sinyal audio asing (unknown/background noise) secara andal tanpa menyebabkan peningkatan False Positive Rate "
        "yang berlebihan ketika tingkat derau lingkungan memburuk (Clean s.d. -5 dB SNR)?*\n\n"
        "### Hipotesis (H4):\n"
        "> *Ambang batas penolakan τ* yang dikalibrasi pada kondisi bersih akan mengalami inflasi False Positive "
        "yang signifikan pada representasi generik/MFCC saat derau meningkat, sementara representasi bioakustik (BirdNET) "
        "mempertahankan selektivitas penolakan yang lebih stabil.*\n\n"
        "---"
    ))

    # Cell 1: Environment & Manifest Loading
    c1 = (
        "import os\n"
        "import sys\n"
        "from pathlib import Path\n"
        "import numpy as np\n"
        "import pandas as pd\n"
        "import matplotlib.pyplot as plt\n"
        "import yaml\n"
        "\n"
        "NOTEBOOK_DIR = Path(os.getcwd())\n"
        "REPO_ROOT = NOTEBOOK_DIR.parent if NOTEBOOK_DIR.name == 'notebooks' else NOTEBOOK_DIR\n"
        "if str(REPO_ROOT) not in sys.path:\n"
        "    sys.path.insert(0, str(REPO_ROOT))\n"
        "\n"
        "MANIFEST_DIR = REPO_ROOT / 'data/manifests'\n"
        "PROCESSED_DIR = REPO_ROOT / 'results/processed'\n"
        "RAW_DIR = REPO_ROOT / 'results/raw'\n"
        "FIGURES_DIR = REPO_ROOT / 'results/figures'\n"
        "PAPER_FIG_DIR = REPO_ROOT / 'paper/figures'\n"
        "FIGURES_DIR.mkdir(parents=True, exist_ok=True)\n"
        "PAPER_FIG_DIR.mkdir(parents=True, exist_ok=True)\n"
        "\n"
        "df_split = pd.read_csv(MANIFEST_DIR / 'dataset_split.csv')\n"
        "df_unk = pd.read_csv(MANIFEST_DIR / 'unknown_open_set_manifest.csv')\n"
        "\n"
        "print(f'[+] Dataset Split: {len(df_split):,} baris')\n"
        "print(f'    - Gallery: {len(df_split[df_split[\"split_role\"] == \"gallery\"]):,}')\n"
        "print(f'    - Calibration Known: {len(df_split[df_split[\"split_role\"] == \"calibration\"]):,}')\n"
        "print(f'    - Query Clean Known: {len(df_split[df_split[\"split_role\"] == \"query_clean\"]):,}')\n"
        "print(f'[+] Unknown Open-Set Manifest: {len(df_unk):,} baris')\n"
        "print(f'    - Unknown Calibration: {len(df_unk[df_unk[\"split_role\"] == \"unknown_calibration\"]):,}')\n"
        "print(f'    - Unknown Test: {len(df_unk[df_unk[\"split_role\"] == \"unknown_test\"]):,}')"
    )
    cells.append(nbf.v4.new_code_cell(c1))

    # Cell 2: Calibration Summary & Frozen Thresholds
    c2 = (
        "with open(REPO_ROOT / 'configs/thresholds.yaml', 'r') as f:\n"
        "    thresholds_cfg = yaml.safe_load(f)\n"
        "\n"
        "df_calib = pd.read_csv(PROCESSED_DIR / 'calibration_summary_table.csv')\n"
        "print('=== HASIL KALIBRASI AMBANG BATAS OBJEKTIF (YOUDEN J) PADA SUBSET TERPISAH ===')\n"
        "display(df_calib[['representation', 'frozen_tau', 'calib_youden_j', 'calib_auroc', 'calib_f1', 'calib_recall', 'calib_fpr']])"
    )
    cells.append(nbf.v4.new_code_cell(c2))

    # Cell 3: Plot Calibration Metrics
    c3 = (
        "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n"
        "fig, axes = plt.subplots(1, 2, figsize=(14, 5))\n"
        "\n"
        "# Subplot 1: Youden's J & AUROC per Representasi\n"
        "x = np.arange(len(df_calib))\n"
        "width = 0.35\n"
        "axes[0].bar(x - width/2, df_calib['calib_auroc'], width, label='Calibration AUROC', color='#1f77b4', alpha=0.85)\n"
        "axes[0].bar(x + width/2, df_calib['calib_youden_j'], width, label=\"Youden's J (TPR - FPR)\", color='#2ca02c', alpha=0.85)\n"
        "axes[0].set_xticks(x)\n"
        "axes[0].set_xticklabels(df_calib['representation'], fontsize=11, fontweight='bold')\n"
        "axes[0].set_ylabel('Score', fontsize=11)\n"
        "axes[0].set_title('A. Kemampuan Separasi pada Subset Kalibrasi Terpisah', fontsize=12, fontweight='bold')\n"
        "axes[0].set_ylim(0, 1.0)\n"
        "axes[0].legend(fontsize=10)\n"
        "for i, r in df_calib.iterrows():\n"
        "    axes[0].text(i - width/2, r['calib_auroc'] + 0.02, f\"{r['calib_auroc']:.3f}\", ha='center', fontsize=9)\n"
        "    axes[0].text(i + width/2, r['calib_youden_j'] + 0.02, f\"{r['calib_youden_j']:.3f}\", ha='center', fontsize=9)\n"
        "\n"
        "# Subplot 2: Frozen Threshold Tau* & Komposisi TPR vs FPR\n"
        "axes[1].bar(x - width/2, df_calib['calib_recall'], width, label='Target Recall (TPR)', color='#3b528b', alpha=0.85)\n"
        "axes[1].bar(x + width/2, df_calib['calib_fpr'], width, label='False Positive Rate (FPR)', color='#d62728', alpha=0.85)\n"
        "axes[1].set_xticks(x)\n"
        "axes[1].set_xticklabels([f\"{r['representation']}\\n(tau*={r['frozen_tau']:.3f})\" for _, r in df_calib.iterrows()], fontsize=10)\n"
        "axes[1].set_ylabel('Rate', fontsize=11)\n"
        "axes[1].set_title('B. Trade-off Sensitivitas vs Spesifisitas pada tau* Beku', fontsize=12, fontweight='bold')\n"
        "axes[1].set_ylim(0, 1.0)\n"
        "axes[1].legend(fontsize=10)\n"
        "for i, r in df_calib.iterrows():\n"
        "    axes[1].text(i - width/2, r['calib_recall'] + 0.02, f\"{r['calib_recall']:.2f}\", ha='center', fontsize=9)\n"
        "    axes[1].text(i + width/2, r['calib_fpr'] + 0.02, f\"{r['calib_fpr']:.2f}\", ha='center', fontsize=9)\n"
        "\n"
        "plt.tight_layout()\n"
        "plt.savefig(FIGURES_DIR / 'e3_calibration_roc_youden.png', dpi=300)\n"
        "plt.savefig(PAPER_FIG_DIR / 'e3_calibration_roc_youden.png', dpi=300)\n"
        "plt.show()"
    )
    cells.append(nbf.v4.new_code_cell(c3))

    # Cell 4: Test Set Transfer Table
    c4 = (
        "df_transfer = pd.read_csv(PROCESSED_DIR / 'threshold_transfer_table.csv')\n"
        "print('=== HASIL EVALUASI TRANSFER AMBANG BATAS BEKU PADA TEST SET (N=400: 200 KNOWN + 200 UNKNOWN) ===')\n"
        "display(df_transfer[['representation', 'condition', 'snr_db', 'AUROC', 'AUPRC', 'Recall_at_tau', 'False_Positive_Rate', 'F1_at_tau', 'delta_Recall', 'delta_FPR']])"
    )
    cells.append(nbf.v4.new_code_cell(c4))

    # Cell 5: Plot Transfer Performance Across SNR
    c5 = (
        "fig, axes = plt.subplots(1, 3, figsize=(18, 5))\n"
        "\n"
        "conditions = ['Clean', 'SNR_20dB', 'SNR_10dB', 'SNR_0dB', 'SNR_-5dB']\n"
        "cond_labels = ['Clean', '+20 dB', '+10 dB', '0 dB', '-5 dB']\n"
        "colors = {'R2': '#1b9e77', 'R1': '#d95f02', 'R0': '#7570b3', 'R3': '#e7298a'}\n"
        "markers = {'R2': 'o', 'R1': 's', 'R0': '^', 'R3': 'x'}\n"
        "labels = {\n"
        "    'R2': 'R2 (BirdNET Bioacoustic)',\n"
        "    'R1': 'R1 (PANNs Generic)',\n"
        "    'R0': 'R0 (MFCC Baseline)',\n"
        "    'R3': 'R3 (Random Control)'\n"
        "}\n"
        "\n"
        "# Subplot 1: AUROC vs SNR\n"
        "for rep in ['R2', 'R1', 'R0', 'R3']:\n"
        "    sub = df_transfer[df_transfer['representation'] == rep]\n"
        "    val_map = {r['condition']: r['AUROC'] for _, r in sub.iterrows()}\n"
        "    y_vals = [val_map[c] for c in conditions]\n"
        "    axes[0].plot(cond_labels, y_vals, marker=markers[rep], color=colors[rep], label=labels[rep], linewidth=2.2, markersize=7)\n"
        "axes[0].set_title('A. Discriminative Power (AUROC) vs Derau', fontsize=12, fontweight='bold')\n"
        "axes[0].set_ylabel('AUROC', fontsize=11)\n"
        "axes[0].set_xlabel('Tingkat Derau (SNR)', fontsize=11)\n"
        "axes[0].set_ylim(0.4, 1.0)\n"
        "axes[0].axhline(0.5, color='gray', linestyle='--', alpha=0.7, label='Chance Level (0.50)')\n"
        "axes[0].legend(fontsize=9, loc='lower left')\n"
        "\n"
        "# Subplot 2: Target Recall at Frozen Tau*\n"
        "for rep in ['R2', 'R1', 'R0', 'R3']:\n"
        "    sub = df_transfer[df_transfer['representation'] == rep]\n"
        "    val_map = {r['condition']: r['Recall_at_tau'] for _, r in sub.iterrows()}\n"
        "    y_vals = [val_map[c] for c in conditions]\n"
        "    axes[1].plot(cond_labels, y_vals, marker=markers[rep], color=colors[rep], label=labels[rep], linewidth=2.2, markersize=7)\n"
        "axes[1].set_title('B. Target Retention (Recall@tau*) vs Derau', fontsize=12, fontweight='bold')\n"
        "axes[1].set_ylabel('Recall pada tau* Beku', fontsize=11)\n"
        "axes[1].set_xlabel('Tingkat Derau (SNR)', fontsize=11)\n"
        "axes[1].set_ylim(0.0, 1.05)\n"
        "axes[1].legend(fontsize=9, loc='lower left')\n"
        "\n"
        "# Subplot 3: False Positive Rate (FPR) vs Derau (Krusial untuk H4!)\n"
        "for rep in ['R2', 'R1', 'R0', 'R3']:\n"
        "    sub = df_transfer[df_transfer['representation'] == rep]\n"
        "    val_map = {r['condition']: r['False_Positive_Rate'] for _, r in sub.iterrows()}\n"
        "    y_vals = [val_map[c] for c in conditions]\n"
        "    axes[2].plot(cond_labels, y_vals, marker=markers[rep], color=colors[rep], label=labels[rep], linewidth=2.2, markersize=7)\n"
        "axes[2].set_title('C. False Alarm Rate (FPR) vs Derau (Uji H4)', fontsize=12, fontweight='bold')\n"
        "axes[2].set_ylabel('False Positive Rate (FPR)', fontsize=11)\n"
        "axes[2].set_xlabel('Tingkat Derau (SNR)', fontsize=11)\n"
        "axes[2].set_ylim(0.0, 1.0)\n"
        "axes[2].legend(fontsize=9, loc='upper left')\n"
        "\n"
        "plt.tight_layout()\n"
        "plt.savefig(FIGURES_DIR / 'e3_threshold_transfer_snr.png', dpi=300)\n"
        "plt.savefig(PAPER_FIG_DIR / 'e3_threshold_transfer_snr.png', dpi=300)\n"
        "plt.show()"
    )
    cells.append(nbf.v4.new_code_cell(c5))

    # Cell 6: Markdown Discussion
    cells.append(nbf.v4.new_markdown_cell(
        "### Pembahasan dan Temuan Kunci Eksperimen E3:\n\n"
        "1. **Keabsahan Metodologi (Strict Split & No Snooping):**\n"
        "   - Ambang batas optimal $\\tau^*$ diperoleh secara empiris melalui kurva ROC dan optimasi Youden's Index ($J = \\text{TPR} - \\text{FPR}$) "
        "pada subset kalibrasi yang terpisah ($N=498$ target bird positif dan $N=498$ kontrol negatif unknown: 249 derau ITERA + 249 spesies non-target).\n"
        "   - Nilai $\\tau^*$ yang diperoleh dibekukan secara permanen: $R_2 = 0.7128$, $R_1 = 0.9117$, $R_0 = 0.9953$, dan $R_3 = 0.5090$.\n\n"
        "2. **Jawaban terhadap Sub-RQ2 & Hipotesis H4:**\n"
        "   - **Divergensi Perilaku Ekstrem antara Representasi Generik ($R_1$) dan Bioakustik ($R_2$):**\n"
        "     - Pada $R_1$ (PANNs CNN14), ketika SNR memburuk ke -5 dB, FPR melonjak secara drastis dari **41.5% menjadi 81.5%** (inflasi $\\Delta\\text{FPR} = +40.0\\%$). "
        "Ini membuktikan fenomena kerentanan representasi audio generik: derau lingkungan membuat model memetakan sinyal asing ke wilayah fitur berdensitas tinggi, "
        "sehingga false alarm mendominasi sistem.\n"
        "     - Sebaliknya, pada $R_2$ (BirdNET), representasi mempertahankan kemampuan diskriminasi yang jauh lebih tinggi (AUROC tetap di kisaran 0.7575 s.d. 0.8849). "
        "FPR $R_2$ bahkan menyusut secara konservatif dari **28.5% ke 9.5%** pada SNR -5 dB (penurunan skor kosinus global), meskipun hal ini diiringi kompromi penurunan Target Recall ke 44.5%.\n"
        "   - **Kontrol Acak ($R_3$) & MFCC ($R_0$):**\n"
        "     - $R_3$ memiliki AUROC $\\approx 0.50$ pada seluruh kondisi (performa tebakan acak murni).\n"
        "     - $R_0$ (MFCC) mengalami degradasi separasi parah dengan FPR mencapai 75.5% pada SNR 0 dB.\n"
    ))

    nb.cells = cells

    # Simpan notebook
    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"[+] Berhasil menulis struktur notebook: {NOTEBOOK_PATH}")

    # Eksekusi notebook agar memiliki output nyata
    print("[*] Mengeksekusi notebook untuk menghasilkan output saintifik...")
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    ep.preprocess(nb, {"metadata": {"path": str(PROJECT_ROOT / "notebooks")}})

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"[+] Eksekusi sukses! Notebook telah dilengkapi visualisasi grafik dan tabel.")

if __name__ == "__main__":
    create_and_execute_notebook()
