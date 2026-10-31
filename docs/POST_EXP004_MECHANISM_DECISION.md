# Post-Experiment 004 mechanism decision — after completed Experiment 005

**Scientific evidence checkpoint:** October 30, 2026.  
**Original policy D remains NO-GO. Clock-aligned policy E receives GO relative to D under the prespecified Experiment 005 high-congestion comparison.** The broader cooperative-routing benefit relative to independent routing remains **unresolved**.

## What we now know

1. **Experiment 003 confirmed better chosen-route timing forecasts** under independent demand. It did not independently establish counterfactual route-ranking accuracy or collective welfare.
2. **Experiment 004 found that injecting that calibration into stateful cooperative routing increased network travel times** in high congestion (D − C +18.5282s, 95% seed-level CI [+14.4698,+22.5866]s). D was NO-GO; 100% trip completion and fairness/tail harms were verified.
3. **The read-only Experiment 004 decomposition** of 60 D/C archives found that switched routes were generally geometrically equivalent in nominal free flow, route assignments became more concentrated, and unchanged-route drivers experienced additional delays. This was evidence for, but not proof of, network redistribution and clock misalignment.
4. **Experiment 005 isolated one prespecified implementation change:** update already-assigned occupancy time bins on the calibrated chosen-route replay clock rather than on the original free-flow clock. The same stateful calibrated path search, calibrated coefficients, demand and detour constraints were held constant in D versus E.
5. **On ten new paired seeds per regime (3401–3410), E improved high-congestion mean travel time by +20.1317s D−E, 95% CI [+16.7378,+23.5256]s**, reducing mean seed-level p90 duration by 50.1s. High-congestion assigned-edge Gini was lower by 0.04664 in E, 57.4% of drivers benefited and 39.14% were harmed; all trips completed. Structured safety/collision fields were present and reported zero in 60 arm outcomes. Prespecified GO conditions passed. [Full report](EXPERIMENT_005_CLOCK_ALIGNMENT_RESULTS.md), [successful run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41172516513).

## Competing mechanisms: current evidence status

| Candidate explanation | Status after Experiment 005 |
|---|---|
| Original forecast-vs-assignment clock inconsistency | **Causally consequential within the tested algorithm**: changing only the chosen-route post-assignment update clock improves network mean and tail under fresh paired demand. |
| Congestion displacement / network spillovers | **Supported but mediator not isolated**: E reduces assigned-road-load concentration and benefits unchanged-route drivers; the link to specific physical bottlenecks is unmeasured. |
| Geometrically longer routes | **Disfavored as primary explanation of Exp004 harm** by the frozen archive reanalysis. |
| Counterfactual candidate-route prediction rank validity | **Unresolved**: chosen-route forecast validation does not establish alternate-route ranking correctness. |
| Stateful search labels, path-dependent time-bin effects | **Unresolved beyond fixed search control**: E and D use the same code but their assignment histories diverge. |
| Objective/fairness misalignment vs independently optimized routing | **Unresolved**: neither Exp004 nor Exp005 demonstrates E's superiority over a paired independent baseline A. |

**Causal scope:** This supports an intervention effect in a synthetic SUMO network with all planned trips known in advance. It does **not** show clock mismatch was the *only* cause of the original D failure or that route-assignment Gini mediated the effect. No real-world safety/behavior or autonomous coordination outcome follows.

## One highest-value next scientific comparison

The immediate unresolved question is now **whether clock-aligned policy E is better than capable independent routing A on identical fresh network/demand seeds**. A narrow paired E-versus-A study (with optional retained D anchor if scientifically justified) should explicitly predefine mean trip-time, completion, p90 and matched-driver fairness, and should not assume improvement based on comparing different seed cohorts. No new seeds have been selected for this **future** study, and no additional simulations are authorized or launched as part of this decision.

Preserve previously approved vehicle-volume, network-size and topology complexity studies as distinct later dimensions; preserve voluntary participation and departure-time coordination as untested research questions. Do not start another broad qualification program.

**Scientific state:** A specific causal mechanism was found and improved, but network-level cooperative advantage over independent behavior has not yet been established.
