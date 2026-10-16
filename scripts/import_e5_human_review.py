"""Validate self-reported human E5 notes and export a NEW CSV; never overwrite."""
from __future__ import annotations
import argparse,csv,hashlib,json
from datetime import datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REVIEW=ROOT/'Rencana-eksperimen-bimbingan/audit-pendengaran-E5'
FIELDS=('review_status','reviewer','reviewed_at','query_vocalisation_audible','top1_vocalisation_audible','background_observation','uncertainty_notes','auditory_interpretation')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def combine_reviews(rows,payload,expected_hash):
    if payload.get('schema')!='e5_human_listening_review_v1' or payload.get('source_review_sheet_sha256')!=expected_hash:
        raise ValueError('Review schema/source checksum differs')
    by_id={r['case_id']:dict(r) for r in rows}
    if len(by_id)!=len(rows):raise ValueError('Duplicate source case IDs')
    seen=set()
    for review in payload.get('reviews',[]):
        identifier=review.get('case_id')
        if identifier in seen or identifier not in by_id:raise ValueError('Duplicate/unknown reviewed case')
        seen.add(identifier);source=by_id[identifier]
        if review.get('source_row_sha256')!=source['source_row_sha256']:raise ValueError('Case provenance differs')
        if review.get('review_status') not in ('reviewed','needs_follow_up'):raise ValueError('Invalid review status')
        for key in FIELDS:
            if not isinstance(review.get(key),str):raise ValueError('Missing/non-text review field: '+key)
        for key in FIELDS:
            if key!='uncertainty_notes' and not review[key].strip():raise ValueError('Empty required review field: '+key)
        for key in ('query_vocalisation_audible','top1_vocalisation_audible'):
            if review[key] not in ('yes','no','uncertain'):raise ValueError('Invalid audible observation')
        parsed=datetime.fromisoformat(review['reviewed_at'].replace('Z','+00:00'))
        if parsed.tzinfo is None:raise ValueError('Review timestamp requires timezone')
        source.update({key:review[key] for key in FIELDS})
    return [by_id[r['case_id']] for r in rows]
def main(review_json,output=None,check_only=False):
    source=REVIEW/'E5_AUDIT_PENDENGARAN.csv'
    with source.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f);fields=reader.fieldnames;rows=list(reader)
    merged=combine_reviews(rows,json.loads(Path(review_json).read_text(encoding='utf-8-sig')),sha(source))
    counts={s:sum(r['review_status']==s for r in merged) for s in ('pending','reviewed','needs_follow_up')}
    if not check_only:
        if output is None:raise ValueError('--output is required unless --check-only')
        output=Path(output).resolve()
        if output.parent!=REVIEW.resolve() or output.suffix.lower()!='.csv':raise ValueError('Use a new CSV directly under audit-pendengaran-E5')
        if output.exists() or output.with_suffix('.metadata.json').exists():raise FileExistsError(output)
        with output.open('x',encoding='utf8',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(merged)
        metadata={'source_sheet_sha256':sha(source),'human_notes_json_sha256':sha(review_json),'output_sha256':sha(output),'counts':counts,'validation_scope':'Structure/provenance only; human observations are self-reported and not verified by software','script_sha256':sha(__file__)}
        output.with_suffix('.metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({'validated_counts':counts,'human_listening_not_inferred_by_code':True},indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--review-json',type=Path,required=True);p.add_argument('--output',type=Path);p.add_argument('--check-only',action='store_true');a=p.parse_args();main(a.review_json,a.output,a.check_only)
