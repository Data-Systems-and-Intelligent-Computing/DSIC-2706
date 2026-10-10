"""
Script: scripts/listen_gedung_f.py
Fungsi: Memutar dan mendengarkan 8 audio Gedung F Frequency yang menghasilkan False Accept di E3.
"""

import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

FILES = [
    ("UNK_TEST_NOISE_014", "data/itera_noise/Gedung F Frequency/32 kHz High Frequency/20260923_162500T.WAV", "banana (Bananaquit)", 0.7335, "547 Hz (98.7% <1kHz)"),
    ("UNK_TEST_NOISE_028", "data/itera_noise/Gedung F Frequency/32 kHz Low Frequency/20260923_101900T.WAV", "whtdov (White-tipped Dove)", 0.7581, "516 Hz (87.4% <1kHz)"),
    ("UNK_TEST_NOISE_036", "data/itera_noise/Gedung F Frequency/32 kHz Medium Frequency/20260923_113900T.WAV", "whtdov (White-tipped Dove)", 0.7253, "500 Hz (98.0% <1kHz)"),
    ("UNK_TEST_NOISE_037", "data/itera_noise/Gedung F Frequency/32 kHz Low Frequency/20260923_110100T.WAV", "whtdov (White-tipped Dove)", 0.7794, "1891 Hz (96.8% <1kHz)"),
    ("UNK_TEST_NOISE_043", "data/itera_noise/Gedung F Frequency/32 kHz High Frequency/20260923_164600T.WAV", "sobtyr1 (S. Beardless Tyrannulet)", 0.7185, "875 Hz (95.4% <1kHz)"),
    ("UNK_TEST_NOISE_058", "data/itera_noise/Gedung F Frequency/32 kHz High Frequency/20260923_170000T.WAV", "banana (Bananaquit)", 0.7486, "594 Hz (95.2% <1kHz)"),
    ("UNK_TEST_NOISE_092", "data/itera_noise/Gedung F Frequency/32 kHz Low Frequency/20260923_102700T.WAV", "banana (Bananaquit)", 0.7531, "750 Hz (99.1% <1kHz)"),
    ("UNK_TEST_NOISE_095", "data/itera_noise/Gedung F Frequency/32 kHz Medium Frequency/20260923_120400T.WAV", "whtdov (White-tipped Dove)", 0.8018, "641 Hz (91.9% <1kHz)"),
]

def main():
    print("=" * 80)
    print("PEMUTAR AUDIO: 8 BERKAS GEDUNG F FREQUENCY (FALSE ACCEPT DI E3)")
    print("=" * 80)
    for i, (qid, path, match, sim, acous) in enumerate(FILES, start=1):
        fname = Path(path).name
        print(f"[{i}] {qid} | {fname:<18} | Match: {match:<30} | Sim: {sim:.4f} | Akustik: {acous}")

    print("\nPilihan:")
    print("  1-8 : Putar audio di Media Player bawaan Windows")
    print("  a   : Buka folder lokasi file di File Explorer")
    print("  q   : Keluar")

    choice = input("\nMasukkan pilihan [1-8 / a / q]: ").strip().lower()
    if choice == 'q':
        return
    elif choice == 'a':
        folder = PROJECT_ROOT / "data/itera_noise/Gedung F Frequency"
        os.system(f'explorer "{folder}"')
    elif choice.isdigit() and 1 <= int(choice) <= 8:
        idx = int(choice) - 1
        target_path = PROJECT_ROOT / FILES[idx][1]
        print(f"Membuka berkas: {target_path}")
        os.startfile(str(target_path))
    else:
        print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
