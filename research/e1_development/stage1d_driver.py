#!/usr/bin/env python3
"""E1 Stage 1D: predeclared DEV_BUILD/DEV_CHECK only, never independent validation.

No externality predictor in this script reads SUMO outputs. Every prospective
prediction is immutably saved BEFORE the corresponding SUMO label is generated.
The SOURCE REVIEW and frozen Stage 1B docs govern this research process.
"""
from __future__ import annotations
import argparse, csv, dataclasses, hashlib, importlib.util, json, os
import pathlib, statistics, subprocess, sys, time, xml.etree.ElementTree as ET
from collections import defaultdict

from research.externality_estimator.schema import Parameters, InvalidScenario
from research.externality_estimator.scenario_io import from_sumo_static_xml
from research.externality_estimator.dataset_contract import select_development_probes
from research.externality_estimator.audit import check_partition, sha256, save_prediction_once
from research.externality_estimator.counterfactual_rollout import predict_counterfactual, predict_bundle
from research.externality_estimator.baselines import historic_quadratic_externality
from research.externality_estimator.label_builder import label_from_tripinfo

P=pathlib.Path
BUILD=tuple(range(5101,5107))
CHECK=tuple(range(5111,5115))
QGRID=(0.35,0.50,0.65)
ARMS=("I","probe0","probe1","probe2","probe3","bundle")
IMAGE="ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb"

def digest(path):
    return hashlib.sha256(P(path).read_bytes()).hexdigest()

def write_once(path, obj):
    path=P(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("x",encoding="utf-8") as f:json.dump(obj,f,indent=2,sort_keys=True);f.write("\n")
    return digest(path)

def frozen_historic():
    p=P("experiments/experiment_007/run_v01.py")
    spec=importlib.util.spec_from_file_location("frozen_experiment_007",p)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def prepare(seed, root, scientific):
    partition="DEV_BUILD" if seed in BUILD else "DEV_CHECK"
    check_partition(seed,partition)
    out=P(root)/f"seed-{seed}"
    out.mkdir(parents=True,exist_ok=False)
    h=frozen_historic()
    net,data,edges,adj,candidates,common,independent,changes=h.setup(seed,out,scientific)
    assert len(data)==1000 and len(independent)==1000
    route_dir=out/"routes";route_dir.mkdir()
    route_files={}
    def route_file(arm, mapping):
        p=route_dir/f"{arm}.rou.xml"
        h.verify_routes(mapping,data,adj)
        h.write_routes(mapping,data,p)
        route_files[arm]=digest(p)
    route_file("I",independent)
    scenario=from_sumo_static_xml(net,out/"trips.xml",route_dir/"I.rou.xml",partition=partition)
    sel=select_development_probes(scenario,seed,partition)
    assert len(sel.probes)==4 and len({x.vehicle_id for x in sel.probes})==4
    probe_by_id={v.vehicle_id:v for v in sel.probes}
    for idx,probe in enumerate(sel.probes):
        alternate=dict(independent)
        alternate[probe.vehicle_id]=probe.alternate_route
        route_file(f"probe{idx}",alternate)
        assert sum(alternate[v]!=independent[v] for v in independent)==1
    bundle=dict(independent)
    for vid in sel.bundle_target_ids:
        bundle[vid]=probe_by_id[vid].alternate_route
    route_file("bundle",bundle)
    assert sum(bundle[v]!=independent[v] for v in independent)==2
    summary={
        "experiment":"post-exp007-e1-stage1d","seed":seed,"partition":partition,
        "source_frozen_development":True,"simulated":False,
        "n":1000,"network_sha256":digest(net),"demand_sha256":digest(out/"trips.xml"),
        "independent_routes_sha256":route_files["I"],"arm_route_sha256":route_files,
        "selection_sha256":sel.immutable_selection_sha,
        "fallback_notes":list(sel.fallback_notes),
        "probes":[{"slot":v.slot,"target_vehicle_id":v.vehicle_id,
                   "alternate_route":list(v.alternate_route),
                   "baseline_route":list(v.baseline_route),
                   "selection_sha":v.selection_sha,"reason":v.reason} for v in sel.probes],
        "bundle_target_ids":list(sel.bundle_target_ids),
        "bundle_overlap_score":sel.bundle_overlap_score,
        "model_sha256":digest(P("research/externality_estimator/link_turn_queue.py")),
        "candidate_source_sha256":digest(P("research/externality_estimator/candidate_routes.py")),
        "simulator_image":IMAGE,
        "baseline_method":"Original frozen Experiment 007 equal-announcement independent I pretrip route-selection"
    }
    write_once(out/"scenario-manifest.json",summary)
    return out,summary

def prediction_record(scenario, manifest, q, version):
    params=Parameters(q_sat=q)
    rows=[]
    for idx,p in enumerate(manifest["probes"]):
        pred=predict_counterfactual(scenario,p["target_vehicle_id"],tuple(p["alternate_route"]),
                                    params,version,uncertainty_seed=manifest["seed"])
        b1=historic_quadratic_externality(scenario,p["target_vehicle_id"],tuple(p["alternate_route"]))
        if pred.status!="OK":
            raise RuntimeError(f"E1 abstained before any outcome label; seed={manifest['seed']} q={q} idx={idx}: {pred.detail}")
        rows.append({
          "arm":f"probe{idx}","target_vehicle_ids":[p["target_vehicle_id"]],
          "q_sat":q,"status":pred.status,
          "pred_self_delta_s":pred.pred_self_delta_s,
          "pred_external_delta_network_s":pred.pred_external_delta_network_s,
          "pred_nonparticipant_delta_network_s":pred.pred_nonparticipant_delta_network_s,
          "pred_total_delta_network_s":pred.pred_all_delta_network_s,
          "per_driver_baseline_s":pred.per_driver_baseline_s,
          "per_driver_swap_s":pred.per_driver_swap_s,
          "model_prediction_hash":pred.prediction_hash,
          "b0_external":0.0,"b1_external":b1["pred_external_delta_network_s"],
          "b2_external":0.0,"source_selection_sha":p["selection_sha"],
          "elapsed_wall_s":pred.elapsed_wall_s
        })
    replacements={p["target_vehicle_id"]:tuple(p["alternate_route"]) for p in manifest["probes"]
                   if p["target_vehicle_id"] in manifest["bundle_target_ids"]}
    bundle=predict_bundle(scenario,replacements,params,version,uncertainty_seed=manifest["seed"])
    if bundle.status!="OK":raise RuntimeError("E1 bundle abstained before simulation")
    rows.append({"arm":"bundle","target_vehicle_ids":manifest["bundle_target_ids"],
        "q_sat":q,"status":bundle.status,
        "pred_self_delta_s":bundle.pred_self_delta_s,
        "pred_external_delta_network_s":bundle.pred_external_delta_network_s,
        "pred_nonparticipant_delta_network_s":bundle.pred_nonparticipant_delta_network_s,
        "pred_total_delta_network_s":bundle.pred_all_delta_network_s,
        "per_driver_baseline_s":bundle.per_driver_baseline_s,
        "per_driver_swap_s":bundle.per_driver_swap_s,
        "model_prediction_hash":bundle.prediction_hash,
        "b0_external":0.0,"b1_external":None,"b2_external":0.0,
        "elapsed_wall_s":bundle.elapsed_wall_s})
    return {"partition":manifest["partition"],"seed":manifest["seed"],"q_sat":q,
            "input_manifest_sha256":digest(P(version.split("@")[1])) if "@" in version else manifest["selection_sha256"],
            "scenario_sha256":sha256(scenario),
            "parameter_sha256":sha256(params),"model_version":"E1-STAGE1D-v1",
            "uncertainty":"UNCALIBRATED_LOW_FIDELITY_CONSERVATIVE_JUNCTION_CONFLICTS",
            "label_data_used":False,"rows":rows}

def make_predictions(seed_dir, selected_q=None):
    seed_dir=P(seed_dir)
    manifest=json.loads((seed_dir/"scenario-manifest.json").read_text())
    scenario=from_sumo_static_xml(seed_dir/"network.net.xml",seed_dir/"trips.xml",
                                   seed_dir/"routes/I.rou.xml",partition=manifest["partition"])
    q_values=QGRID if manifest["partition"]=="DEV_BUILD" else (selected_q,)
    if any(q not in QGRID for q in q_values):raise InvalidScenario("Illegal development calibration parameter")
    outdir=seed_dir/"predictions";outdir.mkdir(exist_ok=True)
    for q in q_values:
        path=outdir/f"E1-q-{q:.2f}.json"
        data=prediction_record(scenario,manifest,q,"E1-STAGE1D-v1")
        save_prediction_once(path,data)
    record={"seed":manifest["seed"],"partition":manifest["partition"],
            "predicted_parameter_values":list(q_values),
            "prediction_shas":{p.name:digest(p) for p in outdir.glob("*.json")}}
    write_once(seed_dir/"prediction-lock.json",record)
    return record

def simulator_preflight():
    v=subprocess.check_output(["sumo","--version"],text=True)
    if "1.28.0" not in v:raise RuntimeError(f"Unexpected SUMO version {v}")
    h=subprocess.check_output(["sumo","--help"],text=True)
    if "--additional-files" not in h:raise RuntimeError("Pinned SUMO lacks interval output flag")

def static_preflight(root,scientific):
    simulator_preflight()
    for seed in BUILD:prepare(seed,root,scientific)
    # Avoid opening check labels or forecasts before q_sat is build-selected.
    # Generate check route manifests only after calibration.
    print(json.dumps({"status":"PASS","phase":"DEV_BUILD_SOURCE_PREFLIGHT",
                      "seeds":list(BUILD),"simulated":False},indent=2))

def run_sumo_for_seed(seed_dir):
    seed_dir=P(seed_dir)
    man=json.loads((seed_dir/"scenario-manifest.json").read_text())
    lock=json.loads((seed_dir/"prediction-lock.json").read_text())
    if man["seed"]!=lock["seed"] or not lock["prediction_shas"]:
        raise RuntimeError("Missing prospective immutable prediction lock")
    for f,sha in lock["prediction_shas"].items():
        if digest(seed_dir/"predictions"/f)!=sha:
            raise RuntimeError("Prediction changed before sim; stop")
    original_ids={t.get("id"):float(t.get("depart")) for t in ET.parse(seed_dir/"trips.xml").getroot().findall("trip")}
    if len(original_ids)!=1000:raise RuntimeError("Incomplete announced demand")
    result_root=seed_dir/"observations";result_root.mkdir(exist_ok=False)
    observations={}
    for arm in ARMS:
        d=result_root/arm;d.mkdir()
        additional=ET.Element("additional")
        ET.SubElement(additional,"edgeData",id="e1-edge",file=str((d/"edgeData.xml.gz").resolve()),
                      period="5",withInternal="true",excludeEmpty="false")
        ET.SubElement(additional,"laneData",id="e1-lane",file=str((d/"laneData.xml.gz").resolve()),
                      period="5",withInternal="true",excludeEmpty="false")
        ap=d/"additional.xml";ET.ElementTree(additional).write(ap,encoding="utf-8",xml_declaration=True)
        cmd=["sumo","-n",str((seed_dir/"network.net.xml").resolve()),
             "-r",str((seed_dir/"routes"/f"{arm}.rou.xml").resolve()),
             "--tripinfo-output",str((d/"tripinfo.xml").resolve()),
             "--statistic-output",str((d/"statistics.xml").resolve()),
             "--collision-output",str((d/"collisions.xml").resolve()),
             "--seed",str(man["seed"]),"--no-step-log","true",
             "--log",str((d/"sumo.log").resolve()),"--additional-files",str(ap.resolve())]
        (d/"command.json").write_text(json.dumps(cmd,indent=2)+"\n")
        with (d/"sumo-stage.log").open("w") as log:
            process=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
        if process.returncode:raise RuntimeError(f"Seed {man['seed']} arm {arm} SUMO failed; see {log.name}")
        values=label_from_tripinfo(d/"tripinfo.xml",original_ids)
        if len(values)!=1000 or not (d/"edgeData.xml.gz").is_file():
            raise RuntimeError("Invalid whole-demand trip outcomes or absent edge observations")
        observations[arm]={"scheduled_to_arrival_s":values,
                           "tripinfo_sha256":digest(d/"tripinfo.xml"),
                           "network_total_s":sum(values.values()),
                           "statistics_sha256":digest(d/"statistics.xml")}
    write_once(seed_dir/"observations-summary.json",
               {"seed":man["seed"],"partition":man["partition"],
                "arm_order":list(ARMS),"observations":observations,
                "prediction_lock_sha256":digest(seed_dir/"prediction-lock.json"),
                "label_created_after_predictions":True})
    print(json.dumps({"seed":man["seed"],"status":"OBSERVATIONS_COMPLETE","n_arms":len(ARMS)}))

def effect_records(seed_dir,q):
    seed_dir=P(seed_dir)
    man=json.loads((seed_dir/"scenario-manifest.json").read_text())
    result=json.loads((seed_dir/"observations-summary.json").read_text())
    predictions=json.loads((seed_dir/"predictions"/f"E1-q-{q:.2f}.json").read_text())
    if predictions["q_sat"]!=q or predictions["seed"]!=man["seed"]:
        raise RuntimeError("Invalid q-sat prediction provenance")
    observed=result["observations"]
    base=observed["I"]["scheduled_to_arrival_s"]
    rows=[]
    targets={f"probe{i}":{p["target_vehicle_id"]} for i,p in enumerate(man["probes"])}
    targets["bundle"]=set(man["bundle_target_ids"])
    for r in predictions["rows"]:
        arm=r["arm"];changed=observed[arm]["scheduled_to_arrival_s"]
        if set(base)!=set(changed):raise RuntimeError("Matched demand ID mismatch")
        delta={v:changed[v]-base[v] for v in base}
        ids=targets[arm]
        actual_self=sum(delta[v] for v in ids)
        actual_ext=sum(dx for vid,dx in delta.items() if vid not in ids)
        actual_nonopt=sum(dx for vid,dx in delta.items() if int(vid[3:])%2)
        actual_total=sum(delta.values())
        if abs(actual_self+actual_ext-actual_total)>1e-6:
            raise RuntimeError("Observed network accounting mismatch")
        rows.append({"seed":man["seed"],"arm":arm,
            "q_sat":q,"observed_self":actual_self,"observed_external":actual_ext,
            "observed_total":actual_total,"observed_nonparticipant":actual_nonopt,
            "pred_external":r["pred_external_delta_network_s"],
            "pred_self":r["pred_self_delta_s"],
            "pred_total":r["pred_total_delta_network_s"],
            "pred_nonparticipant":r["pred_nonparticipant_delta_network_s"],
            "b0_external":r["b0_external"],"b1_external":r["b1_external"],
            "pred_benefit_real_harm":bool(r["pred_external_delta_network_s"] < 0 and actual_ext > 10),
            "model_prediction_hash":r["model_prediction_hash"],
            "changed_route_count":len(ids),
            "realized_nonparticipant_gt30_fraction":
              sum(dx>30 for vid,dx in delta.items() if int(vid[3:])%2)/500,
            "realized_any_gt30_fraction":sum(dx>30 for dx in delta.values())/1000})
    return rows

def make_build_calibration(root,out):
    by_q={}
    for q in QGRID:
        allrows=[]
        for seed in BUILD:
            allrows+=effect_records(P(root)/f"seed-{seed}",q)
        samples=[r for r in allrows if r["arm"].startswith("probe")]
        seed_mae={seed:statistics.mean(abs(r["pred_external"]-r["observed_external"]) for r in samples if r["seed"]==seed) for seed in BUILD}
        if any(not (n>=0) for n in seed_mae.values()):raise RuntimeError("Invalid calibrated error")
        by_q[f"{q:.2f}"]={"mean_seed_mae":statistics.mean(seed_mae.values()),"seed_mae":seed_mae,
                           "max_false_benefit_count":sum(r["pred_benefit_real_harm"] for r in samples)}
    priority={0.50:0,0.35:1,0.65:2}
    selection=min(QGRID,key=lambda q:(round(by_q[f"{q:.2f}"]["mean_seed_mae"],9),priority[q]))
    state={"status":"DEV_BUILD_CALIBRATION_COMPLETE","selected_q_sat":selection,
           "selection_method":"minimum mean of six seed-level singleton externality MAEs; fixed 0.50/0.35/0.65 tie-break",
           "build_seeds":list(BUILD),"by_q":by_q,"no_DEV_CHECK_used":True,"frozen_for_DEV_CHECK":True}
    write_once(out,state)
    print(json.dumps(state,indent=2))
    return selection

def assess_check(root,selected_q,out):
    allrows=[]
    for seed in CHECK:
        allrows+=effect_records(P(root)/f"seed-{seed}",selected_q)
    single=[r for r in allrows if r["arm"].startswith("probe")]
    def seed_mae(name):
        return {seed:statistics.mean(abs(r[name]-r["observed_external"]) for r in single if r["seed"]==seed) for seed in CHECK}
    e1=seed_mae("pred_external");b0=seed_mae("b0_external");b1=seed_mae("b1_external")
    me=statistics.mean(e1.values());m0=statistics.mean(b0.values());m1=statistics.mean(b1.values())
    qualified=me <= 0.95*min(m0,m1) and me<m0 and me<m1
    outcomes={
      "status":"DEVELOPMENT_QUALIFIED_FOR_SEPARATE_VALIDATION_PROTOCOL" if qualified else "DEVELOPMENT_NOT_QUALIFIED",
      "independent_validation":"NOT_STARTED","Test_B":"NOT_RUN",
      "selected_build_only_q_sat":selected_q,
      "metric":"mean of four independent DEV_CHECK seed-level MAEs (externality network-seconds)",
      "MAE_mean_E1":me,"MAE_mean_B0":m0,"MAE_mean_B1":m1,
      "by_seed":{"E1":e1,"B0":b0,"B1":b1},
      "E1_vs_best_baseline_improvement":(min(m0,m1)-me)/min(m0,m1) if min(m0,m1)>0 else None,
      "false_benefit_cases":sum(r["pred_benefit_real_harm"] for r in single),
      "model_uncertainty":"UNCALIBRATED_LOW_FIDELITY_CONSERVATIVE_JUNCTION_CONFLICTS",
      "samples":{"check_seeds":len(CHECK),"single_swaps":len(single),"bundle_arms":len(allrows)-len(single)},
      "seed_level_limitations":"Only four independent development-check seeds; within-seed probes share baseline; not independent confirmation",
      "historical_test_a":"NO-GO, unchanged"
    }
    write_once(out,outcomes)
    return outcomes,allrows

def develop(root,scientific):
    root=P(root)
    root.mkdir(parents=True,exist_ok=False)
    stage={"study":"E1_STAGE1D_DEVELOPMENT_ONLY","status":"IN_PROGRESS","allowed_seeds":{"build":list(BUILD),"check":list(CHECK)},"old_Test_A":"NO-GO","Test_B":"NOT_RUN"}
    try:
        simulator_preflight()
        for seed in BUILD:
            p,man=prepare(seed,root,scientific)
            make_predictions(p)
        # Every build forecast has been finalized before running any build SUMO label.
        stage["build_predictions_frozen"]=True
        for seed in BUILD:
            run_sumo_for_seed(root/f"seed-{seed}")
        q=make_build_calibration(root,root/"build-selected-parameter.json")
        stage["selected_q"]=q
        for seed in CHECK:
            p,man=prepare(seed,root,scientific)
            make_predictions(p,selected_q=q)
        stage["check_predictions_frozen_before_check_labels"]=True
        for seed in CHECK:
            run_sumo_for_seed(root/f"seed-{seed}")
        results,rows=assess_check(root,q,root/"development-verdict.json")
        stage["status"]=results["status"]
        with (root/"devcheck-probes.csv").open("w",newline="") as f:
            keys=list(rows[0])
            w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
    except Exception as error:
        stage["status"]="INCOMPLETE_OR_BLOCKED"
        stage["error"]=repr(error)
        write_once(root/"failure-manifest.json",stage)
        raise
    finally:
        (root/"stage1d-workflow-manifest.json").write_text(json.dumps(stage,indent=2)+"\n")
    print(json.dumps({"status":stage["status"],"selected_q":stage.get("selected_q"),"seeds":list(BUILD)+list(CHECK)},indent=2))

def main():
    a=argparse.ArgumentParser()
    a.add_argument("command",choices=("preflight","develop"))
    a.add_argument("--out",required=True)
    a.add_argument("--scientific",default="scientific")
    v=a.parse_args()
    if v.command=="preflight":static_preflight(v.out,v.scientific)
    else:develop(v.out,v.scientific)
if __name__=="__main__":
    main()
