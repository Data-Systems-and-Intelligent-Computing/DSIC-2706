import pandas as pd

df = pd.read_csv(r"D:\FILE AND TASK\TA\data\itera_noise\Embung E ITERA Frequency\analysis_summary_embung_e.csv")
print("=" * 80)
print("HASIL ANALISIS AUDIO AUDIOMOTH: EMBUNG E ITERA FREQUENCY (20 SEPTEMBER 2026)")
print("=" * 80)

for folder, g in df.groupby("folder"):
    print(f"\n[ DIREKTORI: {folder} ]")
    print(f"Jumlah Berkas         : {len(g)} berkas WAV")
    print(f"Rentang Waktu Header  : {g['rec_time'].iloc[0]} s/d {g['rec_time'].iloc[-1]}")
    print(f"Durasi per Berkas     : Min={g['duration_sec'].min()}s, Max={g['duration_sec'].max()}s (55.0s: {sum(g['duration_sec'] == 55.0)}/{len(g)})")
    print(f"Sample Rate           : {g['framerate'].iloc[0]} Hz (Mono 16-bit PCM)")
    print(f"Gain Terbaca Hardware : {g['actual_gain'].unique().tolist()}")
    print(f"Baterai AudioMoth     : {g['battery_v'].min():.2f} V - {g['battery_v'].max():.2f} V")
    print(f"Suhu Operasi          : {g['temp_c'].min():.1f} °C - {g['temp_c'].max():.1f} °C")
    print(f"Filter Center Freq    : {g['center_freq_khz'].iloc[0]} kHz")
    print(f"Filter Window Length  : {g['window_samples'].iloc[0]} samples")
    print(f"Trigger Threshold     : {g['threshold_pct'].iloc[0]}%")
    print(f"Min Trigger Duration  : {g['min_trigger_s'].iloc[0]} s")
    print(f"Rata-rata RMS Energi  : {g['rms'].mean():.5f} (Min: {g['rms'].min():.5f}, Max: {g['rms'].max():.5f})")
    print(f"Peak Amplitudo        : Rata-rata {g['peak'].mean():.4f} (Max: {g['peak'].max():.4f})")
    print(f"Clipping / Distorsi   : {g['clipping_samples'].sum()} sampel (Berkas kliping: {sum(g['clipping_samples'] > 0)} dari {len(g)})")

print("\n" + "=" * 80)
print("AUDIT KHUSUS 4 BERKAS PENGGANTI (SESI MEDIUM):")
print("=" * 80)
sub_files = df[df['filename'].str.startswith('20260920_164')]
print(sub_files[['filename', 'rec_time', 'duration_sec', 'rms', 'peak', 'clipping_samples', 'temp_c', 'battery_v']])

print("\n" + "=" * 80)
print("BERKAS DENGAN DURASI < 55 DETIK (PADA SESI LOW):")
print("=" * 80)
low_irregular = df[df['duration_sec'] < 55.0]
print(low_irregular[['filename', 'rec_time', 'duration_sec', 'rms', 'peak']])
