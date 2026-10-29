#!/usr/bin/env python3
"""M3 general-seed scenario driver, deliberately restricted to inspected development seeds.

The pure plan is general-seed-capable but the executable CLI cannot dispatch
reserved evaluation seeds. No production workflow or approval bypass exists.
"""
import argparse,json,subprocess,sys
from pathlib import Path

FROZEN_SHA="be2e8d27c78c8b6de4891115d6d951edc877ac6e"
WINDOWS=(200,600,1200)
RESERVED=tuple(range(3101,3111))
ALLOWED_REHEARSAL=(2101,)
class Blocked(RuntimeError):pass

def scenario_plan(seed,window):
    if type(seed) is not int or type(window) is not int or window not in WINDOWS:
        raise Blocked("Invalid scenario identity")
    if seed in RESERVED:raise Blocked("Reserved evaluation seed is not authorized")
    if seed not in ALLOWED_REHEARSAL:raise Blocked("Runner rehearsal is development-only")
    return dict(seed=seed,window_seconds=window,scientific_commit=FROZEN_SHA,
                expected_vehicles=1000,mode="development_rehearsal",
                evaluation_authorized=False)

def commands(root,seed,window):
    p=scenario_plan(seed,window)
    root=Path(root)
    net=root/"network.net.xml";trips=root/"trips.xml";routes=root/"original.rou.xml"
    audit=root/"original-audit.csv";manifest=root/"original-manifest.json"
    trace=root/"chosen-decision-trace.csv"
    return [
      ["netgenerate","--grid","--grid.number","10","--grid.length","200","--output-file",str(net)],
      [sys.executable,"frozen/experiments/experiment_002/fixed_demand_v01.py",
       "--net",str(net),"--out",str(trips),"--manifest",str(root/"scenario.json"),
       "--seed",str(seed),"--window",str(window)],
      [sys.executable,"frozen/experiments/experiment_002/trace_actual_predictor.py",
       "--net",str(net),"--trips",str(trips),"--out",str(routes),
       "--audit",str(audit),"--manifest",str(manifest),
       "--trace",str(trace),"--candidate-trace",str(root/"candidate-trace.csv"),
       "--decision-trace",str(root/"decisions.csv")],
      ["sumo","-n",str(net),"-r",str(routes),
       "--additional-files",str(root/"measurement.add.xml"),
       "--fcd-output",str(root/"observed-fcd.xml"),
       "--device.fcd.period","1","--fcd-output.attributes","lane,speed,pos",
       "--vehroute-output",str(root/"native-vehroute.xml"),
       "--vehroute-output.exit-times","true","--vehroute-output.internal","true",
       "--statistic-output",str(root/"statistics.xml"),
       "--tripinfo-output",str(root/"tripinfo.xml"),
       "--collision-output",str(root/"collisions.xml"),
       "--seed",str(seed),"--no-step-log","true","--log",str(root/"sumo.log")]
    ]

def run_development(root,seed,window,frozen_sha):
    scenario_plan(seed,window)  # FIRST guard, before file creation or subprocess.
    if frozen_sha!=FROZEN_SHA:raise Blocked("Frozen code checkout mismatch")
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    (root/"measurement.add.xml").write_text(
       '<additional><edgeData id="external" file="native-external.xml" period="30" excludeEmpty="false" withInternal="false"/></additional>\n')
    for cmd in commands(root,seed,window):
        subprocess.run(cmd,check=True)
    (root/"development-runner-provenance.json").write_text(json.dumps(
        scenario_plan(seed,window),indent=2)+"\n")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--window",type=int,required=True)
    p.add_argument("--out",required=True)
    p.add_argument("--frozen-sha",required=True)
    a=p.parse_args()
    run_development(a.out,a.seed,a.window,a.frozen_sha)

if __name__=="__main__":main()
