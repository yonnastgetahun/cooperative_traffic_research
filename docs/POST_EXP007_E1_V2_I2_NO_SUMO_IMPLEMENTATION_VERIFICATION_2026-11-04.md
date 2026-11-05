# Experiment 007 — E1-v2 I2 no-SUMO implementation and verification

**Research date:** November 4, 2026 (CI November 5 UTC).  
**Stage:** V2-I2: **IMPLEMENTATION-CORRECTNESS / DEVELOPMENT DESIGN READINESS**, not calibrated externality skill.  
**Scientific boundary:** No new SUMO simulations or training have been dispatched in this stage. No independent validation, policy Test B, or social publication. Original Experiment 007 Test A remains NO-GO and E1 Stage 1D remains DEVELOPMENT NOT QUALIFIED.

## Implementation footprint

New research package under \`research/externality_estimator_v2/\`:
- \`movement.py\` compiles only the canonical J0–J4-audited one-lane network, 1,320 priority movements, right-to-left foe and response bitsets, immutable typed movement/request indices and pinned original SUMO source reference; rejects other networks.
- \`scheduler.py\` implements READY-FOE-TOPOLOGICAL-GREEDY among *present, ready, one-lane FIFO heads*. It uses directional priority ordering, pairwise foe/receiving/source/via exclusions, source-turn service constraints, a deterministic rotation, and exclusive \`cont=1\` fallback. Cyclic or contradictory priority produces explicit abstention, not arbitrary passage.
- \`network_evolution.py\` retains original E1's one-second finite-storage propagation, source insertion, time and service-token rules, and complete per-driver mass/arrival accounting; replaces junction service selection alone.
- \`counterfactual.py\` reuses the original legal-candidate and t0 feature contract; computes baseline and alternative full-driver predictions, own effects, all-other externality, nonparticipant effects, and fresh full joint bundle predictions.
- \`tests/\` contains **24 mandatory V2-I1 gates** plus a **full original 1,000-driver grid/no-SUMO paired smoke**, with the 22 frozen E1 original regression tests also preserved.

Original \`research/externality_estimator/\` scientific code is **untouched**. The new module cannot call SUMO's runtime, read future tripinfo/FCD or access evaluation outputs to improve a prospective prediction.

## Verified engineering results

[Original GitHub Actions pull-request verification](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41962188016) on Python 3.11 and Python 3.12:

| Test group | Python 3.11 | Python 3.12 |
|---|---|---|
| V2-I1 V01–V24 required no-SUMO fixtures | PASS 24/24 | PASS 24/24 |
| Added V25 whole original network no-SUMO forecast | PASS 1/1 | PASS 1/1 |
| Original E1 regression suite | PASS 22/22 | PASS 22/22 |
| No-oracle-import and no-simulator source guard | PASS | PASS |
| Original 1,000-driver baseline+swap wall time | 1.706s | 2.893s |

**The full original-road-system smoke is an engineering test using a previously inspected seed-5101 route choice, not fresh E1-v2 scientific accuracy evidence.** Its only valid claim is that a complete, 1,000-driver paired forecast can be computed under the model's stated assumptions and runtime on that fixture. No new SUMO outcome labels were generated or read for that comparison.

Engineering tests establish source integrity, deterministic physical guards and the mathematical ability to represent distinct other-driver effects. They **do not establish** true junction throughput, calibrated false-benefit risk, externality magnitude/direction, real-world deployment feasibility or policy efficacy.

## Audit limitations and remaining decisions

- SUMO's static non-foe relation still does not guarantee physically simultaneous crossing. The conservative exclusive \`cont=1\` rule and one-head-per-lane approximation may remain incomplete.
- Versioned priority cycles trigger abstention, which may rise on new, unobserved traffic demands; record the complete abstention rate instead of hiding it.
- All real Stage 1D E1 development-check outcomes 5111–5114 and historic Experiment 007 seeds 4101–4105 have already been inspected. They cannot become fresh unseen E1-v2 results.
- An implementation unit-test gate is **not** an independent validation gate and never authorizes Test B directly.

## Next authorized scientific sequence — separately frozen execution contracts

With the user's broad conditional authorization, the next milestone is a **new E1-v2 development study protocol** that prospectively freezes new demand seeds, selected route swaps/bundles, primary MAE and false-benefit gates, simulator SHA, raw evidence preservation, information/forecast lock and maximum SUMO run footprint. Only then execute those development-only arms.

If development fails, preserve the negative result and stop. If it succeeds, independently freeze a separate **unseen** estimator-validation study, with truly distinct seeds/perturbations, no adaptive tuning and a decision gate. **Only after that independent pass** may a frozen cooperative-versus-equally-informed independent Test B run with full all-driver scheduled-to-arrival time and individual/nonparticipant fairness as joint criteria.

**Conclusion:** V2-I2 implementation is **engineering-ready for a separate scientifically frozen development study**. It has **NOT** yet demonstrated the prediction accuracy required to advance to independent validation.
