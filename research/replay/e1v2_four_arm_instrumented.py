#!/usr/bin/env python3
"""E1-v2 D1 four-arm passive, source-locked, retrospective instrumented replay.

ONLY (6112,I),(6112,probe2),(6113,I),(6113,probe2). These historical cases were
selected after outcomes were known. No E1 prediction, route generator, novel
seed, independent validation or cooperative Test B is run by this program.

CLI:
 preflight --root original --ledger original-ledger/SHA256_PER_MEMBER.csv --out ...
 replay --root original --seed 6112 --arm I --out ...
 aggregate --root original --replays replays --out ...

Pinned container SUMO 1.28.0, GHCR sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb
"""
from __future__ import annotations
import argparse,collections,csv,gzip,hashlib,json,math,pathlib,statistics,subprocess,sys
import xml.etree.ElementTree as ET
from research.replay import exp007_instrumented_v01 as prior

P=pathlib.Path
SELECTION={6112:("I","probe2"),6113:("I","probe2")}
WHO={6112:"veh0142",6113:"veh0038"}
EXPECTED_TOTAL={6112:3219.0,6113:-3883.0}
EXPECTED_OTHERS={6112:3215.0,6113:-3960.0}
FIELDS=("depart","arrival","duration","departDelay","waitingTime","timeLoss")
IMAGE="ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb"
MAX_PER_ARM=512*1024*1024
MAX_FOUR=2*1024*1024*1024
SOURCE_RUN=41966516110
def sha(path):return prior.digest(path)
def getj(path):return json.loads(P(path).read_text())
def outj(path,d):
    p=P(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
def writecsv(path,rows,fields=None):
    p=P(path);p.parent.mkdir(parents=True,exist_ok=True)
    if fields is None:fields=list(rows[0]) if rows else []
    with p.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");w.writeheader();w.writerows(rows)
def scheduled(path):
    return {v.get("id"):float(v.get("depart")) for v in ET.parse(path).getroot().findall("trip")}
def routes(path):
    return {v.get("id"):tuple(v.find("route").get("edges").split())
            for v in ET.parse(path).getroot().findall("vehicle")}
def tripinfo(path):
    return {v.get("id"):{f:float(v.get(f)) for f in FIELDS if v.get(f) is not None}
            for v in ET.parse(path).getroot().findall("tripinfo")}
def origin(root,seed,arm):
    return P(root)/("seed-"+str(seed))/"observations"/arm
def assert_sources(root,full_ledger=None):
    root=P(root);summary={}
    if full_ledger is not None:
        members=[p for p in root.rglob("*") if p.is_file()]
        assert len(members)==695,("original source file count",len(members))
        known={p.relative_to(root).as_posix():p for p in members}
        with open(full_ledger,newline="") as f: rows=list(csv.DictReader(f))
        assert len(rows)==695 and set(known)=={r["member"] for r in rows}
        for record in rows:
            p=known[record["member"]]
            assert p.stat().st_size==int(record["bytes"]) and sha(p)==record["sha256"],record["member"]
    verdict=getj(root/"development-verdict.json")
    assert verdict["scientific_status"]=="DEVELOPMENT_NOT_QUALIFIED"
    assert verdict["new_validation"]=="NOT_STARTED" and verdict["Test_B"]=="NOT_RUN"
    locks=getj(root/"all-prediction-locks.json")
    assert locks["status"]=="FROZEN_BEFORE_ANY_SUMO_OUTCOME"
    for seed in SELECTION:
        folder=root/("seed-"+str(seed))
        m=getj(folder/"scenario-manifest.json")
        lock=getj(folder/"prediction-lock.json")
        ob=getj(folder/"observations-summary.json")["observations"]
        assert m["seed"]==seed==lock["seed"]
        for p,h in ((folder/"network.net.xml",m["network_sha256"]),
                    (folder/"trips.xml",m["demand_sha256"]),
                    (folder/"predictions/predictions.json",lock["prediction_sha256"])):
            assert sha(p)==h,(p,h)
        s=scheduled(folder/"trips.xml")
        assert len(s)==1000 and len(set(s))==1000
        base=routes(folder/"routes/I.rou.xml")
        assert set(base)==set(s)
        assert m["probes"][2]["target_vehicle_id"]==WHO[seed]
        for arm in SELECTION[seed]:
            rp=folder/"routes"/(arm+".rou.xml")
            op=origin(root,seed,arm)
            assert sha(rp)==m["arm_route_sha256"][arm]
            assert sha(op/"tripinfo.xml")==ob[arm]["tripinfo_sha256"]
            assert sha(op/"statistics.xml")==ob[arm]["statistics_sha256"]
            alt=routes(rp)
            changed={i for i in s if base[i]!=alt[i]}
            assert changed==(set() if arm=="I" else {WHO[seed]}),(seed,arm,changed)
            t=tripinfo(op/"tripinfo.xml")
            assert set(t)==set(s)
            for vid,v in t.items():
                assert v["arrival"]>=v["depart"]>=s[vid]-0.021
            cmd=getj(op/"command.json")
            assert isinstance(cmd,list) and cmd[0]=="sumo"
            assert "--seed" in cmd and int(cmd[cmd.index("--seed")+1])==seed
        baseline=tripinfo(origin(root,seed,"I")/"tripinfo.xml")
        treat=tripinfo(origin(root,seed,"probe2")/"tripinfo.xml")
        diff={i:(treat[i]["arrival"]-s[i])-(baseline[i]["arrival"]-s[i]) for i in s}
        net=sum(diff.values())
        others=sum(x for i,x in diff.items() if i!=WHO[seed])
        assert abs(net-EXPECTED_TOTAL[seed])<.1 and abs(others-EXPECTED_OTHERS[seed])<.1,(seed,net,others)
        summary[str(seed)]={"network_sha256":m["network_sha256"],
                            "demand_sha256":m["demand_sha256"],
                            "route_shas":{a:m["arm_route_sha256"][a] for a in SELECTION[seed]},
                            "treated":WHO[seed],"original_total_difference":net,
                            "original_other_driver_difference":others}
    return {"G0":"PASS","member_ledger_verified":full_ledger is not None,
            "original_run":SOURCE_RUN,"source_arm_pairs":summary,
            "original_verdict":"DEVELOPMENT_NOT_QUALIFIED",
            "validation":"NOT_STARTED","Test_B":"NOT_RUN"}
def pinned_preflight():
    d=prior.version_preflight()
    helptext=subprocess.check_output(["sumo","--help"],text=True)
    assert "--step-length" in helptext
    assert "--fcd-output" in helptext and "--vehroute-output.exit-times" in helptext
    return d
def preflight(root,ledger,out):
    report={"G0":"INCOMPLETE","G1":"INCOMPLETE","phase":"PREFLIGHT"}
    try:
        report.update(assert_sources(root,full_ledger=ledger))
        report["pinned"]=pinned_preflight()
        report["G1"]="PASS"
        report["output_max_per_arm_bytes"]=MAX_PER_ARM
        report["output_max_four_bytes"]=MAX_FOUR
        report["allowed_arms"]={str(k):list(v) for k,v in SELECTION.items()}
    except Exception as e:report["error"]=repr(e)
    outj(out,report);print(json.dumps(report,indent=2),flush=True)
    if report["G0"]!="PASS" or report["G1"]!="PASS":raise RuntimeError(report.get("error","G0/G1 incomplete"))
def make_add(out):
    p=out/"additional.xml";root=ET.Element("additional")
    ET.SubElement(root,"edgeData",id="e1-edge",file=str((out/"edgeData.xml.gz").resolve()),
                  period="5",withInternal="true",excludeEmpty="false")
    ET.SubElement(root,"laneData",id="e1-lane",file=str((out/"laneData.xml.gz").resolve()),
                  period="5",withInternal="true",excludeEmpty="false")
    ET.ElementTree(root).write(p,encoding="utf-8",xml_declaration=True)
    return p
def safety(root):
    sec=ET.parse(root/"statistics.xml").getroot().find("safety")
    if sec is None:raise RuntimeError("SUMO safety summary missing")
    fields=("collisions","emergencyStops","emergencyBraking")
    coll=len(ET.parse(root/"collisions.xml").getroot().findall(".//collision"))
    return {k:sec.get(k) for k in fields}|{"collision_events":coll}
def compare_one(source,replay,sched):
    old=tripinfo(source/"tripinfo.xml");new=tripinfo(replay/"tripinfo.xml")
    assert set(old)==set(new)==set(sched) and len(old)==1000
    maxima={}
    for f in FIELDS:
        if any(f not in old[i] or f not in new[i] for i in sched):
            raise RuntimeError("G2 required tripinfo field absent: "+f)
        maxima[f]=max(abs(old[i][f]-new[i][f]) for i in sched)
        if maxima[f]>.02000001:raise RuntimeError(f"G2 per-driver mismatch {f}: {maxima[f]}")
    before=sum(t["arrival"]-sched[i] for i,t in old.items())
    after=sum(t["arrival"]-sched[i] for i,t in new.items())
    if abs(after-before)>.10000001:raise RuntimeError("G2 aggregate mismatch "+str(after-before))
    original_safety=safety(source);replay_safety=safety(replay)
    if original_safety!=replay_safety:raise RuntimeError("G2 structured safety mismatch")
    return {"ids":1000,"maximum_field_deviation_seconds":maxima,
            "original_network_elapsed_s":before,"replay_network_elapsed_s":after,
            "absolute_network_total_difference_s":abs(after-before),
            "safety":replay_safety}
def run_replay(root,seed,arm,out):
    assert seed in SELECTION and arm in SELECTION[seed],"Attempt outside frozen four arms"
    root=P(root).resolve();out=P(out).resolve()
    out.mkdir(parents=True,exist_ok=False)
    info={"seed":seed,"arm":arm,"status":"INVALID","G0":"UNKNOWN","G1":"UNKNOWN",
          "G2":"NOT_RUN","G3":"NOT_TESTED","source_run":SOURCE_RUN}
    try:
        orig=assert_sources(root)
        info["G0"]=orig["G0"]
        info["G1"]="PASS" if pinned_preflight() else "INVALID"
        folder=root/("seed-"+str(seed))
        src=origin(root,seed,arm)
        add=make_add(out)
        cmd=["sumo","-n",str(folder/"network.net.xml"),
             "-r",str(folder/"routes"/(arm+".rou.xml")),
             "--tripinfo-output",str(out/"tripinfo.xml"),
             "--statistic-output",str(out/"statistics.xml"),
             "--collision-output",str(out/"collisions.xml"),
             "--seed",str(seed),"--no-step-log","true",
             "--log",str(out/"sumo.log"),
             "--fcd-output",str(out/"fcd.xml.gz"),
             "--vehroute-output",str(out/"vehroute.xml.gz"),
             "--vehroute-output.exit-times","true",
             "--additional-files",str(add)]
        original_cmd=getj(src/"command.json")
        # Original physics command has exactly the same flag/value pairs except
        # observation-only FCD, vehroute and additional-file path, plus output paths.
        physics_flags=("--seed","--no-step-log")
        for k in physics_flags:
            assert k in original_cmd and k in cmd
            assert original_cmd[original_cmd.index(k)+1]==cmd[cmd.index(k)+1]
        outj(out/"command.json",{"command":cmd,"original_command":original_cmd,
                               "original_inputs_sha":orig["source_arm_pairs"][str(seed)]})
        info["G2"]="SIMULATOR_ATTEMPT"
        with (out/"sumo-stage.log").open("w") as log:
            result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT,check=False)
        info["returncode"]=result.returncode
        if result.returncode:raise RuntimeError("SUMO failure; inspect sumo-stage.log")
        info["G2"]=compare_one(src,out,scheduled(folder/"trips.xml"))
        info["status"]="G2_PASS_G3_PENDING"
        required=("fcd.xml.gz","vehroute.xml.gz","edgeData.xml.gz","laneData.xml.gz")
        for name in required:
            if not (out/name).is_file() or (out/name).stat().st_size<100:
                raise RuntimeError("Mandatory observational stream unavailable: "+name)
        size=sum((out/name).stat().st_size for name in required)
        info["compressed_observation_bytes"]=size
        if size>MAX_PER_ARM:raise RuntimeError("Predefined 512MiB compressed observation budget exceeded")
        info["sha256"]={p.name:sha(p) for p in out.iterdir() if p.is_file()}
    except Exception as e:
        info["status"]="INVALID_OR_BLOCKED";info["error"]=repr(e)
    outj(out/"attempt.json",info)
    print(json.dumps(info,indent=2)[:6000],flush=True)
    if info["status"]!="G2_PASS_G3_PENDING":raise RuntimeError(info.get("error","Replay incomplete"))
def read_fcd(path):
    tracks=collections.defaultdict(dict)
    near01=collections.Counter();near10=collections.Counter()
    nearpositions=collections.defaultdict(list);viaevents=collections.Counter()
    per_second_near=collections.Counter();edge_first={}
    n=0;first=None;last=None;previous_time=-float("inf");last_lane={}
    with gzip.open(path,"rb") as f:
        for _,x in ET.iterparse(f,events=("end",)):
            if x.tag!="timestep":continue
            t=float(x.get("time"))
            if t<previous_time:raise RuntimeError("G3 non-monotonic FCD timestep")
            previous_time=t
            first=t if first is None else first;last=t
            for v in x.findall("vehicle"):
                vid=v.get("id")
                lane=v.get("lane")
                if not (vid and lane and all(v.get(k) is not None for k in ("pos","speed","x","y"))):
                    raise RuntimeError("G3 missing required FCD field")
                pos=float(v.get("pos"));speed=float(v.get("speed"))
                assert math.isfinite(pos) and math.isfinite(speed)
                if t in tracks[vid]:raise RuntimeError("G3 duplicate ID/time")
                tracks[vid][t]=(lane,pos,speed)
                edge=lane.rsplit("_",1)[0]
                if (vid,edge) not in edge_first:edge_first[(vid,edge)]=t
                bin5=int(t//5)*5
                if speed<=0.1:
                    near01[(edge,bin5)]+=1
                    nearpositions[(edge,t)].append(pos)
                    per_second_near[t]+=1
                if speed<=1.0:near10[(edge,bin5)]+=1
                before=last_lane.get(vid)
                if before is not None and before!=lane and lane.startswith(":"):
                    viaevents[(lane,bin5)]+=1
                last_lane[vid]=lane
                n+=1
            x.clear()
    if len(tracks)!=1000 or first is None:raise RuntimeError("G3 missing FCD driver IDs")
    clusters=collections.Counter()
    for (edge,t),positions in nearpositions.items():
        positions.sort()
        longest=1;group=1
        for a,b in zip(positions,positions[1:]):
            if b-a<=10:group+=1
            else:longest=max(longest,group);group=1
        longest=max(longest,group)
        if longest>=3:clusters[(edge,int(t//5)*5)]+=1
    return {"tracks":tracks,"near01":near01,"near10":near10,
            "clusters":clusters,"via":viaevents,"first_entries":edge_first,
            "samples":n,"n_vehicles":len(tracks),"first":first,"last":last,
            "near01_samples":sum(near01.values()),"near10_samples":sum(near10.values())}
def route_exit_audit(p,expected):
    with gzip.open(p,"rb") as f:root=ET.parse(f).getroot()
    vals=root.findall("vehicle")
    if len(vals)!=1000:raise RuntimeError("G3 vehroute incomplete vehicle count")
    ids=set();total_exits=0
    for v in vals:
        vid=v.get("id")
        if vid in ids or vid not in expected:raise RuntimeError("G3 invalid vehroute ID")
        ids.add(vid)
        route=v.find("route")
        if route is None or not route.get("exitTimes"):
            raise RuntimeError("G3 absent vehroute exitTimes")
        if tuple(route.get("edges").split())!=expected[vid]:
            raise RuntimeError("G3 route changed after observation")
        xs=route.get("exitTimes").split()
        if len(xs)!=len(expected[vid]):raise RuntimeError("G3 exitTimes/edge sequence mismatch")
        total_exits+=len(xs)
    return total_exits
def detector_bounds(p):
    first=None;last=None;rows=0;partials=0
    with gzip.open(p,"rb") as f:
        for _,n in ET.iterparse(f,events=("end",)):
            if n.tag!="interval":continue
            b=float(n.get("begin"));e=float(n.get("end"))
            if e<=b or e-b>5.001:raise RuntimeError("G3 invalid detector duration")
            first=b if first is None else min(first,b)
            last=e if last is None else max(last,e)
            if e-b<4.999:partials+=1
            rows+=len(n)
            n.clear()
    if first is None or rows<=0:raise RuntimeError("G3 empty detector")
    return {"start":first,"end":last,"rows":rows,"partial_end_bins":partials}
def first_divergence(a,b):
    times=sorted(set(a)|set(b))
    for t in times:
        x=a.get(t);y=b.get(t)
        if x is None or y is None or x[0]!=y[0] or abs(x[1]-y[1])>.02 or abs(x[2]-y[2])>.02:
            return t
    return None
def hot_edges(a,b,field):
    current=b[field];old=a[field]
    keys=set(current)|set(old)
    edges=collections.defaultdict(lambda:{"net":0,"abs":0,"first10":None,"maxbin":0})
    for edge,t in sorted(keys,key=lambda k:(k[1],k[0])):
        change=current[(edge,t)]-old[(edge,t)]
        d=edges[edge];d["net"]+=change;d["abs"]+=abs(change)
        if abs(change)>d["maxbin"]:d["maxbin"]=abs(change)
        if abs(change)>=10 and d["first10"] is None:d["first10"]=t
    return sorted([{"edge":e,"signed_change":d["net"],"absolute_change":d["abs"],
                    "largest_bin_difference":d["maxbin"],
                    "first_5s_bin_abs_ge10":d["first10"]} for e,d in edges.items()],
                  key=lambda v:(-v["absolute_change"],v["edge"]))
def analyse(root,replays,out):
    root=P(root);replays=P(replays);out=P(out);out.mkdir(parents=True,exist_ok=True)
    base=assert_sources(root)
    individual=[];arms=[];contrasts=[];hot=[];queue=[];junction=[];early=[];case_summary=[]
    all_fcd={};all_trip={};total_raw_bytes=0
    for seed in SELECTION:
        folder=root/("seed-"+str(seed))
        sched=scheduled(folder/"trips.xml")
        for arm in SELECTION[seed]:
            q=replays/("replay-"+str(seed)+"-"+arm)
            attempt=getj(q/"attempt.json")
            if attempt.get("status")!="G2_PASS_G3_PENDING":raise RuntimeError("G2 attempt failure: "+str((seed,arm)))
            valid=compare_one(origin(root,seed,arm),q,sched)
            all_trip[(seed,arm)]=tripinfo(q/"tripinfo.xml")
            f=read_fcd(q/"fcd.xml.gz")
            all_fcd[(seed,arm)]=f
            expected=routes(folder/"routes"/(arm+".rou.xml"))
            exits=route_exit_audit(q/"vehroute.xml.gz",expected)
            edge=detector_bounds(q/"edgeData.xml.gz")
            lane=detector_bounds(q/"laneData.xml.gz")
            lastarrival=max(x["arrival"] for x in all_trip[(seed,arm)].values())
            if min(edge["end"],lane["end"])<lastarrival-5:
                raise RuntimeError("G3 detector coverage ends before final arrival")
            if f["last"]<lastarrival-5:
                raise RuntimeError("G3 vehicle tracks end before original completions")
            for vid,t in all_trip[(seed,arm)].items():
                if vid not in f["tracks"]:raise RuntimeError("G3 no vehicle trace "+vid)
                track=f["tracks"][vid]
                if min(track)>t["depart"]+2 or max(track)<t["arrival"]-3:
                    raise RuntimeError("G3 vehicle-specific FCD starts late/ends early "+vid)
            names=("fcd.xml.gz","vehroute.xml.gz","edgeData.xml.gz","laneData.xml.gz")
            actualbytes=sum((q/n).stat().st_size for n in names)
            if actualbytes>MAX_PER_ARM:raise RuntimeError("G3 per-arm compressed output budget exceeded")
            total_raw_bytes+=actualbytes
            arms.append({"seed":seed,"arm":arm,"G2":"PASS","G3":"PASS",
                "G2_max_field_s":max(valid["maximum_field_deviation_seconds"].values()),
                "G2_absolute_total_error_s":valid["absolute_network_total_difference_s"],
                "FCD_vehicles":1000,"FCD_samples":f["samples"],
                "FCD_nearstop_samples_0_1ms":f["near01_samples"],
                "FCD_nearstop_samples_1_0ms":f["near10_samples"],
                "vehroute_external_edge_exits":exits,
                "edgedata_rows":edge["rows"],"lanedata_rows":lane["rows"],
                "last_fcd_s":f["last"],"last_trip_arrival_s":lastarrival,
                "compressed_observation_bytes":actualbytes})
    if total_raw_bytes>MAX_FOUR:raise RuntimeError("G3 total 2GiB compressed output cap exceeded")
    for seed in SELECTION:
        b=all_trip[(seed,"I")];v=all_trip[(seed,"probe2")]
        oldf=all_fcd[(seed,"I")];newf=all_fcd[(seed,"probe2")]
        target=WHO[seed]
        for vid in b:
            td=(v[vid]["arrival"]-b[vid]["arrival"])
            dinsert=v[vid]["depart"]-b[vid]["depart"]
            ddur=v[vid]["duration"]-b[vid]["duration"]
            dwait=v[vid]["waitingTime"]-b[vid]["waitingTime"]
            if abs(dinsert+ddur-td)>.1:raise RuntimeError("FCD G3 paired elapsed accounting failed")
            divergence=first_divergence(oldf["tracks"][vid],newf["tracks"][vid])
            individual.append({"seed":seed,"vehicle":vid,"changed_planned_route":int(vid==target),
                "nonparticipant":int(int(vid[-4:])%2==1),
                "arrival_delta_s":td,"insertion_delta_s":dinsert,
                "duration_delta_s":ddur,"waiting_delta_s":dwait,
                "first_vehicle_track_difference_s":divergence if divergence is not None else ""})
        matched=[r for r in individual if r["seed"]==seed]
        total=sum(r["arrival_delta_s"] for r in matched)
        others=sum(r["arrival_delta_s"] for r in matched if not r["changed_planned_route"])
        ins=sum(r["insertion_delta_s"] for r in matched)
        durations=sum(r["duration_delta_s"] for r in matched)
        wait=sum(r["waiting_delta_s"] for r in matched)
        if abs(total-EXPECTED_TOTAL[seed])>.1 or abs(others-EXPECTED_OTHERS[seed])>.1:
            raise RuntimeError("G2 pairwise network outcomes failed frozen original expected contrast")
        if abs(total-ins-durations)>.1:raise RuntimeError("G3 scheduled-to-arrival decomposition")
        harmed=sum(r["arrival_delta_s"]>30 for r in matched)
        nonp=[r for r in matched if r["nonparticipant"]]
        harmnonp=sum(r["arrival_delta_s"]>30 for r in nonp)
        helpn=sum(r["arrival_delta_s"]<0 for r in matched)
        hurt=sum(r["arrival_delta_s"]>0 for r in matched)
        nearold=oldf["near01_samples"];nearnew=newf["near01_samples"]
        top=hot_edges(oldf,newf,"near01")
        topclusters=hot_edges(oldf,newf,"clusters")
        hot.extend([{"seed":seed,"metric":"nearstop_0_1ms_vehicle_samples",**r} for r in top[:30]])
        queue.extend([{"seed":seed,"metric":"three_stopped_vehicles_within_10m_cluster_steps",**r}
                      for r in topclusters[:30]])
        first_target=first_divergence(oldf["tracks"][target],newf["tracks"][target])
        other_first=min((r["first_vehicle_track_difference_s"] for r in matched
                     if r["vehicle"]!=target and r["first_vehicle_track_difference_s"]!=""),default=None)
        # Empirical first-of-edge footprint is ACTUAL, not historical E1 per-edge prediction.
        for path, data in (("I",oldf),("probe2",newf)):
            routepath=routes(root/("seed-"+str(seed))/"routes"/(path+".rou.xml"))[target]
            for rank,ed in enumerate(routepath):
                t=data["first_entries"].get((target,ed))
                early.append({"seed":seed,"arm":path,"vehicle":target,"route_edge_number":rank,
                    "edge":ed,"first_observed_FCD_sample_s":t if t is not None else "",
                    "time_precision":"1second_sample_interval; not continuous entry"})
        # Descriptive movement-event counts where FCD actually observed via internal lanes.
        internal_lanes={l for f in (oldf,newf) for l,_ in f["via"]}
        net=ET.parse(root/("seed-"+str(seed))/"network.net.xml").getroot()
        via_map={}
        for e in net.findall("connection"):
            if e.get("via"):via_map[e.get("via")]=(e.get("from"),e.get("to"))
        for via in sorted(internal_lanes):
            if via not in via_map:continue
            bcount=sum(n for (lane,t),n in oldf["via"].items() if lane==via)
            acount=sum(n for (lane,t),n in newf["via"].items() if lane==via)
            if bcount!=acount:
                junction.append({"seed":seed,"internal_lane":via,
                    "from_external_edge":via_map[via][0],"to_external_edge":via_map[via][1],
                    "observed_first_internal_lane_samples_I":bcount,
                    "observed_first_internal_lane_samples_probe2":acount,
                    "difference":acount-bcount,
                    "note":"sampled internal-lane entry; short crossings may not be observed at 1s sampling"})
        case_summary.append({"seed":seed,"target":target,"actual_externality_network_s":others,
                "actual_all_driver_network_s":total,"insertion_network_s":ins,
                "duration_network_s":dur,"waiting_network_s":wait,
                "nearstop_FCD_delta_vehicle_samples":nearnew-nearold,
                "nearstop_FCD_delta_1ms_threshold":newf["near10_samples"]-oldf["near10_samples"],
                "drivers_helped":helpn,"drivers_harmed":hurt,"drivers_harmed_gt30":harmed,
                "nonparticipant_drivers_harmed_gt30":harmnonp,
                "nonparticipant_n":len(nonp),
                "target_first_trace_divergence_s":first_target,
                "first_other_driver_trace_divergence_s":other_first,
                "top_nearstop_edge":top[0]["edge"] if top else None,
                "top_nearstop_edge_signed_change":top[0]["signed_change"] if top else None,
                "top_cluster_edge":topclusters[0]["edge"] if topclusters else None})
        contrasts.append({"seed":seed,"observed_other_driver_network_s":others,
                    "observed_all_driver_network_s":total,
                    "source_insertion_network_s":ins,
                    "in_network_duration_network_s":dur,
                    "recorded_waiting_time_network_s":wait})
    writecsv(out/"G2_G3_replay_gates.csv",arms)
    writecsv(out/"driver_matched_differences.csv",individual)
    writecsv(out/"actual_target_edge_entry_samples.csv",early)
    writecsv(out/"nearstop_edge_5s_hotspots.csv",hot)
    writecsv(out/"nearstop_spatial_cluster_hotspots.csv",queue)
    writecsv(out/"observed_internal_lane_entry_differences.csv",junction,
             fields=("seed","internal_lane","from_external_edge","to_external_edge",
                     "observed_first_internal_lane_samples_I","observed_first_internal_lane_samples_probe2",
                     "difference","note"))
    writecsv(out/"pairwise_network_accounting.csv",contrasts)
    report={"status":"VALID_RETROSPECTIVE_OBSERVATIONAL_REPLAY_NO_CAUSAL_MEDIATOR_IDENTIFIED",
            "G0":"PASS","G1":"PASS","G2":"PASS","G3":"PASS",
            "original_source_run":SOURCE_RUN,"replay_arms":4,"matched_driver_tripinfo":4000,
            "compressed_four_arm_bytes":total_raw_bytes,
            "original_verdict":"DEVELOPMENT_NOT_QUALIFIED","independent_validation":"NOT_STARTED","Test_B":"NOT_RUN",
            "research_limit":"two seeds selected retrospectively; no independent predictor validation; junction mediation not randomized",
            "case_results":case_summary,"gate_rows":arms}
    outj(out/"scientific_summary.json",report)
    lines=[
      "# E1-v2 four-arm passive replay — scientific findings",
      "",
      "## Relevance to the central cooperative-traffic question",
      "Cooperation may improve aggregate traffic only if the effects of one person's changed route on other drivers can be forecast accurately. These four retrospective replays trace actual vehicle movements for two already-observed contrasting cases. They do not validate a forecasting model or show a cooperative-policy advantage.",
      "",
      "**Status: VALID RETROSPECTIVE INSTRUMENTED OBSERVATION.** All four selected attempts reproduced original 1,000-driver outcomes and contained FCD, exit-time, edge/lane and exception evidence. The unique physical causal mediator remains unidentified. Frozen E1-v2 development NO-GO is unchanged; independent validation and cooperative Test B remain unexecuted.",
      "",
      "## Scientific evidence and provenance",
      "- Original archived development execution: GitHub Actions 41966516110; original member-byte release exp007-e1v2-d1-development-nogo-2026-11-04.",
      "- Original simulations: SUMO 1.28.0 image "+IMAGE+".",
      "- Two seeds selected **after viewing original results**; four arms (6112 I/probe2 and 6113 I/probe2), 4,000 matched replay tripinfos; not four statistically independent replications.",
      "- Original SHA256s, route containment and prospective prediction locks checked. Passive flags only, no new demand or routing decisions.",
      "",
      "## Gates",
      "| Seed / arm | G2 per-field max deviation (seconds) | FCD vehicle samples | Near-stopped samples ≤0.1m/s | External edge exits |",
      "|---|---:|---:|---:|---:|"]
    for r in arms:
        lines.append(f"| {r['seed']} / {r['arm']} | {r['G2_max_field_s']:.3f} | {r['FCD_samples']:,} | {r['FCD_nearstop_samples_0_1ms']:,} | {r['vehroute_external_edge_exits']:,} |")
    lines+=["","## Paired original-network outcome and physical time accounting",
      "| Seed / changed vehicle | Others' net cost (network-s) | All-driver change (network-s) | Insertion component | In-network duration | Recorded waiting (included within duration) | FCD near-stop sample change |",
      "|---|---:|---:|---:|---:|---:|---:|"]
    for r in case_summary:
        lines.append(f"| {r['seed']} / {r['target']} | {r['actual_externality_network_s']:+.0f} | {r['actual_all_driver_network_s']:+.0f} | {r['insertion_network_s']:+.0f} | {r['duration_network_s']:+.0f} | {r['waiting_network_s']:+.0f} | {r['nearstop_FCD_delta_vehicle_samples']:+.0f} |")
    lines+=["",
      "The observed travel-time effects mainly occurred after insertion in these two selected scenarios; recorded stopped waiting and independent FCD near-stopped samples are related but not identical measurements. Waiting is already part of each vehicle's duration and was NOT added to elapsed network cost.",
      "",
      "## Driver-level chronology and traffic response (descriptive only)",
      "| Seed | Changed driver's first matched trace divergence (s) | Earliest matched other-driver FCD difference (s) | Largest absolute edge near-stop response |",
      "|---|---:|---:|---|"]
    for r in case_summary:
        lines.append(f"| {r['seed']} | {r['target_first_trace_divergence_s']} | {r['first_other_driver_trace_divergence_s']} | {r['top_nearstop_edge']} ({r['top_nearstop_edge_signed_change']:+.0f} near-stopped vehicle samples) |")
    lines+=["",
      "FCD is sampled at one-second steps. First observed lane/edge appearance is **not** exact continuous-time entry. The historical E1-v2 predictions do NOT archive per-edge forecast clocks, so this study does NOT manufacture prospective per-edge forecast-versus-actual errors.",
      "Observed internal-lane sampling and queue-proxy clusters are documented in the accompanying machine-readable tables. A one-second internal-lane sample can miss a short crossing. A cluster is a declared spatial proxy (three or more stopped vehicles within 10m consecutive position gaps), **not** an independent causal diagnosis of an upstream spillback wave.",
      "",
      "## Competing hypotheses and limits",
      "| Candidate | What the new evidence can assess | What remains unproven |",
      "|---|---|---|",
      "| T: temporal ordering | Observed per-driver road/lane sample sequences, departure times and divergence onset | Model-vs-SUMO per-edge prediction error without archived model event trace |",
      "| Q: physical queuing | Near-stop exposures, contiguous spatial groups, edge and time redistribution | Unique causal upstream spillback mediator absent a controlled intervention |",
      "| J: junction service | Internal-lane entry samples linked to verified static connection map | True crossing concurrency and causal contribution of one junction; 1s sampling misses fast movements |",
      "| A: accounting/measurement | All original 4,000 vehicle outcomes and route hashes preserved; FCD and exit-time evidence available | Generalizability from two retrospectively selected seeds |",
      "",
      "**Disposition:** A valid explanatory observation can identify timing- and queue-associated patterns but not a unique junction/queue causal effect. E1-v2's frozen D1 NO-GO stands. A future model E1-v3 would need fresh development and independent validation. Do not open the reserved 6201–6212 or 6301–6312 seeds or run Test B without a separately authorized prospective protocol.",
      "",
      "## Reproducibility assets",
      "This report accompanies scientific_summary.json, G2_G3_replay_gates.csv, driver_matched_differences.csv, actual_target_edge_entry_samples.csv, nearstop_edge_5s_hotspots.csv, nearstop_spatial_cluster_hotspots.csv, observed_internal_lane_entry_differences.csv, and pairwise_network_accounting.csv. Full FCD, original-exitTimes and detectors are retained in the separate evidence release, not mixed with original frozen D1 members.",
      "",
      "**No social publication was authorized or initiated.**"]
    (out/"FINAL_SCIENTIFIC_REPORT.md").write_text("\n".join(lines)+"\n")
    print(json.dumps(report,indent=2)[:18000],flush=True)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("command",choices=("preflight","replay","aggregate"))
    ap.add_argument("--root",required=True)
    ap.add_argument("--ledger")
    ap.add_argument("--seed",type=int)
    ap.add_argument("--arm")
    ap.add_argument("--replays")
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    if a.command=="preflight":
        if not a.ledger:raise SystemExit("Missing SHA-256 original member ledger")
        preflight(a.root,a.ledger,a.out)
    elif a.command=="replay":
        if not a.arm or a.seed is None:raise SystemExit("Explicit frozen seed/arm required")
        run_replay(a.root,a.seed,a.arm,a.out)
    else:
        if not a.replays:raise SystemExit("Missing original replay path")
        analyse(a.root,a.replays,a.out)
if __name__=="__main__":main()
