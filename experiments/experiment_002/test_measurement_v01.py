#!/usr/bin/env python3
"""M0 contract tests: synthetic fixtures, no SUMO runtime or network needed."""
import csv, os, tempfile, unittest
from pathlib import Path
import measurement_v01 as m

class MeasurementContractTests(unittest.TestCase):
    def test_half_open_time_bins(self):
        self.assertEqual([m.bin_index(t,30) for t in [0,29.999,30,59.999,60]], [0,0,1,1,2])
        self.assertEqual(m.overlap_seconds(25,65,30,60),30)
        self.assertEqual(m.overlap_seconds(25,30,30,60),0)
        with self.assertRaises(ValueError):m.overlap_seconds(2,1,0,3)
        with self.assertRaises(ValueError):m.bin_index(-1,30)
    def test_internal_and_external_distinct(self):
        self.assertEqual(m.edge_id('B0C0_0'),('B0C0','external'))
        self.assertEqual(m.edge_id(':C0_0_0'),(':C0_0','internal'))
        self.assertEqual(m.edge_id('bad'),(None,'invalid'))
        self.assertEqual(m.edge_id(''),(None,'missing'))
    def test_repeated_edge_join_without_collapsing(self):
        route=[{'edge':e} for e in ['A','B','A']]
        samples=[(0,'A','external','A_0',3,5),
                 (1,':X','internal',':X_0',1,0),
                 (2,'B','external','B_0',3,5),
                 (3,':Y','internal',':Y_0',1,0),
                 (4,'A','external','A_0',0,10)]
        out,report=m.phase_segments('veh0',route,samples,{'arrival':5})
        self.assertEqual(report['status'],'matched')
        self.assertEqual([r[2] for r in out],['A','B','A'])
        self.assertEqual(sum(r[7] for r in out),2)
    def test_consecutive_same_edge_separated_by_junction(self):
        samples=[(0,'A','external','A_0',2,10),
                 (1,':J','internal',':J_0',2,1),
                 (2,'A','external','A_0',2,2)]
        out,status=m.phase_segments('v',[{'edge':'A'},{'edge':'A'}],samples,{'arrival':3})
        self.assertEqual(status['status'],'matched')
        self.assertEqual([r[1] for r in out],[0,1])
        self.assertEqual(len(out),2)
    def test_internal_delay_not_assigned_to_external(self):
        route=[{'edge':'A'},{'edge':'B'}]
        samples=[(0,'A','external','A_0',0,1),
                 (1,':J','internal',':J_0',0,1),
                 (3,'B','external','B_0',5,1)]
        out,_=m.phase_segments('veh0',route,samples,{'arrival':4})
        self.assertEqual(out[0][6],1) # external sampled seconds
        self.assertEqual(out[0][7],1) # internal sampled seconds
        self.assertEqual(out[0][10],1) # missing telemetry remains unresolved
        self.assertEqual(out[0][8],1) # external stopped time
    def test_unmatched_route_is_visible(self):
        out,status=m.phase_segments('v',[{'edge':'A'},{'edge':'B'}],
            [(0,'A','external','A_0',2,0)],{'arrival':3})
        self.assertFalse(out)
        self.assertEqual(status['status'],'unmatched_route')
    def test_fcd_internal_and_stops_and_missing_data(self):
        fcd='''<fcd-export><timestep time="0"><vehicle id="v1" lane="A_0" speed="0" pos="2"/></timestep>
        <timestep time="1"><vehicle id="v1" lane=":J_0" speed="0.5" pos="1"/></timestep>
        <timestep time="2"><vehicle id="v1" lane="B_0" speed="4" pos="4"/>
        <vehicle id="v2" lane="" speed="4"/></timestep></fcd-export>'''
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'fcd.xml';path.write_text(fcd)
            tracks,bins,meta=m.read_fcd(path,30)
        self.assertEqual(meta['internal_vehicle_samples'],1)
        self.assertEqual(bins[('A',0,'external')][1],1)
        self.assertEqual(bins[(':J',0,'internal')][2],1)
        self.assertEqual(meta['excluded_samples']['missing'],1)
        self.assertEqual(meta['timestep_gap_counts']['1.0'],2)
    def test_fcd_reject_duplicate_or_out_of_order_times(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'fcd.xml'
            path.write_text('<fcd-export><timestep time="1"/><timestep time="1"/></fcd-export>')
            with self.assertRaises(RuntimeError):m.read_fcd(path,30)
    def test_native_empty_edge_and_partial_final_bin(self):
        native='''<meandata><interval begin="0" end="30">
            <edge id="A" sampledSeconds="15.5" occupancy="3.5" waitingTime="2"/>
            <edge id="B" sampledSeconds="0"/></interval>
            <interval begin="30" end="34"><edge id="A" sampledSeconds="1"/></interval></meandata>'''
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'edge.xml';path.write_text(native)
            rows,meta=m.read_native(path,False)
        self.assertEqual(len(rows),3)
        self.assertEqual(rows[('A',0,30)]['sampledSeconds'],15.5)
        self.assertIsNone(rows[('B',0,30)]['occupancy'])
        self.assertIn((30.,34.),{(a,b) for a,b in [(k[1],k[2]) for k in rows]})
    def test_native_internal_separate(self):
        native='<meandata><interval begin="0" end="30"><edge id="A" sampledSeconds="4"/><edge id=":J_0" sampledSeconds="2"/></interval></meandata>'
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'edge.xml';path.write_text(native)
            rows,meta=m.read_native(path,True)
        self.assertEqual(meta['internal_edge_records'],1)
        self.assertEqual(len(rows),2)
    def test_stop_threshold_and_reconciliation(self):
        samples=[(0,'A','external','A_0',0.01,2),
                 (1,'A','external','A_0',.4,3),
                 (2,':J','internal',':J_0',.2,1),
                 (4,'B','external','B_0',8,1)]
        out,status=m.phase_segments('v',[{'edge':'A'},{'edge':'B'}],samples,{'arrival':5})
        self.assertEqual(status['status'],'matched')
        self.assertEqual(out[0][8],1) # below 0.1
        self.assertEqual(out[0][9],2) # below 1.0
        self.assertEqual(out[0][10],1) # unknown second
    def test_overcoverage_flagged_not_silenced(self):
        samples=[(0,'A','external','A_0',2,3),
                 (0,'A','external','A_0',2,3),
                 (1,'B','external','B_0',2,3)]
        out,_=m.phase_segments('v',[{'edge':'A'},{'edge':'B'}],samples,{'arrival':2})
        self.assertEqual(out[0][13],'sampling_overcoverage')
        self.assertGreater(out[0][11],0)

if __name__=='__main__':unittest.main()
