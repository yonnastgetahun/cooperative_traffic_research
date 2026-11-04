# Post–Experiment 007 / E1 Stage 1D — Physical-Mechanism Failure Investigation
## Prospective scientific specification and staged evidence plan v1

**Written:** November 3, 2026
**Status:** INVESTIGATION SPECIFICATION / ANALYSIS PLAN ONLY. NOT executed. Not a change to E1, its Stage 1D qualification rules, or any previous model predictions.
**Authorization boundary:** The user authorized developing and publishing a prospective investigation of the E1 development failure. This document does NOT authorize source-code changes to E1, new SUMO simulations, recalibration, a replacement E2 model, a fresh estimator-validation cohort, Test B, or social-media publication. Each future execution stage requires separate approval after its scope and protocol are frozen.

### Scientific question

**Why did a queue-aware model that passes conservation and counterfactual bookkeeping tests predict very small marginal effects on other travelers and almost no bundle interaction, when the frozen Stage 1D SUMO scenarios showed large network responses?**

The investigation must distinguish (1) verified source and physical-model simplifications, (2) directly observed simulator traffic dynamics, (3) mismatch between E1's latent state and retrospective SUMO measurements, and (4) a demonstrably causal defect. A plausible mechanism, visual correlation, or parameter story is not a uniquely identified cause.

**Permanent unchanged disposition:** Original Experiment 007 Test A = NO-GO; E1 Stage 1D = DEVELOPMENT NOT QUALIFIED; independent estimator validation = NOT STARTED; cooperative routing Test B = NOT RUN.

---

## 1. Frozen evidence, failure description and provenance

Read-only sources of truth:

1. [Original E1 development specification](POST_EXP007_PROSPECTIVE_NETWORK_EXTERNALITY_ESTIMATOR_DEVELOPMENT_SPEC.md); [frozen E1 Stage 1B executable development protocol](POST_EXP007_E1_EXECUTABLE_DEVELOPMENT_PROTOCOL_V1_2026-11-03.md).
2. [Stage 1C implementation verification](POST_EXP007_E1_STAGE1C_IMPLEMENTATION_RECORD_2026-11-03.md), [Stage 1D source and physics review](POST_EXP007_E1_STAGE1D_SOURCE_AND_PHYSICS_REVIEW_2026-11-03.md).
3. [E1 Stage 1D final independent archive audit](POST_EXP007_E1_STAGE1D_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-03.md) and permanent compact [per-probe](results/exp007_e1_stage1d_devcheck_probes.csv), [per-seed](results/exp007_e1_stage1d_devcheck_seed_mae.csv) and [bundle](results/exp007_e1_stage1d_devcheck_bundles.csv) tables.
4. [Durable original Stage 1D scientific evidence release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1-stage1d-development-2026-11-03), including **706 SHA-256-verified extracted members**, the 60 original SUMO-arm tripinfo files and corresponding model predictions and summaries. Source [workflow 41737336992](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41737336992), frozen development source commit **05b770cf000f84677524e0a1e89bea06ec0e703b**.
5. For historical context, [Experiment 007 P0–P3 structural investigation](POST_EXP007_EXTERNALITY_ESTIMATOR_P0_P3_FINAL_SCIENTIFIC_REPORT.md) and the [six-run time-resolved replay](POST_EXP007_SIX_RUN_INSTRUMENTED_REPLAY_FINAL_SCIENTIFIC_REPORT.md). Those six retrospective replays came from *different scenarios* and must never be treated as unseen confirmation of E1.

### Result to explain, not re-score

On the four already inspected development-check seeds **5111–5114**, the mean of the four seed-level singleton externality MAEs was:

| Predictor | Archived development-check mean externality MAE |
|---|---:|
| B0 zero externality | 1,555.875 network-seconds |
| B1 old frozen assigned-demand proxy | 1,555.267549 network-seconds |
| E1 queue-aware model | 1,555.125 network-seconds |

E1's **0.00917%** improvement over B1 failed the frozen minimum **5%** development gate. E1 also produced **two predicted benefits that were observed as large harms to other travelers**, a separate mandatory gate failure:

- 5111 probe2: **−4 predicted** versus **+2,567 observed** network-seconds of externality.
- 5114 probe2: **−6 predicted** versus **+3,945 observed** network-seconds of externality.

Across 16 single swaps, E1 predicted externalities from **−6 to +21**, while actual externalities ranged **−2,267 to +3,945 network-seconds**. Its mean absolute predicted externality magnitude was only **3.625 network-seconds**, compared with **1,555.875** mean absolute realized magnitude. The four observed bundle interactions were **−3,424, −2,839, −383, −799 network-seconds**, against E1-predicted **0, 0, −7, 0**. The bundle selector assigned **zero forecast overlap** to all four checked bundles. The failures could involve weak timing, incorrect network response, lack of modeled shared junction conflict, route-choice coverage, or several issues simultaneously.

**Inference caution:** 16 route probes share four independent seed baselines. The four independent **demand seeds**, not the 16 probes or 16,000 nested driver records, are the replication units. The 5111–5114 responses are already inspected and can be used only for **retrospective failure diagnosis**; they are no longer unseen development-check observations for any redesigned version.

## 2. Frozen implementation facts to be audited

Use exact **Stage 1D source commit 05b770c** for factual source claims. Read current main only as a convenience when its file blob SHA is independently confirmed identical. No edits to frozen E1 source during the archive-only phases.

- The static SUMO input adapter reads external directed roads, legal edge-to-edge connections, and announced trip/route files. It assigns every turn the same **conflict_class='all'** within a synthetic priority junction; it does **not** reconstruct SUMO's full lane-specific priorities, foe/response bitsets or actual multimovement compatibility.
- In the deterministic queue engine, **used_conflicts** is a per-tick set. Once a movement uses a given (junction, conflict class), another movement in that class cannot cross in that tick, even if those turns could coexist in real simulator behavior. The class is conservative; whether it explains the observed *direction* or *scale* of E1's specific externality errors is **not yet established**.
- Each directed road has one FIFO occupancy queue and finite storage; head-of-line constraints can block vehicles behind a turn that cannot discharge. The model does **not** track lane-specific turn queues, lane changes, within-edge positions or shock-wave movement.
- The model integrates in **one-second ticks**, applies a minimum travel-time eligibility clock and source-insertion capacity, uses global q_sat service tokens and finite receiving slots, and pairs two full predicted network evolutions. Its outputs are made from all driver identities and reconcile self, others and nonparticipants; mathematical decomposition is already verified.
- Nominal global **q_sat=0.50** was selected **using DEV_BUILD only**. Values 0.50 and 0.65 tied on build MAE. This weak build sensitivity motivates scrutiny of controlling junction conflict/service caps, but does not show which constraint actually bound the predicted counterfactuals.
- The Stage 1D original evidence includes 5-second **edgeData and laneData** SUMO observations. No complete 1-second Stage 1D FCD trace or prospective E1 edge-time trace is established from the original audit report alone. **P0 must inventory actual members first**; absence of an output means no claim about that measurement. The previous six-replay FCD covers other historical seed/arm combinations and is not a substitute.

**The core methodological risk:** Fixing the code after viewing its failures and then reporting improved fit on these exact seeds would be contaminated development fitting. This plan separates observation and hypothesis formulation from any future **prospectively frozen** implementation and new test cohort.

## 3. Falsifiable mechanism hypotheses and distinguishable predictions

### H1 — Junction conflict and discharge misrepresentation

**Proposed mechanism:** A one-movement-per-junction-per-second approximation treats some simultaneously compatible priority movements as mutually exclusive, changes discharge allocation and queue growth, and makes route-swap counterfactuals insensitive or wrong-sign.

**Source-grounded prediction:** A frozen-source readback will demonstrate when the 'all' class prevents a second otherwise legal movement within the same tick. On small deterministic networks containing explicitly compatible and explicitly conflicting turns, model service differs from a connection-aware compatible-movement reference. In observed SUMO development-arm edge/lane data, locations with high or competing turn demand may show throughput, occupancy and waiting patterns inconsistent with the coarse E1 junction service assumption.

**Would count against H1:** Compatible movements are scarce at affected junctions/times, or corrected **diagnostic-only** service accounting does not coincide with a meaningful fraction of E1's pressure mismatch. Even a source-level defect is not automatically proof that it generated +2,567 or +3,945 network-second errors.

**Important nuance:** The tested synthetic grid's junctions are **priority** controlled. Do not ascribe a signal-phase problem to this study unless actual signal control is verified in the input network.

### H2 — Link-wide FIFO and finite-storage propagation mismatch

**Proposed mechanism:** One queue for an entire directed edge, with a single head-of-line turn, cannot describe distinct lane-specific queues or within-link shock-wave propagation. It may impose unrealistic blockage or miss how one perturbation affects travelers with unchanged routes.

**Predictions:** Archived edge/lane waiting and occupancy differ in ways that are inconsistent with an E1 single-lane-aggregated queue, including substantial lane-to-lane variation and queue persistence/discharge changes in the five-second data. E1 may underrepresent the number of affected vehicles, the delay duration or the spatial influence region.

**Would count against H2:** Lane-level queue/flow differences are small after reconciling per-lane semantics and observation coverage, or E1's mismatch persists on controlled no-lane-choice toy networks where FIFO is physically appropriate.

**Limit:** Detector waiting, occupancy and stop measures are not automatically exactly equivalent to E1's queue-head waiting counter or effective vehicular delay. Reconciliation must define units, denominator, vehicle presence/absence and the effect of internal junction edges.

### H3 — Route-entry clock, insertion and time-grid mismatch

**Proposed mechanism:** E1's one-second eligibility rounding, source admission, edge-travel timing and common t0 demand may shift when traffic reaches a contested junction, producing large secondary impacts even if own ETA changes are small.

**Predictions:** When comparing only compatible measurements, large disagreement in actual edge entry, aggregate edge occupancy and within-scenario insertion time precedes or accompanies queue/discharge differences. A difference of one tick that moves a critical junction arrival across a busy period might have amplified effects in the SUMO environment.

**Would count against H3:** Timing alignment is accurate at decisive bottlenecks but forecast externality magnitudes remain compressed, suggesting the source of error is downstream response physics or interaction modeling.

**Limit:** The Stage 1D 5-second detectors may support interval flow and waiting analysis but may not identify per-vehicle first-entry timing. **Do not pretend that 1-second FCD exists in this cohort unless the archived file inventory confirms it.**

### H4 — Nonadditivity and unrecognized shared influence

**Proposed mechanism:** Prospectively scored edge-time overlap of intended routes is not a sufficient indicator of *indirect* interaction through receiving capacity, queue spillback or alternate turns. The pair of modified routes can affect the same downstream drivers even without direct predicted edge-time overlap.

**Predictions:** Observed bundle-minus-singles differences will have distinctive temporal/spatial waiting patterns outside the changed route edges, and the affected unchanged-route identities may have different experienced time under each single and joint arm. E1 predicted 0,0,−7,0 network-second interaction on four DEV_CHECK bundles despite material actual interactions.

**Would count against H4:** Reconstructed joint outcome differences are explained by a measurement/accounting artifact, or spatial/time influence patterns are indistinguishable after proper baseline alignment.

**Limit:** All four frozen DEV_CHECK bundle choices had zero predicted overlap score and were thus low-overlap **fallback choices**. This subset was not a balanced or independent random sample of low- and high-overlap pairs. Never generalize its interaction distribution or interpret it as a passed/failed *future prospective* overlap-ranking test.

### H5 — Global parameter identifiability / limited sensitivity

**Proposed mechanism:** The global saturation rate q_sat was not the binding or identifying constraint in key responses, potentially because junction conflict tokens or storage dominated. A near-tie of two q_sat values in build MAE could indicate weak response to this parameter under the frozen model.

**Predictions:** On deterministic model fixtures only, identify the active binding constraints per movement per second (link exit tokens, turn tokens, shared conflict limit, receiving storage, FIFO head eligibility, source admission); parameter perturbations should only change flow when they change a binding constraint.

**Would count against H5:** Distinct q_sat values materially change the same scene's predicted link/turn flows but effects cancel at the global MAE summary. In that case the apparent tie may be aggregate averaging, not a lack of sensitivity.

**Limit:** No claim of a uniquely identified saturation rate or physical road capacity follows from three candidate settings and six build seeds.

## 4. Staged execution plan and scientific stop gates

### P0 — Evidence preservation and observation-contract inventory (archive only)

**Inputs:** release ZIP, all 706 SHA-ledger entries, frozen source at 05b770c, 10 scenario manifests, 10 prediction-locks, 22 parameter-specific prediction files, 60 matched tripinfo outputs and available edge/lane detector files.

**Operations:** Recheck file SHA256, demand and route fingerprints, per-driver completion; inventory files and their actual XML tags/attributes, interval coverage, detector units and whether optional FCD/vehroute outputs exist. Reconstruct DEV_BUILD and DEV_CHECK boundaries and check route-change counts; do not merge previously separate outcome labels into predictor features. Record missing outputs explicitly.

**Gate P0:** If a required original ZIP member is missing, hash fails, a checked 1,000-driver identity set is incomplete or source/label lineage is ambiguous: **STOP interpretive mechanism claims**, report integrity failure. Stage 1D NO-GO remains unchanged regardless.

### P1 — Static junction/connection and source-constraint audit (archive and code only)

**Operations:** Enumerate priority junction types, connections, lanes and per-connection metadata (including raw request/foe/response/index fields **where present**, with semantics independently checked against pinned SUMO 1.28.0). Compare static potential compatible movements to E1's per-junction single 'all' conflict class. Extract and audit exact E1 \`used_conflicts\`, link/turn service token, FIFO and snapshot receiving ordering. Build a **non-simulating** static compatibility register: per junction, legal movement pairs that may be simultaneously compatible, unknown or incompatible; no invented signal cycles.

**Gate P1:** If conflict compatibility cannot be derived reliably, label movement semantics **UNKNOWN** and do not claim a precise capacity defect from static data alone. Publish a parser/metadata limitation rather than guessing.

### P2 — Frozen-data traffic-state difference map (existing SUMO outputs only)

**Operations:** For each completed seed pair, compare at matched **5-second time/edge/lane windows**: recorded waiting, vehicle throughput, occupancy, speed and any available stop measures. Separate internal vs external edge groups, empty-interval handling and vehicle arrival/insertion summaries. Avoid summing an interval statistic across intervals unless its definition permits that aggregation; retain per-interval counts and durations. Compare baseline, each singleton and each two-swap bundle within **the same seed**. Track prospective target route differences and unchanged-route driver effects using the existing 1,000 matched tripinfos.

**Prespecified case map (selected after outcomes, explanatory only):**
- 5111 probe2 (predicted −4, realized +2,567 other network-s);
- 5114 probe2 (predicted −6, realized +3,945 other network-s);
- 5113 probe1 (large realized benefit on others with small positive E1 forecast);
- seed 5111, 5112, 5113 and 5114 bundles for joint interaction;
- retain the complete 60-arm table for context and to avoid cherry-picked numerators.

**Gate P2:** If a physical queue/discharge claim requires FCD or per-vehicle stop/edge arrival data that the original archive did not collect, stop at a **5-second aggregated observation** and define what additional passive measurements would be needed. No synthetic reconstruction of unobserved queues may be presented as a fact.

### P3 — E1 state accounting and mechanism-discrimination fixtures (NO SUMO)

Use the exact frozen E1 source and identical static input on toy/small networks. **Do not change or re-train E1.** Generate model-internal trace of snapshot receiving slots, eligible FIFO heads, turn/link/service tokens, junction conflict occupancy, source insertion and per-tick queue counts. These traces are **retrospective diagnostic computations**, not contemporaneously frozen predictions for the inspected Stage 1D cases and **must not be used as new validation claims**.

Fixtures:
- Two nonconflicting legal turns at the same junction; verify E1's one 'all' conflict-class cap and its throughput implication relative to independently specified physical compatibility.
- Two truly conflicting turns sharing a lane/receiving pool; verify that independent compatibility accounting cannot exceed finite sending/receiving capacity.
- Lane-specific downstream receiving obstruction versus the existing single FIFO head; map which unchanged-route drivers' predicted journey times are influenced.
- Timing shifts of ±1 model tick around a constrained turn; show whether the predicted response is discontinuous and whether that implies a feasible amplification mechanism.
- Two different-route targets with zero direct edge overlap but shared downstream influenced junction(s); test whether actual joint model rollout produces nonadditivity.
- Global q_sat fixture values 0.35, 0.50 and 0.65; count how often link tokens, turn tokens, junction conflicts, receiving slots, source admission or FIFO eligibility are binding.
- No-leakage, source-byte-identity, legal routes, mass conservation, nonparticipant accounting, deterministic readback and missing-data abstention.

**Gate P3:** A toy fixture showing a structural defect is **source/physical-model evidence only**. A revised junction algorithm must not replace frozen E1 in these outputs. Any improved toy outcome is not an improved development MAE.

### P4 — Explicit hypothesis adjudication and prospective follow-on decision

Produce one matrix by H1–H5 with: source evidence, independent archived SUMO observation, compatibility of units/clocks, alternative explanations, status (**SUPPORTED AS DESCRIPTIVE / CONTRADICTED / INSUFFICIENT / CODE DEFECT VERIFIED**), and the *smallest new prospective discriminating experiment* required to identify a causal effect. Count source-level and observed-in-SUMO claims separately. Rank hypotheses by strength of direct evidence and the computational cost of discriminating tests, not by how much they might retrospectively improve E1 MAE.

**Final scientific exit:** (a) validated old-artifact reconciliation, (b) named physical assumptions with clear evidence limits, (c) verified source-invariant/compatibility defects if demonstrated, (d) proposed versioned E1-v2 design changes and independent development data requirements, (e) a decision to pursue additional controlled work or stop. No automatic upgrade to Stage 2 or Test B.

## 5. Possible new controlled work — explicitly NOT authorized

If P0–P4 show insufficient recorded physical resolution, propose a **separate frozen, instrumented replay protocol** before running it. A minimal *candidate* for review is two previously observed false-benefit seed/arm pairs (seed 5111 I/probe2 and 5114 I/probe2), **four original-route replays**, adding passive 1-second FCD/edge-exit time traces and preserving all old trip outcomes to strict per-driver tolerances. These are post-outcome-selected **explanatory** repeats, not fresh estimator validation. Their exact simulator command, hashes, observation flags, original-tripinfo equivalence thresholds, raw retention and stopping conditions must be frozen in a separate execution specification, and approved before dispatch.

If the goal instead is to distinguish a particular physical parameter or junction conflict *causally*, specify a **controlled simulator capacity/connection intervention** with separate baseline and perturbed arms, changed-physics logs, appropriate same-seed comparisons, predeclared causal estimand and fresh research seeds. Such an intervention no longer tests the original unchanged physics and cannot be folded into the old Stage 1D score.

To **evaluate a modified E1-v2**, first write a new prospective design and implementation freeze **without using** DEV_CHECK 5111–5114 or original 4101–4105 as untouched holdout. Collect a separate development build/check cohort; the redesigned model must predict before counterfactual labels, pass new diagnostics and false-benefit controls, and only then be considered for independently frozen Stage 2 validation. No new seed IDs, numerical PASS thresholds, experiment count or route-optimization effects are authorized or silently implied by this current specification.

**Never use hidden new SUMO executions to debug E1-v2 within this archive investigation.**

## 6. Required reproducibility deliverables for separately approved execution

1. **Evidence manifest:** frozen GitHub source SHA, archive/release URL, 706-member SHA ledger, exact seed and arm subset, original E1 model parameter version, and every time/feature coverage limitation.
2. **Junction compatibility and bottleneck register:** link/junction IDs, raw SUMO connection metadata, E1 conflict group, compatible/unknown alternatives and documented evidence; no invented actual right-of-way behavior.
3. **Edge/lane/time observations:** 5-second interval differences and route-difference fingerprints, with distinct measures for sampled waiting, speed, occupancy, entering/leaving and internal-connection behavior; original read-only data only.
4. **Source-constraint audit:** deterministic toy fixtures and reproducible binding-constraint counts; no editing or retraining of original E1.
5. **Hypothesis matrix:** H1–H5 supported, contrary and missing evidence, causal inference limits and prespecified smallest future discriminating intervention.
6. **Complete scientific report and machine-readable tables:** negative, inconclusive and unsupported findings included; original externality/MAE and false-benefit values copied from permanent verified audit as prior facts, never relabeled as new independent test.
7. **Durable archiving:** review and verify raw and derivative artifacts, SHA hashes, report source and final disposition. No social publication without separate permission.

## 7. Safety, fairness, and scientific interpretation

- **No retrofit of frozen conclusions:** E1 DEVELOPMENT NOT QUALIFIED and original Test A NO-GO remain the published scientific decisions, regardless of any later explanation of failure.
- **No prospective outcome leakage:** Existing 5111–5114 and 4101–4105 cases are **retrospectively inspected**. They cannot be used to claim generalization from a redesigned predictor.
- **No social objective or optimization:** This investigation does not assign new cooperative routes, shift departures, alter signals, control vehicles or compare collective policies.
- **Nonparticipants remain visible:** Track effects on unchanged-route and nonparticipating drivers. A small predicted own-time effect is not evidence of little external harm; fairness is not a single average.
- **Synthetic scope:** This work concerns a 10×10 synthetic SUMO priority-junction system. Neither E1's conservation tests nor simulator safety statistics imply human safety, consent or navigation advantage.
- **Uncertainty is an outcome:** If archive metrics do not distinguish H1–H5 or a unique physical cause, state that precisely. Do not infer a traffic bottleneck from spatial correlation alone.

**End of current authorization:** The protocol is ready for prospective review and publication as a plan. **P0–P4 have not yet been executed under this plan, and no new simulations, model modification, independent validation or Test B have begun.** The next proposed action is **P0 archive inventory and read-only source audit**, only after separate authorization to execute this investigation.
