# Cooperative Traffic Research — T1 controlled physical-interaction observation plan

**Date:** November 6, 2026  
**Status:** **APPROVED FOR PLAN PUBLICATION ONLY — NOT AUTHORIZED TO EXECUTE**  
**Scientific type:** Prospective, descriptive physical-observation investigation on previously inspected T1 development seed 2101; **not** a new cooperative-policy evaluation, predictor calibration, or causal isolation experiment.  
**Maximum future execution (separate approval required):** Exactly two passively instrumented SUMO arms, original independent timing **B** and original cooperative timing **C**.  
**Original verdict:** **T1 current 10-second forecast/policy DEVELOPMENT NO-GO**, unchanged.

## 1. WHY — relevance to voluntary collective decision-making

Our foundational question is whether voluntary collective decisions can improve network-wide traffic outcomes relative to equally informed independent decisions without unacceptable participant or nonparticipant harm. The phase-zero T1 forecast predicted **C−B = −50.6263499 network-seconds** for twelve +10-second voluntary-style departure shifts. In one previously inspected SUMO development case, the same complete schedule produced **C−B = +618 network-seconds**: +120 intentional predeparture seconds, +9 insertion seconds, and +489 additional in-network seconds.

The crucial externality reversal was among the **988 drivers whose requested departures did not change**: **−85.313 model-predicted seconds versus +614 realized seconds**. The twelve shifted drivers were predicted to incur +34.687 seconds collectively and actually incurred +4. Across 500 nonparticipants the realized increase was +543 seconds, and 102 had >30 seconds additional realized journey cost. We must not select a cooperative policy on apparent benefits for unshifted drivers until we understand whether those effects can be physically observed and eventually forecast.

The prior [SHA-verified archive-first findings](POST_T1_ARCHIVE_FIRST_PREDICTION_FAILURE_SCIENTIFIC_FINDINGS_2026-11-06.md) demonstrated that the model's nominal free-flow arrival clocks and 10-second edge-bin phase produce a fragile forecast: for the *same fixed C schedule*, moving the bin phase from 0 to +2.5 seconds changed the predicted sign from −50.626s to **+4.449s**. However, the original archive lacked vehicle-level edge-entry, junction-movement and queue traces; it cannot identify the physical mechanism that produced +618s. The present study addresses **observability and chronology**, not whether another model can be tuned to succeed.

### One question

> **Can we identify the earliest traffic interactions through which the twelve coordinated departure changes affected the other 988 vehicles, and are those interactions sufficiently observable to support a falsifiable future forecasting hypothesis?**

**Qualified meaning of “identify”:** establish an accurately measured chronology, locations and compatible interaction pathways. Temporal or spatial proximity alone is **not** proof that one shifted driver caused a particular unshifted driver's delay, and this study cannot uniquely attribute the +618s reversal to one bottleneck.

## 2. Fixed original evidence and boundaries

**Sources of truth**
- [Original T1 feasibility scientific report](POST_C1_T1_TIMING_FEASIBILITY_FINAL_DEVELOPMENT_REPORT_2026-11-06.md)
- [Archive-first numerical and fairness findings](POST_T1_ARCHIVE_FIRST_PREDICTION_FAILURE_SCIENTIFIC_FINDINGS_2026-11-06.md)
- [Archived result run 42183640504](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504) and [original 24-file ZIP artifact 13486493479](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504/artifacts/13486493479), original ZIP SHA256 `b524729226c44b722f2c8c157f017dee98181dcd8dfb97c2ec14401229184fae`
- **Original run code revision:** `bbc0fadefcaa11d499e394d648526358d97358ee`; original source and routes must be taken from the inspected archive and corresponding revision, **not a later generated variant**
- [Original T1 forecast implementation](../research/t1_timing/feasibility.py), [SUMO invocation and tripinfo parser](../experiments/experiment_007/run_v01.py), [compact machine-readable checkpoint](results/t1_dev2101_feasibility_compact_2026-11-06.json).

The archived ZIP actually includes the network, demand, T1 feasibility JSON, all A/B/C route XML, tripinfo, statistics, collision files and logs. **It does not contain FCD, timestamped lane/edge movements, junction discharge or vehicle-level queue evolution.** The original Actions artifact has a stated 30-day retention window ending approximately December 6, 2026 UTC; its original bytes/digest should be preserved in long-lived research evidence *before* expiry if execution/reporting proceeds.

**Unchanged experimental conditions:** original SUMO **1.28.0** environment and seed 2101; all 1,000 identities, 500 eligible participants, original preferred departures, original independent route sequences, B no-shift assignments, C's exact twelve +10s shifts, original network geometry and junction rules, simulation clock, vehicle dynamics, random settings, and chronological presentation of requested-departure XML. **Reuse archived B/C input route files and original network byte-for-byte**. No A replay: original A and B are equivalent in this development case.

**Absolute prohibition under this plan:** no SUMO execution now; no new seed/cohort, reserved 6201–6212 or 6301–6312, E1-v2 validation or Experiment 007 Test B; no shifts reoptimized, bins or penalties changed, T1 forecast repaired or fitted, new junction rules, alternative simulator, new policy arms, or external publication. The fact that this plan specifies a bounded replay is **not execution approval**.

## 3. Competing explanatory pathways and observations

| Candidate | Specific testable observation | What a passive trace cannot prove |
|---|---|---|
| **Source insertion / departure ordering** | Time and order of actual B/C first insertion for all IDs, especially unshifted vehicles queued near modified departures | A changed insertion sequence alone does not establish a particular downstream harm mediator |
| **Incorrect nominal downstream arrival clocks** | Actual per-driver edge-entry/exit times versus frozen nominal free-flow edge arrival profiles on the twelve shifted routes and interacting corridors | A signed timing error does not by itself predict the C−B policy effect |
| **Junction approach and receiving constraint** | First observed changed approach arrival, low-speed queue accumulation, turn passage/discharge timing, and downstream receiving occupancy | Co-observed queue/service changes are not a unique causal bottleneck |
| **Network-wide traffic interactions and stochastic event-order sensitivity** | Whether unchanged requested-departure drivers first diverge at a common lane/edge, adjacent approach, or source insertion time, versus broad distributed changes | Neither one seed nor two policies identifies the contribution of any individual shift |
| **10-second bin/assigned-count aliasing** | Compare physical edge-entry histories to the **already frozen** modeled edge-bin resources associated with the twelve shifts | Replaying trajectories does not retroactively validate the failed numerical proxy or identify a favorable bin phase |

Important competing clue: original aggregate **SUMO stopped `waitingTime` fell by 1,079s** in C despite +489s in-network duration. Do **not** presuppose that more network-wide stopping caused the harm. Separate stopped time, slow-moving time, insertion and in-network duration; retain opposing local changes as well as harms.

## 4. Minimal passive measurement protocol (conditional on later authorization)

1. **Input/provenance lock, offline:** Match saved network and route file SHA-256 values against the original archive. Preserve the original B/C vehicle records, departure ordering, vehicle/route identity, SUMO 1.28.0 environment/container image digest, options, and source revision. Verify all proposed instrumentation flags are supported by the pinned SUMO executable **without running a traffic simulation**; if they are not available, revise the prospective plan transparently before seeking execution authorization.
2. **One B and one C replay only:** Use original archived `network.net.xml`, B/C `routes.rou.xml`, and the original SUMO flags. Add **output-only** instrumentation, preferably: full-vehicle FCD at the original simulation step (nominally 1 s) with ID, lane, lane position, speed and (if available in 1.28.0) acceleration; plus `--vehroute-output` with `--vehroute-output.exit-times` for per-driver road exit timestamps. Both outputs must cover **all** relevant vehicles, not just the twelve shifters or vehicles selected after observing harm. Leave the original `--tripinfo-output`, statistics, collision and logging outputs unchanged. Do not add demand-sampling, detector-device probabilities, dynamic rerouting, junction interventions, TraCI controls, changed step length, or other behavior-affecting instrumentation.
3. **Check trace semantics:** FCD samples a vehicle's state per simulator step, including internal lanes when available; it does not automatically give exact substep junction crossing times. Vehroute exit times provide per-edge timing of completed trajectories but are not themselves direct measurements of queue front, right-of-way causes or gap acceptance. Use the actual simulator step as the resolution floor and distinguish “first *observed* divergence” from unknowable substep physical first cause. SUMO source documentation: [FCD](https://sumo.dlr.de/docs/Simulation/Output/FCDOutput.html), [per-edge route exit times](https://sumo.dlr.de/docs/Simulation/Output/VehRoutes.html), [tripinfo clock definitions](https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html).
4. **No instrumentation-triggered outcome change:** Pair every B/C vehicle with the original archived B/C tripinfo and original ID/routes/departure schedules. Validate original 1,000/1,000 completion, insertion delays, actual trips, exact +618s preferred-to-arrival contrast, +120/+9/+489 bridge, and the unchanged 12/988 and 500/500 fairness categories. New trace output is interpretable only after the strict replay integrity gate below.

### Hard replay integrity gate — before interpreting any movement

- Archived network and B/C route files must be byte-identical to inputs; route/ID membership, requested departure, and participant labels must be exact. Original seed, SUMO build/image and dynamics settings must be unchanged; the command-line diff must consist **only of output options/filenames**.
- Require precisely the same completed 1,000 vehicle IDs in each replay arm, and **matched per-driver** archived `depart`, `departDelay`, `arrival`, `duration`, `waitingTime`, `timeLoss` at recorded precision (allow at most **0.01s numeric serialization tolerance** for originally printed two-decimal quantities). Require `sum( arrival - preferred )` within **0.05 network-s per arm** of 211,051 (B) and 211,669 (C). If outputs have greater precision, prefer exact numeric equality.
- Exactly reproduce the baseline event/completion/exception counts (including no reported structured collisions, emergency braking or emergency stops), or report any divergence rather than calling it harmless. If any required comparison fails, label **INVALID_REPLAY**; stop without movement or mechanism claims. Do not silently retry with changed physics, altered instrumentation or alternative seeds.

## 5. Predeclared analyses — no post-hoc bottleneck storytelling

**Analysis unit:** matched vehicle ID and original fixed route; physical events are descriptive observations, not independent statistical replications. The policy contrast is one previously inspected development-seed pair. No confidence interval across FCD rows or individual drivers.

**Pass 1 — source clocks:** Confirm the first planned C shift and actual B/C source insertions; order the earliest B/C discrepancies in requested departure, true insertion time, inserted lane/position and source waiting, distinguishing expected intervention changes from effects on unshifted vehicles. Identify the first observed unshifted vehicle's **source insertion** divergence separately from its first in-network movement difference.

**Pass 2 — edge and junction chronology:** Construct each vehicle's ordered external and internal lane/edge transitions and exit times, preserving sample-time precision/uncertainty. For the original twelve shifted routes and their shared/adjacent movement corridors, find (a) the earliest changed arrival/occupancy/exit histories; (b) the earliest *unshifted* lane/edge/timing divergence; (c) the first observed changes in local queue proxies or junction passage order; (d) subsequent spatial-temporal propagation. State the earliest independently measured divergence and alternate prior events. Capture the whole network so effects without exact edge overlap are not automatically discarded.

**Pass 3 — distinguish types of delay:** Compare original and replayed trip-level insertion, in-network duration, stopped `waitingTime`, `timeLoss` and full preferred-to-arrival cost. For candidate corridors, use FCD to distinguish stationary queue proxies (defined in the report with an explicit speed threshold), lower-speed moving exposure and changed junction clearance; do not equate a stationary proxy with a measured right-of-way failure. Assess both increases and decreases, including the original net `waitingTime` decrease.

**Pass 4 — connect observed clocks to the frozen forecast:** Report nominal predicted arrival minus actual measured edge arrival for twelve shifted routes and predeclared shared/adjacent corridors, by time and network region. Contrast actual occupancy/arrival patterns with the original forecast's 10s edge-bin hypotheses; **do not refit, re-bin, reoptimize, or recompute a more favorable policy**. This comparison can identify forecast representational failures but is not independent prediction validation.

**Pass 5 — all-driver harms and negative controls:** Report 12 shifted/988 unshifted, 500 eligible/500 nonparticipant, source-insertion changed/unchanged, overlap/nearby/not-observed-near groups; all-driver total, severe >30s harms, tail and helped/harmed counts. Use all drivers, not only early interactions or high-harm corridors. Analyze route-overlap groupings only as exploratory associations, not causal attributions. Preserve the previously known 477 helped, 481 harmed, 42 unchanged and 205 severe-harm drivers as archival comparison anchors.

**Minimal mechanism candidate evidence** should include **a reproducible B/C first-divergence chronology**, at least one explicitly documented upstream/downstream sequence involving unshifted traffic (departure/insertion, shared movement or junction, altered queue/arrival/service, downstream change) at the stated observational resolution, and a clearly named measured feature that could prospectively predict a network consequence. A candidate cannot be declared “causal” on this basis and can still be unsupported if equally plausible earlier pathways remain.

## 6. Stopping/decision framework

| Result | Valid scientific decision |
|---|---|
| Input/outputs fail historical parity or mandated traces unavailable | **INVALID_REPLAY / EVIDENCE_INCOMPLETE.** Stop; no physical interpretation or new model. |
| Parity holds, but first effects cannot be localized or chains cannot be distinguished at achieved resolution | **OBSERVED EFFECT, MECHANISM UNRESOLVED.** Keep T1 NO-GO; do not automatically add instrumentation or simulations. Consider stopping this timing proxy or a different coordination mechanism. |
| Parity holds and a coherent measured interaction/queue-clock chronology is evident, with explicit remaining alternatives | **OBSERVABLE CANDIDATE MECHANISM ONLY.** Propose *one* separate, falsifiable forecast or physical-mediator hypothesis for prospective approval; no coefficient fitting or policy restart using this observation alone. |
| A plausible candidate is identified but harms to nonparticipants or uncertainty cannot be bounded for choices | **INSUFFICIENT FOR COOPERATIVE DEPLOYMENT.** Retain original policy NO-GO and fairness warnings; revisit whether timing coordination is an appropriate mechanism. |

### Exit criterion

The study should terminate after the planned **two** replay arms and one archive-plus-trace analysis. It has succeeded scientifically if it reports **what was physically observable, which earliest interaction candidates were supported or contradicted, what remained unidentifiable, and whether exactly one falsifiable subsequent hypothesis is justified**. Negative/inconclusive evidence is a valid completion. Any new physical intervention, alternative simulator, predictive model, unseen evaluation data or T1 policy execution requires a **new** prospective decision and explicit authorization.

## 7. Reporting and governance

Publish **one consolidated scientific findings report** to GitHub after authorized execution, together with raw measurement provenance and compact derived tables. The report should include input/output hashes, pinned SUMO version, exact command delta, replay-parity gate, earliest-event timelines with resolution bounds, full predicted-versus-observed cost bridge, participant/nonparticipant fairness, competing interpretations and a **STOP / CONDITIONAL NEXT HYPOTHESIS** decision.

Do not produce many interim reports/PRs. Never claim passive observations prove a unique causal junction, generality across traffic conditions, human willingness, real-road benefits, or cooperative superiority over equally informed independent behavior. Do not publish to LinkedIn or X without separate approval of an actual substantive milestone and its visual materials.

**Authorization checkpoint:** User approval on November 6, 2026 covers **writing and publishing this plan**. **No simulator run, pipeline change, new experimental cohort, or model implementation is authorized by it.**
