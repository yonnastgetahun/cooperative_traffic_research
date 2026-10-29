# M3 General-Seed Driver Design Review v0.1

Status: implementation review only, no held-out execution.

The driver now builds the frozen network, demand, chosen-route trace and SUMO observation command sequence for an inspected development scenario. It rejects every reserved seed 3101–3110 before writing files or invoking a subprocess. Eight synthetic tests cover the command sequence, scientific SHA pin and denied execution.

The runner is not yet production complete: native observation parsing, R3 exception policy, R4 paired seed aggregation, full artifact manifests, protected-environment activation and end-to-end development equivalence must be integrated and verified. This pull request does not run SUMO or generate any new demand.

Scientific freeze: be2e8d27c78c8b6de4891115d6d951edc877ac6e. A separate explicit user authorization is required before any reserved seed is generated or evaluated.
