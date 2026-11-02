# Coordination Mechanisms — Comparative Scientific Assessment and Experiment 007 Direction

**Date:** November 1, 2026  
**Status:** Prospective **scientific direction recommendation** only. Not an Experiment 007 frozen protocol, implementation authorization, simulation execution, efficacy finding, or social publication.  
**Scope:** Collective traffic efficiency and realized individual fairness for voluntary human-driver coordination. **Subjective journey quality is deferred.**

## Executive decision

**Recommend a bounded Experiment 007 comparing externality-aware collective route assignment with credible, independently traffic-aware route choice under the same usable information and fixed departure demand.**

The comparison should focus on the **optimization objective**, not rescue policy E or repeat better-prediction tests. The social-cost-aware intervention should seek to reduce expected total network travel time while constraining prospective individual burdens and measuring **realized** harms and nonparticipant spillovers. The independent control must be more credible than legacy A's nominal free-flow shortest paths. Do not label a practical heuristic “system-optimal” without appropriate optimality evidence.

**Second priority:** voluntary departure/bottleneck-entry timing, where the mechanism is physically plausible and existing severe-delay evidence points to queues but the benefit must survive predeparture waiting, deadline and schedule costs.  
**Separate future track:** coordinated traffic-flow control. Literature demonstrates physical wave suppression using controlled automated vehicles; smartphone advice to human drivers cannot be equated with automated acceleration control.

The preference for route assignment is based on **discriminating information value, comparability to the existing evidence, a clean objective-level manipulation and direct fit with the human-driver project vision**—not a prediction it will win. A negative or fairness-deficient result would be scientifically informative.

## 1. Archived project evidence reviewed

Authoritative files:
- [Foundational scientific synthesis](FOUNDATIONAL_SCIENTIFIC_SYNTHESIS_AND_RESEARCH_DIRECTIONS_2026-10-31.md).
- [Exp001–002 research progress](RESEARCH_PROGRESS_REPORT_2026-10-24.md) and [M3 mechanism results](EXPERIMENT_002_M3_BIAS_MECHANISM_RESULTS.md).
- [Exp003 confirmatory prediction](EXPERIMENT_003_CONFIRMATORY_RESULTS.md).
- [Exp004 final four-arm report](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md).
- [Exp005 clock-alignment intervention](EXPERIMENT_005_CLOCK_ALIGNMENT_RESULTS.md).
- [Exp006 E vs A final report](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md), [archived harm investigation](EXPERIMENT_006_ARCHIVED_SEVERE_HARM_MECHANISM_ANALYSIS.md) and [permanent paired seed evidence](results/exp006_a_vs_e_seed_level.csv).
- [Historical cooperative departure-scheduling roadmap](EXPERIMENT_003_DEPARTURE_SCHEDULING_ROADMAP.md); its old “Experiment 003” title is historical, **not** the completed Exp003.

The synthetic 10x10 SUMO grid used 1,000 vehicles and 200/600/1,200-second demand windows. Exp001–002 cooperation was slower than independent routing in its initial comparisons. Exp003 improved chosen-route road-entry forecast MAE by 34.2/46.3/51.3% on independent confirmatory demand; it did not improve routing decisions because no decisions were changed. Exp004's calibrated D was 18.5282s slower than uncalibrated C in high congestion (95% seed-level interval D−C: +14.4698 to +22.5866s); 56.7% of matched drivers were slower. Exp005's alignment of the chosen-route post-assignment occupancy clock made E 20.1317s faster than D (95% D−E interval +16.7378 to +23.5256s) but **did not compare to A**.

Exp006 matched fresh A/E seeds: high-congestion independent A minus cooperative E = **+0.2429 seconds**, 95% CI **[−1.9120,+2.3978] seconds**; network superiority **inconclusive**. **2,798/10,000 (27.98%)** drivers experienced E−A realized delays greater than 30s, versus the experiment-specific 10% severe-harm ceiling; the **joint efficiency/fairness criterion was not met**. A was **nominal free-flow shortest-path**, not dynamic traffic-aware independent navigation.

Among Exp006's selected high-congestion severe-harm cohort, mean additional time was +72.47s, of which +57.17s was observed additional SUMO stopped/near-stopped waiting; 2,792/2,798 had exactly equal reconstructed nominal route time/distance; **882** had unchanged road-edge sequences. These descriptive associations are consistent with queue-mediated redistribution/spillovers. They are **not** identified physical bottleneck causal effects, proof that changing routes causes harm, or evidence that system optimum will help. Existing nominal detour restrictions rejected none of 30,000 proposals; they were not realized-delay safeguards.

Do not use independent drivers as the inferential sample size: matched driver identities support per-driver contrasts, while independent demand **seeds** are the replication units. Do not subtract cross-experiment seed cohort averages as paired causal effects. Keep old Exp006's 30s/10% safeguard a **historical preregistered rule**, not a universal willingness-to-sacrifice estimate.

## 2. External scientific foundations and prior art

### A. System-optimal / externality-aware route assignment
FHWA's Dynamic Traffic Assignment (DTA) guide distinguishes user-optimal, system-optimal and reactive models, route and departure choices, and information availability. A competitive independent baseline must be specified behaviorally; it need not achieve Wardrop dynamic equilibrium to be useful, but neither can historical free-flow A be called a modern independent navigator. [FHWA DTA Fundamentals](https://ops.fhwa.dot.gov/publications/fhwahop13015/sec2.htm).

The **mechanism** is that selecting route r for traveler i changes other travelers' congestion and total cost, not just i's travel time. In stylized link models, marginal social cost includes costs imposed on others as load changes; in dynamic vehicle-level SUMO networks with junction interactions, neither a static edge-count penalty nor a calibrated chosen-route arrival clock is a validated marginal-cost model. Satsukawa, Wada and Watling (2022) study dynamic system-optimal assignment with fixed departures and atomic users, plus marginal-social-cost implementation; it does **not** validate this repository's implementation. [Paper](https://doi.org/10.1016/j.trb.2021.11.001).

Fairness-constrained network assignments are already researched. See [Minimizing the total travel time with limited unfairness in traffic networks (2020)](https://doi.org/10.1016/j.cor.2020.105016) and Jalota et al., [Balancing fairness and efficiency in traffic routing via interpolated traffic assignment (2023)](https://doi.org/10.1007/s10458-023-09616-7). These establish **prior art**, not a new project result. They also highlight why minimizing aggregate cost alone can disadvantage individual travelers. Published mathematical fairness definitions (e.g., comparable travelers with common OD) are **not identical** to Exp006's matched driver's realized E−A harm.

**Distinct falsifiable hypothesis:** On prespecified matched demand and an equally informed, independently traffic-aware control, externality-aware route coordination reduces *realized* network mean/total travel time without exceeding prespecified realized-harm safeguards for participants **or nonparticipants**. A nonpositive/uncertain primary benefit, a benefit solely against legacy A, or unacceptable harmed-driver spillovers would fail the intended joint claim.

**Main methodological risk:** Accurate counterfactual system cost for unchosen route assignments is not supplied by Exp003's chosen-route timing calibration. Search behavior, assignment order, forecast updating, and information access must be matched or disclosed; an alleged globally optimal solution must be supported by a valid bound or replaced with the narrower term **externality-aware heuristic**. Unlimited future SUMO observations for the treatment alone would create a clairvoyant and invalid comparison.

### B. Cooperative departure / bottleneck-entry timing
The **mechanism** is smoothing arrivals to a capacity-constrained road or junction, rather than changing road paths. Classic bottleneck analysis treats queuing **and schedule delay** as actual social costs; in some theoretical models, changing departure choices can eliminate queueing even when the route split is unchanged. See Arnott, de Palma and Lindsey (1990), [Economics of a bottleneck](https://doi.org/10.1016/0094-1190(90)90028-L), and [Departure time and route choice for the morning commute](https://ideas.repec.org/a/eee/transb/v24y1990i3p209-228.html).

Real-world incentive experiments suggest some commuters shift timing, with important transfer limits. The Dutch peak-avoidance experiment reported lower peak travel by incentivized participants but reversion after incentives; this is not evidence that our proposed app-mediated coordination provides net door-to-door savings. [Ettema, Knockaert, Verhoef, 2010](https://doi.org/10.3328/TL.2010.02.01.39-51). Other smartphone-app research analyzes heterogeneous incentive responses. [Arian et al., 2018](https://doi.org/10.1016/bs.atpp.2018.07.001). [Kreindler, Peak-Hour Road Congestion Pricing, 2023](https://www.nber.org/papers/w30903) reinforces that departure inflexibility and actual congestion externalities matter.

**Distinct falsifiable hypothesis:** Under matched OD demand and fixed baseline route policy, voluntary shifts bounded by explicit earliest-departure/latest-arrival and participation constraints reduce *generalized* total door-to-door cost versus drivers choosing departures independently, once predeparture waiting, arriving early/late and deadline failures are counted.

**Main methodological risk:** The previous 200-to-1,200-second demand-window comparisons changed congestion pressure exogenously; they were **not** coordinated voluntary choices and cannot establish net benefit. Saving 40s of in-vehicle delay at the cost of 60s of predeparture waiting is not a 40s collective benefit. Bounded opt-in time flexibility cannot be treated as an arbitrary unpriced departure adjustment. Need explicit preference/deadline assumptions; outcomes are conditional on synthetic willingness models, not observed user consent.

**Potential discriminating comparison after Exp007:** fixed routes and eligibility with independent departure timing vs coordinated shifts, with a separate route+timing factorial **only after** a timing-only effect is supported. Never hide shifted delay outside SUMO tripinfo.

### C. Coordinated traffic-flow control
The **mechanism** is to damp self-exciting speed waves and junction or freeway flow perturbations through coordinated speed/spacing behavior, without rerouting vehicles. It changes the controlled dynamics of vehicles, not the objective of a route recommendation.

Controlled-vehicle studies provide specific external evidence: [Stern et al., Dissipation of stop-and-go waves via control of autonomous vehicles: Field experiments (2018)](https://www.sciencedirect.com/science/article/pii/S0968090X18301517) reports circular-track wave damping with one autonomous controlled vehicle. [Hayat et al., Traffic Smoothing Using Explicit Local Controllers (IEEE Control Systems, 2025)](https://doi.org/10.1109/MCS.2024.3503402) reports real traffic wave damping during an I-24 experiment. Those are **actuated control** demonstrations under their own settings; neither is evidence that a smartphone can obtain reliable, safe acceleration compliance from human drivers or that urban junction delay will necessarily fall.

**Distinct falsifiable hypothesis:** Holding routes, demand and departures fixed, a clearly defined controlled-vehicle policy reduces realized network total delay/stop-wave propagation relative to the same uncontrolled car-following traffic, without creating throughput or individual-harm regressions.

**Main methodological risk:** An automated-control arm and a no-control human-driving baseline mix the physics of actuation and participation modality. A smartphone-only counterpart would need realistically bounded human response, delay, distraction/safety constraints and compliance evidence, which this project lacks. Real-world controlled-AV effects cannot be imputed to the phone-mediated human-driver vision.

## 3. Comparison against the active project criteria

| Criterion | Externality-aware routing | Cooperative departure timing | Flow control |
|---|---|---|---|
| Distinct controlled variable | Assignment objective and multi-driver routes | Departure or bottleneck arrival times | Vehicle speed/spacing trajectories |
| Direct fit to present human + smartphone concept | **High**, as route recommendations | **High**, as optional schedule advice | **Low for automated actuation**; human phone compliance speculative |
| Relevant strong literature | DTA system optimum and fairness-constrained assignment | Bottleneck theory and timing incentives | Field control and wave dissipation |
| Project mechanism already tested? | **No**: E is not a verified social-cost optimizer | **No**: demand windows do not test volunteer timing | **No** |
| Control needed | Dynamic, independent traffic-aware navigation with equal information | Independent time choices with same route policy and schedule costs | Same fixed routes/departures, no flow controller |
| Fairness concern | Rerouted drivers and nonparticipant congestion spillovers | Waiting shifted to predeparture, early/late arrival, inflexibility | Control burden and heterogeneity; causal safety/response claims |
| Measurement availability | Existing SUMO tripinfo; missing reliable counterfactual marginal-cost evaluation | Existing tripinfo plus **new explicit scheduling costs/deadlines** | Time-resolved trajectories and control-specific measurements |
| Closest current scientific uncertainty | **Objective mismatch and externalities**, directly addresses Exp006 | **Queue pressure and temporally shifted cost** | Stop-wave control on a primarily urban grid |
| Cost/identification risk | Moderate/high: dynamic cost externalities difficult | Moderate: specify realistic feasible schedule preferences | High for faithful human-phone implementation |
| Recommended priority | **1**: first rigorous objective comparison | **2**: separate mechanism if route allocation fails or for next factorial stage | **3**: separate vehicle-control research line |

These rankings are qualitative research judgments, not estimated effect sizes or numerical scores. The system-optimal literature is mature; the project's legitimate contribution would be a **transparent empirical test under its information and opt-in constraints**, not claiming invention of system-optimal routing.

## 4. Proposed Experiment 007 — research design direction, NOT frozen protocol

### Primary question and mechanism isolation

**Does accounting for each recommended route's anticipated costs imposed on every vehicle—rather than only the recommended driver's own time—improve *realized* network outcomes in the existing simulator, versus a capable independent navigator with the same available information?**

Specify the objective in advance: approximately minimize the expected sum of **all vehicles'** trip durations at fixed OD demand and departure commitments, not just participant durations. Any fairness constraint is a separate feasibility condition: expected individual burden limits may be applied **ex ante**, while realized matched harms must be audited **ex post**. Do not optimize on held-out outcomes.

A defensible candidate-arm naming convention:
- **I: Independent traffic-aware route choice (new primary comparator).** Drivers select routes to minimize **own** predicted travel time; use a documented dynamic traffic forecast and consistent clock, candidate route set, observation cadence, replanning policy and computational budget. Do **not** call I equilibrium without measuring equilibrium conditions; it is a *traffic-aware independent policy*.
- **S: Externality-aware collective assignment (primary intervention).** The same drivers and candidate choices, same timely information/forecast and budget; eligible opt-in drivers are assigned routes using a prospective proxy for **change in expected whole-network travel time**, with predeclared expected-harm eligibility. Others follow the same independent I logic. No clairvoyant access to future realized simulator states.
- **Historical A (optional descriptive comparator)** remains fixed free-flow shortest path and can aid continuity. It is **not** the primary success benchmark and cannot support claims about Google Maps, Waze or Apple Maps.
- **Historical E** is not a mandatory test arm; comparing against E would answer an algorithm-repair question, not isolate the optimization objective.

An externality cost may be approximated by incremental whole-network loading or suitably validated marginal-cost estimates, including junction interactions and future edge-time loads; a static route-count penalty does not by itself suffice. The planner need not find a global optimum to test this **mechanism**, but any heuristic gap and incomplete counterfactual accuracy must be disclosed.

### Demand and participation

- **Hold fixed** road graph, OD pairs, vehicle counts, scheduled departure times, traffic controls, vehicle behavior, simulator version and random demand seed across I/S. Start with the original **200-second high-congestion regime** as primary because it most strongly exposes congestion interactions; retain the 600/1,200-second regimes as prespecified secondary tests if feasible.
- Candidate **50% simulated opt-in** primary condition is a design proposal informed by the historic 0/5/10/25/50% participation roadmap, not an empirically estimated rate. Participants comply with accepted recommendations only as a **conditional simulation assumption**. Specify the deterministic, seed-reproducible opt-in assignment and balance OD, departure phase and baseline trip length. The 50% nonparticipants follow I in both arms; separately report whether S imposes costs on them.
- An additional **100% eligible participation** sensitivity could diagnose the hypothetical coordination ceiling, not consumer adoption. Avoid a huge participation × topology × demand factorial before finding whether any objective-level effect exists.
- Route-change counts and assignment concentration are diagnostics, not the primary efficiency endpoint.

### Outcomes and decision logic to preregister

**Primary:** paired seed-level difference in realized mean completed-trip duration **I−S** under high congestion, positive favoring S. With the same 1,000 demands and complete trips, total network travel time is exactly 1,000 times the mean; both can be reported without treating them as separate independent outcomes. Use a 95% confidence interval across independently generated paired **seeds**, not driver-level independent samples. A practical minimum effect should be prespecified and justified before testing; do not claim useful improvement from a positive point estimate alone.

**Secondary collective:** total waiting and timeLoss (defined without double counting), number and timing of completions, cumulative discharge/throughput by fixed observation interval, upper-tail completed-trip duration, and road/junction congestion measurements where instrumented. If all 1,000 eventually complete, “100% throughput” is not a useful distinguishing claim; examine temporal discharge, not just totals. Do not equate changed routes or static assigned-edge counts with actual queue relief.

**Fairness and agency:** matched individual **S−I realized delay** distribution, share helped/harmed, p90/p95 within-driver harm, share exceeding a prospective severe-delay threshold, nonparticipant vs participant outcomes, subgroup/OD harms with adequately sized cohorts and seed-level uncertainty. Exp006's >30s/10% benchmark may be retained as a *transparent sensitivity for continuity*, but any new pass/fail threshold requires explicit prospectively justified selection; nominal detour caps do **not** count as realized-harm protection. Treat true consent, opt-out propensity and adherence as **untested** by this simulation.

**Decision:** meaningful aggregate improvement **and** acceptable prespecified realized harm, especially to nonparticipants, must both be supported. Otherwise report **NO-GO for the tested S version**, or **inconclusive** where confidence intervals are too wide. The outcome cannot establish a universal optimum or real-world impact.

### Pre-execution scientific validity gate

Before any frozen Experiment 007 design or SUMO runs, answer:
1. Is there a feasible traffic-aware independent I baseline with the **same information** available to S, explicit computation/replanning cadence and no forecast leakage? If not, the first unit of work is defining a fair comparator, not simulating.
2. Can a candidate's **incremental network externality**, including consequences for nonparticipants, be estimated without using eventual realized SUMO outcomes from the evaluation seed? A prospective heuristic is acceptable, but must be named accurately and validated on separate development demand.
3. How will the proposed algorithm avoid the forecasting-clock and assignment-state inconsistency discovered in Exp005, without simply reproducing E's route-count proxy?
4. What are the predeclared **primary positive practical effect** and independently evaluated realized **fairness gates**? How will they handle uncertainty and censoring?
5. Is the schedule truly held fixed and compliance transparently a simulation assumption? This test must not silently incorporate departure coordination.

Then write and approve a separately frozen scientific protocol: seed allocation, candidate procedures, comparator definitions, simulation integrity controls and success gates. **Do not run any new simulation or algorithm implementation on the authority of this assessment.**

## 5. Why not choose the other mechanisms as Experiment 007 now?

**Departure timing** is plausible and perhaps ultimately more effective against queueing, but Exp006's +57.17s additional stopped time is not proof that drivers have willingness or ability to move travel times, nor that such movement yields a net benefit when predeparture cost is counted. A cleaner, separate timing-only study should follow the route-objective comparison if network externalities remain unresolved.

**Flow control** already has unusually strong external field demonstrations in a different intervention class. Our project's first scientific goal is voluntary, smartphone-facilitated cooperation among human drivers, and a realistic smartphone-to-physical-control response model is currently unsupported. It is a worthwhile independent future line, not a valid test of phone-only route coordination.

**What would change this recommendation?** If a minimally credible independent I baseline and incremental social-cost signal cannot be specified without unacceptable clairvoyance or unbounded complexity, route-objective identification fails the *pre-execution gate*. In that case prioritize a **timing-only, opt-in, schedule-cost-complete** Experiment 007 instead. This is a clear decision contingency, not a license to retune E.

## 6. Knowledge claims and communication boundary

**Established project facts:** the specific Exp003–006 numerical results, null/inconclusive decision, failed fairness gate and retrospective queue-associated harm statistics listed above.

**Existing external science:** DTA objectives and marginal externalities, bottleneck departure/schedule delay, published fairness-constrained assignment, and actuated traffic-wave smoothing under their respective conditions.

**Untested project hypotheses:** explicit social-cost-aware routes can outperform **traffic-aware independent** navigation; voluntary time shifts can deliver net collective cost savings; flow smoothing can work via smartphone guidance to human drivers; any proposed opt-in or harm threshold reflects actual traveler choice.

**Publication:** No LinkedIn or X publication is authorized by this assessment. Only after a **substantive scientific result**, prepare verified visual-first assets (mobile-readable 5–7 slide PDF for LinkedIn; up to four individually legible PNGs for X), platform captions and **one research GitHub landing page**. Present final media and copy for user approval before publishing. Use Metricool for LinkedIn and the existing GitHub Actions/X integration for X, with media-attachment verification and published URLs. Do not substitute text-only posts if media fails.

---
**Research status:** Comparative assessment complete; **Experiment 007 mechanism recommended, not implemented, frozen, simulated or proven.**
