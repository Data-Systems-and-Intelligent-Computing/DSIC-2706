import os
import sys
import wave
import struct
import hashlib
import numpy as np
import pandas as pd
from datetime import datetime
import re

DATA_DIR = r"D:\FILE AND TASK\TA\DSIC-2706\data\itera_noise"
MANIFEST_OUT = r"D:\FILE AND TASK\TA\DSIC-2706\data\manifests\itera_noise_manifest.csv"

# Metadata mapping hardcoded from Notulensi
metadata_map = {
    "Masjid At-tanwir Frequency": {
        "Low": {"lat": -5.357172, "lon": 105.318735, "tanggal": "2026-09-18", "waktu": "13:25"},
        "Medium": {"lat": -5.357195, "lon": 105.318391, "tanggal": "2026-09-18", "waktu": "14:40"},
        "High": {"lat": -5.357166, "lon": 105.318973, "tanggal": "2026-09-18", "waktu": "15:55"}
    },
    "Embung F ITERA Frequency": {
        "Low": {"lat": -5.368573, "lon": 105.320346, "tanggal": "2026-09-20", "waktu": "12:50"},
        "Medium": {"lat": -5.369431, "lon": 105.319074, "tanggal": "2026-09-20", "waktu": "14:05"},
        "High": {"lat": -5.368220, "lon": 105.319832, "tanggal": "2026-09-20", "waktu": "15:25"}
    },
    "Kebun Raya Frequency": {
        "Low": {"lat": -5.368153, "lon": 105.311720, "tanggal": "2026-09-22", "waktu": "14:40"},
        "Medium": {"lat": -5.368818, "lon": 105.311696, "tanggal": "2026-09-22", "waktu": "12:05"},
        "High": {"lat": -5.368632, "lon": 105.312012, "tanggal": "2026-09-21", "waktu": "15:30"}
    },
    "Gedung F Frequency": {
        "Low": {"lat": -5.361041, "lon": 105.314209, "tanggal": "2026-09-23", "waktu": "10:10"},
        "Medium": {"lat": -5.361853, "lon": 105.313722, "tanggal": "2026-09-23", "waktu": "11:30"},
        "High": {"lat": -5.361734, "lon": 105.312915, "tanggal": "2026-09-23", "waktu": "16:10"}
    },
    "Sekitar GKU 1 Frequency": {
        "Low": {"lat": -5.359450, "lon": 105.311566, "tanggal": "2026-09-30", "waktu": "14:23"},
        "Medium": {"lat": -5.359040, "lon": 105.311758, "tanggal": "2026-09-30", "waktu": "15:30"},
        "High": {"lat": -5.358690, "lon": 105.312261, "tanggal": "2026-09-30", "waktu": "16:40"}
    },
    "Gedung F Amplitudo": {
        "Low": {"lat": -5.361192, "lon": 105.314100, "tanggal": "2026-10-01", "waktu": "11:30"},
        "Medium": {"lat": -5.361839, "lon": 105.313902, "tanggal": "2026-10-01", "waktu": "08:25"},
        "High": {"lat": -5.361941, "lon": 105.313175, "tanggal": "2026-10-01", "waktu": "15:00"}
    },
    "Masjid At-tanwir Amplitudo": {
        "Low": {"lat": -5.357215, "lon": 105.318768, "tanggal": "2026-10-02", "waktu": "12:05"},
        "Medium": {"lat": -5.357060, "lon": 105.318228, "tanggal": "2026-10-02", "waktu": "13:15"},
        "High": {"lat": -5.357256, "lon": 105.318604, "tanggal": "2026-10-02", "waktu": "14:30"}
    },
    "Embung F ITERA Amplitudo": {
        "Low": {"lat": -5.368902, "lon": 105.320293, "tanggal": "2026-10-04", "waktu": "12:25"},
        "Medium": {"lat": -5.369377, "lon": 105.319006, "tanggal": "2026-10-04", "waktu": "13:35"},
        "High": {"lat": -5.368215, "lon": 105.320026, "tanggal": "2026-10-04", "waktu": "14:50"}
    },
    "Sekitar GKU 1 Amplitudo": {
        "Low": {"lat": -5.359164, "lon": 105.311835, "tanggal": "2026-10-05", "waktu": "10:05"},
        "Medium": {"lat": -5.359642, "lon": 105.312365, "tanggal": "2026-10-05", "waktu": "11:15"},
        "High": {"lat": -5.358992, "lon": 105.311481, "tanggal": "2026-10-05", "waktu": "12:40"}
    },
    "Kebun Raya Amplitudo": {
        "Low": {"lat": -5.371499, "lon": 105.314085, "tanggal": "2026-10-07", "waktu": "10:35"},
        "Medium": {"lat": -5.369512, "lon": 105.313667, "tanggal": "2026-10-07", "waktu": "11:50"},
        "High": {"lat": -5.370206, "lon": 105.313788, "tanggal": "2026-10-07", "waktu": "13:00"}
    }
}

def get_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def get_audiomoth_metadata(filepath):
    comment = ""
    try:
        with open(filepath, 'rb') as f:
            f.seek(0)
            header = f.read(512)
            icmt_idx = header.find(b'ICMT')
            if icmt_idx != -1:
                size_bytes = header[icmt_idx+4:icmt_idx+8]
                size = struct.unpack('<I', size_bytes)[0]
                comment = header[icmt_idx+8:icmt_idx+8+size].decode('ascii', errors='ignore').strip('\x00')
    except Exception as e:
        pass
    
    device_id = "Unknown"
    firmware = "Unknown"
    gain_setting = "Unknown"
    filter_setting = "Unknown"
    
    # Example AudioMoth comment: 
    # "Recorded at 10:05:00 05/10/2026 (UTC) by AudioMoth 243B1F055C418923 at gain setting 2 while battery was 4.2V and temperature was 31.0C."
    # We can regex it
    m_dev = re.search(r"AudioMoth\s+([A-F0-9]+)", comment)
    if m_dev: device_id = m_dev.group(1)
    
    m_gain = re.search(r"gain setting\s+(\d)", comment)
    if m_gain: gain_setting = m_gain.group(1)
    
    return device_id, firmware, gain_setting, filter_setting

def get_audio_stats(filepath):
    try:
        with wave.open(filepath, 'rb') as wf:
            sr = wf.getframerate()
            n_frames = wf.getnframes()
            dur = n_frames / sr
            
            # Subsample for speed if needed, or full
            audio_data = wf.readframes(n_frames)
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            rms = np.sqrt(np.mean(audio_np**2))
            peak = np.max(np.abs(audio_np))
            return sr, dur, rms, peak
    except:
        return 32000, 55.0, 0.0, 0.0

def process():
    records = []
    
    # Process all WAV files
    wav_files = []
    for root, dirs, files in os.walk(DATA_DIR):
        for f in files:
            if f.upper().endswith('.WAV'):
                wav_files.append(os.path.join(root, f))
                
    print(f"Found {len(wav_files)} WAV files.")
    
    segment_id = 1
    for i, filepath in enumerate(wav_files):
        rel_path = os.path.relpath(filepath, DATA_DIR).replace('\\', '/')
        
        # Derive metadata from path
        parts = rel_path.split('/')
        if len(parts) >= 2:
            lokasi = parts[0]
            raw_detail = parts[1].lower() # e.g. "32 khz high amplitudo"
            if "low" in raw_detail:
                lokasi_detail = "Low"
            elif "medium" in raw_detail:
                lokasi_detail = "Medium"
            elif "high" in raw_detail:
                lokasi_detail = "High"
            else:
                lokasi_detail = "Unknown"
        else:
            lokasi = "Unknown"
            lokasi_detail = "Unknown"
            
        # Get GPS/Time from map
        meta = metadata_map.get(lokasi, {}).get(lokasi_detail, {})
        lat = meta.get("lat", "")
        lon = meta.get("lon", "")
        tanggal = meta.get("tanggal", "")
        waktu_mulai = meta.get("waktu", "")
        filter_type = "Amplitude" if "Amplitudo" in lokasi else "Frequency" if "Frequency" in lokasi else "Unknown"
        
        # Determine daypart
        daypart = "Siang" # Default
        
        # Audio metadata
        dev_id, fw, gain, _ = get_audiomoth_metadata(filepath)
        sr, dur, rms, peak = get_audio_stats(filepath)
        sha = get_sha256(filepath)
        
        records.append({
            "segment_id": f"NOISE_{segment_id:04d}",
            "source_file": rel_path,
            "start_sec": 0,
            "end_sec": dur,
            "duration_sec": dur,
            "lokasi": lokasi,
            "lokasi_detail": lokasi_detail,
            "latitude": lat,
            "longitude": lon,
            "tanggal": tanggal,
            "waktu_mulai": waktu_mulai,
            "daypart": daypart,
            "cuaca": "Cerah", # Default
            "device_id": dev_id,
            "firmware": fw,
            "sample_rate": sr,
            "gain": gain,
            "filter": filter_type,
            "rms": rms,
            "peak": peak,
            "bird_free": "Y",
            "verified_by": "System",
            "verified_date": datetime.now().strftime("%Y-%m-%d"),
            "catatan": "",
            "sha256": sha
        })
        
        segment_id += 1
        if (i+1) % 50 == 0:
            print(f"Processed {i+1}/{len(wav_files)} files...", flush=True)
            
    df = pd.DataFrame(records)
    df.to_csv(MANIFEST_OUT, index=False)
    print(f"Saved manifest to {MANIFEST_OUT}")

if __name__ == '__main__':
    process()
