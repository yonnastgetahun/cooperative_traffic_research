# Experiment 002 — M3 held-out scientific interpretation

**Evidence:** [GitHub Actions run 40953111402](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40953111402), frozen source `be2e8d27c78c8b6de4891115d6d951edc877ac6e`, evaluation merge commit `946ee1d0110f9907d051881aa0193593cf67e88d`.

## Verified evaluation scope

All 30 scenario jobs succeeded: ten prespecified held-out demand seeds 3101–3110, each in 200s, 600s, and 1200s departure windows. All 30 artifacts were retrieved by the successful aggregation job. The aggregate validator accepted all 30 scenarios under its R3 eligibility and hash checks; no missing/ineligible scenarios were reported. This does not independently prove all raw event fields beyond the validated evidence.

## Seed-level paired MAE results

| Window | Time-aware MAE seed mean (s) | Free-flow MAE seed mean (s) | Paired benefit FF minus TA (s) | 95% Student-t interval (s) | Mean signed TA error (s) | Relative MAE improvement |
|---|---:|---:|---:|---|---:|---:|
| 200 (primary) | 52.676698 | 58.000631 | 5.323933 | [5.242847, 5.405019] | 52.616486 | 9.18% |
| 600 | 19.038248 | 22.904172 | 3.865924 | [3.794879, 3.936969] | 18.939766 | 16.88% |
| 1200 | 13.398357 | 16.842725 | 3.444368 | [3.383168, 3.505568] | 13.249838 | 20.45% |

All confidence intervals are computed over **ten independent seed-level paired differences** in each regime, not over individual vehicles or road visits. All three intervals are strictly positive under the frozen fixed-testbed assumptions. The primary prespecified regime is 200 seconds.

## Interpretation

1. The time-aware predictor reduces chosen-route road-entry MAE relative to same-route free-flow predictions in every tested regime.
2. The primary high-congestion 200s regime has the largest absolute benefit (5.32 seconds), but the smallest relative benefit (9.18%) because its baseline error is much larger.
3. Positive mean signed error is close to the corresponding MAE in all three regimes. This is consistent with predominantly late observed entries and substantial systematic underprediction of arrival time; inspect signed-error distributions before attributing the cause to any specific model component.
4. The narrow seed-level confidence intervals quantify variation across the ten demand seeds within the fixed network and simulation assumptions. They do not quantify real-world uncertainty, network variability, or causal traffic benefit.
5. The aggregator's inherited status label `PURE_SYNTHETIC_REVIEW_NOT_HELDOUT_EVALUATION` is inconsistent with this authorized held-out run. Correct reporting metadata in a separate publication-only change, preserving the original run and frozen scientific calculations.

## Research-pathway decision

**Priority 1 — Timing bias decomposition and calibration.** Use the archived paired road-entry rows to separate first-edge departure lag, route-ordinal accumulation, and congestion-regime effects. Prespecify an out-of-sample calibration experiment using fresh seeds; do not refit and claim validation on the held-out M3 seeds.

**Priority 2 — Predictor structure.** Investigate whether omitted temporal congestion dynamics or the frozen route-assignment counter explain residual underprediction. Treat mechanisms as hypotheses, not findings.

**Priority 3 — Routing efficacy.** Only after a calibrated predictor has been independently validated, design a new controlled routing-policy experiment with network-wide travel time, throughput, fairness and exceptions. The M3 chosen-route timing comparison cannot establish routing efficacy.

## Publication boundaries

Do not claim physical road-occupancy prediction, causal intersection delay, improved network-wide traffic, or real-world safety from this evaluation. The study used a fixed synthetic network and ten demand seeds. The existing M3 held-out results should remain immutable; further model development is a new prespecified study.
