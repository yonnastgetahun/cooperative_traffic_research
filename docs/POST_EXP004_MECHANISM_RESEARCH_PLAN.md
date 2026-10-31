# Post-Experiment 004: Mechanism Investigation Research Plan

**Status:** Prospective plan. No new mechanism established and no new SUMO simulations initiated.

## Central question
Why did independently improved traffic predictions produce worse collective routing decisions in Experiment 004? Under what conditions could coordination improve network-wide outcomes?

## Verified starting evidence
- Experiment 003 independently reduced chosen-route road-entry timing MAE by **34.2%, 46.3%, 51.3%** in 200s, 600s, 1200s regimes. This did **not** establish accuracy on counterfactual candidate routes.
- Experiment 004 evaluated **120 scenario-arms**: 10 seeds (3301–3310) × three regimes × four policies: A independent, B original time-aware cooperation, C stateful adapter without calibration, D same adapter with calibration.
- Primary 200s C-minus-D completed-trip duration **−18.53s** (95% seed-level CI **−22.59 to −14.47s**): D was slower. At 600s: −1.78s (CI −2.57 to −0.99s); at 1200s: +0.13s (CI −0.11 to +0.37s), inconclusive.
- **100% trip completion** in every scenario. At 200s, D helped 40.0% of matched vehicles, harmed 56.7%, unchanged 3.3%; mean seed-level p90 duration rose from 348.2s (C) to 393.3s (D).
- C/D changed 6,653 of 10,000 routes at 200s; 5,707 at 600s; 4,395 at 1200s. Structured collision files recorded zero collisions. Consolidated OD-cohort harm and numerical emergency-event summaries remain unresolved.
- B/C were not zero-calibration equivalent: the stateful adapter changes search behavior. **D versus C** isolates calibration within the tested adapter; D versus B does not.

## Competing mechanism hypotheses (not established causes)
1. **Candidate-route validity:** calibration fitted on already-selected routes may misrank unchosen alternatives at decision time.
2. **Search/clock effects:** ordinal-aware labels and calibrated time-bin lookups may change path search in unexpected ways.
3. **Occupancy feedback mismatch:** candidate scoring and post-assignment occupancy updates may use inconsistent timing clocks.
4. **Congestion displacement:** individually attractive route switches may concentrate demand or shift bottlenecks.
5. **Objective/fairness misalignment:** local predicted-cost optimization may worsen total network travel time and impose concentrated OD or tail harms.

## Bounded archived-evidence research sequence
1. **Inventory:** identify available frozen code, demand, route assignments, audits, candidate forecasts, occupancy traces, tripinfo, edge observations and exception statistics. Distinguish archived data from absent measures. Preserve seed pairing and hashes.
2. **Decision-change decomposition:** for all three regimes, compare C/D route switches, matched trip-time changes, route overlap, detours, OD cohorts and unchanged-driver spillovers. Use independent seed as inference unit.
3. **Network redistribution:** examine edge-time load and realized delay where archived evidence permits; test whether changed routes concentrate demand and where delays accrue.
4. **Decision-time consistency:** inspect candidate cost, route ordinal, time-bin lookup, occupancy update and guardrail implementations. If candidate ranking traces are absent, document the minimum future instrumentation without pretending to recover historical decisions.
5. **Finish descriptive gaps:** OD-level harm with minimum cohort sizes and seed-level summaries; emergency braking/stops where values are available. Never infer zero from absent fields.
6. **Synthesize:** produce a hypothesis-evidence matrix: supporting, contradictory, and unavailable observations. Distinguish association from causal mechanism. Recommend one highest-information follow-up intervention only if justified.

## Planned outputs
- `docs/POST_EXP004_EVIDENCE_INVENTORY.md`
- `docs/POST_EXP004_MECHANISM_ANALYSIS.md`
- `docs/POST_EXP004_MECHANISM_DECISION.md`

These are future deliverables, not completed results.

## Gate before any new simulation
Do **not** automatically run new seeds, retune calibration, or extend qualification tests. Propose a new controlled experiment only after identifying a discriminating mechanism question, a clean intervention/control comparison, prespecified network outcomes (mean trip time, completion, tail, fairness), and a fresh frozen seed manifest. Keep the policy-D NO-GO intact.

## Approved future research dimensions — scale and network complexity (2026-10-30)

**Decision:** Preserve scale sensitivity as a separate, future scientific investigation **after** the current Experiment 004 archived-mechanism decomposition. This is authorization to document the research direction, **not** authorization to initiate simulations, change frozen experiments, or assign final study parameters.

Three distinct research axes should not be conflated:

1. **Vehicle-demand pressure at fixed network size:** keep the 10×10 network and departure-window definition controlled while changing demand systematically. Investigate whether cooperative routing harm or benefit changes near congestion thresholds. Previously discussed volumes of 750, 1,000, 1,250 and 1,500 vehicles are *illustrative possibilities*, not approved fixed treatment levels. Normalize and report traffic loading, trip distribution, capacity and queues rather than assuming vehicle count alone describes congestion.
2. **Network scale with controlled demand intensity:** compare network sizes independently of vehicle pressure. Preserve meaningful origin–destination distance distributions, arrival/departure intensity relative to network capacity, and comparable congestion regimes. A hypothetical 20×20 grid with 4,000 vehicles is an illustration, **not** a matched-density design or preapproved experiment.
3. **Network topology and bottleneck complexity:** consider road hierarchy, capacity asymmetry, junction delays, arterial bottlenecks and limited alternative corridors. A larger uniform grid need not test these effects. Network *complexity* may be more informative than size alone, but this remains a hypothesis.

**Required sequencing:** finish the current 60 C/D raw-archive matched route-change and unchanged-driver spillover analysis across ten seeds and three congestion regimes, synthesize the competing mechanism explanations, and only then decide whether a tightly controlled causal mechanism test or a scale-sensitivity experiment provides the most discriminating evidence. Do not expand the present mechanism phase into a broad new testing/readiness program.

**Scientific evaluation if later designed:** compare the same well-defined routing arms and credible independent baseline, report network-wide mean and tail duration, completion, waiting/queuing, route switches, participant/nonparticipant or matched-driver fairness where applicable, and uncertainty at independent seed level. Do not treat more vehicles on a bigger grid as an automatic congestion-equivalent comparison. Keep voluntary participation, compliance and departure-time coordination as separate future research variables, not additions to the present Exp004 analysis.

## Scientific boundaries
This result rejects the **tested calibrated routing policy**, not the general possibility of cooperative traffic improvements. Synthetic advance-demand SUMO results do not establish real-world human participation, departure-time coordination, or autonomous fleet effects.

## Sources
- [Experiment 003 confirmatory results](EXPERIMENT_003_CONFIRMATORY_RESULTS.md)
- [Experiment 004 final report](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md)
- [Experiment 004 original 120-arm execution](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41023721390)
- [Experiment 004 final archived audit](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41098364737)

## New-chat kickoff prompt
> Continue Cooperative Traffic Research using `docs/POST_EXP004_MECHANISM_RESEARCH_PLAN.md`. Experiments 003 and 004 are complete; tested policy D received NO-GO. Start by inventorying existing Experiment 004 archives and decomposing why D changed routes and worsened travel times across all three regimes. Treat candidate-route validity, stateful search and clock effects, occupancy feedback, congestion displacement, and objective misalignment as competing hypotheses, not conclusions. No new simulation or calibration tuning yet. Publish evidence-based mechanism findings and identify one next discriminating research test only if warranted.
