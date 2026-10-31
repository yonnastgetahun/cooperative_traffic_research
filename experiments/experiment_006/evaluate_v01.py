#!/usr/bin/env python3
"""Experiment 006 frozen inference. Seed is the experimental inference unit."""
import argparse
import csv
import json
import math
import statistics
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

SEEDS = tuple(range(3501, 3511))
WINDOWS = (200, 600, 1200)
T_DF9 = 2.2621571627409915
STAT_FIELDS = ("safety.collisions", "safety.emergencyStops", "safety.emergencyBraking")

def quantile(values, p):
    x = sorted(values)
    return x[max(0, math.ceil(len(x) * p) - 1)] if x else None

def interval(values):
    if len(values) != 10 or any(x is None for x in values):
        raise ValueError("Need 10 independent seed-level values")
    avg = statistics.mean(values)
    half = T_DF9 * statistics.stdev(values) / math.sqrt(10)
    return {"mean": avg, "ci95": [avg-half, avg+half], "n_seeds": 10}

def load_routes(path):
    vs = ET.parse(path).getroot().findall("vehicle")
    r = {v.get("id"): tuple(v.find("route").get("edges").split()) for v in vs}
    if len(r) != len(vs) or len(r) != 1000:
        raise ValueError("Missing or duplicate route assignments")
    return r

def load_trips(path):
    vs = ET.parse(path).getroot().findall("tripinfo")
    out = {v.get("id"): {"duration": float(v.get("duration")),
                         "waiting": float(v.get("waitingTime", "0")),
                         "time_loss": float(v.get("timeLoss", "0"))}
           for v in vs}
    if len(out) != len(vs):
        raise ValueError("Duplicate completed trip IDs")
    return out

def safety(path, collision_path):
    root = ET.parse(path).getroot() if path.is_file() else None
    values = {}
    for field in STAT_FIELDS:
        tag, attr = field.split(".")
        e = root.find(tag) if root is not None else None
        raw = e.get(attr) if e is not None else None
        values[field] = float(raw) if raw is not None else None
    if collision_path.is_file():
        collisions = len(ET.parse(collision_path).getroot().findall(".//collision"))
    else:
        collisions = None
    values["collision_file_events"] = collisions
    return values

def classify_diffs(identities, a, e):
    if not identities:
        return None
    ids = sorted(identities)
    benefits = [a[v]["duration"]-e[v]["duration"] for v in ids]
    harm = [-v for v in benefits]
    return {
        "n": len(ids), "mean_A_minus_E_duration_s": statistics.mean(benefits),
        "median_A_minus_E_duration_s": statistics.median(benefits),
        "mean_A_minus_E_waiting_s": statistics.mean(a[v]["waiting"]-e[v]["waiting"] for v in ids),
        "mean_A_minus_E_time_loss_s": statistics.mean(a[v]["time_loss"]-e[v]["time_loss"] for v in ids),
        "helped_E": sum(x>0 for x in benefits),
        "harmed_E": sum(x<0 for x in benefits),
        "unchanged": sum(x==0 for x in benefits),
        "severely_harmed_gt30s": sum(x>30.0 for x in harm),
        "p95_E_minus_A_individual_s": quantile(harm, .95),
        "p99_E_minus_A_individual_s": quantile(harm, .99),
        "max_E_minus_A_individual_s": max(harm),
    }

def read_pair(root, seed, window):
    p = root / f"exp006-seed-{seed}-window-{window}"
    attempt=json.loads((p/"attempt.json").read_text())
    if (attempt.get("status")!="COMPLETE" or attempt.get("seed")!=seed
        or attempt.get("window_seconds")!=window):
        raise ValueError(f"Incomplete or wrong attempted cohort: {p}")
    demand_xml = ET.parse(p/"trips.xml").getroot().findall("trip")
    expected = {t.get("id") for t in demand_xml}
    if len(expected)!=1000:
        raise ValueError("Demand record IDs invalid")
    d={}
    for arm in ("A","E"):
        r=load_routes(p/arm/"routing"/"routes.rou.xml")
        t=load_trips(p/arm/"tripinfo.xml")
        if set(r)!=expected or not set(t).issubset(expected):
            raise ValueError(f"Route / demand / completed ID mismatch at {p} arm {arm}")
        duration=[v["duration"] for v in t.values()]
        d[arm]={"routes":r,"trips":t,"completed":len(t),
                "mean_duration_s":statistics.mean(duration) if duration else None,
                "p90_duration_s":quantile(duration,.9),"p95_duration_s":quantile(duration,.95),
                "p99_duration_s":quantile(duration,.99),
                "mean_waiting_s":statistics.mean([v["waiting"] for v in t.values()]) if t else None,
                "exception_fields":safety(p/arm/"statistics.xml",p/arm/"collisions.xml")}
        if len(t)!=attempt.get(arm,{}).get("completed"):
            raise ValueError("Completion mismatch with attempt manifest")
    A,E=d["A"],d["E"]
    matched=set(A["trips"]) & set(E["trips"])
    changed={v for v in matched if A["routes"][v]!=E["routes"][v]}
    same=matched-changed
    all_stats=classify_diffs(matched,A["trips"],E["trips"])
    res={"seed":seed,"window_seconds":window,"matched":len(matched),
         "complete_pair":A["completed"]==1000 and E["completed"]==1000,
         "A":{k:v for k,v in A.items() if k not in ("routes","trips")},
         "E":{k:v for k,v in E.items() if k not in ("routes","trips")},
         "changed_routes":len(changed),"unchanged_routes":len(same),
         "all":all_stats,"changed":classify_diffs(changed,A["trips"],E["trips"]),
         "unchanged":classify_diffs(same,A["trips"],E["trips"])}
    if res["complete_pair"] and len(matched)==1000:
        res["A_minus_E_mean_duration_s"]=A["mean_duration_s"]-E["mean_duration_s"]
        for q in ("p90","p95","p99"):
            res[f"A_minus_E_{q}_duration_s"]=A[f"{q}_duration_s"]-E[f"{q}_duration_s"]
    return res

def evaluate(source):
    allrows=[read_pair(Path(source),seed,window) for window in WINDOWS for seed in SEEDS]
    summary={}
    for window in WINDOWS:
        rows=[r for r in allrows if r["window_seconds"]==window]
        complete=all(r["complete_pair"] and r["matched"]==1000 for r in rows)
        out={"n_pairs":len(rows),"complete":complete,
             "A_completed":sum(r["A"]["completed"] for r in rows),
             "E_completed":sum(r["E"]["completed"] for r in rows),
             "matched_vehicles":sum(r["matched"] for r in rows),
             "changed_routes":sum(r["changed_routes"] for r in rows)}
        if complete:
            for metric in ("mean","p90","p95","p99"):
                out[f"A_minus_E_{metric}_duration_s"]=interval(
                    [r[f"A_minus_E_{metric}_duration_s"] for r in rows])
            for subgroup in ("all","changed","unchanged"):
                subset=[r[subgroup] for r in rows]
                n=sum(v["n"] for v in subset if v)
                helped=sum(v["helped_E"] for v in subset if v)
                harmed=sum(v["harmed_E"] for v in subset if v)
                severe=sum(v["severely_harmed_gt30s"] for v in subset if v)
                out[subgroup]={"n":n,"E_helped":helped,"E_harmed":harmed,
                               "E_unchanged":n-helped-harmed,
                               "E_severely_harmed_gt30s":severe,
                               "harmed_fraction":harmed/n if n else None,
                               "severe_fraction":severe/n if n else None}
                if all(v is not None for v in subset):
                    out[subgroup]["seed_mean_A_minus_E_s"]=interval(
                        [v["mean_A_minus_E_duration_s"] for v in subset])
                    out[subgroup]["seed_mean_A_minus_E_waiting_s"]=interval(
                        [v["mean_A_minus_E_waiting_s"] for v in subset])
                    out[subgroup]["seed_mean_p95_individual_harm_s"]=interval(
                        [v["p95_E_minus_A_individual_s"] for v in subset])
        field_totals={}
        for arm in ("A","E"):
            vals=[r[arm]["exception_fields"] for r in rows]
            keys=sorted(set().union(*(x.keys() for x in vals)))
            field_totals[arm]={k:(sum(float(v[k]) for v in vals)
                                  if all(v.get(k) is not None for v in vals) else None)
                               for k in keys}
        out["exceptions"]=field_totals
        summary[str(window)]=out
    p=summary["200"]
    if not p["complete"]:
        decision="INCONCLUSIVE / COMPLETION: all-departure effect not identified"
    else:
        ci=p["A_minus_E_mean_duration_s"]["ci95"]
        tail_E_minus_A=-p["A_minus_E_p90_duration_s"]["mean"]
        flags={
            "primary_ci_positive":ci[0]>0,
            "complete_both_arms":p["complete"],
            "tail_E_minus_A_no_more_than_5s":tail_E_minus_A<=5,
            "harmed_fraction_le_50pct":p["all"]["harmed_fraction"]<=0.5,
            "severe_gt30s_fraction_le_10pct":p["all"]["severe_fraction"]<=0.1,
        }
        a=p["exceptions"]["A"]
        e=p["exceptions"]["E"]
        present=all(a.get(k) is not None and e.get(k) is not None for k in STAT_FIELDS)
        flags["structured_exceptions_observed"]=present
        if present:
            flags["no_exception_disadvantage"]=all(e[k]<=a[k] for k in STAT_FIELDS)
        else:
            flags["no_exception_disadvantage"]=None
        if ci[1]<0:
            decision="NO-GO: E slower than A on primary high-congestion outcome"
        elif ci[0]<=0:
            decision="INCONCLUSIVE: primary seed-level interval includes zero"
        elif not all(v is True for v in flags.values()):
            decision="MEAN BENEFIT / FAIRNESS OR EXCEPTION GATE NOT PASSED"
        else:
            decision="GO: E beats this specific independent free-flow A baseline under all prespecified gates"
        p["joint_decision_gates"]=flags
        p["tail_E_minus_A_s"]=tail_E_minus_A
    return {"experiment":"006","status":"completed archival evaluation",
            "inference_unit":"independent demand seed",
            "baseline_limitation":"A is independent nominal free-flow shortest path; NOT modern live traffic-aware navigation.",
            "primary_decision":decision,"regimes":summary,"seed_pairs":allrows}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args()
    result=evaluate(a.root)
    path=Path(a.out)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+"\n")
    with (path.parent/"exp006-paired-seed-summary.csv").open("w",newline="") as f:
        cols=["seed","window_seconds","A_completed","E_completed","matched",
              "A_mean_s","E_mean_s","A_minus_E_mean_s","A_minus_E_p90_s",
              "changed_routes","E_helped","E_harmed","E_severely_harmed_gt30s"]
        w=csv.DictWriter(f,fieldnames=cols)
        w.writeheader()
        for v in result["seed_pairs"]:
            w.writerow({
                "seed":v["seed"],"window_seconds":v["window_seconds"],
                "A_completed":v["A"]["completed"],"E_completed":v["E"]["completed"],
                "matched":v["matched"],
                "A_mean_s":v["A"]["mean_duration_s"],"E_mean_s":v["E"]["mean_duration_s"],
                "A_minus_E_mean_s":v.get("A_minus_E_mean_duration_s"),
                "A_minus_E_p90_s":v.get("A_minus_E_p90_duration_s"),
                "changed_routes":v["changed_routes"],
                "E_helped":v["all"]["helped_E"] if v["all"] else None,
                "E_harmed":v["all"]["harmed_E"] if v["all"] else None,
                "E_severely_harmed_gt30s":v["all"]["severely_harmed_gt30s"] if v["all"] else None,
            })
    print(json.dumps({"decision":result["primary_decision"],
                      "high":result["regimes"]["200"],
                      "moderate":result["regimes"]["600"].get("A_minus_E_mean_duration_s"),
                      "lower":result["regimes"]["1200"].get("A_minus_E_mean_duration_s")},indent=2))

if __name__=="__main__":
    main()
