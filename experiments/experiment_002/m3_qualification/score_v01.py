#!/usr/bin/env python3
"""Mechanical implementation of frozen M3 *timing* summaries on chosen routes.

This qualification CLI only accepts development seed 2101; the pure score_rows
helper is for synthetic fixtures and future separately authorized adapter.
"""
import argparse,collections,csv,json,math,statistics,xml.etree.ElementTree as ET
from pathlib import Path
from guard_v01 import require_development,FROZEN_SHA

def get_rows(path):
    with open(path,newline="") as f:return list(csv.DictReader(f))

def distribution(xs):
    if not xs:return dict(n=0,mae_s=None,bias_s=None,rmse_s=None,abs_p90_s=None,abs_p95_s=None)
    if any(not math.isfinite(x) for x in xs):raise RuntimeError("Nonfinite timing error")
    ordered=sorted(abs(v) for v in xs)
    return dict(n=len(xs),mae_s=round(statistics.mean(ordered),5),
         bias_s=round(statistics.mean(xs),5),
         rmse_s=round(math.sqrt(statistics.mean(x*x for x in xs)),5),
         abs_p90_s=round(ordered[math.ceil(.9*len(ordered))-1],5),
         abs_p95_s=round(ordered[math.ceil(.95*len(ordered))-1],5))

def trips(path):
    result={}
    for e in ET.parse(path).getroot().findall("tripinfo"):
        vid=e.get("id")
        if not vid or vid in result:raise RuntimeError("Duplicate tripinfo")
        result[vid]=dict(depart=float(e.get("depart")),arrival=float(e.get("arrival")),
                         waiting=float(e.get("waitingTime",0)),
                         duration=float(e.get("duration")),
                         time_loss=float(e.get("timeLoss",0)),
                         depart_delay=float(e.get("departDelay",0)))
    return result

def score_rows(rows,tripinfos,planned_vehicles=1000):
    groups=collections.defaultdict(list);index_tracker=collections.defaultdict(list)
    source_counts=collections.Counter()
    for r in rows:
        vid=r["vehicle"];idx=int(r["route_index"])
        if vid not in tripinfos:raise RuntimeError("Unknown trip vehicle: "+vid)
        index_tracker[vid].append(idx)
        observed=float(r["native_entry_s"])
        fcd=float(r["FCD_entry_s"])
        model=float(r["timeaware_predicted_s"])
        freeflow=float(r["freeflow_predicted_s"])
        for x in [observed,fcd,model,freeflow]:
            if not math.isfinite(x) or x<0:raise RuntimeError("Invalid simulation timing value")
        group="first" if idx==0 else "route_1_2" if idx<=2 else "route_3_5" if idx<=5 else "route_6plus"
        groups["timeaware"].append(observed-model)
        groups["freeflow"].append(observed-freeflow)
        groups["timeaware_"+group].append(observed-model)
        groups["freeflow_"+group].append(observed-freeflow)
        groups["FCD_minus_native"].append(fcd-observed)
        lag=tripinfos[vid]["depart"]-model if idx==0 else None
        if idx==0:
            if abs(observed-tripinfos[vid]["depart"])>1e-7:
                raise RuntimeError("First native link entry different from actual tripinfo departure")
            source_counts["first_edge_records"]+=1
    for vid,seq in index_tracker.items():
        if sorted(seq)!=list(range(len(seq))):
            raise RuntimeError("Duplicate or missing edge index: "+vid)
    if len(tripinfos)!=planned_vehicles or len(index_tracker)!=planned_vehicles or source_counts["first_edge_records"]!=planned_vehicles:
        raise RuntimeError("Expected exactly 1000 completed planned trips with first edge entry")
    # departure lag computed once per trip, not once per road
    first_rows={r["vehicle"]:r for r in rows if int(r["route_index"])==0}
    lags=[tripinfos[vid]["depart"]-float(first_rows[vid]["timeaware_predicted_s"]) for vid in sorted(tripinfos)]
    for r in rows:
        vid=r["vehicle"]
        lag=tripinfos[vid]["depart"]-float(first_rows[vid]["timeaware_predicted_s"])
        groups["timeaware_departure_aligned"].append(float(r["native_entry_s"])-float(r["timeaware_predicted_s"])-lag)
    summary={k:distribution(v) for k,v in sorted(groups.items())}
    delta=summary["freeflow"]["mae_s"]-summary["timeaware"]["mae_s"]
    return dict(status="DEVELOPMENT_QUALIFICATION_ONLY_NOT_HELDOUT",
       vehicles=len(index_tracker),edge_traversals=len(rows),
       paired_MAE_benefit_ff_minus_timeaware_s=round(delta,5),
       timing_metrics=summary,departure_lag_s=distribution(lags),
       observed_reference="SUMO native external entry inferred from preceding native link exit, step=1s",
       FCD_reference="first front location per 1s FCD external edge; checked separately",
       primary_statistical_unit="independent seed; not each road edge",
       limits=["No occupancy prediction from prior-route count","No unchosen route realized outcome",
         "Internal residence not causal junction delay","No network/systemwide traffic benefit claim"])

def main():
    p=argparse.ArgumentParser()
    for n in ("paired-road-entry","tripinfo","archived-forecast-report","out"):
        p.add_argument("--"+n,required=True)
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--window",type=int,required=True)
    a=p.parse_args()
    require_development(a.seed,a.window)
    rows=get_rows(a.paired_road_entry)
    summary=score_rows(rows,trips(a.tripinfo))
    reference=json.loads(Path(a.archived_forecast_report).read_text())["forecast_error_seconds"]
    a1=reference["entry_timeaware"]["mae_s"];a2=reference["entry_freeflow"]["mae_s"]
    matched=summary["timing_metrics"]
    # In this frozen development source we already measured identical native/FCD entries.
    # A disagreement here is an implementation integrity issue, not a model accuracy failure.
    if abs(matched["timeaware"]["mae_s"]-a1)>0.0001 or abs(matched["freeflow"]["mae_s"]-a2)>0.0001:
        raise RuntimeError("Qualification does not reproduce prior chosen-route timing error")
    summary.update(seed=a.seed,window_seconds=a.window,
       frozen_scientific_commit=FROZEN_SHA,
       matches_preexisting_M2_forecast_errors=True,
       native_vs_FCD_entry_step_all_equal=matched["FCD_minus_native"]["mae_s"]==0)
    Path(a.out).write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps({k:v for k,v in summary.items() if k!="timing_metrics"},indent=2))
    print("Forecast MAE seconds:",matched["timeaware"]["mae_s"],matched["freeflow"]["mae_s"])

if __name__=="__main__":main()
