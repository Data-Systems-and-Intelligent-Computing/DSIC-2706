"""
STATUS: TIDAK DIGUNAKAN / LEGACY — dipensiunkan pada 18 Oktober 2026.
Bukan produsen hasil E4 lima lokasi. Sumber historis yang sah:
scripts/run_e4_five_locations_v10_stage7.py.draft (hash lihat run_identity.json).
Isi berikut dipertahankan sebagai arsip versi tiga lokasi; jangan dieksekusi.

Script: scripts/run_e4_domain_shift.py
Fungsi: Eksekusi Eksperimen E4 — Sensitivitas Profil Spektral Sumber Derau
        Lintas Habitat Lingkungan Nyata Kampus ITERA.
        Membandingkan ketahanan representasi (R0, R1, R2, R3) ketika kueri
        didegradasi oleh derau dari 3 profil akustik habitat berbeda di ITERA:
        1. Kebun Raya ITERA (Vegetasi Lebat Tropis / Dominasi Biophony Serangga)
        2. Embung F ITERA (Perairan Terbuka / Resonansi Air & Angin)
        3. Gedung F ITERA (Koridor Bangunan / Derau Struktural & Antropogenik)
"""


if __name__ == "__main__":
    raise SystemExit("TIDAK DIGUNAKAN: runner arsip tiga lokasi. E4 lima lokasi sudah selesai; baca run_identity.json dan analisis tersimpan. E4 tidak dijalankan ulang.")

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import librosa
import soundfile as sf
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocess import preprocess_audio, TARGET_SR
from src.embeddings import AudioRepresentationExtractor, R3_CONTROL_VERSION
from src.mix_noise import compute_signal_power, get_e3_reserved_noise_files
from src.retrieve import evaluate_retrieval_corpus

SPLIT_PATH = PROJECT_ROOT / "data/manifests/dataset_split.csv"
NOISE_MANIFEST_PATH = PROJECT_ROOT / "data/manifests/itera_noise_manifest.csv"
NOISE_DIR = PROJECT_ROOT / "data/itera_noise"
FEATURES_DIR = PROJECT_ROOT / "results/features"
PROCESSED_DIR = PROJECT_ROOT / "results/processed"
RAW_DIR = PROJECT_ROOT / "results/raw"
TABLES_DIR = PROJECT_ROOT / "paper/tables"
FIG_DIR = PROJECT_ROOT / "results/figures"
PAPER_FIG_DIR = PROJECT_ROOT / "paper/figures"

for d in [PROCESSED_DIR, RAW_DIR, TABLES_DIR, FIG_DIR, PAPER_FIG_DIR]:
    d.mkdir(parents=True, exist_ok=True)


def load_habitat_noise_files():
    """Mengelompokkan berkas derau ITERA berdasarkan 3 profil habitat utama (eksklusif dari unknown E3)."""
    df_noise = pd.read_csv(NOISE_MANIFEST_PATH)
    e3_reserved = get_e3_reserved_noise_files()
    habitats = {
        "Kebun_Raya": [],
        "Embung_F": [],
        "Gedung_F": []
    }
    for _, r in df_noise.iterrows():
        fn = r["filename"]
        p = NOISE_DIR / fn
        if not p.exists() or p.name.lower() in e3_reserved:
            continue
        if "Kebun Raya" in fn:
            habitats["Kebun_Raya"].append(p)
        elif "Embung F" in fn:
            habitats["Embung_F"].append(p)
        elif "Gedung F" in fn:
            habitats["Gedung_F"].append(p)

    for hab, files in habitats.items():
        print(f"[*] Habitat [{hab}]: {len(files)} berkas audio derau valid (disjoint dari E3).")
        if len(files) == 0:
            raise FileNotFoundError(f"Tidak ada berkas derau untuk habitat {hab}!")
    return habitats


def get_habitat_noise_segment(files: list, samples: int, seed: int = 42, return_path: bool = False,
                              return_audit_info: bool = False):
    """Mengambil segmen acak dari daftar berkas derau habitat tertentu dengan penolakan derau senyap."""
    rng = np.random.default_rng(seed)
    max_attempts = 10
    for attempt in range(max_attempts):
        selected = files[rng.integers(0, len(files))]
        try:
            y, _ = librosa.load(str(selected), sr=TARGET_SR, mono=True)
            if len(y) >= samples:
                start = int(rng.integers(0, len(y) - samples + 1))
                seg = y[start:start + samples].astype(np.float32)
            else:
                repeats = int(np.ceil(samples / len(y)))
                y = np.tile(y, repeats)
                seg = y[:samples].astype(np.float32)
                start = 0

            raw_rms = np.sqrt(np.mean(seg ** 2))
            if raw_rms < 1e-4:
                continue

            try:
                rel_path = str(Path(selected).relative_to(NOISE_DIR)).replace("\\", "/")
            except ValueError:
                rel_path = Path(selected).name

            audit_info = {
                "noise_file": rel_path,
                "noise_start_sample": start,
                "noise_segment_samples": int(samples),
                "noise_seed": int(seed),
                "noise_attempt": attempt + 1,
                "noise_raw_rms": float(raw_rms),
            }
            if return_audit_info:
                return seg, audit_info
            if return_path:
                return seg, rel_path
            return seg
        except Exception as e:
            if attempt == max_attempts - 1:
                raise RuntimeError(f"Gagal memuat derau habitat {selected}: {e}")

    raise ValueError(f"[FATAL] Terdeteksi segmen derau senyap pada habitat setelah {max_attempts} percobaan pengambilan!")


def mix_with_habitat_noise(clean: np.ndarray, noise_files: list, snr_db: float, seed: int = 42,
                           return_noise_path: bool = False, return_audit_info: bool = False):
    """Mencampur sinyal bersih dengan derau habitat tertentu pada SNR eksak."""
    noise, audit_info = get_habitat_noise_segment(noise_files, samples=len(clean), seed=seed, return_audit_info=True)
    rel_path = audit_info["noise_file"]
    p_signal = compute_signal_power(clean)
    p_noise = compute_signal_power(noise)

    if p_signal <= 1e-12:
        audit_info.update({
            "snr_db_target": float(snr_db), "snr_db_achieved": None,
            "signal_power": p_signal, "noise_power_before_scaling": p_noise,
            "noise_gain": None, "post_mix_gain": 1.0, "mix_skipped_silent_signal": True,
        })
        if return_audit_info:
            return clean.copy(), audit_info
        if return_noise_path:
            return clean.copy(), rel_path
        return clean.copy()

    if p_noise <= 1e-10:
        raise ValueError(f"[FATAL] Derau fisik habitat terdeteksi senyap ({rel_path})!")

    target_p_noise = p_signal / (10.0 ** (snr_db / 10.0))
    alpha = np.sqrt(target_p_noise / p_noise)
    scaled_noise = alpha * noise
    noisy = clean + scaled_noise

    max_amp = np.max(np.abs(noisy))
    post_mix_gain = 1.0 / max_amp if max_amp > 1.0 else 1.0
    noisy = noisy * post_mix_gain
    signal_after_gain = clean * post_mix_gain
    noise_after_gain = scaled_noise * post_mix_gain
    achieved_snr = 10.0 * np.log10(compute_signal_power(signal_after_gain) / compute_signal_power(noise_after_gain))
    audit_info.update({
        "snr_db_target": float(snr_db), "snr_db_achieved": float(achieved_snr),
        "signal_power": p_signal, "noise_power_before_scaling": p_noise,
        "noise_gain": float(alpha), "post_mix_gain": float(post_mix_gain), "mix_skipped_silent_signal": False,
    })

    res = noisy.astype(np.float32)
    if return_audit_info:
        return res, audit_info
    if return_noise_path:
        return res, rel_path
    return res


def main():
    print("=" * 80)
    print("[*] MEMULAI E4: SENSITIVITAS PROFIL SPEKTRAL DERAU LINTAS HABITAT KAMPUS ITERA")
    print("=" * 80)

    habitats = load_habitat_noise_files()

    df_split = pd.read_csv(SPLIT_PATH)
    gallery_df = df_split[df_split["split_role"] == "gallery"].reset_index(drop=True)
    query_df = df_split[df_split["split_role"] == "query_clean"].reset_index(drop=True)

    print(f"[*] Total Galeri: {len(gallery_df)}, Total Kueri: {len(query_df)}")

    # Muat audio bersih kueri
    print("[*] Memuat sinyal kueri bersih...")
    query_audios = [preprocess_audio(r["file_path"]) for _, r in query_df.iterrows()]
    query_labels = list(query_df["species_key"])
    gallery_labels = list(gallery_df["species_key"])

    snr_list = [20, 10, 0, -5]
    representations = ["R0", "R1", "R2", "R3"]

    e4_summary_rows = []

    for rep in representations:
        print(f"\n" + "-" * 60)
        print(f"[*] MEMPROSES E4 REPRESENTASI [{rep}]")
        print("-" * 60)

        feat_path = FEATURES_DIR / f"clean_embeddings_{rep}.npz"
        feat_data = np.load(feat_path)
        if rep == "R3":
            cache_version = str(feat_data["r3_control_version"].item()) if "r3_control_version" in feat_data.files else "missing"
            if cache_version != R3_CONTROL_VERSION:
                raise ValueError(
                    f"Cache R3 tidak kompatibel ({cache_version}); jalankan E1 R3 baru dengan "
                    f"kontrol {R3_CONTROL_VERSION} sebelum E4."
                )
        gallery_embs = feat_data["gal_feats"]
        clean_query_embs = feat_data["qry_feats"]

        extractor = AudioRepresentationExtractor(rep)

        # Baseline Clean
        clean_summary, clean_raw = evaluate_retrieval_corpus(
            clean_query_embs, query_labels, gallery_embs, gallery_labels
        )
        clean_map = clean_summary["mAP@10"]
        print(f"    [Clean] mAP@10: {clean_map:.4f}, Top1: {clean_summary['mean_top1']:.4f}")

        # Catat baris Clean
        e4_summary_rows.append({
            "representation": rep,
            "habitat": "Baseline",
            "condition": "Clean",
            "snr_db": 999,
            "mAP@10": clean_map,
            "Top1_Accuracy": clean_summary["mean_top1"],
            "Precision@10": clean_summary["Precision@10"],
            "Recall@10": clean_summary["Recall@10"],
            "relative_retention": 1.0
        })

        all_hab_raw_rows = []

        # Catat baris mentah Baseline Clean
        for i, r_item in enumerate(clean_raw):
            r_item_dict = dict(r_item)
            r_item_dict["query_id"] = query_df.iloc[i]["recording_id"]
            r_item_dict["species_key"] = query_df.iloc[i]["species_key"]
            r_item_dict["recordist"] = query_df.iloc[i].get("author", "Unknown")
            r_item_dict["noise_file"] = "None (Clean)"
            r_item_dict["habitat"] = "Baseline"
            r_item_dict["condition"] = "Clean"
            r_item_dict["snr_db"] = 999
            r_item_dict["representation"] = rep
            all_hab_raw_rows.append(r_item_dict)

        # Evaluasi per habitat dan per SNR
        for hab_name, hab_files in habitats.items():
            for snr in snr_list:
                noisy_embs = []
                used_noise_paths = []
                for i, y_c in enumerate(query_audios):
                    y_n, audit = mix_with_habitat_noise(y_c, hab_files, snr_db=snr, seed=5000 + i, return_audit_info=True)
                    emb_n = extractor.extract(y_n, item_id=f"query_clean:{query_df.iloc[i]['recording_id']}")
                    noisy_embs.append(emb_n)
                    used_noise_paths.append(audit)
                noisy_embs = np.array(noisy_embs, dtype=np.float32)

                h_summary, h_raw = evaluate_retrieval_corpus(
                    noisy_embs, query_labels, gallery_embs, gallery_labels
                )
                h_map = h_summary["mAP@10"]
                h_ret = h_map / max(clean_map, 1e-6)

                print(f"    [{hab_name:10s} | SNR {snr:3d} dB] mAP@10: {h_map:.4f} (Ret: {h_ret*100:.1f}%), Top1: {h_summary['mean_top1']:.4f}")

                e4_summary_rows.append({
                    "representation": rep,
                    "habitat": hab_name,
                    "condition": f"SNR_{snr}dB",
                    "snr_db": snr,
                    "mAP@10": h_map,
                    "Top1_Accuracy": h_summary["mean_top1"],
                    "Precision@10": h_summary["Precision@10"],
                    "Recall@10": h_summary["Recall@10"],
                    "relative_retention": h_ret
                })

                for i, r_item in enumerate(h_raw):
                    r_item_dict = dict(r_item)
                    r_item_dict["query_id"] = query_df.iloc[i]["recording_id"]
                    r_item_dict["species_key"] = query_df.iloc[i]["species_key"]
                    r_item_dict["recordist"] = query_df.iloc[i].get("author", "Unknown")
                    audit = used_noise_paths[i]
                    r_item_dict["noise_file"] = audit["noise_file"]
                    for key, value in audit.items():
                        r_item_dict[key] = value
                    r_item_dict["habitat"] = hab_name
                    r_item_dict["condition"] = f"SNR_{snr}dB"
                    r_item_dict["snr_db"] = snr
                    r_item_dict["representation"] = rep
                    all_hab_raw_rows.append(r_item_dict)

        # Simpan raw query metrics E4
        df_raw_e4 = pd.DataFrame(all_hab_raw_rows)
        raw_out_path = RAW_DIR / f"E4_{rep}_raw.csv"
        df_raw_e4.to_csv(raw_out_path, index=False)
        print(f"    [+] Raw scores E4 {rep} disimpan di: {raw_out_path}")

    # Simpan tabel ringkasan komparatif E4
    df_e4_table = pd.DataFrame(e4_summary_rows)
    table_path = PROCESSED_DIR / "e4_domain_shift_table.csv"
    df_e4_table.to_csv(table_path, index=False)
    df_e4_table.to_csv(TABLES_DIR / "e4_domain_shift_table.csv", index=False)
    print(f"\n[+] Tabel komparatif E4 berhasil disimpan di: {table_path}")

    # Visualisasi Sensitivitas Profil Spektral Lintas Habitat
    print("[*] Membuat grafik komparatif E4...")
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, axes = plt.subplots(1, 2, figsize=(15, 5.5), dpi=300)

    hab_colors = {
        "Kebun_Raya": "#2ca02c", # Hijau vegetasi
        "Embung_F": "#1f77b4",   # Biru perairan
        "Gedung_F": "#d62728"    # Merah koridor bangunan
    }
    hab_labels = {
        "Kebun_Raya": "Kebun Raya (Biophony Vegetasi)",
        "Embung_F": "Embung F (Perairan & Angin)",
        "Gedung_F": "Gedung F (Koridor Struktural)"
    }

    snr_order = [20, 10, 0, -5]
    snr_str = ["+20 dB", "+10 dB", "0 dB", "-5 dB"]

    # Subplot 1: Ketahanan BirdNET (R2) Lintas Habitat
    sub_r2 = df_e4_table[df_e4_table["representation"] == "R2"]
    for hab in ["Kebun_Raya", "Embung_F", "Gedung_F"]:
        hab_data = sub_r2[sub_r2["habitat"] == hab].set_index("snr_db").reindex(snr_order)
        axes[0].plot(snr_str, hab_data["mAP@10"], marker="o", linewidth=2.2, color=hab_colors[hab], label=hab_labels[hab])

    axes[0].set_title("A. Sensitivitas BirdNET (R2) Lintas Habitat ITERA", fontsize=12, fontweight="bold")
    axes[0].set_xlabel("Tingkat Derau (SNR)", fontsize=11)
    axes[0].set_ylabel("mAP@10", fontsize=11)
    axes[0].set_ylim(0.4, 0.7)
    axes[0].legend(fontsize=9.5)

    # Subplot 2: Perbandingan Retensi SNR -5 dB Lintas Model & Habitat
    sub_severe = df_e4_table[df_e4_table["snr_db"] == -5]
    x_models = np.arange(4)
    model_names = ["R2", "R1", "R0", "R3"]
    w = 0.25

    for idx, hab in enumerate(["Kebun_Raya", "Embung_F", "Gedung_F"]):
        hab_vals = [sub_severe[(sub_severe["representation"] == m) & (sub_severe["habitat"] == hab)]["relative_retention"].values[0] * 100 for m in model_names]
        axes[1].bar(x_models + (idx - 1) * w, hab_vals, width=w, color=hab_colors[hab], alpha=0.85, label=hab_labels[hab])

    axes[1].set_xticks(x_models)
    axes[1].set_xticklabels(["R2 (BirdNET)", "R1 (PANNs)", "R0 (MFCC)", "R3 (Random)"], fontweight="bold")
    axes[1].set_title("B. Retensi Relatif pada Derau Ekstrem (-5 dB SNR)", fontsize=12, fontweight="bold")
    axes[1].set_xlabel("Representasi Fitur", fontsize=11)
    axes[1].set_ylabel("Retensi Relatif (% dari Clean)", fontsize=11)
    axes[1].set_ylim(0, 100)
    axes[1].legend(fontsize=9.5)

    plt.tight_layout()
    fig_path = FIG_DIR / "e4_noise_profile_sensitivity.png"
    plt.savefig(fig_path, dpi=300)
    plt.savefig(PAPER_FIG_DIR / "e4_noise_profile_sensitivity.png", dpi=300)
    plt.close()

    print(f"[+] Grafik E4 berhasil disimpan di: {fig_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
