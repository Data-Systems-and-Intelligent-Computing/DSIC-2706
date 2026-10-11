"""
CLI Script: scripts/run_bootstrap.py
Entrypoint untuk mereproduksi uji statistik inferensial bootstrap resampling
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.bootstrap_inference import run_paired_bootstrap

if __name__ == "__main__":
    print("[*] Menjalankan Uji Inferensial Bootstrap Resampling...")
    run_paired_bootstrap()
