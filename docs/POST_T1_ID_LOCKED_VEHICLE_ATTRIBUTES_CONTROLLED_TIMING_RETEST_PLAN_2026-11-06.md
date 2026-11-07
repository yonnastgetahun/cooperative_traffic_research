# Cooperative Traffic Research — T1 controlled timing-only development comparison with driver-identity-locked characteristics

**Date:** November 6, 2026 (Pacific)  
**Status:** **PROSPECTIVE SCIENTIFIC PLAN — DOCUMENTATION ONLY. NOT APPROVAL TO IMPLEMENT OR EXECUTE.**  
**Study class:** Bounded, previously inspected **development seed 2101**; new controlled comparison, **not** a correction or replacement of the historical T1 evidence.  
**Maximum conditional execution, requiring new explicit approval:** **Two SUMO arms, B\* and C\***, with an offline preflight first. No extra A arm or additional seeds.  
**Preserved decision:** Original T1 10-second proxy and cooperative policy **DEVELOPMENT NO-GO**; Experiment 007 Test A and E1-v2 NO-GO; unopened reserved validation/Test B cohorts.

## 1. WHY — restore a valid test of collective timing externalities

Our research asks: **Can voluntary collective traffic decisions outperform equally informed independent decisions while limiting unacceptable harm to participants and nonparticipants?**

The original T1 single development comparison had 1,000 matched drivers, 500 eligible drivers, fixed routes, B with no departure shifts, and C with exactly twelve +10-second shifts. The 10-second model predicted **C−B = −50.626 network-seconds**; SUMO originally reported **C−B = +618 network-seconds**, of which +614 occurred among 988 drivers with unchanged *requested* departures and +543 among 500 nonparticipants.

But the subsequently verified [original-archive control-integrity investigation](POST_T1_EXPERIMENTAL_CONFOUND_ARCHIVE_DIAGNOSTIC_AND_STOP_2026-11-06.md) established a previously unrecognized confound: **380 driver identities had different realized SUMO `speedFactor` values between original B and C**, including **368 of 988 unshifted drivers**. In contrast, all 1,000 `speedFactor` values matched in *route-file input order*, strongly supporting order-dependent assignment of randomized driver characteristics when C's requested departures were sorted. Thus the original +618-second difference is a correct **descriptive comparison of confounded runs**; it **does not isolate the causal effect** of the twelve timing changes.

The previous authorized [physical-observation plan](POST_T1_CONTROLLED_PHYSICAL_INTERACTION_OBSERVATION_PLAN_2026-11-06.md) was stopped before either replay executed; its [GitHub Actions run 42339346968](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42339346968) failed on a shell preflight issue, and the discovery of the speed-factor confound made an observational replay of those original inputs scientifically inappropriate.

**This prospective plan's central question:**

> **After assigning identical vehicle-specific speed factors and other input-defined characteristics to every matched driver in B\* and C\*, do the original twelve voluntary-style +10-second departure changes still produce measurable network-wide effects on the 988 unshifted drivers, including the 500 nonparticipants — and can early physical propagation be observed?**

A genuine future cooperative advantage would additionally have to outperform B\* on **all-driver preferred-departure-to-arrival cost** *and* satisfy prospectively defined individual fairness. This development diagnostic does not establish that advantage.

## 2. WHAT is fixed and what changes

Use the SHA-verified original [T1 Actions artifact 13486493479](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504/artifacts/13486493479), run [42183640504](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504), original ZIP SHA-256 `b524729226c44b722f2c8c157f017dee98181dcd8dfb97c2ec14401229184fae`, original source revision `bbc0fadefcaa11d499e394d648526358d97358ee`, and the pinned original SUMO 1.28.0 container digest `sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`. Preserve both original B/C artifacts and reports **unchanged**.

| Dimension | New independent B\* | New cooperative C\* | Requirement |
|---|---|---|---|
| Original demand and IDs | Original seed-2101 1,000 preferred departures | Same | Exact 1:1 ID/OD/preferred-time match |
| Fixed traffic-aware assigned routes | Original B route sequence per ID | Identical sequence per ID | No routing changes or replanning |
| Timing policy choice | Original B no-shift schedule | Original C twelve +10-second shifts | **No reoptimization**, no new acceptance, no parameter tuning |
| Driver eligibility | Original 500 eligible identities | Same 500 | 500 nonparticipants remain unshifted |
| Individual `speedFactor` | Explicit ID-indexed fixed value | **Same exact value for every same ID** | Supersedes order-dependent default draws |
| Type, vehicle attributes, junction rules, network, SUMO physics | One fixed, documented setting | Byte/parameter-identical | No inadvertent car-following, speed, lane, or priority changes |
| Simulator seed | 2101 | 2101 | Same pinned SUMO, but **same seed alone does not prove all other stochastic draws are paired** |
| Observations | Full original metrics, optionally passive movement traces | Same outputs | Preserve all 1,000 drivers and exceptions |

Call these **B\*** and **C\*** throughout. They are **new controlled-development arms**, not original B and C replays. The original +618 outcome is **not** a parity target for corrected outcomes; preserving it as historical evidence is mandatory.

### The minimal speed-factor control

1. Use the **original B tripinfo record for each driver ID** as the prespecified source of that driver's originally realized `speedFactor`. Do **not** select factors based on whether a driver benefited or was harmed under original C.
2. For each ID, add the **same explicit per-`<vehicle>` `speedFactor` attribute** to B\* and C\* input route files. Preserve original per-ID routes, preferred times, C departure shifts, passenger `vType`, and chronological SUMO input ordering.
3. SUMO documentation confirms that a `speedFactor` directly on a vehicle specifies its individual factor, whereas unspecified passenger vehicle factors are sampled from a distribution: [vehicle definitions and speed distributions](https://sumo.dlr.de/docs/Definition_of_Vehicles,_Vehicle_Types,_and_Routes.html), [randomness in SUMO](https://sumo.dlr.de/docs/Simulation/Randomness.html). **Check the actual pinned SUMO 1.28.0 syntax and output semantics before execution**, not just current online documentation.
4. The original `tripinfo.xml` factor has finite printed precision. Accordingly, the B-derived per-ID value is a **common fixed heterogeneous attribute**, not guaranteed to reconstruct the original higher-precision random draw or historical B vehicle trajectories. Both new arms must use the same recorded numeric value; if the stored values cannot be applied and verified reliably, stop. Do not silently replace all drivers with a uniform speed factor or fit the factors to original outcomes.

**Crucial unresolved methodological issue:** Matching explicit `speedFactor` values does **not** automatically lock all order-sensitive random events (e.g., stochastic car-following, tie-breaking or insertion). Preserve original defaults/physics and the common SUMO seed; document any residual simulator RNG divergence. If source inspection or the development evidence shows another material driver attribute varies by ID between arms, **stop or explicitly classify the result as partly stochastic**, not a fully isolated timing effect. Do not silently eliminate randomness by setting `sigma=0`, changing lane policies, changing step length, or adding extra replicates. Such changes need a distinct prospective protocol.

## 3. HOW — one bounded execution sequence (only after separate approval)

### R0. Archive-and-static-control preflight — **no SUMO simulation**

- Verify the original artifact digest, all original 1,000 IDs, original route sequences, 500 eligible / 500 nonparticipant assignments, preferred and requested departures, original B no-shift and original C twelve +10s shifts.
- Define an **immutable canonical vehicle-property manifest**, one record per ID, containing at least original vType, resolved per-ID `speedFactor`, fixed route, OD, original preferred/requested departure, eligibility, and a digest of all input-defined behavioral attributes. Preserve the original precision and record the new explicit values.
- Build B\*/C\* route files **from the original archived route assignments**, changing only the intended requested departure fields and supplying the common explicit per-vehicle characteristics; sort each output by its own requested departure time as required by SUMO. Require that removing the departure field and row ordering leaves the same 1,000 per-ID vehicle definitions in B\* and C\*.
- Verify `speedFactor` IDs, values, permitted ranges, input schema, file hashes, route continuity, XML consistency and unchanged SUMO options/vehicle-type definitions. Inspect whether stochastic attributes other than `speedFactor` could be newly reassigned by order; flag uncertainty before physics interpretation.
- Check output-only FCD / vehroute flags using the **pinned** binary's help/configuration before execution. No simulation or reserved-cohort access occurs in preflight.

**Hard stop:** Any missing archive member or unverifiable identity/route/attribute parity, unsupported factor semantics, unintended parameter change, nonparticipant shift, route-order error, or need to alter simulator dynamics. Record **CONTROL_INVALID**; do not run B\*/C\*.

### R1. Exactly two matched development SUMO arms (conditional)

- Execute **B\* once** and **C\* once**, under pinned SUMO 1.28.0 and seed 2101. No new seed, third arm, repeat for a favorable result, baseline rewrite, new policy, or automatic workflow retry.
- Collect `tripinfo`, collision, statistics and logs for each arm; obtain vehicle-level *passive* FCD at the existing simulator step and vehroute edge exit timestamps if verified output-only. Capture all vehicle IDs, including nonparticipants; preserve the actual command-line delta, source hashes and complete original/new inputs.
- Before any mechanism diagnosis, verify 1,000 completed unique IDs in each arm; every matched driver's reported `speedFactor` equals the **same prescribed value** in both arms at recorded output precision; every route and eligibility/requested departure remains fixed except the twelve +10s shifts; no missing duration, departure or arrival; explicitly audit insertions, collisions, teleports, emergency stops/braking and other simulator exceptions.
- Confirm that the actual effect accounting closes: `sum(arrival - original_preferred_departure) = sum(requested_shift) + sum(actual_depart - requested_departure) + sum(actual_in_network_duration)`. Do not double count in-network `waitingTime`. The C\*−B\* intentional predeparture component should remain **+120 vehicle-seconds**, while insertion and in-network changes are *unknown* until measured.
- If new output instrumentation materially alters dynamics or requires changing the original simulation physics, mark **INVALID_INSTRUMENTATION** and stop. If same-seed stochastic processes remain potentially scheduling/order-sensitive even after factor locking, preserve and prominently qualify that uncertainty; do **not** call the estimate a uniquely isolated physical causal effect.

**Hard stop:** Missing IDs, unmatched fixed attributes, unverified run identity, changed route/network physics, lost completion, unreliable output clocks, or unsupported trace provenance. Preserve negative/invalid evidence; do not rerun with tuned settings.

### R2. Analyze the controlled timing contrast (no additional simulation)

**Primary descriptive endpoint:** `ΔN = sum_i[(arrival_i,C\* - preferred_i) - (arrival_i,B\* - preferred_i)]` in **network-seconds**, summed across the original 1,000 drivers. Report mean `ΔN / 1000` as well. Compare only **B\* against C\*** for the primary new result; treat historical B/C as confounded context, not an interchangeable control.

**Compulsory components:** +120s scheduled waiting, change in insertion delay, change in in-network trip duration; actual stopped `waitingTime` and `timeLoss` separately, not added to the primary cost. Exact matched passenger-driver accounting, 100% expected completions, exceptions and possible omitted outcomes must be shown.

**Forecast contrast:** The unchanged frozen 10-second proxy's original selected-schedule contrast was **−50.626 network-seconds**. Show its sign against the new realized B\*/C\* contrast **only as a development diagnostic**, since original forecast never modeled heterogeneous speed factors or validated downstream physical arrival clocks. No new coefficients, bin sizes, optimization, or success thresholds.

**Fairness and externalities:** Independently report the 12 shifted / 988 unshifted, 500 eligible / 500 nonparticipants, helped/harmed/unchanged, median and p90/p95 individual change, >30s additional preferred-to-arrival harm, largest individual harm/benefit and route/OD exploratory clusters. Preserve harms among nonparticipants as a central outcome; the historical +614 unshifted and +543 nonparticipant values are **not** targets for recovery or tuning.

**Physical mechanism, only if trace validity passes:** Identify the earliest observed B\*/C\* differences in insertion, external road entry, internal junction occupancy, lane-level stopped/slow exposure, edge exit and downstream arrival. Specify FCD step resolution; preserve both improvements and harms; compare these observations to the *frozen* nominal-edge/10-second-bin forecast without retuning. “Earliest observed difference” is not uniquely causal mediation; changes may propagate via unobserved interactions or residual stochastic events.

**Scientific sampling limit:** One previously inspected seed pair is **one development comparison**, not 1,000 independent replicates. Do not construct an across-seed confidence interval from vehicles, FCD frames, edge records or the two arms. This study is incapable of establishing generality or confirmatory efficiency.

## 4. Competing interpretations and exact decision rules

| Outcome | Scientifically defensible conclusion | Required decision |
|---|---|---|
| Canonical per-ID factors or behavioral attributes cannot be matched, input integrity invalid, or simulator outputs fail accounting | New comparison is invalid or materially confounded | **STOP / CONTROL_INVALID**; preserve evidence, no substitute results |
| B\*/C\* per-ID speed factors match but remaining stochastic order/vehicle-interaction effects cannot be excluded | Better-controlled matched synthetic comparison; not a perfectly isolated physical intervention | Report **RESIDUAL STOCHASTIC UNCERTAINTY** and bound claims; no strong unique causal statement |
| New C\*−B\* outcome differs materially from historical +618 | Original confound mattered to interpretation, but difference does **not** numerically isolate speed-factor contribution because both conditions differ | Preserve historical result; report new effect **without** imputing a component to individual factor changes |
| New C\*−B\* outcome has the same sign as historical +618 | A negative result persists in this newly controlled setting | No retrospective validation of original +618 as purely timing-caused; current T1 policy still NO-GO |
| New C\*−B\* improves overall network cost but imposes excessive participant/nonparticipant delay | Potential aggregate improvement in this one scenario, **not acceptable cooperative success** | Keep developmental status and fairness warning; require independent prospective joint efficiency/fairness criteria |
| Controls hold, a coherent edge/junction response is observable, and an independently falsifiable feature is identifiable | **Candidate physical/externality hypothesis**, not a validated model | Propose **one** later prospectively defined hypothesis if justified; no automatic new simulations |
| Controls hold but observed propagation is ambiguous or no robust mechanism emerges | Mechanism remains unresolved | **STOP CURRENT T1 PROXY**; consider a different cooperative mechanism rather than further unfocused model tuning |

A change in sign, even a benefit, does **not** convert this development seed into confirmatory evidence, and neither confirmation of a traffic response nor good aggregate cost alone establishes voluntary human acceptance or real-world efficacy.

## 5. Execution limits, information parity and safeguards

- **No present execution authorization.** This document authorizes no edits to runnable research code, no GitHub Actions trigger, no SUMO runs, and no access to genuinely unseen seeds.
- Before a later authorized implementation, freeze and review the precise per-ID `speedFactor` extraction/serialization algorithm, input manifest, original B/C requested shifts, pinned SUMO command and decision rules. No choosing an alternative factor source after observing results.
- Preserve the same independent B and joint C *policy outputs* from the original development study. Both original policies received the same forecast and identical feasible timing menu. **Do not** reoptimize schedules or silently strengthen/weaken B; the current question tests a **fixed selected schedule's physical effects**, not whether a redesigned policy is optimal.
- Do not access Experiment 007 reserved **6201–6212** or E1-v2 reserved **6301–6312**, or any new confirmatory cohort. Do not revisit E1-v2, C1, calibration, an alternative simulator, junction priority, or arrival-target behavior as an implicit extension.
- Historic Experiment 007/E1-v2 scientific gates and the negative T1 10-second model/policy verdict remain fixed; no after-the-fact favorable decision thresholds.
- Do not equate an offered +10s shift with verified human consent. The 500 eligible / 500 nonparticipant labels are simulation assumptions.
- No public LinkedIn/X post without separate review and explicit approval.

## 6. What must be delivered **after** a separately authorized study

**One consolidated scientific report**, not a sequence of engineering milestones or repeated reports, containing: source-provenance and per-ID attributes manifest/digests; precise B\*/C\* input difference; pass/fail control and clock audits; actual cost bridge and all-driver harm distributions; earliest observable physical interaction chronology if measured; residual RNG/confound assessment; explicit **STOP / CONDITIONAL NEXT SCIENTIFIC HYPOTHESIS** decision and raw reproducible artifacts (with long-term preservation beyond ephemeral Actions retention).

A successful result means **we can distinguish what the timing-only comparison does and does not identify**, not that C\* can be made faster. If the control remains intrinsically incomplete, report **NO INFERABLE TIMING-ONLY EFFECT** and stop. Any future generalization or policy efficacy study needs a separately authorized prospective protocol, independent seeds and prespecified fairness gates.

## 7. Final scientific decision this plan is designed to inform

**Can a carefully controlled change in the timing of twelve voluntary-style departures produce measurable effects on other drivers in this synthetic network, after eliminating the identified speed-factor assignment confound?** If so, which observations, if any, would justify a single falsifiable next prediction hypothesis?

This would repair the *identification of the question* before returning to the much harder question of whether collective timing decisions can reliably make the network better than equally informed independent decisions.

**Current status:** **PLAN PUBLISHED ONLY; NO SIMULATIONS, MODEL CHANGES, OR EXTERNAL PUBLICATIONS.**
