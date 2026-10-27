#!/usr/bin/env python3
"""Experiment 002 M0/M1: physically interpretable FCD and SUMO edgeData diagnostics.

All metrics are observational, not counterfactual. External-edge FCD samples
are approximate vehicle-seconds; native edgeData sampledSeconds is an independent
SUMO measurement. Decision prior-assigned counts are NEVER physical occupancy.
"""
import argparse, collections, csv, json, math, statistics, xml.etree.ElementTree as ET

def edge_id(lane):
    if not lane:
        return None, "missing"
    if lane.startswith(":"):
        return lane.rsplit("_", 1)[0], "internal"
    if "_" not in lane or not lane.rsplit("_", 1)[1].isdigit():
        return None, "invalid"
    return lane.rsplit("_", 1)[0], "external"

def bin_index(t, width):
    if t < 0 or width <= 0:
        raise ValueError("Nonnegative simulation time and positive bins required")
    return int(math.floor((t + 1e-10) / width))

def overlap_seconds(start, end, a, b):
    if end < start or b < a:
        raise ValueError("Reversed interval")
    return max(0., min(end, b) - max(start, a))

def write_csv(path, fields, records):
    with open(path, "w", newline="") as f:
        w=csv.writer(f);w.writerow(fields);w.writerows(records)

def read_fcd(path, width, stride=1):
    tracks=collections.defaultdict(list)
    bins=collections.defaultdict(lambda: [0.,0.,0.,0.])
    seen_times=set(); missing=collections.Counter()
    first=last=None; previous=None; gaps=collections.Counter()
    samples=0; internal=0; outside=0
    for _, node in ET.iterparse(path, events=("end",)):
        if node.tag != "timestep":continue
        t=float(node.attrib["time"])
        if previous is not None:
            if t <= previous:raise RuntimeError("FCD timesteps unordered or repeated")
            gaps[round(t-previous,6)]+=1
        previous=t
        if first is None:first=t
        last=t;seen_times.add(t)
        for v in node.findall("vehicle"):
            lane=v.get("lane","")
            e,kind=edge_id(lane)
            vid=v.get("id")
            if not vid or not e:
                missing[kind]+=1;continue
            try:speed=float(v.get("speed"))
            except (TypeError,ValueError):
                missing["no_speed"]+=1;continue
            pos=v.get("pos")
            if pos is None:missing["no_lane_position"]+=1
            tracks[vid].append((t,e,kind,lane,speed,float(pos) if pos else None))
            rec=bins[(e,bin_index(t,width),kind)]
            rec[0]+=stride
            if speed<0.1:rec[1]+=stride
            if speed<1.0:rec[2]+=stride
            rec[3]+=1
            samples+=1
            if kind=="internal":internal+=1
        node.clear()
    if first is None:raise RuntimeError("No FCD timesteps")
    cadence=min(gaps) if gaps else stride
    return tracks,bins,{"first_timestep_s":first,"last_timestep_s":last,
        "timestep_gap_counts":{str(k):v for k,v in sorted(gaps.items())},
        "minimum_observed_gap_s":cadence,"sample_weight_s":stride,
        "total_vehicle_samples":samples,"internal_vehicle_samples":internal,
        "excluded_samples":dict(missing),"sample_cadence_assumed_1s":stride==1}

def load_csv(path):
    with open(path, newline="") as f:return list(csv.DictReader(f))

def read_native(path, expected_internal):
    records={}
    intervals=set();duplicate=0;missing=collections.Counter();internal=0
    for _,node in ET.iterparse(path,events=("end",)):
        if node.tag!="interval":continue
        begin=float(node.attrib["begin"]);end=float(node.attrib["end"])
        if end<=begin:raise RuntimeError("Invalid native aggregation interval")
        intervals.add((begin,end))
        for edge in node:
            if edge.tag not in ("edge","lane"):continue
            eid=edge.attrib.get("id","")
            if edge.tag=="lane":eid=edge_id(eid)[0] or eid
            key=(eid,begin,end)
            if key in records:duplicate+=1;continue
            if eid.startswith(":"):internal+=1
            def numeric(name):
                v=edge.get(name)
                if v is None:missing[name]+=1;return None
                return float(v)
            records[key]={"sampledSeconds":numeric("sampledSeconds"),
                "occupancy":numeric("occupancy"),"density":numeric("density"),
                "waitingTime":numeric("waitingTime"),"speed":numeric("speed"),
                "entered":numeric("entered"),"left":numeric("left")}
        node.clear()
    if not records:raise RuntimeError("No native edgeData intervals")
    return records,{"interval_count":len(intervals),"record_count":len(records),
        "internal_edge_records":internal,"duplicate_native_keys":duplicate,
        "missing_native_metrics":dict(missing),"configured_with_internal":expected_internal}

def route_records(trace):
    by_veh=collections.defaultdict(list)
    for r in load_csv(trace):
        by_veh[r["vehicle"]].append(r)
    for vid,route in by_veh.items():
        route.sort(key=lambda r:int(r["route_index"]))
        if [int(r["route_index"]) for r in route] != list(range(len(route))):
            raise RuntimeError("Route index gap or duplicate: "+vid)
    return by_veh

def phase_segments(vid, rows, samples, trip):
    """Match ordered external-edge runs, retaining internal sample states.
    Consecutive duplicate planned edges with no distinguishable transition
    are flagged rather than guessed.
    """
    observed_runs=[]
    for sample in samples:
        t,e,kind,lane,speed,pos=sample
        if kind != "external":continue
        if not observed_runs or e != observed_runs[-1][0]:
            observed_runs.append([e,t])
    expected=[r["edge"] for r in rows]
    actual=[r[0] for r in observed_runs]
    if expected != actual:
        return [],{"vehicle":vid,"status":"unmatched_route","planned_edges":len(expected),
                   "observed_runs":len(actual),"expected":expected,"actual":actual}
    phases=[]
    for i,r in enumerate(rows):
        start=observed_runs[i][1]
        end=observed_runs[i+1][1] if i+1<len(rows) else trip["arrival"]
        if end<start:
            raise RuntimeError("Negative segment duration for "+vid)
        segment=[s for s in samples if start-1e-9<=s[0]<end-1e-9]
        ext=[s for s in segment if s[2]=="external" and s[1]==r["edge"]]
        internal=[s for s in segment if s[2]=="internal"]
        unexpected=[s for s in segment if s[2]=="external" and s[1]!=r["edge"]]
        if unexpected:
            raise RuntimeError("External observations inconsistent with ordered route: "+vid)
        external_s=len(ext)
        internal_s=len(internal)
        unresolved=max(0.,end-start-external_s-internal_s)
        oversampled=max(0.,external_s+internal_s-(end-start))
        phases.append([vid,i,r["edge"],round(start,4),round(end,4),
            round(end-start,4),external_s,internal_s,
            sum(s[4]<0.1 for s in ext),sum(s[4]<1.0 for s in ext),
            round(unresolved,4),round(oversampled,4),
            "|".join(dict.fromkeys(s[3] for s in internal)),
            "matched" if not oversampled else "sampling_overcoverage"])
    return phases,{"vehicle":vid,"status":"matched","planned_edges":len(expected),
                   "observed_runs":len(actual)}

def summarize(values):
    if not values:return {"n":0,"bias":None,"mae":None}
    return {"n":len(values),"bias":round(statistics.mean(values),6),
        "mae":round(statistics.mean(abs(v) for v in values),6),
        "max_abs":round(max(abs(v) for v in values),6)}

def analyze(a):
    by_veh=route_records(a.trace)
    trips={}
    for _,node in ET.iterparse(a.tripinfo,events=("end",)):
        if node.tag!="tripinfo":continue
        trips[node.get("id")]={"arrival":float(node.get("arrival")),
            "depart":float(node.get("depart")),"duration":float(node.get("duration")),
            "waiting":float(node.get("waitingTime",0))}
        node.clear()
    tracks,bins,meta=read_fcd(a.fcd,a.bin_seconds)
    external,exmeta=read_native(a.native_external,False)
    withint,inmeta=read_native(a.native_internal,True)
    proxy=[];phases=[];route_status=[];all_internal=0
    for vid,rows in sorted(by_veh.items()):
        for r in rows:
            count=int(r["prior_assigned_count"])
            cap=float(r["capacity_proxy"])
            proxy.append([vid,r["route_index"],r["edge"],r["lookup_time_bin"],
                count,cap,round(count/cap,8),r["freeflow_s"],
                r["congestion_surcharge_s"],r["junction_proxy_s"],
                "origin_not_searched" if int(r["route_index"])==0
                else "replayed_preassignment_chosen_path"])
        if vid not in trips:
            route_status.append({"vehicle":vid,"status":"missing_tripinfo"});continue
        p,status=phase_segments(vid,rows,tracks.get(vid,[]),trips[vid])
        phases.extend(p);route_status.append(status)
    write_csv(a.proxy,["vehicle","route_index","edge","queried_time_bin",
        "prior_route_assignment_count","model_capacity_proxy","normalized_model_proxy",
        "freeflow_s","congestion_surcharge_s","junction_proxy_s","method"],proxy)
    write_csv(a.phases,["vehicle","route_index","external_edge","first_sample_s",
        "next_first_sample_or_arrival_s","external_to_next_s","external_sample_s",
        "internal_sample_s","external_stop_under_0_1_s","external_stop_under_1_s",
        "unresolved_s","sample_overcoverage_s","internal_lanes","status"],phases)
    native_rows=[];native_err=[];missing_native=0;no_fcd=0
    for (eid,begin,end),rec in sorted(withint.items()):
        kind="internal" if eid.startswith(":") else "external"
        b=bin_index(begin,a.bin_seconds)
        # Native and FCD compare only when periods and bins truly align.
        aligned=abs(end-begin-a.bin_seconds)<1e-7 and abs(begin-b*a.bin_seconds)<1e-7
        fcd=bins.get((eid,b,kind),[0,0,0,0]) if aligned else [0,0,0,0]
        native_sec=rec["sampledSeconds"]
        err=(fcd[0]-native_sec) if native_sec is not None and aligned else None
        if err is not None:native_err.append(err)
        if native_sec is None:missing_native+=1
        if fcd[0]==0 and native_sec and native_sec>0:no_fcd+=1
        native_rows.append([eid,kind,begin,end,end-begin,
            round(fcd[0],5) if aligned else "",
            round(fcd[0]/(end-begin),6) if aligned else "",
            fcd[1] if aligned else "",fcd[2] if aligned else "",
            native_sec,rec["occupancy"],rec["density"],
            rec["waitingTime"],rec["speed"],
            round(err,5) if err is not None else "",
            "aligned" if aligned else "unmatched_bin"])
    write_csv(a.observed,["edge","edge_type","interval_begin_s","interval_end_s",
        "covered_s","fcd_vehicle_sample_seconds","fcd_mean_vehicles",
        "fcd_stopped_under_0_1_s","fcd_stopped_under_1_s",
        "native_sampledSeconds","native_occupancy_percent","native_density",
        "native_waitingTime","native_speed","fcd_minus_native_sampledSeconds",
        "bin_alignment"],native_rows)
    matched=sum(s["status"]=="matched" for s in route_status)
    mismatch=[s for s in route_status if s["status"]!="matched"]
    occupied=[p for p in phases if p[7]>0]
    report={"status":"measurement_development_not_validation",
        "expected_vehicles":a.vehicles,"planned_vehicles":len(by_veh),
        "completed_vehicles":len(trips),"matched_route_vehicles":matched,
        "unmatched_route_vehicles":len(mismatch),"unmatched_first20":mismatch[:20],
        "planned_edges":sum(len(x) for x in by_veh.values()),
        "matched_external_segments":len(phases),
        "internal_visible_segments":len(occupied),
        "observed_internal_sample_seconds":sum(p[7] for p in phases),
        "observed_external_stop_under_0_1_seconds":sum(p[8] for p in phases),
        "unresolved_transition_seconds":round(sum(p[10] for p in phases),3),
        "overcovered_segments":sum(p[11]>0 for p in phases),
        "native_FCD_sampledSeconds_difference":summarize(native_err),
        "native_records_missing_sampledSeconds":missing_native,
        "native_positive_without_FCD_samples":no_fcd,
        "external_edgeData":exmeta,"internal_edgeData":inmeta,"FCD":meta,
        "sample_bins":a.bin_seconds,
        "comparability_warning":"FCD sampling is approximate, native SUMO sampledSeconds and lane coverage may differ; model route count is not physical occupancy",
        "limitations":["Internal-link samples not guaranteed on every crossing",
            "Internal sampled time does not capture all approach delay",
            "Sampling gaps/partial bins are not hidden",
            "Route matching is by ordered external runs, not (vehicle,edge) keys",
            "No unchosen counterfactual or causal decomposition",
            "Simulation is synthetic; no real-road safety or improvement claim"]}
    with open(a.report,"w") as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in
        ("FCD","external_edgeData","internal_edgeData","limitations","unmatched_first20")},indent=2))
    if len(by_veh)!=a.vehicles or len(trips)!=a.vehicles:
        raise RuntimeError("Expected 1000 complete trips")
    if matched/len(by_veh)<.95:
        raise RuntimeError("Ordered-route coverage below 95%; investigate before calibration")
    if not native_err:
        raise RuntimeError("No alignable native/FCD sampledSeconds comparisons")
    if inmeta["internal_edge_records"]==0:
        raise RuntimeError("Native withInternal instrument produced no internal records")
    if meta["internal_vehicle_samples"]==0:
        raise RuntimeError("FCD produced no internal-lane samples")
    if any(float(k)!=1 for k in meta["timestep_gap_counts"]):
        raise RuntimeError("Unexpected FCD cadence; 1-second integration invalid")

def main():
    p=argparse.ArgumentParser()
    for name in ("fcd","native-external","native-internal","trace","tripinfo",
                 "report","observed","phases","proxy"):
        p.add_argument("--"+name,required=True)
    p.add_argument("--bin-seconds",type=int,default=30)
    p.add_argument("--vehicles",type=int,default=1000)
    a=p.parse_args()
    analyze(a)

if __name__=="__main__":main()
