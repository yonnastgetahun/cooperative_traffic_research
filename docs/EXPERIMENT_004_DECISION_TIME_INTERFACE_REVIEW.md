# Experiment 004 — Decision-time interface inspection

**Source files reviewed:** `experiments/experiment_002/time_aware.py`, `cooperative.py`, and `trace_actual_predictor.py` on `main`. This is a source-level scientific inspection, not an Experiment 004 simulation.

## Original cooperative decision mechanics

### Time-binned cooperative prototype (`time_aware.py`)
- `search(origin,dest,departure,edges,adj,occupancy,bin_s,pressure)` uses a heap with a single best cost per edge.
- At each candidate successor `v`, its lookup time is `entry = departure + cost`; the time bin is `int(entry // bin_s)`.
- Predicted surcharge is `freeflow(v) * pressure * (occupancy[(v,bin)] / capacity_proxy(v))`, plus a turn proxy of one second at branching junctions.
- The candidate path is accepted only if its **free-flow** travel time and distance pass detour guardrails; otherwise the free-flow baseline route is used.
- After assignment, occupancy counts are updated at **free-flow-clock** bins, not the calibrated predicted-entry clock.
- The prototype assumes all trips are announced in advance. It does not use actual future SUMO measurements to choose routes.

### Sequential load-penalty prototype (`cooperative.py`)
- Candidate cost is free-flow edge time multiplied by `1 + penalty * prior_assigned_edge_count`.
- There is no predicted entry-time argument or time-bin lookup in this algorithm; directly applying an entry-time calibration would require changing the cost model.

### Trace and Experiment 003
- `trace_actual_predictor.py` captures original candidate/chosen route timing and pre-assignment occupancy, but explicitly reports that replayed path costs can differ from heap winning costs because time-bin lookup depends on path arrival time.
- Experiment 003 fits `p'(v,k)=p(v,k)+a_r+b_r*k` **on already chosen routes**, using observed native road entries only as fitting targets in the separate development cohort. It establishes accuracy on fresh chosen-route data, not candidate-route counterfactual accuracy.

## Non-leaking adapter feasibility

The fixed `a_r,b_r` coefficients are known before a new simulation and can be applied prospectively to predicted candidate arrival times without reading future observations. However, route ordinal `k` is **not tracked in the original heap search state**. A path-dependent calibrated entry time would change time-bin lookups and potentially violate the original one-best-label-per-edge assumption; simply adding `b_r*k` to a scalar cost or replaying it after path selection is not scientifically equivalent.

Further, the existing post-assignment occupancy clock uses free-flow timing. A prospective calibrated-clock update would alter occupancy dynamics in addition to candidate scoring, so it must be held fixed for a clean forecast-input comparison or explicitly identified as a second intervention.

## Decision and next bounded implementation

**Decision:** The calibration is prospective-computable in principle, but **not yet a drop-in replacement** for the original routing search. Do not claim a calibrated cooperative-policy comparison has been performed.

1. Create a separate Experiment 004 search adapter carrying route ordinal and predicted time as explicit state, with deterministic tie-breaking and a clearly documented dominance/pruning rule.
2. Hold the demand, free-flow guardrails, pre-assignment occupancy source, and post-assignment occupancy update rule fixed between original and calibrated policy arms. Document any unavoidable search-state differences.
3. Compare original search vs new stateful search **with zero correction** first. If they differ, the Experiment 004 design must include an adapter-only control arm so that calibration effects are not confounded with the search implementation.
4. Only after that equivalence/adapter-control decision, freeze fresh paired seeds and execute network-outcome simulations.

No M3 or Experiment 003 frozen scientific artifacts are modified.
