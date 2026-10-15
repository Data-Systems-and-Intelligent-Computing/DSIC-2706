"""Build corrected Figures 6 and 8 from the active design and manifest.
Only the new requested output directory is written; legacy figures stay intact.
"""
from pathlib import Path
import argparse,hashlib,json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
ROOT=Path(__file__).resolve().parents[1]

def main(output):
    output=Path(output).resolve()
    if output.parent!=(ROOT/'paper/figures').resolve():raise ValueError('Use a new child of paper/figures')
    if output.exists():raise FileExistsError(output)
    manifest=ROOT/'data/manifests/dataset_split.csv'
    split=pd.read_csv(manifest)
    gallery=split[split.split_role.eq('gallery')].groupby('species_key').size().rename('gallery_count')
    query=split[split.split_role.eq('query_clean')].groupby('species_key').size().rename('query_count')
    table=pd.concat([gallery,query],axis=1).reset_index()
    table['recall10_ceiling']=np.minimum(1,10/table.gallery_count)
    ceiling=np.average(table.recall10_ceiling,weights=table.query_count)
    e1=pd.read_csv(ROOT/'results/tables/10_e1_clean_retrieval_summary.csv')
    output.mkdir(parents=True,exist_ok=False)
    table.to_csv(output/'recall10_ceiling_by_species.csv',index=False)
    fig,ax=plt.subplots(figsize=(13,5.7));ax.set_xlim(0,13);ax.set_ylim(0,5.7);ax.axis('off')
    boxes=[(.3,2.1,3.5,2.1,'Rekaman burung Xeno-Canto\n20 spesies Indonesia\n311 query yang sama\nGallery tetap: 673 rekaman','#edf3fa'),(4.5,3.1,3.7,1.6,'E2: noise dari pool ITERA\n1 segmen per query\nSNR +20, +10, 0, -5 dB','#fff4df'),(4.5,.7,3.7,1.8,'E4: noise dari 5 lokasi\n4 ulangan pemilihan segmen\nSNR +20, +10, 0, -5 dB\n6 kategori AudioMoth dipasangkan','#e5f4ec'),(9,1.9,3.6,2.4,'Ekstraksi R0-R3 beku\nCosine similarity\nRanking dan AP@10 per query\n\nE4: sensitivitas profil lokasi\nAyunan absolut dan retensi','#eef1f5')]
    for x,y,w,h,t,color in boxes:
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=.08',facecolor=color,edgecolor='#526579',linewidth=1.3));ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=11)
    for a,b in [((3.9,3.5),(4.35,3.9)),((3.9,2.5),(4.35,1.7)),((8.35,3.9),(8.85,3.5)),((8.35,1.7),(8.85,2.5))]:ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':'#526579','lw':1.5})
    ax.text(6.5,5.25,'Gambar 6. E2 dan E4 memakai pencampuran aditif terkontrol',ha='center',fontsize=15,weight='bold')
    ax.text(6.5,.12,'Lima lokasi: Kebun Raya, Embung F, Gedung F, Masjid At-Tanwir, sekitar GKU 1.\nDesain ini tidak mengukur burung in-situ, propagasi jarak, atau reverberasi.',ha='center',fontsize=10,color='#364152')
    fig.tight_layout();fig.savefig(output/'fig06_e4_noise_profiles.png',dpi=180);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(13,5.8))
    axes[0].bar(e1.representation,e1['Recall@10'],color=['#64748b','#d95f02','#16856e','#aa6699'])
    axes[0].axhline(ceiling,color='#b45309',linestyle='--',label=f'Batas rata-rata berbobot query: {ceiling:.4f}')
    for i,val in enumerate(e1['Recall@10']):axes[0].text(i,val+.008,f'{val:.4f}',ha='center')
    axes[0].set_ylim(0,.42);axes[0].set_ylabel('Rata-rata Recall@10 (311 query)');axes[0].set_title('E1 pada gallery aktif: 673 rekaman');axes[0].legend(fontsize=9,loc='upper left');axes[0].grid(axis='y',alpha=.2)
    ordered=table.sort_values('recall10_ceiling')
    axes[1].barh(ordered.species_key,ordered.recall10_ceiling,color='#93b7ce');axes[1].set_xlabel('Batas per spesies: min(1, 10 / jumlah gallery relevan)');axes[1].set_xlim(0,.73);axes[1].set_title('15-100 gallery relevan per spesies');axes[1].tick_params(axis='y',labelsize=8)
    fig.suptitle('Gambar 8. Batas Recall@10 membatasi nilai maksimum; kualitas ranking menentukan nilai aktual',fontsize=12,weight='bold')
    fig.tight_layout();fig.savefig(output/'fig08_recall_ceiling_active.png',dpi=180);plt.close(fig)
    sources=[manifest,ROOT/'results/tables/10_e1_clean_retrieval_summary.csv',ROOT/'results/reproductions/E4_5sites_20261011T213404_350219Z/run_identity.json']
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    info={'script_sha256':digest(Path(__file__)),'sources_sha256':{p.relative_to(ROOT).as_posix():digest(p) for p in sources},'gallery_count':int(gallery.sum()),'query_count':int(query.sum()),'species_mean_ceiling':table.recall10_ceiling.mean(),'query_weighted_mean_ceiling':ceiling,'outputs_sha256':{p.name:digest(p) for p in output.iterdir() if p.is_file()}}
    (output/'metadata.json').write_text(json.dumps(info,indent=2)+'\n',encoding='utf8')
    print(json.dumps(info,indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,required=True)
    main(parser.parse_args().output_dir)
