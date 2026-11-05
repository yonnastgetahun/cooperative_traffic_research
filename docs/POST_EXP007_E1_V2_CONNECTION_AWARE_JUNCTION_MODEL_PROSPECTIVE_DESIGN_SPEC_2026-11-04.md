# Cooperative Traffic Research — E1-v2 Connection-Aware Junction-Response Estimator
## Prospective scientific model-design specification v0.1

**Date:** November 4, 2026  
**Status:** **DESIGN SPECIFICATION COMPLETE — NOT AN EXECUTABLE IMPLEMENTATION FREEZE, NO E1-v2 CODE, NO NEW SIMULATIONS, NO MODEL VALIDATION, NO TEST B.**  
**Authorization:** User approved proceeding from the completed SUMO–E1 J0–J4 rule verification to the recommended **E1-v2 connection-aware junction-model design**. This document does not authorize implementation, experimental dispatch, tuning, or public social distribution. Separate authorization is required for source construction and for any SUMO execution.  
**Scientific aim:** Develop a prospective, counterfactual model which distinguishes the *selected driver's own elapsed time* from the sum of *other drivers' elapsed-time changes*, while representing lawful junction movements and time-dependent downstream network interactions more faithfully than frozen E1.

## 0. Scientific disposition and evidence hierarchy

The original Experiment 007 Test A failed (8/20 directional matches, 40%, versus its preregistered 60% threshold); conditional Test B **was not executed**. E1 Stage 1D executed the prespecified 60-arm development study and remained **DEVELOPMENT NOT QUALIFIED**: E1's development-check externality MAE was **1,555.125 network-seconds**, versus **1,555.267549** for the strongest prior benchmark B1, a **0.00917%** improvement against a frozen 5% development requirement. Two E1 forecasts predicted small benefits to other drivers where observed other-driver elapsed-time sums worsened by **+2,567** and **+3,945 network-seconds**. Those results are immutable.

The [completed J0–J4 SUMO 1.28.0 rule audit](POST_EXP007_E1_J0_J4_PRIORITY_JUNCTION_VERIFICATION_FINAL_REPORT_2026-11-04.md) independently verified the exact original movement/request mapping and established a **static rule mismatch**. In the historical 10×10 synthetic network there are **100 priority junctions**, **1,320 request-to-movement mappings**, and **8,836 unordered within-junction movement pairs**. SUMO's encoded request matrices mark **5,764 pairs as mutual non-foes**; **3,940** of those have distinct incoming, outgoing and initial via lanes, including **2,212** with \`cont=0\` for both. The frozen E1 adapter assigns every turn within a priority junction \`conflict_class='all'\`; its engine consequently excludes their joint passage in one one-second model tick.

**Established:** E1 is strictly more restrictive than the static *foe* relationships for those 3,940 candidate pairs. **Not established:** that vehicles physically crossed these pairs concurrently in the old SUMO runs, that relaxing the rule is sufficient to improve externality prediction, or that a specific junction caused any Stage 1D wrong-sign error. Non-foes are *potentially compatible under static conflict coding*, **not automatically simultaneously passable**.

**Sources of truth:**
- [Original E1 Stage 1B executable-development protocol](POST_EXP007_E1_EXECUTABLE_DEVELOPMENT_PROTOCOL_V1_2026-11-03.md).
- [Stage 1D frozen-source development outcome](POST_EXP007_E1_STAGE1D_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-03.md) and [original 706-member preserved raw evidence](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1-stage1d-development-2026-11-03).
- [J0–J4 scientific conclusion](POST_EXP007_E1_J0_J4_PRIORITY_JUNCTION_VERIFICATION_FINAL_REPORT_2026-11-04.md), [full durable movement matrices and source cross-checks](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1-j0-j4-priority-junction-verification-2026-11-04).
- Exact prior execution source commit \`05b770cf000f84677524e0a1e89bea06ec0e703b\`; frozen input-adapter blob \`4ddc2034944354a1605bc798c8df1850e51ea897\`; frozen E1 engine blob \`0d446e2c52efd2b75adf351ad5d577f442a4ac29\`.
- [Tagged SUMO v1_28_0 sumolib implementation](https://github.com/eclipse-sumo/sumo/tree/daf91b5578901d599ac9af53f49d26eeb9aefc3b/tools/sumolib), including \`Node.getLinkIndex\`, \`Node.areFoes\` and \`Node.forbids\`; pinned simulator image digest \`sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb\`.

All historical 4101–4105, six replay cases, and Stage 1D development **5101–5106** / check **5111–5114** are now **retrospectively inspected**. They can guide test fixtures and failure analysis; they must never be relabeled as untouched independent confirmation of E1-v2.

## 1. Precise E1-v2 prediction contract (unchanged scientific question)

For 1,000 announced scheduled drivers under identical synthetic input information \(\mathcal I(t_0)\), compare an original fixed all-driver route assignment \(A_0\) and \(A_1\), in which only an eligible target driver \(i\) has a different connected, legal route. Let \(T_j(A)=arrival_j(A)-scheduled\_departure_j\), including source insertion delay exactly once.

- **Self:** \(\Delta_i^{self}=T_i(A_1)-T_i(A_0)\), individual seconds.
- **Externality:** \(\Delta_i^{other}=\sum_{j\ne i}[T_j(A_1)-T_j(A_0)]\), **network-seconds**.
- **All drivers:** \(\Delta_i^{all}=\Delta_i^{self}+\Delta_i^{other}\), network-seconds.
- **Nonparticipants:** \(\Delta_i^{nonopt}=\sum_{j\in U}[T_j(A_1)-T_j(A_0)]\), with U the immutable nonparticipant roster.

**Sign convention:** negative saves time / predicted benefit; positive adds time / predicted harm. Model predictions must be computed from **two prospective forward evolutions with the same t0 state and other 999 planned routes**, not inferred as a multiple of the target's own cost. Record individual baseline and alternate predicted arrival times for all driver IDs. For a two-route bundle, predict a **new joint network rollout**, not the sum of two singleton effects.

A **complete 1,000-driver arrival accounting** is required; a model unable to clear all drivers within its finite horizon must issue an explicit abstention/incomplete status, not report truncated averages. Waiting is contained in travel time; \`waitingTime\` and \`timeLoss\` are diagnostics and must never be added a second time.

The first scientific context remains **synthetic, fully announced, one-shot pretrip routing**. Knowledge of every vehicle's intention in a real city is an idealized assumption, not an actual smartphone measurement. Fairness remains integral: forecast and report nonparticipant impacts and severe individual harm risk even when aggregate externality looks favorable. Subjective calm and journey-quality endpoints remain deferred.

## 2. Exact model change: junction service, not a broader hidden retrofit

**E1-v2 primary design is a surgical extension of E1's junction scheduling.** Retain the E1-v1 control for comparison and, for v2's initial attribution-focused development mode, keep unchanged wherever possible:

- directed road-link graph, source waiting queues, link storage rule, vehicle FIFO state, 1-second forward step, minimum edge traversal eligibility and route data/identity contracts;
- link/turn capacity tokens, their documented accumulation caps, snapshot receiving slots and synchronous state commit;
- identical OD, scheduled departures, eligibility roster, alternative route set and uncertainty draws under baseline and swapped-route E1-v2 rollouts;
- no new calibration of global saturation rate while assessing **junction-rule implementation correctness** (use the frozen E1 \`q_sat=0.50\` as a declared starting reference, not as a newly validated physical capacity).

**A changed junction policy may expose other model limitations.** Do not simultaneously retune link travel time, speed factors, storage spacing, route selection, departure demand, timing offsets or a learned residual. Any later changes to those dimensions must be separately versioned with distinct hypotheses, ablations and fresh development data, not silently folded into a junction-only result.

### 2.1 Versioned per-movement input contract

Define a typed **movement** for each verified incoming-lane → outgoing-lane SUMO connection (and its \`via\` internal-lane path, where present). Required fields:

| Field | Meaning |
|---|---|
| \`junction_id\`, \`request_index\` | Frozen SUMO priority-junction identity; distinct from \`tlLinkIndex\` |
| \`incoming_edge, incoming_lane, outgoing_edge, outgoing_lane\` | Exact connection and physical lane IDs |
| \`via_lane\`, \`cont\`, \`direction\` | Internal continuation, intermediate stop flag and original turn metadata |
| \`foe_request_indices\` | Read-only static conflicting movement indices from **right-to-left** SUMO bitsets |
| \`yield_to_indices\` | Directional priority obligations from SUMO \`response\` bits, not conflated with foe status |
| \`source_network_sha256, pinned_sumo_source_sha\` | Canonical network and reference implementation provenance |
| \`known_status\` | \`VERIFIED / UNKNOWN / UNSUPPORTED\` and reason |
| \`demand_route_occupancy\` | Forecast prospective vehicle presence and source FIFO head, not future SUMO truth |

**Ingestion hard gate:** Independently verify every relevant movement/request index with the original tag-pinned \`sumolib\` semantics and preserved network fingerprints. For this 10×10 grid the J0–J4 audit mapped **1,320/1,320**, but a redesigned parser must itself verify rather than assume that all new network files follow the same ordering. No edge-level collapsed turn may invent a lane-level priority relationship. A future multi-lane network would require new explicitly supported queue/lane mechanics or an abstention; this experiment's **360 external links are single-lane**.

**Important:** \`foes(i,j)\` answers static relationship; \`yield_to(i,j)\` answers who must give way. \`not foe\` is **not a service entitlement**, **not** proof of a safe crossing, and **not** a guarantee that both vehicles are present.

### 2.2 Proposed conflict-aware time-step service

For a given tick and junction, build a snapshot of candidate movements **only for actual eligible head-of-line vehicle intentions**. An eligible candidate needs a valid route transition, minimum edge time reached, enough sending/turn service token, and positive receiving space at the target lane/link. Unknown turn metadata may force abstention or conservative fallback according to §2.4.

A candidate set is **statically jointly compatible** only when every selected pair is mutually non-foe under verified SUMO request bits and no additional same-source-FIFO, shared-downstream-slot, or shared internal-lane constraint is violated. The model must never treat different non-foe connections as unconstrained unlimited flow.

For example, to describe a *safe discrete approximation* rather than exact SUMO dynamics:

1. Freeze complete pre-tick occupancy, queue heads, eligible source insertions, service-token counts, and downstream receiving slots. Preserve independent candidate arrivals/time eligibility.
2. Build the **candidate movement conflict graph**: nodes are eligible lane-level movements; put an exclusion edge for mutual foes, any same incoming FIFO head, documented shared internal service occupancy, or finite receiving slot contention that cannot be resolved through slot accounting. Mark directional \`response\` yield obligations **separately** from undirected foe edges.
3. In a stable, documented movement-selection order, give feasible **higher-priority, conflicting present requests** precedence; lower-priority movements may proceed when the higher-priority claimant is not active, not ready, or otherwise cannot actually claim a slot. Do not assume \`response\` means all lower-priority traffic is blocked at every tick. Unknown asymmetric/right-of-way cycles must use a documented conservative fallback/abstain, not arbitrary inconsistent decisions.
4. Within equally ranked feasible candidates use an explicit deterministic junction-local rotation and stable movement/vehicle IDs. Allow **multiple compatible movements in the same one-second tick** only after all physical capacity and bitset guards pass. Reject any two conflicting requests from simultaneously consuming service. Conserve exact source/destination vehicle identities.
5. Reserve downstream receiving **per physical lane/link**, decrementing after each selected movement, and commit all source-to-destination changes synchronously. No downstream queue can exceed physical storage and no link can send more than its available service tokens.
6. Preserve an explicit distinction between "crossing permitted at a given tick by a discretized rule" and "SUMO predicts this actual vehicle would have crossed in that second." This module is an approximation; the latter needs controlled simulation evidence.

**Chosen initial policy:** **conservative pairwise independent movement set** with directional priority preference and finite receiving/service limits. This is intentionally smaller than full SUMO vehicle dynamics (which include speed, gap acceptance, internal-lane space and moving priority). The implementation review must turn this pseudocode into an unambiguous algorithm, including graph selection/tie handling and internal continuation behavior, **before using any new outcomes**. Do not pretend this v0.1 document alone freezes executable scheduling mechanics.

### 2.3 Distinguish compatible non-foes from physical constraints

Document distinct stopping reasons per candidate and tick:

- \`NO_FUTURE_FREEFLOW_ELIGIBILITY\`;
- \`SOURCE_FIFO_NOT_HEAD\`;
- \`LINK_SERVICE_EXHAUSTED\`;
- \`TURN_SERVICE_EXHAUSTED\`;
- \`CONFLICTING_FOE_SELECTED\`;
- \`YIELD_HIGHER_PRIORITY_READY\`;
- \`SHARED_RECEIVING_STORAGE_FULL\`;
- \`SHARED_INTERNAL_LANE_BLOCKED\`;
- \`INTERMEDIATE_CONT_UNKNOWN\`;
- \`STATIC_MAPPING_UNKNOWN\`;
- \`MODEL_HORIZON_EXCEEDED\`.

This register is necessary for **mechanistic attribution**, not just debugging. A movement's absence from service must be traceable to a guard; constraints can co-bind. Attribute conditional counts by **tick, junction, movement, target route, and unchanged-route driver** where feasible. Do not label a broad aggregate "junction waiting" as uniquely caused by conflicts.

### 2.4 Internal junctions, 'cont', and uncertainty

The frozen network contains SUMO internal junction and internal-link structure that the old edge-level E1 omits. If \`via\`, \`cont\` or shared internal lanes imply a possible intermediate wait, **do not silently classify it as a clean unrestricted pair** even when raw foe bits are zero.

**Proposed v2 treatment tiers:**

- **Tier A — Verified, simple non-foe pair:** distinct incoming/outgoing/initial internal vias, both \`cont=0\`; allow one-second concurrent eligibility subject to send/turn/receive/priority constraints. This tier is supported by verified static coding, not yet actual traffic discharge.
- **Tier B — Verified foe or priority relation:** preserve the directed response/yield relationship. Never allow static foes to be promoted to unconstrained independent service merely because they have different roads. Within the simplified step model, do not schedule a mutually-foe pair simultaneously unless a later separate micro-validated physical rule explicitly permits it.
- **Tier C — Possible intermediate stop, merged internal path, unresolved mapping, or beyond-scope multi-lane behavior:** default to a labeled **conservative fallback or abstention**. Keep group identifiers/unknown counts; do not assert false precision. Future internal-lane occupancy mechanics are a **separately justified extension** if necessary.

Define one deterministic fallback policy and log its usage rate. If Tier C occupies a large proportion of candidate decisions, the estimator may be too incomplete to qualify and must say so. Static rule compatibility alone must not create imaginary capacity.

## 3. Prespecified scientific hypotheses, negative controls and failure conditions

| Hypothesis | Distinguishable prospective prediction | Contrary evidence / stop |
|---|---|---|
| **V2-H1 junction overrestriction** | On small fully specified mutually non-foe fixtures, v2 can discharge multiple eligible turns per tick while E1 all-class defers a movement, respecting capacity | V2 still excludes such pairs, or exceeds shared receiving, sending or internal service |
| **V2-H2 priority fidelity** | Directed yield logic changes service ordering only when competing **ready** foe vehicles are present; non-foes unaffected by unrelated right-of-way | Direction reversed, higher-priority absent but lower unnecessarily blocked, or priority cycle silently mishandled |
| **V2-H3 unchanged-route propagation** | A target route change can shift eligible capacity and forecast arrival times of unchanged-route drivers, with a distinct nonzero externality | Externality mechanically equals self change or equals zero regardless of coupled constraints |
| **V2-H4 interactions** | Recomputed joint two-swap rollout may differ from sum of singleton effects due to shared queue/receiving and junction conditions | Bundle computed by adding isolated predictions, or interaction vanishes for every deliberately coupled fixture |
| **V2-H5 identifiable constraint effects** | Binding-constraint counters distinguish conflict-limited from token-limited and receiving-limited decisions | Outputs match across all parameter variants without any recorded explanation, or guards/counters don't reconcile |
| **V2-H6 harmful optimism** | Model can output uncertainty/abstain when sign of benefit is not stable or nonparticipant harm risk is large | A predicted tiny negative externality presented as reliable despite plausible severe positive outcomes |

**No guaranteed recovery claim:** Passing fixtures proves narrower internal behavioral properties. It does **not** prove E1-v2 predicts the 1,000-driver synthetic traffic environment, is calibrated, or improves individual fairness in any executed cooperative assignment policy.

## 4. No-SUMO engineering test matrix to freeze before implementation

At minimum the next separately approved implementation protocol must supply reproducible deterministic fixtures for:

1. **Request-index and source SHA**: 1,320/1,320 original movement-to-request mapping; pinned foe/response/cont direction and correct index namespace; reject reversed bit order and guessed \`tlLinkIndex\`.
2. **Mutual non-foes**: eligible distinct inbound/outbound Tier A turn pair from verified A0/A1 junction mapping may both cross in one model tick if token/storage/freeflow permit; frozen E1 comparator defers one.
3. **Mutual foes and yield asymmetry**: two present, ready foes do not consume the same conflicted time-step slot; higher priority gets deterministic precedence, absent high-priority claimant does not cause phantom delay.
4. **Same incoming one-lane FIFO**: two branch movements sharing one source lane cannot overtake each other or assume two physical heads. No simultaneous claims by the same driver.
5. **Downstream receiving and shared internal via**: two static non-foes cannot fill the same single receiving slot; no internal lane double occupancy if explicitly tracked.
6. **Intermediate waiting and ambiguity**: Tier C \`cont\` cases use the documented conservative policy/abstain; no unverified concurrency.
7. **Finite physical mass**: all vehicles in exactly one status, no negative queue, storage overflow, illegal connections, skipped edge-time eligibility or negative service tokens at every tick.
8. **No change and disjoint path**: identical baseline and alternative has zero all-driver effects; a disjoint route swap does not invent external effects.
9. **Equal self but nonzero others**: independently verified synthetic junction scenario breaks the old self/externality algebraic identity.
10. **Positive and negative externalities**: separate toy cases with correctly signed other-driver effects.
11. **Nonadditive two-route bundle**: joint forward calculation and exact all-driver reconciliation.
12. **Scheduled departure/insertion**: source delay included exactly once, including drivers unaffected in route identity.
13. **Missing/future data**: rejected post-t0 observations, SUMO oracle outcomes, unknown request mappings and unsupported features; evaluation labels never imported by inference.
14. **Snapshot determinism and symmetry**: same source, model, parameter, demand and random seed yield byte-identical predicted outputs; counterfactuals share initial information and all other routes.
15. **Uncertainty/abstention**: no calibrated interval claims from toy fixtures; explicit route-benefit abstention state when predictive confidence unavailable.
16. **Runtime and scaling**: bounded 1,000-driver offline paired rollout, actual CPU/RSS recorded; no assertion of mobile real-time feasibility.

**Implementation gate:** All physical, legality, provenance and leakage fixtures must pass. The unchanged old E1 tests remain a regression baseline; modifications must be isolated in a new version/module and cannot overwrite or silently replace the original E1 source.

## 5. Strict evidence partitions and scientific evaluation sequence

### 5.1 Four categories, never relabel

| Partition | Use | Forbidden use |
|---|---|---|
| **HISTORICAL_DIAGNOSTIC**: original 4101–4105, six replays, and all E1 5101–5114 outcomes | Source inspection, physical problem definition, predeclared toy-fixture ideas and explanatory post hoc case studies | New untouched development-check or Stage 2 validation evidence |
| **NEW_V2_DEV_BUILD** | Calibrate any explicitly prespecified v2 parameters, improve engineering and inspect physical diagnostics | Call it unseen independent validation |
| **NEW_V2_DEV_CHECK** | Measure a *build-frozen* candidate once on distinct independent demand seeds | Retune model and then claim the same data remained unseen |
| **FUTURE_INDEPENDENT_VALIDATION** | Confirm a finally locked model on genuinely fresh, untouched seeds and route perturbations under a new protocol | Use for feature selection, residual fitting, picking thresholds or designing the model |

A fifth **FUTURE_TEST_B** must be independently sequestered after successful estimator validation. Previously unused old Test B seed labels **4201–4210** must **not** be treated as automatic new holdout evidence or opened in this phase; reserve a separate new prospective policy cohort.

### 5.2 Required isolating comparisons

A meaningful future engineering/development study must compare:

- **B0:** predict zero externality.
- **B1:** historical frozen quadratic assigned-demand proxy.
- **B2:** own-time-only predictor, explicitly zero predicted externality (helps distinguish own ETA improvement from true external skill).
- **E1-v1:** original frozen all-class queue-aware model (source SHA pinned; do not refit or rewrite).
- **E1-v2-J:** *junction-only* connection-aware modification with E1's other priors and model clocks matched to E1-v1 to the degree possible; differences clearly logged.

Only in separately authorized subsequent protocols may more elaborate revisions (E1-v2-J+internal, different time step, changed source insertion model, learned residual, traffic-demand uncertainty) enter the comparison. This **one-factor-first ablation** is designed to isolate a model intervention. It does not guarantee identification of a causal SUMO bottleneck.

Compare all models on identical legal routes, exact OD/vehicle schedules, eligibility, network and prospective information cutoffs and explicit equal-information assumptions. Compute independent seed-level externality errors **without treating four probes sharing a baseline as independent replicates**. Predictions must be immutable with hashes before SUMO outcomes can be read for each cohort.

### 5.3 Primary and secondary decision measures to preregister

Before any new V2 development data are generated, a separately frozen implementation-and-execution protocol must specify **seed identities, number of single swaps, joint bundles, interaction-overlap strata, resource footprint, primary effect metric and decision thresholds**. This v0.1 model design does **not** authorize or imply a seed budget or a numerical PASS threshold.

Mandatory outcomes for subsequent studies:
- **Primary skill:** externality MAE and signed bias in **network-seconds** by **independent seed**, compared to the best frozen baseline (B0/B1/E1-v1, not retrospectively chosen features).
- **Directional accuracy:** sign on predeclared materially nonzero realized effects; zero/near-zero predictions reported separately; prospective abstentions accounted for rather than removed from the denominator.
- **False predicted benefit / observed network harm:** counts, actual magnitude, calibration and extreme adverse tail. Define a defensible decision-risk gate **before** viewing new outcomes.
- **Ranking and candidate regret:** rank predicted external effects among preselected route swaps; explicitly compare to observed rankings and independent own-only choice.
- **Bundle nonadditivity:** predicted joint change versus sum of isolated changes and the actual original SUMO joint contrast. Include anticipated overlap and low-overlap strata, while acknowledging imperfect prospective overlap predictions.
- **Own versus others and nonparticipants:** separately report target ETA delta, all other drivers' aggregate effects, nonparticipant effects and per-driver harm distributions (including >30s realized harm as a historical **diagnostic**, not an automatic policy success claim).
- **Mechanism accuracy:** turn discharge, movement selection, queue waiting, source insertion, receiving-capacity stalls and actual road-entry-time error **only where a comparable archived/authorized observation exists**. Do not claim vehicle-level entry-clock accuracy from 5-second aggregate edgeData alone.
- **Abstention, uncertainty and compute:** report how often v2 refuses to predict or approve a route change, resource cost per 1,000-driver counterfactual pair, and coverage/uncertainty calibration only when independently supported.

**Report tri-state outcome:** DEVELOPMENT QUALIFIED, NOT QUALIFIED, or INCONCLUSIVE, never a retrospective improvement claim based on the old check seeds. Even qualified development merely permits **proposing** an independent validation protocol; it never triggers Test B.

## 6. Implementation architecture and source-review deliverables (future, not yet authorized)

Proposed **new namespace**, leaving the frozen \`research/externality_estimator/\` untouched:

    research/externality_estimator_v2/
        provenance.py             # pinned SUMO/network and allowed t0 feature SHA
        movement_schema.py        # lane-turn request-index, foes/response/cont/unknown contract
        connection_mapper.py      # exact 1.28.0 mapping + audited cross-checks
        constraint_graph.py       # foes, yield, FIFO, internal/via, downstream storage
        scheduler.py              # deterministic prospective movement selection
        network_evolution.py      # synchronous conservation-preserving rollout
        counterfactual.py         # original/swapped/bundle full 1,000-ID predictions
        diagnostics.py            # binding reasons, queue/time traces, abstention
        compatibility_baselines.py # B0/B1/B2/frozen E1-v1 comparison adapter
        tests/                    # all required no-SUMO invariants and negative controls

Architecture is illustrative until an actual code-level protocol freezes APIs, internal state and ordering, conflicting-lane semantics and quantitative resource gates. A parser that imports pinned SUMO code *offline* to understand a network is different from a predictor that queries SUMO traffic outcomes; the latter is prohibited. A production predictor should consume a versioned, audited **static movement contract** instead of embedding simulator future information.

**No hidden code path:** Do not add a \`push: main\` GitHub Actions workflow that automatically launches SUMO jobs when an E1-v2 source PR merges. All simulator dispatch must be explicitly scoped and separately approved.

## 7. Research stop rules and version-control discipline

- **Mapping failure:** If any required move cannot be reconciled to source-index and bitset semantics, stop or mark unsupported; do not invent "non-foe" service.
- **Conflicting movement admitted simultaneously:** hard invariant failure; stop development data generation.
- **Non-foe pair unable to cross due to real physical constraint:** not automatically a mapping error; log the precise source/receiving/internal/priority guard and test the fixture.
- **Circular yield or undefined cont service:** emit conservative fallback/abstain; do not silently invent gaps.
- **Unbounded queue, lost IDs, post-t0 features or mismatched routes:** invalidate prediction, do not score an aggregate improvement.
- **No improvement on genuinely fresh development-check:** report E1-v2 NOT QUALIFIED or INCONCLUSIVE; do not open Stage 2 and do not reselect check probes to rescue performance.
- **Severe predicted-benefit/actual-harm:** report unchanged; do not hide with aggregate MAE, post-hoc calibration or selective abstention.
- **Compute too expensive:** record scaling and infeasibility; do not claim user-device implementability.
- **Scope creep:** an E1-v2 change beyond junction mechanics requires a separately named version and prospective experimental protocol.

Original E1 and all frozen Experiment 007 results remain immutable and independently reproducible from the preserved GitHub releases. Any new V2 evaluation will have its own signed source, schema, feature cutoffs, prediction lock, seed/route manifest, raw-archive SHA, and complete negative-result report.

## 8. Stage milestones and recommendation

| Milestone | Status at publication | Required separate decision |
|---|---|---|
| **J0–J4:** Pinned SUMO priority-junction source verification | **Complete: STATIC MISMATCH VERIFIED** | Do not re-run as though independent science |
| **V2-D0:** Prospective connection-aware junction design (this specification) | **Complete as design proposal** | Review/authorize implementation freeze |
| **V2-I1:** Freeze executable scheduling semantics, APIs, full tests and candidate sources | **Not started** | Approve source implementation |
| **V2-I2:** Implement new v2 namespace; pass no-SUMO physical/information tests | **Not started** | Approve controlled development data only if tests pass |
| **V2-D1:** New independently grouped development-build/check SUMO comparisons | **Not started** | Decide development qualification; old 5111–5114 cannot serve as fresh check |
| **V2-V:** Separate untouched independent estimator validation | **Not started; strictly conditional** | Independent pass before Test B |
| **Test B:** Whole-policy equally informed independent vs cooperative routing, all-driver efficiency and individual/nonparticipant fairness | **Not run; strictly conditional** | Separate protocol and authorization |

**Immediate recommended next document after this approval:** A **versioned V2-I1 executable implementation freeze** with precise graph-selection/priority arbitration logic, internal-lane/cont treatment, deterministic code contracts, resource ceiling, exact no-SUMO test fixtures and one-factor ablation plan. This is **not** equivalent to approving implementation or fresh simulations.

**Final scientific meaning:** J0–J4 justifies investigating connection-aware junction dynamics as a plausible replacement for one E1 modeling simplification. It does not establish network-effect prediction skill. The deliberate sequence remains **understand externality → develop a prospective, genuinely separate other-driver prediction → validate independently on fresh unseen simulations → only then measure whether cooperative routing helps all drivers without unacceptable individual or nonparticipant harm**.

**Publication boundary:** GitHub research specification only. No LinkedIn/X posting was requested or authorized.
