"""Deterministic one-second, finite-storage, link FIFO network evolution.

This is an intentionally simplified research model, NOT a validated SUMO clone.
No realized traffic outputs are consulted during prediction. See protocol §3.
"""
from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass
from math import isfinite
from time import perf_counter
from typing import Dict, List, Optional

from .schema import InvalidScenario, Parameters, Scenario


@dataclass(frozen=True)
class Event:
    tick: int
    vehicle_id: str
    action: str
    edge: str
    next_edge: str = ""


@dataclass
class Evolution:
    arrivals: Dict[str, int]
    insertion: Dict[str, int]
    events: List[Event]
    waiting_by_link: Dict[str, int]
    elapsed_s: Dict[str, int]
    horizon_end_s: int
    ticks: int


class NonCompletion(RuntimeError):
    """The E1 v1 assumptions cannot clear every scheduled driver."""


def evolve(scenario: Scenario, params: Parameters = Parameters()) -> Evolution:
    links = {l.edge_id: l for l in scenario.links}
    turns = {(x.from_edge, x.to_edge): x for x in scenario.turns}
    people = {v.vehicle_id: v for v in scenario.vehicles}
    sorted_people = sorted(scenario.vehicles, key=lambda v: (v.scheduled_departure_s, v.vehicle_id))
    n = len(sorted_people)
    queues = {eid: deque() for eid in links}
    source_queue = defaultdict(deque)
    in_at: dict[str, int] = {}
    route_index: dict[str, int] = {}
    insertions: dict[str, int] = {}
    arrivals: dict[str, int] = {}
    link_tokens = {eid: 0.0 for eid in links}
    turn_tokens = {key: 0.0 for key in turns}
    source_tokens = {eid: 0.0 for eid in links}
    # stable RR pointer over all inbound road-edges of each junction
    junction_approaches = defaultdict(set)
    for t in scenario.turns:
        junction_approaches[t.junction].add(t.from_edge)
    junction_approaches = {jid: sorted(v) for jid, v in junction_approaches.items()}
    rr = {jid: 0 for jid in junction_approaches}
    events: list[Event] = []
    wait_per_edge = defaultdict(int)
    next_person = 0
    start_wall = perf_counter()

    def pool_cap(rate: float) -> float:
        return max(1.0, rate * params.max_service_token_seconds)

    for t in range(params.horizon_s):
        if params.max_wall_s is not None and (t % 20 == 0) and perf_counter() - start_wall > params.max_wall_s:
            raise NonCompletion("Prospective runtime exceeded offline budget")
        while next_person < n and sorted_people[next_person].scheduled_departure_s <= t:
            v = sorted_people[next_person]
            source_queue[v.route_edges[0]].append(v.vehicle_id)
            next_person += 1

        occupied = {eid: len(q) for eid, q in queues.items()}
        receiving = {eid: links[eid].capacity - occupied[eid] for eid in links}
        assert all(value >= 0 for value in receiving.values())
        remaining_slots = dict(receiving)

        for eid, link in links.items():
            rate = params.q_sat * link.lanes
            link_tokens[eid] = min(pool_cap(rate), link_tokens[eid] + rate)
            source_rate = (params.source_rate_per_lane or params.q_sat) * link.lanes
            source_tokens[eid] = min(pool_cap(source_rate), source_tokens[eid] + source_rate)
        for key, turn in turns.items():
            rate = params.q_sat * turn.effective_lanes
            turn_tokens[key] = min(pool_cap(rate), turn_tokens[key] + rate)

        # Reserve destination exits, based only on pre-tick vehicles and service.
        destined = []
        exit_count = defaultdict(int)
        for eid in sorted(links):
            queue = queues[eid]
            while exit_count[eid] < len(queue) and link_tokens[eid] >= 1 + exit_count[eid] - 1e-9:
                vid = queue[exit_count[eid]]
                driver = people[vid]
                if route_index[vid] != len(driver.route_edges) - 1:
                    break
                if in_at[vid] + links[eid].freeflow_ticks(driver.speed_factor) > t:
                    break
                destined.append((eid, vid))
                exit_count[eid] += 1
        # Crossings: all intended next movements require a turn and downstream room.
        moved = []
        used_on_edge = defaultdict(int)
        used_on_turn = defaultdict(int)
        used_conflicts = set()
        # A source may have destination exits at the head; process only later
        # heads if those destination exits were pre-reserved above.
        for junction in sorted(junction_approaches):
            approaches = junction_approaches[junction]
            if not approaches:
                continue
            start = rr[junction] % len(approaches)
            rotated = approaches[start:] + approaches[:start]
            # Multiple passes allow compatible junction movement classes to
            # proceed, while never passing the next vehicle past FIFO heads.
            while True:
                made = False
                for eid in rotated:
                    idx = exit_count[eid] + used_on_edge[eid]
                    if idx >= len(queues[eid]):
                        continue
                    if link_tokens[eid] + 1e-9 < exit_count[eid] + used_on_edge[eid] + 1:
                        continue
                    vid = queues[eid][idx]
                    driver = people[vid]
                    r_idx = route_index[vid]
                    if r_idx == len(driver.route_edges) - 1:
                        continue
                    if in_at[vid] + links[eid].freeflow_ticks(driver.speed_factor) > t:
                        continue
                    next_edge = driver.route_edges[r_idx + 1]
                    turn = turns[(eid, next_edge)]
                    if turn.junction != junction:
                        continue
                    key = (eid, next_edge)
                    if turn_tokens[key] + 1e-9 < used_on_turn[key] + 1:
                        continue
                    if remaining_slots[next_edge] <= 0:
                        continue
                    conflict = (junction, turn.conflict_class)
                    if conflict in used_conflicts:
                        continue
                    moved.append((eid, next_edge, vid))
                    used_on_edge[eid] += 1
                    used_on_turn[key] += 1
                    remaining_slots[next_edge] -= 1
                    used_conflicts.add(conflict)
                    rr[junction] = (approaches.index(eid) + 1) % len(approaches)
                    made = True
                if not made:
                    break
        # Source insertions share the same pre-tick receiving budget. The
        # remaining slots account for reserved cross-link arrivals; a departing
        # vehicle does not free a slot before the synchronous commit.
        inserted = []
        for eid in sorted(links):
            count = 0
            while source_queue[eid] and remaining_slots[eid] > 0 and source_tokens[eid] + 1e-9 >= count + 1:
                vid = source_queue[eid].popleft()
                inserted.append((eid, vid))
                remaining_slots[eid] -= 1
                count += 1
            source_tokens[eid] = max(0.0, source_tokens[eid] - count)

        # All pre-state waiting at a ready head blocked by capacity is counted
        # as a diagnostic; we never add it to elapsed time separately.
        for eid, q in queues.items():
            sent = exit_count[eid] + used_on_edge[eid]
            if q and len(q) > sent:
                vid = q[sent]
                driver = people[vid]
                if in_at[vid] + links[eid].freeflow_ticks(driver.speed_factor) <= t:
                    wait_per_edge[eid] += len(q) - sent

        departures_by_edge = defaultdict(list)
        for eid, vid in destined:
            departures_by_edge[eid].append(vid)
            arrivals[vid] = t + 1
            events.append(Event(t + 1, vid, "arrive", eid))
        for eid, nxt, vid in moved:
            departures_by_edge[eid].append(vid)
            events.append(Event(t + 1, vid, "cross", eid, nxt))
        for eid in sorted(departures_by_edge):
            for vid in departures_by_edge[eid]:
                if not queues[eid] or queues[eid][0] != vid:
                    raise InvalidScenario("Engine violated global link FIFO ordering")
                queues[eid].popleft()
            link_tokens[eid] -= len(departures_by_edge[eid])
            if link_tokens[eid] < -1e-8:
                raise AssertionError("Negative link service tokens")
        for eid, nxt, vid in moved:
            queues[nxt].append(vid)
            route_index[vid] += 1
            in_at[vid] = t + 1
        for eid, vid in inserted:
            queues[eid].append(vid)
            route_index[vid] = 0
            in_at[vid] = t + 1
            insertions[vid] = t + 1
            events.append(Event(t + 1, vid, "insert", eid))
        for key, n_used in used_on_turn.items():
            turn_tokens[key] -= n_used
            if turn_tokens[key] < -1e-8:
                raise AssertionError("Negative turn service tokens")
        # Strong conservation and storage constraints, including all queued.
        active = [vid for q in queues.values() for vid in q]
        pending = [vid for q in source_queue.values() for vid in q]
        future = [v.vehicle_id for v in sorted_people[next_person:]]
        combined = active + pending + future + list(arrivals)
        if len(combined) != n or len(set(combined)) != n:
            raise AssertionError("Vehicle identity mass conservation failed")
        if any(len(q) > links[eid].capacity for eid, q in queues.items()):
            raise AssertionError("Physical storage exceeded")
        for eid in links:
            if len(queues[eid]) != occupied[eid] + len([x for x in moved if x[1] == eid]) + len([x for x in inserted if x[0] == eid]) - len(departures_by_edge[eid]):
                raise AssertionError("Link occupancy conservation failed")
        if len(arrivals) == n:
            elapsed = {v.vehicle_id: arrivals[v.vehicle_id] - v.scheduled_departure_s for v in sorted_people}
            if any(elapsed[vid] < 0 for vid in elapsed):
                raise AssertionError("Negative driver elapsed")
            return Evolution(arrivals, insertions, events, dict(wait_per_edge), elapsed,
                             max(arrivals.values()), t + 1)
    raise NonCompletion(f"E1 horizon {params.horizon_s}s expired: {len(arrivals)}/{n} arrivals")
