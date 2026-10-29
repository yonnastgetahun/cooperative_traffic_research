#!/usr/bin/env python3
"""Frozen scientific R3/R4 per-scenario processing for authorized M3 evaluation."""
import argparse,hashlib,json,sys
from pathlib import Path
from types import SimpleNamespace

FROZEN_SHA="be2e8d27c78c8b6de4891115d6d951edc877ac6e"

def process(root,frozen,seed,window):
    root=Path(root).resolve();frozen=Path(frozen).resolve()
    required=("original.rou.xml","tripinfo.xml","statistics.xml","observed-fcd.xml",
        "native-external.xml","native-vehroute.xml","chosen-decision-trace.csv",
        "network.net.xml","trips.xml","original-audit.csv")
    missing=[n for n in required if not (root/n).is_file()]
    if missing:raise RuntimeError("Missing scientific evidence: "+",".join(missing))
    sys.path.insert(0,str(frozen/"experiments/experiment_002"))
    import g3_native_vehroute_v01 as native
    import g3_timing_bridge_v01 as bridge
    import g3_r3_exception_audit_v01 as r3
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"m3_qualification"))
    import score_v01 as score
    native.summarize(root/"native-vehroute.xml",root/"original.rou.xml",
        root/"tripinfo.xml",root/"native-events.csv",root/"native-event-integrity.json")
    argv=sys.argv
    try:
        sys.argv=["g3_timing_bridge_v01.py","--trace",str(root/"chosen-decision-trace.csv"),
            "--events",str(root/"native-events.csv"),"--fcd",str(root/"observed-fcd.xml"),
            "--report",str(root/"paired-reference-report.json"),
            "--out",str(root/"paired-road-entry.csv")]
        bridge.main()
    finally:sys.argv=argv
    r3.audit(SimpleNamespace(routes=root/"original.rou.xml",
        tripinfo=root/"tripinfo.xml",replay_tripinfo=root/"tripinfo.xml",
        statistics=root/"statistics.xml",fcd=root/"observed-fcd.xml",
        native=root/"native-external.xml",report=root/"r3-exception-audit.json",
        seed=seed,window=window))
    scores=score.score_rows(score.get_rows(root/"paired-road-entry.csv"),
        score.trips(root/"tripinfo.xml"))
    scores.update(seed=seed,window_seconds=window,frozen_scientific_commit=FROZEN_SHA)
    (root/"seed-level-metrics.json").write_text(json.dumps(scores,indent=2)+"\n")
    r3result=json.loads((root/"r3-exception-audit.json").read_text())
    bridge_result=json.loads((root/"paired-reference-report.json").read_text())
    if r3result["exception_gate"]!="PASS_FOR_THIS_REPLAY":
        raise RuntimeError("R3 ineligible: retain evidence; do not replace seed")
    if bridge_result["matched"]!=bridge_result["planned_edges"]:
        raise RuntimeError("Incomplete native entry join")
    hashes={n:hashlib.sha256((root/n).read_bytes()).hexdigest()
        for n in required+("native-events.csv","paired-road-entry.csv",
                            "paired-reference-report.json","r3-exception-audit.json",
                            "seed-level-metrics.json")}
    return dict(seed=seed,window_seconds=window,scientific_commit=FROZEN_SHA,
                matched_edges=bridge_result["matched"],file_hashes=hashes,
                status="SCIENTIFIC_POSTPROCESS_COMPLETE")

def main():
    p=argparse.ArgumentParser()
    for a in ("root","frozen"):p.add_argument("--"+a,required=True)
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--window",type=int,required=True)
    a=p.parse_args()
    print(json.dumps(process(a.root,a.frozen,a.seed,a.window),indent=2))

if __name__=="__main__":main()
