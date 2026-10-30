# M3 bias mechanism analysis — prespecified exploratory plan

**Scope:** Read-only analysis of all 30 archived M3 scenarios (seeds 3101–3110 × departure windows 200, 600, 1200 seconds). No new simulation, predictor fitting, or edits to frozen scientific results.

## Question
Is the route-progressive signed road-entry timing error attributable primarily to a departure offset, accumulating per-edge traversal mismatch, congestion sensitivity, or route-composition effects?

## Variables and estimands
For vehicle v and route edge ordinal k, let e(v,k) = observed native road-entry time − frozen time-aware predicted road-entry time.
- Initial offset: e(v,0), summarized per seed.
- Within-vehicle increment: Δe(v,k)=e(v,k)−e(v,k−1), for consecutive observed route ordinals. Report per-seed mean, median, count and positive fraction.
- Congestion contrast: differences in seed-level mean Δe across the three windows, with uncertainty based on ten demand seeds.
- Route composition: stratify by complete observed route length and ordinal, avoiding comparison of different cohorts at late ordinals.
- Native traversal proxy: observed interval between consecutive road entries, where present. Compare Δe to that interval, explicitly noting that entry-to-entry time includes edge traversal and junction/queue effects and cannot isolate their causes.

## Method
1. Reuse the archived evidence from successful M3 run 40953111402; validate 30 unique seed/window folders and required paired-road-entry columns.
2. Parse vehicle ID, route index, native entry and time-aware prediction; check uniqueness of (vehicle, ordinal), finite values, and ordinal continuity. Report missingness and any duplicate keys.
3. Compute first-edge offsets and within-vehicle consecutive increments. Aggregate vehicle records within each seed before comparing regimes. Keep seed as the statistical unit; avoid treating individual edge records as independent replicates.
4. Stratify vehicles by route length, and compare common ordinal positions across all three windows. Explicitly report small-cell counts and selection effects.
5. Assess how increments relate to observed inter-entry intervals, without inferring causal edge vs junction delay from this proxy alone.
6. Publish machine-readable per-seed/regime metrics, summary tables, figures and a concise interpretation. Do not label an exploratory association as a proven mechanism.

## Decision rule
- Evidence of consistently small first-edge offsets and positive within-vehicle increments across seeds supports accumulation over fixed departure offset.
- Differences in increment magnitudes across regimes support congestion association, not causal identification.
- If within-route length strata the pattern attenuates, report route-composition confounding.
- If data lacks required fields for an estimand, mark it not identifiable rather than manufacturing a proxy.

## Deliverables
- Reproducible read-only script and GitHub Actions run using archived artifacts.
- Machine-readable per-seed results, route-length strata, quality diagnostics and cross-regime comparison.
- Evidence-linked interpretation with explicit limitations and recommendation for the design of Experiment 003.

**Execution order:** Commit this plan first, then implement and execute. No changes to the frozen M3 protocol.
