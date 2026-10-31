# Cooperative Traffic Research — Foundational Synthesis & Research-Direction Assessment

**Date:** 2026-10-31  
**Status:** Research synthesis and prospective direction assessment; **not a new experiment, algorithm specification, study freeze, or simulation authorization**.  
**Scope:** Return to the original question after Experiments 001–006, compare distinct forms of cooperation, and introduce **quality of journey experience alongside speed** as a first-class future research dimension. Preserve completed negative and positive findings.

## Executive scientific position

**Overarching question:** *Can voluntary, information-enabled coordination among human drivers produce a transportation network that works better for the collective while delivering an acceptable, perhaps smoother and more predictable, experience for individuals? Under what traffic, network and behavioral conditions is that possible?*

The motivating **future scenario**, discussed in the original project conversations, imagines a transportation system with widespread self-driving vehicles benefiting from common awareness and possible coordination. Working backward asks whether a portion of those benefits could be captured by human-driven vehicles through smartphones, shared intentions and voluntary coordination. **This is a research premise, not evidence that autonomous vehicles automatically coordinate, or that present navigation services do no coordination.**

**Current conclusion:** Experiments 001–006 do **not** establish a cooperative system that is both faster network-wide and acceptably fair relative to the original independent routing comparator. They **do** show that predictive accuracy, policy objectives, assignment clocks and traffic interactions are scientifically distinct, and that nominal detour constraints are a poor stand-in for realized harm. The negative Experiment 006 outcome should broaden our inquiry, **not automatically trigger another version of policy E**.

**Important new question:** A journey may be slightly slower yet more predictable, less stop-and-go, less taxing, and more acceptable. Conversely, a small average speed improvement may hide uncomfortable volatility, serious surprise delays, or sacrifices falling on nonparticipants. **Speed, total travel time, perceived quality and fair distribution are not equivalent outcomes.** We must not infer perceived calmness or satisfaction from current SUMO travel-time records.

## 1. Original vision and historical propositions

The earliest [research plan](experiment-plan.md), [project README](../README.md), [research foundations](research-foundations.md), and October 23–24 [progress report](RESEARCH_PROGRESS_REPORT_2026-10-24.md) framed:
1. **Coordination vs independent decisions:** Drivers may jointly allocate road capacity differently from individually selected routes. Sharing intentions might reduce network-wide delays, but this is falsifiable.
2. **Human participation:** Opt-in sharing, compliance and individual consent matter. The historic prospective participation levels were 0%, 5%, 10%, 25%, 50% (with compliance separately varied). These are **proposals, not tested participation effects**.
3. **Bounded, possibly compensated individual sacrifice:** Collective benefits can conflict with individual journey preferences. The project's initial objective was not to require every driver to win every time, but to **understand what tradeoffs can be equitable, voluntary and worthwhile**. Existing harm limits were study-specific decision thresholds, **not elicited participant preferences**.
4. **Temporal cooperation:** Coordinate not only which road drivers use, but **when they depart or enter a bottleneck**, subject to latest-arrival commitments. The historical [departure-scheduling roadmap](EXPERIMENT_003_DEPARTURE_SCHEDULING_ROADMAP.md) proposed 0/30/60/120s voluntary shifts and counting predeparture waiting in total door-to-door cost. It is **unimplemented and unvalidated**. Its title calls it a *proposed Experiment 003*, but the **completed** Experiment 003 is the timing-calibration study. Retain departure scheduling as a **deferred research track**, not a completed experiment or an automatic next feature.
5. **Scientific restraint:** Compare against credible independent, traffic-aware navigation, not merely a weak shortest-path control. Preserve null and negative findings, avoid synthetic-to-real-world claims, and keep user choice, spillovers and local-road impacts visible.

The future-autonomy thought experiment should be tested at the level of **shared information, joint objectives, control and incentive mechanisms**. Autonomy alone does not imply cooperation; human-phone route recommendations are not longitudinal vehicle control.

## 2. Verified evidence: Experiments 001–006

| Phase | Verified evidence | What it does **not** establish |
|---|---|---|
| **001: initial demand calibration** | The same 1,000 vehicles on a 10×10 synthetic grid showed markedly different congestion when departures were spread over 200–1200s; initial independent routing averaged about 198.20s / 146.97s / 138.63s across high/moderate/lower regimes. | Coordinated voluntary departure shifts or real-world congestion reduction. |
| **002: prototype comparisons and independent predictor M3** | Original and time-binned cooperation were slower than independent baseline across initial three-regime comparisons. The held-out M3 time-aware predictor reduced chosen-route timing MAE by about 9.2% / 16.9% / 20.5% versus free-flow timing, but had sizeable signed bias. | Causal routing improvements or correct counterfactual alternative-route ranking. |
| **003: independent timing calibration** | Frozen cumulative correction reduced chosen-route MAE by **34.2% / 46.3% / 51.3%** on disjoint confirmatory seeds. | That improved prediction must improve joint route assignments; Experiment 003 did not change routes. |
| **004: four-arm network test** | Under high congestion, calibrated D worsened mean duration relative to uncalibrated stateful C by **18.5282s** (seed-level 95% CI for D−C **[14.4698,22.5866]s**). Tested D was **NO-GO**; 100% trips completed. | Failure of all forms of coordination or any definitive single failure mechanism. |
| **005: matched clock-alignment intervention** | E, altering only the calibrated chosen-route post-assignment occupancy update clock, improved high-congestion travel time relative to original D by **20.1317s** (95% CI D−E **[16.7378,23.5256]s**); tail and matched-driver safeguards passed **relative to D**. | Superiority to independent routing or proof that clock misalignment was the sole mechanism. |
| **006: E vs independent A** | Fresh paired high-congestion A−E mean **+0.2429s**, 95% CI **[−1.9120,+2.3978]s**: **inconclusive** primary efficiency. **27.98%** of matched drivers were >30s slower with E than A versus a frozen 10% severe-harm threshold: **joint GO not met**. At lower congestion, E was slightly slower than A. | That modern navigation is unbeatable: **A is only independent nominal free-flow shortest path**, not a state-of-the-art dynamic traffic-aware service. |

**Sources of record:** [Exp001–002 progress](RESEARCH_PROGRESS_REPORT_2026-10-24.md); [M3 mechanism](EXPERIMENT_002_M3_BIAS_MECHANISM_RESULTS.md); [Exp003](EXPERIMENT_003_CONFIRMATORY_RESULTS.md); [Exp004](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md); [Exp005](EXPERIMENT_005_CLOCK_ALIGNMENT_RESULTS.md); [Exp006](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md).

### What the Experiment 006 archived harm review added

The [read-only archive review](EXPERIMENT_006_ARCHIVED_SEVERE_HARM_MECHANISM_ANALYSIS.md) compared all 30 original A/E matched scenario archives. For **2,798** high-congestion severe-harm cases (>30s E−A), average additional trip duration was **72.47s**, including **57.17s additional recorded SUMO waiting time**. **2,792/2,798** had the same nominal free-flow route duration and distance in A and E; **882** had precisely unchanged road-edge sequences. The original E candidate guardrails accepted all 30,000 proposed assignments across regimes. Synthetic-grid northeast/southeast destination associations were exploratory; edge-time bottleneck locations have **not** been causally identified.

**Interpretation (limited):** Strong evidence against nominal detour length as the dominant explanation; descriptive evidence consistent with queue/stopped-time exposure and network spillovers. The 57.17s waiting component is an observed association **within a selected harmed cohort**, not a causal mediator estimate. We have **not** established a physical bottleneck, an incentive mechanism, or a route policy that prevents realized harm.

### Inferences we must not make

- Do **not** subtract A/E means from different experiment seed cohorts and call the result a paired treatment effect.
- Do **not** infer that negative E outcomes disprove cooperative scheduling, system-optimal coordination, speed smoothing or partial adoption: those mechanisms have **not been evaluated** by these experiments.
- Do **not** confuse original A's nominal free-flow shortest path with live traffic-aware routing or Wardrop user equilibrium.
- Do **not** claim that 100% modeled route compliance establishes voluntary consent, acceptability or realizable individual safety.
- Do **not** equate a mean of seed-level trip-time p90 values across heterogeneous OD trips with **repeated-trip travel-time reliability** for the same OD/time context.
- The historical 30s/10% Experiment 006 guardrail is a **frozen experiment decision rule**, not a universal ethical boundary or empirically measured participant tolerance.

## 3. Separate the research into three axes, not one sequence of algorithm fixes

| Axis | Independent scientific dimension | Examples |
|---|---|---|
| **Mechanism: what is coordinated?** | Route, departure, bottleneck-entry timing, speed/flow, shared information, incentives | System-optimal route assignment; voluntary time shifting; flow smoothing |
| **Conditions: when and for whom?** | Congestion severity, network size/geometry, topology, percent participating, compliance, information quality, uncertainty, heterogeneous trip constraints | 200/600/1200s demand windows; 5–50% opt-in; arterial chokepoints; imperfect demand |
| **Objectives: what is a better outcome?** | Network duration/throughput, predictability/reliability, smoothness, comfort, individual delay, agency and fair distribution, environmental cost | Mean and tail trip duration; repeated-OD lateness risk; stop/start exposure; user-reported calmness |

**Design implication:** A routing-policy mechanism tested at full penetration on a uniform grid against nominal independent shortest paths tells us very little about a voluntary partial-participation mechanism aimed at reliability or smoothness on a more varied network. Conversely, increasing network size does not by itself test new kinds of coordination.

## 4. Alternative coordination mechanisms: comparative assessment

These are **research candidates**, not approved experiments or implemented policies. All prospective effects below are *hypotheses*, not Cooperative Traffic Research results.

| Candidate mechanism | What it coordinates and optimizes | Core falsifiable question | Key tradeoff / validity risk | Current evidence |
|---|---|---|---|---|
| **A. Individual traffic-aware navigation / shared forecasts** | Shared data and individual predicted journey cost, without binding joint assignment | Does better dynamic independent route choice already capture most of the attainable benefit? | Baseline must actually use dynamic, credible traffic information; our tested A does not | **Baseline gap**; not yet tested |
| **B. Explicit network-externality-aware route assignment** | Route choices evaluated for effect on **other vehicles and total system cost**, potentially subject to fairness limits | Can optimizing actual social consequences outperform individual-time or sequential assigned-count penalties? | Requires realistic counterfactual assignment evaluation; a marginal-cost approximation is not automatically globally optimal | **Mechanism untested**; closest to fundamental user-vs-system optimality question |
| **C. Voluntary departure/bottleneck-entry coordination** | When trips start or enter scarce-capacity segments, possibly combined with routing | Can limited time shifts reduce queuing enough to repay **all predeparture waiting and schedule inconvenience**? | Must honor deadlines, opt-in, generalized door-to-door cost; cannot reuse wider random departure windows as proof | **Historical deferred idea**, untested |
| **D. Traffic-wave smoothing / coordinated driving behavior** | Speed profiles and stop-and-go-wave dynamics, rather than path selection | Can smoother flow reduce oscillations, wasted energy, or uncomfortable driving without requiring shorter trip time? | Vehicle actuation and human phone advice are not interchangeable; safety and comfort need separate validation | **External field literature exists; no local test** |
| **E. Consent- and incentive-compatible participation** | Who opts in, who may sacrifice, compensation/credits/reciprocity, partial compliance | Is a limited-penetration mechanism stable and worthwhile for participants **and nonparticipants** across repeated journeys? | Strategic noncompliance, fairness across users/days and unwillingness to bear unreciprocated harms | **Original design intent**, untested |
| **F. Distributed or adaptive coordination** | Local vs centralized commitments, updates and uncertainty propagation | Can imperfect, evolving information and decentralized decisions produce better outcomes than one-shot advance-demand allocation? | Information delay, oscillatory replanning, communication burden; avoid conflating changed information with changed objective | **Untested** |

**Important distinction:** B, C and D are different physical or optimization interventions; E describes participation and governance conditions that can interact with *any* of them. A is a **benchmark class**, not itself proof of no coordination in existing services. Network topology/volume are **experimental contexts**, not another coordination mechanism.

### Relevant external research (not project findings)

- [FHWA Dynamic Traffic Assignment guide](https://ops.fhwa.dot.gov/publications/fhwahop13015/sec2.htm) distinguishes traveler-optimal, system-optimal and other objectives, and models time-dependent route/departure decisions. This supports explicitly testing the optimization objective rather than equating any predicted-cost routing with system optimum.
- [Dynamic system-optimal traffic assignment with atomic users](https://www.sciencedirect.com/science/article/pii/S0191261521002071) examines marginal social costs and fixed-departure network assignment; it is conceptual precedent, not an established optimum in our simulator.
- [Arnott, de Palma & Lindsey, 1990, *Economics of a bottleneck*](https://www.sciencedirect.com/science/article/abs/pii/009411909090028L) analyzes queue cost **and schedule delay**, reinforcing that coordinating departure must count waiting shifted outside the vehicle.
- [CIRCLES traffic smoothing field experiment, IEEE Control Systems 2025](https://its.berkeley.edu/publications/traffic-smoothing-using-explicit-local-controllers-experimental-evidence-dissipating) provides evidence that controlled vehicle behavior can damp stop-and-go speed oscillations. **That is not evidence our phone-based routing would do so**, nor that subjective calmness automatically improved.
- [FHWA travel-time reliability primer](https://ops.fhwa.dot.gov/publications/fhwahop19062/whatis.htm) distinguishes reliable travel from low congestion and motivates predictability as a separate performance dimension.

No literature example above proves the Cooperative Traffic Research central hypothesis; they establish distinct, well-founded mechanisms to consider.

## 5. Quality of experience vs speed — introduce now, measure honestly later

**New exploratory research dimension, requested October 31:** Evaluate whether the transportation system can provide a **calmer and more dependable journey** even when a trip is not maximally fast. This may be central, rather than secondary, to the future-autonomous-coordination thought experiment.

### A proposed multidimensional outcome framework (not a calibrated utility score)

| Dimension | Candidate measure | What current experiments support | What they do **not** support |
|---|---|---|---|
| **Time and access** | Mean and total end-to-end journey time, person-hours, throughput, missed deadlines | Tripinfo duration, waiting, completion in fixed-departure SUMO | Predeparture sacrifice, real job/family schedule value |
| **Reliability / predictability** | Repeated *same OD and time-context* p90/p95, buffer/planning time, lateness frequency, forecast uncertainty | Cross-seed aggregate trip duration comparisons | True day-to-day reliability with different OD samples/real incidents |
| **Flow smoothness** | Stops per vehicle, time stopped, speed variance, acceleration/jerk exposure, stop-and-go episodes | SUMO `waitingTime` aggregate as **limited stopped-time proxy** | Vehicle trajectory smoothness or comfort from trip duration alone |
| **Perceived comfort and stress** | Traveler-reported calmness, workload, discomfort, perceived predictability or control | **None measured** | Subjective QoE cannot be inferred from queue duration alone |
| **Agency, consent, fairness** | Optional acceptance/rejection, schedule-constraint violations, realized harm distribution, reciprocal benefits over repeated travel | Matched-driver simulation harm comparisons | Actual preferences, compensation adequacy or willingness to comply |
| **Environment and safety** | Fuel/energy, emissions, collisions and validated conflict/near-miss measures | Some structured SUMO exception statistics, not full safety case | Real-world safety, vehicle fuel economy, exposure risks |

**Measurement interpretation:** [FHWA reliability guidance](https://ops.fhwa.dot.gov/publications/tt_reliability/ttr_report.htm) treats predictability and high-delay tails as different from average travel time. [Research on acceleration and jerk vs passenger comfort](https://www.sciencedirect.com/science/article/pii/S0003687022002046) demonstrates why motion profiles matter, but our SUMO archive's travel-time/waiting outcomes do **not** equal measured comfort. Subjective quality requires human reports or validated human-grounded models; operational proxies are not enough.

**Hypothetical Pareto tradeoff, NOT a project result:** a route that takes 90 seconds longer but avoids repeated stoppages and greatly reduces arrival-time uncertainty *might* be preferred by some travelers and rejected by others. We should not impose a universal tradeoff coefficient without preference evidence. Initial research should **report a Pareto frontier** across travel time, reliability, smoothness, and individual harm rather than silently combine them into a single arbitrary 'quality score'.

**Important constraint for future temporal studies:** if a vehicle waits at home before departure, door-to-door generalized elapsed/schedule time **must include that imposed waiting**, even if the SUMO driving segment looks smoother or shorter. Distinguish *time available for other activities* from *unwanted waiting* only when that distinction is specified and validated.

## 6. Which scientific questions now have the highest information value?

These are **candidate investigations**, ranked as directions for thought, **not a preauthorized implementation queue**.

| Research question | Why it deserves attention now | Existing-evidence leverage | Minimum distinguishing evidence before an experiment |
|---|---|---|---|
| **Is the objective wrong?** Route-assignment proxy vs genuine social-cost minimization | Exp006's near-zero network effect and severe individual harm challenge the goal, not just prediction fidelity | Existing A/E assignments and tripinfo give heterogeneous realized effects; cannot reveal unchosen-route counterfactual welfare | Write down feasible counterfactual social-cost and harm-constrained objectives; identify assumptions and a credible dynamic independent benchmark |
| **Is controlling *when*, not only *where*, the missing mechanism?** | Early demand-timing contrasts and queue harm suggest temporal demand pressure matters | Historical regime comparisons show demand-spreading effects, **not voluntary scheduling causality** | Specify schedule deadlines, opt-in, total generalized cost incl predeparture waiting; compare timing-only vs routing-only vs combined |
| **Could quality improve without speed improvements?** | Original 'calmer system' ambition and Exp006 stopped-time patterns warrant wider objective | Existing waiting totals are limited proxies; archived edge-time smoothness absent | Distinguish measurable motion smoothness from subjective quality; select validated outcome definitions |
| **What participation fraction is enough?** | Original human-driver vision is not full compulsory coordination | No mixed-penetration experiment; all treatments assigned all routes | Predefine voluntary participation/compliance and nonparticipant spillover metrics |
| **Where does network structure matter?** | Congestion displacement may depend on bottlenecks and route options | Observed synthetic quadrant associations are descriptive | Vary demand vs grid scale vs topology *separately*, preserving comparable congestion and OD exposure |
| **What is the correct independent benchmark?** | Existing A is nominal shortest-free-flow, below original planned traffic-aware benchmark | Code/source provides exact limitations | Define robust time-dependent independent-rerouting comparator and the type of information it can access |

### Research direction assessment

**Most consequential conceptual gap:** Our tested cooperative mechanisms do **not** explicitly solve an externally validated, network-wide optimal assignment problem. We should not treat successive refinements of E as a general solution. **System-optimal / externality-aware objectives** deserve conceptual scrutiny as a distinct branch.

**Most distinctive untested coordination lever:** **Voluntary departure / bottleneck-entry timing** could change congestion formation without merely shifting drivers onto other roads. Its generalized-time and schedule cost must be modeled honestly.

**Most overlooked outcome:** **Quality of experience**—smoothness, predictability and perceived calmness—has not been scientifically measured, despite being integral to the motivating vision. Start defining its outcome taxonomy **now**, but do not label current SUMO waiting-time records as measured subjective experience.

**Most consequential experimental validity gap:** Before any claim of beating modern navigation, use a stronger credible **independently traffic-aware** baseline. The original A is valid only as the frozen nominal shortest-free-flow comparator used for Experiments 004/006.

**Research design and legitimacy gap:** Full algorithmically imposed compliance does not establish voluntary adoption, equitable allocation of sacrifice, nonparticipant welfare or long-term participation incentives.

## 7. How to choose the next intervention without repeating narrow iteration

Do not write another algorithm or run SUMO yet. The immediate next intellectual deliverable is **one mechanism-comparison decision note** evaluating **at least three substantively different mechanisms**: (i) externality-aware/system-optimal route allocation, (ii) voluntary departure/bottleneck-entry timing, and (iii) speed/flow smoothing or other coordination of motion. Treat consent/partial participation and QoE as cross-cutting dimensions.

Evaluate each candidate explicitly against:
1. **Original-vision fit:** Does it explore an actually distinct form of cooperation, rather than another clock or penalty change?
2. **Falsifiability:** What outcome would refute the hypothesized advantage, and which control cleanly isolates the mechanism?
3. **Public/scientific novelty:** Does existing literature already answer the proposed question? Document overlap and legitimate differentiation, not speculative claims of novelty.
4. **Benchmark credibility:** Is it compared with a realistic independent navigation or non-coordination control rather than only original A?
5. **Fairness and agency:** Can we measure both participants and nonparticipants, actual harms and opportunities to opt out?
6. **Experience and broader welfare:** Can we observe reliability/smoothness without conflating proxies with subjective comfort? Are schedule costs and distribution reported?
7. **Scale and external validity:** Can demand, topology and vehicle participation be varied independently later, without confounding the first result?
8. **Scientific cost:** Does the question require a fresh experiment, or can it be resolved first through existing observations, theory and literature?

**Selection gate:** only after that note should one clearly falsifiable experiment and frozen comparison be nominated. This is a **research decision**, not permission to automatically execute new simulations. Avoid a multi-project engineering roadmap, repeated approval checkpoints or speculative readiness milestones.

## 8. Standing scientific decisions vs open proposals

### Decisions preserved
- Keep completed Experiments 001–006 and their original seed-level conclusions unchanged; Exp004 policy D NO-GO; Exp005 policy E GO *relative to D*; Exp006 A/E primary inconclusive **and joint efficiency/fairness criterion not met**.
- Treat Experiment 006 realized driver harm as essential evidence, but **do not assume policy E is the only future mechanism**.
- Restore the original voluntary-cooperation, participation and departure-time questions.
- Introduce **quality of journey experience vs speed** as a live scientific question now; subjective QoE remains unmeasured.
- Preserve previously approved vehicle-volume, network-scale and topology studies as distinct *future contexts*, not immediate simulations.
- Reaffirm that frozen 30-second harm limits used in an experiment are not universally revealed willingness to sacrifice.

### Proposals, not approvals for execution
- Compare mechanism families and write a direction-selection note before choosing a new intervention.
- Define candidate repeated-trip reliability and trajectory smoothness outcomes; separately consider future user-experience preference elicitation.
- Consider externality-aware system-cost assignment, volunteer scheduling, flow smoothing, mixed participation and stronger independent benchmarks.
- No new model calibration, policy optimization, SUMO seed cohort, safety claim, real-world deployment or social publishing is requested by this synthesis.

## 9. One-sentence project north star

> **Discover when and how voluntary coordination can improve the collective functioning of road traffic while creating journeys that people find reliably acceptable, perhaps calmer and more predictable—even when a small, bounded, consensual sacrifice of speed is involved.**

This remains a scientific hypothesis and research charter, **not an achieved performance claim**.

## External references for context (not evidence from this project)

1. FHWA, [*Traffic Analysis Toolbox XIV: Dynamic Traffic Assignment Fundamentals*](https://ops.fhwa.dot.gov/publications/fhwahop13015/sec2.htm): user vs system optimal objectives, timing and information.
2. Yamaguchi et al., [*Dynamic system optimal traffic assignment with atomic users: Convergence and stability*](https://www.sciencedirect.com/science/article/pii/S0191261521002071), *Transportation Research Part B* (2022): prospective network-externality mechanisms.
3. Arnott, de Palma & Lindsey, [*Economics of a bottleneck*](https://www.sciencedirect.com/science/article/abs/pii/009411909090028L), *Journal of Urban Economics* (1990): scheduling delay + queuing cost.
4. Hayat et al., [*Traffic Smoothing Using Explicit Local Controllers*](https://its.berkeley.edu/publications/traffic-smoothing-using-explicit-local-controllers-experimental-evidence-dissipating), *IEEE Control Systems* (2025): control of stop-and-go waves, not a smartphone-routing study.
5. FHWA, [*Does Travel Time Reliability Matter?*](https://ops.fhwa.dot.gov/publications/fhwahop19062/whatis.htm) and [*Travel Time Reliability: Making It There On Time*](https://ops.fhwa.dot.gov/publications/tt_reliability/ttr_report.htm): reliability distinct from mean speed.
6. [*Standards for passenger comfort in automated vehicles: Acceleration and jerk*](https://www.sciencedirect.com/science/article/pii/S0003687022002046), *Applied Ergonomics* (2023): motion proxies need human grounding.

**Publication state:** This is a foundational synthesis, not Experiment 007. The next numbered experiment remains **unselected**.
