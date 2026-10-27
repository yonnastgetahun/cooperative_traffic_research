#!/usr/bin/env python3
"""Offline replay of frozen R3 audit and R4 seed mapping on past development data.

No SUMO execution, no OD generation, no direct or indirect access to any
reserved evaluation seed. Prints scientific adapter equivalence only.
"""
import argparse,csv,hashlib,json,sys
from pathlib import Path
import xml.etree.ElementTree as ET
from types import SimpleNamespace

from adapters_v01 import (
    FROZEN_SHA,SUMO_IMAGE,od_pair_fingerprint,seed_record,require)
from activation_gate_v01 import inspect_active_workflow_inventory,inspect_inactive_template

def read_json(p):
    return json.loads(Path(p).read_text())

def sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
    return h.hexdigest()

def archived_sha(file):
    data={}
    for line in Path(file).read_text().splitlines():
        pieces=line.split()
        if len(pieces)!=2:raise RuntimeError("Malformed original archived sha256 manifest")
        digest,path=pieces
        if len(digest)!=64:raise RuntimeError("Invalid SHA in archived M2 manifest")
        data[path]=digest
    for name in ("source/network.net.xml","source/trips.xml","source/original.rou.xml"):
        if name not in data:raise RuntimeError("Missing original M2 SHA for "+name)
    return data

def od_from_generated_trips(path):
    root=ET.parse(path).getroot()
    return od_pair_fingerprint((x.get("id"),x.get("from"),x.get("to"))
        for x in root.findall("trip"))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-root",required=True)
    p.add_argument("--frozen-root",required=True)
    p.add_argument("--repo-root",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    source_root=Path(a.source_root);frozen=Path(a.frozen_root)
    repo=Path(a.repo_root);out=Path(a.out)
    out.mkdir(parents=True,exist_ok=True)
    sys.path.insert(0,str(frozen/"experiments/experiment_002"))
    import g3_r3_exception_audit_v01 as frozen_r3
    sys.path.insert(0,str(repo/"experiments/experiment_002/m3_qualification"))
    import guard_v01 as frozen_guard
    guard=frozen_guard.inspect_frozen(frozen)
    if guard["frozen_sha"]!=FROZEN_SHA:
        raise RuntimeError("Frozen code not the approved scientific SHA")
    template=inspect_inactive_template(repo)
    inventory=inspect_active_workflow_inventory(repo)
    if template["heldout_execution_enabled"] or inventory["active_heldout_evaluation_workflow_found"]:
        raise RuntimeError("Held-out workflow unexpectedly active")
    rows=[];total=0;od_hashes={}
    for window in (200,600,1200):
        source=source_root/f"exp002-M3-QUALIFY-window-{window}-seed2101"
        if not source.is_dir():raise RuntimeError("Missing inspected development qualifier "+str(window))
        recorded=read_json(source/"r3-exception-audit.json")
        reportpath=out/f"r3-original-frozen-recomputed-{window}.json"
        args=SimpleNamespace(routes=source/"control.rou.xml",
            tripinfo=source/"tripinfo.xml",replay_tripinfo=source/"tripinfo.xml",
            statistics=source/"statistics.xml",
            fcd=source/"observed-fcd.xml",
            native=source/"native-external.xml",
            report=reportpath,seed=2101,window=window)
        frozen_r3.audit(args)
        recomputed=read_json(reportpath)
        if recomputed!=recorded:
            differences=[k for k in sorted(set(recomputed)|set(recorded))
                         if recomputed.get(k)!=recorded.get(k)]
            raise RuntimeError("Production R3 invocation changed frozen method: "+str(differences))
        metrics=read_json(source/"seed-level-metrics.json")
        bridge=read_json(source/"paired-reference-report.json")
        original=archived_sha(source/"archived-source-hashes.txt")
        h=od_from_generated_trips(source/"regenerated.trips.xml")
        od_hashes[window]=h
        source_details=dict(scientific_commit=FROZEN_SHA,sumo_image=SUMO_IMAGE,
            network_sha256=original["source/network.net.xml"],
            trips_sha256=original["source/trips.xml"],
            routes_sha256=original["source/original.rou.xml"],
            od_pair_sha256=h,
            route_audit_byte_identical=True)
        if sha256_file(source/"control.rou.xml")!=source_details["routes_sha256"]:
            raise RuntimeError("Routes have drifted from archived original SHA")
        result=seed_record(2101,window,metrics,recorded,bridge,source_details)
        require(result["status"]=="ELIGIBLE_BY_FROZEN_R3_RULES",
                "Development scenario ineligible")
        if result["matched_edges"]!=8393:
            raise RuntimeError("Original inspected road-edge cohort changed")
        srch=read_json(source/"search-lookup-integrity.json")
        require(srch.get("status")=="PASS" and srch.get("assigned_edges")==8393,
                "Original search-time read audit incomplete")
        result["source_search_read_count"]=srch["edge_cost_reads_observed"]
        result["R3_output_byte_equivalent_to_frozen_science"]=True
        rows.append(result)
        total+=srch["edge_cost_reads_observed"]
    if len(set(od_hashes.values()))!=1:
        raise RuntimeError("Same development seed has different origin/destination pairs across windows")
    with open(out/"production-adapter-development-records.csv","w",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]))
        wr.writeheader();wr.writerows(rows)
    summary=dict(status="REVIEW_ONLY_PRODUCTION_ADAPTERS_PASSED_DEVELOPMENT_EQUIVALENCE",
        original_frozen_scientific_sha=FROZEN_SHA,
        reviewed_development_seed=2101,regimes=[200,600,1200],
        scenarios_passed=len(rows),total_completed_trips=3000,
        original_road_events=sum(x["matched_edges"] for x in rows),
        original_actual_search_reads=total,
        R3_frozen_pure_method_reproduced_exactly=True,
        R4_seed_record_integrity_passed=True,
        OD_fingerprints_match_across_regimes=True,
        activation_template_disabled=True,
        protected_environment_configured=False,
        heldout_access_authorized=False,
        any_reserved_seed_generated_simulated_or_read=False,
        next_step="Separate protected environment setup and future explicit execution approval")
    (out/"production-adapter-review.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))

if __name__=="__main__":main()
