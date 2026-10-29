"""M3 observation integration contract, review-only and fail-closed.

The frozen scientific R3 audit and timing score are reused by reference.
No simulation, demand generation, or evaluation-seed access.
"""
from pathlib import Path
import json,hashlib

FROZEN_SHA="be2e8d27c78c8b6de4891115d6d951edc877ac6e"
ALLOWED_SEED=2101
WINDOWS=(200,600,1200)
REQUIRED_OBSERVATIONS=("original.rou.xml","tripinfo.xml","native-vehroute.xml",
    "observed-fcd.xml","statistics.xml","native-external.xml",
    "chosen-decision-trace.csv","native-events.csv","paired-road-entry.csv",
    "paired-reference-report.json","r3-exception-audit.json","seed-level-metrics.json")
class ObservationBlocked(RuntimeError):pass

def validate_identity(seed,window):
    if type(seed) is not int or seed!=ALLOWED_SEED or type(window) is not int or window not in WINDOWS:
        raise ObservationBlocked("Only inspected development seed 2101 and frozen regimes permitted")
    return True

def validate_observations(folder,seed,window):
    validate_identity(seed,window)
    folder=Path(folder)
    missing=[name for name in REQUIRED_OBSERVATIONS if not (folder/name).is_file()]
    if missing:raise ObservationBlocked("Missing native observation: "+", ".join(missing))
    read=lambda n:json.loads((folder/n).read_text())
    bridge=read("paired-reference-report.json")
    r3=read("r3-exception-audit.json")
    score=read("seed-level-metrics.json")
    if bridge.get("planned_edges")!=bridge.get("matched") or not bridge.get("matched"):
        raise ObservationBlocked("Native/FCD ordered road entry join incomplete")
    if r3.get("seed")!=seed or r3.get("window_seconds")!=window or r3.get("exception_gate")!="PASS_FOR_THIS_REPLAY":
        raise ObservationBlocked("Frozen R3 exception status not eligible")
    tp=r3.get("reported_teleports") or {}
    if tp.get("teleport_state")!="ZERO_CONFIRMED" or tp.get("teleports_total")!=0:
        raise ObservationBlocked("Native teleport state not explicitly zero")
    if score.get("vehicles")!=1000 or score.get("edge_traversals")!=bridge["matched"]:
        raise ObservationBlocked("Seed-level timing denominator mismatch")
    if score.get("frozen_scientific_commit")!=FROZEN_SHA:
        raise ObservationBlocked("Unfrozen scientific source")
    hashes={n:hashlib.sha256((folder/n).read_bytes()).hexdigest() for n in REQUIRED_OBSERVATIONS}
    return dict(status="INSPECTED_DEVELOPMENT_OBSERVATIONS_INTEGRITY_PASS",
        seed=seed,window_seconds=window,matched_edges=bridge["matched"],
        frozen_scientific_commit=FROZEN_SHA,source_sha256=hashes,
        heldout_authorized=False)

def authorize(*args,**kwargs):
    raise ObservationBlocked("Observation integration cannot authorize reserved seed execution")
