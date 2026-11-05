# E1-v2 archive-only F0-F5 mechanism investigation results

**Scientific outcome:** ARCHIVE-BASED OBSERVATIONAL CHARACTERIZATION; precise physical cause NOT IDENTIFIED.
This audit did not rerun SUMO, reforecast, train, tune, or touch reserved 6201-6212/6301-6312 seeds.

## F0 — Original archive and coverage
- Original **695** source files, **60,000** completed tripinfo records, **60** previously run arms, and ten pred-before-label locks verified.
- Per-member original SHA256 release ledger verified: **True**.
- Five-second edgeData used; exact individual edge-entry clocks and vehicle-resolved FCD NOT established.
- Missing field attributes are not silently read as zeros. Complete stream coverage and internal-edge counts appear in F0_coverage.csv.

## F1 — Actual elapsed-time decomposition
- **50** route-change pairs: own + others = whole-network effect; source insertion + in-network duration = whole-network effect.
- Frozen four-seed E1-v2 MAE **1478.5625 network-seconds**, correct externality direction **5/16**. D1 NO-GO unchanged.
- Driver-level >30-second harm and nonparticipant consequences preserved as descriptive data, not policy Test B.

| Post-outcome selected case | Others observed (network-s) | E1-v2 forecast | Source insertion change | In-network duration change | Aggregate edge waiting change (vehicle-s) |
|---|---:|---:|---:|---:|---:|
| 6111/probe3 | +1847 | +1 | +0.0 | +1821.0 | +1775.0 |
| 6112/probe2 | +3215 | +0 | +2.0 | +3217.0 | +2648.0 |
| 6113/probe2 | -3960 | +0 | -22.0 | -3861.0 | -2320.0 |
| 6114/probe2 | -2929 | +0 | +6.0 | -2888.0 | -2691.0 |

## F2 — Observed five-second edge/queue-associated changes
- **916,987** paired external-edge/time-bin rows compared across all 50 route-change arms.
- Entered and left counts, waiting, sampled seconds and nonadditive speed/occupancy snapshots retained in compressed raw-derived table.
- Temporal adjacency or lag is observational, not a unique spillback or queue-front causal measurement.

## F3 — Priority-junction approach/discharge
- **5,000** junction-by-arm rows for the **100** priority intersections.
- Inbound external-edge left, outbound entered and approach waiting contrasts are aggregate proxies; they do NOT count exact turn movements, gap acceptance, or concurrent crossings.

## F4 — Ten prospectively selected two-route bundles
Four-arm identity: J = C(bundle) - C(single_a) - C(single_b) + C(I); all drivers included. Companion singleton IDs verified per seed.

| Seed | Exact singletons | Actual J (network-s) | E1-v1 predicted J | E1-v2 predicted J | J insertion | J observed edge waiting (veh-s) |
|---|---|---:|---:|---:|---:|---:|
| 6101 | probe0, probe1 | +1915.0 | +0.0 | +0.0 | -8.0 | +132.0 |
| 6102 | probe0, probe1 | +3288.0 | +1.0 | +0.0 | +0.0 | +3657.0 |
| 6103 | probe0, probe1 | -1306.0 | +0.0 | +0.0 | +5.0 | -1545.0 |
| 6104 | probe0, probe1 | +2431.0 | -1.0 | +0.0 | +0.0 | +1024.0 |
| 6105 | probe0, probe1 | -743.0 | +0.0 | +0.0 | -29.0 | +168.0 |
| 6106 | probe0, probe1 | -13.0 | +0.0 | +0.0 | +0.0 | +19.0 |
| 6111 | probe0, probe1 | +830.0 | +6.0 | +0.0 | +0.0 | +475.0 |
| 6112 | probe0, probe1 | +374.0 | +0.0 | +0.0 | +0.0 | -22.0 |
| 6113 | probe0, probe1 | +2308.0 | +0.0 | +0.0 | +0.0 | +1356.0 |
| 6114 | probe0, probe1 | +136.0 | +0.0 | +0.0 | +0.0 | +14.0 |

## F5 — Hypothesis assessment
- **Timing T:** directly observed scheduled and actual trip starts; five-second aggregate edge counts. Exact per-driver edge forecast-vs-truth error NOT OBSERVABLE.
- **Queue Q:** aggregate waiting and occupancy responses observable; true queue-front propagation, downstream receiving and causal mediation UNIDENTIFIED.
- **Junction J:** static conflict model previously verified; aggregate external approach/discharge changes observable; movement-specific right-of-way and gap acceptance UNOBSERVABLE.
- **Bundles B:** ten exact whole-driver interaction contrasts directly reconstructed; they do not prove a single junction or queue was causal.
- **Accounting A:** 60 archived arm identity/source SHA checks, prediction locks, fixed routes, source insertion and duration decomposition passed; missing detector fields and sampling semantics remain documented.

**Final decision:** E1-v2 DEVELOPMENT_NOT_QUALIFIED; independent validation NOT_STARTED; Test B NOT_RUN. Any new instrumented simulation or revised E1-v3 requires a separate prospective protocol and approval. These development records cannot serve as fresh independent holdouts. No real-road or individual-safety efficacy claim.

**Available machine-readable derived evidence:** F0_coverage.csv, F1_effects.csv, F2_edge_5second.csv.gz, F3_junctions.csv, F4_bundles.csv, F0_F5_summary.json.
