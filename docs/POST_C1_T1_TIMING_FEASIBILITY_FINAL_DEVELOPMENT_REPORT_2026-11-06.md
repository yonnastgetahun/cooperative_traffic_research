# T1 cooperative timing — two-question feasibility investigation

**Date:** November 6, 2026 UTC (continuation of November 5 Pacific research milestone)  
**Verdict:** **T1 CURRENT 10-SECOND FORECAST/POLICY DEVELOPMENT NO-GO FOR CONFIRMATORY EXECUTION**. The broader cooperative-timing hypothesis is **UNTESTED**, not rejected.  
**Scope:** Read-only review of prior sources; new narrow T1 code and unit tests; exactly **one previously inspected development demand seed 2101**, with three final A/B/C SUMO arms. No fresh confirmatory seeds, no reserved E1-v2 validation/Test B, no E1-v3, and no social-media publication.

## 1. WHY we conducted this study

The governing research question remains whether voluntary coordinated decisions yield network-wide benefits beyond equally informed independent decisions, without unacceptable individual or nonparticipant harms. Initial cooperative routing failed to show a joint efficiency/fairness advantage; externality estimators failed their frozen qualification gates; C1 proved only case-specific physical priority-rule effect modification. We therefore approved T1 to test timing coordination *as a separate mechanism*, not to keep tuning a failed route estimator.

Before comparing a coordinated policy C with an independently optimized policy B, two essential feasibility questions had to be addressed:

1. **Can independent timing reach a credible stable decision state rather than be artificially weakened by an arbitrary finite-pass cutoff?**
2. **Can a shared forecast distinguish 10-second timing changes in traffic effects, beyond the trivial cost of the departure delay itself—and does that distinction correspond to meaningful simulated outcomes?**

## 2. HOW we investigated them

The same fixed, traffic-aware independently assigned routes from the existing Experiment 007 I route constructor were used across all three arms; 1,000 pre-existing seed-2101 development drivers with preferred departures over 200 seconds; 500 deterministic eligible identities; options 0, +10, +20, +30 seconds, with 5-second maximum *predicted* personal concession. Full announced-demand information was shared by B and C and no post-SUMO outcomes entered their decisions.

A: no shifts. B: individual predicted preferred-departure-to-arrival cost minimization by sequential best response. C: sequential minimization of predicted **all-driver** cost with the same choice menu and nominal assumed acceptance limits. Both used the same **10-second edge-time-bin assigned-demand** proxy derived from nominal route edge timing; this is not a physically validated travel-time predictor.

For B, a fixed-route choice selects a deterministic set of edge-bin resources with affine congestion count costs. The resulting finite atomic congestion game has an **exact Rosenthal potential**, verified by unit test: a driver's unilateral predicted own-cost change equals the potential change. With strict improvement steps, cycles cannot occur. The implementation audits the maximum remaining own-cost improvement rather than merely asserting that 20 passes must be sufficient.

For sensitivity, we separately compared **predicted in-network traffic cost** across timing alternatives *excluding* the mandatory 0/10/20/30-second departure delay. Four predeclared 10-second bin phases (0, 2.5, 5, 7.5 s) probed boundary dependence. We then ran one development-only actual SUMO A/B/C comparison, including **requested shift + SUMO insertion delay + actual in-network duration** for each of the original drivers. This is a feasibility diagnostic, not a confirmatory effect estimate.

## 3. Verified findings

### Question 1 — independent timing stability

**Resolved at the model/algorithm level: PASS.** For seed 2101, B made **zero timing changes** and converged in **one complete pass with maximum residual unilateral predicted improvement 0.0 s**, across all four bin phases. Exact potential identity, forecast conservation and unchanged nonparticipant shifts passed unit/development checks.

This is a **trivial no-shift equilibrium** under the proposed model: none of 500 eligible drivers obtained a total predicted personal benefit large enough to offset the 10-second-or-more voluntary wait. It does *not* establish a strong independent-timing benchmark under a realistic traffic forecast or real users' scheduling objectives. No artificial reduction of B capability caused the B/C difference, but the shared forecast's physical credibility remains insufficient.

### Question 2 — does the 10-second forecast give a useful signal?

**Numerical sensitivity: PASS. Physical predictive usefulness: FAIL / NOT QUALIFIED.**

Across phases, **498–500 of 500 eligible drivers** had a predicted *in-network traffic cost* spread greater than 0.5 s (not counting the departure penalty). The mean predicted traffic spread was approximately **3.72–3.89 s**; **347–369 eligible drivers** had a shift that lowered predicted traffic cost by more than 0.5 s. Yet **zero** eligible drivers had a shift that lowered their *total* predicted personal cost by more than 0.5 s in any tested phase.

C selected **8–12 shifted drivers**, depending on bin phase, while B selected zero. This confirms that the proxy is capable of *numerically ranking* departure alternatives, but its policy decisions depend on the bin alignment and the model does not demonstrate true timing-counterfactual accuracy.

In the phase-zero frozen development A/B/C test, the policy C forecast **50.626 network-seconds lower cost** than B. But SUMO realized **618 network-seconds higher cost** for C. This sign reversal is the important negative result.

| Outcome, inspected dev seed 2101 | A unshifted | B independent | C cooperative |
|---|---:|---:|---:|
| All-driver preferred-departure-to-arrival cost (network-s) | 211,051 | 211,051 | **211,669** |
| Average preferred-departure-to-arrival cost (s/driver) | 211.051 | 211.051 | **211.669** |
| Requested voluntary delay (vehicle-s) | 0 | 0 | 120 |
| SUMO departure insertion delay (vehicle-s) | 840 | 840 | 849 |
| Actual in-network duration (vehicle-s) | 210,211 | 210,211 | 210,700 |
| Completed trips | 1,000 | 1,000 | 1,000 |

**Cost accounting:** relative to B, C added 120 s intentional predeparture waiting, 9 s insertion waiting and 489 s in-network duration, totaling **+618 network-s** or **+0.618 s/driver**. Faster movement on the road was **not** observed; neither was lower total journey cost.

**Exploratory matched harm (B→C):** 477 drivers benefited, 481 were harmed and 42 were unchanged; **205/1,000** had more than 30 s additional cost. Among 500 nonparticipants, **102** experienced more than 30 s additional cost; nonparticipants collectively incurred **+543 network-s**. Only **12 drivers** had their requested departure changed (each +10 s). The other 988 drivers accounted for **+614 network-s** of the aggregate difference. These are data from **one retrospectively eligible development case**, not an independent population fairness rate or an official frozen T1 policy gate. Structured SUMO collision, emergency-stop and emergency-braking counts were zero in the three arms; no real-road safety inference follows.

The small number of changed departures and extensive spillovers are consistent with sensitivity to altered timing, but the evidence does not identify the physical source of the differences. **The shared proxy did not rank this particular coordinated schedule correctly in the SUMO development comparison.** We cannot call it a qualified timing forecaster.

## 4. Integrity, reproducibility and failed-attempt recovery

- [Development PR #99](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/99) contains the new T1-only code, exact-potential and 10s-bin unit tests, and PR-only development workflow. No frozen E1/Experiment 007 files were changed.
- Initial development workflow [42183356993](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183356993) and subsequent [42183532863](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183532863) failed because shifted vehicle departure records were not sorted by their *new requested departures*. These failures were **invalid input-ordering attempts**, not evidence of scientific policy inferiority; their available artifacts/logs were retained. The diagnosis led to a source-only sort fix; no adjustment of scientific decision thresholds.
- **Successful** frozen-input development run: [GitHub Actions 42183640504](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504). Both offline tests and pinned-container SUMO job succeeded; original network/demand/routes were re-used, exactly three completed final development arms, all 1,000 unique matched trips in each.
- [Raw original development evidence ZIP](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504/artifacts/13486493479) (30-day Actions retention); SHA256 `b524729226c44b722f2c8c157f017dee98181dcd8dfb97c2ec14401229184fae`. Contains four-phase feasibility summary, source network/trips, complete original A/B/C route XML, SUMO tripinfo/statistics/collision outputs.
- [Permanent compact machine-readable numerical checkpoint](results/t1_dev2101_feasibility_compact_2026-11-06.json). All historical Experiment 007 Test A and E1-v2 development NO-GO decisions, and unopened 6201–6212 / 6301–6312 cohorts, remain unchanged.

## 5. Scientific interpretation, stopping decision and next direction

The two questions now have discriminating answers:

- **B convergence/feasibility:** yes **for this finite approximate game**, as independently demonstrated by the exact-potential property and the actual zero-regret 2101 baseline. But this says nothing about realism of the model's choice signal.
- **Forecast sensitivity:** yes at the *time-bin numerical* level, but **not qualified as a meaningful forecast of actual SUMO timing externalities**. Development-only empirical observations showed the wrong sign for the tested coordinated schedule, including broader nonparticipant harms.

**Therefore: DEVELOPMENT NO-GO for freezing or executing the present T1 10-second forecast + B/C optimizer on fresh seeds.** This is **not** a NO-GO for cooperative timing as a research hypothesis. The experiment did what feasibility science should: prevented advancing a mechanically working but scientifically unreliable decision signal.

**Recommendation:** Do not tune the occupancy-pressure coefficient, bin phase, maximum departure, or eligibility based on this one seed; do not open new T1 confirmation or old reserved seeds. The next intellectual decision should be whether a very small **physical, counterfactual departure-perturbation test on already-inspected development conditions** could justify a new forecast hypothesis, or whether to move to a mechanism such as direct bottleneck-entry reservation with an explicitly modeled independent comparator. Either would require a *new prospective design* and explicit separate authorization, not an automatic E1-v3-style calibration program.

**No code execution on main:** the committed T1 workflow runs only on PR events. Its merge does not launch new SUMO studies. No external communication approved or initiated.
