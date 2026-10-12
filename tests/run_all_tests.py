"""Run only current method and restart-integrity tests.

Legacy experiment-result and manuscript checks do not run here: the source
tables were withdrawn after the XC42472 imputation finding. They return only
after complete new experiments regenerate them.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests import test_phase_a_integrity, test_restart_preflight
from tests.test_cosine import test_cosine_similarity_properties, test_retrieval_ranking_logic
from tests.test_snr_mixing import test_snr_mixing_accuracy, test_snr_mixing_reproducibility
from tests.test_split_leakage import test_zero_filepath_leakage, test_zero_leakage_between_gallery_and_query, test_zero_recordist_leakage_global
from tests.test_threshold_freeze import test_threshold_frozen_evaluation
from tests.unit.test_manifest_and_models import test_manifest_sha256_integrity, test_model_embedding_dimensions


def main() -> None:
    function_tests = [
        test_zero_leakage_between_gallery_and_query, test_zero_filepath_leakage, test_zero_recordist_leakage_global,
        test_cosine_similarity_properties, test_retrieval_ranking_logic, test_snr_mixing_accuracy,
        test_snr_mixing_reproducibility, test_threshold_frozen_evaluation, test_manifest_sha256_integrity,
        test_model_embedding_dimensions,
    ]
    suite = unittest.TestSuite(unittest.FunctionTestCase(fn) for fn in function_tests)
    loader = unittest.TestLoader()
    suite.addTests(loader.loadTestsFromModule(test_restart_preflight))
    suite.addTests(loader.loadTestsFromModule(test_phase_a_integrity))
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print(f"[PASS] {result.testsRun} current integrity tests")


if __name__ == "__main__":
    main()
