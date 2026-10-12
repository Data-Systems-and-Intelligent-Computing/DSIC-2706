from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / 'notebooks'
SCRIPTS = ROOT / 'scripts'


def direct_source(filename: str) -> str:
    source = (SCRIPTS / filename).read_text(encoding='utf-8-sig')
    source = source.replace('from __future__ import annotations\n', '')
    source = re.split(r'\nif __name__ == [\"\']__main__[\"\']:\s*', source, maxsplit=1)[0].rstrip()
    return f'''# Kode {filename} ditempatkan langsung di notebook ini.\n# Entry point CLI tidak dipanggil otomatis agar hasil valid tidak tertimpa.\n__file__ = str(ROOT / "scripts" / "{filename}")\n\n{source}\n\nprint("Kode {filename} telah dimuat di notebook.")\n'''

for notebook_name, runner in [
    ('02_E0_Preprocessing_Audit.ipynb', 'run_e0_preprocessing_verification.py'),
    ('03_EDA_Physical_Audio.ipynb', 'run_eda_formal.py'),
]:
    path = NOTEBOOKS / notebook_name
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    data['cells'].insert(1, {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": direct_source(runner)})
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('Updated', path)
