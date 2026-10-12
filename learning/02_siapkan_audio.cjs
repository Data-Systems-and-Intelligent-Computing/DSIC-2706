// Latihan 2: dekode, resample, rata-ratakan kanal, dan ambil detik 0-5.
// Menggunakan decoder Edge yang sudah terpasang; tidak mengunduh paket.
// Tidak menulis audio, fitur, atau hasil eksperimen ke disk.
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');
const { createRequire } = require('node:module');

const ROOT = path.resolve(__dirname, '..');
const RATE = 32000;
const SECONDS = 5;
const FILES = [
  ['Query', 'savnig1/XC42472.mp3'],
  ['Gallery relevan', 'savnig1/XC120964.mp3'],
  ['Gallery berbeda', 'ashtai1/XC1003648.mp3'],
];

async function prepareAudio(fileList = FILES, onProgress = () => {}) {
  const dependencies = path.join(os.homedir(), '.cache', 'codex-runtimes',
    'codex-primary-runtime', 'dependencies');
  const bundledRequire = createRequire(path.join(dependencies, 'node',
    'node_modules', '_learning_entry.cjs'));
  const { chromium } = bundledRequire('playwright');
  const edgeCandidates = [
    path.join(process.env['ProgramFiles(x86)'] || 'C:/Program Files (x86)',
      'Microsoft/Edge/Application/msedge.exe'),
    path.join(process.env.ProgramFiles || 'C:/Program Files',
      'Microsoft/Edge/Application/msedge.exe'),
  ];
  let executablePath;
  for (const candidate of edgeCandidates) {
    try { await fs.access(candidate); executablePath = candidate; break; }
    catch { /* Coba lokasi Edge berikutnya. */ }
  }
  if (!executablePath) throw new Error('Microsoft Edge tidak ditemukan.');

  const inputs = [];
  for (const [role, relative] of fileList) {
    const dataRoot = path.join(ROOT, 'data/xeno_canto_indonesia');
    const audioPath = path.resolve(dataRoot, relative);
    if (!audioPath.toLowerCase().startsWith((dataRoot + path.sep).toLowerCase())) {
      throw new Error('Path audio di luar folder target.');
    }
    const bytes = await fs.readFile(audioPath);
    inputs.push({ role, name: path.basename(relative), base64: bytes.toString('base64') });
  }
  const browser = await chromium.launch({
    executablePath, headless: true,
    args: ['--disable-background-networking', '--disable-component-update'],
  });
  try {
    const page = await browser.newPage();
    await page.route('**/*', route => route.abort());
    // Satu konteks dipakai ulang; tiap kiriman hanya memuat satu rekaman.
    await page.evaluate(rate => {
      window.learningContext = new OfflineAudioContext(2, 1, rate);
    }, RATE);
    const results = [];
    for (const input of inputs) {
      let timer;
      try {
        const clip = await Promise.race([
          page.evaluate(async ({ input, rate, seconds }) => {
      const targetLength = rate * seconds;
        const bytes = Uint8Array.from(atob(input.base64), char => char.charCodeAt(0));
        // decodeAudioData mendekode MP3/WAV berdasarkan isi dan meresample
        // ke sampling rate konteks. Stereo belum digabung pada tahap ini.
        const decoded = await window.learningContext.decodeAudioData(bytes.buffer);
        if (decoded.sampleRate !== rate) throw new Error('Resampling tidak sesuai.');
        if (![1, 2].includes(decoded.numberOfChannels)) {
          throw new Error(input.name + ': hanya mono/stereo yang didukung.');
        }
        if (decoded.length < targetLength) {
          throw new Error(input.name + ': durasi kurang dari lima detik.');
        }
        // Mono = (kanal kiri + kanal kanan) / 2. Tidak memilih kanal
        // berdasarkan amplitudo dan tidak menormalisasi volume per rekaman.
        const left = decoded.getChannelData(0);
        const right = decoded.numberOfChannels === 2 ? decoded.getChannelData(1) : left;
        const mono = new Float32Array(targetLength);
        for (let i = 0; i < targetLength; i++) {
          mono[i] = (left[i] + right[i]) / 2;
          if (!Number.isFinite(mono[i])) throw new Error('Sampel audio tidak valid.');
        }
        return {
          name: input.name, role: input.role, sampleRate: rate,
          channels: 1, seconds, samples: Array.from(mono),
        };
          }, { input, rate: RATE, seconds: SECONDS }),
          new Promise((_, reject) => {
            timer = setTimeout(() => reject(new Error(input.name + ': decoder melewati 30 detik.')), 30000);
          }),
        ]);
        results.push(clip);
        onProgress(results.length, inputs.length);
      } finally {
        clearTimeout(timer);
      }
    }
    return results;
  } finally {
    await browser.close();
  }
}

async function main() {
  console.log('LATIHAN 2 - MENYAMAKAN BENTUK AUDIO');
  console.log('Tunggu sebentar; decoder membaca tiga file lokal.\n');
  const clips = await prepareAudio();
  for (const clip of clips) {
    console.log(`File          : ${clip.name}`);
    console.log(`Peran latihan : ${clip.role}`);
    console.log(`Potongan      : detik 0 sampai ${clip.seconds}`);
    console.log(`Sampling rate : ${clip.sampleRate} Hz`);
    console.log(`Kanal         : ${clip.channels} (mono)`);
    console.log(`Jumlah sampel : ${clip.samples.length}`);
    console.log();
  }
  console.log('Semua potongan memiliki 5 x 32000 = 160000 sampel.');
  console.log('Potongan hanya ada di memori; tidak disimpan sebagai file.');
  console.log('Audio asli tetap utuh. Belum menghitung MFCC atau skor kemiripan.');
}

module.exports = { prepareAudio };
if (require.main === module) {
  main().catch(error => {
    console.error('GAGAL: ' + error.message);
    console.error('Kirim pesan ini ke chat; tidak perlu menginstal sendiri.');
    process.exitCode = 1;
  });
}
