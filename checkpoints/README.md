# Checkpoints

Model beku yang dipakai representasi R1 dan R2 dicatat dalam `model_registry.csv`.

Berkas checkpoint tidak diubah atau disalin oleh proses audit, notebook, maupun registri proyek. Cache embedding tervalidasi berada di `results/features/` dan provenance-nya tercatat dalam metadata E1.

[Registri model](model_registry.csv) mencantumkan nama berkas dan ukuran bobot. R1 menggunakan `Cnn14_mAP=0.431.pth` untuk menghasilkan 2.048 fitur, sedangkan R2 menggunakan `BirdNET_GLOBAL_6K_V2.4_Model_FP32.onnx` untuk menghasilkan 1.024 fitur. Keduanya dimuat oleh [pengekstrak fitur](../src/embeddings.py).
