# Experiment 003 — Independent confirmatory scientific results

**Evidence:** [GitHub Actions run 41018871460](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41018871460), artifact [12960469524](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41018871460/artifacts/12960469524). All 30 scenario jobs and final evaluator passed. Frozen scientific code `be2e8d27c78c8b6de4891115d6d951edc877ac6e`; development seeds 2201–2210; disjoint confirmatory seeds 3201–3210; 200s primary, 600s/1200s secondary.

## Prespecified model
For route ordinal k in congestion regime r: `p_calibrated(v,k) = p_frozen_timeaware(v,k) + a_r + b_r*k`. Coefficients fitted on development data and frozen before confirmatory evaluation.

| Regime | a_r (s) | b_r (s per edge) |
|---|---:|---:|
| 200s | 4.053135104279146 | 11.524898884412591 |
| 600s | 1.7868471223107676 | 3.9515691107998387 |
| 1200s | 1.8903085164618962 | 2.6820862794976956 |

## Confirmatory findings
Each regime has ten independent seed-level paired MAE differences; 95% two-sided Student-t intervals use seed as the uncertainty unit.

| Regime | Original time-aware MAE (s) | Calibrated MAE (s) | Paired mean benefit (s) | 95% CI (s) | Calibrated signed error (s) |
|---|---:|---:|---:|---|---:|
| 200s (primary) | 53.2529178985 | 35.0328515175 | 18.2200663810 | [17.2985378997, 19.1415948624] | -0.2448003978 |
| 600s | 18.6479044393 | 10.0226342685 | 8.6252701708 | [8.3988517757, 8.8516885660] | -0.1666460693 |
| 1200s | 13.4612552876 | 6.5529438861 | 6.9083114015 | [6.6549752618, 7.1616475411] | -0.0536165977 |

**Primary endpoint decision:** PASS under the prespecified criterion: 200s paired benefit is positive with a 95% confidence interval wholly above zero. Secondary 600s and 1200s also show positive intervals. Relative MAE reductions are approximately 34.2%, 46.3%, and 51.3%.

## Scientific interpretation and boundaries
A regime-specific linear cumulative timing correction trained on separate development seeds improved chosen-route road-entry prediction accuracy on fresh synthetic demand seeds. Mean signed residuals were near zero, but individual timing errors remain. These are post-hoc forecast corrections on fixed route observations; **no routing decisions were changed in Experiment 003**, and no improvement in network-wide travel time, congestion, fairness, throughput, or safety has been established. The 10x10 synthetic network, SUMO model and regime assumptions limit external generalization. The original M3 scientific outputs remain unchanged.

## Next experiment
Design a controlled routing-policy test comparing independent routing, the original cooperative policy, and a cooperative policy using calibrated predictions on identical fresh demand scenarios. Predefine network-wide outcomes and fairness/exception gates. The calibrated forecast's accuracy advantage is a premise to test, not evidence of routing efficacy.
