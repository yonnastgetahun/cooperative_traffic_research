#!/usr/bin/env python3
"""Create/inspect four B-H1 *static input* manifests only. NO SUMO traffic run.

An emitted I/V schedule or forecast does not establish actual travel time.
Run only after contract.check_policy has qualified both candidate I schedules.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

from contract import (
    DELAYS, NET_EDGES, ROUTES, base_schedule, cost, eligibility,
    qualify_independent, rank, roster, voluntary, xml_write,
)


def write_one(outdir: Path, physical: str, policy: str, schedule: dict[str, int]):
    original = roster()
    eligible, willing = eligibility()
    root = ET.Element("routes")
    ET.SubElement(root, "vType", id="bh1-fixed", length="5",
                  minGap="2.5", maxSpeed="13.9", speedFactor="1",
                  sigma="0", accel="2.6", decel="4.5")
    for record in sorted(original, key=lambda r: (r["p"] + schedule[r["id"]], r["id"])):
        vehicle = ET.SubElement(root, "vehicle", id=record["id"],
            type="bh1-fixed", depart=str(record["p"] + schedule[record["id"]]))
        ET.SubElement(vehicle, "route", edges=" ".join(record["route"]))
    xml_write(outdir / f"bh1_{physical}_{policy}.rou.xml", root)
    ledger = [
        {"id": r["id"], "kind": r["kind"], "preferred": r["p"],
         "requested": r["p"] + schedule[r["id"]],
         "offset": schedule[r["id"]], "route": list(r["route"]),
         "eligible": r["id"] in eligible, "willing": r["id"] in willing}
        for r in original
    ]
    file = outdir / f"bh1_{physical}_{policy}.inputs.json"
    file.write_text(json.dumps({"physical": physical, "policy": policy,
        "status": "INPUTS ONLY: NO PHYSICAL OUTCOMES",
        "roster": ledger}, indent=2) + "\n")
    return file


def make(outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    for physical in ("S", "N"):
        independent, info = qualify_independent(physical)
        if not info["regret_qualifies"]:
            raise AssertionError(f"I not best-response stable in {physical}")
        proposed, v_info = voluntary(independent, physical, 6)
        write_one(outdir, physical, "I", independent)
        write_one(outdir, physical, "V", proposed)

    additional = ET.Element("additional")
    ET.SubElement(additional, "laneAreaDetector", id="pocketE2",
        lane="pocket_0", pos="0", endPos="-0.1", friendlyPos="true",
        period="1", file="pocket-e2.xml", speedThreshold="1.39")
    xml_write(outdir / "bh1-observation.add.xml", additional)
    print("Created four candidate route inputs + E2 observation definition; no traffic execution.")
    check(outdir)


def check(outdir: Path):
    eligible, willing = eligibility()
    records = roster()
    original_ids = {r["id"] for r in records}
    assert len(original_ids) == 96
    compiled_roads = {}
    for physical in ("S", "N"):
        root = ET.parse(outdir / f"bh1_{physical}.net.xml").getroot()
        compiled_roads[physical] = {e.get("id") for e in root.findall("edge")}
    for physical in ("S", "N"):
        baselines = {}
        for policy in ("I", "V"):
            manifest = json.loads((outdir / f"bh1_{physical}_{policy}.inputs.json").read_text())
            rows = manifest["roster"]
            assert len(rows) == 96
            assert {r["id"] for r in rows} == original_ids
            assert len({r["id"] for r in rows}) == 96
            XML = ET.parse(outdir / f"bh1_{physical}_{policy}.rou.xml").getroot()
            xmlvehicles = XML.findall("vehicle")
            assert len(xmlvehicles) == 96
            assert {x.get("id") for x in xmlvehicles} == original_ids
            departures = [int(x.get("depart")) for x in xmlvehicles]
            assert departures == sorted(departures)
            for r in rows:
                assert set(r["route"]).issubset(set(NET_EDGES))
                assert set(r["route"]).issubset(compiled_roads[physical])
                assert r["requested"] == r["preferred"] + r["offset"]
                assert r["offset"] in DELAYS if r["id"] in eligible else r["offset"] == 0
                if policy == "V" and r["id"] not in willing:
                    assert r["offset"] == baselines[r["id"]]["offset"]
            baselines = {r["id"]: r for r in rows}
        print(f"STATIC INPUTS {physical}: 96/96 fixed IDs, sorted route XML, refusal and timing parity")
    add = ET.parse(outdir / "bh1-observation.add.xml").getroot()
    det = add.find("laneAreaDetector")
    assert det is not None and det.get("lane") == "pocket_0"
    print("All four proposed arm inputs validated against compiled networks. NO SUMO TRAFFIC RUN.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=("make", "check"))
    ap.add_argument("--out", type=Path, default=Path("bh1-stage1-static"))
    a = ap.parse_args()
    if a.action == "make":
        make(a.out)
    else:
        check(a.out)


if __name__ == "__main__":
    main()
