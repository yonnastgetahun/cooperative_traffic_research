#!/usr/bin/env python3
"""Generate Experiment 004 routes and execute SUMO for one prespecified arm."""
import argparse,json,subprocess,sys
from pathlib import Path
SEEDS=tuple(range(3301,3311));WINDOWS=(200,600,1200);ARMS="ABCD"
FROZEN="be2e8d27c78c8b6de4891115d6d951edc877ac6e"
def run(seed,window,arm,out,frozen):
    if seed not in SEEDS or window not in WINDOWS or arm not in ARMS:raise ValueError("Not in frozen Experiment 004 manifest")
    out=Path(out).resolve();frozen=Path(frozen).resolve()
    if subprocess.check_output(["git","-C",str(frozen),"rev-parse","HEAD"],text=True).strip()!=FROZEN:raise ValueError("Frozen scientific checkout mismatch")
    if out.exists():raise ValueError("Existing scenario: no overwrite")
    out.mkdir(parents=True)
    record=dict(seed=seed,window_seconds=window,arm=arm,status="FAILED",stage="init",scientific_base=FROZEN)
    try:
        net=out/"network.net.xml";trips=out/"trips.xml"
        commands=[
          ["netgenerate","--grid","--grid.number","10","--grid.length","200","--output-file",str(net)],
          [sys.executable,str(frozen/"experiments/experiment_002/fixed_demand_v01.py"),"--net",str(net),"--out",str(trips),"--manifest",str(out/"demand.json"),"--seed",str(seed),"--window",str(window)],
          [sys.executable,str(Path(__file__).resolve().parent/"four_arm_routes_v01.py"),"--net",str(net),"--trips",str(trips),"--arm",arm,"--window",str(window),"--out",str(out/"routing")],
        ]
        for i,cmd in enumerate(commands):
            record["stage"]=("network","demand","routing")[i]
            with (out/f"stage-{i}.log").open("wb") as log:
                result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
            if result.returncode:raise RuntimeError(f"{record['stage']} failed ({result.returncode})")
        record["stage"]="SUMO"
        cmd=["sumo","-n",str(net),"-r",str(out/"routing"/"routes.rou.xml"),"--tripinfo-output",str(out/"tripinfo.xml"),
             "--statistic-output",str(out/"statistics.xml"),"--collision-output",str(out/"collisions.xml"),
             "--seed",str(seed),"--no-step-log","true","--log",str(out/"sumo.log")]
        with (out/"stage-sumo.log").open("wb") as log:
            result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
        if result.returncode:raise RuntimeError(f"SUMO failed ({result.returncode})")
        record["status"]="COMPLETE"
    except Exception as exc:record["error"]=str(exc)
    finally:(out/"attempt.json").write_text(json.dumps(record,indent=2)+"\n")
    return record
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,required=True);p.add_argument("--window",type=int,required=True)
    p.add_argument("--arm",required=True);p.add_argument("--out",required=True);p.add_argument("--frozen",required=True)
    a=p.parse_args();result=run(a.seed,a.window,a.arm,a.out,a.frozen);print(json.dumps(result))
    if result["status"]!="COMPLETE":sys.exit(1)
