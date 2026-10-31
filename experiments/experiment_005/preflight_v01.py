#!/usr/bin/env python3
"""Development-only preflight: exact D-route parity and E bin replay fixtures."""
import argparse
import collections
import tempfile
from pathlib import Path
import sys

from clock_alignment_routes_v01 import generate, aligned_bins, legacy_bins
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiment_004"))
from four_arm_routes_v01 import generate as legacy_generator
from run_pair_v01 import build_demand


class Edge:
    def __init__(self, ff=10.0):
        self.ff = ff
    def getLength(self):
        return 100.0
    def getLaneNumber(self):
        return 1
    def getSpeed(self):
        return 100 / self.ff


def fixtures():
    # Offsets and ordinal increments force different successor lookup bins.
    edges = {"a": Edge(), "b": Edge(), "c": Edge()}
    adj = {"a": ["b", "c"], "b": ["c"], "c": []}
    occupancy = collections.Counter({("b", 1): 30})
    bins = aligned_bins(["a", "b", "c"], 0.0, edges, adj, occupancy, 4.0, 12.0)
    # a bin0; b entry=0+10+4+12=26 bin0; c entry=10+10+1+4+24=49 bin1
    assert bins == [0, 0, 1], bins
    assert occupancy == collections.Counter({("b", 1): 30}), "Replay mutated occupancy"
    assert legacy_bins(["a", "b", "c"], 0.0, edges) == [0, 0, 0]


def preflight(window, frozen):
    fixtures()
    frozen = Path(frozen).resolve()
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        net, trips = build_demand(2101, window, root, frozen)
        legacy_generator(net, trips, "D", window, root / "original_D")
        generate(net, trips, window, "D", root / "new_D")
        generate(net, trips, window, "E", root / "new_E")
        for filename in ("routes.rou.xml", "audit.csv"):
            old = (root / "original_D" / filename).read_bytes()
            new = (root / "new_D" / filename).read_bytes()
            assert old == new, f"D-replication does not match original Exp004 D: {filename}"
        assert (root / "new_E" / "routes.rou.xml").is_file()
    print(f"PASS: dev seed 2101, window {window}: exact legacy D route+audit parity")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--window", type=int, choices=(200, 600, 1200), required=True)
    p.add_argument("--frozen", required=True)
    args = p.parse_args()
    preflight(args.window, args.frozen)
