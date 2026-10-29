# M3 supervised frozen development rehearsal — verified evidence

**Date:** 2026-10-29. **Decision:** GO for development-supervisor integration only. **Held-out execution: NO-GO / NOT AUTHORIZED.**

## Primary execution evidence

[GitHub Actions run 40944291962](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40944291962) on commit `08321edbf42d88c1e6fdcc4118a63068e3407142` completed successfully. The full frozen SUMO development pipeline was executed through `development_attempt_supervisor_v01.py`, using previously inspected seed **2101** in the 200s, 600s, and 1200s regimes.

| Window | Job | Result | Artifact ID |
|---|---|---|---|
| 200s | supervised-development (200) | SUCCESS | 12928297411 |
| 600s | supervised-development (600) | SUCCESS | 12928846135 |
| 1200s | supervised-development (1200) | SUCCESS | 12928736315 |

All three job logs contain `DEVELOPMENT_POSTPROCESS_REPRODUCED_FROZEN_REFERENCE`. The artifacts were uploaded successfully with 30-day retention. The supervisor preserves per-attempt logs and copies available results into a dedicated archive, including on nonzero exit. Separate offline subprocess tests in [run 40944022907](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40944022907) passed injected failures, preservation, and no-overwrite safeguards.

## Limits and outstanding release gates

- The executable supervisor is intentionally restricted to seed 2101 and does **not** establish general-seed production execution readiness.
- Real SUMO stage-failure injection and complete recovery/aggregation across 30 real scenarios have **not** been demonstrated.
- The actual production runner and frozen R3/R4 general-seed adapters still require qualification using permitted inputs.
- The protected GitHub environment's timer, bypass and branch policy remain **not independently verified** through the available connector.
- No active held-out workflow was enabled, and no reserved seed 3101–3110 was generated, simulated, or inspected in this qualification.

**Next action:** Complete production adapter/orchestration implementation and independently verify release controls, preserving the explicit separate held-out authorization boundary. Do not conflate development GO with held-out execution GO.
