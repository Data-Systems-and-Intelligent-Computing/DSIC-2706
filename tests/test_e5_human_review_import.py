"""Reject E5 provenance errors and preserve pending cases when importing notes."""
import copy,unittest
from scripts.import_e5_human_review import combine_reviews
class HumanReviewImportTests(unittest.TestCase):
    def setUp(self):
        self.rows=[{'case_id':'E5_001','source_row_sha256':'row1','review_status':'pending','reviewer':''},{'case_id':'E5_002','source_row_sha256':'row2','review_status':'pending','reviewer':''}]
        self.note={'case_id':'E5_001','source_row_sha256':'row1','review_status':'reviewed','reviewer':'TEST FIXTURE ONLY','reviewed_at':'2026-10-16T00:00:00+07:00','query_vocalisation_audible':'uncertain','top1_vocalisation_audible':'uncertain','background_observation':'Synthetic test fixture; no listening performed','uncertainty_notes':'Synthetic fixture','auditory_interpretation':'Synthetic test fixture only'}
        self.payload={'schema':'e5_human_listening_review_v1','source_review_sheet_sha256':'sheet','reviews':[self.note]}
    def test_partial_import_preserves_pending_rows_and_inputs(self):
        before=copy.deepcopy(self.rows)
        result=combine_reviews(self.rows,self.payload,'sheet')
        self.assertEqual(result[0]['review_status'],'reviewed')
        self.assertEqual(result[1],before[1])
        self.assertEqual(self.rows,before)
    def test_wrong_source_and_case_hash_are_rejected(self):
        with self.assertRaises(ValueError):combine_reviews(self.rows,self.payload,'different_sheet')
        self.note['source_row_sha256']='wrong_row'
        with self.assertRaises(ValueError):combine_reviews(self.rows,self.payload,'sheet')
    def test_duplicate_or_incomplete_reviews_are_rejected(self):
        self.payload['reviews'].append(copy.deepcopy(self.note))
        with self.assertRaises(ValueError):combine_reviews(self.rows,self.payload,'sheet')
        self.payload['reviews'].pop();self.note['reviewer']=''
        with self.assertRaises(ValueError):combine_reviews(self.rows,self.payload,'sheet')
if __name__=='__main__':unittest.main()
