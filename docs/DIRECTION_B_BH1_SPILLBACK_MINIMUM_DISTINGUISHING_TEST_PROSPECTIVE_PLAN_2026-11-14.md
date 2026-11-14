# Direction B — B-H1 minimum distinguishing test: prospective scientific plan

**Date:** November 14, 2026  
**Status:** APPROVED DIRECTION FOR DOCUMENTATION; PROSPECTIVE DESIGN PLAN — **NOT FROZEN, NOT EXECUTABLE**.  
**Authorization:** Documentation and scientific protocol framing only. **No traffic simulation, new framework evaluation, code/adapter implementation, policy optimization, fresh or reserved cohort, calibration, human recruitment, or external social publication.** No choice of simulator, experimental seeds, effect-size gate, or fairness threshold is authorized by this plan.

## 1. Scientific decision and boundaries

**North Star:** Can voluntary coordination among drivers reduce *all-driver* traffic costs beyond equally informed independent decisions, without unacceptable burdens on participants and nonparticipants?

**B-H1 (candidate):** In a road network with a finite-storage approach to a downstream bottleneck, voluntary timing adjustments by a limited number of drivers *may* prevent queue spillback from obstructing unrelated crossing movements. Any avoided interference could reduce total original-preferred-departure-to-arrival cost more than the cost of the accepted timing adjustments, **even when independent drivers have the same available information**.

This is a **conditional, falsifiable hypothesis**, not a positive project result. The proposed causal mechanism is avoided physical spillback interference, **not** a transfer of waiting time from inside the network to outside it. An existing capable independent timing policy might eliminate the same interference; if so, no incremental coordination benefit is established.

**Disposition of the preceding design checkpoint:** Physical plausibility and a meaningful candidate *difference in objectives* have been identified. The proposition that voluntarily accepted adjustments create a net benefit **beyond a strong independently informed comparator is NOT YET QUALIFIED**. The goal of this document is to define the *minimum distinguishing scientific protocol* and its remaining design gates, without expanding simulator or incentive-model investigations.

Earlier project decisions remain unchanged: [Experiment 006](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md) primary efficiency INCONCLUSIVE and severe-harm criterion not met; [Experiment 007 Test A](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md) predictor NO-GO; [T1 B*/C*](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md) ten-second proxy/policy development NO-GO; [PR #115](POST_T1_DUAL_FRAMEWORK_SOURCE_REVIEW_AND_DECISION_DRAFT_2026-11-09.md) independent simulator fidelity EVIDENCE INSUFFICIENT. No original result, seed status, or source limitations are reversed.

## 2. Minimum physical interaction that would make B-H1 relevant

A *prospective* minimal setting should contain only the necessary ingredients:

1. **Constrained downstream discharge** on a movement served by a finite-storage road link.
2. **A nearby upstream intersection** at which a queue extending backward from that link can obstruct another, otherwise independently usable movement.
3. **Cross-traffic demand** for which that obstruction changes the timing of actual physical passage, not merely a route label.
4. **A bounded, independently accessible waiting/holding opportunity** for a small set of approaching volunteers. It must not itself obstruct other movements or hide costs from the objective.
5. **Physical conservation and accounting:** the same original travelers, demand, destinations, capacities, permitted movements, and any unchanged route constraints under all primary arms.

**Essential distinction:** If a bottleneck has fixed service capacity, the same completion order, and no interfering movement, holding someone before arrival can merely replace in-network queue time with predeparture waiting. Such displacement does **not** automatically reduce preferred-departure-to-arrival time. Therefore, measuring queue reduction alone is insufficient.

The illustration that a driver could accept five seconds of additional cost while three others avoid ten seconds apiece is **hypothetical arithmetic only**, not an observed network result or a fixed intervention specification. Neither the concession menu nor the magnitude of possible physical savings has been established.

## 3. Three policies / controls: isolate cooperation, not a better forecast

### I — Equally informed independent policy (**primary comparator**)

Each driver is allowed the **same timing choices and information** available in the cooperative arm, including the same forecast quality, previously announced intentions if supplied, and any relevant capacity, queue and junction state observable at decision time. Drivers choose to minimize **their own** prospective preferred-departure-to-arrival cost, subject to their own allowable constraints.

A credible I arm must specify a stable individual-response or defensible choice procedure, with tie-breaking, stopping rules, and the treatment of mutually interacting schedules **frozen in advance**. Do not assume I means "nobody moves." Do not weaken I by denying it useful information, a timing option, a comparable decision budget, or a valid improvement path.

**A consequential unresolved gate:** If a credible independent equilibrium or equivalent individually rational comparator cannot be defined without an unrealistic oracle, stop and return to the design decision; do not substitute the original Experiment 006 nominal free-flow A or the historical T1 B merely because they already exist.

### V — Voluntary coordinated timing (**treatment**)

The same eligible drivers are offered **the identical menu of bounded timing alternatives** based on the same predictive information. Unlike I, the proposal accounts for predicted costs imposed on **all drivers**, including cross traffic and drivers who never enroll.

- The right to **decline** is real within the modeled intervention. A declined offer produces the same independently chosen behavior as permitted in I, unless a prospectively stated common response rule changes it.
- Accepted shifts may entail a **limited personal concession**, assessed using the same disclosed forecast. A study-specific allowable concession cannot be inferred from prior T1 thresholds or from a claim about actual willingness.
- Hold participation eligibility, opt-out behavior assumptions, route options, network mechanics, population and stochastic exogenous inputs matched as closely as the experiment permits. Do not assume actual human compliance from simulated acceptance.
- Report **offers, acceptances, refusals, realized changes, costs to volunteers, and costs to those never participating** separately.
- The treatment may not use privileged realized future queue/arrival data, lookahead unavailable to I, or a post-hoc advantageous coordination schedule. A theoretical best allocation may be displayed as an **oracle upper-bound reference only**, never called the practical treatment.

### N — No-spillback **mechanism-negative control**

In a *paired* physical configuration, remove the **specific blockage of unrelated crossing traffic** while preserving the underlying congested movement, its demand and discharge as closely as representationally possible. Both I and V must be evaluated under that configuration: the target is the **difference in V–I effects with versus without spillback**, not merely a drop in absolute travel time after changing topology.

The no-spillback setting need not have identical total capacity or all paths if the removal intrinsically changes them, but **every unavoidable change and its direction must be documented prospectively**. A bypass or isolated crossing could alter other delays; such differences can prevent a unique causal attribution. If no comparable negative-control representation can be specified, classify the mediator conclusion **UNRESOLVED** rather than claiming the intervention uniquely prevented spillback.

Optional, descriptive reference **U** (unchanged original requested departures) may help identify gains from flexibility generally, but **U vs V is not the scientific test of incremental cooperation**. I vs V remains primary.

## 4. Frozen scientific invariants for any *later* authorization

The following must be fully specified **before** any future empirical execution; this plan does not select the values:

| Requirement | Nonnegotiable scientific control |
|---|---|
| Individual IDs / population | Exactly matched original identifiers, origin–destination pairs, preferred times, participation eligibility, and initial exogenous behavior **within the prospective study**; no requirement to reproduce historical T1's precise 1,000 IDs or seed 2101. |
| Information parity | The same available forecasts, announced plans, map, observation and lead time for I and V; no future realized outcomes or asymmetric computation resources. |
| Choice parity | Same routes, departures/entry-time options, allowable deviation windows, and objective timing origin. Only the private vs system-cost decision criterion differs. |
| Voluntary choice | Offers can be declined, and the assumption governing acceptance is documented and varied in a **predeclared** robustness check. No coerced compliance is rebranded as "voluntary." |
| Physical dynamics | Meaningful downstream capacity, finite storage, upstream blocking interactions, cross-traffic service, conservation and queue spillback. |
| Cost integrity | Preserve original preferred departure p_i, requested release s_i, actual admission d_i and arrival a_i for every driver; predeparture wait, insertion wait, in-network delay and downstream impacts all count once. |
| Complete outcomes | All original drivers accounted for; incomplete or unarrived cases handled under a prespecified censoring/exception rule, not dropped to improve the mean. |
| Statistical independence | Prespecify unit of replication as independent demand/physical-scenario seeds or independently generated scenarios (not individual drivers within the same congested run); matched arms and a stochastic-control strategy. |
| Fairness | Prespecify per-driver, participant and nonparticipant harm distribution, upper tail, severe-harm threshold(s), and any disqualifying harms **before looking at outcomes**. |
| Manipulation check | Demonstrate that V actually changes the spillback exposure or crossing-blockage duration predicted by B-H1; avoid claiming a physical mediator from correlation alone. |

**Historical T1 protocol is not inherited:** its exact 1,000 identities, 12 +10-second changes, 200-second departures, archived fixed edge sequences, SUMO speedFactor model and source-specific timing representation are not mandatory for a new prospective Direction B test. A prospective experiment would still require internally matched IDs, clocks, and complete route/timing control within *its own* study.

## 5. Primary endpoint and causal contrasts

For arm P in {I,V} and physical setting M in {S = spillback-capable, N = no-spillback control}, define

\[
C_{P,M} = \sum_{i\in \mathcal{D}}\left(a_{i,P,M}-p_i\right)
\]

where \(\mathcal{D}\) contains **every** originally intended driver, including ineligible drivers, declined volunteers, and cross traffic. The original preferred-departure time p_i is fixed across matched arms. This counts predeparture waiting, road admission delay and actual travel in one common elapsed-time metric.

**Primary incremental-cooperation contrast in the spillback setting:**

\[
\Delta_S = C_{V,S} - C_{I,S}
\]

A negative value favors voluntary coordination. A useful scientific outcome must also meet completion, practical materiality, statistical reliability and fairness gates, not merely have the favored sign.

**Mechanism sensitivity / negative-control contrast:**

\[
\Psi = (C_{V,S}-C_{I,S}) - (C_{V,N}-C_{I,N})
\]

A negative \(\Psi\) would be consistent with a *larger* incremental benefit when the cross-traffic spillback channel is available. **It is not, alone, proof that spillback caused the result**, because modifying the interaction can change other traffic dynamics. The corresponding cross-traffic blocked-time, spillback exposure, queue storage and discharge observations should agree with the proposed mechanism.

**Fairness:** For each matched identity, report \(\delta_i=(a_{i,V,S}-p_i)-(a_{i,I,S}-p_i)=a_{i,V,S}-a_{i,I,S}\); count who gains or loses, how much, and particularly the worst harms among ineligible/nonparticipating drivers. System mean and cross-traffic subgroup gains must not conceal an unacceptable distributional outcome.

**Pre-registration obligations (NOT YET FROZEN):** decide the primary time/horizon and effect-size margin, independent-scenario replication count/statistical uncertainty method, acceptance/opt-out cases, allowable timing shift, exogenous stochastic controls, fairness thresholds, incomplete-trip handling and how to interpret spillback blockage. Do not import study-specific thresholds from Experiment 006 or T1 without justification.

## 6. Necessary falsifying and stop outcomes

This is a test of **incremental cooperation**, not an exercise in finding a favorable scenario.

- **No incremental value:** I already avoids the relevant queue spillback and V offers no meaningful additional system benefit.
- **Queue relocation masquerading as benefit:** decreased in-network stopped time is offset by increased predeparture waiting; full C does not improve.
- **No physical mechanism:** modeled crossing blockage does not occur, does not change, or cannot be uniquely identified under the proposed control.
- **Voluntariness failure:** a claimed benefit requires forced acceptance, an effectively unavailable opt-out, or undisclosed external subsidy.
- **Fairness failure:** reduced average cost is purchased with prospectively unacceptable severe harms, especially to nonparticipants.
- **Weak or unequal baseline:** I fails credible individual optimization, is denied information/options given to V, or an oracle enters V.
- **Attribution failure:** uncontrolled exogenous or stochastic differences and changed network physics dominate observed I–V differences.

**Decision meanings for a later authorized test:** Only a prospective, statistically qualified positive primary result *with* physical-mechanism credibility, voluntary-response fidelity and predeclared fairness gates would support B-H1 in the specified setting. A credible negative or null would weaken **this particular mechanism under those assumptions**, not all possible traffic cooperation. A test with invalid controls is **INCONCLUSIVE / NOT QUALIFIED**, regardless of its numerical sign.

## 7. Bounded next research activity: design qualification only

Before requesting any E3 execution approval, produce a short **design-readiness verdict** on four yes/no questions:

1. Can a physically coherent, bounded spillback-plus-cross-traffic setting be specified without adding untestable complexity?
2. Can an **equally informed, individually rational, credible** I comparator be defined and assessed prospectively?
3. Can V use identical options and information with genuine opt-out while preserving measurable benefits and harms to **every** driver?
4. Can the no-spillback control and complete original-preference-to-arrival metric distinguish **avoided physical interference** from relocated waiting or unrelated network changes?

If any critical gate is unsatisfied, record **NOT READY** and stop or reconsider the physical mechanism. Do not fill the gap by choosing another simulator, tuning an externality predictor or relaxing fairness after seeing results.

**After a qualified design-readiness decision only**, a separate, explicitly authorized milestone might freeze an executable prospective protocol and select a physical simulator or test environment. Neither a platform choice nor any implementation is approved here. Reserved and confirmatory seeds remain unopened.

## 8. Provenance and scientific governance

- [Direction B foundational checkpoint and alternative milestones](DIRECTION_B_FOUNDATIONAL_COOPERATION_SCIENTIFIC_CHECKPOINT_2026-11-12.md).
- [Prior departure-timing candidate — T1-specific, not the B-H1 protocol](POST_C1_T1_PROSPECTIVE_TIMING_PROTOCOL_CANDIDATE_2026-11-05.md).
- [Experiment 006 complete results and fairness failure](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md).
- [Experiment 007 Test A negative estimator finding](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md).
- [T1 identity-locked scientific report](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md).
- [Merged PR #115 dual-framework source assessment](POST_T1_DUAL_FRAMEWORK_SOURCE_REVIEW_AND_DECISION_DRAFT_2026-11-09.md).

**Scientific claim allowed at this checkpoint:** B-H1 identifies an intelligible, physically plausible, falsifiable *candidate* channel for incremental voluntary coordination. **Neither the magnitude, existence in a specific modeled network, voluntary take-up, causal mediator, nor efficacy relative to a strong independent policy has been experimentally shown.**

**Stop here on theory/engineering expansion.** This plan is the record of the conceptual milestone and the gate for a later, separately authorized study—not an authorization to run it.
