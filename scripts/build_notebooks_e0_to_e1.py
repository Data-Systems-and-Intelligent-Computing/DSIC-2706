"""Create runnable, code-only notebooks through E1-R0.

The notebooks invoke the project virtual environment explicitly so their
execution does not depend on the Jupyter kernel's installed packages.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOKS = ROOT / "notebooks"


def code_cell(source: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": source}


def write_notebook(name: str, cells: list[str]) -> None:
    payload = {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}, "language_info": {"name": "python"}},
        "cells": [code_cell(cell) for cell in cells],
    }
    (NOTEBOOKS / name).write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


SETUP = """from pathlib import Path
import os
import subprocess

ROOT = Path.cwd()
if not (ROOT / 'scripts').exists():
    ROOT = Path(r'D:\\FILE AND TASK\\TA')
PYTHON = ROOT / '.venv' / 'Scripts' / 'python.exe'
assert ROOT.exists() and PYTHON.exists(), (ROOT, PYTHON)
RUN_ENV = os.environ.copy()
RUN_ENV['MPLBACKEND'] = 'Agg'
RUN_ENV['MPLCONFIGDIR'] = str(ROOT / 'results' / '.mplconfig')
print(ROOT)
print(PYTHON)
"""


def run_script(script: str) -> str:
    return f"""subprocess.run([str(PYTHON), '-B', 'scripts/{script}'], cwd=ROOT, env=RUN_ENV, check=True)
"""


DISPLAY_E0 = """from IPython.display import Image, display
run = max((ROOT / 'results' / 'reproductions').glob('E0_*'), key=lambda path: path.stat().st_mtime)
print(run)
display(Image(filename=str(run / 'figures' / 'e0_audio_properties.png')))
print((run / 'tables' / 'summary.csv').read_text(encoding='utf-8'))
"""

DISPLAY_EDA = """from IPython.display import Image, display
run = max((ROOT / 'results' / 'reproductions').glob('EDA_*'), key=lambda path: path.stat().st_mtime)
print(run)
display(Image(filename=str(run / 'figures' / 'eda_overview.png')))
print((run / 'tables' / 'summary_by_source.csv').read_text(encoding='utf-8'))
"""

DISPLAY_E1 = """import json
run = max((ROOT / 'results' / 'reproductions').glob('E1_R0_*'), key=lambda path: path.stat().st_mtime)
metadata = json.loads((run / 'metadata.json').read_text(encoding='utf-8'))
print(run)
print(json.dumps(metadata['summary'], indent=2))
print((run / 'tables' / 'per_query.csv').read_text(encoding='utf-8').splitlines()[:6])
"""


PREPROCESS = """snippet = '''
from pathlib import Path
from src.preprocess import TARGET_SR, TARGET_SAMPLES, DURATION_SEC, compute_rms, preprocess_audio

root = Path.cwd()
files = [
    root / 'data/xeno_canto_indonesia/savnig1/XC42472.mp3',
    root / 'data/xeno_canto_indonesia/savnig1/XC120964.mp3',
    root / 'data/xeno_canto_indonesia/ashtai1/XC1003648.mp3',
]
for path in files:
    audio = preprocess_audio(str(path))
    print(path.name, len(audio), TARGET_SR, DURATION_SEC, compute_rms(audio))
assert all(len(preprocess_audio(str(path)) ) == TARGET_SAMPLES for path in files)
'''
subprocess.run([str(PYTHON), '-B', '-c', snippet], cwd=ROOT, env=RUN_ENV, check=True)
"""


def main() -> None:
    write_notebook("01_Preprocessing.ipynb", [SETUP, PREPROCESS])
    write_notebook("02_E0_Preprocessing_Audit.ipynb", [SETUP, run_script("run_e0_preprocessing_verification.py"), DISPLAY_E0])
    write_notebook("03_EDA_Physical_Audio.ipynb", [SETUP, run_script("run_eda_formal.py"), DISPLAY_EDA])
    write_notebook("04_E1_Clean_R0.ipynb", [SETUP, run_script("run_e1_clean_r0.py"), DISPLAY_E1])
    print(f"Created runnable notebooks in {NOTEBOOKS}")


if __name__ == "__main__":
    main()
