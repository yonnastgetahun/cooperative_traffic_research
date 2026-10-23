# Experiment 001 — reproducible cooperative routing (implementation contract)

Status: design locked; implementation and validation pending. No results claimed.

## Question and scope
Can opt-in coordinated routing reduce total network travel time versus credible independent traffic-aware routing, without disproportionately harming nonparticipants? Hold departure times fixed in Experiment 001. Departure-time coordination is a later experiment.

## Network and demand
Start with a small synthetic SUMO network with one origin/destination pair, two viable routes, and a shared or competing bottleneck; record edge lengths, lane counts, speed limits and capacities. Use identical OD trips, vehicle types, departure times, network geometry and random seeds in each matched comparison. Include uncongested and congested demand regimes. Validate that congestion actually emerges before assessing coordination.

## Baseline
Use SUMO-supported travel-time-aware dynamic assignment, not static shortest-distance routing. Document the assignment procedure, information refresh interval and convergence or stopping criteria. Apply the same traffic information assumptions to treatment drivers who do not opt in.

## Treatment
Select participants reproducibly using a seeded draw at 5%, 10%, 25% and 50% participation; include 0% as baseline. Begin with a transparent centralized route-assignment heuristic: consider alternate feasible routes for opted-in trips and select assignments minimizing estimated total system travel time subject to a predeclared individual detour bound. Use a common travel-time estimator for baseline and treatment; do not assume perfect foresight. Test actual compliance separately from enrollment, and never silently reassign nonparticipants. Record assignments, rejected suggestions and realized travel times.

## Metrics and validity
Primary: total realized travel time for completed trips. Secondary: mean/median/95th-percentile trip time, total delay, completed-trip throughput, unfinished trips at cutoff, network occupancy and diversion to local links. Break out participant and nonparticipant outcomes; report worst-off drivers and distribution of time changes. Predeclare how unfinished trips are penalized or handled to prevent artificially good results. Run multiple matched seeds and demand levels, report uncertainty, null and negative outcomes. Compare fairness constraints and no-constraint sensitivity runs.

## Visualization as an experiment output
Export time-stamped vehicle positions (or edge trajectories), routes, run metadata, and time-series aggregate metrics from both conditions. Use a shared simulation clock, matching camera/viewport, and consistent vehicle/route styling. Generate a side-by-side visual of baseline versus treatment with on-screen metrics, a caption stating network type and participation, and a clear simulation/not-real-world label. Preserve full results in GitHub; optionally export a 15–30 second excerpt for X/LinkedIn that links back to methods and full run. Never imply a favorable result if the simulation is inconclusive.

## Reproducibility deliverables
- Network and route-generation source/configuration
- Seeded demand generator and manifest of scenario parameters
- Baseline runner, treatment runner and shared metrics exporter
- Machine-readable trajectory/metric outputs with versioned schema
- Visualization renderer and a representative clip
- README commands, SUMO/Python versions, license/attribution and checks
- Validation notes and results including failed/null runs

## First acceptance gate
One documented network and demand fixture; one repeatable baseline and one treatment using the same trips/seed; metrics exported and checked for missing/uncompleted trips; side-by-side animation generated from actual trajectories. Do not expand to all participation rates or claim benefits until this gate passes.

## Open engineering choices
Exact synthetic network topology, SUMO version, dynamic assignment algorithm, heuristic search budget, detour bound and rendering library must be recorded before results are interpreted. These are implementation parameters, not settled empirical findings.
