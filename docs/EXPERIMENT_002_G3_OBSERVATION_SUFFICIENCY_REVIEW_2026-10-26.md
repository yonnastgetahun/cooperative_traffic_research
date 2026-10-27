# Experiment 002 — G3 Observation Sufficiency Review and Pre-Freeze Decision v0.1

**Date:** October 26, 2026 (Pacific)  
**Decision:** **CONDITIONALLY SUFFICIENT for a limited, simulation-internal timing and road-load diagnostic; NOT sufficient for physical-occupancy forecast calibration, causal junction-delay attribution, or routing efficacy claims.**  
**M3 status:** **NOT FROZEN; held-out seeds 3101–3110 NOT AUTHORIZED or run.**  
**Scope of this review:** Evaluate existing evidence and specify the limits of valid measurement claims; no new SUMO simulation or predictor-policy alteration was undertaken here.  
**Evidence:** [G3 J0–J3 results](EXPERIMENT_002_G3_EVENT_INSTRUMENTATION_RESULTS_2026-10-26.md) · [G3 native/FCD reconciliation](EXPERIMENT_002_G3_RECONCILIATION_FINDINGS_2026-10-26.md) · [nine-development-seed M2 results](EXPERIMENT_002_OCCUPANCY_M2_DEVELOPMENT_RESULTS_2026-10-26.md) · [durable event reports](results/exp002_g3_events_2026_10_26/README.md) · [G3 evidence archive](results/exp002_g3_2026_10_26/README.md).

**Subsequent authorized development-only execution (October 26):** [G3 R0–R2 three-regime verification results](EXPERIMENT_002_G3_R1_R2_VERIFICATION_RESULTS_2026-10-26.md) completed the proposed timing bridge and search-read audit using explored seed 2101 across high/moderate/low congestion. All **25,179** native/FCD ordered external-edge entries matched at the same simulation step; **1,994,952** actual source counter lookups were reconstructed without routing changes. The original review below is retained as the prereview decision and historical limitations inventory. **R0–R2 passed for the examined development scenarios; R3/R4 and M3 freeze remain open; no held-out seeds were touched.**

## 1. Exactly what we intend to validate

**Narrow scientific question:** *Given 1,000 prescribed trips in an immutable synthetic SUMO network, does the original time-aware routing cost model predict **time to reach the next road and downstream road-entry times on routes actually chosen** more accurately than a free-flow-only reference, and how do its errors vary with observed congestion?*

This is a forecast/measurement question, not a test that cooperative routing minimizes system travel time. The prior research still favors independent routing in the evaluated initial development cases. Forecaster accuracy does not demonstrate objective alignment, superior assignments, individual fairness, safety or real-world transfer.

**Permitted primary estimand (proposed for eventual freeze, not yet frozen):**
- Vehicle/route-index **external-edge entry time**, in **simulation seconds**, obtained from an ordered native `vehroute-output.exit-times` stream **including internal links** and the actual `tripinfo.depart` value for the first external edge. For subsequent external edges, infer entry at the exit of the preceding ordered external or internal link, acknowledging the one-second solver-step boundary. Cross-check with FCD first-seen external-edge sample (front position), but **do not substitute** its sample time without declaring a different reference definition.
- Forecasts are **pre-SUMO**, taken from the default-off original time-aware search trace/replay along the route actually selected. The full search-time counter event stream is separate provenance, not an observation of the traffic's physical state.
- Report `observed_native_entry_s - predicted_entry_s` (signed bias, MAE, RMSE, absolute p90 and p95) per **individual development seed × regime**, including first edge, route indices 1–2/3–5/6+, and actual minus scheduled departure lag. The free-flow reference uses the **same chosen routes and trip population**; never compare its forecast error to a separately simulated independent-routing policy and pretend the contexts are equal.
- Secondary timings: ordered external-edge residence, internal-link residence, external-to-external interval, and tripinfo duration/wait/timeLoss. External-to-external includes internal traversal; internal-link residence is **not automatically congestion-caused excess delay**.
- The 30-second reporting window is prespecified. 10- and 60-second binning and 1/2/5-second FCD sensitivity may be shown as robustness descriptions; do **not** choose the best-performing window after viewing data.

**Out of primary scope:** pointwise time-continuous junction crossing, subsecond ground truth, exact congestion caused by a signal, realized costs for candidate routes never driven, physical-road occupancy *predicted by* the assignment-count proxy, real-world human-driver performance, benefit/harms of cooperative route assignment.

## 2. Source-by-source sufficiency review

| Observable / claim | Evidence and supported resolution | Verdict for a *synthetic* validation study | Explicit limits |
|---|---|---|---|
| Trip departure, arrival, duration and completion | Native `tripinfo`; J1 and J3 matched original trip outcomes for 1,000 vehicles | **YES for these tested scenarios** | Applies only to the source SUMO model, fixed network/demand and finished trips; check teleports and unfinished coverage |
| Ordered external-edge visits | `vehroute-output.exit-times`, native internal-edge export; 8,367 external records on J1, original routes matched | **YES at solver-step resolution on J1/J3** | Full three-regime coverage and repeated-edge/edge-boundary audits still require a pre-freeze verification |
| External-edge entry and exit *simulator event steps* | Native consecutive ordered exit times, initial departure and FCD front samples; native events J1/J3 leave trip outcomes invariant | **CONDITIONALLY YES** | Entry is inferred from previous exit; time is quantized to the configured 1-second step, not independent continuous-time crossing |
| Internal-link *residence* | J1 observed 8,338 internal events; J3 `veh0213` residence 42 solver seconds across `:C7_11` and `:C7_19` | **YES as simulated internal residence** | Not an attribution of 42 seconds of *extra* delay caused by the junction; short internal links may have no FCD sample |
| Physical road presence | Native external edge `sampledSeconds` (vehicle-seconds), with half-open intervals and fractional vehicle presence | **YES as SUMO-internal aggregate reference** | Not equal to FCD number of vehicle fronts; not observed real-world traffic; edge-body overlap may make vehicle presence occur on multiple edges |
| Road occupancy percentage | SUMO native `edgeData.occupancy` (percent of roadway space occupied) | **YES as a separately defined SUMO output** | Percent occupancy is not vehicles, `sampledSeconds`, nor planner route-assignment count; preserve source geometry/lanes/step conventions |
| FCD one-second lane/speed/position | Original 1s trajectory front snapshots, stop samples, internal-lane visibility and deterministic route-index matches | **YES for descriptive trajectories and approximate stop time** | Vehicle-front lane can differ from road body extent; FCD cannot establish exact step-internal transition or rear-bumper presence |
| Original planner `occupancy[(edge, bin)]` values | Default-off live instrumentation logged **677,507** source reads and **8,367** assignment updates with zero independent audit errors in development seed 2001; another selected high-load seed passed | **YES as actual planning-input provenance on tested seeds** | The quantity is a *prior announced route assignment count*, not a forecast of native physical occupancy/queue length; full regime coverage not shown |
| Predictor edge/trip timing accuracy | Model cost along chosen path, free-flow reference, matched observed trips | **ELIGIBLE for narrowly scoped diagnostic AFTER native-entry target and join contract are fixed** | Existing 53.52s / 18.67s / 13.32s development MAEs used FCD first-seen entries; do not relabel them native-event entry errors |
| Physical occupancy *prediction* accuracy | The model currently produces assignment counts and cost surcharges, not explicit physical vehicle-seconds or % predictions with matching support | **NO** | Computing native occupancy MAE for the route counter is a unit/estimand error; new explicit pre-SUMO physical-load forecast would be a different model, needing its own plan |
| Junction-*caused* congestion delay | Simulated link residence/approach stops observed, but no valid counterfactual free-junction baseline or causal isolation | **NO** | Keep "internal-link residence" separate from "causal junction delay"; even 42 seconds within internal links is not 42s of junction-caused excess time |
| Cooperative route-policy benefit, fairness or real-world safety | Not part of this G3 instrumentation, no paired objective/fairness test here | **NO** | Cannot be inferred from a forecast-timing comparison, or from SUMO-only sensor integrity |

**External references used to establish the measurement definitions:** [SUMO edgeData `sampledSeconds`, occupancy and derived mean vehicles](https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html); [SUMO vehroute exit times/internal-edge output](https://sumo.dlr.de/docs/Simulation/Output/VehRoutes.html); [SUMO FCD front position and cadence](https://sumo.dlr.de/docs/Simulation/Output/FCDOutput.html). The current repo's experiment evidence establishes successful usage in the pinned SUMO **1.28.0** development environment; current online docs may describe capabilities beyond that exact build.

## 3. Why the earlier native/FCD discrepancy does not invalidate native occupancy

Across the nine M2 scenarios, average absolute native-vs-FCD sampledSeconds differences were modest when many empty bins were included, yet on busy roads `sum(abs(FCD-native))/sum(native)` was ~**4.5% high / 4.9% moderate / 4.4% low**, with selected bins differing by 30 vehicle-seconds. The [211-case cross-edge ledger](results/exp002_g3_2026_10_26/g3-cross-edge-ledger.csv) found downstream-junction-front proximity in all **211 preselected negative outlier bins**, with near-boundary sample counts within one vehicle-second of the difference for 140 cases. The targeted `C6C7` replay showed native 30 vehicle-seconds on the upstream road during [60,90), while FCD showed zero vehicle *fronts* on it and a stopped downstream internal-lane front. This supports vehicle-body boundary overlap as a mechanism, **not exact per-vehicle native accumulator reconstruction**.

**Interpretation for research scope:** The two systems are not required to yield equal totals because they count different phenomena. Retain both sources and their dissimilarities; **use native SUMO road presence as the aggregate simulated-road reference**. Do not publish FCD-front minus native-road differences as "prediction error." A remaining lack of body-length attribution is a **reported limitation** for this narrower study, not by itself evidence that the native measurement is corrupt. A study that claims per-vehicle body occupancy would require further geometric instrumentation.

## 4. Junction timing sufficiency is a conditional yes, not "exact"

Native exit events provide a more defensible, ordered, **step-resolved** timing reference than guessing durations from every one-second FCD front sample. In J1, **16,705** ordered events included **8,338 internal** and **8,367 external** records over 1,000 completed trips; observed per-vehicle tripinfo matched the archived run. In J3, the selected `veh0213` exited `C6C7` at 57s and completed its internal-link sequence at 99s, a measured **42 simulated seconds of internal-link residence**, not causal delay.

Before switching the forecast scoring reference from FCD-first-sample to native-inferred entry:
1. **Run the comparator over the archived original development runs** to quantify how often the two definitions differ by 0, 1, or more simulation steps; audit the full set of planned external edges, repeated IDs, internal ordering and any missing link times. Use only existing development data/replays; do not use holdouts.
2. Establish a single explicit `actual_external_entry_step_s` join rule and account for planned-vs-actual departure. Correct handling of the first and final roads is essential.
3. Confirm consistency across **all three congestion regimes**, or state the remaining limitation rather than assuming one high-load run generalizes. If a limited original-development-seed replay is required, request execution approval separately and verify route/trip invariance against archive.
4. Distinguish **native event-step resolution** from continuous physical boundary crossing and from FCD front time. No arbitrary <1-second claimed accuracy when using 1-second steps.

**Interpretation:** One-second native step measurements are **sufficient to ask a step-level timing-forecast question**. They are **not sufficient** for millisecond-scale junction dynamics or a causal isolation of light/signal delay. A 0.1-second SUMO rerun would change simulation dynamics and is not a cleaner observation of the same simulation; it is not a prerequisite for this narrow study.

## 5. Search-time input sufficiency

The live event observer is a material advance: 677,507 actual `occupancy[(edge,time_bin)]` reads in seed 2001 (high congestion), 678,828 on seed 2103 (high congestion), and byte-identical output with/without the sink. That **resolves search-input provenance for these two inspected high-load development runs**. The original cost arithmetic, heap ordering, chosen routes and assignment revisions are cross-checked.

The *meaning* of the values remains unchanged: prior **assigned-path counts in one planning bin**, not physical occupancy estimates. There is no well-defined residual `observed_occupancy_percent - assigned_count`. At most the counts can be used as predictors/covariates in a prespecified **association** with future observed native road load or entry-time error, with forecasting time support and no future-information leakage disclosed.

Before freeze, require either (a) demonstrate the same event-sink integrity and route invariance on **one moderate and one low-load development replay**, or (b) explicitly narrow the claims and label the absent regimes. No numerical success thresholds should be chosen after reviewing the outcome errors.

## 6. Limitations and severity register

The complete audit-friendly limitation inventory is in [the G3 measurement limitations register](EXPERIMENT_002_G3_MEASUREMENT_LIMITATIONS_REGISTER_2026-10-26.csv). The most consequential entries are:

| ID | Constraint | Freeze impact / proposed disposition |
|---|---|---|
| **L01** | One-second step timestamps, inferred link entries | **Nonblocking if step-level timing is the declared estimand** and coverage tests pass |
| **L02** | Native vehicle-body presence vs FCD vehicle-front counts | **Nonblocking if native occupancy and FCD fronts are never conflated** |
| **L03** | Route-assignment count is not physical occupancy prediction | **Blocks any physical-occupancy forecast-accuracy claim**; remove that estimand from the narrow validation |
| **L04** | Native entry-time/route-index join not yet established across all regimes | **Blocks timing-target freeze** until checked or restricted |
| **L05** | Native stream/outcome invariance checked only on two high-load development replays | **Blocks full three-regime coverage claim** until cross-regime check or explicit limitation |
| **L06** | Junction residence is not junction-caused delay | **Blocks causal-junction-delay claim**, not step-level internal residence |
| **L07** | Original search event coverage only for two high-load development runs | **Blocks cross-regime search-read provenance claim** until extended or scoped |
| **L08** | Model still systematically underpredicts lateness | **Blocks declaring predictor accuracy validated**; does not invalidate observation instrumentation |
| **L09** | Synthetic 10×10 grid, 1,000 vehicles, no real-world observations | **Always blocks real-world generalization/safety claims** |
| **L10** | Native edgeData partial/empty bins and rounding | **Needs explicit coverage and denominator rules** before any aggregate comparison |
| **L11** | Only driven route outcomes are observed | **Blocks counterfactual candidate-route outcome and policy-optimality claims** |
| **L12** | Raw search event artifact retention and data reproducibility | **Need immutable source hashes/code/digest, reproducible route generator and retained schema** |
| **L13** | Teleports/unfinished arrivals and route changes can alter comparisons | **Require explicit event/completion checks**, even when 1,000 trips finish in tested scenarios |
| **L14** | Prior error reports used FCD first-seen entry, not native-inferred entry | **Do not silently reuse published MAEs** under the proposed reference definition |

## 7. Pre-freeze readiness tests — not an M3 freeze proposal

**R0 — Define target and write analysis contract:** Publish one canonical external-edge-entry `observed` reference, prediction timestamp semantics, fixed bins, complete route-index joins, missingness and teleport policy. Declare the native-versus-FCD source roles. Exclude any "physical occupancy forecast MAE" of the assignment counter.

**R1 — Timing-reference bridge:** Produce a development-only paired table for native-inferred entry versus FCD first-sample entry across 200, 600 and 1,200s, verifying (a) every planned external edge is accounted for; (b) first and last edges are handled; (c) step quantization and timestamp differences are reported; and (d) the original previously published FCD-based errors are not rewritten.

**R2 — Search-input provenance coverage:** Verify original search event logging in moderate and low development regimes, proving exact route/audit invariance and counter-update reconstruction for those scenarios, or explicitly scope claims to verified high-load runs.

**R3 — Synthetic-data integrity and native road outcomes:** For every planned seed/window, verify 1,000 completions, route legalities, native `edgeData` output, empty/partial interval rules, no hidden teleport contamination, immutable SUMO digest and Git commit/hash manifests. Define all status codes in the frozen schema.

**R4 — Prespecify analysis and uncertainty before holdout:** State per-seed paired forecast differences (rather than treating all vehicle-edges as independent), means/uncertainty, late bias, missingness, and subgroup error by road/route position/regime. Do not select "passing" accuracy cutoffs based on the inspected development outcomes. The original three-regime negative routing result stays a separate claim.

**R5 — Scientific authorization boundary:** Publish a proposed M3 protocol-freeze document only after R0–R4 are complete and reviewed. The user must explicitly approve freeze and later held-out execution; neither is implied by approving this sufficiency review.

### Decision table

| Decision question | Answer now |
|---|---|
| Are native SUMO aggregate occupancy and 1-second movement records scientifically usable? | **Yes, for bounded simulation-internal observation with explicitly different target quantities** |
| Can we label original prior-route assignment counts a physical occupancy predictor and score them in native vehicle-seconds? | **No** |
| Is native one-second road/internal edge timing sufficient for the specific next forecast-timing diagnostic? | **Conditional yes, provided the route-index/entry target and coverage bridge is implemented** |
| Can we quantify true continuous-time or causal intersection delay? | **No; out of scope unless separately designed** |
| Is the model's forecast calibrated? | **Not yet; development records show significant systematic late bias** |
| Should M3 be frozen or evaluation seeds released today? | **No. Complete R0–R4 and a separate approved freeze proposal first.** |

## 8. Approval/status record

This review implements the approved request to **assess measurement sufficiency and document remaining limitations before proposing any M3 freeze**. It involves source/code/documentation review only and is **not** an implemented change to the SUMO model or evaluation protocol. **No additional simulations or validation-seed runs were performed in this review.**

**Recommended immediate next milestone:** Write and execute the **development-only timing-reference bridge** (R0–R2) with one existing scenario per regime, preserving the original policy and source results, then prepare an M3 preregistration proposal if the evidence supports it. Do not use reserved evaluation seeds `3101–3110`.
