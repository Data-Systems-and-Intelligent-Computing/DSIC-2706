import os
import wave
import struct
import numpy as np
import pandas as pd
import re

BASE_DIR = r"D:\FILE AND TASK\TA\data\itera_noise\Sekitar GKU 1 Frequency"

subdirs = [
    ("32 kHz Low Frequency", "Low"),
    ("32 kHz Medium Frequency", "Medium"),
    ("32 kHz High Frequency", "High")
]

results = []

for sname, target_gain in subdirs:
    spath = os.path.join(BASE_DIR, sname)
    if not os.path.exists(spath):
        print("Path not found:", spath)
        continue
    wavs = sorted([f for f in os.listdir(spath) if f.upper().endswith(".WAV")])
    print(f"=== {sname}: {len(wavs)} files ===")
    for f in wavs:
        fpath = os.path.join(spath, f)
        fsize = os.path.getsize(fpath)
        with wave.open(fpath, "rb") as wf:
            ch = wf.getnchannels()
            sw = wf.getsampwidth()
            sr = wf.getframerate()
            nf = wf.getnframes()
            dur = nf / float(sr)
            raw = wf.readframes(nf)
        
        with open(fpath, "rb") as raw_f:
            content = raw_f.read()
            icmt = ""
            pos = content.find(b"ICMT")
            if pos != -1:
                sz = struct.unpack("<I", content[pos+4:pos+8])[0]
                icmt = content[pos+8:pos+8+sz].decode("latin1", errors="ignore").strip("\x00")
        
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
        if len(samples) > 0:
            rms = float(np.sqrt(np.mean(samples**2)))
            peak = float(np.max(np.abs(samples)))
            dc = float(np.mean(samples))
            clips = int(np.sum(np.abs(samples) >= 0.999))
        else:
            rms, peak, dc, clips = 0.0, 0.0, 0.0, 0

        results.append({
            "folder": sname,
            "target_gain": target_gain,
            "filename": f,
            "filesize": fsize,
            "channels": ch,
            "sample_rate": sr,
            "duration": dur,
            "rms": rms,
            "peak": peak,
            "dc_offset": dc,
            "clipping": clips,
            "icmt": icmt
        })

df = pd.DataFrame(results)
print("Total analyzed:", len(df))
print("\n--- Summary per Folder ---")
for sname, grp in df.groupby("folder"):
    print(f"\nFolder: {sname}")
    print(f"Count: {len(grp)}")
    print(f"Duration: min={grp['duration'].min():.2f}s, mean={grp['duration'].mean():.2f}s, max={grp['duration'].max():.2f}s, exact_55s={(grp['duration']==55.0).sum()}")
    print(f"RMS: min={grp['rms'].min():.5f}, mean={grp['rms'].mean():.5f}, max={grp['rms'].max():.5f}")
    print(f"Peak: min={grp['peak'].min():.4f}, mean={grp['peak'].mean():.4f}, max={grp['peak'].max():.4f}")
    print(f"Clipping: files_with_clips={(grp['clipping']>0).sum()}, total_clips={grp['clipping'].sum()}")
