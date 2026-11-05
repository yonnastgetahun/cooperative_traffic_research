# Cooperative Traffic Research — Controlled Junction Effect-Modification Study
## Proposed next milestone after the E1-v2 four-arm vehicle-level investigation

**Date:** November 5, 2026
**Status:** SCIENTIFIC DESIGN PLAN ONLY; NO simulation, implementation, source change, holdout access, or public/social publishing authorized by this document.
**Scientific classification:** Prospective *physical-intervention design* on previously inspected synthetic traffic cases, not an independent test of a prospective externality predictor.
**Study label:** Post-Experiment-007 C1 (mechanism study, not Experiment 007 Test B or an E1-v3 study).

## 1. Why this matters to the overall research — and what the result would enable

**The overarching project question is whether voluntary coordination among drivers can improve total network travel time compared with equally informed independent routing, while bounding harm to individual participants and nonparticipants.** This is motivated by the possibility that shared awareness and collective decisions could realize some efficiencies imagined in future autonomous transportation networks, even when vehicles are human-driven.

A route recommendation's effect is more than the travel time of the driver receiving it. A changed route can create or dissipate queues, alter intersection service order and change the journey times of other drivers who keep exactly the same planned routes. To make collective routing decisions responsibly, a coordination system would eventually need to predict those **marginal network externalities** rather than simply favor routes with attractive individual costs.

Our observed research sequence has not yet established that ability. Experiment 007 Test A failed, E1-v1 failed development qualification, and connection-aware E1-v2 failed its frozen development gate. The F0–F5 audit and the subsequent four-arm passive replay measured substantial, opposite-sign network effects, confirmed that they involved real in-network stopped-time differences, and revealed temporally coupled traffic responses. **But they did not establish which physical junction/queue mechanism materially changes the causal effect of a route assignment.**

**This next study turns one plausible physical explanation into a controlled, falsifiable question:** if we change only a predeclared priority-junction service rule, does the **network-wide effect of the same route swap** change? Such evidence would help decide whether a future estimator should explicitly represent localized junction priority/receiving constraints, whether a different mechanism should be investigated, or whether the case remains too sensitive or ambiguous to justify further algorithm development.

**The bridge is: voluntary coordinated routing → accurately estimating the consequences of possible route changes → identifying which physical interactions determine those consequences → only then developing and independently evaluating a new estimator → eventually testing collective policy efficacy/fairness against an equally informed independent system.** This experiment addresses the middle step. It does **not** itself demonstrate that coordination works, establish global system optimality or imply a safe real-world traffic intervention.

## 2. Established evidence, not new claims

The completed [four-arm passive replay final report](POST_EXP007_E1_V2_FOUR_ARM_PASSIVE_REPLAY_FINAL_SCIENTIFIC_REPORT_2026-11-05.md) and its [verified original FCD/vehroute evidence release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1v2-fourarm-passive-vehicle-replay-2026-11-05) describe two outcome-selected comparisons on the same 10×10 SUMO 1.28.0 synthetic priority-junction network:

| Original seed | Changed driver / arm | Others' net travel-time change | All-driver travel-time change | SUMO recorded waiting difference | Independent FCD near-stop sample difference |
|---|---|---:|---:|---:|---:|
| **6112** | veh0142 / probe2 vs I | **+3,215 network-s** | +3,219 network-s | +2,775 vehicle-s | +2,768 |
| **6113** | veh0038 / probe2 vs I | **−3,960 network-s** | −3,883 network-s | −3,050 vehicle-s | −3,062 |

All four instrumented replays reproduced all 4,000 original driver records exactly. In seed 6112 the first matched target-driver trace difference was observed at **43 seconds**, with the first other-driver difference at **44 seconds**. In seed 6113 those times were **21 and 23 seconds**. The simulator's actual departure-insertion component was small relative to the overall observed travel-time contrast in each case.

[Archived per-edge FCD hotspot differences](results/exp007_e1v2_fourarm_passive_2026_11_05/nearstop_edge_5s_hotspots.csv) show that seed 6112 had **+2,433** signed near-stopped vehicle samples on directed road **D3E3** under the changed route, with the first 5-second bin of at least ten samples' difference at **155 s**. The route-change target itself took an A/B-side corridor in the observed route traces, not D3E3; this makes D3E3 an **indirect-response candidate**, not a proven source of the first divergence.

**Important timing qualification:** The D3E3 diagnostic peak occurs *after* the earliest observed whole-network trajectory changes. Therefore a junction downstream of D3E3 cannot simply be called the unique *initiator* of the response. At most, the present evidence makes it plausible that this area is a later **amplifier or redistributor** of effects. A different initial mechanism could have triggered the first network divergence.

The [J0–J4 SUMO priority-junction audit](POST_EXP007_E1_J0_J4_PRIORITY_JUNCTION_VERIFICATION_FINAL_REPORT_2026-11-04.md) independently mapped all 1,320 original junction movements and verified static foe/response semantics against the pinned SUMO source. This supports a grounded priority-intervention specification. It does not establish actual movement-specific service rates.

**Frozen status carried into C1:** original Experiment 007 Test A **NO-GO**, E1-v1 development **NOT QUALIFIED**, E1-v2 D1 **DEVELOPMENT_NOT_QUALIFIED**, independent estimator validation **NOT STARTED**, collective cooperative Test B **NOT RUN**. None may be recoded based on C1.

## 3. Primary question and sharply bounded candidate

**Primary causal question in this synthetic system:** For the frozen single-route perturbation probe2, does a prospective, local change to *right-of-way priority at junction E3* alter the realized **marginal total elapsed-time effect** of that route perturbation, beyond the effect the same physical rule change would have produced under the original independent route assignment?

**Preidentified candidate:** Priority junction **E3**, specifically the approach involving **D3E3**. It is chosen retrospectively from the reported seed-6112 near-stop difference, not from a fresh validation cohort. E3 is a *candidate site for effect modification*, not a confirmed traffic bottleneck or a declared cause of the original +3,219 network-second increase.

**Only permissible primary intervention family:** One minimal, static, geometry/route-preserving **right-of-way priority-order modification** between an identified conflicting E3 movement from D3E3 and one other eligible conflicting approach. The physical question is priority/junction service, **not** opening a new lane, moving roads, rerouting, changing departures, adjusting following models or inserting/removing vehicles.

Before execution, a read-only source/trajectory feasibility stage must select and pin **exactly one connection pair and one direction of right-of-way change**. Deterministic selection among source-verifiable E3 conflicting pairs involving the D3E3 inbound lane: choose the pair with the highest count of 5-second bins in **120–300 s** containing sampled approach presence from both incoming directions in original archived 6112/I, then tie-break by canonical lane/connection IDs. Eligibility requires legal distinct incoming/outgoing movements, an actual priority relationship that can be modified without removing the movements, and movement mapping validated against the pinned SUMO 1.28.0 network semantics.

The candidate and exact network difference must be appended to a **frozen executable protocol before any intervention SUMO outcomes**. If the selected pair does not support a safe, scoped legal network edit, or if source equivalence beyond E3 cannot be established: **DESIGN/FEASIBILITY NO-GO; do not pick a different site after inspecting outcomes, and do not run a substitute experiment.**

The study does **not** assume that favoring D3E3 will necessarily make its drivers faster; local priority changes may transfer delay to crossing approaches. For that reason, the primary estimand tests **effect modification**, not a promised directional benefit.

## 4. Controlled factorial comparison and maximum new simulation footprint

Define, for each already inspected seed s, two **route-assignment states** and two **junction states**:

- Route factor R=I: the original independent traffic-aware planned routes held fixed.
- Route factor R=P: the same exact original single-target probe2 route assignment, with the other 999 original routes unchanged.
- Physical factor J=0: the original E3 priority rules, with no modification. This must reproduce the archived four-arm historical inputs/outcomes after any network-conversion steps.
- Physical factor J=1: exactly the source-frozen priority-order edit at E3, with all routes/OD/departure schedules and all other junction/edge physics held fixed.

The **same intervention construction** applies to both original seeds. Seed 6113 is a contrasting, outcome-selected case, **not** a random independent confirmatory replication or a guaranteed negative control.

| Seed | Original/no-op J=0, I | Original/no-op J=0, probe2 | Modified E3 J=1, I | Modified E3 J=1, probe2 |
|---|---|---|---|---|
| **6112** | Matched no-op reconstruction | Matched no-op reconstruction | New intervention | New intervention |
| **6113** | Matched no-op reconstruction | Matched no-op reconstruction | New intervention | New intervention |

**Maximum footprint if later approved:** **8 new SUMO arms**: four necessary original-equivalent **no-op reconstruction** controls and four E3-modified cases. The previously completed historical 4 instrumented replays are archived parity anchors and need not be run yet again without a clear reproducibility necessity. All eight new runs would be at the exact original seed/route/schedule/step-length values. Original archived data and reserved validation/Test B seeds are never replaced or accessed.

A no-op **reconstruction control is essential** because SUMO network conversion can produce differences beyond the desired local priority rule. Its four arms must reproduce the corresponding historical tripinfo records (and safety/exception diagnostics) at the predefined G2 tolerance. If they do not, the priority intervention is **not interpretable** and subsequent J=1 runs must not occur. Similarly, all J=1 variants must preserve every original external road edge, connection legality, 1,000 scheduled trips and unchanged planned route assignments. Internal priority/response differences must be localized to E3 and explicitly audited; unrelated geometry, speed, lane count or right-of-way changes cause **STOP**.

## 5. Primary outcome and why it tests a physical mechanism

For each seed s, route choice R and physical setting J, define all-driver scheduled-to-arrival cost:

C(s,R,J) = sum over all original 1,000 drivers of (arrival(s,R,J,i) − scheduled_departure(s,i)).

The marginal route-assignment network effect in one physical setting is

D(s,J) = C(s,P,J) − C(s,I,J).

The **primary controlled interaction** is

**Psi(s) = D(s,1) − D(s,0).**

Thus **Psi(6112)** asks whether changing the E3 junction rule changes the route swap's +3,219 network-second historical impact. **Psi(6113)** asks the analogous question about its −3,883 network-second historical impact. Holding the junction rule modification common across I/P is essential: simply comparing the new modified-probe2 arm against old I would confound a route effect with changed network physics.

**Interpretation:** A nonzero Psi identifies **route-by-physical-intervention effect modification in the simulated system**, assuming original-input parity and a truly localized modification. It does **not** uniquely isolate waiting at E3 as the mediator, prove E3 was the first source of the original effect, demonstrate global robustness or improve the predictive E1-v2 development score.

**Supporting first-stage evidence:** Verify that the priority edit actually changes observed E3 movement order, approach waiting or sampled internal-lane discharge in a fixed **120–300 s** diagnostic window. If no measurable local service difference occurs, label **MANIPULATION_INACTIVE**, not evidence for or against E3 mediation. Compare observed early/late windows without realigning arms.

A **descriptive practical materiality screen**, not a significance threshold, is absolute Psi(6112) >= **10% of original |D(6112,0)|**, approximately **322 network-seconds**, *and* a verified E3-local dynamic response. Values below that screen are reported as small in the selected case, not as a formal proof of no effect. Present exact Psi for **both seeds regardless of threshold**, with signed and absolute individual harms and spatial positive/negative effects.

Repeat the same controlled interaction calculation for **nonparticipants** (fixed 500 opt-out identities), changed target, other 999, and observed in-network waiting versus source insertion. Never add waiting to scheduled-to-arrival cost: it is already inside journey duration.

## 6. Competing explanations, disconfirmation and diagnostic measurements

| Hypothesis | Evidence consistent with it | Contrary/ambiguous evidence |
|---|---|---|
| **H_J — E3 priority service amplifies or redistributes the route effect** | E3 rule edit changes actual movement service and Psi is material; changed downstream/upstream responses occur after modified E3 crossing behavior | E3 service changes but Psi is negligible, or Psi changes before any E3-related difference and remote effects dominate |
| **H_Q — Receiving capacity/queue propagation elsewhere dominates** | The new E3 rule produces little response, but measured queues persist at downstream receiving links or unrelated junctions; altered road-level effects are spatially distributed | Local E3 response and large Psi support E3 as an effect modifier, though do not disprove additional queues |
| **H_T — Earlier timing changes initiate the cascade** | Earliest other-vehicle divergence remains before E3 hotspot onset, even when E3 intervention modifies later amplitudes | E3 service differences precede most measured secondary effects, subject to one-second sampling ambiguity |
| **H_A — Reconstruction, simulator/event-sequence or hidden-physics artifact** | The no-op rebuilt network changes original trip times, safety records or non-E3 physics; no valid causal contrast exists | No-op controls reproduce exactly and all non-E3 structural invariants match, supporting interpretable E3 intervention contrasts |

**Required observations:** one-second vehicle FCD and road/lane transitions, complete original-matched tripinfo and vehicle-route exits, five-second edge/lane waiting and throughput, verified priority-connection/movement mapping, upstream stopped-vehicle clusters, alternative explanations, 90th/95th-percentile matched individual change, >30-second harms and participant/nonparticipant differences. Both improved and worsened edges and vehicles must appear in the report.

The earlier recordings demonstrate *association*. This new **controlled factor** establishes a causal effect of the *specified E3 network intervention* on the route-swap network response **if the integrity gates pass**. It does not separately randomize queue waiting or every local traffic mediator. Do not claim more specific mediation than the manipulated physical condition supports.

## 7. Pre-execution gates, stopping rules and validity boundaries

**Gate C0 — Immutable original evidence:** Verify the original 695-member E1-v2 source archive and permanent SHA-256 member ledger, exact four historical routes/tripinfos, frozen source image, predeclared D1 NO-GO, stable original 1,000 identities and scheduled departures. Any missing or mismatched file stops the design before simulations.

**Gate C1 — Pinned-version E3 intervention feasibility (NO SUMO):** Use the verified 1,320-movement SUMO source mapping, selected E3 movement pair and original one-second FCD. Specify the precise road/right-of-way attribute edits and deterministic build commands under pinned SUMO **1.28.0**. Confirm no unrelated changes in external edge topology, lane count/speed, route legality, signal control, vehicle behavior, departures or non-E3 request metadata. Freeze generated network SHA and full semantic diff for J=0 and J=1 *before outcomes*. Failure to isolate the intervention -> **DESIGN NO-GO**, not an excuse to explore another bottleneck.

**Gate C2 — No-op reconstruction equivalence:** Run the four J=0 controls only after separately approved execution. Compare all 4,000 driver records to original archived results at **<=0.02 seconds per driver-field** and whole-network totals **<=0.1 network-second per arm**, preserving the previous passive-replay conventions. Compare all available safety, collision, emergency and teleport fields. If reconstruction disagrees: stop without opening the J=1 arms and publish an input-network fidelity failure.

**Gate C3 — Fixed E3 intervention and first-stage manipulation:** Run exactly four J=1 cases only if C2 passes; record network diff, all completed trips, 1-second vehicle lanes/timing, E3 movement service and signed waiting/throughput differences. No change of network or tuning after reading the first changed-physics outcome. If the intervention produces collisions, invalid routes, inconsistent IDs, incomplete trips or inconsistent physics: classify as **INVALID INTERVENTION**, preserve all data and stop physical claims.

**Gate C4 — Independent, preregistered arithmetic audit:** Recalculate Psi and supporting participant/nonparticipant contrasts from original 1,000 identities and scheduled-to-arrival endpoints; audit exact outcome matrices and time-resolved physical responses, effect modification, potential counterexamples, and sign/cancellation. An outcome-selected two-seed case study cannot establish population estimates or formal generalization; no new significance claims based on 2 seeds or 8 nested arms.

**Hard boundaries:** No E1-v2 parameter adjustment; no E1-v3 implementation; no alternative intervention selected after seeing new results; no new time-shift mechanism; no replacement seeds; no random parameter sweep; no reserved **6201–6212** validation or **6301–6312** Test B; no redefinition of old failed D1 accuracy/safety gates; no automatic social publishing.

The study uses priority rather than signalized junctions. SUMO documentation notes that right-of-way depends on junction and edge-priority rules and distinguishes conflicting foes from yielding relationships. Exact semantics must be pinned to SUMO 1.28.0 before C1 is declared feasible: [SUMO plain network priority/right-of-way](https://sumo.dlr.de/docs/Networks/PlainXML.html) and [SUMO network request/foe definitions](https://sumo.dlr.de/docs/Networks/SUMO_Road_Networks.html). Do **not** use a calibrator as an allegedly passive service intervention: SUMO calibrators may insert/remove vehicles and change speeds, violating the fixed-demand comparison ([SUMO calibrator semantics](https://eclipse.dev/sumo/docs/Simulation/Calibrator.html)).

## 8. Deliverables and one scientific next decision

**Deliver one bounded research package once a separate execution is authorized:**

1. Prospectively frozen C1 movement selection, source/geometry diff, and exact paired 8-arm command manifest; no-op/rebuild and priority-intervention network SHAs.
2. Full C0–C4 validity audit including original-vs-no-op per-driver equivalence, collision/exception and complete-route coverage.
3. Exact **2 seeds × 2 routing assignments × 2 physical settings** scheduled-to-arrival results and seed-specific Psi interaction estimates, self/others/nonparticipant/fairness contrasts.
4. Vehicle-level approach, E3 junction discharge and receiving-edge time plots and 5-second queue/flow diagrams with both supporting and contrary cases. Show upstream/downstream lags but do not infer a uniquely causal queue from chronology alone.
5. Original files and new raw outputs with SHA-256 ledger and permanent data release; one consolidated GitHub scientific report and a reader-friendly README update. Explicitly preserve the historical failed E1-v2 verdict and unexecuted Test B.
6. End with **one recommendation**: whether a local junction effect-modification mechanism is materially supported in this exploratory case, disfavored, or unidentifiable. Decide later whether to preregister fresh independent physical evidence, explore receiving-capacity mechanisms or reconsider a different coordination mechanism before any estimator design.

**Possible exit findings:**
- **E3 CASE-LEVEL EFFECT MODIFIER SUPPORTED:** E3 service rule changes locally, and the original route swap's network externality changes materially; this supports a physically grounded *candidate modeling feature*, not a validated estimator.
- **E3 CASE-LEVEL EFFECT WEAK/CONTRADICTED:** A valid priority intervention changes service but leaves route effects small, unchanged or inconsistent; de-prioritize this particular E3 mechanism in these cases, not all bottlenecks.
- **MANIPULATION INACTIVE / RECONSTRUCTION INTEGRITY FAILURE:** No interpretable first-stage contrast; publish the blocker rather than inventing a conclusion.
- **NONLINEAR RESPONSE/CAUSAL ROUTE-ASSIGNMENT EFFECT OBSERVED, PHYSICAL MEDIATOR UNRESOLVED:** The intervention changes traffic but attribution to a single queue or turn is not established; preserve the limits.

**What success means for the larger research:** We will have tested *whether a specific physical constraint can alter route-change externalities under controlled conditions*. Whether that knowledge can improve prospective prediction **still requires newly specified development plus disjoint independent validation**. Whether acting on such a predictor produces a collective benefit **still requires separately approved, matched independent-versus-cooperative Test B with active participant and nonparticipant fairness safeguards**. This plan does not claim either milestone is complete.

**Current status: PLAN WRITTEN; C0–C4 NOT EXECUTED; E1-v2 D1 DEVELOPMENT_NOT_QUALIFIED; independent validation NOT_STARTED; Test B NOT_RUN.**