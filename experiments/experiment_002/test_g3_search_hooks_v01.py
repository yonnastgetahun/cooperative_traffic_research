#!/usr/bin/env python3
"""J2 pure-Python tests for actual edge lookup events; no SUMO runtime required."""
import collections,sys,types,unittest
try:import sumolib
except ImportError:sys.modules["sumolib"]=types.ModuleType("sumolib")
import time_aware

class Edge:
    def __init__(self, length=1.,speed=1.,lanes=1):
        self.length=length;self.speed=speed;self.lanes=lanes
    def getLength(self):return self.length
    def getSpeed(self):return self.speed
    def getLaneNumber(self):return self.lanes

class SearchEvents(unittest.TestCase):
    def setUp(self):
        time_aware.G3_SEARCH_TRACE_SINK=None
        time_aware.G3_ACTIVE_VEHICLE="test_veh"
        time_aware.G3_DECISION_ORDINAL=0
        time_aware.G3_ASSIGNMENT_REVISION=0
        self.edges={e:Edge() for e in ("A","B","C","D")}
        self.adj={"A":["B","D"],"B":["C"],"D":["C"],"C":[]}
    def tearDown(self):time_aware.G3_SEARCH_TRACE_SINK=None
    def test_default_off_and_observation_do_not_change_path(self):
        occ=collections.Counter({("B",0):3,("D",0):0})
        baseline=time_aware.search("A","C",0.,self.edges,self.adj,occ,30,1.)
        events=[]
        time_aware.G3_SEARCH_TRACE_SINK=events.append
        traced=time_aware.search("A","C",0.,self.edges,self.adj,occ,30,1.)
        self.assertEqual(baseline,traced)
        self.assertEqual(baseline[0],["A","D","C"])
        self.assertEqual(next(e for e in events if e["event_type"]=="edge_lookup" and e["to_edge"]=="B")["prior_assigned_count"],3)
        self.assertEqual(len([e for e in events if e["event_type"]=="search_end"]),1)
        self.assertEqual(occ[("B",0)],3) # must not mutate counter
    def test_time_bin_boundary_exact_lookup(self):
        seen=[]
        time_aware.G3_SEARCH_TRACE_SINK=seen.append
        time_aware.search("A","C",29.,self.edges,self.adj,collections.Counter(),30,1.)
        bins=[e["lookup_bin"] for e in seen if e["event_type"]=="edge_lookup"]
        self.assertTrue(bins)
        self.assertTrue(all(b>=1 for b in bins)) # origin freeflow cost 1 => next entry 30.0
    def test_heap_tie_and_stale_entries_are_observed(self):
        logs=[]
        time_aware.G3_SEARCH_TRACE_SINK=logs.append
        time_aware.search("A","C",0.,self.edges,self.adj,collections.Counter(),30,0.)
        self.assertEqual(sum(x["event_type"]=="search_start" for x in logs),1)
        self.assertEqual(sum(x["event_type"]=="destination_reached" for x in logs),1)
        self.assertTrue(any(x["event_type"]=="heap_pop" for x in logs))
        self.assertTrue(any(x["event_type"]=="edge_lookup" and not x["accepted_for_heap"] for x in logs))
if __name__=="__main__":unittest.main()
