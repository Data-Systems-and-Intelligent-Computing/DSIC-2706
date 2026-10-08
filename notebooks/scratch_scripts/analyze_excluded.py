import pandas as pd

exc = pd.read_csv(r"D:\FILE AND TASK\TA\data\manifests\species_excluded.csv")
print("Total excluded:", len(exc))
print()

# Show sample reasons
print("Sample reasons (first 5):")
for _, r in exc.head(5).iterrows():
    print("  " + r["scientific_name"] + ": " + r["alasan_eksklusi"])
print()

# Categorize
non_aves = exc[exc["alasan_eksklusi"].str.contains("Non-Aves", na=False)]
print("Non-Aves:", len(non_aves))

bukan_xc = exc[exc["alasan_eksklusi"].str.contains("Bukan koleksi XC", na=False)]
print("Bukan koleksi XC:", len(bukan_xc))

rating_rendah = exc[exc["alasan_eksklusi"].str.contains("Rating rendah", na=False)]
print("Rating rendah:", len(rating_rendah))

klip_kurang = exc[exc["alasan_eksklusi"].str.contains("Klip < 20", na=False)]
print("Klip < 20:", len(klip_kurang))

author_kurang = exc[exc["alasan_eksklusi"].str.contains("Author < 3", na=False)]
print("Author < 3:", len(author_kurang))

kalah_ranking = exc[exc["alasan_eksklusi"].str.contains("ranking|kuota|Kalah", case=False, na=False)]
print("Kalah ranking/kuota:", len(kalah_ranking))

# Check for quota-only entries
quota_pattern = exc[exc["alasan_eksklusi"].str.strip().str.startswith("Kalah")]
print("Starts with 'Kalah':", len(quota_pattern))

# All unique reason fragments
all_reasons = exc["alasan_eksklusi"].str.split(";").explode().str.strip().unique()
print("\nUnique reason fragments:")
for r in sorted(set(all_reasons)):
    print("  - " + r)
