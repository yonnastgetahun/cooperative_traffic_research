"""Deterministic READY-FOE-TOPOLOGICAL-GREEDY junction scheduler.

One candidate per currently eligible incoming FIFO head. Foes and yielding
are independent: right-of-way applies only to *ready* conflicting candidates.
A static non-foe is NOT an unconditional safe/simultaneous-service guarantee.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping
from .movement import Movement, PriorityAmbiguity

@dataclass(frozen=True)
class Candidate:
    vehicle_id: str
    movement: Movement

    @property
    def src(self) -> str:
        return self.movement.src

    @property
    def dst(self) -> str:
        return self.movement.dst

@dataclass(frozen=True)
class Choice:
    accepted: tuple[Candidate, ...]
    blocked: tuple[tuple[str,str], ...]
    pointer_after: int
    priority_edges: tuple[tuple[str,str], ...]


def select(
    ready: tuple[Candidate, ...],
    approach_order: tuple[str, ...],
    pointer_before: int,
    available_receiving: Mapping[str, int]
) -> Choice:
    """Select pairwise compatible ready movements, conserving receiving slots.

    Every 'ready' candidate must already pass elapsed edge time, link/turn
    service token, upstream FIFO and pre-tick receiving checks. Resource
    reservation is rechecked here for multiple contenders within one tick.
    """
    if not approach_order:
        return Choice((), (), 0, ())
    if not ready:
        return Choice((), (), pointer_before % len(approach_order), ())

    people = {c.vehicle_id:c for c in ready}
    if len(people) != len(ready):
        raise PriorityAmbiguity("Duplicate ready vehicle")
    sources=[c.movement.source_lane for c in ready]
    if len(sources)!=len(set(sources)):
        raise PriorityAmbiguity("More than one ready FIFO head on a lane")
    idxs=[(c.movement.junction,c.movement.index) for c in ready]
    if len(set(idxs))!=len(idxs):
        raise PriorityAmbiguity("Duplicate movement request in one ready group")
    if len(set(c.movement.junction for c in ready))!=1:
        raise PriorityAmbiguity("Candidates from distinct junctions")
    if any(m.movement.yields_to - m.movement.foes for m in ready):
        raise PriorityAmbiguity("Response references a non-foe")
    if any(c.src not in approach_order for c in ready):
        raise PriorityAmbiguity("Unknown approach lane")

    edges=set()
    for i,a in enumerate(ready):
        for b in ready[i+1:]:
            am,bm=a.movement,b.movement
            if (bm.index in am.foes)!=(am.index in bm.foes):
                raise PriorityAmbiguity("Nonreciprocal foes")
            if bm.index in am.yields_to:
                edges.add((b.vehicle_id,a.vehicle_id))
            if am.index in bm.yields_to:
                edges.add((a.vehicle_id,b.vehicle_id))
    def cycle_free():
        stack=set()
        visited=set()
        adj={vid:[] for vid in people}
        for u,v in edges:adj[u].append(v)
        def visit(u):
            if u in stack:raise PriorityAmbiguity("Cycle or contradictory yielding among ready vehicles")
            if u in visited:return
            stack.add(u)
            for v in adj[u]:visit(v)
            stack.remove(u);visited.add(u)
        for u in people:visit(u)
    cycle_free()

    rotating=approach_order[pointer_before % len(approach_order):]+approach_order[:pointer_before % len(approach_order)]
    rank={src:i for i,src in enumerate(rotating)}
    unprocessed=set(people)
    accepted=[]
    blocked=[]
    still_receiving=dict(available_receiving)
    priors=set()
    def order_key(vid):
        c=people[vid]
        return (rank[c.src],c.movement.index,vid)
    while unprocessed:
        heads=[vid for vid in unprocessed
               if not any((u,vid) in edges for u in unprocessed)]
        if not heads:
            raise PriorityAmbiguity("Unresolvable ready-vehicle priority order")
        vid=min(heads,key=order_key)
        unprocessed.remove(vid)
        c=people[vid];m=c.movement
        reason=None
        if still_receiving.get(c.dst,0)<1:
            reason="SHARED_RECEIVING_STORAGE_FULL"
        elif accepted and (m.cont or any(a.movement.cont for a in accepted)):
            reason="TIER_C_EXCLUSIVE_SERVICE"
        else:
            for a in accepted:
                other=a.movement
                if other.index in m.foes or m.index in other.foes:
                    reason=("YIELD_HIGHER_PRIORITY_READY" if (other.index in m.yields_to)
                            else "CONFLICTING_FOE_SELECTED")
                    break
                if other.source_lane==m.source_lane or other.destination_lane==m.destination_lane:
                    reason="SHARED_SOURCE_OR_OUTGOING_LANE"
                    break
                if other.via==m.via:
                    reason="SHARED_INTERNAL_VIA"
                    break
        if reason:
            blocked.append((vid,reason))
            continue
        accepted.append(c)
        still_receiving[c.dst]-=1
    after=pointer_before%len(approach_order)
    if accepted:
        last=accepted[-1].src
        after=(approach_order.index(last)+1)%len(approach_order)
    return Choice(tuple(accepted),tuple(blocked),after,tuple(sorted(edges)))
