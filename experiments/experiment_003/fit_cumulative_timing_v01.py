#!/usr/bin/env python3
"""Experiment 003 development-only cumulative timing calibration.

Fits a_r + b_r * route_index using DEVELOPMENT paired road-entry CSVs only.
No SUMO simulation, no M3 held-out fitting, no implicit confirmatory evaluation.
"""
import argparse,csv,json,math,statistics
from pathlib import Path
M3_HELDOUT=set(range(3101,3111))
REGIMES=(200,600,1200)
def load(root,seed,window):
    path=Path(root)/f"seed-{seed}-window-{window}"/"paired-road-entry.csv"
    with path.open(newline="") as f:
        rows=list(csv.DictReader(f))
    out=[]
    for row in rows:
        k=int(row["route_index"])
        y=float(row["native_entry_s"])-float(row["timeaware_predicted_s"])
        if k<0 or not math.isfinite(y):raise ValueError("Invalid development paired entry")
        out.append((k,y))
    if not out:raise ValueError("Empty development cohort: "+str(path))
    return out
def fit(rows):
    n=len(rows);sx=sum(k for k,y in rows);sy=sum(y for k,y in rows)
    sxx=sum(k*k for k,y in rows);sxy=sum(k*y for k,y in rows)
    denom=n*sxx-sx*sx
    if denom==0:raise ValueError("Need multiple route positions")
    b=(n*sxy-sx*sy)/denom;a=(sy-b*sx)/n
    return dict(offset_s=a,per_edge_s=b,n=n)
def score(rows,coef):
    orig=[abs(y) for k,y in rows]
    corrected=[abs(y-coef["offset_s"]-coef["per_edge_s"]*k) for k,y in rows]
    return dict(original_mae_s=statistics.mean(orig),calibrated_mae_s=statistics.mean(corrected),
        improvement_s=statistics.mean(orig)-statistics.mean(corrected))
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--development-root",required=True)
    p.add_argument("--development-seeds",required=True,help="Comma-separated independent development seed IDs")
    p.add_argument("--out",required=True)
    a=p.parse_args()
    seeds=[int(x) for x in a.development_seeds.split(",")]
    if not seeds or len(set(seeds))!=len(seeds) or any(s in M3_HELDOUT for s in seeds):
        raise SystemExit("Invalid or M3 held-out seed in development cohort")
    result={"status":"DEVELOPMENT_FIT_ONLY","seeds":seeds,"regimes":{}}
    for w in REGIMES:
        data=[(s,load(a.development_root,s,w)) for s in seeds]
        train=[row for _,rows in data for row in rows]
        coeff=fit(train)
        result["regimes"][str(w)]={"coefficients":coeff,
            "in_sample_descriptive_score":score(train,coeff),
            "warning":"In-sample score is not independent validation"}
    Path(a.out).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
