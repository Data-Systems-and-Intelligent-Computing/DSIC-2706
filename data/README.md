# Data

Folder ini menyimpan data asli dan manifes aktif. Audio tidak dipindahkan atau diubah oleh indeks ini.

| Peran | Lokasi utama | Jumlah |
|---|---|---:|
| Burung target | `xeno_canto_indonesia/` dan `manifests/dataset_split.csv` | 673 galeri, 232 kalibrasi, 311 kueri uji |
| Kontrol di luar target | `xeno_canto_indonesia_unknowns/`, `itera_noise/` dan `manifests/unknown_open_set_manifest.csv` | 272 rekaman dari 69 spesies burung non-target dan 271 berkas derau kontrol |
| Derau lapangan | `itera_noise/` dan `manifests/itera_noise_manifest.csv` | 1.528 berkas untuk campuran dan 271 untuk kontrol |

`dataset_registry.csv` memberi indeks ringkas setiap manifes aktif. Inventaris fisik terperinci berada di `results/tables/07_eda_physical_audio_inventory.csv`.
