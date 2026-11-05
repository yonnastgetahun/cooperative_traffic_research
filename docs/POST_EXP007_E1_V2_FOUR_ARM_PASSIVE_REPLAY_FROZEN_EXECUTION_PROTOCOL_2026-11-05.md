# Frozen execution protocol — E1-v2 four-arm passive vehicle replay

**Authorization:** Explicit user approval on November 5, 2026 to execute the [published four-arm plan](POST_EXP007_E1_V2_FOUR_ARM_PASSIVE_VEHICLE_REPLAY_SCIENTIFIC_PLAN_2026-11-05.md). No authorization for estimator revision, expanded experiments, held-out validation, Test B or social publishing.

## Why this matters to the underlying research

Cooperative-routing efficacy would depend on forecasting how a change in one planned route affects all other drivers, versus equally informed independent routing. E1-v2 passed engineering tests but failed empirical externality qualification. F0–F5 established substantial realized network response but lacked exact vehicle-level edge and junction observations. The present historical instrumented study seeks evidence about actual arrival order, stopped queues, receiving links and junction movements; it is **not** a test of policy efficacy, an E1-v2 rescue or a novel independent validation.

## Original science remains frozen

- E1-v2 D1 **DEVELOPMENT_NOT_QUALIFIED** (MAE 1478.5625 vs B0 1478.0625 network-s; 5/16 correct signs vs 60% gate).
- Selected original arms: **6112/I, 6112/probe2 (veh0142), 6113/I, 6113/probe2 (veh0038)**. Historical +3215 and −3960 network-s externalities respectively; +3219 and −3883 all-driver network-s respectively.
- Source original 60-arm run 41966516110 at commit a54b6f650b16a22b0eb5543bb507f9faf5eea034, original 695-member release, and post-F0–F5 permanent observations.
- All four arms were selected **after viewing outcomes**; only two independent historical demand seeds.
- Original future validation seeds **6201–6212** and cooperative Test B **6301–6312** remain unopened.

## Frozen execution identity

**SUMO:** Version 1.28.0; image ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb.

**Approved code:** research/replay/e1v2_four_arm_instrumented.py, original source Git blob c4c10fd7eb463f72eac6cb9685820b8d8b572121; the only pre-simulation repair so far changed the direct-script sibling helper import path, not the estimator, SUMO flags, study population, data, measurements or gates (PR #91 preflight run 42112414233 failed before SUMO with ModuleNotFoundError). Record the executing merge commit and actual script SHA. Record executed checkout commit and actual file SHA.

**Input control:** Original network.net.xml, trips.xml, original I/probe2 routes and immutable predictions, unchanged network physics/car-following, right-of-way, random seed, timestep, vehicle classes, scheduled demand and all route assignments. The original source member ledger of 695 files must SHA-match. Only observational FCD, vehroute exitTimes, 5s edgeData and laneData output options are allowed. Do not invoke any demand generator, estimator, router or optimization intervention.

**Storage:** Four arms only; no auto rerun or extension; 512 MiB compressed observational output maximum per arm and 2 GiB over four; full 1s FCD for all 1000 vehicles, no downsampling.

## Mandatory gates

**G0 — original data:** Verify all source SHA256 ledger members; seed-specific frozen network/trips/route/tripinfo/statistics hashes, all 1000 identities; verify exactly one and only one route change in each probe2 arm. Any mismatch STOP before simulation.

**G1 — source/container:** Confirm pinned 1.28.0 SUMO executable and mandatory passive output options including internal-lane observations and vehroute exit times. Record exact command. Unsupported mandatory channel STOP before simulation.

**G2 — original-outcome equivalence:** Each of 1000 per-arm drivers must reproduce original depart, arrival, duration, departDelay, waitingTime and timeLoss within <=0.02 seconds per recorded field. Matched total scheduled-to-arrival network time differs from original by <=0.1 network-second. Collision XML count and available structured safety statistics must agree exactly. Any mismatch invalidates the corresponding pair and stops scientific interpretation; never loosen the threshold post hoc.

**G3 — vehicle-resolved observation:** 1000 FCD vehicle IDs, timestamps, lane IDs, x/y, pos and speed, 1s time-step resolution, trajectories covering each trip; same planned vehroute edges and complete native exitTimes; detector coverage through final completion. Subsecond crossings and short-lived internal lanes may be censored at 1s; do not invent exact entry times. Missing critical observation yields MEASUREMENT_INSUFFICIENT, not a bottleneck conclusion.

**G4 — fixed descriptive analysis:** Time-align matched driver traces without shifting the clocks; calculate first different observed time, actual per-edge first FCD sample, original scheduled-to-arrival effect and insertion/duration/waiting components, driver and nonparticipant harm, near-stop observations at <=0.1m/s and sensitivity <=1m/s, contiguous spatial groups of >=3 stopped cars separated by <=10m, and observed junction internal-lane samples when supported. Report contradictory and unobserved cases. Do not fit new parameters or interpret correlation as unique junction causation.

**Boundary:** Frozen E1-v2 records do not contain prospective *per-edge* event forecasts. New observed FCD edge times cannot be claimed as E1-v2 model-vs-truth edge prediction errors. Four singleton arms cannot localize all ten earlier two-route bundle interactions.

## Controlled workflow

Pre-merge PR preflight may inspect original archive and pinned SUMO options, **without executing SUMO simulations**. Once the design is merged into main, exactly one non-retrying four-arm execution workflow with github.run_attempt == 1 may perform the four approved SUMO replays, gate-check and archive outcomes. Preserve failures and original files. Publish one consolidated scientific report and permanent checksum-verified trace release only after validity assessment. If blocked, publish the blocker, not new simulations.

**Valid dispositions:** VALID_RETROSPECTIVE_OBSERVATIONAL_REPLAY_CAUSAL_SOURCE_UNIDENTIFIED, INTEGRITY_FAILURE, MEASUREMENT_INSUFFICIENT, or EVIDENCE_DISFAVORS_CANDIDATE. None can automatically qualify E1-v2 or authorize Test B.

No automatic publication to LinkedIn/X; prepare visuals separately only if user requests and approves them.

**Protocol frozen prospectively for instrumentation, not prospectively selected experimental cases.**
