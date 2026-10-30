# Experiment 003 — cumulative timing calibration: prespecified plan v0.1

**Status: design / implementation; no new evaluation run yet.** Written after archived M3 mechanism results and before Experiment 003 implementation. M3 frozen data and code remain immutable.

## Hypothesis

A correction that accumulates predicted delay across route edges, conditioned on congestion regime and route ordinal, will reduce **out-of-sample** chosen-route road-entry MAE relative to the frozen M3 time-aware predictor. The null is no positive improvement on fresh independent seeds.

## Design and independence

- Use a separate **development/calibration** cohort, not the reserved M3 held-out seeds 3101–3110, to fit correction parameters. The existing M3 evidence is exploratory hypothesis-generation only.
- Prespecify a disjoint fresh confirmatory cohort before inspecting its outcomes; do not reuse M3 seeds or calibration seeds for confirmation.
- Retain the same synthetic network, 1,000 vehicles per scenario, and 200s (primary), 600s and 1200s (secondary) departure regimes for comparability.
- Preserve the frozen predictor and compare: (A) original time-aware, (B) calibrated time-aware, (C) free-flow comparator on identical demand and route observations.
- Make calibration a **post-hoc timing forecast adjustment** first, with no change to route assignments. This isolates prediction accuracy from routing-policy effects.

## Candidate correction

For predicted road-entry time p(v,k), use calibrated prediction p'(v,k) = p(v,k) + a_r + b_r * k, with regime r and nonnegative ordinal k. Fit a_r and b_r using only the development cohort. Include a no-correction baseline and a departure-offset-only ablation. Keep parameters frozen before confirmatory execution. If a richer model is considered, require a new versioned plan rather than selecting after looking at confirmatory results.

## Outcomes and safeguards

Primary endpoint: seed-level paired MAE difference (original time-aware minus calibrated time-aware) for the 200s regime. Secondary: 600s and 1200s MAE, signed bias, per-ordinal residuals, positive-error fraction, and exception counts. Use independent seed as uncertainty unit, not individual road entries. Report 95% intervals and the full seed-level distribution. A failed or missing seed is reported, never silently replaced. Prespecify the number of confirmatory seeds and an exact seed manifest before running any confirmatory scenarios.

## Acceptance

Scientific support for calibration requires a positive primary seed-level paired benefit with 95% interval excluding zero, no material degradation in prespecified exception integrity, and no unreported cohort substitutions. Failure or inconclusive evidence is a valid result. Improved timing prediction alone does not establish network-wide cooperative-routing benefit.

## Execution sequence

1. Implement a small, deterministic, read-only calibration-fitting and scoring script that consumes development cohort paired road-entry CSVs; no new safeguards program.
2. Identify or generate independent development data under a separate Experiment 003 workflow, then fit and freeze the coefficients.
3. Commit the fresh confirmatory seed manifest **before** execution and evaluate the frozen correction once.
4. Publish complete results, limitations and a GO/NO-GO recommendation for a subsequent cooperative-routing policy experiment.

**Immediate execution boundary:** Step 1 can proceed now. Do not train on M3 held-out records or run confirmatory seeds before the new seed manifest is committed.
