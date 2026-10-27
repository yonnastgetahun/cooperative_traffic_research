#!/usr/bin/env python3
"""R4 prespecified seed-level *development dry run*, never read evaluation seeds.

The unit of variability is a demand seed within a regime; per-edge observations
must not become independent replicates. Held-out CI helper accepts n=10
synthetic fixtures only; not invoked in development analysis.
"""
import argparse,collections,csv,json,math,statistics
from pathlib import Path

DEVELOPMENT_SEEDS=(2101,2102,2103)
REGIMES=(200,600,1200)
HOLDOUT_COUNT_TARGET=10
T_CRITICAL_DF9_975=2.2621571628540993

def mean_ci_if_ten(values):
    if len(values)!=HOLDOUT_COUNT_TARGET:
        raise ValueError("Prespecified 10-seed interval cannot be computed on other n")
    if not all(math.isfinite(x) for x in values):
        raise ValueError("Nonfinite paired seed delta")
    avg=statistics.mean(values)
    sd=statistics.stdev(values)
    width=T_CRITICAL_DF9_975*sd/math.sqrt(len(values))
    return dict(seed_count=10,mean=avg,sd=sd,half_width=width,
                lower=avg-width,upper=avg+width,
                interpretation="t interval conditional on independent demand seeds in this fixed synthetic testbed; not network or real-world uncertainty")

def read_development(path):
    with open(path,newline="") as f:rows=list(csv.DictReader(f))
    seen={}
    for r in rows:
        s=int(r["seed"]);w=int(r["window_seconds"])
        if s not in DEVELOPMENT_SEEDS or w not in REGIMES:
            raise ValueError("Forbidden seed/window for development analysis")
        if (s,w) in seen:raise ValueError("Duplicate development scenario")
        if int(r["completed"])!=1000 or int(r["planned"])!=1000 or int(r["matched_route_vehicles"])!=1000:
            raise ValueError("Incomplete seed-level coverage")
        ta=float(r["timeaware_entry_mae_s"])
        ff=float(r["freeflow_entry_mae_s"])
        bias=float(r["timeaware_entry_bias_s"])
        if not all(map(math.isfinite,(ta,ff,bias))) or min(ta,ff)<0:
            raise ValueError("Negative/nonfinite error input")
        seen[(s,w)]=dict(seed=s,window_seconds=w,
            timeaware_mae_s=ta,freeflow_mae_s=ff,
            paired_delta_s=ff-ta,timeaware_bias_s=bias)
    expected={(s,w) for s in DEVELOPMENT_SEEDS for w in REGIMES}
    if set(seen)!=expected:
        raise ValueError("Missing prespecified development scenario: "+str(sorted(expected-set(seen))))
    return [seen[k] for k in sorted(seen)]

def summarize(rows):
    report=[]
    for w in REGIMES:
        vals=[r["paired_delta_s"] for r in rows if r["window_seconds"]==w]
        ta=[r["timeaware_mae_s"] for r in rows if r["window_seconds"]==w]
        ff=[r["freeflow_mae_s"] for r in rows if r["window_seconds"]==w]
        b=[r["timeaware_bias_s"] for r in rows if r["window_seconds"]==w]
        report.append(dict(window_seconds=w,seeds=len(vals),
          paired_delta_mean_s=round(statistics.mean(vals),6),
          paired_delta_sd_s=round(statistics.stdev(vals),6),
          paired_delta_median_s=round(statistics.median(vals),6),
          paired_delta_min_s=round(min(vals),6),
          paired_delta_max_s=round(max(vals),6),
          timeaware_MAE_seedmean_s=round(statistics.mean(ta),6),
          freeflow_MAE_seedmean_s=round(statistics.mean(ff),6),
          timeaware_signed_bias_seedmean_s=round(statistics.mean(b),6),
          uncertainty_status="DESCRIPTIVE_THREE_DEVELOPMENT_SEEDS_NO_HELDOUT_CI"))
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    rows=read_development(a.input)
    summary=summarize(rows)
    with open(out/"r4-development-per-seed.csv","w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    with open(out/"r4-development-seed-summary.csv","w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(summary[0]));writer.writeheader();writer.writerows(summary)
    spec=dict(status="R4_DEVELOPMENT_DRY_RUN_NOT_M3",
        schema_version="g3-r4-seed-v0.1",
        dataset="existing published M2 development seeds 2101-2103 only",
        development_seed_list=list(DEVELOPMENT_SEEDS),
        regime_windows_s=list(REGIMES),
        per_seed_paired_delta_definition="MAE_freeflow - MAE_timeaware on identical chosen routes and matched external road visits",
        primary_congestion_window_s=200,
        secondary_windows_s=[600,1200],
        unit_of_analysis="independent demand seed within fixed network",
        uncertainty_methods={
          "development_dryrun":"n=3 means, sample SD, median and range only; no evaluation claims",
          "future_only_after_approval":"ten-paired-seed Student t 95% CI, df9 tcritical 2.2621571628540993",
          "rule_for_fewer_than_ten_eligible":"do not compute planned heldout 10-seed conclusion or replace missing seeds"},
        data_integrity={
          "expected_development_rows":9,"passed":len(rows)==9,
          "completed_each_scenario":1000,
          "no_reserved_evaluation_seed_access":True,
          "not_treating_edges_as_independent":True},
        nonclaims=["not a traffic-routing efficacy comparison","not real-world safety",
          "prior route-assignment count is not physical occupancy",
          "not proof of calibrated predictor","heldout seeds remain unrun"])
    (out/"r4-analysis-dryrun.json").write_text(json.dumps(spec,indent=2)+"\n")
    lines=["# R4 — Development-only paired seed analysis (no M3 freeze)","",
           "This is a dry run of the predeclared formulas using three already inspected seeds per regime.",
           "Each row in the summary represents the variability of **seed-level paired mean errors**; road-edge traversals are not assumed independent.",
           "",
           "| Window | Mean improvement in timing MAE (FF − time-aware), s | Sample SD across 3 seeds, s | Mean TA lateness bias, s |",
           "|---|---:|---:|---:|"]
    for v in summary:
        lines.append(f"| {v['window_seconds']}s | {v['paired_delta_mean_s']:.2f} | {v['paired_delta_sd_s']:.2f} | {v['timeaware_signed_bias_seedmean_s']:.2f} |")
    lines.extend(["","All numbers here are **exploratory development results**. No Student-t held-out confidence interval is calculated from these three seeds.",
      "The later evaluation design targets ten untouched paired seeds per regime, subject to independent freeze authorization.",
      "The time-aware predictor may show lower error while still systematically predicting arrival too early.",
      "Do not equate prediction quality with improved network-wide traffic outcomes.",""])
    (out/"R4_DEVELOPMENT_ANALYSIS.md").write_text("\n".join(lines))
    print("\n".join(lines))

if __name__=="__main__":main()
