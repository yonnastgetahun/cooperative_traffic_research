"""NEW V2-D1 development selection; frozen geometry/hash/clock, NO realized labels."""
from __future__ import annotations
import hashlib
from dataclasses import dataclass
from research.externality_estimator.schema import Scenario, InvalidScenario
from research.externality_estimator.audit import sha256

BUILD = frozenset(range(6101,6107))
CHECK = frozenset(range(6111,6115))
def check_partition(seed:int, partition:str):
    expected = BUILD if partition == "DEV_BUILD" else CHECK if partition == "DEV_CHECK" else frozenset()
    if seed not in expected:
        raise InvalidScenario("Frozen E1-v2 development seed/partition mismatch; old cohorts forbidden")

from research.externality_estimator.candidate_routes import legal_alternatives


@dataclass(frozen=True)
class Probe:
    slot: str
    vehicle_id: str
    alternate_route: tuple[str,...]
    baseline_route: tuple[str,...]
    selection_sha: str
    reason: str = "assigned"


@dataclass(frozen=True)
class DevelopmentSelection:
    partition: str
    seed: int
    probes: tuple[Probe, ...]
    bundle_target_ids: tuple[str, str]
    bundle_overlap_score: int
    fallback_notes: tuple[str, ...]
    immutable_selection_sha: str


def _stable(*parts):
    return hashlib.sha256(":".join(map(str,parts)).encode()).hexdigest()


def select_development_probes(scenario: Scenario,seed:int,partition:str) -> DevelopmentSelection:
    check_partition(seed,partition)
    if partition not in ("DEV_BUILD","DEV_CHECK"):
        raise InvalidScenario("Old diagnostic cohorts cannot define new training pairs")
    if scenario.label_partition!=partition:
        raise InvalidScenario("Scenario partition mismatch")
    edges={l.edge_id:l for l in scenario.links}
    slots=("equal-early","equal-late","different-early","different-late")
    candidates={slot:[] for slot in slots}
    for v in scenario.vehicles:
        if not v.eligible:continue
        base_ff=sum(edges[e].length_m/edges[e].speed_mps for e in v.route_edges)
        for alt in legal_alternatives(scenario,v.vehicle_id):
            if alt==v.route_edges:continue
            ff=sum(edges[e].length_m/edges[e].speed_mps for e in alt)
            nominal="equal" if abs(ff-base_ff)<=.5 else "different"
            phase="early" if v.scheduled_departure_s<100 else "late"
            slot=nominal+"-"+phase
            score=_stable(seed,slot,v.vehicle_id,sha256(alt))
            candidates[slot].append((score,v,alt))
    selected=[];used=set();fallback=[]
    for slot in slots:
        eligible=[(score,v,alt) for score,v,alt in candidates[slot] if v.vehicle_id not in used]
        used_slot=slot
        if not eligible:
            for next_slot in slots:
                eligible=[(score,v,alt) for score,v,alt in candidates[next_slot] if v.vehicle_id not in used]
                if eligible:
                    used_slot=next_slot
                    fallback.append(f"{slot}:no candidate, fallback {next_slot}")
                    break
        if not eligible:raise InvalidScenario("SEED-DESIGN INVALID: <4 distinct eligible swaps")
        score,v,alt=min(eligible,key=lambda x:x[0])
        selected.append(Probe(slot,v.vehicle_id,tuple(alt),tuple(v.route_edges),score,
                              "original slot" if used_slot==slot else f"fallback {used_slot}"))
        used.add(v.vehicle_id)
    # Prospective overlap based only on route geometry + nominal edge-time bins;
    # original Exp007 ordinal clock is used here as a *selection heuristic*,
    # not as the new E1 prospective traffic-state model.
    turn_map={(t.from_edge,t.to_edge):t for t in scenario.turns}
    def footprint(probe):
        v=next(v for v in scenario.vehicles if v.vehicle_id==probe.vehicle_id)
        time=v.scheduled_departure_s
        result=set()
        for edge_before,edge_after in zip(probe.alternate_route,probe.alternate_route[1:]):
            time+=edges[edge_before].length_m/edges[edge_before].speed_mps
            turn=turn_map[(edge_before,edge_after)]
            # Prospective *junction/5s time* exposure, not outcome truth.
            result.add((turn.junction,int(time//5)))
        return result
    pairs=[]
    for a in range(4):
        for b in range(a+1,4):
            score=len(footprint(selected[a]) & footprint(selected[b]))
            tie=_stable(seed,selected[a].vehicle_id,selected[b].vehicle_id)
            pairs.append((-score,tie,selected[a].vehicle_id,selected[b].vehicle_id))
    _,_,first,second=min(pairs)
    best_score=-min(pairs)[0]
    if best_score==0:
        first,second=selected[0].vehicle_id,selected[1].vehicle_id
        fallback.append("bundle: low/no forecast overlap; first two probe slots")
    summary={"seed":seed,"partition":partition,"probes":selected,
             "bundle":(first,second),"overlap":best_score,"fallback":fallback}
    return DevelopmentSelection(partition,seed,tuple(selected),(first,second),best_score,
                                tuple(fallback),sha256(summary))
