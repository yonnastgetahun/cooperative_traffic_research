# B-H1 integrated qualification — evidence register, four-gate acceptance matrix, and disposition

**Date:** November 14, 2026  
**Applies to:** [Integrated prospective protocol v0.1](DIRECTION_B_BH1_INTEGRATED_PROSPECTIVE_PROTOCOL_V0_1_2026-11-14.md) and the prior [execution readiness report](DIRECTION_B_BH1_EXECUTION_READINESS_GATE_2026-11-14.md).  
**Research phase:** **STAGE 1 — SCIENTIFIC DESIGN AND SOURCE REVIEW.** The user approved doing **all four** qualification questions in one bounded segment, with development-only physics validation conditional on a legitimate Stage-1 PASS.  
**Current decision:** **DESIGN CANDIDATE SPECIFIED, EXECUTION STILL NOT QUALIFIED.** No traffic simulations, independent model evaluations, forecast implementation, reserved seeds, empirical outcomes or social-media publication occurred in this segment.

## 1. What is now fixed as a *candidate design*, and what is not established

The [integrated plan](DIRECTION_B_BH1_INTEGRATED_PROSPECTIVE_PROTOCOL_V0_1_2026-11-14.md) resolves earlier *ambiguity about what would be tested* by naming one bounded 2×2 study:

- **Physical setting:** 96 uniquely named prospective vehicles, a main road through S–J–K–T, unrelated W–J–E crossing movement, a 40m J→K storage link, and a timed downstream discharge bottleneck at K. Those geometric/traffic values were chosen **before any B-H1 execution** and are not fitted to outcomes.
- **Physical control:** in S, only the main connection at J may ignore the pinned SUMO no-block heuristic; in N, the **same connection** keeps clear. **No road geometry or nominal K capacity is changed by N.** The difference is explicitly a *junction-driver behavioral rule*, and its effects must be documented. Keep-clear does not switch off queues; it specifically changes whether vehicles enter when the junction may become blocked.
- **Independent I:** same network information, ID set, forecast and \{0,+5,+10\}s choices available to the 12 prespecified eligible main travelers as V; bounded own-cost best responses with a 0.1s residual-regret STOP gate. Old T1 predicted timing costs and its A/B engine are **not qualified substitutes**.
- **Voluntary V:** starts from qualified I, uses **the same** time and forecast options, offers potentially system-beneficial changes to six preselected willing main travelers, honors six decliners, and caps per-driver predicted concession at +5s. The other 84 drivers are ineligible. This is a **hypothetical opt-in model**, not human enrollment evidence.
- **Accounting:** all 96 driver clocks p (preferred), s (requested), d (admitted), a (arrived), full cost, subgroup harm, crossing obstruction, and queue observations. Four cells S-I, S-V, N-I, N-V; \(\Delta_S\) is primary, \(\Psi\) is diagnostic.
- **Prospective safeguards:** report every vehicle (including every cross-traffic nonparticipant), preserve the same exogenous inputs, stop if the independent policy fails its best-response gate, stop on incomplete outcomes or unrelated changes in the negative control, and do not interpret a lower queue without lower *full journey* cost as success.

**These are specified candidate values, not evidence that the physical environment, forecast, choice rule or measurement extraction is operational.** Source-representability and an actual qualifying occurrence of junction blockage require verification; nothing here is an empirical pass.

## 2. Source-backed evidence (what the actual source supports)

| Evidence item | Source verified | Appropriate inference | Unverified part |
|---|---|---|---|
| Junction can have internal lanes, and entry may be controlled by no-block/keep-clear behavior | [Pinned SUMO v1_28_0 intersections](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Simulation/Intersections.md#junction-blocking) | Keeping the junction clear is normally attempted; a connection-level \`keepClear=false\` is a documented candidate intervention; **internal links are necessary** for junction blocking | The proposed J with two through movements has **not** been built/validated; no evidence a driver actually blocks J under S |
| Queues and finite-storage indicators can be instrumented | [Pinned v1_28_0 E2 lane-area detector output](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Simulation/Output/Lanearea_Detectors_(E2).md) | Jam length, occupancy, vehicle counts and halting behavior are available as output families | E2 alone **cannot certify which movement was blocked by which vehicle**; no source-qualified internal-link crossing event ledger exists yet |
| Requested departure may precede actual road insertion | [Pinned SUMO vehicle-definition documentation](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.md) and [pinned insertion documentation](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Simulation/VehicleInsertion.md) | p/s/d/a must be stored separately; complete preferred-departure-to-arrival accounting is necessary | No B-H1 96-identity output schema or all-complete reconciliation has been qualified |
| Prior study's independently optimizing B is tied to a different cost proxy | [Project prior T1 code](../research/t1_timing/feasibility.py), especially its first lines and \`Schedule.personal\`, \`Schedule.optimize\` | Earlier best-response convergence refers to **10s assigned-demand resource costs**; it is not proof of a physically informed B-H1 comparator | New shared forecast/informed I has only a **paper** procedure, no source-verified policy and residual-regret trace |
| Historical scientific cautions are real | [Experiment 006 results](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md); [T1 controlled report](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md); [PR #115](POST_T1_DUAL_FRAMEWORK_SOURCE_REVIEW_AND_DECISION_DRAFT_2026-11-09.md) | Fairness, mismatched driver behavior, complete clocks and event-order coupling cannot be assumed away | No B-H1 observed benefit, safety, human acceptance, or independent cross-model reproduction |

**Version limitation:** the pinned SUMO documentation supports the existence of the relevant features, but is not evidence that a newly constructed traffic scenario produces them. No simulator-default or network-level semantics should be inferred beyond these documented capabilities.

## 3. Four-gate matrix — one qualification decision, not four separate investigations

Two statuses must be kept separate:

- **Protocol-defined:** Does one candidate specify the scientific object and acceptance criteria without being tailored to measured B-H1 outcomes?
- **Executable-qualified:** Is there source-level, artifact and validation evidence sufficient to begin a traffic study without producing an uninterpretable result?

| Gate | Protocol-defined? | Executable-qualified? | Single decisive remaining proof, with STOP condition |
|---|---|---|---|
| **G1: physical spillback and cross traffic** | **YES, candidate** — S/J/K/T and W/J/E topology, 40m storage, K fixed signal; S/N keep-clear explicitly localized | **NO** | Show that this one-road/junction model can be built with correct internal links, valid K signal, permitted crossing, and a source-based event observable for blockage; then verify actual blockage only in a later allowed **development** run. STOP if topology/priority cannot express that claim. |
| **G2: strong, equally informed independent I** | **YES, candidate** — fixed own-cost forecast, timing menu, policy/order/tie/regret gates | **NO** | Complete a reproducible, nonclairvoyant forecast and I decision contract; prove its inputs match V exactly and it can find a stable individual response. STOP if I fails convergence, depends on future observations, or sees less information/fewer options than V. |
| **G3: voluntary V and nonparticipant protection** | **YES, candidate** — 12 eligible, six decliners, six willing, one change each, +5s predicted cost cap, every driver reported | **NO** | Define a verifiable offer/decline event ledger (including zero-take-up) and cost/harm classifications; demonstrate no driver outside eligible IDs is changed, and no decliner is forced. STOP if the claimed benefit depends on coerced compliance or cannot account for all drivers. |
| **G4: N control and 96-ID complete outcome** | **YES, candidate** — one matched keep-clear toggle, same geometry/capacity, Δ and Ψ, full preferred-to-arrival metric | **NO** | Source-qualify an internal junction-blockage log plus trip clocks, and prove the N toggle makes no other unaccounted changes to the model. STOP if no observable conflict event, missing driver, censored trip or altered capacity prevents a trustworthy comparison. |

**Integrated judgment:** All **four scientific design questions now have one explicit candidate answer**, a substantial advance over the previous 0/4 *specification* review. However, **zero are yet independently qualified for executable evidence**, because neither the candidate network nor the common I/V policy nor the complete measurement/control pipeline has been constructed and verified. Reporting "4/4 GO" would conflate paper completeness with physical or operational validity.

## 4. Traceable assumptions and where they can fail

| Assumption | Why included | Principal risk / status |
|---|---|---|
| A 40m one-lane link with 5m cars and 2.5m gaps has roughly five physical spaces | Creates a finite upstream storage near a bottleneck | Geometric simplification, not actual storage guarantee; **unverified** |
| K can apply a 30s-red/30s-green fixed schedule to the lone main movement | Creates transient queue pressure without changing routes | Need source/network construction check; may be unrealistic or unsupported as designed |
| S allows a main vehicle to enter J despite downstream jam; N prevents it | Makes crossing intrusion potentially distinguishable without changing road length | Alters behavioral traffic rule, not just "removes a physical queue"; **causal attribution qualified only conditionally** |
| A 3s forecast service-headway and five-slot threshold approximate the physical queue | Provides one transparent common forecast for I and V | May fail physically, bias rankings, or give a weak I comparator; no oracle allowed |
| 12 timing-eligible main drivers and 6 opt-in candidates represent limited voluntary scope | Probes a non-universal participation setting | Assumed willingness, not actual rational acceptance or measured human behavior |
| Nonparticipant severe-harm thresholds, benefit margin and sample size are candidates | Establish prospective *ideas* of decision criteria | No power/behavioral validation; must be justified/frozen before experiment |
| SUMO 1.28 is reused as a *single physical engine candidate* | Avoids multi-framework scope expansion | Does not imply the reference engine already qualifies the new physical mechanism |

## 5. Immediate bounded qualification package — and no more

To move from **paper design** to an actual **Stage 1 PASS**, restrict the next engineering/source qualification to the **single** design above:

1. **Network and instrument contract:** define source-verifiable input files (nodes, edges, connections, J keep-clear, K signal, 96 intended drivers) and an event/observation ledger for crossing blockage, queue and full trips, without altering historical T1 inputs.
2. **Shared-forecast/independent-policy contract:** specify deterministic event ordering and slot allocation sufficiently precisely to permit the same \(\hat a_i\) function for I and V. Check I's promised termination/stability on the *paper-defined* discrete timing menu; reject a weak comparator.
3. **Opt-in and identity contract:** fixed ID/eligibility/willingness membership, exactly matched I/V records and source-checkable refusal handling.
4. **Paired physical N control and frozen decisions:** inspect the one connection-rule toggle, define which secondary effects would make \(\Psi\) uninterpretable, and freeze all costs, fairness, missing-trip, replication and materiality gates before any physics run.

**Important boundary:** Implementing those fixtures or a policy algorithm is **not being performed by this documentation package**. Before any source/config generation or traffic execution, preserve their scope, review the finished artifacts and record a real 4/4 Stage 1 qualification decision. Only then may a user-authorized, **development-only** physical pilot examine whether J blocking actually appears. No reserved/confirmatory cohorts may be opened during development.

Do **not** continue the old UXsim/CityFlow feasibility loop, retune the T1 proxy, launch an unconstrained congestion search or change the fixed candidate demand merely to cause an encouraging result. Negative feasibility at any gate is a legitimate result.

## 6. Final decision for the approved integrated segment

**COMPLETED:** One coherent B-H1 protocol, one primary I-versus-V comparison, one mechanism-negative N control, one evidence-and-assumptions register and one four-gate acceptance matrix. All are documentation artifacts built from the existing scientific record and source-visible behavior. The candidate is now sufficiently concrete to expose real technical and methodological blockers.

**NOT YET QUALIFIED:** An executable experimental design. Necessary source/model/network artifacts, comparator proof and junction-blocking/clock measurement verification are absent. **Scientific disposition = NOT READY for traffic execution.**

**NEXT GATE (not an automatic four-workstream expansion):** source/static qualification of the *one selected integrated candidate*, followed only on a 4/4 PASS by a bounded development pilot. A failed gate means STOP or an explicitly revised prospective protocol, not quiet post hoc tuning.

**Historical results preserved:** 004 D NO-GO; 006 A/E primary INCONCLUSIVE and severe harm FAILED; 007 Test A NO-GO; original T1 10-second policy development NO-GO; PR #115 cross-framework EVIDENCE INSUFFICIENT.

**What this report does not claim:** a detected instance of physical spillback, a validated voluntary mechanism, a statistically significant efficiency gain, actual human willingness, or any new traffic simulation result.
