# Experiment 002 — Physical occupancy and junction diagnostics: M0–M2 development results

**Research date:** October 26, 2026 (Pacific)  
**Status:** M0 implementation and M1/M2 *development* execution completed successfully. **Physical occupancy comparability is not yet fully validated; held-out evaluation remains blocked.**  
**Authoritative execution:** [M0–M1 final measurement smoke, run 40445882827](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40445882827) · [M2 nine-scenario development matrix and aggregate, run 40446073958](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958)  
**Protocol:** [Measurement Plan v0.1](EXPERIMENT_002_OCCUPANCY_JUNCTION_MEASUREMENT_PLAN_V0_1.md) · [Predictor Validation Plan v0.2](EXPERIMENT_002_PREDICTOR_VALIDATION_PLAN.md)  
**Per-seed measurements:** [M2 3×3 CSV](EXPERIMENT_002_OCCUPANCY_M2_PER_SEED.csv)

## 1. What was executed

- **M0:** Implemented `measurement_v01.py`, `measurement_sensitivity_v01.py`, `fixed_demand_v01.py`, a non-policy-changing reusable scenario runner, and **12 passing pure-Python contract fixtures**. Fixtures cover bin boundaries, internal lanes, stopped time, repeated edges (including consecutive visits after a junction), route mismatch, missing samples, native empty-road records, and overcoverage.
- **M1:** All three congestion windows (200, 600, 1,200 seconds) ran on previously used **development seed 2001**, each with 1,000 completed trips. Original and instrumented route XML and audit CSVs were byte-identical. **100% of planned route segments matched**, with internal-junction samples, external stopped-vehicle samples, native SUMO edgeData, partial-bin flags and source hashes archived.
- **M2:** All **nine prespecified development scenarios** completed: seeds **2101, 2102, 2103** × windows **200/600/1,200 seconds**, **1,000 completed trips each** (9,000 trip completions across runs). **100% vehicle-route and ordered external-edge coverage** in all nine. The aggregate job verified that, for each seed, origin–destination assignments were exactly the same across its three windows.
- Every scenario ran the **unmodified `time_aware.py` policy**; original and traced routes/audits were compared byte-for-byte. We did **not** tune congestion pressure, detour thresholds, junction cost, routes or demand.
- The calibration run used one immutable SUMO image reference across all nine jobs: `ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb`. Reported SUMO version is **1.28.0**. Git SHA, route hashes, seed/window, network and demand manifests are retained in each artifact.
- **Evaluation seeds 3101–3110 were not run or inspected.**

## 2. Forecast accuracy: repeated improvement, persistent underprediction

All errors below compare the original time-aware cost **replayed along chosen routes** with a free-flow timing reference on those **same chosen routes**, using the first one-second FCD external-lane sample as an approximate observed edge-entry time. These are *not* matched independent-routing policy experiments.

| Departure window | Time-aware entry MAE (s, mean ± sample SD of 3 seeds) | Free-flow entry MAE (s, mean) | Time-aware entry bias (observed − forecast, s, mean) |
|---|---:|---:|---:|
| **200s · high load** | **54.45 ± 4.55** | 59.93 | **+54.38** |
| **600s · moderate load** | **19.38 ± 1.51** | 23.35 | **+19.27** |
| **1,200s · low load** | **13.61 ± 0.44** | 17.13 | **+13.45** |

The cost replay reduces forecast error relative to free flow across these **three development seeds**, yet underpredicts road-entry times substantially. Nearly all mean error in the high-load regime is in the *late-arrival direction*. The small three-seed sample SD is descriptive only; neither it nor the 9,000 dependent trip observations establishes statistical significance or adequate held-out precision.

Per-seed time-aware MAE ranges:
- High load: **51.32–59.67s**.
- Moderate load: **18.30–21.10s**.
- Low load: **13.31–14.12s**.

Prior Experiment 002 results still show that the tested cooperative-routing policies performed **worse** than independent routing. More accurate forecasts on chosen routes do **not** establish a cooperative-routing benefit.

## 3. Road occupancy and junction observations

The new pipeline keeps four concepts separate: **(a) original prior route-assignment counts**; **(b) FCD sampled external-road vehicle-seconds and stopped seconds**; **(c) FCD internal-junction sampled time**; and **(d) native SUMO edgeData `sampledSeconds`, density, waiting-time, speed and occupancy percentages.** The original assignment counter is not a forecast of physical occupancy or queue length.

Mean across three development seeds per regime (one-second FCD sampling; vehicle-seconds for the first two numerical measures):

| Window | External-lane stopped-vehicle sample seconds (speed < 0.1 m/s) | Internal-junction sample seconds | FCD minus native edgeData sampledSeconds MAE per edge/bin |
|---|---:|---:|---:|
| 200s | 51,732 | 15,342 | 0.411 vehicle-seconds |
| 600s | 8,063 | 12,614 | 0.264 vehicle-seconds |
| 1,200s | 1,523 | 11,366 | 0.158 vehicle-seconds |

**What this does and doesn't mean:**
- Much more stopped-vehicle sampling occurs on **external approaches** under high demand. This is compatible with queueing being important but **does not isolate its causal contribution** to end-to-end forecast bias.
- Internal junction lanes were observed in roughly **7,300–7,500 route segments per scenario**. Internal-lane visibility is not complete for every transition; one-second FCD snapshots do not resolve subsecond entry/exit boundaries.
- On average over *all* edge/time bins (including very many empty bins), FCD/native sampledSeconds differences are numerically small. **They are not universally negligible:** maximum individual differences reached roughly **20–30 vehicle-seconds**; around **490–920 edge bins per scenario** had positive native sampledSeconds but no corresponding one-second FCD sample. Many correspond to partial-time presence or aggregation-semantic differences. Do not construe the low overall MAE as calibrated occupancy agreement on congested links.
- The parser reports `unresolved_transition_seconds=0` for these uninterrupted one-second FCD streams **by its discrete classification arithmetic**. This is **not evidence that actual junction-entry boundary uncertainty or intersection delay is zero**. Precise subsecond boundary times and the causes of approach stops remain unknown.
- Native SUMO `occupancy` percentages and prior decision-time assignment counts have **different units** and are never scored as if they were the same quantity.
- No counterfactual for any unchosen candidate route was observed.

### Sensitivity: FCD downsampling and bin size

All nine scenarios also produced a prespecified grid of measurement sensitivity checks: 1-, 2-, and 5-second downsampling (reweighted from 1-second observed FCD) under 10-, 30-, and 60-second bins. For the primary 30-second bins, **5-second** thinning produces mean absolute edge/bin vehicle-second differences from the full one-second FCD of approximately **2.56 / 2.22 / 2.03** (200/600/1,200s windows). These nontrivial differences reinforce why apparent calibration must not be inferred from one sampling choice. The per-scenario full sensitivity CSVs are in the workflow artifacts.

## 4. Gates and limits

| Gate | Status after M2 | Explanation |
|---|---|---|
| M0 definitions / fixtures | **Pass for current code** | 12 fixtures and explicitly separate units / half-open bins |
| M1 original policy invariance | **Pass** | All scenarios preserved exact original routes and audits |
| M1–M2 route/observation coverage | **Pass for tested cases** | 1,000/1,000 trips and all planned external traversals matched in every job |
| G3 native physical-occupancy cross-check | **Partially complete / OPEN** | Native and FCD sources acquired and compared, but large outlier edge bins, sparse samples and internal junction coverage need interpretation |
| G4 development seed coverage | **Complete** | All nine scenarios and sampling sensitivities generated; interpretation remains exploratory |
| Predictor accuracy | **NOT validated** | Persistent large positive lateness bias |
| M3 freeze and held-out study | **NOT started** | Immutable run image recorded; no preregistered model/observation freeze or untouched evaluation run |

### Remaining work before any holdout
1. **Diagnose native/FCD outliers on busy edges**, not just overall MAE diluted by zeros; stratify by native sampledSeconds and identify time-boundary/partial-vehicle effects.
2. **Quantify junction-phase uncertainty**, including segments without internal-lane snapshots, explicit bounds at one-second resolution, and external approach stopping separate from internal dwell. Do not label the entire external-to-external interval as intersection delay.
3. **Audit real decision-time occupancy lookup versus chosen-route replay** where necessary. Current trace replays search equations with preassignment counters; it is not exhaustive logging of every explored Dijkstra alternative.
4. Freeze the observation schema, sampling definitions, legal-route and missingness handling, original predictor parameters, source SHA and immutable SUMO digest in an **M3 preregistration proposal**. Obtain explicit approval before releasing untouched evaluation seeds `3101`–`3110`.
5. Only after validation, separately evaluate network objective alignment and fairness using paired independent/cooperative runs. No route-policy changes or penalty sweeps are authorized by these diagnostics.

## 5. Evidence

- [M0–M1 success: three-condition measurement smoke](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40445882827)
- [M2 success: nine calibration jobs and aggregate](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958)
- [Download nine original M2 artifacts + aggregate](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958#artifacts) (GitHub Actions retention: 30 days; published CSV and this report are durable)
- [Previous actual-predictor decision trace](EXPERIMENT_002_ACTUAL_PREDICTOR_TRACE_2026-10-26.md)

**Bottom line:** Measurement instrumentation and development-seed coverage have advanced substantially. The strongest finding remains the predictor's **systematic congestion-dependent lateness bias**, especially at high load. It would be premature to release the held-out study until native/FCD outliers and intersection timing uncertainties are understood and measurement definitions are frozen.
