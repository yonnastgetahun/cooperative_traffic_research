#!/usr/bin/env python3
"""Review frozen-source M3 harness using development outcomes only (seed 2101)."""
import argparse,csv,json,math
from pathlib import Path

FROZEN="be2e8d27c78c8b6de4891115d6d951edc877ac6e"
WINDOWS=(200,600,1200)

def readjson(path):
    return json.loads(Path(path).read_text())

def summarize(root,reference,out):
    root=Path(root);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    with open(reference,newline="") as f:
        previous={int(r["window_seconds"]):r for r in csv.DictReader(f)}
    if set(previous)!=set(WINDOWS):raise RuntimeError("Reference regime coverage incomplete")
    rows=[]
    for w in WINDOWS:
        folder=root/f"exp002-M3-QUALIFY-window-{w}-seed2101"
        if not folder.is_dir():raise RuntimeError("Missing development qualification: "+str(w))
        guard=readjson(folder/"frozen-source-integrity.json")
        inputs=readjson(folder/"seed-and-topology-integrity.json")
        model=readjson(folder/"seed-level-metrics.json")
        audit=readjson(folder/"search-lookup-integrity.json")
        stats=readjson(folder/"r3-exception-audit.json")
        native=readjson(folder/"native-event-integrity.json")
        trip=readjson(folder/"tripinfo-invariance.json")
        bridge=readjson(folder/"paired-reference-report.json")
        assert guard["frozen_sha"]==FROZEN and guard["heldout_authorized"] is False
        assert guard["fingerprint_files_verified"]>=10
        assert inputs["status"]=="PASS" and inputs["seed_specific_od_and_depart_schedule_equal"]
        assert audit["status"]=="PASS" and model["vehicles"]==1000
        assert audit["assigned_edges"]==model["edge_traversals"]
        assert model["seed"]==2101 and model["window_seconds"]==w
        assert model["frozen_scientific_commit"]==FROZEN
        assert stats["reported_teleports"]["teleport_state"]=="ZERO_CONFIRMED"
        assert stats["reported_teleports"]["teleports_total"]==0
        assert stats["exception_gate"]=="PASS_FOR_THIS_REPLAY"
        assert trip["status"]=="PASS" and native["vehicles_with_parsed_events"]==1000
        assert bridge["planned_edges"]==bridge["matched"]==model["edge_traversals"]
        assert (folder/"policy-invariance.txt").is_file()
        metrics=model["timing_metrics"]
        prior=previous[w]
        if abs(metrics["timeaware"]["mae_s"]-float(prior["native_timeaware_MAE_s"]))>0.0001:
            raise RuntimeError("Qualification differs from previously inspected M3 development native timing for "+str(w))
        if abs(metrics["freeflow"]["mae_s"]-float(prior["native_freeflow_MAE_s"]))>0.0001:
            raise RuntimeError("Free-flow model differs from frozen development reference")
        row=dict(seed=2101,window_seconds=w,
                 frozen_commit=FROZEN,
                 completed_vehicles=model["vehicles"],matched_edges=model["edge_traversals"],
                 actual_search_reads=audit["edge_cost_reads_observed"],
                 assigned_edges=audit["assigned_edges"],
                 timeaware_MAE_s=metrics["timeaware"]["mae_s"],
                 freeflow_MAE_s=metrics["freeflow"]["mae_s"],
                 paired_benefit_s=model["paired_MAE_benefit_ff_minus_timeaware_s"],
                 lateness_bias_s=metrics["timeaware"]["bias_s"],
                 native_FCD_entry_step_difference_MAE_s=metrics["FCD_minus_native"]["mae_s"],
                 reported_teleports=stats["reported_teleports"]["teleports_total"],
                 native_internal_link_events=native["internal_event_rows"],
                 invariant_original_routes=True,invariant_trips=True,
                 scenario_gate="PASS_DEVELOPMENT_ONLY")
        rows.append(row)
    fields=list(rows[0])
    with open(out/"qualification-by-regime.csv","w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    summary=dict(status="READY_FOR_SEPARATE_HELDOUT_RUNNER_REVIEW_NOT_AUTHORIZED_TO_RUN",
       frozen_scientific_commit=FROZEN,development_seed=2101,
       verified_regimes=list(WINDOWS),verified_scenarios=3,
       completed_vehicles=3000,matched_edges=sum(x["matched_edges"] for x in rows),
       actual_search_reads=sum(x["actual_search_reads"] for x in rows),
       all_source_input_hashes_and_generator_validated=True,
       matched_original_forecast_metrics=True,
       event_capture_complete=True,teleports_explicitly_zero_for_qualifier=True,
       heldout_data_touched=False,
       runnable_heldout_workflow_enabled=False,
       executed_interpretation="Synthetic development-only qualification; no held-out evaluation or independent routing benefit tested")
    (out/"qualification-integrity.json").write_text(json.dumps(summary,indent=2)+"\n")
    lines=["# Frozen M3 runner — development-only qualification","",
        "**Status:** Full frozen-science harness rehearsed in three previously inspected development conditions. **No held-out seeds run or authorized.**","",
        "| Window | Chosen-route time-aware MAE | Free-flow MAE | Search reads verified | Teleports reported |",
        "|---|---:|---:|---:|---:|"]
    for r in rows:
        lines.append(f"| {r['window_seconds']}s | {r['timeaware_MAE_s']:.2f}s | {r['freeflow_MAE_s']:.2f}s | {r['actual_search_reads']:,} | {r['reported_teleports']} |")
    lines += ["","All development OD, routes, trip outcomes and analysis metrics match frozen preinspected observations.",
        "Reserved evaluation seeds were rejected by the active runner's guard and never generated, simulated or read.",
        "Freeze commit is pinned; native physical road occupancy is not the planner's count of route assignments.",
        "**Only execution readiness is being assessed; a separate approval is required to activate any held-out workflow.**",""]
    (out/"QUALIFICATION_REPORT.md").write_text("\n".join(lines))
    print("\n".join(lines))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True);p.add_argument("--reference",required=True)
    p.add_argument("--out",required=True)
    a=p.parse_args();summarize(a.root,a.reference,a.out)

if __name__=="__main__":main()
