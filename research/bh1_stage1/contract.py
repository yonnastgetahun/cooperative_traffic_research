#!/usr/bin/env python3
"""B-H1 Stage-1 contract checks only. No physical traffic simulation is launched.

Creates proposed *plain* SUMO input XML, independent/voluntary paper schedule
decisions, and checks their inputs; optional 'check-networks' checks netconvert
compiled topology. Neither the analytical forecast nor compilation is an
observed real-traffic or SUMO simulation result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).parent
SPEED = 13.9
EPSILON = 1e-9
DELAYS = (0, 5, 10)
N_MAIN = N_CROSS = 48
NET_EDGES = ("m_in", "pocket", "m_out", "x_in", "x_out")
ROUTES = {
    "main": ("m_in", "pocket", "m_out"),
    "cross": ("x_in", "x_out"),
}
NODES = {
    "S": (0, -250), "J": (0, 0), "K": (0, 40),
    "T": (0, 250), "W": (-250, 0), "E": (250, 0),
}
EDGES = (
    ("m_in", "S", "J", 250),
    ("pocket", "J", "K", 40),
    ("m_out", "K", "T", 210),
    ("x_in", "W", "J", 250),
    ("x_out", "J", "E", 250),
)


def rank(label: str, ids: list[str]) -> list[str]:
    return sorted(ids, key=lambda vid: (hashlib.sha256(
        f"bh1-v01:{label}:{vid}".encode()).hexdigest(), vid))


def roster() -> list[dict]:
    main = [
        {"id": f"m{i:03d}", "p": 5 * i, "kind": "main", "route": ROUTES["main"]}
        for i in range(N_MAIN)
    ]
    cross = [
        {"id": f"x{i:03d}", "p": 5 * i + 2, "kind": "cross", "route": ROUTES["cross"]}
        for i in range(N_CROSS)
    ]
    result = sorted(main + cross, key=lambda r: (r["p"], r["id"]))
    assert len(result) == 96 and len({r["id"] for r in result}) == 96
    return result


def eligibility() -> tuple[set[str], set[str]]:
    ids = [f"m{i:03d}" for i in range(N_MAIN)]
    eligible = set(rank("eligible", ids)[:12])
    willing = set(rank("accept", sorted(eligible))[:6])
    assert len(eligible) == 12 and len(willing) == 6
    return eligible, willing


def green_slot(t: float) -> float:
    """First time >= t in K's proposed 30s-red / 30s-green, 3s slot grid."""
    t = max(t, 30.0)
    cycle = math.floor(t / 60)
    phase = t - 60 * cycle
    if phase < 30 - EPSILON:
        return 60 * cycle + 30
    slot = math.ceil((phase - 30 - EPSILON) / 3)
    if slot >= 10:
        return 60 * (cycle + 1) + 30
    return 60 * cycle + 30 + 3 * slot


def predict(schedule: dict[str, int], physical: str = "S") -> dict[str, float]:
    """Shared nonclairvoyant forecast. Does NOT use actual SUMO observations."""
    if physical not in ("S", "N"):
        raise ValueError(physical)
    rr = roster()
    if set(schedule) != {r["id"] for r in rr}:
        raise ValueError("Schedule not a permutation of the immutable 96 IDs")
    eligible, _ = eligibility()
    for rec in rr:
        delay = schedule[rec["id"]]
        if delay not in DELAYS if rec["id"] in eligible else delay != 0:
            raise ValueError("Invalid eligible/decliner timing")
    main = sorted(
        ((schedule[r["id"]] + r["p"] + 290 / SPEED, r["id"]) for r in rr
         if r["kind"] == "main"),
        key=lambda row: (row[0], row[1]),
    )
    service = {}
    next_slot = 30.0
    events = []
    for arrival, vid in main:
        slot = green_slot(max(arrival, next_slot))
        service[vid] = slot
        next_slot = slot + 3
        events.append((arrival, +1))
        events.append((slot, -1))
    # An event-order approximation: K service preceding same-time arrival.
    events.sort(key=lambda e: (e[0], e[1]))
    out = {}
    for r in rr:
        vid = r["id"]
        if r["kind"] == "main":
            out[vid] = service[vid] + 210 / SPEED
            continue
        t_j = r["p"] + 250 / SPEED
        if physical == "N":
            out[vid] = t_j + 250 / SPEED
            continue
        queue = 0
        unblock = t_j
        found = False
        for t, delta in events:
            if t <= t_j + EPSILON:
                queue += delta
                if queue < 0:
                    raise AssertionError("Impossible negative queue")
                continue
            if queue < 5:
                found = True
                break
            queue += delta
            if queue < 5:
                unblock = t
                found = True
                break
        if not found and queue >= 5:
            raise AssertionError("Predicted queue never clears")
        out[vid] = max(t_j, unblock) + 250 / SPEED
    if set(out) != set(schedule):
        raise AssertionError("A predicted driver was lost")
    if any(out[r["id"]] < r["p"] + schedule[r["id"]] - EPSILON for r in rr):
        raise AssertionError("Arrival earlier than a requested departure")
    return out


def cost(schedule: dict[str, int], physical: str = "S") -> float:
    aa = predict(schedule, physical)
    return sum(aa[r["id"]] - r["p"] for r in roster())


def personal(schedule: dict[str, int], vid: str, physical: str = "S") -> float:
    rec = next(r for r in roster() if r["id"] == vid)
    return predict(schedule, physical)[vid] - rec["p"]


def base_schedule() -> dict[str, int]:
    return {r["id"]: 0 for r in roster()}


def qualify_independent(physical: str) -> tuple[dict[str, int], dict]:
    eligible, _ = eligibility()
    schedule = base_schedule()
    order = rank("eligible", sorted(eligible))
    sweeps = 0
    for sweeps in range(1, 21):
        changes = 0
        for vid in order:
            old = schedule[vid]
            old_cost = personal(schedule, vid, physical)
            scored = []
            for delay in DELAYS:
                trial = dict(schedule)
                trial[vid] = delay
                scored.append((personal(trial, vid, physical), delay != old, delay))
            best = min(scored)
            if best[0] < old_cost - 0.1 - EPSILON:
                schedule[vid] = best[2]
                changes += 1
        if changes == 0:
            break
    max_gain = 0.0
    for vid in order:
        curr = personal(schedule, vid, physical)
        for delay in DELAYS:
            trial = dict(schedule)
            trial[vid] = delay
            max_gain = max(max_gain, curr - personal(trial, vid, physical))
    info = {"physical": physical, "sweeps": sweeps,
            "max_unilateral_gain_s": round(max_gain, 9),
            "regret_qualifies": max_gain <= 0.1 + EPSILON,
            "total_predicted_s": round(cost(schedule, physical), 6)}
    return schedule, info


def voluntary(independent: dict[str, int], physical: str = "S",
              count: int = 6) -> tuple[dict[str, int], dict]:
    eligible, willing = eligibility()
    willing = set(rank("accept", sorted(eligible))[:count])
    schedule = dict(independent)
    done = set()
    offers = []
    for _ in range(len(willing)):
        prior_cost = cost(schedule, physical)
        proposals = []
        for vid in sorted(willing - done):
            current = schedule[vid]
            current_own = personal(schedule, vid, physical)
            for shift in DELAYS:
                if shift == current:
                    continue
                trial = dict(schedule)
                trial[vid] = shift
                own_change = personal(trial, vid, physical) - current_own
                if own_change > 5 + EPSILON:
                    continue
                gain = prior_cost - cost(trial, physical)
                if gain > 0.1 + EPSILON:
                    proposals.append((-gain, own_change, vid, shift))
        if not proposals:
            break
        _, own_change, vid, shift = min(proposals)
        schedule[vid] = shift
        done.add(vid)
        offers.append({"id": vid, "accepted": True, "requested_shift": shift,
                       "predicted_own_change": round(own_change, 6)})
    not_willing = sorted(eligible - willing)
    if any(schedule[x] != independent[x] for x in not_willing):
        raise AssertionError("Decliner was forced to change")
    if any(schedule[x] != independent[x] for x in set(schedule) - eligible):
        raise AssertionError("Ineligible driver shifted")
    return schedule, {"willing": sorted(willing), "decliners": not_willing,
                       "offers": offers, "accepted": len(offers),
                       "total_predicted_s": round(cost(schedule, physical), 6)}


def xml_write(path: Path, root: ET.Element):
    ET.indent(root)
    path.write_bytes(ET.tostring(root, encoding="utf-8", xml_declaration=True))


def generate(outdir: Path):
    """Proposed plain-network fixtures only: NO netconvert or sumo invocation."""
    outdir.mkdir(parents=True, exist_ok=True)
    nodes = ET.Element("nodes")
    for id_, (x, y) in NODES.items():
        ET.SubElement(nodes, "node", id=id_, x=str(x), y=str(y),
                      type=("traffic_light" if id_ == "K" else "priority"))
    xml_write(outdir / "bh1.nod.xml", nodes)
    edges = ET.Element("edges")
    for id_, src, dst, length in EDGES:
        ET.SubElement(edges, "edge", id=id_, **{"from": src, "to": dst},
                      numLanes="1", speed=str(SPEED), length=str(length),
                      priority="2" if id_ in ("m_in", "pocket", "m_out") else "1")
    xml_write(outdir / "bh1.edg.xml", edges)
    for physical, clear in (("S", "false"), ("N", "true")):
        con = ET.Element("connections")
        ET.SubElement(con, "connection", **{"from": "m_in", "to": "pocket",
                                          "fromLane": "0", "toLane": "0",
                                          "keepClear": clear})
        ET.SubElement(con, "connection", **{"from": "pocket", "to": "m_out",
                                          "fromLane": "0", "toLane": "0"})
        ET.SubElement(con, "connection", **{"from": "x_in", "to": "x_out",
                                          "fromLane": "0", "toLane": "0"})
        xml_write(outdir / f"bh1_{physical}.con.xml", con)
    tls = ET.Element("tlLogics")
    log = ET.SubElement(tls, "tlLogic", id="K", type="static", programID="bh1",
                        offset="0")
    ET.SubElement(log, "phase", duration="30", state="r")
    ET.SubElement(log, "phase", duration="30", state="G")
    xml_write(outdir / "bh1.tll.xml", tls)

    eligible, willing = eligibility()
    original = {
        "roster": roster(), "eligible": sorted(eligible), "willing": sorted(willing),
        "options": list(DELAYS), "engine": "SUMO v1_28_0",
        "purpose": "source/static Stage-1 only; NOT simulated physical output",
    }
    (outdir / "bh1-input-contract.json").write_text(json.dumps(original, indent=2) + "\n")

    for physical in ("S", "N"):
        for p in (outdir / f"bh1_{physical}.con.xml",):
            assert p.exists()
    print("Generated candidate plain-network and 96-ID static input contract; no traffic runs.")


def check_net(outdir: Path):
    """Inspect *compiled* XML generated by netconvert, without running traffic."""
    normalized = {}
    for physical in ("S", "N"):
        path = outdir / f"bh1_{physical}.net.xml"
        root = ET.parse(path).getroot()
        ids = {e.attrib["id"] for e in root.findall("edge")}
        if not set(NET_EDGES).issubset(ids):
            raise AssertionError(f"Lost required external edges in {physical}: {ids}")
        internal = [e for e in root.findall("edge")
                    if e.attrib.get("function") == "internal"]
        if not internal:
            raise AssertionError("Compiled physical network lacks internal links")
        con = [c for c in root.findall("connection")
               if c.attrib.get("from") == "m_in" and c.attrib.get("to") == "pocket"]
        if len(con) != 1:
            raise AssertionError("Missing main crossing movement")
        cc = con[0].attrib.get("keepClear", "true").lower()
        expected = {"false", "0"} if physical == "S" else {"true", "1"}
        if cc not in expected:
            raise AssertionError(f"J keep-clear mismatch {physical}: {cc}")
        traffic = [t for t in root.findall("tlLogic") if t.attrib.get("id") == "K"]
        if len(traffic) != 1 or {p.attrib.get("state") for p in traffic[0].findall("phase")} != {"r", "G"}:
            raise AssertionError("K did not retain a single-movement red/green cycle")
        j = [n for n in root.findall("junction") if n.attrib.get("id") == "J"]
        if len(j) != 1 or len(j[0].attrib.get("incLanes", "").split()) < 2:
            raise AssertionError("Cross-traffic junction not compiled as a crossing")
        conflicts = [q.attrib.get("foes", "") for q in j[0].findall("request")]
        if len(conflicts) < 2 or not any("1" in foes for foes in conflicts):
            raise AssertionError("Compiled J has no explicit competing crossing movements")
        for edge in root.iter("connection"):
            edge.attrib.pop("keepClear", None)
        normalized[physical] = ET.tostring(root)
        print(f"NETCONVERT STATIC {physical}: required roads, internal lanes, J, K and keep-clear checked.")
    if normalized["S"] != normalized["N"]:
        raise AssertionError("S/N compiled networks differ beyond intended keep-clear setting")
    print("Compiled S/N topology/priority/signal parity PASS after keep-clear normalization.")
    print("Network XML structurally qualified only; physical blocking still UNVERIFIED.")


def check_policy(outdir: Path):
    """Analytical/decision-contract checks, not a SUMO/physical traffic simulation."""
    rr = roster()
    eligible, willing = eligibility()
    assert len(rr) == 96 and len(eligible) == 12 and len(willing) == 6
    assert len({r["p"] for r in rr}) > 20
    rr_ids = {r["id"] for r in rr}
    result = {"status": "STAGE1_DECISION_CONTRACT_ONLY",
              "not_a_physical_traffic_experiment": True,
              "N": 96, "eligible_n": len(eligible), "willing_n": len(willing)}
    independent = {}
    for physical in ("S", "N"):
        independent[physical], info = qualify_independent(physical)
        result[f"I_{physical}"] = info
        zero, zz = voluntary(independent[physical], physical, 0)
        assert zero == independent[physical] and zz["accepted"] == 0
        coord, vv = voluntary(independent[physical], physical, 6)
        assert set(coord) == rr_ids
        assert all(coord[x] == independent[physical][x] for x in rr_ids - willing)
        assert len(vv["offers"]) <= 6
        for offer in vv["offers"]:
            assert offer["predicted_own_change"] <= 5 + 1e-6
        result[f"V_{physical}"] = vv
        result[f"schedule_{physical}_ID_digest"] = hashlib.sha256(
            json.dumps(coord, sort_keys=True).encode()).hexdigest()
    # A nonconverged independent baseline makes *the scientific gate fail*
    # even if a coordinated schedule happens to show a lower model cost.
    result["G2_baseline_qualified_offline"] = all(
        result[f"I_{m}"]["regret_qualifies"] for m in ("S", "N"))
    (outdir / "static-policy-gates.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items()
                      if k.startswith("I_") or k.startswith("G2_")}, indent=2))
    if not result["G2_baseline_qualified_offline"]:
        raise AssertionError("G2: independent best response did not converge; STOP before traffic")
    print("Static policy integrity checks complete; no physical efficacy claim.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=("generate", "check-networks", "check-policy"))
    ap.add_argument("--out", type=Path, default=Path("bh1-stage1-candidate"))
    args = ap.parse_args()
    if args.action == "generate":
        generate(args.out)
    elif args.action == "check-networks":
        check_net(args.out)
    else:
        check_policy(args.out)


if __name__ == "__main__":
    main()
