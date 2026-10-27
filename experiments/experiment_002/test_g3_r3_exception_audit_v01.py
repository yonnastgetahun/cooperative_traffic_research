#!/usr/bin/env python3
"""R3 protocol fixtures: zero vs missing, teleports and temporal coverage."""
import tempfile,unittest
from pathlib import Path
import g3_r3_exception_audit_v01 as m

class R3(unittest.TestCase):
    def write(self,d,name,txt):
        p=Path(d)/name;p.write_text(txt);return p
    def test_teleport_is_not_inferred_from_absence(self):
        with tempfile.TemporaryDirectory() as d:
            z=self.write(d,"stat.xml",'<statistics><vehicles loaded="1" inserted="1"/><teleports total="0"/></statistics>')
            self.assertEqual(m.statistic_report(z)["teleport_state"],"ZERO_CONFIRMED")
            n=self.write(d,"n.xml",'<statistics><teleports total="2" jam="2"/></statistics>')
            self.assertEqual(m.statistic_report(n)["teleport_state"],"NONZERO_CONFIRMED")
            u=self.write(d,"unknown.xml",'<statistics><vehicles loaded="1"/></statistics>')
            self.assertEqual(m.statistic_report(u)["teleport_state"],"UNKNOWN_NOT_CAPTURED")
    def test_partial_interval_and_empty_native_fields(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.write(d,"native.xml",'<meandata><interval begin="0" end="30"><edge id="A" sampledSeconds="0"/><edge id="B" sampledSeconds="10" speed="1" occupancy="5" density="6" waitingTime="0"/></interval><interval begin="30" end="34"><edge id="A" sampledSeconds="0"/></interval></meandata>')
            r=m.edge_bins(p)
            self.assertEqual(r["status_counts"]["PARTIAL_NATIVE_BIN"],1)
            self.assertEqual(r["status_counts"]["EMPTY_NATIVE_EDGE_NO_SAMPLES"],2)
            self.assertEqual(r["status_counts"]["POSITIVE_NATIVE_SAMPLE_SECONDS"],1)
            self.assertEqual(r["status_counts"].get("MISSING_NATIVE_METRIC_WITH_POSITIVE_SAMPLES",0),0)
    def test_positive_native_samples_missing_metric_is_not_zero(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.write(d,"native.xml",'<meandata><interval begin="0" end="30"><edge id="B" sampledSeconds="1.5" speed="3"/></interval></meandata>')
            r=m.edge_bins(p)
            self.assertGreater(r["status_counts"]["MISSING_NATIVE_METRIC_WITH_POSITIVE_SAMPLES"],0)
    def test_invalid_native_time_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.write(d,"native.xml",'<meandata><interval begin="30" end="20"><edge id="A" sampledSeconds="1"/></interval></meandata>')
            with self.assertRaises(RuntimeError):m.edge_bins(p)
    def test_FCD_pervehicle_gaps_are_separately_counted(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.write(d,"fcd.xml",'<fcd-export><timestep time="0"><vehicle id="v" lane="A_0"/></timestep><timestep time="1"/><timestep time="2"><vehicle id="v" lane="B_0"/></timestep></fcd-export>')
            r=m.fcd_report(p,{"v":(0,4)})
            self.assertEqual(r["within_trip_disappearance_count"],1)
            self.assertEqual(r["structural_anomalies"].get("FCD_GAP_OR_OUT_OF_ORDER_STEP",0),0)
    def test_FCD_timestep_gap_is_exception(self):
        with tempfile.TemporaryDirectory() as d:
            p=self.write(d,"fcd.xml",'<fcd-export><timestep time="0"/><timestep time="2"/></fcd-export>')
            self.assertEqual(m.fcd_report(p,{})["structural_anomalies"]["FCD_GAP_OR_OUT_OF_ORDER_STEP"],1)

if __name__=="__main__":unittest.main()
