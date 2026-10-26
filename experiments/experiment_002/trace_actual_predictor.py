#!/usr/bin/env python3
"""Non-policy-changing trace of the EXISTING time_aware.py candidate search.

The trace replays search's cost equations on candidate and chosen paths using
the occupancy Counter *before* each assignment. It is not a calibrated traffic
forecast, and the replay may differ from search's winning heap cost when the
cost model depends on arrival time. The differences are reported explicitly.
"""
import argparse, collections, csv, json, os, sys
import xml.etree.ElementTree as ET
sys.path.insert(0, os.path.join(os.environ.get("SUMO_HOME", "/usr/share/sumo"), "tools"))
import sumolib
import time_aware as policy

FIELDS = ["vehicle","route_index","edge","predicted_entry_s",
          "predicted_exit_s","predicted_traversal_cost_s","freeflow_s",
          "lookup_time_bin","prior_assigned_count","capacity_proxy",
          "congestion_surcharge_s","junction_proxy_s",
          "freeflow_entry_s","predicted_cost_definition"]

def trace_path(path, departure, edges, adj, occ, bin_s, pressure, vehicle):
    model_clock = departure
    free_clock = departure
    result = []
    for j, eid in enumerate(path):
        e = edges[eid]
        ff = policy.freeflow(e)
        b = int(model_clock // bin_s)
        # Original search initializes its origin with freeflow cost and
        # charges neither occupancy surcharge nor junction penalty.
        count = occ[(eid,b)] if j else 0
        capacity = max(1.0, e.getLength()*max(e.getLaneNumber(),1)/7.5)
        congestion = ff*pressure*(count/capacity) if j else 0.0
        junction = 1.0 if j and len(adj[path[j-1]])>1 else 0.0
        predicted_cost = ff+congestion+junction
        result.append([vehicle,j,eid,round(model_clock,6),
                       round(model_clock+predicted_cost,6),
                       round(predicted_cost,6),round(ff,6),b,
                       count,round(capacity,6),round(congestion,6),
                       round(junction,6),round(free_clock,6),
                       "original-search-equations-replayed-on-route"])
        model_clock+=predicted_cost
        free_clock+=ff
    return result,model_clock-departure

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--net",required=True);p.add_argument("--trips",required=True)
    p.add_argument("--out",required=True);p.add_argument("--audit",required=True)
    p.add_argument("--manifest",required=True);p.add_argument("--trace",required=True)
    p.add_argument("--decision-trace",required=True)
    p.add_argument("--candidate-trace",required=True)
    p.add_argument("--bin-seconds",type=int,default=30)
    p.add_argument("--pressure",type=float,default=1.0)
    p.add_argument("--detour-percent",type=float,default=0.10)
    p.add_argument("--detour-seconds",type=float,default=30.0)
    p.add_argument("--distance-percent",type=float,default=0.15)
    a=p.parse_args()
    trips=sorted(ET.parse(a.trips).getroot().findall("trip"),key=lambda t:(float(t.get("depart")),t.get("id")))
    net=sumolib.net.readNet(a.net)
    records=[]
    original_search=policy.search
    def observed_search(origin,dest,departure,edges,adj,occupancy,bin_s,pressure):
        i=len(records)
        if i>=len(trips):raise RuntimeError("More route searches than trips")
        t=trips[i]
        if origin!=t.get("from") or dest!=t.get("to") or abs(departure-float(t.get("depart")))>1e-6:
            raise RuntimeError("Search order mismatch: trace cannot be trusted")
        candidate,heap_cost=original_search(origin,dest,departure,edges,adj,occupancy,bin_s,pressure)
        base=policy.ff_path(net,origin,dest)
        cand_rows,cand_replay_cost=trace_path(candidate,departure,edges,adj,occupancy,bin_s,pressure,t.get("id"))
        base_rows,base_replay_cost=trace_path(base,departure,edges,adj,occupancy,bin_s,pressure,t.get("id"))
        records.append({"vehicle":t.get("id"),"candidate":candidate,"baseline":base,
                        "candidate_rows":cand_rows,"baseline_rows":base_rows,
                        "heap_cost":heap_cost,"replay_candidate_cost":cand_replay_cost,
                        "replay_baseline_cost":base_replay_cost})
        return candidate,heap_cost
    policy.search=observed_search
    argv_backup=sys.argv
    sys.argv=["time_aware.py","--net",a.net,"--trips",a.trips,
              "--out",a.out,"--audit",a.audit,"--manifest",a.manifest,
              "--bin-seconds",str(a.bin_seconds),"--pressure",str(a.pressure),
              "--detour-percent",str(a.detour_percent),
              "--detour-seconds",str(a.detour_seconds),
              "--distance-percent",str(a.distance_percent)]
    try:
        policy.main()
    finally:
        policy.search=original_search
        sys.argv=argv_backup
    if len(records)!=len(trips):raise RuntimeError("Not all decisions traced")
    actual_routes={v.get("id"):v.find("route").get("edges").split()
                   for v in ET.parse(a.out).getroot().findall("vehicle")}
    audit={r["vehicle"]:r for r in csv.DictReader(open(a.audit))}
    chosen=[];candidate=[];decisions=[]
    for rec in records:
        vid=rec["vehicle"]
        out=actual_routes[vid]
        same_candidate=out==rec["candidate"]
        same_baseline=out==rec["baseline"]
        if not (same_candidate or same_baseline):
            raise RuntimeError("Chosen route inconsistent with original policy: "+vid)
        # Respect the actual route even when candidate == baseline.
        trace=rec["candidate_rows"] if same_candidate else rec["baseline_rows"]
        chosen.extend(trace)
        candidate.extend(rec["candidate_rows"])
        row=audit[vid]
        decisions.append([vid,row["depart"],row["accepted"],row["route_changed"],
                          row["baseline_freeflow_s"],row["candidate_freeflow_s"],
                          row["baseline_distance_m"],row["candidate_distance_m"],
                          rec["heap_cost"],rec["replay_candidate_cost"],
                          rec["replay_candidate_cost"]-rec["heap_cost"],
                          rec["replay_baseline_cost"],
                          "candidate" if same_candidate else "baseline",
                          "detour_guardrail_rejected" if not int(row["accepted"]) else "accepted",
                          " ".join(rec["candidate"])," ".join(out)])
    def write(path,fields,rows):
        with open(path,"w",newline="") as f:
            w=csv.writer(f);w.writerow(fields);w.writerows(rows)
    write(a.trace,FIELDS,chosen)
    write(a.candidate_trace,FIELDS,candidate)
    write(a.decision_trace,["vehicle","depart","guardrail_accepted","route_changed",
           "baseline_freeflow_s","candidate_freeflow_s","baseline_distance_m",
           "candidate_distance_m","original_search_heap_cost_s",
           "candidate_replayed_cost_s","replay_minus_heap_s",
           "baseline_replayed_cost_s","chosen_trace_source","decision_reason",
           "candidate_edges","chosen_edges"],decisions)
    print("Traced decisions:",len(decisions),"chosen traversals:",len(chosen))
    print("Replay minus heap cost max abs:",max(abs(r[10]) for r in decisions))
    with open(a.manifest) as f: manifest=json.load(f)
    manifest["trace_details"]={
        "source_algorithm":"unmodified time_aware.search and time_aware.main",
        "chosen_edge_rows":len(chosen),"candidate_edge_rows":len(candidate),
        "uses_pre_assignment_occupancy":True,
        "replay_differs_from_heap_due_to_time_bin_path_state":"reported_in_decision_trace",
        "original_occupancy_update":"one bin per assigned edge at freeflow travel time",
        "trace_is_not_physical_occupancy":True,
        "trace_is_not_counterfactual_observation":True}
    with open(a.manifest,"w") as f:json.dump(manifest,f,indent=2)
if __name__=="__main__":main()
