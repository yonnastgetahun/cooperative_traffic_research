#!/usr/bin/env python3
"""Aggregate R3 source and exceptional-event evidence for three development regimes."""
import argparse,csv,json
from pathlib import Path

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    root=Path(a.root);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
    rows=[];critical=[]
    for w in (200,600,1200):
        path=root/f"exp002-R3-exception-audit-window-{w}-seed2101"
        if not path.is_dir():raise RuntimeError("Missing R3 scenario artifact "+str(w))
        r=json.loads((path/"r3-exceptions.json").read_text())
        inv=json.loads((path/"simulation-invariance.json").read_text())
        if r["seed"]!=2101 or r["window_seconds"]!=w:
            raise RuntimeError("Unexpected seed/window in R3 aggregate")
        if inv["status"]!="PASS" or r["matched_trip_count"]!=1000 or not r["tripinfo_invariant"]:
            raise RuntimeError("No genuine policy/control invariance in R3")
        state=r["reported_teleports"]["teleport_state"]
        summary=r["native_edge_bins"]["status_counts"]
        row=dict(seed=2101,window_seconds=w,trip_completions=r["matched_trip_count"],
            teleport_state=state,teleport_total=r["reported_teleports"]["teleports_total"],
            collisions_reported=r["reported_teleports"]["safety"].get("collisions") if r["reported_teleports"]["safety"] else None,
            FCD_timestep_count=r["reported_FCD"]["timestep_count"],
            FCD_missing_internal_samples=r["reported_FCD"]["within_trip_disappearance_count"],
            native_bins=r["native_edge_bins"]["native_bins"],
            full_native_bins=summary.get("FULL_30_SECOND_BIN",0),
            partial_native_bins=summary.get("PARTIAL_NATIVE_BIN",0),
            native_displayed_zero_samples=summary.get("DISPLAYED_ZERO_SAMPLED_SECONDS",0),
            native_empty_edge_no_metrics=summary.get("EMPTY_NATIVE_EDGE_NO_SAMPLES",0),
            native_positive_with_missing_metric=summary.get("MISSING_NATIVE_METRIC_WITH_POSITIVE_SAMPLES",0),
            exception_gate=r["exception_gate"])
        rows.append(row)
        if state!="ZERO_CONFIRMED" or r["exception_gate"]!="PASS_FOR_THIS_REPLAY":critical.append(w)
    with open(out/"r3-regime-exception-summary.csv","w",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
    summary=dict(status="R3_DEVELOPMENT_AUDIT_COMPLETE",
        windows=[200,600,1200],development_seed=2101,
        reference_run=40446073958,
        scenario_count=3, all_original_trips_reproduced=True,
        teleports_zero_confirmed_all_regimes=all(r["teleport_state"]=="ZERO_CONFIRMED" for r in rows),
        exception_clear_regimes=[r["window_seconds"] for r in rows if r["exception_gate"]=="PASS_FOR_THIS_REPLAY"],
        exception_open_regimes=critical,
        note="Historical M2 artifacts did not contain explicit teleport statistics; zero/positive results here describe strictly matched development reruns, not original missing metrics.",
        heldout_evaluated=False)
    (out/"r3-integrity.json").write_text(json.dumps(summary,indent=2)+"\n")
    lines=["# R3 — Three-regime exceptional-event and missingness development audit","",
       "**This checks observation policy on existing development seed 2101. It does not freeze M3 or validate the predictor.**","",
       "| Window | Teleport state | Count | Native empty bins | Partial bins | Exception gate |",
       "|---|---|---:|---:|---:|---|"]
    for row in rows:
        lines.append(f"| {row['window_seconds']}s | {row['teleport_state']} | {row['teleport_total']} | {row['native_empty_edge_no_metrics']:,} | {row['partial_native_bins']:,} | {row['exception_gate']} |")
    lines+=["","Native sampledSeconds displayed as zero can be rounded; absent speed/occupancy fields remain missing, not imputed as zeros.",
       "Statistics are from strictly matched development replays with original route and tripinfo invariance; this does not retroactively change archived original outputs.",
       "A nonzero teleport count blocks uninterrupted chosen-road timing claims; collision and teleport counts are not a real-world safety certification.",
       "No evaluation seeds have been run.",""]
    (out/"R3_DEVELOPMENT_EXCEPTION_REPORT.md").write_text("\n".join(lines))
    print("\n".join(lines))

if __name__=="__main__":main()
