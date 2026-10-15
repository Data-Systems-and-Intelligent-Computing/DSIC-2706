"""Materialize the revised RQ/H matrix without replacing any previous table."""
from pathlib import Path
import hashlib,json
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
HISTORICAL=ROOT/'results/tables/27_rq_hypothesis_matrix_current.csv'
SENSITIVITY=ROOT/'results/reproductions/H3_sensitivity_20261015/tables/h3_swing_summary.csv'
OUTPUT=ROOT/'results/tables/28_rq_hypothesis_matrix_revised_2026-10-15.csv'

def main():
    if OUTPUT.exists() or OUTPUT.with_suffix('.metadata.json').exists():raise FileExistsError(OUTPUT)
    matrix=pd.read_csv(HISTORICAL);summary=pd.read_csv(SENSITIVITY)
    for item in ('H3','H4','Sub-RQ 3'):
        if matrix.item.eq(item).sum()!=1:raise ValueError(f'Expected one {item} row')
    full=summary[summary.location_subset.eq('all_5_locations') & summary.metric.eq('absolute_mAP10') & summary.snr_db.eq('mean_over_4_SNR')].iloc[0]
    subset=summary[summary.location_subset.eq('without_Kebun_Raya') & summary.metric.eq('relative_retention') & summary.snr_db.eq('-5')].iloc[0]
    matrix.loc[matrix.item.eq('H3'),['experiment','metric','artifact','result','conclusion','limitation']]=[
        'E4 stored raw + exploratory H3 sensitivity','Absolute mAP@10 and relative-retention location swing; full and without Kebun Raya',SENSITIVITY.relative_to(ROOT).as_posix(),
        f"Full-set mean absolute R1-R2={full.R1_minus_R2:.6f}, CI [{full.ci95_low:.6f}, {full.ci95_high:.6f}]; without Kebun Raya at -5 dB relative R1-R2={subset.R1_minus_R2:.6f}, CI [{subset.ci95_low:.6f}, {subset.ci95_high:.6f}].",
        'Metric- and location-dependent exploratory evidence; no universal R2 stability advantage',
        'Original real-soundscape H3 untested. H3 reframed after results on 2026-10-12; sensitivity added 2026-10-15. No causal spectral test or new-site uncertainty.']
    matrix.loc[matrix.item.eq('H4'),'conclusion']='Exploratory revised interpretation: known acceptance recall falls; false-accept rate does not rise'
    matrix.loc[matrix.item.eq('H4'),'limitation']='H4 operating-point wording changed after results on 2026-10-12; original wording retained in hypotheses.md. Recall at tau measures acceptance, not correct species retrieval. No spectral compression mechanism established.'
    matrix.loc[matrix.item.eq('Sub-RQ 3'),['metric','artifact','result','limitation']]=[
        'Location-conditioned mAP@10 plus absolute and relative swings',SENSITIVITY.relative_to(ROOT).as_posix(),
        'Five locations, four SNRs and four repeats; stability ordering depends on metric and exclusion of Kebun Raya.',
        'Sub-RQ reformulated after results on 2026-10-12. Original focal-to-soundscape question is not tested.']
    matrix.to_csv(OUTPUT,index=False)
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    metadata={'artifact':OUTPUT.relative_to(ROOT).as_posix(),'revision_date':'2026-10-15','sources_sha256':{p.relative_to(ROOT).as_posix():digest(p) for p in (HISTORICAL,SENSITIVITY)},'script_sha256':digest(Path(__file__)),'sha256':digest(OUTPUT),'policy':'Previous tables 23 and 27 and original experiment runs preserved unchanged.'}
    OUTPUT.with_suffix('.metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf8')
    print(OUTPUT)
if __name__=='__main__':main()
