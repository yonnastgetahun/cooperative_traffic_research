"""Only legal fixed route candidates; never select by counterfactual outcomes."""
from __future__ import annotations
import heapq
from .schema import InvalidScenario, Scenario


def legal_alternatives(scenario: Scenario, vehicle_id: str, max_candidates: int = 4):
    """Enumerate simple edge paths obeying known turns, deterministic order.

    Avoids generating traffic outcomes. The detour cap is based only on nominal
    length and freeflow. Baseline path is always first.
    """
    vehicle = next(v for v in scenario.vehicles if v.vehicle_id == vehicle_id)
    edges={x.edge_id:x for x in scenario.links}
    neighbors={key:[] for key in edges}
    for turn in scenario.turns:
        neighbors[turn.from_edge].append(turn.to_edge)
    for values in neighbors.values():
        values.sort()
    start,end=vehicle.route_edges[0],vehicle.route_edges[-1]
    path0=tuple(vehicle.route_edges)
    ff0=sum(edges[e].length_m/edges[e].speed_mps for e in path0)
    length0=sum(edges[e].length_m for e in path0)
    max_ff=ff0+min(30.0,.1*ff0)
    max_length=1.15*length0
    candidates=[path0]
    # bounded by at most 4x nominal number of links; never infinite-cycle search
    limit=max(2,len(edges))
    queue=[(edges[start].length_m/edges[start].speed_mps, (start,))]
    while queue and len(candidates)<max_candidates:
        cost,path=heapq.heappop(queue)
        if len(path)>limit:
            continue
        if path[-1]==end:
            length=sum(edges[e].length_m for e in path)
            if cost<=max_ff+1e-9 and length<=max_length+1e-9 and path not in candidates:
                candidates.append(path)
            continue
        for nxt in neighbors[path[-1]]:
            if nxt in path:
                continue
            ff=cost+edges[nxt].length_m/edges[nxt].speed_mps
            if ff<=max_ff+1e-9:
                heapq.heappush(queue,(ff,path+(nxt,)))
    return tuple(candidates)


def check_candidate(scenario:Scenario,target:str,alternate:tuple[str,...]):
    v=next((v for v in scenario.vehicles if v.vehicle_id==target),None)
    if v is None or not v.eligible:
        raise InvalidScenario("Unknown/ineligible target")
    if len(set(alternate))!=len(alternate) or not alternate:
        raise InvalidScenario("Alternative route looped or empty")
    if alternate[0]!=v.route_edges[0] or alternate[-1]!=v.route_edges[-1]:
        raise InvalidScenario("Alternative endpoints differ from announced trip")
    legal={(t.from_edge,t.to_edge) for t in scenario.turns}
    edges={x.edge_id:x for x in scenario.links}
    if any(x not in edges for x in alternate):
        raise InvalidScenario("Alternative references missing edge")
    if any((a,b) not in legal for a,b in zip(alternate,alternate[1:])):
        raise InvalidScenario("Alternative contains illegal turn")
    own0=sum(edges[e].length_m/edges[e].speed_mps for e in v.route_edges)
    own1=sum(edges[e].length_m/edges[e].speed_mps for e in alternate)
    distance0=sum(edges[e].length_m for e in v.route_edges)
    distance1=sum(edges[e].length_m for e in alternate)
    if own1>own0+min(30.,.1*own0)+1e-9 or distance1>1.15*distance0+1e-9:
        raise InvalidScenario("Candidate beyond frozen nominal detour caps")
