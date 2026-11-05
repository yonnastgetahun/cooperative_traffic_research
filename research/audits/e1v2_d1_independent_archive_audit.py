#!/usr/bin/env python3
"""Archive-only independent E1-v2 D1 development research audit; NO SUMO.

Reads immutable original predictions, source/route hashes and every raw SUMO
tripinfo from the already authorized 60-arm study. Never updates a model,
selects routes, opens future validation seeds or runs a simulation.
"""
import argparse,csv,hashlib,json,pathlib,statistics
import xml.etree.ElementTree as ET

BUILD=tuple(range(6101,6107));CHECK=tuple(range(6111,6115))
ALL=BUILD+CHECK
ARMS=("I","probe0","probe1","probe2","probe3","bundle")
N=1000

def read(path):return json.loads(pathlib.Path(path).read_text())
def sha(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
    return h.hexdigest()
def write(path,value):
    pathlib.Path(path).write_text(json.dumps(value,sort_keys=True,indent=2)+"\n")
def csv_write(path,rows):
    if not rows:return
    with open(path,"w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)

def originals(trips,tripinfo):
    expected={}
    for elem in ET.parse(trips).getroot().findall("trip"):
        vid=elem.get("id");expected[vid]=float(elem.get("depart"))
    if len(expected)!=N:raise AssertionError("Missing scheduled driver identity")
    actual={}
    for elem in ET.parse(tripinfo).getroot().findall("tripinfo"):
        vid=elem.get("id")
        if vid in actual:raise AssertionError("Duplicate SUMO identity")
        actual[vid]=float(elem.get("arrival"))-expected[vid]
    if set(actual)!=set(expected):
        raise AssertionError("SUMO demand identity noncompletion")
    return actual

def audit(root,out):
    root=pathlib.Path(root);out=pathlib.Path(out);out.mkdir(parents=True,exist_ok=True)
    locked=read(root/"all-prediction-locks.json")
    if locked["status"]!="FROZEN_BEFORE_ANY_SUMO_OUTCOME" or locked["locked_seeds"]!=list(ALL):
        raise AssertionError("Unfrozen or mismatched prospective seed list")
    allrows=[];source=[]
    for seed in ALL:
        folder=root/f"seed-{seed}"
        m=read(folder/"scenario-manifest.json")
        lock=read(folder/"prediction-lock.json")
        result=read(folder/"predictions.json")
        obs=read(folder/"observations-summary.json")
        partition="DEV_BUILD" if seed in BUILD else "DEV_CHECK"
        if (m["seed"]!=seed or m["partition"]!=partition or lock["seed"]!=seed
            or result["seed"]!=seed or obs["seed"]!=seed or len(result["rows"])!=5):
            raise AssertionError("Wrong seed/partition/forecast group")
        if sha(folder/"predictions.json")!=lock["prediction_sha256"]:
            raise AssertionError("Prediction changed from predecision SHA")
        if sha(folder/"network.net.xml")!=m["network_sha256"] or sha(folder/"trips.xml")!=m["demand_sha256"]:
            raise AssertionError("Original network/OD changed")
        for arm in ARMS:
            path=folder/"routes"/f"{arm}.rou.xml"
            if sha(path)!=m["arm_route_sha256"][arm]:
                raise AssertionError("Original route file modified")
        if len(m["probes"])!=4 or len(set(x["target_vehicle_id"] for x in m["probes"]))!=4:
            raise AssertionError("Invalid four-probe manifest")
        if len(set(m["bundle_target_ids"]))!=2:raise AssertionError("Invalid bundle")
        before=originals(folder/"trips.xml",folder/"observations"/"I"/"tripinfo.xml")
        original_routes={}
        for veh in ET.parse(folder/"routes"/"I.rou.xml").getroot().findall("vehicle"):
            original_routes[veh.get("id")]=tuple(veh.find("route").get("edges").split())
        for x in result["rows"]:
            arm=x["arm"]
            if arm not in ARMS[1:]:raise AssertionError("Unexpected arm")
            declared=set(x["target_ids"])
            expected=set(m["bundle_target_ids"]) if arm=="bundle" else {
                m["probes"][int(arm[-1])]["target_vehicle_id"]}
            if declared!=expected:raise AssertionError("Target identity mismatch")
            route_file=folder/"routes"/f"{arm}.rou.xml"
            changed_routes={}
            for veh in ET.parse(route_file).getroot().findall("vehicle"):
                changed_routes[veh.get("id")]=tuple(veh.find("route").get("edges").split())
            if set(changed_routes)!=set(original_routes) or {
                vid for vid in original_routes if original_routes[vid]!=changed_routes[vid]
              }!=declared:
                raise AssertionError("One- and two-swap exact original-route invariant failed")
            actual=originals(folder/"trips.xml",
                             folder/"observations"/arm/"tripinfo.xml")
            observed={vid:actual[vid]-before[vid] for vid in before}
            obs_self=sum(observed[v] for v in declared)
            obs_external=sum(d for vid,d in observed.items() if vid not in declared)
            obs_all=sum(observed.values())
            if abs(obs_self+obs_external-obs_all)>1e-6:
                raise AssertionError("Observed externality accounting not conserved")
            r1=x["v1"];r2=x["v2"]
            if any(r["status"]!="OK" for r in (r1,r2)):
                raise AssertionError("Abstained E1 model must not be silently scored")
            for r in (r1,r2):
                lhs=r["per_driver_baseline_s"];rhs=r["per_driver_swap_s"]
                if set(lhs)!=set(before) or set(rhs)!=set(before):
                    raise AssertionError("Incomplete per-identity predicted counterfactual")
                pred_self=sum(rhs[vid]-lhs[vid] for vid in declared)
                pred_ext=sum(rhs[vid]-lhs[vid] for vid in lhs if vid not in declared)
                if abs(pred_self-r["pred_self_delta_s"])>1e-6 or abs(pred_ext-r["pred_external_delta_network_s"])>1e-6:
                    raise AssertionError("Prospective predicted self/external cannot reconcile")
            allrows.append({
                "seed":seed,"partition":partition,"arm":arm,
                "observed_self_s":obs_self,"observed_external_network_s":obs_external,
                "observed_total_network_s":obs_all,
                "v2_self_s":r2["pred_self_delta_s"],
                "v2_external_network_s":r2["pred_external_delta_network_s"],
                "v1_external_network_s":r1["pred_external_delta_network_s"],
                "B0_external_network_s":x["B0_external"],
                "B1_external_network_s":x["B1_external"],
                "B2_external_network_s":x["B2_external"],
                "v2_false_benefit_gt30_network_s":
                    int(r2["pred_external_delta_network_s"]<0 and obs_external>30),
                "v2_sign_correct_material":
                    int(abs(obs_external)>=10 and r2["pred_external_delta_network_s"]*obs_external>0)})
        for arm in ARMS:
            o=obs["observations"][arm]
            if sha(folder/"observations"/arm/"tripinfo.xml")!=o["tripinfo_sha256"]:
                raise AssertionError("Tripinfo SHA diverged from original archived label")
        source.append({"seed":seed,"partition":partition,
                       "demand_sha256":m["demand_sha256"],
                       "network_sha256":m["network_sha256"],
                       "model_v2_sha256":m["model_v2_sha256"],
                       "prediction_sha256":lock["prediction_sha256"],
                       "completed_arms":6,
                       "matched_tripinfos":6000})
    if len(allrows)!=50 or len(source)!=10:
        raise AssertionError("Wrong frozen development footprint")
    check=[x for x in allrows if x["seed"] in CHECK and x["arm"].startswith("probe")]
    names={"B0":"B0_external_network_s","B1":"B1_external_network_s",
           "E1v1":"v1_external_network_s","E1v2":"v2_external_network_s"}
    seed_metrics={seed:{
        name:statistics.mean(abs(x[key]-x["observed_external_network_s"])
               for x in check if x["seed"]==seed)
        for name,key in names.items()} for seed in CHECK}
    average={name:statistics.mean(seed_metrics[s][name] for s in CHECK) for name in names}
    best=min(average[n] for n in ("B0","B1","E1v1"))
    gain=(best-average["E1v2"])/best if best>0 else None
    better=sum(seed_metrics[s]["E1v2"]<min(seed_metrics[s][n]
                   for n in ("B0","B1","E1v1")) for s in CHECK)
    material=[r for r in check if abs(r["observed_external_network_s"])>=10]
    correct=sum(r["v2_sign_correct_material"] for r in material)
    false_benefits=sum(r["v2_false_benefit_gt30_network_s"] for r in check)
    gates={
      "MAE_gain_at_least_10_percent":gain is not None and gain>=.10,
      "strictly_better_than_all_B0_B1_E1v1":all(average["E1v2"]<average[n] for n in ("B0","B1","E1v1")),
      "at_least_3_of_4_seed_improvement":better>=3,
      "at_least_10_material":len(material)>=10,
      "sign_at_least_60_percent":len(material)>0 and correct/len(material)>=.60,
      "zero_false_benefit_gt30_network_seconds":false_benefits==0,
      "all_routes_and_labels_complete":True,
      "all_prediction_lock_checks_passed":True
    }
    predicted_status="DEVELOPMENT_QUALIFIED_FOR_SEPARATE_INDEPENDENT_VALIDATION" if all(gates.values()) else "DEVELOPMENT_NOT_QUALIFIED"
    frozen=read(root/"development-verdict.json")
    if frozen["scientific_status"]!=predicted_status:
        # The original evaluator has an additional resource gate.
        if frozen["gates"].get("offline_resource_pass",False):
            raise AssertionError("Published scientific verdict differs from archive recomputation")
    for k in ("B0","B1","E1v1","E1v2"):
        if abs(frozen["mean_seed_externality_MAE_network_s"][k]-average[k])>1e-6:
            raise AssertionError("Original verdict MAE differs from original tripinfo")
    report={
       "status":"INDEPENDENT_ARCHIVE_RECONCILIATION_COMPLETE",
       "original_development_decision":frozen["scientific_status"],
       "original_Experiment007_TestA":"NO_GO",
       "new_independent_validation":"NOT_STARTED",
       "Test_B":"NOT_RUN",
       "unique_seed_count":10,
       "completed_sumo_arms":60,
       "completed_tripinfo_records":60000,
       "probe_and_bundle_prediction_records":50,
       "check_seed_level_MAE_network_seconds":seed_metrics,
       "mean_check_seed_MAE_network_seconds":average,
       "best_baseline_MAE_network_seconds":best,
       "v2_mean_gain_vs_best":gain,
       "n_improved_seeds":better,
       "material_single_probe_count":len(material),
       "correct_signed_material":correct,
       "severe_false_benefit_count":false_benefits,
       "preregistered_scientific_gates_recomputed":gates,
       "limitations":"Original outcomes, already-inspected development only; no fresh independent confirmation; no causal junction attribution."}
    write(out/"archive-independent-reconstruction.json",report)
    csv_write(out/"archive-50-arm-estimator-contrasts.csv",allrows)
    csv_write(out/"archive-source-manifest.csv",source)
    csv_write(out/"archive-check-seed-MAE.csv",
              [{"seed":s,**seed_metrics[s]} for s in CHECK])
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--root",required=True)
    parser.add_argument("--out",required=True)
    args=parser.parse_args()
    audit(args.root,args.out)
