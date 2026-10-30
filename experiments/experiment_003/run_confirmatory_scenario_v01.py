#!/usr/bin/env python3
"""Experiment 003 fresh confirmatory scenario runner; frozen M3 science."""
import argparse,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]/"experiment_002"/"m3_production_review"
sys.path.insert(0,str(ROOT))
from general_seed_driver_v01 import commands,FROZEN_SHA
from authorized_postprocess_v01 import process
SEEDS=tuple(range(3201,3211))
WINDOWS=(200,600,1200)
def run(seed,window,out,frozen):
    if seed not in SEEDS or window not in WINDOWS:raise ValueError("Seed/window not in Experiment 003 confirmatory manifest")
    frozen=Path(frozen).resolve()
    if subprocess.check_output(["git","-C",str(frozen),"rev-parse","HEAD"],text=True).strip()!=FROZEN_SHA:raise ValueError("Frozen scientific checkout mismatch")
    out=Path(out).resolve()
    if out.exists():raise ValueError("Attempt directory exists; no overwrite")
    out.mkdir(parents=True)
    record={"seed":seed,"window_seconds":window,"status":"FAILED","stage":"initializing","scientific_commit":FROZEN_SHA}
    try:
        (out/"measurement.add.xml").write_text('<additional><edgeData id="external" file="native-external.xml" period="30" excludeEmpty="false" withInternal="false"/></additional>\n')
        for i,cmd in enumerate(commands(out,2101,window)):
            record["stage"]=("network","demand","routing","sumo")[i]
            cmd=[str(frozen/a[7:]) if a.startswith("frozen/") else a for a in cmd]
            for j in range(len(cmd)-1):
                if cmd[j]=="--seed" and cmd[j+1]=="2101":cmd[j+1]=str(seed)
            with (out/f"stage-{i}.log").open("wb") as log:
                result=subprocess.run(cmd,cwd=out if i==3 else None,stdout=log,stderr=subprocess.STDOUT)
            if result.returncode:raise RuntimeError(f"{record['stage']} exited {result.returncode}")
        record["stage"]="postprocess"
        process(out,frozen,seed,window)
        record["status"]="COMPLETE"
    except Exception as exc:
        record["error"]=str(exc)
    finally:
        (out/"attempt.json").write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
    return record
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,required=True);p.add_argument("--window",type=int,required=True)
    p.add_argument("--out",required=True);p.add_argument("--frozen",required=True)
    a=p.parse_args();result=run(a.seed,a.window,a.out,a.frozen)
    print(json.dumps(result))
    if result["status"]!="COMPLETE":sys.exit(1)
