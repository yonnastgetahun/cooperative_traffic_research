# Deferred Research Notes — Quality of Journey Experience versus Speed

**Deferred by research-sequencing decision, November 1, 2026.** Preserve these exploratory ideas, but they are **not active project objectives, hypotheses, primary endpoints, experiment-selection criteria, instrument requirements, or current implementation work**.

**Current sequence:** (1) establish whether substantively different coordination mechanisms improve network-wide traffic flow against credible independent baselines; (2) simultaneously preserve individual fairness, measurable burden, consent/participation assumptions and distributional effects; (3) **later**, once collective coordination mechanisms have clearer evidence, study comfort, predictability, perceived calmness and quality of journey experience.

This file retains the earlier proposed experience-measurement framework **as historical exploratory material** without endorsing its earlier instruction to "introduce now." The original text follows for traceability.

---

## Original October 31 exploratory discussion (superseded sequencing)

**Historical exploratory research dimension, discussed October 31 (now deferred):** Evaluate whether the transportation system can provide a **calmer and more dependable journey** even when a trip is not maximally fast. This may be central, rather than secondary, to the future-autonomous-coordination thought experiment.

### A proposed multidimensional outcome framework (not a calibrated utility score)

| Dimension | Candidate measure | What current experiments support | What they do **not** support |
|---|---|---|---|
| **Time and access** | Mean and total end-to-end journey time, person-hours, throughput, missed deadlines | Tripinfo duration, waiting, completion in fixed-departure SUMO | Predeparture sacrifice, real job/family schedule value |
| **Reliability / predictability** | Repeated *same OD and time-context* p90/p95, buffer/planning time, lateness frequency, forecast uncertainty | Cross-seed aggregate trip duration comparisons | True day-to-day reliability with different OD samples/real incidents |
| **Flow smoothness** | Stops per vehicle, time stopped, speed variance, acceleration/jerk exposure, stop-and-go episodes | SUMO `waitingTime` aggregate as **limited stopped-time proxy** | Vehicle trajectory smoothness or comfort from trip duration alone |
| **Perceived comfort and stress** | Traveler-reported calmness, workload, discomfort, perceived predictability or control | **None measured** | Subjective QoE cannot be inferred from queue duration alone |
| **Agency, consent, fairness** | Optional acceptance/rejection, schedule-constraint violations, realized harm distribution, reciprocal benefits over repeated travel | Matched-driver simulation harm comparisons | Actual preferences, compensation adequacy or willingness to comply |
| **Environment and safety** | Fuel/energy, emissions, collisions and validated conflict/near-miss measures | Some structured SUMO exception statistics, not full safety case | Real-world safety, vehicle fuel economy, exposure risks |

**Measurement interpretation:** [FHWA reliability guidance](https://ops.fhwa.dot.gov/publications/tt_reliability/ttr_report.htm) treats predictability and high-delay tails as different from average travel time. [Research on acceleration and jerk vs passenger comfort](https://www.sciencedirect.com/science/article/pii/S0003687022002046) demonstrates why motion profiles matter, but our SUMO archive's travel-time/waiting outcomes do **not** equal measured comfort. Subjective quality requires human reports or validated human-grounded models; operational proxies are not enough.

**Hypothetical Pareto tradeoff, NOT a project result:** a route that takes 90 seconds longer but avoids repeated stoppages and greatly reduces arrival-time uncertainty *might* be preferred by some travelers and rejected by others. We should not impose a universal tradeoff coefficient without preference evidence. Initial research should **report a Pareto frontier** across travel time, reliability, smoothness, and individual harm rather than silently combine them into a single arbitrary 'quality score'.

**Important constraint for future temporal studies:** if a vehicle waits at home before departure, door-to-door generalized elapsed/schedule time **must include that imposed waiting**, even if the SUMO driving segment looks smoother or shorter. Distinguish *time available for other activities* from *unwanted waiting* only when that distinction is specified and validated.


