#!/usr/bin/env python3
"""G3 fixture tests; no SUMO, external network, or held-out seeds."""
import tempfile,unittest
from pathlib import Path
import g3_reconcile_v01 as g3

class ReconciliationTests(unittest.TestCase):
    def test_junction_bounds_do_not_imply_zero_unknown(self):
        self.assertEqual(g3.phase_bounds(0,1), (0.,1.,'bounded_sample_time_not_causal_delay'))
        self.assertEqual(g3.phase_bounds(3,5), (2.,4.,'bounded_sample_time_not_causal_delay'))
        self.assertEqual(g3.phase_bounds(1,1), (0.,1.,'bounded_sample_time_not_causal_delay'))
        self.assertEqual(g3.phase_bounds(0,1,False), (None,None,'cadence_gap'))
    def test_invalid_phase_cannot_be_silently_integrated(self):
        with self.assertRaises(ValueError):g3.phase_bounds(-1,3)
        with self.assertRaises(ValueError):g3.phase_bounds(1,-1)
        self.assertEqual(g3.phase_bounds(5,2)[2],'invalid_interval')
    def test_busy_bins_do_not_include_empty_bins(self):
        r=dict(native=0.,fcd=0.,delta=0.)
        self.assertIn('both_zero',g3.groups(r))
        self.assertNotIn('busy_native_ge30',g3.groups(r))
        self.assertIn('busy_native_ge30',g3.groups(dict(native=30.,fcd=0.,delta=-30.)))
        self.assertIn('native_positive_fcd_zero',g3.groups(dict(native=.4,fcd=0.,delta=-.4)))
    def test_wape_has_compatible_units_and_zero_denominator(self):
        out=g3.metrics([dict(native=30.,fcd=20.,delta=-10.),dict(native=70.,fcd=75.,delta=5.)])
        self.assertEqual(out['wape'],.15)
        self.assertEqual(out['max_abs'],10.)
        self.assertEqual(out['signed_difference'],-5.)
        self.assertIsNone(g3.metrics([dict(native=0.,fcd=1.,delta=1.)])['wape'])
    def test_no_silent_missing_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(RuntimeError):g3.discover(tmp)
    def test_prespecified_seeds_never_include_holdouts(self):
        self.assertEqual(len(g3.EXPECTED),9)
        self.assertTrue(all(2100<s<3100 for s,w in g3.EXPECTED))
        self.assertEqual(set(g3.WINDOWS),{200,600,1200})

if __name__=='__main__':unittest.main()
