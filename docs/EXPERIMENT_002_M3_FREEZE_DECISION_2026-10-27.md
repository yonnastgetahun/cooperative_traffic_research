# Experiment 002 — M3 Scientific Protocol Freeze: Approval and Decision Record

**Decision date:** October 27, 2026 (America/Los_Angeles).  
**Decision:** **APPROVED — FREEZE THE SCIENTIFIC PROTOCOL ONLY.**  
**Evaluation:** **NOT AUTHORIZED.** No reserved held-out demand seeds have been generated, simulated, opened, or scored.

## Authoritative frozen references

- [Frozen M3 Scientific Protocol v1.0](https://github.com/yonnastgetahun/cooperative_traffic_research/blob/be2e8d27c78c8b6de4891115d6d951edc877ac6e/docs/EXPERIMENT_002_M3_FROZEN_PROTOCOL_V1.md)
- [Freeze Manifest: Git blob fingerprints and source SHA-256 checksums](https://github.com/yonnastgetahun/cooperative_traffic_research/blob/be2e8d27c78c8b6de4891115d6d951edc877ac6e/docs/EXPERIMENT_002_M3_PROTOCOL_FREEZE_MANIFEST_V1.json)
- **Authoritative Git commit:** `be2e8d27c78c8b6de4891115d6d951edc877ac6e`
- [Convenience frozen snapshot branch](https://github.com/yonnastgetahun/cooperative_traffic_research/tree/exp002-m3-protocol-v1-frozen). The commit ID, not the mutable branch name, is the reference that establishes immutability.
- [Successful no-SUMO preflight 40566574722](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40566574722): original measurement/seed fixtures, Python compilation, development seed guard, recorded SHA-256 fingerprints. **No held-out or other SUMO run performed by the preflight.**

## Exactly what is frozen

1. **Question and population:** A synthetic SUMO 10×10, 1,000-trip *chosen-route* external-road-entry timing forecast, not network-wide cooperative routing improvement.
2. **Primary regime:** high load, 200-second departure window; moderate 600s and low 1,200s are secondary and must both be reported.
3. **Reference:** native ordered link exit events including internal links, with inferred external-road entry at the original one-second simulation step. FCD front-position observations remain a distinct cross-check; native road vehicle-seconds/occupancy percent are **not** equated with route-assignment counters.
4. **Predictors:** unchanged original time-aware route-cost forecast and cumulative free-flow timing on identical chosen routes; no SUMO observation leaks into planning.
5. **Analysis unit:** independently generated OD demand **seed**, not an individual vehicle or road-edge visit. Per seed, evaluate time-aware vs free-flow MAE; primary effect `D=MAE_freeflow−MAE_timeaware`. Ten future independent paired seeds per regime, with sample-SD and two-sided Student-t 95% confidence interval across the seed-level differences (`df=9`) if all ten meet integrity criteria.
6. **Exceptions:** explicit teleport statistics; missing is not zero. Missing/teleported/route-divergent/invalid observations block a clean analysis, are reported with denominators, and do **not** trigger outcome-driven seed replacement. Empty and partial native road bins have explicit separate states.
7. **Implementation baseline:** code SHA-256 fingerprints and Git blob hashes in the frozen manifest, original SUMO **1.28.0** immutable image digest `sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`, original one-second solver step, unchanged route planning equations/limits and network/demand generation protocol.

## Evidence reviewed before freezing

- [G3 R0–R2](EXPERIMENT_002_G3_R1_R2_VERIFICATION_RESULTS_2026-10-26.md): all **25,179** external-road entries in three inspected development scenarios matched native vs FCD timestamps at the same simulation step; original policy and all **1,994,952** recorded search counter reads verified.
- [G3 R3–R4](EXPERIMENT_002_G3_R3_R4_EXECUTION_RESULTS_2026-10-26.md): explicit native **zero teleport** status and identical trip outcomes for three development replays, native empty/partial-bin classification, prespecified and tested seed-level uncertainty and source-hash accounting.
- The time-aware predictor remains systematically early in development results; better prediction error than a free-flow reference is **not** established calibration, traffic network optimization, causal junction delay, real-world safety or fairness.

## Non-execution boundary and next separate decision

A scientific protocol and inspected development-code snapshot are frozen. A full runnable **held-out execution harness has not been built or authorized**. Before any evaluation, a separate instruction must authorize execution readiness work and review of a manual-only workflow, immutable input provenance, frozen-code equivalence and artifacts/retention. Running the **reserved evaluation seeds 3101–3110**, even to preview them, then requires **its own explicit approval**.

If any later implementation changes the frozen scientific question, estimator, eligibility rule, analysis method, primary endpoint, original routing policy or seed registry, the work becomes an explicitly versioned **amended protocol** requiring approval *before* any new evaluation outcomes are viewed.

**Outcome:** M3 scientific protocol frozen v1.0. Evaluation not started; the holdout is still unopened.
