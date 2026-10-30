# Post-Experiment 004 archived evidence inventory (initial read-only examination)

**Date:** 2026-10-30  
**Status:** Archive inventory and exploratory inspection, not a newly executed simulation or confirmed causal mechanism.  
**Scientific baseline:** [Frozen four-arm design](EXPERIMENT_004_FOUR_ARM_FROZEN_DESIGN_V01.md), [fresh-seed manifest](EXPERIMENT_004_FRESH_SEED_MANIFEST_V01.md), [final report](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md), and [approved mechanism plan](POST_EXP004_MECHANISM_RESEARCH_PLAN.md).

## Provenance and coverage

- **Source run:** [41023721390](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41023721390), 10 fixed seeds (3301–3310), three departure windows (200/600/1200 s), four arms (A/B/C/D), 120 seed-window-arm combinations, 1,000 vehicles per combination.
- **GitHub Actions artifact registry inspected 2026-10-30:** 121 total artifacts across two pages (100 + 21), including 120 uniquely named `exp004-seed-{seed}-window-{window}-arm-{arm}` scenario archives and one additional artifact. None were marked expired. The current artifact metadata lists expiry on **2026-11-29**; retain derived findings in the repo before archive access lapses.
- **Existing read-only reanalysis:** [run 41098364737](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41098364737) and artifact [12996134768](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41098364737/artifacts/12996134768), downloaded and inspected in this investigation.
- **The audit ZIP has exactly two files:** `exp004-archived-outcome-audit.json` (120 scenario records, 3 regime-level route-change series) and `exp004-fairness-exceptions.json` (120 scenario exception summaries, 90 matched contrasts for C-D/A-D/B-D, regime summaries, per-seed exact-OD descriptive records).
- **Six raw scenario archives opened** (three paired C/D examples, one per regime): seed 3308/200s (artifact IDs 12963195432, 12963076633); seed 3301/600s (12963165256, 12962628472); seed 3303/1200s (12963051057, 12962658300). **These are illustrations, not a random or representative scientific sample**; the full 120-arm evidence is currently represented by the prior audit summaries, not a fresh read of every raw ZIP.

## Evidence content and analytical limits

| Evidence class | What was verified | Scientific usability |
|---|---|---|
| Frozen control and implementation | Four-arm design, frozen seed manifest, source for `four_arm_routes_v01.py`, `prospective_search_adapter_v01.py`, `time_aware.py` and audit scripts | Source-level decision mechanics; causal arm interpretation C versus D |
| Scenario pairing and provenance | All 120 scenario records; 100% completed trips and ten seed-paired comparisons per regime; the six inspected C/D sample pairs have identical `trips.xml` bytes | Outcome differences and route differences can be paired on demand seed and vehicle ID |
| Route outcomes | Original audit includes 120 routing-map based scenario records, seedwise C/D route-switch counts; raw ZIP examples include `routing/routes.rou.xml`, `routing/audit.csv` and `routing/manifest.json` | Full archived C/D route-switch and route-length/overlap decomposition is possible, but requires reading 60 C/D raw archives |
| Trip durations and waiting | Raw sample `tripinfo.xml` has matched completed-trip durations and `waitingTime`; original audit has means and p90 for all 120 | Seed-aware matched-vehicle analyses and distinguishing direct reroute vs unchanged-route spillover |
| Demand and OD | Raw samples have `trips.xml`; final fairness file has exact-OD cohorts in 90 contrasts | Exact OD cohorts are almost all singleton within each seed; must aggregate into prespecified broader spatial/demand groups before interpretable cohort-level inference |
| SUMO safety | Audit JSON has `safety.collisions`, `safety.emergencyBraking`, `safety.emergencyStops` for all 120 scenarios; collision file and `statistics.xml` present in six raw samples | Descriptive audit: all 120 report numeric string `"0"` for each of these three fields; not evidence of real-road safety |
| Network observations | Six raw ZIPs contain `network.net.xml`, `sumo.log`, `statistics.xml`, `tripinfo.xml`, but **no saved edge-time detector data, FCD/trajectory file, or actual per-edge time series** | Route-assignment counts can be reconstructed as a proxy; actual edge-time congestion displacement cannot be directly verified from these sampled raw archives |
| Decision-time counterfactuals | Raw route audit has one final `candidate_predicted_cost` and route eligibility summary per vehicle, **not the rejected candidate labels, per-bin occupancy reads, or alternative-route realized outcomes** | Candidate-route forecast accuracy and exact search-rank reversals are **not identifiable** from these saved samples; source inspection can identify structural mismatch, not its realized frequency |
| Temporal occupancy | Routing code emits free-flow-clock post-assignment occupancy updates; D searches with calibrated forecast-clock bins | Source-level inconsistency is demonstrable. Its quantitative effect is not established without decision-time trace/controlled comparison |

## New descriptive evidence from the already archived 120-arm audit

**Route differences C/D**, summed over 10 seeds and 10,000 matched vehicles per regime:

| Window | C/D different routes | Fraction |
|---|---:|---:|
| 200s | 6,653 | 66.53% |
| 600s | 5,707 | 57.07% |
| 1200s | 4,395 | 43.95% |

**Safety-field gap partially closed:** `safety.emergencyBraking`, `safety.emergencyStops` and `safety.collisions` are present and equal `"0"` in **all 120** records in `exp004-archived-outcome-audit.json`. The [final scientific report](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md) correctly left emergency rates unaggregated **at publication time**; that descriptive gap can now be updated using its own archived evidence. Do not infer anything about real-world safety or unavailable warning classes.

**Exact OD-cohort granularity is inadequate within seeds:** For each regime, 10 C-minus-D seed contrasts contain **9,965 exact OD cohort entries, of which 9,930 have n=1 and 35 have n=2**; no within-seed exact OD cohort has n>=5. This is not evidence that location-dependent harms are absent. It implies that a useful OD fairness question requires coarser, prespecified spatial grouping, with seed-level uncertainty preserved.

## Scientific boundaries and conflicts in project history

- The [older departure-scheduling roadmap](EXPERIMENT_003_DEPARTURE_SCHEDULING_ROADMAP.md) called departure coordination a proposed 'Experiment 003'. The **completed** Experiment 003 is now the independently validated cumulative timing calibration. Departure scheduling remains a deferred, untested design concept; avoid mislabeling it as completed or adding it to the present experiment.
- The repository README contains chronological status passages claiming M3 held-out execution was still pending. Later [Exp003](EXPERIMENT_003_CONFIRMATORY_RESULTS.md) and [Exp004](EXPERIMENT_004_FINAL_SCIENTIFIC_REPORT.md) verified findings supersede those historical snapshot statements.
- Proposed 0/5/10/25/50% voluntary participation, compliance, nonparticipant spillovers, detour fairness and generalized door-to-door time remain **historical research questions**, not measured effects of Experiment 004.
- No experiment should be rerun to answer a question already accessible in the archives.

## Immediate next deliverable

Produce **one seed-paired C/D route-change and spillover decomposition across all 10 seeds in each of the three windows**, reusing 60 raw C/D archived route and tripinfo files. Partition vehicles into changed versus unchanged routes, quantify signed/absolute free-flow and distance changes, realized duration and waiting-time shifts, and use **independent seed** as the unit for interval estimates. Follow this with a short evidence matrix assessing whether route reassignment and unchanged-driver spillovers account for the observed high-congestion harm. Do **not** claim to recover absent candidate-search or physical edge-time trajectories, and do not launch any new SUMO simulations.
