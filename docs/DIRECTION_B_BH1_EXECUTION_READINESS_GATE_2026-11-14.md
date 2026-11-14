# Direction B — B-H1 scientific execution-readiness gate

**Date:** November 14, 2026  
**Status:** **PRE-EXECUTION SCIENTIFIC GATE COMPLETE — NOT READY FOR TRAFFIC EXECUTION**  
**Authorization context:** The user approved advancing the [B-H1 minimum distinguishing spillback plan](DIRECTION_B_BH1_SPILLBACK_MINIMUM_DISTINGUISHING_TEST_PROSPECTIVE_PLAN_2026-11-14.md) toward execution. This record applies that plan's own four design-readiness gates **before** any physical traffic run, rather than treating broad authorization as evidence that the prospective protocol is already frozen.  
**Scope:** Read-only inspection of the existing plan and relevant existing project source; no new experiment, physical traffic simulation, new simulator choice, adapter, algorithm change, reserved cohort, code execution, calibration, human-subject activity or external publication. **No empirical outcome or efficacy claim is made.**

## 1. What was authorized and what was actually assessed

The approval permits forward progress toward a scientifically valid B-H1 experiment. It does not retroactively establish missing primary design specifications. The governing plan explicitly states **NOT FROZEN / NOT EXECUTABLE** and requires a scientific gate before any E3 run. In particular, it does not yet prescribe a qualifying physical network, stable independent-informed policy, acceptance/opt-out protocol, paired no-spillback control, effect-size margin, harm thresholds, replication count or stochastic plan.

This review asks only whether those basic preconditions **already exist in the current source record**. A positive conclusion requires evidence of an executable, prospective, matched scientific protocol; the presence of reusable prior code is insufficient.

## 2. Four non-negotiable readiness gates

| Gate from B-H1 plan | Evidence checked | Status and reason |
|---|---|---|
| **G1. Physically coherent, bounded spillback / cross-traffic setting** | The [B-H1 plan](DIRECTION_B_BH1_SPILLBACK_MINIMUM_DISTINGUISHING_TEST_PROSPECTIVE_PLAN_2026-11-14.md) describes a finite-storage bottleneck and queue intrusion across an upstream intersection, **but defines no frozen physical network and does not show a qualifying blocked cross movement**. The older [Experiment 007 source](../experiments/experiment_007/run_v01.py) creates a 10×10 SUMO grid using \`netgenerate\`, not a prospectively qualified B-H1 test setting. | **NOT READY.** The hypothesized physical blockage has not been established for an actual selected study environment. |
| **G2. Equally informed, credible independently optimizing I** | The [prior T1 schedule code](../research/t1_timing/feasibility.py) implements individual best responses to a **nominal-edge/10-second assigned-demand proxy** with a prespecified 0/10/20/30s menu, rather than physically verified spillback/cross-movement costs. Its convergence on this proxy is not evidence of a stable or adequately optimized **B-H1 independent informed comparator**. The [B-H1 plan](DIRECTION_B_BH1_SPILLBACK_MINIMUM_DISTINGUISHING_TEST_PROSPECTIVE_PLAN_2026-11-14.md) expressly rejects silently substituting old independent A/B policies. | **NOT READY.** Equal information, available physical signal, decision procedure, tie rules and stability criterion are not frozen for B-H1. |
| **G3. Same-information voluntary V with genuine refusal and complete harms** | The B-H1 plan specifies the required **concept** of optional timing changes but no prospective study-specific shifts, eligibility, acceptable predicted concession, acceptance/decline behavior or outcome-completeness specification. Old T1's 5s consent allowance and 50% eligibility are **historical assumptions**, not established B-H1 scientific choices or evidence of real driver willingness. | **NOT READY.** A voluntary test cannot assume everyone accepts, reuse outdated consent thresholds without justification, or conceal harm to those who never enroll. |
| **G4. Paired no-spillback N and complete all-driver cost with mechanism observation** | The B-H1 plan calls for both independent I and voluntary V under physical setting S and matched no-spillback N. No source-backed realization of a paired N with known unaffected bottleneck capacity, cross-traffic blockage logs and all drivers' immutable preferred-to-arrival ledger has yet been qualified. | **NOT READY.** A standard traffic run would not identify the claimed spillback-specific mediator or rule out relocation of waiting. |

**Gate aggregation: 0/4 qualified.** This count is a review of **specification/evidence completeness**, not a measurement of traffic feasibility or a simulation outcome.

## 3. Why launching now would be scientifically misleading

- An independently informed B policy based on a coarse prior assigned-demand proxy might perform poorly for reasons unrelated to voluntary cooperation, producing a false positive for V.
- Without an explicit spillback-capable physical setting and a verified crossing blockage, a shifted schedule could reduce *recorded* queueing yet create no real network benefit.
- Without both I and V in a **paired** N setting, an apparent effect could be caused by changing network geometry/capacity rather than removal of spillback interference.
- Without every driver’s preferred-departure-to-arrival clock and participant/nonparticipant harm report, waiting shifted outside the network could falsely appear as saved traffic time.
- Without frozen shifts, opt-out, harm, effect-size and independent replication rules, choices made after observing test results would make a claimed confirmatory finding unreliable.

## 4. Narrowest executable next step — *scientific qualification, not simulation*

**Authorized direction:** complete the frozen prospective experimental protocol and its design-readiness checks **before** any traffic execution. Keep it small:

1. Specify one minimal physical network with an independently testable downstream storage limit and upstream crossing movement. Require an explicit blocked-crossing observation and an N control that changes only the intended interaction as far as feasible.
2. Specify an I policy that optimizes personal costs under the **same** feasible timing menu and **same nonclairvoyant information** used by V, with frozen tie, iteration, stopping and stability criteria. A separate baseline-qualification failure must halt the study.
3. Freeze an opt-in/decline and limited-concession protocol with explicit assumed acceptance, no human-behavior claims, matched exogenous inputs, and participant/nonparticipant cost accounting.
4. Pre-register the main contrast \`Δ_S = C(V,S) − C(I,S)\`, negative-control contrast \`Ψ = Δ_S − [C(V,N) − C(I,N)]\`, complete-travel outcome \`C(P,M)=Σ_i(a_{i,P,M}−p_i)\`, primary practical margin, fairness thresholds, independent replication plan, stochastic handling, censoring, and falsifying cases.
5. Only after the above **source-verifiable frozen design** is approved should a **development-only** physics/clock/identity smoke or limited pilot be considered, with no reserved or confirmatory cohorts. Any empirical research requires separately documented confirmation that all four gates have passed.

**Stopping rule:** If the four gates cannot be satisfied with one credible minimal setup, stop or reconsider B-H1. **Do not substitute a different simulator, reuse T1's unqualified comparator, tune a predictor, or weaken fairness in order to run something.**

## 5. Scientific disposition

**GO:** to targeted *prospective protocol specification and readiness qualification* under the user's execution approval.

**NO-GO / HOLD:** for **any traffic simulation or outcome claim at this checkpoint**. The model, comparison, negative control, harm accounting and inference rules are not frozen. This is a gate result, **not a negative experimental result for cooperation**.

**Historical decisions unchanged:** Experiment 004 policy-D NO-GO; Experiment 006 primary INCONCLUSIVE / joint efficiency-fairness not met; Experiment 007 Test A NO-GO; T1 ten-second policy development NO-GO; PR #115 UXsim/CityFlow source replication EVIDENCE INSUFFICIENT.

## 6. Primary evidence

- [B-H1 prospective minimum distinguishing plan](DIRECTION_B_BH1_SPILLBACK_MINIMUM_DISTINGUISHING_TEST_PROSPECTIVE_PLAN_2026-11-14.md), including Section 7's explicit four readiness gates and non-execution warning.
- [Direction B conceptual checkpoint](DIRECTION_B_FOUNDATIONAL_COOPERATION_SCIENTIFIC_CHECKPOINT_2026-11-12.md), including separate collective-opportunity, voluntary-feasibility and practical-efficacy levels.
- [Prior T1 schedule feasibility source](../research/t1_timing/feasibility.py), which explicitly calls itself an assigned-demand proxy, not a native physical queue predictor.
- [Experiment 007 runner](../experiments/experiment_007/run_v01.py), which generates the original 10×10 grid and independent route assignments for a different frozen research question.
- [T1 identity-locked final scientific report](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md) and [PR #115 dual-framework assessment](POST_T1_DUAL_FRAMEWORK_SOURCE_REVIEW_AND_DECISION_DRAFT_2026-11-09.md).

**Nothing in this gate report demonstrates an improvement or failure of actual traffic coordination. It records why experimental execution cannot yet make a valid B-H1 scientific claim.**
