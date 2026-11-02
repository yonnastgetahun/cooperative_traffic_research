# Experiment 007 — Two-test scientific design note: externality prediction versus realized network optimization

**Date:** 2026-11-01  
**Status:** **Prospective design refinement, not a frozen protocol, implementation authorization, simulation authorization, or empirical result.**  
**Decision:** Keep the [comparative mechanism assessment](COORDINATION_MECHANISMS_COMPARATIVE_ASSESSMENT_AND_EXP007_DIRECTION_2026-11-01.md) as the mechanism-selection record; make the **marginal prediction / policy efficacy separation explicit** before freezing Experiment 007.

## 1. Why two separate scientific claims?

- **Mechanism-estimation claim (Test A):** A prospective model, given available pre-assignment information and alternative feasible routes, can predict the **sign, approximate magnitude, or relative ranking** of *network externalities* produced by a bounded route change. This is tested against matched, controlled counterfactual SUMO outcomes. Accurate **chosen-route road-entry times** (Exp003) do not establish such accuracy. Correctly measuring the effect of a **single route perturbation** does not prove that a policy jointly changing hundreds of routes is optimal or effective.
- **Collective-policy claim (Test B):** An implementable externality-aware assignment policy, using a frozen estimator, yields **lower realized total network travel time** than a comparably informed, independently traffic-aware assignment policy on **new, independent matched simulation demand**, with prespecified realized-harm protections. Even a sufficiently accurate marginal model does not guarantee this outcome because of nonadditivity, sequential decisions, feedback, objective mismatch, capacity limits, and compliance.
- **Inference discipline:** Mechanism prediction alone ≠ route optimization. Improved aggregate performance alone ≠ proof of accurate marginal estimates or globally optimal routes. Test A estimates a local causal contrast **within SUMO under fixed initially assigned routes**; Test B estimates a whole-policy causal contrast **within SUMO under matched demand**. Neither establishes real-road benefits.

**Historical motivation:** Exp006's mean A−E advantage +0.2429s (95% CI −1.9120 to +2.3978s) was inconclusive; 27.98% of high-congestion matched drivers experienced >30s extra E−A time, failing the study-specific fairness guardrail. Its A baseline used **nominal free-flow shortest paths**, not a contemporary traffic-aware navigation model. Archived severe harms were associated with +57.17s additional stopped/near-stopped waiting in the selected harmed cohort, and 882 affected drivers kept the exact same road-edge sequence. These are observations, not identified causal bottlenecks or marginal-cost estimates. See [Exp006 final report](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md) and [archived harm analysis](EXPERIMENT_006_ARCHIVED_SEVERE_HARM_MECHANISM_ANALYSIS.md).

## 2. Define exactly what is minimized

Let N=1,000 scheduled drivers with fixed demand, network, departure commitments and route assignment vector \(\mathbf r=(r_1,\ldots,r_N)\). Define **realized** network cost

\[
C(\mathbf r) = \sum_{i=1}^{N} T_i(\mathbf r), \qquad
T_i = a_i-d_i^{scheduled}
\]

where \(a_i\) is **actual simulated arrival time**, and \(d_i^{scheduled}\) is **scheduled departure time**. Under SUMO outputs this generally corresponds to completed-trip duration **plus departure/insertion delay**, subject to verifying original field semantics. This prospective choice avoids moving waiting outside the counted trip measure. Departure shifts are **not permitted** in Experiment 007, so no separate scheduling-utility objective is introduced. Report historical-style \`tripinfo.duration\` as a separate, explicitly labeled secondary measure for comparison with Experiments 001–006.

Optimization uses **predicted** whole-network elapsed costs \(\widehat C(\mathbf r\mid\mathcal I)\), not realized evaluation simulator outputs:
\[
\mathbf r^S \approx \arg\min_{\mathbf r\in\mathcal F}\widehat C(\mathbf r\mid\mathcal I).
\]
\(\mathcal F\) is the permitted set of feasible routes for eligible participants with route-validity, opt-in, accessibility and candidate individual-harm limits. The actual experiment verifies *realized* \(C\), not the expected objective alone. Use **externality-aware heuristic**, not **globally system-optimal**, unless a mathematical optimality result is independently supported.

For a feasible one-driver replacement \(r_i\rightarrow r_i'\), with the others' **assigned** routes temporarily held fixed, define:
\[
\Delta_i^{all} C = C(r_i',\mathbf r_{-i})-C(r_i,\mathbf r_{-i})
\]
\[
\Delta_i^{self} T=T_i(r_i',\mathbf r_{-i})-T_i(r_i,\mathbf r_{-i})
\]
\[
\Delta_i^{external} = \Delta_i^{all} C-\Delta_i^{self} T = \sum_{j\neq i}\left[T_j(r_i',\mathbf r_{-i})-T_j(r_i,\mathbf r_{-i})\right].
\]
Each has a **prospective prediction** with a hat and a **realized paired-SUMO** analogue. Negative \(\Delta_i^{all} C\) means the replacement saved *total* travel time in that counterfactual. Negative \(\Delta_i^{external}\) means it helped *others*, even if it harmed the rerouted driver. The other drivers' **routes** are fixed in the probe, but their actual time/speed/queues naturally change in SUMO. This is the causal traffic spillover being measured.

**Nonlinearity warning:** \(\sum_i\widehat{\Delta_i^{external}}\) from isolated perturbations is not generally the externality of a bundle of changes: queues, bottlenecks, discharge, and route interactions are coupled. The proposed probe must include at least one **joint bundle** intervention, and the policy test must measure its own whole-network consequences.

## 3. Equal-information independent/cooperative comparison

**Information set \(\mathcal I\) common to both arms at each decision:** same synthetic topology/capacities/control settings, same eligible preshared OD/demand and announced departure plans (under explicit idealized disclosure assumption), same available observed/predicted road-time states, same forecast model and calibration (including forecast clock), same candidate route set, same map of already assigned route-intentions and fixed occupancy updates, same planning horizon, and identical permitted update/replanning cadence. The policy must never see evaluation-run future SUMO travel times or counterfactual outcomes.

**Common decision mechanics:** same feasible candidates and nominal detour bounds, fixed route-assignment order, same number of assignment sweeps, deterministic seed handling, candidate-enumeration procedure and fallback conditions. Compute/resource usage and foresight horizon should be matched when feasible and reported where inherently different. Both arms should use **the same shared prediction engine**: the independent arm may have access to the same externality inputs but **does not optimize their value**. The treatment difference is the **coefficient of the other-travelers term**, not a better predictor, updated calibration, different update clock or larger candidate set.

**Independent traffic-aware control I:** each eligible driver chooses the feasible route with the lowest **own predicted elapsed time** using a time-dependent traffic forecast and the same feedback protocol. This is a **documented, independently traffic-aware pretrip assignment**, not legacy free-flow A and not by definition a modern live rerouting app, dynamic user equilibrium, Google Maps, Apple Maps or Waze.

**Cooperative treatment S:** for eligible drivers, choose among the identical feasible route candidates based on approximate \(\widehat{\Delta C}=\widehat{\Delta T_i}+\widehat{\Delta T_{others}}\), with predeclared prospective constraints on individual burden. All **N** travelers, including **nonparticipants**, count in the social objective. Nonparticipants retain the **same fixed I-assigned road-edge sequences in both policy arms** in the minimal *one-shot pretrip* test; this isolates physical network spillovers without a second adaptive-rerouting mechanism. Participant route changes may still affect their experienced costs.

**Participation:** 50% prospectively designated eligible vehicles (balanced across OD, departure phase and baseline trip length where possible), same IDs and roster in both arms; 100% compliance **conditional on synthetic eligibility** is a simulator assumption, not empirical evidence of voluntary consent, acceptance or real-world adherence. No demand changes, departure shifts, change in car-following physics, traffic-signal optimization or automated vehicle speed control.

**Control interpretation:** Sharing advance intents with both arms is an **equal-information causal control**, but an idealized disclosure condition. Do not claim the primary comparison directly establishes superiority to any current commercial navigation system.

## 4. Test A: bounded controlled marginal-network-effect probes

**Purpose:** distinguish a genuine anticipatory signal about **others' traffic cost** from better prediction of the treated driver's own route or a static edge-count proxy.

**Source network:** existing 10x10 SUMO grid; high-congestion demand window 200 seconds; 1,000 trips per scenario. Generate a **traffic-aware independent I** baseline route assignment using the shared frozen forward model. On independent **probe seeds**, lock all other initial assignments and perturb **exactly one eligible route** to another valid preselected candidate, then run matched SUMO simulations with unchanged original OD, departures, driver behavior, signals and random settings. Reuse a baseline run within each seed, noting dependence among probes sharing that baseline. Measure \(\Delta_i^{all}\), \(\Delta_i^{self}\), and \(\Delta_i^{external}\) from all realized matched driver times. No counterfactual SUMO outcomes may be fed back to the forecast/policy during the evaluation.

**Smallest bounded screening plan (provisional):** five independent *probe* seeds, four route-swap probes per seed chosen **before observing outcome** to span estimated positive/negative/near-zero externalities and early/late OD contexts, plus one **prospectively defined, small bundle** of plausible interacting swaps per seed. One unchanged I baseline + five perturbation arms = **six SUMO executions per seed; 30 total**. Reuse baseline outputs within a seed for repeated contrasts; estimate uncertainty at the **seed** level, not 25 independent probes. This sparse sample is a **diagnostic screen**, not a broad proof of estimator calibration or every congestion regime. The bundle tests at least a basic violation of additivity. If near-zero perturbations cannot be resolved above simulation variability, report them indeterminate, not incorrect-sign cases.

**Prospective mechanism outcomes:**
- Predicted vs realized **total**, **own**, and **external** changes, with sign conventions and units fixed; retain full per-driver paired differences including nonparticipants.
- Direction/sign concordance only for changes above an independently justified **resolvability/noise floor**, plus magnitude error, signed calibration bias, and ranking/discrimination of beneficial vs harmful feasible changes.
- Explicit comparison with the **own-time-only / zero-externality** predictor (and preferably a trivial assigned-count baseline), to show the externality signal adds predictive information rather than merely repeating self-benefit.
- Bundle predicted joint effect vs realized joint effect and vs **sum of isolated estimates** where corresponding singles are observed; avoid assuming additive marginal effects.
- Document any adverse false-benefit predictions (predicts network benefit; realized network harm), even if average metrics look good.

**Interpretation and gate:** proceed to the whole-policy confirmation only if the frozen estimates demonstrably distinguish at least some materially favorable from unfavorable alternatives **without obvious leakage or sign reversal**, the bundle check does not reveal wholesale unreliability, and route assignment works end-to-end without prohibited changes. Such a small screen is not conclusive proof of marginal-estimator accuracy. Use separate historical/development seeds for debugging/tuning; if probe outcomes are used to change the estimator or select a threshold, repeat independent probe validation before claiming confirmation, or explicitly treat those probes as development-only. Exact quantitative gates must be set **before** running probes; this note does not invent effect-size thresholds.

## 5. Test B: matched-seed realized whole-policy test

**Purpose:** determine whether the **use** of prospective externality estimates improves collective traffic outcomes, not merely whether perturbation forecasts correlate with outcomes.

**Arms (only two primary arms):**
1. **I: independent, traffic-aware control**, using shared predictions and route procedure, own-time coefficient only.
2. **S: externality-aware joint assignment**, otherwise identical, using same estimator and objective changed to predicted network time + explicit predeclared feasibility/fairness protections.

**Smallest provisional confirmatory plan:** 10 *new*, independent matched **policy seeds** in the 200-second high-congestion regime; **two arms per seed = 20 SUMO executions**. Keep these seeds disjoint from **all** development and Test A probe seeds. The earlier experiments' seed-level variance should inform a **prospective power/precision review** before fixing the seed count. Ten is a continuity-based starting point, not a guarantee of enough power to detect a meaningful gain. No opportunistic post-outcome seed additions; if underpowered, predeclare larger N or accept an inconclusive result.

**Primary estimand:** each seed's \(\overline T_I-\overline T_S\), where \(T_i=\) actual simulated arrival minus desired/scheduled departure and all 1,000 same vehicles are included. Report mean paired seed difference, a two-sided 95% interval with **independent seed as the inferential unit**, and total network seconds saved (\(N\times\) mean difference if all vehicles are present and complete). Predeclare the minimum practically meaningful gain \(\delta>0\) and how a positive yet smaller effect should be interpreted. Never pool 10,000 driver identities as if independent seeds.

**Measured secondaries:** historical \`tripinfo.duration\` for comparison, departure/insertion delay (separately; avoid double counting), SUMO waiting and timeLoss (not additive to total cost), time-resolved network discharge, trip completion/censoring, tail absolute-trip-time distribution, changed-route counts, spatial bottleneck congestion where measured, assigned-load concentration only as a diagnostic.

**Fairness/participation outcomes:** paired individual \(T_i^S-T_i^I\) distribution; harmed/helped fraction; p90/p95 individual harm; share with realized delay above a prospectively chosen threshold; separately the **nonparticipant** harm rates, participant harm rates, and adequately populated OD subgroup harms. Verify candidate guardrails constrained **prospective** harm; do not claim such guardrails guarantee **realized** harm. Preserve historic >30-second and 10% threshold as a **clearly labeled continuity sensitivity** unless consciously rejustified and adopted as a **new** decision gate. No subjective comfort, calmness, journey experience or survey outcomes.

**Decision matrix:**
- **A informative; B significant practical benefit and fairness passes:** conditional evidence supporting this externality-aware coordination policy in the tested simulator/regime/participation scenario; not proof of global optimum or real-world superiority.
- **A informative; B fails:** local externality predictions are not sufficient for good collective optimization; investigate coupled assignment effects, heuristics or feasibility, not reflexive recalibration.
- **A weak; B helps:** observed conditional policy benefit but marginal mechanism remains unverified; do not attribute benefit to accurate externalities without discrimination evidence.
- **A weak; B fails or inconclusive:** no validated mechanism or demonstrated collective advantage.
- **B apparent efficiency gain but fairness fails:** **joint success not achieved**, even with positive network mean.
- **B interval covers zero or cannot exclude negligible savings:** inconclusive, not proof of equivalence or failure of all cooperation.

A demonstrable collective claim requires both a prespecified positive / practically meaningful network-level result and prespecified realized fairness success. Changes to thresholds, policy or estimator after seeing confirmatory results require a new independently frozen comparison.

## 6. Smallest study footprint and strict boundaries

**Prospective minimum candidate:** Test A **30 matched-probe SUMO arms** (five seeds × [one control + four singleton probes + one bundle]) and Test B **20 policy SUMO arms** (ten fresh seeds × two arms) = **50 SUMO executions**, *conditional on the precision and model-integrity review*. This is a planning budget, not authorization or a frozen final sample size; a lower budget would require sacrificing probe diversity or seed-level uncertainty. Existing archival data and prior dev seeds should be reused for initial code/model preparation with no fresh runs until an approved frozen protocol exists.

Focus **only on high congestion** initially; medium/lower, alternative topology, vehicle count, other participation rates, imperfect compliance, live rerouting, departure coordination and human-in-the-loop preferences are explicit follow-up tests, **not part of this minimal causal comparison**.

**Required freeze before any simulation:**
1. Specify physical time accounting (including departure insertion delay), correct SUMO field semantics, candidate path feasibility, common forecast information, fixed nonparticipant routes and matching controls.
2. Define how the model computes \(\widehat{\Delta_i^{external}}\) without knowing evaluation future SUMO trajectories; isolate policy objective from forecast quality and clock alignment.
3. Prespecify perturbation selection rules, probe sign/noise thresholds, bundle composition, seed partitions, complete uncertainty procedure, and Test A proceed/stop criteria.
4. Fix I/S routing policies, actual eligibility roster, assignment order, decision cadence and computation comparison.
5. Preregister practically meaningful primary \(\delta\), independent-seed sample size/precision, realized fairness and nonparticipant gates, and all censoring/exception rules.
6. Freeze code/design/results manifest and approve execution separately. Preserve null/negative outcomes and original Exp001–006 reports unchanged.

## 7. What is established versus proposed

**Established in this repository:** chosen-route forecast improvements (Exp003); costly assignment clock inconsistency (Exp005); Exp006 inconclusive network superiority and failed severe-harm safeguard; archival observation of queue-associated realized harm and unchanged-route spillovers.

**Relevant external foundations:** [FHWA DTA fundamentals](https://ops.fhwa.dot.gov/publications/fhwahop13015/sec2.htm) differentiates user/system optimal and information/behavior assumptions; [FHWA DTA validation guidance](https://ops.fhwa.dot.gov/publications/fhwahop13015/sec8.htm) calls for validating model response to changed network conditions; [Jahn et al. (2005)](https://doi.org/10.1287/opre.1040.0197) and [Schulz and Stier-Moses (2006)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=577201) examine system-optimal assignments with user constraints; [Minimizing the total travel time with limited unfairness (2020)](https://doi.org/10.1016/j.cor.2020.105016) illustrates explicit efficiency/fairness tradeoffs. None establishes the proposed project's effectiveness.

**Proposed, not evidenced:** accurate externality ranking in the project's own 10x10 network, practical joint-route improvements, meaningful collective savings over a credible equally informed baseline, opt-in driver acceptance, bounded realized harm under the new policy.

**Publishing:** This conceptual design is a scientific planning milestone, **not an experimental result to publicize automatically**. If later substantive findings warrant LinkedIn/X communication, prepare verified visual-first assets, common reader-friendly GitHub destination, and obtain explicit user approval of media/captions before publication. Subjective journey quality remains intentionally deferred.

---
**Status:** Two-test logic and bounded study proposal defined. **Experiment 007 not frozen, implemented or simulated.**
