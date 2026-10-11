import urllib.request
import urllib.parse
import json

query = """
[out:json];
(
  node["name"~"Gedung F",i](-5.38,105.29,-5.34,105.33);
  way["name"~"Gedung F",i](-5.38,105.29,-5.34,105.33);
  relation["name"~"Gedung F",i](-5.38,105.29,-5.34,105.33);
  node["name"~"Fakultas Sains",i](-5.38,105.29,-5.34,105.33);
  way["name"~"Fakultas Sains",i](-5.38,105.29,-5.34,105.33);
);
out center;
"""

url = "https://overpass-api.de/api/interpreter?data=" + urllib.parse.quote(query)

try:
    req = urllib.request.Request(url, headers={"User-Agent": "Antigravity/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode())
        elements = data.get("elements", [])
        print(f"Found {len(elements)} elements")
        for el in elements:
            name = el.get("tags", {}).get("name", "Unknown")
            coords = el.get("center", {"lat": el.get("lat"), "lon": el.get("lon")})
            print(f"- {name}: lat={coords.get('lat')}, lon={coords.get('lon')}")
except Exception as e:
    print("Overpass error:", e)
