# T1 Cooperative Departure Timing — Prospective Protocol Candidate and Feasibility Review

**Date:** November 5, 2026  
**Status:** **DESIGN REVIEW READY — NOT FROZEN / NOT EXECUTABLE**  
**Approved scope:** Complete the scientific design and source-based feasibility review. **No code implementation, SUMO runs, release of fresh or reserved simulation seeds, estimator tuning, or external social publishing authorized.**  
**Prior approved direction:** [T1 research direction](POST_C1_T1_COOPERATIVE_DEPARTURE_TIMING_RESEARCH_DIRECTION_2026-11-05.md).

## 1. WHY: why study this, rather than continue E1-v3?

The project's original scientific question is whether voluntary collective decisions among human drivers can create better traffic outcomes than equally informed independent decisions, including costs borne by nonparticipants. We are motivated by the possibility of future coordinated/autonomous traffic, but **neither actual AV cooperation nor human acceptance has been established**.

The evidence has narrowed the question. Experiments 001–006 did not establish a joint efficiency/fairness advantage for the previously tested cooperative route assignment; Experiment 007 Test A and E1-v2 development failed their prospective externality-prediction gates; F0–F5 found important nonadditivity; C1's E3 priority manipulation changed route-swap effects by −7,578 and −19,980 network-seconds in two retrospective cases but worsened absolute network cost in both routing states. That is physical effect modification, **not** a validated externality forecaster or beneficial routing mechanism.

Instead of spending another development cycle on uncertain counterfactual route-effects, test a distinct cooperative control surface: **bounded, optional departure-time choices with fixed, matched routes**. The scientific aim is to isolate incremental coordination benefit, not merely benefits from shared forecasts or from spreading demand. A negative result is as valuable as a positive result if it cleanly tests that distinction.

Historical sources: [Experiment 006](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md); [Experiment 007 Test A](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md); [E1-v2 D1](POST_EXP007_E1_V2_D1_FINAL_DEVELOPMENT_AUDIT_2026-11-04.md); [F0–F5](POST_EXP007_E1_V2_F0_F5_ARCHIVAL_MECHANISM_FINAL_REPORT_2026-11-05.md); [C1](POST_EXP007_C1_E3_CONTROLLED_FINAL_SCIENTIFIC_REPORT_2026-11-05.md).

## 2. HOW: what will be controlled, randomized, measured?

**Question:** On a fixed synthetic network and identical set of routes, do voluntary-style coordinated departure adjustments reduce **total original-preference-to-arrival elapsed cost** more than individually optimized departure adjustments with precisely the same traffic information, flexibility and eligible drivers?

All arms begin with identical `N=1000` identities, OD pairs, original preferred departures `p_i` in a high-congestion 200-second window, vehicle dynamics, source network and **one single common, traffic-aware independent pretrip route assignment `r_i`**. Generate routes **before timing optimization** without looking at outcomes from any future arm; keep each route's complete edge sequence unchanged across A/B/C. The traffic-aware pretrip source may reuse the Experiment 007 I generator as common route builder, provided its source, candidate legality and dependence on pre-outcome announced demand are checked. This is an *idealized announced-demand* study, not an experiment against Google Maps/Apple Maps/Waze.

**A — Unshifted:** `s_i = p_i` for all vehicles.

**B — Independent informed timing (primary comparator):** Each eligible simulated driver chooses `s_i` from the same bounded menu to minimize **predicted personal preferred-departure-to-arrival cost**, holding the other currently announced selections fixed. Joint intentions are visible to both B and C in this idealized shared-information setting. No collective objective is used.

**C — Joint coordinated timing:** The identical eligible vehicles consider exactly the same timing options, but a coordinator chooses changes minimizing **the sum of predicted costs for all 1000 drivers** subject to the same permitted options and an explicit simulated acceptance rule. This is a bounded sequential heuristic, **not** proof of global system optimality.

**Primary comparison: B vs C**, interpreted as a *policy comparison* under equal information and fixed routes, **not a proof that every independent-timing policy is inferior**. A is a secondary unchanged-demand control. B and C never observe actual future SUMO outcomes, ground-truth counterfactual travel times, or separate privileged forecasts.

### Provisional eligibility / consent model

- Identical deterministic 50% eligible IDs for B and C; other 50% may not alter departures; eligibility must be seed-reproducible and selected independently of the realized outcomes.
- Candidate shifts `h_i ∈ {0,10,20,30}` seconds **later** than the original preferred departure; zero is always available. Equal choices for B and C. No early departures.
- For C, **assumed opt-in** to an offer only when its *predicted personal cost* is at most **5 seconds worse than keeping that driver unshifted in the current announced schedule**, and the driver's maximum shift is 30 seconds. A failed offer leaves the previous time unchanged. This 5-second concession is a **modeling assumption**, not empirical consent or real-world stated preference. For B, the same 5-second eligibility constraint is available but its own-cost minimization ordinarily declines a predicted sacrifice.
- The no-change alternative and deterministic opt-out/acceptance gate are applied during choice evaluation; do not force a shifted departure on the 50% nonparticipants.
- **Unresolved before freeze:** whether requiring consent against the **current** announced no-shift counterfactual (rather than a fixed initial personal reference) creates order-dependence. The prospective protocol must lock one precise convention and verify it before execution; suggested convention is same-current-announcements with driver's own offset set to zero.

The 50%, 30-second and 5-second values are provisional *scientific policy design choices*. They are not estimates of human willingness and are not adjustable after confirmatory results.

### Common forecast and policy parity

Using an existing 30-second occupancy bin would be too coarse to reliably distinguish proposed 10-second choices. **Do not silently reuse it.** The design-review candidate proposes one minimal, transparent, identical schedule-responsive proxy, not an E1-v3 route-externality estimator:

1. Fixed routes provide each vehicle's ordered edge sequence; the known initial network gives nominal edge free-flow times.
2. For any announced schedule `s`, project arrivals to edge e by `s_i + cumulative nominal free-flow time before edge e` and assign to deterministic **10-second time bins**.
3. Compute count `q(e,b)` of planned uses of each edge/time bin and a static capacity proxy `k_e = max(1, edge_length × lanes / 7.5)`.
4. A provisional edge forecast is `τhat(e,b) = ff_e × (1 + q(e,b)/k_e)`, with pressure coefficient 1.0. This is a deliberately simplified *assigned-demand* proxy, not true physical occupancy, junction discharge or calibrated delay. All constants, inclusion of a vehicle in its own count, boundaries and rounding must be frozen before outcomes.
5. Predicted individual cost is `ĉ_i(s) = (s_i−p_i) + Σ_{e∈r_i} τhat(e,bin(s_i,e))` and predicted collective cost `Ĉ(s) = Σ_i ĉ_i(s)`.
6. For every candidate B or C shift, recompute the **same** schedule-dependent forecast, including changed edge/bin counts of *other vehicles*. This avoids giving C a richer physical model than B; only their objectives differ.

This proposed proxy is **unvalidated** for counterfactual departure shifts; past E1 route-perturbation failures do not validate it. That is a major interpretation and feasibility limitation. The actual comparison would establish only outcomes for these specific algorithms sharing this proxy. It must be treated as exploratory unless a prospective development-only check can establish enough sensitivity to discriminate 10-second shifts without outcome leakage.

### B and C deterministic optimization — to be finalized before freezing

**Shared:** Start all eligible shifts at 0. Each pass visits eligible vehicle IDs in a predeclared SHA256-derived seed-specific order (same order in B and C). For each driver, evaluate all four timing choices with all others fixed and update immediately. Deterministic tie breaking: prefer current offset, then smaller offset, then vehicle ID. No SUMO calls or held-out observation may occur during policy construction.

**B:** Choose the shift yielding lowest `ĉ_i` under the same common forecast, subject to consent/eligibility constraints. Repeat whole passes until no driver has an available unilateral predicted improvement above **0.5 seconds**. Hard maximum **20 passes**. Compute and retain the *maximum remaining unilateral gain*; if >0.5 s at pass 20, classify **BASELINE_NOT_STABLE** and do not treat B as a credible independent equilibrium. Finite sequential best response can cycle: document cycle handling and prohibit cherry-picking the best observed B state.

**C:** Choose the shift yielding lowest `Ĉ(s)` among the same available choices **only if** the collective forecast strictly improves (proposed minimum numerical improvement 1e-6 network-seconds) and the individual acceptance rule passes; otherwise retain the current shift. Stop on a no-change pass or 20 passes. Record the maximum remaining feasible predicted collective gain. C is a local-search joint-scheduling heuristic, not a claimed optimal assignment.

**Resource and fairness caution:** Equal candidate menus and common information matter more than equal CPU time. Still report candidate evaluations, sweeps and compute. If B is less well optimized because of computational caps or poor convergence, the primary interpretation is invalid; do not rescue C by weakening B. Policy choice is based only on predicted `ĉ_i` / `Ĉ`, never SUMO evaluation output.

### Feasibility check needed before freeze

Can the 10-second schedule-responsive proxy discern alternative offsets beyond artificial bin-boundary effects, and can B reach a stable state under the finite best-response procedure? These are **design uncertainties**, not observed successes. Conduct only no-SUMO source/unit checks under a later authorized implementation milestone, then development-only simulations if separately approved. If B fails to qualify or candidate effects are entirely bin artifacts, **DESIGN NO-GO / REVISE PROSPECTIVELY**, without opening confirmatory cohorts.

## 3. Outcomes and scientific decision gates (candidate, not frozen)

Let `p_i` be immutable original preferred departure and `a_{i,P}` **observed arrival** under policy P. The realized all-driver cost:

`C_P = Σ_{i=1}^{1000} (a_{i,P}−p_i)`.

For the primary paired seed comparison use the per-driver difference `Δ_s = [C_B(s)−C_C(s)]/1000`; **positive favors C**. This deliberately includes voluntary predeparture time, SUMO insertion/departure delay and all in-network time; do **not** add waitingTime again. Report `a_{i,P}−p_i = (s_i−p_i) + (actual_depart_i−s_i) + (arrival_i−actual_depart_i)`. Save `p_i` in separate immutable demand manifest because native SUMO `departDelay` is relative to each arm's *requested* departure, not the original preferred departure.

**Candidate statistical gate:** 10 independent, genuinely new paired demand seeds; two-sided Student-t 95% confidence interval over 10 seed-level `Δ_s` values has lower bound **>0**, and mean advantage at least **2.0 seconds per driver**. This is a pragmatic target by analogy with previously frozen studies, **not** powered or proven feasible; include a development-based variance/precision rationale and do not use actual confirmatory observations to change sample size or threshold. If the interval includes zero, classify mean efficacy **INCONCLUSIVE** even if the point estimate is positive.

**Candidate joint fairness gate:** In the **B→C** matched-driver contrasts, all vehicles complete in every arm; at most **10%** of all drivers and **10%** of nonparticipants have **>30 seconds** additional realized preferred-departure-to-arrival cost; at most **50%** of all drivers are strictly harmed; mean of seed-level p90 absolute costs in C is no more than **5 seconds** greater than B. Numeric collision, teleport, emergency stop and braking fields must not show a material unexplained disadvantage, and missing fields cannot be treated as zero. These are conservatively adapted prospective *study-specific research gates* from Experiments 006/007, not measured human preferences.

**Required distribution reporting:** participant/nonparticipant matched cost deltas, delayed and unchanged drivers, mean/median/p90/p95/p99 and p95 *paired harm*, fraction harmed >0/>30 sec, desired-departure versus requested-departure versus insertion waiting components, edge and E3/bottleneck approach queue windows, realized arrival/throughput and scenario completeness. Predeclare hotspot location from *pre-outcome evidence* or use network-wide descriptives without outcome-selected causal claims.

**Decision categories:**
- **GO for this specific fixed-route, assumed-consent timing policy only:** all validity, B-credibility, statistical, practical, completion, fairness and exception gates pass.
- **EFFICIENCY BENEFIT / FAIRNESS NO-GO:** C yields credible mean benefit but fails any joint harm safeguard.
- **PRIMARY NO-GO:** confidence interval excludes zero in direction favoring B, or C fails the predeclared practical gate after adequate evidence; distinguish unfavorable from inconclusive evidence explicitly.
- **INCONCLUSIVE:** interval includes zero; separately report fairness verdict. No post-hoc seed extension.
- **DESIGN / DATA INVALID:** baseline stability, parity, source, completion or accounting fails; preserve failure and make no efficacy claim.

C beating A alone is not a GO. Lower in-network waiting with no improvement in preferred-to-arrival time is not a GO.

## 4. Read-only/source feasibility checkpoint (no new experiments)

Repository capabilities *observed in source*:
- Frozen demand generation: `experiments/experiment_002/fixed_demand_v01.py`; current `experiments/experiment_007/run_v01.py` regenerates the 10×10/200s/1,000-vehicle pretrip scenario and contains an idealized common independent traffic-aware route assignment `I`.
- Existing `experiments/experiment_007/run_v01.py` writes legal fixed route XML with scheduled `depart`, runs SUMO with a fixed seed, and reconciles tripinfo arrival, actual depart and originally scheduled demand. This is a **source-level feasibility finding**, not executed T1 parity testing.
- Existing `experiments/experiment_004/run_arm_v01.py` demonstrates a three-stage network/demand/routing run structure. T1 should re-use, not modify, historical frozen input/generator files.
- Official SUMO vehicle documentation: `depart` is the *requested insertion time*, and actual departure may occur later because a road is full. [Vehicle and route definitions](https://sumo.dlr.de/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.html). [TripInfo documentation](https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html).
- SUMO `duaIterate.py` is a route-choice equilibrium tool; it **does not establish** the stability or credibility of our proposed *departure-time best-response* procedure. [SUMO dynamic user assignment](https://sumo.dlr.de/docs/Demand/Dynamic_User_Assignment.html).
- Relevant transportation scholarship distinguishes dynamic user-equilibrium timing choices from dynamic system optimum. This is theoretical context, not proof for T1. [Dynamic traffic assignment in a corridor network: Optimum versus equilibrium (2022)](https://doi.org/10.1016/j.trb.2022.04.007).

**Still unverified and necessary prior to any freeze:** the new 10-second forecast's suitability, B convergence, C acceptance semantics, exact forecast recomputation, common-route generator's effective traffic-awareness, feasible compute budget, source/unit parity, and precision rationale. No T1 source modifications, no no-op or real SUMO simulations, and no new seed access have occurred in this checkpoint.

## 5. Bounded proposed implementation/evaluation sequence (requires separate authorization)

1. **Approve candidate protocol specifics** (especially B stability, common forecast, voluntary cost allowance, fairness and practical benefit gates); keep them versioned as a **pre-freeze design specification**, with unopened disjoint confirmatory cohort and explicit STOP conditions. A final freeze follows required feasibility qualification, not precedes it.
2. **Only after distinct implementation authorization:** implement narrow route-snapshot / timing-only B/C policy builder and static/unit invariants; verify original source hashes, request/actual departure accounting, deterministic ties, forecast parity and no oracle. No new scientific sample.
3. **Only after additional development-run approval:** minimally test B convergence, C feasibility, 10-second forecast sensitivity and nonparticipant route invariance on already inspected **development-only** demand; document any design changes before final protocol freeze, never on held-out T1 data.
4. **Only after separate fresh-run approval:** candidate budget **10 new disjoint seeds × 3 policy arms = 30 SUMO arms**, with B/C identical seeds and SUMO settings, no substituting results or adding seeds based on observed outcomes. Seed IDs are not yet assigned; do not reuse original 4101–4105, 4201–4210, 6101–6114, 6201–6212 (reserved), 6301–6312 (reserved), or any earlier experiment cohort.
5. Run exactly the frozen audit, publish original outcomes, exceptions and matched-driver evidence with SHA ledger and one report/README link; label **GO, NO-GO, INCONCLUSIVE or INVALID** with scope limits. Visual-first public communication requires separate presentation, review and authorization.

**No silent workflow that auto-executes confirmatory or reserved seeds on merging a documentation PR.**

## 6. Recommendation after feasibility review

**Scientific direction: RETAIN T1.** It directly asks the project's original cooperation-vs-independent question with a new mechanism and bounded resources. **Execution readiness: NOT YET ESTABLISHED.** Two risks dominate: the independent B timing policy may not converge to a credible equilibrium, and a crude shared 10-second time-bin predictor may rank timing choices poorly. These must be dealt with prospectively rather than covered over with favorable C-vs-weak-B results.

**Next decision requested:** Review this protocol candidate and authorize narrowly scoped implementation/feasibility qualification *only once* the design-level comparability and acceptance conventions are accepted. No new SUMO or independent validation is authorized by publication of this document.
