"""Method regression tests for the post-hoc H3 reanalysis; no experiment reruns."""
import tempfile
import unittest
from pathlib import Path
import numpy as np
import pandas as pd
from scripts.run_h3_sensitivity_reanalysis import location_swing,paired_bootstrap,load_arrays,run

class H3SensitivityTests(unittest.TestCase):
    def test_absolute_and_relative_can_reverse_order(self):
        means=np.array([[[.1,.2]],[[.5,.7]]])[:,None,:,:]
        absolute,relative=location_swing(means,np.array([.2,.8]),[0,1])
        self.assertGreater(float(absolute[1,0]),float(absolute[0,0]))
        self.assertLess(float(relative[1,0]),float(relative[0,0]))

    def test_range_is_taken_before_repeat_average(self):
        means=np.array([[[.1,.3],[.3,.1]],[[.1,.3],[.3,.1]]])[:,None,:,:]
        absolute,_=location_swing(means,np.array([.5,.5]),[0,1])
        np.testing.assert_allclose(absolute,.2)
        self.assertEqual(float(np.ptp(means.mean(axis=-2),axis=-1)[0,0]),0)

    def test_identical_representations_stay_paired_in_every_draw(self):
        rng=np.random.default_rng(7)
        c=rng.uniform(.1,.9,8);n=rng.uniform(.1,.9,(4,4,5,8))
        points,draws=paired_bootstrap(np.stack([c,c]),np.stack([n,n]),iterations=100,seed=42)
        for pair in draws.values():
            for metric in pair:np.testing.assert_array_equal(metric[:,0],metric[:,1])
        for pair in points.values():
            for metric in pair:np.testing.assert_array_equal(metric[0],metric[1])

    def test_incomplete_raw_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            pd.DataFrame({'query_id':[f'q{i}' for i in range(311)],'condition':['Clean']*311,'AP@10':[.5]*311}).to_csv(Path(d)/'E4_R1_raw.csv',index=False)
            with self.assertRaisesRegex(ValueError,'row count'):load_arrays(d)

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as d:
            sentinel=Path(d)/'keep.txt';sentinel.write_text('unchanged')
            with self.assertRaises(FileExistsError):run(Path(d))
            self.assertEqual(sentinel.read_text(),'unchanged')

if __name__=='__main__':unittest.main()
