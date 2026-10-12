# Pedoman Metadata Noise ITERA — DSIC-2706

## Status anotasi untuk scope aktif

Bank `data/itera_noise/` dipakai sebagai noise lapangan dalam pencampuran aditif E2/E4 dan sebagai sebagian kontrol unknown E3. Bank ini bebas spesies target penelitian. Karena itu **anotasi spesies target, bounding box vokalisasi target, atau ground truth focal-bird tidak diminta dan tidak diperlukan** untuk E2 maupun E4.

## Metadata yang digunakan

Metadata aktif berasal dari [itera_noise_manifest.csv](../../data/manifests/itera_noise_manifest.csv): path, checksum, lokasi/folder, sesi, serta atribut teknis yang tersedia. Provenance noise pada hasil E2/E4 dilacak melalui raw CSV dan metadata run.

## Batas interpretasi

E4 membandingkan profil noise lokasi dalam additive mixture. Ia bukan evaluasi rekaman burung in-situ; karenanya protokol ini tidak menetapkan aturan anotasi spesies burung untuk menguji domain shift.

## Jika studi lanjutan dilakukan

Studi real-soundscape baru memerlukan desain terpisah: rekaman target-bird in-situ, anotasi waktu/frekuensi dan spesies, kondisi perangkat/mikrofon, serta pemisahan train/calibration/test. Dataset seperti itu tidak diperlukan untuk penelitian aktif ini.
