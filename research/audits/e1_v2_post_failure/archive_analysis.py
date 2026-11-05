#!/usr/bin/env python3
"""F0-F5 historical E1-v2 audit. Archive-only: never invokes SUMO or a predictor."""
import argparse,csv,gzip,hashlib,json,math,pathlib,statistics,xml.etree.ElementTree as ET
from collections import Counter,defaultdict

SEEDS=tuple(range(6101,6107))+tuple(range(6111,6115))
ARMS=("I","probe0","probe1","probe2","probe3","bundle")
FOCUS={(6112,"probe2"),(6113,"probe2"),(6111,"probe3"),(6114,"probe2")}
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda:f.read(1048576),b""): h.update(b)
    return h.hexdigest()
def jsonread(p):return json.loads(p.read_text())
def out_csv(p,rows):
    if not rows:return
    with p.open("w",newline="") as f:
        w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
def trip(p):
    o={}
    for x in ET.parse(p).getroot().findall("tripinfo"):
        i=x.get("id")
        assert i not in o
        o[i]={k:float(x.get(k)) for k in ("depart","arrival","duration")}
    return o
def roads(p):
    return {v.get("id"):tuple(v.find("route").get("edges").split()) for v in ET.parse(p).getroot().findall("vehicle")}
def detect(p,external):
    data={};fields=Counter();internal=0;times=[];short_bins=0;last_end=0
    with gzip.open(p,"rb") as f:
        for event,x in ET.iterparse(f,events=("end",)):
            if x.tag!="interval":continue
            begin=float(x.get("begin"));end=float(x.get("end"))
            assert end>begin and end-begin<=5.001,(p,begin,end)
            if end-begin<4.999:short_bins+=1
            last_end=max(last_end,end)
            times.append(begin)
            for e in x.findall("edge"):
                name=e.get("id")
                if name not in external:
                    internal+=1;continue
                key=(name,begin)
                assert key not in data
                d={"_end":end}
                for field in ("entered","left","departed","arrived","waitingTime","sampledSeconds","speed","occupancy"):
                    v=e.get(field)
                    if v is not None:
                        d[field]=float(v);fields[field]+=1
                data[key]=d
            x.clear()
    assert times and data
    return data,dict(intervals=len(times),start=min(times),end=last_end,short_final_or_partial_intervals=short_bins,external_rows=len(data),internal_rows=internal,fields=dict(fields))
def addrec(rows,path):
    path.parent.mkdir(parents=True,exist_ok=True)
    out_csv(path,rows)
def main(root,out,ledger=None):
    files=sorted(p for p in root.rglob("*") if p.is_file())
    assert len(files)==695,("member count",len(files))
    lookup={p.relative_to(root).as_posix():p for p in files}
    if ledger:
        with open(ledger,newline="") as f:members=list(csv.DictReader(f))
        assert len(members)==695
        for m in members:
            p=lookup[m["member"]]
            assert p.stat().st_size==int(m["bytes"]) and sha(p)==m["sha256"],m["member"]
    verdict=jsonread(root/"development-verdict.json")
    assert verdict["scientific_status"]=="DEVELOPMENT_NOT_QUALIFIED"
    assert verdict["new_validation"]=="NOT_STARTED" and verdict["Test_B"]=="NOT_RUN"
    assert verdict["n_sumo_arms"]==60 and verdict["n_driver_tripinfos"]==60000
    lockall=jsonread(root/"all-prediction-locks.json")
    assert lockall["status"]=="FROZEN_BEFORE_ANY_SUMO_OUTCOME"
    assert lockall["locked_seeds"]==list(SEEDS)
    out.mkdir(parents=True,exist_ok=True)
    f1=[];f2count=0;f3=[];f4=[];cov=[];examples=[]
    f2file=gzip.open(out/"F2_edge_5second.csv.gz","wt",newline="")
    f2fields=["seed","arm","edge","begin_s","delta_entered","delta_left",
              "delta_waiting_vehicle_s","delta_sampled_vehicle_s",
              "baseline_occupancy","changed_occupancy","baseline_speed","changed_speed"]
    f2writer=csv.DictWriter(f2file,fieldnames=f2fields);f2writer.writeheader()
    for seed in SEEDS:
        folder=root/("seed-"+str(seed))
        man=jsonread(folder/"scenario-manifest.json")
        lk=jsonread(folder/"prediction-lock.json")
        obs=jsonread(folder/"observations-summary.json")["observations"]
        assert man["seed"]==lk["seed"]==seed
        for p,hashv in ((folder/"network.net.xml",man["network_sha256"]),
                         (folder/"trips.xml",man["demand_sha256"]),
                         (folder/"predictions/predictions.json",lk["prediction_sha256"])):
            assert sha(p)==hashv
        pred=jsonread(folder/"predictions/predictions.json")
        assert pred["observed_outcomes_used"] is False and len(pred["rows"])==5
        pr={r["arm"]:r for r in pred["rows"]}
        net=ET.parse(folder/"network.net.xml").getroot()
        external={e.get("id") for e in net.findall("edge") if e.get("function")!="internal" and not e.get("id","").startswith(":")}
        assert len(external)==360
        junc={j.get("id") for j in net.findall("junction") if j.get("type")=="priority"}
        assert len(junc)==100
        inc=defaultdict(set);outgoing=defaultdict(set)
        for e in net.findall("edge"):
            if e.get("id") in external:
                inc[e.get("to")].add(e.get("id"));outgoing[e.get("from")].add(e.get("id"))
        schedules={x.get("id"):float(x.get("depart")) for x in ET.parse(folder/"trips.xml").getroot().findall("trip")}
        assert len(schedules)==1000
        route={};tripinfo={};elapsed={};edge={};edge_sum={}
        for arm in ARMS:
            rp=folder/"routes"/(arm+".rou.xml")
            tp=folder/"observations"/arm/"tripinfo.xml"
            assert sha(rp)==man["arm_route_sha256"][arm]
            assert sha(tp)==obs[arm]["tripinfo_sha256"]
            route[arm]=roads(rp);tripinfo[arm]=trip(tp)
            assert schedules.keys()==route[arm].keys()==tripinfo[arm].keys()
            elapsed[arm]={i:tripinfo[arm][i]["arrival"]-schedules[i] for i in schedules}
            for i,x in tripinfo[arm].items():
                assert abs((x["arrival"]-x["depart"])-x["duration"])<.06
            assert abs(sum(elapsed[arm].values())-obs[arm]["network_total_s"])<.12
            edge[arm],coverage=detect(folder/"observations"/arm/"edgeData.xml.gz",external)
            accum=defaultdict(Counter)
            for (eid,t),vals in edge[arm].items():
                for field in ("entered","left","waitingTime"):
                    if field in vals:accum[eid][field]+=vals[field]
            edge_sum[arm]=accum
            coverage.update(seed=seed,arm=arm,trip_records=1000,
                            laneData_gz_bytes=(folder/"observations"/arm/"laneData.xml.gz").stat().st_size,
                            fcd_files=sum(1 for p in (folder/"observations"/arm).glob("*fcd*")))
            cov.append(coverage)
        for idx in range(4):
            arm="probe"+str(idx)
            changed={i for i in schedules if route[arm][i]!=route["I"][i]}
            assert changed=={man["probes"][idx]["target_vehicle_id"]}==set(pr[arm]["target_ids"])
        bundle=set(man["bundle_target_ids"])
        assert bundle=={i for i in schedules if route["bundle"][i]!=route["I"][i]}
        assert bundle==set(pr["bundle"]["target_ids"])
        for arm in ARMS[1:]:
            targets=set(pr[arm]["target_ids"])
            delta={i:elapsed[arm][i]-elapsed["I"][i] for i in schedules}
            selfc=sum(x for i,x in delta.items() if i in targets)
            others=sum(x for i,x in delta.items() if i not in targets)
            allc=sum(delta.values())
            nonp=sum(x for i,x in delta.items() if int(i[-4:])%2)
            insertion=sum(tripinfo[arm][i]["depart"]-tripinfo["I"][i]["depart"] for i in schedules)
            duration=sum(tripinfo[arm][i]["duration"]-tripinfo["I"][i]["duration"] for i in schedules)
            assert abs(selfc+others-allc)<.0001 and abs(insertion+duration-allc)<.12
            v1=pr[arm]["v1"];v2=pr[arm]["v2"]
            for v in (v1,v2):
                assert v["status"]=="OK"
                b=v["per_driver_baseline_s"];a=v["per_driver_swap_s"]
                assert b.keys()==a.keys()==schedules.keys()
                assert abs(sum(a[i]-b[i] for i in schedules)-v["pred_all_delta_network_s"])<.00001
            f1.append(dict(seed=seed,partition=man["partition"],arm=arm,targets="|".join(sorted(targets)),
                observed_self_network_s=selfc,observed_external_network_s=others,
                observed_total_network_s=allc,observed_nonparticipant_network_s=nonp,
                insertion_delta_network_s=insertion,duration_delta_network_s=duration,
                harmed_gt30=sum(x>30 for x in delta.values()),
                nonparticipant_harmed_gt30=sum(x>30 for i,x in delta.items() if int(i[-4:])%2),
                v1_pred_external_network_s=v1["pred_external_delta_network_s"],
                v2_pred_external_network_s=v2["pred_external_delta_network_s"],
                v1_pred_total_network_s=v1["pred_all_delta_network_s"],
                v2_pred_total_network_s=v2["pred_all_delta_network_s"]))
            baseline=edge["I"];modified=edge[arm]
            joined=set(baseline)&set(modified)
            abswait=0.;netwait=0.;first=None;valid=0
            for key in sorted(joined,key=lambda z:(z[1],z[0])):
                a=baseline[key];b=modified[key]
                if abs(a["_end"]-b["_end"])>.001:continue
                if not {"entered","left","waitingTime"}<=a.keys() or not {"entered","left","waitingTime"}<=b.keys():continue
                dw=b["waitingTime"]-a["waitingTime"]
                de=b["entered"]-a["entered"];dl=b["left"]-a["left"]
                netwait+=dw;abswait+=abs(dw);valid+=1
                if first is None and (dw or de or dl):first=key[1]
                f2writer.writerow(dict(seed=seed,arm=arm,edge=key[0],begin_s=key[1],
                    delta_entered=de,delta_left=dl,delta_waiting_vehicle_s=dw,
                    delta_sampled_vehicle_s=b.get("sampledSeconds",float("nan"))-a.get("sampledSeconds",float("nan")),
                    baseline_occupancy=a.get("occupancy",""),changed_occupancy=b.get("occupancy",""),
                    baseline_speed=a.get("speed",""),changed_speed=b.get("speed","")))
                f2count+=1
            if (seed,arm) in FOCUS:
                examples.append(dict(seed=seed,arm=arm,observed_external_network_s=others,
                    v2_pred_external_network_s=v2["pred_external_delta_network_s"],
                    insertion_delta_network_s=insertion,duration_delta_network_s=duration,
                    edge_waiting_change_vehicle_s=netwait,abs_edge_waiting_change_vehicle_s=abswait,
                    first_aggregate_divergence_bin_s=first,matched_edge_bin_rows=valid))
            # Junction counts refer to EXTERNAL edge endpoints only, not vehicle-level turn service.
            def totals(m,edges,field):
                return sum(m[eid].get(field,0) for eid in edges)
            for junction in sorted(junc):
                entry=inc[junction];exit=outgoing[junction]
                f3.append(dict(seed=seed,arm=arm,junction=junction,inbound_edges=len(entry),outbound_edges=len(exit),
                    delta_inbound_left=totals(edge_sum[arm],entry,"left")-totals(edge_sum["I"],entry,"left"),
                    delta_outbound_entered=totals(edge_sum[arm],exit,"entered")-totals(edge_sum["I"],exit,"entered"),
                    delta_inbound_waiting_vehicle_s=totals(edge_sum[arm],entry,"waitingTime")-totals(edge_sum["I"],entry,"waitingTime"),
                    delta_outbound_waiting_vehicle_s=totals(edge_sum[arm],exit,"waitingTime")-totals(edge_sum["I"],exit,"waitingTime")))
        index={p["target_vehicle_id"]:"probe"+str(i) for i,p in enumerate(man["probes"])}
        pa,pb=(index[x] for x in man["bundle_target_ids"])
        selected={x["arm"]:x for x in f1 if x["seed"]==seed}
        def J(field):return selected["bundle"][field]-selected[pa][field]-selected[pb][field]
        common=set(edge["I"])&set(edge[pa])&set(edge[pb])&set(edge["bundle"])
        Jwait=0.;Jwaitabs=0.;nj=0
        for key in common:
            vals=[edge[k][key].get("waitingTime") for k in ("bundle",pa,pb,"I")]
            if None in vals or len({edge[k][key]["_end"] for k in ("bundle",pa,pb,"I")})!=1:continue
            delta=vals[0]-vals[1]-vals[2]+vals[3]
            Jwait+=delta;Jwaitabs+=abs(delta);nj+=1
        f4.append(dict(seed=seed,targets="|".join(man["bundle_target_ids"]),
            singleton_a=pa,singleton_b=pb,selection_overlap=man["bundle_overlap_score"],
            observed_J_all_network_s=J("observed_total_network_s"),
            observed_J_nonparticipant_network_s=J("observed_nonparticipant_network_s"),
            v1_pred_J_all_network_s=J("v1_pred_total_network_s"),
            v2_pred_J_all_network_s=J("v2_pred_total_network_s"),
            J_insertion_network_s=J("insertion_delta_network_s"),
            J_duration_network_s=J("duration_delta_network_s"),
            J_edge_waiting_vehicle_s=Jwait,abs_J_edge_waiting_vehicle_s=Jwaitabs,
            valid_joint_edge_bins=nj))
        print("ARCHIVED",seed,"bundle J=",f4[-1]["observed_J_all_network_s"],
              "forecast J=",f4[-1]["v2_pred_J_all_network_s"],flush=True)
    assert len(f1)==50 and len(f4)==10 and len(cov)==60 and len(f3)==5000
    check=[x for x in f1 if x["seed"]>=6111 and x["arm"]!="bundle"]
    mae=statistics.mean(statistics.mean(abs(x["v2_pred_external_network_s"]-x["observed_external_network_s"])
        for x in check if x["seed"]==seed) for seed in range(6111,6115))
    match=sum(x["v2_pred_external_network_s"]!=0 and
              (x["v2_pred_external_network_s"]>0)==(x["observed_external_network_s"]>0) for x in check)
    assert abs(mae-1478.5625)<1e-7 and match==5
    out.mkdir(parents=True,exist_ok=True)
    out_csv(out/"F0_coverage.csv",cov);out_csv(out/"F1_effects.csv",f1)
    out_csv(out/"F3_junctions.csv",f3);out_csv(out/"F4_bundles.csv",f4)
    f2file.close()
    summary=dict(status="ARCHIVED_CHARACTERIZATION_COMPLETE_CAUSAL_SOURCE_UNIDENTIFIED",
       source_run=41966516110,original_members=695,member_sha_verified=bool(ledger),
       simulated_arms_historical=60,new_sumo_arms=0,original_tripinfos=60000,
       F1_interventions=len(f1),F2_edge_bin_pairs=f2count,F3_junction_rows=len(f3),
       F4_bundle_records=len(f4),devcheck_v2_MAE_network_s=mae,devcheck_sign_matches=match,
       validation="NOT_STARTED",Test_B="NOT_RUN",bundles=f4,selected_case_diagnostics=examples,
       original_verdict="DEVELOPMENT_NOT_QUALIFIED")
    (out/"F0_F5_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    content=["# E1-v2 archive-only F0-F5 mechanism investigation results","",
      "**Scientific outcome:** ARCHIVE-BASED OBSERVATIONAL CHARACTERIZATION; precise physical cause NOT IDENTIFIED.",
      "This audit did not rerun SUMO, reforecast, train, tune, or touch reserved 6201-6212/6301-6312 seeds.","",
      "## F0 — Original archive and coverage",
      f"- Original **695** source files, **60,000** completed tripinfo records, **60** previously run arms, and ten pred-before-label locks verified.",
      f"- Per-member original SHA256 release ledger verified: **{bool(ledger)}**.",
      "- Five-second edgeData used; exact individual edge-entry clocks and vehicle-resolved FCD NOT established.",
      "- Missing field attributes are not silently read as zeros. Complete stream coverage and internal-edge counts appear in F0_coverage.csv.","",
      "## F1 — Actual elapsed-time decomposition",
      f"- **50** route-change pairs: own + others = whole-network effect; source insertion + in-network duration = whole-network effect.",
      f"- Frozen four-seed E1-v2 MAE **{mae:.4f} network-seconds**, correct externality direction **{match}/16**. D1 NO-GO unchanged.",
      "- Driver-level >30-second harm and nonparticipant consequences preserved as descriptive data, not policy Test B.","",
      "| Post-outcome selected case | Others observed (network-s) | E1-v2 forecast | Source insertion change | In-network duration change | Aggregate edge waiting change (vehicle-s) |",
      "|---|---:|---:|---:|---:|---:|"]
    for e in examples:
        content.append(f"| {e['seed']}/{e['arm']} | {e['observed_external_network_s']:+.0f} | {e['v2_pred_external_network_s']:+.0f} | {e['insertion_delta_network_s']:+.1f} | {e['duration_delta_network_s']:+.1f} | {e['edge_waiting_change_vehicle_s']:+.1f} |")
    content+=["","## F2 — Observed five-second edge/queue-associated changes",
      f"- **{f2count:,}** paired external-edge/time-bin rows compared across all 50 route-change arms.",
      "- Entered and left counts, waiting, sampled seconds and nonadditive speed/occupancy snapshots retained in compressed raw-derived table.",
      "- Temporal adjacency or lag is observational, not a unique spillback or queue-front causal measurement.","",
      "## F3 — Priority-junction approach/discharge",
      f"- **{len(f3):,}** junction-by-arm rows for the **100** priority intersections.",
      "- Inbound external-edge left, outbound entered and approach waiting contrasts are aggregate proxies; they do NOT count exact turn movements, gap acceptance, or concurrent crossings.","",
      "## F4 — Ten prospectively selected two-route bundles",
      "Four-arm identity: J = C(bundle) - C(single_a) - C(single_b) + C(I); all drivers included. Companion singleton IDs verified per seed.",
      "",
      "| Seed | Exact singletons | Actual J (network-s) | E1-v1 predicted J | E1-v2 predicted J | J insertion | J observed edge waiting (veh-s) |",
      "|---|---|---:|---:|---:|---:|---:|"]
    for b in f4:
        content.append(f"| {b['seed']} | {b['singleton_a']}, {b['singleton_b']} | {b['observed_J_all_network_s']:+.1f} | {b['v1_pred_J_all_network_s']:+.1f} | {b['v2_pred_J_all_network_s']:+.1f} | {b['J_insertion_network_s']:+.1f} | {b['J_edge_waiting_vehicle_s']:+.1f} |")
    content+=["","## F5 — Hypothesis assessment",
      "- **Timing T:** directly observed scheduled and actual trip starts; five-second aggregate edge counts. Exact per-driver edge forecast-vs-truth error NOT OBSERVABLE.",
      "- **Queue Q:** aggregate waiting and occupancy responses observable; true queue-front propagation, downstream receiving and causal mediation UNIDENTIFIED.",
      "- **Junction J:** static conflict model previously verified; aggregate external approach/discharge changes observable; movement-specific right-of-way and gap acceptance UNOBSERVABLE.",
      "- **Bundles B:** ten exact whole-driver interaction contrasts directly reconstructed; they do not prove a single junction or queue was causal.",
      "- **Accounting A:** 60 archived arm identity/source SHA checks, prediction locks, fixed routes, source insertion and duration decomposition passed; missing detector fields and sampling semantics remain documented.",
      "",
      "**Final decision:** E1-v2 DEVELOPMENT_NOT_QUALIFIED; independent validation NOT_STARTED; Test B NOT_RUN. Any new instrumented simulation or revised E1-v3 requires a separate prospective protocol and approval. These development records cannot serve as fresh independent holdouts. No real-road or individual-safety efficacy claim.",
      "",
      "**Available machine-readable derived evidence:** F0_coverage.csv, F1_effects.csv, F2_edge_5second.csv.gz, F3_junctions.csv, F4_bundles.csv, F0_F5_summary.json.",
      ""]
    (out/"FINAL_F0_F5_REPORT.md").write_text("\n".join(content))
    print(json.dumps({k:v for k,v in summary.items() if k not in ("bundles","selected_case_diagnostics")},indent=2),flush=True)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--root",required=True);p.add_argument("--out",required=True);p.add_argument("--ledger")
    a=p.parse_args();main(pathlib.Path(a.root),pathlib.Path(a.out),a.ledger)
