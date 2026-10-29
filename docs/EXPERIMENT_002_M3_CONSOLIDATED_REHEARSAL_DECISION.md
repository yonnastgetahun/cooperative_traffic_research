# M3 consolidated end-to-end development rehearsal

**Status: verification pending. No held-out execution authorized.**

This pull request runs the *existing* complete development qualification sequence (frozen 10×10 network, 1,000 demand trips, original predictor and route audit, live search-input capture, SUMO native observations, R3 exceptions, and seed-level timing metrics) for previously inspected seed **2101**, separately in the 200-, 600-, and 1,200-second regimes.

Unlike the earlier component-only tests, the workflow independently repeats frozen native event parsing, timing bridge, R3 exception audit and scoring **on the freshly generated development outputs** in the same run. The existing cross-regime aggregator compares all three against the archived development references. Each scenario archives its results and reprocessing evidence even if a stage fails. The consolidated job requires all three to pass.

**GO for implementation readiness** only if every fresh scenario passes the frozen-source and route/trip invariants, native observation/exception gates, exact R3 reproduction, R4 seed timing equivalence, cross-regime integrity and evidence retention. **NO-GO** on any mismatch, missing source, incomplete regime or unclassified exception.

This is a **development readiness** decision, not authorization to execute held-out seeds 3101–3110. The workflow has no held-out seed inputs, uses only seed 2101 and a pinned SUMO image, and does not change the scientific protocol at commit `be2e8d27c78c8b6de4891115d6d951edc877ac6e`.

If the workflow succeeds, the remaining distinct operational question is whether the production evaluation runner and release controls are sufficiently implemented and independently verified. A passing development rehearsal alone cannot certify a runnable held-out evaluation workflow.
