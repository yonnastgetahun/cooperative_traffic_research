#!/usr/bin/env python3
"""Build immutable per-scenario scientific artifact manifest, never replace failed runs."""
import argparse,hashlib,json,xml.etree.ElementTree as ET
from pathlib import Path
from adapters_v01 import FROZEN_SHA,SUMO_IMAGE,od_pair_fingerprint

REQUIRED=("network.net.xml","trips.xml","original.rou.xml","original-audit.csv",
 "tripinfo.xml","statistics.xml","observed-fcd.xml","native-external.xml",
 "native-vehroute.xml","chosen-decision-trace.csv","native-events.csv",
 "paired-road-entry.csv","paired-reference-report.json","r3-exception-audit.json",
 "seed-level-metrics.json")
def make(root,seed,window):
    root=Path(root)
    attempt=json.loads((root/"attempt.json").read_text())
    if attempt.get("status")!="COMPLETE" or attempt.get("seed")!=seed or attempt.get("window_seconds")!=window:
        raise RuntimeError("Incomplete or mismatched attempt; cannot produce eligible manifest")
    for name in REQUIRED:
        if not (root/name).is_file():raise RuntimeError("Missing required scientific artifact: "+name)
    if not (root/"control.rou.xml").is_file() or not (root/"control-audit.csv").is_file():
        raise RuntimeError("Independent route-equivalence artifacts missing")
    if (root/"control.rou.xml").read_bytes() != (root/"original.rou.xml").read_bytes():
        raise RuntimeError("Frozen routes not byte-identical")
    if (root/"control-audit.csv").read_bytes() != (root/"original-audit.csv").read_bytes():
        raise RuntimeError("Frozen audit not byte-identical")
    triproot=ET.parse(root/"trips.xml").getroot()
    trips=[]
    for t in triproot:
        if t.tag in ("trip","vehicle"):
            trips.append((t.get("id"),t.get("from"),t.get("to")))
    od=od_pair_fingerprint(trips)
    files={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in REQUIRED+("control.rou.xml","control-audit.csv")}
    manifest=dict(seed=seed,window_seconds=window,scientific_commit=FROZEN_SHA,
       sumo_image=SUMO_IMAGE,od_pair_sha256=od,route_audit_byte_identical=True,
       files=files,attempt_status="COMPLETE")
    (root/"scenario-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    return manifest
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True)
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--window",type=int,required=True)
    a=p.parse_args()
    print(json.dumps(make(a.root,a.seed,a.window)))
