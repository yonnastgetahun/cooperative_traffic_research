# Experiment 002 — R4 Seed-Level Analysis and Reproducibility Contract v0.1

**Status:** Prespecified October 26, 2026; **development-only implementation and dry-run approved**. This document is **NOT an M3 freeze**, and the held-out evaluation seeds **3101–3110 remain reserved and unopened**.  
**Inputs:** [R3 exception contract](EXPERIMENT_002_R3_EXCEPTION_AND_MISSINGNESS_CONTRACT_V0_1.md) · [G3 sufficiency decision](EXPERIMENT_002_G3_OBSERVATION_SUFFICIENCY_REVIEW_2026-10-26.md) · [R0–R2 verified timing reference](EXPERIMENT_002_G3_R1_R2_VERIFICATION_RESULTS_2026-10-26.md).

## Research scope and frozen primary estimand

**Scientific question:** On the *same chosen routes in a fixed synthetic SUMO scenario*, does the existing time-aware arrival-time model yield lower road-entry absolute timing error than a free-flow-only reference?

For seed `s`, congestion regime `r` in `{200,600,1200}` seconds, and all valid, *jointly matched* external road-entry visits `i` (`N[s,r]` planned records), compute:

- `MAE_TA[s,r] = mean_i |actual_native_entry_step_s - preSUMO_timeaware_entry_s|`.
- `MAE_FF[s,r] = mean_i |actual_native_entry_step_s - freeflow_entry_s|`.
- **Paired benefit `D[s,r] = MAE_FF[s,r] - MAE_TA[s,r]` (seconds)**: positive means the time-aware model is more accurate, not that coordinated routing improved traffic.
- Signed time-aware bias `B[s,r] = mean_i (actual_native_entry_step_s - preSUMO_timeaware_entry_s)`; positive means forecast **too early**.

The *primary scientific condition* is **high congestion (200-second departure window)**, selected now because underprediction was largest in development evidence. **Moderate (600s) and low (1200s) are prespecified secondary conditions.** This prioritization is not a post-hoc pass threshold or a claim of real-world transfer. Report all three conditions and all seeds, including negative/null effects. Do not average per-vehicle edges across seeds as independent experimental replicates. No unchosen-route outcomes are observed.

## Experimental unit, uncertainty and reporting

Each **random demand seed**, not a vehicle or road-edge record, is an experimental replicate. For each regime, summarize all ten intended independent held-out seed-level differences `D[s,r]`: `mean(D)`, sample `SD(D)` with denominator `n-1`, `SE=SD/sqrt(n)`, median, min/max, and **two-sided 95% Student-t interval** `mean(D) ± t_(n-1,0.975)*SE`. For the prespecified target **n=10**, use `t_(9,0.975)=2.262157...`. This interval treats seeds as independent samples conditional on the **fixed network, OD generator, policy and SUMO model**; it does not quantify network-structure uncertainty or provide a guarantee of statistical power. No per-edge iid standard errors, pseudo-replication, or cherry-picked seed exclusions.

**Analysis intent:** Effect-size and uncertainty estimation, not a retrospective "accuracy passed" threshold. Report whether high-load `D` is positive/negative and whether its 95% CI crosses zero; secondary regimes are descriptive with 95% CIs, without significance/power claims. **No formal three-regime hypothesis-testing family or p-value-based go/no-go is authorized in this phase.** Do not interpret a positive timing-error difference as better system-wide cooperative routing. Even a narrow CI says nothing about real-world external validity.

If fewer than ten eligible paired seeds survive integrity checks, **do not replace seeds or calculate a confirmatory 10-seed conclusion**. Publish coverage/exceptions, any exploratory seed summaries clearly labeled, and seek new protocol review. If an entire run fails for an infrastructure cause, the *same exact seed* may be rerun only under a separately approved incident procedure, with source/hash checks; no switching to better-scoring replacement seeds. Preserve all originally attempted outcomes.

## Other prespecified measurements

- For each seed and regime: mean and RMSE, signed bias, absolute p90/p95 of edge entry errors for TA and FF; first road vs route ordinal 1–2, 3–5 and ≥6; actual-minus-scheduled departure lag and departure-aligned timing error; completion, waiting, timeLoss, missed/teleported/changed-route counts. Route group analysis is descriptive.
- Native road occupancy `sampledSeconds` and occupancy percent are **separate observed SUMO metrics**; the route-search `occupancy[(edge,bin)]` is *number of previously announced assignments*, **NOT a physical road-occupancy forecast**. Do **not** calculate native occupancy MAE against the assignment count. Correlations may be considered later under an explicitly separate model.
- Internal-junction residence at SUMO step resolution is a descriptive outcome, not delay caused by a junction. FCD front observations stay a cross-check; historic FCD-entry errors are not silently renamed native errors.
- Prespecified reporting: every seed-level row, unweighted mean of seed-level effects within regime, interval assumptions and numeric precision (full raw stored; report 2 decimal seconds), and original source hashes. A different bin size, routing policy or solver-step length requires a new versioned exploratory analysis, not an opportunistic sensitivity selection.

## Missing data and exceptional scenarios

R3 defines error statuses before analysis. **All** planned 1,000 vehicle IDs and their ordered chosen-road visits form the observation denominator per seed. Missing/teleported/unmatched edges are not scored as zero and not silently dropped. Complete-case results, if ever shown, require visible `N_planned`, `N_matched`, exception counts and a warning that missingness may be nonrandom. **Full primary analysis eligibility requires zero unclassified missing/teleported/changed-route exceptions and independently verified source invariance**. Record a blocked seed/regime as `INELIGIBLE`, and do not pretend n remains 10.

## Prespecified evaluation registry and leakage controls

- **Already inspected development seeds:** 1001, 1002, 1003, 2001, 2101, 2102, 2103. These may be used for instrumentation fixtures and descriptive dry runs, but **not** as new evaluation seeds.
- **Reserved, untouched evaluation seeds:** 3101–3110, **10 per each of three congestion windows**, with identical seed-specific OD pairs across windows and windows differing only by scheduled departures.
- No generation, preview, querying, simulation or publication of held-out outcomes until a separately reviewed/approved **M3 freeze and held-out execution**. The seed numbers are a reservation, not an execution permit.
- Predictor settings (`bin_seconds=30`, `pressure=1`, current detour 10% or 30s and distance cap 15%), route generator and deterministic vehicle ordering remain fixed while instrumentation is evaluated.
- Same vehicle OD pairs, original choice rule and time-aware route policy across any paired seed scenario. Alternative independent-routing system benefit is a **different** experiment and requires its own control arm and fairness objective.

## Reproducibility manifest and code changes

For every attempt archive schema version, research protocol SHA, `GITHUB_SHA`, SUMO image **immutable digest**, SUMO version, solver step length, all CLI and additional-file options, 10×10 network generator configuration, seed/window, 1,000-trip generator, route method and all parameters, SHA256 network/trips/chosen route/FCD/native vehroute/tripinfo/prediction CSV/statistic.xml when captured. Store `source_run_id`, observed event counts, FCD cadence, native edgeData half-open intervals, route-order checks, explicit teleport status, missingness status and test outcomes. Validate manifests mechanically; an omitted digest or unchecked comparator revision blocks freezing.

**Raw evidence retention:** Archive compact per-seed outputs and hashes in the repository. GitHub Actions artifacts have finite retention; record URL/ID/expiry and ensure that full raw records can be regenerated from pinned inputs. Do not assume temporary artifact availability is indefinite.

## Implementation dry run (approved, development only)

Use existing published [M2 nine-seed rows](EXPERIMENT_002_OCCUPANCY_M2_PER_SEED.csv) to test seed-level aggregation **without treating those seeds as independent held-out evidence**. Build fixtures that reject missing seed/window combinations, duplicate rows, negative values and any seeds other than 2101–2103 in dry-run mode. Demonstrate that the three-regime paired difference is derived from seed-level MAEs, not pooled trip or edge rows. The production 10-seed confidence interval code and protocol itself may be reviewed/tested on synthetic fixtures, but **must not read held-out data**.

**R4 implementation PASS** means a documented, tested analysis and provenance recipe is reproducible. It does **not** mean forecast calibration, a statistical finding, an M3 protocol freeze, or held-out-study authorization.

## Freeze preparation checklist (no automatic freeze)

- R0–R2 scientific measurement results and source invariance documented.
- R3 exception policy implemented and verified, with explicit teleport statistics; no field treated as missing-as-zero.
- R4 code fixtures, development dry run and analysis manifest pass, with seed-level independence preserved.
- All unsupported scientific claims (real traffic, native physical occupancy predictions, causal junction delays, unchosen-route counterfactuals) excluded.
- Publish a **separate M3 preregistration proposal** with schema and SHA, and request explicit user approval for the freeze. **A further separately explicit authorization is required to run any held-out seed.**
