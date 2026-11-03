"""Stage 1D no-SUMO regression: bounded legal routes on a 10x10, 1,000-driver grid."""
import unittest
from research.externality_estimator.schema import Link, Turn, Vehicle, Scenario
from research.externality_estimator.candidate_routes import legal_alternatives
from research.externality_estimator.dataset_contract import select_development_probes

def grid():
    nodes=[(x,y) for x in range(10) for y in range(10)]
    roads=[]
    for x,y in nodes:
        for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if 0<=nx<10 and 0<=ny<10:
                roads.append((f"e{x}_{y}__{nx}_{ny}", (x,y), (nx,ny)))
    links=tuple(Link(e,200.,13.89,1) for e,_,_ in roads)
    junction={eid:(source,dest) for eid,source,dest in roads}
    turns=tuple(Turn(a,b,f"j{v[0]}_{v[1]}") for a,(u,v) in roads
                for b,(vv,w) in roads if v==vv and w!=u)
    vehicles=[]
    for i in range(1000):
        x=(i*7)%10
        y=(i*3)%10
        targetx=(x+4+(i%5))%10
        targety=(y+3+((i//5)%5))%10
        # Choose a simple directed rectangular route with no repeated road.
        pts=[(x,y)]
        while x!=targetx:
            x+=1 if targetx>x else -1
            pts.append((x,y))
        while y!=targety:
            y+=1 if targety>y else -1
            pts.append((x,y))
        if len(pts)<2:
            pts.append(((x+1)%10,y))
        path=tuple(f"e{a[0]}_{a[1]}__{b[0]}_{b[1]}" for a,b in zip(pts,pts[1:]))
        vehicles.append(Vehicle(f"veh{i:04d}",i%200,path,i%2==0))
    return Scenario(links,turns,tuple(vehicles),label_partition="DEV_BUILD")

class FullCohortRouteSearch(unittest.TestCase):
    def test_1000_drivers_deterministic_and_bounded(self):
        s=grid()
        x=select_development_probes(s,5101,"DEV_BUILD")
        y=select_development_probes(s,5101,"DEV_BUILD")
        self.assertEqual(x.immutable_selection_sha,y.immutable_selection_sha)
        self.assertEqual(len(x.probes),4)
        self.assertEqual(len(set(v.vehicle_id for v in x.probes)),4)
        self.assertEqual(len(x.bundle_target_ids),2)
        self.assertTrue(all(v.vehicle_id.startswith("veh") for v in x.probes))
        self.assertTrue(all(len(legal_alternatives(s,v.vehicle_id))<=4 for v in s.vehicles[:30]))
