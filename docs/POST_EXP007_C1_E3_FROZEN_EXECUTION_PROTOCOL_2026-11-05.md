# Post-Experiment 007 C1 — frozen executable E3 priority effect-modification protocol

**Date:** November 5, 2026. **Authorization:** The user approved execution of the [C1 research plan](POST_EXP007_CONTROLLED_E3_JUNCTION_EFFECT_MODIFICATION_RESEARCH_PLAN_2026-11-05.md), merged as PR #94. This protocol is the executable specification for the same study.

## Why this matters to cooperative traffic research

A cooperative route recommendation can benefit the network only if the collective effects of altering routes can eventually be anticipated and fairly managed. The original marginal externality estimators failed; the E1-v2 four-arm observational replay showed substantial changes in other drivers' waiting, but it could not identify their physical cause. **C1 isolates one priority-junction rule as a controlled factor** and tests whether it modifies the *network effect of the same route swap*. It is a physical case study, **not** a test of a cooperative optimizer, proof of a unique queue mediator or independent predictor validation.

## Original C0/C1 evidence frozen before traffic intervention outcomes

- **Original source:** 695 source files verified with exact SHA256 ledger, original E1-v2 D1 run 41966516110, all 60 historic arms complete. The selected two source seeds 6112/6113 and their I/probe2 routes were previously inspected.
- **Pre-outcome selection run:** [C0/C1 feasibility run 42125134835](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42125134835) (no SUMO). In seed 6112/I the two E3 approach movements had 35 shared 5-second presence bins in the frozen 120–300s window; selected from six source-verifiable eligible conflicting pairs by the frozen ranking and lexicographic tie-break.
- **Original yielding turn:** D3E3 to E3E4, E3 request 14, internal lane :E3_14_0.
- **Original major turn:** E4E3 to E3E2, E3 request 1, internal lane :E3_1_0.
- **Exact supported netconvert change:** one plain-XML prohibition overriding the original pair priority: prohibitor D3E3->E3E4, prohibited E4E3->E3E2. Two reciprocal E3 response bits invert (request 1 bit 14, 0 to 1; request 14 bit 1, 1 to 0); the original major connection changes M to m. All other E3 request bits, foes, cont, connections and every road/other junction remain structurally identical.
- **No raw .net.xml manual edits:** SUMO warns that generated network elements are interdependent; use the supported, source-checked netconvert patch only.
- **Immutable execution input:** Four exact J0/J1 network member bytes from run **42125134835**, not regenerated in the simulator job. SUMO netconvert writes metadata that can change the raw ZIP/XML SHA across runs without changing traffic semantics, so preserve the precise original C1 network files. Exact source, J0/J1, patch SHA256 and candidate are locked in [C1_FROZEN_INTERVENTION_LOCK.json](../research/c1_e3/C1_FROZEN_INTERVENTION_LOCK.json). The C1 PR check independently re-generates the same *semantics* and validates the frozen member-byte SHA.
- **Pinned image:** ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb, SUMO 1.28.0.

## Factorial design and primary estimand

Two already inspected seeds, 6112 and 6113. Each preserves original independent assignment I and one preselected route swap probe2 (6112 target veh0142, 6113 target veh0038) under either J0 original-equivalent network or J1 precisely changed priority at E3. **At most eight SUMO arms; four mandatory J0 no-op reconstructions must qualify before any four J1 runs.** This is one scenario family selected after outcomes were seen, not a new independent replicate cohort.

C(s,R,J) = sum over all 1,000 matched vehicles of (actual arrival minus original scheduled departure). D(s,J) = C(s,probe2,J) minus C(s,I,J). Primary interaction: **Psi(s) = D(s,J1) minus D(s,J0)**. Old D(s,J0) must reproduce +3219 network-seconds for 6112 and -3883 for 6113. Seed 6112 exploratory materiality flag: absolute Psi >= 321.9 network-seconds AND an observable local E3 service/approach response. This is not a significance threshold or a model GO.

Mandatory secondary outcomes: changed driver/other 999/fixed 500 nonparticipants, insertion/duration/waiting without double-counting, p90/p95 individual changes, >30-second harms, safety, 1-second vehicle FCD, E3 movement samples, and five-second upstream/downstream waiting/flow. Show contrary evidence and both benefits and harms.

## Non-negotiable gates

**C0:** 695 original member SHAs, four original routes/tripinfos, pinned simulator and D1 NO-GO match. Failure stops before simulations.

**C1:** Stored fixed E3 movement pair, patch and the exact four original J0/J1 network bytes match frozen SHA ledger. Verified structural difference involves E3 only, with no changes to road geometry, other junctions, route legality or simulator behavior. Failure stops before simulations.

**C2:** Run four original-route J0 no-op controls first, in fixed sequence. All **4,000** per-driver original depart/arrival/duration/departDelay/waitingTime/timeLoss fields must match within **0.02 seconds** and each total within **0.1 network-second**. Original collision and safety summaries agree. **Any** mismatch stops before J1; no change of tolerances after outcomes.

**C3:** Only following completed C2 gate, run exactly four J1 changed-priority arms. Original demand/route files and random seed fixed; 1,000 completions per arm; no collisions, telemetry gaps or illegal routes. No field/dropout substitution or after-outcome modification.

**C4:** Independently recompute Psi per seed, route and physical state; verify original J0 full-network effects, sign, fairness strata and local service response. An inactive intervention or incoherent measurement remains a negative/inconclusive result. A nonzero Psi estimates *effect modification by the whole specified local network change*, not the causal contribution of stopped waiting at E3 alone.

## Execution and research integrity

Workflow is triggered **once by a single versioned execution-trigger file** after review/merge, with retry guard. Later source edits cannot accidentally start another eight-arm experiment. All original evidence, 8-arm attempts, raw FCD/tripinfo/vehroute/edge/lane files, exact input manifests, gate decisions and SHA256 checksums are preserved. In an integrity stop, no missing arms are silently replaced. A separate results PR will publish one consolidated negative/null/positive scientific report and README update.

**Invariants:** Original Experiment 007 Test A NO-GO; E1-v2 D1 DEVELOPMENT_NOT_QUALIFIED; independent estimator validation NOT_STARTED; cooperative Test B NOT_RUN. No retuning, fresh seeds, unsealing reserved 6201–6212 or 6301–6312, real-road efficacy claims, or social publishing.
