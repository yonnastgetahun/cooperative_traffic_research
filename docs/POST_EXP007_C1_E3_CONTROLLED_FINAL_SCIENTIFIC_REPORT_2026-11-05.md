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

## Absolute network cost and fairness caution

The difference-in-differences Psi describes **effect modification**, not an absolute improvement from installing the E3 priority reversal. The modified-priority setting raised **all-driver scheduled-to-arrival time** under both fixed routing assignments in both selected seeds:

| Seed | J0 I cost | J1 I cost | J0 probe2 cost | J1 probe2 cost | Change in absolute network cost J1−J0, I / probe2 |
|---|---:|---:|---:|---:|---:|
| 6112 | 210,647 | 224,329 | 213,866 | 219,970 | **+13,682 / +6,104 network-s** |
| 6113 | 209,676 | 246,842 | 205,793 | 222,979 | **+37,166 / +17,186 network-s** |

Thus the negative Psi values reflect that a changed route is **relatively less harmful or more beneficial under an E3 rule that made these two network cases substantially slower overall**. Neither modified-E3 policy can be labeled a welfare-improving junction design on the basis of these figures. The result does not suggest deploying this priority reversal.

Nonparticipants' route-swap externality changed from **+2,731 to −1,947 network-s** in seed 6112, and **−1,972 to −13,182 network-s** in seed 6113. However, within their respective modified-priority settings, **76/500** (seed 6112) and **70/500** (seed 6113) nonparticipants still suffered more than 30 seconds of added travel time under probe2 versus independent I. For all drivers the comparable counts were **133/1,000** and **146/1,000**. These are descriptive harms in this selected experiment, not the unexecuted Test B fairness gates.

The pre-outcome selection and exact E3-only semantic patch are preserved under source lock **7a903174bf177a56789e531773b43d427dfd873f47a695ddcd4d9df0cceaebe2**. The priority change cannot uniquely identify E3 as the *original* bottleneck: the original vehicle trajectories diverged elsewhere earlier, and changing E3 may alter the downstream network sensitivity without being the initiating mechanism.

## Interpretation and original limitations
The controlled factor can identify how the local E3 priority rule affects the *marginal response to a route swap* on the selected synthetic network, assuming the source and no-op identity gates hold. It does not randomize queue waiting or prove that E3 initiated the original network-wide divergence; in the original passive replay, the earliest driver divergence preceded the prominent D3E3 hotspot.
The reported 10% of |D(6112,J0)| screen (about 322 network-seconds) is exploratory, not a population significance test, and does not substitute for development or independent validation. Inspect both directions, exceptions, speed/queue data, individual p90/p95 and nonparticipant effects. Waiting is not added twice to travel-time cost.
The exact candidate pair was selected from previously inspected seed-6112 I approach presence and frozen before all eight outcome-generating SUMO arms. Both seeds were previously inspected; no new independent predictor skill is claimed.
## Evidence
Original reference run 41966516110; original instrumented trajectory run 42113107379; C0/C1 preflight run 42125134835. Complete source manifest, frozen rule, original/no-op/changed network hashes, all eight tripinfo/FCD/vehroute/detector archives and SHA256 ledger accompany this report.

**Scientific conclusion:** A case-level effect-modifier result may motivate a new prospective modeling hypothesis but does not establish cooperative traffic superiority. The E1-v2 D1 NO-GO and unexecuted Test B remain unchanged.
