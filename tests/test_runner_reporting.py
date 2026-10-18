"""Protect honest pass/skip reporting, including missing model checkpoints."""
import io,unittest
from unittest.mock import patch
class RunnerReportingTests(unittest.TestCase):
    def test_pass_skip_failure_and_error_are_separate(self):
        from tests.run_all_tests import AuditedTestResult, summarize_result
        def passed(): pass
        def skipped(): raise unittest.SkipTest("synthetic missing input")
        def failed(): raise AssertionError("synthetic failure")
        def errored(): raise RuntimeError("synthetic error")
        suite=unittest.TestSuite(unittest.FunctionTestCase(f) for f in (passed,skipped,failed,errored))
        result=unittest.TextTestRunner(stream=io.StringIO(),resultclass=AuditedTestResult).run(suite)
        counts=summarize_result(result)
        self.assertEqual({k:counts[k] for k in ('collected','passed','skipped','failures','errors')},
                         {'collected':4,'passed':1,'skipped':1,'failures':1,'errors':1})
    def test_missing_checkpoint_is_a_skip(self):
        from tests.unit.test_manifest_and_models import check_model_embedding_dimension
        with patch('src.embeddings.AudioRepresentationExtractor',side_effect=FileNotFoundError('synthetic missing checkpoint')):
            with self.assertRaises(unittest.SkipTest):check_model_embedding_dimension('R1')
if __name__=='__main__':unittest.main()
