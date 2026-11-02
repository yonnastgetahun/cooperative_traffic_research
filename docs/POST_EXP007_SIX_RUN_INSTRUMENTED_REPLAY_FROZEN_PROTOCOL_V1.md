# Frozen protocol v1 — Six-run instrumented replay after Experiment 007

**Date:** 2026-11-02. **User approval:** execution of the previously published six-run replay. This protocol is frozen **before** any replay simulation; no new routing decisions or forecasts are permitted.

## Main question and scope

Can time-resolved physical observations of vehicle arrival, waiting, queues, lane/edge throughput and junction dynamics explain how a fixed route change created real network-wide effects orders of magnitude larger than the frozen assigned-count estimator predicted?

An **exploratory mechanism investigation** selected after observing Experiment 007 Test A; not new independent forecast validation, not a collective optimization study, and not proof of unique junction causality.

Original Test A scientific decision stays **NO-GO: 8/20 correct directions = 40% vs frozen 60% gate**. Test B remains unexecuted. Subjective journey quality remains deferred; individual and nonparticipant realized harm remain active as descriptive observations.

## Six and only six replay arms

| ID | Seed | Original arm | Specific change | Originally recorded contrast |
|---|---:|---|---|---|
| R1 | 4101 | I | baseline | reference |
| R2 | 4101 | probe2 | veh0000 | predicted external zero, realized external +3,181 network-seconds |
| R3 | 4102 | I | baseline | reference |
| R4 | 4102 | probe0 | veh0582 | predicted external −1.08, realized external +2,724 |
| R5 | 4102 | probe1 | veh0158 | predicted external +13.499, realized external +3,763 |
| R6 | 4102 | bundle | veh0582 and veh0158 | total +3,572, interaction −2,989 network-seconds |

Use only **unchanged original** inputs from GitHub Actions run 41380998833 (artifacts exp007-probe-4101 and exp007-probe-4102). Per-arm SUMO files must be copied from original ZIPs rather than regenerated with any policy generator.

Source frozen routing implementation merge: afa252c8d9ec31b247db49f2e2b0e30ce6d31fc8. Pinned simulation image: ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb (SUMO 1.28.0).

## Original source hashes to require before running

| File | Seed 4101 SHA256 | Seed 4102 SHA256 |
|---|---|---|
| network.net.xml | 7e5bb888a87bf9b7e52034275a5a848f7b6b319957f452a1d64bd54b93f01d52 | 5961868f82c6831d3d3d89f2fb22d1807cc47db9d5e6adaef11cd67e4ac76e7c |
| trips.xml | 66ab35c2ef7bb2aad10aba191012e8ce54b15470c07cf62ab4079966b7a7a130 | 15a47acfbb090c8bb5d469735127c151fe8cf4c7f6f5e1963c9269859e92d895 |
| I/routes.rou.xml | da86fc7b2311fc118d0735e7bf87f6b640eaac79bc6d80b69574722e3b78f57a | 5b669a1b8132fcb5f8e184faa66bf77d76c74d93a014582aceb0484c350747ac |
| probe2/routes.rou.xml | 13b9da58162f1df38001b4ffb14de3678237dc1d54098ef52d5db1c571a83013 | not selected |
| probe0/routes.rou.xml | not selected | 8e6bcafa2c9059eefd6558222308df1e86a8b886b1ce98d39561304465b83b0f |
| probe1/routes.rou.xml | not selected | 5e4cd19bd8e85c7d852e135a569d5678f2ea412bc0144ed28fa8962702c02470 |
| bundle/routes.rou.xml | not selected | df349601d418b83b05d3aa0776bee1f6e23d3101ef92771a385a45fed6df32b3 |

Validate complete original 43-member archives, attempt COMPLETE, scheduled 1,000 IDs per family, identical demand/route files, original SHA and exactly one/two altered route identities before any SUMO execution.

## Observation-only instrument changes

Original SUMO command must remain exactly the same regarding network, assigned route, random seed, car-following, signals and environment: network; route file; tripinfo, statistics, collisions, seed, no-step-log and log outputs.

Add only:
- One-second FCD trajectory output for all vehicles (vehicle ID, time, lane, position, speed, Cartesian x/y). No downsampling or selection.
- Per-vehicle route output with exit-times, if fully supported by pinned container.
- Additional-file **edgeData** and **laneData** detectors with a fixed **5-second period**, internal edges/lanes enabled, occupancy, sampled vehicle seconds, flow, speed and waiting. Files compressed where supported.

**Mandatory G1:** In the pinned SUMO 1.28.0 container, inspect sumo --version and sumo --help for every added command-line option, plus validate detector XML definitions before any sim. Unsupported core output or version mismatch = STOP and report; never silently omit critical fields.

## Equivalence and interpretation gates

**G0:** Original source byte hashes, route and demand identity, six exact cases checked; no missing artifact.

**G1:** Version, schema and flags checked without simulation.

**G2:** Compare original historical tripinfo with each instrumented replay for **all 1,000 matched driver IDs**:
- Depart, arrival, duration, departDelay, waitingTime and timeLoss **per driver and field within 0.02 seconds** (tighter if original quantization permits).
- 1,000 completed trip identities, unchanged scheduled departures, same route sequence and 100% completion.
- Exactly match originally observed structured collisions, emergency-braking and emergency-stop fields and collision-file events.
- Reconstruct signed total network changes, single-driver self/external effects and the seed-4102 bundle joint-minus-single interaction within **0.02 network-seconds per contrast** from printed original data.
- If *any* G2 field fails, **no physical inference from that replay**; preserve and report the failed attempt. Do not loosen the thresholds afterward.

**G3:** All 1,000 IDs represented in FCD over their actual active intervals; monotone 1-second timestamps, usable lane/position/speed, route-exit coverage, 5-second measured edge/lane interval data through last arrival. FCD near-stop primary threshold ≤0.1 m/s, optional descriptive sensitivity ≤1.0 m/s. If absent or corrupt, observation-insufficient, not mechanistically proven.

No claim of a causal junction bottleneck until there is temporally ordered route divergence → localized queue/flow shift → secondary driver effect and competing explanations are evaluated. Even then it is a candidate physical mechanism: queue/waiting mediators were not separately randomized.

## Analysis (only if G2 and G3 succeed)

1. Seed 4101 predicted-zero veh0000: compare 30-second assigned-count forecast footprint to actual observed edge transitions, 5-second physical occupancy and queue/throughput changes.
2. Seed 4102 veh0582 sign reversal and veh0158 magnitude error: identify timing of changed driver approach, blocked/junction episodes, queue/flow evolution, and spread to unchanged-route drivers.
3. Seed 4102 four-arm joint interaction: calculate J = (bundle − I) − (probe0 − I) − (probe1 − I) using total arrival-minus-scheduled-departure time for all 1,000 drivers; original expected −2,989 network-seconds. Examine spatial/temporal interaction without assuming a unique mediator.
4. Decompose actual total effects into insertion delay plus completed-trip duration. SUMO waiting already contributes to duration; timeLoss is not an additional additive component.
5. Retain participant and nonparticipant matched individual harm distributions. No inference of human consent or real-world performance.

## Stopping, reporting and authorization boundaries

One original arm execution per selected case: **six maximum**. No replacement seeds, expanded topology, changed route candidates, model tuning, Experiment 007 Test B, or user-facing publication. Failed executions must be preserved. Finish with **one consolidated scientific report** and machine-readable readback/gate results, links to raw measurement artifacts, original fingerprints, observation coverage and explicit limitations.

If G0/G1 fails, no replay should start. If G2 fails, stop causal interpretation and record equivalence failure; a successful workflow run is not a scientific PASS. If G3 fails, report insufficient instrumentation. If all gates pass, report only supportable candidate traffic mechanisms; unchanged original Test A NO-GO.

This document is the **frozen scientific protocol**, not evidence that six simulations have run. It must be merged before execution starts.
