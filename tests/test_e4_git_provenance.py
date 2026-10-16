"""Frozen E4 identity source hashes must survive actual Git storage."""
import hashlib,json,subprocess,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class FrozenE4GitBytesTests(unittest.TestCase):
    def test_every_tracked_source_asset_matches_local_and_git_bytes(self):
        assets=json.loads((ROOT/'results/reproductions/E4_5sites_20261011T213404_350219Z/run_identity.json').read_text())['identity']['assets']
        checked=0
        for key,item in assets.items():
            if key.endswith('_cache') or key.endswith('_metadata') or key.endswith('_checkpoint'):continue
            with self.subTest(asset=key):
                actual=hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()
                self.assertEqual(actual,item['sha256'])
                stored=subprocess.check_output(['git','show','HEAD:'+item['path']],cwd=ROOT)
                self.assertEqual(hashlib.sha256(stored).hexdigest(),item['sha256'])
                checked+=1
        self.assertEqual(checked,10)
if __name__=='__main__':unittest.main()
