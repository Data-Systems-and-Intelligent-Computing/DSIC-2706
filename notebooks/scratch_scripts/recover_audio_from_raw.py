import os
import re
import io
import wave
import hashlib
import time

LOG_PATH = r"C:\Users\Fabio\.gemini\antigravity\brain\29c8c496-9c02-45a8-aece-af8d01cc9493\.system_generated\tasks\task-2268.log"
DEST_BASE = r"D:\FILE AND TASK\TA\data\itera_noise\Data_Uji_4_Oktober_2026_Amplitudo"

os.makedirs(DEST_BASE, exist_ok=True)
folder_map = {
    "low": os.path.join(DEST_BASE, "32 kHz Low Amplitudo"),
    "medium": os.path.join(DEST_BASE, "32 kHz Medium Amplitudo"),
    "high": os.path.join(DEST_BASE, "32 kHz High Amplitudo")
}

for folder in folder_map.values():
    os.makedirs(folder, exist_ok=True)

print(f"[*] Menyiapkan folder tujuan pemulihan di: {DEST_BASE}")

# 1. Parse semua 180 catatan dari file log
with open(LOG_PATH, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

records = []
p_re = re.compile(r"\[\+\] Pukul (\d{2}):(\d{2}):(\d{2}) \| Gain:\s*(\w+)\s*\| Batt:\s*([\d\.]+)V \| Temp:\s*([\d\.]+)C \| Sektor/Offset:\s*(\d+)")

for line in lines:
    m = p_re.search(line)
    if m:
        hh, mm, ss, gain, batt, temp, offset_str = m.groups()
        rec_time = f"{hh}:{mm}:{ss}"
        fn = f"20261004_{hh}{mm}{ss}T.WAV"
        records.append({
            "time": rec_time,
            "filename": fn,
            "gain": gain.lower(),
            "batt": float(batt),
            "temp": float(temp),
            "offset": int(offset_str)
        })

print(f"[*] Berhasil memuat {len(records)} metadata rekaman dari log pemindaian.")

for g, subf in folder_map.items():
    sub_recs = [r for r in records if r["gain"] == g]
    print(f"    - {g.upper():6}: {len(sub_recs)} berkas (Target: 60)")

wav_len = 3520806
success_count = 0
failed_count = 0
skipped_count = 0

print("\n[*] Memulai proses ekstraksi sektor fisik (Read-Only)...")
t0 = time.time()

with open(r"\\.\E:", "rb") as disk:
    for idx, rec in enumerate(records, 1):
        target_dir = folder_map[rec["gain"]]
        dest_path = os.path.join(target_dir, rec["filename"])
        
        # Periksa apakah file sudah ada dan valid di disk tujuan
        if os.path.exists(dest_path) and os.path.getsize(dest_path) == wav_len:
            try:
                with wave.open(dest_path, "rb") as w:
                    if w.getnchannels() == 1 and w.getframerate() == 32000 and w.getnframes() == 1760000:
                        success_count += 1
                        skipped_count += 1
                        continue
            except:
                pass
        
        # Cari magic header RIFF
        aligned_sector = (rec["offset"] // 512) * 512
        disk.seek(aligned_sector)
        block = disk.read(4096)
        
        rel_date_idx = block.find(b"04/10/2026")
        if rel_date_idx == -1:
            print(f"[!] GAGAL mencari tanggal pada offset {rec['offset']} ({rec['filename']})")
            failed_count += 1
            continue
            
        rel_riff_idx = block.rfind(b"RIFF", 0, rel_date_idx)
        if rel_riff_idx == -1:
            print(f"[!] GAGAL mencari magic header RIFF pada {rec['filename']}")
            failed_count += 1
            continue
            
        riff_abs_offset = aligned_sector + rel_riff_idx
        riff_aligned_seek = (riff_abs_offset // 512) * 512
        seek_diff = riff_abs_offset - riff_aligned_seek
        
        disk.seek(riff_aligned_seek)
        raw_stream = disk.read(((wav_len + seek_diff + 511) // 512) * 512)
        wav_bytes = raw_stream[seek_diff : seek_diff + wav_len]
        
        try:
            bio = io.BytesIO(wav_bytes)
            with wave.open(bio, "rb") as w:
                ch = w.getnchannels()
                sr = w.getframerate()
                nf = w.getnframes()
                dur = nf / sr
                
            if ch != 1 or sr != 32000 or dur != 55.0:
                print(f"[!] Parameter audio tidak sesuai: ch={ch}, sr={sr}, dur={dur} ({rec['filename']})")
                failed_count += 1
                continue
                
            with open(dest_path, "wb") as out_f:
                out_f.write(wav_bytes)
                
            success_count += 1
            if idx % 10 == 0 or idx == len(records):
                print(f"    [{idx:>3}/{len(records)}] Berhasil diekstrak & divalidasi: {rec['filename']} ({dur:.1f}s, {rec['gain'].upper()})")
                
        except Exception as err:
            print(f"[!] Gagal validasi WAV {rec['filename']}: {err}")
            failed_count += 1

t1 = time.time()
print(f"\n[+] Ekstraksi selesai dalam {t1 - t0:.2f} detik!")
print(f"[+] Total Berkas Berhasil Dipulihkan: {success_count} / {len(records)} (Sudah ada sebelumnya: {skipped_count})")
print(f"[+] Total Berkas Gagal             : {failed_count}")
