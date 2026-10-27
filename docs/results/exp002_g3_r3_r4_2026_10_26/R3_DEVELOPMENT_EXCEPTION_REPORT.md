# R3 — Three-regime exceptional-event and missingness development audit

**This checks observation policy on existing development seed 2101. It does not freeze M3 or validate the predictor.**

| Window | Teleport state | Count | Native empty bins | Partial bins | Exception gate |
|---|---|---:|---:|---:|---|
| 200s | ZERO_CONFIRMED | 0 | 3,268 | 360 | PASS_FOR_THIS_REPLAY |
| 600s | ZERO_CONFIRMED | 0 | 3,801 | 0 | PASS_FOR_THIS_REPLAY |
| 1200s | ZERO_CONFIRMED | 0 | 8,468 | 360 | PASS_FOR_THIS_REPLAY |

Native sampledSeconds displayed as zero can be rounded; absent speed/occupancy fields remain missing, not imputed as zeros.
Statistics are from strictly matched development replays with original route and tripinfo invariance; this does not retroactively change archived original outputs.
A nonzero teleport count blocks uninterrupted chosen-road timing claims; collision and teleport counts are not a real-world safety certification.
No evaluation seeds have been run.
