"""Build verified, local-only E5 listening clips; never create human judgements."""
from __future__ import annotations
import argparse,csv,hashlib,html,json,os,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import pandas as pd
import soundfile as sf
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.preprocess import preprocess_audio,TARGET_SR
from src.mix_noise import mix_audio_at_snr
REVIEW=ROOT/'Rencana-eksperimen-bimbingan/audit-pendengaran-E5'
E2=ROOT/'results/reproductions/E2_controlled_20261012T021600_897497Z'
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def load_csv(p):
    with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def build(output):
    output=Path(output).resolve()
    if output.parent!=REVIEW.resolve():raise ValueError('Use a new direct child of audit-pendengaran-E5')
    if output.exists():raise FileExistsError(output)
    sheet=REVIEW/'E5_AUDIT_PENDENGARAN.csv'
    meta=json.loads((REVIEW/'metadata.json').read_text())
    if sha(sheet)!=meta['output_sha256']:raise ValueError('Review sheet changed; preserve reviews and review new provenance first')
    for rel,expected in meta['source_sha256'].items():
        if sha(ROOT/rel)!=expected:raise ValueError('Source checksum mismatch: '+rel)
    cases=load_csv(sheet)
    if len(cases)!=120:raise ValueError('Expected 120 cases')
    output.mkdir(parents=True,exist_ok=False);(output/'clips').mkdir()
    clean_cache={};written={};input_hashes={};raw_cache={};indexes=[]
    def clean(identifier,rel):
        if identifier not in clean_cache:
            p=ROOT/rel;input_hashes[rel]=sha(p);clean_cache[identifier]=preprocess_audio(rel)
        return clean_cache[identifier]
    def clip(name,y):
        rel='clips/'+name+'.wav'
        if rel not in written:
            if y.shape!=(160000,) or not np.isfinite(y).all():raise ValueError('Invalid waveform '+name)
            target=output/rel;sf.write(target,y,TARGET_SR,subtype='FLOAT',format='WAV')
            back,sr=sf.read(target,dtype='float32')
            if sr!=TARGET_SR or not np.array_equal(back,y):raise ValueError('Waveform roundtrip differs '+name)
            written[rel]={'sha256':sha(target),'float32_waveform_sha256':hashlib.sha256(y.astype('<f4').tobytes()).hexdigest(),'samples':len(y),'sample_rate':sr,'peak':float(np.max(np.abs(y)))}
        return rel
    for i,case in enumerate(cases,1):
        qid=case['query_id'];cond=case['condition'];rep=case['representation']
        key=(rep,cond)
        if key not in raw_cache:
            source=E2/'raw'/f'{rep}_{cond}.csv';input_hashes[source.relative_to(ROOT).as_posix()]=sha(source)
            raw_cache[key]={r['query_id']:r for r in load_csv(source)}
        raw=raw_cache[key][qid]
        if raw['top1_recording_id']!=case['top1_recording_id']:raise ValueError('Top-1 mismatch '+case['case_id'])
        yclean=clean(qid,case['query_audio_path'])
        qclean=clip('clean_'+qid,yclean)
        y=yclean;audit=None
        if cond!='Clean':
            y,audit=mix_audio_at_snr(yclean,float(raw['snr_db']),seed=int(float(raw['noise_seed'])),return_audit_info=True)
            for field in ('noise_file','noise_seed','noise_start_sample','noise_segment_samples','noise_attempt'):
                expected=raw[field] if field=='noise_file' else int(float(raw[field]))
                if audit[field]!=expected:raise ValueError('Mixture identity mismatch '+case['case_id']+' '+field)
            for field in ('snr_db_achieved','noise_gain','post_mix_gain'):
                if not np.isclose(audit[field],float(raw[field]),rtol=1e-6,atol=1e-6):raise ValueError('Mixture value mismatch '+field)
            if abs(audit['snr_db_achieved']-float(raw['snr_db']))>0.5:raise ValueError('SNR tolerance failed')
            nrel='data/itera_noise/'+audit['noise_file'];input_hashes.setdefault(nrel,sha(ROOT/nrel))
        qclip=clip('query_'+qid+'_'+cond,y)
        top=clip('clean_'+case['top1_recording_id'],clean(case['top1_recording_id'],case['top1_audio_path']))
        indexes.append({'case_id':case['case_id'],'representation':rep,'condition':cond,'failure_mode_computational':case['failure_mode_computational'],'query_id':qid,'top1_recording_id':case['top1_recording_id'],'query_clip':qclip,'query_clean_clip':qclean,'top1_clip':top,'mixture_verified':cond=='Clean' or audit is not None,'snr_db_achieved':None if audit is None else audit['snr_db_achieved'],'source_row_sha256':case['source_row_sha256'],'review_status':'pending'})
        if i%20==0:print(f'Listening clips verified: {i}/120',flush=True)
    for rel,expected in input_hashes.items():
        if sha(ROOT/rel)!=expected:raise RuntimeError('Input changed during export '+rel)
    with (output/'case_audio_index.csv').open('x',encoding='utf8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=indexes[0],lineterminator='\n');writer.writeheader();writer.writerows(indexes)
    document=HTML.replace('__CASES__',json.dumps(indexes,ensure_ascii=False).replace('<','\u003c')).replace('__PACK__',sha(sheet))
    (output/'index.html').write_text(document,encoding='utf8',newline='\n')
    report={'status':'LISTENING_MATERIALS_VERIFIED_HUMAN_REVIEW_PENDING','created_utc':datetime.now(timezone.utc).isoformat(),'script_sha256':sha(__file__),'source_review_sheet_sha256':sha(sheet),'cases':len(indexes),'unique_clips':len(written),'export_format':'WAV IEEE float32; exact sample roundtrip verified','sample_rate_hz':TARGET_SR,'duration_seconds':5,'mixture_identity_and_SNR_verified':True,'human_reviews_created':0,'source_hashes':input_hashes,'clips':written,'index_sha256':sha(output/'case_audio_index.csv'),'html_sha256':sha(output/'index.html')}
    (output/'metadata.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps({k:report[k] for k in ('status','cases','unique_clips','human_reviews_created')},indent=2),flush=True)
HTML=r'''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Audit pendengaran E5</title>
<style>body{font:17px system-ui;max-width:900px;margin:28px auto;padding:0 20px;line-height:1.5;background:#f6f8fa;color:#17212b}section{background:white;padding:22px;border-radius:12px;margin:18px 0}audio{width:100%}label{display:block;margin-top:14px}input,select,textarea,button{font:inherit;padding:9px;box-sizing:border-box}textarea{width:100%;min-height:80px}button{cursor:pointer;margin:8px 8px 0 0}small{color:#415268}#status{font-weight:bold}input{max-width:100%}</style>
<h1>Audit pendengaran E5</h1><p>120 kasus terpilih. Klip mengikuti preprocessing dan campuran E2. Label komputasional bukan pengamatan pendengar. Semua ulasan dimulai kosong.</p>
<section><label>Nama pendengar <input id="reviewer" autocomplete="name"></label><label>Kasus <select id="case"></select></label><p id="info"></p><p id="status"></p><button id="prev">Sebelumnya</button><button id="next">Berikutnya</button></section>
<section><h2>Audio pembanding</h2><p>Query pada kondisi eksperimen</p><audio id="query" controls preload="none"></audio><p>Query clean dengan segmen yang sama</p><audio id="clean" controls preload="none"></audio><p>Hasil retrieval Top-1</p><audio id="top" controls preload="none"></audio><p><small>Pengaturan volume pemutar tidak mengubah file. Jangan menyimpulkan spesies atau sumber gangguan hanya dari label komputasional.</small></p></section>
<section><h2>Catatan pendengar</h2><label>Vokalisasi pada query terdengar? <select id="qa"><option value="">Pilih setelah mendengar</option><option value="yes">Ya</option><option value="no">Tidak</option><option value="uncertain">Tidak pasti</option></select></label><label>Vokalisasi pada Top-1 terdengar? <select id="ta"><option value="">Pilih setelah mendengar</option><option value="yes">Ya</option><option value="no">Tidak</option><option value="uncertain">Tidak pasti</option></select></label><label>Pengamatan latar<textarea id="background"></textarea></label><label>Ketidakpastian / masalah segmen<textarea id="uncertainty"></textarea></label><label>Interpretasi pendengaran<textarea id="interpretation"></textarea></label><button id="save">Simpan sebagai sudah diulas</button><button id="follow">Tandai perlu tindak lanjut</button><button id="export">Unduh catatan JSON</button><p><small>Catatan disimpan lokal pada browser; unduh JSON sebagai bukti. File CSV penelitian tidak diubah oleh halaman ini. Catatan yang belum disimpan tidak dihitung selesai.</small></p></section>
<script>
const cases=__CASES__,key='e5-listening-__PACK__',el=id=>document.getElementById(id);let reviews={};try{reviews=JSON.parse(localStorage.getItem(key)||'{}')}catch(e){}let pos=0;cases.forEach((c,i)=>el('case').add(new Option(c.case_id+' · '+c.representation+' · '+c.condition,i)));
function show(){const c=cases[pos],r=reviews[c.case_id]||{};el('case').value=pos;el('info').textContent=c.representation+' | '+c.condition+' | '+c.failure_mode_computational+' | Query '+c.query_id+' → '+c.top1_recording_id;el('query').src=c.query_clip;el('clean').src=c.query_clean_clip;el('top').src=c.top1_clip;for(const [a,b] of [['qa','query_vocalisation_audible'],['ta','top1_vocalisation_audible'],['background','background_observation'],['uncertainty','uncertainty_notes'],['interpretation','auditory_interpretation']])el(a).value=r[b]||'';if(r.reviewer)el('reviewer').value=r.reviewer;el('status').textContent='Status kasus: '+(r.review_status||'pending')+' · Selesai '+Object.values(reviews).filter(x=>x.review_status==='reviewed').length+'/120';}
function save(status){if(!el('reviewer').value.trim()||!el('qa').value||!el('ta').value||!el('background').value.trim()||!el('interpretation').value.trim()){alert('Isi pendengar, pengamatan query/Top-1, latar, dan interpretasi terlebih dahulu.');return}const c=cases[pos];reviews[c.case_id]={case_id:c.case_id,source_row_sha256:c.source_row_sha256,review_status:status,reviewer:el('reviewer').value.trim(),reviewed_at:new Date().toISOString(),query_vocalisation_audible:el('qa').value,top1_vocalisation_audible:el('ta').value,background_observation:el('background').value,uncertainty_notes:el('uncertainty').value,auditory_interpretation:el('interpretation').value};try{localStorage.setItem(key,JSON.stringify(reviews))}catch(e){alert('Penyimpanan browser gagal; segera unduh JSON.')}show()}
el('case').onchange=()=>{pos=+el('case').value;show()};el('prev').onclick=()=>{pos=Math.max(0,pos-1);show()};el('next').onclick=()=>{pos=Math.min(cases.length-1,pos+1);show()};el('save').onclick=()=>save('reviewed');el('follow').onclick=()=>save('needs_follow_up');el('export').onclick=()=>{const data={schema:'e5_human_listening_review_v1',source_review_sheet_sha256:'__PACK__',exported_at:new Date().toISOString(),reviews:Object.values(reviews)},url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'})),a=document.createElement('a');a.href=url;a.download='E5_catatan_pendengaran.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)};show();
</script></html>'''
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True);build(p.parse_args().output_dir)
