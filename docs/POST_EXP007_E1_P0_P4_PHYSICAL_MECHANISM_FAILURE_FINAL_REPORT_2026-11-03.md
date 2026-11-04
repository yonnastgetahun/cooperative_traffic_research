# E1 Stage 1D — P0–P4 Physical-Mechanism Failure Investigation: Final Scientific Report

**Research record:** November 3, 2026.  
**Disposition:** **P0–P4 archived-evidence and frozen-source mechanism investigation COMPLETE. The precise causal reason E1 failed qualification is NOT IDENTIFIED.**  
**Scientific boundaries:** Original Experiment 007 Test A remains NO-GO; E1 Stage 1D remains **DEVELOPMENT NOT QUALIFIED**; independent Stage 2 estimator validation and policy Test B remain **NOT RUN**. This report changes none of the historical predictions, outcomes or acceptance gates.  
**Execution type:** Original Stage 1D research ZIP, frozen E1 source, read-only five-second detector analysis and deterministic no-SUMO toy fixtures. **Zero new SUMO simulations, no E1 source edit, no recalibration, no new held-out seeds, no routing optimization.**

**Prospective controlling plan:** [E1 failure investigation specification, P0–P4](POST_EXP007_E1_PHYSICAL_MECHANISM_FAILURE_INVESTIGATION_SPEC_AND_PLAN_2026-11-03.md).  
**Original failed development study:** [Stage 1D final audit](POST_EXP007_E1_STAGE1D_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-03.md) and [permanent raw evidence release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1-stage1d-development-2026-11-03).  
**Frozen reference code:** original execution commit 05b770cf000f84677524e0a1e89bea06ec0e703b, verified source blobs for the core queue engine 0d446e2c52efd2b75adf351ad5d577f442a4ac29 and static SUMO adapter 4ddc2034944354a1605bc798c8df1850e51ea897.

## Executive finding

We now know **what E1's simplifications do**, and have measured **where and when** the original SUMO outputs respond differently. We cannot yet quantify how much of E1's 1,555.125 network-second development-check externality MAE was specifically *caused* by those simplifications.

**Three new high-signal findings:**

1. **Junction model limitation directly demonstrated:** all legal external turn movements at a synthetic priority junction are assigned the same conflict class by E1's input parser. The original E1 queue engine accepts at most one movement in that class per model tick. A frozen-source toy fixture with two **stipulated compatible** turns delays one crossing by one second under the shared class, whereas declaring distinct classes permits both simultaneously. This is a real, deterministic **source-model behavior**, not evidence that the exact same pair is compatible under the historical SUMO priority metadata or that this caused the actual network error.

2. **Global capacity tuning was effectively unidentifiable in its two leading settings on the development-build predictions:** saved predictions at q_sat **0.50 and 0.65** were bytewise equal in their **entire paired 1,000-driver elapsed-time vectors** for **all 30 evaluated build probe/bundle arms** (six seeds × five interventions). All 30 predicted externalities were therefore identical, explaining the exact tie in build MAE without proving *which* internal constraint rendered the change ineffective. The q_sat 0.35 and 0.50 externalities differed for 24 of 30 arms. This is a newly extracted prediction-sensitivity fact, not new independent validation.

3. **Physical waiting is distributed and nonlinear in the selected failure cases.** In the two largest wrong-sign benefit cases, comparing original SUMO edgeData with matched same-seed baseline found aggregate external-edge waiting increases of **+1,056** and **+3,571 vehicle-seconds**, with large increases on some links and reductions on others. Four same-seed joint-minus-single detector contrasts reveal substantial, sometimes offsetting queue-associated changes; two roughly track the sign/magnitude of actual network-time interaction, two do not. These are **observed edge-time measures**, not a decomposition proving uniquely causal junctions or a demonstration that waiting alone equals the externality.

**Important narrowing:** This 10×10 original grid has **360 external directed roads, each with one lane**. The original hypothesis that E1 fails because it cannot represent **competition between multiple lanes on these same road edges** cannot be tested or used to explain these data: no such external multi-lane variation exists. Within-link spatial propagation and internal junction movement representation remain simplified, but the original Stage 1D archive lacks vehicle-resolved FCD to isolate them.

## P0 — Raw archive, predictions, source and observation inventory: PASS

Archived evidence was independently opened and checked without running SUMO:

| Record or property | Verified value |
|---|---:|
| Original downloaded GitHub Actions ZIP SHA-256 | f8d2b76bd6eda63e11889bd7708888bfdb55af78edd0b30526a9d981feb72fa6 |
| ZIP member count | **706** |
| Separate frozen demand-seed families | **10** (DEV_BUILD 5101–5106, DEV_CHECK 5111–5114) |
| SUMO simulation arms | **60/60** (one I, four single swaps, one bundle per seed) |
| Exact matched tripinfo identities | **60,000 = 1,000 per arm** |
| Prediction locks | **10**, with saved SHA-256 matches |
| Parameter-specific prediction files | **22** (18 build; four check) |
| Original five-second edgeData files | **60** |
| Original five-second laneData files | **60** |
| Original one-second FCD vehicle trajectory files | **0** |

Every original tripinfo file's SHA-256 matched its archived observation summary; network, demand and route files matched each frozen seed manifest; each single swap had only the nominated vehicle's planned route changed and each bundle exactly two. All 21 previously frozen no-SUMO mathematical/input tests also passed when rerun against the SHA-matched original model source.

**Validity:** Integrity and available measurement types established. Predictions and route hashes are consistent with the previously audited prediction-first process. The archive is not new held-out evidence, and source/hash checks alone cannot prove timing of every event outside the saved workflow provenance.

## P1 — Physical model and SUMO priority-junction structure: SOURCE LIMITATION VERIFIED

| Physical/source fact | Evidence |
|---|---|
| 360 external directed road links | Parsed archived original network.net.xml |
| **One external lane on every road link** | All 360 have exactly one lane |
| 100 priority junctions and 352 SUMO internal junctions | Archived network type counts |
| 1,320 distinct legal external edge-to-edge turn pairs | Archived connection elements |
| 2,992 individual lane-connection XML rows | Archived network |
| 1,320 priority-junction request elements | Archived junction metadata |
| 96/100 priority junctions have at least one nonzero foe bit | Raw request metadata, not yet mapped to exact compatible movement pairs |
| Single E1 conflict group | Static adapter emits conflict_class = all at every parsed legal turn |
| One accepted movement per group per tick | Frozen E1 used_conflicts check on (junction, conflict_class) |

**Demonstrated code behavior:** Assigning every movement the same class means E1 treats all simultaneous traversals at a priority intersection as mutually exclusive in one-second resolution, even if some may legally coexist under the actual junction's priority rules. The archived request foe/response/index bitfields exist, but **their exact index-to-connection and right-of-way interpretation has NOT been independently validated** against pinned SUMO 1.28.0. We therefore do **not** assert any specific observed two movements should have crossed simultaneously.

**Nature of issue:** A deliberately conservative, previously disclosed model-fidelity limitation—not necessarily a violation of E1's originally frozen fallback contract. Its influence on the failed E1 predicted externalities remains to be isolated.

## P2 — Original time-resolved traffic measurements: OBSERVED, NOT A UNIQUE BOTTLENECK

We compared the **four previously inspected DEV_CHECK seeds (5111–5114)** across their original baseline, four individual probes and bundle: **24 complete edgeData arms and 20 same-seed intervention-versus-I comparisons**. Files contain nonoverlapping five-second waiting, sampled vehicle time, entering/leaving counts, speed and occupancy; missing/empty interval values were treated as zero for **waiting totals** only when the edge was absent from that interval. We excluded SUMO internal edges from aggregate external-edge summaries and retained internal detector data in the untouched original archive.

For the two predefined false-benefit probe cases:

| Archived comparison | E1 predicted others' effect | Actual others' effect | External-edge detector waiting change | Distribution among external edges |
|---|---:|---:|---:|---|
| **5111 probe2 vs I** | **−4 network-s** | **+2,567 network-s** | **+1,056 vehicle-s** | 93 edges with >10s increase; 92 edges with >10s decrease |
| **5114 probe2 vs I** | **−6 network-s** | **+3,945 network-s** | **+3,571 vehicle-s** | 93 edges with >10s increase; 92 edges with >10s decrease |

These signed edge waiting totals are the sum of recorded, disjoint five-second intervals for external edges only. They **cannot be added to scheduled-departure-to-arrival time**, and they **do not equal the network-wide travel-time change or the 999-driver externality**. Route changes may affect on-link waiting, turning delays, actual moving speed, source insertion, internal junction time and the rerouted driver's own time.

**Selected spatial/time observations, not causal attribution:**

- On **seed 5111 probe2**, edge **C3D3** accumulated **−844 vehicle-seconds** of signed waiting difference (first |delta| ≥10 seconds in an interval at **185s**), while edge **C5D5** accumulated **+648 seconds** (first large interval near **175s**). Other large signed effects occurred on F8G8, C2D2, D2E2 and H6G6.
- On **seed 5114 probe2**, edge **F4E4** accumulated **+1,300 vehicle-seconds** (first |delta| ≥10 interval **185s**); D6E6 +951 and F7E7 +892, while E3F3 was −619. These are **synthetic grid IDs**, not real road names or uniquely proven bottlenecks.
- Both cases show **simultaneous positive and negative local waiting contrasts**, consistent with redistribution and interacting congestion. Whether these are upstream causes, downstream consequences, or both cannot be determined uniquely from these measurements.
- Source and detector coverage was checked in detail for 5111 I/probe2 and 5114 I/probe2: each had **360 distinct external lanes and zero multilaned external-edge intervals**, with window coverage from t=0 through approximately **563–636 seconds**, depending on arm.

**No vehicle-level timing attribution from these archives:** The 60 Stage 1D arm files contain **no FCD** and no original per-vehicle edge-exit trajectory export. EdgeData's five-second aggregate entered/left observations cannot be represented as each driver's exact edge entry clock. The earlier six-run 4101/4102 FCD belongs to **different, already inspected historical scenarios** and is not a substitute for this data.

### P2 bundle interaction, including time-indexed waiting differences

For each seed we used the **same two original individual probe arms that defined its frozen bundle** (probe0 and probe1) and computed the exact four-arm difference-of-differences. All are descriptive, retrospective comparisons:

| Development-check seed | Actual joint-minus-single all-driver network elapsed interaction | Five-second external-edge waiting interaction | E1 predicted all-driver interaction |
|---|---:|---:|---:|
| 5111 | **−3,424 network-s** | **−3,118 vehicle-s** | 0 |
| 5112 | **−2,839** | **−2,762** | 0 |
| 5113 | **−383** | **+78** | −7 |
| 5114 | **−799** | **+288** | 0 |

External-edge waiting interaction uses (bundle − probe0 − probe1 + I) **at the matching five-second bin and edge**, summed across the complete measured time horizon. In 5111/5112 it moves in the same direction and similar magnitude to all-driver network interaction. In **5113/5114 its sign is opposite**, demonstrating that aggregate external-edge waiting alone is not a universally sufficient explanation. Across these four bundles, many road/time cells contributed with opposing signs; interpreting any one as *the unique mediator* is unsupported.

**The frozen original bundle selector recorded forecast overlap score zero in all four DEV_CHECK seeds.** These are selected low-overlap fallbacks, not a balanced randomized sample of high- versus low-overlap interaction mechanisms. E1-v1's forecast of almost zero interaction cannot be rescued by using original SUMO results as model input.

## P3 — Frozen-source, no-SUMO physics fixtures: PASS WITH CAUSAL LIMITS

The auditor tested the exact old model's source files against their expected Git blob hashes and reran **21 existing no-SUMO unit tests**: all passed. These check conservation, legality, paired accounting, route identities, nonparticipant sums, and the original identity-breaking E1 fixture. They establish code integrity, **not** predictive skill in Stage 1D SUMO.

A **two-vehicle stipulated-compatible-turn toy scenario** was evaluated using the unchanged frozen E1 evolution engine. All physical inputs and vehicle schedules were held fixed except the **turn conflict label** provided as a fixture input:

| q_sat (veh/s/lane) | Frozen shared all-class crossing ticks | Two deliberately distinct toy conflict classes crossing ticks |
|---|---|---|
| 0.35 | 5, 6 | **5, 5** |
| 0.50 | 4, 5 | **4, 4** |
| 0.65 | 4, 5 | **4, 4** |

Both turns independently enter different receiving links. Under the shared class, the second vehicle arrived one second later. The class-separated fixture lets the stipulated compatible movements cross at the same tick. **These are contrived model fixtures, not new SUMO simulations or evidence that a real historical turn pair was simultaneously compatible.** The fixture does not replace E1 with a tuned variant or provide a new held-out MAE.

**Parameter-sensitivity audit of original immutable predictions:**

- For all **30 DEV_BUILD interventions** (six seeds × four single swaps plus one bundle), the complete saved vectors of **both baseline and alternate elapsed times for all 1,000 identities** were **identical** between q_sat 0.50 and 0.65.
- Consequently **30/30 external predictions** were identical; the two settings tied exactly on original DEV_BUILD MAE and cannot be distinguished by those observed prediction outcomes.
- The 0.35 versus 0.50 external predictions differed on **24/30** build interventions.
- The toy fixture demonstrates that one-second capacity rounding can make q=0.50 and 0.65 produce identical crossing times in a simple setting, while q=0.35 can change them. **This is a possible mechanism, not a demonstrated explanation** of the entire 1,000-driver saturation-rate tie. A detailed binding-constraint trace from the archived E1 model's actual development scenarios was **not retained**, so shares of active link, junction or receiving constraints are currently **unidentified**.

## P4 — Hypothesis adjudication: what can we claim?

| Hypothesis | What is verified | What remains unproven | Status |
|---|---|---|---|
| **H1 Junction conflict/discharge** | E1 uses one all-conflicts class per priority junction; toy model timing shows its restriction; original SUMO contains richer priority/request metadata | The amount/direction of Stage 1D externality error caused by this choice, or which real SUMO turns should be concurrently served | **SOURCE LIMITATION VERIFIED; causal contribution insufficient** |
| **H2 Link FIFO / spatial propagation** | Model has one FIFO queue per directed link; the grid has exactly one lane on each external road; substantial distributed 5-second waiting differences | Lane-to-lane competition on this grid (not present); within-edge spillback fronts without per-vehicle positions | **MULTILANE EXPLANATION NOT APPLICABLE; other aspects insufficient** |
| **H3 Entry timing, insertion and clocks** | Recorded five-second flow/waiting dynamics differ by original route assignment; E1 rounds eligibility to 1s | Vehicle-specific edge-entry errors, arrival-bin causal amplification and insertion-versus-junction attribution without Stage 1D FCD | **INSUFFICIENT OBSERVATION** |
| **H4 Bundle nonadditivity** | Four large realized joint-minus-single interactions and measurable five-second external waiting interaction; original E1 predicted 0,0,−7,0 | Specific queues/intersections causing each response; prospective validity on unseen, independent pairs | **OBSERVED INTERACTION; CAUSAL PATH NOT IDENTIFIED** |
| **H5 Saturation prior identifiability** | q=0.50 and q=0.65 gave identical full 1,000-driver predicted vectors for 30/30 build interventions; 0.35 differed on 24/30; toy exhibits time quantization | Whether conflict cap, link service or storage dominated the original network cases; true physical saturation rate | **EMPIRICAL PREDICTION INSENSITIVITY VERIFIED; constraint cause insufficient** |

**Why no unique explanation:** H1, H3, H4 and H5 are related; observing a model simplification and a simultaneous SUMO waiting difference does not isolate a causal mediator. Source-level rule tests, five-second aggregates, and retrospective selected probes cannot identify which changed junction property would have rescued the frozen E1 predictions. **No corrective parameter or algorithm has been tried against these outcomes in this investigation.**

## Scientific decision and independently authorized next work

**This P0–P4 investigation is COMPLETE with a qualified result: E1's simplifications are now documented, but their causal contribution to the Stage 1D NO-GO is unresolved.** The scientific value is clearer hypothesis selection and recognition of which physical measurements are missing. It is **not** a successful or validated E1-v2 predictor.

**Recommended order for separate future consideration, not automatically authorized:**

1. **Model-contract study:** Decode and independently verify SUMO 1.28.0 priority junction request/foe/response indexing and turn compatibility against the preserved 10×10 network, while preserving original E1 as frozen. Define a falsifiable enhanced connection-aware junction hypothesis. This step should not tune or fit to 5111–5114 outcomes.
2. **Targeted observational replay proposal:** Freeze a new **four-arm** passive-instrumentation plan for the two previously observed wrong-sign pairs (5111 I/probe2 and 5114 I/probe2) if vehicle-level edge timings or discharge queues are essential. Require identical original route/input SHA and tripinfo equivalence, preserve existing unsuccessful results, and label these replays **retrospective physical explanation only**. Do **not** run them under this approval.
3. **Prospective E1-v2 model/specification:** If physical and source evidence warrants a change, define its new junction/queue design, no-future-information contract, distinct **fresh development-build and development-check** cohorts, falsifiable inaccurate-benefit safeguards and resource budget **before new training or outcomes**. Original 4101–4105 and used 5101–5114 are permanently contaminated for independent validation.
4. **Independent validation, then policy Test B only conditionally:** An E1-v2 candidate must first satisfy a newly frozen development gate and then pass a separate genuinely unseen estimator-validation study. Only afterward could its frozen predictions support a matched, equally informed cooperative-versus-independent routing Test B with participant and nonparticipant realized fairness gates.

**What this cannot justify:** Altering historical Test A NO-GO, changing Stage 1D's 5% development gate or its two false-benefit cases, claiming a specific junction caused a 3,945 network-second externality, deploying E1 in a navigation product, or concluding that cooperative routing succeeds/fails against independent traffic-aware routing.

## Reproducibility inventory

- [Prospective P0–P4 study plan](POST_EXP007_E1_PHYSICAL_MECHANISM_FAILURE_INVESTIGATION_SPEC_AND_PLAN_2026-11-03.md).
- [Original E1 Stage 1D scientific report and decision](POST_EXP007_E1_STAGE1D_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-03.md).
- [Durable source evidence with per-member SHA ledger](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1-stage1d-development-2026-11-03).
- [Original frozen E1 queue-engine source](../research/externality_estimator/link_turn_queue.py) and [static SUMO adapter](../research/externality_estimator/scenario_io.py); original source blob SHA pins above.
- Compact machine-readable original archive/physical diagnostic tables in [P0–P4 results directory](results/) named exp007_e1_p0_p4_*.csv and matching source fixture JSON. These are **descriptive derived data from original evidence only**. Raw 5-second detector records remain in the durable full release.
- The audit Python sources are included as a [P0–P4 reproducibility bundle](../research/audits/README_E1_P0_P4_ARCHIVE_AUDIT.md); they perform no SUMO execution or parameter fitting.

**Permanent status:** **P0–P4 completed; E1 Stage 1D development NOT QUALIFIED; independent validation NOT STARTED; policy Test B NOT RUN.** No social-media publication performed or authorized.
