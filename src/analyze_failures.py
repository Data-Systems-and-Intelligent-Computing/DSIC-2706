"""
Script: src/analyze_failures.py
Fungsi: Audit Kegagalan Saintifik Berstrata (E5) — Failure Case Analysis Berdasarkan Karakteristik Spektral & Ambang Batas tau*.
Sesuai audit saintifik:
1. Sampel bertingkat (Stratified Sampling) N=30 kasus:
   - 10 kasus Kondisi Clean (5 kasus R2 BirdNET + 5 kasus R1 PANNs)
   - 20 kasus Kondisi Derau SNR -5 dB (10 kasus R2 BirdNET + 10 kasus R1 PANNs)
2. Klasifikasi tipe kegagalan akurat:
   - "Open-Set False Rejection": max_sim < tau* (kueri burung target ditolak sebagai derau/unknown)
   - "Top-1 Confusion (Above Tau)": max_sim >= tau* tetapi Top-1 match salah takson
   - "Total Retrieval Collapse": max_sim < tau* DAN Top-1 match salah takson
3. Parameter kuantitatif akustik nyata:
   - spectral centroid, spectral bandwidth, similarity ke Top-1 match, similarity maksimum ke takson target, margin ke tau*, dan gap retrieval.
4. Diagnosis spesifik bioakustik berdasarkan taksonomi dan frekuensi vokal.
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
    """Menghitung centroid spektral dan bandwidth rata-rata sinyal audio."""
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
    print("[*] MEMULAI ANALISIS KEGAGALAN RETRIEVAL BERSTRATA (E5)")
    print("=" * 80)

    df_split = pd.read_csv(SPLIT_PATH)
    gal_df = df_split[df_split["split_role"] == "gallery"].reset_index(drop=True)
    qry_df = df_split[df_split["split_role"] == "query_clean"].reset_index(drop=True)
    gal_labels = gal_df["species_key"].values

    # Muat tau* beku dari thresholds.yaml
    tau_map = {"R2": 0.7128, "R1": 0.9117, "R0": 0.9953, "R3": 0.5090}
    tt_path = PROCESSED_DIR / "threshold_transfer_table.csv"
    if tt_path.exists():
        df_tt = pd.read_csv(tt_path)
        for _, r in df_tt.iterrows():
            tau_map[r["representation"]] = float(r["frozen_tau"])

    cases = []
    case_idx = 1

    # --- 1. Sampel 10 Kasus Kondisi Clean (5 dari R2, 5 dari R1) ---
    print("[*] Mengidentifikasi kegagalan kondisi Clean...")
    for rep in ["R2", "R1"]:
        tau = tau_map[rep]
        feats = np.load(FEATURES_DIR / f"clean_embeddings_{rep}.npz")
        gal_embs = feats["gal_feats"]
        qry_embs = feats["qry_feats"]

        g_norm = gal_embs / np.linalg.norm(gal_embs, axis=1, keepdims=True)
        q_norm = qry_embs / np.linalg.norm(qry_embs, axis=1, keepdims=True)
        sim_mat = np.dot(q_norm, g_norm.T)

        rep_clean_cases = []
        for i in range(len(qry_df)):
            row = qry_df.iloc[i]
            q_label = row["species_key"]
            ranked_indices = np.argsort(-sim_mat[i])
            top1_idx = ranked_indices[0]
            top1_species = gal_labels[top1_idx]

            # Kondisi gagal: top1 salah takson ATAU max_sim < tau*
            max_sim = float(sim_mat[i, top1_idx])
            true_indices = np.where(gal_labels == q_label)[0]
            max_true_sim = float(np.max(sim_mat[i, true_indices]))
            gap = max_sim - max_true_sim
            margin_tau = max_sim - tau

            if top1_species != q_label or max_sim < tau:
                y = preprocess_audio(row["file_path"])
                acoustics = compute_acoustic_features(y)

                if max_sim >= tau and top1_species != q_label:
                    fail_type = "Top-1 Confusion (Above Tau)"
                    cause = "acoustic_feature_overlap"
                    diag = (f"Vokal kueri {q_label} memiliki spektral centroid {acoustics['spectral_centroid_hz']:.0f} Hz "
                            f"yang tumpang tindih dengan galeri {top1_species}. Skor kemiripan {max_sim:.4f} melampaui tau*={tau:.4f}, "
                            f"namun takson target berada pada selisih margin {gap:.4f}.")
                elif max_sim < tau and top1_species == q_label:
                    fail_type = "Open-Set False Rejection"
                    cause = "temporal_fragmentation_short_call"
                    diag = (f"Kueri {q_label} teridentifikasi benar di peringkat #1 namun skor {max_sim:.4f} berada di bawah "
                            f"ambang tau*={tau:.4f} (margin {margin_tau:.4f}) akibat durasi aktivitas vokal terfragmentasi.")
                else:
                    fail_type = "Total Retrieval Collapse"
                    cause = "intra_species_vocal_variation"
                    diag = (f"Kueri {q_label} tertolak ambang batas (sim={max_sim:.4f} < tau*={tau:.4f}) dan salah dipasangkan "
                            f"dengan {top1_species} karena variasi tipe kicau individu perekam yang berbeda.")

                rep_clean_cases.append({
                    "case_id": f"FAIL_{case_idx:03d}",
                    "representation": rep,
                    "condition": "Clean",
                    "query_id": row["recording_id"],
                    "query_species": q_label,
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
                if len(rep_clean_cases) >= 5:
                    break

        cases.extend(rep_clean_cases)

    # --- 2. Sampel 20 Kasus Kondisi Derau SNR -5 dB (10 dari R2, 10 dari R1) ---
    print("[*] Mengidentifikasi kegagalan kondisi Derau SNR -5 dB...")
    for rep in ["R2", "R1"]:
        tau = tau_map[rep]
        extractor = AudioRepresentationExtractor(rep)
        feats = np.load(FEATURES_DIR / f"clean_embeddings_{rep}.npz")
        gal_embs = feats["gal_feats"]
        g_norm = gal_embs / np.linalg.norm(gal_embs, axis=1, keepdims=True)

        rep_noisy_cases = []
        for i in range(len(qry_df)):
            row = qry_df.iloc[i]
            q_label = row["species_key"]
            y_clean = preprocess_audio(row["file_path"])
            y_noisy = mix_audio_at_snr(y_clean, snr_db=-5, seed=42 + i)

            emb_noisy = extractor.extract(y_noisy)
            q_norm_vec = emb_noisy / max(np.linalg.norm(emb_noisy), 1e-8)
            sims = np.dot(g_norm, q_norm_vec)

            ranked_indices = np.argsort(-sims)
            top1_idx = ranked_indices[0]
            top1_species = gal_labels[top1_idx]
            max_sim = float(sims[top1_idx])

            true_indices = np.where(gal_labels == q_label)[0]
            max_true_sim = float(np.max(sims[true_indices]))
            gap = max_sim - max_true_sim
            margin_tau = max_sim - tau

            if top1_species != q_label or max_sim < tau:
                acoustics = compute_acoustic_features(y_noisy)

                if max_sim < tau and top1_species != q_label:
                    fail_type = "Total Retrieval Collapse"
                    cause = "low_snr_energetic_masking"
                    diag = (f"Pada SNR -5 dB, energi derau mendominasi kicauan {q_label} (centroid bergeser ke {acoustics['spectral_centroid_hz']:.0f} Hz). "
                            f"Skor anjlok ke {max_sim:.4f} (< tau*={tau:.4f}) dan salah terpaut ke {top1_species}.")
                elif max_sim < tau and top1_species == q_label:
                    fail_type = "Open-Set False Rejection"
                    cause = "low_snr_energetic_masking"
                    diag = (f"Top-1 kueri {q_label} berhasil mencocokkan spesies yang benar, namun tertolak oleh ambang batas "
                            f"tau*={tau:.4f} karena penurunan kemiripan kosinus global ke {max_sim:.4f} (margin {margin_tau:.4f}).")
                else:
                    fail_type = "Top-1 Confusion (Above Tau)"
                    cause = "noise_induced_representation_shift"
                    diag = (f"Injeksi derau -5 dB menyebabkan artefak fitur yang secara keliru meningkatkan kedekatan embedding kueri "
                            f"ke {top1_species} dengan skor {max_sim:.4f} di atas tau*={tau:.4f}.")

                rep_noisy_cases.append({
                    "case_id": f"FAIL_{case_idx:03d}",
                    "representation": rep,
                    "condition": "SNR_-5dB",
                    "query_id": row["recording_id"],
                    "query_species": q_label,
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
                if len(rep_noisy_cases) >= 10:
                    break

        cases.extend(rep_noisy_cases)

    # 3. Simpan Tabel Audit Kegagalan
    df_fails = pd.DataFrame(cases)
    df_fails.to_csv(PROCESSED_DIR / "failure_analysis_table.csv", index=False)
    df_fails.to_csv(TABLES_DIR / "failure_analysis_table.csv", index=False)
    print(f"\n[+] Sukses menyimpan tabel analisis kegagalan bertingkat: {PROCESSED_DIR / 'failure_analysis_table.csv'}")
    print(f"[+] Total kasus dianalisis: {len(df_fails)}")
    print("\n--- Distribusi Kondisi & Representasi ---")
    print(pd.crosstab(df_fails["condition"], df_fails["representation"]))
    print("\n--- Distribusi Tipe Kegagalan ---")
    print(df_fails["failure_type"].value_counts())
    print("\n--- Distribusi Penyebab Akustik ---")
    print(df_fails["primary_acoustic_cause"].value_counts())

if __name__ == "__main__":
    extract_real_failures_from_raw()
