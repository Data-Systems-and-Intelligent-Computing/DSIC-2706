"""Draw the missing complete research workflow; never reads or changes audio.

Run from any directory with matplotlib installed. --overwrite only replaces
this builder's four named outputs in its own folder.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUTPUTS = ['alur_penelitian_lengkap.png', 'alur_penelitian_lengkap.svg',
           'alur_penelitian_lengkap.mmd', 'metadata_diagram.json']


def main(overwrite=False):
    if not overwrite and any((HERE / p).exists() for p in OUTPUTS):
        raise FileExistsError('Output exists; review it before using --overwrite')
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.fonttype': 'none'})
    fig, ax = plt.subplots(figsize=(11.7, 18), dpi=110)
    fig.subplots_adjust(left=.015, right=.985, top=.985, bottom=.015)
    ax.set_xlim(0, 120); ax.set_ylim(180, 0); ax.axis('off')
    ink = '#183448'; border = '#506577'
    palette = {'plan': '#EAF1F8', 'data': '#EFF6FA', 'process': '#EAF5EF',
               'experiment': '#FFF6E6', 'analysis': '#F0EDF9', 'write': '#F2F3F5'}
    nodes = {}; edges = []; text_checks = []

    def node(key, x, y, w, h, title, lines=(), kind='process', size=9.3, rounded=False):
        size *= 1.15
        patch = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0.0,rounding_size={h/2 if rounded else .9}',
                               linewidth=1.1, edgecolor=border, facecolor=palette[kind], zorder=3)
        ax.add_patch(patch)
        title_obj = ax.text(x+w/2, y+2.0, title, ha='center', va='top', fontsize=size+.6,
                            fontweight='bold', color=ink, zorder=4)
        text_checks.append((key, title_obj, patch))
        if lines:
            body = ax.text(x+w/2, y+5.0, '\n'.join(lines), ha='center', va='top', fontsize=size,
                           linespacing=1.22, color=ink, zorder=4)
            text_checks.append((key, body, patch))
        nodes[key] = {'x': x, 'y': y, 'w': w, 'h': h, 'title': title, 'lines': list(lines)}

    def edge(a, b, points=None, dashed=False):
        start = nodes[a]; end = nodes[b]
        if points is None:
            points = [(start['x']+start['w']/2, start['y']+start['h']),
                      (end['x']+end['w']/2, end['y'])]
        for i in range(len(points)-1):
            arrow = FancyArrowPatch(points[i], points[i+1], arrowstyle='-|>' if i==len(points)-2 else '-',
                                    mutation_scale=9, linewidth=1.05, linestyle='--' if dashed else '-',
                                    color=border, shrinkA=0, shrinkB=2 if i==len(points)-2 else 0, zorder=1)
            ax.add_patch(arrow)
        edges.append((a,b,dashed))

    ax.text(60, 1, 'Alur penelitian dari perumusan masalah sampai pelaporan',
            ha='center', va='top', fontsize=15, fontweight='bold', color=ink)
    node('start', 47, 7, 26, 6, 'MULAI', kind='plan', rounded=True)
    node('problem', 9, 17, 102, 10, '1. Studi pustaka dan perumusan penelitian',
         ['Masalah umum → kebutuhan retrieval burung pada derau ITERA → RQ, tujuan, dan batas penelitian.',
          'Tetapkan rancangan; dokumentasikan perubahan H3/H4 setelah hasil sebagai eksploratif.'], kind='plan', size=9.2)
    node('target', 3, 32, 35, 12, '2a. Audio burung target',
         ['Xeno-Canto Indonesia', '20 spesies; 1.216 rekaman'], kind='data')
    node('noise', 42.5, 32, 35, 12, '2b. Derau fisik ITERA',
         ['AudioMoth; 1.799 berkas', '5 lokasi; 6 kategori konfigurasi'], kind='data')
    node('unknown', 82, 32, 35, 12, '2c. Kontrol unknown',
         ['272 burung non-target', '+ 271 derau khusus dari bank ITERA'], kind='data')
    node('audit', 9, 49, 102, 10, '3. Audit sumber dan pembagian data',
         ['Periksa metadata, SHA-256, keterbacaan audio, identitas rekaman, dan asal derau.',
          'Pisahkan galeri/kueri/kalibrasi target tanpa irisan rekaman, path, atau perekam.'], size=9.2)
    node('split_target', 3, 64, 35, 12, '4a. Target',
         ['Galeri 673; kueri 311', 'Kalibrasi known 232'], kind='data')
    node('split_noise', 42.5, 64, 35, 12, '4b. Bank derau',
         ['Pool pencampuran 1.528', 'Cadangan unknown 271'], kind='data')
    node('split_unknown', 82, 64, 35, 12, '4c. Unknown: 543',
         ['Kalibrasi 233; uji 310', 'Terpisah dari kelas target galeri'], kind='data')
    node('preprocess', 9, 81, 102, 11, '5. Standardisasi audio dan audit praproses E0',
         ['Mono; 32 kHz; 5 detik; jendela energi tertinggi atau padding; normalisasi RMS.',
          'E0 memeriksa 100 rekaman serta probe representasi. R3 menggunakan ID, bukan waveform.'], size=9.2)
    node('embedding', 9, 97, 102, 12, '6. Representasi beku dan galeri referensi',
         ['R0: MFCC mean + std (40-d) | R1: PANNs CNN14 (2.048-d) | R2: BirdNET v2.4 (1.024-d).',
          'R3: kontrol ID (40-d). R2 memakai adapter 48 kHz dan jendela 3 detik.',
          'Galeri 673 tetap; normalisasi L2 dan cosine similarity dalam ruang representasi masing-masing.'], size=9.1)
    node('e1', 2, 115, 27, 17, '7a. E1: acuan clean',
         ['311 kueri; galeri tetap', 'Ranking → mAP@10, Top-1,', 'Recall@10, P@10, MRR', 'Acuan untuk retensi'], kind='experiment', size=8.8)
    node('e2', 31.5, 115, 27, 17, '7b. E2: derau terkontrol',
         ['311 kueri + noise pool', 'SNR +20, +10, 0, −5 dB', 'Ranking dengan galeri tetap', 'Skor absolut dan retensi'], kind='experiment', size=8.8)
    node('e3', 61, 115, 27, 17, '7c. E3: ambang beku',
         ['Kalibrasi clean: 232 known', '+ 233 unknown → J → τ beku', 'Uji: 311 known + 310 unknown', 'Clean dan 4 SNR; recall/FPR'], kind='experiment', size=8.7)
    node('e4', 90.5, 115, 27, 17, '7d. E4: lima lokasi',
         ['311 kueri × 5 lokasi', '× 4 SNR × 4 ulangan', '24.880 evaluasi / representasi', 'Baca hasil E4 yang tersimpan'], kind='experiment', size=8.7)
    node('stats', 2, 139, 38, 14, '8a. Analisis statistik',
         ['E1/E2: perbandingan berpasangan.', 'H3 dari E4: ayunan absolut/relatif;',
          '10.000 bootstrap dan subset lokasi.', 'H3/H4 reformulasi: eksploratif.'], kind='analysis', size=8.9)
    node('e5', 44, 139, 74, 14, '8b. E5: diagnosis dan audit pendengaran',
         ['Diagnosis dari E2/E3 dan metadata E4 yang tersedia.', '120 kasus pilihan E2: dengarkan segmen kueri dan Top-1;',
          'catat pendengar, tanggal, pengamatan, dan ketidakpastian.', 'Kolom E4 yang tidak tersedia tetap ditandai tidak tersedia.'], kind='analysis', size=9.1)
    node('synthesis', 9, 158, 102, 10, '9. Sintesis, pemeriksaan integritas, dan reproduksi yang diizinkan',
         ['Hubungkan hasil dengan RQ/H; periksa sumber tabel/gambar serta batas klaim.',
          'E4 historis tidak dijalankan ulang; campuran ini belum menguji burung target in-situ.'], size=9.2)
    node('write', 9, 172, 102, 6, '10. Penulisan BAB 1–5, bimbingan, kesimpulan/saran, dan arsip akhir',
         kind='write', size=9.0, rounded=True)

    edge('start','problem')
    for dest in ('target','noise','unknown'):
        edge('problem',dest,[(60,27),(60,29),(nodes[dest]['x']+17.5,29),(nodes[dest]['x']+17.5,32)])
        edge(dest,'audit',[(nodes[dest]['x']+17.5,44),(nodes[dest]['x']+17.5,46),(60,46),(60,49)])
    for dest in ('split_target','split_noise','split_unknown'):
        center=nodes[dest]['x']+17.5
        edge('audit',dest,[(60,59),(60,61),(center,61),(center,64)])
        edge(dest,'preprocess',[(center,76),(center,78),(60,78),(60,81)])
    edge('preprocess','embedding')
    for dest in ('e1','e2','e3','e4'):
        center=nodes[dest]['x']+13.5
        edge('embedding',dest,[(60,109),(60,112),(center,112),(center,115)])
    for src in ('e1','e2','e4'):
        center=nodes[src]['x']+13.5
        edge(src,'stats',[(center,132),(center,134),(21,134),(21,139)])
    for src in ('e2','e3','e4'):
        center=nodes[src]['x']+13.5
        edge(src,'e5',[(center,132),(center,136),(81,136),(81,139)])
    for src in ('stats','e5'):
        center=nodes[src]['x']+nodes[src]['w']/2
        edge(src,'synthesis',[(center,153),(center,155),(60,155),(60,158)])
    edge('synthesis','write')

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for key,text,patch in text_checks:
        tb=text.get_window_extent(renderer); pb=patch.get_window_extent(renderer)
        if tb.x0 < pb.x0+2 or tb.x1 > pb.x1-2 or tb.y0 < pb.y0+2 or tb.y1 > pb.y1-2:
            raise ValueError(f'Text does not fit node {key}: {text.get_text()}')
    fig.savefig(HERE/OUTPUTS[0], dpi=300, facecolor='white')
    fig.savefig(HERE/OUTPUTS[1], facecolor='white')
    plt.close(fig)
    svg = HERE / OUTPUTS[1]
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n',
                   encoding='utf-8', newline='\n')
    mmd=['flowchart TB']
    for key,n in nodes.items():
        label='<br/>'.join([n['title'],*n['lines']]).replace('"',"'")
        mmd.append(f'    {key}["{label}"]')
    for a,b,dashed in edges:
        mmd.append(f'    {a} {"-.->" if dashed else "-->"} {b}')
    (HERE/OUTPUTS[2]).write_text('\n'.join(mmd)+'\n',encoding='utf-8',newline='\n')
    sources=['data/manifests/dataset_split.csv','data/manifests/unknown_open_set_manifest.csv',
             'data/manifests/itera_noise_manifest.csv','src/preprocess.py','src/mfcc.py','src/embeddings.py',
             'src/retrieve.py','src/calibrate_threshold.py','scripts/run_e5_diagnostics.py',
             'docs/research/hypotheses.md','results/reproductions/E4_5sites_20261011T213404_350219Z/run_identity.json',
             'Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/ringkasan_pendengaran.json']
    meta={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'New protocol illustration only; no experiment execution',
          'reason_new':'Existing local flowcharts are partial or contain historical gallery/threshold/soundscape assumptions',
          'outputs':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in OUTPUTS[:3]},
          'sources_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources},
          'generator_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'interpretation':'Arrows show research dependencies. Review/write is a subsequent phase, not a claim of approved chapters. R3 is an ID control; E4 is stored historical output.',
          'text_fit_checks':len(text_checks),'text_fit_passed':True}
    (HERE/OUTPUTS[3]).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print('Created one complete workflow as PNG, SVG and editable Mermaid; all node text fits.')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--overwrite',action='store_true')
    main(parser.parse_args().overwrite)
