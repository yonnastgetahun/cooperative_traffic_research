# G3 Measurement Reconciliation — Archived Development Evidence

**Status:** Offline G3 reconciliation and cross-edge case inspection completed. **G3 is NOT closed. M3 freeze is NOT authorized.**

- [Reconciliation report](G3_RECONCILIATION_REPORT.md) and [gate ledger](g3-integrity.json)
- [Stratified native/FCD road-bin differences](g3-occupancy-strata.csv)
- [Ranked outlier road bins](g3-top-edge-bin-outliers.csv) and [front-near-junction vehicle evidence](g3-cross-edge-ledger.csv)
- [Cross-edge case summary](g3-cross-edge-summary.json)
- [Junction sampling uncertainty](g3-junction-uncertainty.csv)
- [Per-scenario integrity](g3-per-scenario.csv)

Original SUMO [M2 run 40446073958](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958); [G3 audit run 40448102464](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40448102464); [cross-edge evidence run 40448538736](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40448538736).

**Scope:** Nine existing M2 development scenarios only. No additional routing runs or holdout usage. Observing a vehicle's front near the start of a downstream internal lane is **consistent with** vehicle extent extending over the prior road boundary, but is **not an exact reconstruction of SUMO native per-vehicle sampledSeconds**. Do not present this observation as proof of a calibrated traffic predictor or a cooperative-routing benefit.
