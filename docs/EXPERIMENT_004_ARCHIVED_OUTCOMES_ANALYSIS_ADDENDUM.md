# Experiment 004 archived-outcomes analysis addendum

**Prespecified before inspecting the additional values.** Source: completed 120-arm run 41023721390. Read-only reanalysis; no new SUMO simulations. The original completed-trip contrast remains unchanged.

## Metrics and decision
1. **Completion:** unique tripinfo vehicle IDs / 1,000 expected, by seed, window and arm. Detect duplicate IDs and missing tripinfo; never silently substitute another seed.
2. **Censoring:** report incomplete vehicles and completion differences. The archive may not contain last-known travel time for noncompleters; if absent, label all-departure mean travel time not identifiable. Do not treat completed-trip mean as unbiased if completion differs. Report conservative bounds only where a defensible common horizon and partial travel time are available.
3. **Fairness:** report completed-trip p90, distribution of durations, and OD-cohort comparison when the original trips XML and vehicle IDs support matching. If OD is unavailable, explicitly mark OD fairness not identifiable.
4. **Exceptions:** report collisions from collisions.xml, and teleport/emergency-stop statistics from statistics.xml when present. Preserve missing fields as unavailable, not zero. Read scenario logs for warnings where structured fields are absent.
5. **Route decisions:** compare per-vehicle route edge sequences across arms C and D; count changed routes for matched vehicles and report missing/duplicate IDs.
6. **Analysis unit:** paired demand seed, 10 seeds per window. Preserve 200s D versus C as primary; 600s/1200s and A/B comparisons secondary. Do not interpret prediction MAE as network-wide benefit.

## Final decision
GO only if the prespecified primary network travel-time comparison favors D with seed-level 95% CI entirely positive (C minus D), completion is not materially worse, and fairness/exception findings do not reveal material harm. If primary CI entirely negative, classify **NO-GO for the tested calibrated policy** regardless of secondary metrics; still report the complete evidence. If inconclusive or key outcomes unidentifiable, classify INCONCLUSIVE rather than a success. This decision concerns the tested policy, not cooperative traffic research as a whole.
