# We tested whether a route change's impact on *everyone else* could be predicted. It could not—yet.

**Cooperative Traffic Research · Experiment 007 Test A · November 2026**

## The finding

A cooperative traffic system needs more than good predictions of how long an individual trip will take. It must estimate whether moving one vehicle to a different road will help—or delay—other drivers.

In the next step of our [open-source research](../README.md), we tested exactly that question in a synthetic 10x10 SUMO road network with 1,000 simulated vehicles under high congestion.

We ran **30 successful simulations** across five independent demand seeds. In each seed, we kept everyone else's planned route unchanged while changing one eligible vehicle's route in four preselected probes. We also tested a combined two-route change.

The forecast predicted the direction of the actual impact on other vehicles correctly in only **8 of 20 probes (40%)**. Our scientific protocol required **at least 60%** to proceed. All 20 probes had material realized impacts under the preregistered criterion.

The estimated effects ranged roughly **−3 to +13.5 network-seconds**. Actual effects ranged **−3,777 to +4,328 network-seconds**. A *network-second* here is one second of travel-time change **summed across drivers**, not that many seconds for one driver. Five probes even predicted **zero impact** while producing a materially nonzero effect.

When two routes were changed together, their actual combined network impact also differed substantially from simply adding their separately measured impacts—evidence that network interactions cannot be assumed additive.

## Why this matters

The experiment was deliberately divided into two scientific tests:

- **Test A:** Can a frozen model predict how individual route changes affect the rest of the network?
- **Test B:** If so, does coordinating routes based on those predictions actually improve whole-network travel time compared with a comparably informed independent routing policy, while respecting individual fairness?

**Test A failed its frozen progression rule. Test B was correctly not executed.**

This is **NO-GO for the particular assigned-demand marginal-externality model**, not evidence that cooperative traffic routing is impossible or inferior to contemporary navigation systems. We have not established whether a better physically grounded estimator—one that captures junction queues, spillovers, and interactions among route assignments—could succeed.

The model used advance-announced demand and fixed simulated compliance assumptions. These results are not observations of actual drivers, smartphone navigation users, or autonomous fleets. No subjective comfort or calmness was evaluated.

## Read the reproducible scientific record

- [Complete Experiment 007 Test A final scientific report](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md)
- [Frozen pre-execution protocol](EXPERIMENT_007_FROZEN_PROTOCOL_V1.md)
- [All twenty selected singleton route perturbations](results/exp007_test_a_probes.csv)
- [Five two-swap bundle interactions](results/exp007_test_a_bundles.csv)
- [Original 30-simulation execution](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833) (five probe jobs passed; the original *aggregation runner* lacked a SUMO Python dependency)
- [Successful scientific aggregation using the original, unchanged archives](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41381425091)
- [Original scenario artifacts and aggregate JSON](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md#original-scientific-design-and-provenance) (GitHub Actions artifact retention is limited)

## Next question

**Can we validate a prospective model of network interactions that is accurate enough for a fair, genuinely collective routing experiment?**

That is an open hypothesis. The result instructs us not to claim a network-wide optimization benefit merely because a planner produces different routes or improved chosen-route forecasts.

---
*Experiment 007 remains a conditional study stopped at its prespecified Test A gate. No Test B policy efficacy or fairness conclusion is available. Visual publication drafts require approval before sharing on LinkedIn or X.*
