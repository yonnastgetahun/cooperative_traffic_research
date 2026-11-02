#!/usr/bin/env python3
"""Bounded, read-only-input six-run Experiment 007 physical mechanism replay.

Original scenario files from original GitHub Actions run 41380998833.
No routing or demand regeneration; use pinned SUMO 1.28.0 image.
Tasks: preflight, replay, aggregate.
"""
import argparse
import collections
import csv
import gzip
import hashlib
import json
import math
import os
import pathlib
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

P = pathlib.Path
ARMS = {
    4101: ("I", "probe2"),
    4102: ("I", "probe0", "probe1", "bundle")
}
ROUTE_SHA = {
    (4101, "I"): "da86fc7b2311fc118d0735e7bf87f6b640eaac79bc6d80b69574722e3b78f57a",
    (4101, "probe2"): "13b9da58162f1df38001b4ffb14de3678237dc1d54098ef52d5db1c571a83013",
    (4102, "I"): "5b669a1b8132fcb5f8e184faa66bf77d76c74d93a014582aceb0484c350747ac",
    (4102, "probe0"): "8e6bcafa2c9059eefd6558222308df1e86a8b886b1ce98d39561304465b83b0f",
    (4102, "probe1"): "5e4cd19bd8e85c7d852e135a569d5678f2ea412bc0144ed28fa8962702c02470",
    (4102, "bundle"): "df349601d418b83b05d3aa0776bee1f6e23d3101ef92771a385a45fed6df32b3",
}
NETWORK_SHA = {
    4101: "7e5bb888a87bf9b7e52034275a5a848f7b6b319957f452a1d64bd54b93f01d52",
    4102: "5961868f82c6831d3d3d89f2fb22d1807cc47db9d5e6adaef11cd67e4ac76e7c",
}
TRIPS_SHA = {
    4101: "66ab35c2ef7bb2aad10aba191012e8ce54b15470c07cf62ab4079966b7a7a130",
    4102: "15a47acfbb090c8bb5d469735127c151fe8cf4c7f6f5e1963c9269859e92d895",
}
EXPECTED_CHANGE = {
    (4101, "I"): set(), (4101, "probe2"): {"veh0000"},
    (4102, "I"): set(), (4102, "probe0"): {"veh0582"},
    (4102, "probe1"): {"veh0158"}, (4102, "bundle"): {"veh0582", "veh0158"}
}
G2_FIELDS = ("depart", "arrival", "duration", "departDelay", "waitingTime", "timeLoss")
SAFETY_FIELDS = ("collisions", "emergencyStops", "emergencyBraking")
ROOT_RUN = 41380998833

def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def xml(path):
    return ET.parse(path).getroot()

def orig_routes(p):
    result = {}
    for v in xml(p).findall("vehicle"):
        r=v.find("route")
        assert r is not None
        result[v.get("id")] = tuple(r.get("edges").split())
    assert len(result) == 1000
    return result

def trip_fields(p):
    result = {}
    for v in xml(p).findall("tripinfo"):
        result[v.get("id")] = {k: float(v.get(k)) for k in G2_FIELDS}
    assert len(result) == 1000
    return result

def assert_orig(folder, seed):
    folder=P(folder)
    assert seed in ARMS
    assert digest(folder/"network.net.xml") == NETWORK_SHA[seed], "network SHA mismatch"
    assert digest(folder/"trips.xml") == TRIPS_SHA[seed], "demand SHA mismatch"
    attempt=json.loads((folder/"attempt.json").read_text())
    assert attempt["status"]=="COMPLETE" and int(attempt["seed"])==seed and int(attempt["n_runs"])==6
    files=[p for p in folder.rglob("*") if p.is_file()]
    assert len(files)==43, "original archive member count mismatch"
    ids=[v.get("id") for v in xml(folder/"trips.xml").findall("trip")]
    assert len(ids)==len(set(ids))==1000
    fixed={v.get("id"): (v.get("depart"),v.get("from"),v.get("to"))
        for v in xml(folder/"trips.xml").findall("trip")}
    assert all(v[0] is not None and v[1] and v[2] for v in fixed.values())
    base=orig_routes(folder/"I/routes.rou.xml")
    assert set(base)==set(ids)
    for arm in ARMS[seed]:
        routes=folder/arm/"routes.rou.xml"
        assert digest(routes)==ROUTE_SHA[(seed,arm)], "historical route SHA mismatch"
        alt=orig_routes(routes)
        assert set(alt)==set(base)
        changed={v for v in base if base[v]!=alt[v]}
        assert changed==EXPECTED_CHANGE[(seed,arm)], "route-changed cohort mismatch"
        original=trip_fields(folder/arm/"tripinfo.xml")
        assert set(original)==set(ids)
    return {"seed":seed,"original_files":43,
            "network_sha256":NETWORK_SHA[seed],"demand_sha256":TRIPS_SHA[seed],
            "selected_arms":list(ARMS[seed])}

def version_preflight():
    out=subprocess.check_output(["sumo","--version"],text=True)
    if "1.28.0" not in out:
        raise RuntimeError("Pinned SUMO version mismatch: "+out[:400])
    helpout=subprocess.check_output(["sumo","--help"],text=True)
    flags=("--fcd-output","--vehroute-output","--vehroute-output.exit-times","--additional-files",
           "--tripinfo-output","--collision-output","--statistic-output")
    missing=[flag for flag in flags if flag not in helpout]
    if missing:raise RuntimeError("Pinned SUMO missing mandatory flags: "+str(missing))
    add=ET.fromstring('<additional><edgeData id="exp007-edge" file="a.xml" period="5" withInternal="true" excludeEmpty="false"/><laneData id="exp007-lane" file="b.xml" period="5" withInternal="true" excludeEmpty="false"/></additional>')
    assert [x.tag for x in add]==["edgeData","laneData"]
    assert all(x.get("period")=="5" and x.get("withInternal")=="true" for x in add)
    return {"sumo_version":out.splitlines()[0],"required_cli_flags":list(flags),
            "detectors":"edgeData+laneData, 5-second period, internal lanes/edges, well-formed XML"}

def preflight(root,out):
    result={"status":"FAILED","phase":"G0/G1"}
    try:
        original={}
        for seed in ARMS:
            original[str(seed)]=assert_orig(P(root)/("exp007-probe-%d"%seed),seed)
        result.update(status="PASS",historical_inputs=original,pinned_options=version_preflight())
    except Exception as e:
        result["error"]=str(e)
    P(out).parent.mkdir(parents=True,exist_ok=True)
    P(out).write_text(json.dumps(result,indent=2)+"\n")
    if result["status"]!="PASS":raise RuntimeError(result.get("error"))
    print(json.dumps(result,indent=2))

def safe_number(x):
    return float(x) if x is not None else None

def check_g2(old,new,old_stats,new_stats,old_col,new_col):
    oldr=trip_fields(old); newr=trip_fields(new)
    if set(oldr)!=set(newr):
        raise RuntimeError("G2 failed: matched identity mismatch")
    max_field={}
    for k in G2_FIELDS:
        max_field[k]=max(abs(oldr[vid][k]-newr[vid][k]) for vid in oldr)
        if max_field[k]>0.02000001:
            raise RuntimeError("G2 historical per-driver %s mismatch: %r"%(k,max_field[k]))
    before=xml(old_stats).find("safety")
    after=xml(new_stats).find("safety")
    if before is None or after is None:
        raise RuntimeError("G2 safety statistics absent")
    for k in SAFETY_FIELDS:
        if before.get(k)!=after.get(k):
            raise RuntimeError("G2 field %s differs: %s / %s"%(k,before.get(k),after.get(k)))
    if len(xml(old_col).findall(".//collision"))!=len(xml(new_col).findall(".//collision")):
        raise RuntimeError("G2 collision file event count mismatch")
    return {"matching_trips":len(oldr),"max_absolute_error_by_field_s":max_field,
            "recorded_safety":{k:after.get(k) for k in SAFETY_FIELDS},
            "network_elapsed_s":sum(v["arrival"]-v["depart"]+v["departDelay"] for v in newr.values()),
            "original_network_elapsed_s":sum(v["arrival"]-v["depart"]+v["departDelay"] for v in oldr.values())}

def make_additional(out):
    root=ET.Element("additional")
    ET.SubElement(root,"edgeData",id="exp007-edge",
                  file=str((out/"edgedata.xml.gz").resolve()),period="5",
                  withInternal="true",excludeEmpty="false")
    ET.SubElement(root,"laneData",id="exp007-lane",
                  file=str((out/"lanedata.xml.gz").resolve()),period="5",
                  withInternal="true",excludeEmpty="false")
    p=out/"instrumentation.add.xml"
    ET.ElementTree(root).write(p,encoding="utf-8",xml_declaration=True)
    return p

def replay(source,seed,arm,out):
    if (seed,arm) not in ROUTE_SHA:raise ValueError("Not a frozen six-run arm")
    source=P(source).resolve();out=P(out).resolve()
    out.mkdir(parents=True,exist_ok=False)
    result={"seed":seed,"arm":arm,"status":"FAILED","gate":"G0",
            "original_run":ROOT_RUN,"original_route_sha256":ROUTE_SHA[(seed,arm)]}
    try:
        assert_orig(source,seed)
        result["gate"]="G1"
        result["pinned_version"]=version_preflight()
        add=make_additional(out)
        command=["sumo","-n",str(source/"network.net.xml"),"-r",str(source/arm/"routes.rou.xml"),
                 "--tripinfo-output",str(out/"tripinfo.xml"),
                 "--statistic-output",str(out/"statistics.xml"),
                 "--collision-output",str(out/"collisions.xml"),
                 "--seed",str(seed),"--no-step-log","true","--log",str(out/"sumo.log"),
                 "--fcd-output",str(out/"fcd.xml.gz"),
                 "--vehroute-output",str(out/"vehroute.xml.gz"),
                 "--vehroute-output.exit-times","true",
                 "--additional-files",str(add)]
        (out/"command.json").write_text(json.dumps(command,indent=2)+"\n")
        result["gate"]="G2"
        with (out/"sumo-stage.log").open("w") as f:
            run=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT)
        if run.returncode:
            raise RuntimeError("SUMO exit code %d; inspect original stage log"%run.returncode)
        result["g2"]=check_g2(source/arm/"tripinfo.xml",out/"tripinfo.xml",
          source/arm/"statistics.xml",out/"statistics.xml",
          source/arm/"collisions.xml",out/"collisions.xml")
        for name in ("fcd.xml.gz","vehroute.xml.gz","edgedata.xml.gz","lanedata.xml.gz"):
            p=out/name
            if not p.exists() or p.stat().st_size<150:
                raise RuntimeError("G3 missing mandatory output "+name)
        result["gate"]="G3"
        # Pass G3 only after consolidated audit, where full paired outputs are available.
        result["status"]="G2_PASS_PENDING_G3"
        result["sha256"]={p.name:digest(p) for p in out.iterdir() if p.is_file()}
    except Exception as e:
        result["error"]=repr(e)
    (out/"attempt.json").write_text(json.dumps(result,indent=2)+"\n")
    if result["status"]!="G2_PASS_PENDING_G3":
        raise RuntimeError(result.get("error","Replay failed"))
    print(json.dumps({"seed":seed,"arm":arm,"status":result["status"],
                      "max_errors":result["g2"]["max_absolute_error_by_field_s"]}))

def open_xml(p):
    if p.suffix==".gz":return gzip.open(p,"rb")
    return open(p,"rb")

def stream_fcd(p):
    seen=set();counts=collections.Counter();first=None;last=None;lastt=-1
    near=collections.Counter()
    with open_xml(p) as f:
        for _,node in ET.iterparse(f,events=("end",)):
            if node.tag=="timestep":
                t=float(node.get("time"));assert t>=lastt
                lastt=t
                if first is None:first=t
                last=t
                for v in node.findall("vehicle"):
                    vid=v.get("id")
                    if vid is None or v.get("lane") is None or v.get("pos") is None or v.get("speed") is None:
                        raise RuntimeError("G3 missing FCD identity/lane/position/speed")
                    seen.add(vid)
                    counts[(int(t//5)*5,v.get("lane").rsplit("_",1)[0])]+=1
                    if float(v.get("speed"))<=.1:
                        near[(int(t//5)*5,v.get("lane").rsplit("_",1)[0])]+=1
                node.clear()
    if len(seen)!=1000 or first is None:
        raise RuntimeError("G3 incomplete FCD ID coverage")
    return {"vehicles":len(seen),"first":first,"last":last,
            "samples":sum(counts.values()),"near_stop_samples":sum(near.values()),
            "count5":counts,"near5":near}

def intervals(p,kind):
    values=collections.defaultdict(dict)
    first=None;last=None;entries=0
    with open_xml(p) as f:
        for _,node in ET.iterparse(f,events=("end",)):
            if node.tag=="interval":
                b=float(node.get("begin"));e=float(node.get("end"))
                if e<=b:raise RuntimeError("G3 malformed detector interval")
                if first is None or b<first:first=b
                if last is None or e>last:last=e
                for item in node:
                    if item.tag not in ("edge","lane"):continue
                    edge_id=item.get("id")
                    if edge_id is None:continue
                    values[(round(b,3),edge_id)]={
                       "speed":safe_number(item.get("speed")),
                       "waitingTime":safe_number(item.get("waitingTime")),
                       "occupancy":safe_number(item.get("occupancy")),
                       "sampledSeconds":safe_number(item.get("sampledSeconds")),
                       "entered":safe_number(item.get("entered")),
                       "left":safe_number(item.get("left"))}
                    entries+=1
                node.clear()
    if not entries or first is None:raise RuntimeError("G3 detector produced no interval data")
    return {"first":first,"last":last,"n":entries,"data":values}

def route_coverage(p):
    with open_xml(p) as f:
        root=ET.parse(f).getroot()
    vs=root.findall("vehicle")
    if len(vs)!=1000:raise RuntimeError("G3 vehroute IDs incomplete")
    seen=set()
    for v in vs:
        vid=v.get("id")
        if vid in seen:raise RuntimeError("G3 duplicate vehroute ID")
        seen.add(vid)
        x=v.find("route")
        if x is None or not x.get("edges"):raise RuntimeError("G3 missing route edges")
        if not x.get("exitTimes"):raise RuntimeError("G3 missing exitTimes")
    return len(seen)

def analyse(source,root,out):
    root=P(root);source=P(source);out=P(out);out.mkdir(parents=True,exist_ok=True)
    expected=[(4101,"I"),(4101,"probe2"),(4102,"I"),(4102,"probe0"),(4102,"probe1"),(4102,"bundle")]
    summary={"study":"post-exp007-six-run-observational-replay",
             "historical_test_a":"NO-GO; 8/20 directional agreement","test_b":"NOT_RUN",
             "status":"INVALID","gate":"G2","six_arms":[],"contrasts":{}}
    rows=[];observed={};detectors={};fcdstats={}
    try:
        for seed,arm in expected:
            p=root/("replay-%d-%s"%(seed,arm))
            result=json.loads((p/"attempt.json").read_text())
            if result.get("status")!="G2_PASS_PENDING_G3":
                raise RuntimeError("G2 failed for %d %s: %s"%(seed,arm,result.get("error")))
            # Independent readback of the original against instrumented output.
            audited=check_g2(source/("exp007-probe-%d"%seed)/arm/"tripinfo.xml",
                             p/"tripinfo.xml",
                             source/("exp007-probe-%d"%seed)/arm/"statistics.xml",
                             p/"statistics.xml",
                             source/("exp007-probe-%d"%seed)/arm/"collisions.xml",
                             p/"collisions.xml")
            observed[(seed,arm)]=audited["network_elapsed_s"]
            f=stream_fcd(p/"fcd.xml.gz")
            e=intervals(p/"edgedata.xml.gz","edge")
            l=intervals(p/"lanedata.xml.gz","lane")
            nr=route_coverage(p/"vehroute.xml.gz")
            # Each detector covers entire simulation until the end of observed FCD.
            if e["last"]<f["last"]-5 or l["last"]<f["last"]-5:
                raise RuntimeError("G3 insufficient edge/lane temporal coverage")
            if nr!=1000:raise RuntimeError("G3 vehroute incompleteness")
            detectors[(seed,arm)]=e
            fcdstats[(seed,arm)]=f
            rows.append({"seed":seed,"arm":arm,"G2":"PASS","G3":"PASS",
                         "max_field_error_s":max(audited["max_absolute_error_by_field_s"].values()),
                         "vehicles":1000,"FCD_samples":f["samples"],
                         "FCD_near_stop_samples":f["near_stop_samples"],
                         "edgedata_records":e["n"],"lanedata_records":l["n"],
                         "end_fcd_s":f["last"]})
        def contrast(seed,arm):
            return observed[(seed,arm)]-observed[(seed,"I")]
        for seed,arm in expected:
            if arm!="I":summary["contrasts"]["%d_%s"%(seed,arm)] = contrast(seed,arm)
        J=contrast(4102,"bundle")-contrast(4102,"probe0")-contrast(4102,"probe1")
        summary["contrasts"]["4102_bundle_interaction"]=J
        # Original total network-seconds contrasts (not externality):
        original={ (4101,"probe2"):3177.,(4102,"probe0"):2626.,
                   (4102,"probe1"):3935.,(4102,"bundle"):3572.}
        for key,want in original.items():
            if abs(contrast(*key)-want)>.02000001:
                raise RuntimeError("G2 network total mismatch for %r"%str(key))
        if abs(J-(-2989.))>.02000001:
            raise RuntimeError("G2 bundle interaction mismatch")
        differences=[]
        for seed,arm in expected:
            if arm=="I":continue
            current=detectors[(seed,arm)]["data"]
            baseline=detectors[(seed,"I")]["data"]
            for key in set(current)|set(baseline):
                a=current.get(key,{})
                b=baseline.get(key,{})
                wa=a.get("waitingTime")
                wb=b.get("waitingTime")
                if wa is None or wb is None:continue
                differences.append({"seed":seed,"arm":arm,"start_s":key[0],"edge":key[1],
                                    "delta_waiting_s":wa-wb})
        differences.sort(key=lambda x:(abs(x["delta_waiting_s"]),x["seed"]),reverse=True)
        with (out/"edge_time_waiting_differences.csv").open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=["seed","arm","start_s","edge","delta_waiting_s"])
            w.writeheader();w.writerows(differences)
        summary.update(status="VALID_EXPLORATORY",gate="G3",six_arms=rows,
           top_absolute_edge_waiting_differences=differences[:30],
           caution="Observed edge-time waiting differences are descriptive, not uniquely causal mediation of total travel time.")
    except Exception as exc:
        summary["error"]=repr(exc)
    with (out/"replay-scientific-summary.json").open("w") as f:
        json.dump(summary,f,indent=2)
    with (out/"replay-coverage.csv").open("w",newline="") as f:
        cols=["seed","arm","G2","G3","max_field_error_s","vehicles","FCD_samples",
              "FCD_near_stop_samples","edgedata_records","lanedata_records","end_fcd_s"]
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
    print(json.dumps(summary,indent=2)[:12000])
    if summary["status"]!="VALID_EXPLORATORY":raise RuntimeError(summary.get("error","Invalid run"))

def main():
    a=argparse.ArgumentParser()
    a.add_argument("action",choices=("preflight","replay","aggregate"))
    a.add_argument("--root")
    a.add_argument("--source")
    a.add_argument("--out",required=True)
    a.add_argument("--seed",type=int)
    a.add_argument("--arm")
    args=a.parse_args()
    if args.action=="preflight":preflight(args.root,args.out)
    elif args.action=="replay":replay(args.source,args.seed,args.arm,args.out)
    else:analyse(args.source,args.root,args.out)
if __name__=="__main__":
    main()
