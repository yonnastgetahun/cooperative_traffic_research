# Experiment 003 development cohort manifest v0.1

**Purpose:** Fit the prespecified regime-specific cumulative timing correction on new, independent development evidence. M3 held-out seeds 3101–3110 remain excluded from fitting.

**Development seeds (fixed before execution):** 2201, 2202, 2203, 2204, 2205, 2206, 2207, 2208, 2209, 2210.

**Regimes:** 200, 600, 1200-second departure windows. **Scenario count:** 30 (10 development seeds × 3 regimes). **Vehicles:** 1,000 per scenario, unchanged 10×10 synthetic road network.

**Frozen scientific base:** `be2e8d27c78c8b6de4891115d6d951edc877ac6e`; pinned SUMO image inherited from the successful M3 workflow. Generate demand, routing and native observations without modifying the frozen scientific methods. These are development seeds and are not a new held-out evaluation.

**Training rule:** Fit the prespecified `a_r + b_r*k` correction separately for each regime using only the ten development seeds; record all 30 input hashes, model coefficients and in-sample descriptive metrics. In-sample metrics are **not** independent validation.

**Failure handling:** Preserve failed scenarios, do not silently replace seeds, and do not fit if any of the 30 required development scenarios is missing or invalid.

**Next boundary:** After fitting, freeze coefficients and prespecify a fresh disjoint confirmatory seed manifest *before* executing the confirmatory cohort. The confirmatory cohort must exclude both 2201–2210 and M3 held-out 3101–3110.

**Decision:** This manifest authorizes development-data generation and fitting, not confirmatory scientific claims.
