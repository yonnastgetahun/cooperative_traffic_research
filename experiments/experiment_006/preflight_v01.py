#!/usr/bin/env python3
"""Development seed 2101 preflight: identical frozen A/E outputs, no fresh cohort."""
import argparse
import hashlib
import json
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from run_pair_v01 import (
    SCIENTIFIC_BASE, POLICY_SOURCE, check_revision, demand, routes, sha256,
)

def execute(window, scientific, policies):
    check_revision(scientific, SCIENTIFIC_BASE)
    check_revision(policies, POLICY_SOURCE)
    with tempfile.TemporaryDirectory(prefix="exp006-development-") as tmp:
        root = Path(tmp)
        net, trips, expected = demand(2101, window, root, scientific)
        report = {"seed": 2101, "window_seconds": window,
                  "demand_sha256": sha256(trips), "arms": {}}
        for arm in ("A", "E"):
            first = root / f"{arm}-reference"
            second = root / f"{arm}-verification"
            first.parent.mkdir(exist_ok=True)
            first.mkdir()
            second.mkdir()
            r1 = routes(arm, net, trips, window, first / "routing", policies)
            r2 = routes(arm, net, trips, window, second / "routing", policies)
            if r1 != r2 or set(r1) != expected:
                raise ValueError(f"{arm}: route IDs mismatch, nonrepeatability or missing vehicles")
            for file in ("routes.rou.xml", "audit.csv"):
                a = (first / "routing" / file).read_bytes()
                b = (second / "routing" / file).read_bytes()
                if a != b:
                    raise ValueError(f"{arm}: bytewise {file} parity failed")
            report["arms"][arm] = {
                "route_sha256": sha256(first / "routing" / "routes.rou.xml"),
                "audit_sha256": sha256(first / "routing" / "audit.csv"),
                "number_of_routes": len(r1),
            }
        # Validate the unmodified independent A generator: all A routes match
        # original frozen nominal free-flow shortest paths, vehicle by vehicle.
        sys.path.insert(0, str(policies / "experiments" / "experiment_002"))
        import time_aware as policy
        import sumolib
        network = sumolib.net.readNet(str(net))
        originals = {x.get("id"): x for x in ET.parse(trips).getroot().findall("trip")}
        arm_A = root / "A-reference" / "routing" / "routes.rou.xml"
        actual = {v.get("id"): v.find("route").get("edges").split()
                  for v in ET.parse(arm_A).getroot().findall("vehicle")}
        if any(actual[vid] != policy.ff_path(network, x.get("from"), x.get("to"))
               for vid,x in originals.items()):
            raise ValueError("A is not the frozen nominal free-flow shortest-path policy")
        print(json.dumps({"status": "PASS", **report}, indent=2))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--window", type=int, choices=(200, 600, 1200), required=True)
    p.add_argument("--scientific", required=True)
    p.add_argument("--policy-source", required=True)
    a = p.parse_args()
    execute(a.window, Path(a.scientific).resolve(), Path(a.policy_source).resolve())
