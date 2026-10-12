// Satu query melawan subset gallery yang dipilih sebelum menghitung skor.
// Tidak menulis ke results/, paper/, atau file audio.
const fs = require('node:fs/promises');
const path = require('node:path');
const crypto = require('node:crypto');
const { prepareAudio } = require('./02_siapkan_audio.cjs');
const { mfccSummary, cosine } = require('./03_hitung_kemiripan.cjs');
const ROOT = path.resolve(__dirname, '..');
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex');

function retrievalMetrics(ranking, targetSpecies, k = 10) {
  if (!Number.isInteger(k) || k < 1 || ranking.length < k) {
    throw new Error('k harus positif dan tidak melebihi jumlah kandidat.');
  }
  if (new Set(ranking.map(row => row.recording_id)).size !== ranking.length) {
    throw new Error('ID kandidat duplikat.');
  }
  const relevant = ranking.filter(row => row.species_key === targetSpecies).length;
  if (!relevant) throw new Error('Gallery tidak memiliki rekaman relevan.');
  const hits = ranking.slice(0, k).filter(row => row.species_key === targetSpecies).length;
  return {
    relevant, hits, k,
    top1: Number(ranking[0].species_key === targetSpecies),
    precision: hits / k,
    recall: hits / relevant,
  };
}

async function main() {
  console.log('LATIHAN 4 - SATU QUERY MENCARI DI 30 REKAMAN');
  const plan = JSON.parse(await fs.readFile(path.join(__dirname, 'gallery_latihan_30.json'), 'utf8'));
  const manifest = await fs.readFile(path.join(ROOT, 'data/manifests/dataset_split.csv'));
  if (hash(manifest) !== plan.manifest_sha256) {
    throw new Error('Manifes berubah sejak kandidat dipilih. Kirim pesan ini ke chat.');
  }
  if (plan.gallery.length !== 30 || plan.query.split_role !== 'query_clean' ||
      plan.gallery.some(row => row.split_role !== 'gallery')) {
    throw new Error('Peran/jumlah rekaman pada daftar latihan tidak sesuai.');
  }
  const records = [plan.query, ...plan.gallery];
  const names = new Map();
  const hashes = new Set();
  const fileList = [];
  for (const row of records) {
    const prefix = 'data/xeno_canto_indonesia/';
    if (!row.file_path.startsWith(prefix)) throw new Error('Folder audio tidak sesuai.');
    const audioRoot = path.resolve(ROOT, prefix);
    const fullPath = path.resolve(ROOT, row.file_path);
    if (!fullPath.toLowerCase().startsWith((audioRoot + path.sep).toLowerCase())) {
      throw new Error('Path audio keluar dari folder target.');
    }
    const name = path.basename(fullPath);
    if (name !== row.recording_id + '.mp3' || names.has(name)) {
      throw new Error('Nama atau ID rekaman tidak unik/sesuai.');
    }
    const checksum = hash(await fs.readFile(fullPath));
    if (checksum !== row.sha256 || hashes.has(checksum)) {
      throw new Error(name + ': checksum berubah atau audio duplikat.');
    }
    names.set(name, row);
    hashes.add(checksum);
    fileList.push([row === plan.query ? 'Query' : 'Gallery', row.file_path.slice(prefix.length)]);
  }
  console.log('File/manifes sesuai checksum. Membaca 31 potongan audio; tunggu sebentar.');
  const clips = await prepareAudio(fileList, (done, total) => {
    if (done % 5 === 0 || done === total) console.log(`Audio siap: ${done}/${total}`);
  });
  const features = clips.map((clip, index) => {
    const result = { name: clip.name, vector: mfccSummary(clip.samples, clip.sampleRate).vector };
    if ((index + 1) % 5 === 0 || index === clips.length - 1) {
      console.log(`MFCC selesai: ${index + 1}/${clips.length} rekaman`);
    }
    return result;
  });
  const queryName = plan.query.recording_id + '.mp3';
  const query = features.find(row => row.name === queryName);
  if (!query) throw new Error('Fitur query tidak ditemukan.');
  // Pengurutan hanya menggunakan fitur audio dan nama sebagai pemecah seri.
  const scored = features.filter(row => row !== query)
    .map(row => ({ name: row.name, score: cosine(query.vector, row.vector) }))
    .sort((a, b) => b.score - a.score || a.name.localeCompare(b.name));
  // Label baru digabungkan setelah pengurutan untuk menilai relevansi.
  const ranking = scored.map(row => ({ ...row, ...names.get(row.name) }));
  const metrics = retrievalMetrics(ranking, plan.query.species_key, 10);
  if (metrics.relevant !== 15) throw new Error('Jumlah relevan pada latihan harus 15.');
  console.log(`\nQuery: ${plan.query.recording_id} (${plan.query.scientific_name})`);
  console.log('Gallery latihan: 30; relevan: 15; berbeda spesies: 15.');
  console.log('\nSEPULUH HASIL TERATAS');
  console.log('Urutan | Rekaman    | Spesies | Skor     | Relevan');
  ranking.slice(0, 10).forEach((row, i) => console.log(
    `${String(i + 1).padEnd(6)} | ${row.recording_id.padEnd(10)} | ${row.species_key.padEnd(7)} | ${row.score.toFixed(6)} | ${row.species_key === plan.query.species_key ? 'YA' : 'TIDAK'}`));
  console.log(`\nTop-1       : ${metrics.top1 ? 'BENAR' : 'SALAH'} untuk satu query ini`);
  console.log(`Relevan @10 : ${metrics.hits} dari 10 hasil`);
  console.log(`Precision@10: ${metrics.hits}/10 = ${(metrics.precision * 100).toFixed(2)}%`);
  console.log(`Recall@10   : ${metrics.hits}/15 = ${(metrics.recall * 100).toFixed(2)}%`);
  console.log('\nIni subset 30 kandidat; hasil tidak mewakili gallery lengkap 673 rekaman.');
  console.log('MFCC dan potongan detik 0-5 sama dengan latihan 03.');
  console.log('Bukan eksperimen resmi atau bukti ketahanan derau. Tidak ada hasil yang ditulis.');
}

module.exports = { retrievalMetrics };
if (require.main === module) {
  main().catch(error => {
    console.error('GAGAL: ' + error.message);
    console.error('Kirim pesan ini ke chat.');
    process.exitCode = 1;
  });
}
