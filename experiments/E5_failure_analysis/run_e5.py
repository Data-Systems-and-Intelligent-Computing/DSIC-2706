"""
E5: Failure Analysis Audit
- Mengaudit minimal 20 kasus kegagalan retrieval (False Positive & False Negative).
- Mengklasifikasikan penyebab: low SNR, interferensi antropogenik, vokalisasi serupa, dll.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.analyze_failures import audit_failure_cases


def run_e5_failures():
    print("=" * 70)
    print("[*] MENJALANKAN EXPERIMENT E5: FAILURE ANALYSIS")
    print("=" * 70)

    df_fail = audit_failure_cases([])
    print(f"[+] Berhasil mengaudit {len(df_fail)} kasus kegagalan retrieval.")
    print("=" * 70)
    return df_fail


if __name__ == "__main__":
    run_e5_failures()
