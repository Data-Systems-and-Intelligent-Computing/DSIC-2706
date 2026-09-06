# Protokol Kalibrasi Ambang Batas Open-Set — DSIC-2706

## 1. Perumusan Masalah Open-Set
Dalam kondisi nyata, sistem bioakustik harus menolak query yang tidak termasuk ke dalam takson target di Gallery.
Keputusan sistem dirumuskan sebagai:
$$\text{Decision}(q) = \begin{cases} 1 \text{ (Accept Candidate)}, & \text{jika } \max_{g \in \mathcal{G}} \text{CosineSimilarity}(e_q, e_g) \ge \tau \\ 0 \text{ (Reject / Unknown)}, & \text{jika } \max_{g \in \mathcal{G}} \text{CosineSimilarity}(e_q, e_g) < \tau \end{cases}$$

## 2. Aturan Pembekuan Ambang Batas (*Frozen Threshold Rule*)
- Ambang batas $\tau$ dioptimasi **HANYA** pada partisi kalibrasi independen (`calibration` set dan subset `unknown` kalibrasi).
- Kriteria optimasi adalah indeks Youden's $J = \text{TPR} - \text{FPR}$ pada kurva ROC empiris.
- Setelah $\tau^*$ terpilih, nilainya **DIBEKUKAN** dan disimpan dalam `configs/thresholds.yaml`.
- Dilarang keras menyetel ulang $\tau$ setelah melihat hasil evaluasi pada test set.

## 3. Evaluasi Transfer Ambang Batas Lintas Derau
Nilai $\tau^*$ yang sama dievaluasi melintasi kondisi:
1. Clean
2. SNR 20 dB
3. SNR 10 dB
4. SNR 0 dB
5. SNR -5 dB

Pergeseran metrik diukur menggunakan $\Delta \text{Recall} = \text{Recall}(\text{SNR}) - \text{Recall}(\text{Clean})$ dan $\Delta \text{FPR} = \text{FPR}(\text{SNR}) - \text{FPR}(\text{Clean})$.
