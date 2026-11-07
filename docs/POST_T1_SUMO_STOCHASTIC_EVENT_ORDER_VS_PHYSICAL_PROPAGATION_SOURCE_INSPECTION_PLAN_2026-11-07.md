# Cooperative Traffic Research — Post-T1 SUMO stochastic event ordering versus physical traffic propagation

**Plan date:** November 6, 2026 Pacific / November 7, 2026 UTC  
**Status:** APPROVED FOR WRITING AND GITHUB PUBLICATION ONLY. SOURCE INSPECTION NOT YET EXECUTED UNDER THIS DOCUMENT.  
**Method:** Read-only, archive-first audit of the exact SUMO 1.28.0 version and previously completed T1 B*/C* observations. No additional simulations, policy changes, calibration, or forecasting model development.  
**Scope and scientific decision inherited:** Current T1 10-second model/policy **DEVELOPMENT NO-GO**; Experiment 007 Test A and E1-v2 NO-GO remain unchanged. No reserved cohorts are opened.

## 1. Why: return to the fundamental cooperative-traffic question

The project's fundamental question is whether **voluntary collective decisions by human drivers can improve network-wide traffic outcomes compared with equally informed independent decisions without unacceptable harm to participants or nonparticipants**. To answer it, an observed change in unshifted drivers' journeys must be attributable to the traffic intervention under adequately controlled simulator conditions, rather than inadvertently reassigned vehicle characteristics or an unidentified random-number coupling.

In the original development-only T1 comparison (historical B versus C), twelve drivers delayed their preferred departure by 10 seconds. The fixed 10-second nominal-edge forecast predicted a 50.626 network-second collective benefit but SUMO reported 618 network-seconds more cost. That historical comparison was subsequently found confounded: **380 of 1,000 matched IDs were assigned different speedFactor values**, including 368 of the 988 unshifted IDs. The original result remains an authentic descriptive comparison, not a timing-only causal estimate.

A new, prospectively specified development pair **B*/C*** retained the same twelve planned shifts and assigned each ID the same explicit historical-B speedFactor in both arms. The controls and both 1,000-trip completions passed on inspected seed 2101, and the new C* schedule cost **2,131 network-seconds more than B*** (120 intentional waiting, 8 insertion delay, 2,003 in-network). Among the 988 unshifted drivers the difference was +2,177 network-seconds; among 500 nonparticipants it was +294, with 91 nonparticipants experiencing more than 30 seconds additional journey cost. These figures are development-only outcomes, not independent proof that timing coordination causes harm.

The passive full-network traces first show a shifted-vehicle divergence at **t=25s** and differences among unshifted vehicles at **t=27s**, including one on the shifted driver's road and another on a road approximately 914m away from that first shifted vehicle's location. This is a warning about attribution, **not proof that random-number coupling caused the remote difference**. Other changed departures, physical pathways, simulator event timing, floating-point/sample precision, and other RNG consumers must be examined.

**Why this investigation matters:** Before improving a forecast of other drivers' consequences, determine whether the simulation comparisons isolate meaningful timing-mediated traffic interactions. Improving the model before this control question is resolved risks optimizing against an artifact of how the simulator handles randomness or event ordering.

## 2. Exact scientific question and competing explanations

> **In the pinned SUMO version used for T1, can remaining differences in vehicle dynamics and early B*/C* movement be distinguished as (a) intervention-mediated physical traffic propagation, (b) consumption or reassignment of random draws caused by load/update ordering, or (c) other numerical, observational, or implementation differences — sufficiently to make a timing-only causal comparison interpretable?**

The audit must separate **observed facts**, **mechanism hypotheses**, and **unresolved information**.

| Hypothesis | Mechanism under consideration | What would strengthen it | What would weaken it |
|---|---|---|---|
| **H_RNG — shared-stream event-order coupling** | Departure reordering or altered internal event counts change the random values consumed by other vehicle identities or at later updates | Source confirms shared sequential RNG used by active vehicle dynamics or insertion; archival first-difference timing and affected IDs match reachable consumption changes | All relevant random draws are demonstrably ID-local/counterfactually coupled, with no schedule-dependent draw reassignment |
| **H_LOCAL — physical queue/junction propagation** | Earlier or later vehicle insertion changes leaders, gaps, approaches, capacity, service, queues, and downstream travel times | Timestamped shared/adjacent lane interactions precede affected unshifted vehicle changes with a physically plausible path | Distant effects precede any physically reachable interaction under all shifted vehicles and examined paths |
| **H_GLOBAL — deterministic update/insertion ordering** | Differences in load order, insertion queue order, lane iteration or tie breaking change the simulator state even without reassigned RNG values | Pinned source shows behavior-sensitive ordering and evidence supports changed order at the observed first-divergence time | Relevant iteration and tie decisions are invariant or differences appear with a clearly documented physical path |
| **H_NUM — observation/numerical boundary** | FCD sampling resolution, coordinate/rounding differences, step-level evaluation order, or output semantics produce apparent early differences | Differences are near recorded precision, absent in corroborating per-edge timestamps, or occur at a reporting boundary | Substantial persistent position/speed and later edge-exit differences confirm a real simulated-state divergence |
| **H_OTHER — unmeasured vehicle behavior** | Device randomness, car-following sigma, lane-changing, collision resolution or dynamically loaded state remains unmatched despite fixed speedFactor | Source/configuration identifies active per-step stochastic components not controlled per vehicle | Those components are unused or fully paired under the exact T1 inputs |

**Hypotheses can coexist.** A change in stochastic driving after two vehicles physically meet may be a legitimate response to the intervention, not automatically an independent confound. Conversely, a random draw reallocated to an otherwise physically disconnected driver can compromise attribution. The audit must define which randomness is part of the **physical response** and which is unwanted differences in **exogenous conditions**.

### Scientific estimand to clarify before any new experiment

For the existing synthetic simulation, the intended treatment is **only the twelve original C* departure-time changes**, with all other originally specified traveler and network properties held fixed. The desired counterfactual holds fixed *exogenous* driver characteristics and, wherever meaningful, exogenous random innovations while permitting road interactions (queues, insertion feasibility, lane changes induced by traffic, and physically consequent reactions) to change.

A fixed global numerical seed is not itself proof of that coupling; nor is complete elimination of stochastic car following desirable. **This plan does not prespecify a new random-control method before the source audit establishes one.**

## 3. Immutable evidence and source provenance

### Project records

1. [Completed T1 ID-locked B*/C* final scientific report](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md) — exact measured effects, fairness, first observed differences and limitations.
2. [Prospective identity-locked B*/C* design](POST_T1_ID_LOCKED_VEHICLE_ATTRIBUTES_CONTROLLED_TIMING_RETEST_PLAN_2026-11-06.md) and [original speed-factor confound finding](POST_T1_EXPERIMENTAL_CONFOUND_ARCHIVE_DIAGNOSTIC_AND_STOP_2026-11-06.md).
3. [Permanent raw evidence release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/t1-idlocked-dev2101-2026-11-07): original B/C source, new B*/C* inputs, canonical per-driver manifest, two SUMO tripinfo/statistics/collision files, full passive FCD, per-edge vehroute timings and derived diagnostic JSON. Archive: `t1-idlocked-dev2101-complete-evidence.tar.gz`, recorded SHA256 `c3541593131930101ba7237bf2460765c385de5dafa5eab07a986ef1178a396a`; verify SHA256 per-member manifest before interpreting files.
4. [Completed two-arm execution](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42348701379) and [successful **preservation-only**, no-SUMO execution](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42348947234). Original execution's overall failure was **only** the post-study GitHub CLI release step; all scientific control/analysis gates passed.
5. [Pinned study implementation snapshot](https://github.com/yonnastgetahun/cooperative_traffic_research/tree/f943db3d2e9decd14ed17f8b374fbb3c4f9b4429/research/t1_timing) and [original Experiment 007 SUMO caller](../experiments/experiment_007/run_v01.py): inspect **actual committed invocation** and output options rather than guessing scenario defaults. Source code on a later branch or a newer GitHub release must not silently substitute for code that was run.

### Exact SUMO engine

- Executed engine: **SUMO 1.28.0**, pinned image `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`.
- **First source-integrity task:** identify the exact 1.28.0 source tag/commit and build configuration corresponding to that binary, and record a reproducible citation (tag, git SHA, source path, line ranges, build flags where available). A public SUMO `main` branch or documentation updated after the release is **context, not proof** of the compiled code's behavior.
- SUMO's [randomness documentation](https://sumo.dlr.de/docs/Simulation/Randomness.html) describes separate generators for vehicle loading, probabilistic flows, driving dynamics, and vehicle devices, and stochastic behavior in the default Krauss car-following model through `sigma`. The [vehicle insertion documentation](https://sumo.dlr.de/docs/Simulation/VehicleInsertion.html) describes insertion constraints, queueing and departure delay. These are **starting hypotheses**; trace the precise code paths and configuration active in **1.28.0**.
- Track the actual code referenced by SUMO 1.28.0 for (names are search starting points, **not already verified active modules**): `RandHelper` and RNG ownership/seeding, `MSVehicle` / `MSBaseVehicle`, `MSVehicleControl`, `MSVehicleType`, `MSInsertionControl`, `MSLane`, `MSLaneChanger`, `MSNet`, and selected car-following model classes. Do not assume every listed file is a runtime participant.

### Research limitations already fixed

- Exactly **one** previously inspected development-seed comparison; the 1,000 drivers, multiple FCD frames and per-edge events are **not independent replications**.
- No independent T1 policy qualification, no held-out forecasts, no demonstrated real-world cooperation or human acceptance.
- Original T1, Experiment 007 Test A, and E1-v2 negative decisions remain unchanged; never open reserved **6201–6212**, **6301–6312**, or an unseen T1 confirmatory cohort.

## 4. Archive-first and source-inspection sequence — ZERO new SUMO

### R0 — Recover, fingerprint and freeze the observational basis

**Inputs:** permanent release and original provenance above, all original/new B/C and B*/C* route and tripinfo files, FCD, vehroute edge-exit, command/options and canonical per-driver manifest.

Read-only verification:
- Verify release and per-member SHA256 digests, source revision, pinned container, generated B*/C* routes, matching 1,000 IDs, 12 exact shifts, identical per-ID speedFactor and fixed route sequences.
- Reconfirm the accounting anchors (new **+2,131 = +120 +8 +2,003**; +2,177 among unshifted; +294 among nonparticipants), but **do not rerun or expand statistical tests already completed**.
- Identify the precise executed vType defaults, departLane/departPos/departSpeed, `sigma`, lane-changing and stochastic-device settings, step length, simulation threads, route loading steps, seed/random flags, and any explicit/implicit RNG choices. Mark unrecorded fields as **unverified**, not absent.

**Output:** small source/evidence ledger (name, original checksum, engine/source location, relevant values, known vs unknown).  
**Stop:** If essential original source or executable identity cannot be verified, mark `SOURCE_PROVENANCE_INCOMPLETE`; do not claim specific runtime RNG behavior.

### R1 — Trace random-number consumption and update order in pinned source

Study **only** the active execution pathway, not every SUMO component. Answer these questions directly:

1. **RNG inventory:** Exactly how many or what categories of PRNG streams exist in this build? Which stream is used for vehicle-type/speed loading, stochastic car following, lane-changing (if any), random insertion/position, devices and any scheduled-event tie breaking? Identify the initialization seed and ownership (global, subsystem, vehicle-local, or hash-derived), and whether each stream is advanced per loaded vehicle, per simulation step, per physical event or per call site.
2. **Load / insertion ordering:** Does sorting by requested departure alter vehicle construction order, ID/numerical indices, queue placement, iteration order, insertion retries or RNG-consumption sequence? Can changed departure order alter another driver's random numbers before any feasible traffic interaction?
3. **Driving dynamics:** Identify the actual car-following/lane-changing models and whether their random draws are shared, per-vehicle, or per-event, with active default parameters and step-level ordering. Do not infer activation merely because a feature exists in source.
4. **Other possible remote coupling:** Inspect global update ordering, route-loading batches, multithread settings, tie-breaking, shared state or device initialization that could connect otherwise separated vehicles at the observed early times. Distinguish **source-proven** data flow from speculation.
5. **Counterfactual pairing:** Does the code already supply a documented ID-keyed RNG or independently reproducible per-driver stochastic stream that survives rescheduling? What remains order-sensitive? If no robust pairing is possible **without changing physical driving rules**, record that fact. **Do not implement a replacement RNG, set sigma=0, or modify SUMO.**

**Output:** one compact table, per active code path: random/no random; source commit/path/line; input or event that advances it; scope of shared state; possible B*/C* coupling; evidentiary confidence.  
**Stopping condition:** The audit is enough when every **material** plausible RNG/ordering pathway has a grounded status (`ACTIVE_AND_ORDER_SENSITIVE`, `ACTIVE_BUT_ID_LOCAL`, `INACTIVE`, or `UNRESOLVED`). Do not expand into an unlimited SUMO code review.

### R2 — Confront source hypotheses with **existing** vehicle traces

Using the already released B*/C* FCD/vehroute/manifest (no new simulation or modified policy):

- Establish an ordered list of **all twelve** scheduled changes, not just first shifted vehicle `veh0113`. Determine which vehicles had actually entered or been omitted at each observed divergence.
- Independently reconfirm t=25 first recorded shifted-vehicle difference and t=27 earliest unshifted changes. Check every early event's reported lane, position, speed and step; distinguish ≤0.02m/0.02m/s descriptive comparison tolerance from measured differences at saved precision.
- Investigate **both** first unshifted examples (`veh0111` on `C2D2_0` and `veh0022` on `F6F5_0`): were they in a physically connected shared edge, adjacent approach, related insertion batch, or wholly separate local states **at the relevant time**? The reported ~914m separation concerns the **first shifted driver only** and straight-line distance; do not use it as a physical reachability proof for all twelve changes.
- Trace available timing from source insertion through actual upstream and downstream edge exits in the original saved data; characterize the **earliest observed** divergence and the uncertainty of a one-second FCD sample. Identify earliest **unshifted actual departure** changes separately from in-network movement.
- Compare the observed timeline against the pinned source's actual RNG-call and insertion/update schedule. Classify explanations as **consistent**, **in tension**, **ruled out by available observations**, or **not distinguishable**; require evidence for every category.
- Test the negative-control boundary: no archived unshifted FCD discrepancy was observed before the earliest affected B* requested departure. This does **not** by itself establish causality or rule out later global RNG coupling.
- Preserve participant/nonparticipant harm and helped-driver distributions without attributing a driver-specific gain/loss to one shifted vehicle. Keep network aggregate, recorded stopped time and physical throughput distinct from any forecast.

**Output:** concise earliest-event chronology and hypothesis-evidence matrix; links to stored traces/IDs/time ranges. Do not invent unrecorded RNG states, substep trajectories, exact priority decisions, or individual-route causal contributions.

### R3 — Separate three scientifically different kinds of uncertainty

**(A) Exogenous random-state mismatch:** Can a driver who has no physical connection to the changed departure receive a different input-like random innovation only because the event/draw sequence changed? A matching simulation seed alone does not rule this out.

**(B) Endogenous stochastic traffic response:** Once the intervention physically changes a vehicle's leaders, conflicts, lane choices or queue, legitimate driving randomness may diverge. Eliminating it would alter the phenomenon under study and could produce a misleadingly deterministic answer.

**(C) Deterministic network propagation / numerical event ordering:** Even with identical random streams, a small schedule perturbation may alter a congested network's traffic trajectory nonlinearly, especially at insertion and junction-service thresholds. Network-wide divergence alone is not proof of a random-number defect.

Report whether (A), (B), or (C) is **supported, contradicted, or unresolved**, and whether a clean causal timing-only *estimand* is operationally identifiable with the existing simulator. Explicitly differentiate a **reproducible same-seed total simulator contrast** from a **well-paired intervention effect under controlled exogenous randomness**; these are not interchangeable.

### R4 — Stop/continue scientific decision (no experiment automatically launched)

| Source-and-archive outcome | Decision |
|---|---|
| Exact pinned source unverified, necessary logs absent or actual RNG ownership cannot be determined | **EVIDENCE_INCOMPLETE**. Preserve limitations; no causal label, estimator, or extra simulations. |
| Material order-sensitive exogenous RNG assignment is established but a source-supported, non-physics-changing pairing/control is possible | **CONTROL_CANDIDATE_IDENTIFIED**. Document *one* falsifiable prospective test of that control; separately seek authorization. |
| No material exogenous RNG coupling is active, with a plausible physical/insertion chronology consistent with traces | **PHYSICAL_PROPAGATION_PLAUSIBLE**, **not uniquely causal**. One separately approved discriminating control may be warranted, not a forecast rewrite. |
| Both source-side RNG coupling and physical propagation remain plausible, or archive cannot discriminate | **MECHANISM_UNRESOLVED / STOP T1 PROXY**. Do not build a new estimator or run speculative parameter sweeps; consider an alternate coordination mechanism. |
| Active RNG cannot be paired without disabling realistic behavior or changing the intervention definition | **NO CLEAN T1 COMPARISON UNDER CURRENT DESIGN**. Recommend suspending this path or specifying a distinct scientific estimand and prospective design for later review. |

**Important:** Even a persuasive source-based RNG explanation would not numerically partition the observed +2,131 network-seconds between RNG and traffic physics, identify one causal bottleneck, validate the failed forecast, or establish cooperative timing efficacy. Do not use this audit to retroactively change original experiments.

## 5. One future experiment — conditional and not authorized

**The default next step is no new experiment.** A later investigation becomes justified only if R0–R4 expose exactly one critical unresolved mechanism with a feasible, **minimal** discriminating comparison whose controls and predictions can be frozen *before* execution.

Any future proposal would need to explicitly define:
- The causal estimand, exact vehicle-ID/exogenous-randomness pairing and what stochastic physical behavior is intentionally preserved;
- One testable contrast and negative control that distinguishes predicted random-number coupling from physically reachable propagation;
- Original routes/schedules, network, SUMO version, allowed inspected development conditions, command/input diff, independent source of truth and immutable evidence hashes;
- A **bounded** run budget and hard invalid-input/invalid-output stopping gates. No code, new seeds, reserved cohorts or SUMO run are included in this plan;
- Expected learning and distinct possible decisions, including **STOP** when no mechanism can be separated;
- The same all-driver preferred-departure-to-arrival objective, matched harms, and participant/nonparticipant fairness, not solely the simulator's in-network mean time.

A future engine comparison (CityFlow, MATSim, Aimsun, Vissim) is a separate transport-model generalizability question, **not** a substitute for identifying the existing SUMO counterfactual.

## 6. Reporting, publication and scientific safeguards

Publish **one consolidated source-inspection and archive-diagnostic scientific report** to the GitHub research system of record after a separately authorized analysis, with:
1. Exact SUMO 1.28.0 source provenance and actual build/options; links to cited source lines.
2. A finite RNG/ordering call-path ledger and classification of which components were active.
3. Archival early-event chronology and spatial-temporal reachability qualifications, including all 12 shifts.
4. Explicit distinctions between exogenous mismatches, endogenous stochastic responses and deterministic physical propagation.
5. Clear supported/contradicted/unresolved findings, original study/fairness status, and one **STOP / CONDITIONAL NEW CONTROL TEST / ALTERNATIVE MECHANISM** decision.

Avoid incremental PR proliferation, repeated numerical re-audits and development to justify development. **No SUMO simulation, new predictor, policy adjustment, seed access, retuning, source-code modification, or social media publication is authorized by publication of this plan.** The source-inspection itself is an investigation to be executed deliberately and recorded, not something already established by this document.

**Why this gets us closer to the founding question:** The goal is not just to see that changing twelve departures correlates with widespread journey changes. It is to know whether those changes represent **predictable consequences of collective road use** that a fair voluntary decision-maker could act on, rather than artifacts of simulator bookkeeping. If they are not distinguishable, preserving a NO-GO and changing scientific direction is the appropriate research result.

**This plan ends at the decision gate; it does not manufacture another experiment.**
