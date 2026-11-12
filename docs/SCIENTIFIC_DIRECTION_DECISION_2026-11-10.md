# Scientific direction decision — Make the central question central again

**Decision discussed:** November 10, 2026 · **Public-facing summary:** November 11, 2026  
**Direction:** Prefer **B — a new, independently designed investigation of the fundamental cooperation hypothesis**. Defer **A — exact T1 cross-framework replication**.  
**Scope:** Scientific direction and prospective protocol work **only**. This is not a new empirical finding, a frozen protocol, authorization to implement an algorithm, run a simulation, open a reserved cohort, or claim practical cooperative traffic benefits.

## The question we began with

Could voluntary coordination among drivers improve network-wide traffic outcomes **beyond equally informed independent decisions**, without unacceptable costs to participants or nonparticipants?

Our motivating thought experiment starts with a possible future in which vehicles can share awareness and coordinate choices. Autonomous driving does not automatically imply such cooperation, nor is this project claiming that existing navigation products cannot coordinate.

## What the evidence taught us

- **Experiment 001:** On the initial synthetic road network, both tested cooperative-routing prototypes had longer mean trips than the nominal free-flow independent baseline across three congestion regimes. That baseline was **not** equivalent to modern traffic-aware navigation. [Research progress report](RESEARCH_PROGRESS_REPORT_2026-10-24.md).
- **Experiments 003–004:** Independent confirmatory tests reduced chosen-route road-entry prediction MAE by **34.2%** under high congestion (46.3% and 51.3% in the other regimes). But the tested calibrated cooperative routing policy D increased mean trip duration by **18.53 seconds** relative to its uncalibrated adapter C under high congestion. **Policy D: NO-GO.** These are distinct tests and do not establish that prediction improvement caused the deterioration. [Prediction report](EXPERIMENT_003_CONFIRMATORY_RESULTS.md) · [Routing report](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md).
- **Experiments 005–006:** Correcting the policy clock improved E relative to flawed D by **20.13 seconds** at high congestion; that was not an independent-routing advantage. Against nominal free-flow independent A, E's estimated mean benefit was **0.24 seconds** (95% CI **−1.91 to +2.40**), **inconclusive**. **27.98%** of matched drivers experienced over 30 seconds of additional delay, so the joint efficiency/fairness criteria were **not met**. [Correction report](EXPERIMENT_005_CLOCK_ALIGNMENT_RESULTS.md) · [E-versus-A report](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md).
- **Experiment 007 and E1-v2:** The Test A externality predictor correctly identified the sign in **8 of 20** qualifying probes, below its frozen 60% gate; the conditional cooperative Test B was **not run**. Subsequent E1-v2 development also failed qualification. [Experiment 007 report](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md) · [E1-v2 audit](POST_EXP007_E1_V2_D1_FINAL_DEVELOPMENT_AUDIT_2026-11-04.md).
- **C1 and T1:** A controlled synthetic-junction change materially modified route-change consequences in two studied cases without establishing a better road network. A better-controlled T1 timing comparison produced **+2,131 all-driver network-seconds** for the tested coordinated schedule; shared random-event-order effects remain unresolved, so that total cannot be uniquely attributed to physical traffic propagation. The current T1 forecast and timing policy retain a **development NO-GO**. [C1 report](POST_EXP007_C1_E3_CONTROLLED_FINAL_SCIENTIFIC_REPORT_2026-11-05.md) · [T1 controlled report](POST_T1_ID_LOCKED_CONTROLLED_DEVELOPMENT_FINAL_SCIENTIFIC_REPORT_2026-11-07.md) · [SUMO source audit](POST_T1_SUMO_RNG_EVENT_ORDER_AND_PHYSICAL_PROPAGATION_SOURCE_AUDIT_FINAL_REPORT_2026-11-07.md).

These findings describe tested algorithms and synthetic conditions. They do **not** rule out all beneficial cooperative allocations, demonstrate real-world willingness to participate, or establish a general cooperative advantage.

## Two different problems

1. **Existence:** Under physically meaningful traffic and voluntary-choice constraints, can a beneficial collective allocation exist beyond what equally informed independent drivers could achieve?
2. **Prediction and implementation:** Can an algorithm forecast consequences, find that allocation, and implement it reliably?

These are related, but a theoretically advantageous allocation is **not** yet an effective algorithm or an acceptable real-world intervention.

> We've spent considerable effort on the second problem—predicting traffic consequences and engineering policies—without yet establishing a clean experimental setting in which the first problem can be investigated.
>
> A new scientific design should first make that distinction explicit. A plausible theoretically superior allocation would motivate further research, but not prove practical cooperative traffic benefits. Conversely, another failed heuristic would not establish that no beneficial coordinated allocation exists.

## Why the focus changes

Further simulator-specific replication could clarify the original T1 result, but it is not the highest-priority route to answering the overarching hypothesis. The [UXsim and CityFlow feasibility assessment, PR #115](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/115), has been merged into the historical record with an **EVIDENCE INSUFFICIENT** source-assessment conclusion. Neither framework was qualified for faithful exact-T1 reproduction; an independent release-TAR verification item and representation/measurement questions remain unresolved. This is **not** a finding that either simulator is generally invalid.

**Direction B is the preferred intellectual priority:** first specify a small, credible, simulator-independent conceptual comparison in which genuinely collective choices are distinguishable from independently informed choices. Any prospective protocol must account for full preferred-departure-to-arrival costs, participants and nonparticipants, meaningful physical interactions, information parity, and voluntary acceptance assumptions.

**Next activity:** Conceptual and prospective-protocol assessment only. No new experiment, simulation, implementation, reserved-cohort access, research-policy change, or external social publication is authorized by this document.

**Product-development lesson:** Some technical complexity was necessary and informative. The decision is to be more selective about complexity that advances the central uncertainty—not to hide negative results, dismiss simulation work, or guarantee a favorable outcome.
