# G3 — Offline reconciliation first-pass report

**Status: measurement diagnosis advanced, G3 remains OPEN; NO held-out validation.**

[Source M2 artifacts](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958#artifacts).
Nine previously completed development-seed scenarios were processed. No new SUMO runs or route changes.

## Busy external roads (native sampledSeconds >= 30 per full 30-second bin)

| Window | Bins | Absolute disagreement / native sum | Largest edge-bin discrepancy |
|---|---:|---:|---:|
| 200s | 6,700 | 4.5% | 30.0 vehicle-seconds |
| 600s | 4,844 | 4.9% | 30.0 vehicle-seconds |
| 1200s | 2,290 | 4.4% | 30.0 vehicle-seconds |

This is an **observational measurement mismatch**, not a proven SUMO error.
Empty bins are reported separately; native partial last bins with unavailable aligned FCD are counted as incomparable, not set to zero.

## Junction evidence

66,853 route transitions show internal-lane samples, and 317 do not.
Conservative 1-second **sample-based** internal dwell limits total 51,116–185,139 seconds.
They do not isolate junction-caused delay; external approaches can contain queues. A previous zero unresolved-seconds value was bookkeeping, not perfect timing certainty.

## Decision gates

| Gate | Status |
|---|---|
| G3-0_source_integrity | PASS |
| G3-1_occupancy_mechanisms | OPEN |
| G3-2_junction_sampling_bounds | PARTIAL |
| G3-3_live_search_time_lookup_capture | OPEN |
| G3-4_freeze_ready | NO |

## Required next diagnostic work

1. Inspect outlier edge-bins against raw FCD vehicle IDs, lane positions, speed and network geometry before assigning a physical explanation.
2. Investigate time-boundary/cross-edge vehicle-extent effects and compare occupied-bin errors; classify unresolved cases explicitly.
3. To claim actual search-time occupancy lookup provenance, add non-policy-changing event capture or narrow the research claim to chosen-path replay.
4. Revisit G3 only after a reconciled case ledger; **do not freeze M3 or touch evaluation seeds 3101–3110**.

Better forecast MAE on chosen routes does not imply better cooperative-routing outcomes.
