# G3 native-versus-FCD timing bridge: three development regimes

**Status: Three development regimes checked. No M3 freeze or held-out validation.**

| Window | Native time-aware MAE | FCD time-aware MAE | Native free-flow MAE | Verified search reads |
|---|---:|---:|---:|---:|
| 200s | 51.32s | 51.32s | 56.65s | 664,400 |
| 600s | 18.73s | 18.73s | 22.63s | 664,761 |
| 1200s | 13.41s | 13.41s | 16.83s | 665,791 |

All cases reuse prespecified seed 2101 and the unchanged original policy.
Native SUMO road entry is inferred from ordered preceding link exit at the one-second solver step.
FCD first external road observation measures a vehicle-front sample at one-second cadence.
The references are retained separately; neither measures actual native physical body occupancy.
True search-time route-assignment counts were independently verified in all three conditions.
Prediction quality is not certified by these instrumentation passes.
Prior published FCD error reports remain historical, unchanged.
Reserved evaluation seeds 3101–3110 remain untouched.
