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
   - Spesies Target (salah satu dari 16 spesies target).
   - Unknown Bird (burung lain di luar 16 target).
   - Non-Bird Biophony (katak, jangkrik, serangga).
   - Anthropophony / Geophony (angin, kendaraan, langkah kaki).
3. **Pemberian Skor Keyakinan (Confidence):**
   - `1.0`: Identifikasi vokal jelas, karakteristik spektral khas terlihat di spektrogram.
   - `0.5`: Vokal sayup-sayup atau terjadi interferensi derau berat.
