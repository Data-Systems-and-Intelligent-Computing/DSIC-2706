import requests, time
import pandas as pd

freeze = pd.read_csv(r"D:\FILE AND TASK\TA\data\manifests\species_freeze.csv")
API_KEY = "95dc5b3f6834b56e17da4cf68cc890cb470d1284"
headers = {"X-API-Key": API_KEY, "User-Agent": "BirdSoundResearch/1.0"}

total_pages = 0
for _, r in freeze.iterrows():
    s_key = r["species_key"]
    s_name = r["scientific_name"]
    genus, species = s_name.split(" ", 1)
    query = f"gen:{genus} sp:{species}"
    try:
        resp = requests.get(
            "https://xeno-canto.org/api/3/recordings",
            params={"query": query, "key": API_KEY, "page": 1},
            headers=headers,
            timeout=10,
        )
        data = resp.json()
        n_rec = data.get("numRecordings", 0)
        n_pages = data.get("numPages", 0)
        total_pages += int(n_pages)
        print(f"{s_key} ({s_name}) -> recs: {n_rec}, pages: {n_pages}")
    except Exception as e:
        print(f"Error for {query}: {e}")
    time.sleep(0.3)

print(f"\nTotal pages to fetch across all 20 species: {total_pages}")
