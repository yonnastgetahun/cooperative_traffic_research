#!/usr/bin/env python3
"""Seed-paired independent-unit statistical analysis of frozen Exp005 D vs E."""
import argparse
import collections
import json
import math
import statistics
import xml.etree.ElementTree as ET
from pathlib import Path

SEEDS = tuple(range(3401, 3411))
WINDOWS = (200, 600, 1200)
T_95_DF9 = 2.2621571627409915


def percentile(values, fraction):
    s = sorted(values)
    return s[math.ceil(fraction * len(s)) - 1] if s else None


def ci10(values):
    if len(values) != 10:
        raise ValueError("Ten seed-level values required")
    mean = statistics.mean(values)
    halfwidth = T_95_DF9 * statistics.stdev(values) / math.sqrt(10)
    return {"mean": mean, "ci95": [mean - halfwidth, mean + halfwidth], "n_seeds": 10}


def route_map(path):
    vehicles = ET.parse(path).getroot().findall("vehicle")
    result = {v.get("id"): tuple(v.find("route").get("edges").split()) for v in vehicles}
    if len(result) != len(vehicles):
        raise ValueError("Duplicate route ID")
    return result


def trip_map(path):
    trips = ET.parse(path).getroot().findall("tripinfo")
    result = {t.get("id"): {
        "duration": float(t.get("duration")),
        "waiting": float(t.get("waitingTime", "0")),
        "time_loss": float(t.get("timeLoss", "0")),
    } for t in trips}
    if len(result) != len(trips):
        raise ValueError("Duplicate completed-trip ID")
    return result


def route_concentration(routes, net):
    edges = ET.parse(net).getroot().findall("edge")
    ids = [e.get("id") for e in edges
           if not e.get("id", "").startswith(":") and e.get("function") != "internal"]
    counts = collections.Counter({eid: 0 for eid in ids})
    for path in routes.values():
        counts.update(path)
    x = sorted(counts.values())
    n = len(x)
    total = sum(x)
    if n < 2 or total <= 0:
        raise ValueError("Invalid network assignment counts")
    gini = (2 * sum((i + 1) * v for i, v in enumerate(x)) / (n * total)
            - (n + 1) / n)
    top_n = max(1, math.ceil(n * 0.1))
    return {"gini": gini, "top_decile_share": sum(x[-top_n:]) / total}


def scenario(folder, seed, window):
    a = json.loads((folder / "attempt.json").read_text())
    if a["status"] != "COMPLETE" or a["seed"] != seed or a["window_seconds"] != window:
        raise ValueError(f"Invalid attempt: {folder}")
    arms = {}
    for arm in ("D", "E"):
        p = folder / arm
        routes = route_map(p / "routing" / "routes.rou.xml")
        trips = trip_map(p / "tripinfo.xml")
        if len(routes) != 1000 or set(trips) - set(routes):
            raise ValueError(f"Missing/extra vehicle IDs: {folder}, {arm}")
        x = list(v["duration"] for v in trips.values())
        arms[arm] = {
            "routes": routes, "trips": trips,
            "n_completed": len(trips),
            "mean_trip_s": statistics.mean(x) if x else None,
            "p90_trip_s": percentile(x, 0.9),
            "assignment": route_concentration(routes, folder / "network.net.xml"),
        }
    D, E = arms["D"], arms["E"]
    if set(D["routes"]) != set(E["routes"]):
        raise ValueError("Arm vehicle identity mismatch")
    matched = set(D["trips"]) & set(E["trips"])
    if len(matched) != 1000:
        # Do not infer the primary all-departure effect from selective completions.
        raise ValueError(f"Incomplete matched data: {folder} has {len(matched)}")
    changed = {v for v in matched if D["routes"][v] != E["routes"][v]}
    unchanged = matched - changed
    def subset(identities):
        if not identities:
            raise ValueError("Empty subgroup")
        diffs = [D["trips"][v]["duration"] - E["trips"][v]["duration"]
                 for v in sorted(identities)]
        waits = [D["trips"][v]["waiting"] - E["trips"][v]["waiting"]
                 for v in sorted(identities)]
        return {
            "n": len(diffs), "mean_D_minus_E_trip_s": statistics.mean(diffs),
            "mean_D_minus_E_wait_s": statistics.mean(waits),
            "E_helped": sum(d > 0 for d in diffs),
            "E_harmed": sum(d < 0 for d in diffs),
            "unchanged_duration": sum(d == 0 for d in diffs),
        }
    return {
        "seed": seed, "window_seconds": window,
        "D": {k: v for k, v in D.items() if k not in ("routes", "trips")},
        "E": {k: v for k, v in E.items() if k not in ("routes", "trips")},
        "D_minus_E_mean_trip_s": D["mean_trip_s"] - E["mean_trip_s"],
        "D_minus_E_p90_s": D["p90_trip_s"] - E["p90_trip_s"],
        "D_minus_E_gini": D["assignment"]["gini"] - E["assignment"]["gini"],
        "D_minus_E_top_decile_share":
            D["assignment"]["top_decile_share"] - E["assignment"]["top_decile_share"],
        "changed": subset(changed), "unchanged": subset(unchanged),
        "all": subset(matched),
    }


def evaluate(root):
    records = []
    for window in WINDOWS:
        for seed in SEEDS:
            folder = Path(root) / f"exp005-seed-{seed}-window-{window}"
            records.append(scenario(folder, seed, window))
    summary = {}
    for window in WINDOWS:
        rows = [r for r in records if r["window_seconds"] == window]
        out = {"n_scenarios": 10, "matched_driver_count": 10000}
        for key in ("D_minus_E_mean_trip_s", "D_minus_E_p90_s",
                    "D_minus_E_gini", "D_minus_E_top_decile_share"):
            out[key] = ci10([r[key] for r in rows])
        for category in ("changed", "unchanged", "all"):
            out[category] = {
                "matched_vehicles": sum(r[category]["n"] for r in rows),
                "mean_trip_s": ci10([r[category]["mean_D_minus_E_trip_s"] for r in rows]),
                "mean_wait_s": ci10([r[category]["mean_D_minus_E_wait_s"] for r in rows]),
                "helped_E": sum(r[category]["E_helped"] for r in rows),
                "harmed_E": sum(r[category]["E_harmed"] for r in rows),
            }
        summary[str(window)] = out
    primary = summary["200"]
    interval = primary["D_minus_E_mean_trip_s"]["ci95"]
    tail_E_minus_D = -primary["D_minus_E_p90_s"]["mean"]
    harmed_E_fraction = primary["all"]["harmed_E"] / 10000
    if interval[0] > 0 and tail_E_minus_D <= 5 and harmed_E_fraction <= 0.5:
        decision = "GO for aligned update relative to original D only"
    elif interval[1] < 0:
        decision = "NO-GO: aligned update increased primary mean trip time"
    elif interval[0] > 0:
        decision = "PRIMARY IMPROVED but secondary fairness/tail gate failed"
    else:
        decision = "INCONCLUSIVE: primary seed-level interval overlaps zero"
    return {
        "evidence": "Original frozen demand / route and SUMO archives; 30 fresh pairs",
        "interpretation_warning": "Comparisons identify only this assignment-clock intervention under controlled synthetic network conditions; not an independent-routing advantage.",
        "primary_decision": decision,
        "primary_tail_E_minus_D_s": tail_E_minus_D,
        "primary_E_harmed_fraction": harmed_E_fraction,
        "regimes": summary,
        "seed_pairs": records,
    }


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--root", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    result = evaluate(args.root)
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "primary_decision": result["primary_decision"],
        "primary_D_minus_E_mean": result["regimes"]["200"]["D_minus_E_mean_trip_s"],
        "regime_differences": {
            w: result["regimes"][str(w)]["D_minus_E_mean_trip_s"]["mean"]
            for w in WINDOWS
        },
    }, indent=2))
