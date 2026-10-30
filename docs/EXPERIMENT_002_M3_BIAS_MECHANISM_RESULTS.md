# M3 archived mechanism analysis — results and interpretation

**Evidence:** [Successful GitHub Actions run 41015381178](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41015381178), artifact 12959142102. All 30 archived M3 scenarios (seeds 3101–3110 × windows 200, 600, 1200 seconds) were processed. This is exploratory reanalysis of frozen held-out evidence; no new SUMO simulation.

## Findings

| Measure | 200s | 600s | 1200s |
|---|---:|---:|---:|
| Mean first-edge signed error (s) | 0.8444 | 0.6301 | 0.5231 |
| Mean within-vehicle consecutive-edge error increment (s) | 11.8593 | 4.2629 | 2.9274 |
| SD across 10 seed-level mean increments (s) | 0.5800 | 0.2268 | 0.0369 |
| Mean fraction of positive increments | 0.9150 | 0.9187 | 0.9094 |
| Mean observed inter-entry interval (s) | 26.5592 | 18.6346 | 17.2076 |

### Route-length-stratified mean increments (seconds)

| Observed route length | 200s | 600s | 1200s |
|---|---:|---:|---:|
| 1–4 edges | 13.4582 | 5.0614 | 3.5886 |
| 5–8 edges | 12.9598 | 4.4412 | 3.1108 |
| 9–16 edges | 11.2471 | 4.1315 | 2.7975 |
| 17+ edges | 9.1878 | 3.7648 | 2.5616 |

## Interpretation

Initial entry offset is small compared with subsequent positive increments, supporting **progressive timing underprediction** rather than a fixed departure-offset explanation. The increment is largest in the 200-second high-congestion regime and remains positive within every observed route-length stratum. Approximately 91% of consecutive-entry increments are positive in each regime.

This is an **association**, not a demonstrated causal source of delay. Entry-to-entry intervals combine travel and junction/queue effects. Stratifying by observed route length does not remove route selection, edge composition or congestion exposure differences. Seed-level SD is descriptive; no new confirmatory hypothesis test was performed. The same ten held-out seeds must not be reused as independent validation of a fitted correction.

## Decision

M3 exploratory mechanism analysis is complete. The next research experiment should test a **prespecified congestion-aware cumulative timing correction**, with separate development and fresh confirmatory seeds, against the unchanged frozen time-aware predictor and free-flow baseline. No claim of cooperative-routing benefit follows from this analysis.
