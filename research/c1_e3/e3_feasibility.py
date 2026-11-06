#!/usr/bin/env python3
"""C1 feasibility only: original-file integrity, prospective E3 pair selection,
netconvert plain XML right-of-way patch, strict source-semantic differences.
NEVER invokes SUMO, netgenerate, routing, or model predictions.
Historical cases 6112 and 6113 were selected after viewing outcomes.
"""
from __future__ import annotations
import argparse,collections,csv,gzip,hashlib,json,pathlib,re,subprocess,xml.etree.ElementTree as ET

P=pathlib.Path
SEEDS=(6112,6113)
ARMS=("I","probe2")
PINNED_VERSION="1.28.0"
ORIGINAL_ACTION=41966516110
FCD_ACTION=42113107379
E3="E3"
APPROACH="D3E3"
BIN_START=120
BIN_END=300

def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()
def j(path):return json.loads(P(path).read_text())
def write(path,o):
    p=P(path);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n")
def source_integrity(root,ledger):
    root=P(root)
    paths=[x for x in root.rglob("*") if x.is_file()]
    with open(ledger,newline="") as f: rows=list(csv.DictReader(f))
    assert len(rows)==len(paths)==695,(len(rows),len(paths))
    assert {x["member"] for x in rows}=={x.relative_to(root).as_posix() for x in paths}
    for row in rows:
        p=root/row["member"]
        assert p.stat().st_size==int(row["bytes"]) and sha(p)==row["sha256"],row["member"]
    verdict=j(root/"development-verdict.json")
    assert verdict["scientific_status"]=="DEVELOPMENT_NOT_QUALIFIED"
    assert verdict["new_validation"]=="NOT_STARTED" and verdict["Test_B"]=="NOT_RUN"
    assert j(root/"all-prediction-locks.json")["status"]=="FROZEN_BEFORE_ANY_SUMO_OUTCOME"
    result={}
    for seed in SEEDS:
        folder=root/("seed-"+str(seed))
        m=j(folder/"scenario-manifest.json")
        o=j(folder/"observations-summary.json")["observations"]
        lock=j(folder/"prediction-lock.json")
        assert m["seed"]==seed and lock["seed"]==seed
        for path,want in ((folder/"network.net.xml",m["network_sha256"]),
                          (folder/"trips.xml",m["demand_sha256"]),
                          (folder/"predictions/predictions.json",lock["prediction_sha256"])):
            assert sha(path)==want
        baseline=None
        for arm in ARMS:
            route=folder/"routes"/(arm+".rou.xml")
            assert sha(route)==m["arm_route_sha256"][arm]
            assert sha(folder/"observations"/arm/"tripinfo.xml")==o[arm]["tripinfo_sha256"]
            ids={x.get("id"):tuple(x.find("route").get("edges").split())
                 for x in ET.parse(route).getroot().findall("vehicle")}
            assert len(ids)==1000
            if baseline is None:baseline=ids
            else:
                changed={k for k in ids if ids[k]!=baseline[k]}
                assert changed=={ {6112:"veh0142",6113:"veh0038"}[seed] }
        result[str(seed)]={"network_sha":m["network_sha256"],
                           "demand_sha":m["demand_sha256"],
                           "I_route_sha":m["arm_route_sha256"]["I"],
                           "probe2_route_sha":m["arm_route_sha256"]["probe2"]}
    return result

def bit(raw,k):return raw[-1-k]=="1"
def movement_map(net):
    root=ET.parse(net).getroot()
    node=next(x for x in root.findall("junction") if x.get("id")==E3)
    assert node.get("type")=="priority"
    requests={int(r.get("index")):r for r in node.findall("request")}
    n=len(requests)
    assert n in (9,16),n
    conns={}
    for c in root.findall("connection"):
        via=c.get("via","")
        m=re.fullmatch(r":E3_(\d+)_(\d+)",via)
        if not m:continue
        idx=int(m.group(1))
        assert idx not in conns,("duplicate E3 mapping",idx)
        conns[idx]=dict(src=c.get("from"),dst=c.get("to"),
                        fromlane=c.get("from")+"_"+c.get("fromLane"),
                        tolane=c.get("to")+"_"+c.get("toLane"),via=via,
                        cont=c.get("cont",""))
    assert sorted(conns)==sorted(requests)==list(range(n)),(sorted(conns),sorted(requests))
    for idx,r in requests.items():
        assert len(r.get("response",""))==len(r.get("foes",""))==n
        assert set(r.get("foes","")+r.get("response",""))<={"0","1"}
        assert all(not bit(r.get("response"),i) or bit(r.get("foes"),i) for i in range(n))
    return root,requests,conns

def sampled_lane_bins(fcd):
    present=collections.defaultdict(set)
    with gzip.open(fcd,"rb") as f:
        for event,elem in ET.iterparse(f,events=("end",)):
            if elem.tag!="timestep":continue
            t=float(elem.get("time"))
            if BIN_START<=t<BIN_END:
                b=int(t//5)*5
                for v in elem.findall("vehicle"):
                    lane=v.get("lane")
                    if lane:present[lane].add(b)
            elem.clear()
    return present

def choose_pair(requests,moves,presence):
    candidates=[]
    n=len(requests)
    for a in range(n):
        A=moves[a]
        if A["src"]!=APPROACH:continue
        for b in range(n):
            if a==b:continue
            B=moves[b]
            if B["src"]==APPROACH or A["dst"]==B["dst"]:continue
            if A["fromlane"]==B["fromlane"] or A["tolane"]==B["tolane"]:continue
            ra=requests[a];rb=requests[b]
            if not (bit(ra.get("foes"),b) and bit(rb.get("foes"),a)):continue
            a_yields=bit(ra.get("response"),b)
            b_yields=bit(rb.get("response"),a)
            if a_yields==b_yields:continue
            score=len(presence[A["fromlane"]] & presence[B["fromlane"]])
            pair=(a,b)
            candidates.append(dict(a=a,b=b,score=score,
                                   a_from=A["fromlane"],a_to=A["tolane"],
                                   b_from=B["fromlane"],b_to=B["tolane"],
                                   a_route=A["src"]+"->"+A["dst"],
                                   b_route=B["src"]+"->"+B["dst"],
                                   a_yields_to_b=a_yields,b_yields_to_a=b_yields))
    candidates.sort(key=lambda c:(-c["score"],c["a_from"],c["a_to"],c["b_from"],c["b_to"],c["a"],c["b"]))
    assert candidates,"C1 NO-GO: no verified E3 D3E3 directional-foe movement pair"
    selected=candidates[0]
    assert selected["score"]>0,"C1 NO-GO: no 120–300s simultaneous five-second approach-presence bins"
    return selected,candidates

def run(cmd,log):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    P(log).write_text(p.stdout)
    if p.returncode:raise RuntimeError("netconvert failed; see "+str(log)+": "+p.stdout[-1200:])
    return p.stdout

def normalized(root):
    # Canonical semantic XML keyed by id + child appearance, excludes metadata comments and location.
    result=collections.defaultdict(dict)
    for parent in root:
        if parent.tag=="edge":key=parent.get("id")
        elif parent.tag=="junction":key=parent.get("id")
        elif parent.tag=="connection":key=(parent.get("from"),parent.get("to"),
                                          parent.get("fromLane"),parent.get("toLane"),parent.get("via"))
        else:continue
        assert key not in result[parent.tag],(parent.tag,key)
        def snap(element):
            return (element.tag,tuple(sorted(element.attrib.items())),tuple(snap(c) for c in element))
        result[parent.tag][key]=snap(parent)
    return result

def semantic_diff(original,reconstructed,altered):
    # Valid only if a netconvert no-op represents every original edge/junction/connection.
    orig=normalized(ET.parse(original).getroot())
    noop=normalized(ET.parse(reconstructed).getroot())
    changed=normalized(ET.parse(altered).getroot())
    counts={}
    modifications={}
    for tag in ("edge","junction","connection"):
        for stage,other in (("noop",noop),("intervention",changed)):
            missing=set(orig[tag])-set(other[tag])
            extra=set(other[tag])-set(orig[tag])
            different={k for k in orig[tag].keys() & other[tag].keys() if orig[tag][k]!=other[tag][k]}
            counts[f"{tag}_{stage}"]={"missing":len(missing),"extra":len(extra),"different":len(different)}
            modifications[(tag,stage)]=(missing,extra,different)
    # Any global geometry/connection/reconstruction change invalidates causal isolation.
    for tag in ("edge","junction","connection"):
        missing,extra,different=modifications[(tag,"noop")]
        assert not (missing or extra or different),("C1 no-op semantic mismatch",tag,len(missing),len(extra),len(different))
    for tag in ("edge","connection"):
        missing,extra,different=modifications[(tag,"intervention")]
        assert not (missing or extra or different),("C1 non-E3 geometry/connection mismatch",tag,len(missing),len(extra),len(different))
    missing,extra,different=modifications[("junction","intervention")]
    assert not (missing or extra) and different=={"E3"},("C1 requires only junction E3 change",len(missing),len(extra),different)
    return counts

def run_all(original,fcd,ledger,out):
    original=P(original);out=P(out);out.mkdir(parents=True,exist_ok=True)
    status={"study":"Post-Exp007 C1 controlled E3 feasibility",
            "status":"C0_INCOMPLETE","C0":"INCOMPLETE","C1":"INCOMPLETE",
            "sumo_traffic_runs":0,"sumo_version":"1.28.0",
            "future_validation":"NOT_STARTED","Test_B":"NOT_RUN"}
    try:
        status["original"]=source_integrity(original,ledger)
        status["C0"]="PASS";status["status"]="C1_PROCESSING"
        version=subprocess.check_output(["netconvert","--version"],text=True)
        assert PINNED_VERSION in version,("Wrong netconvert version",version)
        commands=subprocess.check_output(["netconvert","--help"],text=True)
        assert "--sumo-net-file" in commands and "--connection-files" in commands
        source6112=original/"seed-6112"/"network.net.xml"
        source6113=original/"seed-6113"/"network.net.xml"
        root,requests,moves=movement_map(source6112)
        _,r13,m13=movement_map(source6113)
        assert [(k,moves[k]) for k in moves]==[(k,m13[k]) for k in m13]
        assert all(requests[k].attrib==r13[k].attrib for k in requests)
        present=sampled_lane_bins(fcd)
        selected,candidates=choose_pair(requests,moves,present)
        status["candidate_count"]=len(candidates)
        status["selected_pair"]=selected
        with (out/"E3_PROSPECTIVE_PAIR_CANDIDATES.csv").open("w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=list(candidates[0]));w.writeheader();w.writerows(candidates)
        # SUMO's official plain .con.xml format, using a prohibitor/prohibited
        # patch to netconvert. Do not edit network.net.xml request bits by hand.
        # Invert one existing directional relation; keep identical legal moves.
        old_priority=selected["b_route"] if selected["a_yields_to_b"] else selected["a_route"]
        old_yield=selected["a_route"] if selected["a_yields_to_b"] else selected["b_route"]
        el=ET.Element("connections")
        ET.SubElement(el,"prohibition",prohibitor=old_yield,prohibited=old_priority)
        patch=out/"E3_priority_reversal.con.xml"
        ET.ElementTree(el).write(patch,encoding="utf-8",xml_declaration=True)
        status["patch_sha256"]=sha(patch)
        for seed in SEEDS:
            f=original/("seed-"+str(seed))/"network.net.xml"
            no=out/("seed-%s-J0-rebuilt.net.xml"%seed)
            yes=out/("seed-%s-J1-E3.net.xml"%seed)
            run(["netconvert","--sumo-net-file",str(f),"--output-file",str(no)],
                out/("netconvert-noop-%s.log"%seed))
            run(["netconvert","--sumo-net-file",str(f),"--connection-files",str(patch),
                 "--output-file",str(yes)],out/("netconvert-E3-%s.log"%seed))
            status.setdefault("network_build",{})[str(seed)]={
                "original_sha256":sha(f),"no_op_sha256":sha(no),
                "priority_changed_sha256":sha(yes),
                "semantic_comparison":semantic_diff(f,no,yes)}
        status["C1"]="PASS";status["status"]="C0_C1_FEASIBILITY_PASS"
    except Exception as e:
        status["status"]="C0_C1_DESIGN_NO_GO"
        status["error_type"]=type(e).__name__
        status["error"]=str(e)
    write(out/"C0_C1_feasibility_verdict.json",status)
    print(json.dumps(status,indent=2),flush=True)
    if status["status"]!="C0_C1_FEASIBILITY_PASS":raise RuntimeError(status.get("error"))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--original",required=True)
    p.add_argument("--fcd",required=True)
    p.add_argument("--ledger",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args();run_all(a.original,a.fcd,a.ledger,a.out)
