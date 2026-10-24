# Experiment 001 — congestion calibration plan (draft protocol)

Status: calibration design; no calibration results yet. Preserve the existing smoke-test workflow and artifacts.

## Purpose
Identify low, moderate, and high congestion regimes on the 10×10 synthetic SUMO grid using 1,000 fixed origin–destination trips. This is a *baseline calibration*, not evidence of cooperative routing gains.

## Important distinction
The existing smoke-test workflow uses 1,000 trips with depart = i × 0.2 seconds, a 200-second release window, seed 1001, and a static duarouter baseline. Calibration may use this for feasibility, but the scientific independent-routing control must ultimately be a documented, credible traffic-aware dynamic assignment, consistent with docs/experiment-001-implementation.md.

## Proposed calibration matrix
- Grid: 10×10, 200 m edge length, unchanged vehicle class and network settings.
- Vehicle count: 1,000 in every initial scenario.
- Departure windows: 200, 300, 600, 900, 1,200 seconds (including the existing 200-second reference).
- Construct each departure schedule deterministically; hold the 1,000 origin–destination pairs fixed across windows, then change *only* departures.
- Run at least three independent matched seeds per window after initial engineering validation; save seed, SUMO version, network and trips files, exact CLI options, workflow commit SHA, and scenario manifest.
- Use a common, sufficiently long simulation cutoff for comparisons; record and report unfinished trips explicitly, never silently discard them.

## Outputs and checks
For every run, save tripinfo, summary time series, routes, demand manifest, and machine-readable CSV/JSON summary. Report started/completed/unfinished vehicles, mean/median/p95 trip duration, mean waiting time, total travel time, total delay (with definition), throughput and peak accumulation. Fail validation if inputs mismatch or required output is missing. Avoid interpreting low mean duration when completion is poor.

## Selecting regimes
Choose low, moderate and high based on observed congestion and route-choice opportunities, not on favorable cooperative-routing results. Document the thresholds *before* running treatment. If changing departures alone cannot produce useful levels, revise demand or bottleneck configuration as a separately versioned calibration round; never quietly mix different networks or OD sets.

## Next implementation tasks
1. Add a separate manual GitHub Actions calibration workflow, without overwriting experiment-001-smoke-test.yml.
2. Parameterize departure window and seed; preserve OD pairing; export manifests and results.
3. Run a single validation case, then the full matrix; inspect congestion and route alternatives.
4. Publish frozen scenario manifests and a calibration report.
5. Implement and validate independent traffic-aware routing, then compare cooperative routing with matched trips/seeds and participant/nonparticipant fairness measures.

No calibration workflow has been executed or verified by this document alone.
