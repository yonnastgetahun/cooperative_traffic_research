# Experiment 004 — Full archived C/D route-change and spillover decomposition

**Analysis date:** October 30, 2026  
**Status:** Completed exploratory reanalysis of the frozen Experiment 004 evidence. **No new SUMO simulations, retuning, or policy changes.**  
**Evidence source:** [Original 120-arm run 41023721390](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41023721390), its 60 original C/D scenario ZIP artifacts, and the [published archived audit](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41098364737).  
**Original primary finding remains frozen:** D minus C mean duration +18.5282 seconds at 200s, 95% paired seed-level CI [+14.4698,+22.5866] seconds; calibrated D policy NO-GO.

## What was actually analyzed

Every C and D scenario ZIP was retrieved for **10 fresh seeds 3301–3310 × three departure windows 200/600/1200 seconds × two arms = 60 ZIPs**, representing 30 matched C/D scenarios and **30,000 paired vehicle identities**. All had 1,000 completed tripinfos and route assignments. The C/D `trips.xml` demand bytes matched exactly within all 30 seed-window pairs, and the per-vehicle route change counts and arm mean trip durations reproduced the previously published 120-arm audit.

Read-only joins used vehicle ID within seed-window pairs. 'Changed' means the complete edge sequence differs in C and D; 'unchanged' means exact edge-sequence identity. Outcomes are **D − C**, so positive values mean calibrated D is slower. Vehicle-trip durations, waiting time, time loss, and departure delay came from original `tripinfo.xml`; assignment sequences came from `routing/routes.rou.xml`. Nominal route distance and free-flow time were reconstructed from the original `network.net.xml` edge lane length and speed. Per-edge route-assignment counts are **assigned-demand proxies, not measured physical occupancy**. Their Gini and top-decile share were computed across all directed non-internal network edges.

For each regime and subgroup, means and Student-t 95% confidence intervals were computed from **ten seed-level subgroup means**, not from treating vehicle records as 10,000 independent experimental replications. These subgroup comparisons are exploratory; the original C/D primary endpoint is unchanged.

## New results — matched outcomes by route-change status

| Departure regime | Group | Matched vehicles / 10 seeds | Mean D − C duration | 95% seed-level CI | Seeds with slower D |
|---|---|---:|---:|---:|---:|
| High, 200s | Changed route | 6,653 | **+23.799s** | [+19.512,+28.086]s | 10/10 |
| High, 200s | Unchanged route | 3,347 | **+7.949s** | [+4.251,+11.646]s | 9/10 |
| Moderate, 600s | Changed route | 5,707 | **+2.490s** | [+1.333,+3.647]s | 10/10 |
| Moderate, 600s | Unchanged route | 4,293 | **+0.800s** | [+0.278,+1.323]s | 9/10 |
| Lower, 1200s | Changed route | 4,395 | **−0.522s** | [−0.859,−0.186]s | 1/10 |
| Lower, 1200s | Unchanged route | 5,605 | **+0.166s** | [−0.063,+0.396]s | 7/10 |

**Interpretation:** In high congestion, harm under D is present among both changed-route and unchanged-route vehicles. The unchanged-route difference is consistent with **network-mediated spillovers** from altered traffic assignment, because a vehicle retained its route and demand context while the rest of the network's assignments changed. This does **not** identify a particular edge bottleneck or prove that the documented clock mismatch caused the harm. Differences for unchanged drivers may include downstream interaction effects and simulator path dynamics.

For high congestion, changed-route vehicles averaged **+17.076s waiting time**, and unchanged-route vehicles **+5.963s waiting time** (D − C). Regime-wide D − C mean waiting time was +13.3916s. This supports a realized queuing/delay interpretation, without isolating the causal edge or junction.

## Route geometry and assignment concentration

| Regime | Changed routes with same nominal free-flow distance and duration | Mean changed-route nominal free-flow difference (D − C) | Assigned-edge load Gini increase (D − C) | Top 10% edge assignment share increase |
|---|---:|---:|---:|---:|
| High 200s | **97.98%** | −0.0017s | **+0.0413** | **+2.23 percentage points** |
| Moderate 600s | **98.30%** | +0.0017s | **+0.0117** | **+0.73 percentage points** |
| Lower 1200s | **98.20%** | +0.0010s | **+0.0045** | **+0.42 percentage points** |

Nominal free-flow equality uses reconstructed per-edge lane length/speed with a 1e-6 absolute tolerance. Equal nominal duration/distance does **not** mean the same physical edge sequence, turn exposure, signal constraints, or realized travel time. The average free-flow changes are near zero in practical magnitude; longer nominal detours do **not** explain the high-congestion +18.53s deterioration.

The 200s assigned-edge-load Gini increase was **positive in all 10 seeds**, 95% seed-level CI [+0.0380,+0.0445]; its top-decile traffic-assignment-share increase had CI [+0.0206,+0.0240]. At 600s, the Gini increase was also positive in all ten seeds; at 1200s, the mean Gini shift was smaller, including two slightly negative seeds. These are assignment-concentration measures only, not measured queue distributions. A more concentrated assignment distribution is consistent with a congestion displacement pathway but alone does **not** identify congestion causality.

## Seed-level descriptive evidence

Each row gives: changed route count / 1,000, changed-group mean D−C duration, unchanged-group mean D−C duration, all-driver mean D−C duration, and D−C assignment-load Gini.

| Window | Seed | Changed | Changed mean (s) | Unchanged mean (s) | All mean (s) | Gini Δ |
|---|---:|---:|---:|---:|---:|---:|
| 200 | 3301 | 683 | +28.378 | +6.631 | +21.484 | +0.0459 |
| 200 | 3302 | 659 | +29.962 | +13.217 | +24.252 | +0.0395 |
| 200 | 3303 | 670 | +24.419 | +7.612 | +18.873 | +0.0417 |
| 200 | 3304 | 642 | +14.192 | −1.844 | +8.451 | +0.0351 |
| 200 | 3305 | 672 | +23.003 | +10.787 | +18.996 | +0.0418 |
| 200 | 3306 | 670 | +25.945 | +5.876 | +19.322 | +0.0445 |
| 200 | 3307 | 670 | +28.351 | +11.582 | +22.817 | +0.0470 |
| 200 | 3308 | 701 | +29.974 | +14.268 | +25.278 | +0.0451 |
| 200 | 3309 | 633 | +19.325 | +10.106 | +15.942 | +0.0346 |
| 200 | 3310 | 653 | +14.446 | +1.251 | +9.867 | +0.0373 |
| 600 | 3301 | 559 | +5.009 | +1.073 | +3.273 | +0.0163 |
| 600 | 3302 | 551 | +1.657 | +1.196 | +1.450 | +0.0098 |
| 600 | 3303 | 578 | +1.946 | +1.109 | +1.593 | +0.0117 |
| 600 | 3304 | 578 | +0.377 | −1.147 | −0.266 | +0.0072 |
| 600 | 3305 | 563 | +1.217 | +0.760 | +1.017 | +0.0179 |
| 600 | 3306 | 570 | +1.696 | +1.295 | +1.524 | +0.0094 |
| 600 | 3307 | 545 | +3.004 | +1.407 | +2.277 | +0.0104 |
| 600 | 3308 | 620 | +5.487 | +0.571 | +3.619 | +0.0162 |
| 600 | 3309 | 560 | +2.495 | +0.809 | +1.753 | +0.0088 |
| 600 | 3310 | 583 | +2.012 | +0.930 | +1.561 | +0.0092 |
| 1200 | 3301 | 463 | −0.268 | +0.439 | +0.112 | +0.0046 |
| 1200 | 3302 | 444 | +0.426 | +0.246 | +0.326 | +0.0031 |
| 1200 | 3303 | 428 | −0.453 | +0.306 | −0.019 | +0.0060 |
| 1200 | 3304 | 431 | −0.369 | +0.364 | +0.048 | −0.0001 |
| 1200 | 3305 | 421 | −1.264 | −0.161 | −0.625 | −0.0010 |
| 1200 | 3306 | 457 | −0.648 | +0.048 | −0.270 | +0.0084 |
| 1200 | 3307 | 407 | −0.253 | +0.713 | +0.320 | +0.0053 |
| 1200 | 3308 | 488 | −0.576 | −0.289 | −0.429 | +0.0089 |
| 1200 | 3309 | 425 | −1.082 | +0.224 | −0.331 | +0.0060 |
| 1200 | 3310 | 431 | −0.738 | −0.227 | −0.447 | +0.0042 |

Per-seed values are rounded for display; all primary and subgroup interval estimates above were calculated from unrounded original tripinfo data. Do not infer causal contribution from counting harmed drivers by group.

## Hypothesis assessment, updated

| Candidate mechanism | Status after full archive reanalysis |
|---|---|
| **Longer nominal detours** | **Strongly disfavored as main explanation**: approximately 98% of switched routes have unchanged nominal free-flow geometry, and mean free-flow difference is negligible. |
| **Congestion redistribution / spillover** | **Supported observationally**: routes differ, assigned-load Gini increases, and identical-route drivers are slower under high congestion. The specific physical bottlenecks and causal pathways remain unobserved. |
| **Forecast-clock / occupancy-update mismatch** | **Structurally established in source**: calibrated search bins versus free-flow assignment bins; **causal magnitude unknown**. |
| **Candidate-route misranking** | **Unresolved**: Experiment 003 validated chosen-route timing, not rejected candidates or route-rank accuracy. |
| **Stateful search behavior** | **Unresolved quantitatively**: C and D use the same adapter but calibrated forecast timing may change path exploration and labels; rejected label traces were not archived. |
| **Objective/fairness misalignment** | **Plausible and not isolated**: local proxy scoring does not explicitly minimize realized social cost; high-congestion mean, tail and matched-driver harms remain adverse. |

## Research decision and next concrete scientific test

**Finding:** The archived data strengthen the traffic-assignment concentration and network-spillover explanation, and strongly disfavor nominal route-lengthening as the dominant cause. They do **not** isolate whether the structural lookup/update clock mismatch generated those bad assignments or whether another candidate-ranking/optimization limitation was responsible. Preserve Experiment 004 calibrated policy-D **NO-GO**.

**Next focused question:** Does aligning the post-assignment occupancy-update clock with the calibrated candidate-search clock reduce route-assignment concentration and collective delay, compared with the original D policy under otherwise identical conditions?

A *future* controlled D-versus-D_clock_aligned comparison would alter **only** the assignment-update timing rule, holding the predictor, ordinal-aware search state, OD demand, detour guardrails, SUMO configuration, and independent seed pairing fixed. Before execution, prespecify the exact update rule, fresh cohort, and primary network outcome; measure mean time, completion, tails, unchanged-driver spillovers and assignment concentration. This could identify the causal effect **of the changed update clock**, but would not automatically prove all other candidate-ranking issues solved. This is a narrow proposed discriminating test, **not an authorized or executed new simulation**.

Keep future vehicle-volume sensitivity, larger grids and nonuniform topology as separate approved research directions *after* the current mechanism investigation; do not conflate their effects.

## Reproducibility and limits

- Original source run: [41023721390](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41023721390). Original archives were all available and marked unexpired on this examination; GitHub artifact metadata currently lists expiration on November 29, 2026.
- Existing matched-outcome audit: [41098364737](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41098364737).
- Source definitions: [`time_aware.py`](../experiments/experiment_002/time_aware.py), [`prospective_search_adapter_v01.py`](../experiments/experiment_004/prospective_search_adapter_v01.py), [frozen design](EXPERIMENT_004_FOUR_ARM_FROZEN_DESIGN_V01.md).
- The read-only decomposition matched all published C/D per-seed travel-time means and route-change totals; no original archives or scientific methods were modified.
- A complete 60-ZIP SHA-256 input manifest, 90 subgroup-seed rows, 30,000 paired-vehicle derived records and the read-only analysis script were generated in the analysis environment; this document preserves the full regime- and seed-level scientific findings on GitHub. The original temporary source ZIPs were not copied into the repository.
- This was **exploratory analysis performed after seeing the Experiment 004 outcomes**. Subgroup 95% confidence intervals are descriptive uncertainty summaries, not prospectively multiplicity-controlled confirmatory tests.
- No saved physical edge-time queue traces or rejected candidate-search traces were identified in the original raw archives. Load concentration is calculated from static route assignments, not from observed realized traffic flow.
