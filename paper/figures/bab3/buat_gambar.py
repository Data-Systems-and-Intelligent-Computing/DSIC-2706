from pathlib import Path
import csv, json, collections
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none'})

def setup(w=8,h=10):
    fig,ax=plt.subplots(figsize=(w,h)); ax.set(xlim=(0,100),ylim=(0,100)); ax.axis('off'); fig.patch.set_facecolor('white'); return fig,ax
def box(ax,x,y,w,h,text,fs=11,rounded=False):
    b=FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.35,rounding_size=2' if rounded else 'square,pad=0.25',facecolor='white',edgecolor='#222222',linewidth=1.2)
    ax.add_patch(b); ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs,linespacing=1.4)
def arrow(ax,x1,y1,x2,y2):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=11,lw=1.1,color='#222222'))
def save(fig,name):
    fig.savefig(HERE/f'{name}.png',dpi=220,bbox_inches='tight',facecolor='white')
    fig.savefig(HERE/f'{name}.svg',bbox_inches='tight',facecolor='white')
    plt.close(fig)

with (ROOT/'data/manifests/dataset_split.csv').open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
with (HERE/'ne_50m_admin_0_countries.geojson').open(encoding='utf-8') as f: world=json.load(f)['features']
names=sorted(set(r['scientific_name'] for r in rows)); colors=plt.get_cmap('tab20').colors
fig,ax=plt.subplots(figsize=(15,8)); ax.set_facecolor('#f1f6f8')
for f in world:
    geo=f['geometry']; country=f['properties']['ADMIN']
    polys=geo['coordinates'] if geo['type']=='MultiPolygon' else [geo['coordinates']] if geo['type']=='Polygon' else []
    for poly in polys:
        ring=np.asarray(poly[0]);
        if len(ring)<3 or ring[:,0].max()<93 or ring[:,0].min()>144 or ring[:,1].max()<-13 or ring[:,1].min()>9: continue
        ax.add_patch(Polygon(ring,closed=True,facecolor='#e6e6e2',edgecolor='#8b8b85',linewidth=.38,zorder=1))
available=[r for r in rows if r['latitude'].strip() and r['longitude'].strip()]
pts=np.array([[float(r['longitude']),float(r['latitude'])] for r in available])
for i,name in enumerate(names):
    sel=np.array([r['scientific_name']==name for r in available])
    ax.scatter(pts[sel,0],pts[sel,1],s=19,c=[colors[i]],edgecolor='#222222',linewidth=.2,alpha=.85,zorder=3)
handles=[Line2D([0],[0],marker='o',linestyle='',markerfacecolor=colors[i],markeredgecolor='#333',markersize=6,label=f'{i+1:02}. {n}') for i,n in enumerate(names)]
ax.legend(handles=handles,title='Label spesies (20)',loc='center left',bbox_to_anchor=(1.02,.5),fontsize=9,title_fontsize=10,frameon=False)
ax.set(xlim=(94,142.5),ylim=(-12.5,8),xlabel='Bujur',ylabel='Lintang')
ax.set_aspect('equal',adjustable='box'); ax.grid(color='#cccccc',lw=.4,zorder=0)
unique_coords=len(set((r['latitude'],r['longitude']) for r in available))
fig.text(.12,.035,f"Lokasi rekaman, bukan persebaran seluruh spesies. {len(available)} dari {len(rows)} rekaman berkoordinat; {unique_coords} pasangan koordinat unik.",fontsize=10)
fig.text(.12,.012,'Sumber: metadata Xeno-Canto dalam dataset_split.csv; batas peta Natural Earth 1:50m.',fontsize=9)
fig.savefig(HERE/'04_peta_lokasi_rekaman.png',dpi=220,bbox_inches='tight',facecolor='white')
fig.savefig(HERE/'04_peta_lokasi_rekaman.svg',bbox_inches='tight',facecolor='white');plt.close(fig)
print('Rekaman:',len(rows),'koordinat:',len(available),'hilang:',len(rows)-len(available),'koordinat unik:',unique_coords)
