import requests, json, re

xc_id = '409514'
url = f'https://xeno-canto.org/{xc_id}'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers, timeout=15)
print('status:', r.status_code)

# Cari JSON embed di halaman
lat_matches = re.findall(r'"lat"\s*:\s*"([^"]+)"', r.text)
lng_matches = re.findall(r'"lng"\s*:\s*"([^"]+)"', r.text)
print('lat:', lat_matches[:5])
print('lng:', lng_matches[:5])

# Cari hz
hz_matches = re.findall(r'"hz-low"\s*:\s*"([^"]*)"', r.text)
hzh_matches = re.findall(r'"hz-high"\s*:\s*"([^"]*)"', r.text)
print('hz-low:', hz_matches[:3])
print('hz-high:', hzh_matches[:3])

# Cari data JSON di script
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, 'html.parser')
scripts = soup.find_all('script')
print(f'\nTotal script tags: {len(scripts)}')
for i, s in enumerate(scripts):
    if s.string and ('lat' in s.string or 'recording' in s.string.lower()):
        print(f'\nScript {i} (first 800 chars):')
        print(s.string[:800])
        break

# Cari di table / dl
dls = soup.find_all('dl')
print(f'\nTotal dl tags: {len(dls)}')
for dl in dls:
    print(dl.get_text(separator=' | ', strip=True)[:300])
    print('---')
