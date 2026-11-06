# Cooperative Traffic Research — T1 Cooperative Departure Timing
## Approved scientific direction and prospective experiment concept

**Date:** November 5, 2026  
**Decision:** DIRECTION APPROVED — NOT A FROZEN PROTOCOL  
**Status:** Research direction approved for prospective design and feasibility review. This document does **not** authorize code implementation, SUMO experiments, use of reserved seed cohorts, alteration of prior estimator/policy gates, or external publication.  
**Working label:** T1 — Voluntary Cooperative Departure Timing vs. Independent Traffic-Aware Timing (post-C1 concept).

## 1. Why we are doing this experiment

The foundational question is whether today's human-driven vehicles can achieve some collective transportation benefits potentially available to coordinated future autonomous fleets: **can voluntary shared decisions improve total traffic outcomes over equally informed independent decisions, without unacceptable harm to individual participants or nonparticipants?**

The experiment is motivated by *negative as well as positive* evidence:

- Experiments 001–002: the initial cooperative-routing variants did not beat the tested independent assignments in the synthetic 10×10 network.
- Experiments 003–004: chosen-route timing prediction improved on independent evaluation, yet the calibrated cooperative routing policy D worsened high-congestion trip durations by **18.53 s/driver** versus the otherwise comparable adapter C.
- Experiments 005–006: correcting a consequential forecast/occupancy clock mismatch improved E relative to flawed D; versus independent nominal-free-flow A, E's high-congestion advantage was **+0.2429 s (A−E; 95% seed-level CI −1.9120 to +2.3978 s)**, inconclusive. **27.98%** of matched drivers incurred >30 s additional realized delay, violating the experiment's prespecified severe-harm gate. A was **not** a modern traffic-aware independent navigation comparator.
- Experiment 007 Test A: the original route-swap externality estimator passed only **8/20** directional matches against a **60%** frozen gate. Conditional cooperative policy Test B did not run.
- E1-v2 D1: connection-aware estimator engineering completed, but **DEVELOPMENT_NOT_QUALIFIED** (5/16 sign matches; MAE 1,478.5625 network-s versus 1,478.0625 for zero-externality B0). Independent E1-v2 validation and policy Test B remain unopened.
- F0–F5 and the four-arm vehicle replay: large route-dependent effects involved changed stopped-time exposure and nonadditive route-bundle interactions; neither investigation identified a unique physical causal bottleneck.
- C1: an E3 priority reversal materially changed the network-wide *relative effect* of a frozen single-driver route swap on two retrospectively selected seeds (interaction Ψ = **−7,578** and **−19,980 network-s**), **while making absolute network cost worse under both assignments in each seed**. C1 identifies case-level physical effect modification, not a beneficial junction design, independently predictive externality model, or successful cooperative routing.

These findings caution against continuing to revise E1 solely because it already exists. **The next scientific question is whether timing coordination—rather than rerouting—can create incremental collective value beyond equal traffic information and individual timing flexibility.** This is a different mechanism, not an attempt to rescue failed policies.

Sources: [C1 final scientific report](POST_EXP007_C1_E3_CONTROLLED_FINAL_SCIENTIFIC_REPORT_2026-11-05.md), [Experiment 007 Test A](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md), [E1-v2 D1 audit](POST_EXP007_E1_V2_D1_FINAL_DEVELOPMENT_AUDIT_2026-11-04.md), [Experiment 006](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md), [Experiment 004](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md).

## 2. What exactly we want to discover

**Primary scientific question:** When equally informed drivers have identical opportunities to change departure time, can a *voluntary jointly coordinated* schedule reduce **total desired-departure-to-arrival time across all drivers**, compared with a credible independently optimized traffic-aware schedule, while meeting individual and nonparticipant harm safeguards?

Separate three mechanisms:
1. **Information benefit:** improved decisions from better traffic forecasts.
2. **Individual flexibility benefit:** improved outcomes simply because drivers can shift departure times.
3. **Coordination benefit:** additional outcomes from jointly choosing compatible timing decisions.

The primary estimand must isolate (3). Merely spreading a 200-second demand window over more time does **not** establish cooperation, nor is less *in-network* waiting by itself a gain if drivers wait longer before leaving.

## 3. Hypotheses (not established claims)

- **H1 / primary:** Compared with a properly implemented, equally informed independent-timing policy B, cooperative policy C reduces total desired-departure-to-arrival elapsed time in the high-congestion setting, by a prospectively defined meaningful amount, while passing a separately prespecified fairness safeguard.
- **H0:** C does not yield a meaningful improvement over B once predeparture time and all original drivers are included.
- **H2 / mechanism:** C reduces synchronized entry demand at predeclared bottlenecks and associated queuing.
- **H3 / externalities:** C changes outcomes for nonparticipants, who do not change their own planned departure times.
- **H4 / fairness:** Benefits, if present, can be uneven; any aggregate gain must be reported with severe individual harms and nonparticipant effects.

Outcome-driven adjustments to H1, the harm rules, or the comparison baseline are prohibited.

## 4. Experiment environment and invariants

**Proposed starting environment:** existing synthetic 10×10 SUMO road network, high-congestion scenario, 1,000 drivers, original *preferred* departure times distributed over 200 seconds. Keep original OD demand, vehicle identities, road geometry, traffic rules, vehicle behaviors and simulator configuration identical across matched arms.

Use one **common, capable independent traffic-aware route generator** to assign planned routes, then freeze each driver's route across A, B and C for the timing-only causal comparison. Route assignment construction, traffic information, prediction model, capacity assumptions and permissible timing choices must be documented and equal across B/C; neither may inspect realized future SUMO outcomes or otherwise have oracle information.

This is intentionally a **timing-policy experiment conditional on fixed shared routes**, not a claim of superiority over contemporary navigation systems that dynamically change routes as well as departure times.

## 5. Three matched policies

| Arm | Policy | Purpose |
|---|---|---|
| **A** | No timing intervention: all original preferred departures retained | Baseline demand and congestion |
| **B** | Independent traffic-aware timing: eligible vehicles choose their own bounded departure adjustments to minimize their individual expected cost | Controls for information and individual flexibility; **primary comparator** |
| **C** | Cooperative timing: same eligible vehicles may accept a jointly chosen set of bounded adjustments to reduce total declared network cost | Tests incremental coordination |

**Primary comparison is C versus B**, not C versus A.

B must be credible: specify a fair independent best-response/update scheme with common information and a defensible convergence or iteration stopping rule, including what is observable to drivers. C must not be advantaged with a stronger forecast, different permissible choices, or actual future simulator outcomes. Both optimization objectives, incentives and information permissions require prospective specification. If parity or B quality is not defensible, do not claim a valid C-vs-B test.

## 6. Provisional participation design (to be decided before protocol freeze)

| Variable | Illustrative proposal only |
|---|---|
| Eligible fraction | 50% of 1,000 drivers |
| Eligible timing choices | 0, +10, +20, +30 seconds from preferred departure |
| Maximum shift | 30 seconds later; original departure remains available |
| Nonparticipants | Fixed original preferred departure |
| Route changes between arms | None |
| Acceptance/compliance | Explicitly assumed and modeled; no actual human preferences observed |

Equal eligibility and timing constraints in B and C. A recommendation is an **offer**, not forced behavior. Explicitly define the acceptance rule, utility/compensation assumptions if any, and what happens on refusal before confirmatory testing. The nominal 50%/30-second values are not validated human limits and must not be mistaken for demonstrated willingness to cooperate.

## 7. Primary measurement: do not hide delay outside the network

For every original driver i, let preferred departure be `t_i^*` and observed arrival under policy p be `a_{i,p}`.

**Primary all-driver elapsed cost:**

`C_p = Σ_i (a_{i,p} − t_i^*)`

Count **all 1,000 drivers**, participant and nonparticipant, and any waiting between preferred and actual departure. The principal comparison is `C_B − C_C` (positive favors C). Also report the per-driver mean and the independent seed-level paired variation.

Example: a 20-second departure delay that saves 15 seconds of in-network travel is a **5-second loss**, not a gain.

Prespecify separately any schedule-disutility or deadline penalties beyond elapsed time; never double count waiting already included. Record trip completion, insertion/teleport/exception coverage, and censoring rules. In-network waiting, stopped time, bottleneck approach demand, throughput, discharge and queue patterns are **secondary explanatory metrics**, not substitutes for the all-driver cost.

## 8. Fairness and voluntary-cooperation tests

Calculate matched vehicle-level B/C differences using the original identities. Report:
- Helped, harmed and unchanged shares and the signed magnitude distribution.
- Matched-driver median, p90/p95 additional cost and severe-harm fraction.
- Aggregate and distributional outcomes for **participants vs nonparticipants**, and delayed vs non-delayed drivers.
- Benefits and harms associated with predeparture shift separately from in-network travel-time changes.
- Safety, trip-completion and exception diagnostics available in SUMO; no real-road safety claim.

Set a prospective joint efficiency-plus-fairness decision rule. Experiment 006's >30 s and 10% severe-harm criterion is **historical, not automatically binding**; if adopted here, specify why and freeze it before outcomes. Define what constitutes an actual opt-in in this simulation and keep that separate from real human acceptance.

## 9. Bounded prospective execution plan (not authorized to run)

1. **Design/feasibility only:** write precise B and C decision algorithms, common forecast, bounded choice and acceptance rules, predeclared bottleneck diagnostics, independent-information parity and reproducibility checks.
2. **Development-only rehearsal:** previously inspected *development* data may be used solely for code/instrumentation and feasibility diagnosis; do not call them independent scientific evidence or tune on future confirmatory labels.
3. **Freeze prospective protocol:** input and model source fingerprints, candidate choices, primary effect, meaningful-improvement threshold, seed-level statistical procedure, exception and fairness gates, stopping conditions, cohort selection and capped compute budget.
4. **If separately authorized:** illustrative main confirmatory footprint **10 genuinely new, disjoint demand seeds × three arms = 30 SUMO executions**, plus minimal development-only feasibility checks. Actual budget and power/precision rationale must be settled before freeze.
5. **Audit and publish:** pre-specified paired seed-level analysis, matched-driver and nonparticipant distribution, predeparture vs in-network decomposition, contrary findings, original evidence/checksums and an explicit GO / NO-GO / INCONCLUSIVE verdict.

The independent demand seed, **not the 1,000 driver identities**, is the statistical replication unit. Preserve original Experiment 007, E1-v2 and C1 evidence and negative decisions. Do **not** use previously inspected 6112/6113 as independent confirmation, access reserved E1-v2 **6201–6212** or conditional Test B **6301–6312** cohorts, or revise E1 behavior under this plan.

## 10. Prespecified integrity and stopping conditions

Stop before confirmatory outcomes if:
- The independent B baseline is weak, ill-defined or given inferior information.
- B and C do not share the same original routes, demand, timing options and forecast access.
- Actual versus preferred departures or out-of-network waiting are not accounted for.
- The acceptance/compliance model is undefined, or identity/route/physics invariants fail.
- Event completeness, simulator validity or the predeclared exception handling cannot be verified.

Preserve and report an unfavorable, null or invalid run. Do not retrospectively change eligibility, candidate timing set, objective, seeds, gates or comparator to obtain a positive result.

## 11. What the outcomes would mean

| Result | Scientific learning |
|---|---|
| C beats B on total all-driver elapsed cost, and passes fairness | Evidence for incremental coordination value in this *synthetic, fixed-route, assumed-participation* setting |
| C reduces road waiting but not desired-departure-to-arrival cost | Delay was shifted outside the road rather than eliminated |
| C and B are similar | Individual traffic-aware timing may capture available timing benefits |
| C saves aggregate cost but harms a severe minority or nonparticipants | Potential efficiency advantage without acceptable tested fairness |
| C is worse than B | This particular timing-coordination scheme did not work |
| Effects are heterogeneous across fresh seeds | Coordination benefit depends on case-specific traffic conditions; broad claims remain premature |

Even a positive result does **not** establish practical human adoption, real-road improvement, full route-plus-departure superiority, or an autonomous-fleet claim.

## 12. Next milestone and approval boundary

**Next authorized intellectual milestone:** T1 prospective scientific *design and feasibility review*. Produce a single precise frozen-protocol candidate with credible B/C construction, information parity, consent model, statistical plan, practical effect threshold and fairness gates, then request **separate authorization before launching implementation or SUMO**.

**Standing scientific question:** *With comparable knowledge and comparable freedom to adjust departures, does organizing human drivers' decisions collectively produce a better total network outcome than well-informed independent decision-making?*

**Communication:** This is an internal GitHub research-planning record, not an external LinkedIn/X publication. Any future visual-first external update requires full asset review and separate explicit approval.
