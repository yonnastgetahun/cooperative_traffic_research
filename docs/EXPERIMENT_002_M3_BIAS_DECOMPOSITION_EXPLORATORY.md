# M3 exploratory bias decomposition — first held-out case

**Source:** [M3 held-out run 40953111402](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40953111402), artifact `m3-eval-seed-3101-window-200` (ID 12933456625), `paired-road-entry.csv`.

**Scope:** One of ten prespecified seeds in the primary 200-second regime. Exploratory, not a new independent confirmatory evaluation.

Computed signed timing error as `native_entry_s - timeaware_predicted_s`, grouped by zero-based `route_index`. There were 8,424 paired road-entry records across 1,000 vehicles.

| Route index | N records | Mean signed error (s) | Median signed error (s) |
|---|---:|---:|---:|
| 0 | 1000 | 0.775 | 0.400 |
| 1 | 1000 | 13.902 | 5.038 |
| 2–3 | 1951 | 29.434 | 12.014 |
| 4–7 | 2969 | 66.867 | 47.725 |
| 8–15 | 1488 | 116.757 | 109.189 |
| 16+ | 16 | 140.247 | 139.036 |

Across all rows the mean signed error is 53.016s, and for route index > 0 it is 60.053s.

## Preliminary interpretation

The first-edge error is small relative to the later-edge errors. Thus a single fixed initial departure offset does not plausibly explain most of this seed's aggregate bias. The increasing mean signed error by ordinal is consistent with accumulated travel-time underprediction, but this cross-sectional pattern may also reflect differences in route lengths, vehicle cohorts, and censoring. It does **not** yet establish a causal mechanism.

## Next bounded analysis

1. Repeat this exact computation for all ten archived primary-regime seeds (3101–3110); summarize seed-level rather than treating road entries as independent replicates.
2. Compute **within-vehicle increments** in signed error between successive route indices, separating first-edge offset from subsequent accumulation.
3. Inspect predicted traversal cost, native edge-entry intervals, and route length strata. Distinguish congestion-dependent traversal mismatch from junction/dwell effects where the existing records permit.
4. Preserve M3 frozen evaluation artifacts. Any calibration model must be evaluated on fresh independent data, not presented as validated on these same held-out seeds.

No new simulations were run for this analysis.
