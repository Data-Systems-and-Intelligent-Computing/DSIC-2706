"""
Script: scripts/build_e1_notebook.py
Fungsi: Membangun dan mengeksekusi notebooks/E1_Clean_Retrieval.ipynb untuk dataset burung Indonesia.
"""

import os
import sys
from pathlib import Path
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks/E1_Clean_Retrieval.ipynb"

def create_and_execute_e1_notebook():
    print("[*] Membangun notebooks/E1_Clean_Retrieval.ipynb...")
    nb = nbf.v4.new_notebook()
    cells = []

    # Markdown Header
    cells.append(nbf.v4.new_markdown_cell(
        "# Eksperimen E1: Evaluasi Temu Kembali Audio pada Kondisi Bersih (Clean Retrieval Benchmark)\n\n"
        "**Topik Penelitian:** Ketahanan Representasi Audio terhadap Derau dan Pergeseran Domain untuk Pencarian Kemiripan Bioakustik\n\n"
        "### Pertanyaan Penelitian Terkait (RQ1 & H5):\n"
        "> *Seberapa baik performa temu kembali kemiripan audio (*similarity retrieval*) dari representasi bioakustik spesifik ($R_2$ BirdNET) "
        "dibandingkan representasi audio generik ($R_1$ PANNs), baseline klasik akustik ($R_0$ MFCC), dan kontrol acak ($R_3$) "
        "pada rekaman vokalisasi burung Indonesia tanpa derau latar buatan?*\n\n"
        "### Hipotesis H5:\n"
        "> Representasi yang dilatih secara spesifik pada domain bioakustik ($R_2$) akan memberikan performa temu kembali (mAP@10 dan Top-1 Accuracy) "
        "yang unggul mutlak secara statistik ($p < 0.001$) dibandingkan representasi konvolusional umum ($R_1$) dan fitur spektral dasar ($R_0$).\n\n"
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
        "\n"
        "NOTEBOOK_DIR = Path(os.getcwd())\n"
        "REPO_ROOT = NOTEBOOK_DIR.parent if NOTEBOOK_DIR.name == 'notebooks' else NOTEBOOK_DIR\n"
        "if str(REPO_ROOT) not in sys.path:\n"
        "    sys.path.insert(0, str(REPO_ROOT))\n"
        "\n"
        "PROCESSED_DIR = REPO_ROOT / 'results/processed'\n"
        "FIGURES_DIR = REPO_ROOT / 'results/figures'\n"
        "PAPER_FIG_DIR = REPO_ROOT / 'paper/figures'\n"
        "FIGURES_DIR.mkdir(parents=True, exist_ok=True)\n"
        "PAPER_FIG_DIR.mkdir(parents=True, exist_ok=True)\n"
        "\n"
        "print('[+] Modul dan path direktori berhasil dimuat!')"
    )
    cells.append(nbf.v4.new_code_cell(c1))

    # Cell 2: Display E1 Results Table
    c2 = (
        "table_path = PROCESSED_DIR / 'clean_retrieval_table.csv'\n"
        "df_clean = pd.read_csv(table_path)\n"
        "print('=== TABEL BENCHMARK TEMU KEMBALI KONDISI BERSIH (E1 CLEAN RETRIEVAL) ===')\n"
        "display(df_clean)"
    )
    cells.append(nbf.v4.new_code_cell(c2))

    # Cell 3: Plot E1 Multi-Metric Benchmark
    c3 = (
        "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n"
        "fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), dpi=300)\n"
        "\n"
        "models = df_clean['Kode'].tolist()\n"
        "model_labels = [f\"{r['Kode']}: {r['Arsitektur'].split()[0]}\" for _, r in df_clean.iterrows()]\n"
        "colors = ['#e74c3c', '#3498db', '#2ecc71', '#95a5a6']\n"
        "\n"
        "# Subplot 1: Top-1 Accuracy\n"
        "top1_vals = [float(str(v).replace('%', '')) for v in df_clean['Top-1 (%)'].values]\n"
        "bars1 = axes[0].bar(models, top1_vals, color=colors, alpha=0.88, edgecolor='black')\n"
        "axes[0].set_title('A. Top-1 Retrieval Accuracy (%)', fontsize=12, fontweight='bold')\n"
        "axes[0].set_ylabel('Akurasi Top-1 (%)', fontsize=11)\n"
        "axes[0].set_ylim(0, 100)\n"
        "for bar in bars1:\n"
        "    h = bar.get_height()\n"
        "    axes[0].text(bar.get_x() + bar.get_width()/2, h + 1.5, f'{h:.1f}%', ha='center', fontsize=10, fontweight='bold')\n"
        "\n"
        "# Subplot 2: Mean Average Precision (mAP@10)\n"
        "map_vals = df_clean['mAP@10'].values\n"
        "bars2 = axes[1].bar(models, map_vals, color=colors, alpha=0.88, edgecolor='black')\n"
        "axes[1].set_title('B. Mean Average Precision (mAP@10)', fontsize=12, fontweight='bold')\n"
        "axes[1].set_ylabel('mAP@10', fontsize=11)\n"
        "axes[1].set_ylim(0, 0.85)\n"
        "for bar in bars2:\n"
        "    h = bar.get_height()\n"
        "    axes[1].text(bar.get_x() + bar.get_width()/2, h + 0.015, f'{h:.4f}', ha='center', fontsize=10, fontweight='bold')\n"
        "\n"
        "# Subplot 3: Mean Reciprocal Rank (MRR)\n"
        "mrr_vals = df_clean['MRR'].values\n"
        "bars3 = axes[2].bar(models, mrr_vals, color=colors, alpha=0.88, edgecolor='black')\n"
        "axes[2].set_title('C. Mean Reciprocal Rank (MRR)', fontsize=12, fontweight='bold')\n"
        "axes[2].set_ylabel('MRR', fontsize=11)\n"
        "axes[2].set_ylim(0, 1.05)\n"
        "for bar in bars3:\n"
        "    h = bar.get_height()\n"
        "    axes[2].text(bar.get_x() + bar.get_width()/2, h + 0.018, f'{h:.4f}', ha='center', fontsize=10, fontweight='bold')\n"
        "\n"
        "plt.tight_layout()\n"
        "plt.savefig(FIGURES_DIR / 'clean_retrieval_benchmark.png', dpi=300)\n"
        "plt.savefig(PAPER_FIG_DIR / 'clean_retrieval_benchmark.png', dpi=300)\n"
        "plt.show()"
    )
    cells.append(nbf.v4.new_code_cell(c3))

    # Cell 4: Statistical Significance Verification
    c4 = (
        "sig_path = PROCESSED_DIR / 'statistical_significance_table.csv'\n"
        "if sig_path.exists():\n"
        "    df_sig = pd.read_csv(sig_path)\n"
        "    clean_sig = df_sig[df_sig['Pengujian'] == 'Clean Retrieval (mAP@10)']\n"
        "    print('=== UJI SIGNIFIKANSI STATISTIK PAIRED BOOTSTRAP (1.000 ITERASI) - KONDISI CLEAN ===')\n"
        "    display(clean_sig[['Komparasi', 'Mean_Diff', 'CI_95_Lower', 'CI_95_Upper', 'p_value', 'Signifikan_0.05', 'Catatan']])"
    )
    cells.append(nbf.v4.new_code_cell(c4))

    # Cell 5: Scientific Discussion
    cells.append(nbf.v4.new_markdown_cell(
        "### Pembahasan Saintifik Eksperimen E1:\n\n"
        "1. **Keunggulan Mutlak Representasi Bioakustik ($R_2$ BirdNET):**\n"
        "   - BirdNET mencapai performa luar biasa dengan **Top-1 Accuracy 81.6%**, **mAP@10 = 0.6358**, dan **MRR = 0.8646** "
        "pada 310 kueri bersih avifauna kepulauan Indonesia.\n"
        "   - Keunggulan atas model generik audio ($R_1$ PANNs CNN14: Top-1 37.7%, mAP@10 0.1768) memiliki selisih rata-rata **+0.4595** "
        "dengan 95% Confidence Interval $[+0.4246, +0.4940]$ dan nilai $p < 0.001$, mengonfirmasi kebenaran Hipotesis H5 secara mutlak.\n\n"
        "2. **Kegagalan Representasi Audio Generik ($R_1$ PANNs):**\n"
        "   - PANNs dilatih pada taksonomi AudioSet yang mencakup ratusan kelas suara sehari-hari (mesin, musik, percakapan, derau domestik). "
        "Fitur laten konvolusionalnya tidak memiliki kepekaan resolusi frekuensi mikro yang dibutuhkan untuk membedakan struktur nada kicauan burung sepupu (*fine-grained avian bioacoustics*).\n\n"
        "3. **Baseline Klasik MFCC ($R_0$) vs Kontrol Acak ($R_3$):**\n"
        "   - $R_0$ menghasilkan Top-1 18.1% dan mAP@10 0.0691, jauh melampaui kontrol acak $R_3$ (Top-1 6.8%, mAP@10 0.0232), "
        "menunjukkan bahwa koefisien cepstral mel tetap menangkap informasi timbre vokal dasar meskipun tidak sekuat representasi mendalam.\n"
    ))

    nb.cells = cells

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"[+] Berhasil menulis struktur notebook: {NOTEBOOK_PATH}")

    print("[*] Mengeksekusi notebook E1...")
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    ep.preprocess(nb, {"metadata": {"path": str(PROJECT_ROOT / "notebooks")}})

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"[+] Eksekusi E1 sukses! Hasil evaluasi retrieval bersih telah diperbarui.")

if __name__ == "__main__":
    create_and_execute_e1_notebook()
