# M3 Native Observation Integration Review

Status: offline integration only; not a complete executable held-out runner.

This change verifies completeness and provenance of native SUMO vehicle events, FCD, native edge data, frozen R3 exception reports and R4 seed-level timing cohorts. Nine synthetic tests exercise missing observations, teleports, mismatched joins, scientific-source drift and reserved-seed rejection. No new SUMO simulations or demand generation are performed.

Remaining: connect and qualify the actual end-to-end postprocessing invocation with existing development data; verify general-seed production execution, complete manifests and all 30 scenario failure dispositions, and confirm live environment protections. The frozen science remains at be2e8d27c78c8b6de4891115d6d951edc877ac6e. Held-out evaluation is not authorized.
