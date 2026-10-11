import pandas as pd

exc = pd.read_csv(r"D:\FILE AND TASK\TA\data\manifests\species_excluded.csv")
freeze = pd.read_csv(r"D:\FILE AND TASK\TA\data\manifests\species_freeze.csv")
train = pd.read_csv(r"D:\FILE AND TASK\TA\data\BirdClef\train.csv")

# Rebuild pipeline from train.csv
clean = train[train["author"].str.strip().str.lower() != "unknown"]
el = clean[(clean["class_name"] == "Aves") & (clean["collection"] == "XC") & (clean["rating"] >= 3.0)]
sp = el.groupby("primary_label").agg(
    n_klip=("filename", "count"),
    n_author=("author", "nunique"),
).reset_index()
full_pass = sp[(sp["n_klip"] >= 20) & (sp["n_author"] >= 3)]
print("=== Pipeline from train.csv ===")
print("Aves + XC + rating>=3 (all species):", len(sp))
print("+ klip>=20 + author>=3:", len(full_pass))
print()

# What does species_excluded.csv say?
freeze_keys = set(freeze["species_key"])
exc_keys = set(str(k) for k in exc["species_key"])
pipeline_keys = set(full_pass["primary_label"])
quota_exc = exc[exc["alasan_eksklusi"].str.contains("Di luar kuota", na=False)]
quota_keys = set(str(k) for k in quota_exc["species_key"])

print("=== Manifest accounting ===")
print("Freeze (selected):", len(freeze_keys))
print("Excluded total:", len(exc_keys))
print("  - Quota-only:", len(quota_keys))
print("  - Other reasons:", len(exc_keys) - len(quota_keys))
print("Freeze + Quota-only:", len(freeze_keys) + len(quota_keys))
print()

# The discrepancy: pipeline says 156, manifests say 98
print("=== Discrepancy analysis ===")
missing = pipeline_keys - freeze_keys - quota_keys
print("Species that PASS pipeline but are NOT in freeze AND NOT in quota-excluded:", len(missing))
for k in sorted(list(missing)):
    row = full_pass[full_pass["primary_label"] == k].iloc[0]
    in_exc = exc[exc["species_key"].astype(str) == k]
    if len(in_exc) > 0:
        reason = in_exc["alasan_eksklusi"].iloc[0]
    else:
        reason = "*** NOT IN EXCLUDED FILE AT ALL ***"
    print("  " + k + ": klip=" + str(row["n_klip"]) + ", author=" + str(row["n_author"]) + " -> " + reason[:80])

print()
print("=== Diagnosis ===")
print("These", len(missing), "species pass the volume threshold (klip>=20, author>=3)")
print("but were excluded in species_excluded.csv for 'Rating rendah' reasons.")
print("This is because select_birdclef_species.py uses MEAN rating across ALL")
print("recordings (including non-XC, low-rated ones) as the exclusion reason,")
print("while the pipeline filters individual recordings with rating>=3.0 first.")
print()
print("Correct pool size for DEC-10:")
print("  From train.csv pipeline: 156 species pass Aves+XC+rating>=3+klip>=20+author>=3")
print("  From manifests (freeze+quota-only): 20 + 78 = 98")
print("  Discrepancy:", 156 - 98, "species have conflicting exclusion reasons")
