# Cooperative Traffic Research — Experiment 007 Post-Test-A P0–P3 Mechanism Investigation

**Completed:** November 2, 2026.  
**Status:** **Read-only archived-evidence mechanism investigation COMPLETE (P0–P3).** No SUMO runs, altered frozen outcomes, new route policy, new calibration or Test B.  
**Scientific result:** A **structural inadequacy of the assigned-demand externality proxy is demonstrated for the 20 selected probes**, alongside substantial **descriptive network-wide, queue-associated effects**. The specific physical origin and causal bottlenecks of the realized effects **remain unidentified**.

## Executive finding

We independently audited **all five original Experiment 007 Test A archive families (4101–4105)**, every one of their **six arms** (30/30), and 20,000 matched driver comparisons across the twenty individual route perturbations. The original frozen conclusions reproduced exactly:

- **8/20 (40%)** correct predicted externality directions, below the original **60%** Test A gate; five material effects predicted as zero.
- Frozen mean absolute prediction error **1,801.7100 network-seconds** across the twenty purposively selected probes.
- Predicted externality range **−3.2397 to +13.4989 network-seconds**; realized range **−3,777 to +4,328 network-seconds**.
- **Five** two-swap bundles exhibited nonzero realized interaction effects: **+218, −2,989, −2,672, −1,930, −1,502 network-seconds** (one per seed).
- **Test A remains NO-GO; Test B was not executed.** No collective route-optimization benefit/fairness outcome is established or refuted.

**New and strongest mechanism finding:** In all twenty original scenarios the predicted network-wide cost delta was **twice the predicted own-driver cost delta** to within **9.6×10⁻¹⁴ seconds**, implying \`predicted_externality = predicted_self_delta\` to the same precision. Every tested route swap had **exactly equal nominal free-flow travel time** and uniform lane/speed properties. For these probe conditions, the supposed estimate of consequences for other drivers **was not a distinct independently informed prediction of traffic interactions**: it was algebraically linked to the own-driver prediction. This explains the signal's lack of distinctiveness and its five predicted-zero effects; it does **not** by itself explain the exact realized multi-driver delays.

## Evidence and reproducibility

Primary frozen sources:

- [Original Experiment 007 protocol](EXPERIMENT_007_FROZEN_PROTOCOL_V1.md) and [original frozen Test A scientific report](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md)
- [Exact unchanged implementation](../experiments/experiment_007/run_v01.py), frozen implementation merge **\`afa252c8d9ec31b247db49f2e2b0e30ce6d31fc8\`**
- [Original Test A simulation execution](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833): seed-specific original 43-file ZIP artifacts, each one \`I\`, \`probe0\` to \`probe3\`, \`bundle\`
- [Recovered original Test A aggregation](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41381425091); reused all original archives, never reran scenarios
- [Published investigation plan](POST_EXP007_EXTERNALITY_ESTIMATOR_MECHANISM_INVESTIGATION_PLAN.md)
- [Reproducible new P0–P3 standard-library Python audit source](../research/audits/exp007_p0_p3_audit.py)
- [Successful PR-only archive audit](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41513678811) and [successful merged-main audit](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41513917088), each reading **only** original archived artifacts, without importing or invoking SUMO
- The corresponding \`exp007-p0-p3-archive-audit\` workflow artifact contains SHA256 per-file manifest, 30-arm coverage, twenty recomputed predicted/realized contrasts, **20,000 per-driver differences**, subgroup summaries, five bundle interactions, and structured exception records. Original GitHub Actions artifacts are scheduled to expire on **December 2, 2026**; see preservation note below.

The independent audit recomputed predictions from original \`network.net.xml\`, \`trips.xml\`, \`I/routes.rou.xml\`, all assigned edge-time bins and the frozen model equation—not by copying original prediction totals from its \`probe-results.json\`. Realized contrasts were independently summed from actual matched \`tripinfo.xml\` records for **all 1,000 drivers**.

### P0 — Integrity verification: PASSED

- Five original seed archives inspected: **43 original files per seed (215 total archive members)**; original network, demand, all six route XMLs, all six tripinfo XMLs, SUMO statistics, collision files and logs present.
- Every within-seed arm contained **1,000 matched unique driver identities** and complete tripinfo. Network/OD/scheduled departure were the same across all arms per seed.
- The four individual probes changed **exactly one assigned road-edge sequence**, and each two-route bundle changed the intended **two**; all other assigned road-edge sequences remained unchanged.
- For each original per-driver record, reconstructed elapsed journey time equaled **actual arrival minus scheduled departure = completed duration + actual insertion delay**, up to XML rounding precision. This prevents mistaking insertion delay for a separate uncounted journey cost.
- Predicted self/total/external deltas independently reproduced all 20 original records to numerical precision. Realized sums reproduced all original per-probe and bundle contrasts. Sign gate reproduced unchanged.
- All 30 original simulator logs identify **SUMO 1.28.0**. Driver \`speedFactor\`, \`departLane\` and recorded \`rerouteNo\` were unchanged between baseline and treatment across all five seed families. This supports within-seed input comparability; it does **not** prove exact reproducibility under a fresh simulator replay or identify a physical queue.
- Safety/exception fields were actually captured. Across the five seed families the independent baseline had **one recorded emergency-braking event**, and \`probe0\` also had **one**; other probe/bundle arms recorded zero. All recorded collision counts were zero. These simulator events do not imply real-world road safety.

The original Experiment 007 reporting and the 60% gate remain untouched.

## P1 — Mathematical mechanism of the predictor: STRUCTURAL LIMITATION VERIFIED

The original assigned-demand proxy uses a 30-second edge-time bin and a static assigned count q. For an edge e with nominal free-flow time f and capacity proxy c, modeled total travel cost per edge-time bin is:

\[
F_e(q)=f_e \left(q+\frac{q^2}{c_e}\right).
\]

The code computes \`predicted_total_delta\` by replacing one route's footprint in aggregate q and summing the changes in F. It computes \`predicted_self_delta\` as the cost of the chosen driver's old route under old q versus alternative route under new q. Then it defines \`predicted_external_delta = predicted_total_delta − predicted_self_delta\`.

For one feasible swap with unit occupancy in each unique edge-time bin, algebra gives:

\[
\widehat{\Delta C}_{total}-2\,\widehat{\Delta T}_{self}
=\sum_{e\in old\setminus new} f_e(1+1/c_e)
-\sum_{e\in new\setminus old}f_e(1+1/c_e).
\]

For **the actual twenty selected Test A probes**, the old/new paths have the same total nominal free-flow time and all involved external edges share the same speed and lane-count properties, so the right-hand side cancels. Thus:

\[
\widehat{\Delta C}_{total}=2\,\widehat{\Delta T}_{self},
\qquad
\widehat{\Delta C}_{external}=\widehat{\Delta T}_{self}.
\]

This was verified numerically from reconstructed original input assignments across all 20 cases: **max absolute discrepancy 9.5923×10⁻¹⁴ seconds**. Importantly, the identity is **conditional on this route class and cost function**; it is not a theorem that all possible routes or real traffic networks have equal self and external costs.

**Implication:** Although the estimator formally subtracts a modeled self-cost from modeled total cost, it does **not independently encode multi-driver queue, junction discharge, spillback or traffic-wave changes** in these probes. The five predicted zeros reflect a cancellation in this proxy, not evidence that there would be no traffic consequences. Such an identity is best described as a **structural limitation of the chosen model under this test design**, not automatically a software arithmetic defect or evidence that accurate network-externality prediction is impossible.

**Independent diagnostic caveat:** This study did not refit or validate an improved model on new held-out perturbations. The original 20 selected probes cannot support a claim that a different cost formula would work.

## P2 — What actually happened to other drivers?

Reconstructing each selected singleton comparison across the **999 other vehicles** yields the following *descriptive averages across 20 probe comparisons* (not independent-sample inferential estimates):

| Metric | Mean per route-change probe | Interpretation |
|---|---:|---|
| Other drivers with longer realized journeys | **436.3 of 999** | Widespread adverse impact |
| Other drivers with shorter realized journeys | **421.85 of 999** | Widespread offsetting benefit |
| Other drivers unchanged in elapsed time | **140.85 of 999** | Substantial responsiveness across network |
| Net realized externality | **+601.25 network-seconds** | Mean signed total; individual probes range strongly positive and negative |
| Other drivers' total completed-duration change | **+604.40 network-seconds** | Time after actual insertion |
| Other drivers' insertion-delay change | **−3.15 network-seconds** | Insertion is not dominant in mean absolute network accounting |
| Other drivers' recorded waiting-time change | **+605.60 network-seconds** | Strong descriptive queue/stopped-time association |
| Ten largest absolute individual contributions | **5.52% of total absolute individual changes**, on average | The magnitude of changes was dispersed, not dominated by ten extreme drivers |

The signed net change is a balance of substantial positive and negative individual changes. Averaging across selected probes is descriptive and **not a treatment effect estimated over randomly sampled possible route changes**.

Per-probe signed externalities and waiting-time changes had a **descriptive Pearson correlation approximately 0.888**, but at least several probes showed **opposing signs** between net waiting and net elapsed-time changes. This neither establishes waiting as a causal mediator nor means stopped time explains every observed contrast. The original metric \`timeLoss\` is a separate SUMO diagnostic and is not added to \`waitingTime\` or elapsed time.

**Physical network spillover:** The routes of all other **999** vehicles were held fixed between each probe and its baseline, but hundreds of their realized trip times changed. That directly identifies a **whole-network counterfactual response in the simulator**, not the particular physical road or intersection producing it. About **767 of the 999** other drivers per probe (mean) did not share any *planned road edge* with either the replaced driver's old or new route, yet that broad subset also showed nonzero aggregated changes. This finding is consistent with connected network effects, but route-edge nonoverlap is not evidence of any particular path of propagation.

**Participation:** The prospective roster comprised 500 eligible and 500 noneligible drivers. With the changed target among eligible drivers, all **500 nonparticipants** were unchanged in planned route but could experience changed congestion. Descriptively, they accounted for approximately **+189.75 network-seconds** of signed externality per probe on average; the **other 499 participants** accounted for approximately **+411.50**. Both groups had gains and losses. This is not a full policy-level fairness result, because Experiment 007 Test B was never run.

**Departure phase:** A secondary descriptive analysis grouping scheduled departures into five 40-second bins found both positive and negative aggregate outcomes. Exact OD pair strata were generally too small to support stable OD-specific harm inference (on the inspected 4101 baseline, 992 unique origin-destination pairs among 1,000 vehicles). No causal congestion location is assigned to any origin/destination group.

### P2 — Bundled routes and nonadditivity

Five original paired two-swap comparisons measured **realized joint effect minus the sum of individually measured effects**:

| Independent seed | Realized interaction, network-seconds | Original model predicted interaction |
|---|---:|---:|
| 4101 | +218 | 0 |
| 4102 | −2,989 | 0 |
| 4103 | −2,672 | 0 |
| 4104 | −1,930 | approximately −2.16 |
| 4105 | −1,502 | 0 |

This reveals large differences between actual coupled traffic responses and additivity assumptions in these **purposively selected small bundles**. It supports investigating coupling and congestion feedback, but is not a unique identification of a queue, signal or junction as the mediator.

## P3 — What can and cannot be established from archived evidence?

| Candidate hypothesis | Evidence status | Scientific interpretation |
|---|---|---|
| **H1: Structural proxy's externality is not distinct** | **Verified** for all 20 probes by source-level algebra and independently recomputed costs | Strongest currently established mathematical mechanism of signal inadequacy |
| **H2: 30-second predicted edge-arrival bins are misaligned with actual edge entries** | **Unidentified** from existing original data | No native per-edge entry timestamps or FCD traces; cannot assign a mismatch to specific times/roads |
| **H3: Junction queues, discharge and spillback produce large physical effects** | **Descriptively plausible**, waiting and unchanged-route contrasts support network interactions | Specific causal physical bottleneck, queue source, and causal delay propagation **not established** |
| **H4: Departure insertion changes explain the large contrasts** | **Disfavored as dominant explanation in aggregate accounting** | Mean net insertion change −3.15 network-seconds, while mean realized externality +601.25; individual probes may vary |
| **H5: Interactions between route changes matter** | **Observed** for five selected bundles | Joint effects were not equal to sums of individual effects; no unique physical mediator established |
| **H6: Different random driver characteristics caused comparisons** | **Disfavored by observed original metadata**, but not fully ruled out | Same vehicle ID-specific speedFactor/departLane/rerouteNo in all arms; same SUMO seed/version. No independent identical-input replay performed |
| **H7: Probe-selection bias affects generalizability** | **Established design limitation** | 20 nonrandom model-ranked probes, five independent demand seeds; cannot estimate population forecast accuracy or use 20 as independent inferential units |
| **H8: Spatial/temporal heterogeneity** | **Descriptive only; insufficient for causal location** | Depart-phase and route-overlap groupings show variation, but exact OD strata are sparse and edge-time trajectories absent |

The original ZIPs contained planned routes, completed-trip records, simulation statistics, collision logs, net geometry and demand records but **no time-resolved FCD traces, edge/lane detector records, or direct vehicle-by-vehicle road-entry timestamps**. Therefore **P3 cannot credibly identify a particular junction, bottleneck, spillback wave or causal temporal sequence** from this frozen evidence.

**Sampling and inference caveats:** The twenty individual probes were purposively selected using model-ranked estimated effects and share five independent baselines. Even the large counterfactual network-seconds are not equivalent to twenty independent randomized seeds or real-world conditions. We preserve original project results without altering Experiment 007's frozen gates.

## Final determination and smallest next discriminating action

**P0 complete:** Original identities, numeric predictions, outcomes and archival integrity independently verified.  
**P1 complete:** A restrictive algebraic coupling of self and external forecasts is demonstrated for the tested equal-freeflow route swaps.  
**P2 complete:** The impacts across other drivers, recorded waiting, insertion delay, participation groups and bundle interactions were reconstructed.  
**P3 complete:** We determined exactly what the archive can support versus what lacks temporal-spatial observability. The physical bottleneck cause remains **unidentified**.

**Recommendation:** Do not run Experiment 007 Test B, relax the failed gate, or merely tune the quadratic assigned-count penalty on these twenty seen outcomes. First consider a **separately authorized, six-run instrumented replay** of the original baseline/selected route changes to record actual edge arrivals, lane occupancy, queues and speed through time while preserving route assignments, SUMO version and seed. It would be *exploratory* (seeds chosen after seeing these results), and must pass an unchanged-tripinfo/instrumentation-equivalence check before interpreting traces. The [published investigation plan](POST_EXP007_EXTERNALITY_ESTIMATOR_MECHANISM_INVESTIGATION_PLAN.md#6-conditional-smallest-follow-up-trace-a-few-frozen-route-changes-not-a-new-routing-policy) proposes exact seeds/arms and falsifiable measurements.

An improved estimator would require **new independent validation** on unseen demand and route perturbations before a fresh cooperative optimization efficacy test. This report **does not authorize** the six-run instrumented replay. There is no new routing policy efficacy or fairness claim.

## Preservation, data and communication boundaries

The reproducible P0–P3 audit workflow explicitly uses archived run 41380998833, never launches SUMO, verifies 20,000 matched single-route driver contrasts and produces its own hashes, seed-level results and per-driver CSV. Original GitHub Actions artifacts expire **December 2, 2026 UTC**, so preserving copies of raw archives and permanent derivatives is important for long-term replicability.

**No publication to LinkedIn or X** occurred as part of this investigative research. If these findings are subsequently shared, prepare scientifically verified visual-first content using a single GitHub landing page and obtain explicit review and approval of both assets and captions. Individual fairness remains an active research safeguard; subjective quality of journey experience remains deferred.

---

**Scientific decision: P0–P3 COMPLETE, externality proxy structural limitation identified, exact physical bottleneck unresolved, Experiment 007 Test A original NO-GO unchanged and Test B not executed.**
