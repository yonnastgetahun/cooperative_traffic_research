# Experiment 002 — M3 Production Adapter and Activation-Safeguard Review

**Date:** October 27, 2026 (Pacific).  
**Result:** **PRODUCTION R3/R4 ADAPTERS REVIEWED SUCCESSFULLY ON SYNTHETIC FIXTURES AND ARCHIVED DEVELOPMENT DATA.**  
**Execution readiness:** **NOT ACTIVATED; NO HELD-OUT SEEDS RUN OR AUTHORIZED.**

**Original frozen scientific protocol:** [M3 v1.0](EXPERIMENT_002_M3_FROZEN_PROTOCOL_V1.md), authoritative Git commit `be2e8d27c78c8b6de4891115d6d951edc877ac6e`.  
**Prespecified review plan:** [M3 Production Adapter Review v0.1](EXPERIMENT_002_M3_PRODUCTION_ADAPTER_REVIEW_PLAN_V0_1.md).  
**Successful review:** [GitHub Actions 40577231235](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40577231235).  
**Successful permanent evidence publication:** [GitHub Actions 40577473593](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40577473593).  
**Durable artifact bundle:** [Review evidence and per-regime tables](results/exp002_m3_production_adapter_review_2026_10_27/README.md).

## What was built without altering the frozen science

- [R3 exception/eligibility and R4 seed-level statistical adapters](../experiments/experiment_002/m3_production_review/adapters_v01.py): pure, side-effect-free routines. R3 eligibility is evaluated against the output from the **actual frozen R3 scientific method**, rather than introducing a replacement definition. Future ten-seed paired analysis calls the unchanged frozen `mean_ci_if_ten` calculation, with the demand seed—not an edge or vehicle—as the replicate.
- [Activation guard](../experiments/experiment_002/m3_production_review/activation_gate_v01.py): unconditionally refuses held-out execution today, rejects any request to generate a reserved evaluation seed, inspects the three hard-disabled jobs in the inactive template, and checks that no active held-out workflow exists under `.github/workflows`.
- [Offline original-science equivalence runner](../experiments/experiment_002/m3_production_review/review_development_v01.py): checks out the pinned frozen code, independently re-invokes the **original R3 audit** and compares it exactly with archived successful development reports. It checks source SHA, native/trip integrity, original route hash, normalized origin–destination identity across regimes and resulting seed-level timing summaries.

All eight synthetic/adversarial tests passed. They exercised unknown or positive teleport counts, missing FCD/native fields, missing/duplicated seed-regimes, malformed timing cohorts, different OD pairs across a seed's regimes, preserved paired MAE arithmetic, a ten-seed Student-t example with **fabricated dummy labels**, and blocked held-out activation.

## Results against inspected development evidence

The offline review used only the **previously run 2101 development seed** for congestion windows 200, 600 and 1,200 seconds. It invoked **no SUMO simulation, no demand generation and no new routing selection**. In all three cases the original frozen R3 report was reproduced **exactly**, and the new production record mapper preserved original R4-relevant timing cohorts and parameters.

| Check | Outcome |
|---|---|
| Frozen source SHA and 14 file fingerprints | **Verified** |
| R3 original-method reproduction | **Exact agreement in all 3 reviewed development regimes** |
| Completed original trips | **3,000** |
| Original chosen-road entries mapped | **25,179** |
| Original search-time route-assignment reads already independently verified | **1,994,952** |
| Prespecified same-seed OD matching across windows | **Passed** |
| Synthetic ten-seed R4 Student-t analysis fixtures | **Passed** (no held-out inputs) |
| Active held-out workflow | **None** |
| Reserved evaluation seed 3101–3110 ever generated or inspected | **No** |

The numbers above reproduce **historical** development evidence; they are not new independent predictor-validation results. In those historical cases, time-aware timing estimates had lower MAE than same-route free-flow estimates but still substantially underpredicted arrival times under congestion.

## What the safeguards establish—and what they do not

The existing evaluation template, [`docs/templates/experiment-002-m3-heldout-evaluation.yml.disabled`](templates/experiment-002-m3-heldout-evaluation.yml.disabled), is not an active GitHub Actions workflow; all its jobs are hard-disabled. The active review workflow uses only existing development artifacts. **The active review and qualification workflows do not permit reserved evaluation seeds.** This is a workflow-level safeguard, not a claim that an authorized repository maintainer is physically unable to execute the frozen standalone demand generator with an arbitrary seed outside those workflows. A protected environment and a separate execution authorization are still necessary before activation.

**Remaining material operational blocker:** A GitHub protected environment with required reviewers for `m3-holdout-reviewers` has **not been independently verified or configured by this work**. A file saying `approved=true` would not be an adequate independent authorization mechanism. Separate approved environment setup and GitHub access review are required before an evaluation workflow can be activated. The review adapters are **pure implementation building blocks**, not a completed, deployed 30-scenario production experiment pipeline.

**Subsequent GitHub operational audit:** The [October 27 safeguards decision](EXPERIMENT_002_M3_OPERATIONAL_READINESS_REVIEW_2026-10-27.md) discovered a previously unrestricted historical calibration seed input; it is now guarded against 3101–3110. GitHub's current `main` branch is **not protected**, and `m3-holdout-reviewers` is **not verified** (HTTP 404). These settings block activation even though the production adapters passed offline checks.

## Decision register

| Gate | Result |
|---|---|
| Frozen scientific question and method | **Previously approved and unchanged** |
| Production R3 eligibility adapter equivalence | **PASS on archived development cases** |
| Production R4 seed-level inference logic | **PASS on synthetic dummy-seed fixtures** |
| Strict missingness, duplicate, OD-matching and seed replacement rules | **PASS in unit tests** |
| Source-fingerprint and immutable-image consistency | **PASS in offline development review** |
| Manual activation/absence of armed held-out workflow | **PASS as current disabled state** |
| GitHub protected environment / reviewer configuration | **NOT VERIFIED — BLOCKER** |
| General-seed runnable production driver and 30-scenario archive/eligibility mechanics | **NOT DEPLOYED — separate review** |
| Held-out evaluation | **NOT AUTHORIZED / NOT STARTED** |

## Recommended next decision

The next separately approved milestone is to complete the **operational activation safeguards and production harness integration**, including verifying a protected environment with actual required reviewers, a manual-only `workflow_dispatch` design, and independent production-adapter equivalence checks that still use synthetic or previously examined development data. **Running any of the ten reserved seeds** in any of the three regimes requires a distinct explicit authorization **after** that readiness review.

Do not interpret code-level preparedness as permission to generate or preview held-out outcomes. The frozen protocol, original model choices, estimator, seed registry and uncertainty analysis remain unchanged.

**Bottom line:** R3/R4 production adapters and fail-closed safeguards passed their authorized offline review; held-out execution is still intentionally blocked.
