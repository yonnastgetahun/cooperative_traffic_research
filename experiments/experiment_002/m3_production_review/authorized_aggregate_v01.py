#!/usr/bin/env python3
"""Consolidate only 30 eligible, hashed M3 scenario bundles; preserve NO-GO diagnostics."""
import argparse,json,sys
from pathlib import Path
from production_bundle_validator_v01 import validate_bundle
from adapters_v01 import REGIMES,Ineligible,summarize_seed_level
from release_record_v01 import SEEDS
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from g3_r4_seed_analysis_v01 import mean_ci_if_ten

def aggregate(root,out):
    root=Path(root);out=Path(out);out.mkdir(parents=True,exist_ok=True)
    records=[];errors=[]
    for seed in SEEDS:
        for window in REGIMES:
            folder=root/f"m3-eval-seed-{seed}-window-{window}"
            try:
                if not folder.is_dir():raise Ineligible("Missing scenario artifact")
                records.append(validate_bundle(folder,seed,window))
            except Exception as exc:
                errors.append(dict(seed=seed,window_seconds=window,error=str(exc)))
    status=dict(expected_scenarios=30,validated_scenarios=len(records),
                failures=errors,scientific_conclusion_permitted=False)
    (out/"completeness.json").write_text(json.dumps(status,indent=2)+"\n")
    if errors:
        (out/"RESULT.md").write_text("# M3 evaluation incomplete\n\n"
            "One or more prespecified scenarios failed or were ineligible. "
            "No seed substitution and no planned ten-seed inference. "
            "See completeness.json for exceptions.\n")
        raise Ineligible(f"{len(errors)} prespecified scenarios missing/ineligible")
    summary=summarize_seed_level(records,SEEDS,mean_ci_if_ten)
    status["scientific_conclusion_permitted"]=True
    (out/"completeness.json").write_text(json.dumps(status,indent=2)+"\n")
    (out/"seed-records.json").write_text(json.dumps(records,indent=2)+"\n")
    (out/"scientific-results.json").write_text(json.dumps(summary,indent=2)+"\n")
    lines=["# M3 frozen held-out evaluation", "",
      "Thirty prespecified scenarios passed eligibility and artifact integrity.",
      "Primary regime: 200 seconds; secondary: 600 and 1200 seconds.",
      "Uncertainty unit: independent demand seed (n=10), not road traversals.", "",
      "| Window | Mean paired MAE benefit (s) | 95% Student-t CI (s) |",
      "|---|---:|---|"]
    for x in summary["regimes"]:
        lines.append(f'| {x["window_seconds"]} | {x["paired_benefit_mean_s"]:.3f} | '
            f'[{x["confidence_interval_95_s"][0]:.3f}, {x["confidence_interval_95_s"][1]:.3f}] |')
    lines += ["","Forecast timing accuracy does not establish causal network-wide routing benefit or real-world safety."]
    (out/"RESULT.md").write_text("\n".join(lines)+"\n")
    return summary

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--root",required=True);p.add_argument("--out",required=True)
    a=p.parse_args()
    print(json.dumps(aggregate(a.root,a.out),indent=2))
