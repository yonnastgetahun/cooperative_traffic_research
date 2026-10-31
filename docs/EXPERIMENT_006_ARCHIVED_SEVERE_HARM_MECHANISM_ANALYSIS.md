# Experiment 006 — Archived severe-delay mechanism investigation

**Date:** 2026-10-31. **Status:** Completed exploratory **read-only** decomposition of the original Experiment 006 A-versus-E simulation evidence. **No new SUMO simulation, calibration retuning, route modification or revised experiment criteria.**  
**Frozen scientific decision unchanged:** Experiment 006's high-congestion network-mean result A−E was **+0.2429s** (95% seed-level CI **[−1.9120,+2.3978]s**, inconclusive). The predeclared fairness criterion **failed**: 27.98% of drivers under E were more than 30s slower than under independent A, versus a maximum acceptable 10%. See [original scientific report](EXPERIMENT_006_FINAL_SCIENTIFIC_REPORT.md).

## 1. Evidence and integrity

- Original completed [GitHub Actions run 41185989951](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41185989951), original [30 paired A/E scenario artifacts](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41185989951), and [consolidated original report artifact 13036878652](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41185989951/artifacts/13036878652).
- Downloaded **all 30 of the original paired ZIPs**: ten fixed seeds `3501–3510` × three departure windows `200/600/1200s`, each containing the original A/E route XML, routing audits, demand, network, SUMO tripinfo and simulator statistics. Parsed **30,000 matched vehicle ID pairs** (10,000 per window). Verified all pair manifests COMPLETE, matched 1,000 A and E vehicle/demand IDs per seed-window, 1,000 completed trips per arm, exact origin/destination and scheduled departure identities, and duplicated no IDs.
- Reproduced the frozen severe-harm count from original tripinfo: **2,798/10,000** at 200s, **738/10,000** at 600s, **93/10,000** at 1200s. The corresponding original A/E changed-route totals were **5,703/5,757/5,193**. In each regime and every original seed, the E routing audit recorded `accepted=1` for **all 1,000 candidates**.
- Computed nominal route distance/time by summing the original network's external-edge lane lengths and lane free-flow speeds. Joined per-driver observed `duration`, `waitingTime`, `timeLoss`, `departDelay`, route paths and original routing-audit guardrail decisions. No per-edge realized queue/FCD trajectories were present in the downloaded original scenario archives.
- Geographic cohorts below are **synthetic grid quadrants**, not neighborhoods or real-world locations. Each origin/destination edge was assigned a quadrant by its midpoint relative to the grid's `x=900m`, `y=900m` center. Spatial groupings, threshold comparisons and subgroup intervals in this report are **exploratory post-outcome analyses**, not pre-registered confirmatory findings. Keep **ten independent demand seeds** as the inferential units.

## 2. Primary observation: severe delay comes with traffic waiting, not nominal route length

The **2,798 high-congestion severely harmed vehicle identities** had a mean E−A completed-trip-duration increase of **+72.470s**, composed arithmetically of mean reported `waitingTime` increase **+57.169s (78.9% of the mean duration difference)** and mean residual duration difference **+15.301s (21.1%)**. `timeLoss` increased **+71.915s** on average; this separately measures time lost against SUMO's reference movement, not an additional component to add to waiting time. Mean `departDelay` difference was only **+0.031s**, so increased scheduled-departure delay does not explain the severe effect.

**Cautions:** `tripinfo.waitingTime` is a SUMO aggregate for stopped/near-stopped time, not an identified physical bottleneck or all possible slow-moving queue delay. The difference in waiting is an **association among drivers selected because they were harmed**, not a randomized mediator estimate or proof that waiting alone caused the policy contrast.

Among these 2,798 affected identities:
- **2,792 (99.79%)** had **exactly equivalent reconstructed nominal free-flow route duration and distance**, even though some had different actual road sequences; only six had a positive nominal difference.
- **2,485 (88.81%)** had additional recorded waiting exceeding half their own additional completed-trip duration.
- **1,493 (53.36%)** suffered **more than 60 additional seconds**; **301 (10.76%)** suffered **more than 120 additional seconds**.
- Mean completed duration was **203.46s under A vs 275.93s under E**, while mean SUMO waiting was **35.74s under A vs 92.91s under E** for this *selected* harmed cohort.
- The severe-harm fraction among 10,000 high-congestion matches was **27.98%** (range **24.4%–30.3%** across ten seeds; descriptive seed-level mean 95% CI **[26.62%,29.34%]**).

**Interpretation:** The dominant observable difference is traffic interaction and stopped-time exposure, **not a longer nominal path**, departure scheduling, or an inability of trips to complete. Actual road-level sources of those delays remain unresolved.

## 3. Route switching raises risk, but unchanged-route harm demonstrates network spillovers

| High congestion (200s) | Route changed between A/E | Exactly same road-edge sequence |
|---|---:|---:|
| Matched drivers | 5,703 | 4,297 |
| Severely harmed (>30s slower under E) | **1,916** | **882** |
| Severe-harm incidence | **33.60%** | **20.53%** |
| Mean extra duration among severely harmed | +74.97s | +67.04s |
| Mean extra waiting among severely harmed | +58.48s | +54.33s |

The **13.04 percentage point** changed-versus-unchanged severe-risk difference appeared in the same direction in **all ten seeds** (descriptive seed-level 95% CI **[10.80,15.28] percentage points**). But **31.52% of all 2,798 severe-harm cases** had **no route change**. Among 1,916 severely harmed changed-route vehicles, **1,910** still had identical nominal free-flow duration/distance compared with A.

Route-change membership is **post-treatment** (which route the policy selected), and other vehicle route assignments simultaneously differ. These comparisons **cannot isolate causal effects of switching a given driver**. They are nonetheless consistent with network-mediated traffic displacement: unchanged-route vehicle journeys became slower under the altered aggregate route assignment.

## 4. The nominal detour guardrail never activated

The original E `routing/audit.csv` showed **zero rejected candidates out of all 30,000 assignments across 30 pairs** (10,000/10,000 accepted at each window). In high congestion, 98.10% of **all** 10,000 matched routes had reconstructed equal nominal free-flow distance and time, including **2,792 of 2,798** severe-harm cases. Only 190 of all changed high-congestion routes had a small positive nominal free-flow difference, and just six of those were severely harmed.

The frozen guardrail checks candidate **free-flow** duration/distance against the free-flow baseline, **not realized queue-mediated travel time or individual future harm**. It was neither designed nor triggered to cap the later measured >30s E−A delay. Zero rejection does not prove a guardrail implementation defect; it proves the existing nominal guardrail **did not distinguish the harm mode observed in these simulations**.

## 5. Congestion regime, baseline trip length, and departure phase

| Departure window (same 1,000 cars, differently timed) | Severe E−A >30s | Mean extra E−A duration among affected | Mean extra waiting among affected |
|---|---:|---:|---:|
| **200s high** | **2,798/10,000 = 27.98%** | +72.47s | +57.17s |
| **600s moderate** | **738/10,000 = 7.38%** | +47.44s | +35.79s |
| **1200s lower** | **93/10,000 = 0.93%** | +38.75s | +26.96s |

In the 200s cohort, severe-harm rates were **22.10%** for baseline nominal trips under 90s (n=3,064), **28.19%** for 90–150s (n=5,271), and **38.14%** for those over 150s (n=1,665). Grouping scheduled departures into five equal-duration intervals gave severe-harm rates of **22.2%, 30.05%, 29.1%, 30.55%, 28.0%**, respectively. The highest incidence was not confined to the final departure period. These are descriptive associations; longer routes have greater exposure opportunity to queues.

The original experiments manipulate **departure-window congestion pressure**, not vehicle count or grid size. Do not describe this as a test of scaling or network size.

## 6. Geographic concentration of harm on the synthetic grid (exploratory)

Endpoint quadrant classification uses original network edge midpoints at x/y halves of the 0–1800m grid. At high congestion:

| Destination quadrant | Matched drivers | Severe E−A >30s | Severe fraction |
|---|---:|---:|---:|
| Northeast (NE) | 2,657 | 948 | **35.68%** |
| Southeast (SE) | 2,570 | 841 | **32.72%** |
| Northwest (NW) | 2,569 | 580 | **22.58%** |
| Southwest (SW) | 2,204 | 429 | **19.46%** |

The NE-minus-SW destination severe-incidence difference was positive in **all ten seeds**; seed-level mean risk difference **16.28 percentage points**, exploratory CI **[13.65,18.91] percentage points**. Among 16 origin-to-destination quadrant combinations, **SW→NE** had **258/584 = 44.18%** severe harm versus **SW→SW** with **60/497 = 12.07%**. This provides a *spatially specific investigative hypothesis*, not a claim that a particular junction, movement direction, or bottleneck was causally responsible. Multiple exploratory subgroup comparisons were made without multiplicity control.

**A descriptive check against simple trip-length or route-switch composition:** the destination NE versus SW severe-harm gradient persists within shorter nominal trip strata (for A routes under 90s: NE **257/824=31.2%** vs SW **96/672=14.3%**) and medium nominal trip strata (90–150s: NE **521/1430=36.4%** vs SW **196/1145=17.1%**). It also appears among drivers whose routes did *not* change (NE **274/1086=25.2%** vs SW **140/1015=13.8%**) and drivers whose routes *did* change (NE **674/1571=42.9%** vs SW **289/1189=24.3%**). These are **stratified descriptive rates**, not covariate-adjusted randomized effects; they strengthen the case for investigating destination-specific traffic interactions while leaving the cause open.

## 7. Route-assignment concentration proxy (not measured physical congestion)

Along each driver's E-selected route, counts of vehicles assigned to its edges were compared between E and A using static final route assignments. Among high-congestion severely harmed drivers, the mean **E−A assigned-count difference averaged over the E route's edges** was **+1.148 vehicles per edge**; for drivers not severely harmed it was **−0.521**. The severe-minus-not-severe contrast was positive for all ten seeds, exploratory seed-level mean difference **+1.665 assigned vehicles/edge** (95% CI **[+1.212,+2.117]**).

This is consistent with uneven demand redistribution into roads more exposed to severe harm, particularly alongside the stronger NE/SE destination association. But final static route counts **cannot identify edge-time coincident flow, physical occupancy, junction delays, or the causal mediating road bottleneck**. Assignment concentration could be a symptom rather than a cause.

## 8. Current hypothesis-evidence matrix

| Candidate explanation | Evidence from archives | Scientific status |
|---|---|---|
| **Longer nominal detours** | 99.79% of high-congestion severe harms on identical nominal free-flow time/distance | **Strongly disfavored** as main explanation |
| **Departure delays** | Average A/E departure-delay shift among severely harmed only +0.031s | **Strongly disfavored** |
| **Traffic queue/stopped-time exposure** | +57.17s additional SUMO waiting among +72.47s harmed duration; frequent unchanged-route harm | **Strong descriptive support**; actual edge/junction causes not identified |
| **Congestion displacement/spillover** | 882 same-route severe cases, assignment-count exposure differences, geography gradients | **Supported observationally**; route selection, exposure and physical congestion not separately randomized |
| **Specific spatial/directional bottlenecks** | NE/SE destination severe-risk elevation, SW→NE high-risk OD group | **Exploratory location hypothesis** only, no edge-time trajectories |
| **Nominal detour/guardrail inadequacy** | All 30,000 candidate guardrails accepted, 27.98% high-congestion realized severe harm | **Directly demonstrated gap** between nominal restrictions and realized fairness goals |
| **Counterfactual route-ranking accuracy / social-optimality** | Candidate labels/rejected alternatives and realized alternative-route outcomes not archived | **Unresolved** |

## 9. Scientific synthesis and bounded next step

**Conclusion:** The Experiment 006 severe-harm mechanism is most accurately described as **queue-associated, spatially patterned congestion redistribution, amplified among route-switched drivers but also affecting unchanged-route drivers**, while the nominal detour safeguards provide no realized-delay protection. These are supported observations, **not a fully identified causal bottleneck**. The research has moved beyond “perhaps routes were simply longer.”

**Next highest-information study from existing evidence:** Deepen spatial-temporal interpretation of the high-harm OD cohorts using the current original tripinfo waiting/timeLoss and final route assignments, while recognizing that archived road-level *time-resolved* occupancy and wait trajectories are unavailable. A future **single discriminating experiment** would require prospective road-edge time-bin instrumentation and one narrowly defined fairness-aware routing intervention to test whether predicted *realized harm* can be bounded. **No such intervention has been defined, authorized or executed in this analysis**. Keep vehicle volume, grid size/topology, participation rates, and departure-time coordination distinct future axes. Do not retune E or rerun completed work.

## Reproducibility and data preservation

- All original seed/window ZIPs are listed in the [GitHub Actions run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41185989951) and are subject to limited retention.
- [Permanent derived per-seed analysis](results/exp006_severe_harm_per_seed.csv) and [input SHA-256 archive manifest](results/exp006_harm_archives_sha256.csv) are committed alongside this report.
- Definitions: harm `duration_E-duration_A > 30s` (strict), `changed_route` iff A/E route edge sequences differ; nominal route free-flow time = sum external lane `length/speed`; grid quadrants = origin/destination edge midpoint split at x=900m and y=900m; SUMO waiting from original `tripinfo.waitingTime`; edge load proxy = count of original assigned routes containing each edge, with E route as the averaging path.
- Inferential samples are the ten independent demand seeds; vehicle identities support matching, **not** extra independent experimental units. Analysis was retrospective after observing Experiment 006 outcomes; reported subgroup intervals are descriptive, unadjusted for multiplicity.

**Preserve Experiment 006 primary INCONCLUSIVE and joint network efficiency/fairness NO-GO. No experimental outcome has been changed.**
