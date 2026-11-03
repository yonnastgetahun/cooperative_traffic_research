# Cooperative Traffic Research — Prospective Network-Externality Estimator: Full Development Specification

**Date:** November 2, 2026  
**Research stage:** After Experiment 007 Test A, archival investigation P0–P3, and six-run instrumented replay.  
**Status:** **Prospective design and development specification only. NOT a frozen implementation protocol, new simulation, trained model, independently validated estimator, or authorization to run Test B.**  
**Research objective:** Build a scientifically credible, computationally bounded predictor of how a **proposed individual route change** affects **(a) that driver's own actual elapsed time** and, separately, **(b) the actual elapsed times of everyone else** on a coupled road network. Preserve reproducible evidence, equal information and individual fairness.

## 0. Executive decision

**Recommended development direction: an explicitly counterfactual, junction-aware, finite-capacity network-response model**, starting with a deterministic conservation/queue approximation rather than a black-box model trained to match the failed Experiment 007 outcomes.

The estimator must:
1. Start from **the same prospective information** under an unchanged route assignment and a one-route alternative.
2. Simulate or approximate **time-dependent vehicle arrival, link queues, intersection/turn discharge, blocking, downstream receiving capacity and upstream spillback** for each counterfactual.
3. Produce **separately identifiable predicted self-time change and others'-time changes**, then reconcile them to a total; externality cannot simply be a fixed multiple of the driver's own-cost prediction.
4. Quantify **uncertainty and risk**, especially when a nominally cooperative diversion is predicted to help others but may actually hurt them.
5. Work without using SUMO's **unrealized future trajectory, route-probe outcome, or held-out validation labels** as at-decision input.
6. Demonstrate minimal mathematical, integrity and engineering readiness **before** a newly frozen and truly independent externality-validation study. Only after that separate validation succeeds may the project reopen a whole-policy Test B.

The **new scientific claim is NOT yet established**. The development specification is a falsifiable design proposal. If the proposed approach cannot predict counterfactual network effects credibly, report failure and reconsider the coordination mechanism rather than claiming improvement from an untested route policy.

### Why this work is necessary

Experiment 007 Test A: 30 controlled SUMO executions, five independent demand seeds, 20 deliberately selected single-route swaps and five two-route bundles. Correct sign on only **8/20 = 40%** of material externalities; original **60% progression gate failed**. Mean absolute externality prediction error was **1,801.71 network-seconds** on the selected probes. Five predictions were zero while realized effects were material. **Test B was not executed.**

The [completed P0–P3 investigation](POST_EXP007_EXTERNALITY_ESTIMATOR_P0_P3_FINAL_SCIENTIFIC_REPORT.md) independently reconstructed those outcomes and demonstrated that, **for all 20 tested equal-nominal-free-flow alternatives**, the former assigned-count proxy predicted:
- total network-cost change = **2 × own-driver predicted cost change**;
- predicted externality = **own-driver predicted cost change** (numerical precision).

The [six-run observational replay](POST_EXP007_SIX_RUN_INSTRUMENTED_REPLAY_FINAL_SCIENTIFIC_REPORT.md) reproduced **all six original 1,000-driver outcomes exactly**. It recorded one-second vehicle movements and five-second edge/lane measurements, with large observed road-entry-time errors relative to 30-second model bins, major waiting-time differences, and an original **−2,989 network-second** two-route interaction in one selected seed. These are **development diagnostics and mechanism clues**, NOT independent validation of any replacement model, and do not identify one junction as a unique causal mediator.

The historical Test A **NO-GO remains unchanged**, as does the unexecuted status of Test B. **Individual fairness stays active. Subjective journey quality and comfort stay deferred.**

## 1. Precise prediction problem, estimands and units

### 1.1 Predecision context

At decision time t0, a complete but potentially uncertain network scenario is characterized by:
- road network topology, link/turn geometry, allowed movements, lanes, free-flow times, storage and nominal discharge parameters;
- observed/historically inferred traffic state available **no later than t0** (including possible initial queues, flows and incident/signal information);
- known or probabilistically estimated departure demand and route intentions, distinguishing eligible opt-in commitments from unobserved background demand;
- selected eligible vehicle i, original feasible route r_i, proposed feasible route r'_i, both with the **same scheduled departure**;
- all other announced route choices held fixed for the *local one-change contrast* (their **realized journey times may change**), with identical demand, driver identities and random-state assumptions across counterfactuals.

The first research domain deliberately retains the previously idealized **full announced demand** used for the equal-information synthetic comparison. An operational smartphone-only partial-information mode is **a separate later capability**; never represent precise announced travel intentions of every vehicle as observed in a real-world deployment.

### 1.2 Ground-truth outcomes (available only after a controlled SUMO run)

For individual driver j in scenario A, define elapsed journey time **from scheduled departure**, including insertion delay:

~~~
T_j(A) = actual_arrival_j(A) − scheduled_departure_j
~~~

Let A0 be the original all-driver assigned routes and A1 replace only selected driver's route with the permitted candidate.

~~~
Δself_i     = T_i(A1) − T_i(A0)
Δexternal_i = Σ_{j ≠ i} [ T_j(A1) − T_j(A0) ]
Δall_i      = Δself_i + Δexternal_i
Δnonopt_i   = Σ_{j nonparticipants} [ T_j(A1) − T_j(A0) ]
~~~

**Sign convention:** negative = benefit/time saved; positive = harm/additional time. **Units:** elapsed seconds per driver for self; **network-seconds** (seconds summed over drivers) for external and total. Mean seconds per person is reported separately with its own denominator.

**Critical:** SUMO waitingTime is contained in completed-trip duration; insertion delay is counted exactly once in scheduled-to-arrival total. TimeLoss is a diagnostic, **not an extra additive travel-time component**. Require 1,000 original identities to arrive in each arm, or label all-demand effect unidentifiable instead of reporting a completed-only convenience estimate.

### 1.3 Prospective outputs (must be produced before the counterfactual run)

Given only available predecision context I(t0) and two fixed routes, the model shall produce:

| Output | Definition | Required |
|---|---|---|
| pred_self_delta_s | Predicted target individual's elapsed change, in seconds | Yes |
| pred_external_delta_network_s | Predicted sum of *other vehicles'* elapsed changes, in network-seconds | Yes |
| pred_all_delta_network_s | **Exactly** pred_self + pred_external, reconciliation output | Yes |
| pred_nonparticipant_delta_network_s | Predicted aggregate impact on unconsented/nonparticipant drivers | Yes in full-announced mode |
| self/others harm probabilities | Predicted risk of own burden, severe harm to others, and positive externality when model uncertainty is meaningful | Development target |
| prediction intervals | Calibrated or explicitly *uncalibrated* predictive ranges; do not claim calibration on development data | Development target |
| model_input_timestamp | t0 and feature information cut-off; no future simulation observations | Yes |
| model_version, feature/source hashes | Full model and data provenance | Yes |
| candidate validity and runtime | Feasibility, candidate path fingerprints, forecast latency/memory | Yes |

When driver-specific identities are modeled, retain an optional **per-vehicle counterfactual outcome table** and group totals. Aggregate-only predictive methods must still explain how an external term is separately derived and checked for conservation, no double counting, and nonparticipant effects.

A mere subtraction of two algebraically coupled versions of the prior quadratic assignment cost **does not qualify** as a genuinely independent prediction of other-driver network consequences.

## 2. Distinguish the decision-time forecast from retrospective measurements

### A. Allowed in the prospective estimator

- Static network geometry, connected candidate routes, lane and turn restrictions, capacity/storage priors, traffic signal schedules *if available/announced at t0*.
- Historical traffic summaries built exclusively from **development** data; model coefficients/uncertainty calibrated on designated development partitions.
- Predecision network state inferred from information available at or before t0. A past probe's FCD or measured lane waiting may inform **offline model design or training only**, never the prediction input for an unseen future probe.
- The same predeclared demand schedule, announced participating routes and selected background-demand estimate as would be available to the independent comparison policy.
- Independent random uncertainty samples drawn from a fixed, documented distribution and seed, reused fairly across baseline and swapped-route rollout.

### B. Prohibited as model inputs at decision time

- SUMO vehicle trajectories, queue lengths or edge arrivals **after** t0 for the same held-out seed being evaluated.
- Actual alternate-route tripinfo, detector waiting totals, SUMO edge exit times, future arrivals, or realized counterfactual results.
- Label-derived features such as "which probe actually helped," post-treatment queues, or a correction inferred from the same held-out outcome.
- Different information between prospective cooperative and independent policies in later Test B.
- Any hidden adjustment of scheduled departure, other drivers' planned routes, traffic-signal logic or driver compliance while calculating one-route effects.

**Design principle:** Using SUMO to create controlled labels during development is permitted **offline**; querying SUMO to reveal the answer for the new decision under evaluation is **simulation clairvoyance**, not forecasting. Every feature must be tagged with availability time, source, missing-data behavior and whether it is a real deployable observation or idealized simulator input.

## 3. Recommended architecture: prospective dynamic network-response estimator

### 3.1 Four explicitly separate modules

**M1 — Input/state and demand estimator.** Translate announced routes, scheduled departures and predecision traffic measurements into time-indexed edge/junction *inflows* and initial congestion state. Track unknown background arrivals separately; include uncertainty if partial demand. Forecast entry times, not only nominal route order. Preserve t0 information cut-off.

**M2 — Bounded link/turn queue and discharge model.** A conservation-based, cell/link transmission or queueing approximation with receiving and sending constraints and junction movement capacities, including storage limits. Track:
- number of vehicles occupying and queued on each directed link or short cell at each discrete time step;
- predicted link-entry and exit times and turn-dependent service availability;
- intersection turn demand, permitted movements, priorities/green phases when known, limited discharge and blocking;
- downstream receiving capacity; an upstream link cannot discharge vehicles into a full downstream link;
- queue spillback on upstream approaches and propagation to otherwise unchanged-route drivers.

**M3 — Paired counterfactual rollout.** Run two independent *predicted network evolutions* starting from the **identical forecastable initial state and identical other drivers' demand/intended routes**:
- baseline A0 with original route r_i;
- intervention A1 with permitted alternative r'_i.
Use common input and uncertainty samples to reduce artificial contrast variance. Estimate a **completion/arrival time for each modeled vehicle** under both, including expected insertion delay if modeled. Do not simply add nominal time penalties to a fixed static path.
Compute self delta from the **target's two predicted arrival times**. Compute external delta by **explicitly summing the predicted arrival changes of j≠i**, including nonparticipants and unaffected-route vehicles; only afterward compute total as their sum.

**M4 — Calibration, uncertainty and audit adapter.** Estimate unknown congestion/queue parameters from *development-only* measurements, track predictive spread, return reliability/abstention flags, enforce reproducible outputs and expose the exact predicted causes (edge/time forecast congestion, junction receiving constraints). Do not train solely to maximize sign agreement on the historically failed 20 probes.

The dynamic model is a **tractable physical approximation**, not a complete SUMO emulator; its physical assumptions must be tested and failure documented.

### 3.2 Minimal physical state and update

A recommended first version uses directed edge or short-cell states at a **proposed 5-second time step** (consistent with the instrumented replay's 5-second aggregate measurements), with 1-second FCD used **offline for diagnostic calibration** where available. Exact spatial discretization is a later freeze decision and must be justified by jam density, link length and ability to represent storage.

For cell/link k and step t:

~~~
occupancy[k,t+1] =
    occupancy[k,t] + entered[k,t] − exited[k,t]

sending[k,t] = min(occupancy[k,t], flow_capacity[k,t])
receiving[k,t] = min(free_storage[k,t], downstream_acceptance[k,t])
turn_flow[k→m,t] <= sending[k,t], receiving[m,t], junction_turn_service[k→m,t]
~~~

The model needs *consistent* node and turn flow allocation: two movements cannot both consume the same downstream receiving capacity, and mutually conflicting turns cannot exceed a common junction service budget. If unknown, label priority/phase assumptions as approximations and test sensitivity. Conservation, nonnegative state and bounded storage are **hard invariants**.

Time-dependent vehicle entry/exit is determined by these flows and ordered demand cohorts, not by extrapolating the old fixed **30-second ordinal edge clock**.

**Queue spillback condition:** when downstream storage is saturated or turn discharge is restricted, upstream flow must be throttled and additional delay can propagate to vehicles whose planned routes did not change.

The operational output is a route-level and network-level prediction, not proof that each modeled stop occurs at the real causal junction.

### 3.3 A bounded progression — no premature deep learning

| Candidate | Purpose | Development decision |
|---|---|---|
| **B0: zero externality** | Naive null prediction for all other-driver effects | Mandatory benchmark |
| **B1: frozen old assigned-demand quadratic proxy** | Directly retain the failed Experiment 007 comparator without altering historic results | Mandatory benchmark |
| **B2: improved own-time-only timing predictor** | Distinguish externality skill from good individual ETA skill | Mandatory benchmark |
| **E1: queue-aware constrained-flow counterfactual** | **Primary development candidate**. Predict pair of network evolutions with link/junction sending/receiving | Build only after source/unit design freeze |
| **E2: queue-aware + spillback and learned development-only residual** | **Conditional extension**, only if E1 diagnoses specific unmodeled effects and E2 information/runtime remains legitimate | No automatic implementation; document incremental information and complexity |

**Prefer E1 first.** Learned residual corrections are optional and must not introduce post-treatment information leakage or overfit six retrospectively selected traces. An alternative robust statistical model may be compared in a subsequent amendment, but not silently added to rescue a poor E1 result.

### 3.4 Important practical constraint: information and computation

Full 1,000-vehicle paired network rollouts per possible swap may be too expensive for consumer-scale real-time route decisions. Instrument E1's inference time, peak memory and scaling versus active vehicles, time horizon, candidate routes and network size. First target **offline research feasibility** with deterministic 10×10, 1,000-driver scenarios; do not assert smartphone deployability without a separate latency and information study.

For later scalability consider localized influence regions, warm-started baseline rollouts, sparse turn matrices, and batch/parallel vehicle proposals. Any approximation must document whose effects are excluded and how much error that omission creates. Do not declare a false external benefit simply because distant effects were truncated.

## 4. Prior observations to use as diagnostics, not validation labels

The existing historical cases may guide unit tests, failure modes and physical explanation:

- The 20 Experiment 007 probes: externality sign 8/20, five zero predictions with material realized effects, large magnitude errors and five nonadditive bundles.
- Original P0–P3: the **conditional exact identity** external prediction = own prediction for equal nominal-cost swaps; extensive consequences among other drivers with unchanged route sequences; waiting and insertion decomposed.
- Six-run replay: all six original tripinfo and safety fields reproduced exactly; forecast 30-second bin disagreements on many route edges (e.g., **11/12** on one seed-4102 target baseline); substantial waiting differences; a target entering road segment C6C5 **39 seconds earlier** when another route was changed; original combined two-route interaction **−2,989 network-seconds**.
- No uniquely identified real causal junction; isolated source edges are *hypothesis candidates*, not known true mediators.

**Allow use:** engineering fixture design, choosing queue/discharge state variables, unit-test examples, diagnostic illustrations and historical model-comparison reporting.

**Disallow use:** calling fitted performance on 4101/4102 "held out", selecting E1/E2 only because it matches their signed effects, inferring validation success from that same six-run evidence, claiming observed edge waiting is a predecision input, or generalizing from two post-outcome-selected seeds.

## 5. Explicit independent self-vs-external identification checks

These checks are **mandatory before any independent validation freeze**, using deterministic hand-built miniature networks/fixtures (not SUMO outcomes):

1. **Conservation:** Vehicle counts cannot become negative; outflow respects per-link/junction capacity; entering and exiting flows reconcile with occupancy; storage limits and queues do not create/destroy vehicles.
2. **Paired equality:** Identical A0 and A1 route and state produce self=0, external=0, total=0 to within declared numeric tolerances.
3. **Two disjoint paths:** With no shared downstream conflict and enough capacity, a swap can alter own route time without inventing large delays for unrelated drivers.
4. **External-only interference:** Construct equal free-flow alternatives and a junction where target self times are equal or nearly equal while another driver's discharge is meaningfully delayed. Model must permit nonzero predicted externality **without requiring nonzero own-time delta**. Verify no fixed rule enforces external=self or total=2×self.
5. **Positive and negative externalities:** Demonstrate examples of both added network cost and third-party benefit from comparable-route swaps, without selectively changing other drivers' demand.
6. **Queue spillback:** Downstream receiving cap reduction must create an upstream delay in appropriate traffic cohorts even if their route remains unchanged.
7. **Turn competition:** Shared junction discharge constrains two conflicting movements; turn penalties are not simply static per-edge load with no flow conservation.
8. **Arrival timing:** Different initial queue or departure conditions shift predicted entry times across bins. Reject the old fixed ordinal 30-second clock as the sole state evolution.
9. **Two-route nonadditivity:** On an intentionally coupled toy network, predicted joint effect **can differ** from the sum of two isolated effects. The model must compute actual joint counterfactual predictions rather than adding marginal estimates by assumption.
10. **Independent population accounting:** The predicted external term is computed by summing other drivers' modeled time differences, and \`all=self+others\` holds; target ID never accidentally counted among "others." Nonparticipant totals are correct by identity set.
11. **Insertion delay:** If link entrance storage prevents scheduled entry, own/all elapsed includes the modeled insertion delay exactly once.
12. **No future data:** A feature manifest and tests prove that all inference-time features are available ≤t0; deliberately insert fake future features and ensure the estimator rejects them.
13. **Reproducibility:** Same context/model/configuration yields byte-identical predictions and consistent uncertainty samples; seed is explicit and logged.
14. **Missing/noisy inputs:** When queues, turns or background flows cannot be estimated, return a documented uncertainty/abstention state instead of unwarranted precise externality signs.
15. **Sign convention:** Positive predicted externality always means harm to others; zero/numerically tiny effects are not forced into a meaningful positive/negative class.

**Gate:** No model may be called "externally informed" unless the externality signal can vary separately from own-time in controlled physical fixtures and all accounting/integrity tests pass.

## 6. Development datasets: strictly separate labels, tuning and independent confirmation

### 6.1 Four source categories (must be tagged)

| Source | Permitted role | Explicitly prohibited |
|---|---|---|
| Existing Experiment 007 probes 4101–4105 and six-run traces 4101–4102 | Historical diagnosis, engineering fixtures, qualitative expected failure cases | Prospective confirmatory accuracy, test-set selection, new validation verdict |
| Deterministic toy networks/unit fixtures | Mathematical and software correctness tests | Generalized empirical accuracy claims |
| **New development-only SUMO cohorts** | Fit physical parameters, debug state evolution, candidate comparison, iterate E1/E2 | Count as unseen independent scientific validation |
| **Fresh future independently frozen confirmation cohorts** | Evaluate a **locked** estimator with immutable predictions made before observations | Training, hyperparameter tuning, changing thresholds after seeing outcomes |

**Crucial:** Development cohorts and the future confirmation set must have **disjoint seed identities** and ideally disjoint perturbation selections. Never reuse the original withheld Experiment 007 Test B policy seeds **4201–4210** as estimator-development labels; Test B must use a clean separate cohort if eventually authorized.

### 6.2 Proposed bounded development study — a plan, not permission to simulate

A practical first budget to freeze during implementation authorization:

- **Development-build partition:** proposed seeds **5101–5106** (six independent demand seeds). Per seed: one original independent traffic-aware baseline, **four prospectively chosen single-route perturbations**, and one two-route bundle. That is **six runs per seed × six seeds = 36 controlled SUMO scenario arms**. Do not launch them under this document.
- **Development-check partition:** proposed seeds **5111–5114** (four additional independent seeds × same six-arm pattern = **24 arms**), used for model/parameter choices and debugging only; label honestly **development evaluation**, not independent validation.
- Distinct **future confirmatory estimator-validation seeds** and **future Test B seeds** will be reserved and frozen in a separate protocol. They must not be opened, simulated, peeked at or used in any architecture selection here.

**Proposed maximum total development footprint: 60 SUMO arms**, contingent on later authorization, pinned version, resource plan and validated scripts. Existing six replays are not added to that number and do not count as prospective out-of-sample evidence. Choose a smaller footprint if informative diagnostics justify it **before** new outcomes are inspected. Do not adapt sample size or swap selection based on partial successes.

**Prospective perturbation selection (before outcome viewing):** sample feasible route swaps across varied predicted baseline congestion exposure, spatial regions, departure times, baseline path lengths, turns and participant identities, with separate bins for near-equal nominal travel times and different nominal times. Include negative, neutral and positive *predicted* externality ranks if predicted classes exist, but avoid only extreme model-picked cases. Preserve all selection seeds and rejected-candidate reasons. Each seed's four probes share one baseline and are **not independent experiment replicates**.

**Bundle selection:** Preselect two distinct eligible swaps in one seed with plausible junction/time overlap and test their combined effect; additionally include at least one low-overlap bundle in future broader development if feasible within budget. Bundle tests assess potential nonadditivity, not global route optimality.

**Counterfactual labels:** Run paired SUMO arms with exactly matching network, OD, scheduled departure, car-following distributions, scenario seed and all non-target **planned routes**. Keep insertion delay in the outcome. Preserve route hash differences (one for singleton, exactly two for bundle), 1,000 paired IDs, complete arrivals and original SUMO exception metrics. An unchanged SUMO seed supports paired repeatability but may not guarantee identical random-consumption trajectories after a route swap; run separate identical-input determinism checks on *development fixtures only* if needed.

**Measurement exports:** tripinfo, statistics/collisions, 5-second edge/lane traffic summaries and optional FCD samples from development scenarios. Record labels for every other driver's actual elapsed difference. Never feed *counterfactual* or future per-seed SUMO traces back into a prediction for that same scenario during its evaluation phase.

### 6.3 Dataset schema and leakage prevention

Minimum per-probe row:

~~~
experiment_partition, seed, baseline_id, probe_id, target_vehicle_id,
decision_time_s, original_route_hash, alternate_route_hash,
model_version, feature_cutoff, input_feature_hash,
pred_self_delta_s, pred_external_delta_network_s,
pred_nonparticipant_delta_network_s, pred_all_delta_network_s,
predicted_probability_network_benefit, prediction_uncertainty,
observed_self_delta_s, observed_external_delta_network_s,
observed_nonparticipant_delta_network_s, observed_all_delta_network_s,
route_changed_count, completed_count_baseline, completed_count_swap,
simulation_source_sha, network_sha, demand_sha, config_sha, eligibility_roster_sha
~~~

Store predicted rows **before** attaching observed outcomes in a distinct immutable file, with timestamp/hash; preserve original route input manifests and raw arm outputs. For retrospective development seeds, record that model parameters were allowed to depend on other development cohorts, and distinguish in-sample vs tuning-partition evaluation.

Do not place realized labels or "future route travel time" in the allowed feature table.

## 7. Training/calibration approach and controls

**E1 queue-aware physics model (first choice):**
- Derive link/turn capacity/storage and free-flow parameters from frozen geometry and independently available development calibration measurements.
- Initialize queues from predecision state or documented prior, not from later truth.
- Calibrate only a small, explicitly enumerated set of interpretable parameters (e.g., saturation flows, junction capacity/turn priorities, queue discharge factor, background-demand uncertainty) on development partitions.
- Separate forecasts of demand inflows from physical propagation; don't let adjustment of unknown background demand silently absorb prediction errors.
- Minimize a transparent development loss combining observed link counts/entry/exit times, target own elapsed time, **other drivers' aggregate elapsed change**, sign of material externality, and physical-invariant penalties. Weight choices must be frozen before formal independent confirmation; do not allow own-ETA fit to dominate the externality objective without reporting that tradeoff.
- Consider multistep forecast stability and partial observability; changes to future queues should flow from the model, not from held-out actual queue records.

**E2 residual correction (only if qualified):**
- Retain the physical base as the counterfactual state engine.
- Use development-only residuals associated with *predecision available* features, e.g., congestion proximity, competing turn demand, queue pressure proxies, and uncertainty ranges. No future realized waiting/trajectory from validation arms.
- Freeze feature set, version and coefficients; compare E2 **incrementally** against E1 and B0–B2 on development-check seeds. If improvement is unstable or appears only on previously inspected probes, discard E2.

**Parameter identifiability:** Multiple capacity/turn/queue assumptions could explain the same aggregated trip times; inspect which parameters are separately constrained by observed flow/occupancy and disclose unidentifiable combinations. Do not label one calibrated coefficient as a uniquely measured intersection capacity without appropriate evidence.

## 8. Development diagnostics, not a substitute for scientific validation

Report **both magnitude and direction**, not just a single regression score:

### A. Forecast skill and risk

- Seed-level mean absolute error (MAE) and signed bias of **pred_external** in network-seconds, compared with zero-externality B0, old B1 and own-only B2.
- Sign agreement on effects exceeding a **prospectively chosen materiality/noise floor**; count near-zero/abstained effects separately, never assign false correct signs to zeros. Report predicted-benefit/realized-harm and predicted-harm/realized-benefit confusion.
- Ranking of candidate swaps by **actual external effects**, including pairwise ranking mistakes and selected-option regret where possible.
- Own ETA change accuracy **separately** from externality accuracy; report whether improving own ETA masks weak external effect estimation.
- Prediction interval coverage, calibration and sharpness for self, external and nonparticipant effects; if uncertainty methods are unvalidated, label ranges provisional.
- Impact on consenting and nonconsenting driver subgroups and the distribution of simulated individual harms (>30-second historical continuity threshold as a diagnostic, not an automatic ethical guarantee).
- Interaction prediction for the two-route bundle: actual joint total minus isolated individual total changes; report whether model can distinguish nonadditive traffic states.

### B. Time and traffic mechanism skill

- Edge-entry-time errors in seconds and 5-/30-second bin agreement, split by forecast horizon, junction exposure and baseline queue level.
- Edge/turn conservation residuals, discharge/receiving cap violations, negative queues, jam storage exceedances.
- Edge-level near-stop queue lengths, waiting, turn discharge and spillback onset/extent against **development-only** measured traces; show timing uncertainty.
- Downstream/upstream propagation lag and large-effect cases with unchanged routes; avoid turning correlation into a uniquely established causal bottleneck.
- Separate insertion delay and stopped-time contributions; preserve tripinfo semantics.

### C. Experiment/inference integrity

- **Independent demand seed** is the unit for reported repeated-sample uncertainty; probe records within seed share the baseline and must be clustered.
- Distribution of errors across seeds and forecast horizons; one result on 1,000 nested driver IDs is not 1,000 independent replications.
- One-time model version and lookahead cutoff; exact counts of failed inputs and incomplete trips; safety exception fields retained.
- Runtime/memory and cost per one-driver swap, per bundle and per 1,000 vehicles.
- Compare own/external decomposition on the old equal-freeflow route cases **as a smoke test only**, with explicit development-contamination label.

### D. Suggested development-only readiness gates (not a validation PASS)

Before requesting a new independent validation protocol:
1. **Every physical and data-integrity unit test passes**, including the explicit equal-own-time/nonzero-externality toy case and absence of the old forced identity.
2. Realized labels and predictor features remain separated by timestamp and immutable files; no simulation future values are read as prospective features.
3. All scheduled development paired arms required for reporting have matched demand, valid connected routes, complete identities, and reconciled scheduled-to-arrival costs.
4. E1 beats B0 and frozen B1 on a **predeclared primary externality-error measure** on the development-check partition, with results shown by seed and with unchanged severe false-benefit diagnostics. A development improvement only authorizes proposing **independent validation**, not policy Test B.
5. Directional skill, false-benefit rates, uncertainty coverage, bundle interaction and own-time prediction are all reported, including negative and inconclusive findings.
6. The estimator can produce distinct self and other predictions under capacity/queue changes and returns a documented abstention when predictions are unreliable.
7. Inference cost is measured and feasible for the intended **offline research** footprint; claim no mobile deployment feasibility.
8. Candidate model/features and acceptance thresholds for the **future independent validation** are proposed and frozen **before fresh confirmatory labels are viewed**, with any changes to the old Test A 60% gate explicitly justified as a new prospective study rather than retroactive rescue.

If any required integrity item fails, report **DEVELOPMENT NOT QUALIFIED**. If numerical skill is weak, report a model limitation; do not invent a success by changing probe subsets or thresholds after observing results.

## 9. Independent validation — required next milestone but explicitly NOT executed here

The **next separate scientific protocol** will:
- select genuinely fresh independent demand seeds and one-/two-swap comparisons, with a fixed sampling frame, different from historic 4101–4105 and new 5101–5114 development seeds;
- predeclare the candidate E1 or E2, version/hash, input contract, uncertainty method, sign definition, materiality threshold, sample size/power plan and practically meaningful improvement criteria **before any holdout SUMO execution**;
- produce immutable prospective predictions before calculating or revealing paired SUMO counterfactual outcomes;
- assess whether sign, magnitude, bias, candidate ranking, bundle nonadditivity, high-impact false-benefit errors and realized subgroup harms improve over B0–B2 with seed-level uncertainty;
- make a **PASS / FAIL / INCONCLUSIVE** independent scientific decision, with failed results published unmodified;
- keep Test B's separate matched demand seeds sealed until an independently validated estimator is frozen.

**The original Experiment 007 60% Test A gate is historical.** A new independent-validation threshold should not be selected simply because 40% failed or the development performance suggests it is easy. Derive thresholds from decision consequences, noise resolution, false-benefit risk, seed-level variance and explicit intended policy use. Do not claim a validation PASS without a predeclared whole criterion set and sufficient independent replicates.

## 10. Future Test B interface and individual fairness (no Test B now)

After an independently validated version is frozen:
- reuse the **same candidate routes, same announced demand, same network information, same forecast horizon and same safeguards** for a comparably informed independent traffic-aware routing baseline and cooperative externality-aware routing;
- make the **objective**, not information access, the studied difference;
- cooperative candidate impact can be represented as **pred_self + pred_external**, subject to opt-in eligibility, valid routes, prospective own-burden caps, predicted risk and computational constraints;
- measure actual scheduled-departure-to-arrival total time for **all vehicles**, not only participants, using new matched seeds;
- separately report realized participant and **nonparticipant** delay distributions, tail harms and predeclared severe-harm/exception gates; a positive mean without fairness is not a joint success;
- do not label a sequential heuristic globally system-optimal without proof; do not claim to outperform live Google Maps, Apple Maps or Waze based on a synthetic comparator.

The estimator must be able to **abstain from a risky reroute** when uncertainty, fairness or the lack of a trustworthy distinct externality signal makes its benefit ambiguous. A predicted external gain is not guaranteed realized fairness.

## 11. Implementation boundaries, repository architecture and outputs

**Proposed logical modules, to be authored only with separate implementation authorization:**

~~~
research/externality_estimator/
  schema.py                  # scenario identity, timestamped allowed inputs
  candidate_routes.py        # fixed, legal routes; no new outcome-based choices
  state_estimator.py          # t0 occupancy, inflows, background demand
  link_turn_queue.py         # finite-capacity conservation and junction discharge
  counterfactual_rollout.py  # baseline and one-swap predicted evolutions
  externality_outputs.py     # separate target and other/opt-out deltas
  uncertainty.py             # bounds/abstain/seeded risk
  baselines.py               # zero, frozen quadratic, own-only
  label_builder.py           # offline SUMO matched counterfactual labels
  audit.py                   # leak guards, hashes, seed partitions, uncertainty
  tests/                     # physical, algebraic and data integrity fixtures
~~~

**Deliverables for the development milestone:**

1. A model/assumption register with every feature's availability timestamp, source and failure mode.
2. A technical derivation of finite-capacity link/turn propagation, vehicle journey-time reconstruction and own/external counterfactual decomposition.
3. Fixed candidate route and information contracts compatible with the later equal-information independent baseline.
4. Automated unit/integrity tests covering conservation, capacity, queue spillback, zero/no-route cases, nonadditivity, risk and equal-own-cost but nonzero-externality counterexamples.
5. Frozen *development-only* data manifest, selected seeds/probes and resource footprint (not authorized by this document).
6. A reproducible benchmark comparing B0–B2 to E1 (and optional separately justified E2), with per-seed metrics, signs, false-benefit and uncertainty diagnostics.
7. Complete provenance: original data/source SHA, pinned SUMO image, deterministic configurations, observed-label and precomputed-prediction hashes, calibration record, raw artifacts/retention and parameter changes.
8. A candid **DEVELOPMENT QUALIFIED / NOT QUALIFIED / INCONCLUSIVE** report, stating whether an unseen validation study is scientifically justified and what its predeclared gates should measure.

**No hidden work:** This document itself authorizes **no GitHub Actions simulation dispatch, code implementation, parameter training, alteration of frozen Experiment 007 reports, or social posting**. It is a design contract. An implementation freeze and source-review milestone must precede any new development simulations. A separate independent validation freeze and decision must precede Test B.

## 12. Falsifiable failure cases and alternatives

The project must publish a negative result if:
- externality predictions remain a fixed function of own-time predictions on essential physically coupled cases;
- queues or capacity constraints violate conservation or cannot explain time evolution from allowed information;
- new estimates perform no better than the zero-externality or frozen proxy benchmarks on the development-check cohort;
- sign/magnitude forecasts appear accurate only after using hidden future observations or directly fitting already-seen 4101/4102 mechanisms;
- severe predicted-benefit/actual-harm mistakes or nonparticipant harms remain large/uncertain;
- uncertainty ranges become so wide that almost all feasible interventions require abstention;
- candidate evaluation exceeds practical offline computation at the intended problem size;
- the physical parameters needed are unidentifiable under realistic predecision observations.

If a prospective marginal estimator proves infeasible, the project should reconsider **timing-only coordination** or another bounded mechanism rather than blindly refining an invalid traffic model. Such a switch requires a new hypothesis, equal-information baseline and human feasibility/consent review.

## 13. Prior art and documentation, carefully distinguished from our evidence

- [SUMO dynamic user assignment documentation](https://sumo.dlr.de/docs/Demand/Dynamic_User_Assignment.html): illustrates why independent shortest-path and equilibrium assumptions differ from network-wide route choice; it does not establish this estimator's skill.
- [SUMO automatic routing documentation](https://sumo.dlr.de/docs/Demand/Automatic_Routing.html) and [routing behavior](https://sumo.dlr.de/docs/Simulation/Routing.html): current/recent information and future time-dependent travel-time estimates; the equal-information independent control must be credible, not a free-flow strawman.
- [SUMO lane/edge traffic measures](https://eclipse.dev/sumo/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html): units and semantics for occupancy, entered/left flow, waiting and interval collection. Detector output is **retrospective ground truth**, not automatically available at t0.
- Mehrabipour and Hajbabaie, *Distributed Methodology for a Cell-Transmission-Based System Optimal Dynamic Traffic Assignment*, published online 2024, [DOI 10.1177/03611981241292339](https://doi.org/10.1177/03611981241292339): prior art motivating explicit time-dependent flow conservation and the computational tradeoff; **not evidence that our proposed E1 has been implemented, calibrated or validated**.
- [SUMO public documentation](https://sumo.dlr.de/docs/): current online documentation may differ from the pinned **SUMO 1.28.0** used historically. Verify all prospective simulator options against the pinned image before future execution.

## 14. Final scientific decision

**SPECIFICATION COMPLETE; DEVELOPMENT NOT STARTED.**

The recommended next engineering-science artifact is a **frozen E1 counterfactual queue-model implementation and development protocol** based on this document, with the explicit identity-breaking fixture, a legitimate prospective information contract and a bounded development-only simulation budget. Only after its implementation and development checks pass should a new, independently frozen externality-validation study be considered.

The scientific sequence remains: **develop a better estimator → independently validate it on fresh unseen traffic counterfactuals → consider Test B only if validation succeeds, under equal information and realized individual fairness safeguards.** The evidence currently supports the *need* for a better estimator, **not the success of one**.
