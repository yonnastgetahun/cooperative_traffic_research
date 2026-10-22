# Can We Make Traffic Flow Better by Cooperating?

Every day, drivers sit in traffic despite having powerful navigation apps. Those apps help us choose routes, but a good route for each driver isn't necessarily the best outcome for everyone.

**What if we could bring some of the collective intelligence of tomorrow's autonomous transportation networks to today's human-driven roads?**

## The idea

Explore whether drivers could voluntarily share travel intentions and accept limited, coordinated route recommendations to reduce *total* congestion. This isn't a claim that today's maps do no coordination, or that autonomous cars automatically cooperate. It's a question we can test.

## Scientific foundations

- **Wardrop's equilibrium:** Individually attractive routes need not minimize total network travel time.
- **System-optimal assignment:** A different distribution of routes may reduce total travel time, sometimes at a cost to particular drivers.
- **Price of anarchy:** The gap between outcomes under self-interested choices and coordinated optimization.
- **Braess's paradox:** Under certain conditions, adding a road can make travel slower.
- **Phantom traffic jams and cooperative control:** Stop-and-go waves can arise without a blockage; controlled vehicle behavior can sometimes dampen them.
- **Swarm intelligence and biological networks:** Local interactions can produce useful collective patterns, but biological analogies aren't proof that a traffic intervention will work.
- **Mechanism design:** Cooperation must address incentives, consent, fairness, and the temptation to ignore recommendations.
- **Induced demand:** Better traffic flow can encourage additional driving over time.

## Assumptions to challenge

1. A highly autonomous fleet *might* drive more smoothly, but autonomy alone does not imply network-wide cooperation.
2. Coordination of human drivers might deliver some benefits sooner, using existing smartphones.
3. A minority of participating drivers might influence the wider network; the effect and required participation are unknown.
4. Benefits must be evaluated against capable traffic-aware navigation, not an artificially weak baseline.

## What we'll test

**Hypothesis:** Voluntary, smartphone-compatible coordination of route and timing choices can measurably improve network-wide outcomes compared with independent traffic-aware routing.

Start with an open-source traffic simulation, such as [SUMO](https://sumo.dlr.de/), holding road network and trip demand constant. Compare credible independent routing with coordinated routing at different participation and compliance rates. Measure total travel time, delay, fairness, and spillovers to local streets. Report null or negative results too.

**Status:** Problem framing and research design. No simulation results yet.

## Further reading

- [Wardrop's principles (background)](https://en.wikipedia.org/wiki/Wardrop%27s_principles)
- [Braess's paradox (background)](https://en.wikipedia.org/wiki/Braess%27s_paradox)
- [SUMO documentation](https://sumo.dlr.de/docs/)
- [Slime mold network design research (2010)](https://pubmed.ncbi.nlm.nih.gov/20093467/)

See [research foundations](docs/research-foundations.md), [experiment plan](docs/experiment-plan.md), and [project checkpoint](docs/checkpoint.md) for evolving notes.
