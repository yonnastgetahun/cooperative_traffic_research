# Experiment 002 — Actual predictor trace: three-regime development diagnostics
**Run date:** October 26, 2026 (Pacific)  
**Status:** **Development smoke completed successfully. Predictor NOT yet validated.**  
**Execution:** [GitHub Actions run 40443562182](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40443562182), commit `7055f55fb5bc0dbac507d46ced5fd8af4323588d`  
**Protocol:** [Approved Predictor Validation Plan v0.2](EXPERIMENT_002_PREDICTOR_VALIDATION_PLAN.md)  
**Source code:** [original route generator](../experiments/experiment_002/time_aware.py), [non-policy-changing trace](../experiments/experiment_002/trace_actual_predictor.py), [prediction comparison](../experiments/experiment_002/compare_traced_predictor.py)

## Executive result

We can now measure the **original time-aware search's congestion and junction cost equations** along each chosen route, rather than only reconstructing free-flow arrival times afterward. Using SUMO-observed road-entry samples, the time-aware trace predicts arrival times more accurately than a free-flow-only reference **in each of three development scenarios**. However, its arrival-time estimates still systematically underpredict what happens, especially when 1,000 trips depart within 200 seconds.

This is **predictor diagnostics, not evidence of network improvement**: the smoke evaluates one development seed per regime, evaluates predictions on **chosen routes**, and does not run a matched independent-routing counterfactual. The previous Experiment 002 result (independent routing better on three inspected seeds/regimes) remains unchanged.

## Experimental setup and integrity checks

- Synthetic 10×10 SUMO grid, 200-meter grid spacing; **1,000 identical OD pairs** generated with seed **2001** per scenario.
- Departure windows: **200, 600, and 1,200 seconds**. Seed 2001 is a development/smoke seed, **not a held-out evaluation seed**. The schedules scale with the windows.
- **Three of three jobs succeeded; 1,000/1,000 trips finished per job.**
- Each scenario yielded **8,367 planned and 8,367 matched vehicle-edge traversals (100% matching)**. This eliminates earlier ambiguity about dropped unmatched rows for *these* scenarios; it does not guarantee all future tests will match.
- Trace-driven route files and audit CSVs were **byte-for-byte identical to the original uninstrumented `time_aware.py`** in every job. Routing policy and parameters were not changed.
- The original search heap's selected-route cost matched replayed chosen-path cost within the CSV numeric tolerance for **all 1,000 decisions per scenario**. This supports interpretation of the trace, but does **not** record every explored search alternative.
- Routes changed relative to baseline: **621 (high), 618 (moderate), 532 (low)**. **Zero guardrail rejections** in these particular three scenarios. Thus detour guardrails were present but were not stress-tested by rejected candidates in this smoke.
- SUMO version: **1.28.0**, as recorded by the jobs. Image reference `ghcr.io/eclipse-sumo/sumo:latest` remains **mutable**; an immutable digest is required before definitive held-out evaluation.
- Raw `network.net.xml` SHA-256 hashes differ between jobs because the files are generated independently; a post-run comparison of normalized network edges and connections produced the **same topology hash in all three jobs**, `e83507404883e295511ae08d63eb7f5974204e18e01541096a669f7df15eda97`. The OD-pair tuples likewise matched exactly (`97950b2ecbe8845ba30fbd04e400d34492815e5ca1976b3df6afa11efcb10795`). Full original file hashes remain in each artifact's `input-hashes.txt`.

## Forecast vs. observation

Observed road-entry times are approximated from **first external-edge FCD samples at 1-second resolution**. Mean absolute error and bias are measured in **seconds**; lower MAE is better. Both predictor and reference are evaluated on the same chosen time-aware routes.

| Congestion / window | Road-entry MAE: free-flow | Road-entry MAE: time-aware | Time-aware entry bias (observed − predicted) | Time-aware absolute p95 |
|---|---:|---:|---:|---:|
| High / 200 s | 58.89 | **53.52** | +53.47 | 186.85 |
| Moderate / 600 s | 22.55 | **18.67** | +18.57 | 59.33 |
| Low / 1,200 s | 16.80 | **13.32** | +13.19 | 40.20 |

The positive time-aware biases indicate **systematic underprediction**, not unbiased calibration. Correcting the entry errors for observed scheduled-versus-actual departure lag reduces MAE only modestly: **52.70**, **18.03**, and **12.83** seconds respectively.

As a secondary approximation, the observed interval from the first sample on an external edge to the next external edge (or trip arrival) includes **junction delay**, not just edge traversal. In that diagnostic, mean absolute model-cost error is **11.47**, **4.05**, and **2.89** seconds respectively, versus free-flow **12.61**, **4.91**, and **3.66**. Do **not** interpret those numbers as direct calibrated physical-edge traversal errors.

### Accumulating error along a route

At the **first edge**, mean entry error is approximately the observed departure lag: **0.84 / 0.66 / 0.51 s** for high / moderate / low. For **route edges 6 and later**, time-aware entry MAE grows to **100.79 / 33.89 / 23.60 s**. Forecast error therefore accumulates substantially down the trip, most seriously under congestion. This suggests examining queue and junction delay representation before adding optimization complexity.

For context only, observed mean trip duration *in this time-aware development arm* was **217.12 / 152.53 / 142.06 s**, with mean SUMO waiting **54.86 / 8.50 / 1.78 s**. These values must **not** be compared as a matched experiment with the earlier seed-1001–1003 baseline averages.

## Critical measurement limits

1. The original routing predictor's `occupancy[(edge, time_bin)]` is a **count of previously assigned routes at a single free-flow entry bin**, divided by a simple road capacity proxy. It is **not physical road occupancy**, queue length, or a multibin prediction of time spent on the road.
2. The trace replays the original cost equations **along chosen routes using pre-assignment counters**. It logs candidate/choice/rejection and the original search total cost. It does not provide a full record of every discarded Dijkstra search-state expansion.
3. Separate occupancy diagnostic files compare **assembled predicted route-interval vehicle-seconds** with one-second sampled FCD external-lane vehicle-seconds. Because the source model, internal lanes, time sampling, and junction treatment differ, these occupancy differences are **exploratory**, not a calibrated occupancy forecast accuracy score. Do not call the original count proxy a validated prediction.
4. One-second FCD samples approximate entry events. Edge-to-next-edge intervals incorporate internal junction crossings; observed pure edge exit is not directly measured here.
5. Unchosen candidate routes have **no observed counterfactual**. No routing objective, fairness, or individual-driver safety claims follow from this measurement exercise.
6. One development seed per regime cannot establish calibration stability, uncertainty or statistical significance. Held-out evaluation has **not begun**.

## Decision gates

| Gate | Status | Rationale |
|---|---|---|
| Workflow execution | **Pass** | All three regimes completed and artifact uploads succeeded |
| Non-policy-changing trace | **Pass for this smoke** | Exact route/audit equality against the original policy |
| Vehicle-edge join coverage | **Pass for this smoke** | 100% matched at 8,367/8,367 per regime |
| Measurement-definition/occupancy gate | **Open** | Assignment counts vs physical occupancy, junction effects and 1-second samples require clearer alignment |
| Predictor accuracy gate | **Not passed** | Some improvement over free-flow, but significant systematic late arrivals |
| Objective alignment and fairness | **Not tested in this smoke** | Requires separately paired policy interventions and explicit individual outcomes |
| Held-out validation | **Not started** | Seed 2001 already informed development |

## Next approved research actions

1. **Fix measurement definitions, not routing weights.** Record the original assignment-count query alongside a separately defined actual time-binned occupied vehicle-seconds / observed congestion reference; do not relabel the assignment count as physical occupancy. Evaluate junction/intersection effects and sampling resolution explicitly.
2. Separate prediction error from accumulated queue delay and observed departure lag. Break down systematic bias by network link, trip position, and congestion regime; preserve the free-flow comparison on identical chosen routes.
3. **Prespecify additional disjoint seeds before running them.** Suggested development/calibration seeds: **2101, 2102, 2103**, followed (only after model/measurement freeze) by evaluation seeds **3101–3110** per regime. These are planned assignments, **not completed experiments**, and do not guarantee statistical power.
4. Pin SUMO by **immutable container digest** before held-out evaluation. Continue publishing version, code commit, input hashes, and complete seed-level results.
5. Only after measurement quality is understood and predictor settings are frozen should we test objective alignment and whether any new routing policy improves **total realized travel time and driver fairness**, using paired independent-routing controls.

## Immutable evidence and reproducibility

[Run and downloadable artifacts](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40443562182#artifacts) (30-day GitHub Actions retention):

- `exp002-actual-predictor-trace-window-200-seed2001` — artifact ID `12707277377`
- `exp002-actual-predictor-trace-window-600-seed2001` — artifact ID `12706942709`
- `exp002-actual-predictor-trace-window-1200-seed2001` — artifact ID `12707082649`

Each bundle includes `actual-predictor-report.json`, per-vehicle `chosen-decision-trace.csv`, `candidate-decision-trace.csv`, `route-decisions.csv`, `vehicle-edge-errors.csv`, `occupancy-diagnostic.csv`, input hashes, forecast hashes, the original and traced routes/audits, SUMO version, FCD, tripinfo and input manifest.

**Interpretation:** This smoke establishes a functioning, non-policy-changing measurement path. It exposes a meaningful but incomplete predictive improvement over free flow alongside large, congestion-dependent systematic bias. It does not resolve whether cooperative traffic coordination is beneficial.
