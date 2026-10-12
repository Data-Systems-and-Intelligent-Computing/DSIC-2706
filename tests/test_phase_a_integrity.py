"""Small synthetic regression tests for Phase A; no project audio is read."""

import unittest
from unittest.mock import patch
import sys
import types

import numpy as np
import pandas as pd

# The bundled learning runtime does not include PyYAML. This temporary test
# stub only allows import of the constants; it never loads or processes audio.
try:
    import yaml  # noqa: F401
except ModuleNotFoundError:
    sys.modules["yaml"] = types.SimpleNamespace(safe_load=lambda _stream: {})

from src.e3_alignment import align_known_noisy_scores
from src.embeddings import AudioRepresentationExtractor, R3_CONTROL_VERSION
try:
    from src import mix_noise
    MIX_IMPORT_ERROR = None
except ModuleNotFoundError as error:
    mix_noise = None
    MIX_IMPORT_ERROR = error


class E3AlignmentTests(unittest.TestCase):
    def test_scores_follow_query_id_not_csv_row_order(self):
        raw = pd.DataFrame({
            "query_id": ["Q2", "Q1"],
            "max_similarity_score": [0.2, 0.9],
            "noise_file": ["second.wav", "first.wav"],
        })
        aligned = align_known_noisy_scores(raw, ["Q1", "Q2"])
        self.assertEqual(aligned["query_id"].tolist(), ["Q1", "Q2"])
        self.assertEqual(aligned["max_similarity_score"].tolist(), [0.9, 0.2])

    def test_missing_or_duplicate_query_id_fails_loudly(self):
        with self.assertRaisesRegex(ValueError, "ganda"):
            align_known_noisy_scores(pd.DataFrame({
                "query_id": ["Q1", "Q1"], "max_similarity_score": [0.1, 0.2]
            }), ["Q1", "Q2"])
        with self.assertRaisesRegex(ValueError, "tidak identik"):
            align_known_noisy_scores(pd.DataFrame({
                "query_id": ["Q1"], "max_similarity_score": [0.1]
            }), ["Q1", "Q2"])


class RandomControlTests(unittest.TestCase):
    def test_r3_is_stable_by_id_and_independent_of_waveform(self):
        self.assertEqual(R3_CONTROL_VERSION, "stable_id_v1")
        extractor = AudioRepresentationExtractor("R3", random_seed=7)
        a = extractor.extract(np.zeros(32, dtype=np.float32), item_id="query:Q1")
        b = extractor.extract(np.ones(32, dtype=np.float32), item_id="query:Q1")
        c = extractor.extract(np.zeros(32, dtype=np.float32), item_id="query:Q2")
        np.testing.assert_array_equal(a, b)
        self.assertFalse(np.array_equal(a, c))
        self.assertAlmostEqual(float(np.linalg.norm(a)), 1.0, places=6)

    def test_r3_rejects_missing_stable_id(self):
        with self.assertRaisesRegex(ValueError, "item_id"):
            AudioRepresentationExtractor("R3").extract(np.zeros(8, dtype=np.float32))


@unittest.skipIf(MIX_IMPORT_ERROR is not None, f"Mixer dependencies unavailable: {MIX_IMPORT_ERROR}")
class MixingAuditTests(unittest.TestCase):
    def test_audit_records_actual_snr_even_when_peak_gain_is_needed(self):
        clean = np.ones(16, dtype=np.float32) * 0.8
        noise = np.tile(np.array([1.0, -1.0], dtype=np.float32), 8) * 0.05
        source_audit = {
            "noise_file": "synthetic-test.wav", "noise_start_sample": 12,
            "noise_segment_samples": 16, "noise_seed": 9, "noise_attempt": 1,
            "noise_raw_rms": float(np.sqrt(np.mean(noise ** 2))),
        }
        with patch.object(mix_noise, "get_noise_segment", return_value=(noise, source_audit)):
            mixed, audit = mix_noise.mix_audio_at_snr(clean, snr_db=0, seed=9, return_audit_info=True)
        self.assertEqual(mixed.shape, clean.shape)
        self.assertEqual(audit["noise_file"], "synthetic-test.wav")
        self.assertLess(audit["post_mix_gain"], 1.0)
        self.assertAlmostEqual(audit["snr_db_achieved"], 0.0, places=5)


if __name__ == "__main__":
    unittest.main()
