"""
Script: scripts/audit_gedung_f_birdnet.py
Fungsi: Audit akustik dan pencocokan BirdNET terhadap 8 berkas Gedung F Frequency yang menghasilkan False Accept di E3.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd
import soundfile as sf
import scipy.signal as signal

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.embeddings import AudioRepresentationExtractor
from src.preprocess import preprocess_audio

def main():
    print("=" * 80)
    print("[*] AUDIT AKUSTIK & INFERENSI BIRDNET TERHADAP 8 BERKAS GEDUNG F FREQUENCY")
    print("=" * 80)

    # 1. Muat Galeri dan Fitur R2
    npz_data = np.load(PROJECT_ROOT / "results/features/clean_embeddings_R2.npz")
    gal_feats = npz_data["gal_feats"]  # (3653, 1024)
    split_df = pd.read_csv(PROJECT_ROOT / "data/manifests/dataset_split.csv")
    gal_df = split_df[split_df["split_role"] == "gallery"].reset_index(drop=True)

    extractor = AudioRepresentationExtractor("R2")
    frozen_tau = 0.7128

    files = [
        ("UNK_TEST_NOISE_014", "data/itera_noise/Gedung F Frequency/32 kHz High Frequency/20260923_162500T.WAV"),
        ("UNK_TEST_NOISE_028", "data/itera_noise/Gedung F Frequency/32 kHz Low Frequency/20260923_101900T.WAV"),
        ("UNK_TEST_NOISE_036", "data/itera_noise/Gedung F Frequency/32 kHz Medium Frequency/20260923_113900T.WAV"),
        ("UNK_TEST_NOISE_037", "data/itera_noise/Gedung F Frequency/32 kHz Low Frequency/20260923_110100T.WAV"),
        ("UNK_TEST_NOISE_043", "data/itera_noise/Gedung F Frequency/32 kHz High Frequency/20260923_164600T.WAV"),
        ("UNK_TEST_NOISE_058", "data/itera_noise/Gedung F Frequency/32 kHz High Frequency/20260923_170000T.WAV"),
        ("UNK_TEST_NOISE_092", "data/itera_noise/Gedung F Frequency/32 kHz Low Frequency/20260923_102700T.WAV"),
        ("UNK_TEST_NOISE_095", "data/itera_noise/Gedung F Frequency/32 kHz Medium Frequency/20260923_120400T.WAV")
    ]

    results = []
    for qid, rel_path in files:
        full_path = PROJECT_ROOT / rel_path
        raw_audio, sr = sf.read(str(full_path))
        
        # Sinyal terproses (5.0 detik @ 32 kHz)
        proc_sig = preprocess_audio(str(full_path))
        emb = extractor.extract(proc_sig)
        
        # Kosinus kemiripan terhadap galeri
        sims = np.dot(gal_feats, emb)
        top_idx = np.argsort(sims)[::-1][:3]
        max_sim = float(sims[top_idx[0]])
        
        # Spektrum sinyal 5s
        freqs, psd = signal.welch(proc_sig, 32000, nperseg=2048)
        tot_p = np.sum(psd)
        p_sub1k = np.sum(psd[freqs < 1000]) / tot_p * 100
        p_1_4k = np.sum(psd[(freqs >= 1000) & (freqs < 4000)]) / tot_p * 100
        p_4_8k = np.sum(psd[(freqs >= 4000) & (freqs < 8000)]) / tot_p * 100
        
        # Peak frekuensi di wilayah >500 Hz
        mask_mid = freqs >= 500
        f_mid = freqs[mask_mid]
        psd_mid = psd[mask_mid]
        top_freq = f_mid[np.argmax(psd_mid)]
        
        top1_row = gal_df.iloc[top_idx[0]]
        top1_sp = top1_row["species_key"]
        top1_cname = top1_row["common_name"]
        
        top2_row = gal_df.iloc[top_idx[1]]
        top2_sp = top2_row["species_key"]
        top2_cname = top2_row["common_name"]
        
        results.append({
            "Query ID": qid,
            "Berkas": Path(rel_path).name,
            "Waktu": Path(rel_path).parent.name,
            "Max Cosine Sim": max_sim,
            "Status vs tau*": "False Accept" if max_sim >= frozen_tau else "True Reject",
            "Top-1 Matched Species": f"{top1_sp} ({top1_cname})",
            "Top-1 Sim": float(sims[top_idx[0]]),
            "Top-2 Matched Species": f"{top2_sp} ({top2_cname})",
            "Top-2 Sim": float(sims[top_idx[1]]),
            "Sub-1kHz (%)": p_sub1k,
            "1-4kHz (%)": p_1_4k,
            "4-8kHz (%)": p_4_8k,
            "Peak High Freq": top_freq
        })

    df_res = pd.DataFrame(results)
    print(df_res.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("[*] RINGKASAN TEMUAN EMPIRIS:")
    print("=" * 80)
    for _, r in df_res.iterrows():
        print(f"- {r['Query ID']} ({r['Berkas']}, {r['Waktu']}):")
        print(f"    Max Sim = {r['Max Cosine Sim']:.4f} melampaui tau* = {frozen_tau}")
        print(f"    Dicocokkan oleh BirdNET ke galeri: {r['Top-1 Matched Species']} (Sim={r['Top-1 Sim']:.4f})")
        print(f"    Karakteristik Akustik: Sub-1k={r['Sub-1kHz (%)']:.1f}%, 1-4k={r['1-4kHz (%)']:.1f}%, Peak={r['Peak High Freq']:.0f} Hz")
    
if __name__ == "__main__":
    main()
