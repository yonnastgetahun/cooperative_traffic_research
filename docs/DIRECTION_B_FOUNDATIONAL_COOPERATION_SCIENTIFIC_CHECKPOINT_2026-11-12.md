# Direction B — Foundational cooperation hypothesis: scientific checkpoint and alternative research milestones

**Date:** 2026-11-12  
**Classification:** Source-grounded conceptual scientific assessment; **not an executed experiment, frozen protocol, or authorization to implement**.  
**Scope:** Return from simulator-specific fidelity investigations to the foundational hypothesis. The archived T1 findings and PR #115's **EVIDENCE INSUFFICIENT** source-feasibility disposition remain unchanged. No new traffic runs, framework assessments, adapters, fresh/reserved cohorts, policy changes, or LinkedIn/X publication are part of this checkpoint.

## 1. North Star and three scientifically distinct problems

**Can voluntary coordination among drivers improve network-wide traffic outcomes beyond equally informed independent decisions, without unacceptable costs to participating or nonparticipating drivers?**

Our previous research concentrated heavily on predicting traffic consequences and engineering policies before establishing a clean research setting for the more basic question of whether beneficial arrangements could *exist and be voluntarily sustained*. A failed heuristic does not prove that no beneficial coordinated allocation exists; conversely a theoretical optimum is not evidence of practical cooperative traffic benefit.

Three levels of scientific questions now require explicit separation:

1. **Collective opportunity (existence):** Does the defined congestion system permit a feasible allocation with lower total cost than a credible equilibrium of fully informed independent decisions?
2. **Voluntary feasibility (stability):** Would people rationally accept and maintain such an allocation, with a right to opt out or deviate and without unacceptable harm to nonparticipants?
3. **Practical discovery (efficacy):** Can a nonclairvoyant system identify and deliver those improvements under realistic traffic interactions, limited prediction skill and meaningful fairness constraints?

**Terminology note:** The preceding discussion called these conceptual levels *E1/E2/E3*. This document uses **Level 1/Level 2/Level 3** to avoid confusing them with the project's historical E1-v1/E1-v2 estimator or the E3 junction. These are distinct conceptual stages, **not new numbered project experiments**.

## 2. Historical evidence and preserved scientific decisions

| Project milestone | Actual evidence | Scientific limitation / decision |
|---|---|---|
| [Experiments 001–002](RESEARCH_PROGRESS_REPORT_2026-10-24.md) | On the original 10×10 synthetic network, the two early cooperative routing prototypes were slower than independent baseline routing in all three studied congestion regimes. | Does not prove no cooperative approach can work; original baseline is not a contemporary traffic-aware navigation service. |
| [Experiment 003](EXPERIMENT_003_CONFIRMATORY_RESULTS.md) | Independent held-out chosen-route timing MAE reductions of **34.2%, 46.3%, and 51.3%** across three regimes. | Prediction improvement was not an experiment on network-wide cooperative efficacy. |
| [Experiment 004](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md) | The tested calibrated policy D increased primary high-congestion average trip duration by **18.53 s** relative to uncalibrated adapter C. | Policy D **NO-GO**, not a universal anti-cooperation result. |
| [Experiment 005](EXPERIMENT_005_CLOCK_ALIGNMENT_RESULTS.md) | Clock-alignment correction E improved high-congestion trip duration by **20.13 s** relative to flawed D. | Does not establish E beats independent routing. |
| [Experiment 006](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md) | High-congestion mean A−E advantage **+0.2429 s**, 95% seed CI **[−1.9120, +2.3978] s**; **27.98%** of drivers had >30 s added realized delay. | Primary network superiority **INCONCLUSIVE**; prespecified joint fairness/efficiency GO **not met**; independent A was nominal free-flow. |
| [Experiment 007 Test A](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md) | Frozen marginal-externality estimator's directional agreement **8/20 = 40%** versus 60% required. | Estimator **NO-GO**; cooperative policy Test B **not run**. |
| [E1-v2, F0–F5, C1](POST_EXP007_C1_E3_CONTROLLED_FINAL_SCIENTIFIC_REPORT_2026-11-05.md) | Counterfactual predictor did not qualify; changing one E3 junction priority materially altered route-swap effects in two pre-inspected cases, but worsened absolute costs under both routing assignments. | Effect modification, not validated optimizer, causal bottleneck proof, or cooperative superiority. |
| [Original T1 B/C and ID-locked B*/C*](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md) | Original B/C +618 network-s was confounded by 380 per-driver speed-factor mismatches; better-controlled B*/C* recorded **+2,131 network-s** for C* versus B* on inspected seed 2101. | T1 10-second proxy/policy remains **DEVELOPMENT NO-GO**; residual stochastic event-order coupling unresolved; not independent confirmation of universal harm. |
| [PR #115 dual-framework investigation](POST_T1_DUAL_FRAMEWORK_SOURCE_REVIEW_AND_DECISION_DRAFT_2026-11-09.md) | Read-only UXsim and CityFlow source assessments identified material fidelity and per-driver clock gaps; original 1,000 identities, routes and schedules were archivally reconciled. | Final source-based disposition **EVIDENCE INSUFFICIENT** for exact T1 replication; default-interface restrictions are not disqualifications of entire frameworks. |

**Overall interpretation:** The project has not yet demonstrated a reproducible efficiency advantage attributable to voluntary coordination with acceptable participant and nonparticipant fairness against a credible equally informed independent comparator. Existing NO-GO, INCONCLUSIVE and unexecuted distinctions must remain intact.

## 3. Relevant prior research (external, not original project results)

1. **User equilibrium versus system optimum:** Independently selected routes can produce higher total latency than a collective optimum. The existence of such a gap in some networks is established theory, not novel to our project. See [Roughgarden, *Selfish Routing and the Price of Anarchy*](https://mitpress.mit.edu/9780262549325/selfish-routing-and-the-price-of-anarchy/) and [Roughgarden (2003)](https://doi.org/10.1016/S0022-0000(03)00044-8).
2. **Bottleneck and schedule cost:** [Arnott, de Palma & Lindsey (1990), *Economics of a bottleneck*](https://doi.org/10.1016/0094-1190(90)90028-L) models queues and timing/schedule delay. Faster motion *after* entering the road is not sufficient if inconvenience simply moved before entry.
3. **Cooperative guidance and compliance:** [Klein & Ben-Elia (2018)](https://doi.org/10.1016/j.trf.2018.09.007) experimentally studied compliance with system-optimal traveler information and incentives, relevant to but not equivalent to our proposed voluntary mechanism.
4. **Real-world routing intervention:** [Arora et al., *Nature Cities* (2026)](https://doi.org/10.1038/s44284-026-00443-x) investigated Google Maps interventions targeting approximately **100 high-congestion segments per city in ten US cities** (per the paper's detailed segment-selection description); directly rerouted fewer than 2% of observed trips, reporting roughly **2% increased speeds on targeted segments** and **0.7% shorter network travel times** in the reported study setting. This does **not** establish our precise opt-in, equally informed, all-driver fairness comparison.
5. **Closely adjacent voluntary-cooperation research:** [Ham, Rahimi-Farahani, Zhang & Bansal (2026) preprint](https://infoscience.epfl.ch/entities/publication/1775dc7f-d49e-45c4-85e1-8fefc45fb61d) models conditional cooperation, endogenous enrollment and tipping points, informed by stated-preference surveys across Singapore, the UK and US. It is a **preprint with modeled equilibrium claims**, not evidence of a deployed field success.

**Research distinctiveness requirement:** Our contribution cannot merely be that social traffic optimum differs from independent equilibrium. A consequential contribution would need to isolate *voluntary adherence and incentives*, *information parity and a strong independent comparator*, *full journey costs* and *effects on nonparticipants*.

## 4. An analytical illustration: better collectively, unstable individually

The conventional **nonatomic Pigou two-route model** assumes one divisible unit of demand with two routes:

- Route A: constant cost **1** per unit.
- Route B: cost **x** per unit, where **x** is the fraction using B.
- At individually selfish equilibrium, **x=1**; total system cost **1**.
- With collective optimization, **x=0.5**; total system cost **0.5×1 + 0.5×0.5 = 0.75**, an illustrative **25% reduction** relative to selfish equilibrium cost.
- At this split, someone assigned route A pays 1 while B costs 0.5; absent external commitments or incentives, that driver has reason to switch. Thus the collective improvement is **not automatically self-enforcing**.

This example is **static mathematical illustration, not a traffic simulation or an original observed benefit**, and proves neither compliance nor real-road effects. It establishes why existence and voluntary implementability are different questions.

## 5. Three evidence levels, their proper gates and cost accounting

| Conceptual level | Question | Feasible kind of evidence | Limitation |
|---|---|---|---|
| **Level 1: collective opportunity** | Can a feasible, physically meaningful allocation lower system cost relative to a capable independent equilibrium? | Transparent analytic game/equilibrium or constrained optimization, with documented assumptions and an idealized optimum clearly labeled | A positive answer is not behaviorally or algorithmically deployable |
| **Level 2: voluntary feasibility** | Would individual participation, acceptance, opt-out, deviation, and repeated incentives sustain the benefit without unacceptable nonparticipant harm? | Mechanism and choice constraints, prospective incentive-compatibility/participation tests, appropriate behavioral evidence | Simulated consent is not a measure of real human willingness |
| **Level 3: practical efficacy** | Can an implementable policy find and realize the benefit under real physical/stochastic interactions and fair information? | Separately authorized, preregistered, matched independent evaluation with full cost/fairness and uncertainty | Model-specific evidence is not automatically real-world proof |

For any **future empirical** system with original preferred departures p_i and actual arrivals a_i, the desired primary measure remains:

**All-driver elapsed cost = Σ_i (a_i − p_i).**

Voluntary predeparture waiting and actual admission delay belong in this elapsed cost. Additional preferences (schedule penalties, risk, monetary incentives, recurring commitments) require separately specified *participation utilities* without double counting time. Do not replace complete 1,000- or N-driver accounting with completed-only averages or physical stopped time.

## 6. Smallest prospective scientific investigation (not yet an experiment)

**Working title:** *Voluntary Cooperation Feasibility — Information-Parity and Participation-Constrained Assessment*.

Consider **two competing routes or one constrained bottleneck**, selected for scientific discriminating power, not to guarantee a positive result. Compare:

- **Independent informed policy:** individually rational stable choices with the same information, timing/route menu and physical assumptions;
- **Collective opportunity bound:** explicitly idealized minimization of total model cost, not a claimed deployable optimizer;
- **Voluntary arrangement:** optional recommendations or transparent commitments with a right to opt out, predicted individual concessions and observed nonparticipant consequences as separately defined requirements.

The immediate deliverable is *a paper protocol/analytical feasibility argument*, not source code. Its question is whether **C_voluntary < C_independent**, *together with* explicit participation and fairness constraints, can hold under a defensible scenario. This inequality is conceptual and **not a frozen confirmatory success gate**.

**Bottleneck null case:** A continuously utilized FIFO bottleneck with fixed capacity and unchanged service order can merely shift a queue outside the road; such displacement need not improve any preferred-departure-to-arrival cost. Any proposed timing mechanism must identify a real source of saved delay or prevented spillback, not count moved waiting as benefit.

Possible analytical outcomes:
- **Gain exists and voluntary constraints hold:** motivates prospective physical verification, *not* a declaration of real-world cooperative success.
- **Collective gain exists but cannot be maintained voluntarily:** prioritize incentives, commitments or mechanism redesign.
- **No meaningful collective opportunity in the chosen model:** reconsider the physical situation, not automatically implement another predictor.

These conclusions are strictly specific to the chosen simple model.

## 7. Alternative next milestones — E2 is not the only choice

| Alternative | Core question | Smallest scientific deliverable | Main risk |
|---|---|---|---|
| **A. Opportunity-gap screening (Level 1)** | Is there any nontrivial collective efficiency available under chosen physical constraints? | Analytical equilibrium-versus-social-optimum contrast, including null physical cases | Repeating a textbook example without novel constraints |
| **B. Voluntary feasibility and stability (Level 2; previous E2 recommendation)** | Can opt-in, acceptable concessions and nonparticipant safeguards support an aggregate gain? | Formal participation/obedience constraints and example feasible/infeasible allocations | Assuming real human acceptance from model parameters |
| **C. Strong independent comparator / information parity** | Would apparent gains survive a capable stable independent baseline with equal information and choices? | A prospectively reviewable baseline-and-parity protocol, including convergence and deviation tests | Pure comparison design does not establish effects |
| **D. Incentive and repeated-cooperation mechanisms** | Are immediate no-harm, reciprocal future savings, credits or limited commitments needed to sustain voluntary choices? | Bounded behavioral/mechanism-design comparison, including opt-out incentives and fairness | Speculative preferences and incentive assumptions |
| **E. Physical-effect/null-case analysis** | Does timing or routing avoid genuine bottleneck interference/spillback, or merely move waiting? | Two small analytic physical cases, one allowing gain and one designed to expose queue displacement | Risk of drifting into model-precision engineering again |
| **F. Human-evidence and field-method review** | Which compliance/enrollment/willingness assumptions actually have empirical support? | Evidence synthesis and prospective measurement design with clearly identified unknowns | Does not establish network efficacy |

**Reasoned provisional recommendation:** Start with a very short **A→B conceptual gate**: state the strongest credible independent equilibrium and a potentially meaningful collective opportunity; immediately examine whether opt-out/obedience, limited sacrifices and nonparticipant fairness remove that opportunity. If Level 1 is already trivial in the selected model, **skip re-deriving known theory and make Level 2 the main research deliverable**. Treat C as a required control in either path, not a separate engineering-readiness program. D–F remain genuine alternatives depending on whether the first obstruction is behavioral, physical, or methodological. There is **no requirement to execute these as six sequential projects**.

## 8. Evidence that would change confidence

**Increase confidence:** An independently evaluated, prospectively specified mechanism delivers a meaningful decrease in **full all-driver original-preferred-to-arrival cost**, compared with an equally informed, capable independent comparator, with favorable seed-/unit-level uncertainty and acceptable participant and nonparticipant harms. A theoretical bound alone is insufficient.

**Decrease confidence:** Under credible physical/behavioral assumptions and a qualified comparator, the specified voluntary mechanism has no advantage, or any apparent gain disappears when advance waiting, deviations and fairness are included. That weakens *the mechanism*, not every conceivable form of cooperation.

**Still unresolved:** Cases confounded by shared random events, weak baseline optimization, incomplete trips, unrealistic participation, privileged predictions or incompatible cost clocks.

## 9. Scientific checkpoint and research governance

**Finding:** Traffic-assignment theory already demonstrates some abstract collective inefficiencies of independent routing. Our project-specific gap concerns whether *fair, voluntary, stable, discoverable* benefits can be made credible under identical information and meaningful physical traffic interactions.

**Decision:** Direction B remains the intellectual research direction; **no single next milestone has been approved as an experiment**. Candidate B (Level 2 voluntary feasibility) is strong, but A, C, D, E and F are legitimate scientific options. The next choice should be a bounded conceptual/protocol deliverable selected for information gain, not another broad simulator/engineering program.

**Do not** execute simulations, open existing reserved validation cohorts, implement new policies or adapters, alter historical NO-GO findings, add new simulation frameworks or initiate external social publication under this document. A future experiment requires its own prospective frozen protocol and separate explicit authorization.

**Project evidence hierarchy:** [Foundational synthesis](FOUNDATIONAL_SCIENTIFIC_SYNTHESIS_AND_RESEARCH_DIRECTIONS_2026-10-31.md) → [original experiment reports](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md) and [T1 source/fairness reports](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md) → [PR #115 dual-framework result](POST_T1_DUAL_FRAMEWORK_SOURCE_REVIEW_AND_DECISION_DRAFT_2026-11-09.md). External literature is contextual, not project experimental validation.
