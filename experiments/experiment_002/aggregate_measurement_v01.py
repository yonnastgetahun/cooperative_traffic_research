#!/usr/bin/env python3
"""Summarize all 9 prespecified development seeds without treating vehicle rows as independent seeds."""
import argparse, csv, glob, json, statistics, xml.etree.ElementTree as ET
from pathlib import Path

WINDOWS=(200,600,1200); SEEDS=(2101,2102,2103)
def trip_ods(path):
    return tuple((t.get("id"),t.get("from"),t.get("to"))
        for t in ET.parse(path).getroot().findall("trip"))
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    Path(a.out).mkdir(parents=True,exist_ok=True)
    rows=[]; missing=[];ods={}
    for seed in SEEDS:
        for window in WINDOWS:
            folder=Path(a.root)/f"exp002-occupancy-M2-window-{window}-seed{seed}"
            if not folder.is_dir():
                missing.append(str(folder));continue
            m=json.loads((folder/"measurement-report.json").read_text())
            prediction=json.loads((folder/"actual-predictor-report.json").read_text())
            scenario=json.loads((folder/"scenario.json").read_text())
            if scenario["seed"]!=seed or scenario["window_seconds"]!=window:
                raise RuntimeError("Scenario metadata mismatch "+str(folder))
            od=trip_ods(folder/"trips.xml")
            if seed in ods and ods[seed]!=od:
                raise RuntimeError(f"OD pairs changed across windows for seed {seed}")
            ods[seed]=od
            errors=prediction["forecast_error_seconds"]
            row={"seed":seed,"window_seconds":window,
                "completed":m["completed_vehicles"],
                "planned":m["planned_vehicles"],
                "matched_route_vehicles":m["matched_route_vehicles"],
                "planned_edges":m["planned_edges"],
                "matched_external_segments":m["matched_external_segments"],
                "internal_visible_segments":m["internal_visible_segments"],
                "fcd_internal_vehicle_samples":m["FCD"]["internal_vehicle_samples"],
                "fcd_external_stop_seconds":m["observed_external_stop_under_0_1_seconds"],
                "unresolved_transition_seconds":m["unresolved_transition_seconds"],
                "native_FCD_vehiclesec_mae":m["native_FCD_sampledSeconds_difference"]["mae"],
                "timeaware_entry_mae_s":errors["entry_timeaware"]["mae_s"],
                "timeaware_entry_bias_s":errors["entry_timeaware"]["bias_s"],
                "freeflow_entry_mae_s":errors["entry_freeflow"]["mae_s"],
                "timeaware_entry_p95_s":errors["entry_timeaware"]["abs_p95_s"],
                "mean_trip_duration_s":prediction["mean_trip_duration_seconds"],
                "mean_waiting_s":prediction["mean_waiting_seconds"]}
            if row["completed"]!=1000 or row["planned"]!=1000:
                raise RuntimeError("Incomplete trips for "+str(folder))
            if row["matched_route_vehicles"]<950:
                raise RuntimeError("Measurement route coverage under 95%")
            rows.append(row)
    if missing:raise RuntimeError("Missing M2 artifacts: "+",".join(missing))
    if len(rows)!=9:raise RuntimeError("Not all 3x3 scenarios available")
    csvpath=Path(a.out)/"per-seed-measurement.csv"
    with open(csvpath,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    lines=["# Experiment 002 M2 — Occupancy & junction measurement development matrix",
       "", "**Status: 9 development scenarios completed. This is not held-out validation.**",
       "", "Three prespecified calibration seeds (2101, 2102, 2103) across the same",
       "200/600/1200-second departure windows, each with 1,000 matched trips.",
       "All origin-destination lists matched across windows for a given seed.",
       "Original route policy and 30-second model parameters were not changed.",
       "", "| Regime | Time-aware entry MAE across three seeds (s, mean ± sample SD) | Free-flow MAE (s) | Mean route match rate |",
       "|---|---:|---:|---:|"]
    for window in WINDOWS:
        group=[x for x in rows if x["window_seconds"]==window]
        tf=[x["timeaware_entry_mae_s"] for x in group]
        ff=[x["freeflow_entry_mae_s"] for x in group]
        coverage=[x["matched_route_vehicles"]/x["planned"] for x in group]
        lines.append(f"| {window}s | {statistics.mean(tf):.2f} ± {statistics.stdev(tf):.2f} | {statistics.mean(ff):.2f} | {100*statistics.mean(coverage):.2f}% |")
    lines+=["","## Scientific limits",
       "- These are three development seeds per regime. A three-seed SD is descriptive, not proof of predictive reliability, statistical significance or adequate power.",
       "- Error measurements use chosen routes only, no unobserved counterfactuals.",
       "- FCD vehicle-seconds and native SUMO sampledSeconds may legitimately differ.",
       "- Model prior-assignment counts are not actual road occupancy.",
       "- Internal-link time and external approach stopping do not identify the cause of junction delay.",
       "- Reserved held-out seeds 3101–3110 were not used.",
       "","## Next decision",
       "Inspect native/FCD measurement agreement, missingness, junction visibility and 10/30/60s plus 1/2/5s sensitivity before freezing the protocol.",
       "Do not launch held-out evaluation without a separate freeze gate."]
    (Path(a.out)/"M2_DEVELOPMENT_REPORT.md").write_text("\n".join(lines)+"\n")
    (Path(a.out)/"m2-integrity.json").write_text(json.dumps({"scenarios":len(rows),
          "windows":WINDOWS,"seeds":SEEDS,"heldout_evaluated":False,
          "all_completed_1000":True,"od_matches_across_windows":True,
          "status":"development_not_heldout_validation"},indent=2))
    print("\n".join(lines))

if __name__=="__main__":main()
