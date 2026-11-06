# Cooperative Traffic Research — Post-T1 Prediction-versus-Realization Investigation Plan
## Why 12 coordinated departure shifts failed to produce the predicted network benefit

**Date:** November 6, 2026  
**Status:** PROPOSED SCIENTIFIC INVESTIGATION PLAN — DOCUMENTATION ONLY; NO ANALYSIS EXECUTION OR NEW SIMULATIONS AUTHORIZED BY THIS DOCUMENT  
**Starting evidence:** The completed T1 development-only feasibility study on previously inspected seed 2101.  
**Research boundaries:** Preserve all Experiment 007 Test A and E1-v2 NO-GO decisions; do not open reserved 6201–6212, 6301–6312, or new T1 confirmatory cohorts. Do not change the current 10-second predictor, optimizer, or scientific gates in this investigation.

## 1. WHY we are doing this — direct connection to the larger objective

Our original scientific question is: **Can voluntary collective decisions among human drivers produce better traffic outcomes than equally informed independent decisions, while limiting harm to participants and nonparticipants?** We are investigating this because some future autonomous traffic systems might share intentions and coordinate actions; the practical research opportunity is to ask what forms of that coordination are possible with human-driven vehicles today. Neither an autonomous-vehicle advantage nor real-world willingness to accept delays has yet been established.

The first routing studies failed to show an acceptable cooperative advantage. Experiment 007 and E1-v2 failed to forecast route-change externalities reliably. C1 showed that local junction priority can greatly modify route-choice consequences, but did not show a beneficial intervention. T1 then shifted our attention from *where* to drive toward *when* to depart.

In the completed T1 development trial, the same shared forecast told the coordinated policy C that a small collection of optional timing adjustments would reduce whole-network cost. The simulator showed the opposite. **That gap is the central scientific obstacle now.** Continuing immediately to another model or a larger study would repeat the earlier mistake of equating a numerically responsive predictor with a physically useful decision signal.

**Purpose of this investigation:** Determine, using existing evidence first, whether the forecast failure is primarily an accounting/implementation problem, a misleading 10-second time-bin timing representation, a failure to represent physical travel and junction queues, or an interaction in the coordinated decision set that the policy cannot predict. We do **not** need to prove that timing coordination works. We need to learn which assumption failed and whether the evidence justifies *any* next intervention.

**Bridge to the original vision:** Reliable or at least adequately bounded predictions of the consequences of voluntary actions are necessary to make cooperation credible and fair. Identifying *why* the T1 timing signal failed helps decide whether to improve forecasting, test a different mechanism such as bottleneck-entry reservation, or suspend the present direction. Distinguish understanding the failure from validating a new predictor, and distinguish both from demonstrating a collective efficiency/fairness advantage.

## 2. WHAT is established — fixed evidence checkpoint, not a new experiment

The development-only T1 run used the existing synthetic 10×10 SUMO network, 1,000 original vehicle identities and preferred departures over 200 seconds, a single shared traffic-aware independent route assignment held fixed across policies, and **500 eligible** drivers with optional 0/10/20/30-second delays.

- A: everyone keeps preferred departure. B: independent timing best responses using shared forecasts. C: joint timing changes under the same forecast and modeled acceptance assumptions.
- **B reached a no-shift equilibrium**, 0 maximum remaining modeled unilateral improvement, in one pass in each of four *forecast-only* bin phases. This establishes convergence in this finite game, **not** a realistic timing-aware equilibrium.
- The 10-second forecast showed nonzero *in-network* cost sensitivity to timing options for 498–500 of 500 eligible identities across phases, but zero drivers showed a modeled *total personal* benefit from shifting after the voluntary departure penalty. Thus numeric sensitivity is not physical predictive validity.
- Under phase-zero C, **12 vehicles shifted departure by +10 seconds each**. Across all drivers the model predicted **C−B = −50.626 network-seconds** (benefit to C), but actual SUMO observations gave **C−B = +618 network-seconds** (harm). The signed discrepancy between predicted and observed policy contrasts is **+668.626 network-seconds**. This is a *single development case*, not an independent error estimate.
- Observed +618 network-seconds decomposed exactly into **+120** intentional predeparture waiting, **+9** additional SUMO insertion delay and **+489** additional actual in-network trip duration. Waiting time already inside trip duration must not be added again.
- Drivers with **unchanged requested departures** accounted for **+614** network-seconds of the C−B difference; the 12 shifted drivers accounted for **+4**. Among nonparticipants (500 fixed eligible-state opt-outs), aggregate difference was **+543** network-seconds; **102/500** had >30 seconds additional realized cost. Across all 1,000 drivers, 477 benefited, 481 were harmed, 42 unchanged, and 205 had >30 seconds additional realized cost.
- The four tested 10-second bin phases (0, 2.5, 5 and 7.5 s) produced 8–12 proposed shifts and differing forecasts, but **only phase zero was run in SUMO**. Do not infer phase-level physical robustness or statistical uncertainty from four modeled phases.

**Verdict carried forward unchanged:** Current T1 10-second model/policy DEVELOPMENT NO-GO for confirmatory execution. The general hypothesis that voluntary timing coordination might be beneficial remains untested.

**Authoritative evidence:** [T1 final development report](POST_C1_T1_TIMING_FEASIBILITY_FINAL_DEVELOPMENT_REPORT_2026-11-06.md), [compact derived evidence JSON](results/t1_dev2101_feasibility_compact_2026-11-06.json), [successful development run 42183640504](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504), [original development archive artifact 13486493479](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504/artifacts/13486493479), [source implementation](../research/t1_timing/feasibility.py), and [original T1 protocol candidate](POST_C1_T1_PROSPECTIVE_TIMING_PROTOCOL_CANDIDATE_2026-11-05.md).

## 3. The bounded scientific question

**Why did policy C select a schedule predicted to save 50.626 network-seconds, whereas the realized schedule increased total cost by 618 network-seconds versus equally informed independent timing B?**

Subquestions:

1. Can the predicted and realized B/C contrasts be independently reconstructed from original immutable records, with correct preferred/requested/actual departure definitions?
2. What portion of predicted C benefit comes from direct costs to the 12 shifted drivers versus forecast externalities to the 988 unshifted drivers? Is that decomposition internally consistent?
3. Do 10-second edge-entry bin boundaries, fixed nominal edge-arrival clocks, or coarse assigned-demand counts create misleading predicted savings?
4. Which observed trip-level delays dominate the realized +489 in-network seconds, and how are these distributed by route, OD, participants and nonparticipants?
5. What remains **unobservable from archived tripinfo and route assignments** (for example exact actual edge-entry times, queue fronts, turn discharge, and causal junction mediation)?
6. Does existing evidence discriminate among the explanations sufficiently to justify a minimal follow-on physical observation, or should the current timing predictor be set aside?

## 4. Competing explanations — hypotheses, not findings

| Hypothesis | Why plausible | What could distinguish it | Evidence that would weaken it |
|---|---|---|---|
| **H_A — Accounting/implementation mismatch** | Preferred departures, requested shifts, insertion delay and in-network duration use different clocks; earlier T1 attempts exposed SUMO input ordering sensitivity | Independently reconstruct the original 1,000 matched vehicle records and predicted before/after arithmetic | Exact all-driver, route, shift and cost parity, with no missing/censored trips |
| **H_BIN — Time-bin aliasing** | A 10-second shift can move estimated visits between sharp 10-second bins without changing plausible queue exposure proportionally | Rebuild the original predicted edge/bin occupancies, changes and per-resource cost contributions; inspect boundary proximity, four phase-only forecasts, and concentration of apparent benefit | Large modeled gains distributed across bins and relatively stable under the predeclared phases |
| **H_CLOCK — Wrong physical arrival order/time** | Predicted edge visits use requested departure plus cumulative **nominal free-flow**, omitting time-dependent queue propagation and vehicle insertion effects | Compare nominal route clock profiles to any actual edge-event evidence **only if present**; archived tripinfo alone does not yield actual edge-entry times | Direct recorded edge timing closely tracks the predicted profiles on the affected movements |
| **H_QUEUE — Unmodeled junction/receiving constraints** | An edge-count proxy does not represent priority, storage, downstream receiving capacity or blocked turns; C1 showed rule-dependent route effects | If a later specifically authorized passive replay is necessary, measure vehicle-level arrivals, queues, discharge and waiting at predeclared candidate intersections | No corresponding observed service/queue changes and alternate mechanisms better explain the contrast |
| **H_INTERACTION — Nonadditive joint timing effects** | Twelve small timing changes could alter many otherwise unchanged journeys; prior route-swap studies observed nonadditivity | Examine total policy-level predicted change, incremental selected-move forecasts, and observed subgroup/time/OD response; do not attribute causal share to a particular move without separately controlled evidence | Observed impact tightly localized to shifted drivers with little change to unchanged-route/departure drivers |
| **H_SENS — Simulator scheduling/perturbation sensitivity** | Same SUMO random seed does not automatically guarantee every internal vehicle event sequence stays paired under changed requested timing | Audit actual requested departure order, insertion, completions, collisions/teleports, seed and source identity; trace the earliest observed divergence if later instrumented | Invalid or nonidentical inputs found, in which case the causal interpretation stops; or controlled replay reproduces outcomes exactly |

These hypotheses can coexist. In particular, an exact accounting audit **does not** prove any unique traffic mediator; and 614 network-seconds experienced by unshifted drivers **does not** mean those 988 drivers were randomly assigned a network-externality treatment.

## 5. HOW we investigate — archive-first evidence sequence

### Phase R0 — Recover and protect source evidence

**No new SUMO.** Retrieve existing run 42183640504 and its original artifact. Verify archive SHA256 and source revision, vehicle count/IDs and fixed route sequences, all A/B/C original preferred dates and requested departure schedules, simulator seed/settings, completed tripinfo identity coverage, and the old failed-attempt distinction. Preserve the initial negative result rather than modifying its artifact.

**Output:** Small inventory and integrity ledger: original files available, file hashes, actual fields captured, missing data, any irreconcilable discrepancies. Distinguish saved forecast outputs from values reconstructed under the same frozen algorithm.

**Stop:** Missing, unverified or incompatible essential files => report EVIDENCE_INCOMPLETE; do not fabricate vehicle/edge traces or proceed to physical explanations.

### Phase R1 — Reconcile primary cost and model prediction algebra

**No new SUMO; no predictor retuning.** Independently recompute for each matched driver:

- Actual preferred-to-arrival = requested_shift + actual_insertion_delay + actual_in-network_duration.
- Total C−B = sum of individual contrasts. Separately reconcile +120, +9, +489 = +618 network-seconds.
- Predicted C−B using identical archived B/C schedules and the original 10-second proxy: predicted direct schedule cost, predicted own in-network effect and predicted effect on every other vehicle. Preserve sign conventions. This is model decomposition, not validation.
- Reconcile changed-departure (12) and unchanged-departure (988) subgroup contributions (+4 and +614); opt-in/nonparticipant counts and +543 nonparticipant network-seconds. Compare predicted vs realized individual/aggregate signs and ranking for **the actually selected C schedule**, not invented single-driver SUMO counterfactuals.
- Inspect any mismatch between forecast **absolute cost level** and actual SUMO baseline separately; large absolute level error is not by itself an explanation of **contrast sign reversal**.

**Output:** One full-network predicted-versus-realized bridge table with explicit clock decomposition, group totals, and numerical identity checks. Define tolerances before computing; archive discrepant rows rather than fixing them opportunistically.

### Phase R2 — Locate where the prediction claimed the benefit

**No new SUMO; reuse frozen forecast.** For the 12 selected shifts and all 1,000 fixed routes:

- Reconstruct predicted original B and chosen C edge/bin resource counts and the signed contribution of each changed edge/time bin to modeled total cost.
- Quantify predicted savings from changes to other vehicles versus direct costs to 12 shifters, and identify concentration in particular resources, time windows, and intersections **as modeled features only**.
- Inspect how many predicted cost changes involve sharp crossings of 10-second boundaries; compare the **already specified** four phase offsets as numerical sensitivity checks. **Do not run those other three phase schedules in SUMO or choose the most favorable phase.**
- Identify whether the model's timing and binning could manufacture exaggerated synchrony, especially since it uses nominal free-flow edge times and the same count-based delay surcharge for all assigned uses of an edge-bin.
- Run unit-level arithmetic consistency checks (for example sum of per-bin predicted changes equals global predicted contrast; moving a vehicle updates edge-bin counts exactly; both arms have the same forecast parameters).
- Keep this as explanatory reverse engineering; do **not** fit pressure coefficients, change bin size, edit optimizer objectives or select a new forecasting model.

**Output:** Top contributing modeled edge-bin/time regions, percentage of nominal forecast gain concentrated in the leading resources, four-phase numerical instability summary, and a concise assessment of H_BIN/H_CLOCK.

### Phase R3 — Characterize the observed harm without inventing traffic traces

**No new SUMO.** With archived tripinfo/route manifests, characterize matched realized timing changes:

- The 12 requested-shift drivers versus 988 unshifted; 500 eligible versus 500 nonparticipants; aggregate, median, p90/p95, >30-s harms; beneficial and harmful cohorts both included.
- Separate insertion delay versus actual in-network duration by matched driver, route/OD corridor and original preferred departure interval, subject to adequate cohort sizes.
- Identify concentrated harm on route-overlapping or nearby-demand cohorts, but treat these associations as **descriptive**. Stratification by route/OD chosen after seeing outcomes is exploratory and not inferential.
- The original T1 archive is reported to contain tripinfo, route XML, statistics, collisions and a feasibility JSON. **Do not assume it contains one-second FCD, exact per-edge entry times, junction service trajectories or five-second edge detectors** without verifying the archive inventory.
- Attribute observed changes to *the full C schedule versus B*. Do not attribute a particular driver's harm to one of the 12 moves without additional controlled counterfactual evidence.

**Output:** Complete observed harm accounting, mapped hypotheses that archival data can support or refute, and an explicit unobservable/mechanism-unknown list.

### Phase R4 — Decision: is an additional physical observation justified?

First determine whether R0–R3 explain the discrepancy adequately.

- If a numerical/accounting integrity defect is identified, report the failure; do not silently repair the original scientific results. Any correction is a new version with a traceable audit and distinct prospective approval.
- If bin aliasing or proxy assumptions dominate the **predicted** improvement, the appropriate conclusion may be simply that the present signal is not trustworthy; **do not automatically create a better predictor**.
- If R0–R3 confirm correct accounting and a large, physically unexplained realized response, consider one **conditional, separately authorized passive replay** of *the same previously inspected seed-2101 B and C scheduled inputs* with FCD/edge-level diagnostics. Instrumentation must be strictly passive, preserve the same routes, requested times, SUMO parameters and output identity, and reproduce the old matched tripinfo at a preregistered tolerance **before** physical interpretation. The minimal maximum would be **two** additional SUMO arms (B and C); A is identical to B in the archived T1 seed and need not be rerun absent an integrity reason.
- Predeclare first-divergence chronology, relevant edge/turn measurements, queue proxies, source insertion and spillover analyses *before* the replay. If passive instrumentation changes outcomes or cannot be verified, classify INVALID_REPLAY and stop.
- Such a replay could reveal **where and when** traffic differed, not uniquely establish a causal traffic mediator. Isolating one movement's contribution would require its own new controlled intervention protocol, not a post-hoc interpretation of FCD.
- If the available information does not support a discriminating replay, explicitly recommend **no additional simulation** and reconsider an alternative coordination mechanism rather than manufacturing model progress.

**Critical authorization boundary:** The user has requested publication of this **plan**, not execution of R0–R4, code changes or new simulations. Archive-only analysis or a later replay must not be initiated from this document; obtain appropriate execution authorization separately. No GitHub Actions workflow in this documentation PR may auto-run SUMO.

## 6. Scientific standards and exit criteria

The investigation succeeds when it produces an honest causal-evidence boundary, **not** when C becomes faster.

Deliver one consolidated retrospective report (not a long chain of intermediate PRs) containing:

1. Verified archival/source manifest and strict parity/exception records.
2. Independently audited model contrast and realized cost bridge; account separately for intentional predeparture, insertion and in-network duration.
3. Model-bin, nominal entry timing and forecast phase diagnostics with **no coefficient fitting**.
4. Matched-driver and nonparticipant harm distribution, with both favorable and unfavorable effects.
5. An explicit evidence matrix for H_A, H_BIN, H_CLOCK, H_QUEUE, H_INTERACTION and H_SENS labeled **supported, weakened, unresolved or not observable**, rather than pretending a unique explanation has been proven.
6. A single prospective decision: **STOP CURRENT T1 PROXY**, **AUTHORIZE ONE MINIMAL PASSIVE DEVELOPMENT REPLAY FOR A DISTINCT UNRESOLVED QUESTION**, or **PROPOSE A DIFFERENT, FUTURE SCIENTIFIC DIRECTION**. Do not call a revised model qualified without fresh development and disjoint independent validation.

**Hard stops:** source/archive integrity failure, missing fields essential to a claimed conclusion, any attempt to access reserved 6201–6212/6301–6312 or genuinely unseen cohorts, a change to the existing failed predictor/optimizer, outcome-led gate changes, or scientifically non-discriminating extra simulations.

## 7. What different answers would mean for the larger question

- **Arithmetic/accounting problem:** we learn the prior effect estimate was invalid or misinterpreted; do not infer a coordination mechanism.
- **Bin/nominal-clock failure:** the numerical forecast was sensitive but disconnected from physical queue timing; a new mechanism or carefully specified prediction hypothesis would need *new* independent qualification.
- **Genuine queue/junction-mediated externalities:** this strengthens the case that coordinated timing can affect many drivers, **not** that it improves their collective welfare; future work must explicitly confront queue physics and fairness.
- **Ambiguous physically coupled network response:** the honest result is that the cause is unresolved on the available evidence; either authorize narrowly targeted observation or stop.
- **No plausible path from refined timing forecast to a credible voluntary mechanism:** preserve the failed T1 policy and compare alternatives, including bottleneck-entry reservation, before spending more computation.

**Final question to carry to the next milestone:** *What physical or forecasting assumption caused a small voluntary-style timing intervention to be predicted as collectively beneficial yet realized as collectively harmful, and is that assumption sufficiently identifiable to justify another scientific test?*

The broader cooperative-traffic hypothesis remains open; no real-road safety, human willingness, or cooperative advantage has been established. Public LinkedIn/X updates require separate review and explicit approval.
