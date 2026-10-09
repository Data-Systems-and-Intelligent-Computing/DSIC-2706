"""
Script: src/analyze_failures.py
Fungsi: Audit Kegagalan Saintifik Terstratifikasi Lintas Spesies (E5).
Taksonomi Moda Kegagalan Berdasarkan Kriteria Ambang Batas tau* dan Kesalahan Top-1 Match:
1. Sampel terstratifikasi acak N=30 kasus dari seluruh taksa burung:
   - 10 kasus Kondisi Clean (5 spesies unik R2 BirdNET + 5 spesies unik R1 PANNs)
   - 20 kasus Kondisi Derau SNR -5 dB (10 spesies unik R2 BirdNET + 10 spesies unik R1 PANNs)
2. Klasifikasi moda kegagalan objektif:
   - "Open-Set False Rejection": Top-1 match benar spesies target, namun max_sim < tau* (margin < 0)
   - "Top-1 Confusion (Above Tau)": max_sim >= tau* (margin >= 0) namun Top-1 match salah spesies
   - "Total Retrieval Collapse": max_sim < tau* DAN Top-1 match salah spesies
3. Pengukuran parameter fisik terukur:
   - spectral_centroid_hz, bandwidth_hz, mean_rms, top1_similarity, true_class_max_similarity, retrieval_gap, margin_to_tau.
"""

import os
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import librosa

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocess import preprocess_audio, TARGET_SR
from src.embeddings import AudioRepresentationExtractor
from src.mix_noise import mix_audio_at_snr

SPLIT_PATH = PROJECT_ROOT / "data/manifests/dataset_split.csv"
FEATURES_DIR = PROJECT_ROOT / "results/features"
PROCESSED_DIR = PROJECT_ROOT / "results/processed"
RAW_DIR = PROJECT_ROOT / "results/raw"
TABLES_DIR = PROJECT_ROOT / "paper/tables"

def compute_acoustic_features(y: np.ndarray, sr: int = TARGET_SR) -> dict:
    """Menghitung centroid spektral, bandwidth, dan RMS rata-rata sinyal audio nyata."""
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)
    bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)
    return {
        "spectral_centroid_hz": float(np.mean(cent)),
        "bandwidth_hz": float(np.mean(bw)),
        "mean_rms": float(np.mean(rms))
    }

def extract_real_failures_from_raw():
    print("=" * 80)
    print("[*] MEMULAI ANALISIS KEGAGALAN RETRIEVAL TERSTRATIFIKASI LINTAS SPESIES (E5)")
    print("=" * 80)

    df_split = pd.read_csv(SPLIT_PATH)
    gal_df = df_split[df_split["split_role"] == "gallery"].reset_index(drop=True)
    qry_df = df_split[df_split["split_role"] == "query_clean"].reset_index(drop=True)
    gal_labels = gal_df["species_key"].values

    tau_map = {"R2": 0.7128, "R1": 0.9117, "R0": 0.9953, "R3": 0.5090}
    tt_path = PROCESSED_DIR / "threshold_transfer_table.csv"
    if tt_path.exists():
        df_tt = pd.read_csv(tt_path)
        for _, r in df_tt.iterrows():
            tau_map[r["representation"]] = float(r["frozen_tau"])

    cases = []
    case_idx = 1
    rng = np.random.default_rng(42)

    # --- 1. Sampel 10 Kasus Kondisi Clean (5 spesies R2, 5 spesies R1) ---
    print("[*] Mengidentifikasi kegagalan kondisi Clean...")
    for rep in ["R2", "R1"]:
        tau = tau_map[rep]
        feats = np.load(FEATURES_DIR / f"clean_embeddings_{rep}.npz")
        gal_embs = feats["gal_feats"]
        qry_embs = feats["qry_feats"]

        g_norm = gal_embs / np.linalg.norm(gal_embs, axis=1, keepdims=True)
        q_norm = qry_embs / np.linalg.norm(qry_embs, axis=1, keepdims=True)
        sim_mat = np.dot(q_norm, g_norm.T)

        fails_by_sp = {}
        for i in range(len(qry_df)):
            row = qry_df.iloc[i]
            q_label = row["species_key"]
            top1_idx = int(np.argmax(sim_mat[i]))
            top1_species = gal_labels[top1_idx]
            max_sim = float(sim_mat[i, top1_idx])
            true_indices = np.where(gal_labels == q_label)[0]
            max_true_sim = float(np.max(sim_mat[i, true_indices]))

            if top1_species != q_label or max_sim < tau:
                fails_by_sp.setdefault(q_label, []).append({
                    "idx": i, "row": row, "top1_species": top1_species,
                    "max_sim": max_sim, "max_true_sim": max_true_sim
                })

        available_species = sorted(fails_by_sp.keys())
        chosen_species = rng.choice(available_species, size=min(5, len(available_species)), replace=False)

        for sp in sorted(chosen_species):
            item = fails_by_sp[sp][0]
            i = item["idx"]
            row = item["row"]
            top1_species = item["top1_species"]
            max_sim = item["max_sim"]
            max_true_sim = item["max_true_sim"]
            gap = max_sim - max_true_sim
            margin_tau = max_sim - tau

            y = preprocess_audio(row["file_path"])
            acoustics = compute_acoustic_features(y)

            if max_sim >= tau and top1_species != sp:
                fail_type = "Top-1 Confusion (Above Tau)"
                cause = "latent_representation_confusion"
                diag = (f"Kueri {sp} melampaui ambang batas (sim={max_sim:.4f} >= tau*={tau:.4f}) namun keliru "
                        f"dipasangkan ke {top1_species} (retrieval gap={gap:.4f}). Centroid spektral={acoustics['spectral_centroid_hz']:.0f} Hz.")
            elif max_sim < tau and top1_species == sp:
                fail_type = "Open-Set False Rejection"
                cause = "similarity_margin_deficit"
                diag = (f"Top-1 kueri {sp} mencocokkan taksa benar namun tertolak ambang batas (sim={max_sim:.4f} < "
                        f"tau*={tau:.4f}, margin={margin_tau:.4f}). Centroid spektral={acoustics['spectral_centroid_hz']:.0f} Hz.")
            else:
                fail_type = "Total Retrieval Collapse"
                cause = "acoustic_feature_overlap"
                diag = (f"Kueri {sp} mengalami kegagalan ganda: skor di bawah ambang batas (sim={max_sim:.4f} < "
                        f"tau*={tau:.4f}) dan salah dipasangkan ke {top1_species}. Centroid spektral={acoustics['spectral_centroid_hz']:.0f} Hz.")

            cases.append({
                "case_id": f"FAIL_{case_idx:03d}",
                "representation": rep,
                "condition": "Clean",
                "query_id": row["recording_id"],
                "query_species": sp,
                "recordist": row["author"],
                "predicted_top1_species": top1_species,
                "top1_similarity": round(max_sim, 4),
                "true_class_max_similarity": round(max_true_sim, 4),
                "retrieval_gap": round(gap, 4),
                "threshold_tau": round(tau, 4),
                "margin_to_tau": round(margin_tau, 4),
                "failure_type": fail_type,
                "spectral_centroid_hz": round(acoustics["spectral_centroid_hz"], 1),
                "bandwidth_hz": round(acoustics["bandwidth_hz"], 1),
                "primary_acoustic_cause": cause,
                "quantitative_diagnosis": diag
            })
            case_idx += 1

    # --- 2. Sampel 20 Kasus Kondisi Derau SNR -5 dB (10 spesies R2, 10 spesies R1) ---
    print("[*] Mengidentifikasi kegagalan kondisi Derau SNR -5 dB...")
    for rep in ["R2", "R1"]:
        tau = tau_map[rep]
        extractor = AudioRepresentationExtractor(rep)
        feats = np.load(FEATURES_DIR / f"clean_embeddings_{rep}.npz")
        gal_embs = feats["gal_feats"]
        g_norm = gal_embs / np.linalg.norm(gal_embs, axis=1, keepdims=True)

        fails_by_sp = {}
        for i in range(len(qry_df)):
            row = qry_df.iloc[i]
            q_label = row["species_key"]
            y_clean = preprocess_audio(row["file_path"])
            y_noisy = mix_audio_at_snr(y_clean, snr_db=-5, seed=42 + i)

            emb_noisy = extractor.extract(y_noisy)
            q_norm_vec = emb_noisy / max(np.linalg.norm(emb_noisy), 1e-8)
            sims = np.dot(g_norm, q_norm_vec)

            top1_idx = int(np.argmax(sims))
            top1_species = gal_labels[top1_idx]
            max_sim = float(sims[top1_idx])
            true_indices = np.where(gal_labels == q_label)[0]
            max_true_sim = float(np.max(sims[true_indices]))

            if top1_species != q_label or max_sim < tau:
                fails_by_sp.setdefault(q_label, []).append({
                    "idx": i, "row": row, "y_noisy": y_noisy,
                    "top1_species": top1_species, "max_sim": max_sim,
                    "max_true_sim": max_true_sim
                })

        available_species = sorted(fails_by_sp.keys())
        chosen_species = rng.choice(available_species, size=min(10, len(available_species)), replace=False)

        for sp in sorted(chosen_species):
            item = fails_by_sp[sp][0]
            i = item["idx"]
            row = item["row"]
            y_noisy = item["y_noisy"]
            top1_species = item["top1_species"]
            max_sim = item["max_sim"]
            max_true_sim = item["max_true_sim"]
            gap = max_sim - max_true_sim
            margin_tau = max_sim - tau

            acoustics = compute_acoustic_features(y_noisy)

            if max_sim < tau and top1_species == sp:
                fail_type = "Open-Set False Rejection"
                cause = "low_snr_signal_attenuation"
                diag = (f"Pada SNR -5 dB, Top-1 kueri {sp} berhasil mencocokkan taksa benar, namun tertolak oleh ambang "
                        f"tau*={tau:.4f} karena skor kemiripan tertekan ke {max_sim:.4f} (margin={margin_tau:.4f}). Centroid={acoustics['spectral_centroid_hz']:.0f} Hz.")
            elif max_sim >= tau and top1_species != sp:
                fail_type = "Top-1 Confusion (Above Tau)"
                cause = "latent_representation_confusion"
                diag = (f"Injeksi derau -5 dB menyebabkan artefak fitur pada {sp} yang secara keliru menempel ke "
                        f"{top1_species} dengan skor {max_sim:.4f} di atas tau*={tau:.4f}. Centroid={acoustics['spectral_centroid_hz']:.0f} Hz.")
            else:
                fail_type = "Total Retrieval Collapse"
                cause = "severe_noise_distortion"
                diag = (f"Pada SNR -5 dB, energi derau mendominasi kicauan {sp} (centroid={acoustics['spectral_centroid_hz']:.0f} Hz). "
                        f"Skor anjlok ke {max_sim:.4f} (< tau*={tau:.4f}) dan salah terpaut ke {top1_species}.")

            cases.append({
                "case_id": f"FAIL_{case_idx:03d}",
                "representation": rep,
                "condition": "SNR_-5dB",
                "query_id": row["recording_id"],
                "query_species": sp,
                "recordist": row["author"],
                "predicted_top1_species": top1_species,
                "top1_similarity": round(max_sim, 4),
                "true_class_max_similarity": round(max_true_sim, 4),
                "retrieval_gap": round(gap, 4),
                "threshold_tau": round(tau, 4),
                "margin_to_tau": round(margin_tau, 4),
                "failure_type": fail_type,
                "spectral_centroid_hz": round(acoustics["spectral_centroid_hz"], 1),
                "bandwidth_hz": round(acoustics["bandwidth_hz"], 1),
                "primary_acoustic_cause": cause,
                "quantitative_diagnosis": diag
            })
            case_idx += 1

    # 3. Simpan Tabel Audit Kegagalan
    df_fails = pd.DataFrame(cases)
    df_fails.to_csv(PROCESSED_DIR / "failure_analysis_table.csv", index=False)
    df_fails.to_csv(TABLES_DIR / "failure_analysis_table.csv", index=False)
    print(f"\n[+] Sukses menyimpan tabel analisis kegagalan: {PROCESSED_DIR / 'failure_analysis_table.csv'}")
    print(f"[+] Total kasus dianalisis: {len(df_fails)}")
    print("\n--- Distribusi Kondisi & Representasi ---")
    print(pd.crosstab(df_fails["condition"], df_fails["representation"]))
    print("\n--- Distribusi Tipe Kegagalan ---")
    print(df_fails["failure_type"].value_counts())
    print("\n--- Distribusi Spesies Kueri (Keragaman Taksa) ---")
    print(df_fails["query_species"].value_counts())

if __name__ == "__main__":
    extract_real_failures_from_raw()
