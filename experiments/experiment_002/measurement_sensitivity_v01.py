#!/usr/bin/env python3
"""M2 offline FCD sensitivity: 1/2/5-second sampling and 10/30/60s bins.

Reweights actual 1-second SUMO FCD positions, not a new traffic simulation.
This checks measurement stability; it does not estimate native occupancy percent.
"""
import argparse, collections, csv, json, math, statistics, xml.etree.ElementTree as ET

def export(args):
    samples=[]
    previous=None; gaps=[]
    for _,node in ET.iterparse(args.fcd,events=("end",)):
        if node.tag!="timestep":continue
        t=float(node.get("time"))
        if previous is not None:gaps.append(round(t-previous,6))
        previous=t
        for v in node.findall("vehicle"):
            lane=v.get("lane","")
            if not lane:continue
            e=lane.rsplit("_",1)[0]
            kind="internal" if lane.startswith(":") else "external"
            samples.append((t,v.get("id"),e,kind))
        node.clear()
    if not samples:raise RuntimeError("FCD contained no vehicle samples")
    if any(abs(g-1)>1e-8 for g in gaps):
        raise RuntimeError("Sensitivity requires complete 1-second SUMO output")
    max_t=max(t for t,vid,e,k in samples)
    rows=[];details={}
    for width in [10,30,60]:
        baseline=collections.Counter()
        for t,vid,e,kind in samples:
            baseline[(e,int(t//width),kind)]+=1.
        for stride in [1,2,5]:
            sampled=collections.Counter()
            distinct=collections.defaultdict(set)
            for t,vid,e,kind in samples:
                if int(round(t))%stride:continue
                b=int(t//width)
                sampled[(e,b,kind)]+=min(float(stride),(b+1)*width-t)
                distinct[vid].add(e)
            keys=set(baseline)|set(sampled)
            errors=[sampled.get(k,0)-baseline.get(k,0) for k in keys]
            abs_errors=[abs(x) for x in errors]
            total_baseline=sum(baseline.values())
            total_sampled=sum(sampled.values())
            counts=[len(v) for v in distinct.values()]
            rows.append([width,stride,len(keys),len(distinct),
                round(statistics.mean(abs_errors),6),
                round(max(abs_errors),6),round(sum(errors),4),
                round(total_baseline,4),round(total_sampled,4),
                round(sum(v for (e,b,k),v in sampled.items() if k=="internal"),4)])
    with open(args.output,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["bin_seconds","FCD_thinning_seconds","edge_bins",
            "vehicles_seen","fcd_vehiclesec_MAE_vs_one_sec",
            "max_absolute_vehiclesec_bin_error","signed_total_vehiclesec_delta",
            "one_sec_total_vehiclesec","thinned_total_vehiclesec",
            "thinned_internal_vehiclesec"])
        w.writerows(rows)
    with open(args.report,"w") as f:
        json.dump({"status":"measurement_sensitivity_not_new_simulation",
          "one_sec_timesteps_verified":True,
          "run_id":"same_frozen_chosen_routes",
          "sampling_periods_seconds":[1,2,5],"time_bins_seconds":[10,30,60],
          "table":dict(zip(["rows"],[len(rows)])),
          "important_limit":"FCD values are reweighted discrete position samples. Native edgeData occupancy has different semantics; no interpolation of missing junction states is assumed."},f,indent=2)
    print("Sensitivity rows",len(rows))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for a in ("fcd","output","report"):p.add_argument("--"+a,required=True)
    export(p.parse_args())
