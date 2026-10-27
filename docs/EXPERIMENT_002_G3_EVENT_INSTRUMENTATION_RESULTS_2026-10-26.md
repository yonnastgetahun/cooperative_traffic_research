# Experiment 002 — G3 J0–J3 Targeted Event Instrumentation: Results & Gate Review

**Research date:** October 26, 2026 (Pacific)  
**Status:** **J0–J3 execution completed successfully. G3 overall PARTIAL/OPEN; M3 freeze NOT approved and untouched evaluation seeds remain reserved.**  
**Approved design:** [G3 Targeted Event Instrumentation v0.1](EXPERIMENT_002_G3_EVENT_INSTRUMENTATION_DESIGN_V0_1.md)  
**Evidence archive:** [Durable J1/J2/J3 reports, integrity checks, hashes and workflow links](results/exp002_g3_events_2026_10_26/README.md)  
**Original earlier G3 findings:** [G3 native/FCD reconciliation](EXPERIMENT_002_G3_RECONCILIATION_FINDINGS_2026-10-26.md)

## Executive finding

Two important ambiguities in our predictor diagnostics are now substantially reduced. First, **SUMO provides ordered, simulation-step-resolution vehicle exit-time records for external roads and internal junction links** without changing the traffic outcomes in the tested replay. Second, a default-off event sink inside the **original time-aware routing algorithm** captured every `occupancy[(edge,time_bin)]` read evaluated by its search, not merely costs reconstructed after selecting a route. An independent audit replayed the sequence of reads and assignment updates successfully.

Neither instrument is a calibrated real-world traffic predictor. Occupancy during route search remains a **prior assignment count**, not observed vehicles or road occupancy percentage; internal-link elapsed time is **not necessarily caused by the junction**. Both diagnostic replays use previously inspected development seeds and no held-out outcomes.

## J0 — Event schema and deterministic fixtures: PASSED

- Built native `vehroute-output.exit-times` and internal-edge parser with tests for repeated external roads, interleaved internal links, monotonic times, missing exit times, and equal-step timestamps.
- Added strict per-vehicle tripinfo control, comparing depart/arrival/duration/waiting/timeLoss/departDelay fields where present.
- Added independent actual search-event audit and fixtures for edge counter read values, time-bin boundaries, heap relaxations, and route-policy invariance.
- The default search event sink is **off** unless explicitly enabled in a diagnostic. The routing optimization equations, penalty values, detour rules, route ordering and SUMO demand remain unchanged.

The GitHub Actions J1 and J2 fixture jobs passed. A passing fixture does not prove correctness on arbitrary networks; real-data invariance and coverage were checked separately.

## J1 — Native SUMO step-resolved exit times: PASSED for development seed 2001

[Successful GitHub run 40452285124](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40452285124)

Using the previously inspected **200-second high-load scenario, seed 2001**, pinned to SUMO **1.28.0** with immutable image digest `sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`:

- **1,000/1,000 vehicle trip records parsed**.
- **16,705 total native ordered movement records**, including **8,338 internal-junction edge records** and **8,367 external-road records**.
- Native external route edge sequences matched all 1,000 archived planned routes.
- No departure/arrival-time mismatches, missing vehicles, nonmonotone event errors or route-count inconsistencies.
- The new SUMO run's per-vehicle tripinfo fields matched the previously archived simulation for every vehicle.

**Timing interpretation:** `vehroute.exitTimes` marks simulated road/internal-link exit times at the solver's **original one-second simulation-step resolution**. Inferred enter times based on a preceding edge's exit are not independently measured continuous crossings. This does not establish subsecond physical precision.

## J2 — Actual original search-time occupancy reads: PASSED for seed 2001

[Successful GitHub run 40452726452](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40452726452)

The original `time_aware.search` logic was equipped with a **default-off** event sink that records the actual counter value **at the moment of each evaluation**, including routes never ultimately selected. The diagnostic also records heap pops, candidate edges, bin indices, free-flow cost, congestion surcharge, junction proxy, original relaxation decisions, guardrail choices, and subsequent occupancy updates.

| Measurement | Events in verified 200-second development run |
|---|---:|
| Completed route-search decisions | **1,000** |
| Actual edge-cost/assignment-count lookups | **677,507** |
| Heap-pop events | **182,618** |
| Chosen-route occupancy-counter updates | **8,367** |
| Distinct edge-time-bin counter keys used after assignment | **3,188** |
| Independent search event integrity errors | **0** |

The independent event auditor reconstructed every encountered counter value from earlier assignment-update events and verified the cost identity, revision order and relaxation acceptance. Original policy **with the sink disabled**, original policy **with the sink enabled**, and the **previously archived original output** produced **byte-identical route XML and audit CSV**. This substantially resolves the previously open search-time-lookup provenance issue for the tested run.

**No claim is made that the assignment counter estimates actual queue length or instantaneous occupied vehicles.** The output is a reproducible description of the existing search behavior and includes both chosen and unchosen candidate evaluations, **not** realized outcomes of unchosen routes.

## J3 — Preselected C6C7 cross-edge case: PASSED for seed 2103/high congestion

[Successful GitHub run 40453154885](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40453154885)

The target was selected **before replay** from the original G3 discrepancy ledger: vehicle `veh0213`, external road `C6C7`, high congestion (200-second departure window), seed `2103`, the interval `[60,90)`. The new native event stream and actual search event stream were generated with the original demand, network and pinned SUMO image.

- All **1,000 vehicles** completed and the original per-vehicle departure, arrival and travel outcomes matched. Route XML/audit again remained byte-identical with/without search observation and against the archived route assignment.
- The actual search-time event auditor independently passed: **678,828 lookup events** and **8,458 assignment updates** with consistent counter revisions.
- Native SUMO shows `veh0213` leaving external edge `C6C7` at simulation time **57.0 seconds**.
- It subsequently traversed internal links `:C7_11` and `:C7_19`, exiting those internal links at **98.0 and 99.0 seconds** respectively: **42 simulated seconds of internal-link residence**, from the external road exit to the final internal-link exit.
- Throughout `[60,90)`, the archived 1-second FCD record places the vehicle's **front on internal lane `:C7_11_0` for all 30 seconds**, essentially stationary at approximately **1.34 meters** into the lane (30/30 samples below 0.1 m/s).
- Simultaneously, native SUMO external `edgeData` reports **30 vehicle-seconds** on upstream road `C6C7` during that bin, while FCD reports **0 vehicle-front samples** there.

**Interpretation:** This is compelling, reproducible case-level support for **front-lane position versus physical vehicle-extent accounting across an edge boundary**. It is not proof that this particular vehicle contributed exactly 30 native road-seconds; native `sampledSeconds` remains aggregated rather than attributed to individual vehicle bodies. It also does **not** mean the full 42 seconds was delay *caused* by intersection design or traffic lights: the vehicle might be blocked while physically on internal lanes.

[Durable C6C7 native event and FCD case JSON](results/exp002_g3_events_2026_10_26/j3-c6c7-anchor-observation.json).

## J4 — Scientific decision gates after J0–J3

| Gate | Current status | Evidence/remaining issue |
|---|---|---|
| J0 fixture validation | **PASS** | Synthetic event/lookup cases plus strict error handling |
| J1 native event collection | **PASS on selected development replay** | Native internal-edge exit events, full route match, unchanged tripinfo |
| J2 actual search-time lookup provenance | **PASS on selected development replay** | 677,507 exact reads + 8,367 counter updates, zero independent auditor errors, byte-identical routes |
| J3 selected negative-occupancy case | **PASS for reproducing and timing the anchor** | Native step events align with FCD and original 30-second discrepancy |
| G3-1 native/FCD physical-extent accounting | **PARTIAL** | Strong case-level evidence, but exact per-vehicle native vehicle-body attribution, other-sign residuals and all occupied-bin behavior remain unverified |
| G3-2 junction-phase measurement | **PARTIAL** | Native internal-link residence measured at solver-step resolution; true causal junction delay and continuous crossing time remain unidentifiable |
| G3-3 live search input provenance | **PASS for two inspected development seeds (2001, 2103)** | Live search capture vs independent counter replay; other regimes not exhaustively tested |
| G3-4 readiness to freeze M3 protocol | **NOT READY** | Measurement definitions, residual limits and target units need a reviewed protocol freeze |

No predictor-accuracy threshold was retroactively chosen, and no routing efficacy or physical safety improvement is established.

**Follow-on observation sufficiency review (October 26):** [G3 Sufficiency Review and Pre-Freeze Decision](EXPERIMENT_002_G3_OBSERVATION_SUFFICIENCY_REVIEW_2026-10-26.md) and [14-item Limitations Register](EXPERIMENT_002_G3_MEASUREMENT_LIMITATIONS_REGISTER_2026-10-26.csv) conclude that native SUMO movement events are appropriate for step-level chosen-route timing, and native edge data are appropriate for simulated aggregate road presence, but these are not the same estimand as the planner's route-assignment counter. Native-entry joins and search-input provenance need moderate/low regime verification before proposing a freeze. **This is a review, not a freeze or held-out authorization.**

## Recommended next narrow decision

1. **Observation contract:** Treat native SUMO road `sampledSeconds` / occupancy and trajectory-front FCD as **different targets**. Use the native aggregate for physical-road presence, and native `vehroute.exitTimes` for step-resolved ordered movement. Do not directly subtract search assignment counts from native road occupancy percentages.
2. **Measurement resolution:** Decide whether one-second, native step-level junction residence is sufficient for the predictor-validation question. If yes, keep the original SUMO step; no TraCI or 0.1-second new-dynamics experiment is needed solely to sharpen timestamps.
3. **Remaining semantic reconciliation:** If needed for an accuracy claim, instrument body-overlap geometry or compare native `sampledSeconds` against a like-for-like reconstructed vehicle-body presence integral. Do not simply force FCD front-counts to match it.
4. **Research boundary:** Keep `3101–3110` untouched. **Request separate approval for a carefully specified M3 preregistration/freeze only when these definitions and residual limitations are judged sufficient.** M3 held-out simulations are not authorized.

## Reproducibility and evidence

All source artifacts are development-only and include pinned image, source Git SHA, route hashes and observations. The complete compressed search-event streams are retained by GitHub Actions for a limited time; versioned workflows enable regeneration after expiry. Small integrity and event summaries are preserved in the [durable event evidence archive](results/exp002_g3_events_2026_10_26/README.md).

- [Original M2 development matrix](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958)
- [J1 native movement events run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40452285124)
- [J2 original search-time read verification](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40452726452)
- [J3 high-load targeted case replay](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40453154885)
- [Compact archived summaries and input hashes](results/exp002_g3_events_2026_10_26/README.md)

**Bottom line:** The ambiguous 1-second FCD-only junction timing can be improved using **native simulator exit events**, and actual search-time counter reads are now observed directly rather than inferred. This substantially narrows G3's open questions, but does not eliminate all measurement-definition differences or justify held-out predictor evaluation.
