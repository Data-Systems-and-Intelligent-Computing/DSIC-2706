"""Archive Fabio's E5 notes, apply one confirmed amendment, and summarize.

Never rewrites experiment outputs, the blank review sheet, or an existing
export. Human prose and original listening timestamps remain verbatim.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.import_e5_human_review import FIELDS, combine_reviews, main as import_reviews

REVIEW = ROOT / 'Rencana-eksperimen-bimbingan/audit-pendengaran-E5'
LOCAL = timezone(timedelta(hours=7))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path: Path, value: object) -> None:
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def log(folder: Path, event: str) -> None:
    now = datetime.now(timezone.utc)
    path = folder / 'LOG_AUDIT.md'
    if not path.exists():
        path.write_text('# Log pengerjaan audit E5\n\n', encoding='utf-8')
    with path.open('a', encoding='utf-8', newline='\n') as stream:
        stream.write(f'\n- **{now.isoformat()} / {now.astimezone(LOCAL).isoformat()}:** {event}\n')
    print(event, flush=True)


def audibility(rows: list[dict[str, str]]) -> dict:
    n = len(rows)
    result = {'n_cases': n}
    for field in ('query_vocalisation_audible', 'top1_vocalisation_audible'):
        counts = Counter(r[field] for r in rows)
        result[field] = {key: counts[key] for key in ('yes', 'no', 'uncertain')}
    result['both_audible_yes'] = sum(
        r['query_vocalisation_audible'] == r['top1_vocalisation_audible'] == 'yes' for r in rows
    )
    return result


def grouped(rows: list[dict[str, str]], field: str) -> dict:
    groups = defaultdict(list)
    for row in rows:
        groups[row[field]].append(row)
    return {key: audibility(value) for key, value in sorted(groups.items())}


def summary(rows: list[dict[str, str]]) -> dict:
    pairs = defaultdict(list)
    top1 = defaultdict(list)
    for row in rows:
        pairs[(row['query_id'], row['condition'])].append(row)
        top1[row['top1_recording_id']].append(row)
    conflicts = []
    for key, group in pairs.items():
        if len({r['query_vocalisation_audible'] for r in group}) > 1:
            conflicts.append({'query_id': key[0], 'condition': key[1],
                              'case_observations': {r['case_id']: r['query_vocalisation_audible'] for r in group}})
    top1_conflicts = []
    for key, group in top1.items():
        if len({r['top1_vocalisation_audible'] for r in group}) > 1:
            top1_conflicts.append({'top1_recording_id': key,
                                   'case_observations': {r['case_id']: r['top1_vocalisation_audible'] for r in group}})
    dates = [datetime.fromisoformat(r['reviewed_at'].replace('Z', '+00:00')).astimezone(LOCAL) for r in rows]
    return {
        'schema': 'e5_human_audit_summary_v1',
        'analysis_unit': 'Selected case row; counts are descriptive, not population failure rates',
        'overall': audibility(rows),
        'audio_representations_R0_R1_R2': audibility([r for r in rows if r['representation'] != 'R3']),
        'review_status': dict(Counter(r['review_status'] for r in rows)),
        'reviewers': dict(Counter(r['reviewer'] for r in rows)),
        'listening_local_first': min(dates).isoformat(),
        'listening_local_last': max(dates).isoformat(),
        'unique_queries': len({r['query_id'] for r in rows}),
        'unique_query_condition_pairs': len(pairs),
        'by_representation': grouped(rows, 'representation'),
        'by_condition': grouped(rows, 'condition'),
        'by_failure_mode': grouped(rows, 'failure_mode_computational'),
        'query_not_audible_cases': [r['case_id'] for r in rows if r['query_vocalisation_audible'] == 'no'],
        'top1_uncertain_cases': [r['case_id'] for r in rows if r['top1_vocalisation_audible'] == 'uncertain'],
        'within_listener_query_category_differences': conflicts,
        'within_listener_top1_category_differences': top1_conflicts,
        'within_listener_note': 'Repeated-audio category differences are reported, not silently resolved or treated as inter-rater agreement.',
    }


def md_table(groups: dict) -> str:
    lines = ['| Kelompok | Kasus | Kueri yes / no / ragu | Top-1 yes / no / ragu |',
             '|---|---:|---:|---:|']
    for key, value in groups.items():
        q = value['query_vocalisation_audible']; t = value['top1_vocalisation_audible']
        lines.append(f"| {key} | {value['n_cases']} | {q['yes']} / {q['no']} / {q['uncertain']} | {t['yes']} / {t['no']} / {t['uncertain']} |")
    return '\n'.join(lines)


def report(folder: Path, rows: list[dict[str, str]], stats: dict, csv_path: Path) -> str:
    q = stats['overall']['query_vocalisation_audible']; t = stats['overall']['top1_vocalisation_audible']
    real = stats['audio_representations_R0_R1_R2']; rq = real['query_vocalisation_audible']
    by_id = {r['case_id']: r for r in rows}
    examples = []
    for identifier in ('E5_001', 'E5_005', 'E5_018', 'E5_037', 'E5_063', 'E5_105'):
        row = by_id[identifier]
        interpretation = row['auditory_interpretation'].replace('\n', ' ').replace('|', '/')
        examples.append(f"| {identifier} | {row['representation']} / {row['condition']} | {row['failure_mode_computational']} | {interpretation} |")
    consistency = []
    for key in ('within_listener_query_category_differences', 'within_listener_top1_category_differences'):
        for item in stats[key]:
            identity = item.get('query_id', item.get('top1_recording_id'))
            condition = item.get('condition', 'Top-1 galeri')
            values = ', '.join(f'{case}: {value}' for case, value in item['case_observations'].items())
            consistency.append(f'- {identity}, {condition}: {values}.')
    if not consistency:
        consistency.append('- Tidak ada perbedaan kategori pada audio berulang yang diperiksa.')
    return f'''# Hasil audit pendengaran E5 dan progres bimbingan

**Tanggal laporan: 30 Oktober 2026.** Pendengar: Fabio Banyu Cyto. Sebanyak **120/120 kasus pilihan mempunyai catatan pendengaran** dan lolos validasi struktur serta identitas sumber. Tidak ada baris pending atau needs_follow_up pada ekspor. Ini bukti pelaksanaan audit oleh satu pendengar berdasarkan catatannya; pemeriksaan perangkat lunak tidak mengesahkan identitas spesies atau pengalaman mendengar secara independen.

## 1. Bukti dan koreksi yang disetujui

- [JSON asli](E5_catatan_pendengaran_asli.json) disimpan identik byte dengan berkas yang dikirim Fabio.
- [JSON hasil satu koreksi](E5_catatan_pendengaran_terkoreksi.json) mengubah hanya E5_105, `query_vocalisation_audible`, dari `uncertain` ke `yes`.
- Fabio mengonfirmasi salah tekan: “itu kepencet yang ragu (aslinya terdengar jelas)”. [Catatan koreksi](koreksi_E5_105.json) menyimpan alasan, otorisasi, dan hash sebelum/sesudah.
- [CSV gabungan 120 kasus](../{csv_path.name}) mempertahankan kolom eksperimen sumber dan seluruh teks pengamatan asli. Tanggal pendengaran tidak diganti dengan waktu pengolahan.
- [Ringkasan hitungan](ringkasan_pendengaran.json), [manifest hash](manifest_artefak.json), dan [log pengerjaan](LOG_AUDIT.md) tersedia untuk pemeriksaan.

Periode waktu catatan, pada UTC+07:00: **{stats['listening_local_first']}** sampai **{stats['listening_local_last']}**. File kosong sumber serta metadata persiapan 16 Oktober tetap menjadi riwayat. Status nol ulasan pada dokumen persiapan lama tidak menggambarkan hasil impor 30 Oktober ini.

## 2. Cara analisis dan satuan hitung

Penggabungan memakai `case_id`, hash setiap baris, dan hash lembar sumber melalui importer yang sudah ada. Seluruh label, representasi, kondisi, skor, dan ambang tetap berasal dari E5 terdahulu. Analisis hanya menghitung kategori isian manusia secara deskriptif, lalu mengelompokkannya menurut representasi, kondisi, dan jenis kegagalan komputer.

Terdapat **{stats['unique_queries']} kueri unik** dan **{stats['unique_query_condition_pairs']} pasangan kueri–kondisi unik**. Unit hitung tabel adalah 120 baris kasus pilihan. Sampel dipilih menurut jenis kegagalan: masing-masing 40 false rejection, confusion, dan collapse; masing-masing representasi 30 kasus; masing-masing kondisi 24 kasus. Komposisi pilihan ini tidak mengestimasi frekuensi kegagalan pada seluruh kueri. Tidak dilakukan uji signifikansi yang menganggap 120 kasus independen.

## 3. Hasil keterdengaran

| Audio yang dinilai | Terdengar (yes) | Tidak terdengar (no) | Ragu (uncertain) | Penyebut |
|---|---:|---:|---:|---:|
| Kueri sesuai kondisi | {q['yes']} ({100*q['yes']/120:.2f}%) | {q['no']} ({100*q['no']/120:.2f}%) | {q['uncertain']} | 120 kasus |
| Hasil Top-1 | {t['yes']} ({100*t['yes']/120:.2f}%) | {t['no']} ({100*t['no']/120:.2f}%) | {t['uncertain']} ({100*t['uncertain']/120:.2f}%) | 120 kasus |

Pada **{stats['overall']['both_audible_yes']} kasus**, kueri dan Top-1 sama-sama dinyatakan terdengar. Pada subset **90 kasus R0/R1/R2**, kueri terdengar pada **{rq['yes']}/90 kasus**. R3 dipisahkan karena vektornya bergantung pada ID, bukan waveform; retensi atau dugaan distraksi audio pada R3 tidak boleh ditafsirkan seperti model audio.

### Menurut representasi

{md_table(stats['by_representation'])}

### Menurut kondisi

{md_table(stats['by_condition'])}

Clean berarti tidak diberi derau tambahan pada eksperimen. Rekaman sumber masih dapat mempunyai latar. Top-1 berasal dari galeri tetap, sehingga kategori Top-1 pada kelompok SNR bukan hasil menyuntikkan SNR tersebut ke audio galeri.

### Menurut jenis kegagalan komputer

{md_table(stats['by_failure_mode'])}

False rejection berarti hasil pertama berspesies sesuai metadata tetapi skornya di bawah ambang. Confusion berarti hasil pertama berbeda spesies dan skornya melewati ambang. Label operasional collapse berarti hasil pertama salah dan skor maksimum di bawah ambang; label itu tidak membuktikan sepuluh hasil semuanya salah.

## 4. Pembahasan yang didukung catatan

Sebagian besar kueri pada kasus kegagalan yang dipilih masih mengandung suara burung yang terdengar menurut Fabio. Ini menunjukkan bahwa kegagalan pada pilihan kasus ini tidak selalu bersamaan dengan hilangnya seluruh suara burung dari pendengaran. Keterdengaran oleh manusia dan keberhasilan ranking/ambang komputer merupakan ukuran yang berbeda. Mendengar suara burung juga belum membuktikan bahwa vokalisasi yang terdengar berasal dari spesies target metadata.

Empat kueri dinyatakan tidak terdengar: {', '.join(stats['query_not_audible_cases'])}. Top-1 diragukan pada {', '.join(stats['top1_uncertain_cases'])}. Kasus tersebut memperlihatkan batas penafsiran pendengaran ketika latar atau suara singkat menyulitkan pemeriksaan. Nama sumber latar seperti hujan, angin, air, mesin, atau serangga dalam catatan adalah kesan pendengar jika belum diukur/dikonfirmasi secara terpisah.

Contoh berikut menyalin interpretasi Fabio, termasuk ejaan aslinya:

| Kasus | Representasi / kondisi | Diagnosis komputer | Catatan pendengar (verbatim) |
|---|---|---|---|
{chr(10).join(examples)}

Pada E5_001, metadata Top-1 sama spesiesnya dengan kueri walaupun kesan bunyinya berbeda. Perbedaan bunyi tidak otomatis membatalkan label spesies. Pada E5_105, kalimat “Mungkin terdistraksi ...” merupakan dugaan Fabio; karena kasus ini R3, kalimat tersebut tidak dijadikan mekanisme gangguan pada embedding berbasis ID.

## 5. Pemeriksaan konsistensi dan batas interpretasi

Terdapat {len(stats['within_listener_query_category_differences'])} kelompok kueri–kondisi berulang dengan kategori keterdengaran berbeda, dan {len(stats['within_listener_top1_category_differences'])} kelompok rekaman Top-1 berulang dengan kategori berbeda. Daftar berikut dipertahankan sebagai pemeriksaan transparansi, tanpa mengganti pilihan pendengar:

{chr(10).join(consistency)}

Pada E5_018, deskripsi latar menyebut Top-1 “hanya suara angin”, sementara pilihan Top-1 dan interpretasinya menyatakan kicauan terdengar. Kedua teks tetap disimpan sebagai ambiguitas redaksional; tidak ada koreksi tambahan tanpa konfirmasi Fabio. Laporan memakai kategori terstruktur untuk menghitung, bukan menebak pengganti jawaban dari kalimat bebas. Status `reviewed` menyatakan catatan sudah dibuat, bukan semua pengamatan sudah bebas ketidakpastian.

Audit hanya melibatkan satu pendengar dan tidak bersifat penilaian buta; halaman menampilkan identitas/diagnosis kasus. Tidak dihitung kesepakatan antarpendengar. Sampel dipilih dari kegagalan dan tidak memiliki kelompok pembanding sukses yang seimbang. Tidak disimpulkan penyebab kausal derau, jarak, serangga, atau sifat arsitektur. E4 tidak mendapat penambahan ciri akustik atau anotasi melalui audit ini.

## 6. Bahan pembahasan E5 untuk naskah (draf)

Audit pendengaran dilakukan oleh peneliti terhadap 120 kasus E5 yang telah dipilih berdasarkan kelompok representasi, kondisi, dan jenis kegagalan komputasional. Setiap kasus dihubungkan dengan identitas sumber dan pengamatan atas kueri serta hasil Top-1. Setelah satu koreksi isian yang dikonfirmasi peneliti, vokalisasi pada kueri dinyatakan terdengar pada {q['yes']} dari 120 kasus dan tidak terdengar pada {q['no']} kasus. Vokalisasi pada Top-1 dinyatakan terdengar pada {t['yes']} kasus, tidak terdengar pada {t['no']} kasus, dan diragukan pada {t['uncertain']} kasus. Temuan ini menunjukkan bahwa, dalam kasus kegagalan yang dipilih, keterdengaran vokalisasi oleh peneliti sering tetap ada ketika ranking atau keputusan ambang gagal menurut metadata. Penafsiran dibatasi oleh pemilihan kasus, pengulangan beberapa audio, pendengar tunggal, ketiadaan penilaian buta, dan ketidakpastian identitas sumber suara. Audit tidak digunakan untuk mengubah label acuan atau menyimpulkan penyebab kausal kegagalan.

Paragraf ini merupakan bahan pembahasan yang dapat ditinjau pembimbing. Persetujuan memulai atau mengesahkan bab skripsi tetap mengikuti bimbingan; paket ini tidak menulis ulang bab yang sudah ada.

## 7. Progres yang dapat dilaporkan

| Pekerjaan nomor 1–3 | Hasil 30 Oktober 2026 |
|---|---|
| Arsip dan ekspor audit | JSON asli, JSON terkoreksi, CSV 120 kasus, serta metadata sumber tersedia. |
| Analisis manusia–komputer | Tabel deskriptif menurut representasi, kondisi, dan jenis kegagalan; contoh kasus dan batas analisis tersedia. |
| Pembahasan dan progres | Laporan ini menyediakan pembahasan E5 dan draf paragraf naskah. |
| Integritas | Hanya satu nilai isian manusia berubah atas konfirmasi Fabio; sumber eksperimen tidak ditimpa. Bukti pemeriksaan akhir dicatat pada log dan manifest. |
| Publikasi GitHub | Status commit/push ditambahkan ke log setelah pemeriksaan lingkup perubahan. |

Pelaporan audit manusia dapat diperbarui menjadi **catatan tersedia 120/120, satu pendengar**, dengan batas dan ambiguitas di atas. Ini tidak otomatis mengesahkan seluruh Gate 4 atau seluruh naskah. Inferensi E4 tetap tidak diulang dan hasil reproduksi terdahulu dipertahankan sebagai riwayat.

## 8. Mengulangi pengolahan catatan di direktori baru

Jalankan dari akar proyek, gunakan direktori dan nama CSV yang belum ada:

```powershell
.\\.venv\\Scripts\\python.exe -B scripts/finalize_e5_human_review.py --review-json Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-20261030/E5_catatan_pendengaran_asli.json --output-dir Rencana-eksperimen-bimbingan/audit-pendengaran-E5/hasil-ulangan-baru --csv-output Rencana-eksperimen-bimbingan/audit-pendengaran-E5/E5_HASIL_ULASAN_ULANGAN.csv --confirm-e5-105-query-audible
```

Flag konfirmasi hanya digunakan karena Fabio sudah secara eksplisit mengoreksi E5_105 dalam percakapan ini. Skrip tidak mengisi atau menafsirkan pengamatan manusia baru. Pengulangan pengolahan ini tidak melibatkan audio, embedding, atau inferensi E0–E5.
'''


def main(review_json: Path, output_dir: Path, csv_output: Path, confirmed: bool) -> None:
    if not confirmed:
        raise ValueError('Explicit confirmation of E5_105 is required')
    review_json = review_json.resolve(); output_dir = output_dir.resolve(); csv_output = csv_output.resolve()
    if output_dir.parent != REVIEW.resolve() or csv_output.parent != REVIEW.resolve():
        raise ValueError('Outputs must stay directly inside the E5 audit area')
    if csv_output.suffix != '.csv':
        raise ValueError('csv-output must end in .csv')
    if csv_output.exists() or csv_output.with_suffix('.metadata.json').exists():
        raise FileExistsError(csv_output)
    if output_dir.exists() and any(p.name != 'LOG_AUDIT.md' for p in output_dir.iterdir()):
        raise FileExistsError('Use a new output folder, or a folder containing only its initial audit log')
    source_sheet = REVIEW / 'E5_AUDIT_PENDENGARAN.csv'
    raw = review_json.read_bytes(); original = json.loads(raw.decode('utf-8-sig'))
    source_rows = read_rows(source_sheet)
    validated = combine_reviews(source_rows, original, sha(source_sheet))
    if len(validated) != 120 or any(r['review_status'] != 'reviewed' for r in validated):
        raise ValueError('This closeout expects the full set of 120 reviewed cases')
    corrected = copy.deepcopy(original)
    before = next(r for r in original['reviews'] if r['case_id'] == 'E5_105')
    after = next(r for r in corrected['reviews'] if r['case_id'] == 'E5_105')
    if before['query_vocalisation_audible'] != 'uncertain':
        raise ValueError('Expected E5_105 original value uncertain; review source before applying amendment')
    after['query_vocalisation_audible'] = 'yes'
    differences = [(a['case_id'], key, a.get(key), b.get(key))
                   for a, b in zip(original['reviews'], corrected['reviews'])
                   for key in sorted(set(a) | set(b)) if a.get(key) != b.get(key)]
    if differences != [('E5_105', 'query_vocalisation_audible', 'uncertain', 'yes')]:
        raise ValueError('Unexpected semantic changes in human notes')
    merged = combine_reviews(source_rows, corrected, sha(source_sheet))
    output_dir.mkdir(exist_ok=True)
    log(output_dir, 'Validasi sumber, 120 ID, hash lembar/baris, kolom wajib, dan tanggal berzona waktu: lulus.')
    original_path = output_dir / 'E5_catatan_pendengaran_asli.json'
    with original_path.open('xb') as stream:
        stream.write(raw)
    corrected_path = output_dir / 'E5_catatan_pendengaran_terkoreksi.json'
    save_json(corrected_path, corrected)
    save_json(output_dir / 'koreksi_E5_105.json', {
        'schema': 'e5_confirmed_human_amendment_v1',
        'confirmation_date_local': '2026-10-30',
        'applied_at_utc': datetime.now(timezone.utc).isoformat(),
        'confirmed_by': 'Fabio Banyu Cyto', 'authorization_source': 'Explicit user confirmation in this chat',
        'confirmation_quote': 'itu kepencet yang ragu (aslinya terdengar jelas)',
        'case_id': 'E5_105', 'field': 'query_vocalisation_audible',
        'before': 'uncertain', 'after': 'yes',
        'source_sha256': sha(original_path), 'corrected_sha256': sha(corrected_path),
        'other_review_fields_unchanged': True, 'original_listening_timestamps_preserved': True,
    })
    log(output_dir, 'JSON asli diarsipkan identik byte. Satu koreksi terkonfirmasi E5_105: uncertain menjadi yes; teks serta tanggal asli dipertahankan.')
    import_reviews(corrected_path, csv_output, False)
    exported = read_rows(csv_output)
    if exported != merged:
        raise ValueError('Exported CSV differs from validated merge')
    for old, new in zip(source_rows, exported):
        if any(old[key] != new[key] for key in old if key not in FIELDS):
            raise ValueError('Experiment metadata changed during review import')
    log(output_dir, f'CSV baru {csv_output.name} dan metadata dibuat melalui importer aktif; 120 baris cocok persis dengan penggabungan tervalidasi.')
    stats = summary(exported)
    save_json(output_dir / 'ringkasan_pendengaran.json', stats)
    (output_dir / 'README.md').write_text(report(output_dir, exported, stats, csv_output), encoding='utf-8', newline='\n')
    log(output_dir, 'Analisis deskriptif dan laporan progres/pembahasan dibuat. R3 dipisahkan dari 90 kasus representasi audio; keterbatasan dan ambiguitas dipertahankan.')
    if review_json.read_bytes() != raw or sha(original_path) != hashlib.sha256(raw).hexdigest():
        raise ValueError('Original human source changed')
    paths = [p for p in output_dir.iterdir() if p.name != 'LOG_AUDIT.md']
    paths += [csv_output, csv_output.with_suffix('.metadata.json'), Path(__file__).resolve(), source_sheet]
    save_json(output_dir / 'manifest_artefak.json', {
        'schema': 'e5_human_audit_artifact_manifest_v1',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'source_git_head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'sha256': {p.relative_to(ROOT).as_posix(): sha(p) for p in sorted(paths)},
        'hash_exclusions': ['This manifest (self-reference)', 'LOG_AUDIT.md (append-only progress including publication steps)'],
        'validation': {'reviewed': 120, 'pending': 0, 'needs_follow_up': 0,
                       'human_field_changes': differences, 'experiment_columns_unchanged': True,
                       'original_download_unchanged': True},
        'scope': 'Human-note processing only; no audio/inference/metric/threshold/ground-truth changes',
    })
    log(output_dir, 'Manifest SHA-256 dibuat. JSON Downloads, lembar kosong sumber, serta kolom eksperimen dipastikan tetap utuh.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--review-json', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--csv-output', type=Path, required=True)
    parser.add_argument('--confirm-e5-105-query-audible', action='store_true')
    args = parser.parse_args()
    main(args.review_json, args.output_dir, args.csv_output, args.confirm_e5_105_query_audible)
