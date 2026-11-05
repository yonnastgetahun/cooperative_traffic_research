# Cooperative Traffic Research — E1-v2-J1 Frozen Development Study v1 (V2-D1)

**Freeze date:** November 4, 2026 (prior to any V2-D1 simulation or new outcome).  
**Authorization:** User explicitly approved the complete *conditional* V2 development → independent confirmation → cooperative Test B sequence. **No retrospective threshold changes, seed re-selection, or opening of independent validation/Test B if an intervening gate fails.**  
**State at freeze:** [V2-I2 original 25 no-SUMO tests and 22 original E1 regressions passed](POST_EXP007_E1_V2_I2_NO_SUMO_IMPLEMENTATION_VERIFICATION_2026-11-04.md), including one historical 1,000-driver full-grid static forecast. Neither E1-v2 externality skill nor dynamic junction equivalence is established.

## 1. Predeclared question, scope and exact estimands

For one prespecified legal route swap of an eligible driver i, can the **frozen, connection-aware E1-v2-J1** predictor better estimate the **SUMO-realized change in journey time summed over all other drivers** than both B0 (zero effect), B1 (old quadratic assigned-demand predictor) and frozen E1-v1 (old one-conflict-class finite-storage predictor), without producing dangerous false network benefits?

- \`T_j(A) = actual_arrival_j(A) - scheduled_departure_j\`, including insertion delay once.
- \`delta_self\` is the changed driver's own elapsed difference in **seconds**.
- \`delta_external\` is the sum of elapsed-time differences of all **999 other drivers**, in **network-seconds**, negative for benefit, positive for harm.
- \`delta_total = delta_self + delta_external\`; \`delta_nonparticipant\` sums the unchanged opt-out roster.
- One joint two-route bundle must be scored by a *fresh paired predicted forward rollout*, not by adding singleton deltas. Its realized interaction is the joint SUMO network contrast minus the two separate single-route contrasts.
- Require all **1,000 IDs** and arrival times in every SUMO arm. No completed-only substitution if a vehicle fails.

**Frozen physical domain:** same original 10×10 SUMO 1.28.0 one-lane external roads, 100 priority junctions, 1,000 vehicles, 200-second congested departures, 50% nominal eligible opt-ins (even IDs). All 1,000 route plans are prospectively announced to both predictors as an **idealized synthetic-information assumption**. This is not a comparison against Google Maps, Apple Maps or Waze, and not real-world human consent.

## 2. Model, data and simulator isolation

**Immutable models:** E1-v2-J1 source from merged V2-I2 [PR #79](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/79); frozen E1-v1 source from execution commit 05b770cf000f84677524e0a1e89bea06ec0e703b and its original read-only comparator. Global \`q_sat=0.50\`, 1-second model clock and all storage/receiving/insert semantics fixed. **NO V2-D1 parameter fitting**, residual learner, junction amendment or selection from measured new effects.

**Static geometry/intent:** Pinned original SUMO container \`ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb\` (SUMO 1.28.0). Frozen original independent traffic-aware route initialization and generator at source commit \`be2e8d27c78c8b6de4891115d6d951edc877ac6e\`; preserve source SHA and exact command/seed for each new scenario. No departure, signal or car-following change.

**Hard predecision information rule:** E1-v2's \`predict_counterfactual\` sees static network, source/speed/capacity priors, announced planned routes and original synthetic schedule only; **never** SUMO postdecision queues, tripinfo, edgeData, laneData, FCD, counterfactual labels, or any outcome used to select probes. Baseline and swapped route predictions generated and SHA-256 locked **before** paired SUMO execution; original SUMO outputs collected separately.

## 3. Frozen new seed groups and maximum footprint

| Partition | Independent demand seeds | Baseline + four single swaps + one two-swap bundle | Planned SUMO arms |
|---|---|---|---:|
| **V2_DEV_BUILD_NEW** | **6101–6106** (6) | 6 arms per seed | **36** |
| **V2_DEV_CHECK_NEW** | **6111–6114** (4) | 6 arms per seed | **24** |
| **Total** | **10 disjoint new seeds** | One baseline reused per seed | **60** |

No seed in 4101–4105, 5101–5114 or 4201–4210 may be used as an independent cohort. **Future independent estimator-validation seeds** provisionally reserved **6201–6212**, **unopened** until development qualifies. **Future Test B seeds** provisionally reserved **6301–6312**, **unopened** until independent estimator validation qualifies. Do not even precompute routes or browse outcomes in the latter two groups now. A later study must separately freeze its own exact sample sizes and acceptance gates.

**Four route-swap slots, per seed, selected from prospective geometry only:**
1. Nominal free-flow difference ≤0.5s and scheduled departure <100s.
2. Nominal free-flow difference ≤0.5s and scheduled departure ≥100s.
3. Nominal free-flow difference >0.5s and scheduled departure <100s.
4. Nominal free-flow difference >0.5s and scheduled departure ≥100s.

Use same legal connected route alternatives, nominal detour cap and hash-based stable ranking as frozen E1 Stage 1D. If a slot has no eligible candidate, use the unchanged prespecified slot-fallback precedence. If fewer than four distinct eligible IDs exist, **DESIGN INVALID; STOP** (no favorable replacement seed).

**Bundle:** choose the two of four selected swaps with maximum *prospective* common junction/5-second entry footprint, tie-break by seeded SHA256; if forecast overlap is zero, first two slots; record low overlap. Because the original E1 baseline uses a simplified clock, this overlap is **selection metadata only**, not an observation or a claim that actual traffic pairs were independent.

**Negative result retention:** A failed prediction, malformed route, incomplete SUMO arm or simulator exception produces a reported **INCOMPLETE / NOT QUALIFIED** status. Do not expand the 60-arm budget, select new seeds to rescue results, or drop unfavorable probes. Re-execution of the exact same infrastructure-failed arm requires logged reasons and fixed inputs—not postoutcome adaptation.

## 4. Frozen development measurement and comparators

For every selected singleton, write exactly one frozen result row per model before any simulation. Required predictions:

- B0: all externality predictions exactly zero.
- B1: frozen original Experiment 007 quadratic assigned-demand proxy.
- B2: frozen own-time-only ETA predictor with externality set to zero; reporting B2 separately prevents own ETA accuracy from being interpreted as genuine spillover prediction.
- E1-v1: **unchanged old all-class finite-storage queue model**, same input and q_sat=0.50.
- **E1-v2-J1**: new connection-aware junction model only; all other originally frozen physics unchanged.

Predictions for the original 1,000 individual identities must be available from both E1 models, with \`pred_self\`, \`pred_external\`, \`pred_nonparticipant\`, \`pred_total\`, status, runtime and model/input/route SHA. If either E1-v1 or E1-v2 cannot complete for a required candidate, record its abstention; **do not score an unobserved delta as zero**. A required E1-v2 abstention makes it **NOT QUALIFIED** for this fixed offline scientific case.

SUMO outputs: complete matched tripinfo for 1,000 drivers/arm, input hashes, five-second edge/lane diagnostics as feasible, run logs and statistics. Waiting is **already contained in SUMO duration** and must not be added twice to scheduled-to-arrival cost. All nonparticipant effects and individual >30-second harm fractions are descriptive diagnostics here, not the future Test B policy fairness gate.

## 5. Prospective development-check GO / NO-GO / INCONCLUSIVE gate

**Unit of inferential independence:** one frozen demand seed, **not** its four route probes or 1,000 nested driver identities. The 4 check seeds form a small **development-only engineering screen**, not broad scientific confirmation.

**Primary improvement:**
- Compute per-seed MAE across its four singleton externality probes, in **network-seconds**, then the arithmetic mean over **four DEV_CHECK seeds**.
- Compare E1-v2 against B0, B1, and frozen E1-v1. Primary comparator is the **lowest mean MAE among all three**.
- Require E1-v2 mean MAE **at least 10% lower** than that best comparator and strictly lower than each comparator. The 10% is a prospective **practical research-development threshold**, not a confidence interval or real-world materiality estimate.
- At least **three of four check seeds** must show lower E1-v2 seed-level MAE than that seed's best B0/B1/E1-v1 benchmark; prevents a single spectacular seed from masking broad regression.

**Directional / adverse-safety gate:**
- Materiality: \`abs(realized_external) >= 10 network-seconds\`. Zero predicted externalities count as no correct signed prediction, with a separate abstention/near-zero count.
- Among material singleton probes, require **≥60% sign concordance**, with at least **10 material observations**. Report raw numerator and denominator, per seed and the 95% seed-level uncertainty limitation.
- **Zero** E1-v2 predicted-benefit/realized-harm cases where \`pred_external < 0\` and \`observed_external > 30 network-seconds\`. The >30 threshold is an **aggregate network-seconds** development hazard flag, not a per-person harm threshold.
- Declare a development failure if any mandatory v2 source, no-future input, legal route, full-demand completion or prediction lock integrity gate fails. Do not count predicted intervals as calibrated: this E1-v2 version is a deterministic point forecast.

**Secondary mandatory diagnostics, not flexible success substitutes:** self MAE (individual seconds), own/external identity check, signed externality bias, nonparticipant MAE (network-seconds), false-harm/false-benefit confusion, binned direction/calibration and ranking of candidate route alternatives, predicted vs actual bundle interaction, interaction nonadditivity, p90/p95 individual harm and >30s harm fractions for opt-in versus nonparticipants, measured waiting/edge occupancy, inference wall-time/peak memory/abstention. No one secondary success rescues a primary or adverse-safety failure.

**Offline resource screen:** ≤120s per paired predicted candidate and ≤2GiB peak RSS on documented runner, otherwise RESOURCE_REVIEW_REQUIRED and do not claim feasible operational performance.

**Joint disposition:** \`DEVELOPMENT_QUALIFIED_FOR_SEPARATE_INDEPENDENT_VALIDATION\` only if **ALL** primary, direction, adverse-safety, completeness, non-leakage and resource gates pass. Otherwise \`DEVELOPMENT_NOT_QUALIFIED\` (or \`INCOMPLETE/INCONCLUSIVE\` for missing evidence). A negative result is preserved and stops the authorized sequence before new independent validation or Test B.

## 6. Workflow protocol, predictions-first evidence and stopping sequence

**Preflight (no SUMO run):** pin source commit and E1/ E1-v2 blob SHAs; validate V01–V25 and old E1 regression gates, 1,320 movement topology mapping, new seed-group disjointness and exactly four legal proposed changes/one bundle per cohort. Preserve scenario network/demand/route hashes and selection SHA. An invalid seed stops the workflow.

**Predict-before-label:**
1. Generate **all ten** new demand/route manifests and select probes using only predecision information.
2. Freeze original E1-v1, E1-v2, B0/B1/B2 predictions **and SHA-256s for all ten seeds** before any new SUMO label is generated. With no calibration allowed, the model is unchanged between build and check groups. Store full 1,000 identity predicted arrays and every abstention/unknown reason.
3. Verify frozen predictor hashes and the complete original route list. If any required prospective prediction fails, stop and report failure without launching 60 simulations merely to hunt a better seed.
4. Run up to the fixed **36 V2_DEV_BUILD** scenario arms, preserving all original labels and physical diagnostics, then (only if integrity passes) **24 V2_DEV_CHECK** arms. No tuning, code amendments, parameter selection or probe reselection after seeing the first new outcome.
5. Join observed labels to the already frozen predictions **in a separate read-only evaluator**. Compute seed-level metrics and ALL preregistered gate results.
6. Archive every source file, original predecision prediction, raw SUMO tripinfo, five-second measurements, SHA manifest, complete per-seed row, validity/gate outcome and final scientific report. GitHub Actions artifacts expire, so durable public release or separately retained original-byte archive must be verified.

**Progression boundary:** The future independent estimator-validation protocol is only *drafted and executed* if V2-D1 returns QUALIFIED. It must use new, unopened 6201–6212 seeds and fixed risk/calibration/ranking criteria. A fresh, still-sealed 6301–6312 cohort may be used for later Test B **only if independent validation passes**.

## 7. Interpretation boundaries

A successful development screen does NOT establish independent calibration or that cooperation reduces travel times. Stage 2 must evaluate fresh, unseen single-route and interacting bundle cases with direction, magnitude, sign-risk, calibration, ranking, robustness and group harms. A deterministic point estimator has **no calibrated predictive interval**; that fact alone prevents claims of uncertainty calibration without a separate prospective method/fit.

Test B, if eventually permitted, compares a **cooperative network-externality-aware policy** against an **equally informed independent traffic-aware baseline**, with the objective (not information or computational foresight) being the studied treatment. Success requires both actual network scheduled-departure-to-arrival improvement **across all drivers** and independently passing realized participant/nonparticipant fairness gates. A pass on the 10×10 network applies only to those synthetic SUMO and opt-in/compliance assumptions.

**Publication:** GitHub scientific records of both positive and negative results are authorized. LinkedIn/X social publication is not automatic under this research protocol.

**Frozen scientific stop rule:** **NO development GO ⇒ NO independent validation ⇒ NO Test B**. Do not override it merely because the user has authorized the entire conditional sequence.
