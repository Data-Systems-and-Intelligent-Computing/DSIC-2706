import pandas as pd

df = pd.read_csv(r"D:\FILE AND TASK\TA\data\itera_noise\Gedung F Amplitudo\analysis_summary_gedung_f_amplitudo.csv")
for folder, grp in df.groupby("folder"):
    total_samples = grp["duration_sec"].sum() * 32000
    clip_sum = grp["clipping_samples"].sum()
    clip_pct = (clip_sum / total_samples) * 100 if total_samples > 0 else 0
    print(f"=== {folder} ===")
    print(f"Count: {len(grp)}")
    print(f"Duration: min={grp['duration_sec'].min():.2f}s, mean={grp['duration_sec'].mean():.2f}s, max={grp['duration_sec'].max():.2f}s, 55s={(grp['duration_sec']==55.0).sum()}, >=5s={(grp['duration_sec']>=5.0).sum()}")
    print(f"RMS: min={grp['rms'].min():.5f}, mean={grp['rms'].mean():.5f}, max={grp['rms'].max():.5f}")
    print(f"Peak: min={grp['peak'].min():.4f}, mean={grp['peak'].mean():.4f}, max={grp['peak'].max():.4f}")
    print(f"Clipping: files={(grp['clipping_samples']>0).sum()}, total={clip_sum}, pct={clip_pct:.5f}%")
    print(f"Temp: min={grp['temp_c'].min():.1f}C, mean={grp['temp_c'].mean():.1f}C, max={grp['temp_c'].max():.1f}C")
    print(f"Battery: min={grp['battery_v'].min():.2f}V, mean={grp['battery_v'].mean():.2f}V, max={grp['battery_v'].max():.2f}V")
    print(f"Time: {grp['rec_time'].iloc[0]} to {grp['rec_time'].iloc[-1]}")
    print(f"Filter: {grp['filter_type'].iloc[0]} ({grp['filter_freq_khz'].iloc[0]} kHz), Threshold: {grp['threshold_type'].iloc[0]} ({grp['threshold_pct'].iloc[0]}%)")
    print(f"Sub1k: {grp['band_sub1k'].mean():.2f}%, 1k-4k: {grp['band_1k_4k'].mean():.2f}%, 4k-8k: {grp['band_4k_8k'].mean():.2f}%, >8k: {grp['band_above8k'].mean():.2f}%\n")
