#!/usr/bin/env python3
"""Aggregate Experiment 004 network outcomes with paired seed-level inference."""
import argparse,json,math,statistics,xml.etree.ElementTree as ET
from pathlib import Path
SEEDS=range(3301,3311);WINDOWS=(200,600,1200);ARMS="ABCD"
def scenario(folder):
    a=json.loads((folder/"attempt.json").read_text())
    if a["status"]!="COMPLETE":raise ValueError(f"Incomplete scenario {folder}")
    trips=ET.parse(folder/"tripinfo.xml").getroot().findall("tripinfo")
    durations=[float(t.get("duration")) for t in trips]
    if not durations:raise ValueError("No completed trips")
    return dict(n_completed=len(durations),mean_trip_s=statistics.mean(durations),
                p90_trip_s=sorted(durations)[math.ceil(.9*len(durations))-1])
def analyze(root):
    records=[]
    for seed in SEEDS:
        for w in WINDOWS:
            for arm in ARMS:
                folder=Path(root)/f"seed-{seed}-window-{w}-arm-{arm}"
                m=scenario(folder)
                records.append(dict(seed=seed,window_seconds=w,arm=arm,**m))
    summary={}
    for w in WINDOWS:
        data={(x["seed"],x["arm"]):x for x in records if x["window_seconds"]==w}
        contrasts={}
        for lhs,rhs in (("C","D"),("B","C"),("B","D"),("A","D")):
            vals=[data[(seed,lhs)]["mean_trip_s"]-data[(seed,rhs)]["mean_trip_s"] for seed in SEEDS]
            m=statistics.mean(vals);sd=statistics.stdev(vals)
            h=2.2621571627409915*sd/math.sqrt(len(vals))
            contrasts[f"{lhs}_minus_{rhs}"]=dict(mean_s=m,ci95_s=[m-h,m+h],n_seeds=len(vals))
        summary[str(w)]=contrasts
    return dict(scenarios=records,regimes=summary,primary_D_vs_C_positive=summary["200"]["C_minus_D"]["ci95_s"][0]>0,
        warning="Completed-trip means must be interpreted with completion counts and censoring; not alone sufficient for network benefit.")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();res=analyze(a.root);Path(a.out).write_text(json.dumps(res,indent=2)+"\n");print(json.dumps(res["regimes"],indent=2))
