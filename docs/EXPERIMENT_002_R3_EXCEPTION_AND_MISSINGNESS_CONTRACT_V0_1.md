# Experiment 002 — R3 Exceptional Events and Missing Data Contract v0.1

**Status:** **Approved and executed successfully on the three development scenarios, October 26, 2026.** [R3–R4 findings and gate evidence](EXPERIMENT_002_G3_R3_R4_EXECUTION_RESULTS_2026-10-26.md). **M3 is NOT frozen; no held-out seed access permitted.**  
**Source:** [R0–R2 verification](EXPERIMENT_002_G3_R1_R2_VERIFICATION_RESULTS_2026-10-26.md) · [Observation sufficiency review](EXPERIMENT_002_G3_OBSERVATION_SUFFICIENCY_REVIEW_2026-10-26.md).  
**Execution scope:** Previously inspected seed **2101** under windows **200, 600, 1,200 seconds**, with no route, demand, physics, or predictor changes. Later apply identical rules to every frozen evaluation scenario.

## Purpose and three-valued evidence

An uninterrupted trip and a completed trip are not synonyms. SUMO can teleport stuck vehicles and omit them from FCD during teleportation. For the event `teleport_count` distinguish **ZERO_CONFIRMED** (explicit native statistic and event evidence), **NONZERO_CONFIRMED**, and **UNKNOWN_NOT_CAPTURED**. An absent statistic field does **not** mean zero. Do not make a clean-teleport claim from tripinfo completion or FCD-only matching.

**Primary observation reference:** ordered native SUMO vehicle external-entry step inferred from preceding link exit (or actual departure for first external edge), compared with same chosen-route pre-SUMO prediction. Units are seconds at the original 1-second simulation step.

**Exceptions, machine-readable codes and disposition:**

| Code | Trigger | Treatment |
|---|---|---|
| `MISSING_PLANNED_TRIP`, `DUPLICATE_VEHICLE_ID` | planned count/IDs invalid | **BLOCK** measurement gate |
| `MISSING_TRIPINFO`, `UNFINISHED_TRIP`, `NEGATIVE_DURATION` | missing/future/censored trip outcome | **BLOCK** full-population analysis; report as missing, not zero |
| `EXPLICIT_TELEPORT`, `UNKNOWN_TELEPORT_COVERAGE` | native statistic positive / absent | **BLOCK** clean-timing certification; count teleports and keep affected road visits separate when identified |
| `ROUTE_SEQUENCE_MISMATCH`, `DUPLICATE_ROUTE_INDEX` | actual external path differs from planned ordered route | **BLOCK** affected joins and complete-coverage gate; retain original source |
| `FCD_GAP`, `FCD_DUPLICATE_VEHICLE_STEP`, `MISSING_FCD_LANE` | timeline not full 1s or lane absent | **BLOCK** paired timing/FCD reference; preserve native events if valid but do not silently substitute |
| `NEGATIVE_EVENT_INTERVAL`, `EVENT_COUNT_MISMATCH` | malformed native exit-time sequence | **BLOCK** timing reference |
| `PARTIAL_NATIVE_BIN` | final native interval not full 30 seconds | report actual begin/end and coverage; exclude from full-bin comparisons **only**, not from trip outcomes |
| `EMPTY_NATIVE_EDGE_NO_SAMPLES` | `sampledSeconds=0` with native occupancy/speed absent | classify as **not applicable** field, never fabricate zero speed |
| `MISSING_NATIVE_METRIC_WITH_POSITIVE_SAMPLES` | occupied edge but required metric absent | **BLOCK** affected field-level comparison and record missingness |
| `ROUNDED_SAMPLED_SECONDS_ZERO` | native `sampledSeconds=0.00` | treat as **displayed zero with rounding uncertainty**, not proof zero physical vehicle-time |
| `UNEXPECTED_DYNAMIC_REROUTE`, `UNRECONCILED_SIMULATOR_CHANGE` | route or per-vehicle baseline diverges | **BLOCK** provenance gate |

A record can carry multiple codes. Missingness is **not missing completely at random by assumption**. Do not impute zero, delete affected vehicle-edges silently, or present complete-case metrics as unbiased results. A full per-edge error claim requires a verified event for every planned edge; if a scenario fails, retain all source artifacts and report denominator/exclusion counts, then investigate/replay the **same development** scenario as appropriate. For a future held-out scenario, deviations are evaluated under a separately approved, preregistered incident-response rule with no score-based tuning.

### Teleport and safety checks

Use SUMO **`--statistic-output`** (`teleports.total`, optional breakdown), `--collision-output`, and log/warnings where supported; record every field's provenance and whether it was *actually collected*. A count of zero means zero **reported** teleports for that simulation under that setting, not global safety. Prior M2 packages lack explicit statistics and must remain `UNKNOWN_NOT_CAPTURED` until a **strictly matched development replay** has been independently verified.

The R3 replay must use archived seed 2101, identical chosen routes, pinned SUMO 1.28.0 digest, 1-second solver step, and all 1,000 original trip records. Adding observer files is allowed; modifying teleport thresholds, car-following, collision behavior, routes or time-step length is prohibited. Compare per-vehicle `tripinfo` depart, arrival, duration, waitingTime, timeLoss and departDelay to the archived run; fail if any differ.

### Native edgeData and FCD integrity

For external `edgeData`: require numeric nonnegative `sampledSeconds` and unique edge/time interval; validate half-open `[begin,end)`, full 30-second bins and actual end of partial final bin. Keep **empty edge**, **zero displayed sampledSeconds**, **missing field**, and **partial interval** distinct; SUMO may omit speed/density/occupancy/waitingTime on unused edges. Native percentage occupancy must not be subtracted from front-based FCD counts or the planner's prior assignment counts. Report count and coverage by class across all roads, not only occupied ones.

For FCD: verify every emitted timestep at exactly one original simulation second; within each timestep IDs unique, lanes present; track any vehicle disappearing before its observed arrival and any reappearance. Vehicle absence before departure or after arrival is expected, not a missing-record error. An unexplained gap during active travel is an exception, even if native tripinfo completed.

### Reproducibility and decision gates

Record code SHA, pinned image digest, SUMO version, scenario seed/window, exact network/trips/route SHA256, original M2 run IDs, simulator observer options, counters, and the immutable output hashes. Archive `r3-exceptions.json`, `r3-native-bin-status.csv`, and the source `statistic.xml`, collision log, and tripinfo invariance proof.

**R3 PASS only if:** (1) schema/fixture tests pass, (2) all planned routes/trips and native/FCD event joins are complete, (3) the explicit teleport statistic is parsed and handled under this policy, (4) native empty/partial/missing classifications are complete, (5) full tripinfo invariance and source hashes are verified, and (6) no unclassified exception is silently ignored. **Pass denotes defensible measurement handling, not a calibrated predictor or an assertion of real-world safety.**

References: [SUMO Statistic Output](https://sumo.dlr.de/docs/Simulation/Output/StatisticOutput.html), [teleports and FCD limitations](https://sumo.dlr.de/docs/Simulation/Why_Vehicles_are_teleporting.html), [native edgeData empty/partial semantics](https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html).
