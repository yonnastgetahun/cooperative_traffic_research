# M3 held-out runner qualification — engineering review (no evaluation)

**Status: IN PROGRESS — held-out execution remains NO-GO.**

## Established evidence
- Development rehearsal run 40838046735 passed 200s, 600s, 1200s and consolidation on previously inspected seed 2101.
- Frozen scientific commit: `be2e8d27c78c8b6de4891115d6d951edc877ac6e`.
- The development runner deliberately rejects any seed other than 2101. Do not weaken this guard to simulate a production test.

## Production release qualification checklist
1. Inspect the actual evaluation orchestrator and verify its planned 10 seeds × 3 windows, independent inputs, pinned scientific and SUMO versions, and fail-closed defaults. Do not generate any reserved inputs.
2. Verify the evaluation workflow cannot dispatch without separate explicit approval, protected environment enforcement, and independently checked release permissions; screenshots alone are insufficient.
3. Exercise production orchestration with mock scenario IDs and synthetic artifacts, never reserved seeds or scientifically meaningful simulated data. Prove the 30-case manifest, unique case IDs, correct provenance, and no accidental substitution with seed 2101.
4. Inject failures at input retrieval, generation, simulation, postprocessing, aggregation and upload. Confirm every attempted case preserves diagnostics and a missing/failed case makes consolidation fail.
5. Verify artifact hashes, per-case status, run provenance, retention policy, completeness checks, and independent review of the final manifest.
6. Publish a signed-off engineering GO/NO-GO decision supported by run links and machine-readable evidence. Keep the held-out template disabled until separate explicit authorization.

## Decision
**NO-GO** until all six checks have verifiable evidence. No held-out seed 3101–3110 may be generated, simulated, or read under this review.

This document is an engineering qualification plan, not proof that the checks have passed.
