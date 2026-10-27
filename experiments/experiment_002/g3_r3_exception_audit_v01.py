#!/usr/bin/env python3
"""R3 development-only audit of explicit SUMO incidents and native missingness.

Never infer no teleports from trip completion alone or convert absent native
speed/occupancy to zero. Source is the ORIGINAL archived chosen-route run.
"""
import argparse,collections,csv,json,math,xml.etree.ElementTree as ET

def trips_from_routes(path):
    root=ET.parse(path).getroot();out={}
    for v in root.findall("vehicle"):
        vid=v.get("id");route=v.find("route")
        if not vid or vid in out or route is None:raise RuntimeError("Duplicate/missing vehicle/route")
        out[vid]=(float(v.get("depart")),route.get("edges","").split())
    return out

def tripinfos(path):
    out={}
    for _,e in ET.iterparse(path,events=("end",)):
        if e.tag!="tripinfo":continue
        vid=e.get("id")
        if not vid or vid in out:raise RuntimeError("Duplicate/missing tripinfo ID")
        dep=float(e.get("depart"));arr=float(e.get("arrival"))
        if not math.isfinite(dep) or not math.isfinite(arr) or arr<dep:
            raise RuntimeError("Invalid trip duration")
        out[vid]=(dep,arr)
        e.clear()
    return out

def statistic_report(path):
    root=ET.parse(path).getroot()
    tp=root.find("teleports");vehicles=root.find("vehicles");safety=root.find("safety")
    if tp is None or tp.get("total") is None:
        state="UNKNOWN_NOT_CAPTURED";n=None
    else:
        n=int(tp.get("total"))
        if n<0:raise RuntimeError("Invalid native teleport count")
        state="ZERO_CONFIRMED" if n==0 else "NONZERO_CONFIRMED"
    return dict(teleport_state=state,teleports_total=n,
        teleports_breakdown=(dict(tp.attrib) if tp is not None else {}),
        vehicles=(dict(vehicles.attrib) if vehicles is not None else None),
        safety=(dict(safety.attrib) if safety is not None else None))

def fcd_report(path,trips):
    previous=None;steps=0;invalid=collections.Counter()
    vehicle_times=collections.defaultdict(list)
    for _,e in ET.iterparse(path,events=("end",)):
        if e.tag!="timestep":continue
        t=float(e.get("time"));steps+=1
        if previous is not None and abs((t-previous)-1.0)>1e-7:
            invalid["FCD_GAP_OR_OUT_OF_ORDER_STEP"]+=1
        previous=t;present=set()
        for v in e.findall("vehicle"):
            vid=v.get("id");lane=v.get("lane","")
            if not vid or vid in present:invalid["FCD_DUPLICATE_OR_MISSING_VEHICLE_ID"]+=1
            present.add(vid)
            if not lane:invalid["MISSING_FCD_LANE"]+=1
            if vid not in trips:invalid["UNEXPECTED_FCD_VEHICLE_ID"]+=1
            vehicle_times[vid].append(t)
        e.clear()
    unexplained=[]
    for vid,arr in vehicle_times.items():
        if any(arr[i+1]-arr[i]>1.000001 for i in range(len(arr)-1)):
            unexplained.append(vid)
    if steps==0:invalid["FCD_EMPTY"]+=1
    return dict(timestep_count=steps,distinct_observed_vehicles=len(vehicle_times),
        structural_anomalies=dict(invalid),
        vehicles_with_within_trip_disappearance=unexplained[:50],
        within_trip_disappearance_count=len(unexplained))

def edge_bins(path,expected_width=30):
    states=collections.Counter();intervals=set();edge_pairs=set()
    missing_required=[];zero_with_observed_values=0
    for _,node in ET.iterparse(path,events=("end",)):
        if node.tag!="interval":continue
        start=float(node.get("begin"));end=float(node.get("end"))
        if not all(map(math.isfinite,(start,end))) or end<=start:
            raise RuntimeError("Invalid native aggregation interval")
        if (start,end) in intervals:raise RuntimeError("Duplicate native interval")
        intervals.add((start,end))
        width=end-start
        category="FULL_30_SECOND_BIN" if abs(width-expected_width)<1e-6 else "PARTIAL_NATIVE_BIN"
        for edge in node.findall("edge"):
            eid=edge.get("id")
            key=(eid,start,end)
            if key in edge_pairs:raise RuntimeError("Duplicate native edge/time bin")
            edge_pairs.add(key);states[category]+=1
            sample=edge.get("sampledSeconds")
            if sample is None:
                states["MISSING_NATIVE_SAMPLED_SECONDS"]+=1
                missing_required.append(key)
                continue
            val=float(sample)
            if not math.isfinite(val) or val<0:raise RuntimeError("Negative/nonfinite native sample")
            if val==0:
                states["DISPLAYED_ZERO_SAMPLED_SECONDS"]+=1
                if edge.get("speed") is None and edge.get("occupancy") is None:
                    states["EMPTY_NATIVE_EDGE_NO_SAMPLES"]+=1
                if any(edge.get(x) is not None for x in ("speed","occupancy")):
                    zero_with_observed_values+=1
            else:
                states["POSITIVE_NATIVE_SAMPLE_SECONDS"]+=1
                for name in ("speed","occupancy","density","waitingTime"):
                    if edge.get(name) is None:
                        states["MISSING_NATIVE_METRIC_WITH_POSITIVE_SAMPLES"]+=1
                        missing_required.append((eid,start,end,name))
        node.clear()
    if not intervals or not edge_pairs:raise RuntimeError("No native edgeData")
    return dict(native_bins=len(edge_pairs),native_intervals=len(intervals),
                status_counts=dict(states),missing_required_first20=missing_required[:20],
                zero_sample_bins_with_other_values=zero_with_observed_values)

def audit(a):
    original=trips_from_routes(a.routes)
    trip=tripinfos(a.tripinfo)
    replay=tripinfos(a.replay_tripinfo)
    if len(original)!=1000 or len(trip)!=1000 or len(replay)!=1000:
        raise RuntimeError("Expected 1000 planned and completed trip records")
    if set(original)!=set(trip) or set(trip)!=set(replay):
        raise RuntimeError("Planned/completed/replay vehicle populations differ")
    for vid in trip:
        if trip[vid]!=replay[vid]:raise RuntimeError("Observation changed trip outcome "+vid)
    stat=statistic_report(a.statistics)
    fcd=fcd_report(a.fcd,trip)
    native=edge_bins(a.native)
    exception=collections.Counter()
    if stat["teleport_state"]=="UNKNOWN_NOT_CAPTURED":exception["UNKNOWN_TELEPORT_COVERAGE"]+=1
    if stat["teleport_state"]=="NONZERO_CONFIRMED":exception["EXPLICIT_TELEPORT"]+=stat["teleports_total"]
    exception.update(fcd["structural_anomalies"])
    if fcd["within_trip_disappearance_count"]:
        exception["WITHIN_TRIP_FCD_DISAPPEARANCE"]+=fcd["within_trip_disappearance_count"]
    for k in ("MISSING_NATIVE_SAMPLED_SECONDS","MISSING_NATIVE_METRIC_WITH_POSITIVE_SAMPLES"):
        if native["status_counts"].get(k):exception[k]+=native["status_counts"][k]
    result=dict(status="R3_DEVELOPMENT_OBSERVATION_POLICY_APPLIED",
        seed=a.seed,window_seconds=a.window,
        matched_trip_count=1000,route_population_invariant=True,tripinfo_invariant=True,
        reported_teleports=stat,reported_FCD=fcd,native_edge_bins=native,
        scientific_exception_counts=dict(exception),
        exception_gate=("PASS_FOR_THIS_REPLAY" if not exception else "OPEN_INVESTIGATION"),
        missing_policy="absent optional native values are NOT zero; zero sampledSeconds may be rounded; teleports require explicit statistic",
        claims_blocked=["real-world safety","causal intersection delay","physical occupancy prediction by route assignment counter"])
    with open(a.report,"w") as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ("reported_FCD","native_edge_bins")},indent=2))
    if any(k in exception for k in ("FCD_GAP_OR_OUT_OF_ORDER_STEP","FCD_DUPLICATE_OR_MISSING_VEHICLE_ID","MISSING_FCD_LANE","MISSING_NATIVE_SAMPLED_SECONDS")):
        raise RuntimeError("Critical R3 source integrity exception")
    if stat["teleport_state"]=="UNKNOWN_NOT_CAPTURED":
        raise RuntimeError("Native SUMO teleport status was not observed")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("routes","tripinfo","replay-tripinfo","statistics","fcd","native","report"):
        p.add_argument("--"+name,required=True)
    p.add_argument("--seed",type=int,required=True)
    p.add_argument("--window",type=int,required=True)
    a=p.parse_args()
    if a.seed!=2101 or a.window not in (200,600,1200):
        raise RuntimeError("R3 only authorized for prespecified development seed 2101")
    audit(a)
