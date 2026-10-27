#!/usr/bin/env python3
"""Advance-announcement, time-binned routing prototype. NOT live routing or a safety guarantee."""
import argparse, collections, csv, heapq, json, math, os, sys
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.join(os.environ.get("SUMO_HOME", "/usr/share/sumo"), "tools"))
import sumolib

# G3 observation hook; disabled by default. It may ONLY emit immutable copies
# of already-computed values, never modify queues, costs, routes or counters.
G3_SEARCH_TRACE_SINK = None
G3_ACTIVE_VEHICLE = None
G3_DECISION_ORDINAL = -1
G3_ASSIGNMENT_REVISION = 0

def g3_emit(kind, **fields):
    if G3_SEARCH_TRACE_SINK is not None:
        G3_SEARCH_TRACE_SINK(dict(event_type=kind,
            vehicle=G3_ACTIVE_VEHICLE, decision_ordinal=G3_DECISION_ORDINAL,
            assignment_revision=G3_ASSIGNMENT_REVISION, **fields))

def build_graph(net):
    edges = {e.getID(): e for e in net.getEdges() if not e.isSpecial() and e.allows("passenger")}
    adj = {}
    for eid, edge in edges.items():
        nxt = []
        for next_edge, connections in edge.getOutgoing().items():
            if next_edge.getID() not in edges:
                continue
            if any(conn.getFromLane().allows("passenger") and conn.getToLane().allows("passenger") for conn in connections):
                nxt.append(next_edge.getID())
        adj[eid] = sorted(set(nxt))
    return edges, adj

def freeflow(e):
    return e.getLength() / max(e.getSpeed(), 0.1)

def search(origin, dest, departure, edges, adj, occupancy, bin_s, pressure):
    queue = [(freeflow(edges[origin]), origin)]
    best = {origin: freeflow(edges[origin])}
    prev = {}
    g3_emit("search_start", origin=origin, destination=dest, departure_s=departure,
            bin_seconds=bin_s, pressure=pressure)
    while queue:
        cost, u = heapq.heappop(queue)
        g3_emit("heap_pop", edge=u, popped_cost_s=cost, best_cost_s=best[u],
                stale=cost > best[u] + 1e-8)
        if cost > best[u] + 1e-8: continue
        if u == dest:
            g3_emit("destination_reached", edge=u, best_cost_s=best[u])
            break
        for v in adj[u]:
            entry = departure + cost
            b = int(entry // bin_s)
            e = edges[v]
            # Forecast occupancy is an assignment proxy, NOT calibrated physical queue length.
            cap_proxy = max(1.0, e.getLength() * max(e.getLaneNumber(), 1) / 7.5)
            # Read the exact original counter once; emit after computing the cost.
            assigned_count = occupancy[(v, b)]
            predicted = assigned_count / cap_proxy
            turn_proxy = 1.0 if len(adj[u]) > 1 else 0.0
            cost_v = freeflow(e) * (1.0 + pressure * predicted) + turn_proxy
            new = cost + cost_v
            g3_emit("edge_lookup", from_edge=u, to_edge=v,
                    heap_cost_s=cost, predicted_entry_s=entry, lookup_bin=b,
                    prior_assigned_count=assigned_count, capacity_proxy=cap_proxy,
                    freeflow_edge_s=freeflow(e),
                    congestion_surcharge_s=freeflow(e) * pressure * predicted,
                    junction_proxy_s=turn_proxy, new_label_cost_s=new,
                    previous_best_s=best.get(v, float("inf")),
                    accepted_for_heap=new < best.get(v, float("inf")) - 1e-8)
            if new < best.get(v, float("inf")) - 1e-8:
                best[v] = new; prev[v] = u
                heapq.heappush(queue, (new, v))
    if dest not in best: raise RuntimeError("No legal path: " + origin + " to " + dest)
    path = [dest]
    while path[-1] != origin: path.append(prev[path[-1]])
    path.reverse()
    g3_emit("search_end", path_edges=" ".join(path), winning_cost_s=best[dest])
    return path, best[dest]

def ff_path(net, origin, dest):
    path, _ = net.getShortestPath(net.getEdge(origin), net.getEdge(dest), vClass="passenger")
    if not path: raise RuntimeError("No baseline route")
    return [e.getID() for e in path]

def route_distance(path, edges):
    return sum(edges[e].getLength() for e in path)

def main():
    global G3_ACTIVE_VEHICLE, G3_DECISION_ORDINAL, G3_ASSIGNMENT_REVISION
    G3_ACTIVE_VEHICLE = None
    G3_DECISION_ORDINAL = -1
    G3_ASSIGNMENT_REVISION = 0
    p = argparse.ArgumentParser()
    p.add_argument("--net", required=True); p.add_argument("--trips", required=True)
    p.add_argument("--out", required=True); p.add_argument("--audit", required=True)
    p.add_argument("--manifest", required=True)
    p.add_argument("--bin-seconds", type=int, default=30)
    p.add_argument("--pressure", type=float, default=1.0)
    p.add_argument("--detour-percent", type=float, default=0.10)
    p.add_argument("--detour-seconds", type=float, default=30)
    p.add_argument("--distance-percent", type=float, default=0.15)
    a = p.parse_args()
    if a.bin_seconds <= 0 or a.pressure < 0: raise ValueError("Invalid bin/pressure")
    net = sumolib.net.readNet(a.net)
    edges, adj = build_graph(net)
    trips = ET.parse(a.trips).getroot().findall("trip")
    occupancy = collections.Counter()
    output = ET.Element("routes")
    ET.SubElement(output, "vType", id="passenger", vClass="passenger")
    rows = []
    for ordinal, t in enumerate(sorted(trips, key=lambda t: (float(t.get("depart")), t.get("id")))):
        G3_ACTIVE_VEHICLE = t.get("id")
        G3_DECISION_ORDINAL = ordinal
        origin, dest, depart = t.get("from"), t.get("to"), float(t.get("depart"))
        g3_emit("decision_start", origin=origin, destination=dest, departure_s=depart)
        base = ff_path(net, origin, dest)
        candidate, forecast_cost = search(origin, dest, depart, edges, adj, occupancy, a.bin_seconds, a.pressure)
        base_time = sum(freeflow(edges[e]) for e in base)
        candidate_time = sum(freeflow(edges[e]) for e in candidate)
        base_distance = route_distance(base, edges)
        candidate_distance = route_distance(candidate, edges)
        time_allowance = min(a.detour_seconds, a.detour_percent * base_time)
        eligible = candidate_time <= base_time + time_allowance + 1e-8 and candidate_distance <= base_distance * (1 + a.distance_percent) + 1e-8
        chosen = candidate if eligible else base
        g3_emit("guardrail_decision", accepted=bool(eligible),
                candidate_edges=" ".join(candidate), chosen_edges=" ".join(chosen),
                baseline_edges=" ".join(base), candidate_freeflow_s=candidate_time,
                baseline_freeflow_s=base_time, forecast_heap_cost_s=forecast_cost)
        vehicle = ET.SubElement(output, "vehicle", id=t.get("id"), type="passenger", depart=t.get("depart"))
        ET.SubElement(vehicle, "route", edges=" ".join(chosen))
        clock = depart
        for eid in chosen:
            b = int(clock // a.bin_seconds)
            before = occupancy[(eid,b)] if G3_SEARCH_TRACE_SINK is not None else None
            occupancy[(eid, b)] += 1
            if G3_SEARCH_TRACE_SINK is not None:
                G3_ASSIGNMENT_REVISION += 1
                g3_emit("assignment_update", edge=eid, lookup_bin=b,
                        prior_assigned_count=before, new_assigned_count=occupancy[(eid,b)])
            clock += freeflow(edges[eid])
        g3_emit("decision_end", updated_edges=len(chosen))
        rows.append([t.get("id"), t.get("depart"), int(eligible), int(chosen != base), round(base_time,3), round(candidate_time,3), round(base_distance,3), round(candidate_distance,3), round(forecast_cost,3)])
    ET.ElementTree(output).write(a.out, encoding="utf-8", xml_declaration=True)
    with open(a.audit, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["vehicle","depart","accepted","route_changed","baseline_freeflow_s","candidate_freeflow_s","baseline_distance_m","candidate_distance_m","candidate_predicted_cost"]); w.writerows(rows)
    with open(a.manifest, "w") as f:
        json.dump({"algorithm":"time-binned advance-announcement occupancy proxy v0.1","bin_seconds":a.bin_seconds,"pressure":a.pressure,"detour_percent":a.detour_percent,"detour_seconds":a.detour_seconds,"distance_percent":a.distance_percent,"vehicles":len(trips),"changed_routes":sum(r[3] for r in rows),"assumptions":["all announced trips known at planning time","capacity and intersection delays are uncalibrated proxies","not live rerouting","predicted bounds do not guarantee realized bounds"]},f,indent=2)
    if len(trips) != 1000: raise RuntimeError("Expected 1000 trips")
if __name__ == "__main__": main()
