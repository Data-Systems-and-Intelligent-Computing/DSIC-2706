"""Gambar acuan E0–E5 untuk digambar ulang di Draw.io."""

from dataclasses import dataclass
from pathlib import Path
import textwrap

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle


OUTPUT = Path(__file__).resolve().parent
INK = '#18313F'
LINE = '#3B5363'


@dataclass
class Node:
    key: str
    title: str
    detail: str = ''
    shape: str = 'process'
    x: float | None = None
    width: float | None = None


@dataclass
class Edge:
    start: str
    end: str
    label: str = ''
    loop: bool = False


def data(key, title, detail='', **kwargs):
    return Node(key, title, detail, 'data', **kwargs)


def decision(key, title, **kwargs):
    return Node(key, title, shape='decision', **kwargs)


def wrap(text, columns):
    return '\n'.join(
        '\n'.join(textwrap.wrap(line, width=columns, break_long_words=False,
                                break_on_hyphens=False))
        for line in text.split('\n')
    )


def render(filename, code, title, rows, edges, note='', gallery_inputs=()):
    placed = {}
    y = 23
    for index, row in enumerate(rows):
        count = len(row)
        gap = 8 if count == 2 else 5
        width = 104 if count == 1 else 140 / count - gap
        height = 0
        for col, node in enumerate(row):
            w = node.width or (51 if node.shape == 'decision' and count == 1 else width)
            x = node.x if node.x is not None else 5 + (col + .5) * 140 / count
            factor = 1.48 if node.shape == 'decision' else 1
            heading = wrap(node.title, max(12, int((w - 5) / (factor * 1.12))))
            detail = wrap(node.detail, max(14, int((w - 6) / 1.04)))
            head_lines = heading.count('\n') + 1
            detail_lines = detail.count('\n') + 1 if detail else 0
            h = 4.3 + 2.75 * head_lines + 2.4 * detail_lines
            if node.shape == 'decision':
                h = max(16, h + 4)
            placed[node.key] = dict(node=node, x=x, width=w, height=h,
                                    heading=heading, detail=detail, row=index)
            height = max(height, h)
        for node in row:
            placed[node.key]['y'] = y + height / 2
        y += height + 9
    total = y + (10 if note else 0)
    fig = plt.figure(figsize=(12, total / 12.5), facecolor='white')
    ax = fig.add_axes((.015, .01, .97, .98), xlim=(0, 150), ylim=(total, 0))
    ax.set_axis_off()
    ax.text(75, 5, code, ha='center', va='center', fontsize=12, color=LINE)
    ax.text(75, 12, title, ha='center', va='center', fontsize=19,
            fontweight='bold', color=INK)

    def arrow(points):
        if len(points) > 2:
            ax.plot(*zip(*points[:-1]), color=LINE, lw=1.25, zorder=1)
        ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle='-|>',
                                    color=LINE, linewidth=1.25, mutation_scale=12,
                                    shrinkA=0, shrinkB=.2, zorder=1))

    for edge in edges:
        start, end = placed[edge.start], placed[edge.end]
        x1, y1 = start['x'], start['y'] + start['height'] / 2
        x2, y2 = end['x'], end['y'] - end['height'] / 2
        if edge.loop:
            x1 = start['x'] - start['width'] / 2
            x2 = end['x'] - end['width'] / 2
            points = [(x1, start['y']), (2.5, start['y']),
                      (2.5, end['y']), (x2, end['y'])]
            label_x, label_y = 3, (start['y'] + end['y']) / 2
        elif end['row'] - start['row'] > 1:
            rail = 147.5 if start['x'] > 75 else 2.5
            points = [(x1, y1), (x1, y1 + 2), (rail, y1 + 2),
                      (rail, y2 - 3), (x2, y2 - 3), (x2, y2)]
            label_x, label_y = rail, (y1 + y2) / 2
        elif abs(x1 - x2) < .01:
            points = [(x1, y1), (x2, y2)]
            label_x, label_y = x1 + 1, (y1 + y2) / 2
        else:
            mid = (y1 + y2) / 2
            points = [(x1, y1), (x1, mid), (x2, mid), (x2, y2)]
            label_x, label_y = x2, mid - 1.7
        arrow(points)
        if edge.label:
            ax.text(label_x, label_y, edge.label, fontsize=9, color=INK,
                    ha='left' if edge.loop else 'center', va='center',
                    bbox=dict(facecolor='white', edgecolor='none', pad=.8), zorder=5)

    text_bounds = []
    for item in placed.values():
        node = item['node']
        x, y, w, h = item['x'], item['y'], item['width'], item['height']
        left, top = x - w / 2, y - h / 2
        style = dict(facecolor='white', edgecolor=LINE, linewidth=1.25, zorder=2)
        if node.shape == 'data':
            style['facecolor'] = '#EDF4FB'
            patch = Polygon([(left + 2, top), (left + w, top),
                             (left + w - 2, top + h), (left, top + h)], **style)
        elif node.shape == 'decision':
            style['facecolor'] = '#EEF6F1'
            patch = Polygon([(x, top), (left + w, y), (x, top + h), (left, y)], **style)
        else:
            patch = Rectangle((left, top), w, h, **style)
        ax.add_patch(patch)
        head_lines = item['heading'].count('\n') + 1
        title_y = y if not item['detail'] else top + 2.1 + 1.375 * head_lines
        fontsize = 11 if w < 36 else 12
        title_artist = ax.text(x, title_y, item['heading'], ha='center', va='center', fontsize=fontsize,
                               color=INK, fontweight='bold', linespacing=1.2, zorder=3)
        text_bounds.append((title_artist, left + 2, left + w - 2))
        if item['detail']:
            detail_lines = item['detail'].count('\n') + 1
            detail_y = top + 3.3 + 2.75 * head_lines + 1.2 * detail_lines
            detail_artist = ax.text(x, detail_y, item['detail'], ha='center', va='center',
                                    fontsize=10 if w < 36 else 10.5, color=INK,
                                    linespacing=1.2, zorder=3)
            text_bounds.append((detail_artist, left + 2, left + w - 2))

    for key, side in gallery_inputs:
        item = placed[key]
        direction = -1 if side == 'left' else 1
        border = item['x'] + direction * item['width'] / 2
        x = border + direction * 4
        ax.add_patch(Circle((x, item['y']), 1.8, facecolor='#EDF4FB',
                            edgecolor=LINE, linewidth=1.1, zorder=3))
        ax.text(x, item['y'], 'G', fontsize=10, ha='center', va='center',
                color=INK, fontweight='bold', zorder=4)
        arrow([(x - direction * 1.8, item['y']), (border, item['y'])])
    if note:
        ax.text(75, total - 6.5, wrap(note, 125), ha='center', va='center',
                fontsize=9.5, color=LINE, linespacing=1.2)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for artist, left, right in text_bounds:
        allowed_width = ax.transData.transform((right, 0))[0] - ax.transData.transform((left, 0))[0]
        actual_width = artist.get_window_extent(renderer).width
        if actual_width > allowed_width:
            artist.set_fontsize(artist.get_fontsize() * allowed_width / actual_width * .98)
    fig.savefig(OUTPUT / f'{filename}.png', dpi=180, facecolor='white')
    plt.close(fig)


def chain(*names):
    return [Edge(a, b) for a, b in zip(names, names[1:])]


render('e0_prapemrosesan', 'E0', 'Prapemrosesan dan Audit Audio', [
    [data('audio', 'Rekaman sesuai pembagian data', 'Galeri, kueri target, kalibrasi, dan kontrol')],
    [Node('load', 'Baca dan seragamkan audio', 'Satu kanal (mono) dan laju pencuplikan 32 kHz')],
    [decision('duration', 'Berapa durasi rekaman?')],
    [Node('short', 'Kurang dari 5 detik', 'Tambahkan sampel nol di akhir'),
     Node('equal', 'Tepat 5 detik', 'Gunakan segmen yang tersedia'),
     Node('long', 'Lebih dari 5 detik', 'Geser jendela 5 detik setiap 1,25 detik; pilih RMS tertinggi')],
    [decision('rms', 'RMS lebih besar dari 10⁻⁶?')],
    [Node('scale', 'Sesuaikan RMS', 'Kalikan amplitudo menuju RMS 0,05'),
     Node('keep', 'Gunakan amplitudo yang tersedia')],
    [Node('clip', 'Batasi amplitudo', 'Rentang −1 sampai 1')],
    [data('ready', 'Audio siap untuk tahap berikutnya', 'Panjang 5 detik = 160.000 sampel')],
    [Node('audit', 'Audit 100 rekaman target',
          '55 galeri, 26 kueri uji, dan 19 kalibrasi; acak dengan seed 20261012 + indeks kelompok')],
    [data('report', 'Catatan audit prapemrosesan',
          'Dekode, format, laju pencuplikan, kanal, durasi, awal segmen, panjang keluaran, dan nilai berhingga')],
], chain('audio', 'load', 'duration') + [
    Edge('duration', key) for key in ('short', 'equal', 'long')
] + [Edge(key, 'rms') for key in ('short', 'equal', 'long')] + [
    Edge('rms', 'scale', 'Ya'), Edge('rms', 'keep', 'Tidak'),
    Edge('scale', 'clip'), Edge('keep', 'clip')
] + chain('clip', 'ready', 'audit', 'report'))

render('e1_pencarian_acuan', 'E1', 'Pencarian Kemiripan pada Kondisi Acuan', [
    [data('gal', '673 rekaman galeri setelah E0', 'Tanpa derau tambahan'),
     data('query', '311 kueri target setelah E0', 'Tanpa derau tambahan')],
    [Node('prepare', 'Siapkan audio dan ID tiap rekaman', 'Bentuk representasi galeri dan kueri dengan aturan yang sama')],
    [Node('mfcc', 'MFCC', '20 koefisien; FFT 1.024; geser 512 sampel; rerata + simpangan baku → 40 nilai'),
     Node('panns', 'PANNs CNN14', 'Bobot tetap; masukan 32 kHz → 2.048 nilai'),
     Node('birdnet', 'BirdNET v2.4', '48 kHz; jendela 3 detik, geser 1 detik; rerata → 1.024 nilai'),
     Node('random', 'Kontrol acak', 'ID rekaman dan seed 42 → 40 nilai')],
    [Node('l2', 'Normalisasi L2', 'Lakukan untuk setiap representasi')],
    [data('gfeatures', 'Fitur galeri tetap', 'Referensi yang sama dipakai pada E1, E2, E3, dan E4'),
     data('qfeatures', 'Fitur kueri acuan', 'Simpan urutan ID dan label spesies')],
    [Node('cosine', 'Hitung kemiripan kosinus', 'Bandingkan setiap kueri dengan 673 rekaman galeri pada representasi yang sama')],
    [Node('rank', 'Urutkan dan nilai hasil', 'Skor tertinggi di urutan pertama; relevan jika label spesies sama dengan kueri')],
    [data('metrics', 'Kinerja acuan', 'mAP@10, P@10, recall@10, MRR, dan ketepatan Top-1'),
     data('scores', 'Skor tertinggi target', 'Masukan untuk uji ambang E3'),
     data('top1', 'Top-1 dan skor', 'Masukan untuk diagnosis E5')],
], [Edge('gal', 'prepare'), Edge('query', 'prepare')] + [
    Edge('prepare', key) for key in ('mfcc', 'panns', 'birdnet', 'random')
] + [Edge(key, 'l2') for key in ('mfcc', 'panns', 'birdnet', 'random')] + [
    Edge('l2', 'gfeatures'), Edge('l2', 'qfeatures'), Edge('gfeatures', 'cosine'),
    Edge('qfeatures', 'cosine'), Edge('cosine', 'rank')
] + [Edge('rank', key) for key in ('metrics', 'scores', 'top1')],
       note='Kontrol acak dibentuk dari ID rekaman. Model pralatih memakai bobot tetap selama ekstraksi.')

render('e2_snr_terkontrol', 'E2', 'Pengujian Derau pada SNR Terkontrol', [
    [data('query', '311 kueri target setelah E0'),
     data('noise', 'Bank derau campuran', '1.528 berkas; kontrol derau E3 sudah disisihkan')],
    [Node('pair', 'Pilih segmen derau untuk setiap kueri',
          'Ambil 5 detik; seed 20261012 + indeks kueri; ulangi derau yang lebih pendek hingga cukup')],
    [decision('energy', 'RMS derau ≥ 10⁻⁴?')],
    [Node('normalize', 'Normalisasi segmen derau',
          'Target RMS 0,05; pertahankan pasangan kueri–derau lintas SNR dan representasi')],
    [Node('s20', 'SNR +20 dB'), Node('s10', 'SNR +10 dB'),
     Node('s0', 'SNR 0 dB'), Node('sm5', 'SNR −5 dB')],
    [Node('mix', 'Sesuaikan daya derau lalu campurkan', 'Tambahkan derau yang sudah diskalakan ke kueri')],
    [Node('peak', 'Sesuaikan puncak dan catat campuran',
          'Jika puncak > 1, skalakan seluruh campuran; simpan ID derau, awal segmen, seed, dan SNR aktual')],
    [Node('features', 'Bentuk vektor kueri campuran', 'MFCC, PANNs, BirdNET, dan kontrol acak; normalisasi L2'),
     data('gallery', 'Fitur galeri tetap dari E1', '673 rekaman per representasi')],
    [Node('retrieve', 'Hitung kosinus dan urutkan galeri', 'Gunakan label spesies untuk menilai relevansi hasil')],
    [Node('metric', 'Hitung kualitas tiap SNR', 'mAP@10 dan metrik pendukung'),
     data('scores', 'Skor tertinggi ke E3', 'Untuk keputusan penerimaan target'),
     data('top1', 'Top-1 dan skor ke E5', 'Untuk diagnosis kegagalan')],
    [data('retention', 'Bandingkan dengan acuan E1',
          'Perubahan = mAP berderau − mAP acuan; retensi = mAP berderau ÷ mAP acuan')],
], [Edge('query', 'pair'), Edge('noise', 'pair'), Edge('pair', 'energy'),
    Edge('energy', 'pair', 'Tidak · pilih ulang', loop=True),
    Edge('energy', 'normalize', 'Ya')] + [
    Edge('normalize', key) for key in ('s20', 's10', 's0', 'sm5')
] + [Edge(key, 'mix') for key in ('s20', 's10', 's0', 'sm5')] + chain('mix', 'peak', 'features', 'retrieve') + [
    Edge('gallery', 'retrieve')
] + [Edge('retrieve', key) for key in ('metric', 'scores', 'top1')] + [Edge('metric', 'retention')],
       note='Pemilihan derau dicoba maksimal 10 kali. Jika seluruh percobaan gagal, kode menghentikan pencampuran.')

render('e3_ambang', 'E3', 'Kalibrasi dan Pengujian Ambang Tetap', [
    [data('cal', 'Data kalibrasi setelah E0', '232 target + 233 kontrol; tanpa derau tambahan'),
     data('test', '310 kueri kontrol uji setelah E0', '155 burung non-target + 155 derau lingkungan')],
    [Node('cal_features', 'Ekstraksi fitur kalibrasi dan L2', 'Lakukan untuk setiap representasi'),
     Node('conditions', 'Siapkan kondisi kontrol uji', 'Acuan serta SNR +20, +10, 0, −5 dB; gunakan bank derau campuran')],
    [Node('cal_scores', 'Ambil skor kalibrasi tertinggi', 'Kemiripan kosinus terhadap galeri tetap'),
     Node('test_features', 'Ekstraksi fitur kontrol uji dan L2', 'Lakukan untuk setiap kondisi dan representasi')],
    [Node('roc', 'Susun ROC dari skor kalibrasi', 'Status target dan kontrol diketahui'),
     Node('control_scores', 'Ambil skor kontrol uji tertinggi', 'Kemiripan kosinus terhadap galeri tetap')],
    [Node('filter', 'Saring kandidat ambang', 'Nilai berhingga pada rentang 0,01 < ambang < 0,9999'),
     data('target_scores', 'Skor tertinggi target dari E1–E2', '311 kueri; acuan dan empat SNR')],
    [Node('select', 'Pilih kandidat dengan Youden tertinggi', 'J = penerimaan target − penerimaan keliru kontrol'),
     Node('combine', 'Gabungkan skor target dan kontrol uji', '311 target + 310 kontrol pada tiap kondisi')],
    [data('tau', 'Tetapkan satu ambang per representasi', 'Gunakan ambang yang sama untuk semua kondisi uji'),
     Node('test_ready', 'Siapkan skor untuk tiap kondisi', 'Bandingkan setiap skor tertinggi dengan ambang representasinya')],
    [decision('accept', 'Skor ≥ ambang tetap?', x=110, width=57)],
    [Node('yes', 'Terima kueri', x=91, width=32),
     Node('no', 'Tolak kueri', x=129, width=32)],
    [data('rates', 'Hitung penerimaan tiap kondisi',
          'Proporsi target diterima dan kontrol keliru diterima; bandingkan dengan kondisi acuan', x=110, width=65)],
    [data('decisions', 'Kirim keputusan penerimaan ke E5',
          'ID kueri, representasi, kondisi, ambang, skor, dan diterima/ditolak', x=110, width=65)],
], chain('cal', 'cal_features', 'cal_scores', 'roc', 'filter', 'select', 'tau') +
   chain('test', 'conditions', 'test_features', 'control_scores') + [
    Edge('control_scores', 'combine'), Edge('target_scores', 'combine'),
    Edge('combine', 'test_ready'), Edge('tau', 'accept'), Edge('test_ready', 'accept'),
    Edge('accept', 'yes', 'Ya'), Edge('accept', 'no', 'Tidak'),
    Edge('yes', 'rates'), Edge('no', 'rates'), Edge('rates', 'decisions')],
       gallery_inputs=(('cal_scores', 'left'), ('control_scores', 'left')),
       note='G = fitur galeri tetap dari E1. Jika kandidat ambang kosong, kode menyediakan persentil ke-25 skor target kalibrasi sebagai aturan cadangan.')

render('e4_profil_lokasi', 'E4', 'Perbandingan Kinerja pada Lima Lokasi', [
    [data('query', '311 kueri target yang sama setelah E0'),
     data('noise', 'Bank derau campuran', '1.528 berkas; kontrol E3 disisihkan')],
    [Node('sites', 'Kelompokkan derau menurut lokasi',
          'Kebun Raya, Embung F, Gedung F, Masjid At-Tanwir, dan Sekitar GKU 1')],
    [Node('draw', 'Pilih derau untuk setiap kueri dan lokasi',
          'Empat ulangan; seed = 5000 + 100000 × indeks ulangan + indeks kueri')],
    [Node('snr', 'Bentuk empat kondisi SNR',
          '+20, +10, 0, −5 dB; segmen tetap lintas SNR dan representasi dalam lokasi dan ulangan yang sama')],
    [Node('mix', 'Campurkan dan catat identitas derau',
          'Atur daya derau; sesuaikan puncak bila perlu; catat segmen dan SNR aktual')],
    [Node('features', 'Ekstraksi fitur kueri dan L2', 'MFCC, PANNs, BirdNET, dan kontrol acak'),
     data('gallery', 'Fitur galeri tetap dari E1', '673 rekaman per representasi')],
    [Node('retrieve', 'Hitung kosinus dan urutkan galeri',
          'Simpan AP@10 tiap kueri, kesesuaian Top-1, dan skor tertinggi')],
    [Node('metric', 'Hitung mAP@10 per lokasi', 'Pisahkan menurut SNR, ulangan, dan representasi'),
     data('diagnostic', 'Kesesuaian Top-1 dan skor ke E5', 'Bersama ambang tiap representasi dari E3')],
    [Node('range', 'Hitung rentang dalam tiap ulangan',
          'mAP@10 tertinggi − terendah dari lima lokasi pada SNR yang sama')],
    [Node('mean', 'Ringkas kestabilan antarlokasi',
          'Rata-ratakan rentang empat ulangan; bagi dengan mAP@10 acuan untuk rentang relatif')],
    [data('output', 'Perbandingan kinerja dan kestabilan',
          'Lengkapi dengan sensitivitas penghilangan satu lokasi secara bergiliran')],
], [Edge('query', 'draw'), Edge('noise', 'sites')] + chain('sites', 'draw', 'snr', 'mix', 'features', 'retrieve') + [
    Edge('gallery', 'retrieve'), Edge('retrieve', 'metric'), Edge('retrieve', 'diagnostic')
] + chain('metric', 'range', 'mean', 'output'),
       note='Perbandingan dilakukan pada kueri yang sama. Lokasi dan potongan derau yang tersedia menjadi cakupan interpretasi.')

render('e5_diagnosis_kegagalan', 'E5', 'Diagnosis Kegagalan dan Audit Pendengaran', [
    [data('e2', 'Hasil kueri target E1–E2', 'Kesesuaian Top-1 dan skor; acuan tersimpan dalam hasil E2'),
     data('e4', 'Hasil kueri target E4', 'Kesesuaian Top-1 dan skor tertinggi'),
     data('e3', 'Ambang tetap dari E3', 'Satu ambang per representasi')],
    [Node('align', 'Selaraskan identitas tiap kasus', 'Cocokkan ID kueri, representasi, kondisi, dan ambang')],
    [decision('top1', 'Spesies Top-1 sesuai dengan kueri?')],
    [decision('match_score', 'Skor ≥ ambang?'), decision('wrong_score', 'Skor ≥ ambang?')],
    [data('success', 'Top-1 benar dan diterima', 'Catat sebagai pencarian berhasil'),
     data('reject', 'Top-1 benar tetapi ditolak'),
     data('confusion', 'Top-1 keliru tetapi diterima'),
     data('collapse', 'Top-1 keliru dan ditolak')],
    [Node('failures', 'Kumpulkan tiga kategori kegagalan', 'Simpan sumber eksperimen, representasi, dan kondisi setiap kasus')],
    [Node('margin', 'Hitung margin tiap kasus', 'Skor tertinggi dikurangi ambang'),
     Node('acoustic', 'Periksa audio kasus E2', 'Bentuk ulang campuran; hitung centroid, bandwidth, dan RMS'),
     data('controls', 'Keputusan kontrol uji dari E3', 'Kueri kontrol diterima atau ditolak')],
    [Node('summary', 'Rangkum diagnosis kueri target',
          'E2 memakai skor dan ciri akustik; E4 memakai kesesuaian Top-1 dan skor'),
     Node('control_summary', 'Rekap keputusan kontrol', 'Hitung penerimaan keliru dan penolakan yang benar')],
    [Node('sample', 'Pilih 120 kasus kegagalan E2',
          'Hingga dua per kombinasi representasi, kondisi, dan kategori; seed 20261012')],
    [Node('listen', 'Bandingkan tiga rekaman melalui pendengaran',
          'Satu pendengar memeriksa kueri sesuai kondisi, kueri acuan, dan rekaman Top-1')],
    [Node('notes', 'Catat keterdengaran vokalisasi dan suara latar', 'Terdengar, tidak terdengar, atau ragu; tambahkan catatan pendengar')],
    [data('output', 'Ringkasan pola kegagalan', 'Hubungkan kategori, margin, ciri akustik yang tersedia, dan catatan pendengaran')],
], [Edge(key, 'align') for key in ('e2', 'e4', 'e3')] + chain('align', 'top1') + [
    Edge('top1', 'match_score', 'Ya'), Edge('top1', 'wrong_score', 'Tidak'),
    Edge('match_score', 'success', 'Ya'), Edge('match_score', 'reject', 'Tidak'),
    Edge('wrong_score', 'confusion', 'Ya'), Edge('wrong_score', 'collapse', 'Tidak'),
] + [Edge(key, 'failures') for key in ('reject', 'confusion', 'collapse')] + [
    Edge('failures', 'margin'), Edge('failures', 'acoustic'),
    Edge('margin', 'summary'), Edge('acoustic', 'summary'),
    Edge('controls', 'control_summary'), Edge('control_summary', 'output')
] + chain('summary', 'sample', 'listen', 'notes', 'output'),
       note='Identitas rekaman Top-1 dan ciri akustik E4 mengikuti ketersediaan arsip. Catatan audit dirangkum secara deskriptif.')
