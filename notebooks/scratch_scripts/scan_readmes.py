import sys
from pathlib import Path

readme_files = [
    'data/README.md',
    'docs/README.md',
    'Rencana-eksperimen-bimbingan/README.md',
    'Rencana-eksperimen-bimbingan/minggu-1/README.md',
    'Rencana-eksperimen-bimbingan/minggu-2/README.md',
    'Rencana-eksperimen-bimbingan/minggu-3/README.md',
    'Rencana-eksperimen-bimbingan/minggu-4/README.md',
    'experiments/E0_pipeline_sanity/README.md',
    'experiments/E1_clean_retrieval/README.md',
    'experiments/E2_noise_robustness/README.md',
    'experiments/E3_open_set_threshold/README.md',
    'experiments/E4_real_soundscape/README.md',
    'experiments/E5_failure_analysis/README.md',
    'experiments/E6_external_validation/README.md',
]

for rf in readme_files:
    p = Path(rf)
    if not p.exists():
        continue
    content = p.read_text(encoding='utf-8')
    lines = content.splitlines()
    print(f"FILE: {rf} ({len(lines)} lines)")
    
    # Check for keywords
    keywords = ['14 spesies', '16 spesies', 'pink noise', 'pink_noise', 'BirdCLEF', 'AudioMoth', 'Gate 1', 'Gate 1-R', 'Sumatera', 'Pantanal']
    found = [k for k in keywords if k.lower() in content.lower()]
    print(f"  Keywords detected: {found}")
    print(f"  First 5 lines:")
    for l in lines[:5]:
        print(f"    {l[:100]}")
    print("-" * 50)
