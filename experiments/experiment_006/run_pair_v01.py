#!/usr/bin/env python3
"""Experiment 006: A-vs-E paired fresh-demand runner; immutable existing routing code."""
import argparse
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SEEDS = tuple(range(3501, 3511))
WINDOWS = (200, 600, 1200)
SCIENTIFIC_BASE = "be2e8d27c78c8b6de4891115d6d951edc877ac6e"
POLICY_SOURCE = "2997fd27c58e3b30cfd55a3c30ce4638ae8a1795"

def check_revision(path, target):
    actual = subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
    if actual != target:
        raise ValueError(f"Frozen revision mismatch for {path}: {actual} != {target}")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 256), b""):
            h.update(block)
    return h.hexdigest()

def call(command, log):
    with open(log, "wb") as f:
        p = subprocess.run(list(map(str, command)), stdout=f, stderr=subprocess.STDOUT)
    if p.returncode:
        raise RuntimeError(f"Stage {Path(log).name} failed ({p.returncode})")

def demand(seed, window, root, scientific):
    net = root / "network.net.xml"
    trips = root / "trips.xml"
    call(["netgenerate", "--grid", "--grid.number", "10", "--grid.length", "200",
          "--output-file", net], root / "network.log")
    call([sys.executable, scientific / "experiments/experiment_002/fixed_demand_v01.py",
          "--net", net, "--out", trips, "--manifest", root / "demand.json",
          "--seed", seed, "--window", window], root / "demand.log")
    trip_ids = [t.get("id") for t in ET.parse(trips).getroot().findall("trip")]
    if len(trip_ids) != 1000 or len(set(trip_ids)) != 1000:
        raise ValueError("Incorrect demand count / duplicate IDs")
    return net, trips, set(trip_ids)

def routes(arm, net, trips, window, output, policy_source):
    if arm == "A":
        code = policy_source / "experiments/experiment_004/four_arm_routes_v01.py"
    elif arm == "E":
        code = policy_source / "experiments/experiment_005/clock_alignment_routes_v01.py"
    else:
        raise ValueError("Only A and E")
    call([sys.executable, code, "--net", net, "--trips", trips, "--arm", arm,
          "--window", window, "--out", output], output.parent / "routing.log")
    x = ET.parse(output / "routes.rou.xml").getroot().findall("vehicle")
    values = {}
    for v in x:
        route = v.find("route")
        if route is None:
            raise ValueError("Missing route")
        values[v.get("id")] = (v.get("depart"), route.get("edges"))
    if len(values) != 1000:
        raise ValueError("Duplicate or absent vehicle routes")
    return values

def simulate(arm, seed, net, routing, output):
    call(["sumo", "-n", net, "-r", routing / "routes.rou.xml",
          "--tripinfo-output", output / "tripinfo.xml",
          "--statistic-output", output / "statistics.xml",
          "--collision-output", output / "collisions.xml",
          "--seed", seed, "--no-step-log", "true",
          "--log", output / "sumo.log"], output / "sumo-stage.log")
    records = ET.parse(output / "tripinfo.xml").getroot().findall("tripinfo")
    ids = [x.get("id") for x in records]
    if len(ids) != len(set(ids)) or len(ids) > 1000:
        raise ValueError("Invalid tripinfo IDs")
    return {"completed": len(ids), "incomplete": 1000-len(ids),
            "tripinfo_sha256": sha256(output / "tripinfo.xml")}

def run(seed, window, path, scientific, policy_source):
    if seed not in SEEDS or window not in WINDOWS:
        raise ValueError("Outside prospective frozen cohort")
    scientific = Path(scientific).resolve()
    policy_source = Path(policy_source).resolve()
    check_revision(scientific, SCIENTIFIC_BASE)
    check_revision(policy_source, POLICY_SOURCE)
    path = Path(path).resolve()
    if path.exists():
        raise ValueError("Evidence output exists; do not overwrite")
    path.mkdir(parents=True)
    attempt = {"experiment": "006", "status": "FAILED", "stage": "initial",
               "seed": seed, "window_seconds": window,
               "scientific_base": SCIENTIFIC_BASE, "policy_source": POLICY_SOURCE,
               "arms": ["A", "E"]}
    try:
        attempt["stage"] = "demand"
        net, trips, expected = demand(seed, window, path, scientific)
        attempt["demand_sha256"] = sha256(trips)
        attempt["network_sha256"] = sha256(net)
        for arm in ("A", "E"):
            output = path / arm
            output.mkdir()
            routing = output / "routing"
            attempt["stage"] = f"routing_{arm}"
            values = routes(arm, net, trips, window, routing, policy_source)
            if set(values) != expected:
                raise ValueError(f"Missing or extra routed vehicle IDs: {arm}")
            original_depart = {t.get("id"): t.get("depart")
                               for t in ET.parse(trips).getroot().findall("trip")}
            if any(values[i][0] != original_depart[i] for i in expected):
                raise ValueError("Departure time changed")
            attempt[arm] = {"routes_sha256": sha256(routing / "routes.rou.xml"),
                            "routing_audit_sha256": sha256(routing / "audit.csv")}
            attempt["stage"] = f"SUMO_{arm}"
            attempt[arm].update(simulate(arm, seed, net, routing, output))
        attempt["status"] = "COMPLETE"
        attempt["stage"] = "finished"
    except Exception as e:
        attempt["error"] = str(e)
    finally:
        (path / "attempt.json").write_text(json.dumps(attempt, indent=2) + "\n")
    return attempt

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--window", type=int, required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--scientific", required=True)
    p.add_argument("--policy-source", required=True)
    a = p.parse_args()
    result = run(a.seed, a.window, a.out, a.scientific, a.policy_source)
    print(json.dumps(result))
    if result["status"] != "COMPLETE":
        sys.exit(1)
