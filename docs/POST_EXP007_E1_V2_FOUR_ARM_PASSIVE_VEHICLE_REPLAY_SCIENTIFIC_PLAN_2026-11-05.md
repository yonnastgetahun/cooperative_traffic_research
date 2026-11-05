# E1-v2 — Four-Arm Passive Vehicle-Level Replay: Next Scientific Milestone

## Why this milestone matters to our overall research

**Our research asks whether voluntary coordination among drivers can lower total network travel time compared with equally informed independent, traffic-aware routing, while protecting participants and nonparticipants from unreasonable harm.** A cooperative decision rule must understand more than one driver's shortest path: it must anticipate how changing that driver's route affects everyone else's travel time (**network externality**).

Experiment 007's original marginal-externality estimator failed Test A. Subsequent E1-v1 and E1-v2 queue/junction-aware development models also failed qualification. The completed [E1-v2 F0–F5 archive-only investigation](POST_EXP007_E1_V2_F0_F5_ARCHIVAL_MECHANISM_FINAL_REPORT_2026-11-05.md) measured large, sometimes nonadditive effects on other drivers, but five-second **aggregate** road data could not show which individual vehicles reached a junction at what time, where queues physically formed, or how turns were served.

**This milestone addresses the missing observational link: route choice → actual vehicle-entry and junction timing → queues/discharge → realized effects on other drivers.** It may identify a falsifiable limitation to guide a future externality estimator or suggest that a different coordination mechanism is preferable. It **cannot** demonstrate that cooperative routing works, rehabilitate E1-v2, or replace the independent policy-efficacy Test B.

The distinctive scientific contribution sought is a source-verifiable, vehicle-level *explanation of contrasting, already-observed route perturbations*, not another round of model tuning.

**Research date:** November 5, 2026  
**Status:** PROSPECTIVE EXPLANATORY STUDY **PLAN ONLY**; not an execution authorization, not a frozen runtime protocol, and not a completed result.  
**Scope:** Four passive, matched replays of original E1-v2 development arms. No route changes, no model revisions, no new seeds, and no social publishing under this plan.  
**Standing negative verdict:** E1-v2 D1 **DEVELOPMENT_NOT_QUALIFIED**; independent validation **NOT_STARTED**; cooperative policy Test B **NOT_RUN**.

## 1. What we already know

The completed [E1-v2 D1 final scientific audit](POST_EXP007_E1_V2_D1_FINAL_DEVELOPMENT_AUDIT_2026-11-04.md) verified 60 frozen SUMO arms, 60,000 matched trip records and ten predictions-before-label locks. On four development-check seeds, E1-v2 externality MAE was **1,478.5625 network-seconds**, slightly worse than zero-externality B0 (**1,478.0625**), and correct direction was **5/16 = 31.25%** against the required 60%.

The [F0–F5 follow-up](POST_EXP007_E1_V2_F0_F5_ARCHIVAL_MECHANISM_FINAL_REPORT_2026-11-05.md) verified 695 original source files and inspected 50 interventions, 2,133,360 paired five-second external-edge/time observations, 5,000 junction-summary rows and ten two-route bundles. E1-v2 predicted *zero* total bundle interaction in all ten cases; realized joint-minus-single effects ranged **−1,306 to +3,288 network-seconds**. The aggregate detector observations were not sufficient for uniquely assigning causal responsibility to queue propagation, dynamic junction discharge or another physical mechanism.

Two preidentified contrasting single-route cases are especially informative:

| Already-inspected case | Changed driver's ID | Observed effect on **other** drivers | Whole-network effect | Source insertion contribution | In-network duration contribution |
|---|---|---:|---:|---:|---:|
| Seed 6112, probe2 | veh0142 | **+3,215 network-s** (harm) | +3,219 | +2 | +3,217 |
| Seed 6113, probe2 | veh0038 | **−3,960 network-s** (benefit) | −3,883 | −22 | −3,861 |

These numbers were measured before this new plan. They suggest that the *majority of the selected whole-network effects* occurs during simulation rather than before insertion, but do not explain the physical reason. The cases were **chosen after inspecting their outcomes**; they are not new independent model-validation samples.

**Source of original data:** [GitHub Actions run 41966516110](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41966516110), execution commit **a54b6f650b16a22b0eb5543bb507f9faf5eea034**, [original 695-member permanent evidence release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1v2-d1-development-nogo-2026-11-04), and [corrected F0–F5 derived-data release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1v2-f0-f5-archive-only-2026-11-05-v2). The original simulator was SUMO **1.28.0** in pinned image **ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb**.

## 2. Primary scientific question, aims and limits

**Question:** When just one eligible driver's *planned* route changes, what time-resolved differences in vehicle arrival, stopped vehicles, upstream/downstream loading and priority-junction service precede the large positive or negative elapsed-time changes experienced by drivers whose assigned routes are unchanged?

**Aim 1 — Vehicle time alignment.** Capture when each affected vehicle actually enters or leaves a road and approaches or crosses priority junctions, at the original simulator's time-step resolution. Find the first verifiable divergences between matched baseline and perturbed traffic.

**Aim 2 — Queue and service mechanism.** Determine whether changes in near-stopped vehicle clusters, upstream occupancy and receiving-link conditions temporally precede differences in junction discharge and secondary-driver delay. Preserve alternative mechanisms and contrary examples.

**Aim 3 — Whole-driver accounting and fairness.** Independently confirm that matched scheduled-to-arrival network effects, including **nonparticipants**, reproduce the original outcomes. Keep insertion delay, in-network duration, stopped waiting and tail harm separate: waiting is already inside duration, not an extra additive travel cost.

**Observability boundary:** E1-v2's historical prediction files contain full-trip per-driver predictions, **not archived model edge-entry forecasts**. An instrumented SUMO replay can resolve the **actual observed chronology** but cannot, by itself, compute a model-vs-actual per-edge prediction error. A post-outcome, source-locked model-event diagnostic would be a separate proposal, explicitly labeled retrospective, and must not be mistaken for independent validation.

**Bundle boundary:** The four replays below are **single-route** pairs, not four-arm joint-swap experiments. They cannot directly localize the ten observed bundle interactions. Those existing quantitative bundle findings remain preserved; any vehicle-resolved bundle study would require a distinct, separately justified protocol rather than automatic expansion.

## 3. Exactly four predefined passive replays

| Replay | Development seed | Original arm | Intervention | Purpose |
|---|---:|---|---|---|
| R1 | **6112** | **I** | Original independent traffic-aware planned assignments | Baseline for a large realized harm case |
| R2 | **6112** | **probe2** | Original single swap by **veh0142** | Trace how +3,215 other-driver network-s arose |
| R3 | **6113** | **I** | Original independent traffic-aware planned assignments | Baseline for a large realized benefit case |
| R4 | **6113** | **probe2** | Original single swap by **veh0038** | Trace how −3,960 other-driver network-s arose |

Each arm uses the original **1,000 matched driver identities** on the synthetic 10×10 high-congestion priority-junction network, with the original 200-second departure schedule. There are exactly **4,000 replay trip records**, but only **two independent demand seeds**; the four arms and nested driver observations must not be treated as four independent random replications.

**Do not reselect cases, regenerate routes, expand to other seeds, replace failed cases, introduce a new routing policy, change simulator physics, or open reserved 6201–6212 validation / 6301–6312 Test B data.** Both route swaps and their earlier numerical outcomes are already public and inspected.

## 4. Competing, falsifiable explanations

| Hypothesis | Evidence consistent with it | Evidence against / interpretive limit |
|---|---|---|
| **T — Temporal alignment / insertion:** changed road arrival order amplifies effects even without meaningful source insertion changes | New vehicle-level chronology shows early changes in approach/edge-entry order and subsequent secondary delays | Near-identical entry order despite large effects; original insertion decomposition already makes a *pure insertion* explanation less plausible in these cases |
| **Q — Queue propagation / receiving link:** local blockage or queue dissipation spreads to connected upstream roads | Measured contiguous, near-stopped clusters and delayed/relieved exits develop along a connected path before changes to unchanged-route drivers | No coherent upstream/downstream propagation, or widespread changes without observed local queue signatures |
| **J — Dynamic priority-junction service:** simplified E1-v2 scheduling misses realized yielding, movement ordering or receiving-capacity constraints | Verified movement and internal-lane transitions show altered approach delays, turn sequences or discharge matching local traffic response | No movement-level divergence at candidate junctions; any observed order alone cannot prove the junction is the unique causal mediator |
| **A — Replay/measurement validity or event sensitivity:** discrepancies are artifacts of instrumentation, source clocks, reporting precision or unstable event sequence | Replays fail exact original-driver outcome parity or reporting definitions do not match | Parity and temporal coverage pass; physical network response remains real **in these matched simulations**, while unique mediation is still unproven |

These expectations are **diagnostic**, not a post-hoc replacement for E1-v2's frozen 10%-MAE and 60%-sign qualification gates. Report both evidence supporting and evidence contradicting each proposed mechanism.

## 5. Passive instrumentation and frozen physical environment

**Unchanged:** Original network.net.xml, trips.xml, each original arm's route XML, all vehicle/driver IDs and schedules, seed, SUMO 1.28.0 image digest, demand, car-following/lane-changing settings, priority junction logic, simulation step length, random settings and original tripinfo/statistics/collision outputs. Never call the route generator or the E1-v2 forecast engine during the replay.

**Observation-only additions, after verifying these flags in the exact pinned container:**

1. **1-second all-vehicle FCD:** Save vehicle ID, simulation timestamp, x/y, internal/external lane ID, along-lane position and speed; include all active vehicles, no sample probability or downsampling. Define actual entry/exit transitions at the recorded time-step resolution, not fictitious continuous-time precision.
2. **Vehicle-route edge exits:** Save original planned/traversed edge sequence and exit times using vehroute-output with exit-times, if confirmed supported. Keep internal-edge transition handling explicit.
3. **Five-second edge/lane mean-data:** Retain the original detector configuration and compare with the archived 5-second streams, preserving partial final intervals, per-arm end times, external versus internal edge coverage, and missing-field semantics.
4. **Tripinfo and exception channels:** Save all 1,000 completions, actual departures, arrivals, durations, reported waiting/time loss, collisions and available structured emergency indicators for each arm. These reproduce the historical outcomes and are not replaced by trajectory-derived estimates.

**Specific field-precision warning:** SUMO documentation notes that displayed sampledSeconds of 0.00 can conceal a small positive amount rounded in output. Therefore the old F0–F5 zero-sample convention is a *recorded-precision convention*, not proof that every such road interval contained literally no vehicle at any instant. Compare it with the vehicle-resolved trace instead of claiming exact physical zero. Do not reinterpret speed or occupancy as additive time costs.

**Storage safeguard before execution:** Produce an estimate and confirm a durable raw-evidence retention strategy. Set a prospective maximum of **512 MiB of compressed observation output per replay and 2 GiB across the four**. If the exact full-vehicle-resolution evidence cannot fit that maximum or cannot be preserved durably, report a design/resource limitation **before any data-dropping, thinning or extra execution**. No silent FCD sampling to meet the cap.

Official SUMO references (documentation may describe newer behavior; the pinned 1.28.0 executable governs): [FCD](https://sumo.dlr.de/docs/Simulation/Output/FCDOutput.html), [vehicle routes and exit times](https://sumo.dlr.de/docs/Simulation/Output/VehRoutes.html), [edge/lane traffic measures](https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html), and [tripinfo](https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html).

## 6. Mandatory stop/go stages for a future separately authorized execution

### Gate G0 — Original evidence/provenance, before any SUMO
- Re-download original 695 member release and verify each saved checksum and original scenario manifest; verify four exact arm inputs and 1,000 original IDs per arm.
- Confirm original network/demand/route SHA-256 and unchanged scenario parameters. Compare paired I/probe2 assignments: **exactly one changed route**, with all 999 other original planned routes, OD values and schedules unchanged.
- If any source cannot be verified or original outputs are unavailable: **STOP** and publish an integrity limitation.

### Gate G1 — Instrumentation preflight, no SUMO
- Confirm all flags, output attributes, internal-lane coverage, 1-second sampling, compressed output, parser schema and storage bounds under the exact pinned image.
- Freeze command lines, analysis definitions, original and post-instrumentation output comparisons, maximum footprint and checksums in a replay-specific manifest.
- If a required measurement is unsupported: **STOP**; do not modify the simulator or substitute a different version.

### Gate G2 — Exact primary-outcome reproduction
- Execute **only the four specified arms**, preserving all original uninstrumented physics and inputs.
- Before investigating trajectories, compare *all 1,000 paired vehicle records per arm* against the corresponding original: ID, depart, arrival, duration, reported waiting and departure delay where present. Require the original reported precision to match, with at most **0.02 seconds per driver-field** for numerical parsing; for aggregate scheduled-to-arrival totals, require **≤0.1 network-second** difference from totals reconstructed at original recorded precision. These thresholds may not be relaxed after results.
- Verify exactly 1,000 completions, original routes, structured exception counts where recorded and the original +3,219 / −3,883 total network-second comparisons (with correct precision).
- **Any non-equivalent arm invalidates its corresponding replay comparison.** Preserve the discrepancy, do not select replacement seeds or present its new traces as the mechanism of the historical outcome.

### Gate G3 — Trace completeness and observational validity
- Confirm one-second FCD coverage for all active drivers and documented simulation time range, vehicle-to-lane mapping, internal-lane/turn interpretation and vehicle-route exit consistency.
- Distinguish inferred edge-transition intervals and possible subsecond ambiguity from true exact physical crossing events.
- If critical track observations are missing, produce **MEASUREMENT_INSUFFICIENT**, not a claimed bottleneck diagnosis.

### Gate G4 — Scientific interpretation and bounded decision
- Run the preregistered diagnostics only for G2/G3-valid paired replays, present competing explanations, contrary examples and ambiguity.
- Separate **route-change total effects**, which are observed under the original matched intervention, from the *causal contribution of waiting at a named junction*, which is **not** independently identified by passive observation.
- Declare either **CASE-LEVEL MECHANISM CHARACTERIZED, CAUSAL SOURCE STILL OPEN**, **ONE OR MORE HYPOTHESES DISFAVORED**, or **INTEGRITY/OBSERVABILITY LIMITATION**. Do not turn one visually striking sequence into an established universal traffic law.

## 7. Prespecified analyses if the replay passes

1. **Matched vehicle timelines:** Plot all four runs on their native simulation clock (no post-hoc time shift). Track actual departures, edge exits, junction-lane transitions, arrivals and waits. Predeclare primary temporal views at **1-second trajectory resolution**, **5-second road summaries** and **30-second descriptive buckets**.
2. **First divergence and spread:** Identify the earliest matched divergence for the changed driver and for vehicles with unchanged original routes, then examine upstream/downstream connectivity and elapsed delays. The F0–F5 first five-second divergence reports for the two selected probes are *historical clues*, not a guarantee of a unique causal onset.
3. **Queue proxies:** Use the primary **≤0.1 m/s** near-stop criterion and separate **≤1.0 m/s** sensitivity, report counts, stop durations, lane position and contiguous near-stop patterns. Do not call a slow-edge aggregate a physically measured queue front without matching vehicle positions.
4. **Priority junctions:** Using the J0–J4 static connection/foe map, identify observed approach arrivals, internal-lane progression and downstream admission. Count turn discharge only where movement identity can be reconstructed; otherwise label as unknown. These intersections are **priority**, not traffic-light-controlled.
5. **Network time and distribution:** Reconcile every driver's scheduled-to-arrival change with insertion delay plus in-network duration, and describe helped/harmed/unchanged drivers, p90/p95, >30-second additional delay and fixed opt-out-roster effects. The historical Test B fairness threshold does **not** become a gate on these selected single-route diagnostic cases.
6. **Spatial alternatives:** Compare both increases and reductions in congestion, including locations away from the changed driver's physical route. Preserve evidence inconsistent with both queue and junction hypotheses rather than retrospectively choosing one explanatory location.

Only two outcome-selected seeds are observed. Numerical uncertainty, descriptive sensitivity and case-specific timing are appropriate; claims of independent statistical generalization, new estimator accuracy or cooperative efficacy are **not**.

## 8. Deliverables, decision and explicit non-goals

**One consolidated GitHub scientific package, not a new engineering-readiness program:**

- Source and command manifest: exact four historical arms, original/replay SHA-256s, pinned container, code, original flags and observation-only flag differences.
- Reproducibility table for **4,000** replay trip records, per-driver outcome equality, exceptions and any failed gates.
- Preserved 1-second FCD, optional vehroute edge-exit logs and original-equivalent five-second detectors with verified source-to-output provenance; large data in checked durable release assets rather than Git history.
- Matched vehicle/junction time diagrams, spatial queue-proxy comparison and per-driver effects, including nonparticipants and contradictory patterns.
- A hypothesis evidence matrix identifying **DIRECT OBSERVATION**, **CONSISTENT WITH**, **CONTRADICTS**, **NOT OBSERVABLE** and **CAUSAL ROLE UNIDENTIFIED**.
- A short final explanation of what was newly learned, why it matters for the original coordination research, and **one specific next scientific decision** only if the data warrants it.
- Update README with the result and its limitations. Prepare visual-first LinkedIn/X publication materials only if this is a substantive result, and **obtain explicit approval before publication**.

**No automatic E1-v3 development, no new model fitting, no validation on inspected 6101–6114 seeds, no opening reserved 6201–6212 / 6301–6312 data, no policy Test B, no vehicle-level control intervention, and no claims about actual human-driver consent, safety or journey comfort.**

**Completion condition:** The four planned attempts are finished with validated observations **or** a mandatory provenance/reproduction/instrumentation gate yields an explicitly published stop. An unresolved physical explanation is a valid scientific outcome; it is not permission to broaden the experiment without a new design.

**Final planning disposition:** *Scientific plan ready for review; four passive SUMO replays NOT AUTHORIZED OR EXECUTED by this document.*