"""Latihan 1: baca metadata fisik tiga audio, tanpa dependensi tambahan.

Tidak mendekode gelombang audio, menghitung MFCC, atau menulis berkas.
Durasi WAV dihitung dari jumlah sampel; durasi MP3 dari frame MPEG.
"""

from pathlib import Path
import struct


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILES = (
    ("Query", "savnig1/XC42472.mp3"),
    ("Gallery relevan", "savnig1/XC120964.mp3"),
    ("Gallery berbeda", "ashtai1/XC1003648.mp3"),
)


def read_wav_info(data):
    """Baca chunk RIFF; termasuk WAV float yang bernama .mp3."""
    riff_end = 8 + struct.unpack_from("<I", data, 4)[0]
    if riff_end > len(data):
        raise ValueError("WAV terpotong: ukuran RIFF melebihi ukuran file.")
    offset = 12
    fmt = None
    data_size = None
    while offset + 8 <= riff_end:
        tag = data[offset : offset + 4]
        size = struct.unpack_from("<I", data, offset + 4)[0]
        start = offset + 8
        if start + size > riff_end:
            raise ValueError("Chunk WAV terpotong.")
        if tag == b"fmt ":
            if size < 16:
                raise ValueError("Header format WAV tidak lengkap.")
            fmt = struct.unpack_from("<HHIIHH", data, start)
        elif tag == b"data":
            if data_size is not None:
                raise ValueError("WAV multi-data belum didukung latihan ini.")
            data_size = size
        offset = start + size + size % 2
    if fmt is None or data_size is None:
        raise ValueError("WAV tidak memiliki chunk format/data.")
    encoding, channels, rate, byte_rate, block_align, bits = fmt
    if encoding not in (1, 3) or not rate or not channels or not block_align:
        raise ValueError("Format WAV belum didukung latihan ini.")
    if byte_rate != rate * block_align or data_size % block_align:
        raise ValueError("Ukuran sampel WAV tidak konsisten.")
    return "WAV", data_size / block_align / rate, rate, channels


def mp3_frame_header(data, offset):
    """Kembalikan ukuran frame, sampling rate, kanal, dan sampel MPEG Layer III."""
    if offset + 4 > len(data):
        return None
    header = int.from_bytes(data[offset : offset + 4], "big")
    if header >> 21 != 0x7FF:
        return None
    version = (header >> 19) & 3
    layer = (header >> 17) & 3
    bitrate_index = (header >> 12) & 15
    rate_index = (header >> 10) & 3
    if version == 1 or layer != 1 or bitrate_index in (0, 15) or rate_index == 3:
        return None
    bitrates = (
        (0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320)
        if version == 3 else
        (0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160)
    )
    rate = (44100, 48000, 32000)[rate_index] // {3: 1, 2: 2, 0: 4}[version]
    samples = 1152 if version == 3 else 576
    size = (144 if version == 3 else 72) * bitrates[bitrate_index] * 1000 // rate
    size += (header >> 9) & 1
    channels = 1 if ((header >> 6) & 3) == 3 else 2
    return size, rate, channels, samples


def read_mp3_info(data):
    offset = 0
    if data[:3] == b"ID3":
        if len(data) < 10 or any(value & 0x80 for value in data[6:10]):
            raise ValueError("Header ID3 tidak valid.")
        tag_size = 0
        for value in data[6:10]:
            tag_size = (tag_size << 7) | value
        offset = 10 + tag_size
        if data[3] == 4 and data[5] & 0x10:
            offset += 10  # Footer ID3v2.4 tidak termasuk ukuran tag.

    # Dua header berturut-turut mengurangi risiko mengira isi tag sebagai audio.
    while offset + 4 <= len(data):
        frame = mp3_frame_header(data, offset)
        if frame:
            next_frame = mp3_frame_header(data, offset + frame[0])
            if next_frame and frame[1:] == next_frame[1:]:
                break
        offset += 1
    else:
        raise ValueError("Frame MP3 yang didukung tidak ditemukan.")

    rate, channels = frame[1:3]
    total_samples = 0
    while True:
        frame = mp3_frame_header(data, offset)
        if frame is None:
            break
        size, current_rate, current_channels, samples = frame
        if (current_rate, current_channels) != (rate, channels):
            raise ValueError("Sampling rate/kanal MP3 berubah di tengah file.")
        if offset + size > len(data):
            raise ValueError("Frame MP3 terakhir terpotong.")
        total_samples += samples
        offset += size
    # Jangan diam-diam mengabaikan kerusakan di tengah stream.
    tail = data[offset:]
    if tail and not (tail.startswith((b"TAG", b"APETAGEX", b"ID3")) or not any(tail)):
        raise ValueError("Ada data sisa tak dikenali setelah frame MP3.")
    return "MP3", total_samples / rate, rate, channels


def read_audio_info(path):
    data = path.read_bytes()
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WAVE":
        return read_wav_info(data)
    return read_mp3_info(data)


def main():
    print("LATIHAN 1 - MENGENAL TIGA FILE AUDIO")
    print("Informasi dibaca dari isi file. Tidak ada file yang diubah.\n")
    for role, relative_path in FILES:
        path = PROJECT_ROOT / "data/xeno_canto_indonesia" / relative_path
        try:
            audio_format, duration, rate, channels = read_audio_info(path)
        except (OSError, ValueError, struct.error) as error:
            print(f"GAGAL membaca {path.name}: {error}")
            return 1
        print(f"File          : {path.name}")
        print(f"Peran latihan : {role}")
        print(f"Format isi    : {audio_format}")
        print(f"Durasi        : {duration:.2f} detik")
        print(f"Sampling rate : {rate} Hz")
        print(f"Kanal         : {channels} ({'mono' if channels == 1 else 'stereo'})")
        if audio_format == "WAV" and path.suffix.lower() == ".mp3":
            print("Catatan       : Nama berakhiran .mp3, tetapi isi file WAV.")
        print()
    print("Durasi MP3 berdasarkan frame; belum memperhitungkan encoder delay/padding.")
    print("SELESAI. Belum menghitung MFCC atau menjalankan eksperimen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
