#!/usr/bin/env python3
"""Explicitly authorized M3 evaluation scenario execution; preserves all attempt evidence.

Does not alter frozen predictor, demand, or simulator code. Run only in pinned
SUMO environment with frozen checkout at FROZEN_SHA. One scenario per invocation.
"""
import argparse,hashlib,json,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
from general_seed_driver_v01 import commands,scenario_plan,FROZEN_SHA,Blocked
from adapters_v01 import SUMO_IMAGE
from authorized_postprocess_v01 import process

def digest(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1048576),b""):h.update(b)
    return h.hexdigest()

def execute(seed,window,out,frozen,acknowledge=False):
    if acknowledge is not True:
        raise Blocked("Explicit evaluation execution flag required")
    plan=scenario_plan(seed,window,authorized_evaluation=True)
    frozen=Path(frozen).resolve()
    if subprocess.check_output(["git","-C",str(frozen),"rev-parse","HEAD"],text=True).strip()!=FROZEN_SHA:
        raise Blocked("Frozen scientific checkout SHA mismatch")
    out=Path(out).resolve()
    if out.exists():raise Blocked("Existing attempt directory: no overwrite/retry")
    out.mkdir(parents=True)
    record=dict(plan,simulator_image=SUMO_IMAGE,status="FAILED",stage="initializing",
                started_at_utc=datetime.now(timezone.utc).isoformat(),files={})
    try:
        (out/"measurement.add.xml").write_text(
            '<additional><edgeData id="external" file="native-external.xml" period="30" excludeEmpty="false" withInternal="false"/></additional>\n')
        for index,cmd in enumerate(commands(out,seed,window,authorized_evaluation=True)):
            record["stage"]=["network","demand","routing","sumo"][index]
            # Frozen script paths are relative to working directory; use absolute frozen paths.
            cmd=[str(frozen / arg[7:]) if arg.startswith("frozen/") else arg for arg in cmd]
            with (out/f"stage-{index}-{record['stage']}.log").open("wb") as log:
                result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=False)
            if result.returncode:raise RuntimeError(f"{record['stage']} exited {result.returncode}")
        record["stage"]="frozen-route-equivalence"
        control=[sys.executable,str(frozen/"experiments/experiment_002/time_aware.py"),
          "--net",str(out/"network.net.xml"),"--trips",str(out/"trips.xml"),
          "--out",str(out/"control.rou.xml"),"--audit",str(out/"control-audit.csv"),
          "--manifest",str(out/"control-manifest.json")]
        with (out/"stage-route-equivalence.log").open("wb") as log:
            subprocess.run(control,stdout=log,stderr=subprocess.STDOUT,check=True)
        if (out/"control.rou.xml").read_bytes()!=(out/"original.rou.xml").read_bytes():
            raise RuntimeError("Frozen route assignment differs from traced predictor")
        if (out/"control-audit.csv").read_bytes()!=(out/"original-audit.csv").read_bytes():
            raise RuntimeError("Frozen route audit differs from traced predictor")
        record["stage"]="postprocess"
        with (out/"stage-4-postprocess.log").open("w") as log:
            try:
                details=process(out,frozen,seed,window)
                log.write(json.dumps(details,indent=2)+"\n")
            except Exception as error:
                log.write(type(error).__name__+": "+str(error)+"\n")
                raise
        record["stage"]="archive"
        record["status"]="COMPLETE"
    except Exception as e:
        record["error"]=str(e)
    finally:
        record["files"]={str(p.relative_to(out)):digest(p) for p in out.rglob("*") if p.is_file() and p.name!="attempt.json"}
        record["finished_at_utc"]=datetime.now(timezone.utc).isoformat()
        (out/"attempt.json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
    return record

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--window",type=int,required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--frozen",required=True)
    p.add_argument("--authorized-evaluation",action="store_true")
    a=p.parse_args()
    result=execute(a.seed,a.window,a.out,a.frozen,a.authorized_evaluation)
    print(json.dumps(result))
    if result["status"]!="COMPLETE":sys.exit(1)

if __name__=="__main__":main()
