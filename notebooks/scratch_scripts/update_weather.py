import pandas as pd

manifest_path = r"D:\FILE AND TASK\TA\data\manifests\itera_noise_manifest.csv"
df = pd.read_csv(manifest_path)

mask = (df['lokasi'].str.contains('Embung F', na=False, case=False)) & (df['lokasi_detail'].str.lower() == 'medium')
df.loc[mask, 'cuaca'] = 'Gerimis (sebentar)'
df.loc[mask, 'catatan'] = 'Terdapat suara hujan ringan (tidak deras) yang berlangsung sebentar.'

df.to_csv(manifest_path, index=False)
print(f"Updated weather for {mask.sum()} records.")
