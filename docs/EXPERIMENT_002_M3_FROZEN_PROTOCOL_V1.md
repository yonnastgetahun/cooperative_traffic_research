# Experiment 002 — M3 Predictor Timing Study: Frozen Scientific Protocol v1.0

**Status: SCIENTIFIC PROTOCOL FROZEN BY EXPLICIT USER APPROVAL ON OCTOBER 27, 2026. HELD-OUT EXECUTION IS NOT AUTHORIZED.**  
**Original proposal:** October 26, 2026 (Pacific). **Freeze decision:** October 27, 2026 (Pacific).  
**Scope:** A synthetic SUMO **chosen-route road-entry timing forecast** comparison, **not** an independent-versus-cooperative system optimization test.

**Prerequisites completed on development evidence:** [R0–R2 timing/search provenance](EXPERIMENT_002_G3_R1_R2_VERIFICATION_RESULTS_2026-10-26.md) · [R3 exception and R4 statistical dry-run results](EXPERIMENT_002_G3_R3_R4_EXECUTION_RESULTS_2026-10-26.md).  
**Scientific contracts to preserve:** [R3 exceptional-event rules](EXPERIMENT_002_R3_EXCEPTION_AND_MISSINGNESS_CONTRACT_V0_1.md) · [R4 seed-level analysis](EXPERIMENT_002_R4_SEED_LEVEL_ANALYSIS_AND_REPRODUCIBILITY_V0_1.md) · [Observation sufficiency and scope limits](EXPERIMENT_002_G3_OBSERVATION_SUFFICIENCY_REVIEW_2026-10-26.md).

## Frozen scientific intent and outcome definitions

**Primary estimand (200-second high-congestion regime):** For each **independent demand seed**, calculate the difference in *same-realized-route mean absolute external-road entry timing error*, `D_s = MAE_freeflow_s - MAE_timeaware_s`. Positive means the time-aware predictor estimated observed road entry more accurately on those routes; it does **not** mean route coordination improved trip outcomes.

**Secondary** identical estimands: 600-second moderate and 1,200-second low-congestion windows. The same seed's OD trip pairs are fixed across its three windows; no aggregation across windows assumes those outcomes independent.

**Observed target:** each vehicle's native simulator external-road entry step derived from ordered `vehroute-output.exitTimes` with internal links, using actual `tripinfo.depart` for the initial external road. Units seconds at the original **1-second SUMO solver step**. Native physical edge `sampledSeconds` and occupancy percent remain separate road-load references, **not** targets for the route-assignment-count proxy. FCD first-front entry is a separate reference consistency check.

**Predictors:** the unchanged `time_aware.py` original chosen-route cost trace, and original chosen-route cumulative free-flow timing reference. Neither predictor can access realized SUMO observations during planning. Preserve original bin = 30 seconds, pressure = 1, free-flow detour limits = 10% or 30 seconds whichever smaller, and 15% distance cap. No reparameterization after viewing evaluation outcomes.

**Unit of statistical replication:** demand seed. Candidate registry **3101–3110** in each regime (target ten independent seeds × three windows, 1,000 vehicles each). **These seeds remain ungenerated/unseen until a distinct post-freeze execution approval**. These ten seeds are a feasibility target, **not a guarantee of statistical power**. Existing exploratory 1001–1003, 2001, 2101–2103 are excluded from the untouched evaluation group.

## Prespecified reporting (before any held-out runs)

1. For each seed and regime, confirm original OD population, route-invariance (with and without default-off search observer), exactly 1,000 planned/completed trip records, all ordered road-entry matches, explicit native teleport statistics and exceptional status classification.
2. Per seed/regime: both predictors' mean absolute error, signed bias, RMSE and absolute p90/p95 on **identical chosen-road visits**, total planned and matched edge counts, actual departure lag, and descriptive error by route index 0, 1–2, 3–5, ≥6. Preserve vehicle-level raw outputs and original network/route hashes. Use the 30-second bin for any displayed road-load strata, with 10/60 as predeclared sensitivity only.
3. Primary high-congestion `D_s`: sample mean, sample SD, median, range, and two-sided **95% Student-t CI** across the planned ten independent seed-level paired differences (`df=9`, critical `2.262157...`). Secondary regimes report the same descriptive seed-level summaries and CIs; no per-edge iid inference or unplanned multiple hypothesis-test claims.
4. Report zero, positive or negative effects and systematic early/late bias candidly. A narrower forecast-error CI is not calibration of physical occupancy and does not establish route-policy optimality, individual fairness, real-world safety or external validity.
5. Every data or code change after freeze must be documented as exploratory. A new independent holdout must be designed before claiming a post-change validation result.

## Strict exception and missing-data disposition

SUMO must emit a **native teleport statistic**; absent does not mean zero. Teleports, missing vehicle trips, unexpected route changes, duplicate/out-of-order events, unexplained within-trip FCD gaps, and mismatched external-edge records invalidate clean full-population timing comparison for that scenario. Do not silently discard affected records, replace seeds, or impute missing timing as zero. Publish exception counts, denominator and source evidence; seek **separate incident review** if any prespecified scenario becomes ineligible. Full n=10 inference is blocked if fewer than ten legitimate seed-level pairs remain.

Empty road bins with absent speed/occupancy metrics are `not applicable`, not numeric zero. Native `sampledSeconds=0.00` has rounding uncertainty. Partial final intervals must be excluded from *full 30-second* bin denominators, while retained as explicitly partial records. Neither rule changes travel-timing records.

## Locked reproducibility contract and separate implementation gate

At freeze, the scientific source snapshot and evidence references are pinned by the accompanying [freeze manifest](EXPERIMENT_002_M3_PROTOCOL_FREEZE_MANIFEST_V1.json). Before held-out execution, the implementation must additionally satisfy these requirements:
- Fixed **Git commit SHA for all runner, predictor, trace, analysis and exception parsing code**, plus full current protocol document hash.
- Immutable SUMO image reference, presently tested at `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`, and SUMO version 1.28.0; do not rely on a mutable image tag.
- `netgenerate` fixed grid 10×10/200-meter spacing, deterministic demand generator and route policy, seed/window mapping, 1-second solver step, all command-line options, trip type, time bin and actual-route selection parameters.
- SHA256 input network/trips/route files, forecasts, native exit events/FCD/native edgeData/tripinfo, statistic.xml and analysis outputs for each run; normalized topology and OD equality across same-seed regimes.
- Predeclared machine-readable **observation, exception, and analysis schemas**, coverage ledger, reporting precision, and archive retention/regeneration policy. Preserve original full logs/hashes even when GitHub Actions artifact retention expires.
- A strictly **manual-triggered held-out workflow** prepared, reviewed and guarded against execution until *a second explicit authorization*. Merely publishing this proposal or workflow does not grant permission to dispatch it.

## Scope exclusions and unresolved scientific limitations

The existing planner's one-bin prior assignment counter is not a forecast of physical vehicles present or occupied road percent; do not compute SUMO native occupancy forecast MAE against it. Native internal-link residence is not causal junction delay, and timing predictions on actually chosen routes do not reveal travel outcomes on unchosen routes. The 10×10 synthetic grid does not establish transfer to Los Angeles, other road networks, drivers or real-world safety.

**Approval of this freeze** authorizes preservation of this precise method and its verified development code snapshot, **not the evaluation runs themselves**. Approval of this frozen protocol does not retroactively make the development outcomes held-out evidence or prove model calibration.

## Approved freeze decisions and remaining execution prerequisites

1. **APPROVED AND LOCKED:** The narrow native simulator-step road-entry estimand, high-congestion primary regime and separate secondary regimes.
2. **APPROVED AND LOCKED:** The R3 exception eligibility rules, including no hidden teleport/missingness exclusions and no seed substitution.
3. **APPROVED AND LOCKED:** The seed-level paired analysis and uncertainty method, including the limitations of n=10.
4. **FROZEN SOURCE REFERENCE:** The [freeze manifest](EXPERIMENT_002_M3_PROTOCOL_FREEZE_MANIFEST_V1.json) binds the approved source commit, Git blob fingerprints, immutable SUMO digest, test run and related artifacts. The full evaluation runner and per-attempt output manifests must be reviewed separately before any simulation.
5. **FREEZE APPROVED OCTOBER 27, 2026.** A **new, separate and explicit instruction** is required for development/review of a held-out execution workflow and for any evaluation run. No reserved seed may be generated, dispatched or inspected based on this freeze alone.

**Binding decision: PROTOCOL FROZEN v1.0; NO HELD-OUT SIMULATIONS AUTHORIZED OR EXECUTED.**


## Freeze integrity, protocol amendments, and non-execution guarantee

- This freeze locks **methodology and the Git-anchored inspected code baseline**. It is not a claim that a full held-out execution harness has already been implemented or independently verified. As of the freeze, the R4 analyzer is deliberately **development-only** and rejects reserved seed IDs. No runnable M3 held-out workflow has been created; this safeguards the explicit execution-approval boundary.
- Any future execution harness must be tested against this frozen protocol and undergo a **separate execution readiness review**. If its implementation changes a frozen estimand, predictor equation, data eligibility rule, seed registry, primary outcome, inferential method or another scientific choice, it must be declared a **new amended protocol**, versioned and approved *before* examining held-out outcomes. Purely mechanical implementation details may be added only with evidence of equivalence to this protocol, explicit SHA references and a new reviewed run authorization.
- Do not use the development results to set post-hoc passing thresholds. The predictor is still known to underpredict road-entry times in all development congestion regimes; freezing measurement does not certify calibration, traffic-network performance, fairness or safety.
- A frozen Git commit SHA and SHA-256 content fingerprints are the authoritative references. The convenience snapshot branch may be moved by a sufficiently privileged GitHub actor; therefore, **verify the commit SHA**, not the branch name alone, before any eventual evaluation.
- Reserved seeds 3101–3110 remain untouched. Never enable a push-triggered held-out workflow or a background automation that simulates them.

**Read before authorizing execution:** [R3 contract](EXPERIMENT_002_R3_EXCEPTION_AND_MISSINGNESS_CONTRACT_V0_1.md), [R4 analysis contract](EXPERIMENT_002_R4_SEED_LEVEL_ANALYSIS_AND_REPRODUCIBILITY_V0_1.md), [R3–R4 evidence](EXPERIMENT_002_G3_R3_R4_EXECUTION_RESULTS_2026-10-26.md).
