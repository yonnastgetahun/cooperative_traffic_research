# Experiment 002 — Controlled Cooperative Routing Study (design v0.1)

Status: approved design; implementation and execution NOT yet completed.

## Research question
Does information-sharing cooperative routing reduce travel time and waiting, without unacceptable fairness costs, compared with independent static shortest-route assignment?

## Fixed conditions
- SUMO 10x10 grid, 200 m edges, 1,000 passenger vehicles.
- Departure windows: 200 s (high), 600 s (moderate), 1,200 s (low).
- Seeds: 1001, 1002, 1003 initially; expand to at least 10 paired seeds before strong inferential claims.
- Generate **one immutable network.net.xml and trips.xml per (window, seed)**. Reuse byte-identical inputs for all strategies. Hash both inputs and record hashes.
- Pin SUMO container by immutable digest or explicit version, and record commands/configuration.
- Preserve Experiment 001 calibration and reproducibility workflows unchanged.

## Treatment arms
A. Independent baseline: existing duarouter shortest-time static routing with no information-sharing; preserve the precise existing settings.
B. Cooperative prototype: before departure, route eligible vehicles using a shared prediction of edge congestion derived from aggregate planned assignments. Use a documented, deterministic iterative assignment algorithm (e.g. sequential assignment with edge-load penalties and stable vehicle order); prohibit use of realized future traffic. Clearly distinguish this from dynamic real-time cooperation.
C. Optional ablation: randomized or load-unaware alternative route assignment, to isolate whether improvement is due to shared information rather than simply route diversification.

## Intervention definition and safeguards
- At each routing decision, use only information that would have been available by that simulation time. Predeparture planned-demand estimates are permissible only if the protocol explicitly assumes advance trip announcements; document this assumption and evaluate its realism.
- Same OD pairs, departures, network, vehicle parameters, SUMO configuration and simulation end conditions in both arms.
- Confirm viable alternative paths exist for a substantial share of trips. If not, redesign the network before interpreting a null result.
- Test participation 0%, 25%, 50%, 75%, 100% after full-participation proof of concept; assignment and compliance must be deterministic per seed.
- Avoid leakage from baseline observed edge travel times into the treatment's route planning.
- Include a non-cooperative re-routing control if the cooperative treatment has more rerouting opportunities than baseline.

## Primary outcomes
- Mean trip duration, seconds, and relative % change (paired by seed/window).
- Mean waiting time, seconds, and relative % change.
- Completion rate; if any trip unfinished, report censored/incomplete outcomes rather than calculating only over finishers.

## Secondary outcomes
- Median and p95 trip duration, total travel time, per-driver difference distribution, proportion helped/harmed, maximum harm, route distance/detour, congestion distribution by edge, and runtime overhead.
- Report per-window results rather than pooling across unlike congestion regimes.

## Validation gates
1. Build a fixture test confirming identical network/trip hashes between A and B.
2. Validate routes and legal connections; confirm 1,000 departures and trip completions, or explicitly report failures.
3. Demonstrate strategy B actually changes route assignments and uses shared load estimates.
4. Run one paired seed/window as a smoke test; inspect route changes, metrics and logs.
5. Run 3x3 paired matrix, then extend to >=10 seeds for stronger uncertainty estimates.
6. Report paired seed-level differences, confidence intervals, and adverse impacts; no causal claim beyond tested simulated conditions.

## GitHub execution plan
- Add a new isolated workflow (Experiment 002), initially manual dispatch.
- Matrix: departure windows [200,600,1200], seeds [1001,1002,1003], strategies [independent,cooperative]; preserve input files and paired comparison reports.
- Publish per-run manifest (including version, algorithm parameters, hashes), tripinfo.xml, route files, metrics.csv and comparison.csv.
- No workflow trigger until implementation passes smoke validation.

## Interpretation
Experiment 001 established congestion calibration and initial reproducibility, **not** a routing improvement. Experiment 002 is the first planned controlled test. A positive result would be evidence only for the implemented strategy and simulated network, not proof of benefits on real roads.
