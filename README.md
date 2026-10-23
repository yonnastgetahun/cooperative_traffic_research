# Can We Make Traffic Flow Better by Cooperating?

Every day, drivers sit in traffic despite having powerful navigation apps. Those apps help us choose routes, but a good route for each driver isn't necessarily the best outcome for everyone.

**What if we could bring some of the collective intelligence of tomorrow's autonomous transportation networks to today's human-driven roads?**

## The idea

Explore whether drivers could voluntarily share travel intentions and accept limited, coordinated route recommendations to reduce *total* congestion. This isn't a claim that today's maps do no coordination, or that autonomous cars automatically cooperate. It's a question we can test.

## Experiment 001: design milestone

The initial experiment design is established; implementation and results are still ahead.

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

**Status:** Experiment 001 design complete; no simulation results yet.

## Further reading

- [Wardrop's principles](https://en.wikipedia.org/wiki/Wardrop%27s_principles)
- [Braess's paradox](https://en.wikipedia.org/wiki/Braess%27s_paradox)
- [SUMO documentation](https://sumo.dlr.de/docs/)

See [research foundations](docs/research-foundations.md), [experiment plan](docs/experiment-plan.md), and [project checkpoint](docs/checkpoint.md) for evolving notes.
