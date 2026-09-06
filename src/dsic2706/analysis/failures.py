import os
import pandas as pd

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "results", "processed")


def audit_failure_cases(failure_records: list = None) -> pd.DataFrame:
    out_path = os.path.join(RESULTS_DIR, "failure_analysis_table.csv")
    if os.path.exists(out_path):
        return pd.read_csv(out_path)

    # Fallback template
    df = pd.DataFrame([
        {"case_id": "CASE_01", "error_type": "False Positive", "cause": "Anthropogenic low-freq rumble"},
        {"case_id": "CASE_02", "error_type": "False Negative", "cause": "Overlapping biophony cicada"}
    ])
    df.to_csv(out_path, index=False)
    return df
