# Cooperative Traffic Research — E1-v2-J Executable Implementation Protocol v1
## V2-I1: connection-aware junction scheduling, no-SUMO verification, and code-freeze contract

**Freeze date:** November 4, 2026  
**Decision:** **V2-I1 IMPLEMENTATION CONTRACT FROZEN IN DOCUMENT FORM. NO E1-v2 SOURCE IMPLEMENTED; NO NEW SUMO RUNS, CALIBRATION, INDEPENDENT VALIDATION OR POLICY TEST B.**  
**Scope:** Implement and test a **single controlled intervention**: replace E1's all-turns-conflict junction admission rule with an explicit, deterministic **priority- and conflict-aware movement scheduler** on the same synthetic, single-external-lane road network. Preserve the original E1 source and failure result. This freezes executable rules and interfaces **before** a separately authorized code implementation. It does **not** authorize any scientific simulation dispatch or public/social-media announcement.

**Parent scientific design:** [E1-v2 prospective scientific design](POST_EXP007_E1_V2_CONNECTION_AWARE_JUNCTION_MODEL_PROSPECTIVE_DESIGN_SPEC_2026-11-04.md).  
**Physical rules evidence:** [Completed J0–J4 original SUMO 1.28.0 priority-junction verification](POST_EXP007_E1_J0_J4_PRIORITY_JUNCTION_VERIFICATION_FINAL_REPORT_2026-11-04.md) and its [durable 10-asset research release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1-j0-j4-priority-junction-verification-2026-11-04).  
**Immutable comparator:** Original Stage 1D [scientific NO-GO](POST_EXP007_E1_STAGE1D_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-03.md), E1 execution source commit \`05b770cf000f84677524e0a1e89bea06ec0e703b\`, model input parser blob \`4ddc2034944354a1605bc798c8df1850e51ea897\`, model queue engine blob \`0d446e2c52efd2b75adf351ad5d577f442a4ac29\`.  
**SUMO network interpretation:** Original pinned SUMO **1.28.0** source commit \`daf91b5578901d599ac9af53f49d26eeb9aefc3b\`, container \`ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb\`. No dependency on live simulator outcomes is allowed in a prospective predictor.

---

## 0. Scientific and authorization boundaries

The original Experiment 007 Test A remains **NO-GO** (8/20 correct externality signs, 40% versus preregistered 60%). E1 Stage 1D remains **DEVELOPMENT NOT QUALIFIED** (E1 externality MAE 1,555.125 network-seconds versus strongest historical B1 1,555.267549 on the frozen development-check cohort; 0.00917% rather than required 5% benefit, plus two severe wrong-sign predicted benefits). The old Test B is **NOT RUN**.

The J0–J4 audit established **1,320/1,320** verifiable junction movement/request mappings, **8,836** unordered within-junction pairs, **5,764** mutually non-foe pairs, **3,940** pairs with distinct incoming/outgoing/initial via lanes, and **2,212** of those with both \`cont=0\`. E1 restricts *all such pairs* to one crossing per junction per one-second model tick. **This is a static-rule discrepancy, not proof that two real SUMO vehicles would simultaneously cross or that a junction fix improves prediction accuracy.**

**This document freezes engineering behavior only.** In particular it does not:
- amend E1's historical outcomes, reported error metrics, model source or scientific decisions;
- choose/reuse historical or current development-check probes to tune E1-v2;
- authorize implementation automatically (separate explicit approval to write/run code), any SUMO runs, a new development simulation budget, training, estimator validation, a Test B optimization policy or social-media publication;
- claim exact replication of gap acceptance, lane-change physics, internal stop behavior, vehicle acceleration, or numerical throughput in SUMO.

The next separate work after this protocol is **V2-I2 implementation plus no-SUMO fixtures**, and after those pass, a **new prospective development-study execution protocol** with completely new development seeds, outcomes and gates. Independent validation and Test B remain later, separate conditional milestones.

## 1. Fixed input domain, source fingerprints and information cutoffs

**Primary supported domain:** the original 10×10 synthetic **priority-junction** SUMO network, **360 external directed edges with one lane each**, 100 priority junctions, 1,320 external lane-to-lane movements. Network geometry/connection/request metadata, permitted edges and announced route intentions are known before the simulated routing decision; this is idealized complete announcement, **not** a claim of real-world visibility into other motorists.

### 1.1 Static movement contract (compile once from frozen network)

Each \`Movement\` record must contain:

\`\`\`text
junction_id: str                     # priority junction
request_index: int                   # SUMO junction request index, NOT TLS linkIndex
incoming_edge, incoming_lane: str
outgoing_edge, outgoing_lane: str
via_lane: str                        # original initial SUMO internal lane
cont: "0" | "1"
direction: str                       # literal original connection direction
foe_indices: frozen set[int]         # raw foes bits, rightmost == index 0
yield_to_indices: frozen set[int]    # raw response bits, rightmost == index 0
canonical_network_sha256: str
raw_network_sha256: str
pinned_sumolib_commit: str
mapping_status: VERIFIED | UNKNOWN | UNSUPPORTED
\`\`\`

**Ingestion rule, hard gate:** Map \`request_index\` by three independent methods used in J0–J4: \`junction.incLanes\`+outgoing connection enumeration; \`via\` ID index; and tagged SUMO 1.28.0 \`Node.getLinkIndex\` / \`Connection.getJunctionIndex\`. Verify foes using \`Node.areFoes\` and response using \`Node.forbids\` at compile time **only**, never call SUMO for future route outcomes. If the relevant network/source hash or any of the three mappings disagree, return \`INVALID_MOVEMENT_MAP\` and **abort before forward modeling**. No guessing with numeric coincidences between 1,320 edge turns and request rows. Reject TLS linkIndex substitutions and reversed bit order.

**Canonical network:** In the original Stage 1D ten archived network files, byte hashes differ due to metadata, while the canonicalized edge, junction and connection structure has the shared SHA-256 \`69c5c32e13987646944cbc7b072d586732402c5b8f3651c379c06fecee65ee14\`. The parser records both canonical and raw file hashes. Any new network hash/domain requires an explicit audited compilation decision, not silent acceptance based on a matching name.

**Supported mapping:** exactly one external lane per original road and exactly one verified movement per traversed external edge-to-edge transition. If the network includes multilaned external roads, ambiguous internal continuation, missing request row/foe/response bit, or unverified movement identity, this *v2-J implementation* must **fail closed** (\`UNSUPPORTED_NETWORK\` / \`INVALID_MOVEMENT_MAP\`) instead of inventing a lane-level priority.

### 1.2 Forecast context and no-clairvoyance boundary

Allowed in \`predict_counterfactual\`: exact static network and preannounced route/OD/departure roster under the synthetic full-information assumption, t0-available network state (this version continues to require **t0=0, initially empty**), source and speed priors frozen before inference, model parameters from designated **future development-build only**, and deterministic uncertainty identifiers. Keep nonparticipants' planned routes fixed in one-probe counterfactuals.

Forbidden: same-seed post-t0 SUMO vehicle dynamics/queues, tripinfo, FCD, detector outcomes, actual alternate-route delay, held-out labels, a secret call to a SUMO executable, or use of the 4101–4105 / 5101–5114 outcomes as untouched validation. Every feature and model input must retain \`observed_at <= t0\` or a separately typed *announced future plan*, not a mislabeled future observation.

## 2. Exact v2-J change and frozen shared physics

**Only permitted model-treatment change versus the E1-v1 comparator:** the junction **movement selection rule and its static verified movement metadata**. Preserve, to the degree the one-lane domain allows, E1's:
- 1-second synchronous tick, deterministic full-driver route progression and finite 1,800-second horizon;
- whole-link FIFO input/source queues; one vehicle can be in precisely one state; same eligible departure, vehicle speed factor and free-flow-ready tick semantics;
- existing link storage \`max(1, floor(length_m * lane_count / 7.5m))\`, \`q_sat=0.50 veh/s/lane\` as frozen **reference only**, source/link/turn service-token mechanics and token cap \`max(1.0, rate*2.0)\`;
- original snapshot-based receiving slots: movement exits this tick do NOT free downstream space in that same tick; source insertions share the pre-tick receiving budget;
- optional paired-route/candidate baseline methods and exact vehicle IDs, and continued **zero predecision state** in this first prototype.

**No changes** to scheduled departure, initial route-choice algorithm, synthetic vehicles, network topology, turn speed, length, nominal spacing, insertion handling or model horizon in the junction-only implementation. Do not silently make q_sat a free parameter, change source admission cadence or introduce an E2 residual learner while testing the junction hypothesis. Report additional model limitations rather than bundling fixes.

### 2.1 Discrete state and global ordering: mandatory pseudocode

In each tick \`t = 0,1,...,1799\`:

\`\`\`text
enqueue only demand with scheduled_departure <= t
snapshot all road queues, original link occupancy, uninserted source queues
receive_remaining[e] = max(0, storage[e] - snapshot_occupied[e])
accrue existing E1 link / per-turn / source service tokens
reserve FIFO destination exits using original E1 ready-time/link-token logic
for junction in sorted(junction_id):
    C = derive eligible SINGLE incoming-lane FIFO-head movement proposals
    validate and classify every C movement against verified priority request matrix
    decide accepted set for this junction via §3, on pre-tick state
    reserve downstream receive_remaining across all selected movements
reserve source insertions against remaining PRE-TICK slots, as in E1
commit destination exits, junction transitions and source insertions synchronously
decrement tokens for exactly the accepted actions
assert mass conservation, FIFO, no negative service, no storage violations
if all N arrived return per-vehicle scheduled-to-arrival elapsed times
at horizon or invalid state emit ABSTAIN/NONCOMPLETION, never completed-only objective
\`\`\`

**Junction proposals:** at most **one currently ready FIFO head per external incoming lane per tick**, after any previously reserved destination exit at that head. Vehicles behind that head cannot become a second candidate in the same tick, even if source tokens might otherwise permit multiple movements. A candidate is *ready* only if: its edge/turn is legal and mapped; it has reached the minimum edge traversal tick; the source link exit token and turn movement token each have at least 1.0 available; the destination has a positive **pre-tick** receiving slot. A proposal not meeting all those requirements is **not a ready competing claimant**, but its exact failed guard is recorded.

**Shared physical occupancy** is enforced per external downstream lane (one lane per road); every accepted movement consumes exactly one of the shared \`receive_remaining\` slots. Any documented internal-via sharing adds a pairwise exclusivity relation; do not invent internal lane storage/temporal movements not represented by the model.

### 2.2 Eligibility and conflict relations

For two ready proposals \`a,b\` at the **same** junction:

- \`foe(a,b)\` if **either** decoded request identifies the other as a foe. The original network's foe pairs are symmetric; if a future network has **asymmetric foe bits**, treat it as \`INVALID_MOVEMENT_MAP\` (never silently treat an asymmetric pair as safe).
- \`yield(a,b)\` means \`a\`'s response bit indicates \`b\` has priority. It must be represented as a directed priority relation **only between ready foes**; do not treat a yield bit as an always-red traffic light.
- \`same_source_lane(a,b)\`, \`same_initial_via(a,b)\` and \`same_downstream_lane(a,b)\` are **additional exclusion relations**, independent of foe bits. Same incoming lane should already be prevented by one-head proposal generation; if two proposals nevertheless share a head or lane, it is an invariant failure.
- \`cont(a) != "0"\` or unsupported intermediate stop metadata creates **Tier C** (conservative service rule below).
- **Tier A:** well-mapped \`cont=0\` movement with verified simple source/outgoing/via. Two Tier A proposals can be considered simultaneously ONLY if mutual non-foes, separate incoming lane, separate outgoing lane, separate via, sufficient send/turn/receiving service and no active priority inhibition.
- **Tier B:** verified foes, including directed yield/asymmetric right of way, where a ready higher-priority claimant must be considered before a ready lower-priority claimant.
- **Tier C:** known \`cont=1\` or otherwise explicitly supported-but-unmodeled intermediate waiting semantics: **exclusive service at that junction for its selected tick**. Tier C is NOT a separate free concurrency class. Unknown bitset or connection mapping is an **input abort/abstain**, not an eligible Tier C service shortcut.

No pair of Tier A movements that are foes may be simultaneously accepted. Multiple distinct non-foe and distinct-resource movements may pass in a tick. **Static non-foe does not imply guaranteed actual concurrent crossing, or physical SUMO equivalence.**

## 3. Deterministic conflict-aware scheduler algorithm (frozen)

**Algorithm v2-J1:** \`READY-FOE-TOPOLOGICAL-GREEDY\`. This is a conservative, deterministic approximation; it does not emulate SUMO's continuous-time car-following or gap acceptance.

### 3.1 Construct ready candidates and priority DAG

For junction \`J\` and time \`t\`:

1. Build \`R\` by selecting at most one FIFO-head candidate per external incoming lane as described in §2.1. **Only ready proposals enter the yield graph.** An absent, unready, already blocked by source/turn token, or downstream-storage-starved vehicle cannot stop an otherwise ready lower-priority claimant merely because a static response bit exists.
2. For every unordered \`(a,b)\` in \`R\`, decode \`foe\` and the *directional* \`yield\` relations using the pinned SUMO request indices. Assert \`yield(a,b) implies foe(a,b)\`; if a request creates two-way yield, a cycle, or an unrecognized priority state, return **\`ABSTAIN_PRIORITY_AMBIGUITY\`** for the complete prospective counterfactual prediction (never guess). Do not "fix" a cycle by sorting IDs.
3. Construct a directed edge \`b -> a\` if \`a\` yields to ready \`b\`; use a topological ordering of only this precedence graph. Unrelated non-foes do not acquire fake yielding constraints.
4. **Tie-breaking / reproducibility:** among current zero-indegree candidates, choose the one first in the *junction-local cyclic sequence* of incoming lane IDs, followed by ascending request index and stable vehicle ID. Store an integer pointer per junction; initialize at 0, advance to the approach following the **last accepted** proposal after each tick; if none accepted, keep the pointer unchanged. No dependence on randomized map/hash iteration order.
5. If a proposal cannot be selected because an earlier accepted proposal conflicts by foe, shares an internal-via or downstream lane, exhausts service/receiving slots, or triggers the Tier C exclusive restriction, record *all binding guards* with one deterministic primary guard; remove that proposal from further consideration for **this tick only**.
6. **Priority-resolution detail:** Process each ready proposal **once** in the topological greedy ordering. If a higher-priority ready foe gets accepted, the lower proposal is blocked by \`YIELD_HIGHER_PRIORITY_READY\` / \`CONFLICTING_FOE_SELECTED\`. If the higher proposal is **not** selected due to another physical guard, it is not a ghost priority claimant and the lower proposal can be considered, subject to the original snapshot and any already accepted competing proposals. A response bit alone is **never** a source of waiting with no actually accepted claimant.
7. For a proposal considered feasible, select it only if it is pairwise eligible against **every** already accepted movement and every per-link/per-turn/receiving limit remains. Two accepted proposals cannot be mutual foes, share a source lane, share an initial internal via, or share an outgoing lane in v2-J1.
8. **Tier C policy (exact):** If a Tier C candidate is selected, accept it only if **no other junction candidate has been selected this tick**; then no further junction candidate may be selected this tick. If a Tier A/B movement was selected first, later Tier C candidates are rejected as \`TIER_C_EXCLUSIVE_SERVICE\`. A Tier C candidate not selected because of insufficient token/receiving is not phantom-blocking. Every known \`cont=1\` candidate counts toward the next tick's deterministic rotation; prolonged Tier C exclusion must be reported as a fairness/throughput limitation.
9. Reserve one downstream slot and one each of available source link/turn service tokens per accepted movement. **Do not** create a second movement from newly exposed FIFO heads within the same tick. All mutations are committed synchronously after selection; preserve E1's source-insertion and destination-exit rules.
10. At the end of this junction, output \`accepted_requests\`, \`rejected_requests\`, \`binding_guards\`, \`rr_pointer_before/after\`, \`priority_edges\`, \`receiving_used\`, \`service_used\`, and \`tier_C_selected\`. Assert these values reconcile exactly to the actual committed occupancy and tokens.

**Algorithm does not maximize count of crossings.** It is a stable, reproducible greedy service approximation that respects verified static rules. The research report must describe its fairness and ordering assumptions as model choices, not as SUMO ground truth. An exact maximum independent-set optimizer is **not** part of v2-J1.

### 3.2 Guard precedence and accounting

Collect **all applicable reasons** for each rejected proposal, but publish a **single primary reason** deterministically using:

1. \`STATIC_MAPPING_UNKNOWN\` / \`INVALID_MOVEMENT_MAP\` / \`UNSUPPORTED_NETWORK\` (model input rejection);
2. \`NO_FREEFLOW_ELIGIBILITY\`, \`SOURCE_FIFO_NOT_HEAD\`;
3. \`LINK_SERVICE_EXHAUSTED\`, \`TURN_SERVICE_EXHAUSTED\`, \`SHARED_RECEIVING_STORAGE_FULL\`;
4. \`ABSTAIN_PRIORITY_AMBIGUITY\`;
5. \`YIELD_HIGHER_PRIORITY_READY\`, \`CONFLICTING_FOE_SELECTED\`;
6. \`SHARED_INTERNAL_VIA\`, \`SHARED_SOURCE_OR_OUTGOING_LANE\`;
7. \`TIER_C_EXCLUSIVE_SERVICE\`;
8. \`MODEL_HORIZON_EXCEEDED\` / \`COMPUTATION_BUDGET_EXCEEDED\`.

An aborted prediction must not produce numerical estimates dressed as complete. Diagnostic counters distinguish *not-yet-ready* vehicles from *ready-but-blocked* vehicles; no retrospective attempt to infer individual SUMO waiting from E1 queue counters is allowed.

### 3.3 Special cases

- **Same-road FIFO:** one externally ready head per incoming lane. Source queue and on-link queue are separate. An arrival behind a just-exited head cannot move until the next tick.
- **Two ready foes, one yields:** accept higher priority first if otherwise feasible, and then exclude conflicting lower. With higher priority absent/unready, permit lower to be considered normally.
- **Priority cycle or mutually contradictory response:** explicitly \`ABSTAIN_PRIORITY_AMBIGUITY\`; do not introduce arbitrary vehicular right of way.
- **Two non-foes sharing outgoing lane:** still **cannot** simultaneously cross in v2-J1, even if receiving capacity is at least two; conservative single-outgoing-lane model contract, not proof SUMO forbids such crossing.
- **Two non-foes sharing initial internal via:** mutually exclusive in v2-J1. Inferred downstream sharing beyond the initial via is unknown, so for this one-lane grid, stop/abstain if a supported test fixture establishes a downstream shared internal bottleneck not represented by this rule; do not invent its capacity.
- **No eligible candidate:** no junction movement, keep RR pointer stable; other already scheduled source insertions or destination exits may still occur globally.
- **Disjoint junctions:** process junctions in sorted ID, but all use the **same pre-tick receiving state** and a shared remaining-slot ledger; a link can receive both upstream road arrivals and source insertions only within that ledger.
- **No change / identical routes:** self, others, total and nonparticipant deltas are exactly zero (subject to fixed numerical tolerance); no spurious divergence from scheduling randomness.
- **Failed paired rollout:** either arm's abort yields an **abstained pair** and is not treated as a scored externality observation.
- **Per-junction time semantics:** predicted crossing at integer tick and actual SUMO sub-second vehicle dynamics are not interchangeable.

## 4. Complete functional interface and immutable output contract

### 4.1 Proposed source layout (new namespace only)

\`\`\`text
research/externality_estimator_v2/
    __init__.py
    provenance.py             # source hashes, feature timestamps, partitions
    movement_schema.py        # typed priority-junction connection/request
    connection_mapper.py      # source-validated static SUMO mapping
    ready_candidates.py       # FIFO heads and token/receiving eligibility
    constraint_graph.py       # foe edges, directed yield DAG, via/outgoing exclusions
    scheduler.py              # v2-J1 topological greedy + Tier C policy
    network_evolution.py      # E1-matched one-second forward state transitions
    counterfactual.py         # full 1000-driver baseline/change/bundle predictions
    diagnostics.py            # per-tick guards, risk, abstentions, resource use
    comparator.py             # read-only frozen E1-v1 and B0/B1/B2 adapters
    tests/                    # deterministic no-SUMO exact fixtures
\`\`\`

The existing \`research/externality_estimator/\` modules and their test outcomes remain **unchanged**. A later source PR must demonstrate that its changes stay in the v2 namespace and the approved no-SUMO test harness, not overwrite the original predictor or old reports.

### 4.2 Function signatures (language-independent contract)

\`\`\`text
compile_verified_movements(
    static_network_xml, pinned_sumo_128_source_ref, archive_fingerprint
) -> MovementContract[verified_records[], foe_matrix, yield_matrix,
                      input_sha, canonical_network_sha, status_or_abstain]

select_junction_movements(
    tick:int, junction_id:str, pre_tick_snapshot:NetworkSnapshot,
    ready_heads:Candidate[], verified_contract:MovementContract,
    service_tokens:ServiceBudgets, receiving_remaining:MutableReservations,
    rr_state:RoundRobinState
) -> JunctionSelection[accepted[], rejected_with_guards[],
                       priority_edges[], reservations[], rr_after, status]

evolve_v2_j(
    Scenario[1000 announced identities, t0=0, all static movements],
    FrozenV2Parameters[q_sat=0.50, one_second_clock, storage, horizon=1800]
) -> Evolution[per_vehicle_arrivals, insertions, diagnostics, status]

predict_counterfactual_v2(
    frozen_scenario, eligible_target_vehicle_id, alternate_legal_route,
    model_version_hash, static_contract_hash, uncertainty_seed
) -> Prediction[1000 matched baseline/swap elapsed values,
                pred_self_s, pred_other_network_s, pred_nonopt_network_s,
                pred_all_network_s, uncertainty_or_abstain,
                input/route/model/parameter hashes, wall_s, peak_RSS]
\`\`\`

**Contracts:** The evaluator never calls SUMO's simulator; offline static movement compilation may use the version-checked \`sumolib\` source, then the runtime predictor consumes **only immutable compiled movement rules**. Feature cutoff is explicit. Each full pair must produce exactly 1,000 original driver identities, including nonparticipants, with no new or missing IDs. \`pred_all = pred_self + pred_other\` within 1e-6 seconds and the nonparticipant sum must be a direct subset of per-driver predicted differences. For bundles, two eligible route changes trigger a **fresh joint forward evolution**, not additive marginals.

The serialized \`Prediction\` must include full individual counterfactual elapsed arrays, one versioned provenance record, full status, input cutoff, route fingerprints, aggregated performance metrics, warning and abstention flags, and complete diagnostics or a referenced hash-stable diagnostic file. **No future SUMO observation** may be available through imports, environmental paths, or model parameters.

## 5. V2-I2 no-SUMO acceptance tests — frozen exact minimum suite

**No SUMO simulations are permitted for V2-I2.** The next source PR must implement named tests and provide exact fixture data/hashes. All suites must pass on Python 3.11 and 3.12 using deterministic fixtures without SUMO executable calls. The original 18 E1 scientific invariant cases remain mandatory as read-only regressions where compatible.

| ID | Test and non-negotiable expected behavior |
|---|---|
| **V01** | **Provenance:** original J0–J4 1,320 movement map matches pinned source; raw/canonical network hash and tag; mismatch rejects input |
| **V02** | **Bit/index correctness:** rightmost request bit is index 0; \`Node.areFoes\` / \`Node.forbids\` agree; artificial reversed-bit/TLS-index substitution fails |
| **V03** | **Mutual non-foe A0 fixture:** two ready, independent \`cont=0\` non-foe turns with adequate service/receiving are accepted in SAME tick; frozen E1 all-class defers one |
| **V04** | **Foe exclusion:** pair with symmetric foe bits can never both be accepted in same tick |
| **V05** | **Asymmetric priority:** ready higher-priority foe accepted before lower; absent/unready or resource-starved higher claimant does not phantom-block lower |
| **V06** | **Cycle/contradiction:** two-way response, directed priority cycle or inconsistent response/foe bits yields explicit \`ABSTAIN_PRIORITY_AMBIGUITY\`, never arbitrary pass |
| **V07** | **One-lane FIFO:** one ready head per incoming external lane, no overtaking or same-tick second-head expansion; other-driver unchanged-route identities remain correct |
| **V08** | **Receiving capacity:** one downstream slot cannot be consumed twice; two non-foes sharing outgoing lane conservatively exclusive even if two slots exist |
| **V09** | **Shared via/internal constraint:** two candidates with same initial via cannot both be selected; unsupported deeper internal link sharing triggers explicit conservative/unsupported state |
| **V10** | **Tier C intermediate \`cont\`:** selected known \`cont=1\` service is exclusive for the whole junction tick; unknown mapping rejects or abstains, never silently treated as Tier A |
| **V11** | **Service budget:** link/turn token guards; fractional tokens accumulate to at least one whole vehicle; no negative tokens or invented bursts |
| **V12** | **Source and insertion accounting:** source-queued delayed vehicles counted exactly once from scheduled departure; source and junction admissions share pre-tick receiving slots |
| **V13** | **Conservation and legality:** each identity occupies exactly one state, legal route transitions only, no negative storage, FIFO breach, impossible travel time or incomplete-only scoring |
| **V14** | **Counters & pointer:** deterministic RR over eligible approaches; no advancing pointer for an unaccepted candidate; blocking guard counts reconcile with accepted and rejected candidates |
| **V15** | **Identical/disjoint counterfactuals:** identical routes produce zero all components; genuinely disjoint routes do not invent other-driver harm |
| **V16** | **Identity-breaking externality:** equal own predicted time with nonzero other-driver predicted change from a coupled junction (not \`external=self\`) |
| **V17** | **Signed effects:** both positive and negative other-driver effects possible on controlled toy networks; sign convention preserved |
| **V18** | **Nonadditive bundles:** two-target joint rollout recomputed and may differ from sum of isolated effects; all-driver and nonparticipant accounting reconcile |
| **V19** | **No-future leakage / partitions:** post-t0 SUMO tripinfo, FCD or oracle fields rejected; previously inspected 4101–4105 / 5101–5114 not permitted as untouched V2 evaluation |
| **V20** | **Hash/determinism:** same input, seed and version yields byte-identical prediction and trace; warning/abstention hashing deterministic |
| **V21** | **Incomplete/abstain:** queue noncompletion at 1,800s, invalid network or uncertainty returns explicit status, not bogus completed-only network time |
| **V22** | **Tier C fairness/coverage:** controlled mixed Tier A and Tier C fixture has deterministic alternating opportunity over ticks when capacity permits; report starvation/deadlock failure rather than quietly ignoring Tier C |
| **V23** | **Speed/snapshot invariance:** crossing cannot occur before free-flow-ready tick, and space freed later in a tick is not prematurely reused |
| **V24** | **Scalability, no-simulator:** 1,000-driver full-graph paired rollout completes with elapsed wall time, memory footprint and abstention rate **reported**, never assumed to meet a production latency |

### 5.1 Hard pass criteria

- V01–V24 **all PASS**, and existing E1 no-SUMO scientific tests remain PASS. No hard tests may be excluded after implementation.
- Explicit A0 non-foe fixture executes 2 compatible movements in one tick; explicit foe fixture executes at most 1; contradictory response yields abstention; sharing physical downstream storage never over-admits.
- Every accepted movement can be justified by the archived static rule, original time eligibility and finite physical budget. Every rejected ready proposal has a traceable reason; counters and vehicle IDs conserve.
- Entire E1 original directory, old scientific reports and historical SHA are unchanged.
- 1,000-driver offline resource measurement is mandatory; **reference investigation budget** is ≤120 seconds per paired candidate and ≤2 GiB peak RSS on a specified GitHub \`ubuntu-latest\` CPU runner, carried from Stage 1B. If the runner is materially different, record \`RESOURCE_REVIEW_REQUIRED\`; do not reinterpret passing fixtures as a deployment guarantee.
- **A pass here is only IMPLEMENTATION-CORRECTNESS / NO-SUMO READINESS.** It is not a development qualification result, an independent estimator validation PASS, or evidence of cooperative policy superiority.

### 5.2 Pre-implementation ambiguity resolution is part of this freeze

The frozen procedure resolves previously open questions as follows:

- Conflict = mutual foe relation; if source file provides nonreciprocal foes, fail input rather than guess.
- Priority = directed response relation among presently ready conflicting requests; topologically order, abstain on cycle.
- Compatible = independent source, receiving and via with mutually no foes, both known \`cont=0\`, adequate token/storage; allow same tick in v2-J1.
- Service selection = deterministic **topological greedy**, not max independent set, sorted globally with documented RR tie-breaker.
- \`cont=1\` = selected turn gets exclusive junction tick; unverified mapping is a hard failure, not another free service movement.
- One-lane source = one ready head/approach/tick; snapshot downstream receiving and source admissions share budgets.
- q_sat = fixed frozen reference 0.50 for V2-I2 correctness; no fitted physical-rate claims.
- Traffic prediction = full-driver paired forward simulation, with zero postdecision information; time-accounting and fairness remain mandatory.

**No other new scientific parameter search or model-family changes** are allowed in the separately authorized V2-I2 source stage. A material change to any rule above requires prospective, versioned protocol amendment before generating or observing new results.

## 6. Strict development-data isolation and later evaluation contract

**No SUMO execution under V2-I1 or V2-I2.** Once source is implemented and unit tests pass, a **separate future V2-D1 protocol** must freeze development seed identities, a prespecified route-perturbation/bundle sampling strategy, expected number of SUMO arms, information/time cutoff, source and input hashes, labels/observation semantics, a primary error measure, false-benefit risk gate and resource budget **before** any new simulation outputs are inspected.

**Current data categories:**

1. \`HISTORICAL_DIAG_ONLY\`: original 4101–4105; six explanatory replay arms; old V1 E1 5101–5114; all inspected J0–J4 static artifacts. These are already seen and cannot become new untouched model checks or validation.
2. \`V2_DEV_BUILD_NEW\`: completely distinct future independent demand seeds, only if separately specified and authorized, for any allowed parameter estimation.
3. \`V2_DEV_CHECK_NEW\`: distinct from V2 build, frozen candidate evaluated once and never retuned using this cohort.
4. \`V2_INDEPENDENT_VALIDATION_FUTURE\`: newly sealed, genuinely never-inspected seeds and route swaps; separate scientific hypothesis, protocol and acceptance criteria.
5. \`FUTURE_TEST_B\`: new matched policy-comparison cohorts **only if** the estimator has passed independent confirmation; do not simply assume unrun old 4201–4210 are fresh.

**Required future comparators:** B0 zero externality; B1 original quadratic proxy; B2 own-time-only/zero externality; **frozen E1-v1** original queue model; and E1-v2-J junction-only treatment. Keep common candidate routes, clock, synthetic demand and forecast information for fair comparison; disclose any unavoidable differences in computational work. Preserve both realized signed externality magnitude and individual harm, nonparticipant subgroup harm, bundle interactions, ranking skill and calibrated uncertainty/abstention. A small improvement in mean MAE alone cannot establish acceptable false-benefit risk.

**V2-D1 outputs** are developmental, not independent validation. No part of this freeze reopens old Experiment 007 Test B or guarantees E1-v2 will pass the new development screen.

## 7. Implementation source review, acceptance artifacts and stop rules

### Next code PR, only after separate V2-I2 authorization

1. Create the new \`research/externality_estimator_v2/\` package, with package-provenance readout and static compiled movement manifest.
2. Implement the exact scheduling routine and no-SUMO fixture test suite before any simulation connectors, CI dispatch or tuning code is present.
3. Supply read-only comparison against original E1-v1 under the same toy cases, preserving all original SHA.
4. Document one-tick candidate trace, priority DAG, chosen compatible movements and rejected/abstained guards; preserve deterministic replay.
5. Instrument total runtime and peak memory at the 1,000-driver research scale, without launching SUMO. If the model abstains, publish the abstention rather than omit the case.
6. Run CI on Python 3.11 and 3.12; freeze the implementation SHA and acceptance report; require scientific source review before merging and before any later development-data approval.

### Source-review stopping conditions

- Any unverified/mismatched request index, reversed bit order, malformed network, unknown active turn or nonone-lane topology: **STOP / INVALID INPUT**.
- Invalid priority (mutual yield or directed cycle), conflicting simultaneous movements, shared via/receiving double-claim, FIFO overtaking, loss of vehicle identities or future-data leak: **STOP / NOT READY**.
- Incomplete predictions, excessive abstentions, resource ceiling failures or unsound Tier C service: **INCOMPLETE / NOT READY**; no silent substitution of E1 old all-class model as a purported V2 result.
- Failed unit tests or unreconciled model source SHA: **DO NOT ADVANCE TO DEVELOPMENT SIMULATION**.
- Accurate-looking historical fit to 5111/5114 wrong-sign cases: **NO VALIDATION CLAIM**, because those observations were already used to formulate the hypothesis.
- Any attempt to dispatch new SUMO development arms or launch Test B under this PR: **OUT OF AUTHORIZATION**.

**Deliverables:** Complete versioned code schema, movement source/canonical network SHA manifest, 24 fixture tests + original E1 regression record, deterministic toy crossing and yield trace, 1,000-driver no-SUMO runtime/memory, explicit model limitations, legal/provenance audit, and a separate short **V2-I2 IMPLEMENTATION READY / NOT READY** report.

## 8. Final scientific and engineering decision

**V2-I1 IMPLEMENTATION PROTOCOL COMPLETE — DOCUMENT FREEZE ONLY.** The exact algorithm is now specified enough to implement without choosing its most consequential behaviors after seeing simulation outcomes. It changes only the proposed junction admission logic, while retaining physically grounded sending, receiving and FIFO guardrails and other-driver counterfactual accounting.

The next conditional, separately approved milestone is **V2-I2: implement the new v2 source package and run V01–V24 no-SUMO tests**. A passing implementation then justifies *consideration* of a separately frozen V2-D1 development-data protocol. A future truly independent validation study and an equally informed cooperative-vs-independent Test B with individual/nonparticipant fairness remain distinct, conditional and unexecuted.

**Do not state E1-v2 improves network-wide prediction or policy outcomes until new, legitimately unseen scientific evidence supports it.**
