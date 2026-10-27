# Experiment 002 — M3 Held-Out Runner Readiness Blueprint v0.1

**Status:** PREPARATION / DEVELOPMENT-ONLY QUALIFICATION. **No held-out workflow is activated. No held-out runs authorized.**  
**Approved scientific freeze:** [Frozen M3 v1.0](EXPERIMENT_002_M3_FROZEN_PROTOCOL_V1.md) · [Immutable source manifest](EXPERIMENT_002_M3_PROTOCOL_FREEZE_MANIFEST_V1.json) at Git commit `be2e8d27c78c8b6de4891115d6d951edc877ac6e`.  
**Preparation authorization:** The user approved preparing and verifying the held-out workflow using development seeds only; this was not permission to generate or run evaluation seeds.


**Inactive, explicitly non-executable review template:** [M3 held-out workflow draft](templates/experiment-002-m3-heldout-evaluation.yml.disabled). This is placed under `docs/templates`, *not* GitHub Actions' active `.github/workflows` directory, and has hard-disabled jobs even if copied. It does not itself implement the not-yet-approved general-seed adapters.

**Latest authorized preparation (October 27):** [Production R3/R4 adapter review findings](EXPERIMENT_002_M3_PRODUCTION_ADAPTER_REVIEW_FINDINGS_2026-10-27.md) and [durable evidence](results/exp002_m3_production_adapter_review_2026_10_27/README.md). Pure adapters and the hard-disabled activation guard passed synthetic tests and original development-data equivalence. The GitHub protected environment with required reviewers has **not** been configured or verified; no active held-out workflow exists.\n\n## Why this is not yet the executable held-out study

The active GitHub workflow [M3 development-only qualification](../.github/workflows/experiment-002-m3-development-qualification.yml) runs **only seed 2101** and uses frozen scientific code checked out at the exact frozen Git SHA, under pinned SUMO image `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`. The first step explicitly rejects evaluation seeds before generating networks or demand.

After the development qualification succeeds, the evaluated scientific estimand is ready for a **separate production implementation review**, not necessarily immediately executable held-out work. The original R3 script rejects nondevelopment seeds by design, as does the original R4 development-only analysis. A future separately authorized implementation can reuse their *frozen scientific definitions*, but must add mechanically equivalent, independently tested general-seed adapters. This constitutes **execution-harness implementation**, not permission to alter the frozen hypothesis or methods.

## Production workflow outline (NOT ACTIVE)

When and only when separately authorized, propose a **manual-only** GitHub Actions workflow with no `push`, `schedule`, `pull_request`, `workflow_run`, or autonomous trigger. It must never be enabled without user review.

For each of the **ten reserved evaluation seeds (3101–3110)**, generate three matched scenarios with departure windows **200, 600, 1200 seconds**, one seeded OD population per seed, and 1,000 vehicles per scenario. **The seed registry is frozen; none of these may be generated or previewed during preparation.**

Each scenario:
1. Check out frozen scientific commit SHA (do not trust a movable branch name); verify frozen protocol/git-blob hashes and immutable SUMO image digest.
2. Generate original 10×10 grid, OD demand and original `time_aware.py` route assignments with the exact original parameters. Compute hashes for every generated input and verify OD tuples match across a given seed's three departure windows. Freeze search candidate inputs before SUMO observations.
3. Run native SUMO with 1-second step, vehicle/internal-edge exit times, one-second FCD, native road `edgeData`, `tripinfo`, teleport `statistic.xml`, collision output and logs.
4. Apply the exact frozen R3 exception rules. An absent teleport statistic is UNKNOWN, not zero. A teleported/missing/unmatched run remains an **ineligible recorded attempt**, not a seed that may be silently replaced.
5. Join native step-level entry times to planned external road visits in original order, with repeated-road-safe matching. Compare original time-aware and same-route free-flow predictions. Preserve individual seed/regime MAE, bias, RMSE, abs p90/p95, departure lag, trip coverage, error by route ordinal, route legality and all exception states.
6. Archive all per-scenario data, hashes, original forecasts and exceptions. Do not announce a network-efficiency gain from any predictive improvement.

The aggregate must run only if **all 30 prespecified scenarios are available with full evidence**, and the frozen seed-level 95% Student-t interval may be computed only if all ten paired seeds per regime satisfy eligibility. Report the high-congestion regime as primary and other regimes as secondary, with no post-hoc cutoff or pseudo-replication. Otherwise stop with an explicit exception/ineligibility memo; ask for new authorization before considering any additional run.

## Activation requirements — future explicit decisions

1. **Complete current development-only end-to-end qualification** with generator equivalence, routes/audits, native timing, R3 teleport/exception data, seed metrics, and historical reproduction. Preserve GitHub Actions link, source SHA and outcomes.
2. **Review a production executable diff** against the frozen scientific SHA for the R3 exception and R4 analysis adapter. Pure adapter code must preserve frozen semantics. Demonstrate missing/teleport/route-change fixtures and that the ten-seed estimator never looks at vehicle-edges as independent replicates.
3. **Publish and test an explicit activation guard** preventing accidental execution. Prefer a GitHub protected environment with named reviewers and a one-time user-approved activation artifact, independently checked by the workflow before any input generation; a permissive or auto-created environment is insufficient. Any active held-out seed matrix before approval is prohibited.
4. **Explicitly request and receive a new user authorization to run held-out evaluation**. Mere approval of this blueprint or frozen scientific protocol does not authorize dispatch.
5. Record the review commit, execution authorizer, code manifests and immutable image before any request to generate reserved seeds.

**Scientific exclusions unchanged:** no physical road-occupancy forecast MAE for the prior assignment counter; internal-junction residence is not causal delay; chosen-route forecast accuracy is not a network-wide cooperative-routing efficacy test; no real-world safety/transfer claim.

**Current boundary:** Only a development-seed qualification workflow is active. The reserved evaluation seeds are untouched.
