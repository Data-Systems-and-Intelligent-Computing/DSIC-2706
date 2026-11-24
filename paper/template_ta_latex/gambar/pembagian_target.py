"""Buat grafik BAB III dari data/manifests/dataset_split.csv dengan ReportLab."""
import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import Canvas


HERE = Path(__file__).resolve().parent
ROLES = (
    ("gallery", "Galeri", "#757575"),
    ("query_clean", "Kueri uji", "#347943"),
    ("calibration", "Kalibrasi", "#365F7A"),
)


def plot(manifest, output):
    counts = defaultdict(Counter)
    authors = defaultdict(set)
    seen = set()
    with manifest.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            ident, role = row["recording_id"], row["split_role"]
            if ident in seen or role not in {key for key, _, _ in ROLES}:
                raise ValueError(f"Periksa ID rekaman atau peran pada {ident}")
            seen.add(ident)
            counts[row["scientific_name"]][role] += 1
            authors[role].add(row["author"].strip())
    species = sorted(counts, key=lambda name: (-sum(counts[name].values()), name))
    maximum = max(sum(row.values()) for row in counts.values())
    tick = 20
    axis_max = ((maximum + tick - 1) // tick) * tick
    row_height = 13
    width, height = 398, row_height * len(species) + 78
    x0, x1 = 92, 337
    top = height - 40
    axis_y = top - row_height * len(species) + 4
    pdf = Canvas(str(output), pagesize=(width, height), invariant=True)
    pdf.setTitle("Pembagian rekaman target per spesies dan peran")
    for i, (key, label, color) in enumerate(ROLES):
        x = (0, 134, 267)[i]
        n = sum(row[key] for row in counts.values())
        pdf.setFillColor(HexColor(color))
        pdf.rect(x, height - 10, 8, 6, fill=1, stroke=0)
        pdf.setFillColor(HexColor("#222222"))
        pdf.setFont("Times-Bold", 9)
        pdf.drawString(x + 12, height - 10, label)
        pdf.setFont("Times-Roman", 8)
        pdf.drawString(x + 12, height - 21, f"{n} klip, {len(authors[key])} nama perekam")
    pdf.setFont("Times-Roman", 8)
    for value in range(0, axis_max + 1, tick):
        x = x0 + (x1 - x0) * value / axis_max
        pdf.setLineWidth(0.35)
        pdf.setStrokeColor(HexColor("#D5D5D5"))
        pdf.line(x, axis_y, x, top + 4)
        pdf.drawCentredString(x, axis_y - 11, str(value))
    pdf.drawCentredString((x0 + x1) / 2, axis_y - 23, "Jumlah klip")
    pdf.setFont("Times-Bold", 8)
    pdf.drawCentredString(369, top + 8, "G / U / K")
    for i, name in enumerate(species):
        row = counts[name]
        y = top - i * row_height
        pdf.setFont("Times-Italic", 8.6)
        pdf.drawRightString(x0 - 4, y - 2.8, name)
        x = x0
        for key, _, color in ROLES:
            segment = (x1 - x0) * row[key] / axis_max
            pdf.setFillColor(HexColor(color))
            pdf.rect(x, y - 4.1, segment, 8.2, fill=1, stroke=0)
            x += segment
        pdf.setFillColor(HexColor("#222222"))
        pdf.setFont("Times-Roman", 8.5)
        pdf.drawCentredString(369, y - 2.8, " / ".join(str(row[k]) for k, _, _ in ROLES))
    pdf.save()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, nargs="?",
                        default=HERE.parents[2] / "data/manifests/dataset_split.csv")
    parser.add_argument("--output", type=Path, default=HERE / "pembagian_target.pdf")
    args = parser.parse_args()
    plot(args.manifest, args.output)
