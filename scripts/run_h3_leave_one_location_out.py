"""Exploratory leave-one-location-out H3 from stored AP@10; never rerun E4."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.run_h3_sensitivity_reanalysis import E4,HABITATS,SNRS,SEED,load_arrays,location_swing,sha256

def run(output,iterations=10000):
    output=Path(output).resolve()
    if output.parent!=(ROOT/'results/reproductions').resolve():raise ValueError('Use a new direct child of results/reproductions')
    if output.exists():raise FileExistsError(output)
    sources=[E4/'raw'/f'E4_{r}_raw.csv' for r in ('R1','R2')]
    before={p.relative_to(ROOT).as_posix():sha256(p) for p in sources}
    clean,noisy,ids=load_arrays(E4/'raw');n=len(ids)
    subsets={'all_5_locations':list(range(5)),**{'without_'+h:[i for i in range(5) if i!=j] for j,h in enumerate(HABITATS)}}
    points={k:location_swing(noisy.mean(axis=-1),clean.mean(axis=-1),keep) for k,keep in subsets.items()}
    draws={k:[np.empty((iterations,2,4)),np.empty((iterations,2,4))] for k in subsets}
    rng=np.random.default_rng(SEED);flat=noisy.reshape(-1,n)
    for start in range(0,iterations,100):
        stop=min(iterations,start+100);size=stop-start;ix=rng.integers(0,n,size=(size,n))
        weights=np.zeros((size,n));np.add.at(weights,(np.arange(size)[:,None],ix),1/n)
        means=(weights@flat.T).reshape(size,2,4,4,5);baseline=weights@clean.T
        for k,keep in subsets.items():
            absolute,relative=location_swing(means,baseline,keep)
            draws[k][0][start:stop]=absolute;draws[k][1][start:stop]=relative
    rows=[]
    for subset in subsets:
        for m,metric in enumerate(('absolute_mAP10','relative_retention')):
            for s,snr in enumerate((*SNRS,'mean_over_4_SNR')):
                point=points[subset][m][:,s] if s<4 else points[subset][m].mean(axis=-1)
                dist=draws[subset][m][:,:,s] if s<4 else draws[subset][m].mean(axis=-1)
                lo,hi=np.quantile(dist[:,0]-dist[:,1],[.025,.975])
                rows.append(dict(location_subset=subset,excluded_location='none' if subset=='all_5_locations' else subset.removeprefix('without_'),metric=metric,snr_db=snr,R1_swing=point[0],R2_swing=point[1],R1_minus_R2=point[0]-point[1],ci95_low=lo,ci95_high=hi,interpretation='R2 narrower' if lo>0 else 'R1 narrower' if hi<0 else 'inconclusive',queries=n,locations=len(subsets[subset]),repeats=4,bootstrap_iterations=iterations))
    table=pd.DataFrame(rows)
    old=ROOT/'results/reproductions/H3_sensitivity_20261015/tables/h3_swing_summary.csv';previous=pd.read_csv(old)
    fields=['R1_swing','R2_swing','R1_minus_R2','ci95_low','ci95_high'];maxdiff=0.
    for row in previous.itertuples(index=False):
        found=table[(table.location_subset==row.location_subset)&(table.metric==row.metric)&(table.snr_db.astype(str)==str(row.snr_db))]
        if len(found)!=1:raise ValueError('Historical H3 row missing')
        expected=np.array([getattr(row,f) for f in fields]);actual=found[fields].to_numpy(float)[0]
        if not np.allclose(expected,actual,atol=1e-12,rtol=1e-12):raise ValueError('Existing H3 results differ')
        maxdiff=max(maxdiff,float(np.max(np.abs(expected-actual))))
    if before!={p.relative_to(ROOT).as_posix():sha256(p) for p in sources}:raise RuntimeError('E4 source changed')
    output.mkdir(parents=True,exist_ok=False);(output/'tables').mkdir()
    table.to_csv(output/'tables/h3_leave_one_location_out.csv',index=False,lineterminator='\n')
    text='# H3 leave-one-location-out sensitivity\n\nAll five locations remain in E4. These six scenarios are exploratory statistical subsets of stored AP@10, not new audio runs. Each omitted-location scenario uses four locations.\n\n'
    for metric in ('absolute_mAP10','relative_retention'):
        text+='## '+metric+' — mean over four SNR levels\n\n| Omitted | R1 | R2 | R1−R2 | CI 95% for difference |\n|---|---:|---:|---:|---|\n'
        for r in table[(table.metric==metric)&(table.snr_db=='mean_over_4_SNR')].itertuples(index=False):
            text+=f'| {r.excluded_location} | {r.R1_swing:.6f} | {r.R2_swing:.6f} | {r.R1_minus_R2:.6f} | [{r.ci95_low:.6f}, {r.ci95_high:.6f}] |\n'
        text+='\n'
    text+='Intervals are unadjusted exploratory percentile intervals conditional on fixed sites/noise segments. Subsets are correlated and do not estimate causal contributions of a location. A narrower range after removing a site is partly a consequence of having fewer locations. All per-SNR values remain in the CSV.\n'
    (output/'README.md').write_text(text,encoding='utf8',newline='\n')
    metadata={'source_raw_sha256':before,'script_sha256':sha256(__file__),'shared_H3_method_sha256':sha256(ROOT/'scripts/run_h3_sensitivity_reanalysis.py'),'seed':SEED,'bootstrap_iterations':iterations,'resampling':'Shared query indices across representations/SNR/repeats/sites and clean denominator; same draws for all subsets','scenarios':subsets,'rows':len(table),'historical_rows_reproduced':len(previous),'maximum_historical_numeric_difference':maxdiff,'previous_summary_sha256':sha256(old),'E4_rerun':False,'source_files_unchanged':True,'limitations':['Exploratory, unadjusted intervals','Conditional on fixed locations and noise segments','Omission is a sensitivity check, not causal attribution'],'outputs_sha256':{p.relative_to(output).as_posix():sha256(p) for p in output.rglob('*') if p.is_file()}}
    (output/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf8',newline='\n')
    print(table[table.snr_db=='mean_over_4_SNR'].to_string(index=False));print('OUTPUT',output)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);a=p.parse_args();run(a.output_dir)
