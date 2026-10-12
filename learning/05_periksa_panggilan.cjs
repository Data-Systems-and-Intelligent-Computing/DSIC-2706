// Diagnostik dua spesies berbeda, dengan batas potongan sebelum skoring.
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const { prepareAudio } = require('./02_siapkan_audio.cjs');
const { mfccSummary, cosine } = require('./03_hitung_kemiripan.cjs');
const ROOT = path.resolve(__dirname, '..');

function cropCall(clip, bounds) {
  if (!Number.isFinite(bounds.start_sec) || !Number.isFinite(bounds.end_sec) ||
      bounds.start_sec < 0 || bounds.end_sec <= bounds.start_sec) {
    throw new Error('Batas potongan tidak valid.');
  }
  const start = Math.round(bounds.start_sec * clip.sampleRate);
  const end = Math.round(bounds.end_sec * clip.sampleRate);
  if (end > clip.samples.length) throw new Error('Potongan di luar audio yang dibaca.');
  return clip.samples.slice(start, end);
}

async function main() {
  console.log('LATIHAN 5 - MEMERIKSA BAGIAN PANGGILAN');
  const bounds = JSON.parse(await fs.readFile(path.join(__dirname, '05_batas_panggilan.json'), 'utf8'));
  const plan = JSON.parse(await fs.readFile(path.join(__dirname, 'gallery_latihan_30.json'), 'utf8'));
  const records = [plan.query, ...plan.gallery];
  const ids = new Set([...bounds.query.map(row => row.recording_id), bounds.candidate.recording_id]);
  const selected = [...ids].map(id => {
    const row = records.find(record => record.recording_id === id);
    if (!row) throw new Error('Rekaman tidak ditemukan dalam daftar latihan: ' + id);
    return row;
  });
  const fileList = [];
  const prefix = 'data/xeno_canto_indonesia/';
  const audioRoot = path.resolve(ROOT, prefix);
  for (const row of selected) {
    const fullPath = path.resolve(ROOT, row.file_path);
    if (!row.file_path.startsWith(prefix) ||
        !fullPath.toLowerCase().startsWith((audioRoot + path.sep).toLowerCase())) {
      throw new Error('Path di luar folder audio target.');
    }
    const hash = crypto.createHash('sha256').update(await fs.readFile(fullPath)).digest('hex');
    if (hash !== row.sha256) throw new Error(row.recording_id + ': checksum audio berubah.');
    fileList.push([row.recording_id, row.file_path.slice(prefix.length)]);
  }
  const clips = await prepareAudio(fileList);
  const byId = new Map(clips.map(clip => [path.parse(clip.name).name, clip]));
  const targetClip = byId.get(bounds.candidate.recording_id);
  const targetSamples = cropCall(targetClip, bounds.candidate);
  const expectedLength = Math.round(bounds.duration_sec * targetClip.sampleRate);
  if (targetSamples.length !== expectedLength) throw new Error('Durasi kandidat tidak sesuai.');
  const targetFeatures = mfccSummary(targetSamples, targetClip.sampleRate);
  const targetFull = mfccSummary(targetClip.samples, targetClip.sampleRate);
  console.log('Mono 32000 Hz; parameter MFCC sama dengan latihan 03/04.');
  console.log(`Kandidat ${bounds.candidate.recording_id}: ${bounds.candidate.start_sec}-${bounds.candidate.end_sec} detik.`);
  for (const item of bounds.query) {
    const queryClip = byId.get(item.recording_id);
    const querySamples = cropCall(queryClip, item);
    if (querySamples.length !== expectedLength) throw new Error('Durasi query tidak sesuai.');
    const queryFeatures = mfccSummary(querySamples, queryClip.sampleRate);
    const baseline = cosine(mfccSummary(queryClip.samples, queryClip.sampleRate).vector, targetFull.vector);
    const score = cosine(queryFeatures.vector, targetFeatures.vector);
    console.log(`\n${item.name} (${item.recording_id}): ${item.start_sec}-${item.end_sec} detik`);
    console.log(`Ukuran masing-masing: ${querySamples.length} sampel, ${queryFeatures.frameCount} bingkai, 38 angka`);
    console.log(`Skor potongan 5 detik    : ${baseline.toFixed(6)}`);
    console.log(`Skor potongan 0,6 detik  : ${score.toFixed(6)}`);
    console.log(`Selisih terhadap 5 detik : ${(score - baseline).toFixed(6)}`);
  }
  console.log('\nKedua hasil dilaporkan, bukan hanya skor yang mendukung dugaan.');
  console.log('Potongan berpusat pada panggilan, tetapi latar belum dihilangkan.');
  console.log('Durasi/bingkai berbeda dari baseline; perubahan skor tidak membuktikan penyebab derau.');
  console.log('Tidak ada audio/hasil eksperimen yang ditulis atau ditimpa.');
}

module.exports = { cropCall };
if (require.main === module) {
  main().catch(error => {
    console.error('GAGAL: ' + error.message);
    console.error('Kirim pesan ini ke chat.');
    process.exitCode = 1;
  });
}
