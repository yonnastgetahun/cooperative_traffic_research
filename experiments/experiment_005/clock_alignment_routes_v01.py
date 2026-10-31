#!/usr/bin/env python3
"""Experiment 005. Only chosen-route assignment bin update varies between D and E."""
import argparse
import collections
import csv
import json
import math
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import sumolib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiment_002"))
sys.path.insert(0, str(ROOT / "experiment_004"))
import time_aware as policy
from prospective_search_adapter_v01 import search as stateful_search

COEFF = {
    200: (4.053135104279146, 11.524898884412591),
    600: (1.7868471223107676, 3.9515691107998387),
    1200: (1.8903085164618962, 2.6820862794976956),
}
BIN_SECONDS = 30
PRESSURE = 1.0


def legacy_bins(chosen, depart, edges, bin_s=BIN_SECONDS):
    """Byte-for-byte behavioral definition of original time_aware.py update clock."""
    clock = depart
    result = []
    for eid in chosen:
        result.append(int(clock // bin_s))
        clock += policy.freeflow(edges[eid])
    return result


def aligned_bins(chosen, depart, edges, adj, occupancy, offset_s, per_edge_s,
                 bin_s=BIN_SECONDS, pressure=PRESSURE):
    """Replay *chosen* route against fixed preassignment counters, then apply bins.

    Replay successor costs exactly as prospective_search_adapter_v01.search.
    Fallback paths rejected by search guardrails use the same replay definition.
    """
    if not chosen or bin_s <= 0 or offset_s < 0 or per_edge_s < 0:
        raise ValueError("Invalid chosen route or calibration")
    bins = [int((depart + offset_s) // bin_s)]
    cost = policy.freeflow(edges[chosen[0]])
    for ordinal, (u, v) in enumerate(zip(chosen, chosen[1:]), start=1):
        entry = depart + cost + offset_s + per_edge_s * ordinal
        b = int(entry // bin_s)
        bins.append(b)
        e = edges[v]
        ff = policy.freeflow(e)
        cap = max(1.0, e.getLength() * max(e.getLaneNumber(), 1) / 7.5)
        surcharge = ff * pressure * (occupancy[(v, b)] / cap)
        turn = 1.0 if len(adj[u]) > 1 else 0.0
        cost = cost + ff + surcharge + turn
    return bins


def generate(net_path, trips_path, window, mode, output):
    if window not in COEFF or mode not in ("D", "E"):
        raise ValueError("Unknown frozen window / arm")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    net = sumolib.net.readNet(str(net_path))
    edges, adj = policy.build_graph(net)
    trips = ET.parse(trips_path).getroot().findall("trip")
    if len(trips) != 1000:
        raise ValueError("Expected 1000 trips")
    occupancy = collections.Counter()
    routes = ET.Element("routes")
    ET.SubElement(routes, "vType", id="passenger", vClass="passenger")
    rows = []
    a, b = COEFF[window]
    for trip in sorted(trips, key=lambda t: (float(t.get("depart")), t.get("id"))):
        origin, dest, depart = trip.get("from"), trip.get("to"), float(trip.get("depart"))
        base = policy.ff_path(net, origin, dest)
        candidate, forecast_cost = stateful_search(
            origin, dest, depart, edges, adj, occupancy, BIN_SECONDS, PRESSURE,
            offset_s=a, per_edge_s=b, force_stateful_zero=True,
        )
        base_time = sum(policy.freeflow(edges[e]) for e in base)
        candidate_time = sum(policy.freeflow(edges[e]) for e in candidate)
        base_distance = policy.route_distance(base, edges)
        candidate_distance = policy.route_distance(candidate, edges)
        time_allowance = min(30.0, 0.10 * base_time)
        eligible = (candidate_time <= base_time + time_allowance + 1e-8
                    and candidate_distance <= base_distance * 1.15 + 1e-8)
        chosen = candidate if eligible else base
        vehicle = ET.SubElement(
            routes, "vehicle", id=trip.get("id"), type="passenger", depart=trip.get("depart")
        )
        ET.SubElement(vehicle, "route", edges=" ".join(chosen))
        if mode == "D":
            bins = legacy_bins(chosen, depart, edges)
        else:
            bins = aligned_bins(chosen, depart, edges, adj, occupancy, a, b)
        # Do not update occupancy until ALL candidate-clock bins are determined.
        for edge, time_bin in zip(chosen, bins):
            occupancy[(edge, time_bin)] += 1
        rows.append([
            trip.get("id"), trip.get("depart"), int(eligible), int(chosen != base),
            round(base_time, 3), round(candidate_time, 3),
            round(base_distance, 3), round(candidate_distance, 3),
            round(forecast_cost, 3),
        ])
    ET.ElementTree(routes).write(
        output / "routes.rou.xml", encoding="utf-8", xml_declaration=True
    )
    with (output / "audit.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "vehicle", "depart", "accepted", "route_changed", "baseline_freeflow_s",
            "candidate_freeflow_s", "baseline_distance_m", "candidate_distance_m",
            "candidate_predicted_cost",
        ])
        w.writerows(rows)
    manifest = {
        "algorithm": "time-binned advance-announcement occupancy proxy v0.1",
        "bin_seconds": BIN_SECONDS, "pressure": PRESSURE,
        "detour_percent": 0.10, "detour_seconds": 30, "distance_percent": 0.15,
        "vehicles": len(trips), "changed_routes": sum(r[3] for r in rows),
        "experiment": "005", "arm": mode, "window_seconds": window,
        "calibration_coefficients": [a, b],
        "assignment_update_clock": "freeflow" if mode == "D" else "calibrated_replay",
        "forecast_uses_future_sumo_observations": False,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--net", required=True)
    p.add_argument("--trips", required=True)
    p.add_argument("--window", type=int, required=True)
    p.add_argument("--arm", choices=("D", "E"), required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    generate(args.net, args.trips, args.window, args.arm, args.out)
