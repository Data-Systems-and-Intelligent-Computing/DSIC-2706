"""Restore only checksum-verified external inputs into a separate Git clone.

Never copy embeddings, modify source inputs, or overwrite a different file.
Uses the active split, including download rows marked VERIFIED_EXISTING.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def rows(rel):
    with (ROOT/rel).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def input_plan():
    downloads={r['file_path']:r for r in rows('data/manifests/download_manifest.csv')}
    active=rows('data/manifests/dataset_split.csv');noise=rows('data/manifests/itera_noise_manifest.csv');unknown=rows('data/manifests/unknown_open_set_manifest.csv')
    if (len(active),len(noise),len(unknown))!=(1216,1799,543):raise ValueError('Active manifest counts differ')
    plan={}
    def add(rel,digest):
        rel=rel.replace('\\','/')
        if len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest.lower()):raise ValueError('Missing/invalid SHA-256 '+rel)
        if rel in plan and plan[rel]!=digest:raise ValueError('Conflicting checksum '+rel)
        if not (ROOT/rel).resolve().is_relative_to(ROOT.resolve()):raise ValueError('Path outside clone')
        plan[rel]=digest
    for r in active:add(r['file_path'],downloads[r['file_path']]['sha256'])
    for r in unknown:add(r['file_path'],r['sha256'])
    for r in noise:add('data/itera_noise/'+r['filename'],r['sha256_checksum'])
    assets=json.loads((ROOT/'results/reproductions/E4_5sites_20261011T213404_350219Z/run_identity.json').read_text())['identity']['assets']
    for key in ('R1_checkpoint','R2_checkpoint'):add(assets[key]['path'],assets[key]['sha256'])
    return plan
def restore(source_root,report,verify_only=False):
    source_root=Path(source_root).resolve();report=Path(report).resolve()
    if source_root==ROOT.resolve():raise ValueError('Source archive must differ from destination clone')
    if not report.is_relative_to((ROOT/'results/reproductions').resolve()):raise ValueError('Report must be under clone results/reproductions')
    if report.exists():raise FileExistsError(report)
    records=[]
    for i,(rel,expected) in enumerate(input_plan().items(),1):
        source=source_root/rel;target=ROOT/rel
        if not source.resolve().is_relative_to(source_root):raise ValueError('Source path outside archive')
        if sha(source)!=expected:raise ValueError('Source SHA mismatch '+rel)
        existed=target.exists()
        if not existed:
            if verify_only:raise FileNotFoundError(target)
            target.parent.mkdir(parents=True,exist_ok=True)
            with source.open('rb') as src,target.open('xb') as dst:shutil.copyfileobj(src,dst,1048576)
        if sha(target)!=expected:raise ValueError('Destination differs; refusing replacement '+rel)
        records.append({'path':rel,'sha256':expected,'bytes':target.stat().st_size,'already_present':existed})
        if i%250==0:print(f'Inputs verified: {i}',flush=True)
    report.parent.mkdir(parents=True,exist_ok=True)
    result={'source_archive':str(source_root),'destination_clone':str(ROOT),'inputs':records,'count':len(records),'embedding_caches_copied':0,'script_sha256':sha(__file__),'verify_only':verify_only}
    with report.open('x',encoding='utf8',newline='\n') as f:json.dump(result,f,indent=2);f.write('\n')
    print(f'PASS: {len(records)} inputs verified; no embedding caches copied',flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--report',type=Path,required=True);p.add_argument('--verify-only',action='store_true');a=p.parse_args();restore(a.source_root,a.report,a.verify_only)
