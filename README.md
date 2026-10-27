# Can We Make Traffic Flow Better by Cooperating?

Every day, drivers sit in traffic despite having powerful navigation apps. Those apps help us choose routes, but a good route for each driver isn't necessarily the best outcome for everyone.

**What if we could bring some of the collective intelligence of tomorrow's autonomous transportation networks to today's human-driven roads?**

## Current research status — October 26, 2026

We have completed Experiment 001 congestion calibration and the initial Experiment 002 comparison in a 10×10 synthetic SUMO network (1,000 vehicles; departure windows of 200, 600, and 1,200 seconds). In the three-seed development comparison, **independent routing produced shorter average trips than both cooperative-routing prototypes** in every congestion regime. This is an early negative result, not a claim about real-world traffic.

The next question is whether the time-aware traffic predictor is accurate enough to guide coordination. Our [three-regime development trace](docs/EXPERIMENT_002_ACTUAL_PREDICTOR_TRACE_2026-10-26.md) is complete. It is more accurate than free-flow timing in all three tested scenarios but **still significantly underpredicts congestion-related delays**, and is not held-out validation.

**Latest milestone (Oct 26):** The physical occupancy/junction measurement code passed its fixtures and ran on **three new development seeds across all three regimes (nine successful cases, 9,000 total completed trip records)**. Mean time-aware road-entry MAE remained **54.45 / 19.38 / 13.61 seconds** (200/600/1,200s) compared with a free-flow reference of **59.93 / 23.35 / 17.13 seconds** on the same chosen routes. The model still substantially underpredicts congestion delay. Native versus sampled occupancy discrepancies and subsecond junction uncertainties remain open. **No held-out seeds were run.**

- [Research progress report — Experiments 001–002](docs/RESEARCH_PROGRESS_REPORT_2026-10-24.md)
- [Approved Experiment 002 Predictor Validation Plan v0.2](docs/EXPERIMENT_002_PREDICTOR_VALIDATION_PLAN.md)
- [Actual predictor trace: development findings and limitations](docs/EXPERIMENT_002_ACTUAL_PREDICTOR_TRACE_2026-10-26.md)
- [Completed M0–M2 development: physical occupancy & junction-delay findings](docs/EXPERIMENT_002_OCCUPANCY_M2_DEVELOPMENT_RESULTS_2026-10-26.md)
- [Measurement design and M3 holdout gates](docs/EXPERIMENT_002_OCCUPANCY_JUNCTION_MEASUREMENT_PLAN_V0_1.md)
- [Latest G3 reconciliation: occupancy semantics, 211 vehicle-level cases and remaining gates](docs/EXPERIMENT_002_G3_RECONCILIATION_FINDINGS_2026-10-26.md)
- [Next design (review pending): G3 junction exit times and actual route-search occupancy reads](docs/EXPERIMENT_002_G3_EVENT_INSTRUMENTATION_DESIGN_V0_1.md)
- [Archived G3 evidence and CSV tables](docs/results/exp002_g3_2026_10_26/README.md)
- [Successful three-regime decision-trace workflow and artifacts](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40443562182)
- [Proposed separate Experiment 003: voluntary departure scheduling](docs/EXPERIMENT_003_DEPARTURE_SCHEDULING_ROADMAP.md)

**Latest diagnostic insight:** G3 reconciliation suggests much of the native road/FCD discrepancy comes from vehicle front-position versus cross-edge physical-presence semantics. In 211 preselected discrepant bins, vehicle fronts were observed near downstream internal junction boundaries. **The interpretation is not exact native per-vehicle attribution, the G3 gate remains open, and held-out seeds are untouched.**

**Research boundary:** No statistically validated cooperative-routing benefit, deployment readiness, or real-world safety improvement has been established.

## The idea

Explore whether drivers could voluntarily share travel intentions and accept limited, coordinated route recommendations to reduce *total* congestion. This isn't a claim that today's maps do no coordination, or that autonomous cars automatically cooperate. It's a question we can test.

## Original Experiment 001 design goals (historical)

The bullets below preserve the original research design and hypotheses. Some planned participation and baseline-comparison scenarios are not yet implemented; see the current-status section above for what has actually been tested.

- **Question:** Can voluntary coordination among some drivers reduce network-wide congestion without unfairly burdening participants or other drivers?
- **Baseline:** Independent, traffic-aware route choices.
- **Intervention:** A transparent centralized cooperative route assignment, initially holding departure times constant.
- **Participation:** Compare 0%, 5%, 10%, 25%, and 50%, with multiple random seeds and later compliance sensitivity tests.
- **Measures:** Total and average travel time, network delay, congestion, and outcomes for participating and nonparticipating drivers.
- **Fairness:** Limit excessive individual detours and measure spillovers; report null and negative outcomes.
- **First implementation:** A small synthetic network with alternative routes in SUMO, followed by reproducible comparisons.
- **Visualization:** Export the same simulation data for side-by-side animations, short social clips, and eventually an interactive presentation. Stock traffic footage in milestone announcements illustrates the problem, not experiment results.

## Scientific foundations

- **Wardrop's equilibrium:** Individually attractive routes need not minimize total network travel time.
- **System-optimal assignment:** A different distribution of routes may reduce total travel time, sometimes at a cost to particular drivers.
- **Price of anarchy:** The gap between outcomes under self-interested choices and coordinated optimization.
- **Braess's paradox:** Under certain conditions, adding a road can make travel slower.
- **Phantom traffic jams and cooperative control:** Stop-and-go waves can arise without a blockage; controlled vehicle behavior can sometimes dampen them.
- **Mechanism design:** Cooperation must address incentives, consent, fairness, and the temptation to ignore recommendations.
- **Induced demand:** Better traffic flow can encourage additional driving over time.

## Assumptions to challenge

1. Autonomy alone does not imply network-wide cooperation.
2. Coordination of human drivers might deliver benefits using existing smartphones.
3. A minority of participating drivers might influence the wider network; the effect and required participation are unknown.
4. Benefits must be evaluated against capable traffic-aware navigation, not an artificially weak baseline.

**Status:** This initial design milestone is historical; calibration and routing experiments have now been run. See the current-status section above for measured results and remaining gaps.

## Further reading

- [Wardrop's principles](https://en.wikipedia.org/wiki/Wardrop%27s_principles)
- [Braess's paradox](https://en.wikipedia.org/wiki/Braess%27s_paradox)
- [SUMO documentation](https://sumo.dlr.de/docs/)

See [research foundations](docs/research-foundations.md), [experiment plan](docs/experiment-plan.md), and [project checkpoint](docs/checkpoint.md) for evolving notes.
