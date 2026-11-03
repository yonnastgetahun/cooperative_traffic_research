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
    # An exact reverse Dijkstra lower bound makes the enumeration A*.
    # The original uniform-cost prefix expansion explored exponentially many
    # partial paths on long grid routes, delaying the full 1,000-driver cohort.
    # This changes search order, NOT the legal connectivity or detour limits.
    reverse = {eid: [] for eid in edges}
    for u, next_edges in neighbors.items():
        for v in next_edges:
            reverse[v].append(u)

    def ff(eid):
        return edges[eid].length_m / edges[eid].speed_mps

    lower = {end: 0.0}
    reverse_q = [(0.0, end)]
    while reverse_q:
        distance, eid = heapq.heappop(reverse_q)
        if distance > lower[eid] + 1e-9:
            continue
        for incoming in reverse[eid]:
            proposed = distance + ff(eid)
            if proposed < lower.get(incoming, float("inf")) - 1e-9:
                lower[incoming] = proposed
                heapq.heappush(reverse_q, (proposed, incoming))
    if start not in lower:
        return tuple(candidates)

    max_depth = len(edges)
    initial_cost = ff(start)
    queue = [(initial_cost + lower[start], initial_cost, (start,))]
    while queue and len(candidates) < max_candidates:
        optimistic, cost, path = heapq.heappop(queue)
        if optimistic > max_ff + 1e-9:
            break
        if path[-1] == end:
            distance_m = sum(edges[e].length_m for e in path)
            if distance_m <= max_length + 1e-9 and path not in candidates:
                candidates.append(path)
            continue
        if len(path) >= max_depth:
            continue
        for nxt in neighbors[path[-1]]:
            if nxt in path or nxt not in lower:
                continue
            total_cost = cost + ff(nxt)
            if total_cost + lower[nxt] > max_ff + 1e-9:
                continue
            new_path = path + (nxt,)
            if sum(edges[e].length_m for e in new_path) > max_length + 1e-9:
                continue
            heapq.heappush(queue, (total_cost + lower[nxt], total_cost, new_path))
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
