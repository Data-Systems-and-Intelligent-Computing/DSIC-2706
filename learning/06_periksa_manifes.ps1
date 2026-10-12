$ErrorActionPreference = 'Stop'
$learningPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$learningScript = Join-Path $PSScriptRoot '..\scripts\audit_manifests.py'

if (-not (Test-Path -LiteralPath $learningPython -PathType Leaf)) {
    throw 'Python bawaan aplikasi tidak ditemukan. Kirim pesan ini ke chat.'
}

& $learningPython -B $learningScript
if ($LASTEXITCODE -ne 0) {
    Write-Host 'Audit menemukan masalah yang harus diperiksa. Kirim hasilnya ke chat; jangan hapus atau mengubah data sendiri.'
    exit $LASTEXITCODE
}
