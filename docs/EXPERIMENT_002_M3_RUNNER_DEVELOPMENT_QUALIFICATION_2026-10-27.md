# Experiment 002 — Frozen M3 Runner Development Qualification and Activation Decision

**Date:** October 27, 2026 (Pacific).  
**Result:** **DEVELOPMENT-ONLY END-TO-END QUALIFICATION PASSED** in all three inspected congestion conditions.  
**Activation status:** **HELD-OUT WORKFLOW NOT ACTIVE; HELD-OUT EVALUATION NOT AUTHORIZED OR RUN.**

## Authorized preparation and evidence

The user approved **preparing and verifying** the future M3 held-out execution pipeline on development data, expressly **without running reserved evaluation seeds**. The scientific protocol had already been [frozen at commit `be2e8d27c78c8b6de4891115d6d951edc877ac6e`](https://github.com/yonnastgetahun/cooperative_traffic_research/commit/be2e8d27c78c8b6de4891115d6d951edc877ac6e). The original freeze remains unchanged.

- [Successful qualification run 40570158400](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40570158400) — original frozen code, immutable SUMO image, one development seed × all three regimes, source-matching / routing / event / scoring gates.
- [Successful permanent publication run 40570984305](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40570984305) — verified every source artifact, saved per-edge timing comparisons and compact audit evidence.
- [Durable qualification evidence archive](results/exp002_m3_qualification_2026_10_27/README.md) — source fingerprints, route/audit and tripinfo invariance, reconstructed inputs, individual seed-level timing reports and error breakdowns.
- [Development-only executable GitHub workflow](../.github/workflows/experiment-002-m3-development-qualification.yml) — intentionally restricted to inspected seed 2101, 200/600/1200-second departure windows.
- [Full frozen-source development runner](../experiments/experiment_002/m3_qualification/run_development_v01.sh) · [fail-closed source/seed guard](../experiments/experiment_002/m3_qualification/guard_v01.py) · [seed-level scorer](../experiments/experiment_002/m3_qualification/score_v01.py).


**Draft for review, not an active held-out workflow:** [Explicitly disabled execution template](templates/experiment-002-m3-heldout-evaluation.yml.disabled). The template is outside `.github/workflows`; every job is disabled. No evaluation-seed workflow can run from it without a new reviewed code change and separate user authorization.

## Verified results

**Three 1,000-trip synthetic development scenarios** (existing seed 2101) passed the six unit fixtures, frozen-source SHA checks for fourteen files, regenerated 10×10 network topology and exact OD/departure schedule equivalence, original route/audit byte comparison with and without tracing, 1-second native/FCD ordered-road timing joins, all actual search-time assignment counter reads and update revisions, full per-vehicle tripinfo invariance, and explicit native teleport/exception checks.

| Window | Completed trips | Ordered road-entry matches | Search-time reads independently verified | Time-aware entry MAE (s) | Free-flow entry MAE (s) | Reported teleports |
|---|---:|---:|---:|---:|---:|---:|
| 200s, high congestion | 1,000 | 8,393 | 664,400 | **51.32** | 56.65 | 0 |
| 600s, moderate | 1,000 | 8,393 | 664,761 | **18.73** | 22.63 | 0 |
| 1200s, low | 1,000 | 8,393 | 665,791 | **13.41** | 16.83 | 0 |
| **Total** | **3,000** | **25,179** | **1,994,952** | — | — | **0** |

All three matched the previously published development outcomes to the same measurement precision. The time-aware model remains systematically early under congestion. **This verifies implementation invariance, not predictor calibration or improved traffic routing.**

The first attempt [40569925000](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40569925000) stopped at the source-commit guard because the manifest distinguished the protocol-document commit from the final manifest-inclusive freeze commit. Those two immutable references were clarified **without relaxing the SHA256 checks**, and the successful end-to-end run followed. An archival-only retry fixed an enum label mismatch and did not rerun traffic.

## Precise readiness classification

| Component | Status |
|---|---|
| Frozen scientific source, SHA-256 fingerprints and pinned SUMO image | **Verified** |
| Original network/OD generator equivalence against archived demand | **Verified for seed2101 in three regimes** |
| Routing and chosen-route prediction invariance | **Verified** |
| Actual planning occupancy-counter read provenance | **Verified** (not physical road occupancy prediction) |
| Native external-road entry and FCD front observation joins | **Verified** |
| R3 native teleports and missingness policy | **Verified in development** |
| R4 per-seed MAE/bias/route-position summaries and synthetic ten-seed CI fixtures | **Verified in development** |
| Independent seed-3101–3110 execution adapter | **Not implemented or reviewed** |
| Full eligible ten-seed/regime aggregation and incident-response harness on actual evaluation data | **Not executed** (requires distinct approval) |
| Active held-out workflow | **None** — intentionally inactive |
| Formal held-out evaluation / result / efficacy claim | **Not started; not authorized** |

**Why no active held-out workflow yet:** The frozen R3 implementation deliberately hard-codes permitted **development seed 2101**, and the frozen R4 analyzer deliberately accepts only development seeds 2101–2103. Extending these to an evaluation execution adapter is a purely mechanical implementation task that must preserve scientific equivalence, but has **not been approved for deployment or tested on the reserved seeds**. The currently active code rejects all reserved seeds before demand generation.

## Recommended next separate authorization

[Inactive held-out runner readiness blueprint](EXPERIMENT_002_M3_HELDOUT_RUNNER_READINESS_BLUEPRINT_V0_1.md) details an eventual **manual-only** workflow with a separately reviewed authorization gate, fixed frozen-code reference, seed-specific output hashes, strict R3 eligibility and R4 seed-level uncertainty across the prespecified ten independent demand seeds per regime.

The next discrete action would be to **review and authorize building/activating the final manual-only held-out adapter and its guard**, with synthetic/development verification of mechanical equivalence. A **further explicit authorization is required to execute any reserved evaluation seed**. No `push`, scheduled or autonomous trigger may be able to dispatch the held-out experiment.

**Scientific exclusions remain:** The model's prior assigned-route counts are not calibrated physical occupancy forecasts; internal-link residence is not causal junction delay; lower forecast MAE on chosen routes is not proof that cooperative routing improves total traffic flow; synthetic SUMO results do not certify real-world safety.

**Final outcome of this approved preparation:** All three development rehearsals passed; results and hashes are durable on GitHub. Held-out data and execution remain untouched and unauthorized.
