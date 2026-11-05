#!/usr/bin/env python3
"""Post-Experiment-007 C1: controlled E3 priority intervention on already-inspected seeds.
Eight-arm maximum; physically preserved original routes/seed/physics except the
single frozen E3 priority-pair change. No predictor, no route generator, no Test B.
Execution is gated: C2 all four no-op outcomes MUST match original before any
J1 modified-network arm. Script accepts only the prospectively frozen lock.
"""
from __future__ import annotations
import argparse,csv,gzip,json,math,pathlib,subprocess,sys,statistics,xml.etree.ElementTree as ET
from collections import Counter,defaultdict
P=pathlib.Path
sys.path.insert(0,str(P(__file__).resolve().parents[1]/"replay"))
from e1v2_four_arm_instrumented import (
 assert_sources,compare_one,scheduled,tripinfo,safety,sha,make_add
)
SOURCE_RUN=41966516110
ARM_ORDER=((6112,"I"),(6112,"probe2"),(6113,"I"),(6113,"probe2"))
EXPECTED={6112:3219.0,6113:-3883.0}
WHO={6112:"veh0142",6113:"veh0038"}
MAX_ARM=512*1024*1024
def readj(p):return json.loads(P(p).read_text())
def savej(p,value):
    p=P(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,sort_keys=True)+"\n")
def writecsv(p,rows,fields=None):
    p=P(p);p.parent.mkdir(parents=True,exist_ok=True)
    fieldnames=fields or (list(rows[0]) if rows else ["empty"])
    with p.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fieldnames,extrasaction="ignore")
        w.writeheader();w.writerows(rows)
def validated_lock(lock,feas):
    lock=readj(lock);result=readj(P(feas)/"C0_C1_verdict.json")
    if lock["status"]!="FROZEN_BEFORE_ANY_C2_C3_SUMO_OUTCOME":raise RuntimeError("Unfrozen source intervention")
    if result["status"]!="C0_C1_ELIGIBLE_TO_FREEZE_EXECUTABLE_PROTOCOL" or result.get("C1_lock_match")!="PASS":
        raise RuntimeError("C0/C1 source-backed E3 lock did not pass")
    if result["patch_sha256"]!=lock["patch_sha256"] or result["network_shas_by_seed"]!=lock["networks"]:
        raise RuntimeError("Network SHA from physical-conversion feasibility differs from frozen lock")
    for seed in (6112,6113):
        for j,label in (("J0","J0_noop"),("J1","J1_modified")):
            p=P(feas)/"networks"/("%d-%s.net.xml"%(seed,j))
            if not p.is_file() or sha(p)!=lock["networks"][str(seed)][label]:
                raise RuntimeError("Changed/new network SHA: "+str(p))
    return lock
def add_observations(out):
    root=ET.Element("additional")
    ET.SubElement(root,"edgeData",id="c1-edge",file=str((out/"edgeData.xml.gz").resolve()),
                  period="5",withInternal="true",excludeEmpty="false")
    ET.SubElement(root,"laneData",id="c1-lane",file=str((out/"laneData.xml.gz").resolve()),
                  period="5",withInternal="true",excludeEmpty="false")
    p=out/"additional.xml";ET.ElementTree(root).write(p,encoding="utf-8",xml_declaration=True)
    return p
def execute_arm(source,feas,seed,arm,j,out):
    if (seed,arm) not in ARM_ORDER or j not in ("J0","J1"):
        raise RuntimeError("Unfrozen arm attempted")
    out.mkdir(parents=True,exist_ok=False)
    net=P(feas)/"networks"/("%d-%s.net.xml"%(seed,j))
    folder=P(source)/("seed-"+str(seed))
    src=folder/"observations"/arm
    route=folder/"routes"/(arm+".rou.xml")
    add=add_observations(out)
    cmd=["sumo","-n",str(net.resolve()),"-r",str(route.resolve()),
         "--tripinfo-output",str((out/"tripinfo.xml").resolve()),
         "--statistic-output",str((out/"statistics.xml").resolve()),
         "--collision-output",str((out/"collisions.xml").resolve()),
         "--seed",str(seed),"--no-step-log","true",
         "--log",str((out/"sumo.log").resolve()),
         "--fcd-output",str((out/"fcd.xml.gz").resolve()),
         "--vehroute-output",str((out/"vehroute.xml.gz").resolve()),
         "--vehroute-output.exit-times","true",
         "--additional-files",str(add.resolve())]
    original=readj(src/"command.json")
    assert original[0]=="sumo"
    for flag in ("--seed","--no-step-log"):
        assert original[original.index(flag)+1]==cmd[cmd.index(flag)+1]
    savej(out/"source_command_and_run.json",{"command":cmd,"original_command":original,
         "original_routes_sha256":sha(route),"source_network_sha256":sha(folder/"network.net.xml"),
         "applied_network_sha256":sha(net),
         "source_run":SOURCE_RUN,"seed":seed,"arm":arm,"priority_setting":j})
    record={"seed":seed,"arm":arm,"setting":j,"status":"ATTEMPTED","g2":"NOT_APPLICABLE","g3":"NOT_VERIFIED"}
    try:
        with (out/"sumo-stage.log").open("w") as log:
            proc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
        if proc.returncode:raise RuntimeError("SUMO returncode "+str(proc.returncode))
        required=("fcd.xml.gz","vehroute.xml.gz","edgeData.xml.gz","laneData.xml.gz",
                  "tripinfo.xml","statistics.xml","collisions.xml")
        for name in required:
            p=out/name
            if not p.exists() or p.stat().st_size<=10:
                raise RuntimeError("Missing mandatory instrumented channel: "+name)
        size=sum((out/k).stat().st_size for k in ("fcd.xml.gz","vehroute.xml.gz","edgeData.xml.gz","laneData.xml.gz"))
        if size>MAX_ARM:raise RuntimeError("Compressed observation exceeds frozen 512MiB per-arm budget")
        record["compressed_observations_bytes"]=size
        record["observational_sha256"]={name:sha(out/name) for name in required}
        if j=="J0":
            g2=compare_one(src,out,scheduled(folder/"trips.xml"))
            record["g2"]="PASS"
            record["g2_checks"]=g2
        else:
            t=tripinfo(out/"tripinfo.xml")
            assert len(t)==1000 and set(t)==set(scheduled(folder/"trips.xml"))
            report=safety(out)
            if report.get("collision_events")!=0 or report.get("collisions") not in (None,"0"):
                raise RuntimeError("INVALID INTERVENTION: simulator collision output nonzero")
            record["g2"]="NOT_APPLICABLE_CHANGED_PHYSICS"
            record["safety"]=report
        record["status"]="COMPLETE"
    except Exception as e:
        record["status"]="INVALID";record["error"]=repr(e)
    savej(out/"attempt.json",record)
    print(json.dumps({k:v for k,v in record.items() if k!="observational_sha256"},indent=2)[:4500],flush=True)
    if record["status"]!="COMPLETE":raise RuntimeError(record["error"])
    return record
def source_check(source):
    return assert_sources(source)
def do_execution(source,feas,lock,out):
    out=P(out);out.mkdir(parents=True,exist_ok=True)
    record={"phase":"C0_C1","status":"INCOMPLETE","original_verdict":"DEVELOPMENT_NOT_QUALIFIED",
            "validation":"NOT_STARTED","Test_B":"NOT_RUN","arms_attempted":[]}
    try:
        frozen=validated_lock(lock,feas);source_check(source)
        record["phase"]="C2_NOOP"
        # The frozen no-op network controls are all completed and independently
        # checked BEFORE the first modified-priority SUMO invocation.
        for seed,arm in ARM_ORDER:
            p=out/("%d_%s_J0"%(seed,arm))
            attempt=execute_arm(source,feas,seed,arm,"J0",p)
            record["arms_attempted"].append({k:attempt[k] for k in ("seed","arm","setting","status","g2")})
            savej(out/"run-state.json",record)
        record["C2"]="PASS";record["phase"]="C3_PRIORITY_MODIFIED"
        savej(out/"run-state.json",record)
        for seed,arm in ARM_ORDER:
            p=out/("%d_%s_J1"%(seed,arm))
            attempt=execute_arm(source,feas,seed,arm,"J1",p)
            record["arms_attempted"].append({k:attempt[k] for k in ("seed","arm","setting","status","g2")})
            savej(out/"run-state.json",record)
        record["C3"]="PASS";record["phase"]="C4_AUDIT"
        savej(out/"run-state.json",record)
        result=evaluate(source,feas,frozen,out)
        record["C4"]="PASS";record["status"]=result["status"]
        record["result"]=result
    except Exception as e:
        record["status"]="INTEGRITY_OR_FEASIBILITY_STOP"
        record["error"]=repr(e)
    savej(out/"run-state.json",record)
    if record["status"]=="INTEGRITY_OR_FEASIBILITY_STOP":
        (out/"STOP_REPORT.md").write_text(
            "# C1 controlled E3 experiment: mandatory gate stopped execution\n\n"
            "**Study status:** C2/C3/C4 INCOMPLETE or INVALID; no scientific causal conclusion.\n\n"
            "Gate: "+record["phase"]+"\n\nError: "+record.get("error","unavailable")+
            "\n\nOriginal E1-v2 D1 DEVELOPMENT_NOT_QUALIFIED, independent validation and Test B NOT RUN. "
            "All attempted arms were retained. Do not rerun different seeds, relax tolerance or alter E3 physics after outcomes.\n")
        raise RuntimeError("C1 execution stopped at "+record["phase"]+": "+record.get("error",""))
    print("PASS: bounded C0-C4 case-study completed. Historical E1-v2 NO-GO unchanged.",flush=True)
def percentile(xs,pct):
    xs=sorted(xs)
    if not xs:return None
    k=(len(xs)-1)*pct/100
    lo=int(k);hi=min(len(xs)-1,lo+1)
    return xs[lo]+(xs[hi]-xs[lo])*(k-lo)
def read_first_lane_samples(path,via):
    # Compare *observed* 1-second sampled internal-lane crossing entries
    # plus cumulative near-stop exposure on incoming E3 roads, 120-300s.
    counts=defaultdict(Counter);last_by_vehicle={}
    waiting=Counter();stop=Counter();samples=0
    with gzip.open(path,"rb") as f:
        for _,node in ET.iterparse(f,events=("end",)):
            if node.tag!="timestep":continue
            t=float(node.get("time"))
            if 120<=t<300:
                for v in node.findall("vehicle"):
                    vid=v.get("id");lane=v.get("lane");speed=float(v.get("speed"))
                    if lane in via and last_by_vehicle.get(vid)!=lane:
                        counts[lane][t]+=1
                    if lane in ("D3E3_0","E4E3_0"):
                        samples+=1
                        if speed<=.1:stop[lane]+=1
                    last_by_vehicle[vid]=lane
            node.clear()
    return {"crossing_counts":{lane:dict(records) for lane,records in counts.items()},
            "near_stop_samples_on_E3_approaches":dict(stop),
            "approach_presence_samples":samples}
def e3_approach_wait(path):
    waiting=Counter();counts=Counter()
    with gzip.open(path,"rb") as f:
        for _,node in ET.iterparse(f,events=("end",)):
            if node.tag!="interval":continue
            b=float(node.get("begin"));e=float(node.get("end"))
            if 120<=b<300:
                for entry in node.findall("edge"):
                    if entry.get("id") not in ("D3E3","E4E3"):continue
                    key=entry.get("id")
                    val=entry.get("waitingTime")
                    ss=entry.get("sampledSeconds")
                    if val is None and ss is not None and float(ss)==0:
                        val="0"
                    if val is not None:waiting[key]+=float(val)
                    counts[key]+=float(entry.get("left") or 0)
            node.clear()
    return {"waiting_s":dict(waiting),"left_counts":dict(counts)}
def evaluate(source,feas,lock,out):
    allarms={};row=[];cases=[];drivers=[]
    for seed,arm in ARM_ORDER:
        sched=scheduled(P(source)/("seed-"+str(seed))/"trips.xml")
        for j in ("J0","J1"):
            folder=out/("%d_%s_%s"%(seed,arm,j))
            original=readj(folder/"attempt.json")
            if original["status"]!="COMPLETE":raise RuntimeError("Missing physical arm for C4")
            tr=tripinfo(folder/"tripinfo.xml")
            if len(tr)!=1000 or tr.keys()!=sched.keys():raise RuntimeError("C4 incomplete cohort")
            cc=sum(tr[v]["arrival"]-sched[v] for v in sched)
            ws=sum(tr[v]["waitingTime"] for v in sched)
            nonp=[v for v in sched if int(v[-4:])%2]
            nonp_c=sum(tr[v]["arrival"]-sched[v] for v in nonp)
            outj=read_first_lane_samples(folder/"fcd.xml.gz",(":E3_14_0",":E3_1_0"))
            flow=e3_approach_wait(folder/"edgeData.xml.gz")
            allarms[(seed,arm,j)]={"trip":tr,"cost":cc,"waiting":ws,
                 "nonparticipant_cost":nonp_c,"local_fcd":outj,"local_edge":flow}
            row.append({"seed":seed,"route":arm,"physical_state":j,
                "all_driver_scheduled_to_arrival_network_s":cc,
                "all_driver_waiting_vehicle_s":ws,
                "nonparticipant_network_s":nonp_c,
                "E3_approach_window_waiting_vehicle_s":sum(flow["waiting_s"].values()),
                "E3_approach_nearstop_samples":sum(outj["near_stop_samples_on_E3_approaches"].values()),
                "E3_selected_movement_first_samples":sum(sum(times.values()) for times in outj["crossing_counts"].values())})
    assert len(row)==8
    for seed in (6112,6113):
        sched=scheduled(P(source)/("seed-"+str(seed))/"trips.xml")
        t={}
        for j in ("J0","J1"):
            a=allarms[(seed,"I",j)];b=allarms[(seed,"probe2",j)]
            diffs={v:b["trip"][v]["arrival"]-a["trip"][v]["arrival"] for v in sched}
            selfv=diffs[WHO[seed]]
            external=sum(v for i,v in diffs.items() if i!=WHO[seed])
            optout=sum(v for i,v in diffs.items() if int(i[-4:])%2)
            harm=sum(v>30 for v in diffs.values())
            npharm=sum(v>30 for i,v in diffs.items() if int(i[-4:])%2)
            t[j]={"delta":b["cost"]-a["cost"],"self":selfv,"external":external,
                  "nonparticipants":optout,"harm_gt30":harm,"nonparticipant_harm_gt30":npharm,
                  "p90_delta_s":percentile(list(diffs.values()),90),
                  "p95_delta_s":percentile(list(diffs.values()),95),
                  "waiting_delta":b["waiting"]-a["waiting"]}
            assert abs(t[j]["delta"]-selfv-external)<.1
            for vid,val in diffs.items():
                drivers.append({"seed":seed,"physical_state":j,"vehicle":vid,
                    "changed_target":int(vid==WHO[seed]),"nonparticipant":int(int(vid[-4:])%2==1),
                    "route_probe2_minus_I_arrival_seconds":val})
        if abs(t["J0"]["delta"]-EXPECTED[seed])>.10001:
            raise RuntimeError("C4 original J0 route contrast not reproduced")
        psi=t["J1"]["delta"]-t["J0"]["delta"]
        first_stage=[]
        for arm in ("I","probe2"):
            a=allarms[(seed,arm,"J0")];b=allarms[(seed,arm,"J1")]
            localA=a["local_fcd"];localB=b["local_fcd"]
            for lane in (":E3_14_0",":E3_1_0"):
                aa=localA["crossing_counts"].get(lane,{})
                bb=localB["crossing_counts"].get(lane,{})
                if aa!=bb:first_stage.append({"route":arm,"measurement":"sampled_entering_internal_lane","lane":lane})
            if a["local_edge"]["waiting_s"]!=b["local_edge"]["waiting_s"]:
                first_stage.append({"route":arm,"measurement":"E3_approach_waiting", "lane":"two approaches"})
            if a["local_fcd"]["near_stop_samples_on_E3_approaches"]!=b["local_fcd"]["near_stop_samples_on_E3_approaches"]:
                first_stage.append({"route":arm,"measurement":"E3_inbound_FCD_nearstop","lane":"two approaches"})
        cases.append({"seed":seed,"J0":t["J0"],"J1":t["J1"],
            "psi_network_s":psi,
            "materiality_screen_abs_psi_gte_10pct_6112":abs(psi)>=.1*abs(EXPECTED[6112]) if seed==6112 else "not_primary",
            "E3_first_stage_change_found":bool(first_stage),
            "first_stage_evidence":first_stage})
    active=any(c["E3_first_stage_change_found"] for c in cases)
    result={"status":"CASE_LEVEL_EFFECT_MODIFICATION_DESCRIPTIVE" if active else "MANIPULATION_INACTIVE",
            "C0":"PASS","C1":"PASS","C2":"PASS","C3":"PASS","C4":"PASS",
            "new_sumo_arms":8,"source_seeds":[6112,6113],
            "original_e1v2_d1":"DEVELOPMENT_NOT_QUALIFIED",
            "independent_validation":"NOT_STARTED","Test_B":"NOT_RUN",
            "causal_scope":"Only effect of frozen localized SUMO E3 priority intervention on route-swap response in two retrospectively chosen simulator cases",
            "not_identified":"Unique waiting, junction or queue mediator; population accuracy; cooperative policy efficacy",
            "cases":cases,"lock_sha256":sha(P(lock["__lock_path"])) if "__lock_path" in lock else None}
    writecsv(out/"C4_all_8_arm_costs.csv",row)
    writecsv(out/"C4_matched_driver_route_effects.csv",drivers)
    savej(out/"C4_scientific_verdict.json",result)
    summary=["# C1 controlled junction priority — case-level physical effect modification",
        "",
        "## Why this matters to the research",
        "The central project asks whether voluntary route coordination can improve all-driver traffic time against equally informed independent routing while protecting individuals. A credible collective optimizer first needs prospective predictions of route-choice externalities. This experiment tests one *physical effect modifier* of existing route choices, not cooperative policy performance or estimator skill.",
        "",
        "**Status:** "+result["status"]+"; original E1-v2 D1 DEVELOPMENT_NOT_QUALIFIED unchanged; independent validation and Test B NOT RUN.",
        "**Design:** 2 pre-inspected seeds × original independent/probe2 planned routes × original/no-op or E3 priority-reversed rule. Exactly eight new SUMO arms, original 1,000 trips per arm.",
        "**Source-pinned priority intervention:** "+lock["chosen"]["new_prohibition"]["prohibitor"]+" gains priority over "+lock["chosen"]["new_prohibition"]["prohibited"]+" at E3. No other road/junction semantic changes in C1. Four no-op J0 replays met G2 individual <=0.02s and aggregate <=0.1 network-s tolerances before the first changed-physics J1 arm.",
        "",
        "## Primary whole-network effect-modification outcome",
        "C(s,R,J) = sum over all 1,000 (arrival - original scheduled departure). D(s,J) = C(s,probe2,J)-C(s,I,J). Psi(s) = D(s,J1)-D(s,J0).",
        "",
        "| Seed | D(J0), original physics | D(J1), E3 modified | Psi network-s | Nonparticipants D(J0) → D(J1) | Local manipulation observed |",
        "|---|---:|---:|---:|---:|---|"]
    for x in cases:
        summary.append("| {seed} | {d0:+,.1f} | {d1:+,.1f} | {psi:+,.1f} | {n0:+,.1f} → {n1:+,.1f} | {manip} |".format(
            seed=x["seed"],d0=x["J0"]["delta"],d1=x["J1"]["delta"],psi=x["psi_network_s"],
            n0=x["J0"]["nonparticipants"],n1=x["J1"]["nonparticipants"],
            manip="Yes, at recorded sampling" if x["E3_first_stage_change_found"] else "No first stage observed"))
    summary+=["","## Interpretation and original limitations",
        "The controlled factor can identify how the local E3 priority rule affects the *marginal response to a route swap* on the selected synthetic network, assuming the source and no-op identity gates hold. It does not randomize queue waiting or prove that E3 initiated the original network-wide divergence; in the original passive replay, the earliest driver divergence preceded the prominent D3E3 hotspot.",
        "The reported 10% of |D(6112,J0)| screen (about 322 network-seconds) is exploratory, not a population significance test, and does not substitute for development or independent validation. Inspect both directions, exceptions, speed/queue data, individual p90/p95 and nonparticipant effects. Waiting is not added twice to travel-time cost.",
        "The exact candidate pair was selected from previously inspected seed-6112 I approach presence and frozen before all eight outcome-generating SUMO arms. Both seeds were previously inspected; no new independent predictor skill is claimed.",
        "## Evidence",
        "Original reference run 41966516110; original instrumented trajectory run 42113107379; C0/C1 preflight run 42125134835. Complete source manifest, frozen rule, original/no-op/changed network hashes, all eight tripinfo/FCD/vehroute/detector archives and SHA256 ledger accompany this report.",
        "",
        "**Scientific conclusion:** A case-level effect-modifier result may motivate a new prospective modeling hypothesis but does not establish cooperative traffic superiority. The E1-v2 D1 NO-GO and unexecuted Test B remain unchanged.",
        ]
    (out/"C1_FINAL_SCIENTIFIC_REPORT.md").write_text("\n".join(summary)+"\n")
    return result
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True);p.add_argument("--feas",required=True)
    p.add_argument("--lock",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    do_execution(P(a.source),P(a.feas),P(a.lock),P(a.out))
if __name__=="__main__":main()
