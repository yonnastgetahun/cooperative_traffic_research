# Experiment 007: We tested the network effects of route changes. Our predictions failed—and the investigation revealed why.

**Cooperative Traffic Research | Public research update | November 2, 2026**

**Status:** Test A completed and failed its prospectively frozen progression gate. Post-test forensic investigation P0–P3 completed. Six-run instrumented replay completed and validated. **Test B was not executed.**

## The question behind this research

Can drivers voluntarily coordinate route choices so that the *entire* traffic network functions more efficiently, while protecting individuals from unacceptable delays?

Conventional individual route selection asks which path is best for each driver's journey. The cooperative hypothesis asks an additional question: **What happens to everyone else when one driver takes a different route?**

Those consequences are known as *network externalities*. A potential cooperative system cannot credibly promise an advantage merely by recommending different routes. It needs to anticipate the collective effects of those decisions, and then test whether acting on those predictions improves **actual total travel time** compared with an independent-routing system that has **comparable traffic information**. Realized driver fairness is a separate required criterion.

Experiment 007 deliberately separated these claims:

- **Test A — Mechanism validation:** Can a frozen estimator predict the sign and approximate magnitude of the travel-time change experienced by *other drivers* when one planned route is changed?
- **Test B — Collective efficacy:** If Test A supports an estimator, does an externality-aware cooperative route-assignment policy reduce actual whole-network journey time versus an equally informed independent traffic-aware policy, without unacceptable realized harm to participants or nonparticipants?

This separation matters. A model's ability to predict a route is not proof of its ability to predict the *network consequences* of assigning it. And even an accurate local predictor does not guarantee a successful or fair collective optimizer.

## Milestone 1 — The original Test A result: a scientific NO-GO

Using the open-source SUMO simulator, we studied a synthetic **10 × 10 road grid** with **1,000 scheduled vehicles** in a high-congestion **200-second departure window**. The frozen Test A design used five independent demand seeds, each with one baseline, four individual-route perturbations, and one combined two-route perturbation: **30 completed SUMO simulations**.

For the 20 selected single-route changes, the initial estimator was evaluated against the realized summed elapsed-time change among the other **999** vehicles.

| Test A metric | Original result |
|---|---:|
| Correct predicted externality sign | **8/20 = 40%** |
| Frozen minimum required to advance | **60%** |
| Predicted zero externality despite material observed effects | **5/20 probes** |
| Mean absolute externality prediction error | **1,801.71 network-seconds** |
| Predicted externality range | **−3.24 to +13.50 network-seconds** |
| Realized externality range | **−3,777 to +4,328 network-seconds** |

A **network-second** means one second of travel time summed across drivers—not one driver's additional journey duration. Negative effects denote savings; positive effects denote additional elapsed time.

These probes were purposefully chosen by the original model's predictions, **not** sampled at random from every possible route change. Five independently generated demand seeds—not 20 probe identities—were the experimental replication units.

**Decision:** The estimator failed the prespecified Test A gate. **Test B was correctly stopped before execution.** No claim of an efficient or fair cooperative routing advantage was established, nor did this result disprove all possible forms of cooperation.

[Original frozen Test A scientific report](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md) · [Original preregistered protocol](EXPERIMENT_007_FROZEN_PROTOCOL_V1.md)

## Milestone 2 — The P0–P3 investigation: a structural limitation identified

Instead of retuning the estimator to rescue the failed outcome, we audited the original simulation evidence and its mathematics.

The read-only P0–P3 investigation independently checked **all five original archive families**, all **30** scenario arms, and **20,000 matched driver comparisons** across the 20 single-route probes. The original results were reproduced without rerunning SUMO.

The most important finding was **mathematical rather than merely statistical**.

For all 20 tested alternative-route changes, which had equal nominal free-flow travel time on the synthetic grid, the estimator's model-implied total change was approximately **twice its predicted own-driver change**. Consequently:

\[
\widehat{\Delta C}_{\mathrm{total}}
= 2\,\widehat{\Delta T}_{\mathrm{self}},
\qquad
\widehat{\Delta T}_{\mathrm{others}}
= \widehat{\Delta T}_{\mathrm{self}}.
\]

The identities held to numerical precision for the selected probes. In those conditions, the supposed estimate of other drivers' costs **mirrored the treated driver's predicted cost**, rather than providing a distinct prediction of congestion effects on others.

**What this establishes:** The frozen assigned-demand model had an important *structural limitation* for the examined equal-free-flow alternatives. It did not independently represent queue formation, intersection discharge, spillbacks, or interacting traffic-flow changes as measured physical mechanisms.

**What it does not establish:** That an algebraic identity necessarily holds for all possible route classes or road networks; that every prediction failure is explained exclusively by this identity; or that cooperative routing is impossible.

The same audit also showed that route changes affected many drivers whose assigned road-edge sequences remained unchanged. On average across the purposefully selected probes, approximately **436 other drivers became slower** and **422 became faster**. The network effect was the difference between many offsetting individual gains and losses—not simply the effect on the rerouted vehicle.

The five original two-route bundles also demonstrated departures from additive forecasts: their realized bundle interactions were **+218, −2,989, −2,672, −1,930, and −1,502 network-seconds**. Observing interaction does not by itself identify the junction causing it.

[Complete P0–P3 forensic investigation](POST_EXP007_EXTERNALITY_ESTIMATOR_P0_P3_FINAL_SCIENTIFIC_REPORT.md) · [Reproducible archive audit](../research/audits/exp007_p0_p3_audit.py)

## Milestone 3 — A six-run replay: observing what the model missed

The original records lacked time-resolved vehicle positions and road-level measurements. We therefore froze a **separate six-run observational replay**, selected *after seeing* the Experiment 007 outcomes:

- Seed 4101: baseline and the individual-route probe whose externality was predicted as **zero**.
- Seed 4102: baseline, two individual-route probes, and their combined two-route assignment.

The replay reused the original network, 1,000-vehicle demand, route files, simulator seeds, and pinned **SUMO 1.28.0** environment. Only passive measurements were added: approximately **one-second vehicle trajectories**, route-edge exit times, and **five-second edge/lane traffic observations** including junction-related measurements.

**All six replays passed the original-outcome equivalence gates.** Across 6,000 matched trip records, the checked trip fields reproduced the corresponding historical outputs with **0.00-second maximum difference**; recorded simulator exception fields also matched. This is a validation of replay fidelity, not a real-world safety claim.

### Three findings from the new observations

**1. Actual road-entry timing diverged substantially from the forecast.** In the examined seed-4102 baseline, one target driver's predicted 30-second road-entry bins disagreed with the observed bins on **11 of 12 route edges**; another target differed on **11 of 13**. These are selected trace diagnostics, not a population-wide timing-accuracy estimate.

**2. Stopped-time waiting was an important observed component of the network effect.** Adding or changing a single planned route produced large differences in actual stopped time across other vehicles. For example:

| Original route intervention versus same-seed baseline | Added total network travel time | Additional recorded waiting time |
|---|---:|---:|
| Seed 4101, predicted-zero single-route probe | **+3,177 network-seconds** | **+2,829 network-seconds** |
| Seed 4102, first single-route probe | **+2,626** | **+1,357** |
| Seed 4102, second single-route probe | **+3,935** | **+3,419** |
| Seed 4102, combined two-route probe | **+3,572** | **+2,594** |

SUMO's recorded waiting time is **already included** in trip duration; these are *component comparisons*, not quantities to add together. Separate departure-insertion changes were relatively small in these selected contrasts. One-second near-stop trajectory samples broadly corroborated the waiting differences.

**3. Traffic responses interacted across route assignments.** In seed 4102, a driver following the **same planned route** reached synthetic road segment **C6C5 39 seconds earlier** when another vehicle's route was changed as part of the combined two-route scenario. The full joint effect was **−2,989 network-seconds** relative to the sum of the two separately measured effects:

\[
3,572-(2,626+3,935)=-2,989.
\]

Five-second measurements also exposed localized regions of increased and decreased waiting—notably different times and directions on synthetic edges such as **D6C6**, **D3E3**, and **E6E5**. These traces directly establish differences in physical traffic-state observations; they do **not** prove that a particular named junction was the unique causal source of the complete network effect.

### What changed in our understanding

We now have *two distinct kinds of evidence*:

- A **verified structural deficiency** in the tested estimator's prediction of others' costs.
- **Reproducible physical observations** that actual traffic effects were strongly time-dependent, queue-associated and nonadditive in the selected replay cases.

Neither is sufficient by itself to claim that a redesigned estimator will work. The six runs were exploratory, selected after examining the Test A outcomes, and were not independent validation on unseen traffic scenarios.

[Complete six-run scientific report](POST_EXP007_SIX_RUN_INSTRUMENTED_REPLAY_FINAL_SCIENTIFIC_REPORT.md) · [Frozen replay protocol](POST_EXP007_SIX_RUN_INSTRUMENTED_REPLAY_FROZEN_PROTOCOL_V1.md) · [Reproducible replay code](../research/replay/exp007_instrumented_v01.py)

## Reproducible research and evidence preservation

The investigation retained its scientific audit trail rather than overwriting the negative finding:

- Original frozen Test A outcomes, full scientific reports, independent archive audits and reproducible code remain in the repository.
- The six instrumented replay runs, the two original frozen seed archives, the scientific analysis and SHA-256 member/asset manifests are published together in a [permanent GitHub research release](https://github.com/yonnastgetahun/cooperative_traffic_research/releases/tag/exp007-sixrun-replay-2026-11-02).
- No new estimator was trained or declared valid, no new cooperative policy was tested, no human opt-in/compliance was observed, and no real-road claims were made.

**Boundary:** This is an intentionally constrained synthetic-network study. The original independent policy was a documented traffic-aware pretrip control under idealized shared demand information, **not** a validated emulation of Google Maps, Apple Maps or Waze. Test B, which would compare cooperative and independent policies directly, remains unexecuted. Realized individual fairness remains an active requirement; subjective comfort and journey quality remain deferred.

## What comes next: the scientific sequence

**1. Develop a better estimator.** Build a prospective model that can distinguish **a driver's own predicted travel time** from the **network effects on other drivers**, incorporating relevant traffic interactions such as junction queues, bottleneck discharge, congestion propagation and actual road-entry timing. The current traces inform the problem definition but must not be mistaken for a validated model.

**2. Validate it independently on fresh, unseen simulations.** Freeze the new estimator and evaluation protocol before testing. Use new independent demand seeds and route perturbations **not used to design, fit or select the model**. Measure predicted-versus-realized externality direction, magnitude, calibration, rankings, robustness and adverse false-benefit cases. Include interacting bundles. Do not call the estimator validated because it fits the original failed probes or six explanatory replays.

**3. Proceed to Test B only if validation succeeds.** With the estimator frozen, compare **cooperative network-externality-aware routing** against an **equally informed independent traffic-aware routing baseline** on new matched simulations. Measure real, scheduled-departure-to-arrival network time for **all drivers** and separately require realized **individual and nonparticipant fairness**, not just an improvement in average time. Any success must be restricted to the tested simulator, network and participation assumptions.

The sequence is deliberate: **understand and predict the externality → validate on data the model has never seen → test whether coordination produces a collective benefit without unacceptable individual harm.**

## The research question remains open

**Can voluntary cooperation produce a genuinely better traffic system for everyone—or do the interactions and fairness costs defeat the predicted advantage?**

Experiment 007 has **not** answered that question yet. It has moved us from a failed prediction toward a clearer understanding of what the next estimator would have to know—and what evidence would be required before we make a collective-optimization claim.

---

*Cooperative Traffic Research · Open-source scientific progress update · November 2026. This page is a retrospective synthesis of the original Experiment 007 results and subsequent archive-only and instrumented investigations. No new result beyond the linked reports is claimed.*
