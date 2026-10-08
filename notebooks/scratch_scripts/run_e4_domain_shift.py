import os
import sys
import numpy as np
import pandas as pd
import librosa
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocess import preprocess_audio, TARGET_SR, TARGET_SAMPLES
from src.embeddings import AudioRepresentationExtractor
from src.mix_noise import compute_signal_power
from src.retrieve import evaluate_retrieval_corpus

SPLIT_PATH = PROJECT_ROOT / "data/manifests/dataset_split.csv"
SOUNDSCAPE_DIR = PROJECT_ROOT / "data/BirdClef/train_soundscapes"
E4_RESULTS_PATH = PROJECT_ROOT / "results/processed/e4_domain_shift_table.csv"

def get_soundscape_noise_segment(samples: int, seed: int = 42) -> np.ndarray:
    """Mengambil segmen acak dari dataset soundscape alam bebas BirdCLEF."""
    rng = np.random.default_rng(seed)
    ogg_files = [f for f in os.listdir(SOUNDSCAPE_DIR) if f.endswith('.ogg')]
    selected = str(SOUNDSCAPE_DIR / rng.choice(ogg_files))
    
    try:
        y, _ = librosa.load(selected, sr=TARGET_SR, mono=True)
        if len(y) >= samples:
            start = rng.integers(0, len(y) - samples + 1)
            return y[start:start + samples].astype(np.float32)
        else:
            repeats = int(np.ceil(samples / len(y)))
            y = np.tile(y, repeats)
            return y[:samples].astype(np.float32)
    except Exception as e:
        print(f"Error loading {selected}: {e}")
        return np.zeros(samples, dtype=np.float32)

def mix_with_soundscape(clean: np.ndarray, snr_db: float, seed: int = 42) -> np.ndarray:
    """Mencampur sinyal dengan derau soundscape pada rasio SNR tertentu."""
    noise = get_soundscape_noise_segment(samples=len(clean), seed=seed)
    
    p_signal = compute_signal_power(clean)
    p_noise = compute_signal_power(noise)
    
    if p_signal <= 1e-12 or p_noise <= 1e-12:
        return clean
        
    target_p_noise = p_signal / (10.0 ** (snr_db / 10.0))
    alpha = np.sqrt(target_p_noise / p_noise)
    noisy = clean + alpha * noise
    
    max_amp = np.max(np.abs(noisy))
    if max_amp > 1.0:
        noisy = noisy / max_amp
        
    return noisy.astype(np.float32)

def main():
    print("Memulai Eksekusi E4: Real Soundscape Domain Shift...")
    if not SOUNDSCAPE_DIR.exists():
        print(f"Error: Direktori {SOUNDSCAPE_DIR} tidak ditemukan!")
        return

    df_split = pd.read_csv(SPLIT_PATH)
    gallery_df = df_split[df_split['split_role'] == 'gallery']
    query_df = df_split[df_split['split_role'] == 'query_clean']

    snr_list = [20, 10, 0, -5]
    rep_codes = ["R0", "R1", "R2", "R3"]
    results = []

    for rep in rep_codes:
        print(f"\n--- Memproses {rep} ---")
        extractor = AudioRepresentationExtractor(rep)
        
        # Ekstraksi Gallery
        gallery_embs, gallery_labels = [], []
        for _, r in gallery_df.iterrows():
            y = preprocess_audio(r['file_path'])
            gallery_embs.append(extractor.extract(y))
            gallery_labels.append(r['species_key'])
        gallery_embs = np.array(gallery_embs)
        
        # Ekstraksi Query Clean
        query_audios, query_labels = [], []
        for _, r in query_df.iterrows():
            y = preprocess_audio(r['file_path'])
            query_audios.append(y)
            query_labels.append(r['species_key'])
            
        # Baseline Clean
        clean_embs = np.array([extractor.extract(y) for y in query_audios])
        clean_summary, _ = evaluate_retrieval_corpus(clean_embs, query_labels, gallery_embs, gallery_labels)
        clean_map = clean_summary["mAP@10"]
        print(f"[Clean] mAP@10: {clean_map:.4f}")
        
        results.append({
            "representation": rep, "condition": "Clean", "snr_db": 999,
            "mAP@10": clean_map, "Top1": clean_summary["mean_top1"]
        })
        
        # Evaluasi per SNR
        for snr in snr_list:
            noisy_embs = []
            for i, y_clean in enumerate(query_audios):
                y_noisy = mix_with_soundscape(y_clean, snr_db=snr, seed=100+i)
                noisy_embs.append(extractor.extract(y_noisy))
            noisy_embs = np.array(noisy_embs)
            
            noisy_summary, _ = evaluate_retrieval_corpus(noisy_embs, query_labels, gallery_embs, gallery_labels)
            print(f"[SNR {snr:3d} dB] mAP@10: {noisy_summary['mAP@10']:.4f}")
            
            results.append({
                "representation": rep, "condition": f"SNR_{snr}dB", "snr_db": snr,
                "mAP@10": noisy_summary["mAP@10"], "Top1": noisy_summary["mean_top1"]
            })
            
    df_results = pd.DataFrame(results)
    df_results.to_csv(E4_RESULTS_PATH, index=False)
    print(f"\nSelesai! Hasil disimpan di {E4_RESULTS_PATH}")

if __name__ == "__main__":
    main()
