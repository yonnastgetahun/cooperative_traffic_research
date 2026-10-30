# Experiment 004 — Verified adapter-equivalence result and four-arm design freeze

**Evidence:** [GitHub Actions run 41023185707](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41023185707), commit `ac3132a14a2e07ffd766ae2ff2d6835b3f3e43db`, three archived regime artifacts. All jobs succeeded, but their reported equality tests were **false**.

| Departure window | Original and stateful zero-calibration route files byte-identical? | Audit files byte-identical? | Decision |
|---|---|---|---|
| 200s | No | No | Adapter-only control required |
| 600s | No | No | Adapter-only control required |
| 1200s | No | No | Adapter-only control required |

These findings establish an implementation difference under zero correction. They do not yet quantify how many vehicle routes differ, nor any travel-time effect. The test uses inspected development seed 2101; it is not a network-wide routing-outcome experiment.

## Frozen prospective four-arm comparison

**A — Independent routing:** Original independent baseline; no cooperative occupancy penalty.

**B — Original cooperative routing:** Frozen original time-aware cooperative algorithm with original forecast and original search state.

**C — Stateful adapter, calibration OFF:** New ordinal-aware search with offset and per-edge coefficients set to zero; original guardrails and occupancy-update rule.

**D — Stateful adapter, calibration ON:** Exactly the same stateful search, guardrails and occupancy-update rule as C, but uses frozen Experiment 003 coefficients:
- 200s: offset 4.053135104279146 s; per-edge 11.524898884412591 s
- 600s: offset 1.7868471223107676 s; per-edge 3.9515691107998387 s
- 1200s: offset 1.8903085164618962 s; per-edge 2.6820862794976956 s

**Primary causal contrast:** D versus C at 200s, paired by independent demand seed, testing whether enabling calibration changes mean completed-trip travel time while holding the stateful search implementation fixed.

**Secondary comparisons:** D versus C at 600s/1200s; C versus B to measure adapter effects; D versus B for the combined intervention; D versus A to test whether the calibrated cooperative approach improves upon independent routing. These secondary contrasts must not be described as the isolated causal effect of calibration.

## Execution and analysis rules

1. Use the same 10×10 synthetic network and 1,000 vehicle demand instances per scenario. Run all four arms with exactly the same fresh demand seed and regime. Do not reuse seeds 2101, 2201–2210, 3101–3110, or 3201–3210 as a new confirmatory cohort.
2. Prespecify the exact fresh seed identities and the fixed algorithm/adapter revisions **before** running any outcome simulation. Do not change model parameters or pick winners after seeing network results.
3. Preserve per-arm routes, assignment audits, SUMO tripinfo, network statistics, collision/exception evidence, and route-change counts.
4. Primary outcome is seed-level paired difference in mean completed-trip travel time between D and C under 200s. Report 95% Student-t confidence interval using independent demand seed as the unit. Predefine handling of incomplete/censored trips and report completion fraction alongside travel time; do not claim improvement by excluding delayed or unfinished vehicles.
5. Secondary outcomes include completed-trip fraction, 90th-percentile trip time, throughput, fairness by OD cohort, exception/collision integrity and all three regimes.
6. The original two cooperative prototypes are not interchangeable. Arm B explicitly uses the time-binned `time_aware.py` algorithm, not `cooperative.py`. A separate study would be required to evaluate the other cooperative prototype.
7. **Critical validity check:** D and C must differ only in the fixed calibrated forecast input. Document and verify the decision-time use of route ordinal, forecast clock, candidate costs and assignment updates. Future observed SUMO data must never enter routing decisions.

## Scientific decision

The Experiment 003 chosen-route prediction-accuracy result remains independently supported, but does not establish any network-wide benefit. The four-arm Experiment 004 design is frozen **at the arm and endpoint level** by this document. Execution is not authorized as scientifically ready until the exact fresh seed manifest and algorithm revisions are committed and the prospective C/D decision-time interface is verified. This is a bounded scientific implementation requirement, not a new general readiness program.

**No Experiment 004 network-wide traffic outcome has yet been measured.**
