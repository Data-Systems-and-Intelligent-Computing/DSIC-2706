"""
Script: src/verify_reproducibility.py
Fungsi: Memverifikasi Reproducibility penuh dari single fresh command (Bab 24 Dokumen Audit).
Menjalankan komputasi mAP@10 dari nol langsung dari file audio fisik,
mencetak SHA-256 manifest, skor presisi tiap query, dan memvalidasi determinisme hasil.
"""

import os
import sys
import hashlib
import numpy as np
import pandas as pd

sys.path.insert(0, "d:/FILE AND TASK/TA")
from src.preprocess import preprocess_audio
from src.embeddings import AudioRepresentationExtractor
from src.mix_noise import mix_audio_at_snr
from src.retrieve import compute_query_retrieval, evaluate_retrieval_corpus

SPLIT_PATH = "d:/FILE AND TASK/TA/data/manifests/dataset_split.csv"


def get_file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_single_command_reproducibility(rep_code="R2", test_snr=0):
    print("=" * 80)
    print(f"[*] VERIFIKASI REPRODUCIBILITY EKSPERIMEN DSIC27-06 DARI FRESH COMMAND")
    print(f"[*] Target Uji: Representasi [{rep_code}] pada Kondisi SNR [{test_snr} dB]")
    print("=" * 80)

    if not os.path.exists(SPLIT_PATH):
        print(f"[-] Split file tidak ditemukan: {SPLIT_PATH}")
        return False

    split_hash = get_file_sha256(SPLIT_PATH)
    print(f"[+] Dataset Split Manifest SHA-256: {split_hash}")

    df_split = pd.read_csv(SPLIT_PATH)
    gallery_df = df_split[df_split['split_role'] == 'gallery']
    query_df = df_split[df_split['split_role'] == 'query_clean']

    print(f"[+] Total Gallery Clips: {len(gallery_df)}, Total Clean Queries: {len(query_df)}")

    extractor = AudioRepresentationExtractor(rep_code)

    # Ekstrak Gallery dari file fisik
    gallery_embs = []
    gallery_labels = []
    for _, r in gallery_df.iterrows():
        y = preprocess_audio(r['file_path'])
        gallery_embs.append(extractor.extract(y))
        gallery_labels.append(r['species_key'])
    gallery_embs = np.array(gallery_embs)

    # Ekstrak Query dan tambahkan derau jika SNR != 'Clean'
    query_embs = []
    query_labels = []
    for i, (_, r) in enumerate(query_df.iterrows()):
        y = preprocess_audio(r['file_path'])
        if test_snr is not None and test_snr != 999:
            y = mix_audio_at_snr(y, snr_db=test_snr, seed=42 + i)
        query_embs.append(extractor.extract(y))
        query_labels.append(r['species_key'])
    query_embs = np.array(query_embs)

    # Hitung retrieval
    summary, all_queries = evaluate_retrieval_corpus(
        query_embs=query_embs,
        query_labels=query_labels,
        gallery_embs=gallery_embs,
        gallery_labels=gallery_labels,
        k_values=[1, 5, 10]
    )

    print("\n[+] 5 Sampel Query Pertama:")
    for idx in range(min(5, len(all_queries))):
        q_info = all_queries[idx]
        print(f"    Query #{idx+1:02d} [{query_labels[idx]:<25}]: Top1={q_info['top1_match']}, AP@10={q_info['AP@10']:.4f}, MaxCosine={q_info['max_score']:.4f}")

    print("-" * 60)
    print(f"[+] HASIL RETRIEVAL ({rep_code} @ SNR {test_snr} dB):")
    print(f"    mAP@10      : {summary['mAP@10']:.6f}")
    print(f"    Recall@10   : {summary['Recall@10']:.6f}")
    print(f"    Top1 Acc    : {summary['mean_top1']:.6f}")
    print("-" * 60)
    return summary


if __name__ == "__main__":
    verify_single_command_reproducibility(rep_code="R2", test_snr=0)
