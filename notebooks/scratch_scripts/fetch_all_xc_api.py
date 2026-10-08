import json
import time
from pathlib import Path
import pandas as pd
import requests

API_KEY = "95dc5b3f6834b56e17da4cf68cc890cb470d1284"
headers = {
    "X-API-Key": API_KEY,
    "User-Agent": "BirdSoundResearch/1.0",
    "Accept": "application/json",
}

CACHE_FILE = Path(r"C:\Users\Fabio\.gemini\antigravity\brain\29c8c496-9c02-45a8-aece-af8d01cc9493\scratch\xc_api_cache.json")
FREEZE_CSV = Path(r"D:\FILE AND TASK\TA\data\manifests\species_freeze.csv")

def main():
    freeze_df = pd.read_csv(FREEZE_CSV)
    
    # Load existing cache if exists
    if CACHE_FILE.exists():
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        print(f"Loaded existing cache with {len(cache):,} recordings.")
    else:
        cache = {}

    session = requests.Session()
    session.headers.update(headers)

    total_added = 0
    for idx, row in freeze_df.iterrows():
        s_key = row["species_key"]
        s_name = row["scientific_name"]
        genus, species = s_name.split(" ", 1)
        query = f"gen:{genus} sp:{species}"
        
        print(f"[{idx+1}/20] Fetching {s_key}: {s_name} ({query})...")
        
        # Get page 1 first to determine total pages
        try:
            resp = session.get(
                "https://xeno-canto.org/api/3/recordings",
                params={"query": query, "key": API_KEY, "page": 1},
                timeout=15,
            )
            if resp.status_code != 200:
                print(f"  Error HTTP {resp.status_code} for page 1")
                continue
            data = resp.json()
            num_pages = int(data.get("numPages", 1))
            num_recs = int(data.get("numRecordings", 0))
            print(f"  Total {num_recs} recs across {num_pages} pages.")
            
            # Process page 1 recordings
            for rec in data.get("recordings", []):
                rec_id = str(rec.get("id"))
                if rec_id not in cache:
                    cache[rec_id] = rec
                    total_added += 1
            
            # Process remaining pages
            for page in range(2, num_pages + 1):
                time.sleep(0.25)
                p_resp = session.get(
                    "https://xeno-canto.org/api/3/recordings",
                    params={"query": query, "key": API_KEY, "page": page},
                    timeout=15,
                )
                if p_resp.status_code == 200:
                    p_data = p_resp.json()
                    for rec in p_data.get("recordings", []):
                        rec_id = str(rec.get("id"))
                        if rec_id not in cache:
                            cache[rec_id] = rec
                            total_added += 1
                else:
                    print(f"  Page {page} failed with status {p_resp.status_code}")
                    
        except Exception as e:
            print(f"  Exception while fetching {s_name}: {e}")
            
        time.sleep(0.25)

    print(f"\nFinished! Total unique recordings in cache: {len(cache):,} (New added: {total_added:,})")
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    print(f"Saved cache to: {CACHE_FILE}")

if __name__ == "__main__":
    main()
