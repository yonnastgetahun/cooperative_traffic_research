# E1-v2 D1 — Pre-outcome collector-path repair and scientific integrity record

**Date:** November 4, 2026 (GitHub execution November 5 UTC).  
**Reason:** The authorized first main-branch V2-D1 development workflow [41964194079](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/41964194079) completed the frozen 10-seed forecast calculations and failed **before any SUMO scenario arm** due to an orchestration file-path error.

**Observed failure:** \`FileNotFoundError: development/seed-6101/predictions/predictions.json\` from the inherited, frozen Stage 1D \`run_sumo_for_seed\` evidence collector. New V2-D1 instead wrote \`development/seed-6101/predictions.json\` in the seed root, then stored SHA in the original collector's \`prediction_shas\` schema. The error was a storage adapter mismatch, not model abstention, traffic prediction error, or a failed scientific accuracy gate.

**Verified scientific exposure before repair:** Original run's output \`workflow-provenance.json\` reported \`simulator_executions=0\` and \`INCOMPLETE_OR_BLOCKED\`. None of 60 new traffic outcomes existed or were examined. The fresh 6101–6106 and 6111–6114 contexts and 50 prospective predictions were used **only for predecision completeness**, not calibrated against SUMO, and no model updates were performed.

**Exact prospective fix:**
- Write prediction records once to \`seed-XXXX/predictions/predictions.json\`.
- Update the V2-D1 digest and read-only evaluator paths accordingly.
- Preserve the same \`prediction-lock.json\` SHA-256, full fixed ten-seed \`all-prediction-locks.json\` structure, original data generator, frozen v2 and E1-v1 source blobs, seed IDs, route-selection method, signal and vehicle physics, proposed 60-arm budget, 10% MAE development threshold, direction/false-benefit gates and conditional stop rules.
- A repeated no-SUMO prospective preflight must PASS before any new SUMO execution. Any newly opened results before the repaired lock would invalidate the study; this did not occur.

**Scientific disposition:** A documented **pre-outcome infrastructure repair**, not an opportunity to choose a more favorable model or sample. It is scientifically permissible to rerun the whole frozen prospective sequence with original fixed inputs because no simulator outcomes were viewed and no estimator source, parameters, candidate design or acceptance criteria changed.

**Boundaries:** Independent estimator validation (future 6201–6212) and Test B (future 6301–6312) remain unopened. Original Experiment 007 Test A NO-GO and original E1 Stage 1D DEVELOPMENT_NOT_QUALIFIED remain unchanged. No public social communication was authorized.
