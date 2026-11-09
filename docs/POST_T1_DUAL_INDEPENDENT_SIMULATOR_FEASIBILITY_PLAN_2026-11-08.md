# Post-T1 scientific planning milestone — parallel UXsim AND CityFlow feasibility

**Date:** November 8, 2026 (Pacific)  
**Classification:** PROSPECTIVE SCIENTIFIC PLANNING / DOCUMENTATION AND READ-ONLY SOURCE ASSESSMENT ONLY  
**Disposition:** **BOTH UXsim AND CityFlow are mandatory, independently evaluated tracks. SUMO stays a reference; it is not the sole authority on traffic behavior.**  
**Authorization boundary:** Write, review, and publish this plan and source-backed preliminary risk inventory to this GitHub repository. **No new SUMO, UXsim, CityFlow, or other traffic simulation; no simulator smoke test, calibration, new data generation, adapter implementation, policy execution, stochastic replay, new cohorts, estimator tuning, or external social post is authorized.**

## 1. WHY: scientific motivation, not an effort to find a favorable simulator

The research question remains whether voluntary coordination can improve all-driver original-preference-to-arrival costs against **equally informed independent decisions**, without imposing unacceptable harm on people who did not participate. The scientific priority is not to make any simulator return a positive result: it is to determine when a result reflects physical traffic mechanisms rather than an avoidable dependence on one model's representation, random-state handling, or numerical implementation.

Our one previously inspected T1 development seed 2101 contains 1,000 stable intended driver identities, original preferred departures over a 200-second window, a preassigned fixed route for each driver, and original B (independent) and C (coordinated) schedules. Only 12 driver requests moved +10 seconds in C. In the original comparison, 380 matched IDs had different assigned speed factors, preventing a clean timing-only attribution; the original C−B observed +618 network-seconds remains descriptive. The better-controlled B*/C* comparison locked each recorded speed factor to its ID and held routes and twelve original shifts constant; it observed **C*−B* = +2,131 all-driver preferred-to-arrival network-seconds**, including +2,177 across the 988 unchanged-departure drivers and +294 across the 500 nonparticipants (91 additional costs above 30 seconds). The source-and-archive audit found a **plausible** shared lane-associated RNG stream mechanism in SUMO v1_28_0, but did **not** partition that +2,131 into stochastic versus physical causal contributions.

Therefore, the current T1 ten-second forecast and policy remain **DEVELOPMENT NO-GO**. Experiment 007 Test A and E1-v2 NO-GO also remain intact. Neither autonomous-car coordination nor real-world driver willingness has been experimentally demonstrated. These negative and unresolved findings are the reason to examine **two independently developed simulation frameworks**. They do not discredit SUMO, nor do they validate UXsim or CityFlow ahead of review.

**Primary objective for this milestone:** Determine, separately for **UXsim** and **CityFlow**, whether their documented formats and source mechanisms could preserve our original fixed-identity, fixed-route, departure-timing experiment and its all-driver cost accounting *without silently changing the scientific question*. Produce a two-model feasibility disposition, not a new traffic outcome.

## 2. Frozen source contract: what BOTH candidates must preserve

Treat the original archived T1 materials as an immutable reference dataset, with published SHA/provenance and an explicit canonical source hierarchy. The B*/C* evidence release supplies identity-locked records and controlled outputs; the original T1 archive supplies the earliest demand, chosen routes, preferred departures, B/C requested schedules and their original evidence. **Do not treat any simulated arrival from SUMO as an input target for either new framework.** Do not construct an alternative demand from one of the final results.

| Dimension | Nonnegotiable scientific requirement | Documentary feasibility evidence |
|---|---|---|
| **1. Driver identity** | Exactly the original 1,000 unique original driver IDs must be traceable through input, planned release, internal state, finished trip, exceptions, and cost rows. Preserve which 500 are eligible, which 500 are nonparticipants, which 12 are shifted and which 988 have unchanged requested departures. One-to-many platoon representations and generated engine IDs require explicit lossless mapping; never call a group of five vehicles one individual driver. | Named per-vehicle API, flow and ID creation source, representational unit (vehicle vs packet), a deterministic 1:1 ID crosswalk design, and proof obligations for duplicates, drops and insertion order. |
| **2. Original departures** | For each ID preserve immutable preferred departure p_i and the original requested schedules s_i for B and C (or B* and C* as documented), including **sub-second precision**, exact 12 × +10s changes, and all 988 unchanged requests. Distinguish requested release, actual admission to network, and arrival. | Model's time unit, release-file field types, integration time step, rounding and queue rules, and an explicit precision error budget. Truncating 22.6s to 22s is **not** faithful. |
| **3. Fixed routes** | Preserve the complete ordered original **external-edge** sequence r_i for every ID, with valid and unambiguous edge/link mapping; disable dynamic route substitution. Internal junction connectors may differ, but must be documented and must not cause a different external-edge path. | Route-enforcement API or flow format, edge-to-link/road crosswalk and topology/turn-legality validation; document any route construction or connector expansion. |
| **4. Meaningful junction constraints** | Preserve physical opportunity for queues, spillback, competing/conflicting movements, merges, and relevant intersection service limits. Do not simply draw the original grid or assume identical road geometry implies equivalent junction dynamics. | Source-level node transfer/signal/priority/capacity rules, junction conflict and lane connectivity representation, and a **junction-equivalence gap register** against SUMO; document non-equivalences without pretending a bitwise physical match is possible. |
| **5. All-driver accounting** | Retain exact original preferred departure separately. For all 1,000 completed drivers, define C_P = sum_i (a_i,P − p_i). The per-ID bridge is (s_i,P − p_i) + (actual_admission_i,P − s_i,P) + (a_i,P − actual_admission_i,P). Preserve missing/incomplete trips as explicit failures; report affected subgroup rows. Do not double-add on-road waiting or equate network-entry-to-exit travel time with preferred-to-arrival cost. | Per-ID requested/admission/arrival or route-end event sources and lifecycle semantics; how to export exact clocks without dropping finished vehicles, plus an accounting reconciliation contract. |

**Strict parity means input semantics and output measurability, NOT numerical agreement with SUMO trip times.** Different traffic models may legitimately yield different outcomes. Neither may gain a favorable setup from changing demand, routes, voluntary-choice menus, participant labels or posthoc metrics. A problem on one dimension is a disclosed blocker, not permission to simplify silently.

### Immutable reference, comparison structure and metric definitions

- **Reference cohort:** development seed 2101 only, already inspected; use original archival evidence **read-only**. No reserved/unseen demand seeds (including the E1-v2 6201–6212 and conditional Test B 6301–6312 ranges).
- **Relevant arms for future separately authorized comparability:** independent B* and coordinated C*, retaining the same 1,000 IDs, original preferred departures and original requested shifts; A, original B/C and B*/C* are historical, distinguishable sources, not interchangeable labels.
- **Current task:** model/format/source inspection. The 1,000-record scenario is a **specification to assess**, not an instruction to convert and simulate it now.
- **Observational clock contract:** p_i = original preferred departure; s_i,P = requested departure; d_i,P = actual admission/insertion; a_i,P = actual completed arrival. Cost_i,P = a_i,P − p_i. If the simulator logs only an aggregate average, the metric is **not established**. Reject partial-completion denominator changes.
- **Future-only descriptive contrasts:** C_C*−C_B* for all 1,000; shifted 12 vs unchanged 988; eligible 500 vs nonparticipants 500; harmed/helped/unchanged; >30s additional cost and tails. A different simulator's contrast will not be a controlled statistical replication across independent demand seeds without a separately frozen study.
- **Static validation target:** exactly 1,000 unique IDs and 1,000 preferred clock/route records with no many-to-one losses; exact intended schedule pair, zero route substitutions in the proposed representation, all junction constraints traceable, and a defined 1,000-row arrival-logging path. Future executed equality is NOT proven by a static source audit.

## 3. Two mandatory, independent tracks

### Track U — UXsim (must complete even if CityFlow appears easier)

**Framework identity:** [UXsim](https://github.com/toruseo/UXsim) is a mesoscopic / macroscopic Python traffic simulator; unlike microscopic SUMO, default vehicle representation and clock resolution must be examined explicitly.

**Read-only preliminary source observations at commit [b7e2738](https://github.com/toruseo/UXsim/tree/b7e27388757a0e4c64f303c9606a3d5a5ef40388):**
- The Python World.addVehicle API accepts an explicit vehicle name, origin, destination and departure time. The Vehicle.enforce_route method sets a specified route and rejects inconsistent next-link routing. This supports a **candidate** identity and fixed-route mapping, not validated parity for this dataset.
- Default World.deltan is 5 (platoon grouping), and Vehicle converts departure time to a discrete timestep. Default behavior must not be mistaken for 1,000 independent one-car agents or exact fractional release. Assess whether one-driver-per-agent representation and fractional departures can be preserved **without silently altering the model's scientifically meaningful dynamics**.
- The model documents node/merge and signal-based constraints, but equivalence to SUMO's actual priority, queuing and lane-connection behavior is **unproven**.
- Traveled-route and clock APIs include an arrival marker and note a difference between departing the origin and entering the first link under congestion; ascertain whether requested, admitted and arrival times are all recoverable per original ID.

**Required UXsim evidence tasks (source/doc only):**
1. Locate the exact name/identity lifecycle and any auto-renaming/packet semantics in the pinned Python engine; separately record C++-engine differences and **do not switch engines** for convenience.
2. Inspect DELTAN, DELTAT, reaction-time and departure quantization with special attention to original fractional p_i. Determine whether exact preservation is supported; document loss or required prospective design change.
3. Verify method behavior and constraints for one explicit complete enforced route per ID, including path-legality validation and behavior at entry and junctions.
4. Trace signal phases, node capacity, merge priority and queue spillback semantics. Produce a topology/junction crosswalk from archived SUMO primitives to UXsim primitives, with **not representable** explicitly allowed as an outcome.
5. Identify native per-ID admission and finish clocks and a possible noninvasive export path; check completion/abort/wait flags and avoid double-counting queue time.
6. Record unresolved stochastic-driver/packet attributes, numerical resolution and experimental comparability gaps; do not claim UXsim sidesteps all sources of coupling.

**Candidate disposition now:** Explicit IDs and fixed-route enforcement are **source-supported capabilities**; full 1,000-driver individualism, exact subsecond departure fidelity, meaningful junction comparability and complete cost extraction are **NOT YET QUALIFIED**.

### Track C — CityFlow (equally mandatory, not a fallback)

**Framework identity:** [CityFlow](https://github.com/cityflow-project/CityFlow) is a road-network and intersection-oriented traffic simulator with flow-defined vehicles, per-road route definitions, lane links and traffic phases.

**Read-only preliminary source observations at commit [81ee0f4](https://github.com/cityflow-project/CityFlow/tree/81ee0f47659ca66177a71f81676691c58ee89184):**
- The documented flow file supports explicit ordered road routes and startTime/endTime plus an interval. In engine source, each flow is numbered flow_i and creates vehicles with IDs such as flow_i_0. There is **no verified native source-ID field in that standard flow schema**; a stable explicit crosswalk would be necessary even if one single-vehicle flow per original driver is feasible.
- The inspected flow loader reads startTime/endTime as **integers**. The included SUMO conversion example uses int(float(depart)), which loses original fractions such as 22.6s. This is a **current material precision blocker** for an unmodified standard-file import, not an acceptable rounding convention.
- The roadnet schema documents roadLinks, laneLinks and traffic-light phases, which are promising for concrete junction constraints. Their behavior and topology may still differ from SUMO; automatic conversion cannot be presumed faithful.
- The Python API exposes currently running vehicle IDs and state and an **aggregate average travel time**. In C++ engine source, finished vehicles are removed from the live vehicle map. Neither fact alone establishes a persistent original-ID-to-arrival ledger suitable for the required cost equation.
- Vehicle start and finish timing can be affected by flow generation and network admission; preserve the requested-vs-realized clock distinction, not only flow startTime.

**Required CityFlow evidence tasks (source/doc only):**
1. Inspect flow generation, integer release parsing, interval stepping, start/end inclusivity, entry queues and vehicle ID assignment. Specify a **lossless** 1,000-ID crosswalk with exactly one generated vehicle per original ID, or mark it unsupported.
2. Determine whether original fractional departures can be represented faithfully under a documented supported API. If not, classify **BLOCKED FOR EXACT T1 REPLICATION**, and describe any hypothetical future engine change only as a *new, separately authorized engineering project*, not something performed now.
3. Check complete ordered route semantics and all original route turns, laneLinks and roadLinks (no implicit shortest-path substitution); compare converter edge mappings against original route IDs.
4. Inspect intersection conflict/priority behavior, signal defaults, stop lines and queue/entry capacity against the original 10×10 grid. A geometrically matched grid is insufficient.
5. Inspect event/vehicle lifecycle data and replay hooks for **per-original-ID completed arrival**, actual admission and exceptions. Aggregate get_average_travel_time is **insufficient**; define the missing instrumentation boundary without implementing it.
6. Document which dynamics and random stream controls can be held invariant per mapped driver across B*/C*. Never claim CityFlow is the scientifically 'correct' replacement simply because its randomness differs.

**Candidate disposition now:** Explicit routes and nontrivial junction structures are **source-supported capabilities**; exact fractional departure clocks are **blocked by the inspected standard flow-loader path**; identity mapping, all-driver completion clocks and behavioral equivalence are **NOT YET QUALIFIED**. Do not upgrade to GO solely because a converter exists.

## 4. Parallel evidence matrix and classification rules

Complete the same five-row assessment for **each model**. Neither may be dropped, deferred indefinitely, or selected in place of the other based on ease of use.

| Requirement | UXsim — preliminary status | CityFlow — preliminary status |
|---|---|---|
| 1,000 original identities | **Candidate**, named addVehicle; default grouped-vehicle semantics require audit | **Candidate with mapping**, generated flow-based IDs; 1:1 generation unverified |
| Original subsecond schedules | **Open / potential blocker**, timestep quantization requires audit | **Blocked in inspected standard flow loader** (integer startTime); alternate faithful API not established |
| Fixed original edge routes | **Candidate**, enforce_route available; original edge crosswalk unverified | **Candidate**, ordered flow routes; topology/lanelink legality unverified |
| Meaningful junction constraints | **Candidate**, mesoscopic nodes/merges/signals; semantic gap unmeasured | **Candidate**, laneLinks/roadLinks/signals; semantic gap unmeasured |
| Preferred-to-arrival 1,000-driver cost | **Open**, arrival/log path exists; full release/admission/finish bridge unverified | **Open / significant gap**, live vehicle API and aggregate average alone insufficient |

These are **planning-level source observations**, not empirical feasibility passes. Assign final documentation-review classifications independently per dimension:

- **SOURCE-SUPPORTED / QUALIFIED FOR FUTURE IMPLEMENTATION REVIEW:** exact relevant API, source semantics and traceable mapping identified; all invariants feasible *on paper*; still NOT tested in a simulation.
- **BLOCKED:** inspected architecture or interface cannot satisfy an invariant without changes or losses.
- **UNRESOLVED:** documentation and source inspection are insufficient to establish fidelity.
- **NOT REPRESENTATIONALLY COMPARABLE:** the model may be useful for broader research, but alters the scientific unit, topology/junction mechanism or outcome in a way that cannot support the original matched-driver hypothesis.

Never equate a SOURCE-SUPPORTED verdict with empirical validated equivalence. No GO to run traffic is allowed under this milestone.

## 5. Work packages and publication requirements

**P0 — Evidence freeze and provenance.** Inventory exact archived T1 reference inputs/release SHA, research arms and clock definitions. Identify the canonical immutable 1,000-ID demand, route and original-preference records; do not reconstruct them from aggregate summaries or changed arrival outputs. Pin UXsim and CityFlow repository commit SHA, official docs paths and source lines. Review only.

**P1-U — UXsim evaluation.** Produce one independently authored UXsim five-axis source/evidence ledger with specific paths/line references, identity/packet audit, original fractional-departure analysis, exact-route enforcement check, junction gap table, clock-export mechanism and blocker list. Do not run a sample.

**P1-C — CityFlow evaluation.** Produce one independently authored CityFlow five-axis ledger of the same depth: flow identity mapping, integer schedule limitation, route/junction legality, engine admission, completed vehicle clock extraction and blocker list. Do not run a sample.

**P2 — Joint static comparability review.** Place the **two complete** ledgers side-by-side using the same immutable scientific contract. Explicitly record differences in platoon/vehicle unit, numerical time granularity, turning and priority rules, congestion spillback and per-driver clock availability. Inspect whether a credible common *question* can be tested in both, not whether their motion should match SUMO's exact numbers. **Do not relax a requirement because one simulator fails it.**

**P3 — Prospective scientific decision (no execution).** Issue one of:
1. **BOTH SOURCE-QUALIFIED FOR FUTURE DESIGN** — each meets the static contract independently; propose separate implementation and validation protocols, only for later approval.
2. **ASYMMETRIC / ONE BLOCKED** — record the full UXsim and CityFlow assessment, keep the blocked track explicitly open, and specify a minimal corrective feasibility question for each gap. Do not report 'two independent validators' or silently use only the easier one.
3. **BOTH BLOCKED / FRAMEWORK REFORMULATION NEEDED** — retain SUMO reference and report what faithful comparison cannot currently support. Recommend a revised future hypothesis with a new user decision, not a forgiving substitute scenario.
4. **EVIDENCE INSUFFICIENT** — publish the precise missing source evidence and stop. Absence of traffic runs is intentional, not an inconclusive traffic result.

**Deliverables to publish together at the close of the assessment (not claimed complete by this plan):**
- UXsim source evidence ledger and proposed lossless mapping contract.
- CityFlow source evidence ledger and proposed lossless mapping contract.
- Shared five-axis parity/junction/clock comparison matrix, including any irreducible model-family differences.
- A one-page **both-tracks** GO-to-design / BLOCKED / INCOMPLETE recommendation with named next authorization checkpoints.
- Frozen scientific question, original archive links and reproducible source revision pins. Negative capability findings are first-class results.

## 6. Governance, stopping rules and next authorization

1. **No new experiments in this milestone.** This includes no quick benchmark, tiny synthetic example, import-and-run smoke test, retrospective resimulation, simulator installation followed by an engine step, or hidden rerun in CI. Only source, documentation, manifest/schema and archival inspection are allowed.
2. **No model implementation or tuning.** No adaptations to CityFlow/UXsim clocks or engine internals, no SUMO random-stream patch, no traffic model calibration, no new forecasting model, no route/per-driver scheduling policy changes.
3. **No claim of independent scientific confirmation.** Until both frameworks are characterized, adapted through separately authorized work, and each tested under a prospective frozen and fair protocol, the T1 observed harm, forecast failure and RNG mechanism evidence remain SUMO-specific development observations.
4. **No changed cohort or release gates.** Seed 2101 stays already inspected development evidence; reserved cohorts stay unopened. Any eventual test requires explicit prospective input/control freeze, compute footprint, acceptance and severe-harm reporting plan, and separate user approval.
5. **Nonparticipant fairness is mandatory.** A simulator adaptation that loses the original 500 nonparticipant labels, per-driver effects or completed-arrival clocks cannot answer the project question even if it reports plausible overall congestion.
6. **Preserve contradictory evidence.** Do not discard a simulator because it is inconvenient or gives a different answer. Do not choose it because it produces positive results. Document the limitations of each model as well as SUMO.
7. **Publication scope:** This plan is authorized for **GitHub documentation only**. A new substantive result or public LinkedIn/X announcement requires a separate editorial decision; the preceding T1 pivot announcement is historical and must not be reposted.

**Exit condition for the planning milestone:** A clear, version-pinned, reproducible **dual-track feasibility plan** is published (this document). No UXsim or CityFlow scientific qualification is claimed by publishing it. The **next execution boundary** is a separate authorization to conduct the two read-only source evaluations and/or later implement adapters and run traffic simulations. Publication of this plan is not authorization for either.

## 7. Sources and source hierarchy

**Project's own archival evidence — controlling for facts about T1:**
- [Prospective original T1 design, B/C policy fairness and cost accounting](POST_C1_T1_PROSPECTIVE_TIMING_PROTOCOL_CANDIDATE_2026-11-05.md).
- [T1 original feasibility outcome and forecast sign reversal](POST_C1_T1_TIMING_FEASIBILITY_FINAL_DEVELOPMENT_REPORT_2026-11-06.md).
- [Original B/C identity/speedFactor confound](POST_T1_EXPERIMENTAL_CONFOUND_ARCHIVE_DIAGNOSTIC_AND_STOP_2026-11-06.md).
- [Controlled B*/C* final scientific report and 1,000-ID source provenance](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md).
- [SUMO stochastic event-order versus physical propagation source-and-archive final report](POST_T1_SUMO_RNG_EVENT_ORDER_AND_PHYSICAL_PROPAGATION_SOURCE_AUDIT_FINAL_REPORT_2026-11-07.md).
- [Preserved B*/C* complete evidence release, checksums and per-driver manifest](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/t1-idlocked-dev2101-2026-11-07).

**Independent framework sources — relevant capabilities only, NOT experimental validation:**
- UXsim [official documentation](https://toruseo.jp/UXsim/docs/index.html), [vehicle/world/route, departure and node source at pinned commit](https://github.com/toruseo/UXsim/blob/b7e27388757a0e4c64f303c9606a3d5a5ef40388/uxsim/uxsim.py); [framework model description](https://toruseo.jp/UXsim/docs/mechanism.html).
- CityFlow [flow format](https://github.com/cityflow-project/CityFlow/blob/81ee0f47659ca66177a71f81676691c58ee89184/docs/source/flow.rst), [roadnet and junction format](https://github.com/cityflow-project/CityFlow/blob/81ee0f47659ca66177a71f81676691c58ee89184/docs/source/roadnet.rst), [flow generator / ID semantics](https://github.com/cityflow-project/CityFlow/blob/81ee0f47659ca66177a71f81676691c58ee89184/src/flow/flow.cpp), [engine loader and completed-vehicle behavior](https://github.com/cityflow-project/CityFlow/blob/81ee0f47659ca66177a71f81676691c58ee89184/src/engine/engine.cpp), [existing SUMO conversion code, integer truncation risk](https://github.com/cityflow-project/CityFlow/blob/81ee0f47659ca66177a71f81676691c58ee89184/tools/converter/converter_v2.py), [Python/API reference](https://cityflow.readthedocs.io/en/latest/start.html).

**Evidence standard:** Cite exact pinned source versions in the eventual assessment, distinguish original archival outcomes from framework source claims, and label every extrapolation as an inference. No finding about actual UXsim or CityFlow T1 traffic outcomes can be inferred from this document.
