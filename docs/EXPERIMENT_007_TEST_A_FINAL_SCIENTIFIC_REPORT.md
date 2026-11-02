# Experiment 007 — Test A scientific findings and prospective decision

**Date:** November 1, 2026 (GitHub execution November 2 UTC).  
**Decision:** **NO-GO for progressing this frozen assigned-demand marginal-externality estimator to the Experiment 007 Test B policy confirmation.** This is a **mechanism-screen failure**, not evidence that all cooperative optimization is ineffective or that cooperative routing is inferior to independent dynamic navigation. **Test B was not executed.**

## Executive finding

The frozen Experiment 007 design separated (A) **predicting marginal effects on other drivers** from (B) **demonstrating improved whole-network route assignment**. Test A completed all 30 planned SUMO arms (five independent seeds, each one independent traffic-aware baseline, four selected singleton route swaps and one two-swap bundle) with the original 1,000-vehicle, 10x10 synthetic grid and 200-second departures.

Among the 20 preselected singleton probes, all **20** had \`|realized externality| >= 10 network-seconds\` (the frozen materiality rule). The predicted and realized signs agreed in only **8/20 = 40%**, below the predeclared **60% gate**. Five of the 20 probes predicted **zero** externality yet had materially nonzero observed effects. Excluding the zero predictions as a descriptive sensitivity gives **8/15 = 53.3%** agreement, also below 60%; that is **not** a retroactive change to the gate.

The detector's **mean absolute signed externality-prediction error** over the 20 deliberately sampled probes was **1,801.71 network-seconds**. Predicted externalities ranged **−3.24 to +13.50 network-seconds**, while realized externalities ranged **−3,777 to +4,328 network-seconds**. These figures are **not** single-driver delay: they are *sums of time changes across the other 999 modeled vehicles*. The observed sensitivity of the network to even one altered assignment is far larger than the static occupancy proxy anticipated.

**Frozen consequence:** Test A gate **FAILED**; the conditional Test B jobs were **SKIPPED**. Therefore Experiment 007 has **not** tested or established whether the social-objective route assignment S beats the comparably informed independent policy I under fresh policy seeds. No policy-wide fairness verdict can be assigned to S from unexecuted Test B.

## Original scientific design and provenance

- [Prospective two-test design](EXPERIMENT_007_TWO_TEST_PROSPECTIVE_SCIENTIFIC_DESIGN_NOTE.md).
- [Frozen protocol v1](EXPERIMENT_007_FROZEN_PROTOCOL_V1.md), merged in [PR #37](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/37) before any fresh Test A/ B simulation seeds.
- [Implementation and PR-only development validation](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/38); merged code commit **\`afa252c8d9ec31b247db49f2e2b0e30ce6d31fc8\`**. Development seed 2101 passed with 1,000 legal routes, 793 vehicles offering an alternative, all nonparticipant routes invariant; I and S differed on **one** route in this development scenario (descriptive only).
- [Original Test A scientific execution, GitHub Actions run 41380998833](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833): all five probe matrix jobs completed successfully; six SUMO arm outputs per seed, **30/30 complete**. The *original aggregation job alone* failed on the generic Ubuntu runner because the module imports \`sumolib\` at import time. This is a software execution-environment defect, **not a scientific Test A failure**. No original probe scenarios were rerun, altered or selectively replaced.
- [Aggregation recovery PR #39](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/39) and [successful recovery run 41381425091](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41381425091). It used the unchanged frozen Python evaluator and the original Test A archive artifacts inside the original pinned SUMO container, with no change to forecast parameters, policy, sample, selection, or thresholds. Original 30 simulations were reused, not repeated.
- [Archived aggregate evaluation artifact 13113532802](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41381425091/artifacts/13113532802); original scenario artifacts: [4101](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833/artifacts/13113601035), [4102](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833/artifacts/13112598454), [4103](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833/artifacts/13113318421), [4104](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833/artifacts/13113303286), [4105](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833/artifacts/13113072566). GitHub Actions artifacts have 30-day retention.
- Permanent numerical records: [20 frozen singleton probes](results/exp007_test_a_probes.csv) and [five two-swap bundles](results/exp007_test_a_bundles.csv). Both derive from original aggregate JSON.

Test A changed one predeclared participant route at a time, **holding all other assigned road-edge sequences fixed** while allowing SUMO traffic flows and queues to react. \`predicted_externality = predicted_total_cost_change - predicted_self_cost_change\`; \`realized_externality = sum of realized scheduled-departure-to-arrival changes for the other 999 drivers\`. Negative values mean the route swap helps *other vehicles*. The model was a deliberately explicit, static 30-second-binned assignment-count cost proxy using the Experiment 003 high-regime clock correction. This was **not** a learned or field-validated physical bottleneck or queue response model.

## Frozen Test A result across the five independently generated seeds

| Seed | Singleton probes | Sign matches | Predicted zeros with material realized effect | Realized two-swap bundle total delta (network-seconds) | Bundle realized interaction vs sum of singleton outcomes |
|---|---:|---:|---:|---:|---:|
| 4101 | 4 | 1 | 1 | +617 | +218 |
| 4102 | 4 | 1 | 1 | +3,572 | −2,989 |
| 4103 | 4 | 2 | 1 | −1,490 | −2,672 |
| 4104 | 4 | 2 | 1 | −4,118 | −1,930 |
| 4105 | 4 | 2 | 1 | +979 | −1,502 |
| **All** | **20** | **8** | **5** | **Different signs across seeds** | **All five nonzero** |

The model predicted nearly additive bundle outcomes: its incremental bundle-minus-isolated predicted interaction was **0** in four seeds and about **−2.16 network-seconds** in one. The realized bundle-minus-isolated interaction ranged **−2,989 to +218 network-seconds**, with heterogeneous signs and large mismatches. This is specific evidence against treating separately estimated local increments as automatically additive under these simulator conditions. It is **not** a unique causal identification of a physical junction or queue mechanism.

### Additional transparent diagnostics

- Three of the five probes predicting an improvement to others (**negative predicted externality**) actually **increased** others' total realized time.
- The five "zero predicted" probes were counted as sign failures under the frozen exact sign-concordance rule; all five realized material effects, including both signs.
- Mean absolute realized externality: **1,802.25 network-seconds**; the close value of the prediction MAE to this magnitude is consistent with the model contributing very little usable scale information in this deliberately selected diagnostic sample, but not an independent out-of-sample R² estimate.
- The 20 probes were **purposively** selected at predicted rank extremes/near zero/median, not sampled at random across all feasible route changes. These observations are diagnostic, **not an unbiased estimate** of prediction quality across all routes, congestion conditions or road networks.
- Five seeds, not 20 independent driver samples, are the replication units. Per-probe values sharing an unchanged seed baseline are dependent. Sign fraction is a transparent prespecified screen statistic, not a formal population confidence interval. We do **not** claim an inferential estimate of global performance based on these 20 selected contrasts.

## Scientific interpretation and limitations

**Established within this study:** When a single eligible planned route was changed on the synthetic network, the chosen model's predicted signed externalities failed the frozen discrimination rule and substantially understated the magnitude of realized network spillovers in these preselected probes. The two-swap bundles also showed large interaction effects relative to individual-swaps-add-up assumptions. **No Test B efficacy or fairness comparison was made.**

**Plausible, not proven explanations:** the assignment-count and fixed edge-bin clock proxy fails to capture nonlinear junction discharge, queue interactions and discrete traffic flow transitions; very small predicted differences are unstable for ranking; predicted cost may miss some departure insertion and other vehicle interactions. These possibilities require *separately designed tests*. Results do not pinpoint a physical bottleneck, nor prove that no accurate prospective marginal estimator can be built.

**Comparison to previous research:** Exp003 established chosen-route timing improvements, not alternative-route counterfactual network externalities. Exp005 corrected a real assignment-clock mismatch, not this model's social-cost calibration. Exp006 A-vs-E remained mean-inconclusive with failed individual harm safeguards, and is not a modern traffic-aware navigation comparison. Experiment 007's Test A clarifies an additional empirical gap without overturning those historical outcomes.

**Fairness:** Individual changed-driver and nonparticipant elapsed outcomes were included in the paired SUMO records, but the **joint I-versus-S fairness criteria were not evaluated**, because the conditional policy comparison was not executed. The frozen 30-second / 10% severe-harm safeguard remains a **study-specific proposed policy gate**. No real human opt-in, safety or subjective journey quality was measured; subjective comfort/calmness remains explicitly deferred.

## Final scientific decision and future direction

**TEST A NO-GO: the specific frozen forecast model's marginal-externality signal is not sufficiently discriminative by its preregistered gate. TEST B NOT RUN. No evidence of a successful cooperative network-wide optimization policy from Experiment 007.**

The appropriate next research decision is **not** to rerun Test B after seeing this result, change the 60% gate, selectively exclude the zero predictions, tune a coefficient to rescue this particular model, or make a broad “cooperation cannot work” claim. First evaluate whether a physically better-founded, uncertainty-aware marginal-cost estimator (including bottleneck/queue dynamics and joint-assignment interactions) can be defined and validated on **fresh** development/confirmatory data. Cooperative departure timing remains a distinct candidate mechanism, not something disproved by this result.

The original 50-execution *conditional* footprint terminated properly after **30** successful Test A simulations. Scientific reporting is complete for this conditional test; no unexecuted Test B outcomes should be imputed.

**Communication:** This is a substantive negative scientific result and potentially suitable for a visual-first LinkedIn/X update, but **no social publication has been prepared, approved, or initiated here**. Actual media and captions require separate explicit user approval.
