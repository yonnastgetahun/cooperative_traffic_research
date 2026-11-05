#!/usr/bin/env python3
"""E1 J0-J4: source/version-checked read-only priority-junction rule verification.

Consumes archived E1 Stage1D files, archived SHA256 per-member ledger and
pinned SUMO v1_28_0 tools/sumolib source. No SUMO simulator or E1 modification.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

from lxml import etree as LXML

SEEDS=(5101,5102,5103,5104,5105,5106,5111,5112,5113,5114)
SUMO_SOURCE_COMMIT="daf91b5578901d599ac9af53f49d26eeb9aefc3b"
E1_IO_BLOB="4ddc2034944354a1605bc798c8df1850e51ea897"
E1_ENGINE_BLOB="0d446e2c52efd2b75adf351ad5d577f442a4ac29"
E1_STAGE1D_COMMIT="05b770cf000f84677524e0a1e89bea06ec0e703b"
ORIGINAL_ARTIFACT_ID=13280496865
ORIGINAL_ARTIFACT_RUN=41737336992
ORIGINAL_ARTIFACT_ZIP_SHA="f8d2b76bd6eda63e11889bd7708888bfdb55af78edd0b30526a9d981feb72fa6"

def sha_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):
            h.update(chunk)
    return h.hexdigest()

def git_blob(path):
    payload=Path(path).read_bytes()
    return hashlib.sha1(b"blob "+str(len(payload)).encode()+b"\0"+payload).hexdigest()

def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def write_csv(path,rows):
    if not rows:
        raise RuntimeError("Do not publish an empty CSV: "+str(path))
    cols=list(rows[0].keys())
    with Path(path).open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=cols)
        writer.writeheader()
        writer.writerows(rows)

def bit(bits,index):
    if index<0 or index>=len(bits):
        raise ValueError("Bit index outside request width")
    if set(bits)-set("01"):
        raise ValueError("Non-binary junction request")
    return bits[-(index+1)]=="1"

def fail_unless(condition,description):
    if not condition:
        raise AssertionError(description)

def validate_bit_decoder():
    # Official example: index 0 rightmost, not leftmost.
    assert bit("011",0) and bit("011",1) and not bit("011",2)
    assert bit("001",0) and not bit("001",1) and not bit("001",2)
    # Deliberate wrong-end interpretation would fail this control.
    assert "001"[0]=="0" and bit("001",0)

def source_preflight(root,ledger,pinned):
    root=Path(root);ledger=Path(ledger);pinned=Path(pinned)
    validate_bit_decoder()
    model_paths={
        "e1_input_adapter":"research/externality_estimator/scenario_io.py",
        "e1_fifo_engine":"research/externality_estimator/link_turn_queue.py"
    }
    fail_unless(git_blob(model_paths["e1_input_adapter"])==E1_IO_BLOB,
                "Historical E1 input adapter differs from frozen source")
    fail_unless(git_blob(model_paths["e1_fifo_engine"])==E1_ENGINE_BLOB,
                "Historical E1 FIFO engine differs from frozen source")
    commit=subprocess.check_output(["git","-C",str(pinned),"rev-parse","HEAD"],text=True).strip()
    fail_unless(commit==SUMO_SOURCE_COMMIT,"Wrong pinned sumolib commit: "+commit)
    node_code=(pinned/"tools/sumolib/net/node.py").read_text(encoding="utf-8")
    fail_unless("len(self._foes[link1]) - link2 - 1" in node_code
                and "for lane_id in self._incLanes" in node_code
                and "ps[-(possProhibitorIndex + 1)]" in node_code,
                "SUMO 1.28.0 node method signatures or bit indexing unexpected")
    with ledger.open(newline="",encoding="utf-8") as f:
        ledger_rows=list(csv.DictReader(f))
    files=sorted(p for p in root.rglob("*") if p.is_file())
    seen={r["member"] for r in ledger_rows}
    fail_unless(len(ledger_rows)==len(files)==706 and len(seen)==706,
                "Frozen 706-member archive/ledger incomplete")
    for row in ledger_rows:
        filepath=root/row["member"]
        fail_unless(filepath.is_file(),"Missing original archive member "+row["member"])
        fail_unless(filepath.stat().st_size==int(row["bytes"]),"Byte size mismatch "+row["member"])
        fail_unless(sha_file(filepath)==row["sha256"],"Original member hash mismatch "+row["member"])
    input_manifest=[]
    semantic_hashes=set()
    for seed in SEEDS:
        folder=root/("seed-"+str(seed))
        man=read_json(folder/"scenario-manifest.json")
        fail_unless(man["seed"]==seed,"Seed manifest identity mismatch")
        network=folder/"network.net.xml"
        rawsha=sha_file(network)
        fail_unless(rawsha==man["network_sha256"],"Network fingerprint mismatch for "+str(seed))
        xml=LXML.parse(str(network)).getroot()
        core=b"".join(LXML.tostring(child,method="c14n",with_comments=False)
                     for child in xml if child.tag in ("edge","junction","connection"))
        semantic=hashlib.sha256(core).hexdigest()
        semantic_hashes.add(semantic)
        input_manifest.append({"seed":seed,"network_sha256":rawsha,
                               "semantic_edges_junctions_connections_sha256":semantic,
                               "network_size_bytes":network.stat().st_size})
    fail_unless(len(semantic_hashes)==1,
                "Topology/traffic-rule content differs between ten development seeds")
    return {
        "archive_members_verified":len(ledger_rows),
        "original_artifact_id":ORIGINAL_ARTIFACT_ID,
        "original_run_id":ORIGINAL_ARTIFACT_RUN,
        "original_artifact_zip_sha256_as_published":ORIGINAL_ARTIFACT_ZIP_SHA,
        "sumo_pinned_version":"1.28.0",
        "sumo_source_commit":commit,
        "sumolib_node_sha256":sha_file(pinned/"tools/sumolib/net/node.py"),
        "sumolib_net_sha256":sha_file(pinned/"tools/sumolib/net/__init__.py"),
        "historical_e1_commit":E1_STAGE1D_COMMIT,
        "e1_input_adapter_git_blob":E1_IO_BLOB,
        "e1_engine_git_blob":E1_ENGINE_BLOB,
        "canonical_network_sha256":next(iter(semantic_hashes)),
        "raw_network_sha_count":len({row["network_sha256"] for row in input_manifest}),
        "network_evidence_by_seed":input_manifest,
        "source_validation":"PASS; source/version/member hashes and canonical original network match"
    }

def request_maps(network,pinned):
    # Independent mapping A: follow the actual SUMO v1.28.0 Node.getLinkIndex
    # ordering: junction.incLanes followed by connections outgoing per lane.
    root=ET.parse(str(network)).getroot()
    external={e.get("id"):e for e in root.findall("edge")
              if e.get("function")!="internal" and not e.get("id","").startswith(":")}
    lane_out=defaultdict(list)
    conns=[]
    for conn in root.findall("connection"):
        a,b=conn.get("from"),conn.get("to")
        if a in external and b in external:
            lane_out[a+"_"+conn.get("fromLane")].append(conn)
            conns.append(conn)
    # Independent mapping B: parse generated via lane ID :junction_index_lane
    # without consulting incoming lane sequence or connection XML order.
    by_via=defaultdict(dict)
    for conn in conns:
        m=re.fullmatch(r":(.+)_(\d+)_(\d+)",conn.get("via",""))
        fail_unless(m is not None,"Unparseable initial internal via-lane ID")
        jid=m.group(1);idx=int(m.group(2))
        fail_unless(idx not in by_via[jid],"Duplicate via-index within junction "+jid)
        by_via[jid][idx]=conn

    # Full independent authority: the exact tag-pinned sumolib implementation,
    # loaded as a separate external package, never the E1 parser.
    sys.path.insert(0,str(Path(pinned).resolve()/"tools"))
    import sumolib
    network_api=sumolib.net.readNet(str(network),withInternal=True,withFoes=True)
    rows=[];mapping_by_j={};api_connections={};junctions=[]
    for junction in root.findall("junction"):
        if junction.get("type")!="priority":
            continue
        jid=junction.get("id")
        reqs={int(r.get("index")):r for r in junction.findall("request")}
        candidates=[c for lane in junction.get("incLanes","").split()
                      for c in lane_out.get(lane,())]
        fail_unless(len(candidates)==len(reqs)==len(by_via[jid]),
                    "Connection/foe-request count mismatch at "+jid)
        fail_unless(sorted(reqs)==list(range(len(reqs))),
                    "Noncontiguous request indices "+jid)
        sums=network_api.getNode(jid)
        conns_by_index={}
        for c in sums.getConnections():
            if c.getFrom().getID() not in external or c.getTo().getID() not in external:
                continue
            idx=c.getJunctionIndex()
            fail_unless(idx>=0 and idx not in conns_by_index,
                        "Pinned SUMO getLinkIndex invalid or duplicate for "+jid)
            conns_by_index[idx]=c
        fail_unless(set(conns_by_index)==set(reqs),
                    "Pinned sumolib and archived request indices disagree "+jid)
        for idx,conn in enumerate(candidates):
            fromlane=conn.get("from")+"_"+conn.get("fromLane")
            tolane=conn.get("to")+"_"+conn.get("toLane")
            via=conn.get("via")
            fail_unless(by_via[jid][idx] is conn,
                        "Incoming-lane order and generated via index disagree "+jid+":"+str(idx))
            sconn=conns_by_index[idx]
            fail_unless(sconn.getFromLane().getID()==fromlane
                        and sconn.getToLane().getID()==tolane
                        and sconn.getViaLaneID()==via,
                        "Tagged SUMO Node.getLinkIndex mapping disagree "+jid+":"+str(idx))
            req=reqs[idx]
            foes=req.get("foes","")
            response=req.get("response","")
            fail_unless(len(foes)==len(response)==len(reqs)
                        and set(foes+response)<=set("01"),
                        "Invalid request bitstring at "+jid+":"+str(idx))
            fail_unless(all(not bit(response,k) or bit(foes,k)
                            for k in range(len(reqs))),
                        "SUMO response bit not included among foes "+jid+":"+str(idx))
            rows.append({
                "junction_id":jid,"junction_type":"priority","request_index":idx,
                "from_edge":conn.get("from"),"from_lane":fromlane,
                "to_edge":conn.get("to"),"to_lane":tolane,
                "via_lane":via,"raw_direction":conn.get("dir",""),
                "raw_connection_state":conn.get("state",""),
                "cont":req.get("cont",""),"foes_raw":foes,
                "response_raw":response,"foes_indices":";".join(str(i) for i in range(len(reqs)) if bit(foes,i)),
                "response_indices":";".join(str(i) for i in range(len(reqs)) if bit(response,i)),
                "tl_link_index":conn.get("linkIndex",""),
                "mapping_methods":"incLanes_order;via_index;SUMO_v1_28_0_Node_getLinkIndex",
                "mapping_status":"VERIFIED"
            })
        mapping_by_j[jid]=(candidates,reqs)
        api_connections[jid]=(sums,conns_by_index)
        junctions.append(jid)
    fail_unless(len(junctions)==100 and len(rows)==1320,
                "Incorrect priority junction or request coverage")
    return rows,mapping_by_j,api_connections,root

def compare_pairs(mapping_by_j,api_connections):
    pairrows=[];diffrows=[];byjunction=[]
    total=Counter()
    examples={}
    for jid in sorted(mapping_by_j):
        members,requests=mapping_by_j[jid]
        node,api=api_connections[jid]
        ctr=Counter()
        n=len(members)
        for i in range(n):
            for j in range(i+1,n):
                ci,cj=members[i],members[j]
                ri,rj=requests[i],requests[j]
                foe_ij=bit(ri.get("foes"),j)
                foe_ji=bit(rj.get("foes"),i)
                response_ij=bit(ri.get("response"),j)
                response_ji=bit(rj.get("response"),i)
                fail_unless(foe_ij==node.areFoes(i,j) and foe_ji==node.areFoes(j,i),
                            "Independent pinned SUMO areFoes bit decoding failed")
                # response row i indicates higher-priority j forbids i
                fail_unless(response_ij==node.forbids(api[j],api[i])
                            and response_ji==node.forbids(api[i],api[j]),
                            "Independent pinned SUMO forbids priority decoding failed")
                if foe_ij!=foe_ji:
                    raise AssertionError("Unexpected nonreciprocal foes in this pinned network")
                share_source=(ci.get("from")==cj.get("from") and ci.get("fromLane")==cj.get("fromLane"))
                share_downstream=(ci.get("to")==cj.get("to") and ci.get("toLane")==cj.get("toLane"))
                share_initial_via=ci.get("via")==cj.get("via")
                mutual_nonfoe=not foe_ij and not foe_ji
                independent=not (share_source or share_downstream or share_initial_via)
                clean=mutual_nonfoe and independent
                cont_i=ri.get("cont","0");cont_j=rj.get("cont","0")
                strict=clean and cont_i=="0" and cont_j=="0"
                directional=response_ij!=response_ji
                if mutual_nonfoe:
                    category="MUTUAL_NONFOES"
                elif directional:
                    category="FOES_DIRECTIONAL_YIELD"
                else:
                    category="FOES_OTHER"
                row={
                    "junction_id":jid,"movement_i":i,"movement_j":j,
                    "i_from_lane":ci.get("from")+"_"+ci.get("fromLane"),
                    "i_to_lane":ci.get("to")+"_"+ci.get("toLane"),
                    "i_via_lane":ci.get("via"),
                    "j_from_lane":cj.get("from")+"_"+cj.get("fromLane"),
                    "j_to_lane":cj.get("to")+"_"+cj.get("toLane"),
                    "j_via_lane":cj.get("via"),
                    "foe_i_marks_j":int(foe_ij),"foe_j_marks_i":int(foe_ji),
                    "i_yields_to_j":int(response_ij),"j_yields_to_i":int(response_ji),
                    "category":category,
                    "same_incoming_lane":int(share_source),
                    "same_outgoing_lane":int(share_downstream),
                    "same_initial_via_lane":int(share_initial_via),
                    "cont_i":cont_i,"cont_j":cont_j,
                    "distinct_source_and_receiving":int(independent),
                    "clean_potential_nonfoe":int(clean),
                    "strict_cont0_nonfoe":int(strict),
                    "E1_all_conflict_allows_same_tick":0,
                    "actual_simultaneous_SUMO_crossing_observed":"NOT_MEASURED",
                    "interpretation":"STATIC_RULE_ONLY"
                }
                pairrows.append(row)
                ctr["pair_count"]+=1
                ctr["nonfoe_count"]+=int(mutual_nonfoe)
                ctr["foe_count"]+=int(not mutual_nonfoe)
                ctr["directional_priority_foes"]+=int(not mutual_nonfoe and directional)
                ctr["clean_potential_nonfoes"]+=int(clean)
                ctr["strict_cont0_nonfoes"]+=int(strict)
                ctr["nonfoes_sharing_source_or_receiving"]+=int(mutual_nonfoe and not independent)
                if clean:
                    diffrows.append({k:row[k] for k in row})
                    if jid not in examples:
                        examples[jid]=row
        byjunction.append({
            "junction_id":jid,"request_count":n,"movement_count":n,
            "unordered_pairs":ctr["pair_count"],
            "mutual_nonfoes":ctr["nonfoe_count"],
            "foes":ctr["foe_count"],
            "directional_yield_foes":ctr["directional_priority_foes"],
            "clean_potential_nonfoes_distinct_in_out":ctr["clean_potential_nonfoes"],
            "clean_cont0_nonfoes":ctr["strict_cont0_nonfoes"],
            "nonfoes_sharing_source_or_receiver":ctr["nonfoes_sharing_source_or_receiving"],
            "e1_all_class_allows_pair_same_tick":0,
            "mapping_coverage":"COMPLETE",
            "actual_vehicle_flow":"NOT_MEASURED"
        })
        total.update(ctr)
    fail_unless(len(pairrows)==8836 and len(diffrows)==3940
                and total["nonfoe_count"]==5764
                and total["strict_cont0_nonfoes"]==2212,
                "Static movement matrix differs from reviewed frozen source")
    return pairrows,diffrows,byjunction,dict(total),examples

def original_e1_fixtures():
    from research.externality_estimator.schema import Link,Turn,Vehicle,Scenario,Parameters
    from research.externality_estimator.link_turn_queue import evolve
    links=tuple(Link(edge,15.0,15.0,1,storage_vehicles=10)
                for edge in ("A1A0","A0B0","B0A0","A0A1"))
    people=(Vehicle("fixture-A",0,("A1A0","A0B0")),
            Vehicle("fixture-B",0,("B0A0","A0A1")))
    results=[]
    for q in (0.35,0.50,0.65):
        cases={}
        for name,classes in (("FROZEN_E1_ALL_CLASS",("all","all")),
                             ("TOY_STIPULATED_SEPARATE_CLASSES",("left","right"))):
            s=Scenario(links,(Turn("A1A0","A0B0","A0",classes[0]),
                              Turn("B0A0","A0A1","A0",classes[1])),people)
            ev=evolve(s,Parameters(q_sat=q))
            crosses={e.vehicle_id:e.tick for e in ev.events if e.action=="cross"}
            fail_unless(len(crosses)==2,"Toy crossings missing")
            cases[name]={"crossings":crosses,
                         "arrival_ticks":ev.arrivals,
                         "nominal_q_sat":q,
                         "simulator":"E1_NOT_SUMO"}
        fail_unless(len(set(cases["FROZEN_E1_ALL_CLASS"]["crossings"].values()))==2,
                    "Old E1 shared-class should defer one toy turn")
        fail_unless(len(set(cases["TOY_STIPULATED_SEPARATE_CLASSES"]["crossings"].values()))==1,
                    "Toy independently labeled turns should be concurrent")
        results.append({"q_sat":q,"cases":cases,
                        "rule_label_change_only":True,
                        "never_used_for_sumo_skill":"TRUE"})
    return results

def main(root,ledger,pinned,out):
    root=Path(root);out=Path(out)
    out.mkdir(parents=True,exist_ok=True)
    j0=source_preflight(root,ledger,pinned)
    network=root/"seed-5111/network.net.xml"
    movement_rows,maps,apis,xml=request_maps(network,pinned)
    pair_rows,difference_rows,summary_rows,totals,examples=compare_pairs(maps,apis)
    fixtures=original_e1_fixtures()
    tests=subprocess.run([sys.executable,"-m","unittest","discover","-q",
                          "research/externality_estimator/tests"],text=True,capture_output=True)
    fail_unless(tests.returncode==0,"Frozen E1 no-SUMO test suite failed: "+tests.stderr[-2000:])
    j4={
      "study":"Post E1 Stage1D J0-J4 static priority-junction rule verification",
      "status":"VERIFIED_STATIC_MISMATCH",
      "original_E1_Stage1D":"DEVELOPMENT_NOT_QUALIFIED",
      "original_Exp007_Test_A":"NO_GO",
      "new_independent_validation":"NOT_STARTED",
      "cooperative_Test_B":"NOT_RUN",
      "sumo_simulations_executed":0,
      "estimator_source_changed":False,
      "J0":j0,
      "J1":{
         "request_to_movement_mappings":len(movement_rows),
         "priority_junctions":len(maps),
         "independent_methods":["incLanes+connection order as pinned Node.getLinkIndex",
                                "generated internal via lane index",
                                "actual pinned sumolib Node.getLinkIndex"],
         "pinned_sumolib_foes_response_checks":len(pair_rows)*4,
         "unresolved_mappings":0,"status":"PASS"
      },
      "J2":{
         "unordered_pairs":len(pair_rows),
         "mutual_nonfoes":totals["nonfoe_count"],
         "foes":totals["foe_count"],
         "nonfoe_distinct_source_destination_via":len(difference_rows),
         "nonfoe_distinct_source_destination_via_and_cont0":totals["strict_cont0_nonfoes"],
         "junctions_with_clean_nonfoes":sum(x["clean_potential_nonfoes_distinct_in_out"]>0 for x in summary_rows),
         "status":"VERIFIED_STATIC_NONFOE_RELATIONS_NOT_DYNAMICAL_CAPACITY"
      },
      "J3":{
         "frozen_e1_fixtures":len(fixtures),"no_sumo_original_unit_tests":"PASS",
         "all_clean_pairs_excluded_by_E1_one_conflict_class":len(difference_rows),
         "fixture_validity":"MODEL_ONLY - alternative conflict labels are stipulated, not a corrected estimator",
         "status":"PASS_EXPLANATORY_ONLY"
      },
      "J4":{
         "decision":"VERIFIED_STATIC_MISMATCH; DYNAMIC_EFFECT_UNKNOWN",
         "known":"E1 all-class forbids within-tick crossing of mutually non-foe, distinct-source/destination pairs",
         "unknown":"Whether/when vehicles simultaneously traverse those SUMO movements and how much E1 development error is attributable",
         "causal_claim":"NOT_ESTABLISHED",
         "future_work":"Only separately authorized new E1-v2 design or controlled SUMO instrumented/micro-test"
      }
    }
    write_csv(out/"sumo_request_to_connection_map.csv",movement_rows)
    write_csv(out/"sumo_priority_pairwise_rules.csv",pair_rows)
    write_csv(out/"e1_vs_sumo_junction_rule_differences.csv",difference_rows)
    write_csv(out/"junction_rule_summary.csv",summary_rows)
    write_csv(out/"original_network_raw_vs_canonical_manifest.csv",j0["network_evidence_by_seed"])
    write_json(out/"fixture_rule_comparisons.json",fixtures)
    write_json(out/"independent_crosscheck.json",{
         "sumolib_v1_28_0_commit":SUMO_SOURCE_COMMIT,
         "foe_directional_checks":len(pair_rows)*2,
         "response_directional_checks":len(pair_rows)*2,
         "via_index_agreement":len(movement_rows),
         "incoming_order_agreement":len(movement_rows),
         "sumolib_getLinkIndex_agreement":len(movement_rows),
         "mismatched_or_unknown":0,
         "node_source_sha256":j0["sumolib_node_sha256"]
    })
    write_json(out/"e1_junction_rule_source_manifest.json",j0)
    write_json(out/"j0_j4_scientific_summary.json",j4)
    (out/"scientific_readout.md").write_text(
         "# E1 J0-J4 Junction-Rule Verification: archive-only outcome\n\n"
         "**VERIFIED STATIC MISMATCH; DYNAMIC CONTRIBUTION UNKNOWN.**\n\n"
         "Mapped all 1,320 priority movements to their request bits using independent incoming lane order, via indices and the exact pinned SUMO 1.28.0 sumolib API. "
         "Of 8,836 distinct movement pairs, 5,764 are mutual non-foes, 3,940 are mutual non-foes with different incoming and receiving external lanes and different initial via lanes; 2,212 of those have cont=0 for both. "
         "Every candidate pair is excluded from the **same one-second tick** by frozen E1 conflict_class=all. "
         "These counts are static relationship differences, not observations of simultaneous vehicles or verified throughput loss. "
         "The 100 original priority-junction movement maps are complete. "
         "The entire original 706-member Stage1D archive was verified against the durable per-file release ledger. "
         "No simulations were run, no E1 source changed, and original Stage1D NO-GO and Test B nonexecution remain unchanged.\n\n"
         "Pinned SUMO v1_28_0 source: https://github.com/eclipse-sumo/sumo/tree/daf91b5578901d599ac9af53f49d26eeb9aefc3b/tools/sumolib\n",
         encoding="utf-8")
    print(json.dumps({"decision":j4["J4"]["decision"],"movements":len(movement_rows),
       "pairs":len(pair_rows),"nonfoes":totals["nonfoe_count"],
       "clean_nonfoes":len(difference_rows),"clean_cont0":totals["strict_cont0_nonfoes"],
       "unknown_mappings":0,"source_semantic_sha":j0["canonical_network_sha256"]},indent=2))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",required=True)
    parser.add_argument("--ledger",required=True)
    parser.add_argument("--pinned-source",required=True)
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    main(args.root,args.ledger,args.pinned_source,args.out)
