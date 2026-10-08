"""
Script: scripts/build_e4_notebook.py
Fungsi: Membangun dan mengeksekusi notebooks/E4_Real_Soundscape_Domain_Shift.ipynb dengan perbandingan 4 representasi saintifik dan pembahasan jujur.
"""

import os
import sys
from pathlib import Path
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_PATH = PROJECT_ROOT / "notebooks/E4_Real_Soundscape_Domain_Shift.ipynb"

def create_and_execute_e4_notebook():
    print("[*] Membangun notebooks/E4_Real_Soundscape_Domain_Shift.ipynb...")
    nb = nbf.v4.new_notebook()
    cells = []

    # Markdown Header
    cells.append(nbf.v4.new_markdown_cell(
        "# Eksperimen E4: Sensitivitas Profil Spektral Sumber Derau (Soundscape Tropis vs. Derau ITERA)\n\n"
        "**Topik Penelitian:** Ketahanan Representasi Audio terhadap Derau dan Pergeseran Domain untuk Pencarian Kemiripan Bioakustik\n\n"
        "### Pertanyaan Penelitian Terkait (Sub-RQ4 & H3):\n"
        "> *Seberapa sensitif representasi audio (R0, R1, R2, R3) terhadap perbedaan karakteristik spektral sumber derau "
        "ketika membandingkan derau lapangan terbuka/antropogenik ITERA (E2) dengan derau latar belakang soundscape alam tropis (E4)?*\n\n"
        "### Catatan Integritas Metodologis (Audit Reframing):\n"
        "> Eksperimen E4 menguji sensitivitas terhadap **profil spektral derau latar (noise source spectral sensitivity)** secara aditif terkontrol. "
        "Domain shift in-situ lapangan penuh (melibatkan transmisi jarak fisik, reverberasi kanopi, dan polifoni spesies simultan) "
        "dinyatakan sebagai arah penelitian masa depan (*future work*) karena repositori rekaman lapangan ITERA (`data/itera_soundscape_annotations/`) "
        "belum memiliki anotasi batas waktu-frekuensi (*bounding-box ground truth*).\n\n"
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
        "RAW_DIR = REPO_ROOT / 'results/raw'\n"
        "FIGURES_DIR = REPO_ROOT / 'results/figures'\n"
        "PAPER_FIG_DIR = REPO_ROOT / 'paper/figures'\n"
        "FIGURES_DIR.mkdir(parents=True, exist_ok=True)\n"
        "PAPER_FIG_DIR.mkdir(parents=True, exist_ok=True)\n"
        "\n"
        "print('[+] Seluruh modul dan pustaka berhasil diinisialisasi!')"
    )
    cells.append(nbf.v4.new_code_cell(c1))

    # Cell 2: Comparative Table E2 vs E4
    c2 = (
        "df_e4 = pd.read_csv(PROCESSED_DIR / 'e4_domain_shift_table.csv')\n"
        "print('=== TABEL KOMPARATIF RETRIEVAL: E2 (DERAU ITERA) VS E4 (SOUNDSCAPE TROPIS) ===')\n"
        "display(df_e4[['representation', 'condition', 'snr_db', 'mAP@10_E2_ITERA', 'mAP@10_E4_Soundscape', 'delta_mAP10_E4_minus_E2', 'retention_E2', 'retention_E4']])"
    )
    cells.append(nbf.v4.new_code_cell(c2))

    # Cell 3: Plot E2 vs E4 Comparison Across Models
    c3 = (
        "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n"
        "fig, axes = plt.subplots(1, 2, figsize=(15, 5.5))\n"
        "\n"
        "snr_conditions = ['Clean', 'SNR_20dB', 'SNR_10dB', 'SNR_0dB', 'SNR_-5dB']\n"
        "snr_labels = ['Clean', '+20 dB', '+10 dB', '0 dB', '-5 dB']\n"
        "colors = {'R2': '#1b9e77', 'R1': '#d95f02', 'R0': '#7570b3', 'R3': '#e7298a'}\n"
        "\n"
        "# Subplot 1: Kurva mAP@10 E2 (Garis Solid) vs E4 (Garis Putus-putus)\n"
        "for rep in ['R2', 'R1', 'R0', 'R3']:\n"
        "    sub = df_e4[df_e4['representation'] == rep]\n"
        "    e2_map = {r['condition']: r['mAP@10_E2_ITERA'] for _, r in sub.iterrows()}\n"
        "    e4_map = {r['condition']: r['mAP@10_E4_Soundscape'] for _, r in sub.iterrows()}\n"
        "    y_e2 = [e2_map[c] for c in snr_conditions]\n"
        "    y_e4 = [e4_map[c] for c in snr_conditions]\n"
        "    axes[0].plot(snr_labels, y_e2, marker='o', color=colors[rep], linewidth=2.0, label=f\"{rep} (E2 ITERA)\")\n"
        "    axes[0].plot(snr_labels, y_e4, marker='s', color=colors[rep], linestyle='--', linewidth=2.0, alpha=0.8, label=f\"{rep} (E4 Soundscape)\")\n"
        "\n"
        "axes[0].set_title('A. Perbandingan mAP@10: Derau ITERA vs Soundscape', fontsize=12, fontweight='bold')\n"
        "axes[0].set_ylabel('mAP@10', fontsize=11)\n"
        "axes[0].set_xlabel('Tingkat Derau (SNR)', fontsize=11)\n"
        "axes[0].set_ylim(0.0, 1.0)\n"
        "axes[0].legend(fontsize=8.5, ncol=2, loc='center right')\n"
        "\n"
        "# Subplot 2: Discrepancy Gap delta = mAP_E4 - mAP_E2\n"
        "for rep in ['R2', 'R1', 'R0', 'R3']:\n"
        "    sub = df_e4[df_e4['representation'] == rep]\n"
        "    gap_map = {r['condition']: r['delta_mAP10_E4_minus_E2'] for _, r in sub.iterrows()}\n"
        "    y_gap = [gap_map[c] for c in snr_conditions]\n"
        "    axes[1].plot(snr_labels, y_gap, marker='^', color=colors[rep], linewidth=2.2, label=f\"{rep} Gap (E4 - E2)\")\n"
        "\n"
        "axes[1].axhline(0.0, color='black', linestyle=':', alpha=0.7)\n"
        "axes[1].set_title('B. Gap Sensitivitas Profil Spektral (Δ mAP@10)', fontsize=12, fontweight='bold')\n"
        "axes[1].set_ylabel('Δ mAP@10 (E4 Soundscape - E2 ITERA)', fontsize=11)\n"
        "axes[1].set_xlabel('Tingkat Derau (SNR)', fontsize=11)\n"
        "axes[1].set_ylim(-0.10, +0.12)\n"
        "axes[1].legend(fontsize=9, loc='upper left')\n"
        "\n"
        "plt.tight_layout()\n"
        "plt.savefig(FIGURES_DIR / 'e4_noise_profile_sensitivity.png', dpi=300)\n"
        "plt.savefig(PAPER_FIG_DIR / 'e4_noise_profile_sensitivity.png', dpi=300)\n"
        "plt.show()"
    )
    cells.append(nbf.v4.new_code_cell(c3))

    # Cell 4: Markdown Discussion
    cells.append(nbf.v4.new_markdown_cell(
        "### Pembahasan Saintifik Eksperimen E4:\n\n"
        "1. **Stabilitas Model Bioakustik (BirdNET R2):**\n"
        "   - Representasi bioakustik spesifik ($R_2$) menunjukkan konsistensi ketahanan yang luar biasa tinggi terhadap pergantian sumber derau. "
        "Selisih antara derau lapangan ITERA dan soundscape tropis BirdCLEF berada pada rentang sangat sempit $\\Delta\\text{mAP} = [-0.0101, +0.0169]$ across all SNR levels.\n"
        "   - Hal ini mengindikasikan bahwa representasi spasio-temporal vokal burung yang dipelajari BirdNET bersifat invarian terhadap profil derau spektral aditif.\n\n"
        "2. **Sensitivitas Ekstrem Model Generik (PANNs R1):**\n"
        "   - Sebaliknya, model generik AudioSet ($R_1$) memperlihatkan divergensi signifikan: pada SNR 0 dB, mAP@10 adalah **0.1918** di bawah derau soundscape tropis, "
        "namun merosot ke **0.1290** di bawah derau ITERA (gap $\\Delta = +0.0628$). Pada SNR -5 dB, gap mencapai **+0.0890** (0.1480 vs 0.0590).\n"
        "   - Hal ini membuktikan bahwa representasi audio generik sangat rentan terhadap *karakteristik energi frekuensi* spesifik derau: "
        "derau antropogenik/angin AudioMoth ITERA yang memiliki konsentrasi energi rendah-menengah mendegradasi representasi PANNs jauh lebih destruktif dibanding desis soundscape kanopi hutan.\n\n"
        "3. **Keterbatasan dan Arahan Penelitian:**\n"
        "   - Karena eksperimen ini menggunakan pencampuran aditif, efek jarak propagasi, pantulan tanah/daun, dan vokalisasi simultan burung lain "
        "belum terkuantisasi penuh. Validasi lapangan in-situ sesungguhnya membutuhkan dataset soundscape beranotasi bounding-box lokal ITERA di masa mendatang.\n"
    ))

    nb.cells = cells

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"[+] Berhasil menulis struktur notebook: {NOTEBOOK_PATH}")

    print("[*] Mengeksekusi notebook E4...")
    ep = ExecutePreprocessor(timeout=600, kernel_name="python3")
    ep.preprocess(nb, {"metadata": {"path": str(PROJECT_ROOT / "notebooks")}})

    with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print(f"[+] Eksekusi E4 sukses! Seluruh grafik komparatif telah diperbarui.")

if __name__ == "__main__":
    create_and_execute_e4_notebook()
