"""Development comparators; B1 historical quadratic proxy is NOT changed here."""
from __future__ import annotations
from collections import Counter
from math import floor
from typing import Tuple
from .schema import Scenario

OFFSET=4.053135104279146
PER_EDGE=11.524898884412591
BIN=30


def zero_externality(*_args,**_kwargs) -> float:
    return 0.0


def own_only_externality(*_args,**_kwargs) -> float:
    return 0.0


def _footprint(route: Tuple[str,...], scheduled:int, edges:dict) -> Counter:
    clock=float(scheduled)
    q=Counter()
    for idx,eid in enumerate(route):
        bucket=floor((clock + OFFSET + PER_EDGE*idx)/BIN)
        q[(eid,bucket)] += 1
        clock += edges[eid].length_m/edges[eid].speed_mps
    return q


def historic_quadratic_externality(scenario: Scenario, vid: str, alternate_route: Tuple[str,...]):
    """B1: the immutable historical Exp007 30-second assigned-count formula.

    This baseline is a *comparator*, not a proposed E1 predictor. SUMO does not
    enter the calculation. Historical homogeneous-speed geometry is expected.
    """
    edges={x.edge_id:x for x in scenario.links}
    target=next(x for x in scenario.vehicles if x.vehicle_id==vid)
    before=Counter()
    for v in scenario.vehicles:
        before.update(_footprint(v.route_edges,v.scheduled_departure_s,edges))
    a=_footprint(target.route_edges,target.scheduled_departure_s,edges)
    b=_footprint(tuple(alternate_route),target.scheduled_departure_s,edges)
    dq={k:b.get(k,0)-a.get(k,0) for k in a.keys()|b.keys()}
    def travel(eid,occupancy):
        e=edges[eid]
        ff=e.length_m/e.speed_mps
        cap=max(1.,e.length_m*e.lanes/7.5)
        return ff*(occupancy+occupancy*occupancy/cap)
    total=sum(travel(k[0],before[k]+v)-travel(k[0],before[k]) for k,v in dq.items())
    own0=sum(n*(edges[k[0]].length_m/edges[k[0]].speed_mps)*(1+before[k]/max(1.,edges[k[0]].length_m*edges[k[0]].lanes/7.5)) for k,n in a.items())
    own1=sum(n*(edges[k[0]].length_m/edges[k[0]].speed_mps)*(1+(before[k]+dq.get(k,0))/max(1.,edges[k[0]].length_m*edges[k[0]].lanes/7.5)) for k,n in b.items())
    return {"pred_self_delta_s":own1-own0,"pred_external_delta_network_s":total-(own1-own0),"pred_total_delta_network_s":total}
