# Cooperative Traffic Research — Six-Run Instrumented Replay: Scientific Specification and Execution Plan

**Date:** November 2, 2026  
**Research stage:** Post–Experiment 007, after P0–P3 investigation  
**Status:** **SPECIFICATION / PROSPECTIVE PLAN ONLY — NOT AN EXECUTED STUDY OR FROZEN EXECUTION PROTOCOL.**  
**User authorization in this step:** Write and publish the full six-run replay specification first. **Do not run SUMO, change the routing algorithm, revise the failed Experiment 007 gate, or publish social-media updates.** A separate execution-stage authorization and an immutable protocol/code snapshot will precede the replay.

## Executive scientific purpose

**Central question:** How did deliberately changing one or two planned routes create very large *realized* changes in the total elapsed travel time of other vehicles, while the original assigned-demand externality model predicted small, zero, or opposite effects?

The completed [P0–P3 investigation](POST_EXP007_EXTERNALITY_ESTIMATOR_P0_P3_FINAL_SCIENTIFIC_REPORT.md) established that, for all 20 selected equal-nominal-free-flow swaps, the original predicted total change was twice the predicted own-driver change; therefore the predicted externality mirrored the own-driver signal. That is a **verified, conditional structural limitation of the model**. It does **not** identify what happened physically at particular junctions or times.

This study targets the missing **time-resolved traffic mechanism**, using the **exact original assigned routes, driver demand, seeds, network and simulator version**, augmented only with noninvasive observational outputs. It is a **retrospectively selected exploratory mechanism study**, not a new independent validation of externality prediction, not a new route optimizer, and not Experiment 007 Test B.

### What success means

Success is **reproducing original observed outcomes with instrumentation** and extracting a defensible, time-ordered account of where traffic flow, stops and road-entry patterns diverged. A named bottleneck is not required for success. If multiple explanations remain observationally compatible, publish an **unresolved mechanism** rather than inventing a unique cause.

The original Experiment 007 Test A **NO-GO (8/20 sign agreement = 40%, below 60%) remains frozen**. Experiment 007 Test B remains **unexecuted**. The 30 original simulations are historical evidence and are not to be repeated or replaced in full.

## 1. Frozen historical evidence and data provenance

Sources of truth:

1. [Original Experiment 007 frozen protocol](EXPERIMENT_007_FROZEN_PROTOCOL_V1.md).
2. [Experiment 007 Test A final report](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md).
3. [Original 30-simulation run 41380998833](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833), with per-seed artifacts named \`exp007-probe-4101\` through \`exp007-probe-4105\`; the raw original archives currently have expiry near **December 2, 2026 UTC**.
4. [P0–P3 final scientific investigation](POST_EXP007_EXTERNALITY_ESTIMATOR_P0_P3_FINAL_SCIENTIFIC_REPORT.md), [archival audit code](../research/audits/exp007_p0_p3_audit.py), and [successful archive-only audit](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41513917088).
5. Frozen Experiment 007 route/simulation source at implementation merge \`afa252c8d9ec31b247db49f2e2b0e30ce6d31fc8\` (source file \`experiments/experiment_007/run_v01.py\`), demand generator at \`be2e8d27c78c8b6de4891115d6d951edc877ac6e\`, pinned SUMO container \`ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb\` (original logs identify SUMO 1.28.0).
6. [Permanent singleton summary](results/exp007_test_a_probes.csv) and [per-seed bundle effects](results/exp007_test_a_bundles.csv).

**Pre-execution prerequisite:** Download and hash-check the two original seed archives (4101 and 4102) and their raw \`network.net.xml\`, \`trips.xml\`, \`demand.json\`, original \`routes.rou.xml\`, \`tripinfo.xml\`, \`statistics.xml\`, \`collisions.xml\`, \`sumo.log\` and stage logs for all six selected arms. Retain immutable originals alongside outputs; do not regenerate the demand, network, or route XML from a newer algorithm. Record original file SHA-256, prior action-run IDs, frozen source commit, pinned image digest, original command-line options and exact instrumented-only differences.

If originals are unavailable, incomplete, internally inconsistent or hash-unverifiable, **stop before new simulation**. Do not replace an expired original with a regenerated scenario and call it a replay.

## 2. Exactly six predefined instrumented SUMO executions

The selected cases are **post-outcome choices** motivated by the prior P0–P3 analysis. Their results can explain particular examples but are not independent confirmatory evidence about population prediction accuracy.

| Replay ID | Historical seed | Original arm | Route change compared with baseline I | Why this case |
|---|---:|---|---|---|
| **R1** | 4101 | \`I\` | None | Baseline control for original seed 4101 |
| **R2** | 4101 | \`probe2\` | Single pre-existing route swap for **veh0000** | Predicted externality **0**, realized externality **+3,181 network-seconds** |
| **R3** | 4102 | \`I\` | None | Baseline control for original seed 4102 |
| **R4** | 4102 | \`probe0\` | Single original swap for **veh0582** | Predicted externality approximately **−1.08**, realized **+2,724 network-seconds** — opposite direction |
| **R5** | 4102 | \`probe1\` | Single original swap for **veh0158** | Predicted externality approximately **+13.50**, realized **+3,763 network-seconds**, a large magnitude mismatch |
| **R6** | 4102 | \`bundle\` | Original simultaneous swaps for **veh0582 and veh0158** | Observed total network effect **+3,572 network-seconds**, versus **+6,561** summed singleton *total* effects; realized interaction **−2,989 network-seconds** |

**Sign:** Positive \`S − I\` denotes more elapsed travel time (harm); negative denotes savings. A *network-second* is one second summed over vehicles, not one driver's additional journey time. Singleton **external** effects exclude the changed driver's own elapsed time; bundle interaction is defined using **total** system changes to avoid ambiguity about the set of treated drivers.

**Do not conflate** R2's realized externality (+3,181) with its realized **total** network effect (+3,177). For seed 4102, the two singletons' realized total effects were **+2,626 and +3,935**, whereas the bundle was **+3,572**. These are original frozen observations, not prospective replay findings.

**Scope:** Exactly these six runs, not 30, 50, or a new matched-seed cohort. One synthetic 10×10 grid, 1,000 identical scheduled demand identities per arm, 200-second high-congestion demand window. Same frozen simulation seed within each paired seed family. Do not alter scheduled departure, route choices, routing consent/eligibility, car-following model, lane-change model, intersection control, device probability or randomness settings.

## 3. Falsifiable mechanism questions

### M1 — Predicted edge-bin agreement vs realized arrival timing

Does a route change with a **zero or very small predicted externality** nevertheless alter *actual* vehicle arrival times and/or the simultaneous demand at an edge or turning movement in a time window where the 30-second assigned-demand proxy predicted no change?

**Evidence:** For changed driver and affected matched cohort, compare original predicted edge/bin footprints with observed edge entry/exit times derived from the traced movements. Quantify bin shifts (same bin, adjacent bin, multiple-bin difference), mean/median absolute entry-time residuals and differences in actual time-concurrent demand. Distinguish predicted *assignment-count bins* from time-averaged **physical** lane occupancy.

**Counterfinding:** If observed edge-entry times and physical traffic pressures remain essentially unchanged on relevant edges despite material network outcome differences, this hypothesis does not explain the selected effects; inspect other sources such as departure insertion, downstream movement and measurement integrity.

### M2 — Queue emergence and junction discharge

Do altered edge/turn movements precede growth or dissipation of stopped/slow-moving vehicle groups, changed intersection throughput, and subsequent delays of drivers whose assigned routes remain unchanged?

**Evidence:** Time-indexed vehicle tracks (lane/edge, position, speed), 5-second edge/lane waiting/speed/occupancy/flow, queue proxies using an explicit speed threshold, signal and internal junction geometry where available, and temporal ordering: candidate divergence → local flow/queue change → secondary-driver delay. Compare against the same seed's unchanged I trajectory. Identify evidence of spillback only if spatial vehicle positions show queue influence propagating upstream to another entry/edge; do **not** equate increased edge waiting alone with measured spillback.

**Counterfinding:** No consistent local queue or intersection-flow divergence near the affected paths, or network difference largely attributable to another measurable process. The result can remain unresolved rather than asserting queue causation.

### M3 — Insertion delay versus on-network time

Does most of the network effect arise before vehicle insertion or during travel?

**Evidence:** Independently reconstruct \`arrival − scheduled_departure = departDelay + duration\` for all original and replay arms. Split net differences into insertion delay, recorded stopped waiting during travel, and residual movement-duration component. **Do not add waiting or timeLoss as independent extra journey cost**; they are already part of trip duration or separate diagnostics.

**Counterfinding:** If insertion shifts explain most of a selected effect, an exclusively on-road queue narrative is inadequate.

### M4 — Nonadditivity of two route changes

At what **time and location** does R6 depart from the naive sum of R4 and R5, and can the traced dynamics explain the −2,989 network-second original joint interaction?

**Evidence:** For seed 4102, calculate \`D_interaction(t) = D_bundle(t) − D_probe0(t) − D_probe1(t)\` for aligned interval-specific physical metrics, always relative to the same I baseline, and reconcile accumulated per-vehicle final travel-time interaction with original −2,989 network-seconds. Show whether effects arise on shared edges or junction approaches or via cascades elsewhere.

**Caution:** Time-varying mean speed and occupancy are nonlinear aggregated measures; differences should not be added as though they were causal travel-time contributions. Use time-resolved metrics to locate plausible dynamic interactions; **do not claim a unique mediator** merely because one junction's change precedes subsequent delay.

### M5 — Simulation and instrumentation integrity

Can the exact original per-driver outcomes be reproduced after attaching observational outputs?

**Evidence:** Original and replay input files/route assignments byte-for-byte identical; pinned SUMO image digest/version, seed, driving behavior and simulation options fixed; tripinfo and event fields reproduce within predeclared tolerances. If instrumentation affects the trajectories, stop and classify as an integrity problem rather than interpreting the altered simulation as the original physical mechanism.

## 4. Instrumentation contract: observational outputs only

All options and additional-file attributes **must be verified using the pinned SUMO 1.28.0 image's \`sumo --help\` and a no-new-simulation syntax/preflight review before execution**. Online documentation describes intended capabilities but is not a substitute for checking the exact image.

### 4.1 Required high-resolution vehicle movements

- Use \`--fcd-output <arm>/fcd.xml.gz\` with **all 1,000 vehicles** (no probabilistic sampling), default simulation 1-second steps; explicitly record effective \`--step-length\` and verify it matches original.
- Require time, vehicle ID, external/internal lane or edge mapping (vehicle \`lane\` and \`pos\`, or lane identity derivable unambiguously), 2-D x/y position and speed. Preserve junction/internal-lane observations. Do not enable \`--fcd-output.geo\` on the synthetic Cartesian grid.
- The expected FCD format and sampling options must be checked in the pinned image. If essential position/speed/lane fields are missing or truncated, **fail the measurement validity gate**; do not silently substitute aggregated means.
- Record one-second temporal alignment and output precision so an edge transition is not mistaken for the exact continuous-time entry instant. Mark observations between discrete samples as interval-censored at the sampling resolution.

### 4.2 Per-route edge traversal times

- Request \`--vehroute-output <arm>/vehroute.xml.gz\` and \`--vehroute-output.exit-times true\`, if verified supported by the pinned image.
- Validate each vehicle's ordered road-edge sequence against original \`routes.rou.xml\`; use exit times to reconstruct approximate edge entry, travel and waiting-exposure windows. The first edge's entry is actual insertion time, not scheduled departure; other external-edge boundaries may include internal junction transitions.
- When FCD and vehroute times disagree, report matching definitions, internal-edge handling and time-step precision before treating the difference as an error.

### 4.3 Interval edge and lane traffic state

Use an **observation-only** SUMO \`--additional-files\` definition containing:
- \`<edgeData id="exp007-edge" file="edgedata.xml.gz" period="5" withInternal="true" .../>\`
- \`<laneData id="exp007-lane" file="lanedata.xml.gz" period="5" withInternal="true" .../>\`

Require real measured interval definitions for \`begin\`, \`end\`, sampled vehicle-seconds, speed, \`occupancy\`, \`waitingTime\`, entered/left counts when available and internal edges/lanes. The **5-second intervals** are shorter than the **30-second forecast bins** to resolve the ordering of congestion development without excessive per-step detector output. Preserve the original 30-second predicted assignment-bucket definitions separately.

Explicitly distinguish:
- \`assigned_count(edge, 30s bin)\`: prospective counter from planned routes, **not** a physical occupancy measurement;
- \`edgeData/laneData occupancy\`: simulator-measured interval-based utilization, unit/definition checked;
- \`queue proxy\`: count or line of near-stopped vehicles derived from FCD using the same documented speed threshold (default 0.1 m/s in the project tripinfo waiting definition), with sensitivity at 1.0 m/s **descriptive only**.

Edge/lane flow, speed and stopped-time summaries are not interchangeable with route assignment load. If extra measurement options are unsupported by the image, stop the preflight and explicitly amend the prospective spec **before** execution, rather than dropping a promised essential signal after outcomes are known.

### 4.4 Existing output channels retained

Preserve original-equivalent \`tripinfo.xml\`, \`statistics.xml\`, \`collisions.xml\`, \`sumo.log\` and stage log outputs, with original flags; add only observational FCD/vehroute/additional-file outputs. Record actual SUMO command and exact parameter diff against original. No \`--fcd-output\` downsampling, random device assignment, live TraCI policy intervention or traffic-signal changes.

### 4.5 Output and storage safeguards

Output volume could be substantial (all vehicles at every step). Prefer gzip by filename when supported, retain exact uncompressed-content SHA-256 where practical, log sizes/record counts and preserve each of six runs separately. Stream XML parsing in postprocessing rather than loading all FCD records into memory. Use temporary GitHub Actions artifacts **plus a permanent scientific summary and integrity manifest**; do not promise that all large FCD traces will fit normal Git history. Set an explicit artifact-retention and archival plan before starting.

## 5. Mandatory preflight and replay-validity gates

### Gate 0 — Original evidence present (before any simulation)

Require both original seed families and six selected arm route/measurement records; SHA256 and expected original ancestry; exact 1,000 matched identities, identical within-seed OD/departures, one changed route in singleton, two in bundle. If missing, **STOP**.

### Gate 1 — Pinned-version instrumentation support (no simulation)

Review pinned SUMO 1.28.0 \`--help\` and detector XML schema/output semantics. Verify FCD lane/speed/position, vehroute exit-times, internal laneData/edgeData, 5s period, gzip/paths, actual seed/step-length and XML generation. Check parser contracts and deterministic per-arm output directories. Unsupported essential feature → **STOP and document**. No new test seed may be substituted.

### Gate 2 — Primary outcome equivalence (during exact six replays)

For each selected arm compare *each of all 1,000 vehicles* with its original matching \`tripinfo.xml\`:
- Same IDs, scheduled departure, source and destination, planned road-edge sequence and 1,000 arrivals.
- \`depart\`, \`arrival\`, \`duration\`, \`departDelay\`, \`waitingTime\`, \`timeLoss\` agree **within 0.02 seconds per value** (or the original XML's finer printed quantization, whichever is tighter; do not lower the bar after seeing failures).
- Original structured \`statistics.xml\` collision, emergency-braking and emergency-stop counts agree **exactly** when originally present; collision XML event count agrees exactly.
- Reconstructed original **single-swap network total and externality**, and the original seed-4102 bundle interaction, agree within **0.02 network-seconds per paired comparison** after computing from original precision-preserving fields (if output precision yields greater aggregate rounding error, report this explicitly and **STOP rather than retroactively loosening the threshold**).

If **any** arm fails, mark that arm and associated contrasts **non-equivalent** and **do not interpret newly instrumented trajectories as the original frozen mechanism**. Publish a reproducibility discrepancy rather than retuning routes, stepping, tolerances or physics. Original Test A decision is unchanged. Every attempted arm remains part of the documented six-run footprint; do not hide incomplete or invalid executions.

### Gate 3 — Observability and accounting

For each equivalent replay:
- FCD vehicle IDs, timestamps, lane identities and speeds are present and coherent; event times monotonically ordered.
- Reconstructed route transitions and edge-exit sequences match original road-edge route plan at 1-second sampling resolution, allowing documented internal-lane ambiguity.
- Five-second lane/edge metrics cover the period of actual traffic, including time after the 200-second departure window through last arrival.
- Reconcile near-stop time inferred from FCD with tripinfo waitingTime, identifying differences due to threshold, internal lanes, sampling and step-level semantics. Check output coverage for all 1,000 vehicles; do not infer missing rows as free-flow travel.

If Gate 2 passes but Gate 3 fails, publish a **measurement insufficient** outcome instead of a physical-bottleneck attribution.

## 6. Prespecified analysis after Gates 0–3 pass

### A. Baseline and treatment trajectories

For both seeds separately:
1. Plot number of active and not-yet-inserted vehicles over time; cumulative departures and arrivals.
2. For each selected changed driver, plot actual lane/edge path and time against baseline I; show route divergence, internal junction traversal and delay.
3. Compute, per external edge and internal junction approach, five-second deltas: flow counts, speed, occupancy, waiting seconds and near-stopped vehicle count.
4. Rank candidate regions by **onset timing**, persistence and magnitude, not only their total delay. The first divergent 5-second interval is a **candidate onset**, not necessarily the primary cause.
5. Compare actual edge-entry times with the forecast 30-second footprint for the target driver and affected others, and report bin shifts/early-vs-late bias. No updating or refitting the forecast.

### B. Queue propagation and unchanged-route spillovers

- For vehicles whose routes are exactly unchanged (all other 999 in singleton probes), compute when and where their observed motion first diverges relative to baseline, relative to candidate edges or connected upstream junctions.
- Define an exploratory "upstream queue propagation" pattern only if spatially contiguous near-stopped vehicle traces appear on an upstream edge *after* the relevant junction/edge slowdown, and precede additional waiting for later vehicles. Do not call traffic wave travel causality proven by descriptive animations.
- Present evidence of competing mechanisms (insertion blocking, shared junction constraints, cross-traffic queues, downstream flow discharge) and report when multiple explanations fit the same traces.
- Use nonparticipant and participant strata where useful, while preserving individual realized-harm measures; do not treat a single traced replay as acceptance/consent evidence.

### C. Bundle interaction (seed 4102)

For I, probe0, probe1, bundle:
- Recalculate final matched \`C_X = sum_i(arrival_X − scheduled_i)\`.
- Define \`J = (C_bundle−C_I) − (C_probe0−C_I) − (C_probe1−C_I)\`; target original **−2,989 network-seconds**.
- Compute trajectory and edge-time differences-of-differences descriptively, with all four arms' FCD/edgeData referenced to the same original I. Search for shared time-window bottleneck formation or dissipation rather than inferring an additive per-driver externality formula.
- Report the strongest plausible time/location interactions with observed chronology and explicit alternatives. The model's algebraic structural limitation is already established; the replay is not a model-fitting exercise.

### D. Required sensitivity and caution

- Primary observed near-stop speed criterion **≤0.1 m/s**; optional separate **≤1.0 m/s** sensitivity. Do not change the main criterion after results.
- Primary time slices **1-second FCD and 5-second lane/edge aggregation**; descriptive 30-second aggregation for comparison to forecast buckets. Do not move windows opportunistically to maximize a claim.
- Report both total **network-seconds** and per-driver averages with correct denominators; avoid conflating total travel-time change with throughput or number of vehicles whose routes changed.
- Report negative/nonconforming evidence, time-step uncertainty, missing internal-lane observations, and all candidate bottlenecks, not just a single visually compelling junction.
- No hypothesis testing across six **post-outcome-selected** arms as independent random replicates. Two seeds are not a statistically powered generalization sample.

## 7. What would justify each scientific conclusion?

| Prospective outcome | Required evidence | Valid conclusion |
|---|---|---|
| **Reproducibility failure** | Gate 2 fails for any original arm or original bundle | Traced results not valid reconstruction of original scenario; physical explanation withheld |
| **Observation failure** | Gate 2 passes but essential FCD/edge-time data missing or internally inconsistent | Original outcomes reproduced, but physical mechanism unresolved due to missing instrumentation |
| **Clock-proxy mismatch demonstrated** | Gate 2/3 pass and observed edge-entry/occupancy timing materially diverges from proxy bin assumptions | The estimator's time-bin approximation is demonstrably inadequate on selected cases; actual queue causation may remain unresolved |
| **Queue/intersection amplification strongly supported** | Time-ordered changed-route arrival/turn, localized growth or dissipation of near-stopped vehicles and corresponding secondary-driver delay | Specific *candidate* congestion mechanism supported for these cases, not a unique causal mediator |
| **Insertion delay dominant** | Most realized elapsed effect reconciled to actual departure insertion rather than post-insertion duration | Counterexample to a purely junction-travel-time explanation |
| **Bundle nonadditivity localized** | Four-arm joint-versus-single contrast aligns with observed edge/time changes while full effect reconciles | Concrete observed coupled-traffic response in selected scenario, still not a validated joint optimizer |
| **Causal bottleneck still unidentified** | Conflicting or insufficient time-ordered observations | Publish explicit uncertainty and exact missing intervention needed; no fabricated certainty |

**Causal-identification boundary:** Because the original experiment manipulated routes and the replay changes only what is observed, the *total route-assignment effect* is identified in the simulator **if** outcomes reproduce. But post-treatment waiting/queue exposure is not separately randomized. A temporal association involving a specific junction does not identify the unique mediated causal effect of that junction. A separate physical capacity/signal intervention would require a **new scientific question and permission**, not an automatic seventh run.

## 8. Execution sequence, integrity and stopping rules

**Planning deliverable in this approved step:** this document is published to GitHub, without creating or dispatching any simulation workflow.

Once execution is separately authorized:
1. **Freeze a replay-specific scientific protocol and source manifest**: exact six IDs, source digests, original archive fingerprints, all measurement flags, analysis code, clock definitions, output filenames, equivalent-trip tolerances and stop conditions. Record that the six cases were selected after Experiment 007 outcomes.
2. Run all **non-SUMO** preflights (original hashes, route invariance, schema/CLI support). Do not require unrelated "engineering readiness" expansion.
3. Replay only the six specified arms under the frozen pinned image, in independent arm directories. Reuse original network/demand/route files; never run a route-generation policy or update model parameters. Preserve failed attempts.
4. Run per-arm original-output equivalence **before** reading new traffic trajectories for scientific interpretation. Stop causal interpretation on failed equivalence.
5. If valid, compute ordered physics/flow diagnostics and the four-arm joint interaction. Keep derived raw tables and plots verifiably linked to original files.
6. Audit all outcomes, record supported/disfavored/unidentified hypotheses and publish **one consolidated scientific report** (not a sequence of exploratory milestone posts) plus manifests and machine-readable evidence to GitHub.
7. Present optional visual LinkedIn/X science communication for a **separate user approval**; do not publish automatically.

**No automatic retries or extra seeds.** If a job fails for environment or measurement reasons, report the exact defect and preserve the attempt; a truly identical deterministic rerun may be proposed for repair with unchanged predeclared settings, but do not launch replacement scenarios or silently amend the six-arm budget. Stop after the bounded evidence is collected or an integrity gate blocks valid interpretation.

## 9. Required end artifacts and exit criteria

One coherent publication package, distinct from the original frozen Experiment 007 outcome:

- **Prospective protocol + immutable provenance:** original and replay file SHA-256 manifests, source/container hashes, route assignment diffs (expected none vs originals), exact six executable commands, and a gate checklist.
- **Replay results:** original-versus-instrumented tripinfo equivalence table for **6,000 driver records**; all recorded exception fields; matched original network totals; identity and completion checks.
- **Raw time-resolved evidence:** six named FCD/vehroute files and six pairs of 5-second edge/lane outputs, or explicitly documented omissions if a mandatory measurement gate blocks interpretation. Time coverage and file sizes recorded.
- **Mechanism diagnostics:** predicted-vs-observed edge-bin timing, edge/junction queue proxy and flow timelines, candidate bottleneck map/locations on the *synthetic* grid, changed- and unchanged-route driver waiting/arrival differences, and the exact seed-4102 bundle interaction accounting.
- **Causal evidence matrix:** directly verified, strongly supported descriptive, unresolved, counterevidence, and limitations. No claim that subjective journey experience was measured.
- **Single scientific recommendation:** whether time-resolved evidence points toward junction/queue-aware marginal forecasting, a still-unresolved reproducibility/measurement problem, or a different discriminating experiment. **Do not rerun Test B or label any future estimator validated without fresh independent data.**

**Completion definition:** Six prespecified attempts are recorded and independently audited, or a mandatory gate prevents meaningful execution/interpretation with a published explanation. A null or inconclusive physical result counts as a completed, scientifically bounded investigation—not a reason to continue tuning or broadening the study indefinitely.

### Existing official SUMO measurement documentation (for planning, not substitute for pinned-version preflight)

- [FCD trajectories](https://sumo.dlr.de/docs/Simulation/Output/FCDOutput.html) — \`--fcd-output\` and observation frequency/vehicle attributes.
- [Vehicle-route output and edge exit times](https://sumo.dlr.de/docs/Simulation/Output/VehRoutes.html) — \`--vehroute-output\`, \`--vehroute-output.exit-times\`.
- [Lane- and edge-based traffic measures](https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html) — \`edgeData\`, \`laneData\`, \`period\`, \`withInternal\`, \`occupancy\`, \`waitingTime\`, flow.
- [TripInfo units and departure accounting](https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html) — actual departure, departDelay, arrival, duration, waiting.
- [SUMO command-line options](https://sumo.dlr.de/docs/sumo.html) — confirm availability under pinned 1.28.0.

---

**End-of-spec decision:** The *scope and intended measurements* for the next exploratory six-run replay are defined; **no new simulation or route-policy optimization is authorized by publishing this specification alone**. Preserve the Experiment 007 Test A NO-GO and unexecuted Test B, keep realized individual fairness active, and defer subjective journey quality.
