# G3 R1–R2 Development-Only Verification — Execution Scope

**Status:** Approved October 26, 2026. **No M3 freeze or held-out evaluation authorized.**

**Fixed cases:** development seed **2101**, windows **200, 600 and 1,200 seconds** (three scenarios). Reuse the frozen road network, OD demand, route file, original forecasts and FCD from [M2 run 40446073958](https://github.com/yonnastgetahun/cooperative_traffic_research/actions/runs/40446073958). SUMO container is pinned by SHA256 digest as specified in the G3 sufficiency review. No new seed, algorithm adjustment or sampling-rate change.

**R1 — Timing reference bridge:** Preserve the original published FCD-first-external-front road-entry error; independently infer native external-road entry from the preceding ordered native link exit, at SUMO's original 1-second solver resolution. Match by **vehicle ID, ordered route index and edge**, including repeated roads. Record every native/FCD entry shift and native-referenced time-aware and free-flow error. Failure to join any planned edge is an instrumentation failure, not a reason to drop it silently.

**R2 — Search-input provenance:** Capture actual preassignment occupancy-counter reads for every explored routing search edge, including unchosen candidates, and every assignment update. Verify against independent event-stream reconstruction and original archived route/audit byte identity. These counts denote planned assignments, *not* measured physical road occupancy.

**Invariance checks:** All 1,000 trip outcomes in each scenario match original archives; unchanged route/audit, network/demand hashes, immutable SUMO digest and the original fixed-step native/FCD source semantics. Summarize at scenario level, not by pretending thousands of vehicle-edge visits are independent evaluation replicates.

**Acceptance:** All three scenario jobs, fixture gate and aggregate job pass; every native and FCD planned road visit is accounted for; all route/cost counters and tripinfo match originals. Fail closed for missing fields, divergent routing or output contamination.

**Scientific boundaries:** This is measurement/provenance verification, not calibration, not causal junction-delay research, not a claim of cooperative-routing benefit, and **not** a predictor-accuracy pass. Reserved seeds **3101–3110** remain untouched. Only a subsequent reviewed and explicitly approved M3 freeze can authorize held-out evaluation.
