# Experiment 002 — G3 R1–R2 Verification Findings

**Date:** October 26, 2026 (Pacific). **Status:** Development instrumentation verification PASSED; **M3 not frozen and no held-out seeds evaluated**.

[Successful three-regime run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40456979518) · [Permanent results and per-edge CSVs](results/exp002_g3_r1r2_2026_10_26/README.md) · [Original approved scope](EXPERIMENT_002_G3_R1_R2_EXECUTION_SCOPE_2026-10-26.md).

## Design and controls

Reused **development seed 2101**, 1,000 trips per congestion regime (departure windows **200, 600, 1,200 seconds**). Inputs were the original M2 networks, trip demand, routes, forecast traces and FCD. SUMO image remained pinned at `sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`; the original one-second solver step was unchanged.

**R1 observation:** The external-road entrance timestamp was inferred from the previous native road/internal-link exit at SUMO step resolution, using tripinfo departure for the first road. FCD provided a separate first-front-position sample reference. All **8,393 external road visits per regime** matched by vehicle and ordered route index: **25,179/25,179 total**, with no missed joins. For every matched traversal, these two *timing* references agreed at the identical simulation step. **This does not imply that FCD vehicle-front counts equal native physical road occupancy.**

**R2 input provenance:** Original route/audit files were byte-identical with the actual-search observer enabled or disabled, and matched the archived M2 policy. Independent verification reconstructed **664,400 / 664,761 / 665,791** original search-edge count reads across the three regimes (**1,994,952 total**), including unchosen search branches. Each scenario recorded **8,393** original route-assignment counter updates. These counters are *planned route assignments*, not measured physical occupancy.

All **3,000 SUMO trips** reproduced their archived tripinfo results. No routing parameters, generated demand, SUMO step length or held-out seeds were changed.

## Development timing results

Road-entry prediction mean absolute error (seconds, lower better), using *identical chosen routes*:

| Departure window | Time-aware MAE | Free-flow MAE | Time-aware signed bias |
|---|---:|---:|---:|
| High / 200s | **51.32** | 56.65 | +51.22 |
| Moderate / 600s | **18.73** | 22.63 | +18.59 |
| Low / 1,200s | **13.41** | 16.83 | +13.15 |

Native event-step and FCD entry references give identical values **in these specific development simulations**. Positive bias means the model still predicts road arrival too early. These results are **not** held-out predictor calibration, proof of statistical significance, or evidence of better cooperative routing. Prior published results remain unchanged.

## Readiness decision

- **R0/R1 — PASS for the three tested regimes:** canonical step-level road-entry convention defined and verified with complete, ordered native/FCD matching.
- **R2 — PASS for the three tested regimes:** actual search-time counter reads independently verified with unchanged route choices.
- **R3 — PARTIAL:** teleport and exceptional-route policies, sparse/partial native edgeData bins, and full reproducibility/retention schema need explicit treatment.
- **R4 — PENDING:** prespecify seed-level uncertainty reporting and analysis before independent evaluation.
- **M3 protocol freeze — NOT APPROVED:** existing physical-occupancy semantics and causal junction-delay limits remain; there is no claim that the predictor accurately forecasts physical occupancy or that internal-link residence measures causation.

**Next decision:** Complete R3/R4 measurement and analysis definitions, then review a distinct M3 freeze proposal. Reserved evaluation seeds **3101–3110 remain untouched**. See the [G3 sufficiency review](EXPERIMENT_002_G3_OBSERVATION_SUFFICIENCY_REVIEW_2026-10-26.md) and [limitations register](EXPERIMENT_002_G3_MEASUREMENT_LIMITATIONS_REGISTER_2026-10-26.csv).
