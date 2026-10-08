import os
import wave
import numpy as np
import pandas as pd
import hashlib

MANIFEST_PATH = r"D:\FILE AND TASK\TA\data\manifests\itera_noise_manifest.csv"
DATA_DIR = r"D:\FILE AND TASK\TA\data\itera_noise"

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def main():
    df = pd.read_csv(MANIFEST_PATH, dtype={'catatan': str})
    
    corrupted_files = []
    clipped_files = []
    
    print(f"Memulai 'playback' dan verifikasi matematis frame-by-frame untuk {len(df)} file WAV...")
    
    for idx, row in df.iterrows():
        filepath = os.path.join(DATA_DIR, row['source_file'])
        
        if not os.path.exists(filepath):
            corrupted_files.append((row['source_file'], "File missing"))
            continue
            
        # 1. Verify SHA-256 match against manifest
        sha = get_sha256(filepath)
        if sha != row['sha256']:
            corrupted_files.append((row['source_file'], "SHA-256 mismatch"))
            continue
            
        try:
            # 2. Simulate "Play" by strictly decoding all PCM frames
            with wave.open(filepath, 'rb') as wf:
                n_frames = wf.getnframes()
                audio_data = wf.readframes(n_frames)
                
                # 3. Check for structural corruption
                if len(audio_data) != n_frames * wf.getsampwidth() * wf.getnchannels():
                    corrupted_files.append((row['source_file'], "Incomplete PCM data chunk"))
                    continue
                
                # 4. Check for clipping (values hitting exact limits of 16-bit PCM)
                audio_np = np.frombuffer(audio_data, dtype=np.int16)
                clip_count = np.sum((audio_np == 32767) | (audio_np == -32768))
                clip_ratio = clip_count / len(audio_np)
                
                # Alert if more than 1% of the audio is completely clipped
                if clip_ratio > 0.01:
                    clipped_files.append((row['source_file'], clip_ratio))
                    
                # 5. Verify Peak consistency
                peak_val = np.max(np.abs(audio_np)) / 32768.0
                if abs(peak_val - row['peak']) > 0.01:
                    corrupted_files.append((row['source_file'], f"Peak mismatch (Manifest: {row['peak']:.3f}, Actual: {peak_val:.3f})"))
                    
        except Exception as e:
            corrupted_files.append((row['source_file'], f"Corrupt frame/header: {str(e)}"))
            
        if (idx + 1) % 200 == 0:
            print(f"Telah memutar dan memverifikasi {idx + 1}/{len(df)} file...", flush=True)

    print("\n--- HASIL VERIFIKASI AKHIR ---")
    if not corrupted_files:
        print("KORUPSI & KONSISTENSI DATA : [LULUS] 0 file bermasalah. Seluruh WAV utuh.")
    else:
        print(f"KORUPSI DITEMUKAN PADA {len(corrupted_files)} FILE:")
        for f, reason in corrupted_files:
            print(f"- {f}: {reason}")
            
    if not clipped_files:
        print("INDIKASI CLIPPING          : [LULUS] 0 file mengalami clipping berlebih (>1%).")
    else:
        print(f"CLIPPING BERLEBIH PADA {len(clipped_files)} FILE:")
        for f, ratio in clipped_files:
            print(f"- {f}: {ratio:.2%} sampel mengalami kliping")
            
    print("Inspeksi tuntas.")

if __name__ == "__main__":
    main()
