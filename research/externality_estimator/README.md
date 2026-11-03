# E1: Stage 1C prospective queue-aware externality estimator (research prototype)

Implements the [frozen Stage 1B protocol](../../docs/POST_EXP007_E1_EXECUTABLE_DEVELOPMENT_PROTOCOL_V1_2026-11-03.md) as a **no-SUMO, deterministic, source-reviewed toy/standalone network model**. This code has **not** been calibrated, trained, compared with independent SUMO labels, scientifically validated, or used for cooperative policy Test B.

Run: `python -m unittest discover -v research/externality_estimator/tests`

**Model assumptions:** Directed-link FIFO vehicle queues with snapshot storage, global service priors, simple junction conflict classes, 1-second clock and 1,800-second horizon. The model cannot assert realistic signal-phase or lane-specific behavior unless the junction connection and conflict metadata are legitimately available at decision time. Unit fixtures establish physical/accounting invariants, **not** predictive accuracy against real traffic or SUMO.

**No future lookahead:** The prospective prediction modules import no SUMO APIs or offline labels. `label_builder.py` is a separate, offline-only data consumer that the predictor cannot import. Do not feed future FCD, tripinfo, observed timeLoss, or alternate-route outcomes as model input. Missing or in-flight state leads to abstention/explicit rejection rather than invented information.

**Approval boundary:** This Stage 1C implementation and its fixture suite do **not** dispatch the 60-arm development SUMO budget. That requires separately reviewed source/CLI integration and explicit authorization. Future independent estimator validation and Test B also remain separate.
