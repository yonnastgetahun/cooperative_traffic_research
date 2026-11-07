#!/usr/bin/env python3
"""Authorized B*/C* controlled dev2101 timing comparison — no unseen cohorts.

Never changes original T1 B/C schedules or forecasts. Uses original B tripinfo
speedFactor by driver ID to control an archival random-attribute confound.
This is a single-seed *development* diagnostic, not independent validation.
"""
import argparse
import collections
import hashlib
import json
import math
import statistics
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

SEED = 2101
ORIGINAL_SHA256 = {
    "source/network.net.xml": "e3ec1811290f39c1a8e6a2c81e24180c08c71e22e0fcdbeb14fcc740aa87d601",
    "source/trips.xml": "b7e1424a7c44e2d4a0c66098006e3c31579a9dcc074d2503b53687a14c223ce5",
    "sumo_B/routes.rou.xml": "3d2984a4010445e8abe03d5855e796a3291b95ca2b0de763f05c0869a1f8a01e",
    "sumo_C/routes.rou.xml": "707b6c215b0792d4cf4d99c15e1a34670595e51995cd6814bc8ea8a7aa2d1718",
    "sumo_B/tripinfo.xml": "b1afa3b889602af2431a1cd7838da5e9f7d9ac8251d9df84aa937e6a6ddffb1a",
    "sumo_C/tripinfo.xml": "3a2c1d3873902f3f000819dd273cd2bce2428fc917312453184b350dde22b9a9",
}
FIELDS = ("depart", "departDelay", "arrival", "duration", "waitingTime", "timeLoss", "speedFactor")

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def require(condition, why):
    if not condition:
        raise RuntimeError(why)

def save(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")

def parse_routes(path):
    root=ET.parse(path).getroot()
    vtypes=[ET.tostring(x,encoding="unicode") for x in root.findall("vType")]
    elems=root.findall("vehicle")
    d={}
    for e in elems:
        vid=e.get("id")
        route=e.find("route")
        require(vid and route is not None and vid not in d, "bad original route identity")
        d[vid]={"depart":float(e.get("depart")),
                "route":tuple((route.get("edges") or "").split()),
                "attributes":dict(e.attrib),
                "route_attrs":dict(route.attrib)}
    require(len(elems)==1000 and len(d)==1000,"expected 1000 route records")
    require(all(a["depart"]<=b["depart"] for a,b in zip(d.values(),list(d.values())[1:])),
            "original route XML not chronological")
    return d,vtypes

def parse_tripinfo(path):
    rows=ET.parse(path).getroot().findall("tripinfo")
    d={r.get("id"):dict(r.attrib) for r in rows}
    require(len(rows)==len(d)==1000,"expected 1000 completed tripinfo identities")
    return d

def original_data(source):
    for rel,expected in ORIGINAL_SHA256.items():
        p=source/rel
        require(p.is_file(), "missing original "+rel)
        require(sha256(p)==expected,"original file SHA256 mismatch "+rel)
    b,bt=parse_routes(source/"sumo_B/routes.rou.xml")
    c,ct=parse_routes(source/"sumo_C/routes.rou.xml")
    info_b=parse_tripinfo(source/"sumo_B/tripinfo.xml")
    info_c=parse_tripinfo(source/"sumo_C/tripinfo.xml")
    pref=ET.parse(source/"source/trips.xml").getroot().findall("trip")
    preferred={v.get("id"):float(v.get("depart")) for v in pref}
    require(len(pref)==len(preferred)==1000,"original preferred IDs invalid")
    require(set(b)==set(c)==set(preferred)==set(info_b)==set(info_c),"original ID sets differ")
    require(bt==ct,"original vType definitions differ")
    eligible=set(sorted(b, key=lambda vid:(hashlib.sha256(
        f"T1:eligible:{SEED}:{vid}".encode()).hexdigest(),vid))[:500])
    shift={}
    for vid in b:
        x,y=b[vid],c[vid]
        require(x["route"]==y["route"] and x["route"],"fixed routes mismatch")
        require(x["route_attrs"]==y["route_attrs"],"route attributes mismatch")
        orig_a={k:v for k,v in x["attributes"].items() if k!="depart"}
        coop_a={k:v for k,v in y["attributes"].items() if k!="depart"}
        require(orig_a==coop_a,"non-depart vehicle input properties mismatch")
        require(abs(x["depart"]-preferred[vid])<1e-7,"original B not unshifted")
        delta=round(y["depart"]-x["depart"],4)
        require(delta in (0,10.0),"unexpected C schedule")
        if delta:
            require(vid in eligible,"nonparticipant shifted")
            shift[vid]=delta
        require(info_b[vid].get("speedFactor") is not None,"B speed factor absent")
    require(len(shift)==12 and sum(shift.values())==120,"not original 12 shifts")
    require(all(math.isfinite(float(x["speedFactor"])) and
                float(x["speedFactor"])>0 for x in info_b.values()),"invalid speed factors")
    changed_sf=sum(info_b[vid]["speedFactor"] != info_c[vid]["speedFactor"] for vid in b)
    require(changed_sf==380,"original speed-factor confound fingerprint changed")
    return b,c,preferred,eligible,shift,info_b,bt

def emit(source,prepared):
    require(not prepared.exists(),"fail closed: prepared inputs already exist")
    b,c,preferred,eligible,shifts,info_b,vtypes=original_data(source)
    prepared.mkdir(parents=True)
    canonical={}
    files={}
    for vid in sorted(b):
        route=b[vid]["route"]
        props={k:v for k,v in b[vid]["attributes"].items() if k!="depart"}
        props["speedFactor"]=info_b[vid]["speedFactor"]
        canonical[vid]={"preferred":preferred[vid],"eligible":vid in eligible,
                        "B_requested":b[vid]["depart"],"C_requested":c[vid]["depart"],
                        "route":list(route),"fixed_attributes":props,
                        "source_B_speedFactor":info_b[vid]["speedFactor"]}
    for arm,old in (("Bstar",b),("Cstar",c)):
        # Preserve original route-file vType element and all per-vehicle attributes.
        # SpeedFactor is explicit (rather than sampled in random file presentation order).
        root=ET.Element("routes")
        for element in ET.parse(source/"sumo_B/routes.rou.xml").getroot().findall("vType"):
            root.append(element)
        for vid in sorted(old,key=lambda vid:(old[vid]["depart"],vid)):
            e=old[vid]
            props={k:v for k,v in e["attributes"].items() if k!="depart"}
            props["depart"]=f'{e["depart"]:.3f}'
            props["speedFactor"]=info_b[vid]["speedFactor"]
            v=ET.SubElement(root,"vehicle",props)
            ET.SubElement(v,"route",e["route_attrs"])
        file=prepared/(arm+".rou.xml")
        ET.ElementTree(root).write(file,encoding="utf-8",xml_declaration=True)
        files[arm]={"path":str(file),"sha256":sha256(file)}
    bb,_=parse_routes(prepared/"Bstar.rou.xml")
    cc,_=parse_routes(prepared/"Cstar.rou.xml")
    for vid in sorted(b):
        xb,xc=bb[vid],cc[vid]
        require(xb["route"]==xc["route"]==b[vid]["route"],"new routes mismatch")
        require({k:v for k,v in xb["attributes"].items() if k!="depart"}==
                {k:v for k,v in xc["attributes"].items() if k!="depart"},
                "new fixed vehicle attributes differ across arms")
        require(xb["attributes"]["speedFactor"]==xc["attributes"]["speedFactor"]==
                info_b[vid]["speedFactor"],"new speedFactor differs by ID")
        require(abs(xb["depart"]-b[vid]["depart"])<1e-7 and
                abs(xc["depart"]-c[vid]["depart"])<1e-7,"new schedules differ from original")
    report={"status":"STATIC_CONTROL_PREFLIGHT_PASS",
            "seed":SEED,"network_sha256":sha256(source/"source/network.net.xml"),
            "original_file_digests":ORIGINAL_SHA256,
            "source_original_t1_run":42183640504,
            "original_artifact_sha256":"b524729226c44b722f2c8c157f017dee98181dcd8dfb97c2ec14401229184fae",
            "total":len(b),"eligible":len(eligible),"shifted":len(shifts),
            "changed_requested_departure":shifts,
            "fixed_vehicle_manifest":canonical,
            "prepared_routes":files,
            "legacy_original_B_C_speed_factor_id_mismatch":380,
            "control_note":"Bstar/Cstar both use original B per-ID printed tripinfo speedFactor; not necessarily historical full-precision random draw."}
    save(prepared/"source_and_control_manifest.json",report)
    return report

def sumo_flags():
    version=subprocess.check_output(["sumo","--version"],text=True)
    require("1.28.0" in version,"incorrect pinned SUMO build "+version)
    help=subprocess.check_output(["sumo","--help"],text=True)
    for flag in ("--fcd-output", "--fcd-output.attributes", "--vehroute-output", "--vehroute-output.exit-times"):
        require(flag in help, "SUMO pinned binary missing "+flag)
    return version.splitlines()[0]

def simulate(source,prepared,obs,arm):
    require(arm in ("Bstar","Cstar"),"Only two authorized development arms")
    require((prepared/"source_and_control_manifest.json").is_file(),"missing preflight manifest")
    version=sumo_flags()
    # Verify inputs exactly preserved since preflight.
    manifest=json.loads((prepared/"source_and_control_manifest.json").read_text())
    require(manifest["status"]=="STATIC_CONTROL_PREFLIGHT_PASS","preflight invalid")
    for k in ("Bstar","Cstar"):
        require(sha256(prepared/(k+".rou.xml"))==manifest["prepared_routes"][k]["sha256"],
                "prepared route changed since preflight")
    require(sha256(source/"source/network.net.xml")==manifest["network_sha256"],
            "network changed since preflight")
    out=obs/arm
    require(not out.exists(),"fail closed: cannot rerun or overwrite "+str(out))
    out.mkdir(parents=True)
    cmd=["sumo","-n",str(source/"source/network.net.xml"),
         "-r",str(prepared/(arm+".rou.xml")),
         "--tripinfo-output",str(out/"tripinfo.xml"),
         "--statistic-output",str(out/"statistics.xml"),
         "--collision-output",str(out/"collisions.xml"),
         "--seed","2101","--no-step-log","true","--log",str(out/"sumo.log"),
         "--fcd-output",str(out/"fcd.xml"),
         "--fcd-output.attributes","x,y,angle,type,speed,lane,pos",
         "--vehroute-output",str(out/"vehroute.xml"),
         "--vehroute-output.exit-times","true"]
    save(out/"command.json",{"command":cmd,"version":version,
        "changed_nonoutput_input":"explicit identical per-ID speedFactor and original B/C departures",
        "passive_additions":["--fcd-output","--fcd-output.attributes","--vehroute-output","--vehroute-output.exit-times"]})
    with (out/"run.log").open("w") as log:
        subprocess.run(cmd,check=True,stdout=log,stderr=subprocess.STDOUT)
    for name in ("tripinfo.xml","statistics.xml","collisions.xml","fcd.xml","vehroute.xml"):
        require((out/name).is_file(), "missing output "+name)

def safety_stats(path):
    root=ET.parse(path).getroot()
    return {t:dict(root.find(t).attrib) if root.find(t) is not None else {}
            for t in ("vehicles","teleports","safety")}

def gate_arm(source,prepared,obs,arm):
    data=json.loads((prepared/"source_and_control_manifest.json").read_text())
    old_b,old_c,preferred,eligible,shifts,info_b,_=original_data(source)
    out=obs/arm
    gate={"arm":arm,"status":"CONTROL_INVALID"}
    save(out/"control_gate.json",gate)
    r=parse_tripinfo(out/"tripinfo.xml")
    routes,_=parse_routes(prepared/(arm+".rou.xml"))
    require(set(r)==set(preferred),"missing or extra completed IDs")
    issues=[]
    requested_sum,insertion_sum,duration_sum,total_sum=0.,0.,0.,0.
    for vid in sorted(r):
        x=r[vid]
        sf=float(x.get("speedFactor","nan"))
        expected=float(info_b[vid]["speedFactor"])
        require(math.isfinite(sf) and abs(sf-expected)<0.011,
                "observed per-ID speedFactor deviates from fixed value "+vid)
        depart=float(x["depart"])
        sched=routes[vid]["depart"]
        delay=float(x["departDelay"])
        dur=float(x["duration"])
        arrive=float(x["arrival"])
        require(depart+1e-6>=sched,"driver departed early "+vid)
        require(abs((depart-sched)-delay)<=0.051,"depart insertion accounting mismatch "+vid)
        require(abs((depart+dur)-arrive)<=0.051,"trip arrival accounting mismatch "+vid)
        require(not x.get("vaporized",""),"vaporized trip "+vid)
        require(x.get("vType")=="passenger","type mismatch "+vid)
        requested_sum+=sched-preferred[vid]
        insertion_sum+=delay
        duration_sum+=dur
        total_sum+=arrive-preferred[vid]
    require(abs(total_sum-(requested_sum+insertion_sum+duration_sum))<=.1,
            "total original-preferred clock accounting mismatch")
    require(abs(requested_sum-(120 if arm=="Cstar" else 0))<.01,
            "requested shift total mismatch")
    stats=safety_stats(out/"statistics.xml")
    require(int(stats["vehicles"].get("inserted","-1"))==1000,
            "not 1000 inserted")
    require(int(stats["vehicles"].get("running","-1"))==0,
            "incomplete running")
    # Exceptions must be recorded, including when present; don't silently drop.
    collisions=len(ET.parse(out/"collisions.xml").getroot().findall("collision"))
    gate={"arm":arm,"status":"CONTROL_PASS","matched_drivers":1000,
          "sum_preferred_to_arrival_network_s":round(total_sum,4),
          "requested_predeparture_s":round(requested_sum,4),
          "insertion_delay_s":round(insertion_sum,4),
          "in_network_duration_s":round(duration_sum,4),
          "exception_counts":stats, "collision_rows":collisions,
          "matched_per_id_speed_factors":1000,
          "replayed_input_sha256":sha256(prepared/(arm+".rou.xml")),
          "trace_sha256":{f:sha256(out/f) for f in ("fcd.xml","vehroute.xml")}}
    save(out/"control_gate.json",gate)
    print(json.dumps({k:gate[k] for k in ("arm","status","sum_preferred_to_arrival_network_s")}))
    return gate

def frames(path):
    """FCD snapshots retained only for earliest per-driver divergence and lane exposure."""
    result={}
    unique=set()
    for evt,x in ET.iterparse(path,events=("end",)):
        if x.tag!="timestep":
            continue
        t=float(x.get("time"))
        s={}
        for v in x.findall("vehicle"):
            vid=v.get("id"); lane=v.get("lane"); pos=v.get("pos"); speed=v.get("speed")
            require(all(y is not None for y in (vid,lane,pos,speed)),
                    "FCD lacks lane/position/speed")
            s[vid]=(lane,float(pos),float(speed))
            unique.add(vid)
        require(t not in result,"duplicate timestep")
        result[t]=s
        x.clear()
    require(len(unique)==1000,"FCD omitted some drivers")
    return result

def first_diff(fb,fc,shifted,overlap):
    seen={}
    for t in sorted(set(fb)|set(fc)):
        a,b=fb.get(t,{}),fc.get(t,{})
        for vid in (set(a)|set(b)) - set(seen):
            x,y=a.get(vid),b.get(vid)
            if x is None or y is None:
                reason="insertion_or_presence"
            elif x[0]!=y[0]:
                reason="lane"
            elif abs(x[1]-y[1])>.02:
                reason="position"
            elif abs(x[2]-y[2])>.02:
                reason="speed"
            else:
                continue
            seen[vid]={"id":vid,"time_s":t,"difference":reason,
                       "group":"shifted" if vid in shifted else "unshifted",
                       "shares_shifted_route_edge":vid in overlap,
                       "B":x,"C":y}
    ordered=sorted(seen.values(),key=lambda e:(e["time_s"],e["id"]))
    return {"first_shifted":next((x for x in ordered if x["group"]=="shifted"),None),
            "first_unshifted":next((x for x in ordered if x["group"]=="unshifted"),None),
            "first_30_events":ordered[:30],
            "first_30_unshifted":[x for x in ordered if x["group"]=="unshifted"][:30],
            "vehicles_with_any_fcd_divergence":len(ordered)}

def lane_counts(frames):
    stop=collections.Counter();slow=collections.Counter()
    for snap in frames.values():
        for lane,pos,speed in snap.values():
            if speed<=.1:
                stop[lane]+=1
            elif speed<5.:
                slow[lane]+=1
    return stop,slow

def exit_clocks(path,canonical):
    root=ET.parse(path).getroot()
    out={}
    for v in root.findall("vehicle"):
        vid=v.get("id")
        require(vid in canonical and vid not in out,"vehroute bad ID")
        route=v.find("route")
        require(route is not None,"missing vehroute route")
        edges=tuple((route.get("edges") or "").split())
        times=[float(x) for x in (route.get("exitTimes") or "").split()]
        require(edges==tuple(canonical[vid]["route"]) and len(times)==len(edges),
                "vehroute exit times or route mismatch "+vid)
        out[vid]=times
    require(len(out)==1000,"incomplete vehroute")
    return out

def freeflows(net):
    root=ET.parse(net).getroot()
    result={}
    for e in root.findall("edge"):
        if e.get("function")=="internal" or e.get("id","").startswith(":"):
            continue
        lane=e.find("lane")
        if lane is not None:
            result[e.get("id")]=float(lane.get("length"))/float(lane.get("speed"))
    return result

def clock_errors(obs,arm,canonical,ff,shifted,overlap):
    trip=parse_tripinfo(obs/arm/"tripinfo.xml")
    exit=exit_clocks(obs/arm/"vehroute.xml",canonical)
    values=collections.defaultdict(list)
    examples=[]
    for vid in sorted(canonical):
        info=canonical[vid]
        intended=info["B_requested" if arm=="Bstar" else "C_requested"]
        actual=float(trip[vid]["depart"])
        group=("shifted" if vid in shifted else
               "unshifted_edge_overlap" if vid in overlap else "unshifted_no_edge_overlap")
        for edge,t_exit in zip(info["route"],exit[vid]):
            err=actual-intended
            values[group].append(err)
            if vid in shifted:
                examples.append((abs(err),vid,edge,round(intended,2),round(actual,2),round(err,2)))
            intended+=ff[edge]
            actual=t_exit
    return {"groups":{g:{"n":len(a),"mean_error_s":statistics.mean(a),
                         "median_error_s":statistics.median(a),
                         "p95_error_s":sorted(a)[int(.95*(len(a)-1))]}
                      for g,a in values.items()},
            "top_30_shifted_road_clock_errors":sorted(examples,reverse=True)[:30]}

def harm_stats(ids,b,c,preferred):
    delta=sorted(float(c[v]["arrival"])-float(b[v]["arrival"]) for v in ids)
    def percentile(a,p):
        if not a: return None
        pos=(len(a)-1)*p
        low=int(math.floor(pos));high=int(math.ceil(pos))
        return a[low]+(a[high]-a[low])*(pos-low)
    return {"n":len(delta),"sum_C_minus_B_network_s":round(sum(delta),5),
            "mean_s":statistics.mean(delta) if delta else None,
            "median_s":percentile(delta,.5),"p90_s":percentile(delta,.9),
            "p95_s":percentile(delta,.95),
            "minimum_s":delta[0] if delta else None,"maximum_s":delta[-1] if delta else None,
            "helped":sum(x<0 for x in delta),"harmed":sum(x>0 for x in delta),
            "unchanged":sum(x==0 for x in delta),
            "harm_gt30_s":sum(x>30 for x in delta)}

def analyze(source,prepared,obs):
    meta=json.loads((prepared/"source_and_control_manifest.json").read_text())
    gates={k:json.loads((obs/k/"control_gate.json").read_text()) for k in ("Bstar","Cstar")}
    require(all(g["status"]=="CONTROL_PASS" for g in gates.values()),"control gate incomplete")
    canonical=meta["fixed_vehicle_manifest"]
    b=parse_tripinfo(obs/"Bstar/tripinfo.xml");c=parse_tripinfo(obs/"Cstar/tripinfo.xml")
    pref={v:info["preferred"] for v,info in canonical.items()}
    shifted=set(meta["changed_requested_departure"]);eligible={v for v,x in canonical.items() if x["eligible"]}
    edge_set={e for vid in shifted for e in canonical[vid]["route"]}
    overlap={vid for vid in canonical if vid not in shifted and
             edge_set.intersection(canonical[vid]["route"])}
    groups={"all":set(canonical),"shifted":shifted,"unshifted":set(canonical)-shifted,
            "eligible":eligible,"nonparticipants":set(canonical)-eligible,
            "unshifted_edge_overlap":overlap,
            "unshifted_no_edge_overlap":set(canonical)-shifted-overlap}
    harm={g:harm_stats(ids,b,c,pref) for g,ids in groups.items()}
    net=harm["all"]["sum_C_minus_B_network_s"]
    req=gates["Cstar"]["requested_predeparture_s"]-gates["Bstar"]["requested_predeparture_s"]
    insert=gates["Cstar"]["insertion_delay_s"]-gates["Bstar"]["insertion_delay_s"]
    duration=gates["Cstar"]["in_network_duration_s"]-gates["Bstar"]["in_network_duration_s"]
    require(abs(net-(req+insert+duration))<.1,"network bridge fails")
    fb=frames(obs/"Bstar/fcd.xml");fc=frames(obs/"Cstar/fcd.xml")
    chronology=first_diff(fb,fc,shifted,overlap)
    times=[x["C_requested"] for v,x in canonical.items() if v in shifted]
    first_intervention=min(x["B_requested"] for v,x in canonical.items() if v in shifted)
    first_obs=chronology["first_unshifted"]
    chronology["first_original_shift_B_time_s"]=first_intervention
    chronology["any_unshifted_divergence_before_first_affected_B_departure"]=(
        first_obs is not None and first_obs["time_s"]<first_intervention)
    ffc=freeflows(source/"source/network.net.xml")
    clocks={k:clock_errors(obs,k,canonical,ffc,shifted,overlap) for k in ("Bstar","Cstar")}
    sb,lb=lane_counts(fb);sc,lc=lane_counts(fc)
    lanes=sorted([{"lane":lane,"B_stopped_vehicle_samples":sb[lane],
                   "C_stopped_vehicle_samples":sc[lane],"delta_stopped":sc[lane]-sb[lane],
                   "B_slow_vehicle_samples":lb[lane],"C_slow_vehicle_samples":lc[lane],
                   "delta_slow":lc[lane]-lb[lane]}
                  for lane in set(sb)|set(sc)|set(lb)|set(lc)],
                 key=lambda x:-abs(x["delta_stopped"]))
    stopped={k:sum(float(v["waitingTime"]) for v in info.values()) for k,info in
             (("Bstar",b),("Cstar",c))}
    timeloss={k:sum(float(v["timeLoss"]) for v in info.values()) for k,info in
             (("Bstar",b),("Cstar",c))}
    result={"classification":"VALID_SINGLE_SEED_DEVELOPMENT_WITH_RESIDUAL_STOCHASTIC_UNCERTAINTY",
            "seed":SEED,
            "primary_Cstar_minus_Bstar_network_s":net,
            "mean_per_driver_s":net/1000,
            "predicted_legacy_C_minus_B_s":-50.62634989192884,
            "contrast_components_s":{"predeparture":req,"insertion":insert,"in_network":duration},
            "sum_stopped_waiting_seconds":stopped,"sum_time_loss_seconds":timeloss,
            "matched_driver_harm":harm,"chronology":chronology,
            "top_25_lane_stopped_differences":lanes[:25],
            "clock_error_vs_nominal_model":clocks,
            "original_input_digests":meta["original_file_digests"],
            "new_input_digests":meta["prepared_routes"],
            "control_gates":gates,
            "limits":["One previously inspected development seed; no independent replication.",
              "Same SUMO random seed and per-ID speedFactor cannot guarantee identical remaining stochastic events.",
              "FCD sampled at SUMO step; earliest observed divergence not necessarily a causal mediator.",
              "Original B/C +618 network-s remains confounded historical evidence.",
              "The model's -50.626 predicted advantage is not a independently validated forecast.",
              "Changing one selected 12-driver schedule is not cooperative policy qualification."]}
    save(obs/"consolidated_diagnostics.json",result)
    lines=[
       "# T1 B*/C* ID-locked development: machine-computed checkpoint",
       "",
       "**Development only; current T1 NO-GO unchanged.**",
       "**Residual RNG uncertainty:** fixing per-ID speed factors does not prove all remaining random driving events identical.",
       "",
       "| Outcome | C*−B* network-seconds |",
       "|---|---:|",
       f'| Total preferred-to-arrival | {net:+.3f} |',
       f'| Intentional departure waiting | {req:+.3f} |',
       f'| SUMO insertion delay | {insert:+.3f} |',
       f'| In-network duration | {duration:+.3f} |',
       f'| Stopped waiting (secondary) | {stopped["Cstar"]-stopped["Bstar"]:+.3f} |',
       f'| Time loss (secondary) | {timeloss["Cstar"]-timeloss["Bstar"]:+.3f} |',
       "",
       "| Group | n | Aggregate Δ network-s | Helped | Harmed | Unchanged | >30s harm |",
       "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for g in ("shifted","unshifted","eligible","nonparticipants","unshifted_edge_overlap","unshifted_no_edge_overlap"):
        s=harm[g]
        lines.append(f'| {g} | {s["n"]} | {s["sum_C_minus_B_network_s"]:+.3f} | {s["helped"]} | {s["harmed"]} | {s["unchanged"]} | {s["harm_gt30_s"]} |')
    lines += ["", "## First observed movement divergences",
      "",
      f'- Earliest originally changed requested departure in B: {first_intervention:.3f}s.',
      f'- First shifted-driver FCD discrepancy: {chronology["first_shifted"]}.',
      f'- First unshifted-driver FCD discrepancy: {chronology["first_unshifted"]}.',
      f'- Unshifted discrepancy before earliest original changed departure: {chronology["any_unshifted_divergence_before_first_affected_B_departure"]}.',
      "",
      "## Leading lane stopped-vehicle-sample changes (descriptive, not a causal bottleneck)",
      "",
      "| Lane | Δ stopped vehicle-samples | Δ slow-moving samples |",
      "|---|---:|---:|",
    ]
    for item in lanes[:15]:
        lines.append(f'| {item["lane"]} | {item["delta_stopped"]:+d} | {item["delta_slow"]:+d} |')
    lines+=["","## Scientific boundary",
      "No unique physical cause, confirmed forecasting skill, cooperative efficacy, cross-seed uncertainty estimate, real-world or human-compliance claim follows from these observations.",
      "Full input/output hashes, individual harms, clock errors, and earliest-30 chronology are in consolidated_diagnostics.json.", ""]
    (obs/"generated_checkpoint.md").write_text("\n".join(lines))
    print(json.dumps({"status":result["classification"],"contrast_s":net,
                      "components":result["contrast_components_s"],
                      "nonparticipants":harm["nonparticipants"],
                      "first_unshifted":first_obs},sort_keys=True))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("mode",choices=["preflight","run","gate","analyze"])
    p.add_argument("--source",default="source-original")
    p.add_argument("--prepared",default="idlocked-inputs")
    p.add_argument("--observed",default="idlocked-observation")
    p.add_argument("--arm",choices=["Bstar","Cstar"])
    a=p.parse_args()
    source=Path(a.source);prepared=Path(a.prepared);obs=Path(a.observed)
    if a.mode=="preflight":
        print(json.dumps({"sumo":sumo_flags(),"static_controls":emit(source,prepared)["status"]}))
    elif a.mode=="run":
        require(a.arm is not None,"--arm is required")
        simulate(source,prepared,obs,a.arm)
    elif a.mode=="gate":
        require(a.arm is not None,"--arm is required")
        gate_arm(source,prepared,obs,a.arm)
    else:
        analyze(source,prepared,obs)
if __name__=="__main__":
    main()
