# Experiment 002 M3 — Consolidated Development Readiness Decision

**Decision date:** 2026-10-29. **Development rehearsal: GO (verified). Held-out evaluation execution: NO-GO / NOT AUTHORIZED.**

## Primary evidence

- [Successful full consolidated rehearsal, GitHub Actions run 40838046735](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40838046735).
- All three independent development-only jobs **200 / 600 / 1200 seconds succeeded** using preinspected demand seed **2101** and the pinned SUMO image.
- The consolidation job **succeeded** and uploaded `m3-consolidated-dev-readiness-evidence` together with three full per-regime artifacts.
- Frozen scientific source: `be2e8d27c78c8b6de4891115d6d951edc877ac6e`.

## What passed

The full qualification sequence regenerated the fixed network and demand, verified seed and topology invariance, reproduced the original chosen-route predictor, traced original search decisions, simulated native SUMO movements, captured 1-second FCD and 30-second native edge bins, audited R3 exceptions and scored paired road-entry timing. The second postprocessing pass independently repeated frozen native parsing, timing bridge, R3 exception output and seed-level timing metrics against the freshly generated development evidence. The unchanged cross-regime aggregator then compared the three scenarios with previously inspected development references. All four jobs completed successfully.

## What failed previously, and why

[Initial run 40832928677](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40832928677) passed all three development jobs but failed during consolidation because the aggregator was passed the unnormalized `qualification` directory instead of `qualification-for-aggregate`. The corrected source was rerun in run 40838046735 and passed. This was a workflow artifact-path defect, **not** a predictor error or change in the frozen scientific protocol.

## Decision boundary

**GO:** The existing complete frozen development simulation and independent native/R3/R4 postprocessing have now been demonstrated end to end in all three previously inspected regimes, with successful consolidated evidence preservation.

**NO-GO for held-out execution:** This is a single development demand seed, not 10 independent held-out seeds. The active `general_seed_driver_v01.py` still explicitly permits only seed 2101; the production evaluation runner, protected-environment release orchestration and complete per-attempt 30-scenario execution/archive semantics have not been independently qualified. The saved GitHub environment's 10-minute timer and administrator bypass controls are screenshot-supported but not independently API-verified. The disabled held-out template must remain disabled. No reserved seed 3101–3110 was generated or run.

## Next concrete action

Do not add another scientific milestone. The sole remaining engineering release task is to qualify the actual 30-scenario execution harness and release controls **without running any held-out seeds**. When that is complete, request separate explicit authorization to execute the held-out evaluation. This development GO is not that authorization.

**Scientific limitation:** M3 tests the accuracy of chosen-route road-entry forecasts; it does not directly establish causal effects of prediction error on network-wide cooperative routing.
