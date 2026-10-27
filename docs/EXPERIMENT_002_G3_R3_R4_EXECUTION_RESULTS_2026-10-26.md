# Experiment 002 — G3 R3–R4 Pre-Freeze Execution Results

**Research session:** October 26, 2026 (Pacific).  
**Status:** **R3 and R4 DEVELOPMENT implementation and verification completed successfully. Measurement-contract readiness advanced; M3 is NOT frozen and held-out evaluation has NOT been authorized or executed.**

**Authorized research:** [R3 exceptional-event and missing-data contract](EXPERIMENT_002_R3_EXCEPTION_AND_MISSINGNESS_CONTRACT_V0_1.md) · [R4 seed-level statistical and reproducibility plan](EXPERIMENT_002_R4_SEED_LEVEL_ANALYSIS_AND_REPRODUCIBILITY_V0_1.md).  
**Execution:** [Successful GitHub Actions run 40459207060](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40459207060), with all fixture, scenario and aggregation jobs passing. [Permanent evidence publication run 40459547923](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40459547923) succeeded.  
**Durable artifacts:** [Complete R3–R4 evidence archive](results/exp002_g3_r3_r4_2026_10_26/README.md), including per-regime native `statistic.xml`, `r3-exceptions.json`, input hashes, tripinfo invariance, and development seed-level CSVs.

## 1. R3 — Exceptional events and missingness

An explicit SUMO native `--statistic-output` replay was executed against **unchanged archived development seed 2101**, at departure windows **200, 600 and 1,200 seconds**, using the previously pinned SUMO image `sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`, original network, routes, demand and one-second solver step.

All **3 × 1,000** tripinfo outcomes exactly matched their archived originals. Explicit native `teleports.total` was emitted and was **0 in each replay**. Native `safety.collisions`, `emergencyStops` and `emergencyBraking` were also 0 in these specific replays; this is **not** a claim of real-world safety. No unexplained within-trip FCD disappearance, missing lane, duplicate vehicle/timestep, or required positive-sample native field anomaly was observed in this set.

| Window | Native teleport count | Native zero-sample/empty-road bins | Partial final native edge bins | R3 gate |
|---|---:|---:|---:|---|
| 200s — high | **0** | 3,268 | 360 | Passed for replay |
| 600s — moderate | **0** | 3,801 | 0 | Passed for replay |
| 1,200s — low | **0** | 8,468 | 360 | Passed for replay |

**Critical classification rule:** zero `sampledSeconds` in native edgeData may be rounded from a small positive value; absent `speed` or `occupancy` on unused roads means **not applicable/undisplayed**, not numeric zero. Final partial intervals do not belong in the full 30-second comparison denominator. Teleports are **UNKNOWN** in any source run lacking an explicit statistic—even if all its vehicles finished—and require an appropriately matched replay or separate evidence; our present zero-teleport proof comes from the invariant controlled replays.

**Policy for future evaluation:** unexpected missing/teleported vehicles, route changes, data gaps and unclassified native fields are flagged and block a clean full-population timing claim. They are neither zero-imputed nor silently dropped; no seed substitution based on outcomes is permitted. Each attempted seed must retain a denominator, an exception ledger and input hashes.

## 2. R4 — Seed-level paired analysis and reproducibility

Built `g3_r4_seed_analysis_v01.py` with synthetic fixtures verifying that a **seed**, not a vehicle or edge visit, is the unit of independent variability. The development-mode code **refuses reserved seeds 3101–3110**, duplicate/missing seed-window rows, incomplete vehicle coverage, negative/nonfinite errors or an inappropriate ten-seed interval request.

A guarded dry run used only the original **three development seeds 2101–2103** per regime (nine previously inspected scenarios). The paired seed-level difference is `MAE_freeflow - MAE_timeaware`, both evaluated on identical chosen routes:

| Window | Mean time-aware error reduction (seconds) | Sample SD across three development seeds (seconds) | Mean time-aware signed late-arrival bias (seconds) |
|---|---:|---:|---:|
| 200s | **5.48** | 0.14 | **+54.38** |
| 600s | **3.97** | 0.07 | **+19.27** |
| 1,200s | **3.52** | 0.09 | **+13.45** |

The **high-congestion regime (200s)** is prespecified as primary for any later evaluation. Moderate and low are secondary but must still be reported. The proposed held-out design has **ten independent paired seed effects per regime**, with a two-sided Student-t 95% interval across those ten **seed-level** differences (`df=9, t*=2.262157...`). It **does not** treat thousands of vehicle-edge errors as independent observations; ten seeds do not automatically provide adequate statistical power.

If fewer than ten valid paired seeds remain, do **not** silently replace them or declare the ten-seed analysis complete. The positive development error reduction does **not** establish unbiased calibration, system travel-time benefit or real-world transfer. No held-out intervals or p-values were calculated during this dry run.

## 3. Gate and scientific-decision record

| Gate | Result | Scope |
|---|---|---|
| R3 fixtures and explicit incident-status semantics | **PASS** | Tested code distinguishes explicit zero, positive and unknown teleport status |
| R3 native road empty/partial and FCD coverage classification | **PASS for these three development replays** | 3,000 original trips invariant; no critical unclassified exceptions |
| R3 collision/teleport count | **ZERO confirmed in the three matched replays** | Other archived runs without explicit statistics still have UNKNOWN event status |
| R4 prespecified independent experimental unit and statistics | **PASS as code/analysis plan** | Paired seed-level difference, high-load primary, no per-edge pseudoreplication |
| R4 development seed dry run | **PASS** | Seeds 2101–2103 only, nine scenarios; no held-out confidence intervals |
| G3 native timing and search-input reference | **Previously PASSED for inspected three-regime development replay** | See [R0–R2 results](EXPERIMENT_002_G3_R1_R2_VERIFICATION_RESULTS_2026-10-26.md) |
| Predictor accuracy/calibration | **NOT established** | Substantial systematic early forecasts persist |
| M3 protocol freeze and held-out seed access | **NOT approved / NOT started** | Requires a distinct written freeze proposal, review and authorization |

## 4. What is ready, and what must still be decided

The **narrow simulated road-entry timing measurement contract** is sufficiently specified to prepare a formal, reviewable M3 freeze **proposal**: native link exit-based entry at original one-second resolution; unchanged original time-aware prediction along actually driven routes; free-flow forecast on the same routes; complete ordered route coverage; explicitly recorded teleport and other exception states; seed-level paired uncertainty with no imputation.

The forthcoming freeze proposal must explicitly lock Git commit, predictor input/analysis and output schemas, SUMO immutable digest, input hashing and generator, exact exception-handling implementation, all report fields, source-artifact/retention strategy, and reserved seed registry. **No execution workflow should read or simulate evaluation seeds before that separate freeze decision.** A further explicit approval is required to release the held-out study after freeze.

**Scope exclusions remain binding:** Original route-assignment counts are not forecasts of physical road occupancy. Internal-link residence is not causal junction delay. Free-flow comparison of prediction accuracy is not an independent/cooperative network-efficacy trial. Current evidence is synthetic SUMO only, not operational traffic safety.

**Bottom line:** R3 and R4 have been implemented, tested, run against prior development evidence and published. The next step is a scientific review of an **M3 preregistration/freeze proposal**, not automatic evaluation.
