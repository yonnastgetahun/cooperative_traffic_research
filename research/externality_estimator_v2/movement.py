"""Prospective, static SUMO 1.28.0 priority-movement contract. No SUMO simulation.

Movement mapping was independently checked against tagged SUMO v1_28_0 sumolib
in the archived J0-J4 study. Runtime predictions never read FCD/tripinfo.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import hashlib
import re
import xml.etree.ElementTree as ET

SUMO_SOURCE_COMMIT = "daf91b5578901d599ac9af53f49d26eeb9aefc3b"
KNOWN_CANONICAL_GRID_SHA = "69c5c32e13987646944cbc7b072d586732402c5b8f3651c379c06fecee65ee14"


class InvalidMovementMap(ValueError):
    pass


class PriorityAmbiguity(RuntimeError):
    pass


def bits(raw: str) -> frozenset[int]:
    if not raw or set(raw) - {"0", "1"}:
        raise InvalidMovementMap("Missing/nonbinary request bits")
    return frozenset(i for i, char in enumerate(reversed(raw)) if char == "1")


@dataclass(frozen=True)
class Movement:
    junction: str
    index: int
    src: str
    dst: str
    via: str
    foes: frozenset[int]
    yields_to: frozenset[int]
    cont: bool = False
    source_lane: str = ""
    destination_lane: str = ""

    def __post_init__(self):
        if not self.junction or not self.src or not self.dst or self.index < 0:
            raise InvalidMovementMap("Incomplete priority movement")
        if not self.via:
            raise InvalidMovementMap("Missing via lane")
        if not self.yields_to.issubset(self.foes):
            raise InvalidMovementMap("Response outside foes bitset")
        if self.index in self.foes or self.index in self.yields_to:
            raise InvalidMovementMap("Self-foe/response not supported")
        if not self.source_lane:
            object.__setattr__(self, "source_lane", self.src + "_0")
        if not self.destination_lane:
            object.__setattr__(self, "destination_lane", self.dst + "_0")


@dataclass(frozen=True)
class MovementMap:
    records: tuple[Movement, ...]
    canonical_sha: str = "TOY_FIXTURE"
    source_commit: str = SUMO_SOURCE_COMMIT

    def __post_init__(self):
        if self.source_commit != SUMO_SOURCE_COMMIT:
            raise InvalidMovementMap("Unpinned SUMO source")
        keys = [(m.src, m.dst) for m in self.records]
        if len(set(keys)) != len(keys):
            raise InvalidMovementMap("One-lane turn map has duplicated external edge transitions")
        indices = [(m.junction, m.index) for m in self.records]
        if len(set(indices)) != len(indices):
            raise InvalidMovementMap("Duplicate junction request indices")
        by_j = {}
        for m in self.records:
            by_j.setdefault(m.junction, []).append(m)
        for jid, members in by_j.items():
            if sorted(m.index for m in members) != list(range(len(members))):
                raise InvalidMovementMap("Missing junction request index " + jid)
            n = len(members)
            if any(max(m.foes | m.yields_to, default=-1) >= n for m in members):
                raise InvalidMovementMap("Bitset exceeds request count")
            for a in members:
                for b in members:
                    if a.index == b.index:
                        continue
                    if (b.index in a.foes) != (a.index in b.foes):
                        raise InvalidMovementMap("Asymmetric foe relation")

    def by_edge_pair(self) -> dict[tuple[str, str], Movement]:
        return {(m.src, m.dst): m for m in self.records}


def compile_frozen_grid_network(path: str | Path) -> MovementMap:
    """Compile *only* audited one-lane topology; fail closed for other networks."""
    try:
        from lxml import etree as LXML
    except ImportError as error:
        raise InvalidMovementMap("lxml required for exact pinned canonical contract") from error
    xml = LXML.parse(str(path)).getroot()
    core = b"".join(LXML.tostring(e, method="c14n", with_comments=False)
                    for e in xml if e.tag in ("edge", "junction", "connection"))
    sha = hashlib.sha256(core).hexdigest()
    if sha != KNOWN_CANONICAL_GRID_SHA:
        raise InvalidMovementMap("Unknown network topology or request rules: " + sha)
    root = ET.parse(str(path)).getroot()
    links = {edge.get("id"): edge for edge in root.findall("edge")
             if edge.get("function") != "internal" and not edge.get("id", "").startswith(":")}
    if len(links) != 360 or any(len(e.findall("lane")) != 1 for e in links.values()):
        raise InvalidMovementMap("Only audited 360-edge one-lane grid supported")
    by_src_lane = {}
    for c in root.findall("connection"):
        a,b = c.get("from"),c.get("to")
        if a in links and b in links:
            key = a + "_" + c.get("fromLane", "")
            by_src_lane.setdefault(key, []).append(c)
    result = []
    count = 0
    for node in root.findall("junction"):
        if node.get("type") != "priority":
            continue
        jid = node.get("id")
        requests = {int(r.get("index")):r for r in node.findall("request")}
        connections = [c for lane in node.get("incLanes", "").split()
                       for c in by_src_lane.get(lane, ())]
        if len(connections) != len(requests) or set(requests) != set(range(len(requests))):
            raise InvalidMovementMap("Incomplete incoming-lane ordering " + jid)
        for index,c in enumerate(connections):
            match = re.fullmatch(r":(.+)_(\d+)_(\d+)", c.get("via", ""))
            if not match or match.group(1) != jid or int(match.group(2)) != index:
                raise InvalidMovementMap("Via/request-index disagreement: " + jid)
            req = requests[index]
            foe = req.get("foes",""); response = req.get("response","")
            if len(foe) != len(requests) or len(response) != len(requests):
                raise InvalidMovementMap("Inconsistent request bit-width")
            result.append(Movement(
                junction=jid,index=index,src=c.get("from"),dst=c.get("to"),
                via=c.get("via"),foes=bits(foe),yields_to=bits(response),
                cont=req.get("cont", "0") == "1",
                source_lane=c.get("from") + "_" + c.get("fromLane"),
                destination_lane=c.get("to") + "_" + c.get("toLane")))
            count += 1
    if count != 1320:
        raise InvalidMovementMap("Unexpected number of mapped priority movements")
    return MovementMap(tuple(result),canonical_sha=sha)
