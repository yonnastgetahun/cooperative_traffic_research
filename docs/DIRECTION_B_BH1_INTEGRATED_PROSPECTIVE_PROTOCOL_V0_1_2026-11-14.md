# B-H1 integrated four-gate qualification — single prospective protocol v0.1

**Date:** November 14, 2026  
**Research direction:** Direction B — minimum distinguishing investigation of voluntary cooperation.  
**Status:** **INTEGRATED DESIGN CANDIDATE / NOT YET EXECUTABLE / NO EMPIRICAL CLAIMS.** Specific values below are *prospective proposals*, selected before B-H1 physical execution; they are not measurements, calibration results, or a frozen confirmatory protocol.  
**Approval scope:** The owner approved one coordinated package to address **G1 physical spillback, G2 independent comparator, G3 voluntary participation, and G4 paired negative control and accounting** together. Conditional development execution was envisioned **only after Stage 1 qualifies all four**. This document does **not** retroactively pass that prerequisite or launch a traffic run.

## 1. Scientific question, treatment and primary outcome

**B-H1:** In a finite-storage bottleneck whose queue can physically obstruct an upstream crossing, allowing a limited number of drivers to accept a timing sacrifice can reduce **all drivers' original-preferred-departure-to-arrival time** relative to equally informed, independently rational timing choices, without unacceptable harm to nonparticipants.

This is a study of a **difference in decision objectives** (individual versus all-driver), **not** a study of improved prediction accuracy, another externality estimator, a new simulator, or exact T1 reproduction.

**Primary comparison** in the spillback-capable setting S: I (credible independent informed schedule) versus V (limited optional coordinated schedule), both using the same announced input information and same timing options. **Negative-control comparison** in setting N: repeat I versus V when the intersection's physical *blocking permission* is disabled.

Let \(\mathcal D\) contain every driver, \(p_i\) original preferred departure, \(s_i\) requested departure, \(d_i\) actual road insertion and \(a_i\) completed arrival. Then:

\[
C_{P,M}=\sum_{i\in\mathcal D}(a_{i,P,M}-p_i), \qquad
\Delta_S=C_{V,S}-C_{I,S}
\]

and the diagnostic contrast is

\[
\Psi=\Delta_S-(C_{V,N}-C_{I,N}).
\]

Negative \(\Delta_S\) favors coordination. Negative \(\Psi\) is **consistent with**, but does not uniquely prove, a spillback-mediated additional benefit. The primary endpoint includes all holding before road entry and all insertion delay. A lower in-network queue alone is never a GO.

## 2. G1 — One defined, intentionally small physical setting

**Candidate physical engine for an eventual bounded development check:** the project's already-used, pinned **SUMO 1.28.0** reference. This is **not** a renewed multi-framework evaluation and is **not** an assertion that the proposed network has already run successfully.

### Plain-network topology (candidate coordinates in meters)

| Node | Coordinate | Role |
|---|---|---|
| S | (0, −250) | Main-movement entry |
| J | (0, 0) | Crossroads upstream of bottleneck; internal junction links required |
| K | (0, 40) | Downstream single-direction signalized bottleneck |
| T | (0, 250) | Main-movement exit |
| W | (−250, 0) | Cross-traffic entry |
| E | (250, 0) | Cross-traffic exit |

Directed **single-lane** links: \`S→J\` (250m), \`J→K\` (**40m storage**), \`K→T\` (210m), \`W→J\` (250m), \`J→E\` (250m). Nominal speed **13.9 m/s** throughout; modeled vehicle length **5m** and minimum gap **2.5m**. Main demand has fixed route **S–J–K–T**; cross traffic has fixed route **W–J–E**. No route assignment, detours or new destinations occur in I versus V.

**K discharge proposal:** fixed 60s cycle, first 30s red and next 30s green, serving the J→K→T movement. This controls downstream discharge; the proposed small link can accumulate a queue during red. Its approximate spatial storage is only a *hypothesis* (40/(5+2.5) ≈ 5 vehicles); an actual lane/link/vehicle-level model must confirm it. A signal at a single permitted through movement must be shown constructible and source-consistent before G1 qualifies.

**J crossing:** two straight movements intersect. The traffic right-of-way and internal lanes must be explicitly inspected in the compiled network. No implicit grade separation, no \`--no-internal-links\`, no unmanaged teleports. A cross vehicle delayed by queue intrusion is the proposed externality; priority-rule delays unrelated to spillback must be distinguished.

**Source-critical fact:** SUMO's junction **no-block heuristic is enabled by default**. The pinned [SUMO v1_28_0 intersection documentation](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Simulation/Intersections.md#junction-blocking) states that internal links are necessary for junction blocking and a node/connection \`keepClear="false"\` can disable that heuristic. Therefore an unmodified SUMO crossroads is **not proof** of the proposed blocking effect.

### Original demand for the *prospective* new model (not historical T1)

For the single predeclared **development-template** case only:

- **48 main-movement drivers** \`m000..m047\`, original preferred \(p_i=5i\) seconds for i=0..47.
- **48 cross-traffic drivers** \`x000..x047\`, original preferred \(p_i=5i+2\) seconds.
- Exactly **96** original identities; all are retained in every arm. Main travelers and cross travelers have their own fixed routes and destinations.
- **One-second time lattice**, with signal/service-phase time origin t=0 and one original-preferred clock per ID; run until every trip completes or a prospectively declared exception threshold is reached. No vehicle is discarded to improve metrics.
- Common deterministic vehicle type in the primary candidate: length 5m, minGap 2.5m, fixed speedFactor=1 and zero random driving imperfection where supported; even with nominally deterministic car-following, stochastic source / event ordering must be audited before any causal statement.
- These traffic volumes, geometry, departure spacing and signal cycle are **a priori illustrative design settings**, not independently demonstrated to trigger spillback. If development verification does not show a physical blockage under S, **stop**. Do not quietly increase demand or shorten the link to manufacture a positive result.

**Source evidence:** [SUMO v1_28_0 intersection and blocking documentation](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Simulation/Intersections.md), [pinned vehicle departure/admission documentation](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Definition_of_Vehicles%2C_Vehicle_Types%2C_and_Routes.md) and [pinned lane-area detector documentation](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Simulation/Output/Lanearea_Detectors_(E2).md). They support *available mechanisms and output families*, not proof that the constructed candidate produces the desired physical event.

## 3. G2 — One credible independent-informed comparator, not the old T1 proxy

**Identical information in I and V:** network, original driver IDs, preferred departures, full announced schedules, fixed routes, public signal phases, assumed vehicle dynamics, and a **single immutable, nonclairvoyant timing forecast \(\hat a_i(s)\)** built from announced inputs. Neither policy may query realized future arrivals or SUMO counterfactuals while selecting schedules.

**Permitted options for the same 12 eligible main-driver IDs in both I and V:** \(\{0,+5,+10\}\) seconds relative to p_i. The other 36 main drivers and all 48 cross drivers have fixed requested departures p_i. Eligibility uses ascending SHA-256 of \`bh1-v01:eligible:<ID>\`, selecting the first 12 of 48 main IDs. The same eligibility/ID mapping, behavioral attributes and tie rules apply across I and V and S/N. These numbers are prospective restrictions, not inferred driver willingness.

**One deliberately simple, shared schedule-responsive forecast (paper definition, NOT implemented or validated):**
1. Approximate main arrival at J from \(\hat t_J=s_i+250/13.9\), and arrival at K by adding \(40/13.9\).
2. Order K arrivals by \(\hat t_K\), deterministic ID as tie break. Assign one predicted downstream service slot every **3s during K green** and no slots during red; predicted K exit is the first unoccupied feasible slot after predicted arrival.
3. Approximate storage at J→K by **five vehicle slots**, consistent with the approximate 40m / 7.5m vehicle-plus-gap relation. Compute a forecast queue by predicted K arrival/service events. Treat a predicted cross arrival at J as *blocked* in S only while the queue crosses the five-slot threshold; forecast the earliest unblocked cross-service moment. N removes that forecast blockage but retains queueing at K. **This approximation is not a measured physical model** and does not establish that occupancy actually blocks J.
4. For each ID, forecast \(\hat c_i(s)=\hat a_i(s)-p_i\). Main and cross arrivals include predeparture waiting, predicted K service, and nominal remaining route time. This same forecast function and the same action options are available to both I and V.
5. The forecasts must be frozen, mechanically specified, nonclairvoyant, and separately qualified for coherent event ordering and no negative queue lengths **before** source-code implementation or traffic execution. No calibration against future test outcomes is authorized by this description.

**I decision rule:** starting from every eligible main driver at p_i, iterate individual best responses to **own** \(\hat c_i\) while holding others' current announced schedules fixed; use deterministic SHA-256 ordering of eligible IDs. Recompute the shared forecast for each trial action. Resolve ties by retaining the current schedule, then preferring the smaller delay. Stop when the largest possible unilateral own-cost improvement is **≤0.1s**, or after **20 full sweeps**, whichever first. **If residual regret exceeds 0.1s, I FAILS QUALIFICATION**; do not compare V against a nonconverged I as if it were an independent equilibrium. A second distinct predeclared starting schedule should check sensitivity to local equilibria; if significantly different, document multiplicity and retain the best defensible I comparator or stop.

**Why this is not an already qualified predictor:** The 3s green-slot service and five-slot queue forecast are *ex ante simplified rules*, and source or development evidence has not shown that their candidate rankings are usable. They are deliberately shared to preserve information parity; equality of forecasts is necessary but does not alone establish a strong independent baseline. If I consistently responds to forecast artifacts rather than physical costs, classify the primary comparison invalid even if V appears favorable.

## 4. G3 — Limited participation and optional coordination, not simulated consent

**V uses the exact same eligible IDs, forecast, timing menu, tie rules and network knowledge as I.** Begin from the qualified I schedule. A deterministic ascending SHA-256 ranking of \`bh1-v01:accept:<ID>\` among the 12 eligible IDs preselects **six willing-to-consider-offers** and **six decliners**, independently of realized outcomes. This is a **hypothetical behavioral scenario**, not observed human consent; the six decliners retain their I choices.

For the six willing IDs, consider at most one individual's schedule change at a time. Recompute the complete \(\sum_j\hat c_j(s)\) from the same forecast used by I; propose the candidate maximizing reduction in **all-driver** predicted cost, subject to:
- A per-driver predicted own-cost increase no greater than **+5s** versus keeping that driver's current I schedule in the same announced context;
- Shift choice \(\{0,+5,+10\}\) relative to p_i, no early travel;
- A strictly positive predicted all-driver improvement greater than **0.1s**;
- Previously declined driver schedules stay identical to I;
- At most **one accepted revision per willing driver** (thus at most six actual schedule revisions); ties favor retaining the current schedule and then the smaller requested delay. Stop sooner when no eligible accepted improving revision remains.

**Refusal is honored:** no recommendation is forced or assigned to a decliner. If no offers are accepted, V collapses to I and that is a valid null result. A prespecified sensitivity comparison must include **zero willingness** and **all 12 eligible willing**; neither is evidence that real people would accept.

**Matched physical and behavioral exogenous settings:** the only treatment difference is chosen requested schedules from the above decision objectives and acceptance assumptions. The 48 cross drivers and 36 ineligible main drivers never receive timing changes. All 96 drivers remain in the accounting: 84 are ineligible (36 other main travelers plus 48 cross travelers), six preselected eligible drivers decline offers, and six eligible drivers may accept offers. Report these three groups and actual unchanged-requested-departure drivers separately. A displaced queue or worse outcome for a nonparticipant is harm, regardless of whether volunteers benefit.

**Interpretation ceiling:** This is a *voluntary-style offer acceptance model*, not a proof of genuine enrollment, rationality, repeated compliance, or real-world willingness. Payments, enforcement and long-term reciprocity are intentionally out of scope to avoid reopening the previous E2 detour.

## 5. G4 — Physically matched no-blocking control and complete outcomes

**S (spillback-capable):** At J, allow main vehicles to enter the crossing despite downstream congestion by disabling the pinned engine's no-block heuristic on **only the J main→J→K movement**, with internal links enabled (candidate \`keepClear="false"\` on that connection). Permit the resulting physical crossing blockage to occur; **do not assert it will occur** until verified.

**N (blocked-crossing prevention control):** Identical geometry, demand, K signal, options, vehicle type, simulator settings and timing policies, but enable \`keepClear="true"\` for that **same connection**, restoring prevention of main vehicles becoming stuck across J. The downstream main queue can still exist in N; this is more precisely a **crossing-blockage-disabled control**, not a traffic-free or no-queue world.

**Explicit identification caveat:** Changing keep-clear changes a **behavioral junction-entry rule**. This offers a tightly localized manipulation of modeled blocking permission without changing road lengths or nominal discharge. It does not by itself prove that \(\Psi\) is a pure physical mediation effect, or that real drivers behave as if \`keepClear=false\`. Report the change and scrutinize its secondary effects on insertion, queue storage, priority and throughput. If it changes unrelated junction behavior, mechanism attribution remains **UNRESOLVED**.

**Four-cell 2×2 protocol** (same prospective demand/vehicle identities in every cell):

| Physical setting | Independent policy I | Voluntary policy V |
|---|---|---|
| **S: crossing-blocking allowed** | S–I primary baseline | S–V primary treatment |
| **N: keep-clear enabled** | N–I mechanism baseline | N–V mechanism treatment |

**Measurement ledger for each of the 96 IDs and each condition:** original ID, OD, route sequence, main/cross classification, eligible, willing/decline, p_i, requested s_i, actual road insertion d_i, trip completion a_i, completion/abort/teleport status, per-ID assigned speed/vehicle dynamics, \((s_i-p_i)+(d_i-s_i)+(a_i-d_i)=a_i-p_i\), and difference against the same person's I result. All sums include *every* driver. Any incomplete trip or unexplained teleport fails the primary completion gate; it cannot be silently excluded.

**Mechanism observations (diagnostic, not interchangeable with measured cost):**
- J→K queue extent/occupancy over time from a source-qualified E2 lane-area detector;
- time that a main vehicle physically obstructs J's crossing conflict region, and the number/timing of cross vehicles delayed *by that obstruction*, not by their normal priority or signal;
- throughput at K and physical red/green phase schedule;
- cross-driver individual arrival costs, including those who never participated;
- deliberate distinction among upstream queue, main-line waiting, crossing blockage, and a mere delayed departure.

The pinned [SUMO v1_28_0 E2 lane-area detector docs](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Simulation/Output/Lanearea_Detectors_(E2).md) document jam length and occupancy, **but such detector output does not by itself prove a crossing was blocked**. That physical event needs an independently observable conflict-region/vehicle-state audit. The exact output contract must be source-qualified before G4 can pass.

## 6. Statistical, fairness and outcome decisions — *candidate pre-registration values*

The below values are proposed **before B-H1 outcome inspection**; their adequacy and measurement feasibility remain review items before freeze:

- **Development qualification:** one preidentified development-only demand template described in §2. It verifies the network/clock ledger, J blockage in S, its absence in N when relevant, I residual-regret gate and whether forecasts respect the same information set. It cannot support an efficacy claim. **No physics run has occurred.**
- **Independent evaluation, only after freeze:** prospectively proposed **20 independently generated matched demand scenarios**. Their generation method must be specified, versioned and kept unopened until the frozen protocol passes its preflight; drivers within a scenario are not independent inferential units.
- **Primary quantitative gate candidate:** mean paired \((C_{V,S}-C_{I,S})/96\) at most **−1.0 seconds per intended driver**, with a two-sided 95% paired independent-scenario confidence interval wholly below zero. The one-second margin is a **proposed materiality threshold**, not a power calculation or data-derived cutoff. An underpowered/inconclusive result remains inconclusive.
- **Mechanism gate candidate:** corresponding physical crossing-blockage duration and cross-movement delay decrease in S–V; \(\Psi<0\) with prespecified uncertainty calculation, and N shows that V does not obtain the same claimed benefit solely by shifting waiting. \(\Psi\) alone is not proof of mediation.
- **Fairness gate candidates:** 100% accounted-for driver outcomes; zero unexplained teleports; among nonparticipants at most **10%** with additional preferred-to-arrival delay **>10s** and no single nonparticipant with an additional delay **>30s**; for willing participants report all realized harms and flag any exceeding **+10s**. These are *prospective research safeguards*, not elicited driver preferences or validation of actual consent.
- **Sensitivity (not new tuning):** opt-out extremes and explicit forecaster/physical mismatches, with no selective extension of seeds after seeing results. Post-result changes create a **new protocol**, not a repaired result.

**Possible final labels for a later authorized study:** **GO (qualified model-specific incremental benefit with all safeguards)**; **EFFICIENCY WITHOUT FAIRNESS**; **NO-GO for tested B-H1 intervention**; **INCONCLUSIVE**; or **NOT QUALIFIED** when physical/I/clock/source conditions are invalid. The original Experiment 006 harm threshold and T1 numbers are **not inherited** as standards.

## 7. One coordinated qualification sequence and stop rules

**Stage 1 — protocol/source design qualification (this document):**
1. Verify S/N is representable with identical topology and an isolated J keep-clear difference, fixed K signal, internal links, actual finite storage and source-backed crossing obstruction observation;
2. Verify the shared forecast is fully deterministic, nonclairvoyant and usable for *both* a converged credible independent comparator and voluntary all-driver recommendation;
3. Verify fixed eligibility, the restricted menu, genuine simulated refusal and nonparticipant outcome identity preservation;
4. Verify every cost clock and completeness rule, negative-control interpretation, independent evaluation unit, and prospective fairness/materiality decisions form one coherent 2×2 design.

**Stage 1 must output one four-gate evidence matrix with** source links, frozen choices, residual assumptions, and PASS/NOT READY. **No traffic may run when a critical source/design gate is NOT READY.** Source documentation supporting \`keepClear\` and E2 queue outputs does **not** prove the candidate J geometry compiles or that a crossing-blockage output exists.

**Stage 2 — development-only verification, conditional on Stage 1 PASS:** a minimal, separately identified physically executed development check may inspect actual J blockage in S, reduced blockage in N, ledger completion and I qualification. No confirmatory seeds, no favorable policy claims, no parameter fitting to force predicted gains. If the selected geometry or model fails, report failure and return to a **new explicitly revised protocol**; do not quietly tune the original candidate.

**Scope boundary:** Do not add new frameworks, revive the cross-framework T1 project, conduct more toy equilibrium or incentive investigations, publish social media, or start a multi-run policy sweep. B-H1 remains about *the incremental value of limited voluntary decisions*, not the sophistication of a model.

## 8. Scientific provenance

- [Original Direction B checkpoint](DIRECTION_B_FOUNDATIONAL_COOPERATION_SCIENTIFIC_CHECKPOINT_2026-11-12.md).
- [B-H1 mechanism/prospective decision plan](DIRECTION_B_BH1_SPILLBACK_MINIMUM_DISTINGUISHING_TEST_PROSPECTIVE_PLAN_2026-11-14.md).
- [Current execution-readiness gate, previous 0/4 status](DIRECTION_B_BH1_EXECUTION_READINESS_GATE_2026-11-14.md).
- [Experiment 006 efficacy/fairness results](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md).
- [T1 controlled development outcome](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md).
- [PR #115 dual-source assessment](POST_T1_DUAL_FRAMEWORK_SOURCE_REVIEW_AND_DECISION_DRAFT_2026-11-09.md).
- [Pinned SUMO v1_28_0 physical junction documentation](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Simulation/Intersections.md).

**No B-H1 empirical data have been produced.** The numeric and analytic setup above is a candidate *design* to assess before any experiment, not a demonstrated improvement or new frozen scientific result.
