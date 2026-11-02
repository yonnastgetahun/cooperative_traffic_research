# Experiment 007 — Frozen prospective scientific protocol v1

**Freeze date:** 2026-11-01. **Authorized:** User approved end-to-end execution of the [two-test prospective design](EXPERIMENT_007_TWO_TEST_PROSPECTIVE_SCIENTIFIC_DESIGN_NOTE.md). **Scope:** exactly the high-congestion 200-second regime; no subjective experience endpoints; no social publishing without a new explicit approval.

## Main causal claims and nonclaims

Test A evaluates **precomputed marginal externality predictions**, not a successful optimizer. Test B, only after the specified Test A gate, evaluates **realized whole-network effects** of a frozen cooperative route assignment relative to an equally informed independent traffic-aware assignment. Failure in either must be reported unchanged. This study does not demonstrate optimality, real-world vehicle benefits or human consent.

## Frozen scenario, information and source

- 10x10 SUMO grid from \`netgenerate --grid --grid.number 10 --grid.length 200\`, 1,000 vehicles, 200-second departure window; frozen original \`fixed_demand_v01.py\` at \`be2e8d27c78c8b6de4891115d6d951edc877ac6e\`. SUMO container pinned to \`ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb\`.
- Fresh probe seeds **4101–4105**, prospective policy seeds **4201–4210**; development uses **2101 only** and/or unit fixtures. Seeds not reused between probe and policy confirmation. No adaptive selection based on held-out SUMO results.
- 50% nominal eligible opt-ins: deterministic even vehicle indices (500 of 1,000) under identical roster in both policies. Simulation compliance is 100% by modeling assumption **only**, not demonstrated real-world voluntary participation.
- Both arms know the full frozen announced demand, exact route-intention occupancy, network, vehicle schedule, candidate routes and the same forecast. This is intentionally an **idealized equal-information pretrip** comparator, not a claim to beat existing navigation software.
- Identical prospective network forecast based on fixed time-binned assigned-route edge counts: 30-second bins, route ordinal entry clock \`scheduled_departure + cumulative_edge_freeflow_before_entry + 4.053135104279146 + 11.524898884412591 * ordinal\` (index 0 at first edge). For edge-bin demand q, edge time model \`ff*(1+q/capacity_proxy)\`, \`capacity_proxy=max(1,length*lane_count/7.5)\`; predicted total \`sum(ff*(q+q*q/cap))\`. The assumed pressure coefficient is **1.0**. This is a simplified *assigned-demand* forecast, **not** calibrated physical occupancy/queue delay or a known accurate externality estimator. Predictions never access future SUMO output.
- Candidate route set (identical for I/S): nominal fastest edge-graph shortest route plus up to three deterministic edge-weight-perturbed shortest routes (weight \`ff*(1+0.25*stable_hash(vehicle, variant, edge))\`, three variant salts); connected legal passenger-edge paths, deterministic, no loops. Exclude candidates with >min(30s, 10% nominal freeflow baseline) extra nominal freeflow time or >15% extra nominal distance. If alternatives unavailable, that driver cannot change route.
- A fixed initial common traffic-aware full-demand assignment (one chronological sweep of own-cost greed under the shared prospective model) supplies the initial route-intention map. Nonparticipants retain this assignment under both policies. One identical subsequent chronological sweep of eligible drivers is evaluated under two objectives: **I** minimize candidate predicted *own* elapsed route cost, **S** minimize *total* predicted network assigned-edge travel cost. Both update occupancy only after complete route selection and reuse the same calibrated clock. Candidates obey the identical prospective predicted-own-burden cap of +30s relative to their initial route (both arms); the S policy does not access any extra observation or horizon. Keep route generation procedures/candidate set and number of optimization passes equal. Report computational work differences if any.
- Observe \`arrival - scheduled_departure\` in **both** arms, including insertion delay. Require matching scheduled demand and no change to departures. Report SUMO \`duration\` separately for comparability with Experiments 001–006. \`waitingTime\` and \`timeLoss\` are diagnostics, not additive extra costs.

## Test A: prospective route-perturbation screen

For each of five independent seeds, create baseline I, four predetermined distinct eligible individual route-swap probes selected **only from predicted** externality ranking (lowest, highest, closest to zero, middle distinct ranked option, preserving distinct driver IDs), and a two-swap bundle of the first two. Baseline and perturbation routes otherwise identical; same demand, departures, SUMO seed. **Six runs per seed, 30 runs**. If fewer than four valid distinct driver probes, mark a design-validity failure and withhold Test B.

For each individual probe record:
- predicted and realized \`delta_all = sum(all arrival - scheduled_departure) difference\`, \`delta_self\`, \`delta_external=delta_all-delta_self\`, with **negative meaning benefit**;
- absolute errors, signed calibration errors and sign agreement for **materially nonzero** realized effects;
- own-time-only **zero externality** benchmark and count of predicted network benefits that actually harm the network;
- bundle predicted joint change, realized joint change, and discrepancy from sum of corresponding isolated changes.

**Noise/materiality threshold:** realized absolute externality >= **10 network-seconds**; other effects classed "indeterminate near zero." No correlation tests using 20 probes as independent random replications. Estimate sign agreement by seed and report all five seeds separately.

**Advance gate to B:** each of all five seeds yields complete, consistent six-run archives; at least **10** materially nonzero externality observations; at least **60% sign concordance** among material probes overall; no systematic data leakage/clock or route integrity failure; at least one bundle with nonzero observed interaction to quantify. This gate is a **diagnostic minimum** not proof of reliable externality predictions. If it fails, **NO-GO for mechanism-screen progression** and stop automatic Test B; do not alter thresholds or reselect probes after observing results. If no bundle interaction detected, explicitly report that and still proceed if other gates pass (lack of observed interaction is not evidence the model is additive).

## Test B: whole-policy paired efficacy and fairness

On **10 fresh independent seeds 4201–4210**, compare **I versus S** with same OD/departures/eligible drivers/information and whole-route assignment process, two SUMO arms per seed (**20 runs**); B automatically executes only if A gate passes. The independent **seed** is the inferential unit; 10,000 matched vehicle identities are repeated nested measurements, not 10,000 independent samples.

**Primary:** seed-paired \`mean_scheduled_to_arrival_I - mean_scheduled_to_arrival_S\` (positive favors S). Predeclared practical minimum mean benefit **2.0 seconds per driver**, while statistical evidence requires two-sided 95% t-interval **lower bound >0** and point estimate **>=2.0s**. Ten seeds are a bounded replication budget and **may be underpowered**; if interval crosses zero, call inconclusive and do not extend on the observed results.

**Fairness joint decision gates:** all 1,000 trips must complete in each arm with valid matched identities; across 10,000 matched drivers no more than **10%** may incur **>30.0s additional** realized scheduled-to-arrival time under S (historical Exp006 continuity rule, selected here prospectively as a conservative study-specific gate); separately **nonparticipants** must also have **<=10%** >30s harm; less than/equal **50%** of all drivers may have strictly longer realized time in S. Report p90/p95 individual harm, OD effects if adequately powered, participant/nonparticipant means, waiting, insertion delay, changed routes, and collision/emergency statistics where available. No claims about real-road safety based on SUMO zeros. If completion fails, do not calculate completed-only means as definitive all-demand causal effects.

**Joint conclusion:** GO for this frozen policy only if Test A gate passes, B primary and practical targets pass, all fairness/exception checks are acceptable; otherwise NO-GO or INCONCLUSIVE based on failure. In any case publish negative results. Test A success never constitutes Test B success; Test B success is not evidence of global optimality.

## Integrity and stopping rules

- Freeze before running seed 4101 or 4201. The frozen protocol **may not be revised post-outcome**. Preserve source commit SHAs, all route/tripinfo/manifest/diagnostics, aggregate per-seed CSV and full report.
- Before evaluation, run unit and **development-only seed 2101** tests for route legality, identical input sets, clock consistency, no forecast leakage, seed matching, parsing \`arrival-depart\`, and nonparticipant route invariance. Fix code defects without changing the scientific decision rules; document such fixes and rerun development verification.
- No broad parameter tuning, medium/low regimes, topology scaling, departure shifts, automated driving control, or comfort/calming studies under this experiment.
- The experiment may **stop early for invalid measurement or Test A gate failure**, with a published full explanation and original artifacts. No simulations for B if the gate fails.

**Note:** This is an intentionally minimal conditional causal study. The fixed numerical gates are reasoned experiment design choices, not estimates of human consent or real-world harm tolerance. **Public social-media distribution still requires separate review and approval of actual visual assets and copy.**
