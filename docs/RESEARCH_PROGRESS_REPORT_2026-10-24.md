# Cooperative Traffic Research — Progress Report
**Research session:** October 23–24, 2026 (Pacific time)  
**Repository:** [cooperative_traffic_research](https://github.com/yonnastgetahun/cooperative_traffic_research)  
**Scope:** Experiments 001–002; Experiment 003 design extension  
**Status:** Experimental infrastructure functioning; three-regime comparison completed; predictor accuracy investigation in progress. **No cooperative-routing improvement demonstrated.**

## Executive summary
We built and operated a reproducible, GitHub Actions–based SUMO research pipeline without needing to run experiments on a local Mac. We established three distinct congestion conditions on a 10×10 synthetic road network with 1,000 vehicles, validated their repeatability, and tested independent routing against two cooperative-routing prototypes.

Both cooperative strategies were slower on average than independent routing in all three congestion regimes tested. We diagnosed route redistribution, created a time-aware routing prototype with predicted detour guardrails, closed a gap in the three-regime coverage, and launched predictor-validation instrumentation. The first successful prediction-vs-observation smoke test showed substantial error in a **free-flow arrival-time reconstruction**, which is a diagnostic reference and **not yet a direct validation of the full congestion-aware cost predictor**.

## 1. What we did

### Experiment 001 — Demand calibration and reproducibility
- Fixed a 10×10 grid, 200-meter edges and 1,000 passenger vehicles.
- Varied the departure window (200, 300, 600, 900, 1,200 seconds) to induce different congestion levels without changing fleet size.
- Selected 200 seconds (high), 600 seconds (moderate) and 1,200 seconds (low) as the primary research regimes.
- Ran a nine-case reproducibility matrix: all three windows × seeds 1001, 1002, 1003. All nine jobs succeeded, each completing 1,000 trips.
- Mean independent-routing trip durations across the three seeds were approximately 198.20s (high), 146.97s (moderate), 138.63s (low).

### Experiment 002 — Initial cooperative-routing tests
- Implemented a deterministic, predeparture, shared edge-assignment-count routing prototype. This is **not** real-time vehicle coordination.
- Conducted a paired 1,000-vehicle smoke test (200-second window, seed 1001); fixed an initial missing SUMO Python module path.
- Tested congestion penalties 0.01, 0.02, 0.04, 0.08, 0.12. All five jobs succeeded. None beat the independent baseline in that single scenario; 0.02 was the least-bad tested cooperative setting.
- Ran vehicle-level and road-level diagnostic workflows. Fixed a SUMO output-path error during the road-level instrumentation.
- Observed heterogeneous road-speed changes and individual-driver impacts. These support further investigation of congestion redistribution but do not by themselves identify a causal bottleneck.

### Time-aware cooperative-routing prototype
- Implemented a prototype that assigns routes using coarse time-binned planned edge occupancy and a simplified junction penalty.
- Added predicted free-flow detour guards (10% or 30 seconds, whichever is smaller, and a 15% distance cap). These **do not guarantee realized travel-time fairness or physical safety**.
- Fixed an outgoing-edge SUMO API mismatch; successful smoke test then compared independent, original cooperative and time-aware routing.
- On the 200-second, seed-1001 smoke test, mean trip durations were approximately 197.67s (independent), 199.54s (original cooperative), 209.85s (time-aware). All 1,000 trips per arm completed.

### Corrected experimental coverage gap
We discovered that although Experiment 001 used all three congestion regimes, the subsequent Experiment 002 algorithm tests and diagnostics had largely remained at 200 seconds. This was a **workflow implementation/coverage oversight**, not an intentional narrowing of the research question.

We created a new isolated [three-regime coverage backfill workflow](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40072443736). It successfully completed **nine paired scenarios** (200/600/1,200 seconds × seeds 1001/1002/1003), each comparing the same three routing strategies. This closed the initial coverage gap, though it is not a held-out statistical validation.

## 2. Principal results

**Average trip duration (seconds), mean across three seeds; lower is better**

| Congestion / departure window | Independent | Original cooperative (penalty 0.02) | Time-aware cooperative |
|---|---:|---:|---:|
| High / 200s | **198.20** | 204.02 | 212.09 |
| Moderate / 600s | **146.97** | 148.54 | 151.40 |
| Low / 1,200s | **138.63** | 140.47 | 140.94 |

**Interpretation:** Independent routing had the lowest mean duration in all three tested regimes. The time-aware candidate was particularly worse under high congestion. These are initial synthetic-network, three-seed results. We have **not** established statistical significance, real-world transferability or safety.

## 3. Predictor-validation milestone
- Published [Predictor Validation Plan v0.2](https://github.com/yonnastgetahun/cooperative_traffic_research/blob/main/docs/EXPERIMENT_002_PREDICTOR_VALIDATION_PLAN.md), updated with all three congestion regimes and the completed coverage evidence; approval was subsequently granted for implementation.
- Implemented an isolated instrumentation workflow to record forecasts, observe SUMO traffic using FCD output, and compare predictions to observations.
- Fixed an unsupported FCD period option; [the successful predictor-validation smoke run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40073685024) used development seed 2001 and the 200-second window.
- Recorded **8,367 matched planned edge traversals**, with mean absolute road-entry time error approximately **58.9 seconds** and p95 absolute error approximately **197.3 seconds**. The occupancy-bin comparison's mean absolute count difference was approximately **1.87 vehicles**.
- **Critical limitation:** These metrics compare a reconstructed **free-flow arrival forecast along the chosen routes** with observed SUMO trajectories. They do not yet directly measure the original time-aware route search's congestion surcharge or junction-cost forecasts. Occupancy counts are sampled unique vehicles per time bin, not instantaneous physical occupancy. The predictor itself has **not passed validation**.

## 4. What we learned
1. **Traffic demand timing matters.** Spreading the same 1,000 departures across a longer window materially reduced congestion in the synthetic baseline. This is not proof that voluntary individual departure scheduling would improve total door-to-door journey time.
2. **Rerouting is not automatically beneficial.** Hundreds of routes changed, yet system mean trip duration worsened.
3. **Congestion must be modeled in space *and* time.** A cumulative edge-assignment count and crude time-bin proxies omit realistic queue formation, signal/intersection delay and occupancy dynamics.
4. **Predicted detour limits are not realized-harm limits.** A route can satisfy a planning threshold and still impose unexpected delay on a driver.
5. **Coverage must be enforced explicitly.** Single-regime smoke tests are useful, but cannot substitute for a three-regime comparative study.
6. **Instrumentation is a research result, not proof of accuracy.** The new measurement pipeline works, but the first error estimates concern a free-flow reference model and require deeper validation.

## 5. What is next (priority order)

### Next milestone — Instrument the actual congestion-aware predictor
1. Add a *non-policy-changing* trace of every routing decision: vehicle ID, edge, predicted entry/exit time, estimated occupancy, free-flow cost, congestion surcharge, junction penalty, candidate route, chosen route and rejection reason.
2. Validate units, time-bin semantics and route legality. Fix measurement definitions for occupancy spanning multiple time bins; distinguish predicted counts from observed vehicle-seconds and occupancy.
3. Align frozen predictions with observed SUMO edge entry/exit events. Quantify timing and traversal errors, missingness, systematic bias, queue/intersection effects and forecast error accumulation.
4. Benchmark against free-flow-only and cumulative edge-count references. Do not assume the more complex predictor is better.
5. Report whether errors arise from the predictor, the route-selection objective, or both; do not tune against held-out data.

### Then — Full three-regime predictor calibration and validation
- Use 200, 600 and 1,200-second departure windows, 1,000 vehicles, identical paired inputs.
- Prespecify **new disjoint calibration and evaluation seeds**. Seeds 1001–1003 have already informed development and are not untouched holdouts; seed 2001 is a development smoke seed.
- Begin with at least three calibration seeds per regime; target at least ten held-out paired seeds per regime for stronger uncertainty estimates, without claiming this automatically provides adequate statistical power.
- Freeze predictor settings before held-out tests. Report seed-level results, uncertainty, total journey time, fairness and completion.
- Only after predictor accuracy and objective alignment are understood should we design a new routing algorithm or broad optimization sweep.

### Separate future extension — Experiment 003
[Cooperative departure scheduling](https://github.com/yonnastgetahun/cooperative_traffic_research/blob/main/docs/EXPERIMENT_003_DEPARTURE_SCHEDULING_ROADMAP.md) is formally on the roadmap. Future comparisons should distinguish routing alone, voluntary departure timing alone, and both together; include predeparture delay in door-to-door time and respect individual deadlines/eligibility. Not yet implemented.

## 6. Research integrity and execution controls
- Preserve existing artifacts and historical workflows; do not overwrite earlier results.
- Keep smoke tests, scenario coverage, predictor accuracy validation and scientific conclusions as **separate milestone gates**.
- Pin and record SUMO version/container digest, repository commit and immutable input hashes for future reproducibility.
- Clearly label the limits of synthetic simulations; no physical-world safety, operational or traffic-network performance claim is supported yet.
- This report records progress and evidence. It does not authorize additional algorithm changes beyond the already approved predictor-validation instrumentation scope.

## 7. Key GitHub evidence
- [Experiment 001 nine-case reproducibility](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40066595847)
- [Initial paired cooperative smoke test](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40067497552)
- [Five-penalty sweep](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40068411813)
- [Vehicle-level diagnostics](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40069352997)
- [Road-level diagnostics](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40070768551)
- [Time-aware routing smoke test](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40071388202)
- [Three-regime coverage backfill](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40072443736)
- [Successful predictor-instrumentation smoke test](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40073685024)

---
**Overall assessment:** We progressed from congestion calibration to a reproducible three-regime comparison and functioning predictor-observation instrumentation. The results currently favor independent routing. The highest-value next step is to validate the *actual* congestion-aware predictor, not to claim a cooperative-routing benefit or blindly retune penalties.
