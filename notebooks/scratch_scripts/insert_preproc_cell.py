import json

nb_path = r"D:\FILE AND TASK\TA\notebooks\E1_Clean_Retrieval.ipynb"
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

# Code for Preprocessing Verification
preproc_cell_code = """# ==============================================================================
# BUKTI FISIK PRAPEMROSESAN AUDIO: TABEL METRIK & VISUALISASI KOMPARASI
# ==============================================================================
import librosa.display

print("\\n" + "-" * 85)
print("[BUKTI PRAPEMROSESAN] Mengaudit statistik prapemrosesan pada seluruh berkas...")
print("-" * 85)

audit_records = []
for idx, row in df_valid.iterrows():
    p = row['full_path']
    y_raw, sr_raw = librosa.load(p, sr=None, mono=False)
    dur_raw = len(y_raw) / sr_raw if y_raw.ndim == 1 else y_raw.shape[1] / sr_raw
    y_raw_mono = librosa.to_mono(y_raw) if y_raw.ndim > 1 else y_raw
    rms_raw = float(np.sqrt(np.mean(y_raw_mono ** 2)))
    peak_raw = float(np.max(np.abs(y_raw_mono)))
    
    y_proc = preprocess_audio(p)
    rms_proc = float(np.sqrt(np.mean(y_proc ** 2)))
    peak_proc = float(np.max(np.abs(y_proc)))
    
    audit_records.append({
        'id': row['id'],
        'species_key': row['species_key'],
        'split_role': row.get('split_role', 'gallery'),
        'sr_original': sr_raw,
        'sr_processed': TARGET_SR,
        'dur_original_sec': round(dur_raw, 2),
        'dur_processed_sec': DURATION_SEC,
        'rms_original': round(rms_raw, 4),
        'rms_processed': round(rms_proc, 4),
        'peak_original': round(peak_raw, 4),
        'peak_processed': round(peak_proc, 4)
    })

df_audit = pd.DataFrame(audit_records)
audit_csv_path = os.path.join(results_proc_dir, "preprocessing_verification_table.csv")
df_audit.to_csv(audit_csv_path, index=False)
print(f"[SAVE] Tabel verifikasi prapemrosesan disimpan ke: {audit_csv_path}")

print("\\n" + "=" * 85)
print("[RINGKASAN] STATISTIK PERUBAHAN SINYAL (SEBELUM VS SESUDAH PRAPEMROSESAN)")
print("=" * 85)
print(f"{'Parameter Sinyal':<28} | {'Sebelum Prapemrosesan (Mentah)':<30} | {'Sesudah Prapemrosesan (Standar)':<30}")
print("-" * 85)
print(f"{'Laju Sampel (Sample Rate)':<28} | {df_audit['sr_original'].min()} - {df_audit['sr_original'].max()} Hz (Variatif)      | {TARGET_SR} Hz (Konstan)")
print(f"{'Durasi Rekaman':<28} | {df_audit['dur_original_sec'].min():.1f} - {df_audit['dur_original_sec'].max():.1f}s (Rerata: {df_audit['dur_original_sec'].mean():.1f}s)    | {DURATION_SEC} detik (Konstan / 160.000 sampel)")
print(f"{'Energi RMS (Root Mean Sq)':<28} | {df_audit['rms_original'].min():.4f} - {df_audit['rms_original'].max():.4f} (Rerata: {df_audit['rms_original'].mean():.4f}) | {df_audit['rms_processed'].mean():.4f} (+- {df_audit['rms_processed'].std():.4f}) (Tepat 0.05)")
print(f"{'Puncak Amplitudo (Peak)':<28} | {df_audit['peak_original'].min():.4f} - {df_audit['peak_original'].max():.4f} (Rerata: {df_audit['peak_original'].mean():.4f}) | {df_audit['peak_processed'].min():.4f} - {df_audit['peak_processed'].max():.4f} (Aman / Tidak Klip)")
print("=" * 85)

# Visualisasi Komparasi Grafis 4-Panel (Before vs After)
sample_case = df_valid[df_valid['species_key'] == 'Apalharpactes mackloti'].iloc[0]
raw_path = sample_case['full_path']
y_orig, sr_orig = librosa.load(raw_path, sr=None, mono=True)
dur_orig = len(y_orig) / sr_orig
t_orig = np.linspace(0, dur_orig, len(y_orig))

y_32k_samp = librosa.resample(y_orig, orig_sr=sr_orig, target_sr=TARGET_SR)
if len(y_32k_samp) > TARGET_SAMPLES:
    hop = TARGET_SAMPLES // 4
    num_windows = max(1, (len(y_32k_samp) - TARGET_SAMPLES) // hop + 1)
    best_rms, best_start = -1.0, 0
    for i in range(num_windows):
        seg = y_32k_samp[i*hop : i*hop + TARGET_SAMPLES]
        r = np.sqrt(np.mean(seg**2))
        if r > best_rms:
            best_rms = r
            best_start = i*hop
    sel_start_sec = best_start / TARGET_SR
    sel_end_sec = sel_start_sec + DURATION_SEC
else:
    sel_start_sec = 0.0
    sel_end_sec = dur_orig

y_final = preprocess_audio(raw_path)
t_final = np.linspace(0, DURATION_SEC, len(y_final))

fig, axs = plt.subplots(2, 2, figsize=(16, 8))
axs[0, 0].plot(t_orig, y_orig, color='#4a7c59', alpha=0.8, linewidth=0.6)
axs[0, 0].axvspan(sel_start_sec, sel_end_sec, color='#c94c4c', alpha=0.35, 
                  label=f'Segmen Terpilih ({sel_start_sec:.1f}s - {sel_end_sec:.1f}s, RMS Tertinggi)')
axs[0, 0].set_title(f"A. Waveform Asli (Mentah): {sample_case['species_key']} (Durasi: {dur_orig:.1f}s, SR: {sr_orig}Hz)")
axs[0, 0].set_xlabel("Waktu (detik)")
axs[0, 0].set_ylabel("Amplitudo")
axs[0, 0].legend(loc='upper right')
axs[0, 0].grid(True, linestyle='--', alpha=0.5)

axs[0, 1].plot(t_final, y_final, color='#1f4e79', linewidth=0.8)
axs[0, 1].set_title("B. Waveform Standar Terpilih (Durasi: 5.0s, SR: 32.000Hz, Target RMS: 0.05)")
axs[0, 1].set_xlabel("Waktu (detik)")
axs[0, 1].set_ylabel("Amplitudo Ternormalisasi")
axs[0, 1].set_ylim(-1.05, 1.05)
axs[0, 1].grid(True, linestyle='--', alpha=0.5)

S_orig = librosa.feature.melspectrogram(y=y_orig, sr=sr_orig, n_mels=64, fmin=150, fmax=15000)
S_orig_db = librosa.power_to_db(S_orig, ref=np.max)
img1 = librosa.display.specshow(S_orig_db, sr=sr_orig, x_axis='time', y_axis='mel', fmin=150, fmax=15000, ax=axs[1, 0], cmap='viridis')
axs[1, 0].axvspan(sel_start_sec, sel_end_sec, color='red', alpha=0.25, linestyle='--')
axs[1, 0].set_title("C. Mel-Spektrogram Asli (Seluruh Rentang Waktu)")
fig.colorbar(img1, ax=axs[1, 0], format="%+2.0f dB")

S_proc = librosa.feature.melspectrogram(y=y_final, sr=TARGET_SR, n_mels=64, fmin=150, fmax=15000)
S_proc_db = librosa.power_to_db(S_proc, ref=np.max)
img2 = librosa.display.specshow(S_proc_db, sr=TARGET_SR, x_axis='time', y_axis='mel', fmin=150, fmax=15000, ax=axs[1, 1], cmap='viridis')
axs[1, 1].set_title("D. Mel-Spektrogram Terpilih & Ternormalisasi (Fokus 5.0 Detik Kicauan)")
fig.colorbar(img2, ax=axs[1, 1], format="%+2.0f dB")

plt.tight_layout()
preproc_plot_path = os.path.join(results_fig_dir, "preprocessing_before_after_comparison.png")
plt.savefig(preproc_plot_path, dpi=300)
plt.show()
print(f"[SAVE] Gambar komparasi prapemrosesan disimpan ke: {preproc_plot_path}")
"""

# Check if preproc_cell already exists
has_preproc = any("BUKTI FISIK PRAPEMROSESAN AUDIO" in "".join(c.get("source", [])) for c in nb["cells"])
if not has_preproc:
    new_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in preproc_cell_code.strip().split("\n")]
    }
    # Insert after Cell 4 (index 5)
    nb["cells"].insert(5, new_cell)
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
    print("Preproc cell inserted successfully! Total cells:", len(nb["cells"]))
else:
    print("Preproc cell already exists.")
