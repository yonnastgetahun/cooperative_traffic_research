#!/usr/bin/env python3
"""M3 end-to-end native postprocessing rehearsal, only archived development seed 2101.

Runs frozen original parsing/bridge/R3 and unchanged seed-level score function.
No network generation, no SUMO, no reserved seed data or execution.
"""
import argparse,hashlib,json,sys
from pathlib import Path
from types import SimpleNamespace

FROZEN_SHA="be2e8d27c78c8b6de4891115d6d951edc877ac6e"
WINDOWS=(200,600,1200)
class RehearsalBlocked(RuntimeError):pass

def require_seed(seed,window):
    if type(seed) is not int or seed!=2101 or type(window) is not int or window not in WINDOWS:
        raise RehearsalBlocked("Only inspected development seed 2101 allowed")

def postprocess(source,out,frozen,seed,window):
    require_seed(seed,window) # before mkdir or imports of scientific code
    source=Path(source);out=Path(out);frozen=Path(frozen)
    if not source.is_dir() or not (frozen/"experiments/experiment_002/g3_r3_exception_audit_v01.py").is_file():
        raise RehearsalBlocked("Missing archived development data or frozen source")
    required=("control.rou.xml","tripinfo.xml","statistics.xml","observed-fcd.xml",
      "native-external.xml","native-vehroute.xml","chosen-decision-trace.csv",
      "seed-level-metrics.json","r3-exception-audit.json","paired-reference-report.json")
    missing=[n for n in required if not (source/n).is_file()]
    if missing:raise RehearsalBlocked("Missing archived evidence: "+",".join(missing))
    sys.path.insert(0,str(frozen/"experiments/experiment_002"))
    import g3_native_vehroute_v01 as native
    import g3_timing_bridge_v01 as bridge
    import g3_r3_exception_audit_v01 as r3
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"m3_qualification"))
    import score_v01 as score
    out.mkdir(parents=True,exist_ok=True)
    native.summarize(source/"native-vehroute.xml",source/"control.rou.xml",
       source/"tripinfo.xml",out/"native-events.csv",out/"native-report.json")
    old_argv=sys.argv
    try:
        sys.argv=["g3_timing_bridge_v01.py","--trace",str(source/"chosen-decision-trace.csv"),
          "--events",str(out/"native-events.csv"),"--fcd",str(source/"observed-fcd.xml"),
          "--report",str(out/"paired-reference-report.json"),"--out",str(out/"paired-road-entry.csv")]
        bridge.main()
    finally:sys.argv=old_argv
    args=SimpleNamespace(routes=source/"control.rou.xml",tripinfo=source/"tripinfo.xml",
       replay_tripinfo=source/"tripinfo.xml",statistics=source/"statistics.xml",
       fcd=source/"observed-fcd.xml",native=source/"native-external.xml",
       report=out/"r3-exception-audit.json",seed=seed,window=window)
    r3.audit(args)
    computed=score.score_rows(score.get_rows(out/"paired-road-entry.csv"),
       score.trips(source/"tripinfo.xml"))
    previous=json.loads((source/"seed-level-metrics.json").read_text())
    for key in ("vehicles","edge_traversals","paired_MAE_benefit_ff_minus_timeaware_s"):
        if computed[key]!=previous[key]:
            raise RehearsalBlocked("Frozen score differs from archived development reference: "+key)
    for key in ("timeaware","freeflow"):
        if abs(computed["timing_metrics"][key]["mae_s"]-
               previous["timing_metrics"][key]["mae_s"])>0.0001:
            raise RehearsalBlocked("Frozen predictor metric drift")
    actual=json.loads((out/"r3-exception-audit.json").read_text())
    expected=json.loads((source/"r3-exception-audit.json").read_text())
    if actual!=expected:raise RehearsalBlocked("Frozen R3 output changed")
    bridge_result=json.loads((out/"paired-reference-report.json").read_text())
    if bridge_result["matched"]!=bridge_result["planned_edges"]:
        raise RehearsalBlocked("Incomplete native/FCD road-entry joins")
    files=("native-events.csv","native-report.json","paired-reference-report.json",
           "paired-road-entry.csv","r3-exception-audit.json")
    result=dict(status="DEVELOPMENT_POSTPROCESS_REPRODUCED_FROZEN_REFERENCE",
       seed=seed,window_seconds=window,scientific_commit=FROZEN_SHA,
       vehicles=computed["vehicles"],matched_edges=computed["edge_traversals"],
       source_sha256={name:hashlib.sha256((source/name).read_bytes()).hexdigest() for name in required},
       output_sha256={name:hashlib.sha256((out/name).read_bytes()).hexdigest() for name in files},
       heldout_authorized=False)
    (out/"postprocess-integrity.json").write_text(json.dumps(result,indent=2)+"\n")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True);p.add_argument("--out",required=True)
    p.add_argument("--frozen",required=True);p.add_argument("--seed",type=int,required=True)
    p.add_argument("--window",type=int,required=True)
    a=p.parse_args()
    print(json.dumps(postprocess(a.source,a.out,a.frozen,a.seed,a.window),indent=2))

if __name__=="__main__":main()
