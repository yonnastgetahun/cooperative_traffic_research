# Experiment 003 independent confirmatory cohort — frozen manifest

**Committed before execution.** Fresh confirmatory seeds: **3201–3210**, ten seeds, each at **200, 600 and 1200-second** departure windows (30 scenarios, 1,000 vehicles each). Excludes development seeds 2201–2210 and M3 held-out seeds 3101–3110.

**Frozen scientific code:** `be2e8d27c78c8b6de4891115d6d951edc877ac6e`; SUMO image digest `sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`.

**Frozen coefficients** from [development run 41017939494](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41017939494), artifact 12960840506:

| Regime | Offset a (seconds) | Per-route-edge b (seconds) |
|---|---:|---:|
| 200s | 4.053135104279146 | 11.524898884412591 |
| 600s | 1.7868471223107676 | 3.9515691107998387 |
| 1200s | 1.8903085164618962 | 2.6820862794976956 |

For ordinal k: `calibrated_predicted_entry = frozen_timeaware_predicted_entry + a_r + b_r * k`. No coefficient refitting, model selection, or route reassignment on confirmatory data.

**Primary endpoint:** 200s seed-level paired MAE improvement (original minus calibrated), mean across 10 seeds and 95% two-sided Student-t confidence interval. Scientific support requires the primary interval to exclude zero on the positive side. **Secondary:** same MAE analysis at 600s and 1200s, signed error, and eligibility/exception diagnostics. Independent seed is the uncertainty unit; road-entry rows are not independent replicates. Missing/ineligible seeds fail closed without replacement. Results do not establish cooperative routing benefit.

**Status:** frozen plan only; no confirmatory results are asserted.
