# Experiment 002 — G3 Measurement Reconciliation Protocol v0.1

**Status:** Approved for a measurement-only reconciliation of existing M2 development artifacts; **not approval for held-out evaluation**.  
**Scope:** Previously recorded seed 2101/2102/2103 × 200/600/1200-second SUMO datasets only. No new route selection, parameter tuning, seed generation, or SUMO simulations required for the first pass.  
**Parent documents:** [Measurement plan](EXPERIMENT_002_OCCUPANCY_JUNCTION_MEASUREMENT_PLAN_V0_1.md) · [M2 findings and known limits](EXPERIMENT_002_OCCUPANCY_M2_DEVELOPMENT_RESULTS_2026-10-26.md) · [Predictor-validation plan](EXPERIMENT_002_PREDICTOR_VALIDATION_PLAN.md)  
**Immutable source run:** [M2 calibration artifacts, workflow 40446073958](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958).

## 1. Problem and frozen diagnostic questions

Existing aggregate edge-bin mean absolute difference (MAE) across *every* edge/time bin can look small because empty road bins dominate. Meanwhile busy road/time bins show discrepancies approaching an entire 30 vehicle-seconds, and the junction-phase parser reports zero unresolved duration simply by allocating each sampled second to an external or internal lane. This is **not proof of exact intersection dwell measurement**.

G3 asks:

1. Does the observed-versus-native sampled vehicle-seconds disagreement concentrate in occupied or congested bins, and can its largest examples be classified by verified measurement semantics rather than assumed causes?
2. How much internal-junction dwell is actually observed, how many junction traversals are not observed internally, and what time uncertainty remains between discrete samples?
3. Does the predictor decision-time assigned-route count match the original *search-time input*, rather than being confused with observed occupancy? Can we distinguish chosen-path replay from unchosen search expansions?
4. Is the measurement contract, source provenance, and missingness accounting complete enough to propose an M3 freeze?

No retrospective numerical threshold is used to assert that a predictor is accurate; G3 is primarily a **methodology and classification gate**.

## 2. Occupancy audit and reproducible selection

For **each of the nine preselected scenarios**, analyze all native SUMO `edgeData` **external** edge/time bins. Reconcile against the matching `observed-edge-bins.csv` row derived from 1-second SUMO FCD. Independently compare external entries between `native-external.xml` and `native-with-internal.xml` to detect configuration differences.

- Preserve edge ID, half-open bin `[begin,end)`, duration, native `sampledSeconds`, FCD external vehicle sample-seconds, and `difference = FCD - native`.
- Separately tabulate **all bins**, **native-positive bins**, **busy bins (`native sampledSeconds >= 30` vehicle-seconds/30-second bin)**, **native-positive/FCD-zero bins**, and **empty-native/FCD-positive bins**. Busy is a diagnostic stratum, *not* an accuracy success threshold.
- Report per-stratum number of bins, native/FCD sums, signed difference, MAE, p95 absolute difference, max absolute difference, and `sum(|difference|)/sum(native)` when the denominator is positive. Keep both unweighted and volume-weighted views.
- Select the **20 highest absolute-difference external bins per scenario**, breaking ties by edge ID then time; additionally report 20 worst among busy bins. Include raw values and a unique artifact reference so each outlier can be inspected. Do not interpret this selection as a random representative sample.
- Record external/native consistency checks, negative or missing values, coverage and bin alignment; do not silently drop unmatched bins.
- Possible causes to investigate using raw 1-second FCD, upstream/downstream vehicle positions, network lane shapes, queue behavior and SUMO measurement documentation include: fractional entry/exit seconds, multiple-edge vehicle overlap/length effects, native sampledSeconds conventions, lane changes, and internal-lane assignment. **These remain hypotheses unless traced to an individual vehicle/edge and independently supported**. Label unexplained events `unresolved`, not `explained_by_sampling` by default.
- The original `decision_prior_assigned_count` is a route-assignment proxy; do not directly subtract it from either FCD vehicles or SUMO occupancy percent.

## 3. Junction and delay reconciliation

Use `transition-phases.csv` and raw FCD/route/tripinfo as source. A planned `(vehicle, route_index, external_edge)` is the join key; a repeated edge ID may denote a separate visit.

- Report external approach stopped sample-seconds at speed <0.1m/s (also sensitivity <1m/s), separately from samples on internal junction lanes.
- For each measured transition with `n` contiguous internal-lane samples at 1-second cadence, use conservative, explicitly **sample-based**, not causal, dwell-time bounds `[max(0,n-1), min(external_to_next_seconds,n+1)]`. For `n=0`, the interval can contain an unobserved subsecond internal movement; record bounds `[0,min(external_to_next_seconds,1)]` *only where timesteps are verified contiguous*. Flag any missing timesteps, invalid intervals, duplicated samples, or negative bounds as exceptions, not precise measurements.
- Record percent of route segments with observed internal samples, percent without them, total lower/upper bound sums, mean uncertainty width, and the share of internal-sample-absent segments. Do not call the difference between bounds "intersection-caused delay."
- Expose earlier `unresolved_transition_seconds=0` as a **discrete bookkeeping result**, not zero physical phase-boundary uncertainty.
- Check tripinfo arrival/departure consistency and report residual/unclassified time. Any blocked route match must be accounted for; do not replace missing records with zero.
- Without instrumenting exact transition events, a fully identified allocation of external queueing, junction service time, and physical intersection delay may be impossible. Acknowledge identifiability limits rather than inventing a decomposition.

## 4. Decision trace audit

- Verify original/traced `route` XML and audit file hashes or `policy-invariance.txt` and the original search cost versus candidate replay across **all scenarios**; independently count decision records and path rows.
- Validate `decision-count-proxy.csv` schema, nonnegative assignment counts, time-bin semantics, capacity-proxy denominator and cost equation. Preserve origin-edge sentinel `origin_not_searched` separately.
- Note precisely: current `trace_actual_predictor.py` computes pre-assignment **chosen-route replay**, not a complete event log of every searched Dijkstra alternative. Mark complete **search-time lookup audit = OPEN** until a non-policy-changing capture proves lookup equivalence and logs unchosen expansions, or the scientific protocol deliberately narrows the question to chosen-path replay.
- Do not treat prediction-versus-observation association as policy improvement, and do not treat the external-road queueing association as causal attribution.

## 5. Execution phases (approved G3, no new simulations)

**G3-A — Reconcile existing observations.** Implement a deterministic offline audit that consumes the nine previously uploaded GitHub Actions artifacts, not fresh SUMO results. Verify scenario provenance (seed, window, exact route invariance, complete trips), immutable SUMO image reference, expected files, and unchanged OD-pair hashes across windows. Write per-scenario external-native strata, top-outlier tables and coverage reports. Repeat the audit from the same artifacts to check deterministic summaries.

**G3-B — Bound junction sampling uncertainty.** For those same nine datasets, compute internal-sample visibility, upper/lower transition-time bounds, unsampled transitions, apparent stopped time, and missingness. Preserve ordered route-index matching. Use synthetic test fixtures for absent internal samples, discontinuous timelines, partial last bins, and internal lane strings with underscores.

**G3-C — Classify and document.** Investigate the 20 worst external discrepancies per scenario (180 selected edge-bins; overlap with busy top-20 noted). Separate *verified* mechanism, *consistent-with-but-unverified*, and *unresolved*. Do not turn hypotheses into causal findings. If only summary-level data are available, publish an **unresolved diagnostic ledger** and do not pass G3. Identify when further event-level instrumentation is needed.

**G3-D — Closure review (separate decision from M3 freeze).** Publish a versioned G3 memo listing what was reconciled, remaining errors/visibility limits, integrity test results, and an explicit **pass / revise measurement / defer** outcome for each subgate. Publishing the memo is not authorization to run held-out seeds.

## 6. Gates — predeclared, measurement-oriented

| Gate | PASS requires | Otherwise |
|---|---|---|
| G3-0 Integrity | Exactly 9 expected M2 scenarios; 1,000 complete trips per scenario; no reserved seeds; route/audit invariance; valid fixed 30-second bins; external source rows match native output by key; no silently dropped rows | BLOCK |
| G3-1 Occupancy reconciliation | Occupied/busy-bin stratification; top outliers linked to original artifact/row; discrepancy mechanism confirmed with evidence **or explicitly unresolved and scoped away from any accuracy claim**; no unit conflation | REVISE/DEFER |
| G3-2 Junction interval accounting | All matched route segments have valid sample-interval bounds, reported missing-internal fraction and unknown/unclassified bounds; sample gaps detected, and causal claims avoided | REVISE/DEFER |
| G3-3 Forecast provenance | Chosen-path replay matches original search cost and routing; distinction from missing full search-time lookup trace is explicit. Full lookup equivalence must be separately confirmed if required by the intended accuracy claim | REVISE/DEFER |
| G3-4 Freeze readiness | Artifact provenance, code SHA/digest, schema, bin size, missingness policy and all residual uncertainties documented with named owners/next actions | PROPOSE FREEZE ONLY, NOT AUTO-PASS |

No acceptable MAE, bias, or correlation threshold may be added after reviewing these M2 results. If evidence is insufficient, record `OPEN` and **do not proceed to M3**.

## 7. Deliverables and publication policy

- Executable offline G3 audit and fixture tests in **new** files (do not modify original `time_aware.py` or prior results).
- Deterministic artifact download/processing workflow with **no SUMO jobs** and **no evaluation seeds**.
- `g3-per-scenario.csv`, `g3-occupancy-strata.csv`, `g3-top-edge-bin-outliers.csv`, `g3-junction-uncertainty.csv`, `g3-integrity.json`, `G3_RECONCILIATION_REPORT.md`.
- Results published on GitHub with immutable evidence links and explicit gate statuses; keep source artifact IDs, SHA/digest and run ID `40446073958`.

**Success is an auditable explanation of what our instruments measure and do not measure.** It does not imply that the time-aware predictor is calibrated, that cooperative routing helps traffic, that the model is safe for real-world drivers, or that held-out evaluation can begin.
