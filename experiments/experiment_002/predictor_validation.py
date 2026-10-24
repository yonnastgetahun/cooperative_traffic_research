#!/usr/bin/env python3
"""Offline predictor-vs-SUMO observations. Diagnostics, not a new routing policy."""
import argparse,csv,collections,json,math,statistics,xml.etree.ElementTree as ET,os,sys
sys.path.insert(0,os.path.join(os.environ.get("SUMO_HOME","/usr/share/sumo"),"tools"))
import sumolib

def percentile(a,p):
    s=sorted(a);return s[min(len(s)-1,int(p*(len(s)-1)))] if s else None

def write_predictions(args):
    net=sumolib.net.readNet(args.net)
    edges={e.getID():e for e in net.getEdges()}
    vehicles=ET.parse(args.routes).getroot().findall("vehicle")
    rows=[];pred=collections.Counter()
    for v in sorted(vehicles,key=lambda v:(float(v.get("depart")),v.get("id"))):
        t=float(v.get("depart"))
        for idx,eid in enumerate(v.find("route").get("edges").split()):
            e=edges[eid];duration=e.getLength()/max(e.getSpeed(),0.1)
            entry=t;exit=t+duration
            rows.append([v.get("id"),idx,eid,entry,exit,duration])
            # Forecast occupancy as number of vehicles whose predicted edge traversal intersects bin.
            start=int(entry//args.bin_seconds);end=int(max(entry,exit-1e-8)//args.bin_seconds)
            for b in range(start,end+1):pred[(eid,b)]+=1
            t=exit
    with open(args.predictions,"w",newline="") as f:
        w=csv.writer(f);w.writerow(["vehicle","route_index","edge","predicted_entry_s","predicted_exit_s","predicted_freeflow_traversal_s"]);w.writerows(rows)
    with open(args.predicted_occupancy,"w",newline="") as f:
        w=csv.writer(f);w.writerow(["edge","time_bin","predicted_vehicle_count"]);w.writerows((e,b,n) for (e,b),n in sorted(pred.items()))
    print("predicted traversals",len(rows),"vehicles",len(vehicles))

def compare(args):
    # FCD samples at 1-second resolution: lane prefix maps to edge, but internal lanes are excluded.
    prediction=list(csv.DictReader(open(args.predictions)))
    valid_edges={r["edge"] for r in prediction}
    tracks=collections.defaultdict(list)
    observed_bins=collections.defaultdict(set)
    sample_count=0;internal_count=0
    for event,elem in ET.iterparse(args.fcd,events=("end",)):
        if elem.tag!="timestep":continue
        t=float(elem.get("time"))
        for v in elem.findall("vehicle"):
            lane=v.get("lane","")
            edge=lane.rsplit("_",1)[0]
            if edge.startswith(":") or edge not in valid_edges:
                internal_count+=1;continue
            vid=v.get("id")
            tracks[vid].append((t,edge))
            observed_bins[(edge,int(t//args.bin_seconds))].add(vid)
            sample_count+=1
        elem.clear()
    actual=collections.defaultdict(list)
    for vid,points in tracks.items():
        previous=None
        for t,e in points:
            if previous!=e:actual[(vid,e)].append(t)
            previous=e
    pairs=[];missing=0;repeated=0
    for r in prediction:
        key=(r["vehicle"],r["edge"])
        if len(actual[key])!=1:
            if not actual[key]:missing+=1
            else:repeated+=1
            continue
        pairs.append((float(r["predicted_entry_s"]),actual[key][0],r["edge"]))
    errors=[obs-pred for pred,obs,_ in pairs]
    predicted_occ={(r["edge"],int(r["time_bin"])):int(r["predicted_vehicle_count"]) for r in csv.DictReader(open(args.predicted_occupancy))}
    keys=set(predicted_occ)|set(observed_bins)
    occupancy_errors=[len(observed_bins[k])-predicted_occ.get(k,0) for k in keys]
    with open(args.edge_comparison,"w",newline="") as f:
        w=csv.writer(f);w.writerow(["edge","time_bin","predicted_count","observed_unique_vehicle_samples","difference"])
        for k in sorted(keys):
            o=len(observed_bins[k]);p=predicted_occ.get(k,0)
            w.writerow([k[0],k[1],p,o,o-p])
    report={"prediction_records":len(prediction),"matched_unique_vehicle_edges":len(pairs),
            "missing_vehicle_edges":missing,"ambiguous_repeated_edges":repeated,
            "fcd_valid_samples":sample_count,"fcd_excluded_internal_or_unknown_samples":internal_count,
            "edge_entry_bias_s":statistics.mean(errors) if errors else None,
            "edge_entry_mae_s":statistics.mean(map(abs,errors)) if errors else None,
            "edge_entry_rmse_s":math.sqrt(statistics.mean(e*e for e in errors)) if errors else None,
            "edge_entry_abs_p95_s":percentile([abs(e) for e in errors],.95),
            "occupancy_bin_count":len(keys),"occupancy_count_mae":statistics.mean(map(abs,occupancy_errors)) if keys else None,
            "limitations":["FCD first observed timestep approximates entry, resolution 1 second","FCD internal lanes excluded","occupancy comparison uses distinct vehicle samples per bin, not instantaneous occupancy or vehicle-seconds","prediction is free-flow traversal replay of chosen routes, not original search candidate congestion cost","repeated visits to same edge excluded from entry error","unmatched observations not silently interpreted as zero","no counterfactual route outcome measured"]}
    with open(args.report,"w") as f:json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))
    if len(prediction)==0 or len(pairs)==0:raise RuntimeError("No comparable edge traversals")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("mode",choices=["predict","compare"])
    p.add_argument("--net");p.add_argument("--routes");p.add_argument("--fcd")
    p.add_argument("--predictions",default="results/forecasts.csv")
    p.add_argument("--predicted-occupancy",default="results/forecast-occupancy.csv")
    p.add_argument("--edge-comparison",default="results/edge-bin-comparison.csv")
    p.add_argument("--report",default="results/accuracy-report.json")
    p.add_argument("--bin-seconds",type=int,default=30)
    a=p.parse_args()
    if a.bin_seconds<=0:raise ValueError("bin_seconds must be positive")
    (write_predictions if a.mode=="predict" else compare)(a)
if __name__=="__main__":main()
