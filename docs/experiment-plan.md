# First simulation: experimental plan (draft)

**Research question:** Can voluntary coordination of human drivers' routes and departure timing improve total network travel time relative to credible independent traffic-aware navigation?

## Initial design
1. Build a small synthetic network in SUMO with multiple viable routes and congestion.
2. Fix origin-destination demand, departure distributions, network geometry, and random seeds across treatments.
3. Baseline: independent traffic-aware dynamic assignment, not naive shortest-distance routing.
4. Treatment: coordinated assignment for opt-in drivers, with participation levels 0%, 5%, 10%, 25%, 50%; vary compliance separately.
5. Evaluate mean and total travel time, delays, worst-off drivers, route diversion, and network throughput.
6. Repeat across demand levels and random seeds; publish assumptions, failures, and uncertainty.

## Validity risks
Unrealistic route-choice assumptions; perfect compliance; inaccurate traffic dynamics; optimizing a metric that disadvantages some drivers; ignoring nonparticipants and local streets.

## Milestone
First deliverable is a reproducible baseline and one treatment, with no claim of real-world impact until validation.
