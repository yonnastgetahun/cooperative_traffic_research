# Cooperative Traffic Research — Post-Experiment 007 Marginal-Externality Failure Investigation Plan

**Date:** November 2, 2026  
**Status:** Scientific investigation specification and prospective decision framework. **Not a new experiment, protocol freeze, simulator modification, policy calibration, or simulation authorization.**  
**Scope:** Explain the Experiment 007 Test A externality-estimation failure using original archived evidence first, identify what can and cannot be attributed to network dynamics, and recommend the smallest discriminating follow-up only if needed. Individual fairness stays active; subjective journey quality remains deferred.

## 0. Executive research question and authorization boundary

**Primary question:** Why did the frozen assigned-demand marginal-network-externality estimator frequently mispredict the sign and greatly understate the magnitude of realized changes in the total travel time of other drivers when one vehicle's route was changed?

A rigorous answer must separate four possibilities:
1. **Mathematical, accounting, or software problems** in the modeled marginal cost and its self-versus-other decomposition;
2. **Information/timing mismatch** between prospective assigned-edge/bin quantities and the traffic state vehicles actually encounter;
3. **Realized nonlinear interactions** including insertion, queues, intersections and spillovers;
4. **Simulation or selection artifacts** that could inflate, confound or make these comparisons difficult to generalize.

These are competing, potentially overlapping explanations—not established causes.

**What the current authorization covers:** Produce and publish this complete investigation plan, with explicit archival tasks, hypotheses, evidence requirements, outcome definitions, stop conditions and a conditional proposal for narrowly targeted follow-up measurements. **Do not launch SUMO, select a revised optimizer, alter the frozen Experiment 007 code/protocol, or run Experiment 007 Test B under this plan.** Executing a later instrumentation experiment requires its own prospective freeze and authorization. Reusing frozen archives for read-only scientific investigation does not change historical decisions.

### Prior scientific decision remains immutable

Experiment 007 Test A completed **30/30** SUMO executions: five independent seeds (4101–4105), one 1,000-driver traffic-aware baseline, four prespecified singleton route perturbations and one two-route bundle per seed. All **20** singleton probes had absolute realized externalities of at least 10 network-seconds. Only **8/20 (40%)** matched the predicted externality sign, below the frozen **60%** progression criterion; five had predicted zero despite a materially nonzero realized effect. Predicted externality ranged approximately **−3.24 to +13.50 network-seconds**, versus realized **−3,777 to +4,328**. The two-route bundles exhibited interactions substantially different from simple sums of single-swap outcomes.

**Frozen outcome: Test A NO-GO for this estimator; Test B not executed.** No comparison has demonstrated—or disproved—an efficient, fair cooperative route policy over the stronger independently traffic-aware comparator. This investigation must never quietly reinterpret the 40% result as a pass, erase predicted-zero cases, treat 20 selected probes as 20 independent demand seeds, or claim real-world safety or driver benefits.

Primary references:
- [Experiment 007 Test A final scientific report](EXPERIMENT_007_TEST_A_FINAL_SCIENTIFIC_REPORT.md)
- [Frozen Experiment 007 protocol](EXPERIMENT_007_FROZEN_PROTOCOL_V1.md)
- [Two-test scientific design](EXPERIMENT_007_TWO_TEST_PROSPECTIVE_SCIENTIFIC_DESIGN_NOTE.md)
- [Source of the exact Test A model and probe logic](../experiments/experiment_007/run_v01.py)
- [Permanent singleton results](results/exp007_test_a_probes.csv)
- [Permanent two-route bundle results](results/exp007_test_a_bundles.csv)
- [Original five-seed simulation run](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41380998833)
- [Unmodified original-archive scientific aggregation](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41381425091)

## 1. Investigation objectives: what counts as an answer?

**O1. Establish numerical validity.** Independently reconstruct all 20 Test A predicted/realized total, own and external effects from the archived artifacts and original frozen source, or document any discrepancies as analysis limitations. Prove or refute suspected algebraic/implementation identities and unit differences; do not infer physical mechanisms before validating calculations.

**O2. Establish a descriptive anatomy of realized externalities.** Identify which matched drivers contributed to the aggregate gain/loss, whether changes were concentrated or diffuse, and how much aggregate variation coincided with departure insertion delay, stopped waiting, and remaining movement time. A descriptive decomposition **does not** identify a causal mediator.

**O3. Test what archived spatial and temporal information can distinguish.** Determine whether patterns associate with assigned route overlap, OD groups, departure phase or original-route interactions. Do not label an individual junction or spillback event causal without measured time-resolved traffic dynamics.

**O4. Assess actual model-information adequacy.** State exactly which network state the estimator used, what part of the realized outcome that information could identify, where the two-route bundle violates local additivity, and whether its marginal cost contains a distinct signal about others beyond the treated driver's self-cost.

**O5. Recommend one bounded next scientific action.** Either explain a sufficiently established algorithm/measurement issue using original evidence, or define the smallest instrumented replay that could distinguish leading explanations. Only recommend a new independent estimator-validation study after the mechanism investigation; do not start Test B or repurpose its reserved policy seeds.

**Evidence categories required in every finding:** (i) directly verified from frozen code or raw records, (ii) reproducible descriptive association, (iii) prospective falsifiable explanation, or (iv) unidentified/insufficient data. Report important negative and null diagnostics.

## 2. Data lineage and completeness inventory (read-only first)

The original Test A archives must be treated as the source of record, **not only** the published aggregate CSV:

| Original material | Scientific use | Required verification |
|---|---|---|
| Five original seed-specific ZIP artifacts, exp007-probe-4101 through -4105 | Five independently seeded six-arm paired families | Hashes, provenance and one authoritative baseline per seed |
| Original network.net.xml, trips.xml and demand.json | Fixed graph, OD pairs, scheduled departure and traffic demand | 1,000 unique IDs, exact same network and OD/departure across within-seed arms |
| Six routes.rou.xml files per seed (I, four probe arms, bundle) | Actual assigned route contrast and route-change identity | Exactly one planned route changes in each singleton; bundle has exactly intended two; unchanged route sequences byte-for-byte or structurally identical |
| Six tripinfo.xml files per seed | Arrival, actual depart, duration, insertion delay, waiting, timeLoss per driver | Every ID matched, all completed, clock arithmetic and published network totals reproduced |
| SUMO statistics.xml, collisions.xml, simulator/stage logs | Completion and recorded exception checks; simulation settings | No missing or silently altered settings; report what event fields actually contain |
| Original probe-results.json and final Test A aggregate JSON | Frozen prediction/realization contrast and Test A decision | Recompute from raw records independently, maintain all selected probes |
| Original assigned-demand estimator source and pinned SUMO image | Model calculation and simulation dynamics | Record exact blob/source commit and container digest, never change historical baseline |

**Availability/retention:** At the time of planning, the original five-seed artifacts and aggregate evaluation remain accessible in GitHub Actions (the original archived artifacts show expiry on **December 2, 2026 UTC**). Prioritize preserving hashes, raw record inventories and permanent numerical derivatives before expiration. If raw data cannot be obtained for all five seeds, label the coverage gap explicitly; do not quietly substitute new simulations for missing original archives.

**Observed sample archive check (seed 4101, not a claim about all five):** The original ZIP includes network, demand, assigned routes, tripinfo, statistics, collision files and logs for each arm. It does **not** contain FCD vehicle trajectories, interval-specific lane/edge detector output or per-edge vehicle exit timestamps. Inventory all other ZIPs before assuming they share those absences. Original tripinfo therefore supports vehicle-level differences, but it cannot by itself pinpoint a physical queue at an exact junction and time.

### Frozen clocks and quantities

For a matched driver i in arm X:
- **Scheduled-to-arrival elapsed:** T_i(X) = actual_arrival_i(X) − scheduled_departure_i, in seconds.
- **Individual change:** d_i = T_i(probe) − T_i(I).
- **Total network change:** d_all = sum of d_i across all 1,000 identities, in **network-seconds**.
- **Self change:** d_self = d_target.
- **Externality:** d_external = d_all − d_self = sum over the **other 999** matched identities.
- **Sign:** Negative denotes benefit/savings, positive denotes additional realized elapsed time.

SUMO's recorded duration and departure delay must be reconciled with **actual arrival minus scheduled departure** before aggregating. Report SUMO waitingTime as a component of in-vehicle duration and timeLoss as a separate diagnostic, never as independent additional cost. No early-arrival schedule objective or subjective journey quality is introduced here.

## 3. Highest-priority forensic hypothesis: is the model's externality genuinely distinct?

The frozen run_v01.py constructs planned occupancy in 30-second edge-time bins using an advance-demand clock that combines nominal free-flow timing and the previously frozen cumulative correction. For a bin with assigned count q it approximates aggregate edge cost as **free-flow_edge_time × [q + q²/capacity_proxy]**, where capacity_proxy uses edge length and lane count. It estimates the cost difference between assignments, and then labels **predicted_externality = predicted_total_delta − predicted_self_delta**. This is an assigned-demand cost proxy, not a calibrated equation for physical SUMO queue formation.

**Specific code-level diagnostic priority:** In the published singleton results, predicted **total** delta appears to equal approximately **2 × predicted self** delta, with predicted external delta approximately equal to predicted self delta, for the listed probes. In seed 4101's raw JSON the identity also holds to numerical precision, including the zero predictions. The investigation must test whether this follows analytically from:
- identical nominal/free-flow cost of permitted alternative routes on the synthetic grid;
- a quadratic assigned-count objective and the self-cost calculation on the same frozen before/after occupancy maps;
- inclusion of the ego vehicle in both old and new occupancy;
- missing route-time or per-turn interaction terms;
- a particular unit/sign/accounting implementation convention.

**Required computation:** For all twenty archived probes independently calculate predicted total, predicted self, predicted external, residual [pred_total − 2×pred_self], and residual [pred_external − pred_self]; identify any departures from exact numerical identity. Derive the conditions under which the identity must occur and produce at least two hand-checked small synthetic route/bucket examples, one with different nominal path lengths and one with identical nominal path lengths but different edge bins. Use standalone **analytical/unit fixtures only** for this derivation, not fresh SUMO data. Distinguish a model's weak structural expressiveness from a source-code defect: an algebraic identity may be an *intended implication of the proxy* rather than a programming bug.

**Discriminating question:** Does the model independently estimate effects on other vehicles, or does its apparent externality signal mainly mirror own-route cost through a symmetric assigned-bin penalty? A negative answer would explain weak **signal content** without identifying the full origin of large realized traffic effects.

## 4. Competing explanations and discriminating evidence

| ID | Candidate explanation | Positive evidence sought | Counterevidence / limitation |
|---|---|---|---|
| H1 — Structural cost-proxy mismatch | Predicted externality mechanically follows self-cost, sign insensitive to junction or queue exposure; zeros arise from equal proxy costs despite distinct feasible roads | If a validated distinct external term predicts original contrasts with frozen information, pure structural insufficiency is weakened; avoid in-sample rescue |
| H2 — Edge-entry clock and time-bin mismatch | Archived prospective bin entries split from plausible observed road-entry timing; notable assignment interactions near 30s boundaries | Original Test A archives may lack observed edge-entry times; must distinguish unavailable from disproven |
| H3 — Junction capacity, queue formation, blocking/spillback | New targeted edge-time records show changed arrival/platoon at a bottleneck preceding realized queue/waiting changes on otherwise unchanged routes | Aggregate waiting or quadrant association alone is not proof of a particular bottleneck |
| H4 — Departure insertion and aggregate metric mismatch | Realized external difference materially changes when separated into completed duration and departure/insertion delay; unexpected missing/double counts | If accounting reconstructs original totals precisely, numerical accounting errors are disfavored; insertion can remain a physical mechanism |
| H5 — Nonlinear interactions/nonadditivity | Two-swap joint effect differs from sum of individually measured swap effects; concentration around shared edge-time constraints | Original bundle effects establish interaction, not where/why it occurs or that every network scenario behaves so |
| H6 — Simulation random-stream or initialization sensitivity | Repeat of **identical assigned input** under original version and seed differs; identical input with instrumentation changes tripinfo | SUMO is designed to be deterministic for fixed settings/seed in typical configurations; changed routes can still yield dramatically different dynamic behavior without an integrity flaw |
| H7 — Probe selection/generalizability | Extremes/near-zero/median chosen based on model ranking create unstable sign fraction or exaggerated variation in 20 selected examples | Does not reverse frozen Test A NO-GO, and cannot establish population prediction accuracy without a separate cohort |
| H8 — Heterogeneity of spatial/temporal exposure | Matched high-harm vehicles cluster in departure, OD or baseline-path cohorts, with path overlap and waiting correlating to shifts | Retrospective strata are multiple, dependent and exploratory; no causal junction attribution |

H1, H4 and basic integrity of H6 can be investigated from original records and frozen code before any new traffic execution. H2 and H3 may demand time-resolved traces. All hypotheses are tentative until independently audited.

## 5. Ordered, bounded investigation workflow

### Phase P0 — Preserve and audit the frozen evidence (mandatory, no simulation)

1. Inventory all five raw ZIPs, every arm and expected file; produce SHA-256 archive/file manifests and a coverage table for seed × arm × measurement.
2. Read only the original frozen source and archive data. Rebuild the five groups of 1,000 scheduled IDs, baseline routes and probe/bundle routing changes. Verify network, demand, simulator seeds, vehicle count and 100% completion.
3. Reproduce each of the 20 original predicted/realized total/self/external numbers and five bundle interactions; re-evaluate the frozen 8/20 gate **without changing criteria**.
4. Reconcile each per-driver tripinfo clock (scheduled departure, actual departure, duration, arrival); separately compute insertion delay and check that the total is arithmetically consistent.
5. For any inconsistency, publish the precise discrepancy and associated source paths. Do not repair original published outcomes silently; distinguish an audit correction from an originally frozen result.

**P0 deliverables:** evidence-inventory table; SHA manifest; audit report listing exact matching/censoring/route-control checks; original-number reproduction sheet. Stop further causal interpretation if data identity or clock integrity is unresolved.

### Phase P1 — Model-algebra and forecast-information audit (no SUMO)

1. Trace source functions for time-bucket assignment, edge footprint, nominal route alternatives, self-cost, total-cost and delta decomposition, including update order and all calibrated offsets.
2. Recompute every predicted marginal effect directly from original inputs and source definitions without reading future realized tripinfo. Inspect predicted zeros and sign reversals individually; record exact old/new routes, forecast footprint changes, candidate edge-time overlap, capacity proxy and estimated marginal terms.
3. Derive and test the apparent predicted-total ≈ 2×predicted-self identity, including whether identical nominal travel time explains it.
4. Measure which component (nominal path time, time-bin assigned overlap, predicted network load, individual predicted cost) actually differentiates route candidates. Document where externality could change **without** a self-cost change under the current model.
5. Audit code paths for zero cancellation, identical edge-bin footprints despite different routes, deterministic candidate selection, connected routes, exact snapshot state, and use or non-use of observed future values.

**P1 deliverables:** model-equation derivation and unit-sensitive formula audit; 20-probe input/output trace; explicit model limitations and potential defects, each labeled verified vs hypothetical. *Do not refit weights using the original 20 evaluation outcomes and claim independent validation.*

### Phase P2 — Reconstruct the realized individual and collective effects (no SUMO)

For each baseline/singleton pair:
- Calculate the target driver's own difference and the distribution of all **999** other drivers' differences; show net total as the algebraic sum of benefits and harms, not a single opaque aggregate.
- Separately show **waitingTime**, departure insertion delay, historical completed-trip duration, and remainder of duration after recorded waiting; do not assume these components identify physical mechanisms.
- Report helped/harmed/unchanged counts among other drivers, magnitude of top 1/5/10 contributors, positive/negative sums and concentration of aggregate effects. A large aggregate change may reflect a broad small shift or a few extreme drivers; distinguish them.
- Compare **identical road-edge sequence** drivers, nonparticipants and nominally unchanged assignments; identify whether large differences on unaffected routes are consistent with spillovers, while recognizing that each counterfactual traffic network differs dynamically.
- Stratify descriptively by scheduled departure order and sufficiently populated origin/destination groups; report multiple-comparison caveats and avoid cherry-picked causal claims.
- For bundle arms compute observed bundle − isolated-swap-sum for total cost, self/others where meaningful, waiting and insertion. Do not assume interaction can be attributed exclusively to a physical queue.

**P2 deliverables:** per-seed driver-paired diagnostic dataset, distribution plots, cost-component reconciliation and a five-seed bundle comparison, each labeled exploratory. Retain **seed** as independent unit: 20 selected probes sharing five baselines are not 20 independent demand replications.

### Phase P3 — Spatial/temporal evidence sufficiency and counterfactual validity (no SUMO)

1. Inventory whether original archives have any edge/lane time bins, actual route exit timestamps, FCD, detector data or equivalent vehicle-time traces. **If absent, say so**; do not claim to have localized queues from tripinfo or static route strings.
2. With available origin/destination IDs and assigned edges only, compare path overlap, turns, route distance/free-flow time, exposure to the target's old/new routes and time-of-day cohorts. Interpret these as **hypothesis-generating structural associations**.
3. Confirm the original SUMO seed, options, vehicle type distribution, route insertion ordering, netgenerate outputs and simulator version are held comparable. Note that equal random seeds support repeatability, **not identical traffic trajectories across changed-route scenarios**.
4. Check alternative cost metrics/normalizations and whether network-seconds versus per-driver seconds were ever confused. Normalize externality by 999 solely as a labeled descriptive sensitivity, not as a replacement for the frozen objective.
5. Produce an evidence map: which hypotheses can be ruled out, supported descriptively, or are **not identifiable** without actual time-resolved road observations.

**P3 deliverable:** a causal-evidence sufficiency matrix, explicitly naming any gap requiring fresh instrumentation. There is no obligation to start a new simulation if archived evidence already supports a bounded scientific conclusion.

## 6. Conditional smallest follow-up: trace a few frozen route changes, not a new routing policy

**Not authorized for execution by this plan.** If P0–P3 cannot distinguish the dominant hypotheses because the original ZIPs lack road-time dynamics, draft **one prospective, instrumented replay protocol** rather than launching another forecast calibration cycle or full Test B.

**Proposed exploratory minimum (six instrumented SUMO runs, only if needed):**
- Original **seed 4101**, unchanged I baseline and predicted-zero **probe2 (veh0000)**, where the archived frozen probe reported a material realized externality despite zero predicted effect.
- Original **seed 4102**, unchanged I baseline, **probe0 (veh0582)** with predicted-versus-realized sign reversal, **probe1 (veh0158)**, and their original **two-route bundle**, allowing the joint-versus-single interaction to be located in time.
- This selects conspicuous examples **after seeing Test A outcomes**: label the replay **exploratory mechanism investigation**, not independent confirmatory validation or an unbiased externality estimator test. The replay must retain the original frozen routes, network, demand, seed, SUMO version and time settings; no rerouting or predictor changes.

**Proposed measurements:** original tripinfo and statistics plus 1-second or otherwise prespecified FCD vehicle trajectory records (edge/lane, position, speed and time), route edge-exit times where the pinned SUMO version supports them, and fixed-window lane/edge flow, speed, occupancy and waiting summaries through a SUMO additional-file detector configuration. Explicitly distinguish sampled edge occupancy from actual assignment-count proxy; preserve internal junction activity if relevant. Verify in the pinned image that any chosen output option is supported and does not change the model dynamics.

**Required instrumentation-equivalence gate:** Before interpreting traces, compare each replay's original-standard outputs with the corresponding archived tripinfo and route fingerprints; if adding instrumentation changes realized trip outcomes outside an explicitly justified numerical tolerance, **do not interpret the traced dynamics as the historical counterfactual**. Investigate reproducibility first, without modifying frozen scientific outcomes. A baseline repeat with unchanged routes and seed provides a useful check.

**Falsifiable contrasts within the replay:** (a) does the predicted-zero swap alter *actual* edge-time arrival/flow where the proxy's predicted bins are equal? (b) do stopped/queued vehicle-time clusters grow **after** a specific changed-route arrival or turn at a constrained junction? (c) do observed effects primarily arise from insertion delay versus internal traffic waiting? (d) do observed bundle interactions emerge at a shared time/place that is not present in either singleton? (e) can identical-input reproduction distinguish environmental nondeterminism from deterministic yet nonlinear network response?

**Decision boundary:** A targeted trace showing a queue expansion correlated with a changed route is **supporting mechanism evidence**, not necessarily proof that that junction alone caused the whole-network effect. A causal bottleneck claim requires temporally ordered evidence and an appropriately isolated control, potentially a *separately approved* physical-capacity or traffic-control intervention. Do not increase from six runs to an open-ended grid of scenarios without a new scientific protocol.

## 7. Prespecified interpretation and stopping rules for this investigation

This is a **retrospective, mechanism-oriented study**, not a new efficacy experiment. Do not create spurious hypothesis-test p-values by pooling selected drivers or 20 conditional probes as independent seed replications. The primary output is a **correctly characterized explanation and uncertainty**, not a requirement to produce a successful model.

- **Measurement/software defect established:** A reproducible arithmetic, route assignment, or clock discrepancy is isolated from original input/output records with source-level proof. Report whether original Test A effect estimates must be labeled *measurement-invalid*, while retaining the historical result and documenting any correction separately; do not automatically call the estimator accurate.
- **Structural-proxy inadequacy established:** Original code and self/total terms reveal insufficient distinct externality signal or limiting identities; numerical outcomes demonstrate lack of predictive usefulness on this selected cohort. Mark the causal physical drivers of realized traffic response unresolved unless corroborated.
- **Traffic-interaction pattern descriptively supported:** Driver-level waiting/insertion and source/route associations consistently account for observed changes; label network interaction plausible, but specific junction causality unknown without localized traces.
- **Causal bottleneck mechanism supported by new targeted observations:** Requires approved instrumented replay, measurement equivalence and time-resolved observations consistent with the stated counterfactual. Stronger causal attribution requires a subsequent discriminating intervention.
- **Unresolved:** Original archives lack necessary information or tests yield conflicting explanations. Publish clear limitations and name the smallest remaining evidence requirement. **Unresolved is an acceptable scientific result.**

**Never:** change Test A's 60% threshold post hoc; ignore the five predicted zeros; choose new seeds to rescue the result; execute untested Test B; claim that future autonomous vehicles guarantee cooperation; interpret a mathematical objective as a validated collective benefit; claim a real-world voluntary-consent threshold; or introduce subjective QoE as an active endpoint.

## 8. Deliverables, repository organization and completion criteria

The investigation should produce **one consolidated scientific investigation report** with small machine-readable supporting artifacts, rather than another broad engineering-readiness program:

1. **Integrity and provenance:** archive inventory, SHA256 file hashes and seed/arm/vehicle completeness table; known environment and output gaps.
2. **Frozen-estimator forensic results:** independently reconstructed 20 predicted externalities, source-equation proof, sign/zero behavior and candidate-route/bin diagnostics; expected self-vs-external relationship.
3. **Realized impact decomposition:** all matched per-driver elapsed, waiting, insertion and remaining time components; nonparticipant and unchanged-route effects; five original bundle interactions.
4. **Hypothesis/evidence matrix:** what is established, supported descriptively, disfavored, or unidentifiable. Explicitly assess whether a more physically grounded estimator is warranted and what information it would need.
5. **Single next-decision recommendation:** archive-only scientific conclusion **or** a separately frozen six-run trace proposal, with a clear reason each original archived measure was insufficient.
6. **Published final report and permanent derived CSV/JSON** committed to GitHub, linked to original frozen code, protocol, original Test A archives and scientific reporting. Preserve the Experiment 007 test decision unchanged.

**Definition of investigation completion:** Every P0–P3 analysis feasible with preserved originals is evaluated once, with reproducible code/methodology and a coherent scientific interpretation, even if it ends **INCONCLUSIVE**. Do not require new simulations merely to mark the investigation complete.

**Publication standard:** Significant scientific conclusions may later be communicated with a visual-first LinkedIn carousel (typically 5–7 PDF pages) and four readable X images using a common reader-friendly GitHub landing page. **Do not publish** to either social platform until actual assets and captions have been reviewed and explicitly approved. Use verified numbers, note experimental limitations and avoid labeling exploratory causal stories as established mechanisms.

## 9. External documentation for measurement design (not evidence for this experiment)

- [SUMO TripInfo output](https://sumo.dlr.de/docs/Simulation/Output/TripInfo.html) documents actual departure, intended departure, arrival, departDelay, duration and waitingTime.
- [SUMO FCD output](https://sumo.dlr.de/docs/Simulation/Output/FCDOutput.html) documents per-vehicle time-position, lane, speed and optional additional attributes.
- [SUMO edge/lane-based traffic measures](https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html) defines interval occupancy, flow, speed and waiting fields, distinct from static assigned-demand counts.
- [SUMO simulation options](https://sumo.dlr.de/docs/sumo.html) includes vehicle-route exit-time and diagnostic outputs, subject to pinned-version verification.
- [SUMO randomness and reproducibility](https://sumo.dlr.de/docs/Simulation/Randomness.html) describes seeded stochastic dynamics and potential exceptions to bitwise reproduction.

These sources show *potential observability* in SUMO. **They do not imply the original Experiment 007 archives already collected those measurements.**

---

**Plan decision:** Start with P0–P3 archival and source-code investigations, preserving the original Experiment 007 Test A NO-GO and Test B non-execution. Consider the six-run instrumented replay **only after an evidence insufficiency decision and separate authorization**. The goal is understanding, not automatically rescuing a particular routing algorithm.
