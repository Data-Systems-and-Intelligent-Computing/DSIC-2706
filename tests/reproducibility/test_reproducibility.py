import os
import sys
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.verify_reproducibility import verify_single_command_reproducibility


def test_reproducibility_deterministic_check():
    summary = verify_single_command_reproducibility(rep_code="R2", test_snr=0)
    assert summary is not None
    assert "mAP@10" in summary
    assert summary["mAP@10"] > 0.10, "mAP@10 untuk R2 pada SNR 0 dB harus > 0.10"
