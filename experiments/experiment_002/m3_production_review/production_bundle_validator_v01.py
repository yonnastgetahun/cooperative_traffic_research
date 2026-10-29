#!/usr/bin/env python3
"""M3 production artifact integrity preflight; no SUMO, seed generation, or dispatch.

Input is a set of independently produced scenario bundles. This adapter is
pure verification and does not grant permission to generate those bundles.
"""
import argparse,csv,hashlib,json,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from adapters_v01 import (FROZEN_SHA,SUMO_IMAGE,REGIMES,N_VEHICLES,
                           Ineligible,seed_record,summarize_seed_level)
from release_record_v01 import SEEDS,review_release_record
from activation_gate_v01 import require_heldout_execution_authorization

def digest(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""):h.update(b)
    return h.hexdigest()

def validate_bundle(root,seed,window):
    """Validate a hypothetical scenario, no file creation or execution."""
    root=Path(root)
    manifest=json.loads((root/"scenario-manifest.json").read_text())
    if manifest.get("seed")!=seed or manifest.get("window_seconds")!=window:
        raise Ineligible("Scenario identity mismatch")
    if manifest.get("scientific_commit")!=FROZEN_SHA or manifest.get("sumo_image")!=SUMO_IMAGE:
        raise Ineligible("Frozen source or simulator mismatch")
    files=manifest.get("files")
    if not isinstance(files,dict) or not files:raise Ineligible("Missing artifact manifest")
    for name in ("seed-level-metrics.json","r3-exception-audit.json","paired-reference-report.json",
                 "network.net.xml","trips.xml","original.rou.xml"):
        if name not in files:raise Ineligible("Missing required artifact: "+name)
    for name,expected in files.items():
        if Path(name).name!=name or name in (".",".."):
            raise Ineligible("Unsafe artifact path")
        if not isinstance(expected,str) or len(expected)!=64 or any(c not in "0123456789abcdef" for c in expected):
            raise Ineligible("Malformed SHA256")
        if digest(root/name)!=expected:raise Ineligible("Artifact hash mismatch: "+name)
    read=lambda name:json.loads((root/name).read_text())
    source=dict(scientific_commit=FROZEN_SHA,sumo_image=SUMO_IMAGE,
       network_sha256=files["network.net.xml"],trips_sha256=files["trips.xml"],
       routes_sha256=files["original.rou.xml"],
       od_pair_sha256=manifest.get("od_pair_sha256"),
       route_audit_byte_identical=manifest.get("route_audit_byte_identical") is True)
    return seed_record(seed,window,read("seed-level-metrics.json"),
       read("r3-exception-audit.json"),read("paired-reference-report.json"),source)

def validate_registry(root,expected_seeds,ci_function):
    """No silent seed replacement; all 30 records must be valid."""
    if tuple(expected_seeds)!=SEEDS:raise Ineligible("Frozen seed registry mismatch")
    records=[]
    for seed in expected_seeds:
        for window in REGIMES:
            folder=Path(root)/f"seed-{seed}-window-{window}"
            if not folder.is_dir():raise Ineligible("Missing prespecified scenario")
            records.append(validate_bundle(folder,seed,window))
    return summarize_seed_level(records,expected_seeds,ci_function)

def main():
    p=argparse.ArgumentParser(description="Review-only; never dispatches evaluation")
    p.add_argument("--synthetic-fixtures",required=True)
    p.add_argument("--frozen-root",required=True)
    a=p.parse_args()
    if not (Path(a.frozen_root)/"docs/EXPERIMENT_002_M3_PROTOCOL_FREEZE_MANIFEST_V1.json").is_file():
        raise Ineligible("Frozen manifest missing")
    sys.path.insert(0,str(Path(a.frozen_root)/"experiments/experiment_002"))
    from g3_r4_seed_analysis_v01 import mean_ci_if_ten
    # Explicitly not called on reserved data in this review-only entry point.
    raise SystemExit("Production bundle validator prepared; no held-out execution or input inspection authorized")

if __name__=="__main__":main()
