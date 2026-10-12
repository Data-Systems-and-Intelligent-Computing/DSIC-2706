"""Append checksum-verified H3 report materials to the report manifest."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'results/report_materials_manifest.json'
h3=sorted((ROOT/'results/reproductions').glob('H3_habitat_profile_stability_*'))[-1]
payload=json.loads(manifest.read_text(encoding='utf-8'))

def digest(p: Path) -> str:
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

specs=[
 ('table','24_h3_habitat_profile_stability.csv','tables/h3_stability_summary.csv','H3 retention-swing summary and paired-bootstrap inference.'),
 ('table','25_h3_retention_by_habitat_repeat.csv','tables/h3_retention_by_habitat_repeat.csv','H3 per-location retention values across noise repeats.'),
 ('table','26_h3_bootstrap_distribution.csv','tables/h3_bootstrap_distribution.csv','H3 10,000 paired-bootstrap draws.'),
 ('figure','15_h3_habitat_retention_stability.png','figures/h3_habitat_retention_stability.png','H3 report figure: retention profiles and stability swings.'),
]
existing={e['target'] for e in payload['entries']}
for category,target,relative,purpose in specs:
 source=h3/relative
 destination=ROOT/('results/figures' if category=='figure' else 'results/tables')/target
 if digest(source)!=digest(destination): raise RuntimeError(f'checksum mismatch for {target}')
 entry={'category':category,'target':destination.relative_to(ROOT).as_posix(),'source':source.relative_to(ROOT).as_posix(),'sha256':digest(source),'bytes':source.stat().st_size,'purpose':purpose}
 if entry['target'] not in existing:
  payload['entries'].append(entry)
payload['schema']='report_materials_manifest_v2'
payload['h3_note']='H3 report materials were added from read-only statistical analysis of validated E4 raw CSV files.'
manifest.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Updated {manifest.relative_to(ROOT)}: {len(payload["entries"])} entries')
