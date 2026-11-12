# Can We Make Traffic Flow Better by Cooperating?

Every day, drivers sit in traffic despite having powerful navigation apps. Those apps help us choose routes, but a good route for each driver isn't necessarily the best outcome for everyone.

**What if we could bring some of the collective intelligence of tomorrow's autonomous transportation networks to today's human-driven roads?**


## Current scientific direction — Direction B (November 12, 2026)

**Foundational hypothesis first:** Can voluntarily coordinated decisions create a fair, system-wide traffic advantage beyond equally informed and capable independent decisions? The recent simulator investigation is closed at [PR #115](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/115), **EVIDENCE INSUFFICIENT** for faithful original T1 cross-framework replication; that result does not disqualify the broader hypothesis or either simulator architecture.

**[Read the Direction B scientific checkpoint and alternative next milestones](docs/DIRECTION_B_FOUNDATIONAL_COOPERATION_SCIENTIFIC_CHECKPOINT_2026-11-12.md).** It distinguishes (1) collective opportunity, (2) voluntary stability and fairness, and (3) practical discovery; reviews the original negative/inconclusive experiments and recent literature; and compares several defensible *conceptual* next milestones rather than prematurely selecting an experiment. **No new traffic simulation, model implementation, reserved cohorts, or external publication is authorized by this document.**

## Next scientific planning milestone — BOTH UXsim AND CityFlow (November 8, 2026)

**Approved scientific direction: two independent simulator feasibility assessments, not one selected replacement.** Evaluate **[UXsim](https://github.com/toruseo/UXsim) AND [CityFlow](https://github.com/cityflow-project/CityFlow)** in parallel against the same immutable original T1 1,000-driver identities, preferred and requested departure schedules, fixed original edge routes, meaningful junction constraints and original-preference-to-arrival all-driver cost. **SUMO remains the documented reference, not the sole scientific authority.** Initial source inspection identifies candidate identity/route support in both, but flags UXsim's packet and time-step representation and CityFlow's integer flow start times plus generated vehicle IDs as material fidelity risks. No experimental equivalence or future policy benefit is claimed.

**Scope: planning and read-only source evidence only. NO new SUMO, UXsim or CityFlow runs, model implementations, new seeds, adapter executions, or social publication.** Existing T1 / Experiment 007 / E1-v2 NO-GO findings remain unchanged. The two tracks must both be completed and transparently classified, including blocked or unsupported requirements; one model may not silently replace the other. **[Read the dual-framework milestone plan](docs/POST_T1_DUAL_INDEPENDENT_SIMULATOR_FEASIBILITY_PLAN_2026-11-08.md).**


## Recent public research-pivot announcements (November 8 UTC)

The approved research-pivot update was **published and independently verified** on [LinkedIn as a five-page PDF document post](https://www.linkedin.com/feed/update/urn:li:ugcPost:7525113243074252800/) and [X as a single post with four research panels](https://x.com/yonnastgetahun/status/2119346244766031969), without Metricool. [Read the GitHub publication record](social/t1_pivot/PUBLICATION_RECORD_2026-11-08.md). The [reusable manual-only LinkedIn publisher](social/linkedin/README.md) remains available for future separately authorized announcements; this new UXsim + CityFlow planning milestone **does not authorize another social post**.

## Latest scientific finding — T1 shared lane RNG coupling (November 7, 2026 UTC)

**Read-only source-and-archive scientific investigation complete; no SUMO run.** The official SUMO **v1_28_0** source (matching the pinned simulator's reported version, though exact image-to-source build SHA remains unverified) shows that the default Krauss car-following model draws stochastic speed variations from **lane-associated PRNG streams, pooled across 64 indices** — not a separate immutable driver-ID stream. In the SHA-verified original T1 2,032-lane synthetic network, the **first shifted driver's lane C2D2_0** and the **first three unshifted vehicle differences at t=27–28** all map to the **same `lanes_20`** stream despite being on different road segments. This explains a credible *mechanism for distant random-state coupling*, though actual RNG draw logs were not preserved and the +2,131 network-second B*/C* difference cannot be causally partitioned. The [**consolidated source-and-archive final report**](docs/POST_T1_SUMO_RNG_EVENT_ORDER_AND_PHYSICAL_PROPAGATION_SOURCE_AUDIT_FINAL_REPORT_2026-11-07.md) contains exact source line links, all twelve original shifts, trace evidence and a **CONTROL_CANDIDATE_IDENTIFIED / STOP CURRENT T1 PROXY** decision. One separately authorized, prospectively controlled comparison with distinct lane RNG streams could discriminate a narrow hypothesis but would **not** independently qualify coordination or remove every stochastic confound. [Approved investigation plan](docs/POST_T1_SUMO_STOCHASTIC_EVENT_ORDER_VS_PHYSICAL_PROPAGATION_SOURCE_INSPECTION_PLAN_2026-11-07.md) · [Original B*/C* evidence release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/t1-idlocked-dev2101-2026-11-07). Original T1 **DEVELOPMENT NO-GO** unchanged; no additional simulations, predictor changes, reserved seeds, or external publication authorized.

## Previous completed investigation — T1 ID-locked timing comparison (November 7, 2026)

**Completed development-only B*/C* comparison; current T1 10-second proxy/policy DEVELOPMENT NO-GO unchanged.** The [approved identity-locked protocol](docs/POST_T1_ID_LOCKED_VEHICLE_ATTRIBUTES_CONTROLLED_TIMING_RETEST_PLAN_2026-11-06.md) was executed with **exactly two SUMO arms on previously inspected seed 2101**. Both arms preserved all 1,000 IDs, original fixed routes, original independent-versus-twelve-10s departure schedules, and **explicit matched per-driver speed factors**; both completed 1,000 trips and passed control/clock gates. C* increased **all-driver preferred-departure-to-arrival cost by 2,131 network-seconds** (120 planned wait +8 insertion +2,003 in-network); the 988 unshifted drivers experienced +2,177 total network-seconds and 500 nonparticipants +294, including 91 severe additional delays >30s. FCD first recorded changes to unshifted vehicles at t=27s, including a distant effect that makes remaining event-order stochasticity an unresolved confound. **This is not an isolated unique causal network effect, independently confirmed prediction skill, or proof of general cooperative harm.** The initial [execution](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42348701379) passed all research steps but its postprocessing GitHub CLI step failed; a separate **non-SUMO preservation run** succeeded. [**Read the consolidated final scientific report**](docs/POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md) · [**Permanent full evidence release with SHA-256 manifests**](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/t1-idlocked-dev2101-2026-11-07). **No more T1 simulations, estimator changes, reserved seeds, or external publication are authorized.**

## Previous scientific finding — T1 timing-only inference confounded (November 6, 2026)

**Archive-first STOP decision.** An independent audit of the [original T1 development archive](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504/artifacts/13486493479) found that although only 12 requested departure times changed, **380 matched driver IDs had different SUMO `speedFactor` values across independent B and cooperative C, including 368 drivers with unchanged requested departures**. In contrast, the `speedFactor` sequence matched **1,000/1,000 in route-input presentation order**, strongly indicating reallocation of random driver characteristics due to request-order changes. Thus the original realized **+618 network-s** remains an authentic *descriptive* B/C result but **cannot be causally attributed to departure coordination alone**. The original 10-second T1 proxy/policy **DEVELOPMENT NO-GO** remains unchanged. The proposed [physical observation plan](docs/POST_T1_CONTROLLED_PHYSICAL_INTERACTION_OBSERVATION_PLAN_2026-11-06.md) was authorized, but its [single-use workflow](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42339346968) failed during shell preflight **before either SUMO replay executed**; the new confound makes rerunning the same B/C observation scientifically inappropriate. The unused replay workflow/code were removed from the proposed merge. [**Read the consolidated T1 control-integrity finding and stop decision**](docs/POST_T1_EXPERIMENTAL_CONFOUND_ARCHIVE_DIAGNOSTIC_AND_STOP_2026-11-06.md). A distinct prospective per-driver-parameter-controlled design requires separate approval; no reserved cohorts, model tuning, or external publication are authorized.

## T1 development-only feasibility result (November 6 UTC)

**Current T1 timing-proxy DEVELOPMENT NO-GO — do not freeze or launch confirmatory seeds.** The finite independent timing game has an exact potential and its B policy converged with zero remaining gain (no timing shifts) on previously inspected seed **2101**. The shared 10-second proxy numerically distinguished timing choices, but coordinated C predicted **50.63 network-s of benefit** and actually **increased** total preferred-departure-to-arrival cost by **618 network-s** versus independent B in the single development comparison. Only 12 requested departure times changed; nonparticipants had material spillovers. This is a **negative development finding for the tested forecast/policy**, not a rejection of cooperative departure timing generally. [T1 final development feasibility report](docs/POST_C1_T1_TIMING_FEASIBILITY_FINAL_DEVELOPMENT_REPORT_2026-11-06.md) · [Permanent compact results](docs/results/t1_dev2101_feasibility_compact_2026-11-06.json) · [Original successful development workflow](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42183640504). Original Experiment 007 Test A / E1-v2 NO-GO and unexecuted reserved cohorts unchanged.

## Next research direction — T1 cooperative departure timing (approved November 5, 2026)

**Research direction approved, protocol not frozen; no new simulations authorized.** After the completed C1 junction effect-modification study and unsuccessful externality-estimator qualification, the next proposed scientific milestone shifts to **voluntary coordination of departure timing**. Compare a jointly coordinated timing policy with a **credible equally informed independent traffic-aware timing policy**, holding routes and information equal, and measuring all-driver preferred-departure-to-arrival cost plus participant and nonparticipant harms. The goal is to isolate a genuine coordination benefit from information sharing or simple delay shifting. Illustrative timing/participation values and the seed budget remain provisional. [Approved scientific direction](docs/POST_C1_T1_COOPERATIVE_DEPARTURE_TIMING_RESEARCH_DIRECTION_2026-11-05.md) · **[New: Prospective protocol candidate and source-based feasibility review](docs/POST_C1_T1_PROSPECTIVE_TIMING_PROTOCOL_CANDIDATE_2026-11-05.md)**. The candidate specifies independent B convergence, equal-information timing forecasts, consent assumptions, all-driver predeparture-inclusive cost, and prespecified fairness gates; **not frozen, no new SUMO authorized**.

## Current scientific status — Experiment 007 and E1-v2 (November 5, 2026)

**Experiment 007 Test A: NO-GO.** The frozen marginal-externality estimator achieved only **8/20 (40%)** correct directional predictions against a **60%** gate. The independent traffic-aware baseline versus cooperative **Test B was never run**. [Original Test A report](docs/EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md).

**E1-v1 and E1-v2 engineering succeeded, but development prediction qualification failed.** The latest connection-aware **E1-v2-J1** development study completed **60/60 SUMO arms**, **60,000 original tripinfo records** and 10 pre-outcome prediction locks. On development-check seeds **6111–6114**, E1-v2 externality MAE was **1,478.5625 network-seconds** versus **1,478.0625** for the zero-externality B0 reference; directional skill was **5/16 (31.25%)** versus the required **60%**. Frozen decision: **DEVELOPMENT_NOT_QUALIFIED**. Independent-validation seeds **6201–6212** and cooperative policy Test B seeds **6301–6312** remain unopened. [E1-v2 final scientific audit](docs/POST_EXP007_E1_V2_D1_FINAL_DEVELOPMENT_AUDIT_2026-11-04.md) · [Original evidence and SHA256 ledger](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1v2-d1-development-nogo-2026-11-04).

**Latest completed research stage — F0–F5 archive-only mechanism investigation (November 5):** The SHA-verified original 695-file evidence was re-analyzed without new SUMO, model fitting or reserved-seed access. The audit reconciled 50 route-change effects, measured **2,133,360** valid paired five-second edge/time rows and **5,000** descriptive priority-junction contrasts, and reconstructed all ten joint route-bundle interactions. **E1-v2 predicted zero combined-route interaction in all ten cases, while realized interactions ranged from −1,306 to +3,288 network-seconds.** This reveals a model sensitivity problem, **not a uniquely identified causal mechanism**. [Final F0–F5 scientific report](docs/POST_EXP007_E1_V2_F0_F5_ARCHIVAL_MECHANISM_FINAL_REPORT_2026-11-05.md) · [Permanent derived-data release with checksums](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1v2-f0-f5-archive-only-2026-11-05-v2) · [Prespecified F0–F5 plan (PR #85)](docs/POST_EXP007_E1_V2_D1_TIMING_QUEUE_DISCHARGE_BUNDLE_FAILURE_INVESTIGATION_PLAN_2026-11-04.md). Five-second aggregate detectors cannot establish exact vehicle trajectories or causal gap acceptance. Frozen E1-v2 NO-GO and unopened validation/Test B are unchanged.

**Latest completed scientific milestone — four-arm vehicle-resolved mechanism investigation (November 5):** The [user-approved historical four-arm plan](docs/POST_EXP007_E1_V2_FOUR_ARM_PASSIVE_VEHICLE_REPLAY_SCIENTIFIC_PLAN_2026-11-05.md) has now **been executed and independently audited** on two retrospectively selected development seeds, 6112 and 6113 (original I/probe2 pairs; exactly four passive SUMO replays). All **4,000** instrumented driver records exactly reproduced the original departure/arrival/duration/waiting outcomes. One-second FCD independently found **+2,768** and **−3,062** near-stopped vehicle-sample changes (≤0.1m/s) alongside original tripinfo waiting changes **+2,775** and **−3,050 vehicle-seconds** in the harmful and beneficial cases. These observations strongly support different traffic-stopping exposure and route-change response, but do **not** identify a unique causal bottleneck or validate an externality predictor. [Final scientific report](docs/POST_EXP007_E1_V2_FOUR_ARM_PASSIVE_REPLAY_FINAL_SCIENTIFIC_REPORT_2026-11-05.md) · [Permanent four-arm raw trace and checksum release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-e1v2-fourarm-passive-vehicle-replay-2026-11-05) · [Successful no-SUMO archival analysis run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42114348965). Original E1-v2 **DEVELOPMENT_NOT_QUALIFIED**, independent validation NOT_STARTED and cooperative Test B NOT_RUN remain unchanged.

**Latest completed research — C1 controlled E3 junction effect-modification study (November 5, 2026):** The [approved prospective intervention plan](docs/POST_EXP007_CONTROLLED_E3_JUNCTION_EFFECT_MODIFICATION_RESEARCH_PLAN_2026-11-05.md) was implemented on two **retrospectively selected** seeds (6112 and 6113). The pre-outcome lock selected an E3 priority reversal for D3E3→E3E4 versus E4E3→E3E2. **C0–C4 passed:** the four J0 no-op controls reproduced original driver outcomes, and four modified E3 arms completed, exactly **eight new SUMO arms**. The route-by-physical-rule whole-network interaction Ψ was **−7,578 network-seconds for 6112** and **−19,980 network-seconds for 6113**. These are case-specific effects of a local junction priority intervention on the *relative outcome of the same route swap*, **not proof** that the modified priority network is universally better, that a unique queue mediator caused the original effect, or that cooperative routing outperforms informed independent routing. Individual and nonparticipant harms remain material. [C1 final scientific report](docs/POST_EXP007_C1_E3_CONTROLLED_FINAL_SCIENTIFIC_REPORT_2026-11-05.md) · [source-locked original eight-arm research release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-c1-e3-controlled-effect-modification-2026-11-05) · [C1 execution and audit workflow](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/42127084838). Frozen E1-v2 DEVELOPMENT_NOT_QUALIFIED, independent estimator validation NOT_STARTED and cooperative Test B NOT_RUN are unchanged.

**Long-term objective remains open:** Discover whether voluntary, collective routing can improve total traffic outcomes relative to an **equally informed independent traffic-aware baseline**, while measuring participant and nonparticipant harm. No successful cooperative advantage has been demonstrated. Findings are from a synthetic SUMO network, not observed public-road traffic.

## Public research updates (historical; Experiments 003–006)

**[We corrected a consequential routing flaw. But cooperation still didn't win.](docs/RESEARCH_UPDATE_EXPERIMENTS_003_TO_006.md)**

A concise, reader-friendly account of prediction improvements, the unexpected routing failure, its clock-alignment correction, and the inconclusive independent-routing comparison with severe individual harms. This is the **one destination linked from the LinkedIn and X research announcement**, with the frozen reports and original runs linked inside.

## Scientific direction — mechanism efficacy first; experience later (November 1, 2026)

[Foundational Scientific Synthesis & Research-Direction Assessment](docs/FOUNDATIONAL_SCIENTIFIC_SYNTHESIS_AND_RESEARCH_DIRECTIONS_2026-10-31.md) — updated sequencing decision:

1. **Now:** Establish when and how distinct coordination mechanisms (system-optimal route assignment, voluntary departure/bottleneck timing, traffic-flow control) improve network performance against credible independent baselines.
2. **Alongside that:** Continue measuring individual fairness, severe realized delays, consent/participation assumptions and spillover effects.
3. **Later:** Consider quality of experience (comfort, calmness and perceived journey quality). These outcomes are **not active experiment objectives** and have not been measured by our SUMO studies. [Deferred exploration notes](docs/DEFERRED_QUALITY_OF_EXPERIENCE_RESEARCH_NOTES.md).

**Historical direction note (November 1):** The comparative mechanism assessment led to Experiment 007. Its Test A has now run and failed; newer E1-v1/E1-v2 estimator development has also failed to qualify. See the current status above rather than treating this earlier planning state as current.

## Latest verified science — Experiments 001–006 (October 31, 2026)

**Experiment 006 executed:** Clock-aligned cooperative policy E **did not demonstrate a network-wide advantage over independent nominal free-flow shortest-path policy A** on ten new paired high-congestion seeds. Mean completed-trip duration A−E was **+0.2429 seconds** (95% seed-level CI **−1.9120 to +2.3978 seconds**), so the primary efficacy result is **INCONCLUSIVE**. E also delayed **27.98% of matched drivers by more than 30 seconds**, violating the frozen **10% severe-individual-harm limit**. Thus the joint network-efficiency/fairness GO criteria were **not met**. All trips completed; structured collision/emergency statistics were zero. [Full scientific report](docs/EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md) · [Frozen prospective protocol and execution plan](docs/EXPERIMENT_006_E_VS_A_PROSPECTIVE_PROTOCOL.md) · [Successful GitHub run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41185989951).

**Experiment 005 remains scientifically supported:** Clock alignment improved E relative to the original calibrated cooperative D policy by **20.13 seconds** in high congestion (95% paired seed-level CI **16.74–23.53s**); E's advantage over D must **not** be described as superiority over independent A. [Experiment 005 results](docs/EXPERIMENT_005_CLOCK_ALIGNMENT_RESULTS.md).

**Original Experiment 004 D retains its NO-GO decision.** The broader research hypothesis remains unresolved. Current next question: understand and mitigate realized individual harm, while retaining collective efficiency, before any new policy is called a success. The existing 200s regime A is an independent **nominal free-flow** shortest-path baseline, **not** a strong modern traffic-aware navigation system.

**Historical status note:** The dated M3 operational and development milestones below are preserved chronologically. Statements about evaluation seeds remaining unrun describe their October 26–27 snapshots and are superseded by the completed Experiment 003–006 reports.

## Historical research-status archive — October 26–27, 2026

**Latest M3 operational review (October 27):** A [read-only safeguards audit](docs/EXPERIMENT_002_M3_OPERATIONAL_READINESS_REVIEW_2026-10-27.md) passed six tests and closed a legacy manually supplied seed pathway that could have accidentally generated reserved evaluation seeds. GitHub returned **HTTP 404 for the protected reviewer environment** and independently confirmed **`main` is not protected**. [Permanent machine-readable evidence](docs/results/exp002_m3_operational_review_2026_10_27/README.md). **Held-out execution remains blocked and no reserved seeds have run.**



**M3 production-adapter review (October 27):** [R3/R4 production adapters and activation safeguards passed offline review](docs/EXPERIMENT_002_M3_PRODUCTION_ADAPTER_REVIEW_FINDINGS_2026-10-27.md) with [per-scenario evidence](docs/results/exp002_m3_production_adapter_review_2026_10_27/README.md). All eight synthetic tests passed, and frozen R3 outputs were reproduced exactly from already inspected development cases. **Protected GitHub approval environment remains unverified, and reserved evaluation seeds have not run.**


**Held-out workflow preparation (Oct 27):** The [frozen M3 development harness qualified end-to-end](docs/EXPERIMENT_002_M3_RUNNER_DEVELOPMENT_QUALIFICATION_2026-10-27.md) in all three already-inspected seed2101 congestion regimes. [Durable scenario evidence](docs/results/exp002_m3_qualification_2026_10_27/README.md) and an [explicitly inactive held-out workflow draft](docs/templates/experiment-002-m3-heldout-evaluation.yml.disabled) are published. **No held-out execution is enabled or authorized.**


**M3 protocol freeze — October 27, 2026:** **APPROVED and committed** as an exact [frozen Git snapshot](https://github.com/yonnastgetahun/cooperative_traffic_research/tree/exp002-m3-protocol-v1-frozen) (authoritative commit `be2e8d27c78c8b6de4891115d6d951edc877ac6e`). See the [scientific decision record](docs/EXPERIMENT_002_M3_FREEZE_DECISION_2026-10-27.md), [frozen protocol](https://github.com/yonnastgetahun/cooperative_traffic_research/blob/be2e8d27c78c8b6de4891115d6d951edc877ac6e/docs/EXPERIMENT_002_M3_FROZEN_PROTOCOL_V1.md) and [hash manifest](https://github.com/yonnastgetahun/cooperative_traffic_research/blob/be2e8d27c78c8b6de4891115d6d951edc877ac6e/docs/EXPERIMENT_002_M3_PROTOCOL_FREEZE_MANIFEST_V1.json). **This freezes the scientific methodology, not an executable evaluation runner. Held-out seeds 3101–3110 remain unopened and all evaluation runs require separate approval.**



**Latest pre-freeze milestone (Oct 26):** R3 completed native teleport/collision/partial-bin audits in **three invariant development replays**, with **0 reported teleports** across the three cases. R4 implemented and tested **seed-level paired** forecast-error analysis using already inspected development seeds, while keeping all 3101–3110 evaluation seeds untouched. [R3–R4 findings](docs/EXPERIMENT_002_G3_R3_R4_EXECUTION_RESULTS_2026-10-26.md) · [full durable evidence](docs/results/exp002_g3_r3_r4_2026_10_26/README.md). An [M3 protocol freeze proposal](docs/EXPERIMENT_002_M3_PROTOCOL_FREEZE_PROPOSAL_V0_1.md) is published **for review only; neither the freeze nor held-out execution is authorized**.



We have completed Experiment 001 congestion calibration and the initial Experiment 002 comparison in a 10×10 synthetic SUMO network (1,000 vehicles; departure windows of 200, 600, and 1,200 seconds). In the three-seed development comparison, **independent routing produced shorter average trips than both cooperative-routing prototypes** in every congestion regime. This is an early negative result, not a claim about real-world traffic.

The next question is whether the time-aware traffic predictor is accurate enough to guide coordination. Our [three-regime development trace](docs/EXPERIMENT_002_ACTUAL_PREDICTOR_TRACE_2026-10-26.md) is complete. It is more accurate than free-flow timing in all three tested scenarios but **still significantly underpredicts congestion-related delays**, and is not held-out validation.

**Latest G3 timing-reference verification (Oct 26):** A development-only one-seed-per-regime replay matched **25,179/25,179** native external-road entry steps to historical FCD front-position timestamps and independently verified **1,994,952 actual route-search occupancy-counter reads** with unchanged routing and tripinfo. These are instrumentation-integrity results, **not** predictor calibration; the predictor still systematically underestimates arrivals. [See verified findings](docs/EXPERIMENT_002_G3_R1_R2_VERIFICATION_RESULTS_2026-10-26.md). Held-out evaluation is not authorized.

**Latest milestone (Oct 26):** The physical occupancy/junction measurement code passed its fixtures and ran on **three new development seeds across all three regimes (nine successful cases, 9,000 total completed trip records)**. Mean time-aware road-entry MAE remained **54.45 / 19.38 / 13.61 seconds** (200/600/1,200s) compared with a free-flow reference of **59.93 / 23.35 / 17.13 seconds** on the same chosen routes. The model still substantially underpredicts congestion delay. Native versus sampled occupancy discrepancies and subsecond junction uncertainties remain open. **No held-out seeds were run.**

- [Research progress report — Experiments 001–002](docs/RESEARCH_PROGRESS_REPORT_2026-10-24.md)
- [Approved Experiment 002 Predictor Validation Plan v0.2](docs/EXPERIMENT_002_PREDICTOR_VALIDATION_PLAN.md)
- [Actual predictor trace: development findings and limitations](docs/EXPERIMENT_002_ACTUAL_PREDICTOR_TRACE_2026-10-26.md)
- [Completed M0–M2 development: physical occupancy & junction-delay findings](docs/EXPERIMENT_002_OCCUPANCY_M2_DEVELOPMENT_RESULTS_2026-10-26.md)
- [Measurement design and M3 holdout gates](docs/EXPERIMENT_002_OCCUPANCY_JUNCTION_MEASUREMENT_PLAN_V0_1.md)
- [Latest G3 reconciliation: occupancy semantics, 211 vehicle-level cases and remaining gates](docs/EXPERIMENT_002_G3_RECONCILIATION_FINDINGS_2026-10-26.md)
- [**New G3 J0–J3 native junction and exact search-time event findings**](docs/EXPERIMENT_002_G3_EVENT_INSTRUMENTATION_RESULTS_2026-10-26.md)
- [Archived G3 event integrity reports and C6C7 target case](docs/results/exp002_g3_events_2026_10_26/README.md)
- [**Latest: G3 three-regime native/FCD timing and actual search-read verification**](docs/EXPERIMENT_002_G3_R1_R2_VERIFICATION_RESULTS_2026-10-26.md)
- [Archived per-road timing results and counter integrity files](docs/results/exp002_g3_r1r2_2026_10_26/README.md)
- [**G3 observation sufficiency decision: what can be measured and what cannot**](docs/EXPERIMENT_002_G3_OBSERVATION_SUFFICIENCY_REVIEW_2026-10-26.md)
- [G3 limits and blockers before M3 freeze — 14-item register](docs/EXPERIMENT_002_G3_MEASUREMENT_LIMITATIONS_REGISTER_2026-10-26.csv)
- [G3 junction exit times and actual route-search lookup design (executed on development scenarios)](docs/EXPERIMENT_002_G3_EVENT_INSTRUMENTATION_DESIGN_V0_1.md)
- [Archived G3 evidence and CSV tables](docs/results/exp002_g3_2026_10_26/README.md)
- [Successful three-regime decision-trace workflow and artifacts](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40443562182)
- [Proposed separate Experiment 003: voluntary departure scheduling](docs/EXPERIMENT_003_DEPARTURE_SCHEDULING_ROADMAP.md)

**Latest diagnostic insight:** G3 reconciliation suggests much of the native road/FCD discrepancy comes from vehicle front-position versus cross-edge physical-presence semantics. In 211 preselected discrepant bins, vehicle fronts were observed near downstream internal junction boundaries. **The interpretation is not exact native per-vehicle attribution, the G3 gate remains open, and held-out seeds are untouched.**

**Latest G3 sufficiency review:** SUMO-native step-level road/junction timing and native aggregate road load are conditionally sufficient for a *narrow simulation-only timing diagnostic*. Route assignment counts are not physical occupancy forecasts; internal-junction residence is not causal delay. The [pre-freeze review](docs/EXPERIMENT_002_G3_OBSERVATION_SUFFICIENCY_REVIEW_2026-10-26.md) records cross-regime reference-join and provenance checks that must still be completed; **M3 has not been frozen and the evaluation seeds remain untouched.**

**Research boundary:** No statistically validated cooperative-routing benefit, deployment readiness, or real-world safety improvement has been established.

## The idea

Explore whether drivers could voluntarily share travel intentions and accept limited, coordinated route recommendations to reduce *total* congestion. This isn't a claim that today's maps do no coordination, or that autonomous cars automatically cooperate. It's a question we can test.

## Original Experiment 001 design goals (historical)

The bullets below preserve the original research design and hypotheses. Some planned participation and baseline-comparison scenarios are not yet implemented; see the current-status section above for what has actually been tested.

- **Question:** Can voluntary coordination among some drivers reduce network-wide congestion without unfairly burdening participants or other drivers?
- **Baseline:** Independent, traffic-aware route choices.
- **Intervention:** A transparent centralized cooperative route assignment, initially holding departure times constant.
- **Participation:** Compare 0%, 5%, 10%, 25%, and 50%, with multiple random seeds and later compliance sensitivity tests.
- **Measures:** Total and average travel time, network delay, congestion, and outcomes for participating and nonparticipating drivers.
- **Fairness:** Limit excessive individual detours and measure spillovers; report null and negative outcomes.
- **First implementation:** A small synthetic network with alternative routes in SUMO, followed by reproducible comparisons.
- **Visualization:** Export the same simulation data for side-by-side animations, short social clips, and eventually an interactive presentation. Stock traffic footage in milestone announcements illustrates the problem, not experiment results.

## Scientific foundations

- **Wardrop's equilibrium:** Individually attractive routes need not minimize total network travel time.
- **System-optimal assignment:** A different distribution of routes may reduce total travel time, sometimes at a cost to particular drivers.
- **Price of anarchy:** The gap between outcomes under self-interested choices and coordinated optimization.
- **Braess's paradox:** Under certain conditions, adding a road can make travel slower.
- **Phantom traffic jams and cooperative control:** Stop-and-go waves can arise without a blockage; controlled vehicle behavior can sometimes dampen them.
- **Mechanism design:** Cooperation must address incentives, consent, fairness, and the temptation to ignore recommendations.
- **Induced demand:** Better traffic flow can encourage additional driving over time.

## Assumptions to challenge

1. Autonomy alone does not imply network-wide cooperation.
2. Coordination of human drivers might deliver benefits using existing smartphones.
3. A minority of participating drivers might influence the wider network; the effect and required participation are unknown.
4. Benefits must be evaluated against capable traffic-aware navigation, not an artificially weak baseline.

**Status:** This initial design milestone is historical; calibration and routing experiments have now been run. See the current-status section above for measured results and remaining gaps.

## Further reading

- [Wardrop's principles](https://en.wikipedia.org/wiki/Wardrop%27s_principles)
- [Braess's paradox](https://en.wikipedia.org/wiki/Braess%27s_paradox)
- [SUMO documentation](https://sumo.dlr.de/docs/)

See [research foundations](docs/research-foundations.md), [experiment plan](docs/experiment-plan.md), and [project checkpoint](docs/checkpoint.md) for evolving notes.
