# Post-Experiment 004 mechanism investigation — first archived observations

**Date:** 2026-10-30  
**Status:** Exploratory, read-only analysis. No new mechanism has been proven.  
**Companion:** [Evidence inventory](POST_EXP004_EVIDENCE_INVENTORY.md).  
**Primary immutable finding:** C minus D mean trip duration = -18.5282s in 200s regime (95% seed-level CI [-22.5866,-14.4698]); tested D policy is NO-GO.

## Core question

Experiment 003 reduced **chosen-route road-entry timing MAE**, but this does not verify **counterfactual candidate-route rank accuracy** or that the routing policy minimizes a social objective. Experiment 004 shows that turning calibration on (D) within the same stateful adapter (C) changed route assignments and worsened high-congestion outcomes.

## Source-level decision mechanism (verified in repository code)

1. `prospective_search_adapter_v01.py` carries search state `(edge, ordinal, lookup time-bin)` and uses `entry = departure + cost + offset_s + per_edge_s * next_ordinal` to select the occupancy bucket for a successor.
2. The next search score increases by `freeflow + occupancy surcharge + junction proxy`; the calibration correction **shifts occupancy lookup time**, rather than simply adding the Experiment 003 correction to every edge's path cost.
3. `time_aware.py` uses `clock = depart` and then `clock += freeflow(edge)` for post-assignment occupancy updates, irrespective of D's calibrated candidate lookup clock. **Search and allocation clocks are structurally different.**
4. The search surcharge is based on **previously assigned vehicle counts per edge/time-bin divided by a capacity proxy**; this is not measured physical queue/occupancy. Candidate acceptance uses **free-flow** detour/distance guardrails. Neither the code's path score nor the guardrail explicitly optimizes aggregate realized network travel time or protects against realized queue-induced delays.
5. C and D share the same search implementation and occupancy-update rule; D changes calibration coefficients. The old B search and the C zero-calibration adapter were previously shown **not equivalent**, so B/D cannot isolate calibration.

These are **implementation facts**, not proof that the clock mismatch or route-search behavior caused the adverse result. In particular, historical traces do not show which calibrated bin lookups changed candidate ranking.

## First raw-archive matched-driver examples (illustrative only)

The following three C/D ZIP pairs were opened. Vehicle IDs were matched, and the C/D `trips.xml` bytes matched within each example. Positive D-minus-C values mean longer travel time under calibration.

| Window / seed | C/D routes different | Changed-route D-C mean | Same-route D-C mean | Overall D-C mean | Changed-route mean waiting-time shift |
|---|---:|---:|---:|---:|---:|
| 200s / 3308 | 701 / 1000 | +29.974 s (n=701) | +14.268 s (n=299) | +25.278 s | +22.682 s |
| 600s / 3301 | 559 / 1000 | +5.009 s (n=559) | +1.073 s (n=441) | +3.273 s | +3.572 s |
| 1200s / 3303 | 428 / 1000 | -0.453 s (n=428) | +0.306 s (n=572) | -0.019 s | -0.173 s |

**Interpretation:** in the observed high-congestion example, duration and waiting penalties extend even to drivers whose C/D routes were identical. This is **consistent with network-mediated spillovers**, but cannot assign the change to a particular edge, bottleneck or route switch without more evidence. The three examples were selected for archive accessibility and are **not a population sample** or substitute for the complete 10-seed analysis. Seed 3308 has one of the most adverse high-congestion outcomes; do not present its +25.278s as the regime average (+18.5282s).

**Route geometry in the sampled C/D pairs:** for 200s/3308, 687 of the 701 switched routes had exactly the same audited free-flow duration and distance as the alternative; all 701 retained the same number of edges. The 600s/3301 and 1200s/3303 cases likewise had 553/559 and 423/428 switched routes with exactly the same audited free-flow duration and distance, respectively. **Thus these examples do not suggest that the negative outcomes were simply caused by systematically longer nominal routes.** This does not rule out small geometric differences, varying turn/junction exposure, or broader-seed detour effects.

## Which competing explanations can be distinguished today?

| Hypothesis | Evidence currently supporting consideration | Evidence still missing / contradictory | Status |
|---|---|---|---|
| Candidate-route prediction/ranking invalidity | Exp003 validation covers chosen routes only; no candidate-level rank ground truth | All rejected candidate costs and realized counterfactual travel times absent | **Open; not identifiable from current archives** |
| Stateful search / forecast-clock behavior | C/D use same ordinal-aware adapter; D shifts occupancy lookup bins; B/C non-equivalent | Exact historical candidate label/lookup transitions absent | **Source-level mechanism present; effect unquantified** |
| Occupancy feedback misalignment | Search uses calibrated time-bin; update counts assigned vehicles on free-flow bin | No decision-time per-bin occupancy-read trace; no isolated matched-clock intervention | **Source-level mismatch present; causal contribution unknown** |
| Congestion displacement and spillover | Large C/D route differences across all regimes; same-route drivers delayed in high-congestion sample | No archived physical edge-time load/delay data identified in sampled ZIPs | **Observationally consistent, not causally identified** |
| Social-objective and fairness misalignment | Local proxy path-cost optimization; high-congestion overall/p90 harm and 56.7% harmed | No tested system-optimal objective or participant incentives; exact OD cohorts nearly all singleton | **Objective mismatch evident in implementation; impact unisolated** |

## Additional descriptive updates from archived audit

- Every one of the 120 audit records has `safety.emergencyBraking="0"`, `safety.emergencyStops="0"`, and `safety.collisions="0"`. This closes the **numeric structured-field aggregation** omission from the final report, not any real-world safety question.
- The exact within-seed OD grouping has 9,930 singleton cohorts out of 9,965 cohort records per regime (99.65%), so fine-grained OD-cohort effect ranking would mostly rank individuals. Prefer predeclared spatial aggregation if archived origins/destinations suffice.

## Highest-information next read-only analysis

Compute a **30-seed-window C/D matched route-versus-outcome decomposition**, where ten seeds per regime remain the independent statistical units. For each seed classify switched versus unchanged route sequences, quantify:
- mean/median D-minus-C trip duration and waiting shifts by subgroup;
- route geometric cost, overlap and assignment-load differences;
- proportions helped/harmed by subgroup and p90 impacts;
- whether the same-route spillover pattern persists consistently across seeds and fades as congestion declines.

This will test whether the first example's observed spillover association generalizes and whether route length is a material explanation. It cannot alone establish the causal contribution of the forecast-clock mismatch; only after this read-only analysis should we decide whether a **single** controlled clock-alignment intervention or another discriminating experiment is warranted.

**No new simulations, calibration fitting, policy retuning, or readiness program have been initiated.**

## Full 60-archive C/D decomposition (completed)

The full 60-archive, 30 matched seed-window C/D comparison is now documented in [the archived decomposition results](POST_EXP004_FULL_ARCHIVE_DECOMPOSITION_RESULTS.md). It confirms positive high-congestion D−C delay for both changed- and unchanged-route drivers, nearly identical nominal free-flow route geometry in 98% of changed routes, and greater concentration of assigned vehicles by road edge under D. These are strong descriptive findings, not a proven causal explanation; see the linked report for ten-seed intervals, all 30 seed-level rows, uncertainties, and a single future discriminating clock-alignment test proposal.

