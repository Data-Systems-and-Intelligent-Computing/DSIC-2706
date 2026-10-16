import hashlib,json,pathlib,sys
import numpy as np,pandas as pd
BASE=pathlib.Path('D:/FILE AND TASK/TA')
WORK=pathlib.Path('C:/Users/Fabio/AppData/Local/Temp/ta-completion-20261016-1792085956966')
CLONE=WORK/'clean-clone'
progress=json.loads((WORK/'pipeline-progress.json').read_text())
checks=[]
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def compare(name,old,new,columns=None):
 a=pd.read_csv(old,low_memory=False);b=pd.read_csv(new,low_memory=False)
 cols=columns or list(set(a.columns)&set(b.columns));errors=[];numeric_max=0.;counts={}
 if len(a)!=len(b):errors.append('row_count')
 else:
  for c in cols:
   x=a[c];y=b[c]
   if pd.api.types.is_numeric_dtype(x) and pd.api.types.is_numeric_dtype(y):
    xx=x.to_numpy(dtype=float);yy=y.to_numpy(dtype=float);valid=np.isfinite(xx)&np.isfinite(yy)
    delta=float(np.max(np.abs(xx[valid]-yy[valid]))) if valid.any() else 0.;numeric_max=max(numeric_max,delta)
    bad=~np.isclose(xx,yy,rtol=1e-6,atol=1e-6,equal_nan=True)
    if bad.any():errors.append(c);counts[c]=int(bad.sum())
   else:
    bad=x.fillna('<MISSING>').astype(str).ne(y.fillna('<MISSING>').astype(str))
    if bad.any():errors.append(c);counts[c]=int(bad.sum())
 checks.append({'name':name,'rows_original':len(a),'rows_fresh':len(b),'columns_compared':sorted(cols),'maximum_absolute_numeric_difference':numeric_max,'rtol':1e-6,'atol':1e-6,'matches_within_tolerance':not errors,'differing_columns':errors,'differing_rows_by_column':counts,'original_sha256':sha(old),'fresh_sha256':sha(new)})
for rep in ('R0','R1','R2','R3'):
 old=BASE/'results/features'/f'clean_embeddings_{rep}.npz';new=CLONE/'results/features'/f'clean_embeddings_{rep}.npz'
 with np.load(old) as a,np.load(new) as b:
  dims={};maxdiff=0.;same=True
  for k in ('gal_feats','qry_feats'):
   diff=float(np.max(np.abs(a[k]-b[k])));maxdiff=max(maxdiff,diff);same=same and np.allclose(a[k],b[k],atol=1e-6,rtol=1e-6);dims[k]=list(b[k].shape)
  ids=all(np.array_equal(a[k],b[k]) for k in ('gal_ids','qry_ids'))
  checks.append({'name':'fresh_embeddings_'+rep,'shapes':dims,'maximum_absolute_difference':maxdiff,'matches_within_tolerance':bool(same and ids),'IDs_identical':ids,'fresh_archive_sha256':sha(new),'original_archive_sha256':sha(old)})
for filename in ('per_recording.csv','summary.csv','representation_probe.csv'):
 compare('E0_'+filename,BASE/'results/reproductions/E0_20261012_094649/tables'/filename,pathlib.Path(progress['stages']['E0']['output'])/'tables'/filename)
old2=BASE/'results/reproductions/E2_controlled_20261012T021600_897497Z'
new2=pathlib.Path(progress['stages']['E2']['output'])
for rep in ('R0','R1','R2','R3'):
 compare('E1_'+rep,old2/'raw'/f'{rep}_Clean.csv',pathlib.Path(progress['stages']['E1_'+rep]['output'])/'tables/per_query.csv')
for f in sorted((old2/'raw').glob('*.csv')):compare('E2_'+f.name,f,new2/'raw'/f.name)
old3=BASE/'results/reproductions/E3_open_set_20261012T022548_802536Z';new3=pathlib.Path(progress['stages']['E3']['output'])
for group,f in [('tables','frozen_thresholds.csv'),('tables','threshold_transfer.csv'),('raw','calibration_scores.csv'),('raw','test_scores.csv')]:compare('E3_'+f,old3/group/f,new3/group/f)
old5=BASE/'results/reproductions/E5_diagnostics_20261012T091512_868500Z';new5=pathlib.Path(progress['stages']['E5']['output'])
for f in ('all_query_diagnostics.csv','failure_cases.csv','failure_mode_summary.csv','selected_case_manifest.csv','unknown_open_set_diagnostics.csv'):compare('E5_'+f,old5/'tables'/f,new5/'tables'/f)
compare('H3_summary',BASE/'results/reproductions/H3_sensitivity_20261015/tables/h3_swing_summary.csv',CLONE/'results/reproductions/FRESH_H3_20261016/tables/h3_swing_summary.csv')
report={'base_commit':progress['base_commit'],'pipeline_progress':progress,'comparisons':checks,'all_comparisons_match_within_tolerance':all(c['matches_within_tolerance'] for c in checks),'checks_passed':sum(c['matches_within_tolerance'] for c in checks),'checks_total':len(checks),'E4_scope':'Frozen E4 source and statistical reanalysis only; E4 audio/model inference not rerun','input_restoration':json.loads((WORK/'restored-inputs.json').read_text())}
(WORK/'fresh-comparison-report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'passed':report['checks_passed'],'total':len(checks),'mismatches':[c for c in checks if not c['matches_within_tolerance']]},indent=2))
