#!/usr/bin/env python3
"""Read-only, prespecified M3 mechanism analysis of archived paired road entries."""
import argparse,csv,json,math,statistics
from pathlib import Path
from collections import defaultdict
SEEDS=range(3101,3111)
WINDOWS=(200,600,1200)
BANDS=((1,4),(5,8),(9,16),(17,100000))
def mean(x):return statistics.mean(x) if x else None
def median(x):return statistics.median(x) if x else None
def analyze(root):
    records=[];quality=[]
    for window in WINDOWS:
        for seed in SEEDS:
            path=Path(root)/f"m3-eval-seed-{seed}-window-{window}"/"paired-road-entry.csv"
            with path.open(newline="") as f:
                reader=csv.DictReader(f)
                cols=set(reader.fieldnames or [])
                idcol=next((c for c in ("vehicle_id","veh_id","vehicle","id") if c in cols),None)
                required={"route_index","native_entry_s","timeaware_predicted_s"}
                if not idcol or not required<=cols:raise ValueError(f"{path}: missing required fields")
                rows=list(reader)
            vehicles=defaultdict(dict);duplicates=0;invalid=0
            for row in rows:
                try:
                    vid=row[idcol];k=int(row["route_index"])
                    obs=float(row["native_entry_s"]);pred=float(row["timeaware_predicted_s"])
                    if not vid or k<0 or not all(map(math.isfinite,(obs,pred))):raise ValueError()
                except (ValueError,TypeError,KeyError):
                    invalid+=1;continue
                if k in vehicles[vid]:duplicates+=1;continue
                vehicles[vid][k]=(obs,pred)
            if duplicates or invalid:raise ValueError(f"{path}: {duplicates} duplicates, {invalid} invalid rows")
            initial=[];incr=[];interval=[];strata=defaultdict(list);gaps=0
            for vid,seq in vehicles.items():
                if 0 in seq:initial.append(seq[0][0]-seq[0][1])
                else:gaps+=1
                length=len(seq)
                for k in sorted(seq):
                    if k==0:continue
                    if k-1 not in seq:gaps+=1;continue
                    e=seq[k][0]-seq[k][1]
                    prev=seq[k-1][0]-seq[k-1][1]
                    de=e-prev
                    dt=seq[k][0]-seq[k-1][0]
                    incr.append(de);interval.append((de,dt))
                    band=next((f"{lo}-{hi}" for lo,hi in BANDS if lo<=length<=hi),None)
                    if band:strata[band].append(de)
            records.append(dict(seed=seed,window_seconds=window,n_vehicles=len(vehicles),
                first_edge_mean_s=mean(initial),increment_mean_s=mean(incr),
                increment_median_s=median(incr),increment_positive_fraction=sum(x>0 for x in incr)/len(incr) if incr else None,
                n_increments=len(incr),n_missing_predecessors=gaps,
                observed_inter_entry_mean_s=mean([t for _,t in interval]),
                increment_vs_observed_interval_covariance=statistics.covariance([x for x,_ in interval],[t for _,t in interval]) if len(interval)>1 else None,
                route_length_strata=[dict(route_length_band=b,n=len(v),mean_increment_s=mean(v)) for b,v in sorted(strata.items())]))
            quality.append(dict(seed=seed,window_seconds=window,n_rows=len(rows),n_vehicles=len(vehicles),duplicates=duplicates,invalid=invalid,missing_predecessors=gaps))
    regimes={}
    for w in WINDOWS:
        subset=[r for r in records if r["window_seconds"]==w]
        regimes[str(w)]=dict(n_seeds=len(subset),
            first_edge_seed_mean_s=mean([r["first_edge_mean_s"] for r in subset]),
            increment_seed_mean_s=mean([r["increment_mean_s"] for r in subset]),
            increment_seed_sd_s=statistics.stdev([r["increment_mean_s"] for r in subset]),
            mean_positive_fraction=mean([r["increment_positive_fraction"] for r in subset]),
            observed_inter_entry_seed_mean_s=mean([r["observed_inter_entry_mean_s"] for r in subset]),
            route_length_strata=[dict(band=b,seed_mean_increment_s=mean([next((x["mean_increment_s"] for x in r["route_length_strata"] if x["route_length_band"]==b),None) for r in subset if any(x["route_length_band"]==b for x in r["route_length_strata"])])) for b in (f"{lo}-{hi}" for lo,hi in BANDS)])
    return dict(scope="archived_exploratory_M3",scenarios=records,quality=quality,regimes=regimes,
        limitation="Inter-entry time includes traversal and junction/queue delay; covariance is descriptive, not causal.")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--artifacts",required=True);p.add_argument("--output",required=True)
    a=p.parse_args();result=analyze(a.artifacts);Path(a.output).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result["regimes"],indent=2))
