#!/usr/bin/env python3
"""Fail-closed M3 harness qualification guard.

THIS harness has no held-out mode. It will not generate, simulate, or inspect
reserved evaluation seeds. Frozen scientific source is identified by full SHA.
"""
import argparse, json, pathlib, hashlib

FROZEN_SHA="be2e8d27c78c8b6de4891115d6d951edc877ac6e"
FROZEN_PROTOCOL_DOCUMENT_COMMIT="deba2b1c1df7660e57cc9f69a3c9ca3ded356aca"
FROZEN_PROTOCOL="docs/EXPERIMENT_002_M3_FROZEN_PROTOCOL_V1.md"
FROZEN_MANIFEST="docs/EXPERIMENT_002_M3_PROTOCOL_FREEZE_MANIFEST_V1.json"
SUMO_IMAGE="ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb"
DEVELOPMENT_SEED=2101
WINDOWS=(200,600,1200)

def require_development(seed,window,mode="development"):
    if mode!="development" or int(seed)!=DEVELOPMENT_SEED or int(window) not in WINDOWS:
        raise ValueError("M3 qualification is development-only: seed 2101 and windows 200/600/1200; held-out execution is NOT authorized")
    return True

def inspect_frozen(root):
    root=pathlib.Path(root)
    m=json.loads((root/FROZEN_MANIFEST).read_text())
    assert m["status"]=="SCIENTIFIC_PROTOCOL_FROZEN_HELDOUT_EXECUTION_NOT_AUTHORIZED"
    assert m["approval"]["heldout_simulations_authorized"] is False
    assert m["immutable_references"]["source_snapshot_including_frozen_protocol_commit_sha"]==FROZEN_PROTOCOL_DOCUMENT_COMMIT
    assert m["immutable_references"]["frozen_protocol_git_blob_sha1"]=="ab9c52e007188e95b9162a14aa7fc1783d3e278c"
    assert m["simulator"]["image"]==SUMO_IMAGE
    assert (root/FROZEN_PROTOCOL).is_file()
    fingerprints=m["code_provenance"]["sha256_fingerprints_from_successful_no_simulation_preflight"]
    compared=0
    for path, expected in fingerprints.items():
        actual=hashlib.sha256((root/path).read_bytes()).hexdigest()
        if actual!=expected:
            raise RuntimeError("Frozen source hash mismatch: "+path)
        compared+=1
    if compared<10:
        raise RuntimeError("Incomplete freeze fingerprint inventory")
    return dict(status="FROZEN_SOURCE_VERIFIED",frozen_sha=FROZEN_SHA,
                protocol_document_commit=FROZEN_PROTOCOL_DOCUMENT_COMMIT,
                fingerprint_files_verified=compared,heldout_authorized=False,
                image=SUMO_IMAGE)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--window",type=int,required=True)
    p.add_argument("--frozen-root",required=True)
    p.add_argument("--report",required=True)
    a=p.parse_args()
    require_development(a.seed,a.window)
    report=inspect_frozen(a.frozen_root)
    report.update(seed=a.seed,window_seconds=a.window,purpose="development_harness_qualification_ONLY")
    pathlib.Path(a.report).write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))

if __name__=="__main__":main()
