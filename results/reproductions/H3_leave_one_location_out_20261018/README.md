# H3 leave-one-location-out sensitivity

All five locations remain in E4. These six scenarios are exploratory statistical subsets of stored AP@10, not new audio runs. Each omitted-location scenario uses four locations.

## absolute_mAP10 — mean over four SNR levels

| Omitted | R1 | R2 | R1−R2 | CI 95% for difference |
|---|---:|---:|---:|---|
| none | 0.042324 | 0.030949 | 0.011375 | [-0.003993, 0.022140] |
| Embung_F | 0.042324 | 0.028141 | 0.014183 | [-0.001172, 0.027077] |
| Gedung_F | 0.041267 | 0.030617 | 0.010649 | [-0.004645, 0.021937] |
| Kebun_Raya | 0.019567 | 0.026686 | -0.007119 | [-0.018009, 0.003056] |
| Masjid_At_Tanwir | 0.040942 | 0.027424 | 0.013518 | [-0.000356, 0.025027] |
| Sekitar_GKU_1 | 0.037864 | 0.030949 | 0.006915 | [-0.007397, 0.017876] |

## relative_retention — mean over four SNR levels

| Omitted | R1 | R2 | R1−R2 | CI 95% for difference |
|---|---:|---:|---:|---|
| none | 0.240111 | 0.048607 | 0.191504 | [0.152203, 0.241969] |
| Embung_F | 0.240111 | 0.044198 | 0.195913 | [0.154954, 0.247616] |
| Gedung_F | 0.234114 | 0.048087 | 0.186027 | [0.144211, 0.234100] |
| Kebun_Raya | 0.111009 | 0.041912 | 0.069097 | [0.048683, 0.121152] |
| Masjid_At_Tanwir | 0.232270 | 0.043071 | 0.189198 | [0.149751, 0.240940] |
| Sekitar_GKU_1 | 0.214807 | 0.048607 | 0.166200 | [0.128956, 0.212948] |

Intervals are unadjusted exploratory percentile intervals conditional on fixed sites/noise segments. Subsets are correlated and do not estimate causal contributions of a location. A narrower range after removing a site is partly a consequence of having fewer locations. All per-SNR values remain in the CSV.
