#!/usr/bin/env python3
"""Strict B-H1 output accounting contract; test fixtures only, no SUMO execution.

This module can parse future SUMO tripinfo files, but cannot establish
physical spillback mediation merely from tripinfo or aggregate queue logs.
"""
from __future__ import annotations
import argparse
import json
import xml.etree.ElementTree as ET
from pathlib import Path


def parse_complete_tripinfo(root: ET.Element, inputs: list[dict]) -> dict:
    expected = {r["id"]: r for r in inputs}
    if len(expected) != len(inputs):
        raise AssertionError("Nonunique original driver identifiers")
    trips = root.findall("tripinfo")
    observed = {t.get("id"): t for t in trips}
    if len(observed) != len(trips) or set(observed) != set(expected):
        raise AssertionError("Missing, extra, or duplicate original tripinfo ID")
    ledger = {}
    for vid, r in expected.items():
        t = observed[vid]
        if t.get("depart") is None or t.get("arrival") is None:
            raise AssertionError(f"Not completed: {vid}")
        pref = float(r["preferred"])
        requested = float(r["requested"])
        actual = float(t.get("depart"))
        arrival = float(t.get("arrival"))
        if not (arrival >= actual >= requested >= pref):
            raise AssertionError(f"Nonmonotonic preferred/requested/insertion/arrival: {vid}")
        d_delay = float(t.get("departDelay", "nan"))
        if abs(d_delay - (actual - requested)) > 1.01:
            raise AssertionError(f"SUMO insertion-delay inconsistency for {vid}")
        cost = arrival - pref
        parts = ((requested - pref) + (actual - requested) + (arrival - actual))
        if abs(cost - parts) > 1e-7:
            raise AssertionError(f"Clock decomposition failed: {vid}")
        ledger[vid] = {
            "id": vid, "preferred": pref, "requested": requested,
            "inserted": actual, "arrived": arrival, "cost": cost,
            "eligible": r["eligible"], "willing": r["willing"],
            "kind": r["kind"], "route": r["route"],
        }
    return ledger


def summarize(ledger: dict) -> dict:
    ids = sorted(ledger)
    return {
        "N": len(ids), "all_driver_elapsed": sum(ledger[v]["cost"] for v in ids),
        "cross_traffic_elapsed": sum(ledger[v]["cost"] for v in ids if ledger[v]["kind"] == "cross"),
        "noneligible_elapsed": sum(ledger[v]["cost"] for v in ids if not ledger[v]["eligible"]),
    }


def evaluate(outdir: Path):
    """Evaluation-only entrypoint after future physical execution; not in CI."""
    original = json.loads((outdir / "bh1-input-contract.json").read_text())
    ids = {r["id"] for r in original["roster"]}
    if len(ids) != 96:
        raise AssertionError("Unexpected original 96-ID contract")
    arms = {}
    for m in ("S", "N"):
        for policy in ("I", "V"):
            path = outdir / f"bh1_{m}_{policy}.inputs.json"
            inputs = json.loads(path.read_text())["roster"]
            if {r["id"] for r in inputs} != ids:
                raise AssertionError("Original IDs differ across arms")
            tripinfo = outdir / f"bh1_{m}_{policy}.tripinfo.xml"
            if not tripinfo.exists():
                raise AssertionError(f"Missing physical tripinfo evidence: {tripinfo}")
            ledger = parse_complete_tripinfo(ET.parse(tripinfo).getroot(), inputs)
            arms[f"{m}_{policy}"] = {"summary": summarize(ledger), "ledger": ledger}
    contrasts = {}
    for m in ("S", "N"):
        bi = arms[f"{m}_I"]["ledger"]
        vi = arms[f"{m}_V"]["ledger"]
        diff = {vid: vi[vid]["cost"] - bi[vid]["cost"] for vid in ids}
        contrasts[m] = {
            "all_driver_delta": sum(diff.values()),
            "noneligible_delta": sum(diff[vid] for vid in ids if not bi[vid]["eligible"]),
            "noneligible_over_10s": sum(
                diff[vid] > 10 for vid in ids if not bi[vid]["eligible"]),
            "severe_noneligible_over_30s": sum(
                diff[vid] > 30 for vid in ids if not bi[vid]["eligible"]),
            "individual_deltas": diff,
        }
    results = {
        "interpretation": "TRIPINFO COSTS ONLY, NOT PHYSICAL SPILLBACK MEDIATION",
        "S": contrasts["S"],
        "N": contrasts["N"],
        "psi": contrasts["S"]["all_driver_delta"] - contrasts["N"]["all_driver_delta"],
    }
    (outdir / "physical-tripinfo-only-evaluation.json").write_text(
        json.dumps(results, indent=2) + "\n")
    print("Complete matched tripinfo cost ledger written. PHYSICAL MECHANISM STILL REQUIRES SEPARATE FCD/QUEUE EVIDENCE.")


def test_contract():
    """Fictitious 2-ID unit fixtures: no source or synthetic SUMO scenario."""
    inputs = [
        {"id": "demo-a", "preferred": 0, "requested": 5,
         "eligible": True, "willing": True, "kind": "main", "route": ["a"]},
        {"id": "demo-b", "preferred": 0, "requested": 0,
         "eligible": False, "willing": False, "kind": "cross", "route": ["b"]},
    ]
    root = ET.fromstring(
        '<tripinfos>'
        '<tripinfo id="demo-a" depart="6" departDelay="1" arrival="22"/>'
        '<tripinfo id="demo-b" depart="0" departDelay="0" arrival="30"/>'
        '</tripinfos>')
    rows = parse_complete_tripinfo(root, inputs)
    assert abs(rows["demo-a"]["cost"] - 22) < 1e-12
    assert abs(sum(r["cost"] for r in rows.values()) - 52) < 1e-12
    try:
        parse_complete_tripinfo(ET.fromstring('<tripinfos><tripinfo id="demo-a" depart="6" arrival="22"/></tripinfos>'), inputs)
    except AssertionError:
        pass
    else:
        raise AssertionError("Missing driver was not rejected")
    try:
        parse_complete_tripinfo(ET.fromstring(
            '<tripinfos>'
            '<tripinfo id="demo-a" depart="4" departDelay="0" arrival="22"/>'
            '<tripinfo id="demo-b" depart="0" departDelay="0" arrival="30"/>'
            '</tripinfos>'), inputs)
    except AssertionError:
        pass
    else:
        raise AssertionError("Early vehicle insertion was not rejected")
    print("Fictitious accounting contract PASS (no physical evidence and no SUMO run).")


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("action", choices=("test", "evaluate"))
    cli.add_argument("--out", type=Path, default=Path("bh1-stage1-static"))
    args = cli.parse_args()
    if args.action == "test":
        test_contract()
    else:
        evaluate(args.out)
