"""Small synthetic fixtures only; these tests do not perform human listening."""
import unittest
from pathlib import Path

from scripts.finalize_e5_human_review import ROOT, audibility, main, summary


def row(case, representation, query_audible, top1_audible):
    return {
        'case_id': case, 'representation': representation,
        'query_vocalisation_audible': query_audible,
        'top1_vocalisation_audible': top1_audible,
        'query_id': 'SYNTHETIC_QUERY', 'condition': 'SYNTHETIC_CONDITION',
        'top1_recording_id': 'SYNTHETIC_GALLERY',
        'reviewed_at': '2026-10-29T18:00:00+00:00',
        'reviewer': 'SYNTHETIC FIXTURE ONLY', 'review_status': 'reviewed',
        'failure_mode_computational': 'SYNTHETIC_MODE',
    }


class E5HumanFinalizeTests(unittest.TestCase):
    def test_audibility_keeps_no_and_uncertain_separate(self):
        rows = [row('A', 'R0', 'yes', 'yes'), row('B', 'R1', 'no', 'uncertain')]
        counts = audibility(rows)
        self.assertEqual(counts['n_cases'], 2)
        self.assertEqual(counts['query_vocalisation_audible'], {'yes': 1, 'no': 1, 'uncertain': 0})
        self.assertEqual(counts['top1_vocalisation_audible'], {'yes': 1, 'no': 0, 'uncertain': 1})
        self.assertEqual(counts['both_audible_yes'], 1)

    def test_summary_separates_control_and_reports_repeated_audio(self):
        rows = [row('A', 'R0', 'yes', 'yes'), row('B', 'R3', 'no', 'uncertain')]
        result = summary(rows)
        self.assertEqual(result['overall']['n_cases'], 2)
        self.assertEqual(result['audio_representations_R0_R1_R2']['n_cases'], 1)
        self.assertEqual(result['unique_queries'], 1)
        self.assertEqual(result['unique_query_condition_pairs'], 1)
        self.assertEqual(len(result['within_listener_query_category_differences']), 1)
        self.assertEqual(len(result['within_listener_top1_category_differences']), 1)
        self.assertEqual(rows[1]['query_vocalisation_audible'], 'no')

    def test_correction_requires_explicit_confirmation_before_io(self):
        with self.assertRaisesRegex(ValueError, 'Explicit confirmation'):
            main(Path('not-read.json'), ROOT / 'not-created', ROOT / 'not-created.csv', False)

    def test_output_cannot_escape_audit_area(self):
        with self.assertRaisesRegex(ValueError, 'Outputs must stay'):
            main(Path('not-read.json'), ROOT / 'not-created', ROOT / 'not-created.csv', True)


if __name__ == '__main__':
    unittest.main()
