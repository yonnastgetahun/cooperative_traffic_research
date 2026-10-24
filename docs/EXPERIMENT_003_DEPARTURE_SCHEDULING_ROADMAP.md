# Research extension — Cooperative departure scheduling (proposed Experiment 003)

Status: formally added to roadmap; not implemented or validated.

Hypothesis: Coordinating voluntary departure shifts along with routes may reduce total door-to-door time and congestion compared with independent routing.

Four arms: (A) independent routes and fixed departures; (B) cooperative routes and fixed departures; (C) independent routes with coordinated departure shifts; (D) coordinated routes and departure shifts.

Design: same network, OD pairs, demand, and paired seeds. Evaluate maximum allowed departure shifts of 0, 30, 60, 120 seconds, with opt-in eligibility and hard latest-arrival constraints. Count predeparture waiting in generalized journey time, not just SUMO driving time. Report mean and p95 total time, in-vehicle duration, waiting, completion, delay distribution, fairness, and violations. No unsafe speeding or invalid movements; simulated safety is not evidence of real-world safety.

Sequencing: complete Experiment 002 bottleneck and route-level diagnostics before implementing scheduling. Experiment 001's broader departure windows are demand calibration, NOT evidence that individually optimized scheduling improves outcomes.
