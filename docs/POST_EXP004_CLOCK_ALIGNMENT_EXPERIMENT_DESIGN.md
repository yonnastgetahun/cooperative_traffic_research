# Experiment 005 — Prospective clock-alignment causal test (frozen before new-seed execution)

**Status:** Authorized for design, implementation, and execution on October 30, 2026. This document is prospective; no outcomes from Experiment 005 existed when written. Experiment 004 remains frozen and its policy-D NO-GO unchanged.

## Motivation and competing explanations

Experiment 004 calibrated D increased mean completed-trip duration by **18.5282 seconds** relative to adapter-only C at 200s (95% paired seed-level CI for D−C +14.4698 to +22.5866s). The [complete archived decomposition](POST_EXP004_FULL_ARCHIVE_DECOMPOSITION_RESULTS.md) showed higher assigned-edge concentration, +23.799s among changed-route drivers, +7.949s among unchanged-route drivers under high congestion, and approximately 98% of changed routes having the same nominal free-flow distance and time. This is consistent with congestion spillovers, not proof of a particular mechanism.

The code has a structural inconsistency: policy D chooses candidate successors using calibrated lookup time bins, yet after assignment updates the occupancy proxy using uncalibrated free-flow timing. **Hypothesis:** aligning the post-assignment occupancy-update bins with calibrated candidate forecast timing improves network-wide trip duration under high congestion relative to policy D, possibly by preventing assignment concentration. This tests one specific mechanism; candidate-route accuracy and true system-optimality remain unresolved.

## Treatment and control (frozen)

- **D-replication, control:** the original Experiment 004 calibrated stateful-search algorithm, the exact coefficients per regime and the original post-assignment **free-flow** occupancy-bin updates, with no policy change.
- **E, intervention:** identical D search, coefficients, demand, route guardrails, vehicle ordering, network and SUMO settings; **only** the post-assignment occupancy-bin updates are changed to the calibrated predicted-entry clock on the **chosen route**.
- Same frozen Experiment 003 coefficients: 200s `a=4.053135104279146`, `b=11.524898884412591`; 600s `a=1.7868471223107676`, `b=3.9515691107998387`; 1200s `a=1.8903085164618962`, `b=2.6820862794976956`.
- Original SUMO container pinned to `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`; frozen original demand generator at commit `be2e8d27c78c8b6de4891115d6d951edc877ac6e`.
- All travel-time effects reported **D − E**, so **positive favors aligned E**.

### Exact assignment-update rule

When evaluating a new vehicle, routes are searched prospectively with the **unchanged** original `prospective_search_adapter_v01.search`. The same free-flow time and distance guardrails select the **chosen route** (the candidate if eligible, otherwise the independent free-flow fallback).

Both arms use occupancy counters containing only **previously assigned vehicles**. For E, **before modifying occupancy**, replay the chosen edge sequence against this pre-assignment occupancy snapshot:

1. On ordinal `k=0` (origin edge), the calibrated predicted road-entry time is `depart+a_r`. Assign origin to bin `floor((depart+a_r)/30)`; initialize the accumulated search cost to the origin edge's free-flow travel time.
2. For every successor edge at ordinal `k>=1`, compute `predicted_entry = depart + accumulated_search_cost + a_r + b_r*k` and its `floor(predicted_entry/30)` bin. Then increase accumulated search cost by that successor's `freeflow_edge_time * (1+pressure * prior_assigned_count_at_that_edge_bin / capacity_proxy) + turn_proxy`, using the same capacity proxy and branching-junction turn proxy as the original stateful search.
3. **Only after all bins for the chosen route have been computed** increment occupancy `[(edge,bin)]` by one for each chosen edge. This avoids within-vehicle self-feedback. When the candidate is rejected by the unchanged detour guardrails, replay and update the **fallback chosen route**, not the rejected candidate.
4. For control D, update the chosen route at `floor(clock/30)` with `clock=depart` advanced by each successive edge's free-flow time, exactly as `time_aware.py` currently does.
5. Do not use future SUMO observations, physical queues, or actual trip times for route decisions.

The replay rule is a **specific intervention definition**, not a claim that the algorithm's path-dependent calibration is uniquely correct or equivalent to an independently validated counterfactual predictor. A matched development-seed preflight must establish that D-replication produces byte-identical routes and routing audit relative to the unchanged Experiment 004 D code for all three windows. No confirmatory fresh-seed run should begin if this fails.

## Prespecified cohort and endpoints

- **Fresh paired seeds:** `3401, 3402, 3403, 3404, 3405, 3406, 3407, 3408, 3409, 3410`. Disjoint from 2101, 2201–2210, 3101–3110, 3201–3210, 3301–3310. No post-outcome seed replacement.
- **Windows:** 200 seconds **primary**; 600 and 1200 seconds secondary. Each paired arm runs 1,000 identical seeded trips on the fixed synthetic 10×10 SUMO grid. **30 matched seed-window pairs = 60 arm executions**.
- **Primary estimand:** arithmetic mean across ten independent-seed paired differences `mean_completed_trip_duration_D - mean_completed_trip_duration_E` at 200 seconds; two-sided 95% Student-t interval on those ten differences (df=9), with the complete-trip fractions reported.
- **Decision (frozen gates):** GO for the **clock-alignment intervention relative to D** only if (i) the 200s seed-level 95% CI for D−E is entirely positive, (ii) all 1,000 trips complete in every D and E scenario (or equivalently E does not have worse completion; incomplete outcomes demand censoring analysis before any GO), (iii) high-congestion mean of seed-level p90 E−D is no greater than +5 seconds, and (iv) no majority (>50%) of matched high-congestion vehicles has a longer trip in E. If the primary interval lies entirely below zero, classify NO-GO. If it is entirely positive but either descriptive guardrail fails, label 'primary improved but secondary guardrail failed', not GO. Otherwise INCONCLUSIVE. These secondary thresholds are policy-specific cautionary criteria, not separately powered hypothesis tests. A GO is NOT proof of advantage over independent routing A. No threshold or penalty may be tuned based on outcomes.
- **Secondary descriptive outcomes:** mean and p90 completed-trip time for all three regimes, completion/duplicates, matched driver helped/harmed proportions, unchanged-route-driver spillovers, waiting time and time loss, changed-route count, assigned-edge-load Gini and top-decile share, collision/exception structured fields when present. Missing statistics are unavailable, not zero. For incomplete-trip differences, report censoring prominently and do not claim success from selectively completed trips.
- **Reproducibility:** each arm preserves original network, demand, routes, route audit, manifests, tripinfo, SUMO statistics and collision evidence and failed-attempt logs; aggregate with independent demand seed as uncertainty unit.

## Execution boundary

This is a single discriminating two-arm causal test, not a vehicle-volume or network-scale experiment. The confirmed original D control is not retuned and existing 001–004 findings are unchanged. A successful result identifies the incremental causal effect of the prespecified aligned-update intervention under controlled synthetic demand, not that clock misalignment was the only original failure mechanism.

**Historical proposals preserved:** departure-time coordination, participation rates, grid size and road-network complexity remain separate future scientific dimensions.
