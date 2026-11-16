"""Diagram metodologi dari kode dan manifes aktif; tidak mengubah data eksperimen."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse, Polygon, FancyArrowPatch

HERE=Path(__file__).resolve().parent
plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none'})
def canvas(w=8,h=10):
    fig,ax=plt.subplots(figsize=(w,h)); ax.set_xlim(0,100);ax.set_ylim(0,100);ax.axis('off');return fig,ax
def rect(ax,x,y,w,h,text,fs=10,style='box',bold=False):
    if style=='ellipse': p=Ellipse((x+w/2,y+h/2),w,h,edgecolor='black',facecolor='white',lw=1.15)
    elif style=='data': p=Polygon([(x+2,y),(x+w,y),(x+w-2,y+h),(x,y+h)],closed=True,edgecolor='black',facecolor='white',lw=1.15)
    else:p=Rectangle((x,y),w,h,edgecolor='black',facecolor='white',lw=1.15)
    ax.add_patch(p);ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs,linespacing=1.25,weight='bold' if bold else 'normal')
def line(ax,points,arrow=True):
    for (x1,y1),(x2,y2) in zip(points[:-2],points[1:-1]):ax.plot([x1,x2],[y1,y2],color='black',lw=1)
    (x1,y1),(x2,y2)=points[-2:]
    if arrow:ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=11,lw=1,color='black'))
    else: ax.plot([x1,x2],[y1,y2],color='black',lw=1)
def tag(ax,x,y,label):
    rect(ax,x,y,5,4,label,10,bold=True)
def save(fig,name):
    for fmt in ('png','svg'):fig.savefig(HERE/f'{name}.{fmt}',dpi=240,bbox_inches='tight',facecolor='white')
    plt.close(fig)

# Diagram utama: huruf menghubungkan ke gambar rinci yang dicetak terpisah.
fig,ax=canvas(8.4,10.8)
rect(ax,40,94,20,5,'MULAI',10,'ellipse')
rect(ax,23,85,54,6,'Studi pustaka dan perumusan masalah',10)
line(ax,[(50,94),(50,91)])
rect(ax,2,72,30,8,'Rekaman burung\n20 spesies target',9.5,'data')
rect(ax,35,72,30,8,'Rekaman derau\n5 lokasi Itera',9.5,'data')
rect(ax,68,72,30,8,'Kontrol di luar\nspesies target',9.5,'data')
line(ax,[(50,85),(50,82),(17,82),(17,80)])
line(ax,[(50,85),(50,80)])
line(ax,[(50,85),(50,82),(83,82),(83,80)])
rect(ax,14,60,72,7,'Pemilihan dan pembagian data',10);tag(ax,87,63,'A')
for x in (17,50,83):line(ax,[(x,72),(x,69),(50,69),(50,67)])
rect(ax,14,49,72,7,'Prapemrosesan audio dan audit E0',10);tag(ax,87,52,'B');line(ax,[(50,60),(50,56)])
rect(ax,14,38,72,7,'Ekstraksi representasi dan galeri referensi',10);tag(ax,87,41,'C');line(ax,[(50,49),(50,45)])
rect(ax,2,23,22,9,'E1: Acuan\n(rincian D)',9.3)
rect(ax,27,23,22,9,'E2: Variasi SNR\n(rincian D)',9.1)
rect(ax,52,23,22,9,'E3: Ambang\n(rincian E)',9.3)
rect(ax,77,23,22,9,'E4: Lima lokasi\n(rincian D)',9.1)
line(ax,[(50,38),(50,35),(13,35),(13,32)])
line(ax,[(50,35),(38,35),(38,32)])
line(ax,[(50,35),(63,35),(63,32)])
line(ax,[(50,35),(88,35),(88,32)])
rect(ax,13,11,74,7,'E5: analisis kegagalan dan audit pendengaran',9.6);tag(ax,88,14,'F')
for x in (13,38,63,88):line(ax,[(x,23),(x,20),(50,20),(50,18)])
rect(ax,18,1,64,6,'Analisis, interpretasi, dan kesimpulan',9.5,'ellipse');line(ax,[(50,11),(50,7)])
save(fig,'revisi_01_alur_keseluruhan')

# A: sumber dan partisi data; kontrol tidak digabung sebagai data target.
fig,ax=canvas(8.4,9.6)
rect(ax,17,90,66,7,'Rekaman target: 20 label spesies\n1.216 rekaman Xeno-Canto',10,'data')
rect(ax,17,79,66,7,'Pemeriksaan identitas dan metadata\nPembagian kelompok target berdasarkan perekam',10)
line(ax,[(50,90),(50,86)])
for x,text in [(2,'Galeri\n673 rekaman'),(35,'Kueri uji\n311 rekaman'),(68,'Kalibrasi target\n232 rekaman')]:rect(ax,x,64,30,9,text,9.5,'data')
for x in (17,50,83):line(ax,[(50,79),(50,76),(x,76),(x,73)])
rect(ax,3,46,43,9,'Rekaman derau Itera\n1.799 berkas',10,'data')
rect(ax,54,46,43,9,'Rekaman non-target\n272 rekaman',10,'data')
rect(ax,2,28,29,10,'1.528 berkas\nuntuk campuran',9.5,'data')
rect(ax,35,28,29,10,'271 berkas\nuntuk kontrol',9.5,'data')
rect(ax,68,28,30,10,'543 rekaman\ndi luar target',9.5,'data')
line(ax,[(24.5,46),(24.5,42),(16.5,42),(16.5,38)])
line(ax,[(24.5,46),(24.5,42),(49.5,42),(49.5,38)])
line(ax,[(64,33),(68,33)])
line(ax,[(75,46),(75,42),(83,42),(83,38)])
rect(ax,15,6,70,9,'Kontrol di luar target: 233 untuk kalibrasi\ndan 310 untuk pengujian',10,'data')
line(ax,[(83,28),(83,20),(50,20),(50,15)])
save(fig,'revisi_A_pemilihan_dan_pembagian_data')

# B: urutan sesuai preprocess_audio; kondisi durasi merupakan cabang.
fig,ax=canvas(8,10)
for y,t in [(91,'Masukan rekaman audio'),(81,'Baca audio menjadi mono\ndan sesuaikan laju ke 32 kHz'),(69,'Pemeriksaan durasi rekaman'),(34,'Panjang sinyal tepat 5 detik\n(160.000 sampel)'),(22,'Normalisasi RMS menuju 0,05\njika sinyal tidak sangat senyap'),(10,'Batasi amplitudo pada −1 sampai 1')]:rect(ax,18,y,64,7,t,10,'data' if y==91 else 'box')
rect(ax,1,49,32,12,'Lebih dari 5 detik\nPilih RMS terbesar\ngeser 1,25 detik',9)
rect(ax,34,49,32,12,'Tepat 5 detik\nGunakan segmen\napa adanya',9)
rect(ax,67,49,32,12,'Kurang dari 5 detik\nTambahkan nol\ndi akhir sinyal',9)
line(ax,[(50,91),(50,88)]);line(ax,[(50,81),(50,76)])
for x in (17,50,83):line(ax,[(50,69),(50,65),(x,65),(x,61)])
for x in (17,50,83):line(ax,[(x,49),(x,45),(50,45),(50,41)])
line(ax,[(50,34),(50,29)]);line(ax,[(50,22),(50,17)])
save(fig,'revisi_B_prapemrosesan_audio')

# C: model khusus versus kontrol berbasis identitas.
fig,ax=canvas(10,8.2)
rect(ax,27,89,46,8,'Audio siap 5 detik, 32 kHz',10,'data')
for x,txt in [(2,'R0: MFCC\n20 koefisien\nmean + standar deviasi\nvektor 40 nilai'),(27,'R1: PANNs CNN14\nmodel pralatih\nbobot tetap\nvektor 2.048 nilai'),(52,'R2: BirdNET v2.4\n48 kHz; jendela 3 detik\ngeser 1 detik; rata-rata\nvektor 1.024 nilai')]:
    rect(ax,x,57,22,18,txt,9)
rect(ax,77,57,22,18,'R3: kontrol acak\nberdasarkan ID rekaman\nvektor 40 nilai\nbukan fitur audio',9)
for x in (13,38,63):line(ax,[(50,89),(50,82),(x,82),(x,75)])
rect(ax,77,89,22,8,'ID rekaman',10,'data');line(ax,[(88,89),(88,75)])
rect(ax,16,35,68,9,'Normalisasi panjang vektor (L2)\nmasing-masing representasi',10)
for x in (13,38,63,88):line(ax,[(x,57),(x,50),(50,50),(50,44)])
rect(ax,20,15,60,10,'Kueri dan galeri dibandingkan\ndalam representasi yang sama',10)
line(ax,[(50,35),(50,25)])
ax.text(50,5,'Model pralatih yang bobotnya tetap adalah PANNs dan BirdNET.',ha='center',fontsize=9.5)
save(fig,'revisi_C_empat_representasi')

# D: tahapan pengujian tanpa menyatakan hasil.
fig,ax=canvas(9,10)
rect(ax,8,90,38,7,'Kueri target: 311',10,'data');rect(ax,54,90,38,7,'Galeri tetap: 673',10,'data')
rect(ax,22,78,56,7,'E1: pencarian kondisi acuan',10)
line(ax,[(27,90),(27,88),(40,88),(40,85)]);line(ax,[(73,90),(73,88),(60,88),(60,85)])
rect(ax,4,59,43,11,'E2: uji derau terkontrol\nSNR +20, +10, 0, −5 dB\npool derau Itera',9.5)
rect(ax,53,59,43,11,'E4: uji profil 5 lokasi\n4 SNR dan 4 ulangan\npada kueri yang sama',9.5)
line(ax,[(50,78),(50,74),(25.5,74),(25.5,70)]);line(ax,[(50,74),(74.5,74),(74.5,70)])
rect(ax,15,41,70,9,'Pencarian dan pengurutan kandidat\ndengan kemiripan kosinus',10)
line(ax,[(25.5,59),(25.5,55),(50,55),(50,50)]);line(ax,[(74.5,59),(74.5,55),(50,55),(50,50)])
rect(ax,15,25,70,9,'Hitung mAP@10 dan metrik pendukung\nBandingkan kualitas dan retensi dengan acuan',10)
line(ax,[(50,41),(50,34)])
rect(ax,15,6,70,11,'Analisis kestabilan E4 (eksploratif)\nayunan absolut dan relatif; sensitivitas lokasi\nbootstrap kueri berpasangan',9.4)
line(ax,[(50,25),(50,17)])
save(fig,'revisi_D_pengujian_kualitas_dan_lokasi')

# E: kalibrasi dan diagnostik berbeda: label accepted ≠ spesies benar.
fig,ax=canvas(9,10)
rect(ax,3,88,44,8,'Kalibrasi target: 232',9.5,'data');rect(ax,53,88,44,8,'Kalibrasi non-target: 233',9.5,'data')
rect(ax,14,73,72,8,'Skor kemiripan tertinggi ke galeri\nkalibrasi tanpa penambahan derau',9.5)
line(ax,[(25,88),(25,84),(40,84),(40,81)]);line(ax,[(75,88),(75,84),(60,84),(60,81)])
rect(ax,20,61,60,7,'ROC dan indeks Youden → ambang tetap',10)
line(ax,[(50,73),(50,68)])
rect(ax,12,47,76,8,'Terapkan pada kueri uji target dan non-target\nuntuk kondisi acuan dan berderau',9.5)
line(ax,[(50,61),(50,55)])
rect(ax,4,31,42,9,'Skor ≥ ambang\nkueri diterima',10);rect(ax,54,31,42,9,'Skor < ambang\nkueri ditolak',10)
line(ax,[(50,47),(50,44),(25,44),(25,40)]);line(ax,[(50,44),(75,44),(75,40)])
rect(ax,10,14,80,9,'Ukur penerimaan target dan penerimaan keliru kontrol\nKetepatan spesies Top-1 dievaluasi terpisah',9.3)
line(ax,[(25,31),(25,27),(50,27),(50,23)]);line(ax,[(75,31),(75,27),(50,27),(50,23)])
rect(ax,10,1,80,8,'E5: kelompokkan kegagalan; periksa margin, ciri\nyang tersedia, dan 120 kasus audit pendengaran',9.2)
line(ax,[(50,14),(50,9)])
save(fig,'revisi_E_ambang_dan_diagnostik')

# F: empat kategori operasional dan audit kasus terpilih.
fig,ax=canvas(10,8)
rect(ax,23,88,54,8,'Hasil pencarian setiap kueri target\nspesies Top-1, skor, dan ambang',10,'data')
rect(ax,4,69,42,10,'Top-1 sesuai label spesies',10)
rect(ax,54,69,42,10,'Top-1 berbeda label spesies',10)
line(ax,[(50,88),(50,84),(25,84),(25,79)]);line(ax,[(50,84),(75,84),(75,79)])
labels=[('Skor ≥ ambang\nDiterima dan\nTop-1 sesuai',2),('Skor < ambang\nPenolakan meski\nTop-1 sesuai',27),('Skor ≥ ambang\nDiterima tetapi\nTop-1 keliru',52),('Skor < ambang\nDitolak dan\nTop-1 keliru',77)]
for txt,x in labels:rect(ax,x,42,21,15,txt,8.9)
for parent,children in ((25,(12.5,37.5)),(75,(62.5,87.5))):
    for x in children:line(ax,[(parent,69),(parent,64),(x,64),(x,57)])
rect(ax,12,20,76,9,'Kasus gagal: periksa margin terhadap ambang\ndan ciri spektral jika tersedia',9.5)
for x in (37.5,62.5,87.5):line(ax,[(x,42),(x,35),(50,35),(50,29)])
rect(ax,12,3,76,9,'Audit pendengaran: 120 kasus E2 terpilih\nsatu pendengar; analisis deskriptif',9.5)
line(ax,[(50,20),(50,12)])
save(fig,'revisi_F_kategori_kegagalan')
