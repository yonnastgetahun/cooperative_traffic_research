# Experiment 004 — Prespecified network-outcome cohort manifest v0.1

**Status:** Frozen prospective cohort definition, committed before any Experiment 004 network-outcome simulation.

**Fresh demand seeds:** `3301,3302,3303,3304,3305,3306,3307,3308,3309,3310`. These do not overlap with M3 held-out 3101–3110, Experiment 003 development 2201–2210, Experiment 003 confirmatory 3201–3210, or inspected development 2101.

**Regimes:** 200 seconds (primary), 600 and 1200 seconds (secondary). Each demand instance contains 1,000 vehicles on the same 10×10 synthetic road network.

**Arms:** A independent, B original time-aware cooperative, C ordinal-aware adapter with calibration off, D same adapter with frozen Experiment 003 calibration on. Total: 10 seeds × 3 regimes × 4 arms = **120 scenario-arm executions**, paired within each seed/window.

**Frozen calibration parameters:** 200s (4.053135104279146,11.524898884412591), 600s (1.7868471223107676,3.9515691107998387), 1200s (1.8903085164618962,2.6820862794976956), respectively offset and per-edge seconds.

**Primary estimand:** Mean of ten seed-level paired differences `mean_completed_trip_time_C - mean_completed_trip_time_D` at 200s; positive means D is faster. Report two-sided 95% Student-t CI. Primary scientific support requires the CI lower bound above zero **and** no material completion-rate degradation. This is conditional on reporting all incompletions; if completion differs, also report all-departure censored sensitivity metrics before interpreting a completed-trip mean.

**Secondary:** D vs C at 600s/1200s, C vs B, D vs B, D vs A, 90th percentile travel time, completion, throughput, fairness and exceptions. All comparisons paired by seed. No claim of improvement over independent routing unless D vs A independently supports it.

**Scientific code boundary:** Use original frozen Experiment 001/002 routing definitions for A and B. C and D must use one identical, fixed stateful-search implementation and occupancy update rule, differing only in the calibration coefficients. Exact code revision and route-policy implementation provenance must be pinned in the run manifest before simulation dispatch. No future SUMO observations may influence any route choice.

**No rerandomization or replacement of failed seeds.** Preserve failed attempt evidence and report missing/ineligible arms explicitly. No Experiment 004 network outcomes have yet been observed.
