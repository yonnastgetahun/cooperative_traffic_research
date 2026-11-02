#!/usr/bin/env python3
"""Read-only Experiment 007 P0-P3 audit. Uses original GitHub Actions archives only.
No SUMO imports, simulations, frozen-source changes, calibration, or fitted parameters.
Run: python3 research/audits/exp007_p0_p3_audit.py --root evidence --out audit
"""
import argparse,csv,hashlib,json,math,statistics
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

SEEDS=range(4101,4106)
ARMS=("I","probe0","probe1","probe2","probe3","bundle")
OFFSET=4.053135104279146; PER_EDGE=11.524898884412591;BIN=30
def sha(b):return hashlib.sha256(b).hexdigest()
def table(path,rows):
    if not rows:return
    cols=list(dict.fromkeys(k for row in rows for k in row))
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,cols);w.writeheader();w.writerows(rows)
def parse(path):return ET.parse(path).getroot()
def routes(path):
    x=parse(path).findall("vehicle")
    v={y.get("id"):tuple(y.find("route").get("edges").split()) for y in x}
    assert len(x)==len(v)==1000
    return v
def tripinfo(path, scheduled):
    x=parse(path).findall("tripinfo");v={}
    for a in x:
        vid=a.get("id");depart=float(a.get("depart"));arrival=float(a.get("arrival"))
        duration=float(a.get("duration"));insertion=depart-scheduled[vid]
        assert abs(duration+depart-arrival)<.001
        assert abs(insertion-float(a.get("departDelay")))<.05
        v[vid]={"T":arrival-scheduled[vid],"duration":duration,"insertion":insertion,
                "waiting":float(a.get("waitingTime","0")),
                "timeLoss":float(a.get("timeLoss","0"))}
    assert len(x)==len(v)==1000 and set(v)==set(scheduled)
    return v
def edges(path):
    net=parse(path);out={}
    for e in net.findall("edge"):
        if e.get("function")=="internal":continue
        lanes=e.findall("lane")
        if not lanes:continue
        length=float(lanes[0].get("length"));speed=float(lanes[0].get("speed"))
        ff=length/max(speed,.1)
        out[e.get("id")]={"ff":ff,"cap":max(1.,length*len(lanes)/7.5),
                          "lanes":len(lanes),"speed":speed}
    return out
def footprint(path,depart,ee):
    q=Counter();clock=depart
    for k,eid in enumerate(path):
        q[(eid,int((clock+OFFSET+PER_EDGE*k)//BIN))]+=1
        clock+=ee[eid]["ff"]
    return q
def delta(old,new,depart,q,ee):
    if old==new:return {"total":0.,"self":0.,"external":0.}
    a=footprint(old,depart,ee);b=footprint(new,depart,ee)
    dq={key:b.get(key,0)-a.get(key,0) for key in set(a)|set(b)}
    def cost(eid,n):return ee[eid]["ff"]*(n+n*n/ee[eid]["cap"])
    total=sum(cost(key[0],q[key]+v)-cost(key[0],q[key]) for key,v in dq.items())
    before=sum(n*ee[key[0]]["ff"]*(1+q[key]/ee[key[0]]["cap"]) for key,n in a.items())
    after=sum(n*ee[key[0]]["ff"]*(1+(q[key]+dq.get(key,0))/ee[key[0]]["cap"]) for key,n in b.items())
    self=after-before
    return {"total":total,"self":self,"external":total-self}
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",required=True);parser.add_argument("--out",required=True)
    a=parser.parse_args();root=Path(a.root);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    manifest=[];coverage=[];probes=[];bundles=[];paired=[];stats=[];subgroups=[]
    for seed in SEEDS:
        p=root/("exp007-probe-%d"%seed)
        assert p.is_dir(),p
        contents=sorted(f for f in p.rglob("*") if f.is_file())
        assert len(contents)==43,(seed,len(contents))
        for file in contents:
            b=file.read_bytes()
            manifest.append({"seed":seed,"path":str(file.relative_to(p)),"size":len(b),"sha256":sha(b)})
        attempt=json.loads((p/"attempt.json").read_text())
        assert attempt["seed"]==seed and attempt["status"]=="COMPLETE" and attempt["n_runs"]==6
        obs=json.loads((p/"probe-results.json").read_text())
        assert len(obs["records"])==4
        demand=parse(p/"trips.xml").findall("trip")
        scheduled={t.get("id"):float(t.get("depart")) for t in demand}
        assert len(demand)==len(scheduled)==1000
        assert sha((p/"trips.xml").read_bytes())==attempt["demand_sha256"]
        ee=edges(p/"network.net.xml")
        rr={arm:routes(p/arm/"routes.rou.xml") for arm in ARMS}
        tt={arm:tripinfo(p/arm/"tripinfo.xml",scheduled) for arm in ARMS}
        q=Counter()
        for v,path in rr["I"].items():q.update(footprint(path,scheduled[v],ee))
        for arm in ARMS:
            changed=[v for v in scheduled if rr[arm][v]!=rr["I"][v]]
            assert len(changed)==(0 if arm=="I" else 2 if arm=="bundle" else 1)
            safety=parse(p/arm/"statistics.xml").find("safety")
            assert safety is not None
            cv=parse(p/arm/"collisions.xml").findall(".//collision")
            stats.append({"seed":seed,"arm":arm,"collisions":safety.get("collisions"),
                "emergencyStops":safety.get("emergencyStops"),
                "emergencyBraking":safety.get("emergencyBraking"),
                "collisionFileEvents":len(cv)})
            coverage.append({"seed":seed,"arm":arm,"matched":1000,"changed":len(changed),
                "tripinfo":True,"route_data":True,"statistics":True,"fcd":False})
        for idx,pred in enumerate(obs["records"]):
            arm="probe%d"%idx;target=pred["vehicle"]
            assert rr[arm][target]!=rr["I"][target]
            assert all(rr[arm][v]==rr["I"][v] for v in scheduled if v!=target)
            recalculated=delta(rr["I"][target],rr[arm][target],scheduled[target],q,ee)
            for k in ("total","self","external"):
                assert abs(recalculated[k]-pred["predicted"][k])<1e-6,(seed,idx,k)
            group={v:{k:tt[arm][v][k]-tt["I"][v][k]
                   for k in ("T","duration","insertion","waiting","timeLoss")}
                   for v in scheduled}
            for vid,d in group.items():
                assert abs(d["T"]-d["duration"]-d["insertion"])<.05
                paired.append({"seed":seed,"probe":idx,"vehicle":vid,
                    "target":int(vid==target),"participant":int(int(vid[-4:])%2==0),
                    "delta_T":d["T"],"delta_duration":d["duration"],
                    "delta_insertion":d["insertion"],"delta_waiting":d["waiting"],
                    "delta_timeLoss":d["timeLoss"]})
            total=sum(d["T"] for d in group.values())
            self=group[target]["T"];external=total-self
            for k,num in (("total",total),("self",self),("external",external)):
                assert abs(num-pred["realized"][k])<.01
            others=[d for v,d in group.items() if v!=target]
            nominal=sum(ee[e]["ff"] for e in rr[arm][target])-sum(ee[e]["ff"] for e in rr["I"][target])
            assert abs(nominal)<1e-8
            abses=sorted((abs(d["T"]) for d in others),reverse=True)
            probes.append({"seed":seed,"probe":idx,"target":target,
                "pred_external":recalculated["external"],"real_external":external,
                "pred_total":recalculated["total"],"pred_self":recalculated["self"],
                "real_total":total,"real_self":self,
                "pred_total_minus_2self":recalculated["total"]-2*recalculated["self"],
                "nominal_freeflow_difference":nominal,
                "material":int(abs(external)>=10),
                "sign_concordant":int(recalculated["external"]*external>0),
                "predicted_zero":int(abs(recalculated["external"])<1e-8),
                "other_harmed":sum(d["T"]>0 for d in others),
                "other_helped":sum(d["T"]<0 for d in others),
                "other_unchanged":sum(d["T"]==0 for d in others),
                "other_duration_delta":sum(d["duration"] for d in others),
                "other_insertion_delta":sum(d["insertion"] for d in others),
                "other_waiting_delta":sum(d["waiting"] for d in others),
                "other_timeLoss_delta":sum(d["timeLoss"] for d in others),
                "other_top10_abs_share":sum(abses[:10])/sum(abses)})
            # Subgroups are overlapping/descriptive, not independent random samples.
            old=set(rr["I"][target]);new=set(rr[arm][target])
            for name,ids in (
                 ("nonparticipants",[v for v in scheduled if v!=target and int(v[-4:])%2]),
                 ("participants_other",[v for v in scheduled if v!=target and not int(v[-4:])%2]),
                 ("no_direct_route_edge_overlap",[v for v in scheduled if v!=target and not set(rr["I"][v])&(old|new)])):
                values=[group[v]["T"] for v in ids]
                subgroups.append({"seed":seed,"probe":idx,"cohort":name,"n":len(ids),
                   "net_network_s":sum(values),"harmed":sum(v>0 for v in values),
                   "helped":sum(v<0 for v in values)})
        changed=[v for v in scheduled if rr["I"][v]!=rr["bundle"][v]]
        assert set(changed)=={x["vehicle"] for x in obs["records"][:2]}
        bundle_total=sum(tt["bundle"][v]["T"]-tt["I"][v]["T"] for v in scheduled)
        singles=sum(x["realized"]["total"] for x in obs["records"][:2])
        assert abs(bundle_total-obs["bundle"]["realized_total"])<.01
        assert abs(singles-obs["bundle"]["isolated_realized_total_sum"])<.01
        bundles.append({"seed":seed,"observed_joint":bundle_total,
           "observed_individual_sum":singles,
           "observed_interaction":bundle_total-singles,
           "predicted_joint":obs["bundle"]["predicted_total"],
           "predicted_individual_sum":obs["bundle"]["isolated_predicted_total_sum"],
           "predicted_interaction":obs["bundle"]["predicted_total"]-obs["bundle"]["isolated_predicted_total_sum"]})
    assert len(probes)==20 and len(paired)==20000 and len(bundles)==5 and len(coverage)==30
    assert sum(r["sign_concordant"] for r in probes)==8
    assert sum(r["predicted_zero"] for r in probes)==5
    assert sum(r["material"] for r in probes)==20
    for filename,rows in (
        ("p0_manifest.csv",manifest),("p0_coverage.csv",coverage),
        ("p0_safety.csv",stats),("p1_p2_probe_summary.csv",probes),
        ("p2_driver_paired.csv",paired),("p2_subgroups.csv",subgroups),
        ("p2_bundle.csv",bundles)):
        table(out/filename,rows)
    summary={
        "experiment":"007","analysis":"P0-P3 read-only archive investigation",
        "seeds":list(SEEDS),"arms":30,"probe_n":20,"driver_pairs":len(paired),
        "sign_concordant":8,"sign_rate":.4,"frozen_gate_pass":False,
        "prediction_MAE_network_s":statistics.mean(abs(x["pred_external"]-x["real_external"]) for x in probes),
        "max_abs_pred_total_minus_2self":max(abs(x["pred_total_minus_2self"]) for x in probes),
        "predicted_zero_n":5,"material_n":20,
        "avg_other_harmed":statistics.mean(x["other_harmed"] for x in probes),
        "avg_other_helped":statistics.mean(x["other_helped"] for x in probes),
        "avg_top10_abs_share":statistics.mean(x["other_top10_abs_share"] for x in probes),
        "bundle_realized_interactions":[x["observed_interaction"] for x in bundles],
        "no_FCD_edge_time_data":True,"Test_B":"not_run",
        "limitations":"5 independent seeds, 20 purposively selected probes; tripinfo only, no causal junction localization"}
    (out/"p0_p3_summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    print(json.dumps(summary,indent=2))
if __name__=="__main__":main()
