# Post-Experiment 007 — Six-Run Instrumented Replay: Final Scientific Report

**Completed:** November 2, 2026. **Decision:** **VALID exploratory replay; original traffic outcomes reproduced; new time-resolved evidence supports large, spatially distributed queue-associated and timing-sensitive network effects. The unique causal bottleneck remains unidentified.** No new optimizer, calibration, route generation, test seed or Experiment 007 Test B was executed.

## Executive finding

After the P0–P3 archival investigation identified a severe **structural limitation in the assigned-demand externality estimator**, we conducted the separately approved six-run instrumented replay on the original fixed Experiment 007 routes, demand and SUMO 1.28.0 pinned image. All **six of six replays** passed exact per-driver original tripinfo comparison, including all originally recorded event fields. The replay generated one-second vehicle FCD trajectories, vehicle-route edge exit times, and five-second edge/lane measures including internal junctions.

**Two distinct empirical results now coexist:**

1. **The old estimator's marginal externality signal was mathematically inadequate for these particular equal-nominal-free-flow swaps.** The prior P0–P3 report established \`predicted_total_delta = 2 × predicted_self_delta\` and therefore \`predicted_external_delta = predicted_self_delta\` to numerical precision for the 20 originally selected probes. This is a model-structure finding, not merely a noisy physical measurement.
2. **The actual traffic response was strongly coupled and time-dependent.** A single changed assigned road-edge sequence altered waiting and arrival times across many other vehicles; time-resolved trajectories show pronounced 30-second forecast-bin mismatches and temporally shifting concentrations of stopped-time exposure. Two simultaneous route changes were not additive. This is strong **observational mechanism evidence**, not definitive identification of a single bottleneck's causal mediated effect.

**Original scientific history remains unchanged:** Experiment 007 Test A failed 8/20 predicted sign agreement (40% vs prespecified 60%) and received NO-GO for this estimator; its conditional collective-policy Test B was **not run**. No claim is made that a new or existing cooperative policy outperforms capable independent routing.

## 1. Design, execution and provenance

Prospective source of scope: [six-run specification](POST_EXP007_SIX_RUN_INSTRUMENTED_REPLAY_SPEC_AND_PLAN.md), followed by [separately frozen execution protocol](POST_EXP007_SIX_RUN_INSTRUMENTED_REPLAY_FROZEN_PROTOCOL_V1.md), both merged before any replay simulations.

**Original immutable input:** [Experiment 007 Test A source run 41380998833](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833), original seed artifacts exp007-probe-4101 and exp007-probe-4102. Pinned SUMO container digest \`ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb\` (SUMO 1.28.0). Original network, 1,000 trip IDs, scheduled departures and exact original per-arm route files were hash-verified. The original 30-scenario Experiment 007 suite was NOT rerun.

**Replayed exactly six predefined arms:**

| ID | Original seed | Arm | Assignment change | Purpose |
|---|---:|---|---|---|
| R1 | 4101 | I | none | independent-route baseline |
| R2 | 4101 | probe2 | veh0000 | predicted-zero externality that harmed others |
| R3 | 4102 | I | none | independent-route baseline |
| R4 | 4102 | probe0 | veh0582 | forecast/actual externality sign reversal |
| R5 | 4102 | probe1 | veh0158 | externality magnitude error |
| R6 | 4102 | bundle | veh0582 and veh0158 | original nonadditive two-change contrast |

**Execution trace:**
- [Frozen protocol PR #47](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/47).
- [Execution implementation PR #48](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/48), merge \`dc1e29803f61dfb172fe4523cb74ab91704f9d48\`. The implementation was placed under \`research/replay\` to avoid retriggering the already concluded Experiment 007 30-scenario workflow.
- [Six actual replay executions in run 41518373285](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41518373285): pinned source hashes and tool capability preflight succeeded, all **six individual replay and G2-equivalence jobs succeeded**, and all six original route/observation/trajectory artifacts were uploaded. The first consolidated evaluation job had a **downloaded-artifact directory naming error**, unrelated to scientific equivalence; the top-level run is thus marked failed. **Do not conflate that workflow status with a failed SUMO experiment.**
- [Aggregation-only recovery PR #49](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/49) and [successful recovered scientific audit run 41519190750](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41519190750): reads the original six instrumented artifacts with unmodified evaluator code; no SUMO rerun, alternate inputs, post-hoc thresholds or model changes.
- [Frozen analysis code](../research/replay/exp007_instrumented_v01.py). Original source/route/demand checks are preserved in the runner; G2/G3 and edge-time differences are reproducible using the six instrumented archive artifacts.
- [Scientific audit ZIP](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41519190750/artifacts/13176677252) contains validated arm coverage, original network contrasts and five-second edge-waiting differences. Raw per-arm artifacts are available under the original six-run workflow. These GitHub Actions artifacts have finite retention; their principal results and underlying methods are permanently recorded here.

**No subjective journey quality measures or public social-media publication** were initiated.

## 2. Mandatory validity gates — ALL PASSED

| Gate | Verified outcome |
|---|---|
| **G0 frozen original input** | Exact network and route SHA256, original 43-file archive families, 1,000 original identities and exact one-/two-route changes |
| **G1 pinned options** | SUMO 1.28.0 and required passive FCD, vehroute exit-time and edge/lane measurement options available |
| **G2 historical trip outcomes** | **0.00 second maximum per-field deviation** for all 1,000 driver records in each of six arms across depart, arrival, duration, departDelay, waitingTime and timeLoss; original collisions/emergency event fields also matched |
| **G3 observations** | Six valid FCD datasets covering all 1,000 vehicle identities, six complete vehroute edge-exit files and five-second edge/lane interval measurements covering the physical simulation duration |

Together the six runs comprise **6,000 instrumented vehicle trip records**. All vehicles completed their trips and all historical network contrasts reproduced *exactly*.

**Observation coverage:** FCD recorded 203,716 and 206,845 vehicle-time samples for seed 4101 I/probe2, and 211,536, 214,170, 215,483 and 215,132 samples for seed 4102 I/probe0/probe1/bundle. These are **samples of moving or stopped in-network vehicles**, not independent driver identities.

Recorded structured simulator safety counts matched the originals. This establishes no real-world safety equivalence.

## 3. Original network effects reproduced — with physical cost components

Positive contrasts mean **more** total scheduled-departure-to-arrival travel time than baseline. The waiting-time component is already part of duration; \`timeLoss\` is a separate diagnostic and must not be added.

| Fixed intervention versus same-seed I | Realized network elapsed delta (network-seconds) | Difference in completed-trip durations | Insertion-delay difference | Recorded waiting-time difference |
|---|---:|---:|---:|---:|
| 4101 probe2 — veh0000 | **+3,177** | +3,129 | +48 | **+2,829** |
| 4102 probe0 — veh0582 | **+2,626** | +2,634 | −8 | **+1,357** |
| 4102 probe1 — veh0158 | **+3,935** | +3,947 | −12 | **+3,419** |
| 4102 bundle — both | **+3,572** | +3,596 | −24 | **+2,594** |

**Interpretation:** Insertion delay is **not the dominant aggregate component** of these tested effects. Waiting changes are substantial, but the relation is not 100% for every arm: for the probe0 comparison, waiting changed by +1,357 of +2,626 network-seconds, leaving substantial non-stopped duration effects. The exact causal mediator remains open.

**One-second FCD independent near-stop crosscheck (≤0.1 m/s):**

| Arm | Recorded FCD near-stop vehicle-samples, baseline → intervention | Change |
|---|---:|---:|
| 4101 probe2 | 47,779 → 50,583 | **+2,804** |
| 4102 probe0 | 51,867 → 53,229 | **+1,362** |
| 4102 probe1 | 51,867 → 55,296 | **+3,429** |
| 4102 bundle | 51,867 → 54,472 | **+2,605** |

Because FCD samples each active vehicle about once per simulation second, these changes approximate near-stopped **vehicle-seconds** and broadly corroborate tripinfo waiting-time differences (2,829, 1,357, 3,419, 2,594 seconds respectively), notwithstanding sampling threshold/step semantics. This is powerful evidence that actual stopped-time exposure changed, **not** proof that any particular junction caused the network-wide difference.

**Original externality versus self effect:** 4101 probe2 changed target veh0000's trip by **−4 seconds**, while the other 999 drivers gained/lost a net **+3,181 seconds**; 4102 probe0 changed veh0582's time by **−98 seconds**, while other drivers incurred net **+2,724**; 4102 probe1 changed veh0158's time by **+172**, with **+3,763** among others. Bundle total +3,572 with both target drivers combined +24 and the other 998 drivers +3,548. No claim of full-policy individual fairness follows from these exploratory probes.

## 4. Forecast edge-entry timing errors are now directly observable

The frozen estimator's path footprint placed planned arrivals in **30-second bins** based on free-flow timing and a previously frozen per-edge correction. We compared these predicted bins with the **first observed FCD 1-second lane sample** on each external route edge (approximately rather than exact continuous-time road entry). This is an exploratory reconstruction, not an independent calibration experiment.

| Driver and fixed scenario | Forecast bins different from observed, of route edges | Mean absolute predicted-vs-observed first-sample entry-time difference |
|---|---:|---:|
| 4101 veh0000 under I | 2 / 6 | 11.1s |
| 4101 veh0000 under probe2 | 2 / 6 | 12.3s |
| 4102 veh0582 under I | 11 / 12 | 109.9s |
| 4102 veh0582 under probe0 | 7 / 12 | 24.9s |
| 4102 veh0158 under I | 11 / 13 | 58.4s |
| 4102 veh0158 under probe1 | 11 / 13 | 49.5s |
| 4102 veh0582 under bundle | 5 / 12 | 17.4s |
| 4102 veh0158 under bundle | 11 / 13 | 40.4s |

**Concrete coupled example:** On route edge **C6C5**, veh0158 (same planned route in probe1 and bundle) was first observed at **368 s** in probe1 but **329 s** in the bundle—**39 seconds earlier** when veh0582's different route change was also applied. The model's nominal-bin prediction for that edge was approximately **284.8 s**, materially different from both observed entry times. This identifies a realized **route-assignment interaction on an unchanged target route**, without identifying a unique downstream queue mediator.

The selected times and bin mismatches support the hypothesis that the old forecast-clock and assigned-demand approximation missed important traffic dynamics. Because the prior structural identity already limits the externality signal, **better arrival-time estimates alone cannot be assumed to rescue collective route ranking**.

## 5. Localized edge-time waiting patterns observed — not a unique causal bottleneck

Five-second edgeData records (internal junctions included) now identify **where and when** the simulated waiting measures diverged. Selected synthetic-road examples, each relative to the same seed's I baseline:

| Scenario | Strong edge-time contrast | First five-second interval on that edge with ≥10s absolute waiting difference | Important interpretation |
|---|---|---:|---|
| 4101 probe2 | **D5E5**: +1,307s cumulative signed waiting difference (1,583s absolute variation across intervals), largest interval near 320s | 190s | Changed route first diverged near **64s**; later effects spread across numerous roads |
| 4102 probe0 | **C4C3**: +903s cumulative signed waiting difference (1,101s absolute), peak near 305s | 250s | Substantial localized delay growth, but other edges simultaneously lost waiting |
| 4102 probe1 | **D6C6**: −1,431s signed waiting difference (1,699s absolute), with **E6E5** +1,619s signed | 165s on D6C6; 210s on E6E5 | Clear congestion redistribution, with some edge locations improving and others worsening |
| 4102 bundle | **D6C6**: −2,107s signed waiting difference (2,131s absolute), with **D3E3** +1,464s signed | 165s on D6C6; 200s on D3E3 | Strong joint spatial response; does not identify unique causal interaction source |

These are **synthetic grid edge IDs**, not real neighborhoods or publicly road-verified bottlenecks. Signed and absolute waiting differences can reflect offsetting temporal phases, and such interval sums do not directly equal the tripinfo network-wide wait delta in a mechanistically causal decomposition.

**Temporal ordering, exploratory:** the altered target veh0000 first entered a diverging edge around 64 seconds in seed 4101; the earliest ≥10-second edge-interval waiting difference anywhere in that pair occurred around 90 seconds. In seed 4102, veh0158 diverted around 48 seconds, while the first material five-second waiting difference was observed around 85 seconds. These are consistent with downstream traffic consequences, **not conclusive proof** of a unique chain of queue spillback.

### Important alternatives and limits

- Changes in 5-second edge waiting could be effects, intermediates, or co-occurring consequences of route assignments. Queue mediators were **not separately randomized**.
- Counterfactual FCD traffic positions reveal localized stopped groups and edge entry timings, but do not independently identify the contribution of every junction to the final network total.
- This analysis selected just **two seeds and four comparisons after seeing the failed prediction outcomes**. No new statistical test establishes generality across all feasible route changes, network topologies or real roads.
- Detailed lane-specific back-propagation of queue fronts and whether a named intersection's supply or discharge is the *dominant* causal mediator require a distinct falsifiable intervention. We should not claim that such uniqueness has been proven.

## 6. Two-route nonadditivity confirmed with full physical instrumentation

Using the exact original four arms on seed 4102:

\[
J=(C_{\rm bundle}-C_I)-(C_{\rm probe0}-C_I)-(C_{\rm probe1}-C_I)
=3572-2626-3935=\mathbf{-2989}\ \text{network-seconds}.
\]

The original estimator's static cost proxy predicted no comparable interaction in this seed. Instrumented FCD and five-second edge waiting reveal changed congestion timing (including the 39-second C6C5 entry difference for veh0158) and simultaneous positive and negative localized waiting changes.

**Conclusion supported:** Under these frozen SUMO conditions, the realized response to two route changes is **not** the sum of separately realized responses. It is consistent with coupled traffic dynamics.

**Not established:** That queue at D6C6, D3E3, C6C5 or any single intersection was the unique or quantitatively identified cause of −2,989 network-seconds. A physical intervention on the candidate bottleneck would be required to estimate that particular mediated causal pathway.

## 7. Scientific disposition: which hypotheses advanced?

| Mechanism candidate from the original investigation | Status after instrumentation |
|---|---|
| **Estimator mathematical structure conflates self and external cost** | **Verified previously**, unchanged by this replay |
| **Physical road-entry timing disagrees with forecast bins** | **Directly observed in selected traces**, including 11/12 and 11/13 bin disagreements in the 4102 baseline targets |
| **Traffic waiting and queue-associated changes contribute to realized network effects** | **Strong direct descriptive support** from both tripinfo and FCD near-stop samples; altered edge-time waiting across road segments |
| **Departure insertion explains most network travel-time shift** | **Disfavored as dominant** in these four comparisons; separate insertion differences −24 to +48s while total contrasts +2,626 to +3,935s |
| **Joint route assignments have nonlinear effects** | **Directly measured**, J = −2,989 network-seconds in frozen bundle |
| **A particular junction or spillback cascade is the unique causal mediator** | **Not identified**. Edge/time candidate signals now available but no independently randomized physical-junction control |
| **An improved prospective network-externality estimator will succeed** | **Untested**. New model could be proposed; confirm on new independent seed/route perturbations before policy Test B |

## 8. Decision and future research boundaries

**Replay outcome: VALID observational study.** G0–G3 all passed, six historical outcome reproductions exact, and the new high-resolution physical measurements support timing-sensitive, queue-associated network redistribution and nonadditivity in the selected scenarios.

**No new routing-performance GO.** Experiment 007 Test A is still NO-GO for the tested marginal-externality estimator. Test B was never run. The current study did **not** fix the estimator or prove a collective efficiency advantage. Individual fairness remains part of any future prospective policy experiment; subjective experience remains deferred.

**Single next scientific decision:** Before any new model tuning or collective optimization test, determine whether the priority is to (a) specify a **prospective, junction/queue-aware marginal externality estimator** with clean independent validation, or (b) test one **physical bottleneck hypothesis** with a separately controlled intervention to identify a mediator. Option (a) fits the original routing objective; option (b) is needed if a uniquely causal physical explanation is the goal. Neither is automatically authorized by this report. Preserve the original six raw instrumented ZIPs and the recovery audit as finite-retention attachments, and make their data provenance explicit.

**External validity:** Synthetic 10×10 SUMO network, pinned model, only two post-outcome selected seeds, no actual human compliance, no observed voluntary consent, no real-world driver safety or navigation superiority inference.

## 9. Data inventory and reproducibility

- [Original frozen Test A simulation run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833)
- [Six original-input, instrumented replay artifacts (run 41518373285)](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41518373285); each contains source commands, original-hash check, exact tripinfo/statistics, FCD, vehroute, edgeData, laneData and G2 attempt manifest.
- [Read-only recovered scientific audit run 41519190750](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41519190750) and [audit artifact 13176677252](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41519190750/artifacts/13176677252).
- [Frozen data-evaluation source](../research/replay/exp007_instrumented_v01.py): independent tripinfo equality, route counts, FCD and detector coverage, bundle interaction, edge-time differences.
- [Compact permanent replay outcomes](results/exp007_sixrun_instrumented_summary.csv): per-arm original contrast and waiting/insertion changes; [forecast/observed target edge timing summary](results/exp007_sixrun_target_edge_clock_summary.csv); [important synthetic edge-time waiting patterns](results/exp007_sixrun_edge_waiting_hotspots.csv).
- Original archive artifacts are scheduled for expiration **December 2, 2026 UTC**. The permanent report, analytical source, and compact derived data are retained in the repository; preservation of full raw FCD/lane/edge ZIPs requires separate storage or durable mirroring because they exceed the appropriate size for these report documents.

**Scientific completion criterion achieved:** six fixed replay attempts, all gate checks passed, original outcomes preserved, descriptive mechanism evidence extracted, unique causal bottleneck explicitly unresolved, one bounded future scientific decision identified.

**Publishing:** No LinkedIn or X publishing has been initiated. Visual-first external communication would require separate review and explicit approval.
