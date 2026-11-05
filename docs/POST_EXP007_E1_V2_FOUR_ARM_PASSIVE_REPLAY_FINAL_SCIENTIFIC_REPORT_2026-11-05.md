# E1-v2 four-arm passive replay — scientific findings

## Relevance to the central cooperative-traffic question
Cooperation may improve aggregate traffic only if the effects of one person's changed route on other drivers can be forecast accurately. These four retrospective replays trace actual vehicle movements for two already-observed contrasting cases. They do not validate a forecasting model or show a cooperative-policy advantage.

**Status: VALID RETROSPECTIVE INSTRUMENTED OBSERVATION.** All four selected attempts reproduced original 1,000-driver outcomes and contained FCD, exit-time, edge/lane and exception evidence. The unique physical causal mediator remains unidentified. Frozen E1-v2 development NO-GO is unchanged; independent validation and cooperative Test B remain unexecuted.

## Scientific evidence and provenance
- Original archived development execution: GitHub Actions 41966516110; original member-byte release exp007-e1v2-d1-development-nogo-2026-11-04.
- Original simulations: SUMO 1.28.0 image ghcr.io/eclipse-sumo/sumo@sha256:b1298d1fd18244022db4da6498a2e842295c8014147ec78102270eaeb24449cb.
- Two seeds selected **after viewing original results**; four arms (6112 I/probe2 and 6113 I/probe2), 4,000 matched replay tripinfos; not four statistically independent replications.
- Original SHA256s, route containment and prospective prediction locks checked. Passive flags only, no new demand or routing decisions.

## Gates
| Seed / arm | G2 per-field max deviation (seconds) | FCD vehicle samples | Near-stopped samples ≤0.1m/s | External edge exits |
|---|---:|---:|---:|---:|
| 6112 / I | 0.000 | 209,815 | 51,850 | 8,287 |
| 6112 / probe2 | 0.000 | 213,032 | 54,618 | 8,287 |
| 6113 / I | 0.000 | 208,835 | 50,702 | 8,266 |
| 6113 / probe2 | 0.000 | 204,974 | 47,640 | 8,266 |

## Paired original-network outcome and physical time accounting
| Seed / changed vehicle | Others' net cost (network-s) | All-driver change (network-s) | Insertion component | In-network duration | Recorded waiting (included within duration) | FCD near-stop sample change |
|---|---:|---:|---:|---:|---:|---:|
| 6112 / veh0142 | +3215 | +3219 | +2 | +3217 | +2775 | +2768 |
| 6113 / veh0038 | -3960 | -3883 | -22 | -3861 | -3050 | -3062 |

The observed travel-time effects mainly occurred after insertion in these two selected scenarios; recorded stopped waiting and independent FCD near-stopped samples are related but not identical measurements. Waiting is already part of each vehicle's duration and was NOT added to elapsed network cost.

## Driver-level chronology and traffic response (descriptive only)
| Seed | Changed driver's first matched trace divergence (s) | Earliest matched other-driver FCD difference (s) | Largest absolute edge near-stop response |
|---|---:|---:|---|
| 6112 | 43.0 | 44.0 | D3E3 (+2433 near-stopped vehicle samples) |
| 6113 | 21.0 | 23.0 | F4E4 (+74 near-stopped vehicle samples) |

FCD is sampled at one-second steps. First observed lane/edge appearance is **not** exact continuous-time entry. The historical E1-v2 predictions do NOT archive per-edge forecast clocks, so this study does NOT manufacture prospective per-edge forecast-versus-actual errors.
Observed internal-lane sampling and queue-proxy clusters are documented in the accompanying machine-readable tables. A one-second internal-lane sample can miss a short crossing. A cluster is a declared spatial proxy (three or more stopped vehicles within 10m consecutive position gaps), **not** an independent causal diagnosis of an upstream spillback wave.

## Competing hypotheses and limits
| Candidate | What the new evidence can assess | What remains unproven |
|---|---|---|
| T: temporal ordering | Observed per-driver road/lane sample sequences, departure times and divergence onset | Model-vs-SUMO per-edge prediction error without archived model event trace |
| Q: physical queuing | Near-stop exposures, contiguous spatial groups, edge and time redistribution | Unique causal upstream spillback mediator absent a controlled intervention |
| J: junction service | Internal-lane entry samples linked to verified static connection map | True crossing concurrency and causal contribution of one junction; 1s sampling misses fast movements |
| A: accounting/measurement | All original 4,000 vehicle outcomes and route hashes preserved; FCD and exit-time evidence available | Generalizability from two retrospectively selected seeds |

**Disposition:** A valid explanatory observation can identify timing- and queue-associated patterns but not a unique junction/queue causal effect. E1-v2's frozen D1 NO-GO stands. A future model E1-v3 would need fresh development and independent validation. Do not open the reserved 6201–6212 or 6301–6312 seeds or run Test B without a separately authorized prospective protocol.

## Reproducibility assets
This report accompanies scientific_summary.json, G2_G3_replay_gates.csv, driver_matched_differences.csv, actual_target_edge_entry_samples.csv, nearstop_edge_5s_hotspots.csv, nearstop_spatial_cluster_hotspots.csv, observed_internal_lane_entry_differences.csv, and pairwise_network_accounting.csv. Full FCD, original-exitTimes and detectors are retained in the separate evidence release, not mixed with original frozen D1 members.

**No social publication was authorized or initiated.**
