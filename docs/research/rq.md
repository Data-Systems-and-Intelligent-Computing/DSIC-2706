# Pertanyaan Penelitian (Research Questions) — DSIC-2706

## RQ Utama
> **Representasi audio mana yang mempertahankan kualitas similarity retrieval paling baik ketika query bioakustik mengalami peningkatan derau lingkungan dan pergeseran domain dari focal recording ke soundscape?**

---

## Sub-RQ
1. **Sub-RQ 1 (Controlled Noise Degradation):**
   Seberapa besar penurunan `mAP@k`, `Recall@k`, dan `Precision@k` untuk setiap representasi pada beberapa tingkat SNR (20 dB, 10 dB, 0 dB, -5 dB) yang dibentuk secara terkontrol menggunakan background noise lokal ITERA?
2. **Sub-RQ 2 (Open-Set Threshold Transfer):**
   Apakah threshold kemiripan ($\tau$) yang dikalibrasi pada data terpisah tetap mampu menolak *unknown species* dan *background noise* ketika tingkat derau lingkungan meningkat melintasi level SNR yang berbeda?
3. **Sub-RQ 3 (Domain-Specific Advantage):**
   Apakah representasi spesifik bioakustik (*bioacoustic pretrained embedding*) memiliki retensi ketahanan (*relative robustness retention*) yang lebih baik daripada representasi generik (*generic pretrained audio embedding*) dan MFCC pada kondisi derau lingkungan yang setara?
4. **Sub-RQ 4 (Real Soundscape Validation):**
   Sebagai analisis sekunder, seberapa besar kesenjangan retrieval (*retrieval gap*) ketika beralih dari derau aditif terkontrol ke rekaman lapangan nyata (*real ITERA soundscapes*) yang mengalami pergeseran domain akustik multi-sumber?
