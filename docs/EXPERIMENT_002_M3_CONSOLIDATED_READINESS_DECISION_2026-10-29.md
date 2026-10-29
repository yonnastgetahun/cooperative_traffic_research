# Experiment 002 — M3 Consolidated Readiness Decision

**Date:** 2026-10-29 (Pacific).  
**Development rehearsal:** **GO / PASS**.  
**Actual reserved-seed held-out evaluation:** **NO-GO / NOT AUTHORIZED**.

## Verified development rehearsal

[GitHub Actions run 40838046735](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40838046735) completed with **all four jobs successful**: frozen full-development simulation, native observation and postprocessing in each of the 200-, 600-, and 1,200-second congestion regimes, followed by cross-regime consolidation. The prior run [40832928677](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40832928677) had all three scientific jobs pass but failed at aggregation due to a workflow artifact-root path mismatch. The path was corrected without altering scientific code; the successful rerun confirms that defect is resolved.

The rehearsal used only previously inspected **development seed 2101**, with frozen scientific SHA `be2e8d27c78c8b6de4891115d6d951edc877ac6e` and immutable SUMO image `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`.

The successful run preserved four artifacts: three complete per-regime development output packages and one consolidated qualification package. Its original frozen qualification runner verified topology and OD consistency, original routing/predictor equivalence, native one-second observation records, R3 teleport and missing-data gates, frozen timing error reproduction and cross-regime results. A separate postprocessing pass independently repeated frozen native route parsing, timing bridge, R3 audit and seed-level score comparisons on the **fresh outputs**.

**Interpretation:** The development pipeline and cross-regime aggregator work end-to-end under the prespecified development conditions. This is a software and scientific-reproducibility milestone, **not a new predictor-validation result**.

## Final readiness boundary

| Gate | Decision |
|---|---|
| Frozen scientific protocol and source | PASS |
| Fresh development-only full simulation in all 3 regimes | PASS |
| Frozen native observation, R3 and timing-score equivalence | PASS |
| Consolidated development aggregation | PASS |
| Development artifacts retained in GitHub Actions | PASS (retention 30 days) |
| General-seed held-out production workflow | NOT DEPLOYED/NOT QUALIFIED |
| Full reserved-seed release record and approval enforcement | NOT ACTIVATED |
| Live protected-environment timer and admin-bypass status | Screenshot-supported; independent API verification unavailable |
| Actual reserved-seed evaluation | NOT AUTHORIZED |

The existing general-seed driver remains **hard-restricted to development seed 2101**. The inactive held-out template has all jobs disabled. Passing development does not imply that the 30-scenario held-out execution, failure disposition and release controls have been exercised.

## Decision

**GO** for the completed end-to-end development rehearsal and scientific reproduction. **NO-GO** for actual held-out execution today, pending an executable and reviewed production workflow with verified release authorization and adequate environment protections, followed by **a separate explicit user instruction to run reserved seeds 3101–3110**.

Do not add further scientific methodology or unrelated safeguards. Complete only the specific production-release implementation gaps and preserve the frozen estimand. The chosen-route timing study cannot alone establish that predictor errors caused worse cooperative-routing outcomes or that cooperative routing improves system travel times.
