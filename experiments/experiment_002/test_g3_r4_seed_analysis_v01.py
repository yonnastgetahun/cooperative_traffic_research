#!/usr/bin/env python3
"""R4 synthetic fixtures: independent seed units, blocked holdouts, t CI mathematics."""
import csv,math,tempfile,unittest
from pathlib import Path
import g3_r4_seed_analysis_v01 as m

FIELDS=["seed","window_seconds","completed","planned","matched_route_vehicles",
        "timeaware_entry_mae_s","freeflow_entry_mae_s","timeaware_entry_bias_s"]

def emit(path,rows):
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)

def samples():
    return [dict(seed=s,window_seconds=w,completed=1000,planned=1000,
                 matched_route_vehicles=1000,
                 timeaware_entry_mae_s=10+(s-2100),freeflow_entry_mae_s=15+(s-2100),
                 timeaware_entry_bias_s=7)
            for s in (2101,2102,2103) for w in (200,600,1200)]

class R4(unittest.TestCase):
    def test_seed_level_paired_delta_not_pooled_edges(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"data.csv";emit(p,samples())
            rows=m.read_development(p)
            self.assertEqual(len(rows),9)
            report=m.summarize(rows)
            self.assertEqual([x["paired_delta_mean_s"] for x in report],[5.,5.,5.])
            self.assertTrue(all(x["seeds"]==3 for x in report))
    def test_heldout_seed_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"data.csv";v=samples();v[0]["seed"]=3101;emit(p,v)
            with self.assertRaises(ValueError):m.read_development(p)
    def test_missing_and_duplicate_seed_regime_fail(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"data.csv";v=samples();emit(p,v[:-1])
            with self.assertRaises(ValueError):m.read_development(p)
            emit(p,v+[v[0]])
            with self.assertRaises(ValueError):m.read_development(p)
    def test_negative_missing_coverage_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/"data.csv";v=samples();v[2]["matched_route_vehicles"]=999;emit(p,v)
            with self.assertRaises(ValueError):m.read_development(p)
            v=samples();v[1]["timeaware_entry_mae_s"]=-1;emit(p,v)
            with self.assertRaises(ValueError):m.read_development(p)
    def test_t_ci_is_seed_level_and_requires_exactly_ten(self):
        with self.assertRaises(ValueError):m.mean_ci_if_ten([1.,2.,3.])
        result=m.mean_ci_if_ten([1.,2.,3.,4.,5.,6.,7.,8.,9.,10.])
        self.assertAlmostEqual(result["mean"],5.5)
        self.assertAlmostEqual(result["sd"],math.sqrt(55/6),places=8)
        self.assertGreater(result["lower"],0.)
        self.assertEqual(result["seed_count"],10)

if __name__=="__main__":unittest.main()
