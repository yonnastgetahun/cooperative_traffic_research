# G3 — Targeted Event Instrumentation: durable development evidence

**Status:** J0–J3 instrumentation and targeted replay completed; **G3 remains open** until reviewed. **No held-out evaluation or model tuning**.

## Evidence from the archived original development scenarios

- J1: 1,000 trips; 16,705 ordered SUMO movement events; 8,338 internal-junction events.
- J2: 677,507 **actual search-time occupancy counter reads** and 8,367 assignment updates, independently replay-verified. Routes and audit identical to archive.
- J3: native case veh0213 on upstream C6C7, native road exit at 57.0 simulated seconds; internal links :C7_11, :C7_19; native internal exit steps [98.0, 99.0].

## Source workflows
- [J1 native exit events](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40452285124)
- [J2 true search counter reads](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40452726452)
- [J3 preselected junction case](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40453154885)

The large compressed search-lookup event streams remain downloadable from GitHub Actions artifacts for a limited period and can be regenerated using the versioned workflows and original development inputs.

### Scientific boundaries
SUMO exit times have discrete-step semantics, not continuous crossing precision. Internal-link dwell is not necessarily *caused* by the junction. The original search counter denotes prior planned route assignments, not physical occupancy. Recording all its reads does not imply predictor calibration or a cooperative-routing improvement. Evaluation seeds 3101–3110 remain unused.
