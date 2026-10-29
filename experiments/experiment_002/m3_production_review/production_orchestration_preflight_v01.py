#!/usr/bin/env python3
"""Non-dispatching production execution plan and immutable preflight.

Builds a complete planned case registry, never generates demand or runs SUMO.
The production execution path remains intentionally unavailable pending review.
"""
import hashlib
import json
from pathlib import Path
from adapters_v01 import FROZEN_SHA, SUMO_IMAGE, REGIMES
from release_record_v01 import SEEDS, ReleaseBlocked

class PreflightBlocked(RuntimeError):
    pass

def frozen_preflight(frozen_root, scientific_sha, image):
    root = Path(frozen_root)
    if scientific_sha != FROZEN_SHA or image != SUMO_IMAGE:
        raise PreflightBlocked("Scientific SHA or pinned simulator image differs")
    manifest = root / "docs/EXPERIMENT_002_M3_PROTOCOL_FREEZE_MANIFEST_V1.json"
    if not manifest.is_file():
        raise PreflightBlocked("Immutable scientific manifest missing")
    if not (root / "experiments/experiment_002/time_aware.py").is_file():
        raise PreflightBlocked("Frozen predictor missing")
    return {"scientific_commit": FROZEN_SHA, "sumo_image": SUMO_IMAGE,
            "freeze_manifest_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest()}

def planned_registry():
    """Identifiers only; does not construct, inspect or simulate reserved inputs."""
    return tuple({"seed": seed, "window_seconds": window,
                  "state": "NOT_EXECUTED", "evaluation_authorized": False}
                 for seed in SEEDS for window in REGIMES)

def require_execution_authorization(*_args, **_kwargs):
    raise ReleaseBlocked("Production dispatch disabled; separately reviewed activation required")

def inspect_plan(plan):
    expected = {(s, w) for s in SEEDS for w in REGIMES}
    if len(plan) != 30:
        raise PreflightBlocked("Exactly 30 scenarios required")
    keys = [(p.get("seed"), p.get("window_seconds")) for p in plan]
    if set(keys) != expected or len(set(keys)) != 30:
        raise PreflightBlocked("Duplicate, substituted or missing scenario")
    if any(p.get("state") != "NOT_EXECUTED" or p.get("evaluation_authorized") is not False for p in plan):
        raise PreflightBlocked("Unexpected execution/authorization state")
    return {"status": "PLANNED_ONLY_NOT_EXECUTABLE", "scenarios": 30,
            "heldout_execution_authorized": False}

if __name__ == "__main__":
    raise SystemExit("Non-executable production planning module; no evaluation dispatch")
