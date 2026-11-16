from pathlib import Path
import csv
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np

root = Path(__file__).resolve().parents[3]
geometry = root / 'paper/figures/bab3/ne_50m_admin_0_countries.geojson'
manifest = root / 'data/manifests/dataset_split.csv'
target = root / 'paper/figures/bab3/peta_rekaman_xenocanto.png'
with geometry.open(encoding='utf-8') as f:
    countries = json.load(f)['features']
with manifest.open(encoding='utf-8-sig', newline='') as f:
    data = list(csv.DictReader(f))
recording_sites = {}
for row in data:
    if row["latitude"].strip() and row["longitude"].strip():
        point = (float(row["longitude"]), float(row["latitude"]))
        recording_sites.setdefault(row["scientific_name"], set()).add(point)
species = sorted(recording_sites)
unique_coordinates = set().union(*recording_sites.values())
assert len(species) == 20 and len(unique_coordinates) == 371

fig, ax = plt.subplots(figsize=(8, 4.4))
ax.set_facecolor('#f3f6f7')
for country in countries:
    geo = country['geometry']
    polygons = geo['coordinates'] if geo['type'] == 'MultiPolygon' else [geo['coordinates']] if geo['type'] == 'Polygon' else []
    for polygon in polygons:
        xy = np.asarray(polygon[0])
        if len(xy) < 3 or xy[:, 0].max() < 93 or xy[:, 0].min() > 144 or xy[:, 1].max() < -13 or xy[:, 1].min() > 9:
            continue
        ax.add_patch(Polygon(xy, closed=True, facecolor='#ddddda', edgecolor='#92928d', linewidth=.35, zorder=1))
# Alternate marker shapes in addition to color to distinguish similar colors.
colors = plt.get_cmap("tab20").colors
markers = ("o", "s", "^", "D", "v")
for index, name in enumerate(species):
    points = np.asarray(sorted(recording_sites[name]))
    ax.scatter(
        points[:, 0], points[:, 1], s=15, color=colors[index],
        marker=markers[(index // 2) % len(markers)], edgecolors="#252525",
        linewidths=0.27, alpha=0.86, zorder=3, label=name,
    )
ax.set(xlim=(94, 142), ylim=(-12.3, 7.5), xlabel='Bujur (derajat)', ylabel='Lintang (derajat)')
ax.set_xticks([100,110,120,130,140]); ax.set_yticks([-10,-5,0,5])
ax.tick_params(labelsize=8); ax.xaxis.label.set_size(9); ax.yaxis.label.set_size(9)
ax.set_aspect('equal', adjustable='box'); ax.grid(color='#b9b9b9', lw=.3, alpha=.6, zorder=0)
ax.legend(
    title="Spesies burung", loc="upper center", bbox_to_anchor=(0.5, -0.22),
    ncol=3, prop={"size": 8, "style": "italic"}, title_fontsize=9,
    frameon=False, markerscale=1.2, handletextpad=0.35, columnspacing=1.25,
)
fig.savefig(target, dpi=300, bbox_inches='tight', facecolor='white')
plt.close(fig)
print(target, f'{len(species)} spesies, {len(unique_coordinates)} titik unik')
