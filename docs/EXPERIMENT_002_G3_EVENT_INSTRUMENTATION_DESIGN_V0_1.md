# Experiment 002 — G3 Targeted Event Instrumentation Design v0.1

**Date:** October 26, 2026 (Pacific)  
**Status:** **Approved and executed for J0–J3 on October 26, 2026. All targeted development runs and policy-invariance checks succeeded; J4 findings published. G3 remains PARTIAL and M3 evaluation BLOCKED.**  
**Purpose:** Resolve two remaining G3 measurement questions: (A) *when* vehicles traverse external edges and internal junction links, within the resolution of a fixed SUMO simulation; and (B) *which occupancy counter values* the time-aware route-search algorithm actually reads when evaluating every candidate, including unchosen candidates.

**Parent:** [G3 Reconciliation Protocol](EXPERIMENT_002_G3_MEASUREMENT_RECONCILIATION_PROTOCOL_V0_1.md) · [G3 measured findings](EXPERIMENT_002_G3_RECONCILIATION_FINDINGS_2026-10-26.md) · [M2 development run 40446073958](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958).  
**Immutable M2 SUMO image:** `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb` (resolve/test availability before use).  
**Verified execution:** [J0–J3 Event Instrumentation Findings and Gates](EXPERIMENT_002_G3_EVENT_INSTRUMENTATION_RESULTS_2026-10-26.md) · [durable archived integrity and anchor evidence](results/exp002_g3_events_2026_10_26/README.md). This text preserves the originally approved experimental design; its planned steps have now been executed in the limited development scope.

**Research boundary:** Purely synthetic SUMO, 1,000 fixed trips on a 10×10 network. No real driver data, no optimization, no new algorithm, no route/pressure/guardrail changes, no seeds 3101–3110.

## 1. Core design decision

**Use two independent, complementary event streams.**

1. **Simulation movement stream, postdeparture:** Prefer SUMO's built-in `--vehroute-output`, `--vehroute-output.exit-times true`, and `--vehroute-output.internal true` on a replay of the *already frozen* route assignments. Record exit times from external and internal edges, separately from 1-second FCD front-position snapshots, native `edgeData`, and `tripinfo`. This provides edge-exit *simulation timestamps*, not exact unobservable continuous-time border crossings. **Verify that the installed SUMO version actually emits internal-edge exit times with the expected route alignment before claiming this output meets our needs.** If not sufficient, use an **entirely read-only TraCI observer** that calls `simulationStep()`, `getLaneID`, `getLanePosition`, `getRouteIndex`, `getSpeed`, `getLength` and simulation departure/arrival IDs at every original solver step. TraCI observers must never call setters, `vehicle.add`, `reroute`, `moveTo`, or modify simulation parameters.
2. **Routing decision stream, predeparture:** Add an **optional, read-only event sink** inside the original `time_aware.search` loop (off by default), logging each heap expansion and each actual `occupancy[(candidate_edge, queried_bin)]` lookup *before any assignment counter is incremented*. Do not substitute chosen-path replay as proof of what happened during searches of other paths. The search uses the original cumulative single-entry-bin **assignment count**; this is neither physical road occupancy nor a direct calibrated forecast of simultaneous vehicles.

**Keep observation, original search policy, and post-hoc analysis in separate modules, files and GitHub Actions jobs.** An event logger is not allowed to influence the search's queue, tie-breaks, cost arithmetic, occupancy writes or vehicle ordering.

## 2. Scope and scenario selection — no new discovery seeds

**Stage E0: no simulation.** Freeze a v0.1 event schema, synthetic fixtures, output hashing and acceptance tests.

**Stage E1: deterministic minimal replay**, on previously inspected *development* scenarios:
- **200-second window, seed 2001** — first proof that event capture reproduces the successful earlier high-congestion run `40443562182`.
- **200-second window, seed 2103** — selected before replay because the archival G3 ledger contains the interpretable case `C6C7` at simulation `[60,90)`, vehicle `veh0213`, near downstream internal lane `:C7_11_0`.
- **1,200-second window, seed 2101**, only if E1 high-congestion run passes; contrasting low-load condition using an already explored seed.

No full nine-case rerun by default. The user may approve expanding to other previously used **2001/2101–2103** scenarios if the targeted evidence requires it. Seed `1001–1003` remains historical/development; **3101–3110 stay unrun**.

**The distinction between extra *observation outputs* and a changed simulator must be measured, not assumed.** Replay the original routes using exactly the same SUMO version/digest, seed, traffic demand, `netgenerate` configuration, model and step length. Compare all vehicle tripinfo departure/arrival/duration/waiting/timeLoss, route order and completion against the original M2 archived run; use per-vehicle canonical values rather than raw XML byte equality (which may contain generation metadata). If a benign output flag changes behavior or route inputs differ, fail the comparability gate and record why. Do not merge discrepant runs into the original 9-seed averages.

## 3. Temporal resolution: "exact" only to simulation discretization

The M2 experiments used default SUMO **1.0-second solver steps**. Native edge exit times and per-step TraCI snapshots are *simulation-defined event values*, not certified continuous crossing times with subsecond precision.

- Required v0.1 primary interpretation: event timestamps in **simulation seconds at the original 1-second step**, with provenance `native_vehroute` or `read_only_traci`. For an observed transition from an external lane at step `t0` to an internal lane at `t1`, record the boundary interval `(t0,t1]`, its width, and any event timestamp available from SUMO; never silently report `t1` as a perfectly known physical crossing instant.
- Optional **0.1-second solver-step** run is *not* a higher-resolution observation of the identical original traffic simulation: it changes departure insertion, lane changes and car-following dynamics, and must be treated as a **separate sensitivity simulation with different dynamics**, not ground truth for the 1-second M2 results. Do not run it during the first approved E1 sequence.
- The original FCD output has front-bumper location/road membership; vehicle-length overlap with upstream roads can persist after the front enters an internal junction. Keep **front crossing**, **physical-extent occupancy** and **timeLoss/halting** distinct.

SUMO reference: [Vehroute exitTimes and internal-edge option](https://sumo.dlr.de/docs/Simulation/Output/VehRoutes.html), [FCD front-position semantics](https://sumo.dlr.de/docs/Simulation/Output/FCDOutput.html), [time-step effects](https://sumo.dlr.de/docs/Simulation/Basic_Definition.html), [read-only TraCI methods](https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html), [native edge occupancy](https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html).

## 4. Movement-event schema and reconstruction algorithm

Write immutable `movement-events.csv.gz` or `movement-events.parquet` plus `junction-phases.csv` and a human-readable observation log. Every movement event includes:

| Field | Definition |
|---|---|
| `scenario_seed, window_s, simulation_step_s, source_run_sha` | Provenance and original solver resolution |
| `vehicle_id, planned_route_index, observed_edge_ordinal` | Ordered join key; do not collapse repeated edges |
| `event_sequence, event_type` | `actual_depart`, `external_enter`, `external_exit`, `internal_enter`, `internal_exit`, `arrive`, `teleport_start/end`, `missing_sample` |
| `previous_lane_id, next_lane_id, internal_edge_id` | External/internal classification; preserve full `:...` IDs |
| `event_time_s, lower_bound_s, upper_bound_s` | SUMO event time and conservative interpretation interval |
| `front_position_m, vehicle_length_m, speed_mps` | When available; missing is `null`, never a fabricated length |
| `source, observation_status` | `vehroute_exit_times`, `traci_step`, FCD cross-check; measured / bounded / ambiguous / missing |

**Priority extraction route:**
1. Run `sumo` with `--vehroute-output results/observed-vehroute.xml --vehroute-output.exit-times true --vehroute-output.internal true` alongside the same FCD, native edgeData and tripinfo settings. The full route with internals is **diagnostic output only**, never fed back as a route input.
2. Parse route edge IDs and aligned `exitTimes` as ordered tuples, verify counts and monotonicity, and align its external subsequence with the planned ordered route (including repeated IDs). Internal edge exit events between consecutive external exits define a simulation-step-resolved internal movement sequence, subject to SUMO's output conventions.
3. Reconcile first edge with actual `tripinfo.depart`, last edge with arrival, and inter-edge times with one-second FCD lane/position samples and native edgeData. Report how often internal entries/exits are observable and with what temporal support.
4. If native output does not expose transitions sufficiently, run a separate read-only TraCI observer with the same immutable input and 1-second simulation step. Snapshot IDs every step, record lane/edge/route-index changes, and bracket transitions by adjacent observations. Record missing internal observations and arrivals separately. Validate that the TraCI-controlled run reproduces the standalone SUMO baseline before interpreting timing.

**Derived `junction-phases.csv` per external-to-external transition:** `vehicle_id, from_route_index, from_edge, to_route_index, to_edge, preceding_external_exit_s, internal_enter_bound_lo/hi_s, internal_exit_bound_lo/hi_s, subsequent_external_enter_s, internally_observed_s, external_approach_stopped_s, unknown_or_gap_s, event_resolution_s, flags`. Subtract only quantities with compatible time boundaries. **Never call an external approach stop "junction service delay" merely because it occurs near a junction.** Also avoid labeling internal dwell as extra delay: compare to a defensible no-congestion internal traversal reference only in a separately specified analysis.

### Boundary-occupancy verification

For prespecified G3 `211` extreme negative discrepancy bins, prioritize the explicit `veh0213` case and 20 largest high-load examples. Where `length` and `lane position` are available, tag a vehicle as potentially extending onto an upstream road when `front_position_m < vehicle_length_m` on a downstream internal lane. This is a **geometric candidate**, not an exact reconstruction of the native SUMO `sampledSeconds` accumulator: internal lane topology, car-following/entry interpolation and overlaps across junctions can change accounting. Report confirmed link-to-link continuity separately from unexplained numerical residuals.

## 5. Direct *search-time* occupancy lookup events

The current `trace_actual_predictor.py` is explicitly labeled `original-search-equations-replayed-on-route`: its chosen-path records do **not** prove every heap search lookup. New optional `trace_sink` inside `time_aware.search` must emit **raw source events** as the search executes:

| Field | Source / semantics |
|---|---|
| `vehicle_id, departure_s, decision_ordinal, search_event_ordinal` | Actual deterministic vehicle and event order |
| `event_type` | `search_start`, `heap_pop`, `stale_pop`, `edge_lookup`, `relax_accepted`, `relax_rejected`, `destination_reached`, `search_end` |
| `from_edge, to_edge, current_heap_cost_s, predicted_candidate_entry_s, lookup_bin` | Actual popped label, next edge and computed `floor(entry / 30)`; **not** a replay clock |
| `prior_assigned_count, capacity_proxy, freeflow_edge_s, congestion_surcharge_s, junction_proxy_s` | Actual `occupancy[(to_edge, lookup_bin)]` counter value and existing model terms; `prior_assigned_count` is a planning proxy |
| `new_label_cost_s, previous_best_cost_s, accepted_for_heap, predecessor_edge` | Original heap relaxation decision |
| `occupancy_revision, announced_prior_vehicles` | Counter state version/read provenance **before** assigning current vehicle |
| `candidate_route, selected_route, guardrail_reason` | Decision summary after search + existing baseline/detour guard |

Implementation guidance:
- Add a *default-off* callback or event writer without changing any cost calculation, sort order, heap tuple, comparator or mutable occupancy state. Evaluate `count = occupancy[(v,b)]` **once** at the exact original read point, then use that same `count` for the unchanged surcharge computation. Save a copy to the sink *after* the model has already computed its value. If optional logging fails, **fail the diagnostic job rather than silently skipping or falling back to a different routing algorithm**.
- Capture **all** edge lookup attempts and heap decisions for the selected smoke vehicle population; batch/gzip output to avoid exhausting memory. If volume is prohibitive, record a deterministic announced subset **before executing any rerun**, label sample scope, and do **not** claim complete search coverage. Do not silently truncate at a row cap.
- Explicitly log assignment counter updates *after* the route is chosen, with event order and pre-/post-count for every updated bin. Route-decision ordering is `(float(depart), vehicle_id)`.
- Keep candidate path costs and all rejected relaxations separate from *actual observed route outcomes*: no vehicle ever drove the unchosen candidates, so no counterfactual realized timing may be inferred.

**Tests:** Fixtures with known counter values, shared edge lookup across two vehicles, time-bin boundary at `29.999...` vs `30.0`, heap tie/stale entries, accepted and rejected relaxation, repeated edges, candidate rejected by detour guard, and the immutable sorted vehicle order.

## 6. Policy/observation invariance and leakage protection

A **mandatory no-observer control** (same original code, same network/demand, same version, same flags except observational output) is compared to the **observer-enabled** run.

- **Planning invariant:** Exactly 1,000 decisions; byte-identical route XML and audit CSV to original `time_aware.py`; original candidate paths and search cost values unchanged; traced lookup count equals actual executed edge-cost read count under instrumented code.
- **Simulation invariant:** Identical per-vehicle planned and actual departure times, arrival times, duration, route, waiting/timeLoss, and 1,000/1,000 completion; record but do not dismiss any mismatch. Observe SUMO warnings/teleport counts.
- **Stream integrity:** For every nonteleported, completed trip, all planned external edge visits matched by ordered index, every available internal edge event accounted for, strictly ordered exit events, explicit null/missing codes, event counts and step resolution recorded. Cross-check against FCD, `tripinfo` and original native edgeData with compatible semantics.
- **No leakage:** Route-search logs are frozen **before** SUMO executes; simulator observations never enter route selection. Future held-out seeds `3101–3110` do not appear in any workflow matrix, input, or filename.
- **Provenance:** SUMO version + pinned digest, commit SHA, original route input and hashes, model parameters, sample/step length, network and OD normalized hashes, run ID, test suite output, timestamps and warnings.

If the observer changes simulation outcomes or the callback changes route selection, **stop and investigate**. Do not report measurements from a noncomparable pair as though they were the same run.

## 7. Targeted execution and deliverables — pending implementation approval

**J0 — Schema/fixture gate (no new simulation):** Implement pure parsers and event fixtures in new versioned files; fail on missing/duplicate events, invalid internal link sequence, inconsistent timestamps, counter read after assignment, and route-index ambiguity. Confirm output volume boundaries.

**J1 — Original-step native exit-time smoke (one old development scenario):** Use seed **2001**, window **200s**, 1-second SUMO and pinned digest. Verify `vehroute.exitTimes` with internal edges really yields the required ordered data and that collecting the data does not change tripinfo. If it does, stop and evaluate read-only TraCI instead.

**J2 — Original search-time lookup trace (same seed):** Add optional logging, run the original routes with/without observation, prove byte-exact policy invariance and evaluate lookups vs chosen-route replay. No model tuning.

**J3 — Targeted G3 discrepancy follow-up:** Replay seed **2103**, 200s, and optional **2101**, 1200s, only after J1–J2 pass; trace the `C6C7` / `veh0213` anchor with timestamps and actual vehicle geometry. Reconcile positive and negative residuals, leaving incomplete cases unresolved.

**J4 — Scientific review:** Publish `G3_EVENT_OBSERVATION_REPORT.md`, per-vehicle `movement-events`, `junction-phases`, `search-lookups.csv.gz`, `invariance-report.json`, `case-boundary-audit.csv` and a machine-readable G3 gate memo. Update the next-study preregistration *proposal* if justified; do not start M3 or publish predictor-accuracy claims.

### Gate conditions

| Gate | Pass requires | On failure |
|---|---|---|
| J0 schema and unit fixtures | Explicitly distinguish simulation-step time, front-edge occupancy, native physical presence, planning counts and missingness; all deterministic fixtures pass | Fix definitions before using output |
| J1 native movement instrumentation | 1,000 completed trips, ordered external exits, interpretable internal records or clearly documented fallback, unchanged per-vehicle baseline outcomes | Block J2/J3 |
| J2 true search-read provenance | All actual occupancy reads logged or sampled scope declared; exact route/cost/audit invariance; complete counter-update order | Reject "exact search-time" claim |
| J3 discrepant case audit | Anchor evidence independently reproduced, remaining unexplained bins and step-time bounds explicitly labeled | Publish unresolved-case ledger, no closure |
| J4 review | Provenance, comparison, limitations and no-leakage controls present; explicit G3 pass/partial/defer with evidence | Keep G3 open |

**Approval request:** Approve J0–J3 *measurement-only implementation and bounded developer-seed replays*, with J4 publication and gate review. **Separate explicit approval remains required** for M3 freeze and any held-out evaluation. A design commit by itself authorizes no simulation.
