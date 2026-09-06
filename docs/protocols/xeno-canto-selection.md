# Protokol Kurasi Audio Xeno-Canto — DSIC-2706

## 1. Kriteria Inklusi
- **Takson:** 16 Spesies Burung Target Sumatera.
- **Geografis:** Rekaman dari wilayah Indonesia (khususnya Sumatera) dengan koordinat lintang/bujur atau nama lokalitas yang dapat dipertanggungjawabkan.
- **Kualitas Audio:** Mengutamakan rating kualitas A, B, dan C pada metadata Xeno-Canto.
- **Lisensi:** Lisensi Creative Commons terbuka (CC BY, CC BY-NC, CC BY-SA, dsb.).
- **Volume:** Minimal 15 berkas per spesies, maksimal 35 berkas per spesies untuk menjaga keseimbangan korpus.

## 2. Perekaman Manifes & Atribusi
Setiap berkas wajib dicatat dalam `data/manifests/target_birds_manifest.csv` dengan 10 atribut wajib:
1. `recording_id` (ID unik Xeno-Canto)
2. `scientific_name`
3. `common_name`
4. `recordist` (Nama lengkap kontributor)
5. `country` & `locality`
6. `date` & `time`
7. `quality`
8. `license`
9. `url_page` & `url_audio`
10. `sha256` (Checksum integritas berkas)
