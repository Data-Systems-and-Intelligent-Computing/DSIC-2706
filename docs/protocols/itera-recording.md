# Protokol Perekaman Lapangan Lingkungan ITERA — DSIC-2706

## 1. Tujuan Perekaman
Mengumpulkan **bank derau latar** untuk E2 (pencampuran SNR terkontrol) dan negatif *background-only* untuk E3. Rekaman ini **bukan** bukti kehadiran spesies di kampus dan tidak dipakai untuk mengklaim inventarisasi fauna.

## 2. Batasan akses (DEC-11)
Perekaman **hanya diizinkan siang hari**. Sesi malam tidak dilakukan. Keragaman akustik yang dikejar adalah lokasi × gain × metode trigger, bukan fajar/malam.

## 3. Dua metode perangkat: frequency dan amplitude (DEC-12)
Pembimbing mensyaratkan kedua mode trigger AudioMoth agar pipeline eksperimen **memilih berkas yang sudah bertanda metode** di manifes, tanpa filter digital tambahan di kode (tidak ada band-pass / *level gate* post-hoc sebagai pengganti akuisisi).

| Metode | Perilaku perangkat | Fungsi di eksperimen | Status |
|---|---|---|---|
| **Frequency** | Trigger ketika energi pada pengaturan Filter Low / Medium / High terpenuhi | Bank derau dengan karakter pita yang sudah terpisah di perangkat | Diambil 18–30 Sep 2026 |
| **Amplitude** | Trigger ketika amplitudo melewati ambang level | Bank derau dengan karakter level yang sudah terpisah di perangkat | Belum diambil; prasyarat main run E2 |

Kedua metode disimpan sebagai kolom `trigger_method` pada `data/manifests/itera_noise_manifest.csv` (`frequency` atau `amplitude`). Mixer E2 hanya membaca path dari manifes itu.

## 4. Lokasi
Tipe akustik yang diwakili (boleh lebih dari tiga titik fisik):

1. **Perairan / Embung E** — ambien terbuka, angin, aktivitas tepi air.
2. **Vegetasi / Kebun Raya** — kanopi, serangga siang, gemerisik daun.
3. **Antropogenik** — Masjid At-Tanwir, Gedung F, sekitar GKU 1 (kendaraan, HVAC, aktivitas manusia).

Koordinat dan jam sesi frequency tercatat di `data/itera_noise/Notulensi Pengambilan Data Uji ITERA.txt`.

## 5. Spesifikasi teknis
- Perangkat: AudioMoth.
- Laju sampel: **32 kHz**.
- Format: WAV (PCM).
- Pola sesi frequency yang sudah dipakai: rekam **55 s**, jeda **5 s**; Filter Frequency Low / Medium / High; gain sesuai folder sesi.
- Metadata wajib: GPS, lokasi, tanggal/jam (siang), cuaca bila ada, `device_id`, gain, `trigger_method`, `CONFIG.TXT`.
- Segmen yang masuk bank E2: dipotong 5.0 s, **bebas vokalisasi burung target**, `bird_free=true` setelah verifikasi.

## 6. Yang belum boleh diklaim
- Bank derau belum dibekukan (manifes masih header-only).
- Amplitude trigger belum ada.
- Pink noise sintetis **tidak** boleh menggantikan bank ini pada main run.
