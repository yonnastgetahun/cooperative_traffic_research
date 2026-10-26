# Visualization 001 — Three congestion regimes

**Status:** Actual SUMO trajectory capture workflow implemented; rendering and publication pending.
**Purpose:** Publicly explain the simulation scope before the next Experiment 002 predictor-validation milestone.

## Visual treatment
- Format: approximately 14 seconds, 16:9 MP4; one synchronized simulation clock.
- Three side-by-side views of the **same synthetic 10×10 road grid**, based on actual SUMO vehicle FCD x/y positions.
- All scenarios use **1,000 identical origin–destination trips**, seed 1001, identical network and independent/static baseline route selection. The only planned demand variation is each trip's departure time.
- High pressure: 1,000 scheduled departures across 200 seconds (~300/min).
- Moderate: 1,000 across 600 seconds (~100/min).
- Low: 1,000 across 1,200 seconds (~50/min).
- Show the **first 300 simulated seconds** across all three panels (not the full 1,200-second release window); explicitly disclose this in the clip.
- Overlay synchronized clock, current active-vehicle counts, labels and color distinctions.
- Label prominently: **Synthetic SUMO simulations — independent-routing baseline, NOT proof of cooperative routing gains.**

## Source and reproducibility
- New manual workflow: [Experiment 001 — Three-Regime Video Trajectories](../.github/workflows/experiment-001-visualization-trajectories.yml).
- Workflow outputs network geometry, fixed trips, route files, two-second FCD positions, completed trips, input hashes, SUMO version and a per-scenario manifest. Each scenario must complete 1,000 trips and contain vehicle x/y coordinates before rendering.
- Video rendering is subsequent to the capture; the workflow currently generates **data**, not a video. Do not claim a video has been produced until an MP4 is verified.
- This visual is illustrative of the experimental setup. It does not compare cooperative-routing algorithm effects or claim real-road improvements.

## Communications plan
1. Generate a preview video from the three real trajectory artifacts, inspect labeling and synchronized timing on mobile, and obtain sign-off.
2. LinkedIn: provide a research progress update explaining that current experiments show coordination does not automatically improve traffic; we are instrumenting and validating prediction errors next. Attach MP4 as media (Metricool is connected).
3. X: concise curiosity-led progress post with the video and GitHub research link. The verified GitHub publisher currently handles **text only**; video upload must be independently implemented and verified or posted manually from the X app.
4. Do not publish new posts without reviewing the final clip, exact copy and destination settings.

## Next research milestone
Resume the approved [Predictor Validation v0.2](EXPERIMENT_002_PREDICTOR_VALIDATION_PLAN.md): instrument the *actual* congestion-aware decision forecasts, compare with SUMO observations, then validate all 200/600/1200-second regimes using disjoint development and held-out seeds. The video effort does not change that protocol.
