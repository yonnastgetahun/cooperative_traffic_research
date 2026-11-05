# Cooperative Traffic Research — E1-v2 D1 Mechanism Investigation Plan
## Archived edge-entry timing, queue propagation, junction discharge, and route-bundle interactions

**Date:** November 4, 2026  
**Status:** **INVESTIGATION PLAN COMPLETE; ANALYSES NOT EXECUTED UNDER THIS PLAN.**  
**Milestone:** E1-v2 post-development failure investigation, retrospective and explanatory.  
**Authorization boundary:** The user approved writing/publishing a research investigation plan, **not** changing the estimator, fitting a new model, launching SUMO, opening validation or policy Test B seeds, or publishing social updates. Future archival analyses, any diagnostic model replay, new instrumented SUMO observations, and E1-v3 implementation each require their own scoped execution decision.  
**Primary scientific question:** Why did a source-verified, junction-connection-aware E1-v2 counterfactual predictor continue to forecast *tiny changes in other drivers' elapsed times* while SUMO produced large positive and negative network effects and nonadditive responses to two simultaneous route changes?

## 0. Freeze the existing negative finding and its provenance

The completed [E1-v2 D1 development study](POST_EXP007_E1_V2_D1_FINAL_DEVELOPMENT_AUDIT_2026-11-04.md) executed the **frozen 60-arm study**, 10 independent synthetic demand seeds (build **6101–6106** and development-check **6111–6114**), with 1,000 matched original drivers per arm and all ten prediction locks generated **before** SUMO outcomes. The [permanent original research release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1v2-d1-development-nogo-2026-11-04) preserves **695 original member files** and their SHA-256 ledger.

**Immutable D1 result: DEVELOPMENT NOT QUALIFIED.** On the 16 frozen development-check single-route perturbations, independent-seed mean other-driver externality MAE in **network-seconds** was:

| Model | Development-check mean externality MAE |
|---|---:|
| B0 — Zero externality | **1,478.0625** |
| B1 — Frozen quadratic proxy | **1,478.3325** |
| E1-v1 — Original one-conflict-class queue model | **1,478.3125** |
| **E1-v2-J1 — Connection-aware junction model** | **1,478.5625** |

E1-v2 was **0.5 network-seconds worse than B0** instead of at least 10% better than the best comparator. It matched externality direction in **5/16 = 31.25%** materially nonzero cases instead of the required 60%, and improved versus each seed's strongest comparator on **1 of 4** check seeds instead of 3. The prespecified severe false-benefit flag was **zero**, but that is not evidence of well-calibrated decision safety: predicted externalities were tiny and often zero. Actual other-driver effects included substantial benefits and harms. No independent validation was started. **Test B was not run.**

**Other completed research:** Original Experiment 007 Test A remains **NO-GO**; original E1-v1 Stage 1D remains **DEVELOPMENT NOT QUALIFIED**. The [J0–J4 SUMO priority-junction audit](POST_EXP007_E1_J0_J4_PRIORITY_JUNCTION_VERIFICATION_FINAL_REPORT_2026-11-04.md) verified a static conflict-rule mismatch in E1-v1; E1-v2 addressed its junction movement representation, but that change did **not** qualify the externality predictions. The physical explanation for E1-v2's continued failure is **not established**.

**Sources to pin, unchanged:**
- Original research execution: [GitHub Actions 41966516110](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41966516110), execution commit \`a54b6f650b16a22b0eb5543bb507f9faf5eea034\`; original zipped artifact ID 13387764476, original wrapper SHA-256 \`c8b7e508ecbffd2c4b5ea7803dc83024780e1beecd42002c080ebf6b4d0c88e5\`. Distinguish original wrapper SHA from the repackaged permanent research-release ZIP SHA.
- [Frozen V2-D1 protocol and progression gates](POST_EXP007_E1_V2_D1_FROZEN_DEVELOPMENT_PROTOCOL_V1_2026-11-04.md), [one-time pre-outcome collector repair](POST_EXP007_E1_V2_D1_PREOUTCOME_COLLECTOR_PATH_REPAIR_2026-11-04.md), [independent original-archive audit](../research/audits/e1_v2_d1_archive_no_go_audit.py), and [verified numerical effect tables](results/exp007_e1v2_d1_all_arm_effects.csv).
- Frozen models \`research/externality_estimator_v2/network_evolution.py\`, \`scheduler.py\`, \`movement.py\`, \`counterfactual.py\` and \`research/externality_estimator/\` at the execution commit above; record every source blob SHA before retrospective analysis. Original SUMO image \`ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb\`.
- [SUMO official edge/lane mean-data semantics](https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html), [FCD output definition](https://sumo.dlr.de/docs/Simulation/Output/FCDOutput.html), and pinned SUMO 1.28.0 code for any version-sensitive interpretation. Distinguish lane/edge mean-data from E2 lane-area (queue) detectors and per-vehicle FCD.

**No reuse as an independent holdout:** Historic 4101–4105; E1-v1 5101–5114; and **all E1-v2 6101–6114** have been inspected. They can support *retrospective explanation*, **not** future untouched model testing. Keep provisional future independent-validation **6201–6212** and Test B **6301–6312** unopened, even under earlier conditional approval.

## 1. Actual measurement contract: what exists, what does not

Before testing mechanism stories, establish an **observation-availability matrix** from the 695-member archive. The V2-D1 simulation workflow delegates SUMO measurement collection to the previously frozen Stage 1D runner; prior execution reports describe original **5-second edgeData and laneData** streams, plus 1,000 tripinfo records and simulator logs per arm. **Their exact XML fields, time coverage, missing-value conventions, and internal-edge inclusion must be independently inventoried from the original files before any analysis is reported.**

| Quantity / research question | Existing source expected | Interpretive boundary |
|---|---|---|
| Each driver's scheduled departure and actual trip start/arrival | Frozen \`trips.xml\`, SUMO \`tripinfo.xml\` | Direct matched per-driver *trip* timing, including insertion delay; not the driver's edge-by-edge trajectory |
| Original E1-v1 and E1-v2 predicted full-trip elapsed times | SHA-locked \`predictions/predictions.json\` | 1,000 per-driver baseline and swap predictions; **no archived predicted vehicle-by-vehicle edge-entry clock** established |
| Actual arrivals and departures **across external road segments in 5s bins** | SUMO \`edgeData.xml.gz\` / \`laneData.xml.gz\`, if present and complete | Counts \`entered\`, \`left\`, \`departed\`, \`arrived\` are **aggregated**, not a list of which driver entered an edge at an exact second |
| Waiting, sampled vehicle-seconds, occupancy/density/speed by edge/time | Same 5-second mean-data | Traffic-state proxies; **waitingTime is included in elapsed journey time and is not an extra additive penalty** |
| Individual vehicle's exact edge-entry and junction crossing times | One-second FCD, timed vehroute exit events or equivalent | **NOT available in current V2-D1 archive unless P0 proves otherwise**; do not infer individual entry clocks from aggregated \`entered\` counts |
| True queue-tail distance, gap acceptance, movement-specific discharge | Position-resolved trajectories, appropriate area detectors, junction monitors or controlled instrumentation | **Not established by edge/lane mean-data alone**; no claim of uniquely causal queue propagation or turn service |

In SUMO edgeData, \`entered\` means vehicles entering the specified *edge* over an interval; \`left\` means leaving it. \`departed\` and \`arrived\` capture trip origins/destinations and affect count reconciliation. \`sampledSeconds\` is summed vehicle-presence time, not a trip count. No \`FCD\` should be claimed from standard \`edgeData\` merely because both are time-indexed.

**Critical missing forecast trace:** The frozen v2 prediction record serializes **full-trip predicted elapsed values** and aggregates, not a public per-edge or per-turn time sequence. The engine's internal evolution \`Event\` objects are not thereby proven to have been archived in D1. Therefore **model-vs-SUMO edge-entry timing error cannot be measured directly from these existing archives**. A later read-only *post-outcome diagnostic* model reproduction with exact unchanged model/input hashes could produce retrospective model-event traces, but these would be **new diagnostic outputs from a known-outcome scenario**, must be labeled contaminated, and require separate authorization. An exact vehicle-resolved SUMO timing comparison would additionally need a separately authorized *instrumented replay*, not just the existing detector archive.

## 2. Prospective explanatory hypotheses and falsifiable expectations

These hypotheses concern already-observed failures, not preregistered causal outcomes or selection of an improved model. Publish both consistent and inconsistent cases.

### T — Temporal misalignment and source insertion

**Candidate explanation:** Original E1/v2 clocks and coarse, one-second model eligibility misrepresent when demand actually enters roads and reaches constrained junctions. A small timing shift can change which vehicles compete during saturation, potentially amplifying one route's wider effects.

- **Observable in this archive:** 5-second \`entered/left/departed/arrived\` count contrasts per road and time; \`tripinfo.depart\` minus frozen scheduled \`trip.depart\` to quantify source insertion delay; all-driver arrival-time differences. Distinguish insertion and in-network durations.
- **Prediction consistent with T:** significant early edge-count/timing changes relative to baseline, followed by broader changes in waiting and completed journeys; notable source insertion contrasts, if present.
- **Contrary evidence:** large network elapsed differences despite little source-insertion and edge-flow temporal response in the recorded coverage.
- **Cannot establish:** which exact E1-predicted vehicle reached which edge early/late without a genuine model event archive; exact actual vehicle edge-entry clocks or causal amplification without new vehicle-level observation.

### Q — Congestion propagation, downstream receiving and queue redistribution

**Candidate explanation:** E1-v2 retains a one-lane link-wide FIFO, discrete upstream/downstream storage, and approximate discharge clocks that cannot reproduce the timing/extent of downstream blocking and near-stop queues in SUMO.

- **Observable:** matched 5-second external-edge waiting changes (vehicle-seconds), \`sampledSeconds\`, \`occupancy\`, \`speed\` and \`entered/left\` counts across connected upstream/downstream external edges; internal edge data separately if present.
- **Prediction consistent with Q:** a time-ordered, physically connected pattern of occupancy/waiting increases near constrained downstream links accompanied by less upstream discharge or later increases on feeder edges; substantial **positive and negative** waiting changes at different locations.
- **Contrary evidence:** observed time/edge effects not ordered along plausible paths, or network-time changes largely explained by measured insertion delay without the expected recorded in-network pressure response.
- **Cannot establish:** queue fronts, detailed vehicle blocking, or unique causal direction from 5-second averages alone; \`waitingTime\` is not a true pointwise queue-length detector.

### J — Junction approach/discharge and conflict-fidelity gap after the v2 fix

**Candidate explanation:** Static foe/priority correctness is insufficient because actual movement service also depends on dynamic vehicle presence, gap acceptance, priority waiting, internal junction lanes, short-term arrivals and receiving capacity. The v2 scheduler still approximates these processes.

- **Observable:** original 100 priority-junction topology, verified movement/request/foe/response matrices, inbound/outbound 5-second edge flow and waiting/speed/occupancy for associated external edges.
- **Prediction consistent with J:** sustained approach demand and waiting with limited recorded downstream \`left/entered\` throughput around selected junctions, even where static non-foe movements could coexist in principle.
- **Contrary evidence:** approaching volumes and discharge observations show no plausible constrained junction behavior, while large effects originate elsewhere (such as departure insertion).
- **Cannot establish:** specific simultaneous turn crossings, right-of-way compliance, gap acceptance, signal-phase mechanisms (these are **priority**, not signalized junctions), exact movement-specific discharge or physical causal capacity from aggregate edgeData.

### B — Two-route bundle nonadditivity and indirect shared influence

**Candidate explanation:** Two route swaps interact through queues, junction capacity and altered arrival times of unchanged-route drivers even if their planned routes have little direct overlap. E1-v2 may fail to predict this indirect network response.

- **Observable:** per-seed baseline I, the exactly **two singleton arms corresponding to the bundle's declared target IDs**, and the joint bundle; matched all 1,000 tripinfos; 5-second edge-state measures in all four arms.
- **Primary metric:** \`interaction_all = C(bundle) − C(single_a) − C(single_b) + C(I)\`, where \`C\` is **summed scheduled-departure-to-arrival time for all 1,000 drivers** in one arm; compute a separate E1-v2 predicted \`interaction_all\` from its stored *total* predictions. Do not combine singleton **externalities** directly because those exclude different selected target sets.
- **Observable auxiliary interaction:** for a *comparable additive field*, e.g. external-edge waiting vehicle-seconds aggregated across disjoint 5-second windows, calculate the analogous four-arm interaction; report spatial positive/negative contributions, not a uniquely causal edge.
- **Prediction consistent with B:** large joint-minus-single actual interactions that are absent or tiny in E1-v2, with time/edge detector differences distributed away from direct changed edges.
- **Contrary evidence:** matched whole-network interaction is near zero after correct four-arm bookkeeping; a preexisting summary or arm matching error explains the apparent signal.
- **Cannot establish:** a universally nonlinear cooperative routing benefit or statistically independent interaction distribution from these prospectively selected ten bundles.

### A — Accounting, support and null-model alternatives

**Alternative mechanisms that must be ruled out:** a wrong departure-time denominator, completed-only cost, ignored insertion delay, uneven run durations, drift of source-network/route/demand IDs, missing/empty detector fields misread as zeros, failed route-change containment, prediction/label misalignment, one-second tick rounding, or simple near-zero forecasts that mimic the zero-externality baseline. A valid archive must pass these before physical bottleneck attribution.

**No post-hoc model rescue:** Never fit new parameters, alter the v2 clock, select alternative routes for better apparent score or call historic cases fresh validation under this explanatory plan.

## 3. Bounded investigation phases (F0–F5): NO SUMO

### F0 — Archive integrity, time fields and observability inventory

**Scope:** All **10 original seeds × 6 arms**, expected **60,000 trip records**, 10 prediction locks, five model-prediction records per seed, exact original route/demand/network hashes and archived SUMO measurement streams.

Operations:
1. Verify the preserved ZIP's per-member SHA-256 ledger and source commit, report exact member/file counts and compressed/uncompressed sizes. Distinguish the original Actions wrapper checksum from the new release ZIP.
2. Verify each arm's 1,000 identities and complete arrivals; one-route-change containment for probes, exactly two changed original planned routes for each declared bundle; no change of scheduled departure, OD, vehicle group or simulator physics across paired arms.
3. Inspect actual XML attributes and units, sample intervals, first/last \`begin/end\` times, internal-edge inclusion, missing/empty \`edge/lane\` rows and any optional FCD/vehroute traces.
4. Verify prediction JSON hashes and which driver-level versus link/turn-level forecast fields are actually serialized. Create a matrix with evidence levels: **available / reconstructible exactly / only aggregate / unavailable**.
5. Define a fixed joint clock axis, preferably 5-second original bins, **without shifting individual arms to align peaks**. If one arm finishes earlier, treat missing later zero-flow/waiting bins as zeros **only when validated by coverage and output configuration**. Keep missing/unknown status distinct from confirmed zero.

**F0 gate:** Any failed SHA, uncertain identity/departure alignment, unverified outcome source or ambiguous measurement unit means **STOP mechanism claims and publish an integrity limitation**. Earlier D1 NO-GO remains unchanged regardless.

### F1 — Whole-driver effect decomposition and forecast-compression diagnosis

Compute for every one of the 10×5 interventions, comparing its own same-seed baseline:
- \`Δself\` in **individual seconds** (for bundle, the two selected target IDs summed);
- \`Δexternal\` for all *other* original drivers, and \`Δall\` for all 1,000 drivers, in **network-seconds**;
- \`Δnonparticipant\` on fixed opt-out IDs; individual harm/tail distribution and >30s fractions as diagnostics only;
- insertion-delay contribution \`Σ_j[(actual_depart_j−scheduled_j)_arm−(actual_depart_j−scheduled_j)_I]\`;
- in-simulation duration contribution \`Σ_j[(actual_arrival_j−actual_depart_j)_arm−(actual_arrival_j−actual_depart_j)_I]\`; verify insertion + duration equals all-driver elapsed difference **without adding SUMO waitingTime separately**;
- signed and absolute errors for frozen B0, B1, E1-v1 and E1-v2, exact-zero model predictions, number of sign errors and sizes of realized effects for each prediction-sign bucket.

Produce per-seed and all-seed descriptive summaries. The **independent seed** is the replication unit; four single probes share a baseline. The predeclared D1 10%/60%/false-benefit gates must be displayed unchanged but **never re-evaluated after retuning**, since no retuning is authorized.

**Retrospective illustrative cases:** Use all 60 arms in quantitative tables; additionally show transparently post-outcome-selected examples **6112 probe2** (observed +3,215 others' network-s versus E1-v2 predicted 0), **6113 probe2** (−3,960 versus 0), **6111 probe3** (+1,847 versus +1), and **6114 probe2** (−2,929 versus 0). They are explanatory case studies, **not** a random sample or a new test of estimator generalization.

**F1 gate:** Complete self/others/total/insertion-duration reconciliation. Missing or ambiguous original departure fields stop the insertion analysis specifically, not automatically the valid full-trip effect audit.

### F2 — Aggregate edge-entry clock and queue-associated propagation

Using matched 5-second *SUMO-observed aggregate* \`entered/left\` counts, \`departed/arrived\`, \`waitingTime\`, \`sampledSeconds\`, \`speed\` and \`occupancy\` where actually present:

1. Construct fixed (seed, arm, external_edge, time_bin) tables and separate internal-edge tables if meaningful; map external road direction and graph adjacency.
2. Compute **counts and cumulative-count differences** for entered and left; report first divergence in a bin, peak differences, and lag ranges **at five-second resolution**, explicitly **not** exact vehicle entry time.
3. Compute signed +/− waiting vehicle-second changes, occupation/throughput changes and different-coverage denominators by time and edge. Do not sum mean speed or mean occupancy across intervals as if additive; compare them with weights or time-window descriptors.
4. Examine whether recorded downstream discharge reductions co-occur with later upstream buildup along **directed** adjacent roads. Create space/time diagrams (edge/time heatmaps, adjacency-lag records) including both increases and decreases. Treat graph distance and lag as association, not transmission proof.
5. Reconcile \`entered + departed\` vs \`left + arrived\` carefully in aggregate; if an edge's detector semantics, internal-edge handling or teleports prevent exact conservation, describe why instead of force-matching.
6. Measure how much of the all-driver elapsed contrast is accounted for by source insertion changes versus *other observed travel-time components*; compare queue-associated waiting signs with **total elapsed** signs, never claim waiting = externality.

**F2 gate:** If no valid edge/time observations survive coverage checks, return **INSUFFICIENT OBSERVATION**, not invented traffic waves. The presence of aggregated counts does **not** authorize claims about exact per-vehicle clock or uniquely caused queue propagation.

### F3 — Junction approach-discharge and physical plausibility

Join the original pinned 100 priority junctions and verified foe/response/index mapping from [J0–J4 evidence](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1-j0-j4-priority-junction-verification-2026-11-04) to each matched 5-second external-edge detector series.

- Summarize incoming approach \`left/arrived\` and outgoing \`entered/departed\` **separately**; explain why these are not necessarily exact unique turn movement counts.
- Report \`sampledSeconds\`, waiting and speed conditions of inbound external approaches and downstream receiving edges; use known physical connectivity and no invented signal phases.
- Compare near-junction external-edge flow/waiting signatures around the fixed example seeds and full-cohort distribution; avoid declaring a highest-waiting edge "the bottleneck" based only on its change.
- Review v2-J1 code's scheduling assumptions as source facts: one head per incoming lane, one-second clock, service tokens, \`cont=1\` conservative exclusive movement, FIFO, downstream receiving snapshot, and directed yield/foe checks. **Do not rerun or alter E1-v2 as part of this data phase.**
- For each claimed discrepancy, distinguish **STATIC RULE VERIFIED**, **AGGREGATE RESPONSE OBSERVED**, **VEHICLE/TURN MICROBEHAVIOR UNAVAILABLE**, **CONTRADICTED**, **ALTERNATIVE UNRESOLVED**.

**F3 gate:** No movement-specific discharge, gap acceptance or concurrent-crossing estimate without time-resolved vehicle/lane observations. The J0–J4 non-foe map is static eligibility, **not** a measured vehicles/hour capacity.

### F4 — All ten two-route bundles and indirect interactions

For each of the ten independent seeds:
1. Read the archived \`bundle_target_ids\` and locate the *two matching single-probe arms* by target ID. **Do not assume they are probe0/probe1 or the same slots across seeds.**
2. Verify the bundle changes exactly those two planned original routes; all other 998 original routes and all scheduled departures unchanged.
3. Compute actual **all-driver** bundle interaction \`J_all = ΔC_bundle−ΔC_single_a−ΔC_single_b\`, where each \`ΔC\` is the all-driver scheduled-to-arrival difference vs I. Compute E1-v2-J1 and E1-v1 *predicted total* interaction independently from saved model rows.
4. Compute \`J_nonparticipant\` on the unchanged opt-out roster, and matched per-vehicle interaction distributions by participant/nonparticipant and changed-route versus unchanged-route identities. Avoid mixing different self/external target-exclusion sets.
5. For interval-additive fields such as external-edge waiting vehicle-seconds, calculate four-arm \`J_wait(edge,t)\` and sum disjoint windows. Report both signed network totals and absolute \`Σ|J_wait(edge,t)|\` so strong positive and negative local responses cannot cancel invisibly.
6. Compare prospectively recorded bundle overlap score with realized interaction **descriptively**, not as an independently validated overlap predictor; low direct route overlap can still share downstream constraints.
7. Publish a complete ten-seed results table and choose explanatory plots from prespecified high-|J| and low-|J| ends **with an explicit post-outcome-selection label**.

**F4 gate:** A missing companion singleton arm, inconsistent target ID, absent full-driver arrivals, or different route/schedule makes that seed **INVALID FOR INTERACTION**—do not replace it with a different favorable bundle. If 5-second detector observations are incomplete, retain valid journey-time interaction and mark detector interaction unavailable.

### F5 — Hypothesis adjudication, negative-result report and decision

Deliver a **falsifiable evidence matrix** for T, Q, J, B and A:

| Evidence category | Meaning |
|---|---|
| **DIRECTLY VERIFIED** | Original source-level rule, matched per-driver trip record, or measured original detector field with documented units |
| **CONSISTENT WITH** | Time/space pattern compatible with a hypothesis but nonunique |
| **CONTRADICTS** | Predicted diagnostic behavior absent or reversed under valid observation coverage |
| **NOT OBSERVABLE** | Required time/driver/turn information does not exist in original artifact |
| **CAUSAL EFFECT UNIDENTIFIED** | No controlled physical intervention or causal identification has isolated the mechanism |

Report exact seeds/arm IDs, metric denominators, missingness, input/source hashes, the strongest contrary examples and possible alternative mechanisms. **Do not infer unique mediator causality from lagged correlated waiting or construct a new fitted externality model from observed labels.**

**Decision options:**
- **ARCHIVE MECHANISM CHARACTERIZATION COMPLETE, CAUSAL QUESTION OPEN:** report measured temporal network-state and bundle patterns; draft optional targeted instrumentation specification if exact movement timing is needed.
- **INTEGRITY/OBSERVABILITY LIMITATION:** publish the missing/mismatched measure and no mechanism verdict; preserve original outcomes.
- **ONE OR MORE EXPLANATORY HYPOTHESES DISFAVORED:** report negative controls and pivot toward timing, insertion or other specified missing mechanisms; no automatic model redesign.

The original D1 scientific NO-GO, old Test A NO-GO and Test B nonexecution **cannot change** because of this descriptive investigation.

## 4. Only if needed later: separately frozen passive instrumentation study (NOT authorized)

If F0–F5 cannot distinguish arrival timing, queue spillback or movement service, prepare a distinct protocol **before** touching SUMO again. A bounded *proposal for later review*, not a run authorization, is **four previously seen arm replays**:
- seed **6112** original I and **probe2** (large observed *harm* to others); and
- seed **6113** original I and **probe2** (large observed *benefit* to others).

These cases are **retrospectively selected by outcome**, not held-out model validation. A separately approved protocol must freeze original generator/network/vehicle/route/seed hashes, pinned SUMO image, exact tripinfo equivalence to all 1,000 drivers, passive 1-second FCD with internal-lane IDs, optional route/edge-exit time logs, and memory/storage budget. Check whether FCD sampling and native model diagnostics give *comparable units/clocks* before comparing. If exact trips fail reproduction, terminate claims of physical replication and publish the difference. No re-optimized routes, changed queue physics, calibrated estimator, or extended budget by favorable outcomes.

If instead a **causal junction hypothesis** emerges, it requires its own explicit controlled source/geometry/priority intervention, matched control arms, prospective outcome/identification plan and distinct new seeds. Merely replaying two old cases with passive instrumentation cannot prove that altering the E1-v2 junction rule would have improved model forecast skill.

If a redesigned E1-v3 is ever proposed, specify its independent **new development-build**, **new development-check**, and future truly **unseen independent validation** cohorts with frozen model and decision gates *before* viewing new outcomes. Existing 6201–6212 and 6301–6312 remain sealed under the failed V2-D1 sequence; no automatic reallocation is implied.

## 5. Explicit implementation/research workflow for a separately approved F0–F5 audit

**Recommended archive-only repository code, not authored/executed by this plan:**

\`\`\`text
research/audits/e1_v2_post_failure/
  inventory.py              # 695-member SHA/missingness and source manifests
  trip_decomposition.py     # scheduled-vs-actual departure, duration, other IDs
  edge_time_windows.py      # 5-second entered/left/waiting/occupancy
  network_topology.py       # directed edge adjacency and 100 priority junctions
  discharge_audit.py        # edge-count relationships, no invented turn flows
  bundle_interactions.py    # exact target-matched 4-arm contrasts
  hypothesis_register.py    # supports, counterexamples, missingness and caveats
  tests/                    # archive-only conservation and unit/clock fixtures
\`\`\`

**Execution order and hard gates:** F0 integrity first; F1 accounting next; F2/F3 physical observational summaries only when valid fields exist; F4 bundle arithmetic independently; F5 report with original failed benchmarks and unresolved physics. **No new SUMO simulation dispatch** inside the audit workflow. Use an explicit read-only GitHub Actions job with archive download and a checksum verification step; its push event must never implicitly start an experiment. Avoid editing any original prediction, evidence, route, scientific verdict or source files.

**Proposed deliverables upon separately approved execution:**

1. **Source-and-coverage manifest** (original 695 SHA ledger, source commit/image, 60-arm/10-seed coverage, time-bin/field availability, zero/missing convention).
2. **50-arm paired-effect / insertion-time audit** plus per-seed descriptive summary, self vs others vs nonparticipants, sign/near-zero and original predeclared gate outcomes.
3. **Edge/5-second time grid** with cumulative entered/left counts, sampled seconds, waiting vehicle-seconds and appropriately weighted occupancy/speed, plus internal/external coverage distinction.
4. **Junction approach-discharge register** with static connection mapping and 5-second observed flow/queue-proxy timing, including uncertainty rather than fabricated vehicle-specific crossings.
5. **All ten four-arm bundle interaction table** and spatial/temporal waiting interaction figures; identity and route-match checks.
6. **Hypothesis adjudication report** with negative examples, uncertainty, causal limits, and whether more passive data or a different mechanism is needed.
7. **Verified permanent evidence release of newly derived summary tables only**, original raw D1 data preserved unchanged in its existing permanent release.

**Primary stopping point:** A complete archived-data report is a scientific milestone **even if it concludes "timing/causality not identifiable"**. Nothing here is a sign-off for E1-v3, fresh training, Stage 2 validation, cooperative Test B, or an announcement of a cooperative-routing advantage.

## 6. Scientific interpretation and fairness safeguards

- Source and empirical scales remain **synthetic**: SUMO 1.28.0, one 10×10 priority-junction grid, one-lane external roads, complete announced 1,000-driver demand, 50% synthetic eligibility. No real-road, phone telemetry, opt-in behavior or human safety claim.
- Demand-seed is the unit for multi-run uncertainty; nested probes, bundles and all 1,000 drivers are not independent study replicates.
- Positive \`Δexternal\` is *harm to other drivers*, negative is *benefit to others*. Waiting is a component, **not additive** to journey time. Per-person burden and nonparticipant impacts remain separate from network averages.
- Prediction-before-label integrity of frozen D1 is preserved; any retrospective computations after observing outcomes must be explicitly labeled **post-outcome diagnosis**, never new predictive-skill tests.
- The failed D1 qualifiers must remain visible: mean error, externality direction, across-seed consistency and high-impact false-benefit risk. A new explanatory narrative does not reverse the original finding.
- Temporal associations and queue-like patterns cannot alone isolate causal spillback or actual junction discharge. The current archive has no demonstrated one-second FCD; \`edgeData.entered\` is an interval count.
- **No subjective comfort/calmness outcome** is introduced in this estimator failure investigation. The eventual policy fairness test must separately measure realized participant and nonparticipant harms, not just total seconds.
- Failure to explain E1-v2 with this archive is a valid, publishable negative result; do not tune a model to the historical samples and then call the fit independent validation.

**Final status:** **EXPLANATORY INVESTIGATION PROTOCOL WRITTEN; F0–F5 NOT EXECUTED; ORIGINAL E1-v2 DEVELOPMENT NOT QUALIFIED; INDEPENDENT VALIDATION NOT STARTED; TEST B NOT RUN.**
