"""Rebuild only clean E4 input embeddings into a NEW directory.

Never runs E4, mixes noise, replaces historical caches, or edits run_identity.
Original stage7 resume requires the exact recorded bytes; a fresh cache is new
provenance even when its numerical embeddings agree.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
IDENTITY=ROOT/'results/reproductions/E4_5sites_20261011T213404_350219Z/run_identity.json'
DIMS={'R0':40,'R1':2048,'R2':1024,'R3':40}

def sha256(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def rebuild(output,check_only=False):
    output=Path(output).resolve()
    if output.parent!=(ROOT/'results/reproductions').resolve():
        raise ValueError('Use a new direct child of results/reproductions')
    if output.exists():raise FileExistsError(f'Refusing to overwrite {output}')
    identity=json.loads(IDENTITY.read_text(encoding='utf8'))['identity']
    assets=identity['assets']
    source_hashes={}
    for key,item in assets.items():
        if key.endswith('_cache') or key.endswith('_metadata'):continue
        p=ROOT/item['path'];actual=sha256(p)
        if actual!=item['sha256']:raise ValueError(f'Recorded source differs: {key}')
        source_hashes[item['path']]=actual
    manifest=ROOT/'data/manifests/dataset_split.csv'
    frame=pd.read_csv(manifest,dtype={'recording_id':str})
    gallery=frame[frame.split_role.eq('gallery')].reset_index(drop=True)
    queries=frame[frame.split_role.eq('query_clean')].reset_index(drop=True)
    if (len(gallery),len(queries))!=(673,311):raise ValueError('Active split counts differ')
    for f in frame.file_path:
        if not (ROOT/f).is_file():raise FileNotFoundError(f)
    print('Source hashes and 1,216 audio paths verified. No E4/noise inference.')
    if check_only:return
    sys.path.insert(0,str(ROOT))
    from src.preprocess import preprocess_audio
    from src.embeddings import AudioRepresentationExtractor,R3_CONTROL_VERSION
    output.mkdir(parents=True,exist_ok=False)
    generated={}
    for rep,dimension in DIMS.items():
        extractor=AudioRepresentationExtractor(rep,random_seed=42)
        arrays={}
        for namespace,rows,key in [('gallery',gallery,'gal_feats'),('query_clean',queries,'qry_feats')]:
            vectors=[]
            for row in rows.itertuples(index=False):
                # R3 is independent of audio but retains the same stable ID namespace.
                y=np.zeros(160000,dtype=np.float32) if rep=='R3' else preprocess_audio(row.file_path)
                e=extractor.extract(y,item_id=f'{namespace}:{row.recording_id}')
                if e.shape!=(dimension,) or not np.isfinite(e).all():raise ValueError(f'Invalid embedding {rep}/{row.recording_id}')
                vectors.append(e)
            arrays[key]=np.stack(vectors).astype(np.float32)
        payload={**arrays,'gal_ids':gallery.recording_id.to_numpy(dtype=str),'qry_ids':queries.recording_id.to_numpy(dtype=str),'gal_labels':gallery.species_key.to_numpy(dtype=str),'qry_labels':queries.species_key.to_numpy(dtype=str),'representation':np.array(rep),'manifest_sha256':np.array(sha256(manifest))}
        if rep in ('R1','R2'):payload['checkpoint_sha256']=np.array(assets[f'{rep}_checkpoint']['sha256'])
        if rep=='R3':payload['r3_control_version']=np.array(R3_CONTROL_VERSION)
        target=output/f'clean_embeddings_{rep}.npz'
        np.savez_compressed(target,**payload)
        actual=sha256(target)
        generated[rep]={'path':target.relative_to(ROOT).as_posix(),'sha256':actual,'recorded_cache_sha256':assets[f'{rep}_cache']['sha256'],'matches_recorded_bytes':actual==assets[f'{rep}_cache']['sha256']}
        print(rep,arrays['gal_feats'].shape,arrays['qry_feats'].shape,flush=True)
    for rel,expected in source_hashes.items():
        if sha256(ROOT/rel)!=expected:raise RuntimeError(f'Source changed during extraction: {rel}')
    (output/'metadata.json').write_text(json.dumps({'purpose':'Fresh clean-cache reconstruction only; not an E4 result or automatic historical resume','sources':source_hashes,'script_sha256':sha256(__file__),'caches':generated,'numpy_version':np.__version__,'pandas_version':pd.__version__},indent=2)+'\n',encoding='utf8')
    print('Fresh caches created. Historical inputs and run_identity were not modified.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--check-only',action='store_true')
    args=parser.parse_args();rebuild(args.output_dir,args.check_only)
