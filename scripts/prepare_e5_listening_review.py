"""Prepare a blank human listening-review sheet from existing E5 evidence.

Recover omitted group labels by exact matching of EVERY original selected
column against full E2 diagnostics. Refuse missing/ambiguous matches; never
infer labels from names or fill in human observations. No audio processing.
"""
import argparse,csv,hashlib,json
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SELECTED=ROOT/'results/tables/16_e5_selected_case_manifest.csv'
FULL=ROOT/'results/reproductions/E5_diagnostics_20261012T091512_868500Z/tables/all_query_diagnostics.csv'
SPLIT=ROOT/'data/manifests/dataset_split.csv'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def prepare(output):
 output=Path(output).resolve()
 if output.parent!=(ROOT/'Rencana-eksperimen-bimbingan').resolve():raise ValueError('Output must be a new child of Rencana-eksperimen-bimbingan')
 if output.exists():raise FileExistsError(output)
 before={p.relative_to(ROOT).as_posix():sha(p) for p in (SELECTED,FULL,SPLIT)}
 with SELECTED.open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f);fields=reader.fieldnames;selected=list(reader)
 if len(selected)!=120:raise ValueError('Expected 120 selected source rows')
 keys={tuple(row[k] for k in fields) for row in selected}
 lookup=defaultdict(list)
 with FULL.open(encoding='utf-8-sig',newline='') as f:
  for row in csv.DictReader(f):
   if row['source_experiment']!='E2':continue
   key=tuple(row[k] for k in fields)
   if key in keys:lookup[key].append(row)
 with SPLIT.open(encoding='utf-8-sig',newline='') as f:paths={r['recording_id']:r['file_path'] for r in csv.DictReader(f)}
 reviews=[]
 for index,row in enumerate(selected,1):
  matches=lookup[tuple(row[k] for k in fields)]
  if len(matches)!=1:raise ValueError(f'Selected row {index}: expected 1 exact match, got {len(matches)}')
  full=matches[0]
  reviews.append({'case_id':f'E5_{index:03d}','selected_csv_row_1based':index+1,'source_row_sha256':hashlib.sha256(json.dumps(row,sort_keys=True,ensure_ascii=False).encode()).hexdigest(),'representation':full['representation'],'condition':full['condition'],'failure_mode_computational':full['failure_mode'],'query_id':row['query_id'],'species_key_metadata':row['species_key'],'query_audio_path':paths[row['query_id']],'top1_recording_id':row['top1_recording_id'],'top1_species_key_metadata':row['top1_species_key'],'top1_audio_path':paths[row['top1_recording_id']],'snr_db':row['snr_db'],'noise_file':row['noise_file'],'noise_seed':row['noise_seed'],'noise_start_sample':row['noise_start_sample'],'noise_segment_samples':row['noise_segment_samples'],'frozen_tau':row['frozen_tau'],'max_score':row['max_score'],'review_status':'pending','reviewer':'','reviewed_at':'','query_vocalisation_audible':'','top1_vocalisation_audible':'','background_observation':'','uncertainty_notes':'','auditory_interpretation':''})
 if any(sha(ROOT/p)!=h for p,h in before.items()):raise RuntimeError('Source changed during reading')
 output.mkdir(parents=True,exist_ok=False)
 target=output/'E5_AUDIT_PENDENGARAN.csv'
 with target.open('x',encoding='utf8',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=reviews[0].keys(),lineterminator='\n');writer.writeheader();writer.writerows(reviews)
 report={'source_commit':'8bf54415859f3473105c68c369832c2f66522fd8','source_sha256':before,'script_sha256':sha(Path(__file__)),'row_count':len(reviews),'unique_query_condition_pairs':len({(r['query_id'],r['condition']) for r in reviews}),'unique_queries':len({r['query_id'] for r in reviews}),'recovered_columns':['representation','condition','failure_mode'],'recovery_rule':'Exactly one E2 full-diagnostics row must match every original selected CSV column as text','completed_human_reviews':0,'human_observations':'Blank; pending human listening, not inferred by code','source_files_unchanged':True,'output_sha256':sha(target)}
 (output/'metadata.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,required=True);prepare(parser.parse_args().output_dir)
