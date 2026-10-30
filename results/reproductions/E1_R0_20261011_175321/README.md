# E1 — Clean retrieval R0

Reproduksi retrieval bersih untuk baseline MFCC R0 saja.

- `tables/per_query.csv`: metrik setiap kueri.
- `features/embeddings.npz`: embedding gallery dan query.
- `metadata.json`: manifest, hash kode, dan ringkasan metrik.

Status run ini: selesai untuk R0 saja. Pada saat run dibuat, R1–R3 belum menjadi artefak E1 resmi.

**Pembaruan indeks 30 Oktober 2026:** artefak E1 R1–R3 sudah dikonsolidasikan dari cache clean tervalidasi pada 12 Oktober: [R1](../E1_R1_cache_20261012T021032_566409Z/), [R2](../E1_R2_cache_20261012T021034_128124Z/), dan [R3](../E1_R3_cache_20261012T021035_119528Z/). Konsolidasi tersebut tidak diklaim sebagai run historis sebelumnya. Hasil R0, metadata, dan embedding dalam folder ini tidak diubah. [Reproduksi 16 Oktober](../RECHECK_FRESH_20261016/README.md) kemudian menghitung E1 dari embedding yang diekstrak ulang.
