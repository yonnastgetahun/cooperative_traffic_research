#!/usr/bin/env python3
"""Frozen Exp005 scenario runner. Both arms use identical network, demand and SUMO settings."""
import argparse
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

FROZEN = "be2e8d27c78c8b6de4891115d6d951edc877ac6e"
SEEDS = tuple(range(3401, 3411))
WINDOWS = (200, 600, 1200)


def execute(cmd, logpath):
    with logpath.open("wb") as log:
        result = subprocess.run([str(x) for x in cmd], stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f"Failed stage {logpath.name}: return code {result.returncode}")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_demand(seed, window, output, frozen):
    net = output / "network.net.xml"
    trips = output / "trips.xml"
    execute(
        ["netgenerate", "--grid", "--grid.number", "10", "--grid.length", "200",
         "--output-file", net],
        output / "stage-network.log",
    )
    execute(
        [sys.executable, frozen / "experiments/experiment_002/fixed_demand_v01.py",
         "--net", net, "--out", trips, "--manifest", output / "demand.json",
         "--seed", seed, "--window", window],
        output / "stage-demand.log",
    )
    return net, trips


def run_pair(seed, window, output, frozen):
    if seed not in SEEDS or window not in WINDOWS:
        raise ValueError("Not a prespecified Exp005 seed/window")
    output = Path(output).resolve()
    frozen = Path(frozen).resolve()
    if subprocess.check_output(
        ["git", "-C", str(frozen), "rev-parse", "HEAD"], text=True
    ).strip() != FROZEN:
        raise ValueError("Frozen source mismatch")
    if output.exists():
        raise ValueError("No overwriting existing evidence")
    output.mkdir(parents=True)
    record = dict(
        status="FAILED", stage="initialization", seed=seed, window_seconds=window,
        frozen_source=FROZEN, arms=["D", "E"],
    )
    try:
        record["stage"] = "demand"
        net, trips = build_demand(seed, window, output, frozen)
        record["demand_sha256"] = digest(trips)
        for arm in ("D", "E"):
            arm_dir = output / arm
            arm_dir.mkdir()
            routing_dir = arm_dir / "routing"
            record["stage"] = "routing_" + arm
            execute(
                [sys.executable, Path(__file__).parent / "clock_alignment_routes_v01.py",
                 "--net", net, "--trips", trips, "--window", window,
                 "--arm", arm, "--out", routing_dir],
                arm_dir / "stage-route.log",
            )
            record["stage"] = "SUMO_" + arm
            execute(
                ["sumo", "-n", net, "-r", routing_dir / "routes.rou.xml",
                 "--tripinfo-output", arm_dir / "tripinfo.xml",
                 "--statistic-output", arm_dir / "statistics.xml",
                 "--collision-output", arm_dir / "collisions.xml",
                 "--seed", seed, "--no-step-log", "true", "--log", arm_dir / "sumo.log"],
                arm_dir / "stage-sumo.log",
            )
            parsed = ET.parse(arm_dir / "tripinfo.xml").getroot()
            ids = [t.get("id") for t in parsed.findall("tripinfo")]
            if len(ids) != len(set(ids)):
                raise ValueError(f"Duplicate IDs for arm {arm}")
            record[arm] = dict(
                n_completed=len(ids), n_incomplete=1000 - len(ids),
                route_sha256=digest(routing_dir / "routes.rou.xml"),
                tripinfo_sha256=digest(arm_dir / "tripinfo.xml"),
            )
        record["status"] = "COMPLETE"
        record["stage"] = "finished"
    except Exception as exc:
        record["error"] = str(exc)
    finally:
        (output / "attempt.json").write_text(json.dumps(record, indent=2) + "\n")
    return record


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--window", type=int, required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--frozen", required=True)
    args = p.parse_args()
    r = run_pair(args.seed, args.window, args.out, args.frozen)
    print(json.dumps(r))
    if r["status"] != "COMPLETE":
        sys.exit(1)
