# Stage 1B — E1 network-externality estimator: frozen executable development protocol v1

**Date:** November 3, 2026  
**Status:** **Protocol frozen as a design contract; implementation NOT started; no new SUMO simulations, model calibration, independent validation, or Test B authorized in this turn.**  
**Parent document:** [Full prospective estimator development specification](POST_EXP007_PROSPECTIVE_NETWORK_EXTERNALITY_ESTIMATOR_DEVELOPMENT_SPEC.md). This document is the more specific, executable Stage 1B plan, not a repetition of the broader development direction.

## 1. Research question, prior result, and boundaries

The intended estimator predicts how a voluntary route change affects **the selected driver's own actual scheduled-departure-to-arrival time and the summed journey time of all other drivers**. These must be separately derived from an explicitly modeled coupled network, rather than mechanically setting the estimated externality equal to the selected driver's own cost.

The historic Experiment 007 Test A remains **NO-GO**: 8 of 20 correct externality signs (40%) against the frozen 60% gate. P0–P3 established a conditional structural identity, predicted externality = predicted self cost, on 20 equal-free-flow swaps. The subsequent six-run replay reproduced original trips exactly and observed timing errors, waiting differences, and a −2,989 network-second two-route interaction. These are explanatory **historical development diagnostics**, not a validation set for E1. The original conditional Test B was **NOT RUN**.

This document governs Stage 1 **development only**. A new independent estimator-validation study and a later whole-policy Test B each require separate frozen protocols, fresh distinct seeds and separate approval. There is no promise that an improved estimator will pass or that cooperation will outperform independent routing.

**Fairness remains active:** capture predicted effects on nonparticipants and realized participant/nonparticipant harm in development labels. Subjective quality, comfort, and calmness stay deferred. No real-road, mobile deployment or consent evidence is claimed.

## 2. Precise estimands, sign and observable information

For 1,000 announced driver identities, original fixed assignment A0 and one eligible driver's alternate fixed assignment A1, let actual elapsed time of driver j be T_j(A) = actual arrival_j(A) − scheduled departure_j. Define:

- **Own effect:** Δself_i = T_i(A1) − T_i(A0), in individual seconds.
- **Externality:** Δexternal_i = sum over all j≠i of [T_j(A1) − T_j(A0)], in **network-seconds**.
- **Total:** Δall_i = Δself_i + Δexternal_i, in network-seconds.
- **Nonparticipant effect:** Δnonopt_i = sum over original nonparticipant identities j of [T_j(A1) − T_j(A0)].

**Negative** means fewer seconds/benefit; **positive** means added time/harm. No driver can disappear from the denominator. SUMO insertion/departure delay belongs in scheduled-to-arrival time exactly once; in-network waiting is already within journey duration and timeLoss is only a diagnostic.

Before learning a paired SUMO outcome, E1 shall produce prospective predicted baseline and alternate **arrival/elapsed times for each of the same 1,000 identities**, and then sum modeled other-driver changes to calculate predicted externality. The network total MUST reconcile from identities. If either model rollout fails to complete, emit an explicit **ABSTAIN/NONCOMPLETION**, not a completed-only surrogate.

**Information at decision time t0:** identical network, legal connections and capacities, scheduled OD and preannounced route intentions (an idealized full-demand research assumption), frozen eligible/noneligible roster, initial traffic state available by t0, and parameters learned exclusively on development-build data. No post-t0 SUMO FCD, tripinfo, detector queue, future exit time, evaluated probe outcome or held-out label may enter E1 prediction.

## 3. Frozen E1 architecture and physical model

**Model family:** deterministic, link-based, finite-storage, FIFO vehicle/cohort queueing with bounded junction/turn service and receiving constraints, paired counterfactual network rollouts. E1 is an *approximate, forward-looking traffic response simulator*, **not** SUMO itself and not the old static 30-second assigned-demand cost.

**Clock and granularity:** internal updates at **1-second** time steps with 5-second diagnostic aggregation. Each road-edge has explicit free-flow traversal eligibility; queues may accumulate when exits cannot discharge. This is intentionally coarser spatially than a cell-transmission model: it can represent finite-storage upstream blocking but cannot claim to locate precise within-link shock fronts. Historic 30-second forecast bins are not reused as physical evolution.

**Declared E1 priors:**
- For directed edge e: free-flow minimum τ_e = edge lane length / declared speed; exit eligible no earlier than the first discrete step at/after edge entry + τ_e.
- Integer physical storage K_e = max(1, floor(length_e × lane_count_e / 7.5 meters)); 7.5m is an openly stated vehicle-spacing approximation, not an empirical jam-density measurement.
- Nominal link/turn service per compatible lane q_sat = **0.50 vehicle/second**, with the only development-build global calibration candidates **0.35, 0.50, 0.65 veh/s/lane**.
- Service uses fractional **capacity tokens** accumulated per tick; accepting one complete vehicle consumes one token. Token carryover is limited to one second of capacity to avoid unrealistic bursts.
- Turn legality, lane groups and known controls come from the input network. Respect conflict/turn-sharing groups, using an explicitly marked conservative one-conflicting-movement-per-junction-per-tick fallback if conflict metadata cannot be resolved. That fallback requires a model-fidelity audit; it is not a claim to replicate actual SUMO priorities.
- Source-edge admission depends on available storage. An eligible vehicle not inserted stays in a source waiting queue, contributing insertion delay.
- Max simulated horizon **1,800 seconds** from demand start; fail/abstain if any vehicle remains unarrived.

**Synchronous 1-second tick (frozen order):**
1. Read the pre-tick complete network state. Enqueue drivers whose scheduled departure becomes eligible at this tick.
2. Calculate receiving slots R_e = max(0,K_e−N_e) and accrued exit, turn, and junction service. Snapshot capacities are common across all simultaneous contenders.
3. Select eligible **FIFO heads** of inbound links whose minimum free-flow time has elapsed. Allocate legal turns using deterministic sorted-approach round-robin with rotating junction pointer and stable vehicle-ID tie-breaking.
4. Enforce all sending, turn, conflict and downstream receiving constraints jointly, including multiple approaches competing for one downstream link; no downstream double-claim of a slot.
5. Admit source-queued vehicles only within pre-tick remaining source-link receiving budget. Do not reuse a slot freed later within the same tick.
6. Commit all crossings and insertions together. For each link e assert N_e(t+1)=N_e(t)+entered_e−exited_e, 0≤N_e≤K_e, and exactly one location/status per vehicle.
7. Record each arrived vehicle's predicted arrival tick, continue until 1,000 arrivals or horizon failure.

**Physical constraints are hard invariants**, not tunable penalties: conservation of all driver identities, legal turn sequences, no overtaking queue heads, nonnegative links, capacity tokens, bounded storage and no travel faster than the declared minimum edge time.

**Model limitations:** Uniform FIFO on a link may oversimplify turn-lane separation; uncertain signal rules may not be known; the 7.5m storage and saturation-flow priors are not calibrated field observations. A model that needs hidden oracle details of SUMO's future physical queues to work is **not** a prospective predictor.

## 4. Paired counterfactual interface

Frozen public interface (language independent):

    predict_counterfactual(
      scenario [network, announced_demand, initial_state_at_t0, route_intentions, roster],
      selected_vehicle_id, alternative_connected_legal_route,
      model_source_sha, parameter_sha, uncertainty_seed
    ) -> {
      status, input_sha, feature_cutoff_t0,
      per_driver_elapsed_baseline[1000], per_driver_elapsed_swap[1000],
      pred_self_delta_s, pred_external_delta_network_s,
      pred_nonparticipant_delta_network_s, pred_all_delta_network_s,
      prospective_edge_time_and_queue_trace, runtime, uncertainty_status
    }

The **same** source-state estimates, scheduled departures, initial queues, legal routes of others, deterministic priorities and uncertainty draws must be supplied to baseline and alternate rollouts. Only the target's route changes. Derive predicted externality from the **999 individual other-driver counterfactual changes**; predicted total reconciles to self + others within 1e−6s. For a two-target bundle, rerun an actual **joint forward rollout**; do NOT add isolated marginal estimates.

The predictor must be free of SUMO runtime and must never import test labels, historical tripinfo, post-t0 detector outputs or the offline \`label_builder\`. E1 can **abstain** if initial state, legal junction conflicts, horizon completion or prediction reliability is insufficient; no fabricated precise benefit or calibrated interval.

**Baseline comparators (mandatory):** B0 = zero externality; B1 = unchanged historic Experiment 007 quadratic assigned-demand proxy; B2 = own-time-only predictor, with explicitly zero others' effects. E1 = paired queue-aware model. **No learned E2 residual model** in v1.

## 5. Development-only seeds, scenario design and simulation budget

- **DEV_BUILD:** independent demand seeds **5101–5106**, six per seed = **36 SUMO scenario arms**, available to calibrate one global E1 parameter.
- **DEV_CHECK:** independent demand seeds **5111–5114**, six per seed = **24 arms**, used to *assess* the frozen DEV_BUILD-selected model **once**, never to retune it. Development-check results are **not** independent confirmatory validation.
- **Historic 4101–4105**, six instrumented replays, and old Exp001–006: contaminated prior observations, eligible only for explanatory fixtures, not a fresh check.
- **4201–4210**, any future unseen validation seeds and future policy Test B seeds: sealed and unavailable in development.

**Maximum newly proposed development footprint: 60 scenario arms.** Each independent seed has one traffic-aware, fixed-route independent baseline, four prospectively selected single-target swaps (other 999 *planned* routes unchanged), and one prospectively selected two-driver bundle. Same network, 1,000 IDs, demand, departures, car-following assumptions, SUMO random seed and source in all matched arms.

Use **original pinned SUMO 1.28.0 image** digest \`sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb\` and the original synthetic demand-generator commit \`be2e8d27c78c8b6de4891115d6d951edc877ac6e\`. No new optimization, signal control, physical driving manipulation or time-shift decision. Do not launch these 60 arms merely because this document merges.

**Predeclared probe selection (before observing any outcomes):** Generate only legal feasible alternatives under the documented consistent route candidate set. Eligible driver IDs are even-numbered \`veh####\`. Fill four slots: near-equal nominal free-flow difference (≤0.5s) early scheduled departure (<100s), near-equal late (≥100s), different nominal free-flow difference (>0.5s) early, and different late. Use stable SHA-256 of seed, slot, target ID and candidate-route hash to select one unique driver for each slot. If a slot is empty, fill from the next nonempty slot following the fixed priority equal-early, equal-late, different-early, different-late, without repeating driver IDs; log all rejected routes and fallbacks. If fewer than four distinct eligible swaps exist, label the seed **DESIGN INVALID** and stop rather than substituting a new seed.

Choose one combined two-driver bundle from the already selected four swaps by maximal **prospective** junction/time overlap using only baseline forecast inputs; tie-break by stable SHA-256, never by later realized interaction. If all overlap scores are zero, use first two slots and label low overlap. Archive selected route files and hashes **before** evaluating SUMO outcomes.

## 6. Strict development dataset and inference integrity

Maintain separate immutable **prediction** and **label** objects per seed/probe. Record seed partition; driver identity; scheduled OD/route; legal route hashes; eligible roster; model version; parameter SHA; input feature SHA and information timestamp; baseline/alternate predicted arrivals; separately summed predicted self/external/nonparticipant/total; runtime and confidence/abstention. Store label file only after prediction is hashed: matched SUMO baseline/probe tripinfo, all arrivals, actual self/others/total, insertion delay and waiting diagnostics, lane/edge observations as available.

**Data-leakage gates:** no source-to-inference imports from offline label extraction; reject feature timestamps later than t0; no route candidate chosen by true future cost; no development-check model/parameter selection; no future holdout data access; no model that calls SUMO to reveal what would happen in the evaluated counterfactual. Predictions generated after seeing a given probe's actual outcome are **retrospective**, cannot be counted as prospective development-check predictions.

Temporary GitHub Actions output is not automatically durable research preservation. Require source, demand, route, prediction, model and label SHA-256 manifests and a verified permanent storage plan.

## 7. Development qualification criteria (not scientific validation)

**Build-only calibration:** Test global saturation-flow values 0.35, 0.50, 0.65 veh/s/lane on DEV_BUILD; choose the one with lowest arithmetic mean across **six independent seed-level externality MAEs** (four probes nested per seed). If ties within 1e−9, prefer 0.50, then 0.35, then 0.65. Freeze configuration and source SHA before DEV_CHECK predictions.

**One-time DEV_CHECK primary development screen:** E1's arithmetic mean over four DEV_CHECK seed-level externality MAEs must be ≥**5% lower** than the better of B0 (zero) and frozen B1 (historic proxy) evaluated on the *same seed families*, and E1 must strictly outperform both benchmark means. **This is an engineering development-only threshold**, not a Test A/Stage 2 validation gate, not a statistical proof, and not chosen after seeing check outcomes.

**Hard integrity gate:** mandatory fixture tests in §8, timestamp/input hash isolation, all 1,000 completed identities and route invariance in each matched SUMO arm, no illegal turns, no overflow, self+others reconciliation, deterministic outputs. A seed/arm with missing final trips is incomplete; no completed-only network score.

**Safety and calibration diagnostics:** material (|realized external|≥10 network-seconds) sign agreement; false predicted benefit/realized harm; magnitude error/bias; own-time error separately; nonparticipant effects; per-driver >30s harm as historic diagnostic only; seed-level tail harm percentiles; baseline and bundle interactions; model abstention/uncertainty; queue/edge-entry/turn timing errors; inference cost. Report negative results and subgroups. **No fairness guarantee** follows from average externality MAE improvement.

**Offline resource screen:** document actual CPU/peak RSS on pinned CI runner; reference ceiling ≤120s wall-clock per paired swap and ≤2 GB peak memory. An environmental mismatch or exceeded ceiling is **REVIEW REQUIRED**; not evidence of scientific skill or real-time/mobile practicality.

**Disposition:** Every hard physical/data invariant must pass. Successful dev-check screen plus reliable resource/uncertainty reporting may earn **DEVELOPMENT QUALIFIED FOR A SEPARATE INDEPENDENT VALIDATION PROTOCOL**. Otherwise **NOT QUALIFIED / INCOMPLETE / INCONCLUSIVE** with exact failures. A development qualification **never** authorizes a Test B simulation.

## 8. Mandatory fixture suite before any SUMO run

| ID | Required independently checkable behavior |
|---|---|
| T01 | Global identity and per-link conservation, including queued and uninserted drivers |
| T02 | No physical link storage overflow, negative queue or invented vehicle |
| T03 | Link/turn sending, downstream receiving and shared junction capacities all enforced |
| T04 | FIFO, edge minimum traversal time and deterministic tie-breaking honored |
| T05 | Identical baseline/alternate route yields zero own, others and total deltas |
| T06 | Disjoint uncongested paths change own time without inventing unrelated other harms |
| T07 | **Equal-free-flow counterexample** where own-time delta is zero/nearly zero and other-driver externality is nonzero; old external=self identity is NOT hard-coded |
| T08 | Both positive and negative externality signs on separate lawful toy scenarios |
| T09 | Full downstream storage blocks upstream movements and changes unchanged-route drivers' time |
| T10 | Nonadditive combined two-target effect is computed by actual joint rollout |
| T11 | Source insertion delay counted exactly once in scheduled-to-arrival time |
| T12 | Illegal turns and incompatible junction movements rejected |
| T13 | Byte-identical model output for identical frozen inputs/source/parameter/seed |
| T14 | Injected post-t0 FCD, tripinfo, queue or counterfactual labels **rejected** at predictor interface |
| T15 | Missing/unknown model state yields explicit abstain/unreliable output |
| T16 | Nonparticipant sums and target-exclusion from other-driver set correct |
| T17 | All 1,000 arrived by 1,800s or explicit incomplete/nonqualification |
| T18 | DEV_CHECK and any future holdout identities prohibited from model calibration path |

**T01–T18 must pass**, including mandatory T07 and T14, before *any* development SUMO execution.

## 9. Engineering tasks, review and stopping rules

After a **separate implementation authorization**, build under \`research/externality_estimator/\` with modules \`schema.py\`, \`candidate_routes.py\`, \`state_estimator.py\`, \`link_turn_queue.py\`, \`counterfactual_rollout.py\`, \`externality_outputs.py\`, \`uncertainty.py\`, \`baselines.py\`, \`dataset_contract.py\`, \`label_builder.py\`, \`audit.py\`, and \`tests/\`.

**I0** source/CLI/runtime freeze and assumption register; **I1** FIFO finite-storage queue propagation; **I2** per-driver paired counterfactual and identity accounting; **I3** baselines, no-leakage paths and fixed candidate manifest; **I4** all no-SUMO tests and development resource preflight; **I5** separately authorized 60-arm development-only runs; **I6** build-only parameter selection, single check evaluation and complete negative/positive report.

**Pre-execution review gaps:** junction conflict metadata semantics in pinned SUMO; signal/turn priority and per-lane groups; source injection capacity; token corner cases; vehicle speed factors; route connectedness; exact prediction-time cutoff; model artifact budgets. The code implementation must resolve these **prospectively before** simulations, not use undocumented favorable defaults. Any material physical-model or test-gate revision requires a **new versioned protocol amendment before inspecting new outcomes**.

Do not attach an automatic \`push: main\` trigger that launches 60 SUMO simulations. An explicit reviewed execution gate/dispatch is required. Do not execute future Stage 2 validation seeds or the historic unrun Test B cohort as development examples.

## 10. Interpretation of this freeze

**Frozen:** prediction estimands/units, equal-information and no-clairvoyance contract, E1 finite-capacity FIFO link/turn model, 1s update and 5s diagnostics, limited capacity priors, 1,800s horizon, all-driver counterfactual accounting, build/check seed allocations and 60-arm ceiling, deterministic candidate and bundle rules, build-only calibration and comparator set, development-check screening rule, unit tests, provenance, fairness diagnostics and stops.

**Not implemented or proven:** E1 source code, its physical fidelity, prediction accuracy, parameter identifiability, computational feasibility, risk calibration, independent Stage 2 validation, or whole-policy Test B success.

**Stage 1B completed when this document is merged:** The next requested milestone is source-reviewed E1 implementation with no-SUMO fixtures. Only later, with separate explicit approval, may the development-only SUMO budget run. Later still, **separate fresh independent validation** is required before any equal-information cooperative-versus-independent Test B with realized individual and nonparticipant fairness.

**Scientific sequence remains:** develop a distinct prospective externality estimator → independently validate on fresh unseen counterfactual traffic → only if that succeeds, test whether cooperation produces a measurable whole-network advantage without unacceptable individual harm.
