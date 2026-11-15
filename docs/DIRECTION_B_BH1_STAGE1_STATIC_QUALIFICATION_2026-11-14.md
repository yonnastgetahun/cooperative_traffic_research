# B-H1 — Stage-1 source/static qualification of the integrated candidate

**Date:** November 14, 2026  
**Status:** DEVELOPMENT QUALIFICATION ARTIFACTS — SOURCE/STATIC ONLY; **NO PHYSICAL TRAFFIC STUDY OR EMPIRICAL RESULT**.  
**Authority:** Follow the [integrated four-gate protocol](DIRECTION_B_BH1_INTEGRATED_PROSPECTIVE_PROTOCOL_V0_1_2026-11-14.md) and [evidence register](DIRECTION_B_BH1_INTEGRATED_EVIDENCE_REGISTER_AND_READINESS_DECISION_2026-11-14.md). This branch provides concrete candidate fixture definitions and an independent-decision preflight. It does not supersede the original NOT READY traffic-execution decision.

## Source/static deliverables in this segment

- [Proposed one-scenario XML generator and static checks](../research/bh1_stage1/contract.py) uses only Python's standard library. It emits prospective S/N plain-network node, edge, connection, and red/green signal inputs for SUMO netconvert; **it does not call sumo, produce trips, train a predictor, inspect new traffic outcomes, or use fresh/reserved data**.
- [PR-only stage-1 CI](../.github/workflows/bh1-stage1-static.yml) compiles the network under the project's original pinned SUMO 1.28.0 container using **netconvert only** (a static network compiler), inspects the resulting network XML, and checks the deterministic decision/opt-out contract using a paper forecast. **No SUMO traffic simulation is called.**
- The same 96 original proposed IDs, 12 eligible main drivers, six willingness-proxy IDs and time menu 0,+5,+10 seconds are held fixed across the code and the protocol.
- The S/N physical toggle is limited to m_in → pocket at the priority junction J: keepClear=false in S versus keepClear=true in N. The second K signal is proposed as 30s red / 30s green; compilation must prove that the requested program and internal junction links are representable.
- The same analytic predict function is used for individual best responses and system-wide hypothetical voluntary offers. This is a **deliberately imperfect forecast** and not an evaluated physical queue model. It estimates K service in 3s green slots and potential crossing obstruction when a candidate five-vehicle storage limit is exceeded. Do not mistake predicted outcomes for traffic measurements.
- A failure of I's unilateral-regret tolerance <=0.1s after <=20 sweeps prevents any qualified primary comparison; a negative or failed policy check must be preserved without tuning the model based on favorable results.
- Static refusal/eligibility checks demonstrate that a hypothetical six-person willingness set can decline and that no other schedule is altered; **not human compliance**.

## Four-gate interpretation

| Gate | What a static success could demonstrate | What remains unqualified |
|---|---|---|
| G1 physical setting | A plain SUMO network compiles with requested roads, J internal crossing and K red/green; S/N keep-clear modes are distinguishable | Actual congestion spillback and physical J obstruction under the fixed prospective demand |
| G2 independent baseline | A common deterministic policy input set, and successful own-cost best-response stability against the shared approximate forecast | Baseline's meaningful relation to physical congestion; event-clock and stochastic adequacy |
| G3 voluntary timing | Same IDs and options, six modeled decliners unaffected, no other driver forced; zero-take-up returns I | Actual rational willingness, predictive personal cost fidelity, fairness under physical execution |
| G4 no-blocking control and accounting | Both network variants preserve external roads, and a fixed 96-ID input set exists | Physical S/N comparability beyond localized keep-clear, true crossing-obstruction event log, all actual insertion/arrival clocks, completeness |

**Important:** Even if CI successfully builds both networks and the paper decision contract, this is **not automatically a 4/4 executable scientific PASS**. The source/static results are necessary but not sufficient for a scientifically valid physical traffic comparison. A subsequent recorded gate decision must establish whether a strictly bounded development physical check is justified; no confirmatory cohorts or post-hoc effect-selection are permitted.

## Falsification and stopping

- If K's single-movement signal cannot be compiled with the proposed red/green program, or J does not contain distinct crossing streams/internal links, **stop and record G1 NOT READY**, rather than quietly changing geometry or signal settings.
- If the proposed equal-information I does not stabilize under its own rule, **stop and record G2 NOT READY**; do not change the iteration limit or tolerance simply to pass.
- If refusing drivers or noneligible IDs are shifted in V, **stop at G3**.
- If S/N are not compiled identically except for the intended crossing-entry behavior, **stop at G4**.
- If future physical traffic measures cannot include all 96 preferred-to-arrival costs, arrival and insertion times, crossing-obstruction observations, severe harms and nonparticipants, **do not begin the primary B-H1 comparison**.

**Research status:** Historical Experiment 004/006/007 and T1 decisions, PR #115's EVIDENCE INSUFFICIENT outcome, and Direction B's voluntary-participation constraints are unchanged. There is no claim of an observed traffic benefit or even an observed spillback incident in this document.
