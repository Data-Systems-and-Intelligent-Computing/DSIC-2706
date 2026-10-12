// Latihan 3: MFCC -> ringkasan 38 angka -> cosine similarity -> peringkat.
// Implementasi pendidikan tersendiri, bukan konfigurasi E1 resmi repo lama.
// Seluruh perhitungan di memori, tanpa menulis hasil eksperimen.
const { prepareAudio } = require('./02_siapkan_audio.cjs');

const PARAMETERS = Object.freeze({
  rate: 32000, window: 800, hop: 320, fftSize: 1024,
  melFilters: 40, coefficients: 19, floor: 1e-12,
});

function fft(real, imaginary) {
  const n = real.length;
  if (n !== imaginary.length || n < 2 || (n & (n - 1))) {
    throw new Error('Ukuran FFT harus sama dan merupakan pangkat dua.');
  }
  for (let i = 1, j = 0; i < n; i++) {
    let bit = n >> 1;
    for (; j & bit; bit >>= 1) j ^= bit;
    j ^= bit;
    if (i < j) {
      [real[i], real[j]] = [real[j], real[i]];
      [imaginary[i], imaginary[j]] = [imaginary[j], imaginary[i]];
    }
  }
  for (let length = 2; length <= n; length *= 2) {
    const angle = -2 * Math.PI / length;
    const stepReal = Math.cos(angle);
    const stepImaginary = Math.sin(angle);
    for (let start = 0; start < n; start += length) {
      let wr = 1, wi = 0;
      for (let j = 0; j < length / 2; j++) {
        const u = start + j, v = u + length / 2;
        const tr = real[v] * wr - imaginary[v] * wi;
        const ti = real[v] * wi + imaginary[v] * wr;
        real[v] = real[u] - tr;
        imaginary[v] = imaginary[u] - ti;
        real[u] += tr;
        imaginary[u] += ti;
        const oldWr = wr;
        wr = oldWr * stepReal - wi * stepImaginary;
        wi = oldWr * stepImaginary + wi * stepReal;
      }
    }
  }
}

function mfccSummary(samples, sampleRate) {
  const p = PARAMETERS;
  if (sampleRate !== p.rate || samples.length < p.window ||
      !samples.every(Number.isFinite)) {
    throw new Error('Sampel atau sampling rate tidak sesuai protokol latihan.');
  }
  if (samples.reduce((sum, x) => sum + x * x, 0) / samples.length < 1e-20) {
    throw new Error('Potongan audio hening; kemiripan tidak dihitung.');
  }
  const toMel = hz => 2595 * Math.log10(1 + hz / 700);
  const toHz = mel => 700 * (10 ** (mel / 2595) - 1);
  const edges = Array.from({ length: p.melFilters + 2 }, (_, i) =>
    toHz(i * toMel(sampleRate / 2) / (p.melFilters + 1)));
  const bins = p.fftSize / 2 + 1;
  const filters = Array.from({ length: p.melFilters }, (_, m) =>
    Array.from({ length: bins }, (_, k) => {
      const hz = k * sampleRate / p.fftSize;
      return Math.max(0, Math.min(
        (hz - edges[m]) / (edges[m + 1] - edges[m]),
        (edges[m + 2] - hz) / (edges[m + 2] - edges[m + 1])));
    }));
  const window = Array.from({ length: p.window }, (_, j) =>
    0.5 - 0.5 * Math.cos(2 * Math.PI * j / (p.window - 1)));
  const count = Math.floor((samples.length - p.window) / p.hop) + 1;
  const frames = [];
  for (let t = 0; t < count; t++) {
    const real = new Float64Array(p.fftSize);
    const imaginary = new Float64Array(p.fftSize);
    for (let j = 0; j < p.window; j++) real[j] = samples[t * p.hop + j] * window[j];
    fft(real, imaginary);
    const power = Array.from({ length: bins }, (_, k) =>
      (real[k] ** 2 + imaginary[k] ** 2) / p.fftSize);
    const logMel = filters.map(filter => Math.log(Math.max(p.floor,
      filter.reduce((sum, weight, k) => sum + weight * power[k], 0))));
    // DCT-II ortonormal, C1-C19. C0 tidak digunakan pada latihan ini.
    frames.push(Array.from({ length: p.coefficients }, (_, i) =>
      Math.sqrt(2 / p.melFilters) * logMel.reduce((sum, value, m) =>
        sum + value * Math.cos(Math.PI * (i + 1) * (m + 0.5) / p.melFilters), 0)));
  }
  const mean = Array.from({ length: p.coefficients }, (_, k) =>
    frames.reduce((sum, frame) => sum + frame[k], 0) / count);
  const std = mean.map((mu, k) => Math.sqrt(
    frames.reduce((sum, frame) => sum + (frame[k] - mu) ** 2, 0) / count));
  return { vector: [...mean, ...std], frameCount: count };
}

function cosine(a, b) {
  if (!a.length || a.length !== b.length || ![...a, ...b].every(Number.isFinite)) {
    throw new Error('Representasi tidak valid.');
  }
  const normA = Math.sqrt(a.reduce((sum, x) => sum + x * x, 0));
  const normB = Math.sqrt(b.reduce((sum, x) => sum + x * x, 0));
  if (normA < 1e-12 || normB < 1e-12) throw new Error('Representasi bernorma nol.');
  return a.reduce((sum, x, i) => sum + x * b[i], 0) / (normA * normB);
}

async function main() {
  console.log('LATIHAN 3 - MFCC DAN KEMIRIPAN AUDIO');
  console.log('Membaca ulang potongan detik 0-5, mono, 32000 Hz.\n');
  const clips = await prepareAudio();
  const features = clips.map(clip => ({
    ...clip, ...mfccSummary(clip.samples, clip.sampleRate),
  }));
  for (const item of features) {
    console.log(`${item.name}: ${item.samples.length} sampel -> ${item.frameCount} bingkai -> ${item.vector.length} angka`);
  }
  const query = features.find(item => item.name === 'XC42472.mp3');
  if (!query) throw new Error('Query latihan tidak ditemukan.');
  // Skor hanya memakai vektor audio. Label spesies tidak digunakan.
  const ranking = features.filter(item => item !== query)
    .map(item => ({ name: item.name, score: cosine(query.vector, item.vector) }))
    .sort((a, b) => b.score - a.score || a.name.localeCompare(b.name));
  console.log('\nQuery: ' + query.name);
  console.log('Peringkat | Kandidat          | Skor cosine');
  ranking.forEach((item, i) => console.log(
    `${i + 1}         | ${item.name.padEnd(17)} | ${item.score.toFixed(6)}`));
  console.log('\nPERBANDINGAN KETIGA PASANGAN');
  console.log('Pasangan                       | Skor cosine');
  for (let i = 0; i < features.length; i++) {
    for (let j = i + 1; j < features.length; j++) {
      const a = features[i], b = features[j];
      const names = `${a.name} - ${b.name}`;
      console.log(`${names.padEnd(30)} | ${cosine(a.vector, b.vector).toFixed(6)}`);
    }
  }
  console.log('\nSkor lebih tinggi = representasi lebih mirip; bukan probabilitas spesies.');
  console.log('Protokol: Hann 25 ms, hop 10 ms, FFT 1024, 40 filter Mel (0-16000 Hz).');
  console.log('MFCC C1-C19, tanpa pre-emphasis; 19 rata-rata + 19 simpangan baku = 38 angka.');
  console.log('Latihan dua kandidat, bukan evaluasi seluruh gallery atau bukti ketahanan derau.');
  console.log('Tidak ada file audio atau hasil eksperimen yang ditulis.');
}

module.exports = { fft, mfccSummary, cosine, PARAMETERS };
if (require.main === module) {
  main().catch(error => {
    console.error('GAGAL: ' + error.message);
    console.error('Kirim pesan ini ke chat; tidak perlu menginstal sendiri.');
    process.exitCode = 1;
  });
}
