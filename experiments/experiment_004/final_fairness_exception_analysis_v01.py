#!/usr/bin/env python3
"""Read-only matched-vehicle fairness and structured exception analysis for Experiment 004."""
import argparse,csv,json,math,statistics,xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
SEEDS=range(3301,3311);WINDOWS=(200,600,1200);ARMS="ABCD"
def root(path):return ET.parse(path).getroot() if path.is_file() else None
def pct(values,p):
    x=sorted(values)
    return x[max(0,math.ceil(p*len(x))-1)] if x else None
def analyze(base):
    scenarios=[];contrasts=[]
    for seed in SEEDS:
      for window in WINDOWS:
        per_arm={}
        for arm in ARMS:
          folder=Path(base)/f"seed-{seed}-window-{window}-arm-{arm}"
          attempt=json.loads((folder/"attempt.json").read_text())
          if attempt.get("status")!="COMPLETE":raise ValueError(f"Incomplete {folder}")
          trip=root(folder/"tripinfo.xml")
          demand=root(folder/"trips.xml")
          if trip is None or demand is None:raise ValueError(f"Missing trip/demand evidence {folder}")
          expected={t.get("id"):(t.get("from"),t.get("to")) for t in demand.findall("trip")}
          if len(expected)!=1000:raise ValueError("Expected 1000 unique demand trips")
          observed={t.get("id"):float(t.get("duration")) for t in trip.findall("tripinfo")}
          if len(observed)!=len(trip.findall("tripinfo")):raise ValueError("Duplicate tripinfo IDs")
          if set(observed)!=set(expected):raise ValueError("Missing or extra completed vehicles")
          stats=root(folder/"statistics.xml");collisions=root(folder/"collisions.xml")
          collision_count=len(collisions.findall(".//collision")) if collisions is not None else None
          exception_fields={}
          if stats is not None:
            for elem in stats.iter():
              for k,v in elem.attrib.items():
                if any(term in k.lower() for term in ("teleport","emergency","collision")):
                  exception_fields[f"{elem.tag}.{k}"]=v
          durations=list(observed.values())
          scenarios.append(dict(seed=seed,window_seconds=window,arm=arm,n_completed=len(durations),
            p90_trip_s=pct(durations,.9),p99_trip_s=pct(durations,.99),
            collision_count=collision_count,exception_fields=exception_fields))
          per_arm[arm]=(expected,observed)
        for left,right in (("C","D"),("A","D"),("B","D")):
          demand_l,dl=per_arm[left];demand_r,dr=per_arm[right]
          if demand_l!=demand_r:raise ValueError("Paired OD demand mismatch")
          diffs=[dl[v]-dr[v] for v in sorted(dl)]
          cohorts=defaultdict(list)
          for v in dl:cohorts[demand_l[v]].append(dl[v]-dr[v])
          contrasts.append(dict(seed=seed,window_seconds=window,contrast=f"{left}_minus_{right}",
            n_vehicles=len(diffs),mean_s=statistics.mean(diffs),median_s=statistics.median(diffs),
            helped_by_right=sum(x>0 for x in diffs),harmed_by_right=sum(x<0 for x in diffs),
            unchanged=sum(x==0 for x in diffs),p10_difference_s=pct(diffs,.1),p90_difference_s=pct(diffs,.9),
            n_od_cohorts=len(cohorts),od_cohort_mean_differences_s=[dict(origin=o,destination=d,n=len(v),mean_s=statistics.mean(v))
              for (o,d),v in sorted(cohorts.items())]))
    summary={}
    for w in WINDOWS:
      c=[x for x in contrasts if x["window_seconds"]==w and x["contrast"]=="C_minus_D"]
      s=[x for x in scenarios if x["window_seconds"]==w]
      summary[str(w)]=dict(n_seeds=10,matched_vehicles=sum(x["n_vehicles"] for x in c),
        helped_by_D=sum(x["helped_by_right"] for x in c),harmed_by_D=sum(x["harmed_by_right"] for x in c),
        unchanged=sum(x["unchanged"] for x in c),
        mean_p90_by_arm={a:statistics.mean(x["p90_trip_s"] for x in s if x["arm"]==a) for a in ARMS},
        collision_total_by_arm={a:sum(x["collision_count"] for x in s if x["arm"]==a and x["collision_count"] is not None) if all(x["collision_count"] is not None for x in s if x["arm"]==a) else None for a in ARMS},
        exception_fields_present=sorted(set(k for x in s for k in x["exception_fields"])))
    return dict(source_run=41023721390,scenarios=scenarios,matched_contrasts=contrasts,regimes=summary,
      interpretation_limits=["OD groups with few vehicles have unstable means; descriptive only.","Missing exception fields are unavailable, not zero.","Simulation collisions are not a real-world safety estimate."])
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();result=analyze(a.root);Path(a.out).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result["regimes"],indent=2))
