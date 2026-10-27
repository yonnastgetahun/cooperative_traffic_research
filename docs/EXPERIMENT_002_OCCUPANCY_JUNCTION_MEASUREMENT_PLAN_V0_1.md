# Experiment 002 — Physical Occupancy & Junction Delay Measurement Plan v0.1

**Date:** October 26, 2026 (Pacific)  
**Status:** **M0–M2 executed successfully as development instrumentation (October 26, 2026); G3 native/FCD interpretation remains open; M3 held-out freeze/evaluation NOT approved or started.**  
**Parent protocol:** [Approved Predictor Validation Plan v0.2](EXPERIMENT_002_PREDICTOR_VALIDATION_PLAN.md)  
**Evidence:** [Actual predictor trace, October 26](EXPERIMENT_002_ACTUAL_PREDICTOR_TRACE_2026-10-26.md) · [successful three-regime development run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40443562182)  
**Execution and measured results:** [M0/M1 12 passing contract tests + 3 successful SUMO cases](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40445882827) · [M2 nine-scenario + aggregate success](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958) · [Durable M2 findings and gates](EXPERIMENT_002_OCCUPANCY_M2_DEVELOPMENT_RESULTS_2026-10-26.md). All new runs used development seeds only and maintained original route-policy invariance.\n\n**Scope:** Improve *measurement*, not routing policy, routing penalties, or optimization objectives. This is an additive design for the next milestone; it does not supersede the parent protocol.

## 1. Decision to resolve

In the 1,000-vehicle, 10×10 SUMO testbed, the original time-aware route-cost equations predict observed arrival times more accurately than free-flow timing on the same chosen routes, but they **systematically underpredict delay**. In the 200/600/1,200-second development scenarios (seed 2001), mean absolute external-road entry error was **53.52 / 18.67 / 13.32 seconds** for time-aware estimates, versus **58.89 / 22.55 / 16.80 seconds** for free flow. That is **development diagnostic evidence**, not held-out validation or a cooperative-routing benefit.

The original algorithm increments `occupancy[(edge, time_bin)]` once for each preassigned route at the **free-flow entry-time bin**, then divides the count by an approximate storage capacity. It does **not** estimate true vehicles present on an edge throughout the 30-second bin. The prior comparator uses external-edge first-seen FCD samples and model-replayed path intervals; internal junction states, stopped vehicles, partial-bin occupancy and the separation of road versus intersection delay remain insufficiently resolved.

**Primary research question:** Which measurable components of observed congestion explain the model's systematic late-arrival errors: misrepresented edge accumulation, waiting on external approaches, time spent on internal junction lanes, departure lag, or unobserved transition intervals?

**Secondary question:** Is the original *assignment-count proxy* informative about later observed load and delay, even though it is neither a vehicle-count forecast nor a physical occupancy estimate?

**Competing diagnostic hypotheses (not accepted conclusions):**
- H1. The one-bin assignment-count proxy poorly characterizes multi-bin time spent by moving or queued vehicles, especially in the high-load regime.
- H2. External-edge waiting/queues account for substantial delay beyond free-flow travel, while actual time spent on internal junction links may or may not contribute meaningfully.
- H3. Even modest per-segment cost bias accumulates into large predicted-arrival bias on long routes.
- H4. Some apparent timing error comes from FCD sample boundaries or departures later than scheduled rather than the routing predictor.

Do not infer causal proportions from observational correlations alone.

## 2. Measurement contract — distinct concepts, names and units

**Time reference:** SUMO simulation seconds, not wall-clock time. Observation bins are half-open `[k·30,(k+1)·30)`, indexed `k = floor(t/30)`. Report partial first/last bins with their actual covered duration. Use **30 seconds** as the prespecified primary aggregation; report **10 and 60 seconds** as sensitivity analyses, not post-hoc ways to select a flattering result. FCD acquisition uses a **1-second sample period**; record simulation step length and verify output cadence, rather than assuming one second if the configuration differs.

| Quantity | Unit | Definition and use | What it is NOT |
|---|---|---|---|
| `decision_prior_assigned_count` | route assignments | Counter read by the original route search for (edge, queried time bin), immediately before assigning the current vehicle; retain edge, time bin and source-vehicle decision order | Simultaneous vehicles, a physical queue, or observed occupancy |
| `decision_capacity_proxy` | model-specific units | Current `max(1, edge_length_m × lane_count / 7.5 m)` denominator, recorded unchanged | Calibrated capacity or measured road storage |
| `decision_normalized_proxy` | dimensionless | Above assignment count divided by capacity proxy; input to the existing congestion surcharge | The observed fraction of a road occupied |
| `observed_external_vehicle_seconds` | vehicle-seconds/bin | Sum of vehicle samples on the named *external* edge multiplied by verified sample spacing, after coverage checks; count each vehicle once per sample | An exact continuous-time integral or % lane occupancy |
| `observed_external_mean_vehicles` | vehicles | Sampled external-edge vehicle-seconds divided by covered bin duration | Vehicle entries, throughput, or occupancy percentage |
| `observed_internal_vehicle_seconds` | vehicle-seconds/bin | Analogous quantity for SUMO *internal* junction edges, stored separately by internal lane/link | Vehicle-seconds on the preceding external edge |
| `native_edge_sampled_seconds` | vehicle-seconds/bin | SUMO `edgeData.sampledSeconds` independently measured by SUMO for external edges | Identical sampling semantics to reconstructed FCD counts |
| `native_edge_occupancy_pct` | percent | SUMO `edgeData.occupancy` or `laneData.occupancy`, along with lane geometry and native measurement settings | The assignment-count proxy |
| `observed_external_stopped_s` | sampled vehicle-seconds | FCD time on an external lane at speed below **0.1 m/s**, excluding internal links; prespecified sensitivity with threshold **1.0 m/s** | All delay, junction waiting, or a causal signal-delay estimate |
| `observed_internal_dwell_s` | seconds per traversed junction | Approximate time in *observed internal-lane samples* between entering and leaving internal links; explicitly record visibility and ±sampling resolution | Entire intersection/approach delay or exact dwell time |
| `unresolved_transition_s` | seconds per transition | Remaining interval between last known external-lane sample, observed internal samples (if any) and first downstream external sample; nonnegative and flagged if unsupported | Automatically attributed to intersection congestion |
| `observed_external_to_external_s` | seconds per route segment | First sample on external edge i to first sample on next external edge (or trip arrival), as in the existing comparator | Pure physical-edge traversal time |
| `observed_departure_lag_s` | seconds per trip | Actual SUMO tripinfo departure minus planned departure | Congestion predictor error |
| `predicted_edge_cost_s` | seconds per edge | Existing free-flow + original route-count surcharge + original junction proxy on the chosen route, reproduced without route changes | Calibrated link travel time |

**Rule:** Never compare `decision_prior_assigned_count` directly to `native_edge_occupancy_pct` as if both have the same units. Present any relationship as *proxy-to-outcome association*, optionally stratified by regime and edge, not calibrated physical occupancy error. Keep the native and FCD measurements side-by-side for consistency checks.

### Junction and road-phase decomposition

For each vehicle, use full FCD lane IDs (including `:...` internal lane IDs), speed, timestep, and lane position where supported:

1. Identify the ordered sequence of external and internal lane observations. Match external edges to planned `(vehicle_id, route_index, edge_id)`, **not merely (vehicle_id, edge_id)**, so repeat visits are not silently merged.
2. **External segment:** first external-edge sample to last external-edge sample; report elapsed time, sampled stops, and the interval bounds on exact entry/exit. Waiting immediately upstream of a junction remains *external-road waiting*.
3. **Internal junction:** recognize internal lane samples separately; record observed dwell, number of traversed internal lanes, whether samples span the entire internal transition, and visibility limitations.
4. **Transition gap:** the time not directly assignable to external or internal lane samples remains an **unknown interval**. Do not fold it into `junction_delay_s` by default. Use boundary ranges (lower/upper estimates reflecting the 1-second cadence) and a missing/unknown state.
5. Reconcile reconstructed whole-trip sample-based segments with tripinfo actual departure and arrival. Report the residual/unclassified seconds rather than forcing the parts to sum by silently assigning the residual to junctions.

The original predictor's **1-second branching-junction surcharge** is a cost proxy; compare it with observed *transition-time components* only as a diagnostic, and do not interpret difference as proven intersection-caused delay. Distinguish stopped time on approaches from time physically on internal links.

## 3. Capture instruments and correctness checks

Create a **new isolated diagnostic workflow**, leaving prior workflows, the original `time_aware.py` and archived results intact.

- **FCD**: request and verify 1-second sampling, `lane`, `speed` and `pos`; retain internal-lane IDs when emitted. Verify no FCD vehicle coverage filters are active. Log actual sampling cadence and missing data. Do not assume internal junction observations exist for every movement.
- **Native SUMO edge/lane measurement**: configure a 30-second `edgeData` export with `excludeEmpty="false"` and a separate `laneData` or `edgeData` view with `withInternal="true"` for junction interpretation. Capture `sampledSeconds`, `occupancy`, `density`, `waitingTime`, speed and interval begin/end as available; keep internal and external IDs distinct. Native `sampledSeconds` and occupancy obey SUMO's own conventions; do not assume exact equality with FCD sample integrals.
- **Tripinfo and events**: record planned and actual departures, arrivals, `duration`, waiting, departed/arrived counts; inspect teleport/route-change/warning diagnostics where available. Explicitly identify when a planned traversal was not actually observed.
- **Decision-time observations**: retain original frozen `chosen-decision-trace.csv`, `route-decisions.csv`, candidate trace, free-flow-only reference and hash manifest. Add a non-policy-changing observer to log actual search-time bin lookups if current *replay* is insufficient; prove it leaves routes/audits identical to the original policy.
- **Reproducibility**: capture SUMO version, **immutable image digest** (not only `latest`) before calibration, Git SHA, `netgenerate` config, network topology hash, OD tuple hash, trip XML hash, chosen-route hash, decision-trace hash, parameters, time bins, step length and seed. Raw XML hash may vary across independent generations; separately verify normalized topology and OD equivalence.

Native SUMO documentation: [FCD output](https://sumo.dlr.de/docs/Simulation/Output/FCDOutput.html), [edge/lane traffic measures](https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html), and [lane-area detectors](https://sumo.dlr.de/docs/Simulation/Output/Lanearea_Detectors_%28E2%29.html) (optional targeted queue cross-check; do not make E2 deployment a prerequisite).

## 4. Delivery phases and bounded execution

### M0 — Contract and synthetic unit fixtures; no new SUMO run

Implement the definitions and parsers in **new files** with fixtures covering: exact 30-second bin boundaries; vehicle present across several bins; stopped vehicle; zero vehicles / empty edge; missing 1-second sample; partial last bin; an internal-lane chain; route with repeated edge; delayed actual departure; telemetry gap; and legal turn validation. Negative or out-of-order intervals must be detected and labeled.

Prove that (a) assignment-count proxy stays distinct from observed vehicle-seconds and occupancy %, (b) every observed movement has a documented state or missingness reason, and (c) the comparator retains the existing free-flow and original predictor metrics for backward compatibility.

### M1 — Instrumentation smoke with development seed 2001

Run 1,000 matched OD trips on each of **200, 600, 1,200-second** windows using the **existing unmodified time-aware routing policy**. Use the separate manual cloud workflow, with artifact upload even on failure.

Quality checks: byte-identical routes/audits between traced and original policy; all 1,000 tripinfo completions; explicit counts of missing, duplicated and out-of-order FCD samples; repeated-edge-safe route joins; internal-lane observation coverage; report any teleports or discrepancies; reconcile native edgeData and reconstructed sampled occupancy in **units that actually match**. If a SUMO configuration flag or native field behaves differently than assumed, stop and correct *measurement code*, not route choices.

### M2 — Three-regime development/calibration matrix

**Prespecified disjoint development seeds:** `2101`, `2102`, `2103` for each of the three departure windows (nine scenarios, 1,000 trips per scenario). None has been run under this plan yet. Use the same OD generator, model parameters and matched OD pairs across regimes for each seed; only scale departures by the window. Keep all seed-level artifacts and report uncertainty / variation, not only pooled vehicle-level errors.

Primary analysis: per-seed time-aware versus free-flow entry-time bias/MAE/RMSE/p90/p95; physical occupied vehicle-seconds and native occupancy percent independently; external-edge stopped-time, internal-link dwell and unresolved-transition coverage; observed delay by route index, edge, forecast proxy band and congestion level. Show whether measured occupancy predicts later delay, but mark the association as observational.

Sensitivity: FCD sampling thinned from 1 to 2 and 5 seconds; 10/30/60-second aggregation. Document changes in joins, phase assignment and conclusions. Do **not** retune congestion pressure, junction surcharge, detour thresholds or routes in this milestone.

### M3 — Freeze and preregister the held-out study

**Reserved and untouched evaluation seeds:** `3101`–`3110` for each of the three regimes (planned 30 paired scenarios). Do not run, inspect their outcome statistics, or use them to adjust definitions during M0–M2. Ten seeds per regime are a feasibility target, **not guaranteed statistical power**.

Before any held-out evaluation: pin immutable SUMO image digest; freeze route generator, forecast equations, observation definitions, binning, handling of missing samples, comparison methods and code SHA; publish the seed matrix and signed-off analysis plan; record the freeze timestamp and hash. Any later model tuning is *exploratory* and requires a fresh holdout or a new protocol.

**Keep a clear boundary:** This milestone validates **measurement methodology and forecast diagnostics**. The later objective-alignment experiment is separate and will require controlled paired independent/cooperative routing, total realized journey-time and fairness measures.

## 5. Gates — what must be true before advancing

| Gate | Required evidence | If not met |
|---|---|---|
| **G0: Definitions** | Units and half-open bin semantics explicit; fixture tests for overlaps, internal/external distinction, missingness and trip-time reconciliation pass | Fix the parser/specification; do not run calibration |
| **G1: Policy invariance** | Traced and original route XML and audit CSV byte-identical per scenario; original cost components retained; route legality audited | Investigate instrumentation; never silently alter routes |
| **G2: Observation coverage** | All 1,000 trips finish; edge-route joins and all unmatched traversals accounted for; complete sample coverage report, internal-lane visibility and unknown intervals quantified | Label noncomparable rows and investigate; do not report hidden dropouts as success |
| **G3: Native cross-check** | FCD-derived vehicle-seconds / mean number of vehicles and native edgeData `sampledSeconds` / related quantities compared in compatible units, with difference and coverage reports; empty edges accounted for | Document semantics or missing emissions and repair before claiming physical occupancy quality |
| **G4: Calibration evidence** | All nine prespecified development scenarios run; bias/error/coverage broken down per seed and regime; sampling sensitivity assessed | Continue measurement investigation; no holdout release |
| **G5: Freeze** | Version/digest, code/input hashes, definitions, predictor parameters, report schema and untouched seed registry committed and reviewed | No held-out simulations |

**Do not create a data-dependent “accuracy passed” threshold after viewing the results.** Define measurement-quality gates independently from how attractive the predictor's MAE appears. Better predicted timing alone does not establish a reduction in network-wide travel time.

## 6. Expected artifacts

Each scenario's GitHub Actions artifact should contain:

1. `inputs-manifest.json`, network/trips hashes, normalized topology/OD hashes, SUMO version + container digest, route/audit invariance checks.
2. `decision-count-proxy.csv` (original model query values; `vehicle`, decision order, edge, forecast bin, raw count, capacity proxy, cost terms) and frozen chosen-route predictor trace.
3. `observed-edge-bins.csv`: edge/bin, covered seconds, external vehicle-seconds, mean vehicle count, observed stopped vehicle-seconds; never name this raw count “occupancy percent”.
4. `native-edge-bins.csv`: SUMO sampledSeconds, occupancy percent, density, waiting and speed with explicit units, missing-native flags, internal versus external classification.
5. `transition-phases.csv`: vehicle, route index, upstream/downstream external edge, observed internal lane sequence, external and internal sample-time bounds, unresolved seconds, stop samples, status.
6. `vehicle-edge-errors.csv`, `coverage-and-integrity.json`, `error-breakdown.json`, and human-readable `MEASUREMENT_DIAGNOSTIC.md`. Include **failed** job evidence too.

After M2, produce a **nine-scenario cross-seed report** with figures and limitations, plus a **separate freeze proposal**; no held-out claims until M3 is approved and executed.

## 7. Implementation boundaries and approval status

- **Allowed when separately approved for execution:** instrument observation, correct measurement code, add fixtures/diagnostic parsers, create separate manual GitHub Actions jobs and run limited development seeds.
- **Not in scope:** changing the time-aware route generator policy, adding penalty sweeps, using live driver data, declaring safety, launching Experiment 003, publishing a cooperative-routing success claim or using reserved holdout seeds.
- **Evidence preservation:** never rewrite the prior October 26 development results or original experiment workflows. Any measurement-method change after calibration starts must be versioned with its rationale and, where relevant, re-run consistently on development seeds.
- **Current status (Oct 26):** M0 fixtures and new measurement tools were implemented, M1 seed 2001 ran successfully across all three regimes, and M2 nine-scenario development calibration ran successfully with an immutable SUMO image digest per run. The original measurement design is retained for historical reference. **G3 native/FCD differences still require investigation; M3 freeze and all reserved holdouts remain untouched.**

**Approval record:** The user approved M0–M2 execution October 26, 2026. M0–M2 are now complete as developmental measurement milestones. **A separate approval is required for M3 protocol freeze and any held-out seed execution.**
