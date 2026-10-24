# Experiment 002 — Predictor Validation Plan v0.1

**Status: Proposed for review. Not approved for implementation or execution.**

## Decision and motivation

The 1,000-vehicle, 10×10-grid, 200-second-window, seed-1001 smoke test completed for independent, original cooperative, and time-aware cooperative routing. Mean trip durations were approximately 197.67, 199.54, and 209.85 seconds respectively. The time-aware candidate changed 587 routes but was 12.18 seconds slower on average than independent routing. These are results from one synthetic test scenario, not evidence about real-world navigation or safety.

**Research question:** Are the time-aware predictor's estimates of edge occupancy and travel cost accurate enough to guide route decisions, and does the route-selection objective align with realized network travel time and fairness?

Do not change algorithm parameters based on the held-out evaluation results before establishing a validation protocol.

## Phase 0 — Instrumentation and definitions

- Preserve the existing workflows and algorithms. Create a separate, manually triggered diagnostic workflow; record Git SHA, SUMO version/image digest, seed, network/trips hashes, route strategy and parameters.
- Define a prediction record per planned vehicle-edge traversal: vehicle ID, edge ID, predicted entry time bin, predicted exit time, occupancy estimate, edge cost (free-flow, occupancy surcharge, junction proxy), candidate route and decision/rejection reason.
- Define observations from SUMO: actual edge entry/exit times and realized traversal time, time-binned occupancy/vehicle-seconds, waiting time, edge speeds, departures and arrivals. Use appropriate SUMO outputs (e.g., FCD/edgeData and tripinfo), verifying units and output coverage; distinguish samples from unique vehicles.
- **Do not equate assignment counts with realized occupancy**. Current occupancy updates one time bin per traversed edge and do not represent all bins occupied along an edge. Explicitly document this limitation and repair instrumentation before assessing forecast accuracy.
- Audit the current route generator's adjacency/legal-connection handling, baseline route definitions and free-flow detour checks; verify the same vehicle IDs, OD pairs, departure times, and network in every arm.

## Phase 1 — Predictor accuracy (offline replay; no future leakage)

1. Freeze a demand scenario and independently produce the predictor's forecasts *before* SUMO runs. Save predictions and immutable input hashes.
2. Run SUMO using the frozen route assignments. Capture observed edge occupancy and travel times in aligned time bins (initially 30 seconds); validate whether that bin size is meaningful relative to edge travel time.
3. Join predictions to observations by vehicle/edge/time where possible. Account for missing/never-traversed edges and out-of-bin arrival rather than silently dropping them.
4. Report edge-entry time error, traversal-time error (MAE, RMSE, bias, p90/p95), occupancy calibration by time bin, congestion-event precision/recall, and error by intersection/edge demand level.
5. Compare against simple reference predictors: free-flow-only arrival times and the existing cumulative edge-count proxy. A complex predictor should not be considered better merely because it has more inputs.
6. Analyze whether errors accumulate along routes, whether bottleneck links are systematically underestimated, and whether higher predicted load correlates with realized delay. Avoid causal conclusions from correlations alone.

## Phase 2 — Objective alignment

- Compare predicted candidate-route cost rankings with realized route outcomes **only for routes actually driven**; counterfactual outcomes for unchosen routes are not directly observable.
- To estimate counterfactual impacts, use controlled paired SUMO simulations with identical demand and one routing-policy change at a time. Treat system-wide interference between vehicles as part of the causal mechanism.
- Test whether optimizing predicted individual cost correlates with minimizing **total realized travel time across all 1,000 trips**, not just the travel time of rerouted vehicles.
- Report mean, median, p95, worst-case realized delay, helped/harmed fractions, total waiting, trip completion and detour distance. Report predicted guardrail compliance separately from realized harm.
- Check whether predicted time savings were offset by extra distance, junction delay, queue spillback or redistribution of traffic to bottlenecks.

## Phase 3 — Calibration and holdout design

- Use three congestion regimes (departure windows 200, 600 and 1,200 seconds), same 10×10 network and 1,000 trips per scenario.
- Prespecify disjoint calibration/training seeds and held-out evaluation seeds; do not reuse seed 1001 as independent evidence after it has informed design decisions.
- Start with at least three calibration seeds per regime for feasibility and diagnostics, then at least ten **held-out paired seeds per regime** for a stronger assessment. Report seed-level results and uncertainty intervals; this is a design target, not a guarantee of statistical power.
- Freeze all predictor parameters, objective weights and detour thresholds before held-out evaluation. Document any additional tuning as exploratory and rerun on a fresh holdout.
- Pin the SUMO container by immutable digest to avoid drift.

## Phase 4 — Decision gates

**Instrumentation gate:** predictions and observations can be joined with verified units, missingness accounting, legal routes, and complete input manifests.

**Accuracy gate:** report calibrated error against free-flow and edge-count references across congestion regimes; investigate systematic underprediction of congestion. No arbitrary accuracy threshold will be declared successful after seeing results.

**Objective gate:** evaluate whether improvements in forecast accuracy correspond to improvements in total realized journey time and fairness. Better prediction alone does not prove better routing.

**Safety/fairness gate:** no illegal routing, speeding or unsafe maneuvers in the simulation; audit predicted detour caps and realized individual harms separately. Synthetic simulation cannot establish real-world safety.

**Go/no-go:** if forecasts remain poorly calibrated, improve the traffic model before routing optimization. If forecasts improve but network outcomes do not, revisit the assignment objective, equilibrium/interaction assumptions, and matched independent controls rather than tuning blindly.

## Implementation deliverables — ONLY after explicit approval

1. Instrumented predictor emitting vehicle-edge forecast and decision records (CSV/JSON).
2. Separate manual GitHub Actions diagnostic workflow, without modifying Experiment 001 or existing Experiment 002 runs.
3. SUMO observed edge/traversal measurement capture, with integrity and coverage checks.
4. Reproducible prediction-vs-observation report, error breakdown, calibration plots and paired outcomes.
5. Validation memo documenting limitations and whether to revise the predictor, the optimization objective, or both.

## Scope boundaries

- **No new full-scale routing sweep yet.** First validate predictions and metrics on a limited paired smoke scenario.
- Keep voluntary coordinated departures as the separate proposed Experiment 003; count predeparture waiting in door-to-door outcomes when eventually evaluated.
- This plan is for synthetic research, not deployment or traffic safety certification.

**Approval requested:** instrument and validate the predictor according to this plan. Publishing this document does not authorize implementation.
