# Post-T1 — dual independent simulator source-feasibility synthesis and scientific decision (DRAFT FOR REVIEW)

**Date:** 2026-11-09 Pacific  
**Status:** **REVIEW DRAFT — no final source-qualification approval, no merge, no traffic execution**  
**Governing authorization:** [PR #114 plan](POST_T1_DUAL_INDEPENDENT_SIMULATOR_FEASIBILITY_PLAN_2026-11-08.md), merged at project commit [`5d447ff94d057e078dfbbcaf5ea94252684b9f3f`](https://github.com/yonnastgetahun/cooperative_traffic_research/commit/5d447ff94d057e078dfbbcaf5ea94252684b9f3f). Read-only examination of primary archival reports and pinned upstream source; no new source-code implementation, model conversion, static generated dataset, traffic simulator step, reserved cohort or social publication.

**Independent ledgers:** [UXsim](POST_T1_UXSIM_SOURCE_FEASIBILITY_LEDGER_2026-11-09.md) AND [CityFlow](POST_T1_CITYFLOW_SOURCE_FEASIBILITY_LEDGER_2026-11-09.md). Neither is a fallback; both received all five requirement assessments.

## P0. Recovered scientific question, decisions and immutable reference

**Question:** Can voluntary coordination improve *all 1,000 drivers' preferred-departure-to-arrival cost* relative to equally informed independent decisions, without unacceptable individual or nonparticipant harm? Unlike giving drivers shared traffic information or simply moving waiting outside the network, cooperation must add incremental value on the same inputs and fairness terms.

### Research progression — actual evidence, not causal storytelling

| Stage | Verified contribution | Scientific limit / decision |
|---|---|---|
| Experiment 001 and initial routing development | In the original synthetic 10×10 grid, independent nominal-free-flow routing yielded shorter mean trips than both original cooperative prototypes under high/moderate/lower congestion. | This does not compare against today's independently traffic-aware navigation products. [Research progress report](RESEARCH_PROGRESS_REPORT_2026-10-24.md). |
| Experiment 002 / M3 | Time-aware road-entry forecasts beat free-flow baselines across the held-out development-era comparison, but large systematic bias persisted. | Forecast accuracy is not a causal routing benefit. [M3 scientific evidence via README](../README.md). |
| Experiment 003 | Cumulative timing calibration reduced independent confirmatory chosen-route prediction error ~34.2%, 46.3%, 51.3% across the three regimes. | No conclusion about network cost or route-changing counterfactuals. [Experiment 004 contextual report](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md). |
| Experiment 004 | Calibrated cooperative policy D was **18.5282s slower** than same adapter C per trip at high congestion (95% seed CI for C−D −22.5866 to −14.4698s); 120/120 scenario arms and complete trips. | **NO-GO specific D**; better forecasts produced worse tested routing outcomes. [Final report](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md). |
| Experiment 005 | Correcting the stateful routing clock alignment improved policy E by **20.13s** vs flawed D at high congestion. | An engineering/model-time correction, not evidence of E beating independent A. [Results](EXPERIMENT_005_CLOCK_ALIGNMENT_RESULTS.md). |
| Experiment 006 | High-congestion A−E mean **+0.2429s**, 95% seed CI **−1.9120 to +2.3978s**; **27.98%** had >30s additional delay, violating the 10% severe-harm gate. | Primary network-efficiency result **INCONCLUSIVE**; joint efficiency/fairness **NOT MET**. A used nominal free-flow, not a modern traffic-aware baseline. [Final report](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md). |
| Experiment 007 Test A | Frozen marginal-externality predictor achieved **8/20 = 40%** correct signs vs a 60% gate. | **NO-GO** for the particular estimator; policy Test B **not executed**. [Final report](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md). |
| E1-v2, F0–F5 and C1 | E1-v2 development qualification failed; archive audit showed nonadditive route-bundle effects; C1 E3 priority manipulation changed route-swap externalities by **−7,578** and **−19,980 network-s** in two inspected cases. | C1 worsened absolute network costs in both routing assignments; junction effect modification is **not** a validated cooperative policy or unique mediator. [C1 report](POST_EXP007_C1_E3_CONTROLLED_FINAL_SCIENTIFIC_REPORT_2026-11-05.md). |
| T1 original B/C | Original 10-second proxy predicted **−50.626 network-s** for C−B but original SUMO comparison observed **+618 network-s**; 12 requested +10s shifts among 1,000 drivers. | **380 same IDs changed speed factors** across B/C, so this is a **confounded descriptive contrast**, not timing-only causal evidence. [Feasibility](POST_C1_T1_TIMING_FEASIBILITY_FINAL_DEVELOPMENT_REPORT_2026-11-06.md); [confound audit](POST_T1_EXPERIMENTAL_CONFOUND_ARCHIVE_DIAGNOSTIC_AND_STOP_2026-11-06.md). |
| T1 identity-locked B*/C* | Same 1,000 IDs, original routes, original 12 shifts and recorded speed factors paired by ID. C*−B* **+2,131** all-driver network-s (120 requested wait +8 insertion +2,003 in-network). The 988 unchanged-departure drivers incurred **+2,177**; 500 nonparticipants **+294**. | **DEVELOPMENT-ONLY NO-GO** for current proxy/policy. SUMO lane-associated shared PRNG/event-order coupling remains plausible; its contribution is not measurable from archived runs. [Controlled report](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md); [source audit](POST_T1_SUMO_RNG_EVENT_ORDER_AND_PHYSICAL_PROPAGATION_SOURCE_AUDIT_FINAL_REPORT_2026-11-07.md). |

**GO/NO-GO integrity:** Experiment 005 correction versus D is not a GO versus independent A; Experiment 006 joint efficacy/fairness is not met; Experiment 007 Test B and E1-v2 reserved independent validation were not run; current T1 proxy remains development NO-GO; no independently reproduced cooperative gain is established.

### Archive provenance and static input contract

- **Original T1** development run: [GitHub Actions 42183640504](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504), [artifact 13486493479](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504/artifacts/13486493479), ZIP SHA-256 `b524729226c44b722f2c8c157f017dee98181dcd8dfb97c2ec14401229184fae`, original research source commit `bbc0fadefcaa11d499e394d648526358d97358ee`.
- Original B route-input `sumo_B/routes.rou.xml` SHA-256 `3d2984a4010445e8abe03d5855e796a3291b95ca2b0de763f05c0869a1f8a01e`; C route-input SHA-256 `707b6c215b0792d4cf4d99c15e1a34670595e51995cd6814bc8ea8a7aa2d1718`. [Original confound audit](POST_T1_EXPERIMENTAL_CONFOUND_ARCHIVE_DIAGNOSTIC_AND_STOP_2026-11-06.md).
- **B*/C*** permanent archive: [release `t1-idlocked-dev2101-2026-11-07`](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/t1-idlocked-dev2101-2026-11-07), `t1-idlocked-dev2101-complete-evidence.tar.gz`, 7,895,065 bytes, SHA-256 `c3541593131930101ba7237bf2460765c385de5dafa5eab07a986ef1178a396a` per [controlled report](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md). The release contains member/asset SHA-256 manifests and a canonical original-ID manifest. It was published after a preservation-only job; no rerun was required.
- SUMO reference: pinned 1.28.0 image `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`. The [source audit](POST_T1_SUMO_RNG_EVENT_ORDER_AND_PHYSICAL_PROPAGATION_SOURCE_AUDIT_FINAL_REPORT_2026-11-07.md) links SUMO v1_28_0 upstream and separately states that exact container-source build commit identity was not proved.
- **P0 limitation:** This draft checked GitHub published scientific reports, release tag and asset metadata; it has **not re-opened and member-by-member reconciled the 7.9 MB archived tar**, its canonical 1,000-row preferred-departure/eligibility manifest or entire original topology. Therefore no 1,000-row external-edge/clock crosswalk is claimed complete. The archive is a frozen input source to inventory read-only later, **never** a source of target arrival clocks for UXsim/CityFlow.
- Reserved E1-v2 6201–6212 and conditional Test B 6301–6312 cohorts remain unopened; new seeds are not part of this phase.

**Clock parity requirement:** for every original ID and arm P, preserve `p_i` original preferred, `s_i,P` requested, `d_i,P` actual road admission, `a_i,P` completed arrival, including fraction precision. Reconcile `a_i−p_i = (s_i−p_i)+(d_i−s_i)+(a_i−d_i)`. Require all 1,000 completed rows; do not substitute in-network mean or exclude missing journeys. Preserve 12 shifted, 988 unchanged, 500 eligible/500 nonparticipant group contrasts and severe-harm counts.

## P1-U and P1-C source assessment — completed as separate ledgers, NOT source-qualified for execution

- **UXsim:** [pinned Python source `b7e27388757a0e4c64f303c9606a3d5a5ef40388`](https://github.com/toruseo/UXsim/tree/b7e27388757a0e4c64f303c9606a3d5a5ef40388). Explicit names/routes are supported; defaults represent five-vehicle platoons with five-second steps. Subsecond preservation would require reparameterizing `DELTAN × REACTION_TIME`, with physical consequences. Node capacity, signal groups and merge priority exist; microscopic priority-turn equivalence is not shown. Per-agent state/lifecycle exists but exact 1,000-clock accounting is unqualified.
- **CityFlow:** [pinned source `81ee0f47659ca66177a71f81676691c58ee89184`](https://github.com/cityflow-project/CityFlow/tree/81ee0f47659ca66177a71f81676691c58ee89184). Standard flow loader uses integer times and generated IDs; official SUMO converter truncates fractions. Its router **shortest-path-expands anchor road lists**, a separate fixed-route fidelity gap. Road/lane-link junction mechanisms are real but not SUMO-equivalent by assumption. Finished vehicles are removed from the live map; aggregate travel time is not a per-original-driver cost ledger. A Python `push_vehicle` alternate is visible but unqualified, and it also generates engine IDs.

## P2. Same-contract, side-by-side static comparison

**Classifications apply to the specified T1 frozen contract, not overall simulator quality.** `SOURCE-SUPPORTED` refers only to an inspected *component*; a row can still be unqualified for the full original experiment.

| Five nonnegotiable axes | SUMO original reference | UXsim Python, pinned | CityFlow, pinned |
|---|---|---|---|
| **1. Exactly 1,000 original IDs and group labels** | Historical B*/C* static-control and output gates passed, per original report. | Named agents and duplicate rejection **SOURCE-SUPPORTED**; default `DELTAN=5` **NOT original individual units**. `DELTAN=1` mapping **UNRESOLVED** for full data. | Generated `flow_i_j` or `manually_pushed_j` IDs; deterministic original-ID crosswalk **UNRESOLVED**. |
| **2. Original fractional preferred/requested clocks** | Historical T1 B*/C* fractional inputs preserved under its native XML and control checks. | Default clock lattice **BLOCKED** for fractions; fractional reaction-time reparameterization **UNRESOLVED** and changes model semantics. | Standard JSON flow loader integer `startTime/endTime` **BLOCKED**; possible timestamped manual injection **UNRESOLVED**. |
| **3. Every original full fixed external-edge route** | Original B*/C* frozen routes identity-checked. | `enforce_route` **SOURCE-SUPPORTED**; 1,000 edge→link legality mapping **UNRESOLVED**. | Explicit roads **SOURCE-SUPPORTED**, but shortest-path expansion between anchors makes exact per-driver route **UNRESOLVED**. |
| **4. Junction conflicts, queueing, merges, spillback** | Microscopic priority and internal-lane logic source-audited; stochastic coupling still unresolved. | Node flows/signals/merges and finite link storage exist; original right-of-way/turn geometry **UNRESOLVED**; some microscopic conflicts may be **NOT REPRESENTATIONALLY COMPARABLE**. | RoadLinks/LaneLinks/signals and crossing conflicts exist; physical priority/geometry mapping **UNRESOLVED**. |
| **5. Per-ID completed original-preference-to-arrival accounting** | Archived B*/C* `p_i` + requested/admission/arrival decomposition reconciled for all 1,000. | Per-name living/end/abort and link-entry logs **SOURCE-SUPPORTED**; exact lattice/finish-clock and 1,000 rows **UNRESOLVED**. | Standard live API/aggregate **BLOCKED** for exact per-ID finish accounting; alternative native event export **UNRESOLVED**, requires future authorization if it entails implementation. |

### Junction- and representation-equivalence gap register (not quietly normalized away)

| Property | Original SUMO | UXsim prospective gap | CityFlow prospective gap |
|---|---|---|---|
| Traffic unit | Microscopic vehicle | Default platoon of 5; one-driver parameterization changes model | Distinct individual vehicle but flow-generated identity |
| Time | Original subsecond input, pinned SUMO step/log conventions | Quantized `int(p_i/DELTAT)`, reaction-time coupled | Integer standard flow start/end; configurable engine step on alternate path |
| External road list | Pinned ordered SUMO edges | Named Link crosswalk and whole-route constraints not mapped | Road anchors may be connected by Dijkstra, not a verbatim sequence |
| Right-of-way/conflicting turns | Priority junctions, internal connections and SUMO source mechanics | Aggregate node/merge/signal eligibility; movement-specific conflict equivalence absent | Explicit laneLinks/cross-conflict logic; per-junction priority match unproved |
| Origin waiting / admission | SUMO requested shift + insertion delay separated | Home→node wait→first Link; tick conventions need audit | Flow creation→road waiting buffer→actual insertion not yet fully timestamped |
| Finish event | Per-ID native tripinfo archived | Per-name `arrival_time` / `traveled_route` with abort flag, discretized | Native C++ terminal action, but exposed Python API lacks persistent per-ID completed ledger |
| Stochastic coupling | Lane-shared RNG source hypothesis from original audit | Shared `W.rng` in vehicle and merge decisions; no per-ID coupling proof | Engine RNG used in priority/lane decisions; original-ID pairing unproved |

**Meaning of independent:** Two independent software architectures might increase robustness of physical interpretations, *if* the hypotheses and all input/output invariants can be represented. They do not need to reproduce SUMO's trip times numerically. They cannot be called two independent scientific validators because their APIs merely accept superficially similar roads or times.

## P3. Proposed decision for user review — **EVIDENCE INSUFFICIENT; no T1 cross-framework GO**

Both ledgers have been produced, with source citations for each of the five requirements, but **neither model qualifies yet for faithful reproduction of the original 1,000-driver fixed-route T1 comparison**. The source-backed standard-path blockers are real: UXsim's default platoon/time quantization, CityFlow's integer JSON schedule parsing and lack of exposed persistent per-driver finished arrival timestamps. CityFlow also has an anchor-route expansion risk. Alternative configurations and APIs are only hypotheses for future design, and junction equivalence remains unresolved. This is **not** a claim the underlying simulator is defective, that neither could be adapted, or that cooperation fails generally.

**Proposed classification:** The plan's **P3 option 4, EVIDENCE INSUFFICIENT**, with explicit **BLOCKED** status for the named *standard input/output pathways*. Not option 1 (both qualified), not an asymmetric one-simulator selection, and not option 3 (permanently irreconcilable) without proving alternatives impossible.

### Highest-information remaining source/static questions (not an experiment)

1. **P0 completion:** read-only enumerate canonical frozen input, identity and complete external-edge/clock manifests from the permanent evidence archive and verify SHA-256; no new scenario generation. This establishes the exact fraction lattice and complete used edge/turn set.
2. **UXsim:** can a one-driver-per-agent, fraction-capable parameterization preserve the *question* without introducing unacceptable reaction-time/flow-model distortion? If not, record a representational stop.
3. **CityFlow:** do `push_vehicle` plus a source-supported exact-tick scheduling convention supply 1:1 immutable IDs and a correct requested/admission/finish ledger *without code modifications*? Can the full original route sequence survive anchor-path expansion? If not, record a standard-interface stop.
4. **Both:** static priority-junction/connection inventories and explicit omissions, never a geometry-only substitution; identify whether a narrower *new* scientific question would be needed rather than modifying frozen T1.
5. **Cross-model stochastic integrity:** specify what constitutes controlled matched exogenous attributes across B*/C* in each framework, without presuming same seed means same draws or turning off randomness for convenience.

**Stopping rules:** Stop source qualification if any required original time is necessarily rounded, original IDs/labels cannot be recovered one-to-one, road sequence changes unapproved, priority/conflict mechanisms cannot represent the intended hypothesis, or no exact 1,000-row completed-arrival path exists. Publish the blocker, not a favorable simulation result.

### Next authorization checkpoints

- **Now:** user reviews this **draft classification** and the two source ledgers; corrections are handled on the review branch. **Do not merge** before approval.
- **Potential separate future milestone:** user approves a prospective static-fidelity verification design and, only if justified, tightly bounded adapter/clock/output instrumentation. This draft **does not authorize** any such changes.
- **Potential eventual independent simulation:** distinct prospective scientific protocol(s), exact frozen inputs, fair B*/C* control per simulator, seed/randomness strategies, completeness/fairness gates, fixed statistical unit and budget. **Requires an explicit new user authorization.**
- No SUMO, UXsim, CityFlow run; no reserved seeds, altered original reports, recalibration or social publishing occurred in this source review.

**Scientific conclusion limited to feasibility:** As of this inspected source revision, there is insufficient evidence to label **either** independent framework a faithful original-T1 validator. Resolving or explicitly ruling out their representation gaps is more informative than immediately obtaining a third simulated travel-time number.
