# C1 controlled junction priority — case-level physical effect modification

## Why this matters to the research
The central project asks whether voluntary route coordination can improve all-driver traffic time against equally informed independent routing while protecting individuals. A credible collective optimizer first needs prospective predictions of route-choice externalities. This experiment tests one *physical effect modifier* of existing route choices, not cooperative policy performance or estimator skill.

**Status:** CASE_LEVEL_EFFECT_MODIFICATION_DESCRIPTIVE; original E1-v2 D1 DEVELOPMENT_NOT_QUALIFIED unchanged; independent validation and Test B NOT RUN.
**Design:** 2 pre-inspected seeds × original independent/probe2 planned routes × original/no-op or E3 priority-reversed rule. Exactly eight new SUMO arms, original 1,000 trips per arm.
**Source-pinned priority intervention:** D3E3->E3E4 gains priority over E4E3->E3E2 at E3. No other road/junction semantic changes in C1. Four no-op J0 replays met G2 individual <=0.02s and aggregate <=0.1 network-s tolerances before the first changed-physics J1 arm.

## Primary whole-network effect-modification outcome
C(s,R,J) = sum over all 1,000 (arrival - original scheduled departure). D(s,J) = C(s,probe2,J)-C(s,I,J). Psi(s) = D(s,J1)-D(s,J0).

| Seed | D(J0), original physics | D(J1), E3 modified | Psi network-s | Nonparticipants D(J0) → D(J1) | Local manipulation observed |
|---|---:|---:|---:|---:|---|
| 6112 | +3,219.0 | -4,359.0 | -7,578.0 | +2,731.0 → -1,947.0 | Yes, at recorded sampling |
| 6113 | -3,883.0 | -23,863.0 | -19,980.0 | -1,972.0 → -13,182.0 | Yes, at recorded sampling |

## Interpretation and original limitations
The controlled factor can identify how the local E3 priority rule affects the *marginal response to a route swap* on the selected synthetic network, assuming the source and no-op identity gates hold. It does not randomize queue waiting or prove that E3 initiated the original network-wide divergence; in the original passive replay, the earliest driver divergence preceded the prominent D3E3 hotspot.
The reported 10% of |D(6112,J0)| screen (about 322 network-seconds) is exploratory, not a population significance test, and does not substitute for development or independent validation. Inspect both directions, exceptions, speed/queue data, individual p90/p95 and nonparticipant effects. Waiting is not added twice to travel-time cost.
The exact candidate pair was selected from previously inspected seed-6112 I approach presence and frozen before all eight outcome-generating SUMO arms. Both seeds were previously inspected; no new independent predictor skill is claimed.
## Evidence
Original reference run 41966516110; original instrumented trajectory run 42113107379; C0/C1 preflight run 42125134835. Complete source manifest, frozen rule, original/no-op/changed network hashes, all eight tripinfo/FCD/vehroute/detector archives and SHA256 ledger accompany this report.

**Scientific conclusion:** A case-level effect-modifier result may motivate a new prospective modeling hypothesis but does not establish cooperative traffic superiority. The E1-v2 D1 NO-GO and unexecuted Test B remain unchanged.
