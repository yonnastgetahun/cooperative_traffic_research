# Experiment 004 — Does calibrated prediction improve cooperative routing?

**Status: prospective scientific design; no Experiment 004 simulation or outcome claims.**

## Motivation
Experiment 001 found that independent routing outperformed two cooperative policies in three tested congestion regimes. Experiment 003 independently confirmed improved *chosen-route road-entry prediction accuracy* using a fixed regime-specific cumulative correction, but it did not change route assignments. Experiment 004 tests whether improved forecasts actually change routing decisions and improve network-wide outcomes.

## Primary question and falsifiable hypothesis
When the cooperative route-choice mechanism is otherwise held fixed, does substituting the frozen Experiment 003 calibrated predictor for the original predictor improve **mean completed-trip travel time** relative to the original cooperative policy in the 200-second high-congestion regime? A separate comparison against independent routing determines whether calibrated cooperation closes or reverses the Experiment 001 performance gap.

The null hypothesis is no improvement in seed-level mean completed-trip travel time.

## Prespecified arms
- **A — Independent routing:** frozen Experiment 001 independent baseline.
- **B — Original cooperation:** original cooperative algorithm with the original forecast.
- **C — Calibrated cooperation:** same cooperative policy and candidate set, changing only the forecast input to the frozen Experiment 003 correction.
- Optionally repeat both original cooperative prototypes as separate B/C pairs if their interfaces and objective functions differ; never combine them post hoc.

## Critical scientific implementation check
Experiment 003 calibrated **road-entry timestamps along an already chosen route**. These are not automatically equivalent to counterfactual candidate-route costs at decision time. Before executing any routing-policy comparison, document whether the calibrated forecast can be computed causally using only information available at each route decision. Do not use observed future SUMO entry times or post-hoc residuals as routing inputs. If no valid decision-time mapping exists, record that as a scientific design limitation and develop a prospective forecast adapter before any claims of policy efficacy.

## Experimental controls
Use the same 10x10 synthetic road network, 1,000 vehicles per scenario, and 200/600/1200-second departure windows. Pair all arms on the same fresh demand seeds and simulator configuration. Do not reuse development 2201–2210, M3 held-out 3101–3110, or Experiment 003 confirmatory 3201–3210 as new confirmatory seeds. Freeze a new exact seed manifest and all routing-policy code before execution.

## Outcomes
- **Primary:** seed-level paired difference in mean completed-trip travel time between C and B in 200s regime; use independent demand seed as uncertainty unit, report two-sided 95% CI.
- **Essential benchmark:** C versus A (independent routing) in 200s; report separately, with a prespecified criterion for claiming an improvement over independent routing.
- **Secondary:** same comparisons in 600s and 1200s, throughput, completed-trip fraction, network travel-time distribution, 90th-percentile trip time, fairness by route/OD cohort, reroute count, and collision/exception integrity.
- Treat incomplete trips and censoring explicitly. Never infer better outcomes from prediction MAE alone.

## Implementation and decision sequence
1. Inspect the frozen Experiment 001 independent and cooperative route-choice code and identify the actual decision-time forecast interface.
2. Specify a non-leaking, decision-time calibrated forecast adapter and verify that the only B-to-C change is prediction input. If this cannot be established, do not execute a misleading comparison.
3. Prespecify fresh paired demand seeds, route-choice definitions, outcomes, exception gates and primary analysis before simulation.
4. Execute all arms across the three regimes with evidence preservation and seed-level paired analysis.
5. Publish a GO/NO-GO scientific interpretation for cooperative routing, including negative results.

**No new Experiment 004 results are asserted by this design document.**
