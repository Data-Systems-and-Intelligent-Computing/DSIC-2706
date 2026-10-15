"""Protect E5 case provenance and the already-published 120-case selection."""
import unittest
from pathlib import Path
import pandas as pd
from scripts.run_e5_diagnostics import select_failure_cases
ROOT=Path(__file__).resolve().parents[1]
class E5CaseSelectionTests(unittest.TestCase):
    def test_group_labels_and_source_rows_survive_selection(self):
        frame=pd.DataFrame([
            {'query_id':f'q{i}','source_experiment':'E2' if i<6 else 'E4','representation':'R0' if i<3 or i==6 else 'R1','condition':'Clean','failure_mode':'Total retrieval collapse','max_score':i/10}
            for i in range(7)
        ])
        before=frame.copy(deep=True)
        selected=select_failure_cases(frame)
        self.assertEqual(len(selected),4)
        self.assertTrue({'representation','condition','failure_mode'}.issubset(selected.columns))
        self.assertEqual(selected.groupby('representation').size().to_dict(),{'R0':2,'R1':2})
        self.assertTrue(selected.source_experiment.eq('E2').all())
        for row in selected.itertuples(index=False):
            original=frame.loc[frame.query_id.eq(row.query_id)].iloc[0]
            self.assertEqual(row.max_score,original.max_score)
        pd.testing.assert_frame_equal(frame,before)

    def test_historical_120_case_membership_and_values_unchanged(self):
        full=pd.read_csv(ROOT/'results/reproductions/E5_diagnostics_20261012T091512_868500Z/tables/all_query_diagnostics.csv',low_memory=False)
        historical=pd.read_csv(ROOT/'results/tables/16_e5_selected_case_manifest.csv',low_memory=False)
        selected=select_failure_cases(full.loc[full.failure_mode.ne('Accepted correct')])
        self.assertEqual(len(selected),120)
        pd.testing.assert_frame_equal(selected[historical.columns].reset_index(drop=True),historical.reset_index(drop=True),check_dtype=False,rtol=1e-12,atol=1e-12)
if __name__=='__main__':unittest.main()
