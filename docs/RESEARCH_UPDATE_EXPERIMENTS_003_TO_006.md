# We corrected a consequential routing flaw. But cooperation still didn't win.

**Cooperative Traffic Research · Experiments 003–006 · November 2026**

This page is the **single starting point** for the latest research update shared on LinkedIn and X. It explains the findings in plain language and links to the frozen scientific reports, methods and reproducible simulation evidence.

> **What we learned:** Improving traffic forecasts did not automatically improve collective routing. Correcting a timing inconsistency substantially improved one cooperative policy. But against independent routing, the corrected policy showed **no statistically established network-wide advantage**, and a substantial share of drivers experienced worse journeys.

## The story in four experiments

| Experiment | Question | What happened |
|---|---|---|
| **003 · Improve prediction** | Can we better estimate when vehicles enter roads along their chosen routes? | A frozen cumulative timing correction reduced chosen-route prediction MAE by **34.2%**, **46.3%**, and **51.3%** across high, moderate and lower congestion on fresh confirmatory simulation data. |
| **004 · Use those predictions** | Does better prediction improve the cooperative routing decisions? | **No, for this tested policy.** Under high congestion, calibrated cooperative D increased average trip duration by **18.53 seconds** versus the same stateful routing adapter without calibration (C); **56.7%** of matched drivers were slower and **40.0%** were faster. Policy D received **NO-GO**. |
| **005 · Correct the mechanism** | Was a mismatch between forecast and traffic-assignment clocks consequential? | **Yes, within the tested model.** Aligning the clock used to register assigned traffic demand made corrected cooperative E **20.13 seconds faster per trip** than the flawed calibrated D policy under high congestion (95% paired seed-level CI **16.74–23.53 seconds**). This establishes an improvement *relative to D*, **not** independent routing. |
| **006 · Test against independent routing** | Does corrected E beat independent A on matched fresh demand without unacceptable individual harm? | **Not established.** Under high congestion, E's mean advantage was **0.24 seconds** (95% paired seed-level CI **−1.91 to +2.40 seconds**), so superiority was **inconclusive**. **27.98%** of matched drivers had journeys **more than 30 seconds longer** under E; the predeclared fairness safeguard failed. |

**All vehicles completed their trips** in the Experiment 004–006 tested scenarios, so the reported high-congestion travel-time results were not driven by excluding unfinished trips.

### What changed in Experiment 005?

The earlier calibrated routing policy was using two different notions of time. It evaluated possible successor roads using a **calibrated forecast arrival clock**, but it recorded planned occupancy after assigning a route using an **uncalibrated free-flow clock**. Experiment 005 changed only the assignment-update clock on the selected route, holding the stateful candidate search, coefficients, demand and guardrails fixed.

That intervention significantly improved the original policy's results. **It did not mean coordination had become better than an independent-routing baseline.** That separate question motivated Experiment 006.

### What Experiment 006 means

In the fresh-seed comparison, independent A and cooperative E produced nearly equal average trip durations under high congestion, with uncertainty extending in both directions. Although some drivers benefited, **2,798 of 10,000** matched high-congestion drivers experienced **more than 30 seconds** of additional trip time under E.

A read-only analysis of the original archives found that, among those 2,798 drivers, additional trip duration averaged **72.47 seconds**, including **57.17 seconds** of additional recorded SUMO waiting. Most did **not** take nominally longer routes: **2,792** had the same calculated free-flow route distance and time, while **882** kept the exact same road-edge sequence. These findings support a possible role for queue interaction and congestion redistribution, **without identifying a specific causal bottleneck**.

**The scientific distinction:** Fixing a routing algorithm is not the same as discovering an effective coordination mechanism.

## Important limitations

These are controlled **SUMO simulations**, not real-world driving or driver behavior observations. The experiments used a **synthetic 10×10 grid**, **1,000 vehicles per simulation**, and congestion regimes defined by the same demand departing over **200, 600 or 1,200 seconds**. The confirmatory routing comparisons used paired demand and independent simulation seeds within each experiment.

**The Experiment 006 baseline A used nominal free-flow shortest-path routing.** It was **not** a modern, independently traffic-aware navigation service, dynamic user equilibrium, or a benchmark for actual Google Maps, Waze or Apple Maps. We cannot conclude that cooperation universally fails—or that our corrected E policy can outperform those applications.

Experiment 005 and Experiment 006 used **different fresh seed cohorts**. Their effects must be interpreted within the paired policy contrasts actually tested, not combined as though they were a single paired experiment.

The 30-second individual-delay threshold was a **prespecified Experiment 006 research safeguard**, not a measured universal traveler preference. Partial voluntary participation, compliance, departure coordination, diverse topology, and real-world safety remain untested.

## Read the science and reproduce the work

**Scientific reports**

1. [Experiment 003 — Confirmatory timing-calibration results](EXPERIMENT_003_CONFIRMATORY_RESULTS.md)
2. [Experiment 004 — Four-arm routing results and NO-GO decision](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md)
3. [Experiment 005 — Clock-alignment intervention, relative GO versus D](EXPERIMENT_005_CLOCK_ALIGNMENT_RESULTS.md)
4. [Experiment 006 — Corrected cooperation versus independent A and fairness results](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md)
5. [Experiment 006 — Archived severe-delay mechanism investigation](EXPERIMENT_006_ARCHIVED_SEVERE_HARM_MECHANISM_ANALYSIS.md)

**Original execution and data**

- [Experiment 004 — 120 scenario-arm execution](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41023721390)
- [Experiment 005 — Successfully completed fresh paired D/E study](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41172516513)
- [Experiment 006 — Successfully completed fresh paired A/E study](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41185989951)
- [Experiment 005 — Permanent seed-level summary](results/exp005_clock_alignment_seed_summary.csv)
- [Experiment 006 — Permanent seed-level summary](results/exp006_a_vs_e_seed_level.csv)
- [Original project overview and source code](../README.md)

GitHub Actions archives have limited retention; the scientific reports and permanent seed-level summaries preserve the central findings.

## Where the research goes next

Our central research question remains open:

**Under which conditions—and with what kind of coordination—can road traffic operate more efficiently without imposing unacceptable burdens on individual drivers?**

We are broadening the mechanism assessment beyond repeated adjustments to one routing algorithm, including **system-externality-aware / system-optimal routing**, **voluntary departure or bottleneck-entry coordination**, and **traffic-flow control**. Throughout, we will keep realized individual harm and fairness in the evaluation. **Quality of journey experience is a deferred research dimension**, not the focus of the next experiment.

[Read the foundational research-direction synthesis](FOUNDATIONAL_SCIENTIFIC_SYNTHESIS_AND_RESEARCH_DIRECTIONS_2026-10-31.md).

---

*Cooperative Traffic Research is an exploratory, open-source investigation. This page summarizes documented simulation findings; it does not claim real-world deployment readiness or superiority to existing navigation services.*
