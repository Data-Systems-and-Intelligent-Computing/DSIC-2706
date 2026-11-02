# Verifikasi lokasi lima rekaman Xeno-Canto

Tanggal pemeriksaan: 3 November 2026, waktu lokal Asia/Bangkok.

## Hasil verifikasi

Kelima halaman rekaman dan permintaan API resmi Xeno-Canto berhasil diakses (HTTP 200). Kolom negara pada sumber masih menyebut `Indonesia`, tetapi nama lokasi pada halaman maupun API adalah `Bakalalan-Bario Rd, Sarawak`. Semua mencatat koordinat **3.9459, 115.6019**. Dengan demikian, ketidaksesuaian bukan sekadar perbedaan antara salinan lokal dengan sumber yang diakses saat audit.

| Rekaman dan sumber primer | Label pada eksperimen | Tanggal rekaman | Peran pada manifes |
|---|---|---|---|
| [XC208014](https://xeno-canto.org/208014) | Orthotomus ruficeps | 2014-04-14 | gallery |
| [XC208015](https://xeno-canto.org/208015) | Orthotomus ruficeps | 2014-04-14 | gallery |
| [XC207989](https://xeno-canto.org/207989) | Spilornis cheela | 2014-04-14 | gallery |
| [XC207820](https://xeno-canto.org/207820) | Dicrurus hottentottus | 2014-04-15 | gallery |
| [XC207964](https://xeno-canto.org/207964) | Cinnyris jugularis | 2014-04-15 | gallery |

Semua tercatat atas nama Frank Lambert. Nama lokasi juga tercantum pada nama berkas audio sumber. Respons API yang diambil saat pemeriksaan disimpan dalam direktori `evidence/`; kredensial permintaan tidak disimpan di sana.

## Pemeriksaan geografis

Koordinat masukan diuji terhadap geometri batas negara lengkap dari geoBoundaries `gbOpen`, bukan terhadap titik pusat wilayah hasil geocoding. Hasil pengujian: berada di dalam poligon Malaysia dan di luar poligon Indonesia. Urutan koordinat GeoJSON adalah bujur/lintang: `[115.6019, 3.9459]`. Pemeriksaan menggunakan ray casting pada cincin luar dan lubang geometri Polygon/MultiPolygon.

- Malaysia: `MYS-ADM0-87038898`, tahun representasi 2017, sumber OpenStreetMap/Wambacher.
- Indonesia: `IDN-ADM0-11942859`, tahun representasi 2017, sumber OpenStreetMap/Wambacher.
- Versi geometri yang dirujuk API: commit `9469f09` pada repository geoBoundaries. URL dan SHA-256 berkas dicatat dalam [hasil pemeriksaan koordinat](evidence/coordinate_country_check.json).
- Pemeriksaan alamat tambahan melalui Nominatim/OpenStreetMap mengembalikan Lawas, Bahagian Limbang, Sarawak, Malaysia. Koordinat pusat wilayah yang dikembalikan layanan tersebut tidak diperlakukan sebagai koordinat rekaman.
- [Dokumentasi API geoBoundaries](https://www.geoboundaries.org/api.html).
- [Halaman resmi pemerintah Sarawak tentang Bario](https://miri.sarawak.gov.my/web/subpage/webpage_view/226) dan [dokumen JKR Sarawak tentang jalan Bakelalan–Bario](https://jkr.sarawak.gov.my/web/attachment/show/?docid=Rkk3UkNUUHBsSnRIVk94LzRrRmxUZz09OjpNyE-ECPeEOyfhkMM-UOUz) mendukung konteks nama wilayah/jalan tersebut.

Data batas dan alamat tambahan berasal dari OpenStreetMap/Wambacher melalui geoBoundaries serta OpenStreetMap contributors melalui Nominatim, berlisensi ODbL 1.0 sebagaimana metadata sumber. Pemeriksaan ini memverifikasi konsistensi geografis lokasi dan koordinat yang dipublikasikan; bukan pengukuran ulang GPS di lapangan atau pembuktian independen identitas burung.

## Penanganan dalam penelitian

Fabio menerima penggunaan rekaman lintas negara sepanjang spesies atau cakupan label arsipnya terdapat di Indonesia. Karena itu kelima rekaman dipertahankan dalam korpus yang sudah dibekukan. Batasan pada BAB I diperjelas menjadi **20 label spesies burung yang terdapat di Indonesia**; negara asal seluruh rekaman tidak diklaim seragam. Atas permintaan Fabio, catatan kaki lokasi di BAB I dihapus, sedangkan bukti dan hasil audit tetap disimpan di sini.

Penegasan cakupan ini dilakukan setelah hasil eksperimen tersedia. Riwayat kurasi awal tetap dicatat: skrip mengajukan filter negara `cnt:indonesia` kepada API Xeno-Canto dan kelima sumber masih lolos berdasarkan kolom negara tersebut. Penegasan sekarang tidak boleh ditulis seolah-olah pemeriksaan lokasi independen sudah dilakukan sebelum eksperimen. Pernyataan sebelumnya bahwa semua rekaman pasti berasal dari Indonesia tidak didukung hasil audit ini.

Tidak ada penghapusan atau pemindahan audio, perubahan identitas/label, modifikasi manifes eksperimen atau arsip metadata mentah, penggantian negara pada sumber, maupun penghitungan ulang hasil pada audit ini. Skor yang tersedia tetap berlaku untuk korpus asli 1.216 rekaman dengan galeri 673, kueri 311, dan kalibrasi 232. Klaim untuk korpus lain yang mengecualikan kelima rekaman belum diuji. Pemeriksaan geografis ini terbatas pada lima rekaman yang ditandai, bukan pengesahan asal negara seluruh rekaman lainnya.

## Bukti yang disimpan

- `evidence/XC*_api.json`: respons resmi per rekaman pada saat pemeriksaan.
- `evidence/retrieval_log.json`: status akses halaman/API dan bidang lokasi sumber.
- `evidence/MYS_ADM0_metadata.json` dan `evidence/IDN_ADM0_metadata.json`: provenance, lisensi, versi, dan URL geometri.
- `evidence/coordinate_country_check.json`: hasil uji koordinat, sumber, dan hash geometri.
- `evidence/coordinate_reverse_osm.json`: pemeriksaan alamat tambahan.

Respons mentah menyimpan cap waktu UTC; tanggal audit di dokumen ini menggunakan Asia/Bangkok.
