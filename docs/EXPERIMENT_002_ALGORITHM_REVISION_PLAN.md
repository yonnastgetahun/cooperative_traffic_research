# Experiment 002 — Algorithm revision and validation plan (v0.1)

**Status:** Proposed design published for review. **Do not implement or run the revised algorithm until explicit approval.**

## Why revise?
The existing 1,000-vehicle, 10×10 SUMO prototype routes each trip sequentially using an edge-assignment count penalty. At the 200-second departure window and seed 1001, independent routing averaged 197.668 seconds; cooperative penalty 0.02 averaged about 199.54 seconds, with 596 routes changed. A separate road-level diagnostic found heterogeneous speed changes across road segments. This suggests—but does not establish—that route redistribution moves congestion to other links. These observations are one synthetic network and seed, not real-world safety or efficiency evidence.

## Hypothesis
Replacing cumulative, time-insensitive edge-assignment counts with *time-dependent, capacity-sensitive predicted travel costs*, plus individual detour safeguards, may reduce realized system travel time without excessive harm to any driver. A null or negative result is a valid outcome.

## Phase A — Diagnose and validate the existing comparison
1. Preserve all Experiment 001/002 workflows, artifacts and original route generator. Pin the SUMO image by digest/version and record the Git commit.
2. Recompute matched per-vehicle deltas from archived outputs; verify trip IDs, departures, OD pairs, network hash, route legality, and completion. Confirm reported changed/unchanged group means and road-speed counts with documented handling of missing measurements.
3. Generate edge-level time bins (suggest 30 seconds), sampled vehicle seconds, mean speed, waiting time, and entered/left counts for *both* arms. Attribute bottleneck candidates carefully: correlation is not proof of a causal intersection mechanism.
4. Check route distance, free-flow travel time, turning movements and viable alternatives. Report the largest detours and worst harmed drivers. Flag that edge-assignment counts alone are not observed congestion.

## Phase B — Build an explicit predictor (offline, no future leakage)
1. Construct a deterministic forecast of when announced vehicles reach each edge, based on edge length, legal speeds, junction delays and forecasted queues. Update predicted edge occupancy in time bins as routes are assigned.
2. Estimate generalized route cost as predicted in-vehicle travel time plus congestion/junction delay; calibrate on separate training seeds, not on the evaluation seeds. Do **not** feed realized future SUMO outputs from the test arm into route decisions.
3. Preserve legal SUMO connections, vehicle types, road restrictions, fixed departures, OD pairs and network geometry. Require deterministic tie-breaking and a bounded search budget. Log each suggested route, predicted cost, rejected alternative and reason.
4. Define a per-driver detour guardrail *before* evaluation: candidate maximum +10% predicted travel time or +30 seconds, whichever is smaller; also cap extra distance at +15%. These are proposed engineering thresholds to validate, not safety guarantees. A driver may remain on the independent route when no eligible alternative exists.
5. Never permit illegal turns, speeding, or unsafe road behavior. This simulation cannot establish physical-world safety.

## Phase C — Controlled experiment arms
- A: Existing independent static duarouter baseline (historical comparator).
- B: Existing edge-count cooperative algorithm (reference).
- C: Time-aware cooperative routing with safeguards (new candidate).
- D: Time-aware routing with safeguards disabled (ablation, simulated only).
- Optional stronger control: independent *traffic-aware dynamic* routing with matched information/replanning privileges. **Do not claim superiority to realistic independent navigation until this control is implemented.**

Use byte-identical network/trips/seed within each paired comparison. First run a 1,000-vehicle, 10×10, 200-second departure-window smoke test. Then evaluate 200/600/1,200-second windows on **at least 10 prespecified paired seeds** (separate from any predictor tuning seeds). Keep scenario-specific results separate.

## Phase D — Metrics and acceptance gates
- Primary: total realized travel time across all requested trips, with unfinished trips explicitly reported and handled by a prespecified cutoff/censoring policy; paired change versus A, by scenario.
- Secondary: mean, median, p95 and maximum trip duration; waiting; throughput; road speed/occupancy; route distance; driver-level helped/harmed counts and worst harm; compute time.
- Safeguard audits: percentage of drivers exceeding the planned detour limits and the *realized* harm distribution. Predicted bounds do not ensure realized bounds.
- Engineering gates: identical demand, valid routes, reproducible assignments, actual route changes, all artifacts exported, and explicit reporting of failed/incomplete runs.
- Scientific gate: compare paired seed-level differences with uncertainty intervals; disclose null/negative outcomes and all tested parameters. No claims of improvement based on a single seed or a tuned-to-test configuration.

## Phase E — Departure-time coordination (separate Experiment 003)
Retain the approved extension: compare fixed departures, coordinated routes, coordinated voluntary departures, and both. Account for **predeparture delay in door-to-door journey time**, eligibility, latest-arrival constraints and fairness. Do not change departure times during Experiment 002; doing so would confound the routing comparison.

## Proposed implementation deliverables (only after approval)
- Versioned route-prediction module and tests
- Explicit manifest of parameters, SUMO image digest, scenario seeds and input hashes
- Separate manually triggered GitHub Actions smoke workflow; preserve historical workflows
- Paired comparison and driver/edge diagnostics reports (CSV/JSON)
- Validation report with reproducibility checks, uncertainty, limitations and no premature real-world claims

## Approval checkpoint
Review the predictor assumptions, proposed 10%/30-second and 15% detour bounds, 10-seed evaluation design, and choice of independent traffic-aware control. **Publication of this plan does not authorize implementation.**
