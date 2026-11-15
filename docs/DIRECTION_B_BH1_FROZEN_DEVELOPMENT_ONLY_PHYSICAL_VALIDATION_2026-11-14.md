# B-H1 frozen single-template development-only physical validation

**Date / scope:** November 14, 2026 Pacific. This is a **development feasibility pilot, not a confirmatory experiment**. The single configuration and stop/reporting rules below are committed **before** physical traffic execution. No T1/Experiment 007 reserved cohorts, historical-result revisions, or policy tuning for a favorable outcome.

**Authority and gating:** The user approved advancing B-H1 toward execution conditional on source/static qualification. [PR #122](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/122) passed the pinned [Stage-1 static workflow](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/43665983807). This qualifies representability of the candidate network, parity of four arm input files, a stable forecast-based independent policy, opt-out invariants, and source-backed measurement contracts **for a bounded development test only**. It does **not** prove real spillback, physical forecast fidelity, stochastic equivalence, or cooperative efficacy.

## 1. Exactly one prospective candidate (no parameter search)

Retain the unchanged input generators and decision rules in [integrated B-H1 v0.1](DIRECTION_B_BH1_INTEGRATED_PROSPECTIVE_PROTOCOL_V0_1_2026-11-14.md):

- 96 immutable original IDs: 48 main + 48 crossing; fixed preferred departures and routes; 12 eligible main drivers, six hypothetical willing-to-consider offers, six decliners; **84 ineligible drivers**. This is modeled acceptance, not human-behavior evidence.
- S allows main traffic at J to ignore junction keep-clear; N is the **same** geometry with keep-clear enabled at the one main crossing connection. K stays 30s red and 30s green; J→K pocket's nominal length is 40m.
- One identical forecast based on 3s K green-service slots and an approximate five-vehicle queue. I individually optimizes, V offers limited system-cost-improving changes. Same {0,+5,+10}s eligible timing menu, <=0.1s independent residual-regret threshold, +5s maximum predicted personal concession.
- Exactly **four cells** S–I, S–V, N–I, N–V. Every policy schedule is computed **before** physical execution from the source/static contract. No adaptive use of actual future outcomes.
- Fixed simulator: original pinned SUMO 1.28.0 image ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb; one **development-only seed 9101**, 1-second steps, single thread, teleports disabled, fixed end t=2400s. These are pre-result conditions, not independent replication.

## 2. Intended execution and measurements

After **automatically rerunning the Stage-1 static network/policy/accounting gate on the identical commit**, the conditional development workflow may invoke SUMO **for only these four arms**. Each arm must preserve:

- Source-compiled network and planned route XML (96 IDs), immutable preferred/requested clock manifest, and pinned simulator provenance;
- TripInfo: every original vehicle's actual depart, arrival and insertion delay. Sum every preferred-departure-to-arrival elapsed time, including predeparture and insertion waiting;
- FCD at each step with id/lane/pos/speed to detect stalled main vehicles on internal junction J plus cross vehicles waiting at its approach. **Co-occurrence does not establish that one vehicle caused the other's delay.**
- One pocket E2 lane-area detector to observe jam length, separate from real costs and junction conflict observations;
- Complete exit codes, no-teleport status, a bounded execution horizon, artifact preservation and explicit failure outputs.

A failed fixed scenario must be reported. Do not quietly change geometry, the signal cycle, demand, menu, participation rule or time horizon to force a result.

## 3. Four development-phase validity gates

| Gate | Required observation | Failure interpretation |
|---|---|---|
| **D1 — Physical blocking** | Under S, a main vehicle is stalled in J's internal crossing with source-backed cross-approach waiting and pocket queue observations | If absent, **MECHANISM NOT OBSERVED**; not a cooperative efficacy verdict |
| **D2 — Credible independent I** | Source/static forecast-based own-cost regret passes; I has identical available information and choice menus to V | A poor or unequal predictor prevents a claim of superiority over informed independent behavior |
| **D3 — Voluntariness** | Declining and ineligible driver requested times unchanged; modeled offers respect +5s predicted concession, identities and routes | A forced change invalidates the modeled opt-in premise |
| **D4 — Full outcomes and N control** | All 96 arrivals per cell, no unexplained teleports/censoring, compiled S/N parity except keep-clear, meaningful trip/FCD/queue traces | An incomplete or control-confounded record is NOT QUALIFIED |

Physical-mediator caution: stalled internal J traffic and cross-traffic waiting may be correlated because of normal priority behavior. Even when a co-occurrence is detected, the N contrast and detailed physical traces must be reviewed before attributing causal interference uniquely to spillback.

## 4. Development-only outcomes

Report all four summed costs; primary descriptive difference Δ_S=C(V,S)−C(I,S), corresponding Δ_N, Ψ=Δ_S−Δ_N, individual harms, nonparticipants, cross-traffic differences, insertion delays, and source-backed blocked-intersection samples.

**No confidence intervals, new policy GO, claim of real human willingness, or generalized coordination benefit** are warranted from one preinspected development template. A negative or null result remains valid. Output completeness or missing physical mechanism failures must be recorded as NOT QUALIFIED or MECHANISM NOT OBSERVED, **not repaired by another seed or tuned network**.

The separate proposed one-second practical improvement, severe-harm limits, sample size of 20 future independent scenarios, and confidence calculation are **not frozen confirmatory gates**. Reserved and confirmatory cohorts must remain unopened.

## 5. Stopping and provenance

After this single bounded development diagnostic, stop and issue a scientific decision: Is B-H1 physically instantiated and measurable, is the equally informed independent policy credible, and are the voluntary and nonparticipant outcomes complete? Any subsequent confirmatory protocol needs fresh explicit approval and frozen criteria.

Primary evidence: [governing B-H1 plan](DIRECTION_B_BH1_SPILLBACK_MINIMUM_DISTINGUISHING_TEST_PROSPECTIVE_PLAN_2026-11-14.md), [integrated protocol](DIRECTION_B_BH1_INTEGRATED_PROSPECTIVE_PROTOCOL_V0_1_2026-11-14.md), [Stage-1 contract](DIRECTION_B_BH1_STAGE1_STATIC_QUALIFICATION_2026-11-14.md), [SUMO v1_28_0 FCD](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Simulation/Output/FCDOutput.md), [TripInfo](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Simulation/Output/TripInfo.md), and [intersection blocking](https://github.com/eclipse-sumo/sumo/blob/v1_28_0/docs/web/docs/Simulation/Intersections.md#junction-blocking).
