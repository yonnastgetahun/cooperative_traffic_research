#!/usr/bin/env python3
"""Read-only M3 route-ordinal bias decomposition across 30 archived scenario artifacts.

Input is a directory of extracted GitHub artifact folders named
m3-eval-seed-<seed>-window-<window>. No simulations, calibration, or refitting.
"""
import argparse,csv,json,statistics
from collections import defaultdict
from pathlib import Path

SEEDS=range(3101,3111)
WINDOWS=(200,600,1200)
BINS=((0,0),(1,1),(2,3),(4,7),(8,15),(16,99999))

def analyze(root):
    results=[]
    for window in WINDOWS:
        for seed in SEEDS:
            folder=Path(root)/f"m3-eval-seed-{seed}-window-{window}"
            file=folder/"paired-road-entry.csv"
            if not file.is_file():raise FileNotFoundError(str(file))
            with file.open(newline="") as f:
                reader=csv.DictReader(f)
                fields=set(reader.fieldnames or ())
                required={"route_index","native_entry_s","timeaware_predicted_s"}
                if not required<=fields:raise ValueError(f"{file}: missing {required-fields}")
                rows=list(reader)
            grouped=defaultdict(list)
            vehicles=defaultdict(dict)
            for row in rows:
                idx=int(row["route_index"])
                err=float(row["native_entry_s"])-float(row["timeaware_predicted_s"])
                grouped[idx].append(err)
                vid=row.get("vehicle_id") or row.get("veh_id") or row.get("id")
                if vid is not None:vehicles[vid][idx]=err
            bins=[]
            for lo,hi in BINS:
                vals=[v for i,vs in grouped.items() if lo<=i<=hi for v in vs]
                bins.append(dict(index_range=f"{lo}-{hi}",n=len(vals),
                    mean_signed_error_s=statistics.mean(vals) if vals else None))
            increments=[]
            for seq in vehicles.values():
                for idx in sorted(seq):
                    if idx-1 in seq:increments.append(seq[idx]-seq[idx-1])
            results.append(dict(seed=seed,window_seconds=window,n_rows=len(rows),
                n_vehicles=len(vehicles),first_edge_mean_s=statistics.mean(grouped[0]) if grouped[0] else None,
                mean_consecutive_increment_s=statistics.mean(increments) if increments else None,
                n_increments=len(increments),ordinal_bins=bins))
    summary={}
    for window in WINDOWS:
        subset=[r for r in results if r["window_seconds"]==window]
        summary[str(window)]=dict(n_seeds=len(subset),
            mean_first_edge_s=statistics.mean(r["first_edge_mean_s"] for r in subset),
            mean_within_vehicle_increment_s=statistics.mean(r["mean_consecutive_increment_s"] for r in subset if r["mean_consecutive_increment_s"] is not None),
            ordinal_bin_seed_means=[dict(index_range=subset[0]["ordinal_bins"][j]["index_range"],
                mean_s=statistics.mean(r["ordinal_bins"][j]["mean_signed_error_s"] for r in subset if r["ordinal_bins"][j]["mean_signed_error_s"] is not None))
                for j in range(len(BINS))])
    return {"scope":"exploratory_archived_M3_no_new_simulations","scenarios":results,"regimes":summary}

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--artifacts",required=True);p.add_argument("--output",required=True)
    a=p.parse_args();result=analyze(a.artifacts)
    Path(a.output).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result["regimes"],indent=2))
