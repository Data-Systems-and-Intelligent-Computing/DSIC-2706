import pandas as pd

df = pd.read_csv(r"D:\FILE AND TASK\TA\data\itera_noise\Kebun Raya Frequency\analysis_summary_kebun_raya.csv")
print("=" * 80)
print("HASIL ANALISIS AUDIO AUDIOMOTH: KEBUN RAYA ITERA FREQUENCY (21-22 SEPTEMBER 2026)")
print("=" * 80)

for folder, g in df.groupby("folder"):
    print(f"\n[ DIREKTORI: {folder} ]")
    print(f"Jumlah Berkas         : {len(g)} berkas WAV")
    print(f"Tanggal Perekaman     : {g['rec_date'].unique().tolist()}")
    print(f"Rentang Waktu Header  : {g['rec_time'].iloc[0]} s/d {g['rec_time'].iloc[-1]}")
    print(f"Durasi per Berkas     : Min={g['duration_sec'].min()}s, Max={g['duration_sec'].max()}s (55.0s: {sum(g['duration_sec'] == 55.0)}/{len(g)})")
    print(f"Sample Rate           : {g['framerate'].iloc[0]} Hz (Mono 16-bit PCM)")
    print(f"Gain Terbaca Hardware : {g['actual_gain'].unique().tolist()}")
    print(f"Baterai AudioMoth     : {g['battery_v'].min():.2f} V - {g['battery_v'].max():.2f} V")
    print(f"Suhu Operasi          : {g['temp_c'].min():.1f} °C - {g['temp_c'].max():.1f} °C")
    print(f"Filter Center Freq    : {g['center_freq_khz'].unique().tolist()} kHz")
    print(f"Filter Window Length  : {g['window_samples'].iloc[0]} samples")
    print(f"Trigger Threshold     : {g['threshold_pct'].iloc[0]}%")
    print(f"Min Trigger Duration  : {g['min_trigger_s'].iloc[0]} s")
    print(f"Rata-rata RMS Energi  : {g['rms'].mean():.5f} (Min: {g['rms'].min():.5f}, Max: {g['rms'].max():.5f})")
    print(f"Peak Amplitudo        : Rata-rata {g['peak'].mean():.4f} (Max: {g['peak'].max():.4f})")
    print(f"Clipping / Distorsi   : {g['clipping_samples'].sum()} sampel (Berkas kliping: {sum(g['clipping_samples'] > 0)} dari {len(g)})")
    print(f"Distribusi Spektrum   : Sub-1k={g['band_sub1k'].mean():.1f}, 1k-4k={g['band_1k_4k'].mean():.1f}, 4k-8k={g['band_4k_8k'].mean():.1f}, >8k={g['band_above8k'].mean():.1f}")

print("\n" + "=" * 80)
print("AUDIT KHUSUS SESI MEDIUM (59 BERKAS):")
print("=" * 80)
med = df[df['folder'] == '32 kHz Medium Frequency Kebun Raya']
part1 = med[med['filename'] <= '20260922_125500T.WAV']
part2 = med[med['filename'] >= '20260922_142200T.WAV']
print(f"Bagian 1 (12:05 - 12:55): {len(part1)} berkas, RMS={part1['rms'].mean():.5f}, Center Freq={part1['center_freq_khz'].unique().tolist()}")
print(f"Bagian 2 (14:22 - 14:29): {len(part2)} berkas, RMS={part2['rms'].mean():.5f}, Center Freq={part2['center_freq_khz'].unique().tolist()}")
print(f"Total: {len(part1)} + {len(part2)} = {len(med)} berkas (kurang 1 berkas dari 60)")

print("\n" + "=" * 80)
print("TOTAL DATA KEBUN RAYA KESELURUHAN:")
print("=" * 80)
print(f"Total Berkas: {len(df)} berkas WAV (High: 60, Medium: 59, Low: 60)")
print(f"Total Durasi: {df['duration_sec'].sum() / 60:.1f} menit ({df['duration_sec'].sum() / 3600:.2f} jam audio bersih)")
print("=" * 80)
