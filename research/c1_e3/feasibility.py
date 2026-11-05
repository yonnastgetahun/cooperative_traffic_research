#!/usr/bin/env python3
"""C1 controlled E3 candidate-selection / netconvert patch feasibility.
NO traffic simulations. This code never calls SUMO, E1, route generation or
reserved holdouts. Fail closed if the patched SUMO 1.28 network changes anything
outside the specified E3 priority relation. Output is retrospective design data.
"""
from __future__ import annotations
import argparse,collections,csv,gzip,hashlib,json,pathlib,subprocess,sys,xml.etree.ElementTree as ET
from collections import defaultdict
P=pathlib.Path
sys.path.insert(0,str(P(__file__).resolve().parents[1]/"replay"))
from e1v2_four_arm_instrumented import assert_sources,tripinfo,scheduled,compare_one,sha
from research.externality_estimator_v2.movement import compile_frozen_grid_network
SEED=6112
PIN="ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb"
WINDOW=(120,300)
def write(p,obj):
    p=P(p);p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n")
def fmt(el):
    return (el.tag,tuple(sorted(el.attrib.items())),tuple(sorted((fmt(ch) for ch in el))))
def edges(root):
    return {e.get("id"):fmt(e) for e in root.findall("edge")}
def junctions(root):
    return {x.get("id"):fmt(x) for x in root.findall("junction")}
def conn(root):
    return sorted(fmt(x) for x in root.findall("connection"))
def connection_differences(original,candidate):
    def mapped(path):
        root=ET.parse(path).getroot()
        result={}
        for e in root.findall("connection"):
            k=(e.get("from"),e.get("to"),e.get("fromLane"),e.get("toLane"),e.get("via"))
            assert k not in result,("duplicate connection",k)
            result[k]=e.attrib
        return result
    a=mapped(original);b=mapped(candidate)
    assert set(a)==set(b),{"missing":len(set(a)-set(b)),"added":len(set(b)-set(a))}
    rows=[]
    for k in sorted(a,key=lambda z:str(z)):
        before,after=a[k],b[k]
        fields=sorted(f for f in set(before)|set(after) if before.get(f)!=after.get(f))
        if fields:
            rows.append({"from":k[0],"to":k[1],"fromLane":k[2],"toLane":k[3],
                         "via":k[4],
                         "field_changes":{field:{"from":before.get(field),"to":after.get(field)}
                                          for field in fields}})
    return rows

def semantic(original,candidate):
    a=ET.parse(original).getroot();b=ET.parse(candidate).getroot()
    ea,eb=edges(a),edges(b)
    ja,jb=junctions(a),junctions(b)
    ca,cb=conn(a),conn(b)
    return {"edges_added":sorted(set(eb)-set(ea)),
            "edges_removed":sorted(set(ea)-set(eb)),
            "edges_changed":sorted(k for k in set(ea)&set(eb) if ea[k]!=eb[k]),
            "junctions_added":sorted(set(jb)-set(ja)),
            "junctions_removed":sorted(set(ja)-set(jb)),
            "junctions_changed":sorted(k for k in set(ja)&set(jb) if ja[k]!=jb[k]),
            "connections_equal":ca==cb,
            "original_connection_count":len(ca),
            "changed_connection_count":len(cb)}
def source_pair(network):
    mov=compile_frozen_grid_network(network)
    assert mov.canonical_sha=="69c5c32e13987646944cbc7b072d586732402c5b8f3651c379c06fecee65ee14"
    members=[m for m in mov.records if m.junction=="E3"]
    assert len(members)==16,("E3 expected 16 priority requests",len(members))
    opts=[]
    for a in members:
        if a.src!="D3E3" or a.cont:continue
        for b in members:
            if b.src==a.src or b.cont or b.index==a.index:continue
            if a.dst==b.dst or a.via==b.via:continue
            if b.index not in a.foes or a.index not in b.foes:continue
            if (b.index in a.yields_to)==(a.index in b.yields_to):continue
            opts.append((a,b))
    assert opts,"No E3 pairs pass the prospective static priority/independent-lane checks"
    return mov,opts
def fcd_approach_bins(path,approaches):
    occupied=defaultdict(set)
    samples=0
    with gzip.open(path,"rb") as f:
        for _,step in ET.iterparse(f,events=("end",)):
            if step.tag!="timestep":continue
            t=float(step.get("time"))
            if WINDOW[0]<=t<WINDOW[1]:
                for vehicle in step.findall("vehicle"):
                    lane=vehicle.get("lane")
                    if lane in approaches:
                        occupied[lane].add(int(t//5)*5)
                        samples+=1
            step.clear()
    return occupied,samples
def selected_pair(opts,fcd):
    all_approaches={m.source_lane for pair in opts for m in pair}
    bins,samples=fcd_approach_bins(fcd,all_approaches)
    rows=[]
    for a,b in opts:
        overlap=len(bins[a.source_lane]&bins[b.source_lane])
        rows.append(((-overlap,a.src,a.dst,a.index,b.src,b.dst,b.index),a,b,overlap))
    _,a,b,overlap=min(rows,key=lambda item:item[0])
    assert overlap>0,("No sampled co-presence at E3 during predeclared 120-300s window",samples)
    # response row i sets bit j when stream i yields to movement j.
    if b.index in a.yields_to:
        lower,higher=a,b
    else:
        lower,higher=b,a
    return ({"candidate_count":len(rows),"approach_samples":samples,
            "co_presence_5s_bins":overlap,
            "movement_D3E3":{"index":a.index,"from":a.src,"to":a.dst,"via":a.via,
                             "source_lane":a.source_lane,"cont":a.cont},
            "other_movement":{"index":b.index,"from":b.src,"to":b.dst,"via":b.via,
                              "source_lane":b.source_lane,"cont":b.cont},
            "original_yielding_movement":{"index":lower.index,"from":lower.src,"to":lower.dst},
            "original_priority_movement":{"index":higher.index,"from":higher.src,"to":higher.dst},
            "proposed_prohibition_reversal":{"prohibitor":lower.src+"->"+lower.dst,
                                             "prohibited":higher.src+"->"+higher.dst},
            "selection_rule":"maximize number of 5s bins in [120,300) with sampled approach presence in both incoming lanes; tie lexicographic"},
            a,b)
def invoke(cmd,log):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    P(log).write_text("COMMAND: "+json.dumps(cmd)+"\n"+p.stdout)
    if p.returncode:raise RuntimeError("netconvert failed "+str(p.returncode)+": "+p.stdout[-1200:])
def request_bits(net):
    root=ET.parse(net).getroot()
    j=next(x for x in root.findall("junction") if x.get("id")=="E3")
    return {int(x.get("index")):(x.get("foes"),x.get("response"),x.get("cont")) for x in j.findall("request")}
def changed_bitpositions(u,v):
    assert len(u)==len(v)
    return [len(u)-1-i for i,(a,b) in enumerate(zip(u,v)) if a!=b]
def no_op_equal(diff):
    return (not diff["edges_added"] and not diff["edges_removed"]
        and not diff["edges_changed"] and not diff["junctions_added"]
        and not diff["junctions_removed"] and not diff["junctions_changed"]
        and diff["connections_equal"])
def patch_single_pair_ok(orig,noop,modified,a,b):
    # Hard isolation at physical geometry, turn rules, all other junctions.
    diff=semantic(noop,modified)
    if diff["edges_added"] or diff["edges_removed"] or diff["edges_changed"]:
        return False,diff,"Road/lane field changed beyond intended E3 priority pair"
    if diff["junctions_added"] or diff["junctions_removed"] or diff["junctions_changed"]!=["E3"]:
        return False,diff,"Priority edit changed a non-E3 junction or did not affect E3"
    differences=connection_differences(noop,modified)
    diff["connection_changes"]=differences[:100]
    diff["connection_change_count"]=len(differences)
    orig_reqs=request_bits(noop);adjusted_reqs=request_bits(modified)
    diff["E3_response_changes"]=[
       {"request_index":i,"changed_response_bits":changed_bitpositions(orig_reqs[i][1],adjusted_reqs[i][1]),
        "old_response":orig_reqs[i][1],"new_response":adjusted_reqs[i][1]}
       for i in sorted(orig_reqs) if orig_reqs[i][1]!=adjusted_reqs[i][1]
    ]
    lower=a if b.index in a.yields_to else b
    higher=b if lower==a else a
    # SUMO netconvert must update the controlled connection's major/minor
    # state when reversing priority. Permit exactly that semantic E3 state
    # transition on the original major movement, and no geometry, flags,
    # fields, lanes, or any other connection alterations.
    expected_connection_change={
        "from":higher.src,"to":higher.dst,"fromLane":"0","toLane":"0",
        "via":higher.via,
        "field_changes":{"state":{"from":"M","to":"m"}}
    }
    if differences!=[expected_connection_change]:
        return False,diff,"C1 connection mutations exceed the one expected E3 major-to-minor state transition"
    original=request_bits(noop);adjusted=request_bits(modified)
    if original.keys()!=adjusted.keys():
        return False,diff,"E3 movement index set changed"
    changes=[]
    for idx in original:
        foes,resp,cont=original[idx]
        nf,nr,nc=adjusted[idx]
        if foes!=nf or cont!=nc:
            return False,diff,"E3 foe/cont physics changed"
        for bit in changed_bitpositions(resp,nr):changes.append((idx,bit,int(nr[-1-bit])))
    expected={(lower.index,higher.index,0),(higher.index,lower.index,1)}
    actual=set(changes)
    if actual!=expected:
        return False,diff,("E3 priority change was not the exact two-bit reversal; "
                           +json.dumps({"expected":sorted(expected),"actual":sorted(actual)}))
    return True,diff,"C1_VALID_EXACT_LOCAL_PRIORITY_REVERSAL"
def main(args):
    out=P(args.out);out.mkdir(parents=True,exist_ok=True)
    audit={"scientific_stage":"C0_C1_FEASIBILITY","status":"DESIGN_NOT_QUALIFIED",
           "sumo_simulations_executed":0,
           "independent_validation":"NOT_STARTED","Test_B":"NOT_RUN",
           "historical_verdict":"DEVELOPMENT_NOT_QUALIFIED",
           "version_pinned":PIN}
    try:
        sources=assert_sources(P(args.root),full_ledger=args.ledger)
        audit["C0"]="PASS";audit["source"]=sources
        fcd=P(args.replays)/"replay-6112-I"/"fcd.xml.gz"
        attempt=json.loads((fcd.parent/"attempt.json").read_text())
        assert attempt.get("status")=="G2_PASS_G3_PENDING",attempt.get("status")
        assert sha(fcd)==attempt["sha256"]["fcd.xml.gz"]
        orig=P(args.root)/"seed-6112"/"network.net.xml"
        m,options=source_pair(orig)
        lock,a,b=selected_pair(options,fcd)
        audit["selection"]=lock
        netout=out/"networks";netout.mkdir(exist_ok=True)
        noop=netout/"6112-J0.net.xml"
        mod=netout/"6112-J1.net.xml"
        patch=netout/"E3-priority-reversal.con.xml"
        ET.ElementTree(ET.Element("connections")).write(patch,encoding="utf-8",xml_declaration=True)
        root=ET.Element("connections")
        ET.SubElement(root,"prohibition",**lock["proposed_prohibition_reversal"])
        ET.ElementTree(root).write(patch,encoding="utf-8",xml_declaration=True)
        vs=subprocess.check_output(["netconvert","--version"],text=True)
        assert "1.28.0" in vs
        invoke(["netconvert","--sumo-net-file",str(orig),"-o",str(noop)],out/"no-op-netconvert.log")
        nochange=semantic(orig,noop)
        audit["C1_noop_semantic_diff"]=nochange
        if not no_op_equal(nochange):
            raise RuntimeError("DESIGN_NO_GO: netconvert no-op reconstructed network is not structurally identical. "
                               +json.dumps(nochange)[:1500])
        invoke(["netconvert","--sumo-net-file",str(orig),"--connection-files",str(patch),"-o",str(mod)],
               out/"modified-E3-netconvert.log")
        ok,changes,why=patch_single_pair_ok(orig,noop,mod,a,b)
        audit["C1_modified_semantic_diff"]=changes
        audit["C1_rule_verification"]=why
        if not ok:raise RuntimeError("DESIGN_NO_GO: "+why)
        audit["network_shas_by_seed"]={"6112":{
            "source":sha(orig),"J0_noop":sha(noop),"J1_modified":sha(mod)}}
        # Reuse the exact selected E3 pair and the identical plain-XML patch
        # on seed 6113; do not reselect movements on that contrasting seed.
        orig2=P(args.root)/"seed-6113"/"network.net.xml"
        _,pair2=source_pair(orig2)
        wanted=lambda m:(m.index,m.src,m.dst,m.via)
        pair_lookup={(wanted(x),wanted(y)):(x,y) for x,y in pair2}
        a2,b2=pair_lookup[(wanted(a),wanted(b))]
        nop2=netout/"6113-J0.net.xml"
        mod2=netout/"6113-J1.net.xml"
        invoke(["netconvert","--sumo-net-file",str(orig2),"-o",str(nop2)],
               out/"6113-no-op-netconvert.log")
        nodiff2=semantic(orig2,nop2)
        audit["C1_seed6113_noop_semantic_diff"]=nodiff2
        if not no_op_equal(nodiff2):
            raise RuntimeError("DESIGN_NO_GO: 6113 no-op conversion changes non-metadata physics")
        invoke(["netconvert","--sumo-net-file",str(orig2),"--connection-files",str(patch),
                "-o",str(mod2)],out/"6113-modified-E3-netconvert.log")
        good2,delta2,why2=patch_single_pair_ok(orig2,nop2,mod2,a2,b2)
        audit["C1_seed6113_modified_semantic_diff"]=delta2
        if not good2:
            raise RuntimeError("DESIGN_NO_GO: 6113 patch not isolated: "+why2)
        audit["network_shas_by_seed"]["6113"]={
            "source":sha(orig2),"J0_noop":sha(nop2),"J1_modified":sha(mod2)}
        audit["patch_sha256"]=sha(patch)
        if args.lock:
            lock=json.loads(P(args.lock).read_text())
            if lock["status"]!="FROZEN_BEFORE_ANY_C2_C3_SUMO_OUTCOME":
                raise RuntimeError("C1 lock status is not prospectively frozen")
            if lock["patch_sha256"]!=audit["patch_sha256"]:
                raise RuntimeError("C1 patch checksum drift versus frozen execution lock")
            if not args.frozen:
                raise RuntimeError("Frozen source networks from run 42125134835 must be supplied with --frozen")
            for seed in (6112,6113):
                entry=lock["networks"][str(seed)]
                if audit["network_shas_by_seed"][str(seed)]["source"]!=entry["source"]:
                    raise RuntimeError("C1 original input network hash mismatch")
                for label,suffix in (("J0_noop","J0"),("J1_modified","J1")):
                    p=P(args.frozen)/"networks"/("%s-%s.net.xml"%(seed,suffix))
                    regenerated=netout/("%s-%s.net.xml"%(seed,suffix))
                    if not p.is_file() or sha(p)!=entry[label]:
                        raise RuntimeError("Frozen pre-outcome network member differs from exact C1_LOCK")
                    nonmeta=semantic(p,regenerated)
                    if not no_op_equal(nonmeta):
                        raise RuntimeError("Reconstructed C1 semantics differ from pre-frozen intervention: "+json.dumps(nonmeta))
            audit["frozen_network_shas_by_seed"]=lock["networks"]
            selection=audit["selection"]
            chosen=lock["chosen"]
            if not (selection["co_presence_5s_bins"]==lock["co_presence_5s_bins"]==
                    35 and selection["movement_D3E3"]["index"]==chosen["D3E3_index"]
                    and selection["other_movement"]["index"]==chosen["other_index"]
                    and selection["movement_D3E3"]["via"]==chosen["D3E3_via"]
                    and selection["other_movement"]["via"]==chosen["other_via"]
                    and selection["proposed_prohibition_reversal"]==chosen["new_prohibition"]):
                raise RuntimeError("C1 selected intervention drift versus frozen execution lock")
            audit["frozen_lock_sha256"]=sha(P(args.lock))
            audit["C1_lock_match"]="PASS"
        audit["C1"]="PASS"
        audit["status"]="C0_C1_ELIGIBLE_TO_FREEZE_EXECUTABLE_PROTOCOL"
    except Exception as e:
        audit.setdefault("C0","PASS" if "source" in audit else "FAILED")
        audit.setdefault("C1","FAILED")
        audit["error"]=repr(e)
        audit["status"]="C1_DESIGN_NO_GO"
    write(out/"C0_C1_verdict.json",audit)
    print(json.dumps(audit,indent=2)[:14000],flush=True)
    # Always report failure as scientific NO-GO. CI still uploads original evidence.
    if audit["status"]!="C0_C1_ELIGIBLE_TO_FREEZE_EXECUTABLE_PROTOCOL":
        raise RuntimeError("Original C1 design gate was not met. Stop before any SUMO.")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True)
    p.add_argument("--replays",required=True)
    p.add_argument("--ledger",required=True)
    p.add_argument("--lock")
    p.add_argument("--frozen")
    p.add_argument("--out",required=True)
    main(p.parse_args())
