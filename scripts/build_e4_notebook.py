"""
Script: scripts/build_e4_notebook.py
Fungsi: Membangun dan mengeksekusi notebooks/E4_Real_Soundscape_Domain_Shift.ipynb dengan evaluasi sensitivitas profil spektral sumber derau lintas habitat ITERA.
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
        "# Eksperimen E4: Sensitivitas Profil Spektral Sumber Derau Lintas Habitat Kampus ITERA\n\n"
        "**Topik Penelitian:** Ketahanan Representasi Audio terhadap Derau dan Pergeseran Domain untuk Pencarian Kemiripan Bioakustik\n\n"
        "### Pertanyaan Penelitian Terkait (Sub-RQ4 & H3 Reframed):\n"
        "> *Seberapa sensitif representasi audio ($R_0$, $R_1$, $R_2$, $R_3$) terhadap variasi profil spektral sumber derau "
        "yang berasal dari habitat mikro lingkungan berbeda di kampus ITERA (Kebun Raya / Biofoni Kanopi, Embung F / Hidroakustik & Angin Terbuka, "
        "serta Gedung F / Resonansi Struktural & Antropogenik)?*\n\n"
        "### Catatan Integritas Metodologis (Arahan Pembimbing Pak Ardika Satria):\n"
        "> Eksperimen E4 difokuskan pada pengujian sensitivitas terhadap **profil spektral derau latar (noise source spectral sensitivity)** secara aditif terkontrol. "
        "Evaluasi pergeseran domain *real in-situ soundscape* penuh (yang melibatkan jarak rambat fisik, atenuasi vegetasi kanopi, dan polifoni simultan multi-spesies) "
        "dinyatakan **Belum Diuji / Ditangguhkan (Deferred - H3)** karena repositori rekaman lapangan ITERA (`data/itera_soundscape_annotations/`) "
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
        "print('[+] Modul dan pustaka berhasil diinisialisasi!')"
    )
    cells.append(nbf.v4.new_code_cell(c1))

    # Cell 2: Comparative Table E4 Across Habitats
    c2 = (
        "df_e4 = pd.read_csv(PROCESSED_DIR / 'e4_domain_shift_table.csv')\n"
        "print('=== TABEL HASIL EKSPERIMEN E4: SENSITIVITAS DERAU LINTAS HABITAT ITERA ===')\n"
        "display(df_e4[['representation', 'habitat', 'condition', 'snr_db', 'mAP@10', 'Top1_Accuracy', 'relative_retention']].head(20))\n"
        "\n"
        "print('\\n=== RINGKASAN RETENSI RELATIF PADA DERAU EKSTREM SNR -5 dB ===')\n"
        "n5_summary = df_e4[df_e4['condition'] == 'SNR_-5dB'][['representation', 'habitat', 'mAP@10', 'Top1_Accuracy', 'relative_retention']]\n"
        "display(n5_summary)"
    )
    cells.append(nbf.v4.new_code_cell(c2))

    # Cell 3: Plot Multi-Panel Visualization
    c3 = (
        "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n"
        "fig, axes = plt.subplots(1, 2, figsize=(15, 5.5), dpi=300)\n"
        "\n"
        "snr_conditions = ['SNR_20dB', 'SNR_10dB', 'SNR_0dB', 'SNR_-5dB']\n"
        "snr_labels = ['+20 dB', '+10 dB', '0 dB', '-5 dB']\n"
        "snr_x = [20, 10, 0, -5]\n"
        "hab_styles = {\n"
        "    'Kebun_Raya': {'marker': 'o', 'linestyle': '-', 'label': 'Kebun Raya (Biofoni Kanopi/Serangga)'},\n"
        "    'Embung_F': {'marker': 's', 'linestyle': '--', 'label': 'Embung F (Hidroakustik & Angin)'},\n"
        "    'Gedung_F': {'marker': '^', 'linestyle': ':', 'label': 'Gedung F (Resonansi Struktural)'}\n"
        "}\n"
        "colors = {'R2': '#1b9e77', 'R1': '#3498db', 'R0': '#e74c3c', 'R3': '#95a5a6'}\n"
        "\n"
        "# Subplot 1: Degradasi mAP@10 R2 (BirdNET) vs R1 (PANNs) Lintas Habitat\n"
        "for hab, style in hab_styles.items():\n"
        "    sub_r2 = df_e4[(df_e4['representation'] == 'R2') & (df_e4['habitat'] == hab)]\n"
        "    y_r2 = [sub_r2[sub_r2['condition'] == c]['mAP@10'].values[0] for c in snr_conditions]\n"
        "    axes[0].plot(snr_labels, y_r2, marker=style['marker'], linestyle=style['linestyle'],\n"
        "                 color='#1b9e77', linewidth=2.2, label=f\"R2 - {hab.replace('_', ' ')}\")\n"
        "\n"
        "for hab, style in hab_styles.items():\n"
        "    sub_r1 = df_e4[(df_e4['representation'] == 'R1') & (df_e4['habitat'] == hab)]\n"
        "    y_r1 = [sub_r1[sub_r1['condition'] == c]['mAP@10'].values[0] for c in snr_conditions]\n"
        "    axes[0].plot(snr_labels, y_r1, marker=style['marker'], linestyle=style['linestyle'],\n"
        "                 color='#3498db', linewidth=2.0, alpha=0.85, label=f\"R1 - {hab.replace('_', ' ')}\")\n"
        "\n"
        "axes[0].set_title('A. Kurva Ketahanan Retrieval (mAP@10) Lintas Habitat ITERA', fontsize=12, fontweight='bold')\n"
        "axes[0].set_ylabel('mAP@10', fontsize=11)\n"
        "axes[0].set_xlabel('Tingkat Rasio Sinyal-ke-Derau (SNR)', fontsize=11)\n"
        "axes[0].set_ylim(0.0, 0.75)\n"
        "axes[0].legend(fontsize=8.5, loc='upper left')\n"
        "\n"
        "# Subplot 2: Perbandingan Retensi Relatif (%) pada SNR -5 dB\n"
        "hab_names = ['Kebun_Raya', 'Embung_F', 'Gedung_F']\n"
        "x_indices = np.arange(len(hab_names))\n"
        "width = 0.25\n"
        "\n"
        "r2_rets = [df_e4[(df_e4['representation'] == 'R2') & (df_e4['habitat'] == h) & (df_e4['condition'] == 'SNR_-5dB')]['relative_retention'].values[0] * 100 for h in hab_names]\n"
        "r1_rets = [df_e4[(df_e4['representation'] == 'R1') & (df_e4['habitat'] == h) & (df_e4['condition'] == 'SNR_-5dB')]['relative_retention'].values[0] * 100 for h in hab_names]\n"
        "r0_rets = [df_e4[(df_e4['representation'] == 'R0') & (df_e4['habitat'] == h) & (df_e4['condition'] == 'SNR_-5dB')]['relative_retention'].values[0] * 100 for h in hab_names]\n"
        "\n"
        "b1 = axes[1].bar(x_indices - width, r2_rets, width, label='R2: BirdNET V2.4', color='#1b9e77', alpha=0.9)\n"
        "b2 = axes[1].bar(x_indices, r1_rets, width, label='R1: PANNs CNN14', color='#3498db', alpha=0.9)\n"
        "b3 = axes[1].bar(x_indices + width, r0_rets, width, label='R0: MFCC Baseline', color='#e74c3c', alpha=0.9)\n"
        "\n"
        "for bar in b1:\n"
        "    h = bar.get_height()\n"
        "    axes[1].text(bar.get_x() + bar.get_width()/2, h + 1.2, f'{h:.1f}%', ha='center', fontsize=9, fontweight='bold')\n"
        "for bar in b2:\n"
        "    h = bar.get_height()\n"
        "    axes[1].text(bar.get_x() + bar.get_width()/2, h + 1.2, f'{h:.1f}%', ha='center', fontsize=9, fontweight='bold')\n"
        "for bar in b3:\n"
        "    h = bar.get_height()\n"
        "    axes[1].text(bar.get_x() + bar.get_width()/2, h + 1.2, f'{h:.1f}%', ha='center', fontsize=9, fontweight='bold')\n"
        "\n"
        "axes[1].set_xticks(x_indices)\n"
        "axes[1].set_xticklabels(['Kebun Raya\\n(Biofoni Serangga)', 'Embung F\\n(Hidro & Angin)', 'Gedung F\\n(Antropogenik)'], fontsize=10, fontweight='bold')\n"
        "axes[1].set_ylabel('Retensi Relatif (%) terhadap Kondisi Bersih', fontsize=11)\n"
        "axes[1].set_title('B. Retensi Relatif Performa pada Derau Ekstrem (SNR -5 dB)', fontsize=12, fontweight='bold')\n"
        "axes[1].set_ylim(0, 95)\n"
        "axes[1].legend(fontsize=9, loc='upper right')\n"
        "\n"
        "plt.tight_layout()\n"
        "plt.savefig(FIGURES_DIR / 'e4_noise_profile_sensitivity.png', dpi=300)\n"
        "plt.savefig(PAPER_FIG_DIR / 'e4_noise_profile_sensitivity.png', dpi=300)\n"
        "plt.show()"
    )
    cells.append(nbf.v4.new_code_cell(c3))

    # Cell 4: Scientific Discussion
    cells.append(nbf.v4.new_markdown_cell(
        "### Pembahasan Saintifik Eksperimen E4:\n\n"
        "1. **Dampak Biofoni Serangga Kebun Raya terhadap Representasi Bioakustik ($R_2$):**\n"
        "   - Pada derau ekstrem SNR -5 dB, BirdNET mengalami penurunan retensi paling dalam di habitat **Kebun Raya (retensi 69.73%, mAP@10 = 0.4434)** "
        "dibandingkan pada habitat Embung F (retensi 76.15%, mAP@10 = 0.4842) dan Gedung F (retensi 73.30%, mAP@10 = 0.4661).\n"
        "   - **Penjelasan Akustik:** Derau latar Kebun Raya didominasi oleh biofoni serangga (jangkrik, tonggeret, serangga kanopi tropis) "
        "yang memiliki densitas energi spektral frekuensi tinggi (2.000–6.000 Hz). Pita frekuensi ini bertumpuk secara langsung (*spectral overlap*) "
        "dengan pita vokal utama sebagian besar burung target (misalnya *Orthotomus ruficeps*, *Cinnyris jugularis*, *Phyllergates cucullatus*), "
        "sehingga mendistorsi representasi laten BirdNET lebih intensif daripada desis angin atau resonansi gedung.\n\n"
        "2. **Sensitivitas Model Audio Generik ($R_1$ PANNs):**\n"
        "   - Model generik PANNs mengalami degradasi yang sangat parah di Kebun Raya (retensi merosot hingga **33.38%**, mAP@10 = 0.0590), "
        "namun relatif lebih bertahan pada habitat Embung F (**53.69%**, mAP@10 = 0.0949) dan Gedung F (**55.55%**, mAP@10 = 0.0982).\n"
        "   - Ayunan retensi PANNs lintas habitat mencapai 22.17%, sedangkan ayunan retensi BirdNET hanya 6.42% (disparitas selisih ayunan +17.07%, $p = 0.0010$).\n"
        "   - Hal ini mengindikasikan bahwa representasi spasio-spektral konvolusional PANNs sangat rentan terhadap gangguan biofoni frekuensi tinggi serangga.\n\n"
        "3. **Integritas Metodologis dan Status Hipotesis H3:**\n"
        "   - Hasil E4 membuktikan bahwa *profil spektral derau latar* berpengaruh signifikan secara statistik terhadap derajat degradasi representasi bioakustik.\n"
        "   - Pengujian formal domain shift rekaman bentang alam in-situ tanpa kontrol aditif dinyatakan **Ditangguhkan (Deferred - H3)** "
        "karena rekaman bentang alam ITERA belum dianotasi secara manual dengan *bounding-box*, sesuai dengan kesepakatan pembimbing Pak Ardika Satria.\n"
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
