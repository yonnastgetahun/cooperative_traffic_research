# Experiment 004 — Consolidated scientific results and final decision

**Decision: NO-GO for the tested calibrated cooperative-routing policy (arm D).** This is not a rejection of the broader cooperative-traffic research hypothesis.

## Evidence and reproducibility

- [Original four-arm network-outcome simulation, run 41023721390](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41023721390): 120 scenario-arm executions, 10 fresh demand seeds (3301–3310), three departure windows (200, 600, 1200 seconds), four routing arms (A independent, B original time-aware cooperation, C stateful adapter without calibration, D same adapter with frozen Experiment 003 calibration).
- [Final archived fairness/exception audit, run 41098364737](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41098364737): all 120 original archives reanalyzed, no new simulations; output artifact [12996134768](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41098364737/artifacts/12996134768).
- Experiment 003 independently demonstrated improved *chosen-route prediction accuracy*; this experiment tests whether using that calibration improves **network-wide routing outcomes**.

## Primary outcome: completed-trip travel time

The prespecified primary contrast is seed-level mean completed-trip duration in C minus D at 200 seconds; **positive** would favor calibrated routing D. Two-sided 95% confidence intervals use 10 independent demand seeds.

| Departure window | C minus D mean (s) | 95% CI (s) | Interpretation |
|---|---:|---|---|
| 200s — primary/high congestion | -18.5282 | [-22.5866, -14.4698] | D significantly slower |
| 600s — moderate | -1.7801 | [-2.5668, -0.9934] | D slower |
| 1200s — lower | +0.1315 | [-0.1079, +0.3709] | Inconclusive |

Independent routing A was faster than D on the same completed-trip metric: A minus D was -21.6279s (200s), -3.6389s (600s), and -0.6365s (1200s). These are paired seed-level contrasts, not evidence of real-world traffic effects.

## Completion and censoring

All 1,000 vehicles completed their trips in each of the 120 scenario-arm executions: **100% completion, zero incomplete trips**. Thus the reported mean completed-trip duration is not selectively excluding unfinished trips in these scenarios. No imputation for censored vehicles was required.

## Matched-vehicle fairness

The following counts compare the same 10,000 vehicle identities per regime under C and D; helped means D reduced that vehicle's completed-trip duration.

| Regime | Helped by D | Harmed by D | Unchanged |
|---|---:|---:|---:|
| 200s | 3,998 (40.0%) | 5,673 (56.7%) | 329 (3.3%) |
| 600s | 4,294 (42.9%) | 4,701 (47.0%) | 1,005 (10.1%) |
| 1200s | 4,047 (40.5%) | 4,048 (40.5%) | 1,905 (19.1%) |

These are descriptive driver-level proportions, not independent-sample statistical tests.

## Tail travel times

Mean of seed-level 90th-percentile completed-trip durations (seconds):

| Regime | A independent | B original cooperative | C adapter only | D calibrated |
|---|---:|---:|---:|---:|
| 200s | 341.0 | 352.4 | 348.2 | 393.3 |
| 600s | 230.6 | 235.2 | 235.1 | 239.1 |
| 1200s | 215.0 | 217.1 | 217.0 | 216.0 |

At 200s, D's mean seed-level p90 exceeded C's by 45.1 seconds, indicating worse upper-tail travel times.

## Routing changes and exceptions

C versus D route assignments differed for 6,653/10,000 vehicles (200s), 5,707/10,000 (600s), and 4,395/10,000 (1200s). Thus the calibrated input materially changed route choices.

The structured collision evidence reported **zero collisions** for all arms and regimes. The audit detected `safety.emergencyBraking` and `safety.emergencyStops` statistics fields, but their numerical values have **not been consolidated or interpreted**. No claim is made that these event counts are zero, equivalent, or favorable for D.

## Explicit unresolved analyses

- **OD-cohort fairness:** Vehicle-level origin/destination cohort differences were preserved in the archived analysis artifact, but a consolidated OD-level harm distribution, cohort-size filtering and seed-level uncertainty assessment have **not** been completed. We do not claim the absence of localized harms.
- **Emergency events:** Emergency-braking and emergency-stop statistics were captured, but not numerically summarized or compared. Zero collision counts must not be conflated with zero emergency events.
- The fixed 10×10 synthetic network, SUMO dynamics, advance-demand routing and model-specific calibration limit generalization to real roads or live driver coordination.
- Experiment 004 did not test the original `cooperative.py` prototype as a separate B/C pair; its original-cooperation baseline was the time-binned `time_aware.py` algorithm.

## Final decision and next scientific question

**NO-GO for the specific calibrated cooperative-routing policy D.** The prespecified 200s primary travel-time contrast was unambiguously unfavorable, completion was complete, and matched-driver and upper-tail results reinforced the adverse high-congestion outcome. Unresolved OD and emergency-event summaries are retained as limitations; they cannot reverse the negative primary result but remain relevant to detailed distributional and operational interpretation.

**Not a rejection of the overarching hypothesis.** Experiment 003 demonstrated improved prediction accuracy on independent seeds, while Experiment 004 found that integrating those predictions into the tested stateful cooperative routing policy worsened network performance. The next research question is why improved forecasts produced worse route choices, including potential interactions among candidate search state, occupancy-feedback dynamics, forecast-clock alignment, and drivers' collective response. These are hypotheses, not established causes.

No new simulations are required to publish this report.
