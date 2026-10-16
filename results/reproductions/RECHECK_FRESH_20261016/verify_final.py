import csv,hashlib,json,pathlib,subprocess
ROOT=pathlib.Path('D:/FILE AND TASK/TA');OUT=ROOT/'results/reproductions/RECHECK_FRESH_20261016'
def sha(p):
 h=hashlib.sha256()
 with pathlib.Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
identity=json.loads((ROOT/'results/reproductions/E4_5sites_20261011T213404_350219Z/run_identity.json').read_text())['identity']
assets={k:sha(ROOT/v['path'])==v['sha256'] for k,v in identity['assets'].items()};assert all(assets.values())
git_sources={}
for k,v in identity['assets'].items():
 if k.endswith(('_cache','_metadata','_checkpoint')):continue
 git_sources[k]=hashlib.sha256(subprocess.check_output(['git','show','HEAD:'+v['path']],cwd=ROOT)).hexdigest()==v['sha256']
assert len(git_sources)==10 and all(git_sources.values())
snapshots=list((ROOT/'results/reproductions/E4_5sites_20261011T213404_350219Z/raw').glob('E4_R*_conditions/repeat_*/*.json'));assert len(snapshots)==320
for p in snapshots:
 m=json.loads(p.read_text());assert m['query_count']==311;assert sha(p.with_suffix('.csv'))==m['csv_sha256']
materials=json.loads((ROOT/'results/report_materials_manifest.json').read_text())['entries'];assert len(materials)==41
for m in materials:assert sha(ROOT/m['target'])==m['sha256']
review=ROOT/'Rencana-eksperimen-bimbingan/audit-pendengaran-E5'
with (review/'E5_AUDIT_PENDENGARAN.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
assert len(rows)==120 and all(r['review_status']=='pending' and not r['reviewer'] and not r['reviewed_at'] for r in rows)
pack=review/'listening-pack-20261016';m=json.loads((pack/'metadata.json').read_text())
assert m['cases']==120 and m['unique_clips']==276 and m['human_reviews_created']==0
assert sha(ROOT/'scripts/build_e5_listening_pack.py')==m['script_sha256']
assert sha(pack/'case_audio_index.csv')==m['index_sha256'] and sha(pack/'index.html')==m['html_sha256']
for rel,h in m['source_hashes'].items():assert sha(ROOT/rel)==h
for rel,data in m['clips'].items():assert sha(pack/rel)==data['sha256']
comp=json.loads((OUT/'comparison_report.json').read_text());assert comp['checks_passed']==comp['checks_total']==41
assert all(c.get('maximum_absolute_numeric_difference',c.get('maximum_absolute_difference'))==0 for c in comp['comparisons'])
newcase=next((OUT/'local-output').glob('E5_diagnostics_*/tables/selected_case_manifest.csv'))
with newcase.open(encoding='utf-8-sig',newline='') as f:
 reader=csv.DictReader(f);assert {'representation','condition','failure_mode'}.issubset(reader.fieldnames);assert len(list(reader))==120
result={'checked_local_date':'2026-10-16','E4_assets':assets,'E4_Git_source_assets':git_sources,'E4_snapshots_verified':320,'original_report_materials_verified':41,'E5_cases':120,'E5_local_clips_verified':276,'formal_human_reviews_recorded':0,'fresh_reproduction_comparisons_matched':41,'maximum_numeric_difference':0.0,'tests':{'original_venv':36,'fresh_venv':36,'fresh_clone_pipeline_suite_at_base_commit':32},'no_E4_inference_rerun':True,'source_file_preservation':json.loads(pathlib.Path('C:/Users/Fabio/AppData/Local/Temp/ta-completion-20261016-1792085956966/preservation-check.json').read_text())}
(OUT/'final_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n')
print('PASS: 19 E4 assets, 10 Git source blobs, 320 snapshots, 41 original report materials, 276 listening clips, and 41 fresh comparisons verified. Formal human reviews remain 0/120.')
