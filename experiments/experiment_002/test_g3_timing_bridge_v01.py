#!/usr/bin/env python3
"""No-SUMO contract fixtures for native step and sampled front timing."""
import csv,tempfile,unittest
from pathlib import Path
import g3_timing_bridge_v01 as bridge

class BridgeTests(unittest.TestCase):
    def test_fcd_repeat_external_road_after_internal(self):
        xml='<fcd-export><timestep time="0"><vehicle id="v" lane="A_0"/></timestep><timestep time="1"><vehicle id="v" lane=":J_0"/></timestep><timestep time="2"><vehicle id="v" lane="A_0"/></timestep></fcd-export>'
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"fcd.xml";path.write_text(xml)
            self.assertEqual(bridge.fcd_records(path)["v"],[("A",0.),("A",2.)])
    def test_missing_fcd_step_blocks_comparison(self):
        xml='<fcd-export><timestep time="0"/><timestep time="2"/></fcd-export>'
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"fcd.xml";path.write_text(xml)
            with self.assertRaises(RuntimeError):bridge.fcd_records(path)
    def test_native_external_ordinal_is_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/"events.csv"
            with open(path,"w",newline="") as f:
                w=csv.DictWriter(f,fieldnames=["vehicle","edge","kind","ordinal","enter_at_prior_exit_s"])
                w.writeheader()
                w.writerows([dict(vehicle="v",edge="A",kind="external",ordinal=0,enter_at_prior_exit_s=0),
                    dict(vehicle="v",edge=":J",kind="internal",ordinal=1,enter_at_prior_exit_s=1),
                    dict(vehicle="v",edge="A",kind="external",ordinal=2,enter_at_prior_exit_s=2)])
            self.assertEqual([x["edge"] for x in bridge.native_records(path)["v"]],["A","A"])

if __name__=="__main__":unittest.main()
