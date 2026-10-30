#!/usr/bin/env python3
"""Read-only archived Experiment 004 outcome audit; 120 prespecified arm archives."""
import argparse,csv,json,math,statistics,xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
SEEDS=range(3301,3311);WINDOWS=(200,600,1200);ARMS="ABCD"
def read_xml(path):
    if not path.is_file():return None
    return ET.parse(path).getroot()
def evaluate(root):
    records=[];paired={}
    for seed in SEEDS:
      for window in WINDOWS:
        for arm in ARMS:
          folder=Path(root)/f"seed-{seed}-window-{window}-arm-{arm}"
          attempt=json.loads((folder/"attempt.json").read_text())
          if attempt.get("status")!="COMPLETE":raise ValueError(f"Incomplete {folder}")
          trips=read_xml(folder/"tripinfo.xml")
          routes=read_xml(folder/"routing"/"routes.rou.xml")
          original=read_xml(folder/"trips.xml")
          if trips is None or routes is None:raise ValueError(f"Missing tripinfo/routes {folder}")
          completed=trips.findall("tripinfo")
          ids=[x.get("id") for x in completed]
          if len(ids)!=len(set(ids)):raise ValueError(f"Duplicate completed vehicle IDs {folder}")
          route_map={v.get("id"):v.find("route").get("edges") for v in routes.findall("vehicle")}
          if len(route_map)!=len(routes.findall("vehicle")):raise ValueError("Duplicate route vehicle IDs")
          durations=sorted(float(t.get("duration")) for t in completed)
          expected=1000
          if len(route_map)!=expected:raise ValueError(f"Expected 1000 routed vehicles: {folder}")
          collisions=read_xml(folder/"collisions.xml")
          stats=read_xml(folder/"statistics.xml")
          collision_count=len(collisions.findall(".//collision")) if collisions is not None else None
          stats_fields={}
          if stats is not None:
            for elem in stats.iter():
              for key,val in elem.attrib.items():
                if "teleport" in key.lower() or "emergency" in key.lower() or "collision" in key.lower():
                  stats_fields[elem.tag+"."+key]=val
          od={}
          if original is not None:
            od={t.get("id"):(t.get("from"),t.get("to")) for t in original.findall("trip")}
          cohorts=defaultdict(list)
          for t in completed:
            vid=t.get("id")
            if vid in od:cohorts[od[vid]].append(float(t.get("duration")))
          record=dict(seed=seed,window_seconds=window,arm=arm,expected_vehicles=expected,
            n_completed=len(ids),n_incomplete=expected-len(ids),completion_fraction=len(ids)/expected,
            mean_completed_duration_s=statistics.mean(durations) if durations else None,
            p90_completed_duration_s=durations[math.ceil(.9*len(durations))-1] if durations else None,
            collisions_count=collision_count,exception_statistics=stats_fields,
            od_cohort_count=len(cohorts),od_fairness_available=bool(od),
            all_departure_mean_duration_identifiable=len(ids)==expected,
            censoring_note=None if len(ids)==expected else "Incomplete vehicle travel times not inferred from completed trips")
          records.append(record)
          paired[(seed,window,arm)]=route_map
    route_changes={}
    for window in WINDOWS:
      changes=[]
      for seed in SEEDS:
        c=paired[(seed,window,"C")];d=paired[(seed,window,"D")]
        if set(c)!=set(d):raise ValueError("C/D vehicle identity mismatch")
        changes.append(dict(seed=seed,changed=sum(c[v]!=d[v] for v in c),total=len(c)))
      route_changes[str(window)]=changes
    return dict(scenarios=records,route_changes_C_vs_D=route_changes,
      notes=["Missing structured exception fields are unavailable, not zero.",
             "OD fairness availability is reported; detailed cohort effects require matched completed-trip analysis."])
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--out",required=True)
    a=p.parse_args();res=evaluate(a.root);Path(a.out).write_text(json.dumps(res,indent=2)+"\n")
    print(json.dumps({"n_scenarios":len(res["scenarios"]),"completion_ranges":{str(w):[min(x["completion_fraction"] for x in res["scenarios"] if x["window_seconds"]==w),max(x["completion_fraction"] for x in res["scenarios"] if x["window_seconds"]==w)] for w in WINDOWS},"route_changes":{w:sum(x["changed"] for x in v) for w,v in res["route_changes_C_vs_D"].items()}},indent=2))
