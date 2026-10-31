# Experiment 006 — Clock-aligned cooperation E vs independent routing A

**Status (prospective):** Approved to document, implement and execute end-to-end on October 31, 2026. **No Experiment 006 outcomes exist at the time of protocol freeze.** This document must be committed to `main` before fresh-seed simulation. Existing Experiments 001–005 are immutable historical evidence.

## 1. Why this test is necessary

The [Experiment 005 final report](EXPERIMENT_005_CLOCK_ALIGNMENT_RESULTS.md) established that replacing D's inconsistent post-assignment free-flow occupancy clock with calibrated chosen-route replay (policy **E**) improved the high-congestion network mean by **20.1317 seconds relative to D** (95% paired seed-level CI **16.7378–23.5256s**). It did **not** compare E with A on matched fresh demand.

**Scientific question:** Does the frozen clock-aligned cooperative policy E improve network-wide mean trip time compared with the original independent routing baseline A, **without unacceptable deterioration in individual driver outcomes**?

**Critical baseline limitation:** Experiment 004/005 **A chooses an independent shortest path by nominal free-flow travel time** using SUMO's network shortest-path method. It is **not** a state-of-the-art live traffic-aware navigation service, a user equilibrium, or a real-world Google Maps/Waze/Apple Maps benchmark. A positive E−A result in the present 10×10 synthetic grid would therefore establish only superiority to this *specific* baseline; it would **not** prove superiority to modern independent traffic-aware routing.

## 2. Frozen hypotheses, arms, and estimands

- **A: frozen independent-routing baseline.** Execute the original Experiment 004 `four_arm_routes_v01.py` in arm `A` mode, whose independent search returns `ff_path(net, origin, destination)`. Route-assignments, selected routes, fixed departure times and SUMO settings use unchanged source.
- **E: frozen cooperative policy.** Execute Experiment 005 `clock_alignment_routes_v01.py` in arm `E` mode. It retains the stateful calibrated candidate search and detour guardrails, and updates assignment occupancy in chosen-route *calibrated* forecast bins using the read-only pre-assignment counter snapshot. Use original Experiment 003 coefficients exactly, per regime. Do not retune or modify either arm.
- **Paired experiment:** the same fixed synthetic 10×10 SUMO network and the *same* 1,000 vehicles, OD pairs, departure schedule and random seed for A and E. Do not use post-simulation observations for decisions. Freeze source revision and pinned SUMO image before running.
- **Primary congestion regime:** 200-second departure window; other regimes 600s and 1200s are prespecified secondary/exploratory tests.
- **Primary estimand:** mean of 10 paired seed-level contrasts `mean_trip_duration_A − mean_trip_duration_E` at 200s. **Positive favors E.** Two-sided Student-t 95% interval across independent seeds (df=9); driver count (10,000 per arm/regime) does *not* create 10,000 independent experimental replications.
- **Confirmatory primary hypothesis:** E reduces the seed-paired mean completed-trip duration relative to A in high congestion. The statistical criterion is lower bound of its two-sided 95% seed-level confidence interval strictly above zero.

## 3. Fixed fresh cohort and analysis integrity

**Fresh independent demand seeds:** `3501, 3502, 3503, 3504, 3505, 3506, 3507, 3508, 3509, 3510`, disjoint from previous development/confirmatory cohorts 2101, 2201–2210, 3101–3110, 3201–3210, 3301–3310, and 3401–3410. No substitution after outcome inspection.

**Windows:** 200s, 600s, 1200s. **30 paired seed/window scenarios = 60 arm executions**, each with 1,000 vehicle departures; aggregate the ten seed contrasts separately for each regime. The seed number and scenario are fixed before the first SUMO job.

**Implementation freeze:** Use Experiment 004 original arm A code and Experiment 005 E code from the checked-in `main` revision at the time of Experiment 006 implementation; preserve the **exact commit SHA** of that revision and source file hashes in the execution record. The original scientific generator is the frozen commit `be2e8d27c78c8b6de4891115d6d951edc877ac6e`. Use the exact pinned SUMO image `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`. Do not change the 10×10, 200-meter-grid design or the vehicle demand generation. No exploratory modifications to model cost, detour allowance, start-time policy or calibration coefficients.

## 4. Network efficiency and individual fairness (joint, prespecified)

**Primary:** mean completed-trip duration A−E on 200s, 95% independent-seed confidence interval.

**Essential safeguards, evaluated using the same matched driver identities and seed-aware summaries:**
1. **Completion:** all 1,000 vehicles complete in *both arms* in all prespecified cases for a clean mean-duration inference. If any are incomplete, do **not** silently drop or impute; report missing/censored counts, and withhold GO until a defensible all-departure sensitivity analysis is available.
2. **Tail noninferiority:** mean across high-congestion seed-level p90 trip durations for E **must not exceed A by more than 5 seconds**. Also publish the seed-level p90 paired difference and its 95% interval. This is a prespecified pragmatic fairness tolerance, not proof of full distributional equality.
3. **Majority harmed:** the pooled percentage of the **10,000 matched high-congestion vehicle identities** with strictly longer travel time in E than A must be **no more than 50%**. Report helped/unchanged/harmed and seed-level harmed fractions; these are descriptive matched outcomes, not independent-sample hypothesis tests.
4. **Severe individual harm:** at most **10%** of those 10,000 matched vehicles may be delayed **more than 30 seconds** by E compared with A. Separately report seed-level percentages and p95 driver-level E−A travel-time harm. This protects against hiding material concentrated individual sacrifices behind the network average. The 30s/10% threshold is a preselected research policy guardrail, not an empirically estimated user preference.
5. **Exceptions:** report numeric collisions, emergency stops and braking when structured SUMO files contain these attributes; missing must be labeled unavailable rather than zero. Material exceptions prevent an unqualified GO.
6. **Distribution:** report p95/p99 trip-time tails, individual difference quantiles, waiting/time-loss, route-change classification, and unchanged-route-driver spillovers. Stratify origin–destination locations only at a defensible **predefined aggregated geographic level**; do not rank singleton exact-OD cohorts as statistically robust.

**Joint decision rule (200s only):**
- **GO versus this specific A baseline:** primary 95% CI entirely positive, 100% completion in both arms, p90 criterion passes, harmed share <=50%, severe-harm share <=10%, and no material structured exception disadvantage.
- **MEAN BENEFIT / FAIRNESS NO-GO:** primary CI entirely positive but one or more fairness/completion/exception safeguards fail. This must not be characterized as a successful cooperative policy.
- **NO-GO on primary efficiency:** primary CI entirely negative (E demonstrably slower), regardless of other endpoints.
- **INCONCLUSIVE:** primary CI overlaps zero, or essential outcome identification fails. Prespecified mean/fairness status will still be reported.
- No post-hoc changes to thresholds, outcomes, seeds, network scale, participation rates, or policy definitions.

Secondary windows are scientifically informative sensitivity analyses; they **cannot reverse** the 200s primary decision.

## 5. Scientific interpretation boundaries

An E>A outcome would be a first matched-fresh-demand demonstration of cooperative-routing improvement against the **frozen nominal free-flow independent baseline**, under full advance announcement, 100% algorithmic assignment and synthetic SUMO dynamics. It would not show superiority to dynamic traffic-aware navigation, mixed participation, compliance/consent, departure-time shifts, alternative road topology, high-volume scaling or real-world safety. A negative result must be preserved as such, without adjusting the intervention to rescue it.

## 6. End-to-end implementation and execution plan (authorized)

**Step 1 — Freeze this protocol in GitHub** before fresh-seed outcomes; reserve seeds 3501–3510 and record a traceable doc commit. No intermediate scientific approval required.

**Step 2 — Implement a narrow Experiment 006 runner**, reusing the unchanged original A generator and frozen E generator rather than rewriting or optimizing either routing algorithm. Generate each demand once per seed/window, and run two arms with the **same network/demand bytes**. Write `attempt.json`, demand hash, arm route/audit hashes, SUMO logs, tripinfo, collision/statistics and policy provenance. Preserve failed attempts without replacing seeds.

**Step 3 — Development-only parity preflight** on previously inspected seed 2101 under all three regimes, comparing proposed A route XML/audit byte-for-byte to the original A generator, and E route XML/audit byte-for-byte to the existing Experiment 005 E generator. Check matched demand IDs and that A/E differ only in routing policy, not simulation configuration. Fix only implementation/packaging defects; do not revise the experimental hypothesis based on the fresh outcomes.

**Step 4 — Frozen evaluation code**: construct independent-seed paired A−E contrasts, 95% Student-t intervals, per-driver helped/harmed, severe-delay share >30s, tail p90/p95/p99, waiting/time loss, unchanged-route spillovers and structured collision/exception summaries. Strictly validate matched IDs, complete pair count and the seed manifest before a GO decision.

**Step 5 — GitHub Actions implementation:** push a dedicated read-only-development-preflight workflow on the PR. The 30 matched fresh pairs must be **blocked for PR events** and enabled **only on the approved merge to main** after all parity checks. Pin the SUMO container; use GitHub Actions artifacts for the 30 paired inputs/outputs and an aggregated JSON/CSV results artifact. Provide a direct execution URL and a status ledger distinguishing queued, running, failed and completed.

**Step 6 — Execute exactly 30 paired jobs (60 arms)**, with full artifact preservation and no scenario replacements. If a job fails for an environmental or implementation reason, investigate logs and retry only the identical prespecified scenario under unchanged scientific methods; do not summarize incomplete cohorts as successful.

**Step 7 — Audit and publish**: verify the consolidated output and numerical exception evidence, interpret all outcomes against the *frozen* joint criteria, publish the final scientific report and permanent seed-level table under `docs/`, merge to `main`. Include direct links to immutable run artifacts and document their retention. Preserve Experiment 004 D NO-GO and Experiment 005 E-versus-D GO, regardless of A/E result.

**No broad engineering-readiness program and no unrelated vehicle-volume, grid-size, or departure-scheduling study.** One protocol, one bounded causal/efficacy comparison, one results report.
