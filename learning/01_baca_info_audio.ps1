# Jalankan Python yang sudah disediakan aplikasi; tidak menginstal paket.
$ErrorActionPreference = 'Stop'
$learningPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$learningScript = Join-Path $PSScriptRoot '01_baca_info_audio.py'

if (-not (Test-Path -LiteralPath $learningPython -PathType Leaf)) {
    throw 'Python bawaan aplikasi tidak ditemukan. Kirim pesan ini ke chat; tidak perlu menginstal sendiri.'
}

& $learningPython -B $learningScript
if ($LASTEXITCODE -ne 0) {
    throw 'Pembacaan audio belum berhasil. Kirim keluaran terminal ke chat.'
}
