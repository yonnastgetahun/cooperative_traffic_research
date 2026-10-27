#!/usr/bin/env python3
"""Development-only qualification fixtures; no SUMO invocation, no heldout input."""
import math,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import guard_v01 as guard
import score_v01 as score
import verify_inputs_v01 as verify

class FrozenHarnessQualification(unittest.TestCase):
    def test_fail_closed_guard_only_allows_preinspected_development_seed(self):
        for w in (200,600,1200):
            self.assertTrue(guard.require_development(2101,w))
        for bad in (2102,2103,2001,3101,3102,3103,3104,3105,3106,3107,3108,3109,3110):
            with self.assertRaises(ValueError):
                guard.require_development(bad,200)
        for bad in (100,300,999):
            with self.assertRaises(ValueError):
                guard.require_development(2101,bad)
        with self.assertRaises(ValueError):
            guard.require_development(2101,200,mode="holdout")
    def test_full_1000_trip_qualifier_seed_metrics(self):
        r=[];t={}
        for i in range(1000):
            vid=f"veh{i:04d}"; t[vid]={"depart":0.,"arrival":11.}
            r.append(dict(vehicle=vid,route_index="0",edge="A",
                          native_entry_s="0",FCD_entry_s="0",
                          timeaware_predicted_s="0",freeflow_predicted_s="0"))
            r.append(dict(vehicle=vid,route_index="1",edge="B",
                          native_entry_s="10",FCD_entry_s="10",
                          timeaware_predicted_s="8",freeflow_predicted_s="7"))
        out=score.score_rows(r,t)
        self.assertEqual(out["vehicles"],1000)
        self.assertEqual(out["edge_traversals"],2000)
        self.assertAlmostEqual(out["timing_metrics"]["timeaware"]["mae_s"],1.)
        self.assertAlmostEqual(out["timing_metrics"]["freeflow"]["mae_s"],1.5)
        self.assertAlmostEqual(out["paired_MAE_benefit_ff_minus_timeaware_s"],.5)
        self.assertAlmostEqual(out["timing_metrics"]["timeaware_route_1_2"]["bias_s"],2.)
        self.assertEqual(out["timing_metrics"]["FCD_minus_native"]["mae_s"],0.)
    def test_scorer_disallows_missing_ordered_vehicle_edges(self):
        t={f"veh{i:04d}":{"depart":0.,"arrival":10.} for i in range(1000)}
        rows=[dict(vehicle=v,route_index="1",edge="A",native_entry_s="0",
                   FCD_entry_s="0",timeaware_predicted_s="0",freeflow_predicted_s="0") for v in t]
        with self.assertRaises(RuntimeError):score.score_rows(rows,t)
    def test_no_silent_nonfinite_timing_data(self):
        t={f"veh{i:04d}":{"depart":0.,"arrival":10.} for i in range(1000)}
        rows=[dict(vehicle=v,route_index="0",edge="A",native_entry_s="0",
                   FCD_entry_s="0",timeaware_predicted_s="nan",freeflow_predicted_s="0") for v in t]
        with self.assertRaises(RuntimeError):score.score_rows(rows,t)
    def test_original_network_topology_parser(self):
        xml='<net><edge id="A" from="n1" to="n2"><lane index="0" speed="12" length="200"/></edge><connection from="A" to="B" fromLane="0" toLane="0"/></net>'
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/"a.net.xml";b=Path(d)/"b.net.xml"
            a.write_text(xml);b.write_text(xml)
            self.assertEqual(verify.topology(a),verify.topology(b))
        self.assertEqual(verify.topology.__name__,"topology")
    def test_confidence_interval_fixture_is_seed_based_only(self):
        import g3_r4_seed_analysis_v01 as r4
        with self.assertRaises(ValueError):r4.mean_ci_if_ten([1,2,3])
        z=r4.mean_ci_if_ten(list(range(1,11)))
        self.assertEqual(z["seed_count"],10)
        self.assertLess(z["lower"],z["mean"])
        self.assertGreater(z["upper"],z["mean"])

if __name__=="__main__":unittest.main()
