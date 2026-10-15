"""Post-hoc H3 sensitivity from stored E4 metrics; no audio/model imports or E4 writes.

Compute mean-over-repeat location ranges of absolute mAP@10 and retention,
for all five locations and the requested exclusion of Kebun Raya. Bootstrap
shared query IDs across representations, SNRs, repeats, and locations.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
E4 = ROOT / 'results/reproductions/E4_5sites_20261011T213404_350219Z'
REPS = ('R1', 'R2')
SNRS = (20, 10, 0, -5)
HABITATS = ('Embung_F', 'Gedung_F', 'Kebun_Raya', 'Masjid_At_Tanwir', 'Sekitar_GKU_1')
SEED = 20261012

def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load_arrays(raw_dir):
    clean, noisy, common_ids = [], [], None
    for rep in REPS:
        frame = pd.read_csv(Path(raw_dir) / f'E4_{rep}_raw.csv')
        baseline = frame.loc[frame.condition.eq('Clean')].sort_values('query_id')
        ids = baseline.query_id.astype(str).tolist()
        if len(ids) != 311 or len(set(ids)) != 311:
            raise ValueError(f'{rep}: expected 311 unique clean query IDs')
        if common_ids is not None and ids != common_ids:
            raise ValueError('R1/R2 query IDs differ')
        common_ids = ids
        a = np.empty((4, 4, 5, 311))
        if len(frame) != 311 * 81:
            raise ValueError(f'{rep}: unexpected raw row count')
        for s, snr in enumerate(SNRS):
            for repeat in range(4):
                for h, habitat in enumerate(HABITATS):
                    rows = frame.loc[frame.snr_db.eq(snr) & frame.repeat_id.eq(repeat) & frame.habitat.eq(habitat)].sort_values('query_id')
                    if rows.query_id.astype(str).tolist() != ids:
                        raise ValueError(f'{rep}/{snr}/{repeat}/{habitat}: incomplete or duplicate query IDs')
                    a[s, repeat, h] = rows['AP@10'].to_numpy(float)
        clean.append(baseline['AP@10'].to_numpy(float)); noisy.append(a)
    c, n = np.stack(clean), np.stack(noisy)
    if not (np.isfinite(c).all() and np.isfinite(n).all() and (c >= 0).all() and (c <= 1).all() and (n >= 0).all() and (n <= 1).all()):
        raise ValueError('AP values must be finite and in [0,1]')
    if (c.mean(axis=-1) <= 0).any():
        raise ValueError('Clean means must be positive for retention')
    return c, n, common_ids

def location_swing(means, clean_means, keep):
    """means [..., rep, snr, repeat, habitat]; range first, mean repeats second."""
    subset = means[..., keep]
    absolute = np.ptp(subset, axis=-1).mean(axis=-1)
    relative = absolute / clean_means[..., :, None]
    return absolute, relative

def paired_bootstrap(clean, noisy, iterations=10000, seed=SEED):
    n_queries = clean.shape[-1]
    observed = noisy.mean(axis=-1)
    baseline = clean.mean(axis=-1)
    subsets = {'all_5_locations': list(range(5)), 'without_Kebun_Raya': [i for i,h in enumerate(HABITATS) if h != 'Kebun_Raya']}
    point = {key: location_swing(observed, baseline, keep) for key,keep in subsets.items()}
    draws = {key: [np.empty((iterations,2,4)), np.empty((iterations,2,4))] for key in subsets}
    rng = np.random.default_rng(seed)
    flat = noisy.reshape(-1,n_queries)
    for start in range(0,iterations,100):
        stop = min(start+100,iterations); size = stop-start
        indices = rng.integers(0,n_queries,size=(size,n_queries))
        weights = np.zeros((size,n_queries))
        np.add.at(weights,(np.arange(size)[:,None],indices),1/n_queries)
        means = (weights @ flat.T).reshape(size,2,4,4,5)
        c = weights @ clean.T
        for key,keep in subsets.items():
            absolute,relative = location_swing(means,c,keep)
            draws[key][0][start:stop] = absolute; draws[key][1][start:stop] = relative
    return point,draws

def run(output, iterations=10000):
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError(f'Refusing to overwrite output: {output}')
    if output.parent != (ROOT/'results/reproductions').resolve():
        raise ValueError('Output must be a new direct child of results/reproductions')
    if iterations < 100:
        raise ValueError('At least 100 bootstrap iterations are required')
    sources = [E4/'raw'/f'E4_{rep}_raw.csv' for rep in REPS]
    before = {p.relative_to(ROOT).as_posix():sha256(p) for p in sources}
    clean,noisy,ids = load_arrays(E4/'raw')
    observed,draws = paired_bootstrap(clean,noisy,iterations)
    rows = []
    for subset in observed:
        for metric_idx,metric in enumerate(('absolute_mAP10','relative_retention')):
            point = observed[subset][metric_idx]; boot = draws[subset][metric_idx]
            for s,snr in enumerate((*SNRS,'mean_over_4_SNR')):
                values = point[:,s] if s<4 else point.mean(axis=-1)
                distribution = boot[:,:,s] if s<4 else boot.mean(axis=-1)
                difference = distribution[:,0]-distribution[:,1]
                lo,hi = np.quantile(difference,[.025,.975])
                rows.append(dict(location_subset=subset,metric=metric,snr_db=snr,R1_swing=values[0],R2_swing=values[1],R1_minus_R2=values[0]-values[1],ci95_low=lo,ci95_high=hi,interpretation='R2 narrower' if lo>0 else 'R1 narrower' if hi<0 else 'inconclusive',queries=len(ids),locations=5 if subset=='all_5_locations' else 4,repeats=4,bootstrap_iterations=iterations))
    summary = pd.DataFrame(rows)
    after = {p.relative_to(ROOT).as_posix():sha256(p) for p in sources}
    if before != after:
        raise RuntimeError('E4 source changed during analysis')
    output.mkdir(parents=True,exist_ok=False)
    (output/'tables').mkdir(); (output/'figures').mkdir()
    summary.to_csv(output/'tables/h3_swing_summary.csv',index=False)
    profile_rows=[]
    for r,rep in enumerate(REPS):
        for s,snr in enumerate(SNRS):
            for repeat in range(4):
                for h,habitat in enumerate(HABITATS):
                    mean=noisy[r,s,repeat,h].mean()
                    profile_rows.append(dict(representation=rep,snr_db=snr,repeat_id=repeat,habitat=habitat,mAP10=mean,clean_mAP10=clean[r].mean(),relative_retention=mean/clean[r].mean()))
    pd.DataFrame(profile_rows).to_csv(output/'tables/location_map10_by_repeat.csv',index=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(2,2,figsize=(12,8),sharex=True)
    colors={'R1':'#d95f02','R2':'#16856e'}
    for col,subset in enumerate(observed):
        for row,(metric,ylabel) in enumerate((('absolute_mAP10','Absolute mAP@10 swing'),('relative_retention','Relative-retention swing'))):
            ax=axes[row,col]
            sub=summary[(summary.location_subset==subset)&(summary.metric==metric)&(summary.snr_db!='mean_over_4_SNR')]
            for rep in REPS: ax.plot(range(4),sub[f'{rep}_swing'],marker='o',label=rep,color=colors[rep])
            ax.set_title('All 5 locations' if col==0 else 'Without Kebun Raya')
            ax.set_ylabel(ylabel);ax.set_xticks(range(4),['+20','+10','0','-5']);ax.grid(axis='y',alpha=.25);ax.set_ylim(bottom=0)
            if row==1:ax.set_xlabel('SNR (dB)')
    axes[0,0].legend();fig.suptitle('E4 post-hoc sensitivity: range over locations, then mean over four repeats')
    fig.tight_layout();fig.savefig(output/'figures/h3_absolute_relative_sensitivity.png',dpi=180);plt.close(fig)
    metadata=dict(analysis='Exploratory H3 absolute/relative swing and exclusion of Kebun Raya',source_raw_sha256=before,script_sha256=sha256(__file__),seed=SEED,bootstrap_iterations=iterations,numpy_version=np.__version__,pandas_version=pd.__version__,estimand='mean_repeat(max_location(mean_query AP10) - min_location(mean_query AP10)); retention divides by each representation clean mAP10',resampling='Shared query indices across both representations and all conditions; fixed locations and noise draws; clean denominator re-estimated in each draw',limitations=['Post-hoc, unadjusted descriptive percentile intervals; not preregistered confirmation','Conditional on these locations and sampled noise segments; not uncertainty over new locations or recording sessions','Excluding Kebun Raya is a requested sensitivity subset, not removal from E4','No spectral causal mechanism tested'],source_files_unchanged=before==after,outputs_sha256={p.relative_to(output).as_posix():sha256(p) for p in output.rglob('*') if p.is_file()})
    (output/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf8')
    (output/'README.md').write_text('# H3 sensitivity reanalysis\n\nStored E4 raw CSVs only; no audio mixing, inference, or edits to the original run.\n\nBoth absolute mAP@10 swing and relative-retention swing are reported for all five locations and without Kebun Raya. Range is computed within each repeat before averaging repeats. Paired query bootstrap uses 10,000 draws by default; intervals are exploratory and conditional on fixed noise/location samples.\n',encoding='utf8')
    print(summary.to_string(index=False))
    print('OUTPUT',output)
    return output

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--bootstrap-iterations',type=int,default=10000)
    args=parser.parse_args();run(args.output_dir,args.bootstrap_iterations)
