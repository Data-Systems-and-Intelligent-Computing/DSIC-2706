"""
convert_wav_to_mp3.py
Konversi semua file .wav di dataset ke .mp3
- Nama file tetap sama (hanya ekstensi diganti)
- File .wav asli dihapus setelah konversi berhasil
- Bitrate 128kbps (standar xeno-canto)
"""

import os
from pydub import AudioSegment

ROOT = r"D:\FILE AND TASK\TA\data\xeno_canto"

def log(msg):
    print(msg, flush=True)

# Kumpulkan semua file .wav
wav_files = []
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f.lower().endswith(".wav"):
            wav_files.append(os.path.join(root, f))

log("=" * 60)
log(f"  Konversi WAV -> MP3")
log(f"  Ditemukan {len(wav_files)} file .wav")
log("=" * 60)

success = 0
failed  = 0

for wav_path in wav_files:
    # Nama MP3 = nama WAV tapi ganti ekstensinya
    mp3_path = os.path.splitext(wav_path)[0] + ".mp3"
    fname    = os.path.basename(wav_path)

    log(f"\n[KONVERSI] {fname}")
    log(f"  Input : {wav_path}")
    log(f"  Output: {mp3_path}")

    try:
        audio = AudioSegment.from_wav(wav_path)

        # Ambil sampling rate asli dari WAV
        sr = audio.frame_rate
        log(f"  Sampling Rate  : {sr} Hz")
        log(f"  Channels       : {audio.channels}")
        log(f"  Duration       : {round(len(audio)/1000, 2)} detik")

        # Export ke MP3, sampling rate dipertahankan
        audio.export(
            mp3_path,
            format="mp3",
            bitrate="128k",
            parameters=["-ar", str(sr)]
        )

        # Verifikasi file output ada dan tidak kosong
        if os.path.exists(mp3_path) and os.path.getsize(mp3_path) > 0:
            size_kb = os.path.getsize(mp3_path) / 1024
            log(f"  [OK] MP3 tersimpan ({size_kb:.1f} KB)")

            # Hapus WAV asli
            os.remove(wav_path)
            log(f"  [HAPUS] WAV asli dihapus")
            success += 1
        else:
            log(f"  [ERROR] File MP3 tidak terbuat atau kosong!")
            failed += 1

    except Exception as e:
        log(f"  [ERROR] Gagal konversi: {e}")
        failed += 1

log(f"\n{'='*60}")
log(f"  SELESAI")
log(f"  Berhasil dikonversi : {success} file")
log(f"  Gagal               : {failed} file")
log("=" * 60)
