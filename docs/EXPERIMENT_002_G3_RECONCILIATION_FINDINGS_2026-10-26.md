# Experiment 002 — G3 Occupancy and Junction Reconciliation: Evidence & Decision Memo

**Research date:** October 26, 2026 (Pacific time)  
**Status:** **G3 diagnostic execution complete through two evidence passes; G3 NOT closed; M3 held-out freeze NOT authorized.**  
**Approved protocol:** [G3 Measurement Reconciliation v0.1](EXPERIMENT_002_G3_MEASUREMENT_RECONCILIATION_PROTOCOL_V0_1.md)  
**Original M2 evidence:** [nine calibration scenarios](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958) (seeds 2101–2103 × 200/600/1200-second windows)  
**Offline analysis runs:** [G3 measurement-bins and junction-bounds audit](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40448102464) · [G3-C vehicle-level boundary case audit](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40448538736)  
**Durable outputs:** [all G3 evidence files, including complete CSV ledgers](results/exp002_g3_2026_10_26/README.md).

## Executive finding

A major part of the previously “unexplained” difference between native SUMO `edgeData.sampledSeconds` and FCD snapshot-based road counts appears to be **measurement semantics**, not necessarily an error in SUMO or its congestion model.

SUMO's native edge measurements incorporate fractional vehicle time on roads; a vehicle can also overlap multiple edges. SUMO FCD snapshots report the vehicle's **front position on its current lane**. These are **not identical estimands** and must not be treated as if they were. SUMO documentation explicitly notes partial vehicle edge presence, and a SUMO project discussion describes different handling of vehicles overlapping edge boundaries. See [official SUMO edge measures](https://eclipse.dev/sumo/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html), [FCD fields](https://sumo.dlr.de/docs/Simulation/Output/FCDOutput.html), and [SUMO issue 16241 discussion](https://github.com/eclipse-sumo/sumo/issues/16241).

**This interpretation is strongly supported, not fully established by a per-vehicle reconstruction of the native SUMO accumulator.**

## G3-A — Native/FCD discrepancy, measured on occupied roads

Nine original datasets were downloaded and processed offline with no SUMO reruns, routing changes or new seeds. The audit verified **9,000 completed trips**, exact instrumented/original route and audit equivalence, all expected edge rows in external/native output, and one common immutable SUMO image digest.

Full-bin external roads with **native sampledSeconds at least 30 vehicle-seconds** were analyzed separately so zero-volume roads could not dilute the statistics:

| Departure window | Busy edge/time bins (3 seeds pooled) | Sum absolute FCD–native difference / total native vehicle-seconds | Largest absolute bin discrepancy |
|---|---:|---:|---:|
| High / 200s | 6,700 | 4.5% | 30.0 vehicle-seconds |
| Moderate / 600s | 4,844 | 4.9% | 30.0 vehicle-seconds |
| Low / 1,200s | 2,290 | 4.4% | 30.0 vehicle-seconds |

These differences should not be called **native occupancy prediction errors**. They compare different measurement semantics. The full stratified ledger includes empty roads, occupied roads, busy roads, and bins where native SUMO records positive presence but FCD front samples show none. Final partial SUMO intervals without compatible FCD bins were **counted as incomparable**, not silently replaced with zero.

[All nine seed/window strata](results/exp002_g3_2026_10_26/g3-occupancy-strata.csv) · [Ranked external-edge discrepancies](results/exp002_g3_2026_10_26/g3-top-edge-bin-outliers.csv).

## G3-C — Vehicle-level evidence of cross-edge occupancy

To check the preselected worst road-bin discrepancies, a second offline audit scanned the **original one-second FCD records** for vehicle fronts on downstream internal junction lanes, tracking each vehicle's last observed external edge. It used a **5-meter front-position window** as an explicit heuristic, **not** a measured vehicle-length or exact rear-position model.

Among **211 distinct negative-difference bins** (union of top-20 all-external and top-20 busy-bin rankings per seed/window):

- All **211/211** had at least one FCD sample of a vehicle front near the start of an internal junction lane immediately after the discrepant external road.
- In **140/211**, the count of such near-boundary samples differed from the native-minus-FCD road-count deficit by **no more than one vehicle-second**.
- In **210/211**, it differed by **no more than three vehicle-seconds**.

**Illustrative case — seed 2103, high congestion, edge `C6C7`, simulation time [60,90):** Native SUMO measured **30 vehicle-seconds** on `C6C7`; FCD snapshots placed **zero fronts** on that road during the bin. Vehicle `veh0213` had previously traversed `C6C7`, and all **30 sampled seconds** showed its front almost stationary on internal junction lane `:C7_11_0`, about **1.34 meters** into that lane. This is highly consistent with the vehicle physically overlapping the upstream edge even though its **front** was no longer on `C6C7`.

**Caution:** These are a *selected*, nonrandom set of extreme negative differences; the 211/211 proportion cannot be extrapolated to all road bins. Sampling, native edge interpolation, vehicle length, lane position, subsecond transitions, and other edge interactions may also contribute. The 5-meter heuristic is not a calibrated physical model. We have not proven exact native per-vehicle sampledSeconds equivalence.

[Complete 211-case event-level ledger](results/exp002_g3_2026_10_26/g3-cross-edge-ledger.csv) · [machine-readable case summary](results/exp002_g3_2026_10_26/g3-cross-edge-summary.json).

## G3-B — Junction visibility and interval uncertainty

Across the nine datasets, **66,853 external-road transitions contained internal-lane FCD samples; 317 did not**. Conservatively translating the 1-second snapshots into total *internal-link presence* yields aggregate **sample-based bounds of approximately 51,116–185,139 seconds**. These bounds are not a measurement of intersection-*caused* delay.

External approach waiting is recorded separately. The earlier `unresolved_transition_seconds=0` meant that observed one-second samples were assigned to external/internal categories, **not** that true transition boundaries were known exactly.

[Per-seed junction bounds and coverage](results/exp002_g3_2026_10_26/g3-junction-uncertainty.csv).

## Proposed measurement-contract correction (NOT YET FROZEN)

For later predictor validation, propose separating observations into three explicitly non-interchangeable sources:

1. **Primary observed road load/occupancy:** Native SUMO external edge/lane `sampledSeconds` and native occupancy %, with correct denominator, step semantics and partial interval handling. Do not force this to equal the number of FCD vehicle fronts.
2. **Vehicle trajectory/entry events and junction state:** FCD front-position and lane samples, with one-second sampling uncertainty and route-index-based matching. Attribute downstream-junction occupancy and external approach stopping separately; retain unobserved phase bounds.
3. **Predictor's internal planning input:** Prior route-assignment counts indexed by edge and planning bin, on the *original model's own units*. These are neither native road occupancy nor FCD front counts. Chosen-route replay must remain distinguished from a complete original search-time lookup event log.

Before claiming physical occupancy calibration, explicitly define a comparison that maps predictors and SUMO outcomes to **the same target units, time support, and population**. Improved road-entry timing along chosen routes remains distinct from network-wide routing benefit.

## Gate status after the two offline passes

| Gate | Status | Why |
|---|---|---|
| G3-0 source integrity | **PASS** | Nine development source packages, policy invariance, native-source consistency, immutable SUMO version/digest, no held-out access |
| G3-1 occupancy semantic reconciliation | **PARTIAL — strong candidate explanation** | All selected negative outliers show near-boundary junction-front evidence; exact native per-vehicle attribution and positive residual cases remain unverified |
| G3-2 junction timing | **PARTIAL** | Sampling bounds and missing-junction coverage quantified; true phase transitions and causal junction delay not fully identifiable |
| G3-3 exact original search-time occupancy inputs | **OPEN** | Current trace replays chosen path with preassignment counts; not every explored Dijkstra lookup has been logged |
| G3-4 freeze readiness | **NOT READY** | Proposed contract changes are not reviewed/frozen; unresolved mechanisms and lookup provenance remain |

**No arbitrary MAE success cutoff was added after inspecting the data. No predictor validation or cooperative-routing benefit has been established.**

## Next research decision

**Recommend targeted G3 follow-up, not M3 held-out evaluation:**

- **R1:** Adopt or revise the proposed observation definitions; version the measurement code. Verify edge-native `sampledSeconds` semantics with direct examples and quantify remaining difference after reconciling boundary vehicle extent; explicitly account for other-sign residuals and fractional edge transitions.
- **R2:** Preserve internal versus external samples and one-second interval bounds; if necessary, capture exact simulation event times on an **existing development seed** in an isolated observation-only diagnostic (no algorithm changes).
- **R3:** Either implement a non-policy-changing **search-time occupancy lookup recorder** (including unchosen search expansions) with byte-identical route/audit proof, or narrow the predictor-validation claim explicitly to chosen-route replay.
- **R4:** Write an M3 preregistration and freeze proposal *only after* R1–R3 have been assessed. Separate approval is required before any use of reserved seeds **3101–3110**.

**Conclusion:** Our discrepancy has a concrete, independently documented *candidate mechanism*. This is meaningful progress toward a correct measurement contract, but not permission to declare G3 closed.
