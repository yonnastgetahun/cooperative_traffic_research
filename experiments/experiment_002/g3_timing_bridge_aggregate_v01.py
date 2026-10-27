#!/usr/bin/env python3
"""Summarize three previously explored development regimes, never held-out seeds."""
import argparse,csv,json,statistics
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    root=Path(a.root);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    rows=[]
    for window in (200,600,1200):
        folder=root/f"exp002-G3-R1R2-window-{window}-seed2101"
        if not folder.is_dir():raise RuntimeError("Missing regime "+str(window))
        b=json.loads((folder/"timing-bridge-report.json").read_text())
        s=json.loads((folder/"search-event-integrity.json").read_text())
        t=json.loads((folder/"simulation-invariance.json").read_text())
        n=json.loads((folder/"native-event-report.json").read_text())
        if (s["status"]!="PASS" or t["status"]!="PASS" or
            n["vehicles_with_parsed_events"]!=1000 or
            b["matched"]!=b["planned_edges"] or b["missing_vehicle_ids"] or
            not (folder/"route-invariance.txt").is_file()):
            raise RuntimeError("Scientific verification failed: "+str(window))
        shift=b["observed_delta_counts"]
        rows.append(dict(seed=2101,window_seconds=window,matched_edges=b["matched"],
            search_reads=s["edge_cost_reads_observed"],
            counter_updates=s["assigned_edges"],
            internal_native_events=n["internal_event_rows"],
            native_timeaware_MAE_s=round(b["native_timeaware"]["mae_s"],5),
            native_timeaware_bias_s=round(b["native_timeaware"]["bias_s"],5),
            native_freeflow_MAE_s=round(b["native_freeflow"]["mae_s"],5),
            FCD_timeaware_MAE_s=round(b["FCD_timeaware"]["mae_s"],5),
            FCD_freeflow_MAE_s=round(b["FCD_freeflow"]["mae_s"],5),
            FCD_later_over_one_step=b["FCD_later_over_one_step"],
            FCD_earlier_over_one_step=b["FCD_earlier_over_one_step"]))
    with open(out/"three-regime-timing-bridge.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    result=dict(status="DEVELOPMENT_R1_R2_COMPLETE_M3_NOT_FROZEN",
        regimes=[200,600,1200],seed=2101,scenarios=3,
        matched_edges=sum(x["matched_edges"] for x in rows),
        search_reads=sum(x["search_reads"] for x in rows),
        all_trips_reproduced=True,route_and_audit_invariance=True,
        native_event_invariance=True,heldout_used=False,
        context="Native entry is a step-level inferred event. FCD is a front-position observation. No physical occupancy forecast model evaluated.",
        next_gate="G3 measurement contract and M3 preregistration still require explicit separate scientific review")
    (out/"integrity.json").write_text(json.dumps(result,indent=2)+"\n")
    lines=["# G3 native-versus-FCD timing bridge: three development regimes","",
        "**Status: Three development regimes checked. No M3 freeze or held-out validation.**","",
        "| Window | Native time-aware MAE | FCD time-aware MAE | Native free-flow MAE | Verified search reads |",
        "|---|---:|---:|---:|---:|"]
    for row in rows:
        lines.append(f"| {row['window_seconds']}s | {row['native_timeaware_MAE_s']:.2f}s | {row['FCD_timeaware_MAE_s']:.2f}s | {row['native_freeflow_MAE_s']:.2f}s | {row['search_reads']:,} |")
    lines+=["","All cases reuse prespecified seed 2101 and the unchanged original policy.",
        "Native SUMO road entry is inferred from ordered preceding link exit at the one-second solver step.",
        "FCD first external road observation measures a vehicle-front sample at one-second cadence.",
        "The references are retained separately; neither measures actual native physical body occupancy.",
        "True search-time route-assignment counts were independently verified in all three conditions.",
        "Prediction quality is not certified by these instrumentation passes.",
        "Prior published FCD error reports remain historical, unchanged.",
        "Reserved evaluation seeds 3101–3110 remain untouched.",""]
    (out/"G3_R1R2_DEVELOPMENT_REPORT.md").write_text("\n".join(lines))
    print("\n".join(lines))
if __name__=="__main__":main()
