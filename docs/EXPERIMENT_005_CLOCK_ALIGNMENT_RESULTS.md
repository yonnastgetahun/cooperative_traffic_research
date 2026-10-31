# Experiment 005 — Clock-alignment causal test: final scientific results

**Executed:** October 30, 2026 (GitHub Actions UTC October 31).  
**Decision: GO for the prespecified clock-aligned occupancy-update intervention E relative to the original calibrated policy D, under high congestion.** This is **not** a GO for cooperative routing relative to independent routing, and does not overturn Experiment 004's historical policy-D NO-GO.

## Frozen protocol and execution

- [Prespecified Experiment 005 scientific protocol](POST_EXP004_CLOCK_ALIGNMENT_EXPERIMENT_DESIGN.md) was committed **before** fresh-seed simulation.
- [PR #24](https://github.com/yonnastgetahun/cooperative_traffic_research/pull/24), merged as commit `9aa0f326cb48ab8bebf1d849c1d21a5c1242474e`.
- [Successful GitHub Actions run 41172516513](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41172516513): 3/3 development-only parity checks, 30/30 fresh matched-seed scenario pairs, 60/60 SUMO arm runs, consolidated evaluator all successful.
- [Consolidated results artifact 13031374224](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41172516513/artifacts/13031374224) contains `exp005-clock-alignment-results.json` (all seed summaries, subgroups and prespecified decisions).
- 30 original paired scenario ZIP artifacts are independently stored by the same workflow, one per seed/window, preserving both D/E routes, original demands, SUMO tripinfo, collision and statistics XML, and attempted-stage logs. Artifacts have 30-day retention; this document preserves the principal numerical findings after their eventual expiry.
- Frozen 10×10 SUMO grid, 1,000 seeded vehicles in each arm; 10 fresh seeds 3401–3410 per regime, departure windows 200s (primary), 600s and 1200s (secondary).
- **D** kept original Exp004 stateful calibrated search plus **free-flow-clock** post-assignment occupancy updates. **E** changed **only** the occupancy-update bins: chosen-route edge entries were prospectively replayed with calibrated candidate cost/clock bins against pre-assignment occupancy, then incremented after the entire chosen route was evaluated. Fallback chosen routes were treated identically. No future SUMO observations were used for route choices.
- On inspected development seed 2101, the new D control's route XML and routing audit were byte-for-byte identical to the unchanged Experiment 004 D source for **all three regimes**; fresh seeds were withheld until all parity checks passed.

## Primary result — high congestion (200s)

The prespecified primary quantity is **mean completed-trip duration under D minus E**, averaged across independent seed-level paired differences. Positive is a benefit for aligned E.

| Outcome | Original calibrated D | Clock-aligned E | D minus E |
|---|---:|---:|---:|
| Mean completed-trip duration | **231.9206s** | **211.7889s** | **+20.1317s** |
| Mean of seed-level 90th-percentile durations | 388.8s | 338.7s | **+50.1s** |
| Completed trips | 10,000 / 10,000 | 10,000 / 10,000 | No difference |

- **95% paired seed-level Student-t interval for mean D − E:** **+16.7378 to +23.5256 seconds** (n=10 independent seeds, df=9). At the measured 231.92-second D baseline, this is approximately an **8.7% reduction** in average trip time.
- **95% interval for mean seed-level p90 D − E:** **+44.463 to +55.737 seconds**; E lowered the high-congestion upper tail.
- Of 10,000 matched drivers, **5,740 (57.40%) had shorter trips in E, 3,914 (39.14%) had longer trips, 346 (3.46%) were unchanged**. Thus the prespecified no-majority-harmed driver gate passes.
- Every trip in all 30 seed-window D/E pairs completed. There is no incomplete-trip censoring of mean durations.

**Frozen decision gates:** the primary high-congestion 95% CI is entirely above zero; completion was equal; mean seed-level p90 E−D was **−50.1s**, well below the prespecified +5s maximum; only **39.14%** were harmed. **All four criteria passed.**

## All three regimes — paired seed-level inference

| Departure window | Mean duration D (s) | Mean duration E (s) | D − E mean (s) | 95% CI for D − E (s) | P90 D − E (s) |
|---|---:|---:|---:|---|---:|
| **200s (primary)** | 231.9206 | 211.7889 | **+20.1317** | **[+16.7378, +23.5256]** | +50.1 |
| 600s | 152.8898 | 151.1770 | **+1.7128** | [+0.7107, +2.7149] | +2.5 |
| 1200s | 141.2020 | 141.0361 | **+0.1659** | [−0.0431, +0.3749] | +0.5 |

A secondary duration advantage is supported at moderate congestion. The lower-congestion duration effect is inconclusive. This pattern is qualitatively consistent with a more consequential clock/occupancy interaction at higher traffic pressure, but no network scale or threshold effect was experimentally identified.

## Network assignment and matched-driver spillovers

| Regime | Route differences D/E across 10,000 matched vehicles | Assigned-edge-load Gini D − E (95% CI) | Top-decile assigned-edge share D − E |
|---|---:|---|---:|
| 200s | 6,610 | **+0.04664** [+0.04349, +0.04979] | +2.459 percentage points |
| 600s | 6,344 | **+0.01504** [+0.01372, +0.01636] | +0.783 percentage points |
| 1200s | 5,748 | **+0.00646** [+0.00372, +0.00921] | +0.470 percentage points |

Positive D−E Gini/share means E redistributed *assigned routes* less unevenly than D. These are static assigned-edge demand proxies; they are **not measured physical occupancy, queue length or edge-level realized delay**. The causal treatment is the update-clock rule; the fact that route concentration and mean time change together does not mathematically prove concentration mediated all of the travel-time benefit.

**High-congestion subgroups (mean of ten seed-level subgroup means):**

| Vehicle group | Matched vehicles | Mean D − E trip duration | 95% seed-level CI | Mean D − E waiting |
|---|---:|---:|---|---:|
| Routes changed between D/E | 6,610 | **+26.8551s** | [+22.8298, +30.8805] | +18.8448s |
| Exactly unchanged edge-sequence routes | 3,390 | **+7.0777s** | [+4.1104, +10.0449] | +5.5754s |

Network-mediated spillovers are consistent with unchanged-route vehicles benefiting, in addition to routed vehicles. This remains an inference about network interaction rather than identified individual bottleneck causation. Across all high-congestion drivers, D−E waiting time was +14.3337s (95% interval [+11.8071,+16.8603]s).

## Structured exception and collision audit — read-only original archives

After the successful experiment, all **30 original paired scenario ZIPs** were downloaded and read. For each of the **60** D/E arm outputs, the archived `statistics.xml` contains the numerical fields `safety.collisions`, `safety.emergencyStops`, and `safety.emergencyBraking`, all equal to **zero**. The corresponding `collisions.xml` files also contain zero structured collision events. These fields are present, not imputed, for all 10 seeds × 3 windows × 2 arms; all 60 tripinfo files contained 1,000 completed trips. This establishes **only the recorded structured SUMO event results** under these scenarios; it is not a real-road or autonomous-vehicle safety conclusion.

## Seed-level paired evidence (rounded for display)

**Every entry is D minus E**; positive trip-time/p90 implies E improved. Gini is the difference in assignment concentration (D−E). Exact unrounded seed values remain in the frozen results artifact linked above.

| Window | Seed | Trip-time D−E (s) | P90 D−E (s) | Changed routes | Gini D−E |
|---|---:|---:|---:|---:|---:|
| 200 | 3401 | 31.06 | 61 | 671 | 0.0545 |
| 200 | 3402 | 16.16 | 42 | 654 | 0.0477 |
| 200 | 3403 | 19.17 | 45 | 656 | 0.0517 |
| 200 | 3404 | 18.89 | 51 | 660 | 0.0433 |
| 200 | 3405 | 16.30 | 42 | 667 | 0.0405 |
| 200 | 3406 | 13.90 | 43 | 655 | 0.0489 |
| 200 | 3407 | 22.14 | 63 | 654 | 0.0442 |
| 200 | 3408 | 20.22 | 51 | 686 | 0.0422 |
| 200 | 3409 | 20.73 | 57 | 646 | 0.0485 |
| 200 | 3410 | 22.76 | 46 | 661 | 0.0450 |
| 600 | 3401 | 2.32 | 3 | 646 | 0.0159 |
| 600 | 3402 | 2.70 | 6 | 657 | 0.0121 |
| 600 | 3403 | 1.09 | 3 | 627 | 0.0175 |
| 600 | 3404 | -0.66 | -1 | 635 | 0.0158 |
| 600 | 3405 | 3.51 | 12 | 644 | 0.0148 |
| 600 | 3406 | 0.99 | 1 | 650 | 0.0135 |
| 600 | 3407 | 0.20 | 0 | 617 | 0.0171 |
| 600 | 3408 | 1.85 | 1 | 643 | 0.0136 |
| 600 | 3409 | 1.39 | -3 | 606 | 0.0167 |
| 600 | 3410 | 3.73 | 3 | 619 | 0.0133 |
| 1200 | 3401 | 0.55 | 1 | 581 | 0.0098 |
| 1200 | 3402 | -0.34 | -1 | 552 | -0.0009 |
| 1200 | 3403 | 0.51 | 2 | 548 | 0.0104 |
| 1200 | 3404 | 0.00 | 1 | 593 | 0.0057 |
| 1200 | 3405 | 0.42 | 0 | 595 | 0.0063 |
| 1200 | 3406 | 0.08 | 0 | 587 | 0.0072 |
| 1200 | 3407 | -0.14 | 1 | 568 | 0.0047 |
| 1200 | 3408 | 0.03 | -1 | 617 | 0.0031 |
| 1200 | 3409 | 0.19 | 2 | 543 | 0.0125 |
| 1200 | 3410 | 0.35 | 0 | 564 | 0.0059 |

## Scientific interpretation and scope

The intervention was limited to the predeclared **post-assignment occupancy time-bin update**; the original D path search, calibration coefficients, demand, guardrails and SUMO configuration were held fixed. Because each pair used identical frozen demand and source environment, this supports a **causal improvement for this defined clock-alignment intervention within the synthetic simulation**, not merely an observational correlation. It provides evidence that the assignment-clock inconsistency was a consequential contributor to D's poor outcomes.

However, this experiment does **not** establish that:
- Clock mismatch was the **only** mechanism behind Experiment 004's negative result.
- Counterfactual candidate-route prediction/ranking accuracy is validated.
- The aligned policy E beats **independent routing A**. Experiment 005 did not include A on these fresh seeds. Do **not** compare E directly with A from different seed cohorts as if that were a paired causal contrast.
- Physical edge congestion or junction-specific dynamics have been measured here; the route-load concentration statistic is an assigned-demand proxy.
- Voluntary participation, departure scheduling, network scale/topology sensitivity, or real-world autonomous fleets have been tested.

**Next scientific question (not executed here):** Does the now clock-aligned policy E outperform a credible independent routing baseline on matched fresh seeds while preserving the fair-driver/upper-tail outcomes? That would test whether fixing this mechanism turns a harmful cooperative policy into a genuinely **beneficial cooperative alternative**, rather than merely removing most of the demonstrated harm relative to D.

**Decision: GO for clock-aligned E relative to D only; preserve the original Experiment 004 policy-D NO-GO and the broader cooperative-traffic hypothesis as unresolved.**
