#!/usr/bin/env python3
"""Advance-announcement, time-binned routing prototype. NOT live routing or a safety guarantee."""
import argparse, collections, csv, heapq, json, math, os, sys
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.join(os.environ.get("SUMO_HOME", "/usr/share/sumo"), "tools"))
import sumolib

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
    while queue:
        cost, u = heapq.heappop(queue)
        if cost > best[u] + 1e-8: continue
        if u == dest: break
        for v in adj[u]:
            entry = departure + cost
            b = int(entry // bin_s)
            e = edges[v]
            # Forecast occupancy is an assignment proxy, NOT calibrated physical queue length.
            cap_proxy = max(1.0, e.getLength() * max(e.getLaneNumber(), 1) / 7.5)
            predicted = occupancy[(v, b)] / cap_proxy
            turn_proxy = 1.0 if len(adj[u]) > 1 else 0.0
            cost_v = freeflow(e) * (1.0 + pressure * predicted) + turn_proxy
            new = cost + cost_v
            if new < best.get(v, float("inf")) - 1e-8:
                best[v] = new; prev[v] = u
                heapq.heappush(queue, (new, v))
    if dest not in best: raise RuntimeError("No legal path: " + origin + " to " + dest)
    path = [dest]
    while path[-1] != origin: path.append(prev[path[-1]])
    path.reverse()
    return path, best[dest]

def ff_path(net, origin, dest):
    path, _ = net.getShortestPath(net.getEdge(origin), net.getEdge(dest), vClass="passenger")
    if not path: raise RuntimeError("No baseline route")
    return [e.getID() for e in path]

def route_distance(path, edges):
    return sum(edges[e].getLength() for e in path)

def main():
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
    for t in sorted(trips, key=lambda t: (float(t.get("depart")), t.get("id"))):
        origin, dest, depart = t.get("from"), t.get("to"), float(t.get("depart"))
        base = ff_path(net, origin, dest)
        candidate, forecast_cost = search(origin, dest, depart, edges, adj, occupancy, a.bin_seconds, a.pressure)
        base_time = sum(freeflow(edges[e]) for e in base)
        candidate_time = sum(freeflow(edges[e]) for e in candidate)
        base_distance = route_distance(base, edges)
        candidate_distance = route_distance(candidate, edges)
        time_allowance = min(a.detour_seconds, a.detour_percent * base_time)
        eligible = candidate_time <= base_time + time_allowance + 1e-8 and candidate_distance <= base_distance * (1 + a.distance_percent) + 1e-8
        chosen = candidate if eligible else base
        vehicle = ET.SubElement(output, "vehicle", id=t.get("id"), type="passenger", depart=t.get("depart"))
        ET.SubElement(vehicle, "route", edges=" ".join(chosen))
        clock = depart
        for eid in chosen:
            b = int(clock // a.bin_seconds)
            occupancy[(eid, b)] += 1
            clock += freeflow(edges[eid])
        rows.append([t.get("id"), t.get("depart"), int(eligible), int(chosen != base), round(base_time,3), round(candidate_time,3), round(base_distance,3), round(candidate_distance,3), round(forecast_cost,3)])
    ET.ElementTree(output).write(a.out, encoding="utf-8", xml_declaration=True)
    with open(a.audit, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["vehicle","depart","accepted","route_changed","baseline_freeflow_s","candidate_freeflow_s","baseline_distance_m","candidate_distance_m","candidate_predicted_cost"]); w.writerows(rows)
    with open(a.manifest, "w") as f:
        json.dump({"algorithm":"time-binned advance-announcement occupancy proxy v0.1","bin_seconds":a.bin_seconds,"pressure":a.pressure,"detour_percent":a.detour_percent,"detour_seconds":a.detour_seconds,"distance_percent":a.distance_percent,"vehicles":len(trips),"changed_routes":sum(r[3] for r in rows),"assumptions":["all announced trips known at planning time","capacity and intersection delays are uncalibrated proxies","not live rerouting","predicted bounds do not guarantee realized bounds"]},f,indent=2)
    if len(trips) != 1000: raise RuntimeError("Expected 1000 trips")
if __name__ == "__main__": main()
