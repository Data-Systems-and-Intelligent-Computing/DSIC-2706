import os
import wave
import re
import numpy as np
import pandas as pd

BASE_DIR = r"D:\FILE AND TASK\TA\data\itera_noise\Masjid At-tanwir Frequency"

def parse_header_metadata(filepath):
    info_text = ""
    with open(filepath, "rb") as f:
        content = f.read(1024)
        match = re.search(rb"Recorded at ([^\x00]+)", content)
        if match:
            raw_str = match.group(0).decode("ascii", errors="ignore")
            # Clean up trailing non-printables
            clean_str = re.split(r"[\x00-\x08\x0b-\x1f]", raw_str)[0].strip()
            info_text = clean_str
    return info_text

def analyze_all_files():
    folders = [
        ("32 kHz Low Frequency", "Low", "13:25 - 14:25", (-5.357172, 105.318735)),
        ("32 kHz Medium Frequency", "Medium", "14:40 - 15:40", (-5.357195, 105.318391)),
        ("32 kHz High Frequency", "High", "15:55 - 16:55", (-5.357166, 105.318973)),
    ]

    records = []

    for folder_name, target_gain, planned_time, coords in folders:
        folder_path = os.path.join(BASE_DIR, folder_name)
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue

        wav_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(".wav")])
        print(f"Analyzing {folder_name}: {len(wav_files)} files...")

        for idx, filename in enumerate(wav_files):
            file_path = os.path.join(folder_path, filename)
            meta_str = parse_header_metadata(file_path)

            # Parse AudioMoth header text
            # e.g.: Recorded at 14:18:00 18/09/2026 (UTC+7) by AudioMoth 24F31901603767F6 at low gain while battery was 4.7V and temperature was 33.9C. Frequency trigger (4.0kHz and window length of 64 samples) threshold was 0.1% with 1s minimum trigger duration.
            time_match = re.search(r"Recorded at (\d{2}:\d{2}:\d{2})", meta_str)
            rec_time = time_match.group(1) if time_match else filename[:15]

            gain_match = re.search(r"at (low|medium|high|very low|very high) gain", meta_str, re.IGNORECASE)
            actual_gain = gain_match.group(1).capitalize() if gain_match else "Unknown"

            battery_match = re.search(r"battery was ([\d\.]+)V", meta_str)
            battery = float(battery_match.group(1)) if battery_match else np.nan

            temp_match = re.search(r"temperature was ([\d\.]+)C", meta_str)
            temp = float(temp_match.group(1)) if temp_match else np.nan

            trigger_match = re.search(r"Frequency trigger \(([\d\.]+)kHz and window length of (\d+) samples\) threshold was ([\d\.]+)% with (\d+)s minimum trigger duration", meta_str)
            if trigger_match:
                trig_center_khz = float(trigger_match.group(1))
                trig_window = int(trigger_match.group(2))
                trig_threshold = float(trigger_match.group(3))
                trig_min_dur = int(trigger_match.group(4))
            else:
                trig_center_khz, trig_window, trig_threshold, trig_min_dur = np.nan, np.nan, np.nan, np.nan

            # Signal properties from wave
            with wave.open(file_path, "rb") as w:
                n_channels = w.getnchannels()
                sampwidth = w.getsampwidth()
                framerate = w.getframerate()
                n_frames = w.getnframes()
                duration = n_frames / framerate
                
                # Read audio samples
                frames = w.readframes(n_frames)
                audio_data = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0

            # Acoustic statistics
            rms = float(np.sqrt(np.mean(audio_data ** 2)))
            peak = float(np.max(np.abs(audio_data)))
            clipping_samples = int(np.sum(np.abs(audio_data) >= 0.999))
            clipping_ratio = float(clipping_samples / len(audio_data))
            dc_offset = float(np.mean(audio_data))

            records.append({
                "folder": folder_name,
                "target_gain": target_gain,
                "planned_time": planned_time,
                "lat": coords[0],
                "lon": coords[1],
                "file_idx": idx + 1,
                "filename": filename,
                "rec_time": rec_time,
                "channels": n_channels,
                "framerate": framerate,
                "duration_sec": duration,
                "actual_gain": actual_gain,
                "battery_v": battery,
                "temp_c": temp,
                "trig_center_khz": trig_center_khz,
                "trig_window": trig_window,
                "trig_threshold_pct": trig_threshold,
                "trig_min_dur_s": trig_min_dur,
                "rms": rms,
                "peak": peak,
                "clipping_samples": clipping_samples,
                "clipping_ratio": clipping_ratio,
                "dc_offset": dc_offset
            })

    df = pd.DataFrame(records)
    out_csv = r"D:\FILE AND TASK\TA\data\itera_noise\Masjid At-tanwir Frequency\analysis_summary.csv"
    df.to_csv(out_csv, index=False)
    print(f"\nSaved full analysis to {out_csv}")
    return df

if __name__ == "__main__":
    analyze_all_files()
