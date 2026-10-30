#!/usr/bin/env python3
"""Frozen Experiment 003 confirmatory calibration; seed is the uncertainty unit."""
import argparse,csv,json,math,statistics
from pathlib import Path
SEEDS=tuple(range(3201,3211));WINDOWS=(200,600,1200)
COEFFICIENTS={200:(4.053135104279146,11.524898884412591),
 600:(1.7868471223107676,3.9515691107998387),
 1200:(1.8903085164618962,2.6820862794976956)}
def evaluate(root):
    out=[];regimes={}
    for window in WINDOWS:
        for seed in SEEDS:
            folder=Path(root)/f"seed-{seed}-window-{window}"
            attempt=json.loads((folder/"attempt.json").read_text())
            if attempt.get("status")!="COMPLETE" or attempt.get("seed")!=seed or attempt.get("window_seconds")!=window:
                raise ValueError(f"Incomplete scenario {seed}/{window}")
            with (folder/"paired-road-entry.csv").open(newline="") as f:rows=list(csv.DictReader(f))
            if not rows:raise ValueError(f"Empty scenario {seed}/{window}")
            a,b=COEFFICIENTS[window];orig=[];cal=[];signed=[]
            for row in rows:
                k=int(row["route_index"]);obs=float(row["native_entry_s"]);pred=float(row["timeaware_predicted_s"])
                if k<0 or not all(map(math.isfinite,(obs,pred))):raise ValueError("Invalid paired record")
                err=obs-pred
                orig.append(abs(err));cal.append(abs(err-a-b*k));signed.append(err-a-b*k)
            out.append(dict(seed=seed,window_seconds=window,n=len(rows),
                original_mae_s=statistics.mean(orig),calibrated_mae_s=statistics.mean(cal),
                benefit_s=statistics.mean(orig)-statistics.mean(cal),
                calibrated_signed_error_s=statistics.mean(signed)))
        subset=[x for x in out if x["window_seconds"]==window]
        benefits=[x["benefit_s"] for x in subset]
        m=statistics.mean(benefits);sd=statistics.stdev(benefits)
        # Two-sided t critical for df=9.
        half=2.2621571627409915*sd/math.sqrt(10)
        regimes[str(window)]=dict(n_seeds=10,mean_benefit_s=m,ci95_s=[m-half,m+half],
            mean_original_mae_s=statistics.mean(x["original_mae_s"] for x in subset),
            mean_calibrated_mae_s=statistics.mean(x["calibrated_mae_s"] for x in subset),
            mean_calibrated_signed_error_s=statistics.mean(x["calibrated_signed_error_s"] for x in subset))
    return dict(status="FRESH_CONFIRMATORY_RESULTS",coefficient_source="exp003 development run 41017939494",
                scenarios=out,regimes=regimes,primary_support=regimes["200"]["ci95_s"][0]>0)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();result=evaluate(a.root);Path(a.out).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result["regimes"],indent=2))
