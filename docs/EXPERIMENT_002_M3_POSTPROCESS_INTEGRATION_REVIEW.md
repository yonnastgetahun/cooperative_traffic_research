# M3 Archived Development Postprocessing Integration Review

Status: pending GitHub Actions verification. No held-out execution authorized.

This PR reuses the frozen original native vehroute parser, native/FCD timing bridge, R3 exception audit and seed-level R4 scoring function against the three already inspected seed-2101 archives from successful run 40570158400. It requires exact R3 JSON reproduction, matching trip and road-entry denominators and frozen timing MAEs. It records source/output SHA256 manifests. No SUMO or demand generator is called.

Remaining for full production readiness: a reviewed general-seed end-to-end driver, full per-attempt exception and artifact manifests, release authorization and independently verified GitHub environment enforcement. The scientific freeze remains be2e8d27c78c8b6de4891115d6d951edc877ac6e. Reserved seeds 3101–3110 are not authorized.
