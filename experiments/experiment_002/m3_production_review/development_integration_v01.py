"""M3 production-runner integration contract: DEVELOPMENT REHEARSAL ONLY.

This is a pure plan builder, not an evaluation dispatcher. Every plan uses
preinspected seed 2101; future general-seed execution is not implemented.
"""
from dataclasses import dataclass
from pathlib import Path
import hashlib

FROZEN_SHA="be2e8d27c78c8b6de4891115d6d951edc877ac6e"
IMAGE="ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb"
WINDOWS=(200,600,1200)
SEED=2101
REQUIRED=("network.net.xml","trips.xml","original.rou.xml","original-audit.csv",
"chosen-decision-trace.csv","observed-tripinfo.xml","observed-fcd.xml",
"actual-predictor-report.json","scenario.json")

class IntegrationBlocked(RuntimeError):pass

@dataclass(frozen=True)
class DevelopmentScenario:
    seed:int
    window:int
    frozen_sha:str
    sumo_image:str
    archived_run:int
    source_artifact:str

def plan_development(seed=SEED,windows=WINDOWS):
    if type(seed) is not int or seed!=SEED:
        raise IntegrationBlocked("Only already inspected development seed 2101 is permitted")
    if tuple(windows)!=WINDOWS:
        raise IntegrationBlocked("All three prespecified windows must be included exactly once")
    return tuple(DevelopmentScenario(seed,w,FROZEN_SHA,IMAGE,40446073958,
        f"exp002-occupancy-M2-window-{w}-seed2101") for w in windows)

def check_archive(root,scenario):
    if scenario not in plan_development():
        raise IntegrationBlocked("Unapproved scenario")
    root=Path(root)
    missing=[x for x in REQUIRED if not (root/x).is_file()]
    if missing:raise IntegrationBlocked("Incomplete archived source: "+", ".join(missing))
    hashes={}
    for name in REQUIRED:
        hashes[name]=hashlib.sha256((root/name).read_bytes()).hexdigest()
    return {"status":"DEVELOPMENT_ARCHIVE_COMPLETE",
        "seed":scenario.seed,"window":scenario.window,
        "scientific_commit":FROZEN_SHA,"sumo_image":IMAGE,
        "source_sha256":hashes,"heldout_authorized":False}

def execution_authorization(*args,**kwargs):
    raise IntegrationBlocked("No held-out execution path exists in this integration module")
