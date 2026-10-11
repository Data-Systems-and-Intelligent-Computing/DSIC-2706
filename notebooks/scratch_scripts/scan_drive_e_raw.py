import os
import re
import sys
import time

TARGET_DATE = b"04/10/2026"
CHUNK_SIZE = 16 * 1024 * 1024  # 16 MB chunk
OVERLAP = 1024                 # 1 KB overlap between chunks

print("[*] Memulai pemindaian sektor fisik raw disk \\\\.\\E: ...")
start_time = time.time()

# 1. Catat semua file WAV yang sudah terdaftar di sistem berkas E:\
existing_files = []
for root, dirs, files in os.walk(r"E:\\"):
    # Jangan scan FOUND.000 atau System Volume Information jika tidak perlu, tapi catat semua
    for f in files:
        if f.upper().endswith(".WAV"):
            full_path = os.path.join(root, f)
            size = os.path.getsize(full_path)
            existing_files.append((full_path, size))

print(f"[*] Jumlah file WAV aktif di filesystem E:\\: {len(existing_files)}")
for p, s in existing_files:
    if "32 kHz" in p:
        # Tampilkan beberapa contoh
        pass

# 2. Buka raw volume \\.\E: dalam mode read-only binary
total_matches = []
try:
    with open(r"\\.\E:", "rb") as disk:
        offset = 0
        chunk_idx = 0
        carry = b""
        
        while True:
            raw_block = disk.read(CHUNK_SIZE)
            if not raw_block:
                break
            
            data = carry + raw_block
            data_len = len(data)
            
            pos = 0
            while True:
                idx = data.find(TARGET_DATE, pos)
                if idx == -1:
                    break
                
                # Hitung byte offset absolut pada disk
                abs_offset = offset - len(carry) + idx
                
                # Ambil konteks header AudioMoth
                ctx_start = max(0, idx - 60)
                ctx_end = min(data_len, idx + 200)
                ctx = data[ctx_start:ctx_end]
                
                # Ekstrak info waktu, gain, baterai, suhu jika ada
                m = re.search(rb"Recorded at (\d{2}:\d{2}:\d{2}) 04/10/2026.*?by AudioMoth (\w+).*?at (\w+[\-\w]*) gain while battery was ([\d\.]+)V and temperature was ([\d\.]+)C", ctx)
                if m:
                    rec_time = m.group(1).decode()
                    dev_id = m.group(2).decode()
                    gain = m.group(3).decode()
                    batt = m.group(4).decode()
                    temp = m.group(5).decode()
                    total_matches.append({
                        "offset": abs_offset,
                        "time": rec_time,
                        "gain": gain,
                        "battery": batt,
                        "temp": temp,
                        "context": ctx[:120]
                    })
                    print(f"  [+] Pukul {rec_time} | Gain: {gain:6} | Batt: {batt}V | Temp: {temp}C | Sektor/Offset: {abs_offset}")
                else:
                    # Deteksi header parsial / format lain
                    total_matches.append({
                        "offset": abs_offset,
                        "time": "UNKNOWN",
                        "gain": "UNKNOWN",
                        "battery": "-",
                        "temp": "-",
                        "context": ctx[:120]
                    })
                    print(f"  [?] Match non-standard pada offset {abs_offset}: {ctx[:60]}")
                
                pos = idx + len(TARGET_DATE)
            
            # Simpan potongan overlap untuk chunk berikutnya
            if len(raw_block) >= OVERLAP:
                carry = raw_block[-OVERLAP:]
            else:
                carry = b""
            
            offset += len(raw_block)
            chunk_idx += 1
            if chunk_idx % 64 == 0:
                gb = offset / (1024**3)
                elapsed = time.time() - start_time
                speed = (offset / (1024**2)) / max(1, elapsed)
                print(f"  ---> Telah dipindai {gb:.2f} GB ({speed:.1f} MB/s) | Ditemukan: {len(total_matches)} header...")

except Exception as err:
    print(f"[!] Error membaca raw disk: {err}")

elapsed = time.time() - start_time
print(f"\n[*] Selesai memindai seluruh volume {offset / (1024**3):.2f} GB dalam {elapsed:.1f} detik.")
print(f"[*] Total kecocokan header tanggal 04/10/2026 di seluruh sektor fisik: {len(total_matches)}")

# Rekapitulasi kecocokan berdasarkan gain
gains_found = {}
for m in total_matches:
    g = m["gain"].lower()
    gains_found.setdefault(g, []).append(m)

for g, items in gains_found.items():
    print(f"\n--- Kategori Gain: {g.upper()} (Total {len(items)} kemunculan) ---")
    times = [it["time"] for it in items]
    print(f"Rentang waktu: {times[0]} s.d. {times[-1]}")
    # Periksa apakah ada duplikasi offset atau entri terpisah
    unique_times = sorted(list(set(times)))
    print(f"Jumlah timestamp unik: {len(unique_times)}")
    if len(unique_times) < 100:
        print("Daftar waktu unik:", unique_times)
