#!/usr/bin/env python3
"""E1-v2-J1 V2-D1, FROZEN development-only prospective paired SUMO study.

New seeds 6101-6106 and 6111-6114 only. All baseline/one-swap/bundle route
decisions and EVERY model prediction are locked before any new simulator labels.
Never opens validation 6201-6212 or Test B 6301-6312. No calibration or E2.
"""
from __future__ import annotations
import argparse,csv,dataclasses,hashlib,json,os,pathlib,resource,statistics,sys,time
from collections import defaultdict
from research.e1_development import stage1d_driver as old
from research.e1_v2_development.selector import select_development_probes,BUILD,CHECK
from research.externality_estimator.schema import Parameters,InvalidScenario
from research.externality_estimator.scenario_io import from_sumo_static_xml
from research.externality_estimator.counterfactual_rollout import predict_counterfactual as predict_e1
from research.externality_estimator.counterfactual_rollout import predict_bundle as predict_e1_bundle
from research.externality_estimator.audit import sha256,save_prediction_once
from research.externality_estimator_v2.movement import compile_frozen_grid_network
from research.externality_estimator_v2.counterfactual import predict_counterfactual as predict_v2
from research.externality_estimator_v2.counterfactual import predict_bundle as predict_v2_bundle

P=pathlib.Path
SEEDS=tuple(sorted(BUILD))+tuple(sorted(CHECK))
ARMS=("I","probe0","probe1","probe2","probe3","bundle")
Q=0.5
PINNED_IMAGE=old.IMAGE

def write(path,value):
    return old.write_once(path,value)
def digest(path):
    return old.digest(path)

def static_seed(seed,root,scientific):
    if seed not in SEEDS:
        raise InvalidScenario("Unfrozen seed; no hidden data search permitted")
    partition="DEV_BUILD" if seed in BUILD else "DEV_CHECK"
    base=P(root)/("seed-"+str(seed))
    base.mkdir(parents=True,exist_ok=False)
    historic=old.frozen_historic()
    net,data,edges,adj,candidates,common,independent,changes=historic.setup(seed,base,scientific)
    if len(data)!=1000 or len(independent)!=1000:
        raise RuntimeError("Incomplete synthetic demand or independent routes")
    route_dir=base/"routes"
    route_dir.mkdir()
    route_hashes={}
    def route_file(name,mapping):
        historic.verify_routes(mapping,data,adj)
        dst=route_dir/(name+".rou.xml")
        historic.write_routes(mapping,data,dst)
        route_hashes[name]=digest(dst)
    route_file("I",independent)
    context=from_sumo_static_xml(net,base/"trips.xml",route_dir/"I.rou.xml",partition=partition)
    compiled=compile_frozen_grid_network(net)
    selection=select_development_probes(context,seed,partition)
    if len(selection.probes)!=4 or len(set(x.vehicle_id for x in selection.probes))!=4:
        raise RuntimeError("SEED_DESIGN_INVALID: exactly four unique approved probes required")
    byid={x.vehicle_id:x for x in selection.probes}
    for index,probe in enumerate(selection.probes):
        changed=dict(independent)
        changed[probe.vehicle_id]=probe.alternate_route
        if sum(changed[v]!=independent[v] for v in independent)!=1:
            raise RuntimeError("Single-probe changed-route count mismatch")
        route_file("probe"+str(index),changed)
    joint=dict(independent)
    for vid in selection.bundle_target_ids:
        joint[vid]=byid[vid].alternate_route
    if sum(joint[v]!=independent[v] for v in independent)!=2:
        raise RuntimeError("Bundle changed-route count mismatch")
    route_file("bundle",joint)
    manifest={
      "experiment":"E1_V2_D1_FROZEN_PROSPECTIVE_DEVELOPMENT",
      "seed":seed,"partition":partition,"n":1000,"simulated":False,
      "network_sha256":digest(net),"demand_sha256":digest(base/"trips.xml"),
      "independent_routes_sha256":route_hashes["I"],"arm_route_sha256":route_hashes,
      "selection_sha256":selection.immutable_selection_sha,
      "fallback_notes":list(selection.fallback_notes),
      "bundle_target_ids":list(selection.bundle_target_ids),
      "bundle_overlap_score":selection.bundle_overlap_score,
      "probes":[{"slot":x.slot,"target_vehicle_id":x.vehicle_id,
                 "baseline_route":list(x.baseline_route),
                 "alternate_route":list(x.alternate_route),
                 "selection_sha":x.selection_sha,"reason":x.reason} for x in selection.probes],
      "model_v1_sha256":digest("research/externality_estimator/link_turn_queue.py"),
      "model_v2_sha256":digest("research/externality_estimator_v2/network_evolution.py"),
      "movement_parser_sha256":digest("research/externality_estimator_v2/movement.py"),
      "movement_rules_canonical_sha":compiled.canonical_sha,
      "fixed_q_sat":Q,"simulator_image":PINNED_IMAGE,
      "baseline_method":"Original frozen Exp007 independent I pretrip assignment; idealized full announced demand"
    }
    write(base/"scenario-manifest.json",manifest)
    return base

def result_record(seed_dir):
    folder=P(seed_dir)
    manifest=json.loads((folder/"scenario-manifest.json").read_text())
    scenario=from_sumo_static_xml(folder/"network.net.xml",folder/"trips.xml",
                                  folder/"routes"/"I.rou.xml",partition=manifest["partition"])
    movement=compile_frozen_grid_network(folder/"network.net.xml")
    parameters=Parameters(q_sat=Q,max_wall_s=120.0)
    records=[]
    for i,probe in enumerate(manifest["probes"]):
        target=probe["target_vehicle_id"];route=tuple(probe["alternate_route"])
        v1=predict_e1(scenario,target,route,parameters,
                      model_version="FROZEN_E1_V1",uncertainty_seed=manifest["seed"])
        v2=predict_v2(scenario,target,route,movement,parameters,
                      model_version="E1_V2_J1_FROZEN",uncertainty_seed=manifest["seed"])
        if v1.status!="OK" or v2.status!="OK":
            raise RuntimeError("PREDICTION_ABSTAIN; seed "+str(manifest["seed"])+
                               " probe "+str(i)+" E1="+v1.status+" V2="+v2.status+
                               " detail="+v2.detail)
        prior=old.historic_quadratic_externality(scenario,target,route)
        records.append({
          "arm":"probe"+str(i),"target_ids":[target],"v1":dataclasses.asdict(v1),
          "v2":dataclasses.asdict(v2),"B0_external":0.0,
          "B1_external":prior["pred_external_delta_network_s"],
          "B2_external":0.0,
          "time_cutoff_s":scenario.t0_s,
          "source_selection_sha":probe["selection_sha"]
        })
    targets={probe["target_vehicle_id"]:tuple(probe["alternate_route"])
             for probe in manifest["probes"]
             if probe["target_vehicle_id"] in manifest["bundle_target_ids"]}
    v1=predict_e1_bundle(scenario,targets,parameters,
                          model_version="FROZEN_E1_V1",uncertainty_seed=manifest["seed"])
    v2=predict_v2_bundle(scenario,targets,movement,parameters,
                          model_version="E1_V2_J1_FROZEN",uncertainty_seed=manifest["seed"])
    if v1.status!="OK" or v2.status!="OK":
        raise RuntimeError("PREDICTION_ABSTAIN; bundle "+str(manifest["seed"])+
                           " E1="+v1.status+" V2="+v2.status+" "+v2.detail)
    records.append({"arm":"bundle","target_ids":manifest["bundle_target_ids"],
                    "v1":dataclasses.asdict(v1),"v2":dataclasses.asdict(v2),
                    "B0_external":0.0,"B1_external":None,"B2_external":0.0,
                    "time_cutoff_s":scenario.t0_s,
                    "source_selection_sha":manifest["selection_sha256"]})
    return {"partition":manifest["partition"],"seed":manifest["seed"],
            "model_version":"E1_V2_J1_FROZEN","q_sat":Q,
            "input_manifest_sha256":digest(folder/"scenario-manifest.json"),
            "scenario_sha256":sha256(scenario),
            "model_v1_sha256":manifest["model_v1_sha256"],
            "model_v2_sha256":manifest["model_v2_sha256"],
            "time_cutoff_s":scenario.t0_s,
            "observed_outcomes_used":False,
            "uncertainty":"UNCALIBRATED_DETERMINISTIC_POINT_PREDICTIONS",
            "rows":records}

def freeze_all_predictions(root):
    locks=[]
    for seed in SEEDS:
        directory=P(root)/("seed-"+str(seed))
        result=result_record(directory)
        p=directory/"predictions.json"
        sh=save_prediction_once(p,result)
        lock={"seed":seed,"partition":result["partition"],
              "prediction_sha256":sh,"prediction_file":"predictions.json",
              "prediction_shas":{"predictions.json":sh},
              "source_hash":result["model_v2_sha256"],
              "observed_outcomes_used":False}
        write(directory/"prediction-lock.json",lock)
        locks.append(lock)
    write(P(root)/"all-prediction-locks.json",
          {"status":"FROZEN_BEFORE_ANY_SUMO_OUTCOME","locked_seeds":list(SEEDS),
           "model":"E1_V2_J1_FROZEN","locks":locks})
    return locks

def validate_locks(root):
    all_locks=json.loads((P(root)/"all-prediction-locks.json").read_text())
    if all_locks["locked_seeds"]!=list(SEEDS):
        raise RuntimeError("All-seed prospective lock invalid")
    for seed in SEEDS:
        folder=P(root)/("seed-"+str(seed))
        lock=json.loads((folder/"prediction-lock.json").read_text())
        if lock["seed"]!=seed or digest(folder/"predictions.json")!=lock["prediction_sha256"]:
            raise RuntimeError("Prospective prediction file changed before outcomes")

def evaluate_seed(root,seed):
    folder=P(root)/("seed-"+str(seed))
    man=json.loads((folder/"scenario-manifest.json").read_text())
    obs=json.loads((folder/"observations-summary.json").read_text())["observations"]
    pred=json.loads((folder/"predictions.json").read_text())["rows"]
    base=obs["I"]["scheduled_to_arrival_s"]
    rows=[]
    for record in pred:
        arm=record["arm"]
        latest=obs[arm]["scheduled_to_arrival_s"]
        if set(base)!=set(latest) or len(base)!=1000:
            raise RuntimeError("SUMO matched trip cohort incomplete")
        delta={k:latest[k]-base[k] for k in base}
        target=set(record["target_ids"])
        expected=man["bundle_target_ids"] if arm=="bundle" else [man["probes"][int(arm[-1])]["target_vehicle_id"]]
        if target!=set(expected):
            raise RuntimeError("Observed target-route identity mismatch")
        observed_self=sum(delta[k] for k in target)
        observed_external=sum(dx for k,dx in delta.items() if k not in target)
        observed_nonopt=sum(dx for k,dx in delta.items() if int(k[3:])%2)
        observed_total=sum(delta.values())
        if abs(observed_self+observed_external-observed_total)>1e-6:
            raise RuntimeError("Observed self+external reconciliation failure")
        r={"seed":seed,"partition":man["partition"],"arm":arm,
           "target_ids":";".join(sorted(target)),
           "observed_self_s":observed_self,
           "observed_external_network_s":observed_external,
           "observed_nonparticipant_network_s":observed_nonopt,
           "observed_total_network_s":observed_total,
           "E1v2_self_s":record["v2"]["pred_self_delta_s"],
           "E1v2_external_network_s":record["v2"]["pred_external_delta_network_s"],
           "E1v2_nonparticipant_network_s":record["v2"]["pred_nonparticipant_delta_network_s"],
           "E1v2_total_network_s":record["v2"]["pred_all_delta_network_s"],
           "E1v1_external_network_s":record["v1"]["pred_external_delta_network_s"],
           "B0_external_network_s":record["B0_external"],
           "B1_external_network_s":record["B1_external"],
           "B2_external_network_s":record["B2_external"],
           "E1v2_wall_s":record["v2"]["elapsed_wall_s"],
           "E1v1_wall_s":record["v1"]["elapsed_wall_s"],
           "E1v2_predicted_benefit_realized_harm_gt30_network_s":
              int(record["v2"]["pred_external_delta_network_s"]<0 and observed_external>30),
           "E1v2_sign_match_material":
              int(abs(observed_external)>=10 and record["v2"]["pred_external_delta_network_s"]*
                  observed_external>0),
           "E1v2_predicted_zero":int(record["v2"]["pred_external_delta_network_s"]==0),
           "fraction_all_drivers_gt30s":sum(x>30 for x in delta.values())/1000,
           "fraction_nonparticipants_gt30s":
              sum(x>30 for vid,x in delta.items() if int(vid[3:])%2)/500}
        rows.append(r)
    return rows

def assess(root):
    rows=[]
    for seed in SEEDS:
        rows.extend(evaluate_seed(root,seed))
    singles=[x for x in rows if x["arm"].startswith("probe") and x["seed"] in CHECK]
    if len(singles)!=4*len(CHECK):
        raise RuntimeError("Check set incomplete")
    comparisons=["B0","B1","E1v1","E1v2"]
    keys={
      "B0":"B0_external_network_s",
      "B1":"B1_external_network_s",
      "E1v1":"E1v1_external_network_s",
      "E1v2":"E1v2_external_network_s"}
    seed_results={}
    for seed in sorted(CHECK):
        subset=[x for x in singles if x["seed"]==seed]
        seed_results[seed]={name:statistics.mean(abs(x[keys[name]]-
            x["observed_external_network_s"]) for x in subset) for name in comparisons}
    means={name:statistics.mean(seed_results[s][name] for s in sorted(CHECK))
           for name in comparisons}
    best=min(means[n] for n in ("B0","B1","E1v1"))
    gain=(best-means["E1v2"])/best if best else None
    seeds_better=sum(seed_results[s]["E1v2"]<
        min(seed_results[s][n] for n in ("B0","B1","E1v1")) for s in CHECK)
    material=[x for x in singles if abs(x["observed_external_network_s"])>=10]
    correct=sum(x["E1v2_sign_match_material"] for x in material)
    rate=correct/len(material) if material else None
    false_benefit=sum(x["E1v2_predicted_benefit_realized_harm_gt30_network_s"] for x in singles)
    # Predeclared CPU/RSS thresholds; Python ru_maxrss is process-level, not true per probe.
    maxwall=max(x["E1v2_wall_s"] for x in rows)
    peakrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    resource_pass=maxwall<=120 and peakrss<=2*1024*1024
    gates={
      "mean_MAE_improvement_at_least_10pct":gain is not None and gain>=0.10,
      "strictly_beats_all_frozen_comparators":
         all(means["E1v2"]<means[x] for x in ("B0","B1","E1v1")),
      "at_least_three_of_four_seeds_improve":seeds_better>=3,
      "at_least_ten_material_cases":len(material)>=10,
      "sign_match_at_least_60pct":rate is not None and rate>=0.60,
      "zero_severe_false_benefits":false_benefit==0,
      "prediction_lock_integrity":True,
      "all_60_Sumo_arms_complete":True,
      "offline_resource_pass":resource_pass}
    qualified=all(gates.values())
    report={
      "scientific_status":
        "DEVELOPMENT_QUALIFIED_FOR_SEPARATE_INDEPENDENT_VALIDATION" if qualified
        else "DEVELOPMENT_NOT_QUALIFIED",
      "model":"E1_V2_J1_FROZEN","new_validation":"NOT_STARTED","Test_B":"NOT_RUN",
      "n_seeds":10,"n_sumo_arms":60,"n_driver_tripinfos":60000,
      "check_seed_ids":list(CHECK),"check_arms":len(singles),
      "mean_seed_externality_MAE_network_s":means,
      "best_baseline_mean_MAE_network_s":best,
      "E1v2_improvement_over_best_baseline":gain,
      "check_seed_MAE":seed_results,"n_seeds_E1v2_better_than_own_best":seeds_better,
      "n_material":len(material),"n_directional_correct":correct,
      "directional_rate":rate,"false_benefit_count_gt30_network_s":false_benefit,
      "max_pair_wall_s":maxwall,"peak_process_rss_kb":peakrss,
      "gates":gates,"all_prediction_files_locked_before_Sumo":True,
      "uncertainty":"UNCALIBRATED_POINT_ESTIMATOR"}
    write(P(root)/"development-verdict.json",report)
    for name,sample in [("all-original-arm-effects.csv",rows),
                        ("check-singleton-effects.csv",singles)]:
        dest=P(root)/name
        with dest.open("x",newline="") as fd:
            writer=csv.DictWriter(fd,fieldnames=list(sample[0]))
            writer.writeheader();writer.writerows(sample)
    return report

def run(root,scientific,execution):
    root=P(root)
    root.mkdir(parents=True,exist_ok=False)
    status={"study":"FROZEN_E1_V2_D1_DEVELOPMENT_ONLY",
            "phase":"PREDECISION","new_build_seeds":sorted(BUILD),
            "new_check_seeds":sorted(CHECK),"original_Exp007_Test_A":"NO_GO",
            "original_E1_Stage1D":"DEVELOPMENT_NOT_QUALIFIED",
            "independent_validation":"NOT_STARTED","Test_B":"NOT_RUN",
            "simulator_executions":0}
    try:
        old.simulator_preflight()
        for seed in SEEDS:
            static_seed(seed,root,scientific)
        status["phase"]="PREDICTION_FREEZE"
        freeze_all_predictions(root)
        validate_locks(root)
        if not execution:
            status["phase"]="PREDECISION_PASS"
            status["predictions_complete"]=10*5
            return
        status["phase"]="DEVELOPMENT_SIMULATION"
        for seed in SEEDS:
            validate_locks(root)
            old.run_sumo_for_seed(root/("seed-"+str(seed)))
            status["simulator_executions"]+=len(ARMS)
        status["phase"]="SCIENTIFIC_ASSESSMENT"
        verdict=assess(root)
        status["phase"]=verdict["scientific_status"]
        print(json.dumps(verdict,indent=2))
    except Exception as error:
        status["phase"]="INCOMPLETE_OR_BLOCKED"
        status["error"]=repr(error)
        write(root/"failure-manifest.json",status)
        raise
    finally:
        (root/"workflow-provenance.json").write_text(json.dumps(status,indent=2)+"\n")
        print(json.dumps(status,indent=2))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("command",choices=("preflight","develop"))
    p.add_argument("--scientific",default="scientific")
    p.add_argument("--out",required=True)
    args=p.parse_args()
    run(args.out,args.scientific,args.command=="develop")
if __name__=="__main__":main()
