#!/usr/bin/env python3
"""B-H1 source-backed FCD diagnostic contract; not a causal mediation estimator.

Stopped main vehicles on J's internal crossing plus waiting cross vehicles
are co-occurrence *candidates*, not proof that one blocked the other. The
paired keep-clear N condition and traffic-priority rule must be interpreted.
This code does not call SUMO.
"""
from __future__ import annotations
import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def diagnostic(root: ET.Element) -> dict:
    if root.tag != "fcd-export":
        raise AssertionError("Not an FCD export")
    count_t = 0
    main_stopped = 0
    cross_waiting = 0
    simultaneous = 0
    all_t = []
    for timestep in root.findall("timestep"):
        count_t += 1
        time = float(timestep.get("time"))
        main = []
        cross = []
        for veh in timestep.findall("vehicle"):
            id_ = veh.get("id", "")
            lane = veh.get("lane")
            speed = veh.get("speed")
            if lane is None or speed is None:
                raise AssertionError("FCD lane/speed needed; enable output attributes")
            if id_.startswith("m") and lane.startswith(":J_0") and float(speed) <= 0.1:
                main.append(id_)
            if id_.startswith("x") and lane == "x_in_0" and float(speed) <= 0.1:
                cross.append(id_)
        a, b = bool(main), bool(cross)
        main_stopped += a
        cross_waiting += b
        simultaneous += a and b
        if a and b:
            all_t.append(time)
    if count_t == 0:
        raise AssertionError("No time samples in FCD")
    return {
        "timesteps": count_t,
        "stopped_main_on_internal_J_steps": main_stopped,
        "cross_waiting_upstream_J_steps": cross_waiting,
        "simultaneous_stalled_J_main_and_upstream_cross_steps": simultaneous,
        "simultaneous_sample_times": all_t,
        "claim_limit": "co-occurrence only: cross could be yielding to priority, not necessarily spillback",
    }


def evaluate(outdir: Path):
    results = {}
    for physical in ("S", "N"):
        for arm in ("I", "V"):
            path = outdir / f"bh1_{physical}_{arm}.fcd.xml"
            if not path.exists():
                raise AssertionError(f"Missing physical FCD file: {path}")
            results[f"{physical}_{arm}"] = diagnostic(ET.parse(path).getroot())
    (outdir / "fcd-cooccurrence-diagnostics.json").write_text(
        json.dumps(results, indent=2) + "\n")
    print("FCD diagnostics written; no causal mediator was proven by co-occurrence.")


def test():
    r = ET.fromstring(
        '<fcd-export>'
        '<timestep time="0"><vehicle id="m000" lane=":J_0_0" speed="0.0"/>'
        '<vehicle id="x000" lane="x_in_0" speed="0.0"/></timestep>'
        '<timestep time="1"><vehicle id="m000" lane="pocket_0" speed="1.0"/>'
        '<vehicle id="x000" lane="x_in_0" speed="0.0"/></timestep>'
        '</fcd-export>')
    out = diagnostic(r)
    assert out["timesteps"] == 2
    assert out["simultaneous_stalled_J_main_and_upstream_cross_steps"] == 1
    try:
        diagnostic(ET.fromstring(
            '<fcd-export><timestep time="0">'
            '<vehicle id="m000" speed="0"/></timestep></fcd-export>'))
    except AssertionError:
        pass
    else:
        raise AssertionError("Missing FCD lane was not rejected")
    print("Fictitious FCD diagnostic unit test PASS; no actual traffic data.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=("test", "evaluate"))
    ap.add_argument("--out", type=Path, default=Path("bh1-stage1-static"))
    a = ap.parse_args()
    if a.action == "test":
        test()
    else:
        evaluate(a.out)
