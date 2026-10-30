#!/usr/bin/env python3
"""Experiment 004 four-arm route generation. No observed future SUMO input."""
import argparse,csv,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"experiment_002"))
import time_aware as policy
from prospective_search_adapter_v01 import search as stateful_search
COEFF={200:(4.053135104279146,11.524898884412591),600:(1.7868471223107676,3.9515691107998387),1200:(1.8903085164618962,2.6820862794976956)}
def generate(net,trips,arm,window,out):
    if arm not in "ABCD" or window not in COEFF:raise ValueError("Invalid arm/window")
    out=Path(out);out.mkdir(parents=True,exist_ok=True)
    args=["--net",str(net),"--trips",str(trips),"--out",str(out/"routes.rou.xml"),"--audit",str(out/"audit.csv"),"--manifest",str(out/"manifest.json")]
    saved=sys.argv
    original=policy.search
    if arm=="A":
        def independent(origin,dest,departure,edges,adj,occupancy,bin_s,pressure):
            path=policy.ff_path(network,origin,dest)
            return path,sum(policy.freeflow(edges[e]) for e in path)
        import sumolib
        network=sumolib.net.readNet(str(net))
        policy.search=independent
    elif arm=="B":policy.search=original
    else:
        a,b=(0.0,0.0) if arm=="C" else COEFF[window]
        def patched(origin,dest,departure,edges,adj,occupancy,bin_s,pressure):
            return stateful_search(origin,dest,departure,edges,adj,occupancy,bin_s,pressure,
                offset_s=a,per_edge_s=b,force_stateful_zero=True)
        policy.search=patched
    try:
        sys.argv=["time_aware.py"]+args
        policy.main()
    finally:
        policy.search=original;sys.argv=saved
    manifest=json.loads((out/"manifest.json").read_text())
    manifest.update(experiment="004",arm=arm,window_seconds=window,
        calibrated=(arm=="D"),calibration_coefficients=COEFF[window] if arm=="D" else None,
        forecast_uses_future_sumo_observations=False)
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    for key in ("net","trips","arm","out"):p.add_argument("--"+key,required=True)
    p.add_argument("--window",type=int,required=True)
    a=p.parse_args();generate(a.net,a.trips,a.arm,a.window,a.out)
