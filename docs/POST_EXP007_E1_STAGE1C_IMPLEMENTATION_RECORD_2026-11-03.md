# E1 Stage 1C — Source Implementation and No-SUMO Verification Record

**Date:** November 3, 2026  
**Status:** Research prototype implementation; **not trained, not calibrated on new data, not independently validated, not ready for Test B.**  
**Authority:** Stage 1C implementation and mandatory unit tests only, following the frozen [Stage 1B development protocol](POST_EXP007_E1_EXECUTABLE_DEVELOPMENT_PROTOCOL_V1_2026-11-03.md).

## Delivered

A standalone, dependency-free Python implementation under [`research/externality_estimator/`](../research/externality_estimator/) containing:

- `schema.py`: typed, immutable road/turn/vehicle scenarios, explicit time cutoff and rejected future-label features; 1,000-driver research schemas also accept fractional scheduled departures.
- `scenario_io.py`: **static-only SUMO network/announced demand/route XML reader** (not a simulator) with conservative junction-conflict groups and explicit speed-factor prior.
- `link_turn_queue.py`: one-second, deterministic finite-link-storage FIFO network evolution, shared junction turn-service and receiving constraints, blocked source insertions, stop/abstain at 1,800 seconds, per-driver events and conservation checks.
- `counterfactual_rollout.py`: baseline and individual/bundle reassignments using two complete forward predictions; direct per-identity predicted self, other and nonparticipant changes, with reproducible hash and uncalibrated-status flag.
- `candidate_routes.py`, `dataset_contract.py`: legal bounded alternatives and prospectively hash-selected development-only probe/bundle cohorts; no post-treatment outcomes used for selection.
- `baselines.py`, `state_estimator.py`, `uncertainty.py`, `externality_outputs.py`, `audit.py`, `label_builder.py` (offline-only): null, historic-proxy, own-only comparators, zero-initial-state inference, provisional reliability, signed accounting, partition controls and separate offline paired-SUMO label reader.
- Dedicated [GitHub CI workflow](../.github/workflows/exp007-e1-stage1c-no-sumo.yml) installs **no SUMO**, compiles the modules, tests 18 scientific fixture gates plus three static-input/partition tests, and enforces predictor-label import separation.

## Verified tests, and what they DO and DO NOT prove

**Local no-SUMO test suite: 21/21 PASS** on the authored Python implementation. These comprise all **T01–T18** mandatory Stage 1B gates and three added static network/demand/route intake checks. The most important original-identity-breaking fixture is:

> Two legal, equal-free-flow alternative routes produce **zero** predicted travel-time change for the rerouted driver, but **−1 second** of predicted travel-time change for a different, nonparticipating driver due to shared junction turn capacity.

The sign-reversal version produces the opposite externality; a separate two-target bundle fixture yields joint network cost **+1 second** versus **+2 seconds** from summing the isolated swaps. This is a *model-structure and accounting test*, not independent traffic forecast validation.

Other required fixtures verify link storage, mass conservation, turn service/receiving, FIFO, queue blocking, insertion delay, no-swap zero, missing-state rejection, no future-label leakage, byte-identical predictions, ID-based nonparticipant sums, strict build/check/holdout partition rules, and explicit 1,000-driver noncompletion/abstain (no completed-only results).

**No-SUMO scalability smoke tests (NOT validation):** One locally generated, 1,000-vehicle synthetic grid with 360 directed road edges cleared in **440 model seconds**, using about **0.61 wall seconds** on the local Python container. A *historical-input-only engineering smoke* parsed original Experiment 007 seed 4101's 1,000 scheduled demand entries, 360 edges and 1,320 legal static turns, without using SUMO outcomes as predictor input; an uncalibrated E1 forward rollout cleared in **427 model seconds**, about **0.69 local wall seconds**. These smoke results are contingent on the simplified model and do **not** mean E1 predicts actual SUMO traffic correctly or satisfies future CI resource gates on a different runner.

## Explicit scientific and engineering limitations

- The link model uses **one FIFO queue per directed link**, not cell-level shock-wave propagation. Distinct turn pockets, lane-changing and exact SUMO junction phase/priority details are not reconstructed; conservative per-junction conflict groups may overconstrain discharge.
- The static SUMO XML adapter uses network geometry and legal turns but does **not** know private future driver speed variations or physical queues. Unspecified individual speed factors use declared predecision prior 1.0.
- **Fractional announced departure times** in the original demand are eligible at the next 1-second tick; arrival predictions stay in one-second resolution and always subtract the exact fractional scheduled departure. This model discretization could affect real externality forecast skill and must be audited prospectively.
- The primary estimator is deterministic and its output is **UNCALIBRATED_POINT_ESTIMATE**. No confidence interval, human risk guarantee, uncertainty calibration or mobile/online latency capability has been demonstrated.
- Offline development is not started; Stage 1B §4's proposed 60 SUMO scenario arms have **not** been dispatched. The four development-check seeds are *not* Stage 2 independent validation.
- Candidate assignment, junction conflict metadata fidelity, service tokens, stable cohort labels and cross-run portability must be source-reviewed before permitting any new SUMO run.
- Missing or late in-flight network state is rejected/abstained because E1 v1 currently supports only an empty initial state at t0=0. **Do not silently substitute an empty state for a nonempty network.**

## Next authorization gates

1. **COMPLETED:** [Stage 1C CI run 41732300171](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41732300171) passed **21/21 tests on Python 3.11 and 21/21 on Python 3.12** with no SUMO installation. Identity-breaking T07, no-future-data T14 and oracle-import static audit passed on both. Only paths under `research/externality_estimator/`, its own no-SUMO workflow and this report are proposed; the frozen historical Experiment 007 workflow is not triggered. Future implementation changes still require source and physical-meaning review.
2. Independently review the static SUMO junction legality/conflict approximation, fractional 1-second scheduling, source-injection budget and model resource cap against the frozen Stage 1B contract. Any unresolved essential assumption is a **pre-development blocker**; fixture pass alone is not scientific development qualification.
3. Only with **separate explicit approval** proceed to generate/execute the frozen DEV_BUILD 5101–5106 and DEV_CHECK 5111–5114 cases (maximum 60 SUMO arms), with predictions saved before observed labels and calibration using DEV_BUILD only.
4. After a development-only verdict, write/freeze a **new independent validation protocol on genuinely unseen seeds**. **Test B** comparing cooperative vs equally informed independent routing with individual and nonparticipant fairness remains conditional on that validation. Do not reuse original failed Experiment 007 Test A seeds or historical Test B cohorts as development labels.

**Scientific disposition:** Stage 1C source and no-SUMO unit fixtures implemented; **physical dynamics and forecast skill unvalidated.** The 8/20 Test A failure and all prior scientific reports are unchanged. No automatic policy execution, external social posting, or human-road superiority claim.
