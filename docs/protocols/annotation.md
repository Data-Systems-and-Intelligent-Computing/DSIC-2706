# Pedoman Anotasi Soundscape Lapangan — DSIC-2706

## 1. Format Anotasi
Anotasi rekaman soundscape lapangan ITERA disimpan dalam format CSV standar Raven Pro / Audacity:
```text
selection,view,channel,begin_time,end_time,low_freq,high_freq,species_key,scientific_name,confidence
```

## 2. Aturan Pelabelan Ground Truth
1. **Verifikasi Manual:**
   Hanya subset audio yang telah diverifikasi manual oleh pengamat (atau rekaman konfirmasi visual) yang diikutsertakan dalam evaluasi kuantitatif E4.
2. **Kategori Label:**
   - E4 memakai `train_soundscapes` BirdCLEF+ 2026, bukan inventarisasi spesies kampus ITERA.
   - Rekaman ITERA dilabeli untuk bank derau: `background_only`, `bird_present` (ditolak dari E2), `anthropophony`, `geophony`, `non_bird_biophony`.
   - `trigger_method` wajib: `frequency` atau `amplitude` (DEC-12).
   - `daypart` pada rezim aktif selalu `siang` (DEC-11).
3. **Pemberian Skor Keyakinan (Confidence):**
   - `1.0`: Identifikasi vokal jelas, karakteristik spektral khas terlihat di spektrogram.
   - `0.5`: Vokal sayup-sayup atau terjadi interferensi derau berat.
