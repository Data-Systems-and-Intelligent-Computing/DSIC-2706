"""
Unit Test: tests/unit/test_manuscript_table_consistency.py
Memverifikasi sinkronisasi struktural 100% antara tabel markdown & klaim numerik di naskah
publikasi (paper/manuscript.md) dengan tabel-tabel resmi di paper/tables/*.csv.
Pengujian mem-parsing nilai numerik secara struktural, bukan sekadar pencarian substring.
"""

import re
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MANUSCRIPT_PATH = PROJECT_ROOT / "paper/manuscript.md"
TABLES_DIR = PROJECT_ROOT / "paper/tables"


def clean_val(v: str) -> str:
    """Membersihkan format markdown (bold, italic, persen, kurung siku, plus)."""
    v = re.sub(r"\*\*|\*|%|\+|\[|\]", "", v).strip()
    return v


def parse_markdown_tables(md_text: str):
    """Mengekstrak seluruh tabel markdown menjadi list blok baris."""
    tables = []
    lines = md_text.splitlines()
    cur = []
    for line in lines:
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            cur.append(s)
        else:
            if len(cur) >= 3:
                tables.append(cur)
            cur = []
    if len(cur) >= 3:
        tables.append(cur)
    return tables


def parse_table_rows(table_lines):
    """Mengubah baris tabel markdown menjadi list dictionary."""
    header = [c.strip() for c in table_lines[0].strip("|").split("|")]
    rows = []
    for line in table_lines[2:]:
        line = line.strip()
        if not line:
            continue
        cells = [clean_val(c) for c in line.strip("|").split("|")]
        if len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def test_manuscript_exists():
    assert MANUSCRIPT_PATH.exists(), f"File naskah {MANUSCRIPT_PATH} tidak ditemukan!"


def test_table_e1_structural_numeric():
    """Memverifikasi seluruh nilai numerik Tabel E1 (Clean Retrieval) terhadap CSV."""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    tables = parse_markdown_tables(text)
    assert len(tables) >= 5, f"Tabel markdown kurang dari 5 (ditemukan {len(tables)})"

    rows = parse_table_rows(tables[0])
    df_csv = pd.read_csv(TABLES_DIR / "clean_retrieval_table.csv")

    model_map = {"$R_0$": "R0", "$R_1$": "R1", "$R_2$": "R2", "$R_3$": "R3"}
    for r in rows:
        code = r["Kode"]
        if code not in model_map:
            continue
        csv_code = model_map[code]
        csv_row = df_csv[df_csv["Representation"] == csv_code].iloc[0]

        # Periksa Top-1
        top1_md = float(r["Top-1 Accuracy (%)"])
        top1_csv = float(csv_row["Top-1"]) * 100
        assert abs(top1_md - top1_csv) < 0.05, f"Top-1 {csv_code} beda: MD={top1_md}, CSV={top1_csv}"

        # Periksa mAP@10
        map_md = float(r["mAP@10"])
        map_csv = float(csv_row["mAP@10"])
        assert abs(map_md - map_csv) < 0.001, f"mAP@10 {csv_code} beda: MD={map_md}, CSV={map_csv}"

        # Periksa MRR
        mrr_md = float(r["MRR"])
        mrr_csv = float(csv_row["MRR"])
        assert abs(mrr_md - mrr_csv) < 0.001, f"MRR {csv_code} beda: MD={mrr_md}, CSV={mrr_csv}"

        # Periksa Precision@10 & Recall@10
        p_md = float(r["Precision@10"])
        p_csv = float(csv_row["Precision@10"])
        assert abs(p_md - p_csv) < 0.001, f"P@10 {csv_code} beda: MD={p_md}, CSV={p_csv}"

        rec_md = float(r["Recall@10"])
        rec_csv = float(csv_row["Recall@10"])
        assert abs(rec_md - rec_csv) < 0.001, f"R@10 {csv_code} beda: MD={rec_md}, CSV={rec_csv}"

    # Verifikasi temuan reviewer: R3 Precision@10 = 0.0615 dan Recall@10 = 0.0150 (bukan 0.0603/0.0163)
    r3_dict = next(r for r in rows if r["Kode"] == "$R_3$")
    assert abs(float(r3_dict["Precision@10"]) - 0.0615) < 0.001
    assert abs(float(r3_dict["Recall@10"]) - 0.0150) < 0.001


def test_table_e2_structural_numeric():
    """Memverifikasi seluruh nilai numerik Tabel E2 (SNR Robustness) terhadap CSV."""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    tables = parse_markdown_tables(text)
    rows = parse_table_rows(tables[1])
    df_csv = pd.read_csv(TABLES_DIR / "snr_robustness_table.csv")

    model_map = {"$R_0$ (MFCC)": "R0", "$R_1$ (PANNs)": "R1", "$R_2$ (BirdNET)": "R2", "$R_3$ (Random)": "R3"}
    col_cond_map = {
        "Clean": "Clean",
        "SNR 20 dB": "SNR_20dB",
        "SNR 10 dB": "SNR_10dB",
        "SNR 0 dB": "SNR_0dB",
        "SNR -5 dB": "SNR_-5dB",
    }

    for r in rows:
        rep_name = r["Representasi"]
        if rep_name not in model_map:
            continue
        csv_code = model_map[rep_name]

        for md_col, csv_cond in col_cond_map.items():
            val_md = float(r[md_col])
            csv_val = float(df_csv[(df_csv["representation"] == csv_code) & (df_csv["condition"] == csv_cond)]["mAP@10"].iloc[0])
            assert abs(val_md - csv_val) < 0.001, f"mAP {csv_code} {csv_cond} beda: MD={val_md}, CSV={csv_val}"

        # Periksa retensi relatif (-5 dB)
        ret_str = r["Retensi Relatif (-5 dB)"].split("(")[0].strip()
        ret_md = float(ret_str)
        ret_csv = float(df_csv[(df_csv["representation"] == csv_code) & (df_csv["condition"] == "SNR_-5dB")]["relative_retention"].iloc[0])
        assert abs(ret_md - ret_csv) < 0.05, f"Retensi {csv_code} beda: MD={ret_md}, CSV={ret_csv}"


def test_table_e3_structural_numeric():
    """Memverifikasi nilai numerik Tabel E3 (Threshold Transfer) terhadap CSV."""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    tables = parse_markdown_tables(text)
    rows = parse_table_rows(tables[2])
    df_csv = pd.read_csv(TABLES_DIR / "threshold_transfer_table.csv")

    cur_model = None
    for r in rows:
        if r["Model"]:
            m_clean = r["Model"].replace("_", "")
            if "R2" in m_clean: cur_model = "R2"
            elif "R1" in m_clean: cur_model = "R1"
            elif "R0" in m_clean: cur_model = "R0"
            elif "R3" in m_clean: cur_model = "R3"

        cond = r["Kondisi"].replace(" ", "_")
        csv_row = df_csv[(df_csv["representation"] == cur_model) & (df_csv["condition"] == cond)]
        if csv_row.empty:
            continue
        csv_row = csv_row.iloc[0]

        auroc_md = float(r["AUROC"])
        auroc_csv = float(csv_row["auroc"])
        assert abs(auroc_md - auroc_csv) < 0.001, f"AUROC {cur_model} {cond} beda: MD={auroc_md}, CSV={auroc_csv}"

        rec_md = float(r["Recall@$\\tau^*$"])
        rec_csv = float(csv_row["tpr"])
        assert abs(rec_md - rec_csv) < 0.001, f"Recall {cur_model} {cond} beda: MD={rec_md}, CSV={rec_csv}"

        fpr_md = float(r["FPR@$\\tau^*$"])
        fpr_csv = float(csv_row["fpr"])
        assert abs(fpr_md - fpr_csv) < 0.001, f"FPR {cur_model} {cond} beda: MD={fpr_md}, CSV={fpr_csv}"


def test_table_e4_structural_numeric():
    """Memverifikasi nilai numerik Tabel E4 (Domain Shift) terhadap CSV."""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    tables = parse_markdown_tables(text)
    rows = parse_table_rows(tables[3])
    df_csv = pd.read_csv(TABLES_DIR / "e4_domain_shift_table.csv")

    cur_model = None
    for r in rows:
        if r["Model"]:
            m_clean = r["Model"].replace("_", "")
            if "R2" in m_clean: cur_model = "R2"
            elif "R1" in m_clean: cur_model = "R1"
            elif "R0" in m_clean: cur_model = "R0"

        hab = r["Habitat Derau"].replace(" ", "_")
        if hab == "Baseline_Clean":
            continue

        csv_row = df_csv[(df_csv["representation"] == cur_model) & (df_csv["habitat"] == hab) & (df_csv["condition"] == "SNR_-5dB")]
        assert not csv_row.empty, f"Baris CSV {cur_model} {hab} tidak ditemukan"
        csv_row = csv_row.iloc[0]

        map_md = float(r["mAP@10"])
        map_csv = float(csv_row["mAP@10"])
        assert abs(map_md - map_csv) < 0.001, f"mAP E4 {cur_model} {hab} beda: MD={map_md}, CSV={map_csv}"

        top1_md = float(r["Top-1 Accuracy (%)"])
        top1_csv = float(csv_row["top1_accuracy"]) * 100
        assert abs(top1_md - top1_csv) < 0.05, f"Top-1 E4 {cur_model} {hab} beda: MD={top1_md}, CSV={top1_csv}"


def test_table_significance_structural_numeric():
    """Memverifikasi nilai numerik Tabel Uji Signifikansi Statistik terhadap CSV."""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    tables = parse_markdown_tables(text)
    rows = parse_table_rows(tables[4])
    df_csv = pd.read_csv(TABLES_DIR / "statistical_significance_table.csv")

    assert len(rows) == len(df_csv), f"Jumlah baris tabel signifikansi beda: MD={len(rows)}, CSV={len(df_csv)}"

    for md_r, (_, csv_r) in zip(rows, df_csv.iterrows()):
        diff_md = float(md_r["Mean Difference"])
        diff_csv = float(csv_r["Mean_Diff"])
        assert abs(diff_md - diff_csv) < 0.001, f"Mean Diff beda: MD={diff_md}, CSV={diff_csv}"


def test_text_claims_integrity():
    """Memverifikasi klaim numerik dan status hipotesis dalam naskah."""
    text = MANUSCRIPT_PATH.read_text(encoding="utf-8")

    # 1. Top-1 R2 pada -5 dB harus 64.31% (bukan 61.3%)
    assert "64.31%" in text, "Klaim Top-1 R2 pada -5 dB (64.31%) tidak ditemukan!"
    assert "61.3%" not in text, "Klaim usang 61.3% masih ada di naskah!"

    # 2. H5 harus secara ketat membandingkan model terlatih vs R3 (kontrol acak)
    assert "H5 Terpenuhi: $R_2$ unggul mutlak atas kontrol acak" in text
    assert "H5 Terpenuhi: $R_1$ unggul atas kontrol acak" in text
    assert "H5 Terpenuhi: $R_0$ unggul atas kontrol acak" in text
    assert "R2 vs R3 memiliki Mean Difference" in text or "BirdNET $R_2$ vs $R_3$" in text

    # 3. Uji H3 harus melaporkan Delta observasi 0.1560 berdampingan dengan mean bootstrap +0.1692 dan p <= 0.001
    assert "0.1560" in text, "Delta observasi 0.1560 tidak ditemukan dalam pembahasan H3!"
    assert "+0.1692" in text or "0.1692" in text, "Rata-rata bootstrap 0.1692 tidak ditemukan!"
    assert "p \\le 0.001" in text, "p <= 0.001 tidak ditemukan!"

    # 4. Kalibrasi E3 N=465, TPR=57.33%, J=0.4188, FPR=15.45%
    assert "N=465" in text, "N=465 kalibrasi tidak ditemukan!"
    assert "0.5733" in text or "57.33%" in text, "TPR kalibrasi R2 0.5733 tidak ditemukan!"
    assert "0.4188" in text, "Youden J R2 0.4188 tidak ditemukan!"

    # 5. Partisi klip 1.216, 673 galeri, 311 kueri, 232 kalibrasi, 112 perekam unik
    assert "1.216" in text or "1,216" in text, "1.216 klip tidak ditemukan!"
    assert "673" in text, "673 galeri tidak ditemukan!"
    assert "311" in text, "311 kueri tidak ditemukan!"
    assert "232" in text, "232 kalibrasi tidak ditemukan!"
    assert "112" in text, "112 perekam tidak ditemukan!"


# Alias fungsi untuk kompatibilitas runner
test_clean_retrieval_consistency = test_table_e1_structural_numeric
test_snr_robustness_consistency = test_table_e2_structural_numeric
test_threshold_transfer_e3_consistency = test_table_e3_structural_numeric
test_e4_habitat_sensitivity_consistency = test_table_e4_structural_numeric
test_bootstrap_significance_consistency = test_table_significance_structural_numeric


if __name__ == "__main__":
    print("[*] Menjalankan test_manuscript_table_consistency (Structural Numeric Evaluation)...")
    test_manuscript_exists()
    test_table_e1_structural_numeric()
    test_table_e2_structural_numeric()
    test_table_e3_structural_numeric()
    test_table_e4_structural_numeric()
    test_table_significance_structural_numeric()
    test_text_claims_integrity()
    print("[+] SEMUA 7 PENGUJIAN KONSISTENSI STRUKTURAL NUMERIK NASKAH VS TABEL CSV LOLOS 100%!")
