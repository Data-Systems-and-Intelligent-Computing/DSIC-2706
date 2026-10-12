$ErrorActionPreference = 'Stop'
$learningNode = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
$learningScript = Join-Path $PSScriptRoot '03_hitung_kemiripan.cjs'

if (-not (Test-Path -LiteralPath $learningNode -PathType Leaf)) {
    throw 'Alat pembaca audio tidak ditemukan. Kirim pesan ini ke chat.'
}

& $learningNode $learningScript
if ($LASTEXITCODE -ne 0) {
    throw 'Perhitungan kemiripan belum berhasil. Kirim keluaran terminal ke chat.'
}
