# Cooperative Traffic Research — Post-T1 archive-first scientific findings

**Date:** November 6, 2026  
**Scope:** One bounded retrospective diagnostic on previously inspected development seed 2101, without new SUMO execution, code changes, policy retuning, or reserved cohorts.  
**Decision:** The original **T1 current 10-second forecast/policy DEVELOPMENT NO-GO** remains unchanged. The general voluntary timing-coordination hypothesis remains untested.

## 1. Evidence recovery and method

This checkpoint follows the [approved post-T1 investigation plan](POST_T1_PREDICTED_VS_REALIZED_TIMING_BENEFIT_FAILURE_INVESTIGATION_PLAN_2026-11-06.md) (merged [PR #100](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/100), baseline main `d7b3309809ed3968816ee12439ffdad3caf593cd`). Authoritative inputs: [original development report](POST_C1_T1_TIMING_FEASIBILITY_FINAL_DEVELOPMENT_REPORT_2026-11-06.md), [compact evidence](results/t1_dev2101_feasibility_compact_2026-11-06.json), [Actions run 42183640504](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504), [original artifact 13486493479](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504/artifacts/13486493479), frozen [T1 source](../research/t1_timing/feasibility.py) and [underlying Experiment 007 route/SUMO runner](../experiments/experiment_007/run_v01.py). Original run head `bbc0fadefcaa11d499e394d648526358d97358ee`; reviewed `feasibility.py` blob SHA `596a47ee0a1983016189e2aa24103086c03fc2d9`.

**Original ZIP actually downloaded, inspected and SHA-256 verified.** 280,288 bytes; SHA256 `b524729226c44b722f2c8c157f017dee98181dcd8dfb97c2ec14401229184fae` matches GitHub's artifact digest. Its 24 entries contain original demand/network/trips, `feasibility_summary.json`, and A/B/C route XML, SUMO tripinfo, statistics, collisions, logs. **No original FCD, actual vehicle edge-entry event stream, junction service/queue-front measures, or edge detector time series are present.** The demand manifest's `fcd_step_seconds: 1` does *not* establish such a file exists.

**Independent archive-only reconstruction:** parse each original XML trip and route by vehicle ID; compute each realized preferred-to-arrival cost as `arrival - preferred_departure = requested_shift + departDelay + duration`. Reimplement the original 10s model with each archived external edge's `freeflow=lane_length/lane_speed`, `capacity=max(1,lane_length/7.5)`, nominal cumulative free-flow entry time, and resources `(edge,floor((time+phase)/10))`. Total model cost is `sum(shifts)+sum(freeflow*(q+q^2/capacity))`. Recompute B versus the **same originally selected phase-zero C schedule**; do not change chosen timing options, optimizer or coefficients. Predicted original numeric totals reproduce to better than `1e-7` network-s, and per-vehicle observed clocks close at the archived precision.

**Integrity:** 1,000 unique matched completed IDs in every A/B/C arm, same 1,000 fixed routes/network/seed; A and B route XML byte-identical and parsed tripinfo identical. C has 12 eligible IDs shifted exactly +10s, 988 unchanged; no nonparticipant requested shift. Successful C route XML is chronologically sorted after shifting. Each arm reports 1,000 inserted, 0 left running, 0 teleports, 0 structured collisions, emergency stops or emergency braking. Earlier [run 42183356993](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183356993) and [run 42183532863](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183532863) were invalid input-ordering attempts, not scientific negative evidence.

## 2. Predicted-versus-realized network-cost bridge

All quantities are **network-seconds** (sum across 1,000 vehicles); positive C−B is worse.

| Component | B | C | C−B |
|---|---:|---:|---:|
| Voluntary requested predeparture delay | 0 | 120 | **+120** |
| Actual SUMO insertion delay | 840 | 849 | **+9** |
| Actual in-network duration | 210,211 | 210,700 | **+489** |
| **Realized preferred-departure-to-arrival total** | **211,051** | **211,669** | **+618** |
| **Predicted 10s-model total** | 120,980.223182 | 120,929.596832 | **−50.626350** |

Independently reconstructed predicted C−B: `−50.6263498920`; original saved difference: `−50.6263498919`. Observed C−B = **+618**. **Contrast error = +668.626350 network-s**. Large absolute predicted versus measured levels are a separate calibration issue, not by themselves an explanation of the *contrast* reversal. This is a single development case, not a confidence interval.

### The crucial modeled-externality reversal

| Group | Predicted C−B | Actual C−B | Actual minus predicted |
|---|---:|---:|---:|
| **12 shifted drivers** | **+34.687** | **+4** | −30.687 |
| **988 unshifted drivers** | **−85.313** | **+614** | **+699.313** |
| All 500 eligible participants | −4.190 | +75 | +79.190 |
| All 500 nonparticipants | **−46.436** | **+543** | **+589.436** |
| **Network total** | **−50.626** | **+618** | **+668.626** |

The 12 shifters' own modeled *in-network* benefit is −85.313s, but their +120s voluntary waiting leaves **+34.687s modeled net personal cost**. The 988 unchanged-departure drivers were forecast to gain another **85.313s**. **The net cooperative benefit exists only because the model expects other drivers to benefit sufficiently. In the actual simulator, that externality reversed.** These are cohort allocations of the **whole B/C schedule**; they do not identify which of the 12 drivers caused any other driver's change.

## 3. What the time-bin diagnosis demonstrates

The 12 shifted routes contain 123 nominal edge traversals, spanning 106 distinct edges. In the phase-zero 10s forecast, the before/after schedule changes 244 edge-bin cost terms (122 positive, 122 negative) across 31 time bins:

- Gross modeled edge-bin improvements **−1,940.115s**.
- Gross modeled edge-bin deteriorations **+1,769.489s**.
- Net modeled in-network effect **−170.626s**; plus mandatory **+120s** voluntary waiting gives **−50.626s**.

The predicted advantage is a **small, sign-sensitive residual of much larger offsetting proxy contributions**, not a clearly localized physical improvement. The leading 20 modeled saving resources contribute −357.955s (18.45% of gross model savings). Exemplars such as G6G7/bin 19 and D4E4/bin 16 are **nominal modeled resources, not diagnosed physical junction bottlenecks**.

**New sensitivity check: same already selected C schedule at four originally predeclared bin phases; no reoptimization and absolutely no new SUMO runs.**

| Phase (seconds) | **Predicted C−B for same frozen C schedule** | Previously archived separately optimized phase C−B (different schedules, forecast-only) |
|---|---:|---:|
| 0 | **−50.626** | −50.626; 12 shifts |
| 2.5 | **+4.449** | −35.551; 8 shifts |
| 5 | **−4.190** | −39.827; 12 shifts |
| 7.5 | **−5.270** | −29.071; 8 shifts |

Merely shifting the **arbitrary bin origin**, with identical vehicles, requested departure shifts and nominal road geometry, removes nearly all of the forecast advantage or reverses its sign. This directly supports **H_BIN as numerical prediction fragility**. A +10s departure always changes nominal 10s-bin labels; the meaningful problem is that the estimated *benefit* depends so heavily on the arbitrary bin phase. It does **not** establish that binning caused the observed SUMO traffic harm.

**H_CLOCK structural vulnerability:** The [source](../research/t1_timing/feasibility.py) uses requested departure plus cumulative nominal free-flow road time, not measured congestion-dependent edge arrival or queue propagation. We can establish this mismatch in definitions, but cannot quantify its actual per-edge timing error from the archive, which lacks edge events.

## 4. Matched fairness and limited physical observations

| Cohort | n | C−B total | Helped | Harmed | Unchanged | Additional cost >30s |
|---|---:|---:|---:|---:|---:|---:|
| All drivers | 1,000 | **+618** | 477 | 481 | 42 | **205** |
| Shifted | 12 | +4 | 5 | 7 | 0 | 3 |
| Unshifted | 988 | **+614** | 472 | 474 | 42 | 202 |
| Eligible | 500 | +75 | 239 | 239 | 22 | **103** |
| Nonparticipants | 500 | **+543** | 238 | 242 | 20 | **102** |

Across all drivers: median paired cost change 0s, p90 +51s, p95 +69.05s, largest harm +220s, largest benefit −142s. These are descriptive one-seed results, **not** independent fairness rates or newly defined frozen gates. Neither policy can claim acceptable realized fairness on this evidence.

**New qualified physical clue:** Summed SUMO `waitingTime` **decreased by 1,079s** in C relative to B even though total actual in-network duration increased by 489s and reported `timeLoss` increased by 239.16s. Stopped waiting is **inside** trip duration; do not double-count it in the primary cost. Aggregate stopped-time reduction **contradicts a simplistic claim that the +489s entirely represents more total standing still**. It does not rule out localized queue formation, junction receiving constraints, changed moving speeds, or shifts of waiting exposure across vehicles.

Exploratory fixed-route overlap: among 988 unshifted drivers, 810 share at least one route edge with some shifted driver and total +789s; the remaining 178 with no shared route edge total −175s. Route overlap is *not* contemporaneous road interaction, the sets are not randomized, and this is not a causal route or junction diagnosis.

## 5. Competing explanations and remaining evidence gaps

| Hypothesis | Evidence for/against now | Still unanswerable from archive |
|---|---|---|
| **H_A: bad accounting or input** | Strongly weakened by exact matched identities, input chronology, algebra, zero censoring, matched A/B controls | Cannot logically exclude every latent implementation issue; no discrepancy found |
| **H_BIN: 10s bin aliasing** | **Strong evidence for forecast instability**, fixed schedule changes predicted sign under +2.5s bin phase | Cannot establish that phase artifacts directly generated +618 physical network-s |
| **H_CLOCK: nominal arrival order** | Source definitely ignores realized congestion and insertion in downstream nominal edge clocks | No actual vehicle-level edge-entry times to measure timing mismatch |
| **H_QUEUE: junction priority, queuing, spillback** | Physically possible; case-specific historical C1 supports sensitivity to junction rules. Net reported waitingTime *fell*, weakening a simple all-network stopped-delay account | No stepwise queue fronts, turn discharge, receiving capacity, or movement-level chronology |
| **H_INTERACTION / H_SENS** | Broad changes among drivers with no requested shift; same base seed, complete and exception-free policy arms | No causal share by individual changed schedule or earliest simulator event divergence |

**Archivally answerable and now completed:** original ZIP integrity, source provenance, model and observed cost reconciliation, exact group forecasts, modeled resource accounting, fixed-schedule phase sensitivity, matched driver/nonparticipant harms, total stopped-time contrast, original exception and completion checks.

**Not in archive:** actual per-edge entry/exit observations; earliest divergence of vehicle movements; per-junction approach and discharge; queue chronology; attribution of +618s to any specific bottleneck or single shifted driver. Tripinfo is terminal trip evidence, not an edge trajectory.

## 6. Scientific disposition and one narrowly bounded next action

**The existing archive is sufficient to stop the current 10s T1 forecast/policy.** The model's predicted gain was a fragile proxy-based externality, and the actually selected C schedule worsened realized cost and exposed severe participant/nonparticipant harms. **Do not retune bins, phase, pressures, willingness, optimizer, or advance confirmatory seeds.** The original DEVELOPMENT NO-GO is preserved. There is no independent evidence about voluntary human compliance or real-world road outcomes.

**The archive explains why the predicted advantage was untrustworthy, but does not explain the physical mechanism producing the exact +618s reversal.** Therefore the only potentially justified next step *if deciding whether to pursue timing coordination beyond the failed proxy* is a **separately authorized, passive two-arm B/C physical observation on the same previously inspected seed 2101**.

**One preregistered question:** Where/when does actual movement under the fixed C schedule first depart from B in the areas traversed by the shifted drivers, and how do subsequent observed edge entries, junction service, insertion order and waiting changes relate to the large unshifted-driver response?

**Required evidence:** at most **two** SUMO arms with unchanged original B/C schedules, source network, routes, seed, simulation physics, and participant IDs; additional exact edge-entry and lane/turn traces, approximately 1s vehicle movement/queue observations, insertion event order, and original matched tripinfo/fairness. Preserve comprehensive instrumentation, not just cherry-picked delayed vehicles.

**Stopping condition:** Before interpreting any new physical trace, reproduce original B/C route/departure identity, matched tripinfo costs and safety/completion at predeclared original tolerances. If passive instrumentation changes outcomes or replay fails parity, mark **INVALID_REPLAY** and stop. A valid replay can localize and sequence *observed* physical differences; it does **not by itself establish a unique causal mediator**, qualify a new forecast, or demonstrate cooperative policy efficacy. Any further causal intervention requires a distinct prospective decision.

**Connection to the founding research question:** Voluntary coordination is not beneficial merely because a shared forecast assigns an apparent network gain. For this T1 policy, the predicted benefit depended on favorable consequences for drivers whose decisions did not change; that was precisely the unreliable signal. Understanding whether such consequences can be physically observed and predicted without unacceptable harm is a prerequisite to a meaningful comparison with equally informed independent decision-making.
