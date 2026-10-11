"""
CLI Entrypoint: scripts/run_experiment.py
Memfasilitasi eksekusi modular seluruh pipeline eksperimen (E0 s.d E5)
"""

import sys
import argparse
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def main():
    parser = argparse.ArgumentParser(description="DSIC-2706 Experiment Runner")
    parser.add_argument(
        "--experiment", 
        choices=["E0", "E1", "E2", "E3", "E4", "E5", "all"], 
        required=True,
        help="Pilih modul eksperimen yang akan dieksekusi"
    )
    args = parser.parse_args()

    print(f"[+] Menjalankan eksperimen: {args.experiment}")
    if args.experiment in ["E0", "E1", "E2", "E3", "all"]:
        from src.run_benchmark import run_full_benchmark
        run_full_benchmark()
    
    if args.experiment in ["E4", "all"]:
        print("[+] Mengeksekusi E4: Real Soundscape Domain Shift...")
        from notebooks.scratch_scripts.run_e4_domain_shift import evaluate_soundscape_domain_shift
        # atau panggil runner
        import subprocess
        subprocess.run([sys.executable, str(PROJECT_ROOT / "notebooks/scratch_scripts/run_e4_domain_shift.py")], check=True)

    if args.experiment in ["E5", "all"]:
        print("[+] Mengeksekusi E5: Failure Analysis...")
        from src.analyze_failures import extract_real_failures_from_raw
        extract_real_failures_from_raw()

    print(f"[+] Selesai mengeksekusi eksperimen {args.experiment}!")

if __name__ == "__main__":
    main()
